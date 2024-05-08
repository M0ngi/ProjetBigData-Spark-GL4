#!/bin/bash

cp ./tools/kafka_stream_handler.py ./master/

docker compose up --build
