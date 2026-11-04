import json, re, html, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-M4-d/course/modules/M/M4")
cards = json.loads((root / "cards.json").read_text())
print("cards:", len(cards))
ids = [c["id"] for c in cards]
dups = {i for i in ids if ids.count(i) > 1}
print("duplicate ids:", dups)
from collections import Counter
print("grades:", Counter(c["grade"] for c in cards))
print("keys:", Counter(tuple(sorted(c.keys())) for c in cards))
texts = {}
for n in range(1, 11):
    p = root / f"L{n:02d}.html"
    if not p.exists():
        continue
    t = p.read_text()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    texts[f"L{n:02d}"] = re.sub(r"\s+", " ", html.unescape(t))
print("lessons:", sorted(texts))
missing = []
for c in cards:
    lt = texts.get(c["lesson"], "")
    nums = re.findall(r"\d+\.\d+|\d+/\d+|\b\d{2,}\b", c["back"])
    for x in nums:
        if x not in lt:
            missing.append((c["id"], c["lesson"], x))
print("card numbers not found verbatim in own lesson:", len(missing))
for m in missing: print("  ", m)
# cards whose 'basis' missing when grade C
print("C cards without basis:", [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis")])
print("T cards with basis:", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
