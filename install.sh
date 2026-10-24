#!/usr/bin/env sh
# TikGuard installer (review before running). No root, no sudo, no remote code.
set -eu
DIR="$(cd "$(dirname "$0")" && pwd)"

if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
  echo "Python is missing. Run: pkg update && pkg install python git"
  exit 1
fi
PY="$(command -v python3 || command -v python)"

chmod +x "$DIR/tikguard.sh" "$DIR/main.py"

# Optional: install a 'tikguard' command in $PREFIX/bin (Termux) or ~/.local/bin
if [ -n "${PREFIX:-}" ] && [ -d "$PREFIX/bin" ]; then
  BIN="$PREFIX/bin"
else
  BIN="$HOME/.local/bin"; mkdir -p "$BIN"
fi
printf '#!/usr/bin/env sh\nexec "%s/tikguard.sh" "$@"\n' "$DIR" > "$BIN/tikguard"
chmod +x "$BIN/tikguard"

"$PY" "$DIR/main.py" --version
echo "Installed. Start with: tikguard   (or: ./tikguard.sh)"
echo "No third-party packages are required."
