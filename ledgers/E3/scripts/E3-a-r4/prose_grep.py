"""Grep learner prose (page text outside <pre> blocks) of the E3 slice a pages for banned, process and scope words.

Usage: python -I ledgers/E3/scripts/E3-a-r4/prose_grep.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PATTERNS = {
    "banned": r"TODO|TBD|lorem|for brevity|details omitted|beyond the scope|left as an exercise|you can add more|it is important to note|studies show|experts agree|it is well known|obviously|clearly|\.\.\.",
    "process": r"\bbuild(er|ers|ing)?\b|\bverifier\b|\bround\b|REQUEST|unit report|planner|\bverif(y|ied|ication)\b|\bfix(ed)?\b|\bbatch\b|\bslice\b|\bpin\b",
    "scope": r"\b(every|all|always|never|any|only|exactly|same|drives|in general)\b",
}
for page in ("index", "L01", "L02", "L03"):
    text = (ROOT / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    prose = re.sub(r"<pre.*?</pre>", " ", text, flags=re.S)
    prose = re.sub(r"<script.*?</script>|<style.*?</style>", " ", prose, flags=re.S)
    prose_text = html.unescape(re.sub(r"<[^>]+>", " ", prose))
    for name, pat in PATTERNS.items():
        hits = [prose_text[max(0, m.start() - 60) : m.end() + 40].replace("\n", " ")
                for m in re.finditer(pat, prose_text, flags=re.I if name != "scope" else 0)]
        print(f"{page} {name}: {len(hits)}")
        if name != "scope":
            for h in hits:
                print("    ", h)
