"""M5 slice b (L05-L07) card scan: grade/basis rules, per-card lesson numbers, duplicate candidates."""
import json, re, sys, difflib, itertools
path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in ("L05", "L06", "L07")]
print("slice cards", len(sl), "total", len(cards), "dup ids", len(cards) - len({c["id"] for c in cards}))
for c in sl:
    g = c.get("grade"); b = c.get("basis")
    if g == "T" and not (b and b.strip()):
        print("NO BASIS (T)", c["id"])
    if g == "C" and not (b and b.strip()):
        print("NO BASIS (C)", c["id"])
    if g is None and b is not None:
        print("BASIS WITHOUT GRADE", c["id"])
print("ungraded slice cards:", [c["id"] for c in sl if "grade" not in c])
def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower())
pairs = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, norm(a["front"] + " " + a["back"]), norm(b["front"] + " " + b["back"])).ratio()
    if r >= 0.45 and (a["lesson"] in ("L05", "L06", "L07") or b["lesson"] in ("L05", "L06", "L07")):
        pairs.append((round(r, 3), a["id"], a["lesson"], b["id"], b["lesson"]))
for p in sorted(pairs, reverse=True)[:25]:
    print("SIMILAR", p)
# numbers on cards must occur in their lesson text
html = {}
for L in ("L05", "L06", "L07"):
    html[L] = open(f"course/modules/M/M5/{L}.html", encoding="utf-8").read()
for c in sl:
    nums = re.findall(r"\d+\.\d+|\d{2,}", c["back"])
    for n in nums:
        if n not in html[c["lesson"]]:
            print("NUMBER NOT IN LESSON", c["id"], n)
print("number check done")
