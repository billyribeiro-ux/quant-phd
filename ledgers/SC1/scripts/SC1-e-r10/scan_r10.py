"""Round 10 scans over cards.json and the rendered lesson text (no lab code imported).

Usage: python -I scan_r10.py <cards.json> <out_dir>
"""
import difflib
import json
import os
import re
import sys

cards_path, out_dir = sys.argv[1], sys.argv[2]
cards = json.load(open(cards_path, encoding="utf-8"))
lesson = {}
for L in range(1, 9):
    lesson[f"L0{L}"] = open(os.path.join(out_dir, f"L0{L}.txt"), encoding="utf-8").read()
ids = [c["id"] for c in cards]
print("cards", len(cards), "distinct ids", len(set(ids)), "all SC1-cNNN", all(re.fullmatch(r"SC1-c\d{3}", i) for i in ids))
print("key sets", sorted({tuple(sorted(c)) for c in cards}))
print("cite nonempty", [c["id"] for c in cards if c.get("cite")])
print("grade missing", [c["id"] for c in cards if "grade" not in c])
print("grade values", sorted({c.get("grade") for c in cards}, key=str))
print("T/C cards without basis", [c["id"] for c in cards if c.get("grade") in ("T", "C") and not c.get("basis")])
print("T-or-C grade counts", sum(1 for c in cards if c.get("grade") == "T"), sum(1 for c in cards if c.get("grade") == "C"))
bad = ["builder", "verifier", "round ", "fixer", "ledger", "reviewer", "sub-agent", "subagent", "Round "]
for c in cards:
    text = c["front"] + " " + c["back"]
    for w in bad:
        if w.lower() in text.lower():
            print("PROCESS WORD", c["id"], w)
print("concept markup", [c["id"] for c in cards if "data-concept" in (c["front"] + c["back"])])
# identical fronts or backs
fr = {}
bk = {}
for c in cards:
    fr.setdefault(c["front"], []).append(c["id"])
    bk.setdefault(c["back"], []).append(c["id"])
print("identical fronts", [v for v in fr.values() if len(v) > 1])
print("identical backs", [v for v in bk.values() if len(v) > 1])
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, cards[i]["front"] + " " + cards[i]["back"], cards[j]["front"] + " " + cards[j]["back"]).ratio()
        if r >= 0.6:
            pairs.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
print("near-duplicate pairs (ratio>=0.6, front+back)", sorted(pairs, reverse=True))
# numeric tokens of each card vs its own lesson text
miss = []
ntok = 0
for c in cards:
    toks = set(re.findall(r"\d+\.\d+|\d{2,}", c["front"] + " " + c["back"]))
    ntok += len(toks)
    txt = lesson.get(c["lesson"], "")
    for t in toks:
        if t not in txt:
            miss.append((c["id"], t))
print("numeric tokens", ntok, "absent from own lesson", miss)
# cross references: 'Lemma x', 'Proposition x', 'Theorem x', 'Corollary x', 'Remark x', 'Problem X' in card vs own lesson
refs = []
for c in cards:
    for m in re.findall(r"(Lemma|Proposition|Theorem|Corollary|Remark|Example|Definition|Problem|Assumption|Lab) (\d+(?:\.\d+)?|[A-Z]\d?)", c["front"] + " " + c["back"]):
        key = f"{m[0]} {m[1]}"
        refs.append((c["id"], c["lesson"], key))
absent = []
for cid, L, key in refs:
    if key.startswith("Lab"):
        continue
    if key not in lesson.get(L, "") and key.split()[-1] not in lesson.get(L, ""):
        absent.append((cid, L, key))
print("cross-reference tokens", len(refs), "not in own lesson text", absent)
# 'of Lesson K' references
ol = []
for c in cards:
    for m in re.findall(r"of Lesson (\d)", c["front"] + " " + c["back"]):
        ol.append((c["id"], m))
print("of Lesson refs", len(ol))
