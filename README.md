# Big Data Project For University Year GL4 - INSAT

## Description

This project consists of:
* A streaming application, collecting data from public APIs & publishing them to a Kafka Queue.
* Same service as above, however working as a TCP streamer instead of Kafka.
* A spark streaming pipeline, taking data from Kafka & transforming it, making some calculations then storing data to both Hadoop File System & to MongoDB.
* A spark batch processing pipeline, taking a csv file & transforming the data in it, writing to HDFS & to MongoDB.
* A grafana service, reading data from MongoDB & displaying multiple graphs. Some of the graphs are real-time data.

## Tools & Stack used

* Python (Streaming services, Spark streaming & batch processing)
* Grafana (Data display)
* MongoDB
* Hadoop FS
* Spark
* Kafka 
