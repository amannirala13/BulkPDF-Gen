FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get -y install firefox
RUN apt-get -y install xauth
RUN apt-get -y python3


COPY . .

EXPOSE 8887
CMD firefox