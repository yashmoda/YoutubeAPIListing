FROM python:3.6

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools

ARG PROJECT=DjangoProject
ARG PROJECT_DIR=YoutubeAPIListing

RUN mkdir -p $PROJECT_DIR

WORKDIR $PROJECT_DIR

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt


EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
