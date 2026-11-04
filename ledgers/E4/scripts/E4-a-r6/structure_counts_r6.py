"""E4 slice a round 6: word counts (why-it-matters, solutions), misconception and problem counts, quiz items.

Usage: python -I structure_counts_r6.py <checkout-root>
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course" / "modules" / "E" / "E4"


def text_of(fragment: str) -> str:
    fragment = re.sub(r"<script.*?</script>|<style.*?</style>", " ", fragment, flags=re.S)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return " ".join(html.unescape(fragment).split())


for name in ("L01.html", "L02.html", "L03.html"):
    raw = (root / name).read_text(encoding="utf-8")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    why_words = len(text_of(why.group(1)).split()) if why else -1
    sols = re.findall(r'<details class="solution">(.*?)</details>', raw, re.S)
    sol_words = [len(text_of(s).split()) for s in sols]
    mis = len(re.findall(r'<li class="misconception">', raw))
    problems = re.findall(r'<div class="problem" id="([A-Z][0-9])"', raw)
    quiz = len(re.findall(r'<section class="quiz".*?</section>', raw, re.S)) and len(
        re.findall(r'<li class="item"', re.search(r'<section class="quiz".*?</section>', raw, re.S).group(0))
    )
    quiz_exp = len(re.findall(r'<div class="explain" hidden>', raw))
    print(f"{name}: why_it_matters_words={why_words} solutions={len(sols)} min_solution_words={min(sol_words)} "
          f"misconceptions={mis} problems={problems} quiz_items={quiz} explanations={quiz_exp}")
    print(f"{name}: solution word counts {sol_words}")
