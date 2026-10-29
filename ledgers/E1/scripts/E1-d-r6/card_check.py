"""Round-6 E1-d card check: for each card in cards.json, verify its labelled references exist in its lesson,
its numbers appear in the lesson text (or the lab output of that lesson), and report duplicates.

Usage: python ledgers/E1/scripts/E1-d-r6/card_check.py <repo-root>
"""
import html
import json
import pathlib
import re
import sys
from collections import Counter

root = pathlib.Path(sys.argv[1])
mod = root / "course/modules/E/E1"
cards = json.loads((mod / "cards.json").read_text(encoding="utf-8"))


def text_of(path: pathlib.Path) -> str:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


lesson_text = {}
for n in range(1, 10):
    key = f"L{n:02d}"
    lesson_text[key] = text_of(mod / f"{key}.html")

# Labelled references that a card may cite: "Definition 1.1", "Proposition 2.3", "Lab 1", "Misconception 2", ...
label_re = re.compile(r"\b(Definition|Proposition|Lemma|Theorem|Corollary|Remark|Example|Misconception|Problem|Assumption|Section)\s+([0-9]+(?:\.[0-9]+)?|[A-Z][0-9]*|[A-Z])\b")
num_re = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")

problems = []
for c in cards:
    text = lesson_text[c["lesson"]]
    body = c["front"] + " " + c["back"]
    for kind, ident in label_re.findall(body):
        needle = f"{kind} {ident}"
        if needle not in text:
            problems.append((c["id"], c["lesson"], "label-missing", needle))
    # numbers in the card (skip those that are part of a label reference)
    stripped = label_re.sub(" ", body)
    for tok in set(num_re.findall(stripped)):
        if tok in ("1", "2", "0"):
            continue
        if not re.search(r"(?<![\d.])" + re.escape(tok) + r"(?![\d])", text):
            problems.append((c["id"], c["lesson"], "number-not-in-lesson", tok))

dupes = Counter(re.sub(r"\W+", " ", (c["front"] + " " + c["back"]).lower()) for c in cards)
for k, v in dupes.items():
    if v > 1:
        problems.append(("-", "-", "duplicate-text", k[:80]))

ids = Counter(c["id"] for c in cards)
for k, v in ids.items():
    if v > 1:
        problems.append((k, "-", "duplicate-id", str(v)))

print(f"cards: {len(cards)}")
for p in problems:
    print("PROBLEM", *p)
print(f"problems: {len(problems)}")
