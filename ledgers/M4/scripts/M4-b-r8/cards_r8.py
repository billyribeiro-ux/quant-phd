import html, json, re, pathlib
root = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB8-M4-b")
cards = [c for c in json.load(open(root / "course/modules/M/M4/cards.json")) if c["lesson"] in ("L05", "L06", "L07")]
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}), "unique fronts", len({c["front"] for c in cards}))
allc = json.load(open(root / "course/modules/M/M4/cards.json"))
print("all ids unique", len({c["id"] for c in allc}) == len(allc), "all fronts unique", len({c["front"] for c in allc}) == len(allc))
txt = {}
for L in ["L05", "L06", "L07"]:
    h = (root / f"course/modules/M/M4/{L}.html").read_text()
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    txt[L] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))
for c in cards:
    back = c["back"]
    labels = re.findall(r"(Definition|Proposition|Remark|Example|Problem|Assumption|Lemma|Section|Lab) ([0-9]+(?:\.[0-9]+)?|[A-Z][0-9]?)", back)
    miss_l = []
    for kind, num in labels:
        if kind == "Section":
            continue
        pat = f"{kind} {num}"
        if not any(pat in t for t in txt.values()):
            miss_l.append(pat)
    nums = set(re.findall(r"\d+\.\d+|\d+/\d+|\d+", back))
    miss_n = [n for n in nums if not any(n in t for t in txt.values())]
    print(c["id"], c["lesson"], c["grade"], "label-miss" if miss_l else "", miss_l, "num-miss" if miss_n else "", miss_n)
