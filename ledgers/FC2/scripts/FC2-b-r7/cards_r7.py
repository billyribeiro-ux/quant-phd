import json, re, sys, collections, html
root = sys.argv[1]
base = root + "/course/modules/FC/FC2/"
cards = json.load(open(base + "cards.json", encoding="utf-8"))
print("count", len(cards))
ids = [c["id"] for c in cards]
print("dup ids", [k for k, v in collections.Counter(ids).items() if v > 1])
nums = sorted(int(i.split("c")[-1]) for i in ids)
print("missing numbers in c001..c%d:" % max(nums), [n for n in range(1, max(nums) + 1) if n not in nums])
fr = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1])
# statement refs: each "Proposition/Theorem/Remark/Definition/Lemma/Corollary/Example X.Y" in an L04-L06 card must exist in that lesson page
pages = {}
for L in ("L04", "L05", "L06"):
    t = open(base + L + ".html", encoding="utf-8").read()
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    pages[L] = re.sub(r"\s+", " ", t)
    pages[L + "_raw"] = open(base + L + ".html", encoding="utf-8").read()
for c in cards:
    if c["lesson"] not in ("L04", "L05", "L06"):
        continue
    txt = c["front"] + " " + c["back"]
    refs = re.findall(r"(Proposition|Theorem|Remark|Definition|Lemma|Corollary|Example|Problem)\s+(\d+\.\d+)(\([a-z]\))?", txt)
    for kind, num, part in refs:
        pat = kind + " " + num
        present = [L for L in ("L04", "L05", "L06") if (pat + " ") in pages[L + "_raw"] or (pat + "<") in pages[L + "_raw"]]
        print(c["id"], c["lesson"], "ref", kind, num, part, "on page:", present)
    for a in sorted(set(re.findall(r"\bA\d\b|\(N\)|A\d′|A\d'", txt))):
        print(c["id"], c["lesson"], "assumption", a)
    print("CARD", c["id"], c["lesson"], c.get("grade"), c.get("basis", ""), "|", c["front"], "|", c["back"])
