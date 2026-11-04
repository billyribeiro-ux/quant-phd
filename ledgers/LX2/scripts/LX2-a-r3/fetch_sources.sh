#!/bin/sh
# Re-fetch the four primary sources with plain curl and extract their text with pdftotext.
# Usage: sh fetch_sources.sh <empty-scratch-dir>   (the dir is untrusted-data scratch; nothing here is executed from it)
set -eu
D="$1"
mkdir -p "$D"
cd "$D"
curl -sS -m 60 -L -o COMPS-1884_details.html "https://www.govinfo.gov/app/details/COMPS-1884"
curl -sS -m 60 -L -o COMPS-1885_details.html "https://www.govinfo.gov/app/details/COMPS-1885"
curl -sS -m 90 -L -o COMPS-1884.pdf "https://www.govinfo.gov/content/pkg/COMPS-1884/pdf/COMPS-1884.pdf"
curl -sS -m 90 -L -o COMPS-1885.pdf "https://www.govinfo.gov/content/pkg/COMPS-1885/pdf/COMPS-1885.pdf"
curl -sS -m 60 -L -o USREPORTS-463-646_details.html "https://www.govinfo.gov/app/details/USREPORTS-463/USREPORTS-463-646"
curl -sS -m 60 -L -o USREPORTS-521-642_details.html "https://www.govinfo.gov/app/details/USREPORTS-521/USREPORTS-521-642"
curl -sS -m 90 -L -o USREPORTS-463-646.pdf "https://www.govinfo.gov/content/pkg/USREPORTS-463/pdf/USREPORTS-463-646.pdf"
curl -sS -m 90 -L -o USREPORTS-521-642.pdf "https://www.govinfo.gov/content/pkg/USREPORTS-521/pdf/USREPORTS-521-642.pdf"
pdftotext -layout COMPS-1884.pdf comps1884.txt
pdftotext -layout COMPS-1885.pdf comps1885.txt
pdftotext -layout USREPORTS-463-646.pdf dirks.txt
pdftotext -layout USREPORTS-521-642.pdf ohagan.txt
ls -la
