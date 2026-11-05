"""Structure, counts and wording checks for E4 slice-a pages (read-only).

Usage: .venv/bin/python -I ledgers/E4/scripts/E4-a-r10/structure_check.py
Checks: why-it-matters word counts (<=120), solution word counts (>=15), problem tiers (>=3 each),
misconceptions (>=3), quiz items (8-15) with one data-correct per mc item and an explain block,
numeric answers present, duplicate dfn ids across the unit, concept hrefs resolve to a real target.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E4 = ROOT / "course/modules/E/E4"
PAGES = ["L01.html", "L02.html", "L03.html"]


def words(fragment: str) -> int:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = re.sub(r"\\\(|\\\)|\\\[|\\\]", " ", text)
    return len(text.split())


for page in PAGES:
    text = (E4 / page).read_text(encoding="utf-8")
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', text, flags=re.S)
    print(f"{page}: why-it-matters words = {words(wim.group(1))}")
    sols = re.findall(r'<details class="solution">(.*?)</details>', text, flags=re.S)
    short = [i for i, s in enumerate(sols) if words(s) < 15]
    print(f"{page}: solutions = {len(sols)}, under 15 words = {short}")
    tiers = re.findall(r'<div class="tier" data-tier="(\w+)">(.*?)</div>\s*(?=<div class="tier"|</section>)', text, flags=re.S)
    print(f"{page}: tiers = {[(t, len(re.findall(r'class=\"problem\"', b))) for t, b in tiers]}")
    print(f"{page}: misconceptions = {len(re.findall(r'class=\"misconception\"', text))}")
    quiz = re.search(r'<section class="quiz" id="quiz".*?</section>', text, flags=re.S).group(0)
    items = re.findall(r'<li class="item"[^>]*>(.*?)</li>', quiz, flags=re.S)
    for n, it in enumerate(items, 1):
        kind = re.search(r'data-kind="(\w+)"', quiz[quiz.find(it) - 200: quiz.find(it)]) if False else None
        has_explain = 'class="explain"' in it
        correct = it.count("data-correct")
        numeric = 'data-answer=' in it or 'type="number"' in it
        if not has_explain or (not numeric and correct != 1):
            print(f"{page}: quiz item {n} problem: explain={has_explain} correct_marks={correct} numeric={numeric}")
    print(f"{page}: quiz items = {len(items)}")
    print(f"{page}: data-hours = {re.search(r'data-hours=\"(\d+)\"', text).group(1)}")

ids = Counter()
for path in sorted(E4.glob("*.html")):
    for m in re.finditer(r'<dfn id="(def-[\w-]+)" data-concept="([\w-]+)"', path.read_text(encoding="utf-8")):
        ids[m.group(2)] += 1
print("dfn data-concept definitions across E4 pages:", dict(ids))

concepts_html = (ROOT / "course/concepts.html").read_text(encoding="utf-8")
concept_ids = set(re.findall(r'id="([\w-]+)"', concepts_html))
bad = []
for path in sorted(E4.glob("*.html")):
    t = path.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', t):
        if "concepts.html#" in href:
            cid = href.split("#", 1)[1]
            if cid not in concept_ids:
                bad.append((path.name, href))
        elif href.startswith("L") and "#def-" in href:
            target = E4 / href.split("#", 1)[0]
            anchor = href.split("#", 1)[1]
            if not target.exists() or f'id="{anchor}"' not in target.read_text(encoding="utf-8"):
                bad.append((path.name, href))
print("unresolved concept hrefs:", bad if bad else "none")
