"""Blind exemplar extraction (ruling 23): prints only the memo prose of each exemplar.

Drops every <aside class="annotation">, every data-level / data-scores attribute and every
<h4> heading, so the scorer never sees annotations or the level labels. Usage:
  python3 -I blind_extract_r18.py <path-to-project.html>
"""
import re
import sys

path = sys.argv[1]
html = open(path, encoding="utf-8").read()
articles = re.findall(r'<article class="exemplar" id="(exemplar-[ab])"[^>]*>(.*?)</article>', html, re.S)
for art_id, body in articles:
    body = re.sub(r'<aside class="annotation".*?</aside>', "", body, flags=re.S)
    print(f"=== {art_id} ===")
    passages = re.findall(r'<div class="memo-text">(.*?)</div>', body, re.S)
    for i, p in enumerate(passages, 1):
        txt = re.sub(r"<[^>]+>", " ", p)
        txt = re.sub(r"[ \t]+", " ", txt).strip()
        print(f"--- passage {i} ---")
        print(txt)
