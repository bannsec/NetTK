FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y python-pip python-tk xauth && \
    pip install scapy numpy matplotlib

WORKDIR /root

COPY . .

