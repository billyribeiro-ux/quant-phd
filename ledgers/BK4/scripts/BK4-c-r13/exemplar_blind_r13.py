"""Round-13 BK4-c: extract exemplar memo prose with the official scoring, annotations and score attributes removed.

Prints only the memo text of exemplar A and B (headings and paragraphs), so the scorer sees the memo and the rubric
table and nothing else. Run: python3 -I ledgers/BK4/scripts/BK4-c-r13/exemplar_blind_r13.py
"""

import html
import re

SRC = "course/modules/BK/BK4/project.html"
text = open(SRC, encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    start = text.index(f'<article class="exemplar" id="{ex}"')
    end = text.index("</article>", start)
    block = text[start:end]
    block = re.sub(r'<p class="exemplar-verdict".*?</p>', "", block, flags=re.S)
    block = re.sub(r'<aside class="annotation".*?</aside>', "", block, flags=re.S)
    block = re.sub(r"<h4.*?</h4>", "", block, flags=re.S)
    block = re.sub(r"<(h5)>(.*?)</h5>", r"\n## \2", block, flags=re.S)
    block = re.sub(r"<p>(.*?)</p>", r"\1\n", block, flags=re.S)
    block = re.sub(r"<[^>]+>", "", block)
    print(f"=== {ex} (memo prose only) ===")
    print(html.unescape(block).strip())
    print()
