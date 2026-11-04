#!/bin/bash
# LX2-c round 4: plain curl of the SR 26-2 letter PDF (the file behind registry key frb2026fed), then pdftotext.
# Usage: fetch_sr2602_r4.sh <EMPTY_NEW_DIRECTORY>   (downloaded content is untrusted; it is only read as text)
set -eu
D="$1"
cd "$D"
curl -sS -L -o sr2602.pdf -w 'HTTP %{http_code} bytes %{size_download}\n' https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf
pdftotext -layout sr2602.pdf letter.txt
wc -l letter.txt
