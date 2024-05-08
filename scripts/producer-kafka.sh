#!/bin/bash

docker exec -it hadoop-master kafka-console-producer.sh --broker-list localhost:9092 --topic Crypto-Kafka
