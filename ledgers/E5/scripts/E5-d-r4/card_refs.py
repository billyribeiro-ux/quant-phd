import json, re, html, sys
base = sys.argv[1]
cards = json.load(open(f"{base}/course/modules/E/E5/cards.json", encoding="utf-8"))
lessons = {}
for L in sorted({c["lesson"] for c in cards}):
    src = open(f"{base}/course/modules/E/E5/{L}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", " ", src))
    lessons[L] = re.sub(r"\s+", " ", txt)
kinds = r"(Proposition|Remark|Definition|Theorem|Corollary|Assumption|Fact|Derivation|Problem|Example|Lemma|Lab 1, Part|Part|Lesson|Assumption A|Remark)"
pat = re.compile(r"\b(Proposition|Remark|Definition|Theorem|Corollary|Assumption|Fact|Derivation|Problem|Example)\s+(\d+\.\d+|[A-Z]\d+)")
missing = []
for c in cards:
    text = " ".join([c["front"], c["back"], c.get("basis") or ""])
    lt = lessons[c["lesson"]]
    for m in pat.finditer(text):
        label = f"{m.group(1)} {m.group(2)}"
        if label not in lt:
            # also check other lessons (cross-lesson references are allowed when named)
            where = [L for L in lessons if label in lessons[L]]
            missing.append((c["id"], c["lesson"], label, where))
for x in missing:
    print("NOT IN OWN LESSON:", x)
print("checked refs; misses:", len(missing))
