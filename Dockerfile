FROM python:3.9.0b4-alpine
MAINTAINER Ihsan Kursad Unal

ENV PYTHONUNBUFERRED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN apk update\
    && apk add --virtual build-deps gcc python3-dev musl-dev\
    && apk add --no-cache mariadb-dev\
    && apk add jpeg-dev zlib-dev libjpeg
RUN pip install Pillow
RUN pip install mysqlclient

RUN apk del build-deps

RUN adduser -D user
USER user