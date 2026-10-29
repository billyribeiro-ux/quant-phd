import json, re, collections
cards = json.load(open("course/modules/M/M3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
dups = [i for i, n in collections.Counter(ids).items() if n > 1]
print("total", len(cards), "dup ids", dups)
txt = {n: open(f"/tmp/m3b7/{n}.txt", encoding="utf-8").read() for n in ["L04", "L05", "L06"]}
by = collections.Counter(c["lesson"] for c in cards)
print("per lesson", dict(by))
for c in cards:
    if c["lesson"] not in txt: continue
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"]))
    missing = [x for x in nums if x not in txt[c["lesson"]] and x not in c["front"]]
    if c["id"] in ("M3-c084", "M3-c180") or missing:
        print(c["id"], c["lesson"], c["grade"], "missing numbers:", missing)
        print("  front:", c["front"]); print("  back:", c["back"][:160])
