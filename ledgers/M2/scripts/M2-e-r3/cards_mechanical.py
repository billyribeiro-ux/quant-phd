"""Mechanical card checks for M2 cards.json against the lesson HTML (round 2).

Checks: unique ids and fronts; ids sequential-format; lesson exists; every number written in a card (front or back)
appears in its lesson's text; grade/basis/cite rules of BUILDER_RULES 7 and check_pages.
Usage: python3 -I cards_mechanical.py <checkout>
"""
import collections
import html
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
base = root / "course/modules/M/M2"
cards = json.loads((base / "cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
fronts = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
print("id format ok:", all(re.fullmatch(r"M2-c\d{3}", c["id"]) for c in cards))
print("grade counts:", collections.Counter(c.get("grade") for c in cards))
print("cards with basis but grade not C:", [c["id"] for c in cards if c.get("basis") and c.get("grade") != "C"])
print("grade C without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("cite fields:", sum(1 for c in cards if "cite" in c))
print("lessons:", sorted(collections.Counter(c["lesson"] for c in cards).items()))
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
text_cache = {}
def lesson_text(l):
    if l not in text_cache:
        raw = (base / f"{l}.html").read_text(encoding="utf-8")
        raw = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', " ", raw, flags=re.S)
        raw = re.sub(r"<script.*?</script>|<svg.*?</svg>", " ", raw, flags=re.S)
        text_cache[l] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return text_cache[l]
missing = []
for c in cards:
    t = lesson_text(c["lesson"])
    for field in ("front", "back"):
        for n in NUM.findall(c[field]):
            if n not in t:
                missing.append((c["id"], field, n))
print("card numbers not found verbatim in their lesson text (count):", len(missing))
for m in missing:
    print("   ", m)
