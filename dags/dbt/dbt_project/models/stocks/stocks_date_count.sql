SELECT
    CAST (date AS DATE) AS date,
    COUNT(*) as count
FROM {{ ref('stocks_source') }}
GROUP BY 1