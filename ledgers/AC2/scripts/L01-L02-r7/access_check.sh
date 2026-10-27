#!/bin/sh
# Round-7 reproduction of access statements in the L01-L02 learner text and plans/AC2-open-items.md.
# Plain curl only, default redirects not followed except where noted; no challenge page is inspected or bypassed.
for u in https://www.sec.gov/os/webmaster-faq https://www.sec.gov/os/accessing-edgar-data \
         https://doi.org/10.2308/tar-9505096112 https://doi.org/10.2469/faj.v55.n5.2296 \
         https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json; do
  printf '%s ' "$u"; curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" --max-time 30 -A "Mozilla/5.0" "$u"
done
curl -s -o /dev/null -w "dechow publisher page %{http_code}\n" --max-time 30 -A "Mozilla/5.0" \
  "https://publications.aaahq.org/accounting-review/article/70/2/193/18940/Detecting-Earnings-Management"
curl -s -o /dev/null -w "beneish publisher page %{http_code}\n" --max-time 30 -A "Mozilla/5.0" \
  "https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296"
