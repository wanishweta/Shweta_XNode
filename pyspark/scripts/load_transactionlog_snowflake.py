import pyspark
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Snowflake connection options - replace with your own credentials and details
sfOptions = {
    "sfURL": "<your_account>.snowflakecomputing.com",
    "sfDatabase": "<your_database>",
    "sfSchema": "<your_schema>",
    "sfWarehouse": "<your_warehouse>",
    "sfRole": "<your_role>",  # optional
    "sfUser": "<your_user>",
    "sfPassword": "<your_password>"
}


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


# Set the log level to WARN to reduce output verbosity
spark.sparkContext.setLogLevel("WARN")

# Optional: Set the checkpoint directory for streaming operations
checkpoint_dir = "./tmp/spark_checkpoints"

# Specify the Delta table location (or create a new one)
delta_table_path = "/Users/shwetawani/Documents/XNode Project/XNode_project/delta_warehouse"

# Create a new database
spark.sql("CREATE DATABASE IF NOT EXISTS my_database")


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

kafka_df = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# For demonstration purposes, let's output the Kafka data to the console
"""
query = kafka_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()
"""
# Function to write data into Snowflake
def write_to_snowflake(df, epoch_id):
    df.write \
        .format("snowflake") \
        .options(**sfOptions) \
        .option("dbtable", "transactions") \
        .mode("append")  \
        .save()


# Write the streaming DataFrame to Snowflake in micro-batches
query = kafka_df.writeStream \
    .foreachBatch(write_to_snowflake) \
    .trigger(processingTime='2 seconds') \
    .start()


# Await termination (the query will keep running to continuously stream data into Snowflake)
query.awaitTermination()
