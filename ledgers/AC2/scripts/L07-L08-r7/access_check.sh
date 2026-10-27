#!/bin/sh
# Plain-curl status checks for every access statement in L07/L08 learner text and plans (2026-10-27). No bot-check bypass.
OUT=/tmp/ac2-v/L07-L08-r7
mkdir -p "$OUT"
curl -s -o /dev/null -D "$OUT/h1.txt" -w 'doi %{http_code} -> %{redirect_url}\n' --max-time 30 https://doi.org/10.2469/faj.v55.n5.2296
curl -s -o /dev/null -w 'publisher tandfonline %{http_code}\n' --max-time 30 https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296
curl -s -o /dev/null -w 'ivey pdf %{http_code} %{content_type}\n' --max-time 60 https://www.ivey.uwo.ca/media/3775523/value_investing_the_use_of_historical_financial_statement_information.pdf
curl -s -o "$OUT/wiki.html" -w 'wikipedia %{http_code}\n' --max-time 60 https://en.wikipedia.org/wiki/Beneish_M-score
curl -s -o /dev/null -w 'jstor record %{http_code} (status only, no body inspection)\n' --max-time 30 https://www.jstor.org/stable/2672906
curl -s -o /dev/null -w 'sec webmaster-faq %{http_code}\n' --max-time 30 https://www.sec.gov/os/webmaster-faq
curl -s -o /dev/null -w 'sec accessing-edgar-data %{http_code}\n' --max-time 30 https://www.sec.gov/os/accessing-edgar-data
curl -s -o /dev/null -w 'dechow doi %{http_code} -> %{redirect_url}\n' --max-time 30 https://doi.org/10.2308/tar-9505096112
