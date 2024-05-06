"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

# adjust for other database types
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime
import os

CONNECTION_ID = "postgres_conn"
DB_NAME = "postgres"
SCHEMA_NAME = "postgres"
MODEL_TO_QUERY = "stocks_base"
# The path to the dbt project
DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/dbt_project"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=CONNECTION_ID,
        profile_args={"schema": "public", "port": 5432, "host": "astro-dbt-core-sample_b4a9db-postgres-1", "dbname": DB_NAME, "user": "postgres", "password": "postgres"}
    ),
)

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)


@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
)
def big_dag():
    transform_data = DbtTaskGroup(
        group_id="transform_all_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        execution_config=execution_config,
        default_args={"retries": 2},
    )

    transform_data

big_dag()