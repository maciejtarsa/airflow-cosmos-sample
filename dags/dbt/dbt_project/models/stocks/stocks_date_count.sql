SELECT
    date,
    COUNT(*) as count
FROM {{ ref('stocks_source') }}
GROUP BY 1