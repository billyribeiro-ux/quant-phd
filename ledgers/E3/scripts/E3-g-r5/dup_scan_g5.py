import json, difflib, re, sys
cards = json.load(open("course/modules/E/E3/cards.json"))
ids = {c["id"]: c for c in cards}
slice_ids = [c["id"] for c in cards if c.get("lesson") in ("L05","L06","L07","L08")]
print("total cards", len(cards), "slice cards", len(slice_ids), "ids unique", len(ids)==len(cards))
def norm(s): return re.sub(r"\s+"," ",s.lower()).strip()
fronts = {}; backs = {}
for c in cards:
    fronts.setdefault(norm(c["front"]), []).append(c["id"])
    backs.setdefault(norm(c["back"]), []).append(c["id"])
print("exact front dups:", [v for v in fronts.values() if len(v)>1])
print("exact back dups:", [v for v in backs.values() if len(v)>1])
pairs = []
for i, a in enumerate(cards):
    for b in cards[i+1:]:
        if a["id"] not in slice_ids and b["id"] not in slice_ids: continue
        r = difflib.SequenceMatcher(None, norm(a["front"]+" "+a["back"]), norm(b["front"]+" "+b["back"])).ratio()
        if r > 0.45: pairs.append((round(r,3), a["id"], b["id"]))
for p in sorted(pairs, reverse=True): print("near", p)
print("ids in slice:", slice_ids)
gaps = sorted(int(x[5:]) for x in ids if x.startswith("E3-c"))
print("E3-c177 lesson:", ids.get("E3-c177",{}).get("lesson"), "E3-c176 present:", "E3-c176" in ids)
