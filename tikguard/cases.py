"""Local case manager: create, list, view, export, delete."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

from .storage import connect, data_dir
from .utils import clean_text

KINDS = ("report", "recovery", "note")
CATEGORIES = (
    "impersonation", "scam", "harassment", "spam",
    "other-violation", "account-recovery", "profile-note",
)


def create_case(kind: str, category: str, profile_url: str, description: str,
                evidence: str = "", notes: str = "",
                conn: Optional[sqlite3.Connection] = None) -> int:
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    if category not in CATEGORIES:
        raise ValueError(f"category must be one of {CATEGORIES}")
    description = clean_text(description)
    if not description:
        raise ValueError("Description is required.")
    own = conn is None
    conn = conn or connect()
    try:
        cur = conn.execute(
            "INSERT INTO cases (kind, category, profile_url, description, "
            "evidence, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (kind, category, clean_text(profile_url, 300), description,
             clean_text(evidence), clean_text(notes)),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        if own:
            conn.close()


def list_cases(conn: Optional[sqlite3.Connection] = None) -> list[dict]:
    own = conn is None
    conn = conn or connect()
    try:
        rows = conn.execute(
            "SELECT id, kind, category, profile_url, submitted, created_at "
            "FROM cases ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        if own:
            conn.close()


def get_case(case_id: int,
             conn: Optional[sqlite3.Connection] = None) -> Optional[dict]:
    own = conn is None
    conn = conn or connect()
    try:
        row = conn.execute(
            "SELECT * FROM cases WHERE id = ?", (int(case_id),)
        ).fetchone()
        return dict(row) if row else None
    finally:
        if own:
            conn.close()


def mark_submitted(case_id: int, value: bool = True,
                   conn: Optional[sqlite3.Connection] = None) -> bool:
    """User-confirmed flag: the user says they submitted it in the TikTok app."""
    own = conn is None
    conn = conn or connect()
    try:
        cur = conn.execute(
            "UPDATE cases SET submitted = ? WHERE id = ?",
            (1 if value else 0, int(case_id)),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        if own:
            conn.close()


def delete_case(case_id: int,
                conn: Optional[sqlite3.Connection] = None) -> bool:
    own = conn is None
    conn = conn or connect()
    try:
        cur = conn.execute("DELETE FROM cases WHERE id = ?", (int(case_id),))
        conn.commit()
        return cur.rowcount > 0
    finally:
        if own:
            conn.close()


def delete_all(conn: Optional[sqlite3.Connection] = None) -> int:
    own = conn is None
    conn = conn or connect()
    try:
        cur = conn.execute("DELETE FROM cases")
        conn.commit()
        return cur.rowcount
    finally:
        if own:
            conn.close()


def export_case(case_id: int, dest_dir: Optional[Path] = None,
                conn: Optional[sqlite3.Connection] = None) -> Path:
    case = get_case(case_id, conn)
    if case is None:
        raise KeyError(f"Case {case_id} not found.")
    folder = Path(dest_dir) if dest_dir else data_dir() / "exports"
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / f"case_{int(case_id)}.json"
    out.write_text(json.dumps(case, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    return out
