import random
from datetime import datetime, timedelta

import redis
import requests
from celery.schedules import crontab
from celery.task import periodic_task
from django.apps import apps

r = redis.Redis(host="rd01", port=6379)


@periodic_task(run_every=(crontab(minute='*/3')), name="load_video_info", ignore_result=True)
def add_video_info(url=""):
    print("Starting task at: ")
    print(datetime.now())
    search_keyword = "Cryptocurrency"
    api_model = apps.get_model(app_label='search_video', model_name='APIKeys')
    api_key_count = api_model.objects.count()
    # print(api_key_count)
    random_key = random.randint(1, api_key_count)
    # print("--------Random Key--------------")
    # print(random_key)
    api_key = api_model.objects.get(id=random_key).api_key
    if not r.exists("published_after"):
        published_after = datetime.now() + timedelta(hours=-2)
        published_after = str(published_after.strftime('%Y-%m-%dT%H:%M:%SZ'))
        r.set("published_after", published_after).decode("utf-8")
    else:
        published_after = r.get("published_after")
    # print("--------Published After--------------")
    # print(type(published_after))
    if url == "":
        url = "https://www.googleapis.com/youtube/v3/search?q={}&type=video&key={}&part=snippet&publishedAfter={}&maxResults=50".format(
            search_keyword, api_key, published_after)
    # print("--------URL--------")
    # print(url)
    response = requests.get(url)
    # print("--------Response--------------")
    # print(response)
    r.set("published_after", str(datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')))
    if response.status_code == 200:
        video_model = apps.get_model(app_label="search_video", model_name="VideoData")
        video_list = response.json()["items"]
        # print(len(video_list))
        for video in video_list:
            video_id = video["id"]["videoId"]
            published_at = video["snippet"]["publishedAt"]
            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]
            publisher = video["snippet"]["channelTitle"]
            if video_model.objects.filter(video_id=video_id).count() == 0:
                video_data_obj = video_model(video_id=video_id, title=title, description=description,
                                             publisher=publisher,
                                             published_at=published_at, thumbnail_url=thumbnail_url)
                video_data_obj.save()
            # print("---------Video ID------------")
            # print(video_data_obj.video_id)
        if "nextPageToken" in response.json():
            url = url + "&pageToken={}".format(str(response.json()["nextPageToken"]))
            add_video_info(url)
        else:
            return "The videos have been loaded!"
