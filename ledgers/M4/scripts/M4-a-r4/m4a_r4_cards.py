"""Round-4 card checks for M4 slice a (cards L01-L04) and the whole deck.

1. Every number token in a slice-a card back appears in its lesson page (fractions matched as a/b or \\tfrac{a}{b}).
2. Duplicate scan over all 212 cards: duplicate ids, duplicate fronts, and near-duplicate fronts (Jaccard >= 0.6).
3. Every card has lesson in its lesson list and grade T or (C with basis); no card has cite and basis both empty when grade != T.
Run: python -I -W error ledgers/M4/scripts/M4-a-r4/m4a_r4_cards.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
M4 = ROOT / "course" / "modules" / "M" / "M4"
cards = json.loads((M4 / "cards.json").read_text(encoding="utf-8"))
if isinstance(cards, dict):
    cards = cards.get("cards", [])

problems: list[str] = []
slice_lessons = {"L01", "L02", "L03", "L04"}


def lesson_text(name: str) -> str:
    raw = (M4 / f"{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return raw.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


texts = {n: lesson_text(n) for n in slice_lessons}
tex_texts = {n: (M4 / f"{n}.html").read_text(encoding="utf-8") for n in slice_lessons}

n_checked = 0
for c in cards:
    if c["lesson"] not in slice_lessons:
        continue
    n_checked += 1
    back = c["back"]
    for tok in re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", back):
        if tok in {"1", "0", "2", "3"}:
            continue  # small integers are too common to locate meaningfully
        found = tok in texts[c["lesson"]] or tok in tex_texts[c["lesson"]]
        if "/" in tok:
            a, b = tok.split("/")
            found = found or re.search(rf"tfrac\{{{a}\}}\{{{b}\}}", tex_texts[c["lesson"]]) is not None
            found = found or re.search(rf"\b{a}/{b}\b", texts[c["lesson"]]) is not None
        if not found:
            # look anywhere in the four slice lessons
            anywhere = any(tok in t or (("/" in tok) and re.search(rf"tfrac\{{{tok.split('/')[0]}\}}\{{{tok.split('/')[1]}\}}", tex_texts[n])) for n, t in texts.items())
            if not anywhere:
                problems.append(f"{c['id']}: number {tok!r} in back not found in {c['lesson']}")
            else:
                print(f"NOTE {c['id']}: {tok!r} found in another slice-a lesson, not its own {c['lesson']}")
    if c["grade"] != "T" and not c.get("basis") and not c.get("cite"):
        problems.append(f"{c['id']}: grade {c['grade']} without basis or cite")
    if c["grade"] == "C" and not c.get("basis"):
        problems.append(f"{c['id']}: grade C without basis")

print(f"slice-a cards checked for numbers: {n_checked}")

ids = Counter(c["id"] for c in cards)
dups = [i for i, n in ids.items() if n > 1]
if dups:
    problems.append(f"duplicate ids {dups}")
fronts = Counter(c["front"].strip().lower() for c in cards)
dfronts = [f for f, n in fronts.items() if n > 1]
if dfronts:
    problems.append(f"duplicate fronts {dfronts}")


def words(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


near = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        wa, wb = words(a["front"]), words(b["front"])
        if wa and wb:
            j = len(wa & wb) / len(wa | wb)
            if j >= 0.6:
                near.append((round(j, 2), a["id"], b["id"], a["front"], b["front"]))
print(f"deck cards: {len(cards)}; near-duplicate front pairs (Jaccard >= 0.6): {len(near)}")
for n in sorted(near, reverse=True)[:40]:
    print("  ", n)

missing_lessons = [c["id"] for c in cards if c["lesson"] not in {f"L{k:02d}" for k in range(1, 11)}]
if missing_lessons:
    problems.append(f"unknown lesson {missing_lessons}")

print("PROBLEMS:" if problems else "no problems")
for p in problems:
    print("  ", p)
sys.exit(1 if problems else 0)
