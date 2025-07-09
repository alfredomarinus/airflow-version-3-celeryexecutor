from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='hello_world_dag',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=['testing'],
) as dag:
    print_hello_task = BashOperator(
        task_id='print_hello',
        bash_command='echo "Hello World!"',
    )

    print_hello_task