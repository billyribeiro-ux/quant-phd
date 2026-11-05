"""Round 7: scan the E4 cards and lesson math for registry symbols (notation/notation.json) used with another meaning.

Registry symbols checked: T (number of observations), \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}.
Lesson math is read from the HTML \\( ... \\) and \\[ ... \\] spans; cards are read from cards.json text.
Usage: python -I notation_scan_r7.py <cards.json> <lesson html dir>
"""
import glob
import html
import json
import os
import re
import sys

cards_path, lesson_dir = sys.argv[1], sys.argv[2]
REG = [r"\bT\b", r"\\Phi", r"\\gamma_[34]", r"R\^\\ast", r"R\^\{e\\ast\}", r"R_f", r"\\mathbb\{Q\}"]
cards = json.load(open(cards_path, encoding="utf-8"))
print("cards: registry-symbol hits in front/back text")
for c in cards:
    body = c["front"] + " || " + c["back"]
    for pat in REG:
        for m in re.finditer(pat, body):
            lo = max(0, m.start() - 25)
            print(f"  {c['id']} {pat} ...{body[lo:m.end() + 25]}...")
print("lessons: registry-symbol hits inside TeX math spans")
spans = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
for path in sorted(glob.glob(os.path.join(lesson_dir, "L0*.html"))):
    src = open(path, encoding="utf-8").read()
    n = 0
    for m in spans.finditer(src):
        tex = m.group(1) or m.group(2) or ""
        for pat in REG:
            if re.search(pat, html.unescape(tex)):
                n += 1
                print(f"  {os.path.basename(path)} {pat} :: {tex[:90]}")
    print(f"  {os.path.basename(path)} math-span hits: {n}")
