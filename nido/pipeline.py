"""Build the local analytics database.

    python -m nido.pipeline

Steps: raw CSVs -> seeds -> incoming monthly drops -> sql/staging -> sql/marts.
The database file (nido.duckdb) is rebuilt from scratch on every run.
"""
import time
from pathlib import Path

import duckdb

from nido.config import DB_PATH, INCOMING_DIR, RAW_DIR, SCHEMAS, SEEDS_DIR, SQL_DIR
from nido.ingest import ingest_incoming


def load_csv_folder(con: duckdb.DuckDBPyConnection, folder: Path, schema: str) -> None:
    """Create one table per CSV file in the folder, named after the file."""
    for path in sorted(folder.glob("*.csv")):
        con.execute(
            f"CREATE OR REPLACE TABLE {schema}.{path.stem} AS "
            f"SELECT * FROM read_csv_auto('{path.as_posix()}', header = true)"
        )
        rows = con.execute(f"SELECT COUNT(*) FROM {schema}.{path.stem}").fetchone()[0]
        print(f"  {schema}.{path.stem:<22} {rows:>8,} rows")


def run_sql_folder(con: duckdb.DuckDBPyConnection, folder: Path) -> None:
    """Run every .sql file of a folder in alphabetical order (one model per file)."""
    for path in sorted(folder.glob("*.sql")):
        start = time.perf_counter()
        con.execute(path.read_text(encoding="utf-8"))
        print(f"  ran {path.relative_to(SQL_DIR)} in {time.perf_counter() - start:.2f}s")


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    con = duckdb.connect(str(DB_PATH))
    for schema in SCHEMAS:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

    print("1/5 Loading raw extracts")
    load_csv_folder(con, RAW_DIR, "raw")
    print("2/5 Loading seeds")
    load_csv_folder(con, SEEDS_DIR, "seeds")
    print("3/5 Ingesting monthly drops from data/incoming")
    new_rows = ingest_incoming(con, INCOMING_DIR)
    print(f"  {new_rows:,} new rows appended")
    print("4/5 Building staging models")
    run_sql_folder(con, SQL_DIR / "staging")
    print("5/5 Building marts")
    run_sql_folder(con, SQL_DIR / "marts")

    con.close()
    print(f"Done: {DB_PATH.name} is ready")


if __name__ == "__main__":
    main()
