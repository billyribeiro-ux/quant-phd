import json, re, sys, collections
ROOT = sys.argv[1]
base = f"{ROOT}/course/modules/FC/FC2"
cards = json.load(open(f"{base}/cards.json"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
dup = [k for k, v in collections.Counter(ids).items() if v > 1]
print("duplicate ids:", dup)
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets:", dict(keys))
lessons = {}
for L in sorted(set(c["lesson"] for c in cards)):
    lessons[L] = open(f"{base}/{L}.html", encoding="utf-8").read()
bad = []
for c in cards:
    if c["lesson"] not in lessons:
        bad.append((c["id"], "no lesson"))
    if c.get("grade") not in (None, "T", "C", "E", "U"):
        bad.append((c["id"], "grade", c.get("grade")))
    if c.get("grade") == "T" and "basis" not in c:
        bad.append((c["id"], "T without basis"))
    if "basis" in c and c.get("grade") is None:
        bad.append((c["id"], "basis without grade"))
print("structural issues:", bad)
# numbers in card text must appear in the lesson text
numpat = re.compile(r"(?<![\w.])\d+(?:[./]\d+)?(?![\w])")
for c in cards:
    txt = c["front"] + " " + c["back"]
    nums = set(numpat.findall(txt))
    lt = lessons.get(c["lesson"], "")
    missing = [n for n in nums if n not in lt and n not in txt.replace(n, "", 0) or False]
    missing = [n for n in nums if n not in lt]
    if missing:
        print("numbers not in lesson", c["id"], c["lesson"], missing)
print("ids sorted:", ids == sorted(ids))
print("first/last:", ids[0], ids[-1])
