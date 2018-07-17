FROM python:2-stretch

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y vim

RUN apt update && apt -y install libgmp-dev

RUN mkdir -p /usr/src/viff
WORKDIR /usr/src/viff

RUN pip install --upgrade pip

COPY . /usr/src/viff

RUN pip install --no-cache-dir -e .
