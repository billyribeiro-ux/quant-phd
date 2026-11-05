"""Extract plain text per HTML source line for LX1 lessons (round 9 verifier, slice d).

Usage: python -I extract_text.py <lesson.html> > out.txt
Prints each source line as: <lineno>: <text with tags stripped, entities unescaped>.
Only real tags (<letter...>, </...>, <!...>) are stripped; a bare '<' in maths is kept.
Lines empty after stripping are skipped; <script> blocks are dropped.
"""
import html
import re
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read().split("\n")
in_script = False
for i, line in enumerate(src, 1):
    if "<script" in line:
        in_script = True
    if in_script:
        if "</script>" in line:
            in_script = False
        continue
    t = re.sub(r"<(?=[A-Za-z/!])[^>]*>", "", line)
    t = html.unescape(t).strip()
    if t:
        print(f"{i}: {t}")
