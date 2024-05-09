#!/bin/bash

docker cp ./data/bitcoincash.csv hadoop-master:/root/bitcoincash.csv

docker exec -it hadoop-master hdfs dfsadmin -safemode leave
docker exec -it hadoop-master hdfs dfs -put /root/bitcoincash.csv
