# Card checks for L04/L05: every cited label and every multi-digit number must appear in its lesson page;
# full-file duplicate scan (ids, normalised fronts, normalised backs).
import json, re, html, sys, collections
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/FC/FC1/cards.json", encoding="utf-8"))
pages = {}
for L in ("L04", "L05"):
    raw = open(f"{root}/course/modules/FC/FC1/{L}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    txt = re.sub(r"\s+", " ", txt)
    pages[L] = txt
pat = re.compile(r"(Definition \d+\.\d+|Proposition \d+\.\d+(?:\([ivx]+\))?|Example \d+\.\d+|Remark \d+\.\d+|Problem [A-Z]\d|Assumption A\d|Section \d|misconception \d|Lab 1|Fixture [AB]|Proposition 2\.1\(ii\)|Corollary \d+\.\d+)")
problems = []
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = c["front"] + " " + c["back"]
    page = pages[c["lesson"]]
    for m in set(pat.findall(text)):
        needle = m.replace("misconception", "Misconception") if m.startswith("misconception") else m
        if needle not in page and m not in page:
            problems.append((c["id"], "label not in lesson", m))
    for n in set(re.findall(r"\d{3,}", text)):
        if n not in page:
            problems.append((c["id"], "number not in lesson", n))
    print(c["id"], c["lesson"], "grade=%s" % c.get("grade"), "basis=%s" % ("basis" in c), "labels=%s" % sorted(set(pat.findall(text)))[:4])
print("PROBLEMS:", problems)
ids = collections.Counter(c["id"] for c in cards)
print("dup ids:", [k for k, v in ids.items() if v > 1])
fr = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("dup fronts:", [k for k, v in fr.items() if v > 1])
bk = collections.Counter(re.sub(r"\W+", " ", c["back"].lower()).strip() for c in cards)
print("dup backs:", [k for k, v in bk.items() if v > 1])
print("total cards", len(cards))
