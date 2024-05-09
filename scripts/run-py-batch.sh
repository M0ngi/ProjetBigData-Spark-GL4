#!/bin/bash

spark-submit \
    --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 \
    --master local \
    batch_handler.py $@
    
#binance.csv
