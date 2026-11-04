"""Round-8 verifier (M3 slice d): static checks over every card in course/modules/M/M3/cards.json.

1. Structure: JSON loads, ids unique, lesson exists, grade/basis rule, no cite without a registry key.
2. Locator references: every 'Definition N.M', 'Proposition N.M', 'Theorem N.M', 'Lemma N.M', 'Fact N.M', 'Lesson N'
   written in a card's text must name a block that exists in the lesson it is cited from (or in the lesson the card
   points to, for 'Lesson N, <block>' phrasing).
3. Numbers: every number token in a card's front/back must appear in the text of its lesson (the card's own lesson).
4. Deleted identifiers: no card mentions 'Definition 1.2a'.
5. Duplicates: token Jaccard >= 0.40 between card pairs (front+back), listed for reading.
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/cards_static_r8.py
"""

import html
import itertools
import json
import re
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / "course/modules/M/M3"
cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))


def plain(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)


LESSONS = {f"L{n:02d}": plain(BASE / f"L{n:02d}.html") for n in range(1, 10)}
RAW = {f"L{n:02d}": (BASE / f"L{n:02d}.html").read_text(encoding="utf-8") for n in range(1, 10)}
problems = []
ids = [c["id"] for c in cards]
if len(ids) != len(set(ids)):
    problems.append("duplicate ids")
print("cards:", len(cards), "unique ids:", len(set(ids)))
grades = {}
for c in cards:
    grades[c.get("grade", "(none)")] = grades.get(c.get("grade", "(none)"), 0) + 1
    if c["lesson"] not in LESSONS:
        problems.append(f"{c['id']}: unknown lesson {c['lesson']}")
    text = " ".join(str(c.get(k, "")) for k in ("front", "back", "basis"))
    if "1.2a" in text or "Definition 1.2a" in text:
        problems.append(f"{c['id']}: cites deleted Definition 1.2a")
    if c.get("grade") == "C" and not c.get("basis"):
        problems.append(f"{c['id']}: grade C without basis")
    if "cite" in c:
        problems.append(f"{c['id']}: has cite field {c['cite']}")
    # numbers in card text must appear in the cited lesson (plain text)
    lesson_text = LESSONS[c["lesson"]]
    for num in set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", text)):
        if num in {"0", "1", "2", "3"}:
            continue
        if num not in lesson_text:
            problems.append(f"{c['id']} ({c['lesson']}): number {num} not found in lesson text")
    # locator blocks named in the card
    for kind, n in re.findall(r"\b(Definition|Proposition|Theorem|Lemma|Fact|Remark|Example|Exercise)\s+(\d\.\d+)\b", text):
        target = f"{kind} {n}"
        in_own = target in lesson_text
        if not in_own:
            # allowed only as 'Lesson k, <block>' elsewhere in the card
            ok = False
            for lk, body in LESSONS.items():
                if target in body and re.search(rf"Lesson {int(lk[1:])}, {re.escape(target)}", text):
                    ok = True
            if not ok:
                problems.append(f"{c['id']} ({c['lesson']}): '{target}' not in its lesson and not cited as 'Lesson k, {target}'")
print("grades:", grades)
allc = [(c["id"], c["lesson"], (c["front"] + " " + c["back"]).lower()) for c in cards]
pairs = []
for (a, la, ta), (b, lb, tb) in itertools.combinations(allc, 2):
    sa, sb = set(re.findall(r"[a-z0-9]+", ta)), set(re.findall(r"[a-z0-9]+", tb))
    j = len(sa & sb) / max(1, len(sa | sb))
    if j >= 0.40:
        pairs.append((round(j, 2), a, la, b, lb))
pairs.sort(reverse=True)
print("pairs with Jaccard >= 0.40:", len(pairs))
for p in pairs:
    print("  ", p)
print("PROBLEMS:", len(problems))
for p in problems:
    print("  ", p)
