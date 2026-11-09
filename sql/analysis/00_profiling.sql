-- 00_profiling: first look at the raw extracts (run with: python -m nido.query sql/analysis/00_profiling.sql)

-- 1) Row counts per raw table
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM raw.customers
UNION ALL SELECT 'products', COUNT(*) FROM raw.products
UNION ALL SELECT 'orders', COUNT(*) FROM raw.orders
UNION ALL SELECT 'order_items', COUNT(*) FROM raw.order_items
UNION ALL SELECT 'returns', COUNT(*) FROM raw.returns
UNION ALL SELECT 'marketing_spend', COUNT(*) FROM raw.marketing_spend;

-- 2) Date range of orders and duplicate order rows
SELECT
    MIN(order_ts)                       AS first_order,
    MAX(order_ts)                       AS last_order,
    COUNT(*) - COUNT(DISTINCT order_id) AS duplicate_order_rows
FROM raw.orders;

-- 3) How is ship_country spelled?
SELECT ship_country, COUNT(*) AS orders
FROM raw.orders
GROUP BY ship_country
ORDER BY orders DESC;

-- 4) Orders by status and invalid order lines
SELECT status, COUNT(*) AS orders FROM raw.orders GROUP BY status ORDER BY orders DESC;
SELECT COUNT(*) AS invalid_lines FROM raw.order_items WHERE quantity <= 0;
