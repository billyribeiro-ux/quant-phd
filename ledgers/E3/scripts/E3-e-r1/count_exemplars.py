"""Recount the memo-text words of the two exemplars in project.html (outside slice e; observation only)."""
import html
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    article = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, text, re.S).group(0)
    parts = re.findall(r'<div class="memo-text">(.*?)<aside class="annotation"', article, re.S)
    spaced = sum(len(html.unescape(re.sub(r"<[^>]+>", " ", p)).split()) for p in parts)
    glued = sum(len(html.unescape(re.sub(r"<[^>]+>", "", p)).split()) for p in parts)
    print(f"{ex}: memo blocks {len(parts)}, words (tags as breaks) {spaced}, words (tags removed) {glued}")
