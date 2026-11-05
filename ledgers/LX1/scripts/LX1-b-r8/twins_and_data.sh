#!/bin/sh
# LX1-b round 8: run each lab twin alone under python -I -W error in a scratch dir holding only its data,
# check the fx_monthly CSV against MANIFEST, and re-check the Federal Reserve licence quote with plain curl.
# Usage: sh twins_and_data.sh <checkout> <scratch>
CK="$1"; SC="$2"; OUT="$CK/ledgers/LX1/scripts/LX1-b-r8/out"
rm -rf "$SC" && mkdir -p "$SC/L03" "$SC/L04/data" && cp "$CK/course/assets/data/market/fx_monthly.csv" "$SC/L04/data/"
(cd "$SC/L03" && python3 -I -W error "$CK/tests/labs/LX1/lab-LX1-L03-1.py" > "$OUT/twin_L03.out" 2> "$OUT/twin_L03.err"; echo "L03 exit $?")
(cd "$SC/L04" && python3 -I -W error "$CK/tests/labs/LX1/lab-LX1-L04-1.py" > "$OUT/twin_L04.out" 2> "$OUT/twin_L04.err"; echo "L04 exit $?")
sha256sum "$CK/course/assets/data/market/fx_monthly.csv"
python3 -I -c "
import json,sys
m=json.load(open(sys.argv[1]))
e=[d for d in m['datasets'] if d['id']=='fx_monthly'][0]
print('MANIFEST fx_monthly sha256', e['sha256'], 'rows', e['rows'], 'first', e['first'], 'last', e['last'], 'retrieved', e['retrieved'])
" "$CK/course/assets/data/market/MANIFEST.json"
curl -sS -L https://www.federalreserve.gov/disclaimer.htm -o "$SC/disclaimer.htm" -w 'HTTP %{http_code}\n'
grep -o -i "Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission" "$SC/disclaimer.htm" | head -1
