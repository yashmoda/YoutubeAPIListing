# YoutubeAPIListing

This project would call the Youtube API in the background asynchronously with the help of Celery. This would get the videos related to a particular search query (i.e. "Stocks" for the time being) and load some details returned by it into the PostgreSQL database.

There is a GET API which returns the list of all videos that are available in the database if no search query is specified and if a search query is specified then it returns all the videos corresponding to that particular search query in a paginated format which is sorted in descending order of published datetime. The project has been dockerised so it can be installed and run anywhere without any issues.

To run the project you need to simply follow the below mentioned steps:
1. Clone the repository into your machine.
2. Execute the following command to run the docker container:
   ```docker-compose up --build```
3. Navigate to this URL to see the videos that are currently there in the database: http://127.0.0.1:8000/get/
4. You can use the search text box at the top of the page to search for the desired videos
5. You can also use select the different pages from the bottom to navigate through different pages.
