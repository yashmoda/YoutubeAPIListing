from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from search_video.models import VideoData


@require_http_methods(["GET"])
def get_list(request):
    try:
        search_query = request.GET.get("query", "").strip()
        page = int(request.GET.get("page", 1))
        if len(search_query) == 0:
            video_list = VideoData.objects.all()
        else:
            search_query = search_query.replace(" ", " & ")
            query = SearchQuery(search_query)
            vector = SearchVector('title') + SearchVector('description')
            video_list = VideoData.objects.annotate(search=vector).filter(search=query)
        paginator = Paginator(video_list, 20)
        videos = paginator.page(page)
        return render(request, 'home.html', {"videos": videos})
    except Exception as e:
        response_json = {"Message": "An Error Occurred. Please try again later!!", "Error": str(e)}
        return JsonResponse(response_json)
