#!/bin/sh
# Plain-curl fetch of the SR 26-2 letter and its attachment (no bot checks bypassed), then text extraction.
# Usage: sh fetch_sr.sh <empty-scratch-dir>
set -eu
cd "$1"
curl -sS -L -o sr2602.htm https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm
curl -sS -L -o SR2602.pdf https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf
curl -sS -L -o SR2602a1.pdf https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf
pdftotext -layout SR2602.pdf sr.txt
pdftotext -layout SR2602a1.pdf a1.txt
python3 -I -c "
import re, html
t = open('sr2602.htm', encoding='utf-8', errors='replace').read()
t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
t = re.sub(r'<br\s*/?>|</p>|</div>|</li>|</h\d>', '\n', t)
t = html.unescape(re.sub(r'<[^>]+>', '', t))
open('sr_html.txt', 'w', encoding='utf-8').write(re.sub(r'[ \t]+', ' ', t))
"
