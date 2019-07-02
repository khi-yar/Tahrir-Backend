FROM python:3.7

WORKDIR /opt/tahrir

ENV TERM xterm
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update --fix-missing && apt-get install -qqy postgresql-client

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

EXPOSE 55555
