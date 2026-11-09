"""Run the statements of a .sql file against nido.duckdb and print the results.

    python -m nido.query sql/analysis/monthly_kpis.sql
"""
import sys
from pathlib import Path

import duckdb

from nido.config import DB_PATH


def split_statements(sql: str) -> list[str]:
    """Split a script on semicolons, ignoring comment-only chunks."""
    chunks = [c.strip() for c in sql.split(";")]
    return [c for c in chunks if any(line.strip() and not line.strip().startswith("--") for line in c.splitlines())]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m nido.query path/to/file.sql")
    sql = Path(sys.argv[1]).read_text(encoding="utf-8")
    con = duckdb.connect(str(DB_PATH), read_only=True)
    for statement in split_statements(sql):
        print(con.sql(statement).df().to_string(index=False, max_rows=60))
        print()
    con.close()


if __name__ == "__main__":
    main()
