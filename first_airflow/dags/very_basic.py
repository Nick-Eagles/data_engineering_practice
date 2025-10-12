from airflow import DAG
from datetime import datetime


default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
        dag_id="very_basic",
        start_date=datetime(2025, 10, 12, 2),
        schedule_interval="@daily",
        description="A one-task DAG to get comfortable with Airflow",
        default_args=default_args
    ) as dag:
    pass
