"""SQLite storage. All queries are parameterized."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def data_dir() -> Path:
    """Local data directory (never inside the Git-tracked source)."""
    override = os.environ.get("TIKGUARD_HOME")
    base = Path(override) if override else Path.home() / ".tikguard"
    base.mkdir(parents=True, exist_ok=True)
    return base


def db_path() -> Path:
    return data_dir() / "cases.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    category TEXT NOT NULL,
    profile_url TEXT NOT NULL,
    description TEXT NOT NULL,
    evidence TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    submitted INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path) if path else str(db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    conn.commit()
    return conn
