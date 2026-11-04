#!/bin/bash
# Plain curl of the Federal Reserve licence page cited by the hub and the fx_monthly MANIFEST entry, then a quote search.
set -u
OUT=ledgers/LX1/scripts/LX1-a-r2/out/licence
mkdir -p "$OUT"
curl -sS -L --max-time 30 -o "$OUT/disclaimer.htm" -w 'HTTP %{http_code} bytes %{size_download}\n' https://www.federalreserve.gov/disclaimer.htm
.venv/bin/python -I - "$OUT/disclaimer.htm" <<'PY'
import sys, re, html
t = open(sys.argv[1], encoding="utf-8", errors="replace").read()
t2 = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).replace("’", "'")
s = "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission"
print("quote present:", s in t2)
PY
