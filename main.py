#!/usr/bin/env python3
"""Entry point: python main.py"""
import sys

if sys.version_info < (3, 8):
    sys.exit("TikGuard needs Python 3.8+. Run: pkg install python")

from tikguard.cli import main

if __name__ == "__main__":
    sys.exit(main())
