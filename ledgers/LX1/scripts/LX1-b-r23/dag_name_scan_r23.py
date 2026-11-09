"""Name scan: concept names of modules outside the LX1 prerequisite closure, found in the three LX1 pages (tags stripped)."""
import html
import json
import re
import sys

ROOT = sys.argv[1]
CLOSURE = {"E1", "E5", "FC1", "M1", "M2", "P0.1", "LX1"}
d = json.load(open(f"{ROOT}/curriculum/curriculum.json", encoding="utf-8"))
concepts = d["concepts"]
pages = {p: open(f"{ROOT}/course/modules/LX/LX1/{p}.html", encoding="utf-8").read() for p in ("L01", "L03", "L04")}
texts = {}
for p, raw in pages.items():
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    texts[p] = re.sub(r"\s+", " ", html.unescape(raw)).lower()
hits = []
for cid, v in concepts.items():
    mod = v.get("module")
    if mod in CLOSURE:
        continue
    name = v.get("name", "")
    base = re.sub(r"\s*\(.*?\)", "", name).strip().lower()
    if len(base) < 6:
        continue
    for p, t in texts.items():
        if base in t:
            hits.append((p, cid, mod, base))
for h in sorted(hits):
    print("HIT", *h)
print("total_hits", len(hits))
