"""Round-4 verifier (E3-d): word counts of the two exemplar memo texts in project.html.

Counts runs of characters between spaces in the element's text with tags removed (the page's own definition),
with two readings: the memo-text div as written, and the same with the <h5> headings removed.
"""
import html
import re
import sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "course/modules/E/E3/project.html"
src = open(PATH, encoding="utf-8").read()


def memo_texts(article_id: str) -> list[str]:
    start = src.index(f'<article class="exemplar" id="{article_id}"')
    end = src.index("</article>", start)
    block = src[start:end]
    return re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, flags=re.S)


def words(fragment: str) -> int:
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text)
    return len(text.split(" "))  # runs of characters between single spaces, as the page defines
    

for aid in ("exemplar-a", "exemplar-b"):
    parts = memo_texts(aid)
    total_with_headings = sum(words(p) for p in parts)
    total_split = sum(len(re.sub(r"<[^>]+>", " ", html.unescape(p)).split()) for p in parts)
    headings = sum(len(re.findall(r"<h5>(.*?)</h5>", p)) for p in parts)
    body_only = sum(len(re.sub(r"<[^>]+>", " ", html.unescape(re.sub(r"<h5>.*?</h5>", "", p, flags=re.S))).split()) for p in parts)
    print(aid, "memo parts:", len(parts), "| str.split with headings:", total_split,
          "| split-on-space with headings:", total_with_headings, "| h5 headings:", headings,
          "| body only (no headings):", body_only)
