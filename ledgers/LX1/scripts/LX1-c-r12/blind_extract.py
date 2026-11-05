"""Blind extraction: prints each exemplar's essay text only (no annotations, scores, labels or levels)."""
import html
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
for art in re.finditer(r'<article class="exemplar"[^>]*>(.*?)</article>', src, re.S):
    body = art.group(1)
    # keep only the memo text blocks; drop annotation asides, reveal controls and score markup
    body = re.sub(r'<aside class="annotation".*?</aside>', '', body, flags=re.S)
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*(?=<aside|</div>|</article|$)', body, re.S)
    print("=== EXEMPLAR (essay text only) ===")
    for m in memos:
        text = re.sub(r'<[^>]+>', '', m)
        print(html.unescape(re.sub(r'\n\s*\n+', '\n', text)).strip())
        print('---')
    print()
