# Learning and exploring Airflow

In this directory, I practice mostly basic uses of Apache Airflow for
orchestrating data-engineering workflows (in one case a simple ETL pipeline).
I make use of locally hosted resources, including a Postgres database and an S3
bucket using `DBeaver` and `MinIO` respectively. The workflows were heavily
inspired by [coder2j's tutorial](https://www.youtube.com/watch?v=K9AnJ9_ZAXE),
but deviate at times as necessary to independently practice and learn Airflow
most effectively.

## DAGs

DAGS are hosted under `.airflow/dags`, which were developed in this order:

- **very_basic.py**: I do a "Hello world"-like example, where I initially used
`BashOperator` and `PythonOperator`, and later refined things using the Taskflow
API.
- **postgres_test.py**: I develop a proof-of-concept DAG to connect to a local
Postgres database. I use the `SQLExecuteQueryOperator` to create a table and
insert some rows into it.
- **minio_test.py**: Another proof of concept where I use `S3KeySensor` to poke
an S3 bucket hosted locally with MinIO, checking for a specific dataset.
- **postgres_to_s3**: A small ETL pipeline building upon the previous two DAGs
to extract data daily from a Postgres database and load into an S3 bucket (no
real transformation step).

## Other info

For this project, I used `uv` to create a Python virtual environment with the
necessary dependencies, and set the Airflow home to `.airflow`.

```
#   Explicitly activate the virtual environment
source .venv/bin/activate

#   Set Airflow home inside this repo (to be run from this directory)
export AIRFLOW_HOME=$(pwd)/.airflow
```
