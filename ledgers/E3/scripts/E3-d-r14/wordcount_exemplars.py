"""Word count of each exemplar memo: the memo-text blocks only, tags removed, runs of non-space characters, headings included."""

import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
for name in ("exemplar-a", "exemplar-b"):
    start = src.index(f'<article class="exemplar" id="{name}"')
    end = src.index("</article>", start)
    article = src[start:end]
    article = re.sub(r'<aside class="annotation".*?</aside>', "", article, flags=re.S)
    article = re.sub(r'<p class="exemplar-verdict".*?</p>', "", article, flags=re.S)
    memo = " ".join(re.findall(r'<div class="memo-text">(.*?)</div>', article, flags=re.S))
    text = re.sub(r"<[^>]+>", " ", memo)
    print(name, "memo words:", len(text.split()))
    full = re.sub(r"<[^>]+>", " ", article)
    print(name, "article words (incl. verdict and annotations, for reference):", len(full.split()))
# Section word count of the whole project page's own report brief is not counted here.
