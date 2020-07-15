FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y --fix-missing
RUN apt-get install -y python3-pip python3-dev python3-virtualenv build-essential cron sqlite3 vim
RUN apt-get update --fix-missing

RUN pip3 install --upgrade pip

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /opt/app

EXPOSE 8080
EXPOSE 9092

# Install dependencies:
COPY requirements.txt implementacao/server/requirements.txt
RUN pip3 install -r implementacao/server/requirements.txt

COPY install.sh implementacao/server/install.sh
RUN implementacao/server/install.sh

ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen

RUN echo "0 * * * * cd /opt/app/ && /bin/bash gerar_desafio.sh >> log/cron_gerar_desafios.log && cd -" | crontab

COPY . .
