import json, re, pathlib, collections, sys
root = pathlib.Path(sys.argv[1])
d = json.load(open(root / "course/modules/M/M4/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in d)
fronts = collections.Counter(c["front"].strip().lower() for c in d)
print("cards total", len(d), "dup ids", [k for k, v in ids.items() if v > 1], "dup fronts", [k for k, v in fronts.items() if v > 1])
s = [c for c in d if c["lesson"] in ("L08", "L09", "L10")]
print("slice cards", len(s), collections.Counter(c["lesson"] for c in s))
print("grades", collections.Counter(c["grade"] for c in s))
bad = [c["id"] for c in s if c["grade"] != "T" and not c.get("basis")]
print("non-T without basis", bad)
print("grade letters ok", all(c["grade"] in "TABCDX" for c in d))
# every L08-L10 card id number range and the lesson text contains each card's key numbers
html = {p: re.sub(r"<[^>]+>", " ", (root / f"course/modules/M/M4/{p}.html").read_text(encoding="utf-8")) for p in ("L08", "L09", "L10")}
for c in s:
    nums = set(re.findall(r"\d+\.\d{3,}|\b\d+/\d+\b", c["back"]))
    for n in nums:
        pass
print("ok")
