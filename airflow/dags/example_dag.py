from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
#from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator


# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 3, 20),  # Adjust to your desired start date
}

# Initialize the DAG
with DAG(
    'example_dag_run',
    default_args=default_args,
    schedule_interval='* * * * *',  # Runs every minute
    catchup=False,
) as dag:


    # Define a task using BashOperator
    run_bash_task = BashOperator(
        task_id='run_bash_command',
        bash_command='echo "Hello, Airflow!"',  # The bash command to run
        #dag=dag,
    )

    run_bash_task

