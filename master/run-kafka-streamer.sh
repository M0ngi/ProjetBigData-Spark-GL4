#!/bin/bash

spark-submit \
    --master local \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
    --exclude-packages org.slf4j:slf4j-api \
    test.py
