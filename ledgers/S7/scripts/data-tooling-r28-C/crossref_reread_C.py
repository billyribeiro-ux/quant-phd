"""Round-28 part C: today's Crossref record re-reads (api.crossref.org, unauthenticated, no personal data in the request;
2 s between requests). For each DOI: HTTP status, title, container, volume/issue/page and the abstract phrases the
S7 pages quote (abstract phrases are matched after stripping JATS tags). Run: python -I crossref_reread_C.py"""
import json
import re
import time
import urllib.error
import urllib.request

DOIS = {
    "10.1093/rfs/hhy131": ["65%", "452 anomalies", "1.96"],            # Hou, Xue, Zhang (L03 s8 span; r21-L03-s8-hxz)
    "10.1093/rfs/hhaa018": ["2 million", "45%", "3.8", "3.4"],        # Chordia, Goyal, Saretto (r21-L03-s8-chordia)
    "10.1111/jofi.13249": ["different conclusions", "93 countries"],  # Jensen, Kelly, Pedersen (r21-L03-s8-jkp)
    "10.1287/mnsc.2023.03083": ["unobserved"],                        # Chen 2025 (r23-counter-hlz-chen)
    "10.1093/rapstu/raz011": ["156", "12.3%", "different perspective"],  # Chen & Zimmermann (r24-L03-s8-cz-span)
    "10.1214/aop/1024404523": ["domain of attraction"],               # Gine, Gotze, Mason (r23-gine-attribution)
    "10.1214/aop/1015345757": ["domain of attraction", "EX"],         # Bootstrapping the t-statistic (r23-gine-scope)
    "10.1214/24-aoas1983": ["size distortion", "endogeneity"],        # Jiang et al. (r24-L08-jiang-span)
    "10.1016/j.frl.2025.108491": [],                                  # Lu 2025 (no Crossref abstract expected)
}
out = []
for i, (doi, phrases) in enumerate(DOIS.items()):
    if i:
        time.sleep(2)
    url = "https://api.crossref.org/works/" + urllib.request.quote(doi, safe="/")
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            status = r.status
            msg = json.loads(r.read().decode("utf-8"))["message"]
    except urllib.error.HTTPError as e:
        out.append(f"{doi}: HTTP {e.code}")
        continue
    title = (msg.get("title") or [""])[0]
    container = (msg.get("container-title") or [""])[0]
    abstract = re.sub(r"<[^>]+>", " ", msg.get("abstract", "") or "")
    abstract = re.sub(r"\s+", " ", abstract)
    found = {p: (p in abstract) for p in phrases}
    out.append(f"{doi}: HTTP {status} | title {title!r} | container {container!r} vol {msg.get('volume')} issue {msg.get('issue')} page {msg.get('page')} | abstract {'present' if abstract else 'absent'} ({len(abstract)} chars) | phrases {found}")
print("\n".join(out))
