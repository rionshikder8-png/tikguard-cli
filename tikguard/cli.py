"""Interactive terminal UI for TikGuard."""
from __future__ import annotations

import socket
import sys
from typing import Callable, Optional

from . import __version__, cases, recovery, reports, security
from .scanner import profile_url, validate_username
from .storage import data_dir, db_path
from .utils import (ask, clean_text, color, has_module, is_termux, open_url,
                    python_info, rule, wrap)

BANNER = r"""
 _____ _ _    ____                     _
|_   _(_) | _/ ___|_   _  __ _ _ __ __| |
  | | | | |/ / |  _| | | |/ _` | '__/ _` |
  | | | |   <| |_| | |_| | (_| | | | (_| |
  |_| |_|_|\_\\____|\__,_|\__,_|_|  \__,_|
"""

MENU = [
    ("1", "Username Scanner (syntax check + profile URL)"),
    ("2", "Report Assistant (prepare a genuine report)"),
    ("3", "Account Recovery Assistant"),
    ("4", "Security Center"),
    ("5", "Local Case Manager"),
    ("6", "Settings & Diagnostics"),
    ("7", "Help / সাহায্য"),
    ("0", "Exit"),
]


def show_banner() -> None:
    print(color(BANNER, "cyan"))
    print(color(f"TikGuard CLI v{__version__} - local safety helper", "bold"))
    print(rule("="))


def pause() -> None:
    ask("\nPress Enter to continue...")


def show_links(links: dict, open_choice: bool = True) -> None:
    items = list(links.items())
    for i, (label, url) in enumerate(items, 1):
        print(f" {i}. {label}\n    {color(url, 'blue')}")
    if open_choice:
        pick = ask("Open a link in browser? (number, or Enter to skip): ")
        if pick.isdigit() and 1 <= int(pick) <= len(items):
            if not open_url(items[int(pick) - 1][1]):
                print(color("Could not open a browser. Copy the link above.",
                            "yellow"))


# ---------------- Scanner ----------------
def scanner_menu() -> None:
    print(color("\n== Username Scanner ==", "bold"))
    print(wrap("This checks username SYNTAX only and builds a profile URL. "
               "It does NOT verify that an account exists."))
    raw = ask("TikTok username (with or without @): ")
    ok, msg = validate_username(raw)
    if not ok:
        print(color(f"Invalid: {msg}", "red"))
        return
    url = profile_url(raw)
    print(color(f"Valid syntax. URL: {url}", "green"))
    if ask("Open profile in browser? [y/N]: ").lower() == "y":
        if not open_url(url):
            print(color("Could not open browser. Copy the URL above.", "yellow"))
    note = clean_text(ask("Optional local note (Enter to skip): "))
    if note:
        cid = cases.create_case("note", "profile-note", url, note)
        print(color(f"Saved local note as case #{cid}.", "green"))


# ---------------- Reports ----------------
def report_menu() -> None:
    print(color("\n== Report Assistant ==", "bold"))
    print(wrap(reports.NOTICE))
    for key, (_, label) in reports.REPORT_CATEGORIES.items():
        print(f" {key}. {label}")
    cat = ask("Category number: ")
    if cat not in reports.REPORT_CATEGORIES:
        print(color("Invalid category.", "red"))
        return
    url = ask("Profile URL (https://www.tiktok.com/@name): ")
    desc = ask("Describe the ACTUAL violation: ")
    evidence = ask("Evidence references (e.g. screenshot file names, dates): ")
    notes = ask("Notes (optional): ")
    try:
        cid = reports.prepare_report(cat, url, desc, evidence, notes)
    except ValueError as exc:
        print(color(f"Not saved: {exc}", "red"))
        return
    print(color(f"Local report-preparation case #{cid} saved.", "green"))
    print(color("STATUS: prepared locally, NOT submitted to TikTok.", "yellow"))
    print("\nOfficial reporting resources:")
    show_links(reports.OFFICIAL_LINKS)
    if ask("Did you submit it yourself on TikTok? [y/N]: ").lower() == "y":
        cases.mark_submitted(cid)
        print("Marked as submitted (based on your confirmation).")


# ---------------- Recovery ----------------
def recovery_menu() -> None:
    print(color("\n== Account Recovery Assistant ==", "bold"))
    print(color(recovery.WARNING, "yellow"))
    print("\nChecklist:")
    for i, step in enumerate(recovery.CHECKLIST, 1):
        print(wrap(f"{i}. {step}", indent=1))
    print("\nOfficial resources:")
    show_links(recovery.OFFICIAL_LINKS)


# ---------------- Security ----------------
def security_menu() -> None:
    print(color("\n== Security Center ==", "bold"))
    for topic, tips in security.TOPICS.items():
        print(color(f"\n{topic}", "cyan"))
        for tip in tips:
            print(wrap(f"- {tip}", indent=1))
    print(color("\nChecklist:", "cyan"))
    for item in security.CHECKLIST:
        print(f" [ ] {item}")
    print("\n" + wrap(security.DISCLAIMER))
    show_links(security.OFFICIAL_LINKS)


