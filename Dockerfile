FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend
COPY requirements.txt /backend/
EXPOSE 8000
RUN pip install -r requirements.txt
COPY . /backend/
