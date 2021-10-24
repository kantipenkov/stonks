# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
# RUN export DJANGO_SETTINGS_MODULE=stonks.settings.local
# RUN export DJANGO_SECRET_KEY=dummy-secret-key
COPY . /code/