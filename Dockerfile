FROM python:3.10.4
LABEL Maintainer="yuri"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN apt-get update
RUN apt-get -y install stockfish
CMD python3 ./app.py ${BOT_TOKEN:?no BOT_TOKEN}

