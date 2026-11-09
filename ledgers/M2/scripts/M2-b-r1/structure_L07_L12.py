# Structural counts for M2 lessons L07-L12 (run with python -I from checkout root).
import re, sys
from html.parser import HTMLParser
base = "course/modules/M/M2/"
for n in range(7, 13):
    p = f"{base}L{n:02d}.html"
    src = open(p, encoding="utf-8").read()
    m = re.search(r'<p class="why-it-matters">(.*?)</p>', src, re.S)
    text = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
    text = re.sub(r"\\\((.*?)\\\)", r" \1 ", text)
    words = len(text.split())
    mis = len(re.findall(r'<li class="misconception">', src))
    probs = {t: len(re.findall(rf'<div class="tier" data-tier="{t}">', src)) for t in ["mechanics","proof","empirical","research"]}
    nprob = len(re.findall(r'<div class="problem" id="L%02d-' % n, src))
    sols = len(re.findall(r'<details class="solution">', src))
    quiz = len(re.findall(r'<li class="item"', src))
    labs = len(re.findall(r'<section class="lab"', src))
    dfn = re.findall(r'<dfn id="([^"]+)" data-concept="([^"]+)"', src)
    hours = re.search(r'data-hours="(\d+)"', src).group(1)
    claims = len(re.findall(r'data-grade="[TABCDX]"', src))
    ungraded_T = len(re.findall(r'class="block (theorem|proposition|lemma|corollary)"', src))
    print(f"L{n:02d} why_words={words} misc={mis} problems={nprob} sol={sols} tiers={probs} quiz={quiz} labs={labs} dfn={dfn} hours={hours} grade_marks={claims} thm_blocks={ungraded_T}")
