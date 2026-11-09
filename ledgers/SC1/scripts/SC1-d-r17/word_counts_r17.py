"""Word counts of the two exemplar bodies and Summaries (verifier round 17). Usage: word_counts_r17.py <checkout root>."""
import html
import re
import sys
t = open(f"{sys.argv[1]}/course/modules/SC/SC1/project.html", encoding="utf-8").read()
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(rf'<article class="exemplar" id="{ex}".*?</article>', t, re.S).group(0)
    body = re.sub(r'<aside class="annotation".*?</aside>', "", m, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', "", body, flags=re.S)
    body = re.sub(r"<h4[^>]*>.*?</h4>", "", body, flags=re.S)
    blocks = re.findall(r'<div class="memo-text">(.*?)</div>', body, re.S)
    five = blocks[:5]
    noh = [re.sub(r"<h5>.*?</h5>", "", b, flags=re.S) for b in five]
    no_space = sum(len(html.unescape(re.sub(r"<[^>]+>", "", b)).split()) for b in noh)
    tag_space = sum(len(html.unescape(re.sub(r"<[^>]+>", " ", b)).split()) for b in noh)
    summary = len(html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"<h5>.*?</h5>", "", blocks[0], flags=re.S))).split())
    print(f"{ex}: body words (textContent split, headings removed) = {no_space}; tags as spaces = {tag_space}; Summary = {summary}")
