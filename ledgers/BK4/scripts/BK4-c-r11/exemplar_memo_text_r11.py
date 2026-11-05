"""Round-11: print each exemplar's memo prose only (no annotation aside, no official scoring) for blind rubric scoring.

Usage: python -I exemplar_memo_text_r11.py <repo_root>
"""

import html
import re
import sys
from pathlib import Path

page = (Path(sys.argv[1]) / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    article = re.search(r'<article class="exemplar" id="' + ex + r'".*?</article>', page, re.S).group(0)
    memo = re.search(r'<div class="memo-text">(.*?)</div>\s*<aside', article, re.S).group(1)
    text = html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"</(p|h5)>", "\n", memo))).strip()
    print(f"=== {ex} memo prose ({len(text.split())} words)")
    print(text)
