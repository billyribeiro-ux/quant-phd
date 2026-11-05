"""Round-10 blind exemplar text: the memo prose of each exemplar with the annotations, the official verdict and the
data-scores attributes removed. Usage: python blind_memo_text_r10.py <repo_root>"""

import html
import re
import sys
from pathlib import Path

page = (Path(sys.argv[1]) / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="' + ex + r'".*?</article>', page, re.S).group(0)
    m = re.sub(r'<aside class="annotation".*?</aside>', "", m, flags=re.S)
    m = re.sub(r'<p class="exemplar-verdict".*?</p>', "", m, flags=re.S)
    m = re.sub(r'<h4[^>]*>.*?</h4>', "", m, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", m))
    print(f"=== {ex}")
    print(re.sub(r"[ \t]+", " ", text).strip())
