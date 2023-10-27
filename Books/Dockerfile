FROM python:3.10

ENV PYTHONDONTWRITEDBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /proj

RUN pip install --upgrade pip

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .
