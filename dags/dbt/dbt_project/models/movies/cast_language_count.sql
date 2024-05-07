SELECT
    title,
    cast_count
FROM {{ ref('cast_language') }}
WHERE cast_count > 0