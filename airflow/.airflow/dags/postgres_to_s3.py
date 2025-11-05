#   Implement a simple ETL pipeline orchestrated with Airflow: each day, extract
#   that day's associated order data from a Postgres database (in practice
#   hosted locally), then load into S3 (really a local MinIO instance). This
#   particular workflow doesn't feature much of a transformation step

from datetime import datetime, timedelta
import pandas as pd
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

def postgres_to_s3(data_interval_start, data_interval_end):
    #   Connect to the Postgres db and extract rows associated with the current
    #   date
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    start_dt = datetime.fromisoformat(data_interval_start.replace('Z', '+00:00'))
    end_dt = datetime.fromisoformat(data_interval_end.replace('Z', '+00:00'))

    #   For manually triggered DAG runs
    if start_dt == end_dt:
        end_dt = start_dt + timedelta(days=1)
    
    #   Parse the dates into strings of just the date portion
    start_date = start_dt.strftime('%Y-%m-%d')
    end_date = end_dt.strftime('%Y-%m-%d')
    
    cursor.execute(
        f"SELECT * FROM orders WHERE date >= '{start_date}' AND date < '{end_date}';"
    )
    
    #   Convert to DataFrame and export to a temporary CSV
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=column_names)

    #   Write the data to a temporary CSV file
    with NamedTemporaryFile(mode='w', suffix=f'_{start_date}.csv', delete=False) as temp_file:
        df.to_csv(temp_file.name, index=False)
        temp_csv_path = temp_file.name
    
    #   Close database connection
    cursor.close()
    conn.close()

    #   Upload today's CSV to S3
    s3_hook = S3Hook(aws_conn_id='minio_conn')
    s3_hook.load_file(
        filename=temp_csv_path,
        key=f'orders_{start_date}.csv',
        bucket_name='airflow-test',
        replace=True
    )

with DAG(
    dag_id="postgres_to_s3",
    start_date=datetime(2025, 11, 1),
    schedule="@daily",
    description="Move data from a Postgres database to S3",
    default_args=default_args
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3,
        op_kwargs={
            "data_interval_start": "{{ data_interval_start }}",
            "data_interval_end": "{{ data_interval_end }}"
        }
    )

    task1
