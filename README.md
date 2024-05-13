# airflow-cosmos-sample

A sample dbt project with astonomer and airflow.
Based off tutorial found here: https://docs.astronomer.io/learn/airflow-dbt


The DAG is built from manifest, hence we need to manually create the manifest by running:
```
cd dags/dbt/dbt_project
rm -r target
dbt deps
dbt parse
dbt docs generate
cd ../../..
```

To run the project:
```
astro dev start
```

## Sample data for Postgres db
Sample data for db from https://github.com/zseta/postgres-docker-samples/tree/main

copy data into docker container
```
export DB=$(docker ps --filter "name=postgres" --format '{{.Names}}' | cut -d' ' -f1)
docker cp data/schema.sql $DB:/schema.sql
docker cp data/stocks/data/stocks.csv $DB:/stocks.csv
docker cp data/movies/data/credits.csv $DB:/credits.csv
docker cp data/movies/data/movies.csv $DB:/movies.csv
```
exec into the container
```
docker exec -it $DB psql -U postgres -d postgres
```
then create the schemas and copy data into tables
```
\i schema.sql
\copy stocks FROM '/stocks.csv' DELIMITER ',' CSV HEADER;
\copy credits FROM '/credits.csv' DELIMITER ',' CSV HEADER;
\copy movies FROM '/movies.csv' DELIMITER ',' CSV HEADER;
```

## Pre-commig hooks

With manifest and docs generated, you can run pre-commit hooks like:
```
pre-commit run --all-files
```