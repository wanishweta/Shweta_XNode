
import pyspark
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, coalesce
from pyspark.sql.functions import col, from_json, json_tuple, split, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import logging


# Set up logging
logger = logging.getLogger('pyspark_job')
logger.setLevel(logging.INFO)

# Create a console handler and set the level to INFO
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(ch)

logger.info("Spark job started successfully =====================")



# transaction_id,transaction_date,security_id,region_id,trade_volume,trade_value,security_type,trade_type,price_per_unit,valid_from,valid_to,transaction_from,transaction_to

scala_version = '2.12'  # TODO: Ensure this is correct
spark_version = pyspark.__version__

print("spark_version: " + spark_version)
print("scala_version: " + scala_version)


packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.1'
]

args = os.environ.get('PYSPARK_SUBMIT_ARGS', '')
if not args:
    args = f'--packages {",".join(packages)}'
    print('Using packages', packages)
    os.environ['PYSPARK_SUBMIT_ARGS'] = f'{args} pyspark-shell'
else:
    print(f'Found existing args: {args}')



# Create a Spark session
spark = (
    SparkSession.builder
    .appName("KafkaConsumerTransactionLog")

    # Add package for Delta Lake
    #.config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0")  # io.delta:delta-core_2.12:2.2.0
    .config("spark.jars.packages", "io.delta:delta-core_2.12-1.1.0")  # io.delta:delta-core_2.12:2.2.0

    # Add settings to use Delta Lake with Spark session
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    #.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .enableHiveSupport()

    .getOrCreate()
)

logger.info("Spark session created successfully =====================")

# Set the log level to WARN to reduce output verbosity
spark.sparkContext.setLogLevel("WARN")

# Optional: Set the checkpoint directory for streaming operations
checkpoint_dir = "./tmp/spark_checkpoints"

# Specify the Delta table location (or create a new one)
delta_table_path = "/Users/shwetawani/Documents/XNode Project/XNode_project/delta_warehouse"

# Create a new database
spark.sql("CREATE DATABASE IF NOT EXISTS my_database")

# Define the schema for the expected JSON structure
schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("transaction_date", TimestampType(), True),
    StructField("security_id", StringType(), True),
    StructField("region_id", StringType(), True),
    StructField("trade_volume", IntegerType(), True),
    StructField("trade_value", IntegerType(), True),
    StructField("security_type", StringType(), True),
    StructField("trade_type", StringType(), True),
    StructField("price_per_unit", IntegerType(), True),
    StructField("valid_from", TimestampType(), True),
    StructField("valid_to", TimestampType(), True),
    StructField("transaction_from", TimestampType(), True),
    StructField("transaction_to", TimestampType(), True)
])


# Define Kafka parameters
kafka_bootstrap_servers = 'localhost:9092'  # Kafka brokers
kafka_topic = 'transactionlog'  # Kafka topic name

# Read data from Kafka topic
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .load()


# Kafka data contains binary format, so we need to convert it to strings or the desired type
# Let's assume the Kafka message value is in string format (e.g., JSON or plain text)
# We will also extract the key and value columns from the Kafka data


kafka_df = kafka_df.selectExpr("CAST(value AS STRING)")

csv_df = kafka_df.select(
    split(col("value"), ",").alias("csv_values")
)


# Here we are assuming the CSV has 10 columns, adjust based on your actual data
csv_df = csv_df.select(
    col("csv_values").getItem(0).alias("transaction_id"),
    coalesce(col("csv_values")[1].cast(TimestampType()), lit('1970-01-01 00:00:00').cast(TimestampType())).alias("transaction_date"),
    col("csv_values").getItem(2).alias("security_id"),
    col("csv_values").getItem(3).alias("region_id"),
    col("csv_values").getItem(4).alias("trade_volume"),
    col("csv_values").getItem(5).alias("trade_value"),
    col("csv_values").getItem(6).alias("security_type"),
    col("csv_values").getItem(7).alias("trade_type"),
    col("csv_values").getItem(8).alias("price_per_unit"),
    col("csv_values").getItem(9).alias("valid_from"),
    col("csv_values").getItem(10).alias("valid_to"),
    col("csv_values").getItem(11).alias("transaction_from"),
    col("csv_values").getItem(12).alias("transaction_to")
)

columns_filtered = csv_df.filter(col("transaction_id").isNotNull())

deduplicated_df = columns_filtered.dropDuplicates(["transaction_id"])

query = (csv_df  \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start())

query = csv_df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("checkpointLocation", "../output/transactions/tmp/checkpoints")  \
    .option("path", "../output/transactions/data") \
    .partitionBy("transaction_date","region_id") \
    .trigger(processingTime="10 seconds") \
    .start()

# Await termination (the query will keep running to continuously stream data into Snowflake)
query.awaitTermination()
