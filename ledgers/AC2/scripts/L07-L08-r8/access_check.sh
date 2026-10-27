#!/bin/bash
# Plain curl status checks for every access statement in L07/L08 learner text and plans (round 8).
for u in https://doi.org/10.2469/faj.v55.n5.2296 https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296 https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf https://en.wikipedia.org/wiki/Beneish_M-score; do
  echo "== $u"
  curl -s -o /dev/null -D - --max-time 30 -w 'HTTP %{http_code} final=%{url_effective}\n' "$u" | grep -iE '^(HTTP|location)'
done
