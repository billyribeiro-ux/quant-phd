"""Blind-scoring helper: writes project.html with official exemplar annotations removed.

Removes every <aside> block and every <ul> block inside an <article class="exemplar">, every
<li class="meets|misses"> line, every data-score/data-level/data-verdict attribute, and HTML
comments. The output is the exemplar passage text plus the rubric table only.
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
text = re.sub(r'\s(data-(score|level|verdict|annotation|official)[a-z-]*)="[^"]*"', "", text)
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)


def strip_exemplar(match: re.Match[str]) -> str:
    body = match.group(0)
    body = re.sub(r"<aside.*?</aside>", "", body, flags=re.S)
    body = re.sub(r"<ul>.*?</ul>", "", body, flags=re.S)
    body = re.sub(r"<li class=\"(meets|misses)\".*?</li>", "", body, flags=re.S)
    return body


text = re.sub(r"<article class=\"exemplar\".*?</article>", strip_exemplar, text, flags=re.S)
out = []
for line in text.splitlines():
    if re.search(r"(?i)\b(verdict|official|annotat\w*|score[sd]? (?:is|are|=))", line):
        continue
    if re.search(r'class="(meets|misses)"', line):
        continue
    out.append(line)
open(dst, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out), "lines written")
