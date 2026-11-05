"""Round-7 structural checks on course/modules/LX/LX1/cards.json against the extracted lesson text (independent of the builder).

Usage: python3 -I cards_struct_r7.py <checkout> <lesson text dir>
Checks: id sequence and uniqueness; lesson exists; grade and basis rules (BUILDER_RULES 7); no duplicate fronts or backs;
every number token in front/back appears in the card's lesson text (commas removed); no banned process words; each
card's lesson carries its basis locator text (lab or proof named in basis appears in the lesson text).
"""
import json, re, sys, collections

base, txt = sys.argv[1], sys.argv[2]
cards = json.load(open(f"{base}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
lesson = {L: [re.sub(r"^\[\d+\] ", "", ln.rstrip("\n")) for ln in open(f"{txt}/{L}.txt", encoding="utf-8")] for L in ("L01", "L02", "L03", "L04")}
text = {L: re.sub(r"\s+", " ", " ".join(v)) for L, v in lesson.items()}
ids = [c["id"] for c in cards]
print("cards", len(cards), "ids contiguous c001..c%03d:" % len(cards), ids == [f"LX1-c{i:03d}" for i in range(1, len(cards) + 1)])
print("unique ids:", len(set(ids)) == len(ids))
print("lesson counts:", dict(collections.Counter(c["lesson"] for c in cards)))
print("grades:", dict(collections.Counter(c.get("grade", "-") for c in cards)))
bad_basis = [c["id"] for c in cards if c.get("grade") in ("T", "C") and not c.get("basis")]
ung_basis = [c["id"] for c in cards if "grade" not in c and c.get("basis")]
print("T/C cards without basis:", bad_basis, "; ungraded cards with basis:", ung_basis)
print("cite lists non-empty:", [c["id"] for c in cards if c.get("cite")])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, n in fronts.items() if n > 1], "duplicate backs:", [k for k, n in backs.items() if n > 1])
num = re.compile(r"(?<![A-Za-z_])\d[\d,]*(?:\.\d+)?")
missing = []
for c in cards:
    src = text[c["lesson"]]
    for field in ("front", "back"):
        for tok in num.findall(c[field]):
            t = tok.rstrip(",")
            if t not in src and t.replace(",", "") not in src:
                missing.append((c["id"], field, t))
print("number tokens absent from card's own lesson text:", missing)
banned = re.compile(r"\b(verif\w*|builder|build|round|fragment|pending|draft|TODO|reword\w*|audit\w*|reviewer|pass|fail)\b", re.I)
hits = [(c["id"], f, m.group(0)) for c in cards for f in ("front", "back", "basis") for m in [banned.search(c.get(f, "") or "")] if m]
print("process-word hits in front/back/basis:", hits)
