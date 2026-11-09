"""Prose-only word counts (math \\( ... \\) segments removed; raw run-of-characters count also printed)."""
import html
import re
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
for ex in ("exemplar-a", "exemplar-b"):
    start = src.index(f'id="{ex}"')
    end = src.index("</article>", start)
    block = src[start:end]
    passages = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, re.S)
    prose = raw = heads_total = 0
    for p in passages:
        heads = re.findall(r"<h5>(.*?)</h5>", p, re.S)
        body = re.sub(r"<h5>.*?</h5>", "", p, flags=re.S)
        body = html.unescape(re.sub(r"<[^>]+>", " ", body))
        raw += len([w for w in body.split() if w])
        nomath = re.sub(r"\\\(.*?\\\)", " ", body, flags=re.S)
        prose += len([w for w in nomath.split() if w])
        heads_total += sum(len(html.unescape(re.sub(r"<[^>]+>", "", h)).split()) for h in heads)
    print(ex, "prose-only body", prose, "| raw body (math tokens counted)", raw, "| headings words", heads_total,
          "| prose+headings", prose + heads_total)
    if ex == "exemplar-b":
        sm = re.search(r"<h5>Summary</h5>\s*<p>(.*?)</p>", block, re.S)
        s = html.unescape(re.sub(r"<[^>]+>", " ", sm.group(1)))
        print("  B summary raw words", len(s.split()), " prose-only", len(re.sub(r"\\\(.*?\\\)", " ", s, flags=re.S).split()))
