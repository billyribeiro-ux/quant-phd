"""Round-9 cards checks for CS2 (slice d). Reads cards.json and the lesson pages; prints findings."""
import difflib
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOD = ROOT / "course" / "modules" / "CS" / "CS2"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))


def lesson_text(lid: str) -> str:
    src = (MOD / f"{lid}.html").read_text(encoding="utf-8")
    src = re.sub(r"<script.*?</script>", "", src, flags=re.S)
    src = re.sub(r"<style.*?</style>", "", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(src)


texts = {f"L{i:02d}": lesson_text(f"L{i:02d}") for i in range(1, 12)}
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("id pattern ok:", all(re.fullmatch(r"CS2-c\d{3}", i) for i in ids))
print("lessons:", sorted(Counter(c["lesson"] for c in cards).items()))
print("grades:", Counter(c["grade"] for c in cards))
bad_keys = [c["id"] for c in cards if set(c) - {"id", "lesson", "front", "back", "grade", "basis", "cite"}]
print("unexpected keys:", bad_keys)
basis_mismatch = [c["id"] for c in cards if (c["grade"] != "T") != ("basis" in c or "cite" in c)]
print("basis/cite present iff non-T violations:", basis_mismatch)
missing_lessons = [l for l in texts if l not in {c["lesson"] for c in cards}]
print("lessons without a card:", missing_lessons)
print("cite keys used:", sorted({c["cite"] for c in cards if "cite" in c}))

# every number other than 0,1,2 on a card must appear in its lesson text
num_re = re.compile(r"(?<![A-Za-z_\d.])\d+(?:\.\d+)?(?![\d.]*[A-Za-z])")
missing = []
for c in cards:
    t = texts[c["lesson"]]
    for field in ("front", "back"):
        for num in set(num_re.findall(c[field])):
            if num in ("0", "1", "2"):
                continue
            if num not in t:
                missing.append((c["id"], field, num))
print("numbers (other than 0,1,2) not found in own lesson text:", missing)

# near duplicates
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.8 or rb > 0.8 or a["front"] == b["front"]:
            pairs.append((a["id"], b["id"], round(rf, 2), round(rb, 2)))
print("exact duplicate fronts:", [p for p in pairs if p[2] == 1.0])
print("near-duplicate pairs (front or back ratio > 0.8):", len(pairs))
for p in pairs:
    print("  ", p)
