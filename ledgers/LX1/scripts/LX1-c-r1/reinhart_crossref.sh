#!/bin/sh
# Plain curl of the Crossref record for reinhart2009this (DOI from references/references.json), then print key fields.
curl -sS --max-time 40 -A "quant-phd-verifier/1.0" "https://api.crossref.org/works/10.1515/9781400831722" -o "$1" -w "http=%{http_code}\n"
python3 -c "
import json,sys
m=json.load(open(sys.argv[1]))['message']
print('title:', m.get('title')); print('published:', m.get('published',{}).get('date-parts') or m.get('published-print')); print('publisher:', m.get('publisher'))
print('authors:', [(a.get('family'), a.get('given')) for a in m.get('author',[])]); print('isbn:', m.get('ISBN'))
" "$1"
