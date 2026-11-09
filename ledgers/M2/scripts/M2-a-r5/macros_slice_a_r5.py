"""Round-4 slice a: list every TeX macro used in index.html and L01-L06 (math only), against notation.json macros."""
import collections
import json
import re
import sys

root = sys.argv[1]
nt = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
print("about:", nt["about"])
registered = set(nt["macros"])
pages = ["index.html"] + [f"L0{i}.html" for i in range(1, 7)]
used = collections.Counter()
mathbb = []
for p in pages:
    text = open(f"{root}/course/modules/M/M2/{p}", encoding="utf-8").read()
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S):
        tex = m.group(1) or m.group(2) or ""
        for cmd in re.findall(r"\\[A-Za-z]+", tex):
            used[cmd] += 1
        if "\\mathbb" in tex:
            mathbb.append((p, tex[:80]))
print("macros used (math only):")
for cmd, n in sorted(used.items(), key=lambda kv: -kv[1]):
    flag = "" if cmd in registered or cmd in {"\\frac", "\\dfrac", "\\tfrac", "\\cdot", "\\ne", "\\le", "\\ge", "\\lim", "\\to", "\\min", "\\max", "\\sqrt", "\\left", "\\right", "\\bigl", "\\bigr", "\\varepsilon", "\\delta", "\\epsilon", "\\dots", "\\ldots", "\\cdots", "\\mathrm", "\\ln", "\\exp", "\\sin", "\\cos", "\\infty", "\\in", "\\subset", "\\circ", "\\mapsto", "\\lfloor", "\\rfloor", "\\text", "\\quad", "\\qquad", "\\ ", "\\,", "\\blacksquare", "\\sum", "\\prod", "\\int", "\\partial", "\\mid", "\\operatorname", "\\overline", "\\left", "\\bigr", "\\ge", "\\neq", "\\xi", "\\eta", "\\alpha", "\\beta", "\\gamma", "\\sigma", "\\mu", "\\pm", "\\times", "\\colon", "\\frac", "\\cdot", "\\varphi", "\\phi", "\\Delta", "\\tfrac", "\\cdots", "\\emptyset", "\\cup", "\\cap", "\\setminus", "\\Rightarrow", "\\iff", "\\forall", "\\exists", "\\neg", "\\lor", "\\land", "\\to", "\\displaystyle", "\\limits", "\\begin", "\\end"} else "  <-- check"
    print(f"  {cmd:14s} {n:5d}{flag}")
print("mathbb uses in slice:", mathbb)
print("registered macros:", sorted(registered))
