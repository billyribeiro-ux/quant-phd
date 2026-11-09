import json, re, collections, html
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF21-M6-c"
cards = json.load(open(f"{ROOT}/course/modules/M/M6/cards.json", encoding="utf-8"))
print("total cards", len(cards))
ids = [c["id"] for c in cards]
dup_ids = [k for k, v in collections.Counter(ids).items() if v > 1]
fronts = [c["front"].strip().lower() for c in cards]
dup_fronts = [k for k, v in collections.Counter(fronts).items() if v > 1]
print("duplicate ids", dup_ids, "duplicate fronts", dup_fronts)
print("bad prefix", [c["id"] for c in cards if not c["id"].startswith("M6-c")])
lessons = {}
for L in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12"]:
    raw = open(f"{ROOT}/course/modules/M/M6/{L}.html", encoding="utf-8").read()
    lessons[L] = html.unescape(re.sub(r"</?[a-zA-Z!][^>]*>", " ", raw))
print("grades", collections.Counter(c.get("grade") for c in cards))
slice_L = {"L09", "L10", "L11", "L12"}
missing = []
for c in cards:
    if c["lesson"] not in lessons:
        print("UNKNOWN LESSON", c["id"], c["lesson"])
        continue
    if c["lesson"] in slice_L or c["id"] in ("M6-c147", "M6-c148", "M6-c149"):
        nums = set(re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"]))
        for n in nums:
            if n not in lessons[c["lesson"]]:
                missing.append((c["id"], c["lesson"], n))
print("numbers in card text absent from its own lesson (L09-L12 cards and c147-c149):")
for m in missing:
    print("  ", m)
sl = [c for c in cards if c["lesson"] in slice_L]
print("cards in L09-L12:", len(sl))
print(sorted(c["id"] for c in sl))
for cid in ["M6-c102", "M6-c110", "M6-c137", "M6-c141", "M6-c148", "M6-c142", "M6-c143", "M6-c146"]:
    hit = [c for c in cards if c["id"] == cid]
    print(cid, "PRESENT" if hit else "ABSENT", (hit[0]["lesson"], hit[0].get("grade")) if hit else "")
print("references to M6-c137 in cards:", [c["id"] for c in cards if "c137" in json.dumps(c)])
