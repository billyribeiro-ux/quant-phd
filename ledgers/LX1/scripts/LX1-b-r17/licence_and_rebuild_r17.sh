#!/bin/bash
# LX1-b round 17: plain-curl licence check and a scratch rebuild of fx_monthly from the live feed.
# Usage: licence_and_rebuild_r17.sh <repo-root> <scratch-dir-that-does-not-exist>
set -eu
REPO="$1"; S="$2"
mkdir -p "$S/licence" "$S/rebuild/course/assets/data/market" "$S/rebuild/raw"
curl -sS -L --max-time 40 -o "$S/licence/disclaimer.htm" -w "HTTP %{http_code} %{url_effective}\n" https://www.federalreserve.gov/disclaimer.htm
python3 -I -c "
import re, html, sys
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
t = html.unescape(re.sub(r'<[^>]+>', ' ', t)); t = re.sub(r'\s+', ' ', t)
i = t.find('public domain'); print(t[max(0, i-60):i+200])
" "$S/licence/disclaimer.htm"
cp -R "$REPO/tools" "$S/rebuild/" && cp "$REPO/course/assets/data/market/"* "$S/rebuild/course/assets/data/market/"
cd "$S/rebuild" && "$REPO/.venv/bin/python" -I tools/fetch_data.py --fetch --only fx_monthly --keep-raw "$S/rebuild/raw"
sha256sum "$S/rebuild/course/assets/data/market/fx_monthly.csv" "$REPO/course/assets/data/market/fx_monthly.csv"
sha256sum "$S/rebuild/raw/fx_monthly.raw"
