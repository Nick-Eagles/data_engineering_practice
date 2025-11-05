from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    "owner": "Nick",
    "retries": 1,
    "retry_delay": timedelta(minutes=2)
}

#   Construct a simple DAG using the TaskFlow API
@dag(
    dag_id="very_basic",
    start_date=datetime(2025, 10, 12, 2),
    schedule="@daily",
    description="A two-task DAG to get comfortable with Airflow",
    default_args=default_args
)
def very_basic_dag():
    #   A trivial task, just returning the current date
    @task
    def get_time():
        return datetime.now().strftime("%Y-%m-%d")
    
    #   Hello world, except print the current date
    @task
    def hello_world(current_date: str):
        print(f"Hello World, it is currently {current_date}!")

    #   Task order. Since we're using the TaskFlow API, "XComs" become an
    #   argument to the second task
    time_result = get_time()
    hello_world(time_result)

#   Instantiate the DAG
very_basic_dag()
