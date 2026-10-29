import json, re, html, sys
base = sys.argv[1]
cards = json.load(open(f"{base}/course/modules/E/E5/cards.json", encoding="utf-8"))
lessons = {}
for L in sorted({c["lesson"] for c in cards}):
    src = open(f"{base}/course/modules/E/E5/{L}.html", encoding="utf-8").read()
    txt = html.unescape(re.sub(r"</?[a-zA-Z][^>]*>", " ", src))
    lessons[L] = txt
num = re.compile(r"(?<![A-Za-z_\w.])\d+(?:[.,]\d+)*(?![\w])")
miss = 0
for c in cards:
    text = c["front"] + " " + c["back"]
    toks = set(num.findall(text))
    lt = lessons[c["lesson"]]
    absent = [t for t in toks if not re.search(r"(?<![\w.])" + re.escape(t) + r"(?![\w])", lt)]
    if absent:
        miss += 1
        print(c["id"], c["lesson"], "numbers not as standalone tokens in lesson:", sorted(absent))
print("cards with absent numbers:", miss, "of", len(cards))
