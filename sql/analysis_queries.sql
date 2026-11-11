-- Retail Sales Analysis SQL
-- Run after importing data/retail_sales.csv into a table named retail_sales.
-- Syntax is broadly compatible with PostgreSQL; adjust date functions for other databases.

-- 1. Overall business KPIs
SELECT
    SUM(revenue_lkr) AS total_revenue_lkr,
    SUM(profit_lkr) AS total_profit_lkr,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(100.0 * SUM(profit_lkr) / NULLIF(SUM(revenue_lkr), 0), 2) AS profit_margin_pct
FROM retail_sales;

-- 2. Monthly revenue and profit
SELECT
    DATE_TRUNC('month', order_date::date) AS sales_month,
    SUM(revenue_lkr) AS revenue_lkr,
    SUM(profit_lkr) AS profit_lkr
FROM retail_sales
GROUP BY 1
ORDER BY 1;

-- 3. Category performance
SELECT category, SUM(revenue_lkr) AS revenue_lkr,
       SUM(profit_lkr) AS profit_lkr,
       SUM(quantity) AS units_sold
FROM retail_sales
GROUP BY category
ORDER BY revenue_lkr DESC;

-- 4. Regional performance
SELECT region, SUM(revenue_lkr) AS revenue_lkr,
       COUNT(DISTINCT order_id) AS orders
FROM retail_sales
GROUP BY region
ORDER BY revenue_lkr DESC;

-- 5. Sales channel comparison
SELECT sales_channel, SUM(revenue_lkr) AS revenue_lkr,
       AVG(revenue_lkr) AS average_order_value
FROM retail_sales
GROUP BY sales_channel
ORDER BY revenue_lkr DESC;

-- 6. Top 10 products
SELECT product, SUM(quantity) AS units_sold,
       SUM(revenue_lkr) AS revenue_lkr
FROM retail_sales
GROUP BY product
ORDER BY revenue_lkr DESC
LIMIT 10;
