import json, collections, sys, pathlib, re
root = pathlib.Path(sys.argv[1])
cards = json.load(open(root / "course/modules/AC/AC4/cards.json", encoding="utf-8"))
print("total cards", len(cards))
ids = collections.Counter(c["id"] for c in cards); print("dup ids", [k for k, v in ids.items() if v > 1])
fr = collections.Counter(c["front"] for c in cards); print("dup fronts", [k for k, v in fr.items() if v > 1])
print("lessons", collections.Counter(c["lesson"] for c in cards))
for c in cards:
    if c["lesson"] in ("L07", "L08") or c["id"] in ("AC4-c135", "AC4-c136"):
        t = root / f"course/modules/AC/AC4/{c['lesson']}.html"
        txt = t.read_text(encoding="utf-8")
        nums = set(re.findall(r"\d[\d,]*\.?\d*", c["back"]))
        missing = [n for n in nums if n.rstrip('.').replace(',', '') not in txt.replace(',', '')]
        if missing: print(c["id"], "numbers not in lesson html:", missing)
for c in cards:
    if c["id"] in ("AC4-c095","AC4-c108","AC4-c113","AC4-c137","AC4-c138","AC4-c139","AC4-c140"):
        print(c["id"], c["grade"], c.get("basis"), "|", c["back"][:140])
