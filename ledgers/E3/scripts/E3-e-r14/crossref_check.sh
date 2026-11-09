#!/bin/sh
# Plain-curl Crossref lookups for the five E3 registry keys (verifier round 14). No personal data is sent.
for doi in 10.2307/1913738 10.2307/1914185 10.2307/1913778 10.2307/1884324 "10.1016/0304-4068(89)90018-9"; do
  echo "== $doi"
  curl -s -m 30 "https://api.crossref.org/works/$doi" | python3 -c "
import json,sys
d=json.load(sys.stdin)['message']
print(' title:', d.get('title'), '| year:', d.get('issued',{}).get('date-parts'), '| container:', d.get('container-title'), '| vol/issue:', d.get('volume'), d.get('issue'), '| pages:', d.get('page'))
print(' authors:', [a.get('family') for a in d.get('author',[])])
"
done
