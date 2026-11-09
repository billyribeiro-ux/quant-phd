"""Ruling 15 blind extraction: print each exemplar's memo prose only.

Drops <aside class="annotation">, <p class="exemplar-verdict">, and data-score(s)/data-level attributes.
Usage: python -I extract_memo_r16.py <project.html>
"""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
out = []
for m in re.finditer(r'<article class="exemplar"[^>]*>.*?</article>', src, re.S):
    art = m.group(0)
    art = re.sub(r'<aside class="annotation".*?</aside>', "", art, flags=re.S)
    art = re.sub(r'<p class="exemplar-verdict"[^>]*>.*?</p>', "", art, flags=re.S)
    art = re.sub(r'\s+data-scores="[^"]*"', "", art)
    art = re.sub(r'\s+data-level="[^"]*"', "", art)
    art = re.sub(r"<[^>]+>", "", art)
    art = re.sub(r"\n\s*\n+", "\n", art)
    out.append(art.strip())
print("\n=====\n".join(out))
