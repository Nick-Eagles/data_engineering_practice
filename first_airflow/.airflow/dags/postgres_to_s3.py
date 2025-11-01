from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import os
from pyhere import here

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

def postgres_to_s3():
    #   Connect to the Postgres db and extract some example rows
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE date <= '2022-05-01';")
    
    #   Convert to DataFrame and export to a temporary CSV
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=column_names)
    df.to_csv(here('temp.csv'), index=False)
    
    #   Close database connection
    cursor.close()
    conn.close()

with DAG(
    dag_id="postgres_to_s3",
    start_date=datetime(2025, 11, 1, 2),
    schedule="@daily",
    description="Move data from a Postgres database to S3",
    default_args=default_args
) as dag:
    pass
