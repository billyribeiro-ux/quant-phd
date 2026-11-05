import json, re, sys, collections, difflib, html
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/LX/LX1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)) == len(ids), "unique fronts", len({c["front"] for c in cards}) == len(cards))
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
for k, v in keys.items(): print("key set", v, k)
print("grades", collections.Counter(c.get("grade") for c in cards))
bad = [c["id"] for c in cards if ("grade" in c) != ("basis" in c)]
print("grade/basis mismatch", bad)
print("cite nonempty", [c["id"] for c in cards if c["cite"]])
print("lesson field counts", collections.Counter(c["lesson"] for c in cards))
print("ids sorted", ids == sorted(ids), [i for i in ids if not re.fullmatch(r"LX1-c\d{3}", i)])
nums = [int(i[-3:]) for i in ids]
print("missing ids in 1..81:", [n for n in range(1, 82) if n not in nums])
# near duplicates
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = cards[i]["front"] + " " + cards[i]["back"]
        b = cards[j]["front"] + " " + cards[j]["back"]
        r = difflib.SequenceMatcher(None, a, b).quick_ratio()
        if r > 0.85:
            r2 = difflib.SequenceMatcher(None, a, b).ratio()
            pairs.append((cards[i]["id"], cards[j]["id"], round(r2, 3)))
print("near-dup pairs (quick_ratio>0.85) with ratio:", pairs)
# process words
pw = re.compile(r"verif|builder|round|audit|ledger|draft|todo|fragment|pending|reviewer|agent|lab-?\d|ledger", re.I)
for c in cards:
    t = c["front"] + " | " + c["back"] + " | " + c.get("basis", "")
    for m in pw.finditer(t):
        print("process-word hit", c["id"], repr(t[max(0, m.start()-30):m.end()+30]))
# numeric tokens in back vs lesson text
lessons = {}
for lid in ["L01", "L02", "L03", "L04"]:
    src = open(f"{root}/course/modules/LX/LX1/{lid}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", " ", src))
    lessons[lid] = txt
for c in cards:
    toks = set(re.findall(r"\d+(?:\.\d+)?", c["back"] + " " + c["front"]))
    missing = [t for t in sorted(toks) if t not in lessons[c["lesson"]] and t not in lessons["L01"] + lessons["L02"] + lessons["L03"] + lessons["L04"]]
    if missing:
        print("number not in any lesson", c["id"], missing)
    miss_own = [t for t in sorted(toks) if t not in lessons[c["lesson"]]]
    if miss_own:
        print("number not in own lesson", c["id"], c["lesson"], miss_own)
