FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1
ARG DJANGO_PORT

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/
EXPOSE ${DJANGO_PORT}
RUN pip install -r requirements.txt
COPY . /backend/
