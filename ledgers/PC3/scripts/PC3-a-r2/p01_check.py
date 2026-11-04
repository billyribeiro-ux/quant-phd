"""Check the hub claim about P0.1: which concept ids P0.1 owns, whether the concept index marks them not yet released, and whether any PC3 page links them."""
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
cur = json.loads((root / "curriculum/curriculum.json").read_text(encoding="utf-8"))
concepts = cur["concepts"]
p01 = [cid for cid, c in concepts.items() if c.get("module") == "P0.1"]
print("P0.1 concept count:", len(p01))
print("  ids:", p01)
idx = (root / "course/concepts.html").read_text(encoding="utf-8")
for cid in p01:
    m = re.search(r'<li id="%s">(.*?)</li>' % re.escape(cid), idx, re.S)
    print("index", cid, "->", (m.group(1)[-60:].replace("\n", " ") if m else "MISSING"))
pc3 = sorted((root / "course/modules/PC/PC3").glob("*.html"))
ids = set(p01)
for f in pc3:
    txt = f.read_text(encoding="utf-8")
    hits = [m.group(1) for m in re.finditer(r'data-concept="([^"]+)"', txt) if m.group(1) in ids]
    hrefs = [m.group(1) for m in re.finditer(r'concepts\.html#([^"]+)"', txt) if m.group(1) in ids]
    print(f.name, "P0.1 data-concept hits:", hits, "P0.1 hrefs:", hrefs)
