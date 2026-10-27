#!/bin/bash
# plain curl only: no cookies, no challenge inspection; header-only status and redirect target
S=/tmp/verify-ac2r9-l12/ledgers/AC2/scripts/L01-L02-r9/access_check.txt
: > "$S"
for U in \
 "https://www.sec.gov/os/webmaster-faq" \
 "https://www.sec.gov/os/accessing-edgar-data" \
 "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json" \
 "https://doi.org/10.2469/faj.v55.n5.2296" \
 "https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296" \
 "https://doi.org/10.2308/tar-9505096112" \
 ; do
  CODE=$(curl -s -o /dev/null -m 30 -w '%{http_code}' "$U")
  LOC=$(curl -s -o /dev/null -m 30 -w '%{redirect_url}' "$U")
  echo "$CODE  $U  redirect=[$LOC]" | tee -a "$S"
done
echo "--- descriptive non-personal UA on data.sec.gov (no contact address)" | tee -a "$S"
CODE=$(curl -s -o /dev/null -m 30 -A "quant-phd-AC2-verifier/1.0 (non-personal research check)" -w '%{http_code}' "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json")
echo "$CODE  data.sec.gov companyfacts with declared non-personal UA" | tee -a "$S"
