"""Mechanical audit of LX1 cards.json against the extracted lesson text (slice d, round 1).

For each card: (1) every decimal/integer token in front+back appears in its lesson's visible text
(text produced by extract_text.py into the directory given as argv[1]); (2) duplicate detection by
normalised front (token-set Jaccard >= 0.6); (3) id sequence, lesson, grade and basis fields.
Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-d-r1/card_audit.py <textdir>
"""
import json
import re
import sys

textdir = sys.argv[1]
cards = json.load(open("/Users/billyribeiro/.fanout/wt/verifyE1-LX1-d/course/modules/LX/LX1/cards.json", encoding="utf-8"))
lessons = {}
for L in ("L01", "L02", "L03", "L04"):
    lessons[L] = open(f"{textdir}/lx1d_{L}.txt", encoding="utf-8").read()
    # normalise: drop line numbers, collapse whitespace, drop LaTeX braces/backslashes for number lookup
    lessons[L] = re.sub(r"\s+", " ", re.sub(r"^\s*\d+\s", "", lessons[L], flags=re.M))
    lessons[L] = lessons[L].replace("\\", "").replace("{", "").replace("}", "")

num = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
problems = []
ids = [c["id"] for c in cards]
for i, c in enumerate(cards):
    expect = f"LX1-c{i + 1:03d}"
    if c["id"] != expect:
        problems.append(f"{c['id']}: sequence position {i + 1} expects {expect}")
    text = c["front"] + " " + c["back"]
    body = lessons[c["lesson"]]
    for tok in sorted(set(num.findall(text))):
        if tok not in body and tok.rstrip("0") not in body:
            problems.append(f"{c['id']}: token {tok!r} not found in {c['lesson']} text")
    if "grade" in c and c["grade"] == "T" and not c.get("basis"):
        problems.append(f"{c['id']}: T without basis")

def toks(s):
    return set(re.findall(r"[a-z0-9_.]+", s.lower())) - {"the", "a", "of", "in", "and", "is", "to", "for", "what", "does", "with", "at", "by", "on", "whether", "its"}

for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = toks(cards[i]["front"]), toks(cards[j]["front"])
        if a and b and len(a & b) / len(a | b) >= 0.6:
            print(f"near-duplicate fronts: {cards[i]['id']} / {cards[j]['id']} jaccard={len(a & b) / len(a | b):.2f}")

print("cards:", len(cards), "unique ids:", len(set(ids)))
print("per lesson:", {L: sum(1 for c in cards if c["lesson"] == L) for L in lessons})
print("grades:", {g: sum(1 for c in cards if c.get("grade") == g) for g in ("T", "C", None)})
print("problems:", len(problems))
for p in problems:
    print("  ", p)
