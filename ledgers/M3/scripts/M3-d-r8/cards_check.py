import json, re, html, collections
base = "course/modules/M/M3/"
cards = json.load(open(base + "cards.json"))
print("cards", len(cards), "keys", collections.Counter(tuple(sorted(c)) for c in cards))
ids = [c["id"] for c in cards]
print("dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
print("dup fronts", [k for k, v in collections.Counter(c["front"] for c in cards).items() if v > 1])
print("dup backs", [k for k, v in collections.Counter(c["back"] for c in cards).items() if v > 1])
print("grades", collections.Counter(c.get("grade") for c in cards))
lessons = {}
for L in sorted(set(c["lesson"] for c in cards)):
    raw = open(base + L + ".html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lessons[L] = re.sub(r"\s+", " ", txt)
missing = []
for c in cards:
    text = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d+(?:\.\d+)?", text))
    for n in sorted(nums):
        if n not in lessons[c["lesson"]]:
            missing.append((c["id"], n))
print("numbers not found verbatim in own lesson text:", missing)
