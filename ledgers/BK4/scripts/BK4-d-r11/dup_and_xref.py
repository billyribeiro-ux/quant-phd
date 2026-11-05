"""Duplicate scan and cross-reference checks for BK4 cards.json (round 11, verifier d)."""
import json, difflib, re, sys
cards = json.load(open("course/modules/BK/BK4/cards.json"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
print("id pattern ok", all(re.fullmatch(r"BK4-c\d{3}", i) for i in ids))
print("missing numbers in 1..105:", sorted(set(range(1,106)) - {int(i[-3:]) for i in ids}))
print("keys", sorted({tuple(sorted(c.keys())) for c in cards}))
print("grades", {g: sum(1 for c in cards if c.get("grade")==g) for g in ("T","C",None)})
# T or C cards must have basis; None must have no grade
for c in cards:
    if c.get("grade") in ("T","C") and not c.get("basis"):
        print("MISSING BASIS", c["id"])
    if c.get("grade") is None and "basis" in c:
        print("BASIS WITHOUT GRADE", c["id"], c["basis"])
    if c.get("grade") is None:
        pass
# near-duplicate scan on fronts and on backs
pairs=[]
for i in range(len(cards)):
    for j in range(i+1,len(cards)):
        a,b=cards[i],cards[j]
        rf=difflib.SequenceMatcher(None,a["front"],b["front"]).ratio()
        rb=difflib.SequenceMatcher(None,a["back"],b["back"]).ratio()
        if rf>0.6 or rb>0.6:
            pairs.append((round(rf,2),round(rb,2),a["id"],b["id"]))
for p in sorted(pairs, reverse=True):
    print("NEAR", p)
print("near pairs:", len(pairs))
# lesson labels referenced in basis and fronts
lessons = {}
for L in ("L01","L02","L03","L04","L05"):
    txt = open(f"course/modules/BK/BK4/{L}.html", encoding="utf-8").read()
    lessons[L]=txt
for c in cards:
    b = (c.get("basis") or "") + " " + c["front"] + " " + c["back"]
    for m in re.finditer(r"(Proposition|Remark|Example|Problem|Definition|Corollary|Assumption|Lab 1|Section|Claim)\s+([0-9A-Z][0-9.()a-z]*)", b):
        label = m.group(0)
        if label.startswith("Lab 1"): continue
        base = re.sub(r"\(.*", "", m.group(0)).strip()
        if base.startswith("Section") or base.startswith("Claim"): continue
        found_any = any(base in t for t in lessons.values())
        if not found_any:
            print("UNRESOLVED LABEL", c["id"], repr(label))
print("label check done")
