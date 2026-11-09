# Data dictionary

## Raw extracts (`data/raw`)
| Table | Grain | Notes |
|---|---|---|
| `customers` | one row per customer | `country` has inconsistent spellings; `customer_type = internal_test` are QA accounts |
| `products` | one row per product | prices include VAT; `unit_cost_eur` excludes VAT |
| `orders` | one row per order (**with duplicates**) | double-loaded rows from the source system; `ship_country` spellings vary |
| `order_items` | one row per order line | a few lines have `quantity <= 0` (system errors) |
| `returns` | one row per returned line | `refund_eur` includes VAT |
| `marketing_spend` | one row per day and channel | paid channels only |

## Staging, marts and metric definitions
TODO (ticket S4-4)
