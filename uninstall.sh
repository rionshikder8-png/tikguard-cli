#!/usr/bin/env sh
# Removes only the launcher command. Your data in ~/.tikguard is KEPT.
set -eu
for BIN in "${PREFIX:-/nonexistent}/bin" "$HOME/.local/bin"; do
  [ -f "$BIN/tikguard" ] && rm -f "$BIN/tikguard" && echo "Removed $BIN/tikguard"
done
echo "Your cases in ~/.tikguard were NOT deleted."
echo "To delete them too: rm -r ~/.tikguard   (this cannot be undone)"
echo "To delete the app: remove the cloned folder yourself."
