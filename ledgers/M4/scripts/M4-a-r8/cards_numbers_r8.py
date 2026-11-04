"""Verifier r8: every numeric token on a slice-a card back (L01-L04) must occur in its lesson page (TeX-normalized)."""
import html
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M4/cards.json", encoding="utf-8"))
cards = cards if isinstance(cards, list) else cards.get("cards", [])

def norm(s):
    s = re.sub(r"\\[dt]?frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", s)
    s = re.sub(r"\\[dt]?frac(\d)(\d)", r"\1/\2", s)
    s = re.sub(r"\\[a-zA-Z]+|[{}$\\()]", " ", s)
    s = re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", " ", s)))
    return s

pages = {l: norm(open(f"{root}/course/modules/M/M4/{l}.html", encoding="utf-8").read()) for l in ["L01", "L02", "L03", "L04"]}
bad = []
checked = 0
for c in cards:
    if c["lesson"] not in pages:
        continue
    checked += 1
    for tok in set(re.findall(r"\d+(?:/\d+)?(?:\.\d+)?", c["back"])):
        if tok in ("1", "0", "2", "3", "4"):
            continue
        if tok not in pages[c["lesson"]]:
            bad.append((c["id"], c["lesson"], tok))
print("slice-a cards checked", checked)
for b in sorted(bad):
    print("NOT-IN-LESSON", b)
print("done", len(bad), "tokens not found (small integers 0-4 excluded)")
