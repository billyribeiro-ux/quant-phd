"""For each L05-L08 card, list every number in its front/back and whether it occurs in its own lesson dump.

Run: python -I ledgers/E3/scripts/E3-g-r3/card_numbers.py
Also prints a full-scan duplicate check over the 85 slice cards (exact front, exact back, and word-set Jaccard >= 0.6).
"""
import json
import re

ROOT = "."
TXT = f"{ROOT}/ledgers/E3/scripts/E3-g-r3/text"
lessons = {}
for L in ("L05", "L06", "L07", "L08"):
    raw = open(f"{TXT}/{L}.txt", encoding="utf-8").read()
    lessons[L] = raw.replace("\\", "")
cards = json.load(open(f"{ROOT}/course/modules/E/E3/cards.json", encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in lessons]
print("slice cards:", len(sl))
num_re = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
miss = []
for c in sl:
    text = c["front"] + " " + c["back"] + " " + str(c.get("basis", ""))
    lt = lessons[c["lesson"]]
    for m in sorted(set(num_re.findall(text))):
        if m in ("1", "0", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
            continue
        if m not in lt:
            miss.append((c["id"], c["lesson"], m))
print("numbers (>=2 chars, not single digits) absent from own lesson dump:", len(miss))
for x in miss:
    print("  ", x)

# duplicate scan over the whole card file
allc = cards
fronts = {}
backs = {}
for c in allc:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
    backs.setdefault(c["back"].strip().lower(), []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("exact duplicate backs:", [v for v in backs.values() if len(v) > 1])
ids = [c["id"] for c in allc]
print("card ids:", len(ids), "distinct:", len(set(ids)))


def words(c):
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))


pairs = []
for i, a in enumerate(sl):
    for b in sl[i + 1:]:
        wa, wb = words(a), words(b)
        j = len(wa & wb) / len(wa | wb)
        if j >= 0.5:
            pairs.append((round(j, 2), a["id"], b["id"]))
print("slice pairs with word Jaccard >= 0.5:")
for p in sorted(pairs, reverse=True):
    print("  ", p)
