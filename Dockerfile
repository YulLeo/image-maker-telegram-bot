FROM ubuntu:20.04

WORKDIR /meme-and-gifs-generator-telegram-bot

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3 pip

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]
