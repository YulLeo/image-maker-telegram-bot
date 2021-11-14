# Image Maker Telegram bot 

Telegram bot that can receive from the user:

- image and text to it => places the text on the image and returns its transformed
- a set of pictures => creates a GIF from these pictures, adds a watermark to the file and returns a GIF object 


## Get started

### Run in virtualenv

1. Clone repository
```bash
git clone git@github.com:YulLeo/meme-and-gifs-generator-telegram-bot.git
```
2. Create virtual environment `python -m venv venv` and activate it `source venv/bin/activate` for Linux.
3. Set up python dependencies from requirements.txt file
```bash
pip install -r requirements.txt
```
4. Create .env file in the repository root with following environment variables:
```
TELEGRAM_API_TOKEN=<YOUR_TELEGRAM_API_TOKEN>
SECRET_KEY=<MINIO_SECRET_KEY>
ACCESS_KEY=<MINIO_ACCESS_KEY>
```
[How to get Telegram Bot API token](https://core.telegram.org/bots#6-botfather)

5. Set up and run MinIo.

[MinIo Quick Start Guide](https://docs.min.io/docs/minio-quickstart-guide.html)

7. To start bot run following command:
```bash
python main.py
```

### Run with docker
1. Clone repository
```bash
git clone git@github.com:YulLeo/meme-and-gifs-generator-telegram-bot.git
```
2. Create .env file in the repository root with following environment variables:
```
TELEGRAM_API_TOKEN=<YOUR_TELEGRAM_API_TOKEN>
SECRET_KEY=<MINIO_SECRET_KEY>
ACCESS_KEY=<MINIO_ACCESS_KEY>
```
[How to get Telegram Bot API token](https://core.telegram.org/bots#6-botfather)

3. Run
```bash
docker-compose up
```
