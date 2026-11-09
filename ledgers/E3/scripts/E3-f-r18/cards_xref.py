import json, re, sys, html
# For each card: every "Definition/Proposition/Theorem/Lemma/Example/Remark X.Y" and "Problem P/R/M/E n" cited
# must appear as a labelled block (block-title or problem-title) in the card's own lesson page.
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
only = set(sys.argv[1:])
pages = {}
for c in cards:
    L = c["lesson"]
    if only and c["id"] not in only:
        continue
    if L not in pages:
        pages[L] = html.unescape(open(f"course/modules/E/E3/{L}.html", encoding="utf-8").read())
    src = pages[L]
    text = c["front"] + " " + c["back"]
    refs = re.findall(r"\b(Definition|Proposition|Theorem|Lemma|Example|Remark|Corollary) (\d+\.\d+)", text)
    probs = re.findall(r"\b(Problem )?([PRME]\d)\b", text)
    missing = []
    for kind, num in refs:
        if not re.search(rf"{kind} {re.escape(num)}\b", src):
            missing.append(f"{kind} {num}")
    for _, p in probs:
        if not re.search(rf'id="{p}"|>{p} ·', src) and not re.search(rf"\b{p}\b ·", src):
            missing.append(p)
    print(c["id"], L, "refs:", [f"{k} {n}" for k, n in refs], "problems:", [p for _, p in probs], "MISSING:" if missing else "ok", missing if missing else "")
