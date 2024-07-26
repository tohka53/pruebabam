WITH MonthlyProductSales AS (
    SELECT
        DATE_FORMAT(soh.OrderDate, '%Y-%m') AS Mes,
        p.Name AS Producto,
        SUM(sod.OrderQty) AS UnidadesDespachadas
    FROM
        SalesOrderDetail sod
    JOIN SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
    JOIN Product p ON sod.ProductID = p.ProductID
    WHERE
        soh.Status = 5
    GROUP BY
        DATE_FORMAT(soh.OrderDate, '%Y-%m'), p.Name
),
MonthlyCustomerSales AS (
    SELECT
        DATE_FORMAT(soh.OrderDate, '%Y-%m') AS Mes,
        c.CustomerID,
        SUM(soh.TotalDue) AS MontoFacturado
    FROM
        SalesOrderHeader soh
    JOIN Customer c ON soh.CustomerID = c.CustomerID
    WHERE
        soh.Status = 5
    GROUP BY
        DATE_FORMAT(soh.OrderDate, '%Y-%m'), c.CustomerID
),

TopCustomers AS (
    SELECT
        Mes,
        c.CustomerID,
        SUM(soh.TotalDue) AS MontoFacturado,
        p.FirstName,
        p.LastName,
        ROW_NUMBER() OVER (PARTITION BY Mes ORDER BY SUM(soh.TotalDue) DESC) AS CustomerRank
    FROM
        SalesOrderHeader soh
    JOIN Customer c ON soh.CustomerID = c.CustomerID
    JOIN Person p ON c.PersonID = p.BusinessEntityID
    WHERE
        soh.Status =5
    GROUP BY
        DATE_FORMAT(soh.OrderDate, '%Y-%m'), c.CustomerID, p.FirstName, p.LastName
