from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

#   Trivial example of a function using XComs to push data, allowing exchange
#   between tasks
def get_time(ti):
    ti.xcom_push(
        key="current_time", value=datetime.now().strftime("%Y-%m-%d")
    )

with DAG(
        dag_id="very_basic",
        start_date=datetime(2025, 10, 12, 2),
        schedule="@daily",
        description="A one-task DAG to get comfortable with Airflow",
        default_args=default_args
    ) as dag:

    #   Get the current time
    task1 = PythonOperator(
        task_id="get_time",
        python_callable=get_time
    )

    #   "Hello world" but use XComs to get the current time from task1
    task2 = BashOperator(
        task_id="hello_world",
        bash_command="echo 'Hello World, it is currently {{ task_instance.xcom_pull(task_ids='get_time', key='current_time') }}!'"
    )

    task1 >> task2
