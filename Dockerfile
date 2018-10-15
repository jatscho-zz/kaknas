FROM python:3.7-alpine

MAINTAINER Zach Yam "zach.yam@cognite.com"

RUN apk add curl git unzip bash openssh

#Install uWSGI server
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        libc-dev \
        linux-headers; \
    pip install uwsgi; \
    apk del .build-deps;

COPY kaknas /app/kaknas

COPY requirements.txt /app/

COPY entrypoint.sh /app/

WORKDIR /app

#Install requirements
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
