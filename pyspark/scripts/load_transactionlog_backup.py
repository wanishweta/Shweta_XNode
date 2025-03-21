import pyspark
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Snowflake connection options
sfOptions = {
  "sfURL" : "JHAVVFU-YP65809.snowflakecomputing.com",
  "sfDatabase" : "my_database",
  "sfSchema" : "my_schema",
  #"sfWarehouse" : "<your_warehouse>",
 # "sfRole" : "<your_role>",  # Optional, use if applicable
  "sfUser" : "DEMO",
  "sfPassword" : "Snowflake@1234"
}


scala_version = '2.12'  # TODO: Ensure this is correct
spark_version = pyspark.__version__

#packages = []

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.5.1'
]

#packages = [
#    'org.apache.spark:spark-sql-kafka-0-10_2.13:3.4.4',
#    'org.apache.kafka:kafka-clients:3.5.1'
#]

args = os.environ.get('PYSPARK_SUBMIT_ARGS', '')
if not args:
    args = f'--packages {",".join(packages)}'
    print('Using packages', packages)
    os.environ['PYSPARK_SUBMIT_ARGS'] = f'{args} pyspark-shell'
else:
    print(f'Found existing args: {args}')



# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaConsumerTransactionLog") \
    .getOrCreate()
    #.config("spark.jars",
    #        "/Users/shwetawani/Documents/XNode Project/XNode_project/jars/spark-snowflake_2.13-2.16.0-spark_3.4.jar,/Users/shwetawani/Documents/XNode Project/XNode_project/jars/snowflake-jdbc-3.13.1.jar") \
    #.getOrCreate()

# Set the log level to WARN to reduce output verbosity
spark.sparkContext.setLogLevel("WARN")

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
query = kafka_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()




# Await termination (the query will keep running to continuously stream data into Snowflake)
query.awaitTermination()
