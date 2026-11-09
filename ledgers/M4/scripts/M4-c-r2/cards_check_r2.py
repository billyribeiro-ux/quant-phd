"""Verifier round 2, slice M4-c: card checks for cards.json entries of L08 to L10.

1. ids and fronts unique across the whole file; per-lesson counts for L08 to L10.
2. every numeric token (decimal or 2+ digit, or fraction a/b) in a slice card's back appears in its lesson page.
3. token-Jaccard near-duplicate scan (front+back) over the whole file, pairs at or above 0.45 printed.
4. every slice card: grade in T/A/B/C/D/X; a non-T grade carries a basis or cite.
Run as: python -I <this file> <checkout root>.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()
cards = json.loads((ROOT / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
ids = [c["id"] for c in cards]
fronts = [c["front"] for c in cards]
print("duplicate ids", len(ids) - len(set(ids)), "duplicate fronts", len(fronts) - len(set(fronts)))
from collections import Counter
cnt = Counter(c["lesson"] for c in cards)
print("per lesson", {k: cnt[k] for k in sorted(cnt)})
slice_cards = [c for c in cards if c["lesson"] in ("L08", "L09", "L10")]
print("slice cards", len(slice_cards))
pages = {l: (ROOT / f"course/modules/M/M4/{l}.html").read_text(encoding="utf-8") for l in ("L08", "L09", "L10")}
plain = {l: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)).replace("&lt;", "<").replace("&gt;", ">") for l, t in pages.items()}
misses = []
for c in slice_cards:
    toks = set(re.findall(r"\d+\.\d+|\d{2,}|\d+/\d+", c["back"]))
    for tok in sorted(toks):
        if tok not in plain[c["lesson"]] and tok not in pages[c["lesson"]]:
            misses.append((c["id"], tok))
print("number tokens in slice card backs not found in their lesson:", misses if misses else "none")
bad_grade = [c["id"] for c in cards if c["grade"] not in "TABCDX" or len(c["grade"]) != 1]
print("bad grades among all cards:", bad_grade if bad_grade else "none")
nonT_no_basis = [c["id"] for c in slice_cards if c["grade"] != "T" and not c.get("basis")]
print("slice non-T cards without basis:", nonT_no_basis if nonT_no_basis else "none")
def toks(c):
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))
pairs = []
for i in range(len(cards)):
    ti = toks(cards[i])
    for j in range(i + 1, len(cards)):
        tj = toks(cards[j])
        jac = len(ti & tj) / max(1, len(ti | tj))
        if jac >= 0.45:
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"]))
print("near-duplicate pairs (Jaccard >= 0.45) involving slice cards:")
for p in sorted(pairs, reverse=True):
    if p[1] in {c["id"] for c in slice_cards} or p[2] in {c["id"] for c in slice_cards}:
        a = next(c for c in cards if c["id"] == p[1])
        b = next(c for c in cards if c["id"] == p[2])
        print("  ", p, "|", a["front"][:70], "||", b["front"][:70])
print("all-file near-duplicate pairs:", len(pairs))
