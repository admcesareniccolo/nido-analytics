"""Project paths, so every script works from the repository root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "nido.duckdb"
RAW_DIR = ROOT / "data" / "raw"
INCOMING_DIR = ROOT / "data" / "incoming"
SEEDS_DIR = ROOT / "seeds"
SQL_DIR = ROOT / "sql"
SCHEMAS = ("raw", "seeds", "staging", "marts")
