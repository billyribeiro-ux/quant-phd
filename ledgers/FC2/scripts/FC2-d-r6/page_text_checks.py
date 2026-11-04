"""Whole-page text checks for project.html: banned phrases, process words, P-labels, anchors, macros.

Usage: python3 -I page_text_checks.py <repo_root>
"""

import re
import sys

path = sys.argv[1] + "/course/modules/FC/FC2/project.html"
raw = open(path, encoding="utf-8").read()
lines = raw.splitlines()
banned = ["TODO", "TBD", "lorem", "...", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "well known", "obviously",
          "clearly", "historically", "roughly", "approximately", "let us"]
for word in banned:
    for n, line in enumerate(lines, 1):
        if word.lower() in line.lower():
            print("banned hit", word, "line", n)
for n, line in enumerate(lines, 1):
    if re.search(r"\b(we|our|us)\b", re.sub(r"<[^>]+>", " ", line), re.I):
        print("process/pronoun hit line", n, re.findall(r"\b(we|our|us)\b", line, re.I))
print("about-hits", [(n, m) for n, line in enumerate(lines, 1) for m in re.findall(r"about [0-9][^<]{0,30}", line)])
print("P6 label lines", [n for n, line in enumerate(lines, 1) if "P6 ·" in line])
print("macro commands", sorted(set(re.findall(r"\\[A-Za-z]+", raw))))
print("anchors exist", {a: f'id="{a}"' in raw for a in ["conventions", "exemplars", "rubric", "self-assessment"]})
print("line count", len(lines))
