"""Round-9 verifier (M3 slice d): (1) every decimal number on a card appears in the card's lesson HTML or in that lesson's
twin output; (2) pairwise near-duplicate scan of card fronts and backs (token Jaccard >= 0.6 on front+back).

Run: .venv/bin/python -I ledgers/M3/scripts/M3-d-r9/cards_numbers_dupes_r9.py
"""
import html
import itertools
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path.cwd()
M3 = ROOT / "course/modules/M/M3"
cards = json.loads((M3 / "cards.json").read_text(encoding="utf-8"))
texts, outs = {}, {}
for n in range(1, 10):
    lesson = f"L0{n}"
    raw = (M3 / f"{lesson}.html").read_text(encoding="utf-8")
    texts[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    twin = ROOT / f"tests/labs/M3/lab-M3-{lesson}-1.py"
    if twin.exists():
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
        outs[lesson] = r.stdout
miss = []
for card in cards:
    s = card["front"] + " " + card["back"]
    nums = set(re.findall(r"(?<![\w.])\d+\.\d+(?:e-?\d+)?", s))
    for num in nums:
        if num not in texts[card["lesson"]] and num not in outs.get(card["lesson"], ""):
            miss.append((card["id"], card["lesson"], num))
print("decimal numbers not found in lesson text or twin output:", len(miss))
for m in miss:
    print("  ", m)
def toks(c):
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))
pairs = []
T = [toks(c) for c in cards]
for i, j in itertools.combinations(range(len(cards)), 2):
    inter = len(T[i] & T[j])
    union = len(T[i] | T[j])
    if union and inter / union >= 0.6:
        pairs.append((cards[i]["id"], cards[j]["id"], round(inter / union, 2)))
print("pairs with Jaccard >= 0.6:", len(pairs), pairs[:20])
print("pairs scanned:", len(cards) * (len(cards) - 1) // 2)
