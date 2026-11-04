#!/bin/sh
# Plain curl fetches made by the LX2 slice-b verifier (round 1). No login, no bot-check bypass.
# Outputs go to /tmp/lx2b-src (scratch, untrusted). Text extraction used pdftotext from the installed poppler.
set -e
D=/tmp/lx2b-src
mkdir -p "$D"
curl -sS -L -m 60 -o "$D/sr2602.htm" -w "sr2602.htm HTTP %{http_code}\n" "https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm"
curl -sS -L -m 120 -o "$D/sr2602a1.pdf" -w "sr2602a1.pdf HTTP %{http_code}\n" "https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf"
curl -sS -L -m 60 -o "$D/cfa.htm" -w "cfa landing HTTP %{http_code}\n" "https://www.cfainstitute.org/standards/professionals/code-ethics-standards"
for p in standards-of-practice-iii-a standards-of-practice-vi-a standards-of-practice-vi-b; do
  curl -sS -L -m 60 -o "$D/$p.htm" -w "$p HTTP %{http_code}\n" "https://www.cfainstitute.org/standards/professionals/code-ethics-standards/$p"
done
curl -sS -L -m 120 -o "$D/code2024.pdf" -w "code2024.pdf HTTP %{http_code}\n" "https://www.cfainstitute.org/sites/default/files/-/media/documents/ethics-in-practice/code_of_ethics_and_standards_of_professional_conduct_2024.pdf"
PDFTOTEXT=/Users/billyribeiro/.local/share/mise/installs/conda-poppler/26.09.0/.mise-bins/pdftotext
"$PDFTOTEXT" "$D/sr2602a1.pdf" "$D/plain.txt"
"$PDFTOTEXT" "$D/code2024.pdf" "$D/code2024.txt"
