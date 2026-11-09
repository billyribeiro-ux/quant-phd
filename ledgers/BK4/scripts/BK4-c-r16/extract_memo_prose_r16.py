"""Round-16 blind exemplar extraction (ruling 15), slice c.

Writes the memo prose of exemplar A and exemplar B from course/modules/BK/BK4/project.html with the annotation
asides (aside.annotation), the verdict paragraphs (p.exemplar-verdict) and every data-score/data-scores/data-level
attribute removed. Usage: python -I extract_memo_prose_r16.py <checkout-root> <out-dir>
"""

import html
import re
import sys
from pathlib import Path

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
page = (root / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
out.mkdir(parents=True, exist_ok=True)
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(rf'<article class="exemplar" id="{ex}".*?</article>', page, flags=re.S)
    body = m.group(0)
    body = re.sub(r'<aside class="annotation".*?</aside>', "", body, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', "", body, flags=re.S)
    body = re.sub(r'\s(data-scores?|data-level|data-label)="[^"]*"', "", body)
    prose = re.sub(r"<[^>]+>", " ", body)
    prose = re.sub(r"[ \t]+", " ", html.unescape(prose))
    prose = "\n".join(line.strip() for line in prose.splitlines() if line.strip())
    (out / f"{ex}_prose.txt").write_text(prose + "\n", encoding="utf-8")
    print(ex, "chars", len(prose), "contains 'Meets'/'Misses'/'Official':", [w in prose for w in ("Meets", "Misses", "Official", "data-score", "level")])
