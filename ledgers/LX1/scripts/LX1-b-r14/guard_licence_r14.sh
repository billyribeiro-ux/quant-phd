#!/bin/sh
# Round 14: (1) L04 twin guard on scratch copies with a blank GBP cell and a non-decimal cell; (2) FRB licence page via plain curl.
# Usage: sh ledgers/LX1/scripts/LX1-b-r14/guard_licence_r14.sh <checkout>
ROOT="$1"; cd "$ROOT" || exit 1
O=ledgers/LX1/scripts/LX1-b-r14/out; PY="$ROOT/.venv/bin/python"
R=/tmp/lx1b-r14-guard; rm -rf "$R"; mkdir -p "$R/data"; cp tests/labs/LX1/lab-LX1-L04-1.py "$R/"
"$PY" -I - "$ROOT" "$R" <<'PYEOF'
import sys, csv
root, R = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(root + '/course/assets/data/market/fx_monthly.csv', encoding='utf-8')))
gi = rows[0].index('GBP')
blank = [r[:] for r in rows]; blank[100][gi] = ''
open(R + '/data/blank.csv', 'w', newline='', encoding='utf-8').write('\n'.join(','.join(r) for r in blank) + '\n')
txt = [r[:] for r in rows]; txt[200][gi] = '1.2e0'
open(R + '/data/expo.csv', 'w', newline='', encoding='utf-8').write('\n'.join(','.join(r) for r in txt) + '\n')
PYEOF
cd "$R" || exit 1
for f in blank expo; do
  sed "s#\"fx_monthly.csv\"#\"$f.csv\"#" lab-LX1-L04-1.py > run_$f.py
  "$PY" -I -W error run_$f.py > out_$f.txt 2> err_$f.txt; echo "$f exit=$?" ; tail -1 err_$f.txt
done
cp err_blank.txt "$ROOT/$O/guard_blank.err"; cp err_expo.txt "$ROOT/$O/guard_expo.err"
cd "$ROOT" || exit 1
curl -sS -L -m 60 -o /tmp/lx1b-r14-disclaimer.html -w "HTTP %{http_code}\n" https://www.federalreserve.gov/disclaimer.htm > "$O/curl_fed_disclaimer_code.out" 2>&1
cat "$O/curl_fed_disclaimer_code.out"
grep -o "Unless otherwise indicated, information on Board[^<]\{0,200\}" /tmp/lx1b-r14-disclaimer.html | head -1 > "$O/fed_licence_quote.out"
cat "$O/fed_licence_quote.out"
