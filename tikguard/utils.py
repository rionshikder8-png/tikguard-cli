"""Shared helpers: colors, terminal width, URL opening, safe input."""
from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import sys
import webbrowser
from typing import Optional

USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

_CODES = {
    "reset": "0", "bold": "1", "red": "31", "green": "32",
    "yellow": "33", "blue": "34", "magenta": "35", "cyan": "36",
}


def color(text: str, name: str) -> str:
    """Wrap text in an ANSI color when the terminal supports it."""
    if not USE_COLOR or name not in _CODES:
        return text
    return f"\033[{_CODES[name]}m{text}\033[0m"


def term_width(default: int = 60) -> int:
    width = shutil.get_terminal_size((default, 24)).columns
    return max(30, min(width, 100))


def rule(char: str = "-") -> str:
    return char * term_width()


def wrap(text: str, indent: int = 0) -> str:
    import textwrap
    return textwrap.fill(
        text, width=term_width() - indent, initial_indent=" " * indent,
        subsequent_indent=" " * indent,
    )


def is_termux() -> bool:
    return "com.termux" in os.environ.get("PREFIX", "") or bool(
        os.environ.get("TERMUX_VERSION")
    )


def open_url(url: str) -> bool:
    """Open a URL using termux-open-url if present, else the default browser.

    Returns True if a handler was launched. Never raises.
    """
    if not url.startswith("https://"):
        return False
    try:
        if shutil.which("termux-open-url"):
            subprocess.run(["termux-open-url", url], check=False, timeout=15)
            return True
        return bool(webbrowser.open(url))
    except (OSError, subprocess.SubprocessError, webbrowser.Error):
        return False


def ask(prompt: str, default: str = "") -> str:
    """Read a line of input; EOF is treated as an interrupt."""
    try:
        value = input(prompt).strip()
    except EOFError:
        raise KeyboardInterrupt
    return value or default


def clean_text(value: str, max_len: int = 2000) -> str:
    """Strip control characters and limit length."""
    value = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", value or "")
    return value.strip()[:max_len]


def python_info() -> str:
    return f"{platform.python_version()} ({platform.system()})"


def has_module(name: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(name) is not None


def optional(env_name: str) -> Optional[str]:
    return os.environ.get(env_name)
