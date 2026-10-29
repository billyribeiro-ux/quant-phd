import json, re, sys
base = "/Users/billyribeiro/.fanout/wt/verifyB17-M3-d/course/modules/M/M3/"
cards = json.load(open(base + "cards.json", encoding="utf-8"))
lessons = {}
for L in ["L01","L02","L03","L04","L05","L06","L07","L08","L09"]:
    lessons[L] = open(f"/tmp/m3d17txt/{L}.txt", encoding="utf-8").read() if L not in ("L01","L06") else ""
ref = re.compile(r"(Definition|Theorem|Lemma|Proposition|Corollary|Remark|Problem|Example|Section|Assumption|Fact|Lab|Method|Misconception)\s+(\d+(\.\d+[a-z]?)?|\d+\.\d+\([a-z]\)|[A-Z]\d+)")
ids = [c["id"] for c in cards]
dup = sorted({i for i in ids if ids.count(i) > 1})
print("cards", len(cards), "dup ids", dup)
fronts = {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("dup fronts", [v for v in fronts.values() if len(v) > 1])
for c in cards:
    text = c["front"] + " || " + c["back"]
    if c.get("basis"): text += " || " + c["basis"]
    refs = set(m.group(0) for m in ref.finditer(text))
    lt = lessons.get(c["lesson"], "")
    missing = []
    for r in sorted(refs):
        core = r.split()
        pat = re.escape(r)
        # strip trailing ')' for lookup of "(a)"
        if not re.search(pat, lt):
            missing.append(r)
    if missing:
        print(c["id"], c["lesson"], "MISSING refs in lesson:", missing)
print("done")
