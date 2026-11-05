"""Blind exemplar text for rubric calibration: the exemplar passages only, with the annotation asides, the official
scoring paragraph and every data attribute removed. The rubric table is printed first, so the scorer reads the
criteria before the text."""

import html
import re
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text(encoding="utf-8")
rubric = re.search(r'<table class="rubric".*?</table>', page, re.S).group(0)
rows = re.findall(r'<tr data-criterion="(C\d)">(.*?)</tr>', rubric, re.S)
print("RUBRIC (criterion | level 4 | level 3 | level 2 | level 1)")
for crit, body in rows:
    cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<(?:th|td)[^>]*>(.*?)</(?:th|td)>", body, re.S)]
    print(" | ".join(cells))
print()
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(rf'<article class="exemplar" id="{ex}".*?</article>', page, re.S).group(0)
    m = re.sub(r'<aside class="annotation".*?</aside>', "", m, flags=re.S)
    m = re.sub(r'<p class="exemplar-verdict".*?</p>', "", m, flags=re.S)
    print(f"=== {ex} (blind) ===")
    for h, body in re.findall(r'<h5>(.*?)</h5>\s*(.*?)\s*</div>\s*</div>', m, re.S):
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        print(f"[{html.unescape(h)}] " + re.sub(r"\s+", " ", text).strip())
        print()
