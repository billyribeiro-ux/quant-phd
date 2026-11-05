"""Round-10 verifier D: word counts of the two exemplars (project.html) and of the Summary of exemplar B.

A word is a run of non-space characters, per the page's own definition (project.html 'Length'). Math is counted as the text
between \\( and \\) tokens as one word each. Headings (h5) and paragraphs are counted separately."""

import html
import re
from pathlib import Path

PAGE = Path("/Users/billyribeiro/.fanout/wt/verifyD10-M4-d/course/modules/M/M4/project.html").read_text(encoding="utf-8")


def article(label: str) -> str:
    m = re.search(rf'<article class="exemplar" id="{label}".*?</article>', PAGE, re.S)
    return m.group(0)


def memo_parts(block: str):
    heads = re.findall(r"<h5>(.*?)</h5>", block, re.S)
    paras = re.findall(r'<div class="memo-text">(.*?)</div>', block, re.S)
    return heads, paras


def words(text: str) -> int:
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return len(text.split())


for label in ("exemplar-a", "exemplar-b"):
    block = article(label)
    heads, paras = memo_parts(block)
    body_words = sum(words(p) for p in paras)
    head_words = sum(words(h) for h in heads)
    print(f"{label}: headings {len(heads)} ({head_words} words); body paragraphs {len(paras)} ({body_words} words); "
          f"body + headings {body_words + head_words}")
    if label == "exemplar-b":
        summary = re.search(r"<h5>Summary</h5>\s*<p>(.*?)</p>", block, re.S).group(1)
        print("exemplar-b Summary words:", words(summary))
