from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, avg, min, max, count
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType
from database.elasticsearch_client import store_in_elasticsearch

KAFKA_BROKER = "localhost:9092"
SMPP_TOPICS = ["smpp-submit", "smpp-response", "smpp-deliver"]

# Define schema for SMPP packets
schema = StructType([
    StructField("packet_number", LongType(), True),
    StructField("timestamp_ms", DoubleType(), True),
    StructField("source_ip", StringType(), True),
    StructField("destination_ip", StringType(), True),
    StructField("source_port", LongType(), True),
    StructField("sequence_number", StringType(), True),
    StructField("command_status", StringType(), True),
    StructField("message_type", StringType(), True)
])

def process_smp_stream(df, epoch_id):
    """Process batch of SMPP data and store in Elasticsearch."""
    smpp_data = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

    # Compute latency statistics for Submit/Submit-Resp
    latency_stats = smpp_data.groupBy("sequence_number").agg(
        min("timestamp_ms").alias("submit_time"),
        max("timestamp_ms").alias("submit_resp_time")
    ).withColumn("latency", col("submit_resp_time") - col("submit_time"))

    latency_stats.select("sequence_number", "latency").show()

    # Send results to Elasticsearch
    for row in latency_stats.collect():
        store_in_elasticsearch({
            "sequence_number": row["sequence_number"],
            "latency": row["latency"]
        })

# Start Spark Session
spark = SparkSession.builder \
    .appName("SMPP-Stream-Analytics") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark_checkpoint") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", ",".join(SMPP_TOPICS)) \
    .option("startingOffsets", "earliest") \
    .load()

# Process in micro-batches
df.writeStream \
    .foreachBatch(process_smp_stream) \
    .start() \
    .awaitTermination()
