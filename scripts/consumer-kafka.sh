#!/bin/bash

docker exec -it hadoop-master kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic Crypto-Kafka --from-beginning

