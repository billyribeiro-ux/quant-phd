"""Round-9 structural and presence checks on course/modules/PC/PC3/cards.json against the six lessons.

For every card: schema keys, unique id, lesson exists, grade/basis pairing, and every number token that appears in the
card's front or back is looked up in the plain text of the card's own lesson (or, failing that, in any PC3 lesson).
Also checks near-duplicate fronts. Output is printed; nothing is written into the course tree.
"""

import difflib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE9-PC3-d")
PC3 = ROOT / "course/modules/PC/PC3"
cards = json.loads((PC3 / "cards.json").read_text())

lesson_text: dict[str, str] = {}
for L in ["L01", "L02", "L03", "L04", "L05", "L06"]:
    s = html.unescape((PC3 / f"{L}.html").read_text())
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\\\(|\\\)|\\\[|\\\]|\$", " ", s)
    s = re.sub(r"\s+", " ", s)
    lesson_text[L] = s

ids = [c["id"] for c in cards]
problems: list[str] = []
print("cards:", len(cards), "unique ids:", len(set(ids)))
if len(set(ids)) != len(ids):
    problems.append("duplicate ids")
for c in cards:
    keys = set(c)
    if not {"id", "lesson", "front", "back", "cite"} <= keys:
        problems.append(f"{c['id']} missing keys {keys}")
    if c["lesson"] not in lesson_text:
        problems.append(f"{c['id']} unknown lesson {c['lesson']}")
    if ("grade" in c) != ("basis" in c):
        problems.append(f"{c['id']} grade/basis mismatch")
    if c.get("cite"):
        problems.append(f"{c['id']} has cite {c['cite']}")

NUM = re.compile(r"\d+(?:[.,]\d+)*(?:/\d+)?")
absent: list[str] = []
for c in cards:
    text = c["front"] + " " + c["back"]
    for tok in set(NUM.findall(text)):
        t = tok.replace(",", "")
        own = lesson_text.get(c["lesson"], "")
        if tok in own or t in own:
            continue
        anywhere = any((tok in v or t in v) for v in lesson_text.values())
        absent.append(f"{c['id']} ({c['lesson']}): '{tok}' in own lesson={False} in any PC3 lesson={anywhere}")

print("number tokens not found in own lesson:", len(absent))
for a in absent:
    print("  ", a)

# near-duplicate fronts across the whole deck
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, cards[i]["front"], cards[j]["front"]).ratio()
        if r > 0.8:
            pairs.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
print("near-duplicate front pairs (ratio > 0.8):", pairs)
if problems:
    print("PROBLEMS:", problems)
    sys.exit(1)
print("structure: PASS")
