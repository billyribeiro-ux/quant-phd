"""Round 7 (CS2 slice b): every number on a slice card (front or back) must appear in its lesson page text."""
import html
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/CS/CS2/cards.json", encoding="utf-8"))
texts = {}
for n in ("L05", "L06", "L07", "L08"):
    raw = open(f"{root}/course/modules/CS/CS2/{n}.html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    txt = re.sub(r"\s+", " ", txt).replace(",", "").replace(" ", "").replace(" ", "")
    texts[n] = txt
num = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
misses = []
total = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    for field in ("front", "back"):
        for tok in set(num.findall(c[field])):
            total += 1
            t = tok
            if t not in texts[c["lesson"]].replace(",", ""):
                misses.append((c["id"], field, tok))
print(f"numeric tokens checked on slice cards: {total}")
print(f"tokens not found verbatim in lesson text: {len(misses)}")
for m in misses:
    print(m)
