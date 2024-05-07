{{ config(
    tags=["movies_dag"]
) }}

SELECT 
    movie_id,
    title,
    "cast" AS cast,
    crew
FROM {{ source('movies', 'credits')}}