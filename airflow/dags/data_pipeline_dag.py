from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

# Define the SLA miss callback
def sla_miss_callback(context):
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    sla = task_instance.sla
    # Send an alert (could be email, Slack, etc.)
    message = f"SLA for task {task_id} in DAG {dag_id} was missed. SLA was {sla}."
    print(message)
    # Optionally, send an email, or notify Slack, etc.
    # send_email('your-email@example.com', subject='SLA Missed', html_content=message)

# Define the failure callback
def on_failure_callback(context):
    task_instance = context.get('task_instance')
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    exception = context.get('exception')
    print(f"Task {task_id} in DAG {dag_id} failed with exception {exception}")
    # Send an alert (email, Slack, etc.)
    # send_email('your-email@example.com', subject='Task Failed', html_content=f"Task failed: {task_id}")


def on_success_callback(context):
    task_instance = context['task_instance']
    task_id = task_instance.task_id
    dag_id = task_instance.dag_id
    print(f"Task {task_id} in DAG {dag_id} succeeded.")
    # send_email('your-email@example.com', subject='Task Successfully completed', html_content=f"Task failed: {task_id}")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 20),
    'retries': 1,
    'on_failure_callback': on_failure_callback,  # Failure alert
    'on_success_callback': on_success_callback,  # Success alert
    'sla_miss_callback': sla_miss_callback       # SLA missed alert

}

# Define the DAG
dag = DAG(
    'spark_job_ETL_load',
    default_args=default_args,
    description='A DAG to run Spark job every 5 minutes',
    schedule_interval=None,  # This is the cron expression for every 5 minutes
    catchup=False,  # Do not backfill DAG runs
)

# Define the SparkSubmitOperator to submit a Spark job
spark_submit_task = SparkSubmitOperator(
    task_id='submit_spark_job',
    sla=timedelta(minutes=10) , # SLA of 10 minutes
    conn_id='my_spark',  # Use the connection ID for Spark (configured in the Airflow UI)
    application='/Users/shwetawani/Documents/XNode Project/XNode_project/pyspark/scripts/load_transactionlog_csv_with_validations.py',  # Path to your Spark job
    name='spark-job',
    verbose=True,
    driver_memory='2g',  # Adjust memory settings as needed
    executor_memory='2g',  # Adjust memory settings as needed
    conf={'spark.executor.cores': 2},  # Optional Spark configurations
    dag=dag,
)

# Define the task dependencies
spark_submit_task
