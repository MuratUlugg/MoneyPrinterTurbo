#!/bin/sh
# QA kapısı: birim testleri + tarayıcı duman testi. Gerçek yayın verisine dokunmaz (geçici klasör, ayrı port).
# Kullanım: live_overlay/qa/run.sh [python-yolu] [gorsel]    Gerekenler: pytest, node + playwright.
cd "$(dirname "$0")/../.." || exit 2
PY="${1:-python3}"; OUT="${QA_OUT:-/tmp/hediye-qa}"; PORT=8766
"$PY" -m pytest -q test/services/test_live_overlay.py || { echo "QA BAŞARISIZ: birim testleri"; exit 1; }
DATA="$(mktemp -d)"
LIVE_OVERLAY_DATA="$DATA" "$PY" -m live_overlay.server --port $PORT >"$DATA/server.log" 2>&1 &
PID=$!; sleep 3
if [ "$2" = "gorsel" ]; then SCRIPT=visual.js; else SCRIPT=smoke.js; fi  # "gorsel": yalnızca görsel denetim çekimleri
QA_BASE="http://127.0.0.1:$PORT" QA_OUT="$OUT" node live_overlay/qa/$SCRIPT; RC=$?
kill $PID 2>/dev/null; rm -rf "$DATA"
echo "Ekran görüntüleri: $OUT"; exit $RC
