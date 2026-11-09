import json, re, sys, pathlib
cards = json.load(open(sys.argv[1]))
txt = {}
for i in range(1, 25):
    txt[f"L{i:02d}"] = pathlib.Path(f"/tmp/m2e_r1_text/L{i:02d}.txt").read_text(encoding="utf-8")
pat = re.compile(r"\b(Theorem|Proposition|Example|Remark|Lemma|Corollary|Definition|Assumption|Problem|Misconception|Section)\s+(\d+(?:\.\d+)?|[A-Z]\d+|\d+\.\d+)")
problems = []
for c in cards:
    L = c["lesson"]
    body = c["front"] + " " + c["back"]
    for kind, num in pat.findall(body):
        label = f"{kind} {num}"
        # Problem labels like 'M3' or 'R3' appear as 'M3 ·' in lesson text
        if kind == "Problem":
            ok = bool(re.search(r"\b" + re.escape(num) + r"\b", txt[L]))
        elif kind == "Section":
            ok = bool(re.search(r"(^|\n)\s*" + num.split('.')[0] + r"[A-Z]", txt[L], re.M)) or (f"§{num}" in txt[L]) or (f"Section {num}" in txt[L])
        else:
            ok = label in txt[L]
        if not ok:
            problems.append((c["id"], L, label))
    # cross-lesson refs: 'Lesson N' / 'Theorem x of Lesson N' / 'of Lesson L..'
for p in problems:
    print("LOCATOR-NOT-FOUND", *p)
print("cards scanned", len(cards), "locator misses", len(problems))
