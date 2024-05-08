#!/bin/bash

docker exec -it hadoop-master kafka-topics.sh --list --bootstrap-server localhost:9092
