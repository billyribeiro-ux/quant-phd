import json, re, collections, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB9-M2-b/course/modules/M/M2")
cards = json.load(open(root / "cards.json"))
slice_ = [c for c in cards if c["lesson"] in {f"L{n:02d}" for n in range(7, 13)}]
print("total cards", len(cards), "slice cards", len(slice_))
print(collections.Counter(c["lesson"] for c in slice_))
ids = collections.Counter(c["id"] for c in cards)
print("dup ids", [k for k, v in ids.items() if v > 1])
fr = collections.Counter(c["front"] for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1])
for c in slice_:
    html = (root / f"{c['lesson']}.html").read_text()
    nums = set(re.findall(r"(Theorem|Lemma|Corollary|Proposition|Example|Remark|Lesson|Problem|Definition|Assumption) (\d+(?:\.\d+)?)", c["back"] + " " + c["front"]))
    for kind, n in sorted(nums):
        if kind == "Lesson":
            continue
        if f"{kind} {n}" not in html:
            print("MISSING", c["id"], c["lesson"], kind, n, "|", c["front"][:80])
    for k in ("grade",):
        if k not in c: print("NOGRADE", c["id"])
# verbatim check of cards for L11 and L07-L12 with monotone / lemma clause
for c in slice_:
    t = c["back"]
    if "monotone" in t or "Lemma 1.1" in t:
        print("MONO/LEMMA", c["id"], c["lesson"], t[:300])
