#!/bin/bash

# docker cp tools/batch_file/target/batch_file-1.0-SNAPSHOT.jar hadoop-master:/root/batch_file.jar

docker exec -it hadoop-master spark-submit  --class spark.batch.tp21.WordCountTask --master yarn --deploy-mode cluster wordcount-spark.jar input/purchases.txt out-spark2
# docker exec -it hadoop-master spark-submit  --class spark.batch.tp21.WordCountTask --master local wordcount-spark.jar input/purchases.txt out-spark-test
