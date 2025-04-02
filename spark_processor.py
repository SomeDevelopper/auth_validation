from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

spark = SparkSession.builder \
    .appName('KafkaLogSparkStreaming') \
    .master('local[*]') \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoints") \
    .getOrCreate()

schema = StructType([
    StructField('timestamp', TimestampType(), True),
    StructField('route', StringType(), True),
    StructField('ip_address', StringType(), True),
    StructField('response', StringType(), True)
])

df = spark.readStream.format('kafka').option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "kafka_log").load()

parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

query = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()