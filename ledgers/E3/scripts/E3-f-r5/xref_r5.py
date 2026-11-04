import json, re, html, sys
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/E/E3/cards.json"))
pages = {}
for L in ("L01", "L02", "L03", "L04"):
    t = html.unescape(re.sub(r"<[^>]+>", " ", open(f"{root}/course/modules/E/E3/{L}.html", encoding="utf-8").read()))
    pages[L] = re.sub(r"\s+", " ", t)
pat = re.compile(r"(?:(L0\d|M1|Module M1)\s+)?(Proposition|Lemma|Theorem|Remark|Example|Problem|Definition|Assumption|Section|section)\s+([A-Z]?\d+(?:\.\d+)?)(\([a-z]\))?")
bad = []
for c in cards:
    if c["lesson"] not in pages:
        continue
    for m in pat.finditer(c["back"] + " " + c["front"]):
        prefix, kind, num, sub = m.groups()
        if prefix and prefix.startswith("M"):
            continue  # Module M1 references are outside the slice
        target = prefix if prefix in pages else c["lesson"]
        if kind == "Section":
            ok = True
        else:
            label = f"{kind} {num}"
            ok = label in pages[target]
        if kind == "Assumption" and not ok:
            ok = f"Assumption A{num}" in pages[target] or f"A{num}" in pages[target]
        if not ok:
            bad.append((c["id"], c["lesson"], m.group(0), target))
    for m in re.finditer(r"\b([FA]\d)\b", c["back"] + " " + c["front"]):
        pass
print("unresolved labelled references in slice cards:", bad)
