"""Round-2 structure census for M2 L13-L18.

Run: python -I structure_r2.py <checkout_root>
Counts: data-hours; h2 section order; 'Why it matters' words (the lead text after the legend 'Xrefuted' line and
before the first section heading, converted to plain text); solutions per tier; misconception items; quiz items
(li.item); lab sections.
"""

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/M/M2"


def plain(src: str) -> str:
    src = re.sub(r"(?s)<script.*?</script>", "", src)
    src = re.sub(r"(?s)<style.*?</style>", "", src)
    src = re.sub(r"(?i)</(p|li|h[1-6]|div|section|tr|pre|details|summary|figcaption|dt|dd|blockquote)>", "\n", src)
    src = re.sub(r"(?i)<br\s*/?>", "\n", src)
    src = re.sub(r"(?i)<h[1-6][^>]*>", "\n## ", src)
    src = re.sub(r"(?s)<pre[^>]*>", "\n[PRE]\n", src)
    src = re.sub(r"(?s)</?[a-zA-Z][a-zA-Z0-9]*(\s[^>]*)?/?>", "", src)
    return html.unescape(src)


for n in range(13, 19):
    src = (root / f"L{n}.html").read_text(encoding="utf-8")
    hours = re.search(r'data-hours="(\d+)"', src)
    heads = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in re.findall(r"<h2[^>]*>(.*?)</h2>", src, re.S)]
    lines = plain(src).split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "Xrefuted") + 1
    lead_lines = []
    for ln in lines[start:]:
        if ln.startswith("## "):
            break
        if ln.strip():
            lead_lines.append(ln.strip())
    why_words = len(" ".join(lead_lines).split())
    solutions = len(re.findall(r'<details class="solution"', src))
    tiers = {t: len(re.findall(rf'<div class="tier" data-tier="{t}"', src)) for t in ("mechanics", "proof", "empirical", "research")}
    misc = len(re.findall(r'<li class="misconception"', src))
    quiz = len(re.findall(r'<li class="item"', src))
    labs = len(re.findall(r'<section class="lab"', src))
    print(f"L{n}: data-hours={hours.group(1) if hours else None} why_words={why_words} solutions={solutions} tiers={tiers} "
          f"misconceptions={misc} quiz_items={quiz} lab_sections={labs}")
    print(f"    h2: {heads}")
