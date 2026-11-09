"""Data quality checks on the staging layer.

    python -m nido.checks

Each check returns a list of failure messages (an empty list means the check passed).
The script exits with code 1 if any check fails, so CI can block a pull request.

TODO (ticket S2-5): implement the four check_* functions so that `pytest` passes.
"""
import sys

import duckdb
import pandas as pd

from nido.config import DB_PATH

COUNTRIES = {"DE", "AT", "NL", "FR", "IT"}
STATUSES = {"delivered", "shipped", "cancelled", "pending"}


def check_unique(df: pd.DataFrame, column: str) -> list[str]:
    """Fail if the column contains duplicate values.

    Example message: "order_id: 3 duplicate values"
    """
    raise NotImplementedError


def check_not_null(df: pd.DataFrame, columns: list[str]) -> list[str]:
    """One failure message per column that contains nulls.

    Example message: "customer_id: 2 null values"
    """
    raise NotImplementedError


def check_allowed_values(df: pd.DataFrame, column: str, allowed: set) -> list[str]:
    """Fail if the column (ignoring nulls) contains values outside `allowed`.

    Example message: "ship_country_code: unexpected values ['Germany']"
    """
    raise NotImplementedError


def check_min(df: pd.DataFrame, column: str, minimum: float) -> list[str]:
    """Fail if some values are below `minimum`.

    Example message (must match exactly): "quantity: 2 values below 1"
    """
    raise NotImplementedError


def run_checks(con) -> list[str]:
    orders = con.sql("SELECT * FROM staging.stg_orders").df()
    items = con.sql("SELECT * FROM staging.stg_order_items").df()
    customers = con.sql("SELECT * FROM staging.stg_customers").df()
    results = {
        "stg_orders": check_unique(orders, "order_id")
        + check_not_null(orders, ["order_id", "customer_id", "order_ts"])
        + check_allowed_values(orders, "ship_country_code", COUNTRIES)
        + check_allowed_values(orders, "status", STATUSES),
        "stg_order_items": check_unique(items, "order_item_id") + check_min(items, "quantity", 1),
        "stg_customers": check_unique(customers, "customer_id")
        + check_allowed_values(customers, "country_code", COUNTRIES),
    }
    failures = []
    for table, messages in results.items():
        print(f"{'PASS' if not messages else 'FAIL'}  {table}")
        failures += [f"{table}.{m}" for m in messages]
    return failures


def main() -> None:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    failures = run_checks(con)
    con.close()
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
