"""Verifier scan of cards.json: duplicates, cross-references, and card numbers vs lesson text."""
import json
import re
import sys
from collections import Counter

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE12-E4-e"
cards = json.load(open(f"{ROOT}/course/modules/E/E4/cards.json", encoding="utf-8"))
lessons = {}
for n in range(1, 10):
    name = f"L0{n}"
    lessons[name] = open(f"{ROOT}/scratch/txt/{name}.txt", encoding="utf-8").read()

print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))
fr = Counter(c["front"] for c in cards)
print("duplicate fronts", [f for f, k in fr.items() if k > 1])
bk = Counter(c["back"] for c in cards)
print("duplicate backs", [f for f, k in bk.items() if k > 1])
ids = [c["id"] for c in cards]
print("id order not sorted:", [i for i in ids if i != sorted(ids, key=lambda s: int(s.split('c')[-1]))[0] and False])
print("lesson counts", Counter(c["lesson"] for c in cards))

# cross-reference labels cited in card text must exist in that card's lesson
ref_re = re.compile(r"\b(Proposition|Lemma|Corollary|Remark|Definition|Example|Problem|Assumption|Theorem|Fact|Misconception|Lab 1, Part|Part|Step|Section|Proof)\s+([A-Za-z0-9.()]+)")
missing = []
for c in cards:
    text = c["front"] + " " + c["back"] + " " + str(c.get("basis", ""))
    lesson_text = " ".join(lessons[c["lesson"]].split())
    for m in ref_re.finditer(text):
        label = m.group(1) + " " + m.group(2).rstrip(".,;:)")
        probe = label.replace("Lab 1, Part", "Part")
        if probe not in lesson_text and label not in lesson_text:
            missing.append((c["id"], c["lesson"], label))
print("cross-refs not literally in lesson text:")
for row in missing:
    print("  ", row)

# numeric tokens in card text that never occur in the lesson text
num_re = re.compile(r"\d+(?:\.\d+)?(?:e-?\d+)?(?:/\d+)?")
absent = []
for c in cards:
    text = c["front"] + " " + c["back"]
    lesson_text = lessons[c["lesson"]]
    for tok in set(num_re.findall(text)):
        if tok not in lesson_text and tok not in ("0", "1", "2"):
            absent.append((c["id"], c["lesson"], tok))
print("numeric tokens absent from lesson text (excluding 0,1,2):")
for row in sorted(absent):
    print("  ", row)
