"""Username syntax validation and profile URL generation.

Nothing here contacts TikTok. A valid syntax does NOT prove an account exists.
"""
from __future__ import annotations

import re

# TikTok usernames: 2-24 chars, letters, digits, underscores, periods.
# Cannot end with a period.
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]{2,24}$")


def normalize_username(raw: str) -> str:
    return (raw or "").strip().lstrip("@")


def validate_username(raw: str) -> tuple[bool, str]:
    """Return (ok, message)."""
    name = normalize_username(raw)
    if not name:
        return False, "Username is empty."
    if len(name) < 2 or len(name) > 24:
        return False, "Username must be 2 to 24 characters."
    if not _USERNAME_RE.match(name):
        return False, "Only letters, digits, underscore and period are allowed."
    if name.endswith("."):
        return False, "Username cannot end with a period."
    return True, "Valid username syntax."


def profile_url(raw: str) -> str:
    ok, msg = validate_username(raw)
    if not ok:
        raise ValueError(msg)
    return f"https://www.tiktok.com/@{normalize_username(raw)}"


def is_tiktok_profile_url(url: str) -> bool:
    return bool(re.match(
        r"^https://(www\.|m\.)?tiktok\.com/@[A-Za-z0-9_.]{2,24}/?$",
        (url or "").strip(),
    ))
