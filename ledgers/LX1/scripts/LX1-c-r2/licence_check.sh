#!/bin/sh
# LX1-c round 2: plain curl of the licence_url recorded in MANIFEST for fx_monthly, then a quote search.
# Run from the repo root. Output is saved as licence_check.out.
URL="https://www.federalreserve.gov/disclaimer.htm"
curl -sS -m 60 -A "Mozilla/5.0 (Macintosh) plain-curl-verifier" -o /tmp/lx1c-r2-disclaimer.html -w "HTTP %{http_code} bytes %{size_download}\n" "$URL"
python3 -I -c "
import re,html
t=open('/tmp/lx1c-r2-disclaimer.html',encoding='utf-8',errors='replace').read()
txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
q=\"Unless otherwise indicated, information on Board's website is in the public domain and may be copied and distributed without permission\"
print('quote found:', q in txt)
"
