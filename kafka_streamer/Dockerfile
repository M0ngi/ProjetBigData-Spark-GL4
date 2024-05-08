FROM python:alpine3.16

RUN apk update
RUN apk upgrade
RUN apk add build-base
RUN apk add socat

RUN apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    librdkafka \
    librdkafka-dev

RUN  pip install requests confluent-kafka==1.6.0

WORKDIR /app

COPY main.py .
COPY crypto_streamer ./crypto_streamer

CMD python3 main.py