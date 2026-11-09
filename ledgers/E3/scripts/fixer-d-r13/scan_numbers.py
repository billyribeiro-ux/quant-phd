"""Scan: Lab 3 prize range and prize counts, exemplar word counts, and the mixed-pair count."""
import ast
import re
import sys
from fractions import Fraction
from html import unescape
from pathlib import Path

PAGE = Path("/Users/billyribeiro/dev/quant-phd/course/modules/E/E3/project.html")
text = PAGE.read_text(encoding="utf-8")
m = re.search(r"<pre><code class=\"language-python\" data-run>(\"\"\"Rung 3 reference case.*?)</code></pre>", text, re.S)
src = unescape(m.group(1))
tree = ast.parse(src)
answers = None
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "ANSWERS":
        answers = ast.literal_eval(node.value)
prizes = [x for a in answers for x in (a[2] + a[4])]
print("prize min/max", min(prizes), max(prizes))
print("prize counts per lottery", sorted({len(a[2]) for a in answers} | {len(a[4]) for a in answers}))
print("per-lottery prize counts", [(a[0], len(a[2]), len(a[4])) for a in answers])
def mixed(pr, pb):
    g = any(x > 0 and Fraction(p) > 0 for x, p in zip(pr, pb))
    l = any(x < 0 and Fraction(p) > 0 for x, p in zip(pr, pb))
    return g and l
print("mixed pairs", sum(1 for a in answers if mixed(a[2], a[3]) or mixed(a[4], a[5])))
print("pair 0 A", answers[0][2:4], "B", answers[0][4:6])
print("pair 3", answers[3])
print("pairs with 2 prizes in both", [a[0] for a in answers if len(a[2]) == 2 and len(a[4]) == 2])
# exemplar memo word counts: text of memo-text blocks with tags removed
def memo_words(article_id):
    art = re.search(r'<article class="exemplar" id="%s".*?</article>' % article_id, text, re.S).group(0)
    blocks = re.findall(r'<div class="memo-text">(.*?)</div>', art, re.S)
    plain = " ".join(re.sub(r"<[^>]+>", " ", unescape(b)) for b in blocks)
    return len(plain.split())
print("exemplar A memo words", memo_words("exemplar-a"))
print("exemplar B memo words", memo_words("exemplar-b"))
