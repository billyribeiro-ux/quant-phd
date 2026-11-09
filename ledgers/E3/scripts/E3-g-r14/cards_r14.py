"""Round-14 card checks for E3 L05-L08: number/label references resolve in the lesson text; duplicates; scope and process words.

Run as: python -I ledgers/E3/scripts/E3-g-r14/cards_r14.py
Reads course/modules/E/E3/cards.json and the lesson text written by extract_text.py into the scratch dir.
"""
import difflib
import json
import re
import sys

SCRATCH = "/Users/billyribeiro/.fanout/scratch/E3-g-r14"
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in ("L05", "L06", "L07", "L08")]
text = {L: open(f"{SCRATCH}/{L}.txt", encoding="utf-8").read() for L in ("L05", "L06", "L07", "L08")}
print("slice cards:", len(slice_cards), {L: sum(1 for c in slice_cards if c["lesson"] == L) for L in text})
print("all cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
print("unique fronts (all):", len({c["front"] for c in cards}), "unique backs (all):", len({c["back"] for c in cards}))

LABEL = re.compile(r"\b(Proposition|Theorem|Corollary|Remark|Definition|Example|Problem|Lemma)\s+([0-9]+\.[0-9]+|[A-Z][0-9]+)\b")
SECTION = re.compile(r"\b[Ss]ection\s+([0-9]+)\b")
LAB = re.compile(r"Lab 1, part ([A-Z])\b")
bad = []
for c in slice_cards:
    L = c["lesson"]
    body = text[L]
    for kind, num in LABEL.findall(c["back"] + " " + c["front"]):
        # the label must occur in the card's own lesson, or in the lesson it cites
        if f"{kind} {num}" not in body and not any(f"{kind} {num}" in text[X] for X in text):
            bad.append((c["id"], f"{kind} {num}", "absent from all lesson text"))
        elif f"{kind} {num}" not in body:
            bad.append((c["id"], f"{kind} {num}", f"absent from {L}"))
    for num in SECTION.findall(c["back"] + " " + c["front"]):
        if not re.search(rf"^\s*{num}[A-Z]", body, re.M) and not re.search(rf"Section {num}\b", body):
            bad.append((c["id"], f"section {num}", f"no 'section {num}' heading in {L}"))
    if LAB.search(c["back"]) and "Lab 1" not in body:
        bad.append((c["id"], "Lab 1", "absent"))
print("unresolved label references:", len(bad))
for b in bad:
    print("  ", b)

# near duplicates inside the slice (fronts and backs)
dups = []
for i, a in enumerate(slice_cards):
    for b in slice_cards[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.6 or rb > 0.6:
            dups.append((a["id"], b["id"], round(rf, 2), round(rb, 2)))
print("near-duplicate pairs in slice (front or back ratio > 0.6):")
for d in dups:
    print("  ", d)

SCOPE = re.compile(r"\b(only|all|always|every|any|same|drives|exactly|never|none)\b", re.I)
PROCESS = re.compile(r"\b(round|verifier|builder|ledger|fragment|checkout|pin|agent|claude|slice)\b", re.I)
print("scope words in slice card backs:")
for c in slice_cards:
    hits = sorted(set(m.group(0).lower() for m in SCOPE.finditer(c["back"] + " " + c["front"])))
    if hits:
        print("  ", c["id"], hits)
print("process words in slice cards:")
for c in slice_cards:
    hits = sorted(set(m.group(0).lower() for m in PROCESS.finditer(c["back"] + " " + c["front"])))
    if hits:
        print("  ", c["id"], hits)
print("E3-c131 present:", any(c["id"] == "E3-c131" for c in cards))
print("grade field missing in slice:", [c["id"] for c in slice_cards if "grade" not in c])
sys.exit(0)
