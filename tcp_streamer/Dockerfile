FROM python:alpine3.16

RUN apk update
RUN apk upgrade
RUN apk add build-base
RUN apk add socat

RUN  pip install requests

WORKDIR /app

COPY main.py .
COPY crypto_streamer ./crypto_streamer

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 /app/main.py",pty,stderr