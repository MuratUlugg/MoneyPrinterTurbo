#!/bin/sh
# Hediye Arenası: ilk çalıştırmada kurar, sonra paneli açar. Python 3.11+ gerekir.
set -e
cd "$(dirname "$0")/.."
if [ ! -d live_overlay/.venv ]; then
  echo "İlk kurulum yapılıyor, birkaç dakika sürebilir..."
  python3 -m venv live_overlay/.venv
  live_overlay/.venv/bin/python -m pip install --upgrade pip
  live_overlay/.venv/bin/python -m pip install -r live_overlay/requirements.txt
fi
(sleep 2; (command -v xdg-open >/dev/null && xdg-open http://127.0.0.1:8765/) || (command -v open >/dev/null && open http://127.0.0.1:8765/) || true) &
exec live_overlay/.venv/bin/python -m live_overlay.server "$@"
