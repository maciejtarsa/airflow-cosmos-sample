{{ config(
    tags=["stocks_dag"]
) }}

SELECT
    CAST (date AS DATE) AS date,
    CAST (COUNT(*) AS INT) as count
FROM {{ ref('stocks_source') }}
GROUP BY 1