"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.constants import TestIndirectSelection

# adjust for other database types
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import os

DB_NAME = "postgres"
SCHEMA_NAME = "postgres"
# The path to the dbt project
DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/dbt_project"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
from airflow.utils.email import send_email

manifest_path = f"{DBT_PROJECT_PATH}/target/manifest.json"

project_config = ProjectConfig(
    manifest_path=manifest_path,
    project_name="dbt_project",
)

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgres",
        profile_args={"schema": "public", "port": 5432, "host": "dbt_project_b4a9db-postgres-1", "dbname": DB_NAME, "user": "postgres", "password": "postgres"}
    ),
)

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
    dbt_project_path=DBT_PROJECT_PATH,
    test_indirect_selection=TestIndirectSelection.BUILDABLE
)

def send_success_status_email(context):
    task_instance = context['task_instance']
    task_status = task_instance.current_state()

    subject = f"Airflow Task {task_instance.task_id} {task_status}"
    body = f"The task {task_instance.task_id} finished with status: {task_status}.\n\n" \
           f"Task execution date: {context['execution_date']}\n" \
           f"Log URL: {task_instance.log_url}\n\n"

    to_email = "abc@example.com"  # Specify the recipient email address

    send_email(to=to_email, subject=subject, html_content=body)

def send_failure_status_email(context):
    task_instance = context['task_instance']
    task_status = task_instance.current_state()

    subject = f"Airflow Task {task_instance.task_id} {task_status}"
    body = f"The task {task_instance.task_id} finished with status: {task_status}.\n\n" \
           f"Task execution date: {context['execution_date']}\n" \
           f"Log URL: {task_instance.log_url}\n\n"

    to_email = "abc@example.com"  # Specify the recipient email address

    send_email(to=to_email, subject=subject, html_content=body)


@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
)
def a_one_big_dag():
    transform_data = DbtTaskGroup(
        group_id="transform_all_data",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        default_args={"retries": 2},
    )

    start_task = DummyOperator(task_id='start_task')

    end_task = DummyOperator(task_id='end_task')

    success_email_task = PythonOperator(
        task_id='success_email_task',
        python_callable=send_success_status_email,
        provide_context=True,
        dag=dag
    )

    failure_email_task = PythonOperator(
        task_id='failure_email_task',
        python_callable=send_failure_status_email,
        provide_context=True,
        dag=dag
    )

    # Set the on_success_callback and on_failure_callback
    success_email_task.set_upstream(transform_data)
    failure_email_task.set_upstream(transform_data)

    start_task >> transform_data >> end_task
    

a_one_big_dag()

