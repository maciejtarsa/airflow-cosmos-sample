SELECT
    movies.title,
    movies.original_language,
    movies.original_title,
    credits.cast
FROM {{ ref('movies_source') }} AS movies
JOIN {{ ref('credits_source') }} AS credits
ON movies.id = credits.movie_id