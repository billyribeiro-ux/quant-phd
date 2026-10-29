import json, re, html, collections, sys
base = "/Users/billyribeiro/.fanout/wt/verifyB7-M5-d/course/modules/M/M5/"
cards = json.load(open(base + "cards.json"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)) == len(ids))
print("keys", collections.Counter(tuple(sorted(c.keys())) for c in cards))
print("per lesson", collections.Counter(c["lesson"] for c in cards))
print("grades", collections.Counter(c.get("grade") for c in cards))
lessons = {}
for n in range(1, 11):
    raw = open(base + f"L{n:02d}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lessons[f"L{n:02d}"] = txt
bad = []
for c in cards:
    if c["lesson"] not in lessons: bad.append((c["id"], "no lesson")); continue
    txt = lessons[c["lesson"]]
    for field in ("front", "back"):
        for num in re.findall(r"\d+(?:\.\d+)?", c[field]):
            if num not in txt:
                bad.append((c["id"], field, num))
    if c.get("grade") in ("T", "C") and "basis" not in c: bad.append((c["id"], "no basis"))
print("number-not-in-lesson:", bad)
# ordering
order = [int(c["id"].split("c")[-1]) for c in cards]
print("ids ascending:", order == sorted(order), "first/last", ids[0], ids[-1])
