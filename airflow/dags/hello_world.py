from airflow.sdk import dag, task
from datetime import datetime

@dag(
    dag_id='hello_world_dag',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=['testing'],
)

def hello_world():
    @task.bash
    def print_hello():
        return 'echo "Hello World!"'

    print_hello()

hello_world()