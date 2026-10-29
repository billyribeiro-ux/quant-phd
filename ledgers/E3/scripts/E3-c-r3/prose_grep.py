"""Grep learner prose (page text outside <pre> blocks) of L07 and L08 for banned, scope, process and out-of-closure words.

Usage: python -I ledgers/E3/scripts/E3-c-r3/prose_grep.py
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PATTERNS = {
    "banned": r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.",
    "process": r"\bbuild(er|ers|ing)?\b|\bverifier\b|\bround\b|REQUEST|unit report|planner|\bverif(y|ied|ication)\b",
    "scope": r"\b(every|all|always|never|any|only|exactly|same|drives|in general|welfare|market structures?)\b",
    "outside_closure": r"convex|concave|risk-neutral|risk neutral|Bellman|bellman|fixed point|infinite horizon|maximum likelihood|likelihood|estimator|confidence interval|Fisher|martingale|stochastic discount|equity risk premium|equity premium|expected value game|principle of optimality|logit|probability weighting",
}
for page in ("L07", "L08"):
    text = (ROOT / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    prose = re.sub(r"<pre.*?</pre>", " ", text, flags=re.S)
    prose = re.sub(r"<script.*?</script>|<style.*?</style>", " ", prose, flags=re.S)
    prose_text = html.unescape(re.sub(r"<[^>]+>", " ", prose))
    for name, pat in PATTERNS.items():
        hits = []
        for m in re.finditer(pat, prose_text, flags=re.I if name != "scope" else 0):
            s = max(0, m.start() - 70)
            hits.append(prose_text[s : m.end() + 50].replace("\n", " "))
        print(f"{page} {name}: {len(hits)}")
        for h in hits:
            print("    ", h)
