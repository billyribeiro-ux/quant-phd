"""Word counts for the two exemplars in project.html (run-of-characters-between-spaces rule from project.html Length)."""
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
    total_body = 0
    total_heads = 0
    print("==", ex, "passages", len(passages))
    for p in passages:
        heads = re.findall(r"<h5>(.*?)</h5>", p, re.S)
        body = re.sub(r"<h5>.*?</h5>", "", p, flags=re.S)
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        text = re.sub(r"\\\(|\\\)", " ", text)
        words = [w for w in text.split(" ") if w]
        hw = sum(len(html.unescape(re.sub(r"<[^>]+>", "", h)).split(" ")) for h in heads)
        total_body += len(words)
        total_heads += hw
        print(" heads:", [html.unescape(re.sub(r"<[^>]+>", "", h)) for h in heads], "body words", len(words), "head words", hw)
    print(" total body words (no headings):", total_body, " headings words:", total_heads, " total with headings:", total_body + total_heads)
