WITH ConsecutiveCodes AS (
    SELECT 
        codigo,
        secuencial,
        LAG(codigo, 1) OVER (ORDER BY secuencial) AS prev_codigo,
        LAG(codigo, 2) OVER (ORDER BY secuencial) AS prev_prev_codigo
    FROM Secuencial
)
SELECT DISTINCT codigo
FROM ConsecutiveCodes
WHERE codigo = prev_codigo AND codigo = prev_prev_codigo;
