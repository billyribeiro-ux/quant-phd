"""Round-28 part C: the Crossref records for the three L08 Section 6 spans not yet re-read (Moskowitz, Huang, Ahn),
and the Bootstrapping-the-t-statistic abstract's exact restatement (r23-gine-scope). 2 s between requests.
Run: python -I crossref_reread2_C.py"""
import json
import re
import time
import urllib.error
import urllib.request

DOIS = ["10.1016/j.jfineco.2011.11.003", "10.1016/j.jfineco.2019.08.004", "10.3390/jrfm19010046", "10.1214/aop/1015345757"]
for i, doi in enumerate(DOIS):
    if i:
        time.sleep(2)
    url = "https://api.crossref.org/works/" + urllib.request.quote(doi, safe="/")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            status, msg = r.status, json.loads(r.read().decode("utf-8"))["message"]
    except urllib.error.HTTPError as e:
        print(doi, "HTTP", e.code)
        continue
    abstract = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", msg.get("abstract", "") or ""))
    print(f"{doi}: HTTP {status} | {(msg.get('title') or [''])[0]!r} | {(msg.get('container-title') or [''])[0]!r} "
          f"vol {msg.get('volume')} issue {msg.get('issue')} page {msg.get('page')} | published {msg.get('issued', {}).get('date-parts')}")
    if "1015345757" in doi:
        m = re.search(r".{0,160}EX\s*=\s*0.{0,40}", abstract)
        print("   abstract:", abstract[:600])
        print("   'EX = 0' phrase present:", bool(m), "|", m.group(0) if m else None)
