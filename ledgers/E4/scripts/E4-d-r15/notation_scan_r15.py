"""Round-15 notation scan of the E4 project page (VERIFIER 2.4 item 13; notation/notation.json).

Lists every TeX control word used in the page's math, every \\mathbb / \\operatorname / \\mathcal form, and every
registered symbol or macro occurrence. Usage: python -I notation_scan_r15.py <page.html>
"""
import json
import re
import sys
from collections import Counter

page = open(sys.argv[1], encoding="utf-8").read()
nota = json.load(open("notation/notation.json", encoding="utf-8"))
macros = set(nota["macros"])
text = re.sub(r"<[^>]+>", " ", page)
maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, flags=re.S)
math_src = " ".join(a or b for a, b in maths)
ctrl = Counter(re.findall(r"\\[A-Za-z]+", math_src))
print("control words in math:", dict(sorted(ctrl.items(), key=lambda kv: -kv[1])))
print("registered macros used:", {m: ctrl[m] for m in macros if ctrl.get(m)})
print("unregistered macros used:", sorted(k for k in ctrl if k not in macros and k not in
      {"\\alpha","\\beta","\\gamma","\\delta","\\epsilon","\\varepsilon","\\lambda","\\sigma","\\tau","\\mu","\\nu","\\rho",
       "\\kappa","\\Omega","\\omega","\\pi","\\theta","\\Phi","\\phi","\\psi","\\Psi","\\xi","\\eta","\\chi","\\zeta",
       "\\frac","\\sqrt","\\exp","\\log","\\cdot","\\times","\\le","\\ge","\\neq","\\in","\\left","\\right","\\to","\\int",
       "\\sum","\\mid","\\,","\;","\\!","\\quad","\\text","\\begin","\\end","\\cases","\\operatorname","\\mathbb",
       "\\mathcal","\\hat","\\bar","\\ast","\\partial","\\Big","\\big","\\min","\\max","\\pm","\\infty","\\over",
       "\\displaystyle","\\overset","\\dots","\\ldots","\\pi"}))
print("mathbb uses:", re.findall(r"\\mathbb\{[^}]*\}", math_src)[:20])
print("operatorname uses:", sorted(set(re.findall(r"\\operatorname\{[^}]*\}", math_src))))
print("mathcal uses:", sorted(set(re.findall(r"\\mathcal\{[^}]*\}", math_src))))
print("bare capital T in math:", len(re.findall(r"(?<![A-Za-z\\])T(?![A-Za-z])", math_src)))
print("R^ast / x^ast / Phi / gamma_3 / gamma_4 / R_f / Q in math:",
      sum(math_src.count(s) for s in ["R^\\ast", "x^\\ast", "\\Phi", "\\gamma_3", "\\gamma_4", "R_f", "\\mathbb{Q}"]))
