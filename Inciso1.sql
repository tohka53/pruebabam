SELECT 
    DATE_FORMAT(SOH.OrderDate, '%Y-%m') AS Mes,
    ST.Name AS NombreTerritorio,
    SUM(CASE WHEN SOH.Status = 1 THEN 1 ELSE 0 END) AS TrProceso,
    SUM(CASE WHEN SOH.Status = 2 THEN 1 ELSE 0 END) AS TrAprobadas,
    SUM(CASE WHEN SOH.Status = 3 THEN 1 ELSE 0 END) AS TrAtrasadas,
    SUM(CASE WHEN SOH.Status = 4 THEN 1 ELSE 0 END) AS TrRechazadas,
    SUM(CASE WHEN SOH.Status = 5 THEN 1 ELSE 0 END) AS TrEnviadas,
    SUM(CASE WHEN SOH.Status = 6 THEN 1 ELSE 0 END) AS TrCanceladas,
    SUM(CASE WHEN SOH.Status = 1 THEN SOH.TotalDue ELSE 0 END) AS MntProceso,
    SUM(CASE WHEN SOH.Status = 2 THEN SOH.TotalDue ELSE 0 END) AS MntAprobadas,
    SUM(CASE WHEN SOH.Status = 3 THEN SOH.TotalDue ELSE 0 END) AS MntAtrasadas,
    SUM(CASE WHEN SOH.Status = 4 THEN SOH.TotalDue ELSE 0 END) AS MntRechazadas,
    SUM(CASE WHEN SOH.Status = 5 THEN SOH.TotalDue ELSE 0 END) AS MntEnviadas,
    SUM(CASE WHEN SOH.Status = 6 THEN SOH.TotalDue ELSE 0 END) AS MntCanceladas
FROM 
    SalesOrderHeader SOH
JOIN 
    SalesTerritory ST ON SOH.TerritoryID = ST.TerritoryID
GROUP BY 
    DATE_FORMAT(SOH.OrderDate, '%Y-%m'), ST.Name
ORDER BY 
    Mes, NombreTerritorio;
    
    