"""Round-4 verifier: structural counts and prose scans for PC3 slice a (index, L01-L03).

Run from the checkout root: python -I ledgers/PC3/scripts/PC3-a-r4/counts_and_scans_a_r4.py
Counts: why-it-matters words, problems per tier with solutions, misconceptions, quiz items, key-results rows,
lab sections, dfn tags. Scans: banned phrases, process words, out-of-closure concept terms, and the first
learner-visible occurrence of terms that are defined later (stopping rule, expected payoff, event).
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path.cwd()
PAGES = ["index", "L01", "L02", "L03"]
BASE = ROOT / "course/modules/PC/PC3"


def text_of(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def read(name: str) -> str:
    return (BASE / f"{name}.html").read_text(encoding="utf-8")


for p in ["L01", "L02", "L03"]:
    t = read(p)
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
    assert why is not None
    print(p, "why-it-matters words (whitespace split, math tokens counted):", len(text_of(why.group(1)).split()))
    for name, body in re.findall(r'<div class="tier" data-tier="(\w+)">(.*?)</div>\s*</div>', t, re.S):
        print(
            p,
            "tier",
            name,
            "problems:",
            len(re.findall(r'class="problem"', body)),
            "solutions:",
            len(re.findall(r'<details class="solution"', body)),
        )
    print(p, "misconceptions:", len(re.findall(r'class="misconception"', t)))
    quiz_match = re.search(r'<section class="quiz".*?</section>', t, re.S)
    assert quiz_match is not None
    quiz = quiz_match.group(0)
    print(p, "quiz items:", len(re.findall(r'<li class="item"', quiz)), "explain blocks:", len(re.findall(r'class="explain"', quiz)))
    kr_match = re.search(r'<table class="key-results">(.*?)</table>', t, re.S)
    assert kr_match is not None
    print(p, "key-results rows:", len(re.findall(r"<tr><td>", kr_match.group(1))))
    print(p, "lab sections:", len(re.findall(r'<section class="lab"', t)), "expected blocks:", len(re.findall(r'<pre class="expected"', t)))
    print(p, "dfn tags:", len(re.findall(r"<dfn", t)), "claim spans:", len(re.findall(r'class="claim"', t)))

idx = read("index")
obj_match = re.search(r'<ol class="objectives">(.*?)</ol>', idx, re.S)
assert obj_match is not None
print("index objectives:", len(re.findall(r"<li>", obj_match.group(1))))
print("index placement items:", len(re.findall(r'class="item"', idx)))
print("index lesson cards:", len(re.findall(r'class="card"', idx)))
print("index ladder rungs:", len(re.findall(r'class="rung-title"', idx)))

print("\n-- banned phrases (BUILDER 1.3-1.4), prose only --")
BANNED = (
    r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more"
    r"|it is important to note|studies show|experts agree|it is well known|obviously|clearly"
)
for p in PAGES:
    prose = re.sub(r"<pre.*?</pre>", "", read(p), flags=re.S)
    print(p, "banned hits:", re.findall(BANNED, prose, flags=re.I))

print("\n-- process words in learner text (prose, code blocks removed) --")
for p in PAGES:
    prose = re.sub(r"<pre.*?</pre>", "", read(p), flags=re.S)
    print(p, "process-word hits:", re.findall(r"\b(round|rounds|verifier|builder|build|REQUESTS|fixer)\b", prose, flags=re.I))

print("\n-- out-of-closure / prose-only DAG terms (plan section 4) --")
DTERMS = (
    r"martingale|bayesian|kelly|poisson|markov|capm|duration|dcf|adverse selection|winner|stopping time"
    r"|optional stopping|binomial distribution|bid-ask|limit order|mark-to-market"
)
for p in PAGES:
    t = read(p)
    print(p, "D-term hits:", [m.group(0) for m in re.finditer(DTERMS, t, flags=re.I)])

print("\n-- first learner-visible occurrence of terms (tags, code and pre blocks stripped) --")
for p in ["L01", "L02", "L03"]:
    prose = text_of(re.sub(r"<script.*?</script>|<pre.*?</pre>", " ", read(p), flags=re.S))
    for term in ["stopping rule", "stopping polic", "fair game", "expected payoff", "event", "conditional probability"]:
        hits = [m.start() for m in re.finditer(re.escape(term), prose, flags=re.I)]
        if hits:
            print(f"{term!r} in {p}: {len(hits)} hits in prose, first at char offset {hits[0]}")
