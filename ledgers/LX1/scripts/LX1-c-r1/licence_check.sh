#!/bin/sh
# Plain curl of the licence_url recorded for fx_monthly (MANIFEST licence_url), then grep for the quoted grant.
# Usage: sh licence_check.sh <outfile>
curl -sS -L --max-time 45 -o "$1" -w "http_code=%{http_code} bytes=%{size_download}\n" https://www.federalreserve.gov/disclaimer.htm
python3 -c "
import re,html,sys
t=open(sys.argv[1],encoding='utf-8',errors='replace').read()
t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\s+',' ',t)
print('quoted grant present:', 'Unless otherwise indicated, information on Board\'s website is in the public domain and may be copied and distributed without permission. Please cite to the Board as the source of the information.' in t)
" "$1"
