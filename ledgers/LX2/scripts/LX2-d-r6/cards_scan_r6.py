"""LX2-d round 6: structural scan of course/modules/LX/LX2/cards.json (ids, lesson counts, duplicate fronts/backs, numbers)."""
import json
import re
from collections import Counter
from difflib import SequenceMatcher

cards = json.load(open("course/modules/LX/LX2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
print("ids sequential c001..c%03d:" % len(cards), ids == [f"LX2-c{i:03d}" for i in range(1, len(cards) + 1)])
print("lessons", Counter(c["lesson"] for c in cards))
print("keys", Counter(tuple(sorted(c.keys())) for c in cards))
print("grades", Counter(c.get("grade") for c in cards), "basis present", sum(1 for c in cards if c.get("basis")))
print("cite keys", Counter(k for c in cards for k in c.get("cite", [])))
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fr = [norm(c["front"]) for c in cards]
bk = [norm(c["back"]) for c in cards]
print("duplicate fronts", [ (ids[i], ids[j]) for i in range(len(cards)) for j in range(i+1, len(cards)) if fr[i] == fr[j]])
print("duplicate backs", [ (ids[i], ids[j]) for i in range(len(cards)) for j in range(i+1, len(cards)) if bk[i] == bk[j]])
near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = SequenceMatcher(None, fr[i], fr[j]).ratio()
        if r >= 0.75:
            near.append((ids[i], ids[j], round(r, 2)))
print("near-duplicate fronts (ratio>=0.75)", near)
nearb = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = SequenceMatcher(None, bk[i], bk[j]).ratio()
        if r >= 0.75:
            nearb.append((ids[i], ids[j], round(r, 2)))
print("near-duplicate backs (ratio>=0.75)", nearb)
# every card's numbers must appear in its lesson text (plain text dump made from the lesson HTML)
import subprocess
LESSON_TXT = {}
for L in ("L01", "L02", "L03", "L04"):
    LESSON_TXT[L] = subprocess.run(["python3", "-I", "ledgers/LX2/scripts/LX2-d-r6/html_to_text.py",
                                    f"course/modules/LX/LX2/{L}.html"], capture_output=True, text=True, check=True).stdout
for c in cards:
    txt = LESSON_TXT[c["lesson"]]
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"] + " " + c["front"]))
    missing = [n for n in sorted(nums, key=lambda x: (len(x), x)) if n not in txt]
    if missing:
        print(c["id"], c["lesson"], "numbers not found verbatim in lesson text:", missing)
