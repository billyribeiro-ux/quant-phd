"""Word counts of the two exemplar memos on project.html (round 5 verifier, stdlib only).

Counts runs of characters between spaces (str.split) in each div.memo-text with tags removed, under several readings:
with headings (h5), without headings, and with the annotation aside included. Run: python3 -I v5_exemplar_words.py
"""
import re
import sys

PAGE = sys.argv[1] if len(sys.argv) > 1 else "course/modules/E/E3/project.html"
html = open(PAGE, encoding="utf-8").read()


def article(article_id: str) -> str:
    start = html.index(f'id="{article_id}"')
    end = html.index("</article>", start)
    return html[start:end]


def memo_blocks(chunk: str) -> list[str]:
    return re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', chunk, flags=re.S)


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s)


def no_headings(s: str) -> str:
    return re.sub(r"<h5>.*?</h5>", " ", s, flags=re.S)


for name in ("exemplar-a", "exemplar-b"):
    chunk = article(name)
    blocks = memo_blocks(chunk)
    with_h = " ".join(strip_tags(b) for b in blocks)
    without_h = " ".join(strip_tags(no_headings(b)) for b in blocks)
    print(name, "memo blocks:", len(blocks))
    print("  with headings (str.split):", len(with_h.split()))
    print("  without headings (str.split):", len(without_h.split()))
    # tags removed but without collapsing: split on literal single space
    print("  with headings, split(' ') non-empty:", len([t for t in with_h.split(" ") if t]))
    annot = re.findall(r'<aside class="annotation".*?</aside>', chunk, flags=re.S)
    print("  annotation text words (not memo):", len(" ".join(strip_tags(a) for a in annot).split()))
