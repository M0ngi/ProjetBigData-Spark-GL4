from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import  StructType, StructField, StringType, DoubleType, LongType
from pyspark.sql.functions import lit, from_json, window, max, min, avg, count, expr, to_timestamp, from_unixtime #, col, concat
# from pyspark.sql import Window

def write_coin_collection(df: DataFrame, epoch_id):
    print(df)
    df.write \
        .format("mongo") \
        .mode("append") \
        .option("spark.mongodb.output.database", "testDb") \
        .option("spark.mongodb.output.collection", "coin_values") \
        .save()
        # .option("uri", "mongodb+srv://root:roottoor@mongodb") \
        # .option("uri", "mongodb+srv://root:AEyJg8UH4CPyPiIo@cluster0.c3oav3m.mongodb.net/testdb") \
        # .option("uri",mongoURL) \


if __name__ == '__main__':
    spark: SparkSession = SparkSession\
        .builder \
        .appName("SparkStructredStream") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.mongodb.output.uri", "mongodb://root:roottoor@mongodb/?retryWrites=true&w=majority") \
        .config("spark.mongodb.input.uri", "mongodb://root:roottoor@mongodb/?retryWrites=true&w=majority") \
        .getOrCreate()
        # .config("spark.mongodb.output.uri", "mongodb+srv://root:AEyJg8UH4CPyPiIo@cluster0.c3oav3m.mongodb.net/testdb?retryWrites=true&w=majority") \
        # .config("spark.mongodb.input.uri", "mongodb+srv://root:AEyJg8UH4CPyPiIo@cluster0.c3oav3m.mongodb.net/testdb?retryWrites=true&w=majority") \

    spark.sparkContext.setLogLevel("ERROR")
    spark.conf.set("spark.sql.files.ignoreMissingFiles", True)
    
    schema = StructType([
        StructField("data", StructType([
            StructField("id", StringType()),
            StructField("symbol", StringType()),
            StructField("rateUsd", StringType()),
        ])),
        StructField("timestamp", LongType()),
    ])
    
    queries = []

    # Read a Streaming Source
    input_df = spark.readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("subscribe", "Crypto-Kafka")\
        .option("startingOffsets", "earliest")\
        .load()
    
    # Transform to Output DataFrame
    value_df = input_df\
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", schema).alias("json")) \
        .select("json.*") \
        .select("data.*", "timestamp")
    
    value_df = value_df\
        .withColumn("rateUsd", value_df.rateUsd.cast(DoubleType())) \
        .withColumn("timestamp", to_timestamp(from_unixtime(value_df.timestamp/1000)))

    query0 = value_df \
        .withColumn("interval", lit("0")) \
        .withColumn("start", value_df.timestamp) \
        .withColumn("averageRate", value_df.rateUsd) \
        .select("start", "interval", "averageRate", "symbol")
        
    queries.append(query0.writeStream \
        .foreachBatch(write_coin_collection) \
        .start())

    query1 = value_df \
        .withWatermark("timestamp", "1 minutes") \
        .groupBy("symbol", window("timestamp", "1 minutes")) \
        .agg(
            max("rateUsd").alias("max"), 
            min("rateUsd").alias("min"), 
            avg("rateUsd").alias("averageRate"), 
            count(expr("*")).alias("count"),
        ) \
        .select("window.*", "symbol", "averageRate", "count", "max", "min") \
        .withColumn("interval", lit("1mn"))
    
    queries.append(query1.writeStream \
        .foreachBatch(write_coin_collection) \
        .start())
    
    query2 = value_df \
        .withWatermark("timestamp", "5 minutes") \
        .groupBy("symbol", window("timestamp", "5 minutes")) \
        .agg(
            max("rateUsd").alias("max"), 
            min("rateUsd").alias("min"), 
            avg("rateUsd").alias("averageRate"), 
            count(expr("*")).alias("count"),
        ) \
        .select("window.*", "symbol", "averageRate", "count", "max", "min") \
        .withColumn("interval", lit("5mn"))
    
    queries.append(query2.writeStream \
        .foreachBatch(write_coin_collection) \
        .start())
    
        # .outputMode("append") \
        # .format("console") \
        # .option("truncate", False) \
        # .start()

    for q in queries:
        q.awaitTermination()
