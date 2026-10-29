import json, re
cards = json.load(open("/tmp/verifyB2-E1-d/course/modules/E/E1/cards.json", encoding="utf-8"))
texts = {L: open(f"/tmp/E1d-r2/{L}.txt", encoding="utf-8").read() for L in [f"L0{i}" for i in range(1, 10)]}
pat = re.compile(r"\b(Definition|Proposition|Remark|Example|Misconception|Problem|Lemma|Theorem|Corollary|Assumption|Section|Setting|Exercise|Problem)\s(\d+(?:\.\d+)?|[A-Z]\d+|M\d+|R\d+|E\d+|P\d+|M\d+)\b")
missing = []
for c in cards:
    refs = set()
    for m in pat.finditer(c["back"] + " " + c["front"]):
        refs.add(m.group(1) + " " + m.group(2))
    t = texts[c["lesson"]]
    for r in sorted(refs):
        if r == "Setting" or r.startswith("Section") :
            continue
        if not re.search(re.escape(r) + r"(?![\d.])", t):
            # also check other lessons (cross-lesson refs)
            where = [L for L, tt in texts.items() if re.search(re.escape(r) + r"(?![\d.])", tt)]
            missing.append((c["id"], c["lesson"], r, where))
for m in missing: print(m)
print("total", len(missing))
