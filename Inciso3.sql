SELECT 
    DATE_FORMAT(SOH.OrderDate, '%Y-%m') AS OrderMonth,
    ST.Group AS TerritoryGroup,
    AVG(SOH.SubTotal) AS TerritoryMonthAvg,
    (SELECT AVG(SubTotal)
     FROM SalesOrderHeader
     WHERE OrderDate BETWEEN '2014-01-07'    AND '2014-07-07'
    ) AS OrgMonthAvg,
    (AVG(SOH.SubTotal) - 
        (SELECT AVG(SubTotal)
         FROM SalesOrderHeader
         WHERE OrderDate BETWEEN '2014-01-07'    AND '2014-07-07'
        )
    ) AS Diff,
    CASE 
        WHEN AVG(SOH.SubTotal) > 
            (SELECT AVG(SubTotal)
             FROM SalesOrderHeader
             WHERE OrderDate BETWEEN '2014-01-07'    AND '2014-07-07'
            ) 
        THEN 'Above' 
        ELSE 'Below' 
    END AS Indicator
FROM 
    SalesOrderHeader SOH
JOIN 
    SalesTerritory ST ON SOH.TerritoryID = ST.TerritoryID
WHERE 
    SOH.OrderDate BETWEEN '2014-01-07'    AND '2014-07-07'
GROUP BY 
    OrderMonth, TerritoryGroup
ORDER BY 
    OrderMonth, TerritoryGroup;
