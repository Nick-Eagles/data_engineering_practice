from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
        dag_id="very_basic",
        start_date=datetime(2025, 10, 12, 2),
        schedule="@daily",
        description="A one-task DAG to get comfortable with Airflow",
        default_args=default_args
    ) as dag:
    task1 = BashOperator(
        task_id="hello_world", bash_command="echo 'Hello World!'"
    )

    task1
