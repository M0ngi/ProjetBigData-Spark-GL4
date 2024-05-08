#!/bin/bash

docker exec -it hadoop-master kafka-topics.sh --create --topic Crypto-Kafka --replication-factor 1 --partitions 1 --bootstrap-server localhost:9092
