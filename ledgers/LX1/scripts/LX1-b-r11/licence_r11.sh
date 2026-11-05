#!/bin/sh
# LX1-b round 11: plain curl of the fx_monthly licence_url (tools/data_sources.yaml, MANIFEST) and the quoted grant.
# Usage: sh ledgers/LX1/scripts/LX1-b-r11/licence_r11.sh <outdir>
O="$1"; mkdir -p "$O"
curl -sS -L --max-time 30 -o /tmp/lx1b-r11-fed-disclaimer.html -w "%{http_code}\n" https://www.federalreserve.gov/disclaimer.htm > "$O/curl_fed_disclaimer_code.out" 2>&1
python3 -I -c "
t=open('/tmp/lx1b-r11-fed-disclaimer.html',encoding='utf-8',errors='replace').read()
i=t.find('Unless otherwise indicated'); print('quote found at offset', i); print(t[i:i+260].replace(chr(10),' '))
" > "$O/fed_licence_quote.out"
