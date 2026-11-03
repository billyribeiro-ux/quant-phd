"""Full scan of cards.json: ids, lesson keys, duplicate and near-duplicate fronts, and card numbers that the lesson does not contain."""
import json, re, sys, difflib, collections
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)))
print("duplicate ids", [i for i, n in collections.Counter(ids).items() if n > 1])
print("keys", sorted({k for c in cards for k in c}))
print("lessons", collections.Counter(c["lesson"] for c in cards))
norm = lambda s: re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
fronts = [(c["id"], norm(c["front"]), norm(c["back"])) for c in cards]
for i in range(len(fronts)):
    for j in range(i + 1, len(fronts)):
        a, b = fronts[i], fronts[j]
        rf = difflib.SequenceMatcher(None, a[1], b[1]).ratio()
        rb = difflib.SequenceMatcher(None, a[2], b[2]).ratio()
        if a[1] == b[1] or rf > 0.85 or rb > 0.85:
            print(f"NEAR-DUP {a[0]} {b[0]} front_ratio={rf:.2f} back_ratio={rb:.2f}")
            print("   ", cards[i]["front"], " || ", cards[j]["front"])
# every card's lesson must exist as a page
for c in cards:
    if not (root / f"course/modules/M/M2/{c['lesson']}.html").exists():
        print("MISSING LESSON PAGE", c["id"], c["lesson"])
# grade C or D needs basis
for c in cards:
    if c.get("grade") in ("C", "D") and not c.get("basis"):
        print("C/D without basis", c["id"])
# card numbers: every 'Proposition x.y', 'Theorem x.y', 'Example x.y', 'Definition x.y', 'Remark x.y', 'Lemma', 'Assumption', 'Problem' cited in card must appear in that lesson
for c in cards:
    if c["lesson"] not in ("L22", "L23", "L24"):
        continue
    page = (root / f"course/modules/M/M2/{c['lesson']}.html").read_text(encoding="utf-8")
    for m in re.findall(r"(Proposition|Theorem|Example|Definition|Remark|Lemma|Assumption|Corollary|Fact) (\d+\.\d+)", c["front"] + " " + c["back"]):
        token = f"{m[0]} {m[1]}"
        if token not in page:
            print("CARD NUMBER NOT IN LESSON", c["id"], token)
print("scan done")
