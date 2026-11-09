"""Slice e round 1 card scans: ids, keys, grades, process words, banned phrases, near duplicates, numbers vs lesson."""
import difflib
import json
import re
import sys
from collections import Counter

CARDS = sys.argv[1]
OUT = sys.argv[2]
cards = json.load(open(CARDS, encoding="utf-8"))
lessons = {f"L0{i}": open(f"{OUT}/L0{i}.txt", encoding="utf-8").read() for i in range(1, 9)}
ids = [c["id"] for c in cards]
print("cards:", len(cards), "distinct ids:", len(set(ids)))
print("id pattern ok:", all(re.fullmatch(r"SC1-c\d{3}", i) for i in ids))
print("lesson counts:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("grade counts:", dict(Counter(c.get("grade", "none") for c in cards)))
print("key sets:", dict(Counter(tuple(sorted(c.keys())) for c in cards)))
proc = re.compile(r"\b(builder|verifier|round|fixer|ledger|reviewer|sub-?agent)\b", re.I)
banned = ["TODO", "TBD", "lorem", "for brevity", "omitted", "beyond the scope", "exercise", "obviously", "clearly",
          "historically", "roughly", "well known", "important to note", "studies show", "you can add more"]
for c in cards:
    t = c["front"] + " " + c["back"]
    if proc.search(t):
        print("process word:", c["id"], proc.findall(t))
    for b in banned:
        if b.lower() in t.lower():
            print("banned phrase:", c["id"], b)
for k in range(1, 9):
    for lab in ("L0%d" % k,):
        pass
for lesson in lessons:
    if proc.search(lessons[lesson]):
        print("process word in lesson", lesson, proc.findall(lessons[lesson])[:5])
    for b in banned:
        if b.lower() in lessons[lesson].lower():
            print("banned phrase in", lesson, b)
dups = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        if a["front"] == b["front"] or a["back"] == b["back"]:
            print("IDENTICAL front or back:", a["id"], b["id"])
        r = difflib.SequenceMatcher(None, a["front"] + " " + a["back"], b["front"] + " " + b["back"]).ratio()
        if r >= 0.6:
            dups.append((round(r, 3), a["id"], b["id"]))
for d in sorted(dups, reverse=True):
    print("near-dup", d)
num = re.compile(r"\d+(?:\.\d+)?")
missing = []
ntok = 0
for c in cards:
    toks = set(num.findall(c["front"] + " " + c["back"]))
    ntok += len(toks)
    lt = lessons[c["lesson"]]
    for tok in toks:
        if tok not in lt:
            missing.append((c["id"], tok))
print("numeric tokens in cards:", ntok, "absent from own lesson text:", len(missing))
for m in missing[:60]:
    print("  absent:", m)
