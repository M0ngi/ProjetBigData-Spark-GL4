# Big Data Project For University Year GL4 - INSAT

Group:

- Salma Seddik
- Naima Attia
- Med Mongi Saidane

## Description

This project consists of:
* A streaming application, collecting data from public APIs & publishing them to a Kafka Queue.
* Same service as above, however working as a TCP streamer instead of Kafka.
* A spark streaming pipeline, taking data from Kafka & transforming it, making some calculations then storing data to both Hadoop File System & to MongoDB.
* A spark batch processing pipeline, taking a csv file & transforming the data in it, writing to HDFS & to MongoDB.
* A grafana service, reading data from MongoDB & displaying multiple graphs. Some of the graphs are real-time data.

## Architecture

<p align="center">
    <img src="https://i.imgur.com/eSxN5PZ.png" />
</p>

## Spark pipelines

<p align="center">
    <img src="https://i.imgur.com/VDsngO3.png" />
</p>

## Tools & Stack used

* Python (Streaming services, Spark streaming & batch processing)
* Grafana (Data display)
* MongoDB
* Hadoop FS
* Spark
* Kafka
* Docker & Docker compose

## Starting

To run everything, use [up.sh](/up.sh) To reset/shutdown, use [reset.sh](/reset.sh)

## Tools & scripts

* Spark applications are inside [tools](/tools) folder.
* To get a shell on Hadoop containers, you can find bash scripts to do so quickly in [sh](/sh) folder.
* Last, other helper bash scripts can be found inside [scripts](/scripts) folder.