# ---------------- Cases ----------------
def case_menu() -> None:
    while True:
        print(color("\n== Local Case Manager ==", "bold"))
        print(" 1. List cases\n 2. View case\n 3. Export case to JSON\n"
              " 4. Delete one case\n 5. Delete ALL cases\n 0. Back")
        choice = ask("Choose: ")
        if choice == "0":
            return
        if choice == "1":
            rows = cases.list_cases()
            if not rows:
                print("No cases stored.")
            for r in rows:
                state = "submitted(by you)" if r["submitted"] else "local only"
                print(f" #{r['id']} [{r['kind']}/{r['category']}] "
                      f"{r['created_at']} - {state}\n    {r['profile_url']}")
        elif choice in ("2", "3", "4"):
            raw = ask("Case ID: ")
            if not raw.isdigit():
                print(color("Case ID must be a number.", "red"))
                continue
            cid = int(raw)
            if choice == "2":
                case = cases.get_case(cid)
                if not case:
                    print(color("Case not found.", "red"))
                else:
                    for k, v in case.items():
                        print(f" {k}: {v}")
            elif choice == "3":
                try:
                    out = cases.export_case(cid)
                    print(color(f"Exported to {out}", "green"))
                    print("Note: export files are NOT in Git; delete them "
                          "when no longer needed.")
                except KeyError:
                    print(color("Case not found.", "red"))
            else:
                done = cases.delete_case(cid)
                print("Deleted." if done else color("Case not found.", "red"))
        elif choice == "5":
            if ask("Type DELETE to remove all cases: ") == "DELETE":
                print(f"Deleted {cases.delete_all()} case(s).")
            else:
                print("Cancelled.")
        else:
            print(color("Invalid choice.", "red"))


# ---------------- Diagnostics ----------------
def online() -> bool:
    try:
        socket.create_connection(("www.tiktok.com", 443), timeout=3).close()
        return True
    except OSError:
        return False


def diagnostics(check_network: bool = True) -> int:
    print(color("TikGuard diagnostics", "bold"))
    print(f" App version   : {__version__}")
    print(f" Python        : {python_info()}")
    print(f" Termux        : {'yes' if is_termux() else 'no / not detected'}")
    print(f" sqlite3       : {'ok' if has_module('sqlite3') else 'MISSING'}")
    rich = "installed" if has_module("rich") else "not installed (not needed)"
    print(f" rich (opt.)   : {rich}")
    print(" Link opener   : if links fail run 'pkg install termux-tools'")
    print(f" Data folder   : {data_dir()}")
    print(f" Database      : {db_path()}")
    if check_network:
        print(f" Network       : {'online' if online() else 'offline (local features still work)'}")
    return 0 if has_module("sqlite3") else 1


def settings_menu() -> None:
    print(color("\n== Settings & Diagnostics ==", "bold"))
    diagnostics()
    print("\nTroubleshooting:")
    for line in (
        "Links do not open: run 'pkg install termux-tools'.",
        "python not found: run 'pkg install python'.",
        "Offline: scanner, cases and guidance still work; only opening links needs internet.",
        "Remove all data: Case Manager > Delete ALL, or delete the ~/.tikguard folder.",
    ):
        print(wrap(f"- {line}", indent=1))


HELP = """
ENGLISH
 TikGuard helps you check username syntax, prepare GENUINE reports, follow
 official account-recovery steps and improve account security. It never asks
 for passwords/codes/tokens, never submits reports for you, and never contacts
 TikTok unless you choose to open a link. Cases are stored in ~/.tikguard.

বাংলা
 TikGuard দিয়ে আপনি ইউজারনেমের গঠন যাচাই, সত্যিকারের রিপোর্টের প্রস্তুতি,
 অফিসিয়াল অ্যাকাউন্ট রিকভারির ধাপ এবং নিরাপত্তার পরামর্শ পেতে পারেন।
 এটি কখনো পাসওয়ার্ড/কোড/টোকেন চায় না, নিজে থেকে রিপোর্ট পাঠায় না।
 কেস লোকাল ফোনে ~/.tikguard ফোল্ডারে থাকে। আপনি লিংক খুললেই কেবল ইন্টারনেট ব্যবহার হয়।
"""


def help_menu() -> None:
    print(HELP)


ACTIONS: dict[str, Callable[[], None]] = {
    "1": scanner_menu, "2": report_menu, "3": recovery_menu,
    "4": security_menu, "5": case_menu, "6": settings_menu, "7": help_menu,
}


def main_menu() -> int:
    while True:
        show_banner()
        for key, label in MENU:
            print(f" {color(key, 'green')}. {label}")
        choice = ask("\nSelect an option: ")
        if choice == "0":
            print("Goodbye! Stay safe.")
            return 0
        action = ACTIONS.get(choice)
        if action is None:
            print(color("Invalid selection. Enter a number from the menu.", "red"))
            continue
        action()
        if choice != "5":
            pause()


def main(argv: Optional[list[str]] = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        if argv and argv[0] in ("--version", "-V"):
            print(f"TikGuard CLI {__version__}")
            return 0
        if argv and argv[0] in ("diagnostics", "--diagnostics"):
            return diagnostics()
        if argv and argv[0] in ("--help", "-h", "help"):
            print("Usage: python main.py [diagnostics | --version | --help]")
            print(HELP)
            return 0
        return main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        return 130
