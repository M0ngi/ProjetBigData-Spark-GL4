#!/bin/bash

cp ./tools/kafka_stream_handler.py ./master/tools/
cp ./scripts/run-py-kafka.sh ./master/tools/

docker network create \
  --driver=bridge \
  --subnet="172.50.0.0/24" \
  --gateway="172.50.0.1" "hadoop"

docker compose up --build
