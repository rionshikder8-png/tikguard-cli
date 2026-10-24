#!/usr/bin/env sh
# Launcher: run from anywhere inside or outside the repo.
DIR="$(cd "$(dirname "$0")" && pwd)"
if ! command -v python >/dev/null 2>&1 && ! command -v python3 >/dev/null 2>&1; then
  echo "Python not found. Run: pkg install python"
  exit 1
fi
PY="$(command -v python3 || command -v python)"
exec "$PY" "$DIR/main.py" "$@"
