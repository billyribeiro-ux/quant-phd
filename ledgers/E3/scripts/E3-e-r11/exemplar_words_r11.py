import re, sys, html
src = open(sys.argv[1], encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(r'<article class="exemplar" id="%s".*?</article>' % ex, src, re.S)
    body = m.group(0)
    # memo text only: the div.memo-text blocks, headings included, tags removed
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', body, re.S)
    text_memo = " ".join(memos)
    text_memo = re.sub(r"<[^>]+>", " ", text_memo)
    text_memo = html.unescape(text_memo)
    print(ex, "memo-text blocks:", len(memos), "words (whitespace runs, tags removed, headings included):", len(text_memo.split()))
    whole = re.sub(r"<[^>]+>", " ", body)
    print(ex, "whole article incl. verdict and annotations:", len(html.unescape(whole).split()))
    print(ex, "memo-text h5 headings:", re.findall(r"<h5>(.*?)</h5>", body))
