#!/bin/sh
# LX2-d round 6: re-fetch the cited source texts with plain curl (no login, no bot bypass).
# Usage: sh fetch_sources_r6.sh /tmp/lx2d-r6-src
set -e
W=${1:-/tmp/lx2d-r6-src}; mkdir -p "$W"; cd "$W"
PT=${PDFTOTEXT:-$(command -v pdftotext)}
curl -sS -L -m 90 -o sr2602.pdf https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf
curl -sS -L -m 120 -o COMPS-1884.pdf https://www.govinfo.gov/content/pkg/COMPS-1884/pdf/COMPS-1884.pdf
curl -sS -L -m 120 -o COMPS-1885.pdf https://www.govinfo.gov/content/pkg/COMPS-1885/pdf/COMPS-1885.pdf
curl -sS -L -m 150 -o USREPORTS-463-646.pdf https://www.govinfo.gov/content/pkg/USREPORTS-463/pdf/USREPORTS-463-646.pdf
curl -sS -L -m 150 -o USREPORTS-521-642.pdf https://www.govinfo.gov/content/pkg/USREPORTS-521/pdf/USREPORTS-521-642.pdf
curl -sS -L -m 90 -o cfa-standards-of-practice-iii-a.html https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-iii-a
curl -sS -L -m 90 -o cfa-standards-of-practice-vi-a.html https://www.cfainstitute.org/standards/professionals/code-ethics-standards/standards-of-practice-vi-a
"$PT" -layout sr2602.pdf letter.txt
for f in COMPS-1884 COMPS-1885 USREPORTS-463-646 USREPORTS-521-642; do "$PT" -layout $f.pdf $f.txt; done
sha256sum * > SHA256SUMS.txt
# Attachment to SR 26-2 and the CFA pages as plain text (run after the fetch above, in the same directory):
#   curl -sS -L -m 90 -o sr2602a1.pdf https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf
#   pdftotext -layout sr2602a1.pdf att.txt
#   python3 -I html_to_text.py cfa-standards-of-practice-iii-a.html > cfa3a.txt
#   python3 -I html_to_text.py cfa-standards-of-practice-vi-a.html > cfa6a.txt
# SHA-256 of every fetched source is recorded in SHA256SUMS.txt (written by the block above).
