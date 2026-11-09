import json, re, collections, pathlib
cards = json.load(open("/Users/billyribeiro/.fanout/wt/verifyG1-M2-b/course/modules/M/M2/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
print("total", len(cards), "dup ids", [k for k, v in ids.items() if v > 1])
def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
fr = collections.Counter(norm(c["front"]) for c in cards)
print("dup normalized fronts", [k for k, v in fr.items() if v > 1])
bk = collections.Counter(norm(c["back"]) for c in cards)
print("dup normalized backs", [k for k, v in bk.items() if v > 1])
text = {}
for i in range(7, 13):
    text[f"L{i:02d}"] = pathlib.Path(f"/tmp/M2b_text/L{i:02d}.txt").read_text(encoding="utf-8")
changed = ["M2-c096","M2-c099","M2-c102","M2-c104","M2-c107","M2-c111","M2-c112","M2-c113","M2-c114",
           "M2-c134","M2-c143","M2-c145","M2-c146","M2-c147","M2-c152","M2-c161","M2-c162","M2-c163",
           "M2-c169","M2-c177","M2-c178","M2-c180","M2-c422","M2-c423","M2-c425"]
byid = {c["id"]: c for c in cards}
for k in changed:
    c = byid[k]
    nums = re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", c["back"])
    lt = text[c["lesson"]]
    missing = [n for n in nums if n not in lt]
    print(k, c["lesson"], c.get("grade"), "numbers not in lesson text:", missing)
