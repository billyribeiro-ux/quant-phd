"""Blind exemplar extraction (ruling 15): keep only the memo prose of each exemplar. Drops <aside class="annotation">,
the exemplar-verdict paragraph and every data-score/data-level attribute, and prints the rubric table without its
scores. Usage: blind_extract_r16.py <checkout root>."""
import html
import re
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/SC/SC1/project.html", encoding="utf-8").read()
rubric = re.search(r'<table class="rubric".*?</table>', page, re.S).group(0)
rubric = re.sub(r"<caption>.*?</caption>", "", rubric, flags=re.S)
rubric_text = html.unescape(re.sub(r"<[^>]+>", " | ", rubric))
print("RUBRIC (descriptors only):")
print(re.sub(r"(\s*\|\s*)+", " | ", rubric_text))
for ex in ("exemplar-a", "exemplar-b"):
    m = re.search(rf'<article class="exemplar" id="{ex}".*?</article>', page, re.S)
    body = m.group(0)
    body = re.sub(r'<aside class="annotation".*?</aside>', "", body, flags=re.S)
    body = re.sub(r'<p class="exemplar-verdict".*?</p>', "", body, flags=re.S)
    body = re.sub(r"<h4[^>]*>.*?</h4>", "", body, flags=re.S)
    print(f"\n==== {ex.upper()} (memo prose only) ====")
    for block in re.findall(r'<div class="memo-text">(.*?)</div>', body, re.S):
        print(html.unescape(re.sub(r"<[^>]+>", " ", block)).replace("  ", " ").strip())
        print("--")
