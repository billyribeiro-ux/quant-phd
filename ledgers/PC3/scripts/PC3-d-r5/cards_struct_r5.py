"""Structure, grade/basis agreement, cite and duplicate scan for PC3 cards.json, plus numeric tokens of each card
that must appear in its own lesson text (VERIFIER_RULES 2.7; BUILDER_RULES 7).

Usage: python -I ledgers/PC3/scripts/PC3-d-r5/cards_struct_r5.py <checkout> <lesson_text_dir>
"""
import collections
import difflib
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
ltxt = pathlib.Path(sys.argv[2])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
nums = [int(i.split("-c")[1]) for i in ids]
print("cards", len(cards), "unique ids", len(set(ids)), "prefix ok", all(i.startswith("PC3-c") for i in ids))
print("missing numbers", [n for n in range(1, max(nums) + 1) if n not in nums], "ids in ascending order", nums == sorted(nums))
print("grade counts", collections.Counter(c.get("grade") for c in cards))
print("per lesson", collections.Counter(c["lesson"] for c in cards))
print("cite non-empty", [c["id"] for c in cards if c["cite"]])
print("grade without basis", [c["id"] for c in cards if c.get("grade") and not c.get("basis")])
print("basis without grade", [c["id"] for c in cards if c.get("basis") and not c.get("grade")])
print("empty front/back", [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()])
print("placeholder words", [c["id"] for c in cards if re.search(r"TODO|TBD|lorem|\.\.\.", c["front"] + c["back"])])
print("process words", [c["id"] for c in cards if re.search(r"\b(verified|checked by|this card|the lab checks)\b", (c["front"] + c["back"]).lower())])
# exact duplicate fronts or backs
fr = collections.Counter(c["front"] for c in cards)
bk = collections.Counter(c["back"] for c in cards)
print("exact duplicate fronts", [f for f, n in fr.items() if n > 1])
print("exact duplicate backs", [f[:60] for f, n in bk.items() if n > 1])
print("== near-duplicate pairs (front+back ratio > 0.55)")
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = cards[i]["front"] + " " + cards[i]["back"]
        b = cards[j]["front"] + " " + cards[j]["back"]
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r > 0.55:
            pairs.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
for r, a, b in sorted(pairs, reverse=True):
    print(f"  {r} {a} {b}")
print("== numeric tokens of each card vs its own lesson text (after whitespace and comma removal)")
lessons = {}
for n in range(1, 7):
    t = (ltxt / f"L{n:02d}.txt").read_text(encoding="utf-8")
    lessons[f"L{n:02d}"] = re.sub(r"\s+", "", t.replace(",", "").replace(" ", "")).replace("\\,", "")
bad = []
for c in cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for tok in re.findall(r"\d+(?:\.\d+)?", text.replace(",", "")):
        if len(tok) < 2:
            continue
        if tok not in lessons[c["lesson"]].replace(" ", ""):
            bad.append((c["id"], c["lesson"], tok))
print("tokens absent from own lesson:", len(bad))
for b in bad:
    print("  ", b)
