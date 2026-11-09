-- stg_products: product catalogue
CREATE OR REPLACE TABLE staging.stg_products AS
SELECT
    product_id,
    product_name,
    category,
    unit_cost_eur,
    list_price_eur,
    CAST(launched_at AS DATE) AS launched_at,
    is_active
FROM raw.products;
