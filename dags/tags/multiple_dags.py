"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.constants import TestIndirectSelection

# adjust for other database types
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
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

tags = [
    {"tag": "stocks_dag"},
    {"tag": "movies_dag"}
]

for index, item in enumerate(tags):
    tag = item.get('tag')
    tag_1 = tag.split("_")[0]

    with DAG(
        dag_id=f"c_multiple_dags_{tag_1}",
        start_date=datetime(2023, 8, 1),
        schedule=None,
        catchup=False,
    ) as dag:
        
        
    
        transform_data = DbtTaskGroup(
            render_config=RenderConfig(
                select=[f"tag:{tag}"],
            ),
            group_id=f"transform_{tag_1}_data",
            project_config=project_config,
            profile_config=profile_config,
            execution_config=execution_config,
            default_args={"retries": 2},
        )

        if index != len(tags) - 1:
            next_dag_id = f"""c_multiple_dags_{tags[index + 1].get('tag').split("_")[0]}"""
            trigger = TriggerDagRunOperator(
                task_id="trigger_next_dag",
                trigger_dag_id=next_dag_id,
                conf={"message":"Message to pass to c_multiple_dags_movies."},
                trigger_rule="all_done", # trigger even if previous task failed
            )

            
            transform_data >> trigger
        else:
            transform_data

