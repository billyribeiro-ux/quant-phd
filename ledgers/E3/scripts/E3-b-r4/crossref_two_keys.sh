#!/bin/bash
for doi in 10.2307/1913778 10.2307/1914185; do
curl -s -m 30 "https://api.crossref.org/works/$doi" | python3 -c "
import sys,json
m=json.load(sys.stdin)['message']
print(m.get('title'), '|', [a.get('family') for a in m.get('author',[])], '|', m.get('container-title'), m.get('volume'), m.get('issue'), m.get('page'), m.get('issued',{}).get('date-parts'))"
done
