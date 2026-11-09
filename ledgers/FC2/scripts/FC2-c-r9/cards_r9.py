import json, re, sys, itertools
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/FC/FC2/cards.json", encoding="utf-8"))
print("cards:", len(cards), "ids unique:", len({c["id"] for c in cards}) == len(cards))
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())
fr = [norm(c["front"]) for c in cards]; bk = [norm(c["back"]) for c in cards]
print("dup fronts:", len(fr) - len(set(fr)), "dup backs:", len(bk) - len(set(bk)))
def toks(s):
    return set(re.findall(r"[a-z]{4,}", s.lower()))
# near-duplicate check: Jaccard on front+back tokens
cand = []
for a, b in itertools.combinations(cards, 2):
    ta, tb = toks(a["front"] + " " + a["back"]), toks(b["front"] + " " + b["back"])
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.45:
        cand.append((round(j, 3), a["id"], b["id"]))
print("pairs with token Jaccard >= 0.45:", sorted(cand, reverse=True)[:15])
# numeric tokens (length >= 2) in each L07/L08 card vs lesson text
lessons = {L: open(f"{root}/course/modules/FC/FC2/{L}.html", encoding="utf-8").read() for L in ("L07", "L08")}
for c in cards:
    if c["lesson"] not in lessons:
        continue
    text = " ".join([c["front"], c["back"], c.get("basis", "")])
    nums = re.findall(r"\d+(?:\.\d+)?", text)
    miss = [n for n in nums if len(n) >= 2 and n not in lessons[c["lesson"]]]
    if c["id"] in ("FC2-c199", "FC2-c200", "FC2-c207") or miss:
        print(c["id"], c["lesson"], "numeric tokens:", nums, "missing from lesson:", miss)
# the new cards' phrases vs lesson text
checks = {
 "FC2-c199": ["standard deviation of its log return per square root of a year", "volatility \\(\\sigma\\)"],
 "FC2-c200": ["The lower bound of Lesson 5 for a European call, with the same inputs, is", "\\max\\big(S - Ke^{-r\\tau},\\ 0\\big)"],
 "FC2-c207": ["Under A1, A2, A3, A4, A5 and A7, with \\(r > 0\\) and \\(h < \\sigma^2/r^2\\)", "\\(q^{(n)}\\)", "Theorem 3.3 of Lesson 6"],
}
for cid, phrases in checks.items():
    lesson = next(c["lesson"] for c in cards if c["id"] == cid)
    for p in phrases:
        print(cid, "lesson", lesson, "phrase found:", p in lessons[lesson], "|", p)
