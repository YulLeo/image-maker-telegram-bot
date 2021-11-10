FROM python:3.9-slim

WORKDIR /meme-and-gifs-generator-telegram-bot

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]
