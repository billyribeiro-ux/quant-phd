"""Full scan of cards.json: count, ids, duplicates, grades, lesson refs, labels and numbers against lesson text."""
import json, re, sys, html
from collections import Counter
from pathlib import Path
root = Path(sys.argv[1]) / "course/modules/E/E1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("duplicate ids:", [k for k, v in Counter(ids).items() if v > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
print("keys:", sorted({tuple(sorted(c)) for c in cards}))
print("grades:", Counter(c.get("grade","<none>") for c in cards))
print("lessons:", Counter(c["lesson"] for c in cards))
lessons = {}
for i in range(1, 10):
    p = root / f"L0{i}.html"
    t = html.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8")))
    lessons[f"L0{i}"] = re.sub(r"\s+", " ", t)
bad = []
for c in cards:
    if re.search(r"Misconception|Remark \d|Proposition|Example|Corollary|Problem R|Assumption", c["back"]):
        for m in re.finditer(r"(Misconception \d|Remark \d\.\d|Proposition \d\.\d|Example \d\.\d|Corollary \d\.\d|Problem R\d|Assumption \d|Proposition \d)", c["back"]):
            lab = m.group(1)
            hit = lab in lessons[c["lesson"]]
            if not hit:
                bad.append((c["id"], lab))
print("back-label references not printed in own lesson:", len(bad), bad[:40])
