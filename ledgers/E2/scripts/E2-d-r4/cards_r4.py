"""Card checks for E2 slice d, round 4: duplicates, card numbers present in the card's own lesson, and grade/basis."""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
MOD = ROOT / "course" / "modules" / "E" / "E2"
cards = json.loads((MOD / "cards.json").read_text())
print("cards:", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"] for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = Counter(c["back"] for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
lesson_text = {}
for c in cards:
    L = c["lesson"]
    if L not in lesson_text:
        html = (MOD / f"{L}.html").read_text()
        html = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
        html = re.sub(r"<[^>]+>", " ", html)
        html = html.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        lesson_text[L] = re.sub(r"\s+", " ", html)
bad = []
for c in cards:
    nums = set(re.findall(r"\d[\d,]*(?:\.\d+)?", c["back"]))
    for num in sorted(nums):
        n = num.rstrip(",")
        if n not in lesson_text[c["lesson"]]:
            bad.append((c["id"], c["lesson"], n))
print("card numbers absent from own lesson (id, lesson, number):")
for b in bad:
    print("  ", b)
print("grade counts:", Counter(c.get("grade") for c in cards))
print("C without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("basis without C:", [(c["id"], c.get("grade")) for c in cards if c.get("basis") and c.get("grade") != "C"])
