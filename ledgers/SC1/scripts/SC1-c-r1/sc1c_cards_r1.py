import json, re, html, sys, collections
CARDS = sys.argv[1]
ROOT = sys.argv[2]
cards = json.load(open(CARDS, encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"] for c in cards)
backs = collections.Counter(c["back"] for c in cards)
print("cards", len(cards), "dup_ids", [k for k, v in ids.items() if v > 1], "dup_fronts", sum(1 for v in fronts.values() if v > 1), "dup_backs", sum(1 for v in backs.values() if v > 1))
def lesson_text(l):
    t = open(f"{ROOT}/course/modules/SC/SC1/{l}.html", encoding="utf-8").read()
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)
texts = {l: lesson_text(l) for l in ("L07", "L08")}
miss = []
n = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    n += 1
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?", c[field]):
            if tok in ("1", "0", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"):
                continue
            if tok not in texts[c["lesson"]]:
                miss.append((c["id"], field, tok))
print("L07/L08 cards checked", n, "numeric tokens not in lesson (len>1 or decimals):", miss)
a5 = [c["id"] for c in cards if "A5" in c["front"] + c["back"] + c.get("basis", "")]
print("cards mentioning A5 (front/back/basis):", a5)
for cid in ("SC1-c157", "SC1-c159", "SC1-c171", "SC1-c174", "SC1-c201", "SC1-c241", "SC1-c242"):
    c = next(x for x in cards if x["id"] == cid)
    print(cid, c["lesson"], c["grade"], "numbers:", re.findall(r"\d+(?:\.\d+)?", c["back"]))
