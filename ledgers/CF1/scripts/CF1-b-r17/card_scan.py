import json, collections, re, sys
root = sys.argv[1]
cards = json.load(open(root + "/course/modules/CF/CF1/cards.json", encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
print("cards", len(cards), "dup ids", [k for k, v in ids.items() if v > 1])
fr = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1])
# near-duplicate fronts within the CF1 deck for L03/L04 cards
mine = [c for c in cards if c["lesson"] in ("L03", "L04")]
print("L03/L04 cards", len(mine), sorted(c["id"] for c in mine)[:3], "...")
# every L03/L04 card's basis names a Theorem/Definition/Example/Remark/Proposition/Problem/Lab that appears in its lesson
for c in mine:
    html = open(root + "/course/modules/CF/CF1/%s.html" % c["lesson"], encoding="utf-8").read()
    for label in re.findall(r"(Theorem \d\.\d|Definition \d\.\d|Example \d\.\d|Remark \d\.\d|Proposition \d\.\d|Corollary \d\.\d|Problem R\d|Lab 1|Definition 3\.1|Remark 5\.1|Remark 4\.3|Problem M\d)", c["basis"] + " " + c["back"]):
        if label not in html and label.replace("Problem ", "") not in html:
            print("  MISSING in lesson", c["id"], label)
print("basis-label scan done")
