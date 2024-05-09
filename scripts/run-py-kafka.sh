#!/bin/bash

spark-submit \
    --master local \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    --exclude-packages org.slf4j:slf4j-api \
    kafka_stream_handler.py