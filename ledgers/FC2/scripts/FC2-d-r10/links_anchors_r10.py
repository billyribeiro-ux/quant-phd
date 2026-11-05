"""Check project.html's local hrefs and anchors resolve, and the reading keys exist in references/references.json."""
import json
import os
import re
import sys

root = sys.argv[1]
base = os.path.join(root, "course", "modules", "FC", "FC2")
page = open(os.path.join(base, "project.html"), encoding="utf-8").read()
ids_here = set(re.findall(r'id="([^"]+)"', page))
bad = []
for href in re.findall(r'href="([^"]+)"', page):
    if href.startswith(("http://", "https://", "mailto:")):
        continue
    if href.startswith("#"):
        if href[1:] not in ids_here:
            bad.append(("anchor", href))
        continue
    path, _, frag = href.partition("#")
    target = os.path.normpath(os.path.join(base, path))
    if not os.path.exists(target):
        bad.append(("file", href, target))
        continue
    if frag and target.endswith(".html"):
        tid = set(re.findall(r'id="([^"]+)"', open(target, encoding="utf-8").read()))
        if frag not in tid:
            bad.append(("frag", href))
print("project.html local links checked; unresolved:", bad)
refs = json.load(open(os.path.join(root, "references", "references.json"), encoding="utf-8"))
keys = set(refs.keys()) if isinstance(refs, dict) else {r.get("key") for r in refs}
for k in ("hull2021options", "stoll1969relationship", "cox1979option"):
    print("reading key", k, "in registry:", k in keys)
ds = open(os.path.join(root, "tools", "data_sources.yaml"), encoding="utf-8").read()
print("data_sources.yaml option-quote source mentioned:", bool(re.search(r"option", ds, re.I)))
for name in ("L01", "L05"):
    t = open(os.path.join(base, f"{name}.html"), encoding="utf-8").read()
    for a in ("def-arbitrage-opportunity", "def-put-call-parity", "def-option-arbitrage-bounds"):
        if a == "def-arbitrage-opportunity" and name != "L01":
            continue
        if a != "def-arbitrage-opportunity" and name != "L05":
            continue
        print(name, a, "anchor present:", f'id="{a}"' in t)
