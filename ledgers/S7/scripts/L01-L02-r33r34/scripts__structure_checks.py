"""Re-implementation of the card, concept-definition and reference-key checks of the S7 slice (replaces vanished scratch scripts)."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

CHK = Path(sys.argv[1])
cards = json.loads((CHK / "course/modules/S/S7/cards.json").read_text(encoding="utf-8"))
cards = cards["cards"] if isinstance(cards, dict) and "cards" in cards else cards
refs = json.loads((CHK / "references/references.json").read_text(encoding="utf-8"))["entries"]
keys = {e.get("key") for e in refs}
s7 = [c for c in cards if c["id"].startswith("S7-")]
print("cards total", len(cards), "S7 cards", len(s7), "L01", sum(c.get("lesson") == "L01" for c in s7), "L02", sum(c.get("lesson") == "L02" for c in s7))
print("duplicate ids", sorted({c["id"] for c in s7 if [d["id"] for d in s7].count(c["id"]) > 1}))
print("duplicate fronts", sorted({c["front"] for c in s7 if [d["front"] for d in s7].count(c["front"]) > 1}))
cites = {k for c in s7 for k in (c.get("cite") or [])}
print("cite keys in S7 cards not in registry:", sorted(k for k in cites if k not in keys))
print("grade values", Counter(c.get("grade") for c in s7))
print("A/B/D without cite:", [c["id"] for c in s7 if c.get("grade") in ("A", "B", "D") and not c.get("cite")])
print("C without basis:", [c["id"] for c in s7 if c.get("grade") == "C" and not c.get("basis")])
print("cards with basis:", sorted(c["id"] for c in s7 if c.get("basis")))
# concept definitions: curriculum assignment vs <dfn data-concept> in S7 pages
cur = json.loads((CHK / "curriculum/curriculum.json").read_text(encoding="utf-8"))
concepts = cur.get("concepts", {})
assigned = sorted(k for k, c in concepts.items() if c.get("module") == "S7")
print("curriculum concepts assigned to S7:", len(assigned))
defs = []
for f in sorted((CHK / "course/modules/S/S7").glob("L0*.html")):
    defs += re.findall(r'<dfn id="def-([^"]+)" data-concept="([^"]+)"', f.read_text(encoding="utf-8"))
dc = [d[1] for d in defs]
print("S7 lesson <dfn data-concept> count", len(dc), "duplicates", sorted({x for x in dc if dc.count(x) > 1}))
print("defined but not assigned to S7:", sorted(set(dc) - set(assigned)))
print("assigned to S7 but not defined in S7:", sorted(set(assigned) - set(dc)))
for name in ("L01", "L02"):
    html = (CHK / f"course/modules/S/S7/{name}.html").read_text(encoding="utf-8")
    cited = sorted({k for v in re.findall(r'data-cite="([^"]+)"', html) for k in v.split()})
    print(name, "distinct data-cite keys", len(cited), "unresolved:", [k for k in cited if k not in keys])
    print(name, "keys:", cited)
