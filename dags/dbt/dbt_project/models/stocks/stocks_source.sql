SELECT 
    date, 
    symbol, 
    open, 
    high, 
    low, 
    close, 
    adj_close, 
    volume
FROM {{ source('stocks', 'stocks')}}