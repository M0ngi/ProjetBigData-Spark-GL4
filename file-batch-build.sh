#!/bin/bash

old_dir=$(pwd)
cd "${0%/*}"

mvn package -f "./tools/batch_file/pom.xml"
docker cp tools/batch_file/target/batch_file-1.0-SNAPSHOT.jar hadoop-master:/root/batch_file.jar

cd "$old_dir"
