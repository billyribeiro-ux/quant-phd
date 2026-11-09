import json, re, html
# every decimal/integer/fraction in a card back (ignoring labels like E3-c001 and the 'Definition 1.1' style numbers)
# must appear in the lesson page (HTML-unescaped text) or in the lab twin of that lesson
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
pages = {}
twin = {}
for L in ("L01", "L02", "L03", "L04"):
    pages[L] = html.unescape(open(f"course/modules/E/E3/{L}.html", encoding="utf-8").read())
    twin[L] = open(f"tests/labs/E3/lab-E3-{L}-1.py", encoding="utf-8").read()
bad = []
for c in cards:
    if c["lesson"] not in pages:
        continue
    text = c["front"] + " " + c["back"]
    text = re.sub(r"\b(Definition|Proposition|Theorem|Lemma|Example|Remark|Corollary|Problem|section|Section|Lesson|Part|Assumption|A|F|Module M1|Lesson|Lab)\s+[0-9.()a-z]+", " ", text)
    text = re.sub(r"E3-c\d+", " ", text)
    nums = re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:/\d+)?", text)
    src = pages[c["lesson"]] + twin[c["lesson"]]
    miss = [n for n in nums if n not in src and n.split("/")[0] not in src]
    if miss:
        bad.append((c["id"], c["lesson"], miss))
print("cards with numbers not found in lesson or twin:", bad)
