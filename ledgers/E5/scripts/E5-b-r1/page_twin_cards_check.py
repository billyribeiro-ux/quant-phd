"""Checks for E5 L04-L06: (1) page lab code equals its twin modulo the final newline; (2) every card of L04-L06 has
its cited theorem/definition/remark/assumption label in its own lesson; (3) duplicate fronts or ids across the unit;
(4) scope-word and banned-phrase scan of the three lessons. Usage: python3 -I <this file> <checkout-root>
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
bad = 0
for n in ("04", "05", "06"):
    src = (root / f"course/modules/E/E5/L{n}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S).group(1))
    twin = (root / f"tests/labs/E5/lab-E5-L{n}-1.py").read_text(encoding="utf-8")
    same = code == twin.rstrip("\n")
    bad += not same
    print(f"TWIN L{n} page_code==twin(modulo final newline): {same}")

cards = json.loads((root / "course/modules/E/E5/cards.json").read_text(encoding="utf-8"))
pages = {}
for n in ("L04", "L05", "L06"):
    s = (root / f"course/modules/E/E5/{n.replace('L', 'L')}.html").read_text(encoding="utf-8")
    pages[n] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))
pat = re.compile(r"(Definition|Proposition|Remark|Derivation|Corollary|Assumption) (\d+\.\d+|A\d)")
missing = []
for c in cards:
    if c["lesson"] not in pages:
        continue
    for m in pat.finditer(c["front"] + " " + c["back"] + " " + c.get("basis", "")):
        if f"{m.group(1)} {m.group(2)}" not in pages[c["lesson"]]:
            missing.append((c["id"], m.group(0)))
print(f"CARD refs missing from own lesson (L04-L06): {missing}")
bad += bool(missing)
fronts = Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
ids = Counter(c["id"] for c in cards)
print(f"CARDS total={len(cards)} duplicate_fronts={[k for k, v in fronts.items() if v > 1]} "
      f"duplicate_ids={[k for k, v in ids.items() if v > 1]}")
print("CARD L04-L06 count:", sum(c["lesson"] in ("L04", "L05", "L06") for c in cards))
ids_num = sorted(int(c["id"].split("-c")[1]) for c in cards)
print("CARD id gaps (upward numbering):", [i for i in range(1, max(ids_num) + 1) if i not in ids_num])

words = r"\b(only|all|always|every|any|same|exactly|drives?|never|no|none|whenever|each|unique)\b"
for n in ("04", "05", "06"):
    src = (root / f"course/modules/E/E5/L{n}.html").read_text(encoding="utf-8")
    t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(pre|script)\b.*?</\1>", " ", src, flags=re.S)))
    t = re.sub(r"\s+", " ", t)
    hits = [x for x in re.split(r"(?<=[.!?])\s+", t) if re.search(words, x, re.I)]
    print(f"SCOPE L{n} sentences with scope words: {len(hits)}")
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06") and re.search(r"\bonly\b", c["back"] + c["front"]):
        print("SCOPE-WORD CARD:", c["id"], "|", c["back"][:140])
print("FAILS", bad)
