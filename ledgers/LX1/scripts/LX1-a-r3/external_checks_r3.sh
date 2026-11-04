#!/bin/bash
# Round-3 plain-curl checks (no bot check, login or paywall touched). Run from the checkout root.
set -u
OUT=ledgers/LX1/scripts/LX1-a-r3/out
mkdir -p "$OUT/licence"
echo "URL https://www.federalreserve.gov/disclaimer.htm"
curl -sS -L --max-time 30 -o "$OUT/licence/disclaimer.htm" -w "HTTP %{http_code}\n" https://www.federalreserve.gov/disclaimer.htm
grep -o "Unless otherwise indicated[^<]*" "$OUT/licence/disclaimer.htm" | head -1 | cut -c1-200
echo "URL https://api.crossref.org/works/10.1515/9781400831722 (reinhart2009this DOI)"
curl -sS --max-time 30 -o "$OUT/licence/reinhart_crossref.json" -w "HTTP %{http_code}\n" "https://api.crossref.org/works/10.1515/9781400831722"
python3 -I -c "
import json,sys
m=json.load(open(sys.argv[1]))['message']
print('title', m.get('title'), '| subtitle', m.get('subtitle'))
print('authors', [a.get('family') for a in m.get('author',[])], 'issued', m.get('issued',{}).get('date-parts'))
" "$OUT/licence/reinhart_crossref.json"
