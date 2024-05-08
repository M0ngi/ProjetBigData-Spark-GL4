from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import  StructType, StructField, StringType, DoubleType, LongType
from pyspark.sql.functions import from_json, window, avg, count, expr, to_timestamp, from_unixtime #, col, concat
# from pyspark.sql import Window

def write_2mn_period(df: DataFrame, epoch_id):
    print(df)
    df.write \
        .format("mongo") \
        .mode("append") \
        .option("spark.mongodb.output.database", "testDb") \
        .option("spark.mongodb.output.collection", "questions") \
        .option("uri", "mongodb+srv://root:AEyJg8UH4CPyPiIo@cluster0.c3oav3m.mongodb.net/testdb") \
        .save()
        # .option("uri",mongoURL) \


if __name__ == '__main__':
    spark: SparkSession = SparkSession\
        .builder \
        .appName("SparkStructredStream") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

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

    # Read a Streaming Source
    input_df = spark.readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("subscribe", "Crypto-Kafka")\
        .option("startingOffsets", "earliest")\
        .load()

    input_df.printSchema()
    
    # Transform to Output DataFrame
    value_df = input_df\
        .selectExpr("CAST(value AS STRING)") \
        .select(from_json("value", schema).alias("json")) \
        .select("json.*") \
        .select("data.*", "timestamp")
    
    value_df.printSchema()
    
    value_df = value_df\
        .withColumn("rateUsd", value_df.rateUsd.cast(DoubleType())) \
        .withColumn("timestamp", to_timestamp(from_unixtime(value_df.timestamp/1000)))

    value_df.printSchema()

    query = value_df \
        .withWatermark("timestamp", "1 minutes") \
        .groupBy(window("timestamp", "1 minutes")) \
        .agg(avg("rateUsd").alias("averageRate"), count(expr("*")).alias("count")) \
        .select("window.*", "averageRate", "count")
    
    x = query \
        .writeStream \
        .foreachBatch(write_2mn_period) \
        .start()
    
        # .outputMode("append") \
        # .format("console") \
        # .option("truncate", False) \
        # .start()

    x.awaitTermination()
