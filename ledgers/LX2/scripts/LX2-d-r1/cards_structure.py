"""LX2-d round 1: structural audit of course/modules/LX/LX2/cards.json (run from the checkout root)."""
import json, re, sys, collections
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
UNIT = ROOT / "course/modules/LX/LX2"
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
reg = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
keys = set()
if isinstance(reg, dict):
    for k, v in reg.items():
        if isinstance(v, list):
            for r in v:
                if isinstance(r, dict) and "key" in r:
                    keys.add(r["key"])
        elif isinstance(v, dict):
            keys.add(k)
if not keys:
    recs = reg if isinstance(reg, list) else next(v for v in reg.values() if isinstance(v, list))
    keys = {r["key"] for r in recs}
print("registry keys:", len(keys))
print("cards:", len(cards), "fields:", sorted({f for c in cards for f in c}))
ids = [c["id"] for c in cards]
print("unique ids:", len(set(ids)) == len(ids))
expected = [f"LX2-c{i:03d}" for i in range(1, len(cards) + 1)]
print("ids sequential 001..%03d:" % len(cards), ids == expected)
print("lesson counts:", collections.Counter(c["lesson"] for c in cards))
print("grades:", collections.Counter(c.get("grade", "-") for c in cards))
bad_keys = [(c["id"], k) for c in cards for k in c.get("cite", []) if k not in keys]
print("unknown cite keys:", bad_keys)
for c in cards:
    g = c.get("grade")
    grounded = c.get("cite") or c.get("basis")
    if g and g != "T" and not grounded:
        print("GRADE WITHOUT GROUNDING:", c["id"])
    if g == "T" and not c.get("basis"):
        print("T WITHOUT BASIS:", c["id"])
    if not c.get("cite") and not c.get("basis") and c.get("lesson"):
        print("NO CITE OR BASIS (definition-type ok?):", c["id"], c["front"][:70])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [f for f, n in backs.items() if n > 1])
banned = re.compile(r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.|…", re.I)
process = re.compile(r"\b(builder|build|verifier|round|REQUEST|unit report|fixer)\b", re.I)
for c in cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for m in banned.finditer(text):
        print("BANNED-HIT", c["id"], repr(m.group(0)))
    for m in process.finditer(text):
        print("PROCESS-WORD", c["id"], repr(m.group(0)))
# every card's text: list the symbols used
syms = collections.Counter()
for c in cards:
    for m in re.finditer(r"\\\(([^)]*)\\\)|\b([A-Za-z])(?:_[a-z0-9]+)?\b", c["front"] + " " + c["back"]):
        syms[m.group(0)] += 1
print("symbol-like tokens:", sorted(syms.items())[:200])
