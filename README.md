Steps for execution -

Python version used --> 3.12

pip install -r requirements.txt

Step 1:

Kafka set up (either start manually on local machine OR use Docker file provided with the project)

zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
kafka-server-start.sh $KAFKA_HOME/config/server.properties
(new terminal window)

(in Kafka folder of project)
Execute python3 producer.py


Execute consumer script below - ETL script
Execute load_transactionlog.py

---------


Implementation 1: CSV as output

Execute load_transactionlog_csv_with_validations.py (kafka consumer script)
This will save Kafka input data from producer to below location:

pyspark/output/transactions  --> data and tmp folders will get created and files wil be saved as partitioned output

----------------
Implementation 2: Snowflake as output

Execute below 2 scripts to create Snoflake schema design and load metadata:
snowflake/generate_schema.py
snowflake/load_metadata_tables.py

This will create tables structure in snowflake and populate metadata tables

Execute below script to load data into snowflake tables
pyspark/scripts/load_transactionlog_snowflake.py

--------------

Implementation 3: Open source warehouse delta table as output
load_transactionlog_delta.py



————————————

Step 2:

Airflow DAG monitoring
(Ensure that Spark and Airflow are on different ports)


Spark

Start master on 8081
 $SPARK_HOME/sbin/start-master.sh --webui-port 8081

Spark master on —> http://localhost:8081/


To stop master
$SPARK_HOME/sbin/stop-master.sh


Airflow on
	http://localhost:8080/home
It will execute below dag:
airflow/dags/data_pipeline_dag.py

—————————————

Step 3:

Prometheus set up


./prometheus --config.file=prometheus.yml
Localhost:9090.  Dashboard will be seen
Localhost:9090/targets.


To restart prometheus

sudo lsof -i :9308
Kill <PID>


Kafka exporter

docker run -d -p 9308:9308 --name kafka-exporter \
  -e KAFKA_SERVER=localhost:9092 \
  danielqsj/kafka-exporter

./kafka_exporter --kafka.server=localhost:9092


Go to localhost.  http://localhost:9308/metrics.  OR http://localhost:9308/ to open Kafka exporter



