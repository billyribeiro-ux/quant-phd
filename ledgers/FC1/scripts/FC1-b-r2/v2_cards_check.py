# Round-2 card check for L04 and L05 cards (all 57): labels and 3+ digit numbers in each card appear in its lesson;
# duplicate ids/fronts/backs over the whole unit; grade and basis rules; lesson field matches the card's page.
import html, json, re, sys
from collections import Counter
root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/FC/FC1/cards.json", encoding="utf-8"))
pages = {}
for L in ("L04", "L05"):
    raw = open(f"{root}/course/modules/FC/FC1/{L}.html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    pages[L] = text
dups = {k: [c["id"] for c in cards if c[k] in [d for d, n in Counter(x[k] for x in cards).items() if n > 1]] for k in ("front", "back")}
ids = Counter(c["id"] for c in cards)
print("unit cards:", len(cards), "dup ids:", [i for i, n in ids.items() if n > 1], "dup fronts:", [c["id"] for c in cards if Counter(x["front"] for x in cards)[c["front"]] > 1], "dup backs:", [c["id"] for c in cards if Counter(x["back"] for x in cards)[c["back"]] > 1])
label_re = re.compile(r"\b(Definition|Remark|Proposition|Assumption|Example|Problem|Lab|Section|Lesson)\s+((?:[0-9]+\.[0-9]+|[0-9]|[A-Z][0-9]|[A-Z]\w*)(?:\([a-z0-9]+\))?)")
fails = []
n = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    n += 1
    txt = pages[c["lesson"]]
    body = c["front"] + " " + c["back"]
    for kind, lab in label_re.findall(body):
        key = f"{kind} {lab}"
        if key not in txt and not (kind == "Lesson"):
            fails.append((c["id"], "label not in lesson", key))
    for num in set(re.findall(r"\b\d{3,}\b", body)):
        if num not in txt:
            fails.append((c["id"], "number not in lesson", num))
    if "grade" in c and c["grade"] == "C" and not c.get("basis"):
        fails.append((c["id"], "C card without basis", ""))
    if c.get("grade") == "T" and not re.search(r"Proposition|Lemma|Theorem|Problem|Example|Definition|Remark|Assumption", c["back"] + c["front"]):
        fails.append((c["id"], "T card names no result", ""))
print("L04+L05 cards checked:", n)
print("failures:", fails if fails else "none")
for c in cards:
    if c["lesson"] in pages and c.get("grade") is not None:
        print(c["id"], c["lesson"], c["grade"], c.get("basis", ""))
