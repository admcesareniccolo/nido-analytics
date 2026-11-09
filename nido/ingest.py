"""Incremental load: append monthly data drops from data/incoming to the raw tables.

A drop file is named <table>_<YYYY-MM>.csv, for example orders_2026-10.csv.
Rows whose key is already loaded (late re-sends) and duplicates inside a file are skipped.
"""
import re
from pathlib import Path

import pandas as pd

KEYS = {"orders": "order_id", "order_items": "order_item_id"}
FILE_PATTERN = re.compile(r"^(?P<table>[a-z_]+)_(?P<period>\d{4}-\d{2})\.csv$")


def parse_drop_name(file_name: str) -> tuple[str, str] | None:
    """Return (table, period) for a valid drop file name, otherwise None.

    Valid: "orders_2026-10.csv" -> ("orders", "2026-10"). Only tables listed in KEYS are valid.
    TODO (ticket S3-4): implement it (tip: FILE_PATTERN above).
    """
    raise NotImplementedError


def filter_new_rows(new_df: pd.DataFrame, existing_keys: set, key: str) -> pd.DataFrame:
    """Keep only rows whose key is not loaded yet, one row per key, with a clean 0..n index.

    TODO (ticket S3-4): implement it with pandas.
    """
    raise NotImplementedError


def ingest_incoming(con, incoming_dir: Path) -> int:
    """Append every valid drop file to its raw table. Returns the number of new rows."""
    con.execute(
        "CREATE TABLE IF NOT EXISTS raw.load_log "
        "(file_name VARCHAR, table_name VARCHAR, rows_loaded INTEGER, loaded_at TIMESTAMP)"
    )
    total = 0
    for path in sorted(Path(incoming_dir).glob("*.csv")):
        parsed = parse_drop_name(path.name)
        if parsed is None:
            print(f"  skipped {path.name}: unknown file name")
            continue
        table, _period = parsed
        key = KEYS[table]
        existing = {row[0] for row in con.execute(f"SELECT {key} FROM raw.{table}").fetchall()}
        new_keys = filter_new_rows(pd.read_csv(path, dtype=str), existing, key)[[key]]
        con.register("new_keys", new_keys)
        con.execute(
            f"""
            INSERT INTO raw.{table}
            SELECT * EXCLUDE (rn) FROM (
                SELECT d.*, ROW_NUMBER() OVER (PARTITION BY d.{key}) AS rn
                FROM read_csv_auto('{path.as_posix()}', header = true) AS d
                WHERE d.{key} IN (SELECT {key} FROM new_keys)
            )
            WHERE rn = 1
            """
        )
        con.unregister("new_keys")
        con.execute("INSERT INTO raw.load_log VALUES (?, ?, ?, now())", [path.name, table, len(new_keys)])
        print(f"  {path.name}: {len(new_keys):,} new rows -> raw.{table}")
        total += len(new_keys)
    return total
