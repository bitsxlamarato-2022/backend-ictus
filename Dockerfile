FROM python:3.10

RUN mkdir /app
WORKDIR app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY
