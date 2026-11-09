"""Round 3 card cross-check: every card of lessons L04-L06 (and any card naming them) vs its lesson page text."""
import html
import json
import re
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyS3-E1-b/course/modules/E/E1/"
cards = json.load(open(ROOT + "cards.json"))
pages = {}
for L in ("L04", "L05", "L06"):
    raw = open(ROOT + L + ".html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    pages[L] = re.sub(r"\s+", " ", html.unescape(raw))
label_re = re.compile(r"\b(Definition|Proposition|Lemma|Theorem|Corollary|Remark|Example|Assumption|Problem|Lab) (\d+(?:\.\d+)?|[A-Z]\d*|M\d*)\b")
misses = []
checked = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    checked += 1
    text = " ".join([c["front"], c["back"], c.get("basis") or ""])
    page = pages[c["lesson"]]
    for m in label_re.finditer(text):
        lab = m.group(0)
        short = m.group(1) + " " + m.group(2)
        # labels as printed on the page: 'Remark 1.2 <span class="name">' -> text 'Remark 1.2 (the'
        if short not in page and lab not in page:
            misses.append((c["id"], "label", lab))
    for n in re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])", text):
        if n not in page:
            misses.append((c["id"], "number", n))
    if c.get("grade") == "C" and "Lab" not in (c.get("basis") or ""):
        misses.append((c["id"], "C-without-lab-basis", c.get("basis")))
print("cards checked (L04-L06):", checked)
print("misses:", len(misses))
for x in misses:
    print(x)
ids = [c["id"] for c in cards]
print("total cards", len(cards), "duplicate ids", len(ids) - len(set(ids)))
norm = {}
for c in cards:
    k = re.sub(r"[^a-z0-9 ]", "", c["front"].lower())
    norm.setdefault(k, []).append(c["id"])
print("duplicate normalised fronts:", [v for v in norm.values() if len(v) > 1])
sys.exit(0)
