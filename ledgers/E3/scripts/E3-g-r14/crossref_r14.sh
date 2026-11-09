#!/bin/sh
# Plain curl, default user agent, no contact data. Output: crossref_live_r14.out
for doi in 10.2307/1884324 "10.1016/0304-4068(89)90018-9" 10.2307/1914185; do
  enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$doi")
  curl -s -o /tmp/cr_r14.json -w "%{http_code} " "https://api.crossref.org/works/$enc"
  python3 -c "import json;d=json.load(open('/tmp/cr_r14.json'))['message'];print(d.get('DOI'),'|',(d.get('title') or [''])[0],'|',[a.get('family') for a in d.get('author',[])][:2],'|',d.get('issued',{}).get('date-parts'),'|',d.get('container-title'),d.get('volume'),d.get('issue'))"
done
