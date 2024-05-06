# airflow-cosmos-sample

A sample dbt project with astonomer and airflow.
Based off tutorial found here: https://docs.astronomer.io/learn/airflow-dbt

To tun the project:
```
astro dev start
```

## Sample data for Postgres db
Sample data for db from https://github.com/zseta/postgres-docker-samples/tree/main

copy data into docker container
```
docker cp data/schema.sql astro-dbt-core-sample_b4a9db-postgres-1:/schema.sql
docker cp data/stocks/data/stocks.csv astro-dbt-core-sample_b4a9db-postgres-1:/stocks.csv
docker cp data/movies/data/credits.csv astro-dbt-core-sample_b4a9db-postgres-1:/credits.csv
docker cp data/movies/data/movies.csv astro-dbt-core-sample_b4a9db-postgres-1:/movies.csv
```
exec into the container
```
docker exec -it astro-dbt-core-sample_b4a9db-postgres-1 psql -U postgres -d postgres
```
then create the schemas and copy data into tables
```
\i schema.sql
\copy stocks FROM '/stocks.csv' DELIMITER ',' CSV HEADER;
\copy credits FROM '/credits.csv' DELIMITER ',' CSV HEADER;
\copy movies FROM '/movies.csv' DELIMITER ',' CSV HEADER;
```