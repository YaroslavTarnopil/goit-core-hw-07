FROM ubuntu:latest
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt