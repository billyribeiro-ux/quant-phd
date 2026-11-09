"""M2 slice a round 3: structure counts for index.html and L01-L06 (BUILDER_RULES 4.2, 4.3, 5.1; check_pages mirror).

Counts: why-it-matters words (<=120), misconceptions (>=3), problem-set problems per tier (>=3 each),
worked-solution word counts (>=15), quiz items (8-15), key-results rows, lab sections, numbered Assumption blocks,
and data-files attributes. Run: python -I ledgers/M2/scripts/M2-a-r3/structure_slice_a_r3.py <checkout-root>
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M2"


def text_of(fragment: str) -> str:
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(fragment)).strip()


for n in range(1, 7):
    src = (root / f"L{n:02d}.html").read_text(encoding="utf-8")
    why = re.search(r'<p class="why-it-matters">(.*?)</p>', src, re.S)
    why_words = len(text_of(why.group(1)).split()) if why else -1
    miscs = len(re.findall(r'<li class="misconception">', src))
    tiers = {t: len(re.findall(rf'<div class="problem"[^>]*>\s*<span class="problem-title">[^<]*</span>', src)) for t in ["mechanics"]}
    tier_blocks = re.split(r'<div class="tier" data-tier="', src)[1:]
    per_tier = {}
    sol_words = []
    for blk in tier_blocks:
        name = blk.split('"', 1)[0]
        probs = re.findall(r'<div class="problem"', blk)
        per_tier[name] = len(probs)
        for sol in re.findall(r'<details class="solution">(.*?)</details>', blk, re.S):
            body = re.sub(r"<summary>.*?</summary>", "", sol, flags=re.S)
            sol_words.append(len(text_of(body).split()))
    quiz_items = len(re.findall(r'<li class="item"', src))
    kr_rows = len(re.findall(r'<tr><td>', src.split('id="key-results"')[1].split("</table>")[0])) if 'id="key-results"' in src else -1
    labs = len(re.findall(r'<section class="lab"', src))
    assumptions = len(re.findall(r"Assumption \d\.\d", src))
    data_files = src.count("data-files")
    expected_blocks = len(re.findall(r'<pre class="expected"', src))
    print(
        f"L{n:02d}: why_words={why_words} (<=120: {why_words <= 120}); misconceptions={miscs} (>=3: {miscs >= 3}); "
        f"problems per tier={per_tier} (each >=3: {all(v >= 3 for v in per_tier.values()) and len(per_tier) == 4}); "
        f"solution words min={min(sol_words)} (>=15: {min(sol_words) >= 15}); quiz items={quiz_items} (8-15: {8 <= quiz_items <= 15}); "
        f"key-results rows={kr_rows}; labs={labs}; expected blocks={expected_blocks}; data-files={data_files}; "
        f"Assumption mentions={assumptions}"
    )
src = (root / "index.html").read_text(encoding="utf-8")
obj = len(re.findall(r'<ol class="objectives">\s*<li>', src)) and len(re.findall(r"<li><strong>", src.split('id="objectives"')[1].split("</ol>")[0]))
print(f"index: objectives={obj} (4-8: {4 <= obj <= 8}); ladder rungs={len(re.findall(r'<li><div><span class=\"rung-title\">', src))}; "
      f"lesson cards={len(re.findall(r'class=\"card\" href=', src))}; placement items={len(re.findall(r'<li class=\"item\"', src))}; "
      f"skill items={len(re.findall(r'data-skill', src))}; data-hours-lessons=240 data-hours-project=60 "
      f"{'present' if 'data-hours-lessons=\"240\" data-hours-project=\"60\"' in src else 'MISSING'}")
