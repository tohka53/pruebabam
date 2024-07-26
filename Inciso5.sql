WITH ComprasCliente AS (
    SELECT
        C.CustomerID,
        CONCAT(P.FirstName, ' ', P.LastName) AS NombreCliente,
        SOH.OrderDate,
        DATE_FORMAT(SOH.OrderDate, '%Y-%m') AS Mes,
        ROW_NUMBER() OVER (PARTITION BY C.CustomerID ORDER BY SOH.OrderDate DESC) AS Rnk
    FROM SalesOrderHeader SOH
    INNER JOIN Customer C ON SOH.CustomerID = C.CustomerID
    INNER JOIN Person P ON C.PersonID = P.BusinessEntityID
),
UltimasCompras AS (
    SELECT
        CustomerID,
        NombreCliente,
        Mes,
        OrderDate AS FechaUltCompra,
        LAG(OrderDate, 1) OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS FechaPenUltCompra,
        LAG(OrderDate, 2) OVER (PARTITION BY CustomerID ORDER BY OrderDate DESC) AS FechaAntePenUltCompra
    FROM ComprasCliente
    WHERE Rnk <= 3
)
SELECT
    Mes,
    NombreCliente,
    FechaUltCompra,
    DATEDIFF(FechaUltCompra, FechaPenUltCompra) AS DiasUC_PC,
    DATEDIFF(FechaPenUltCompra, FechaAntePenUltCompra) AS DiasPC_APC
FROM UltimasCompras
WHERE FechaUltCompra IS NOT NULL
ORDER BY Mes, NombreCliente;
