from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr, avg, max, min, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import logging
from config.logging_config import get_logger
from config.kafka_config import KAFKA_BROKER, SMPP_TOPIC
from config.config import POSTGRES_CONFIG

logger = get_logger(__name__)

# Define Kafka & PostgreSQL parameters
POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['dbname']}"
POSTGRES_PROPERTIES = {
    "user": POSTGRES_CONFIG["user"],
    "password": POSTGRES_CONFIG["password"],
    "driver": "org.postgresql.Driver",
}

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("SMPP_Spark_Processor") \
    .config("spark.jars", "postgresql-42.2.5.jar") \
    .getOrCreate()

logger.info("✅ Spark Session initialized.")

# Define Kafka message schema
smpp_schema = StructType([
    StructField("sequence_number", IntegerType(), True),
    StructField("source_ip", StringType(), True),
    StructField("dest_ip", StringType(), True),
    StructField("source_port", IntegerType(), True),
    StructField("submit_time_ms", DoubleType(), True),
    StructField("resp_time_ms", DoubleType(), True),
    StructField("latency_ms", DoubleType(), True),
    StructField("command_status", IntegerType(), True),
    StructField("message_id", StringType(), True),
    StructField("msg_body", StringType(), True),
])

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", SMPP_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

logger.info("🔄 Kafka Stream connected.")

# Deserialize JSON messages
df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), smpp_schema).alias("data")) \
    .select("data.*")

# Calculate real-time latency analytics
df_latency = df_parsed \
    .withColumn("latency_ms", col("resp_time_ms") - col("submit_time_ms")) \
    .groupBy() \
    .agg(
        avg("latency_ms").alias("avg_latency"),
        max("latency_ms").alias("max_latency"),
        min("latency_ms").alias("min_latency"),
        count(expr("latency_ms > (SELECT avg_latency)")).alias("above_avg_count"),
        count(expr("latency_ms < (SELECT avg_latency)")).alias("below_avg_count"),
    )

logger.info("🔄 Latency computation added.")

# Write real-time analytics to PostgreSQL
query = df_latency.writeStream \
    .outputMode("update") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.write \
                  .format("jdbc") \
                  .option("url", POSTGRES_URL) \
                  .option("dbtable", "smpp_latency") \
                  .option("user", POSTGRES_PROPERTIES["user"]) \
                  .option("password", POSTGRES_PROPERTIES["password"]) \
                  .option("driver", POSTGRES_PROPERTIES["driver"]) \
                  .mode("append") \
                  .save()) \
    .start()

logger.info("✅ Streaming query started. Writing to PostgreSQL.")

query.awaitTermination()
