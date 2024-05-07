"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig, DbtDag
from cosmos.constants import TestIndirectSelection

# adjust for other database types
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime
import os

DB_NAME = "postgres"
SCHEMA_NAME = "postgres"
# The path to the dbt project
DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/dbt_project"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

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

@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
)
def c_multiple_dags_stocks():
    transform_stock_data = DbtTaskGroup(
        render_config=RenderConfig(
            select=["tag:stocks_dag"],
        ),
        group_id="transform_stock_data",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        default_args={"retries": 2},
    )

    transform_stock_data

c_multiple_dags_stocks()

@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
)
def c_multiple_dags_movies():

    transform_movies_data = DbtTaskGroup(
        render_config=RenderConfig(
            select=["tag:movies_dag"],
        ),
        group_id="transform_movies_data",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        default_args={"retries": 2},
    )

    transform_movies_data

c_multiple_dags_movies()
