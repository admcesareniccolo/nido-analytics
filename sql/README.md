# SQL conventions (from Marco)

- **One model per file**, named like the table it creates: `sql/staging/stg_orders.sql` → `staging.stg_orders`.
- Every model starts with a one-line comment and uses `CREATE OR REPLACE TABLE <schema>.<model> AS ...`.
- `python -m nido.pipeline` runs `staging/` then `marts/`, each in **alphabetical order**:
  a model can only use models that run before it.
- Explicit column lists (no `SELECT *` in final selects), lowercase snake_case names, `_eur` suffix for money.
- `sql/analysis/` holds ad-hoc queries: they are **not** run by the pipeline. Run them with
  `python -m nido.query sql/analysis/<file>.sql`.
- Schemas: `raw` (CSV as-is), `seeds` (reference CSVs in `seeds/`), `staging` (clean), `marts` (business).

`stg_products.sql` is a complete example to copy.
