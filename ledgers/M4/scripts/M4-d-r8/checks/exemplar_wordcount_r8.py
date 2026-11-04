"""Word counts behind the C5 annotations of Exemplars A and B (project.html), round 8, slice d.

A word is a run of characters between spaces (project.html line 326). Body = the memo-text paragraphs; headings counted
separately. Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/exemplar_wordcount_r8.py
"""

import html
import pathlib
import re

SRC = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d/course/modules/M/M4/project.html")
src = SRC.read_text(encoding="utf-8")


def txt(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


for ex in ["exemplar-a", "exemplar-b"]:
    start = src.index(f'id="{ex}"')
    end = src.index("</article>", start)
    block = src[start:end]
    memos = re.findall(r'<div class="memo-text">(.*?)</div>\s*<aside', block, re.S)
    heads, paras = [], []
    for m in memos:
        heads += [txt(h).strip() for h in re.findall(r"<h5>(.*?)</h5>", m, re.S)]
        paras += [txt(p).strip() for p in re.findall(r"<p>(.*?)</p>", m, re.S)]
    body = sum(len(p.split()) for p in paras)
    head = sum(len(h.split()) for h in heads)
    print(f"{ex}: passages {len(memos)} body words {body} with {len(heads)} headings {body + head}")
    if ex == "exemplar-b":
        first = [txt(p).strip() for p in re.findall(r"<p>(.*?)</p>", memos[0], re.S)]
        print(f"exemplar-b Summary words {sum(len(p.split()) for p in first)}")
print("annotation as printed:", re.findall(r"the body is (\d+) words of text \((\d+) with its four headings\)", src))
