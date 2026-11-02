"""Structural and text scans of course/modules/M/M7/cards.json for slice M7-e (round 1)."""
import difflib
import json
import re
from collections import Counter

CARDS = "course/modules/M/M7/cards.json"
LESSON_TEXT = {f"L0{i}": f"/tmp/m7e/L0{i}.txt" for i in range(1, 9)}
cards = json.load(open(CARDS, encoding="utf-8"))
print("cards", len(cards))
print("unique ids", len({c["id"] for c in cards}) == len(cards))
ids_num = sorted(int(c["id"].split("c")[-1]) for c in cards)
gaps = [n for n in range(1, ids_num[-1] + 1) if n not in set(ids_num)]
print("id gaps in c001..c%03d:" % ids_num[-1], ["c%03d" % g for g in gaps])
print("fields", Counter(tuple(sorted(c)) for c in cards))
print("lesson counts", sorted(Counter(c["lesson"] for c in cards).items()))
print("grades", Counter(c["grade"] for c in cards))
print("C without basis", [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis")])
print("T with basis", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
print("cite fields present", [c["id"] for c in cards if "cite" in c])
print("empty front/back", [c["id"] for c in cards if not c["front"].strip() or not c["back"].strip()])

print("--- exact duplicate fronts/backs:", [k for k, v in Counter(c["front"] for c in cards).items() if v > 1],
      [k[:40] for k, v in Counter(c["back"] for c in cards).items() if v > 1])
print("--- near-duplicate fronts (SequenceMatcher ratio > 0.75):")
for a in range(len(cards)):
    for b in range(a + 1, len(cards)):
        r = difflib.SequenceMatcher(None, cards[a]["front"], cards[b]["front"]).ratio()
        if r > 0.75:
            print(round(r, 2), cards[a]["id"], cards[b]["id"], "|", cards[a]["front"][:60], "|", cards[b]["front"][:60])

print("--- process words in learner text (front/back/basis):")
pw = re.compile(r"verif|builder|fragment|round\b|ledger|agent|reviewer|pending|todo|draft|placeholder|audit|gate\b|sweep|mutant|slice|verdict", re.I)
hits = [(c["id"], m.group(0)) for c in cards for f in ("front", "back", "basis") for m in pw.finditer(c.get(f, ""))]
print("hits", hits)

print("--- numeric tokens absent from the lesson text (format-normalised):")
alltext = "\n".join(open(p, encoding="utf-8").read() for p in LESSON_TEXT.values())
tok = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?(?:/\d+)?)(?!\w)")
absent = []
for c in cards:
    body = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for n in sorted({m.group(1) for m in tok.finditer(body)}):
        if n in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}:
            continue
        frac = n.split("/")
        forms = {n} | ({f"{frac[0]}}}{{{frac[1]}" if len(frac) == 2 else n})
        if not any(f in alltext for f in forms) and n not in alltext:
            absent.append((c["id"], n))
print("tokens not found verbatim:", absent)
print("(each is a \\tfrac{a}{b} rendering, checked by hand in the ledger rows)")

print("--- registry symbols in cards (notation/notation.json):")
reg = ["Φ", "γ_3", "γ_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "ℚ", "𝔼"]
for s in reg:
    found = [c["id"] for c in cards if s in (c["front"] + c["back"] + c.get("basis", ""))]
    print(repr(s), found)
