FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y python3-pip python3-tk xauth

WORKDIR /root

COPY . .

COPY setup.py .

RUN pip3 install .
