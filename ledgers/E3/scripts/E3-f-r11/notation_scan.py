"""E3 slice f round 11: math macros used in L01-L04 against notation/notation.json. Run from the checkout root with python3 -I."""
import json
import re
from pathlib import Path

macros = set(json.loads(Path("notation/notation.json").read_text(encoding="utf-8"))["macros"].keys())
cmds = set()
for i in range(1, 5):
    t = Path(f"course/modules/E/E3/L0{i}.html").read_text(encoding="utf-8")
    for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S):
        cmds |= set(re.findall(r"\\[A-Za-z]+", a + b))
standard = {"\\frac", "\\tfrac", "\\dfrac", "\\sum", "\\prod", "\\int", "\\lim", "\\le", "\\ge", "\\ne", "\\cdot", "\\times",
            "\\sqrt", "\\ln", "\\exp", "\\min", "\\max", "\\text", "\\mathrm", "\\operatorname", "\\displaystyle", "\\quad",
            "\\qquad", "\\to", "\\infty", "\\underline", "\\overline", "\\in", "\\mathbb", "\\mathbf", "\\mathcal", "\\lfloor",
            "\\rfloor", "\\ldots", "\\dots", "\\big", "\\bigl", "\\bigr", "\\pm", "\\mapsto", "\\blacksquare", "\\tilde",
            "\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon", "\\varepsilon", "\\eta", "\\phi", "\\kappa", "\\omega",
            "\\pi", "\\sigma", "\\chi", "\\upsilon", "\\xi", "\\mu", "\\lambda", "\\rho"}
print("commands used in L01-L04 math:", sorted(cmds))
print("registered macros used:", sorted(cmds & macros))
print("standard KaTeX commands used (not custom macros):", sorted(cmds & standard))
print("other commands:", sorted(cmds - macros - standard))
print("registered macros never used:", sorted(macros - cmds))
