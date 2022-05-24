FROM python:3.10.4
LABEL Maintainer="yuri"
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD ["apt-get -y install stockfish"]

CMD [ "python3", "./main.py"]

