import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import when

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

df_with_state = df.withColumn("state", when(df["Open"] < df["Close"], "UP").otherwise("DOWN"))

df_with_state.printSchema()

df_with_state.write \
        .format("mongo") \
        .mode("append") \
        .option("spark.mongodb.output.database", "testDb") \
        .option("spark.mongodb.output.collection", "trade_sessions") \
        .save()

# Write the batch processed data to an output file
df_with_state. \
    write \
    .mode("overwrite") \
    .csv("output.csv")