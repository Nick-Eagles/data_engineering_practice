#   A very basic DAG to just do a proof of concept: connect to a local Postgres
#   database and use Airflow to interact with it

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="postgres_test",
    start_date=datetime(2025, 10, 28, 2),
    schedule="@daily",
    description="A minimal DAG connecting to a local Postgres database",
    default_args=default_args
) as dag:
    task1 = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id="postgres_localhost",
        sql="""
        CREATE TABLE IF NOT EXISTS test_table (
            dt date,
            dag_id character varying,
            primary key (dt, dag_id)
        );
        """
    )

    task2 = SQLExecuteQueryOperator(
        task_id="insert_date",
        conn_id="postgres_localhost",
        sql="""
        INSERT INTO test_table (dt, dag_id) values (
            ' {{ ds }} ', '{{ dag.dag_id }}'
        );
        """
    )

    task1 >> task2
