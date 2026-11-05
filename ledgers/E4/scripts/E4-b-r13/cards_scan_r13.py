"""Round-13: every number in a slice card's front/back must appear in its own lesson text; duplicate scan over all cards."""
import html
import json
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
cards = json.load(open(f"{ROOT}/course/modules/E/E4/cards.json", encoding="utf-8"))
texts = {}
for L in ("L04", "L05", "L06"):
    raw = open(f"{ROOT}/course/modules/E/E4/{L}.html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    texts[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
num = re.compile(r"(?<![A-Za-z_])(\d+/\d+|\d+\.\d+|\d+)(?![A-Za-z_])")
misses = 0
n = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    n += 1
    body = texts[c["lesson"]].replace(" ", "")
    for field in ("front", "back"):
        for tok in num.findall(c[field]):
            if tok.replace(" ", "") not in body:
                # tolerate fractions rendered as \tfrac / \frac, i.e. compare numerator and denominator separately
                if "/" in tok:
                    a, b = tok.split("/")
                    if a in body and b in body:
                        continue
                misses += 1
                print(f"NUMBER NOT IN LESSON {c['id']} {field} '{tok}'")
print(f"slice cards {n} misses {misses}")
ids = [c["id"] for c in cards]
fronts = [c["front"].strip().lower() for c in cards]
backs = [c["back"].strip().lower() for c in cards]
print(f"cards {len(cards)} unique ids {len(set(ids)) == len(ids)} duplicate fronts {len(fronts) - len(set(fronts))} duplicate backs {len(backs) - len(set(backs))}")
