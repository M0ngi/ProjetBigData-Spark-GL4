import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import when, expr, window, to_timestamp, avg, max, min, lit, col

if len(sys.argv) < 2:
    print("missing args")
    exit()

spark: SparkSession = SparkSession\
        .builder \
        .appName("TradingSessionProcessing") \
        .config("spark.mongodb.output.uri", "mongodb://root:roottoor@mongodb/?retryWrites=true&w=majority") \
        .config("spark.mongodb.input.uri", "mongodb://root:roottoor@mongodb/?retryWrites=true&w=majority") \
        .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read batch data from a file
df = spark.read.csv(sys.argv[1], header=True, inferSchema=True)

df_with_state = df \
    .withColumn("state", when(df["Open"] < df["Close"], 1).otherwise(-1)) \
    .withColumn("avg", expr("(High + Low) / 2")) \
    .withColumn("interval", lit("1d"))

df_with_state.printSchema()

df_with_state.write \
        .format("mongo") \
        .mode("append") \
        .option("spark.mongodb.output.database", "testDb") \
        .option("spark.mongodb.output.collection", "trade_sessions") \
        .save()

monthly = df_with_state \
    .withColumn("timestamp", to_timestamp(df_with_state.Date)) \
    .groupBy(window("timestamp", "29 days")) \
    .agg(
        avg("avg").alias("avg"),
        max("High").alias("High"),
        min("Low").alias("Low"),
    ) \
    .select("window.*", "avg", "High", "Low") \
    .withColumn("interval", lit("1m")) \
    .withColumn("Date", col("start"))

monthly.printSchema()

monthly.write \
    .format("mongo") \
    .mode("append") \
    .option("spark.mongodb.output.database", "testDb") \
    .option("spark.mongodb.output.collection", "trade_sessions") \
    .save()

# Write the batch processed data to an output file
df_with_state. \
    write \
    .mode("overwrite") \
    .csv("output_1d.csv")

monthly. \
    write \
    .mode("overwrite") \
    .csv("output_1m.csv")
