"""Verifier r8: checks that the function t3_tail_one_sided in L10.html's data-run code equals the twin, and the
docstring sentence matches. Standard library only. Run with -I from the checkout root."""
import html
import re
import sys

page = open("course/modules/M/M4/L10.html", encoding="utf-8").read()
twin = open("tests/labs/M4/lab-M4-L10-1.py", encoding="utf-8").read()
m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
code = html.unescape(m.group(1))
def body(src):
    i = src.index("def t3_tail_one_sided")
    j = src.index("\ndef ", i + 1)
    return src[i:j].strip()
print("page function == twin function:", body(code) == body(twin))
print("twin function sentence present in page:", "Both subtracted terms are near 1/y for large x" in html.unescape(page))
print("page-code length", len(code), "twin length", len(twin))
