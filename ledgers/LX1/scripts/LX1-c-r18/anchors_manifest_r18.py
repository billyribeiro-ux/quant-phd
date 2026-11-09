"""Round-18 LX1-c: href/anchor check for project.html and MANIFEST walk for the three embedded series (verifier-written).
Usage: python -I anchors_manifest_r18.py <checkout_root>"""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1]).resolve() / "course/modules/LX/LX1"
page = (root / "project.html").read_text(encoding="utf-8")
ids = set(re.findall(r'\sid="([^"]+)"', page))
hrefs = re.findall(r'href="([^"]+)"', page)
bad = []
checked = 0
for h in hrefs:
    if h.startswith(("http", "mailto")):
        continue
    checked += 1
    f, _, a = h.partition("#")
    if f == "":
        if a and a not in ids:
            bad.append(h)
        continue
    target = root / f
    if not target.exists():
        bad.append(h + " (missing file)")
        continue
    if a and a not in set(re.findall(r'\sid="([^"]+)"', target.read_text(encoding="utf-8"))):
        bad.append(h)
print("internal hrefs checked:", checked, "bad:", bad)
print("data-concept links:", re.findall(r'data-concept="([^"]+)"', page))

m = json.load(open(sys.argv[1] + "/course/assets/data/market/MANIFEST.json", encoding="utf-8"))
found = []
def walk(o):
    if isinstance(o, dict):
        if o.get("id") in ("fx_daily", "fx_monthly", "ust_daily"):
            found.append((o["id"], o.get("columns"), o.get("first"), o.get("last")))
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(m)
for f in sorted(found):
    print("MANIFEST", f)
print("MANIFEST embedded ids:", sorted(x[0] for x in found))
