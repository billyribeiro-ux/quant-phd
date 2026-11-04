"""List every TeX control sequence used in the math of project.html and in the E3 grader docstrings, and compare with
notation/notation.json macros. Round 5. Standard library only. usage: python -I macros_r5.py <checkout-root>
"""

import json
import re
import sys

root = sys.argv[1]
page = open(f"{root}/course/modules/E/E3/project.html", encoding="utf-8").read()
maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", page, flags=re.S)
text = " ".join(a or b for a, b in maths)
seqs = sorted(set(re.findall(r"\\([A-Za-z]+)", text)))
reg = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
macros = set(reg["macros"].keys())
print("math spans:", len(maths))
print("control sequences used:", seqs)
print("registered macros (with backslash) used:", sorted(f"\\{s}" for s in seqs if f"\\{s}" in macros))
print("used but not registered:", sorted(f"\\{s}" for s in seqs if f"\\{s}" not in macros))
