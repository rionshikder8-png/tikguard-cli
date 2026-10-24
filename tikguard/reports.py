"""Genuine report assistant. Prepares a LOCAL case only; never submits."""
from __future__ import annotations

from . import cases
from .scanner import is_tiktok_profile_url

REPORT_CATEGORIES = {
    "1": ("impersonation", "Impersonation (pretending to be someone else)"),
    "2": ("scam", "Scam or fraud"),
    "3": ("harassment", "Harassment or bullying"),
    "4": ("spam", "Spam or fake engagement"),
    "5": ("other-violation", "Other genuine policy violation"),
}

OFFICIAL_LINKS = {
    "How to report (TikTok Help Center)":
        "https://support.tiktok.com/en/safety-hc/report-a-problem",
    "Community Guidelines":
        "https://www.tiktok.com/community-guidelines",
}

NOTICE = (
    "A case saved here is only a LOCAL preparation. It is NOT a report sent "
    "to TikTok. Submit it yourself in the TikTok app or the official Help "
    "Center. Report only real violations, once per issue."
)


def prepare_report(category_key: str, profile_url: str, description: str,
                   evidence: str = "", notes: str = "") -> int:
    if category_key not in REPORT_CATEGORIES:
        raise ValueError("Unknown report category.")
    if not is_tiktok_profile_url(profile_url):
        raise ValueError("Profile URL must look like https://www.tiktok.com/@name")
    if len((description or "").strip()) < 10:
        raise ValueError("Please describe the actual violation (10+ characters).")
    return cases.create_case(
        "report", REPORT_CATEGORIES[category_key][0], profile_url,
        description, evidence, notes,
    )
