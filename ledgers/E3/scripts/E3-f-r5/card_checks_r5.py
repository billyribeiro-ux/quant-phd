import json, re, html, sys
from collections import Counter
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E3/cards.json"))
lines = open(f"{root}/course/modules/E/E3/cards.json", encoding="utf-8").read().split("\n")
slice_cards = [c for c in cards if c["lesson"] in ("L01", "L02", "L03", "L04")]
print("slice cards:", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids in file:", [k for k, v in ids.items() if v > 1])
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fr = Counter(norm(c["front"]) for c in cards)
print("duplicate normalised fronts:", [k for k, v in fr.items() if v > 1])
bk = Counter(norm(c["back"]) for c in cards)
print("duplicate normalised backs:", [k for k, v in bk.items() if v > 1])
lessons = {}
for L in ("L01", "L02", "L03", "L04"):
    t = html.unescape(re.sub(r"<[^>]+>", " ", open(f"{root}/course/modules/E/E3/{L}.html", encoding="utf-8").read()))
    t = re.sub(r"\s+", " ", t)
    lessons[L] = t
nums = []
for c in slice_cards:
    for tok in re.findall(r"\d+(?:\.\d+)?", c["back"]):
        if tok in ("1", "2", "0", "3"):
            continue
        if tok not in lessons[c["lesson"]]:
            nums.append((c["id"], tok))
print("numeric tokens (excluding 0-3) absent from own lesson:", nums)
miss = []
for c in slice_cards:
    for tok in re.findall(r"\d+(?:\.\d+)?", c["back"]):
        if tok in ("0", "1", "2", "3"):
            continue
        pass
for c in slice_cards:
    print(c["id"], c["lesson"], "grade=", c.get("grade"), "basis=", c.get("basis"), "| back-len", len(c["back"]))
