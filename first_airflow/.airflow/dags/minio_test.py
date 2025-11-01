#   The goal is to demonstrate we can connect to an S3-like bucket, interacting
#   with it from Airflow. In practice, I host a small CSV via MinIO running
#   locally 

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="minio_test",
    start_date=datetime(2025, 10, 30, 2),
    schedule="@daily",
    description="Just connect to a local S3-like bucket with MinIO",
    default_args=default_args
) as dag:
    task1 = S3KeySensor(
        task_id="check_for_file",
        bucket_name="airflow-test",
        bucket_key="example_deliveries.csv",
        aws_conn_id="minio_conn"
    )

    task1
