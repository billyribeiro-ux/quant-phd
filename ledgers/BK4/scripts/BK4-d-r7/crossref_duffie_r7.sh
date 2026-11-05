#!/bin/sh
# Plain curl to the public Crossref works endpoint for the registry DOI of duffie2011central (no personal data sent).
# Usage (from the checkout root): sh ledgers/BK4/scripts/BK4-d-r7/crossref_duffie_r7.sh
S=ledgers/BK4/scripts/BK4-d-r7/out
curl -s -o $S/crossref_duffie_r7.json -w "%{http_code}\n" "https://api.crossref.org/works/10.1093/rapstu/rar001"
python3 -I -c "import json; d=json.load(open('$S/crossref_duffie_r7.json'))['message']; print(d['title'], d['DOI'], d['container-title'], d.get('volume'), d.get('issue'), d.get('page'))"
