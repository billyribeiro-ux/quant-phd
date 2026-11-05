#!/bin/sh
# LX1-b round 13: rebuild fx_monthly from the live issuer feed in a scratch copy (git archive of the pin),
# compare the snapshot bytes, and fetch the issuer licence page with plain curl. Usage: sh <this file> <checkout> <scratch>
CK="$1"; S="$2"; PY="$CK/.venv/bin/python"; O="$CK/ledgers/LX1/scripts/LX1-b-r13/out"
rm -rf "$S" && mkdir -p "$S" && git -C "$CK" archive e919577 | tar -x -C "$S"
(cd "$S" && "$PY" -I tools/fetch_data.py --fetch --only fx_monthly > "$O/fetch_rebuild_fx_monthly_r13.out" 2>&1; echo "exit=$?" >> "$O/fetch_rebuild_fx_monthly_r13.out")
sha256sum "$S/course/assets/data/market/fx_monthly.csv" "$CK/course/assets/data/market/fx_monthly.csv" >> "$O/fetch_rebuild_fx_monthly_r13.out"
curl -sS -L -o "$S/fed_disclaimer.html" -w "%{http_code}\n" https://www.federalreserve.gov/disclaimer.htm > "$O/curl_fed_disclaimer_code.out" 2>&1
grep -o "is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information" "$S/fed_disclaimer.html" > "$O/fed_licence_quote.out" 2>&1
