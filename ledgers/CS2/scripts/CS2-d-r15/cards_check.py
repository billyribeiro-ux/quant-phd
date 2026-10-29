import json, re, html, collections, sys
base = "/Users/billyribeiro/.fanout/wt/verifyB15-CS2-d/course/modules/CS/CS2/"
cards = json.load(open(base + "cards.json"))
ids = [c["id"] for c in cards]
print("count", len(cards), "unique ids", len(set(ids)))
dups = [k for k, v in collections.Counter(ids).items() if v > 1]
print("duplicate ids", dups)
fronts = collections.Counter(c["front"] for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(c["back"] for c in cards)
print("duplicate backs", [k for k, v in backs.items() if v > 1])
print("grades", collections.Counter(c["grade"] for c in cards))
bad = []
for c in cards:
    if c["grade"] == "C" and not c.get("basis"):
        bad.append((c["id"], "C without basis"))
    if c["grade"] == "T" and "basis" in c:
        bad.append((c["id"], "T with basis"))
    if c["grade"] not in ("T", "C"):
        bad.append((c["id"], "bad grade"))
    if set(c.keys()) - {"id", "lesson", "front", "back", "grade", "basis"}:
        bad.append((c["id"], "extra keys " + str(set(c.keys()))))
print("structure problems", bad)
# numbers in back must appear in the lesson text
lessons = {}
for c in cards:
    L = c["lesson"]
    if L not in lessons:
        try:
            raw = open(base + L + ".html", encoding="utf-8").read()
        except FileNotFoundError:
            lessons[L] = None
            continue
        txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        lessons[L] = re.sub(r"\s+", " ", txt)
missing = []
for c in cards:
    txt = lessons.get(c["lesson"])
    if txt is None:
        missing.append((c["id"], "lesson file missing"))
        continue
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["back"]))
    for n in nums:
        if n not in txt:
            missing.append((c["id"], n))
print("numbers not in lesson text (token search):")
for m in missing: print("  ", m)
