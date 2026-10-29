import re, sys, pathlib, html
root = pathlib.Path(sys.argv[1]) / "course/modules/M/M2"
def labels(t):
    labs = set()
    for m in re.finditer(r'<span class="block-title[^"]*">\s*((?:Theorem|Proposition|Corollary|Example|Definition|Remark|Assumption)\s+[0-9.]+)', t):
        labs.add(m.group(1).split()[0] + " " + m.group(1).split()[1])
    for m in re.finditer(r'<span class="problem-title">\s*([A-Z]\d+)\s*·', t):
        labs.add(m.group(1))
    for m in re.finditer(r'<span class="block-title">\s*((?:Theorem|Proposition|Corollary|Example|Definition|Remark)\s+[0-9.]+)', t):
        labs.add(m.group(1).split()[0] + " " + m.group(1).split()[1])
    for m in re.finditer(r'<span class="block-title claim" data-grade="T">\s*((?:Theorem|Proposition|Corollary|Example|Definition|Remark)\s+[0-9.]+)', t):
        labs.add(m.group(1).split()[0] + " " + m.group(1).split()[1])
    labs.add("Assumption 1") if "<strong>Assumption 1.</strong>" in t else None
    return labs
pages = {n: (root / f"L{n:02d}.html").read_text(encoding="utf-8") for n in range(1, 25)}
L = {n: labels(pages[n]) for n in pages}
pat = re.compile(r'(Theorem|Proposition|Corollary|Example|Definition|Remark|Problem|Assumption|Section|Misconception)s?\s+((?:[A-Z]?\d+(?:\.\d+)?))(?:\s+(?:of|in)\s+(?:Lesson|Lesson L|L)\s*L?(\d+))?', re.I)
out = []
for n in range(13, 19):
    t = html.unescape(re.sub(r"<[^>]+>", " ", pages[n]))
    t = re.sub(r"\s+", " ", t)
    for m in pat.finditer(t):
        kind, num, target = m.group(1), m.group(2), m.group(3)
        tgt = int(target) if target else n
        # map to label
        if kind.lower() == "problem":
            key = num if re.match(r"[A-Z]\d+$", num) else None
            if key is None: continue
            ok = key in L[tgt]
            label = key
        elif kind.lower() == "section" or kind.lower() == "misconception":
            continue
        elif kind.lower() == "assumption":
            ok = "Assumption 1" in L[tgt] and num == "1"
            label = f"Assumption {num}"
        else:
            if not re.match(r"\d+(\.\d+)?$", num): continue
            label = f"{kind.capitalize()} {num}"
            ok = label in L[tgt]
        out.append((f"L{n}", m.group(0), f"-> L{tgt}", "OK" if ok else "MISSING"))
seen = set()
for o in out:
    k = (o[0], o[1], o[2], o[3])
    if k in seen: continue
    seen.add(k)
    if o[3] != "OK" or True:
        print(*o)
