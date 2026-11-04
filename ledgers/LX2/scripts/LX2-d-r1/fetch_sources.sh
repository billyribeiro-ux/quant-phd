#!/bin/sh
# LX2-d round 1: re-create the source texts used by check_quotes.py (plain curl, no login, no bot bypass).
# Usage: sh fetch_sources.sh /tmp/lx2d-src   (then run check_quotes.py, which reads /tmp/lx2d-src)
set -e
W=${1:-/tmp/lx2d-src}; mkdir -p "$W"; cd "$W"
PT=${PDFTOTEXT:-/Users/billyribeiro/.local/share/mise/installs/conda-poppler/26.09.0/.mise-bins/pdftotext}
curl -sS -L -m 90 -o sr2602a1.pdf https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf
curl -sS -L -m 90 -o sr2602.pdf https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf
curl -sS -L -m 120 -o COMPS-1884.pdf https://www.govinfo.gov/content/pkg/COMPS-1884/pdf/COMPS-1884.pdf
curl -sS -L -m 120 -o COMPS-1885.pdf https://www.govinfo.gov/content/pkg/COMPS-1885/pdf/COMPS-1885.pdf
curl -sS -L -m 150 -o USREPORTS-463-646.pdf https://www.govinfo.gov/content/pkg/USREPORTS-463/pdf/USREPORTS-463-646.pdf
curl -sS -L -m 150 -o USREPORTS-521-642.pdf https://www.govinfo.gov/content/pkg/USREPORTS-521/pdf/USREPORTS-521-642.pdf
curl -sS -L -m 90 -o cfa-standards-of-practice-iii-a.html https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-a
curl -sS -L -m 90 -o cfa-standards-of-practice-vi-a.html https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-vi-a
"$PT" -layout sr2602a1.pdf att.txt; "$PT" -layout sr2602.pdf letter.txt
for f in COMPS-1884 COMPS-1885 USREPORTS-463-646 USREPORTS-521-642; do "$PT" -layout $f.pdf $f.txt; done
