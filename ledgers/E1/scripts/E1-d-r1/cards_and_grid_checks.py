"""Card and lab-number checks for E1 (run: .venv/bin/python -I <this file> from the repository root). Standard library."""

import html
import json
import re
from pathlib import Path

ROOT = Path(".")
MOD = ROOT / "course/modules/E/E1"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))


def lesson_text(lesson: str) -> str:
    s = (MOD / f"{lesson}.html").read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s))


texts: dict[str, str] = {}
absent = []
dangling = []
for card in cards:
    t = texts.setdefault(card["lesson"], lesson_text(card["lesson"]))
    for n in set(re.findall(r"\d+(?:\.\d+)?", card["front"] + " " + card["back"])):
        if n not in t:
            absent.append((card["id"], n))
    for kind, num in set(re.findall(r"(Definition|Proposition|Theorem|Lemma|Example|Remark|Corollary|Problem|Assumption) ([0-9][0-9.]*[0-9]|[0-9])", card["front"] + " " + card["back"])):
        if f"{kind} {num}" not in t:
            dangling.append((card["id"], f"{kind} {num}"))
print("cards:", len(cards), "ids unique:", len({c["id"] for c in cards}) == len(cards))
print("numbers absent from own lesson:", absent)
print("dangling Definition/Proposition/Example references:", dangling)
numeric_t_without_basis = [c["id"] for c in cards if c.get("grade") == "T" and "basis" not in c]
print("T cards without basis:", len(numeric_t_without_basis))

# Lab 1 of L08 (Pareto grid, X=8, Y=4)
X, Y = 8, 4
pts = [(x, y) for x in range(X + 1) for y in range(Y + 1)]
u = lambda p: (p[0] * p[1], (X - p[0]) * (Y - p[1]))  # noqa: E731


def dominated(p):
    a_, b_ = u(p)
    return any(u(q)[0] >= a_ and u(q)[1] >= b_ and (u(q)[0] > a_ or u(q)[1] > b_) for q in pts)


eff = [p for p in pts if not dominated(p)]
inter = [p for p in eff if 0 < p[0] < X and 0 < p[1] < Y]
print("grid allocations", len(pts), "grid-efficient", len(eff), "interior", len(inter),
      "interior off diagonal", sum(1 for p in inter if p[1] * X != p[0] * Y))
