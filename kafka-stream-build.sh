#!/bin/bash

old_dir=$(pwd)
cd "${0%/*}"

mvn package -f "/home/m0ngi/Projet-BigData/tools/kafka_stream/pom.xml"
docker cp tools/kafka_stream/target/kafka_stream-1.0-SNAPSHOT.jar hadoop-master:/root/kafka_stream.jar

cd "$old_dir"
