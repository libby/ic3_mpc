FROM python:2-stretch

ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y vim

RUN apt update && apt -y install libgmp-dev

RUN mkdir -p /usr/src/mpc
WORKDIR /usr/src/mpc

RUN pip install --upgrade pip
RUN pip install git+https://github.com/sbellem/viff.git@setup

COPY . /usr/src/mpc

RUN pip install --no-cache-dir -e .[dev]
