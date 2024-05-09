#!/bin/bash

docker cp ./data/BinanceUSD.csv hadoop-master:/root/binance.csv

docker exec -it hadoop-master hdfs dfsadmin -safemode leave
docker exec -it hadoop-master hdfs dfs -put /root/binance.csv
