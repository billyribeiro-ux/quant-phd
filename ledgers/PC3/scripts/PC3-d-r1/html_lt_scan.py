"""Flag raw '<' followed by a letter and then a math character (backslash, underscore, digit, parenthesis) in PC3 pages.

HTML5 reads '<' plus an ASCII letter as the start of a tag, so such text is swallowed by the browser.
Run from the checkout root: python3 -I ledgers/PC3/scripts/PC3-d-r1/html_lt_scan.py
"""
import glob
import re

pattern = re.compile(r"<(?!h[1-6][ >])[A-Za-z][\\_(0-9]")
hits = 0
for path in sorted(glob.glob("course/modules/PC/PC3/*.html")):
    for number, line in enumerate(open(path, encoding="utf-8"), 1):
        for m in pattern.finditer(line):
            hits += 1
            print(f"{path}:{number}: {line[m.start():m.start() + 24]!r}")
print(f"hits: {hits}")
