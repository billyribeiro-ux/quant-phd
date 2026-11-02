import json, re, sys, pathlib, html
root = pathlib.Path(sys.argv[1])
cards = json.load(open(root / "course/modules/M/M3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "unique fronts", len({c["front"] for c in cards}))
lessons = {}
for L in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"]:
    p = root / f"course/modules/M/M3/{L}.html"
    if p.exists():
        lessons[L] = html.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8")))
changed = "c025 c031 c034 c050 c063 c064 c065 c067 c082 c119 c123 c130 c133 c134 c136 c175 c182 c187 c188 c189 c190 c192 c193 c194 c195 c196 c197 c198 c199 c200 c201 c202".split()
pat = re.compile(r"\((Definition|Theorem|Proposition|Corollary|Lemma|Remark|Section|Problem|Example) ([0-9]+(?:\.[0-9]+)?(?:\([a-c]\))?)\)")
for c in cards:
    num = c["id"].split("-")[1]
    if num not in changed:
        continue
    L = c["lesson"]
    text = lessons.get(L, "")
    txt = c["front"] + " " + c["back"]
    refs = pat.findall(txt)
    miss = []
    for kind, n in refs:
        base = n.split("(")[0]
        if not re.search(kind + r"\s+" + re.escape(base) + r"\b", text):
            miss.append(f"{kind} {n}")
    nums = sorted(set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", txt)))
    tmiss = [x for x in nums if x not in text]
    print(c["id"], L, c.get("grade", "-"), "refs", [f"{k} {n}" for k, n in refs], "MISSING_REF" if miss else "", miss, "NUMS_NOT_IN_LESSON" if tmiss else "", tmiss)
