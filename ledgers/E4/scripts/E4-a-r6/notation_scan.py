"""E4 slice a round 6: macros and symbols used on the hub and L01-L03 versus notation/notation.json.

Usage: python -I notation_scan.py <checkout-root>. Prints every macro used on the slice pages with its
registry status, the \\mathbb uses, and the symbol set per page (for a manual notation read).
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
notation = json.loads((root / "notation" / "notation.json").read_text(encoding="utf-8"))
macros = set(notation["macros"].keys())
pages = ["index.html", "L01.html", "L02.html", "L03.html"]
base = root / "course" / "modules" / "E" / "E4"
for name in pages:
    text = html.unescape((base / name).read_text(encoding="utf-8"))
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    body = " ".join(a or b for a, b in maths)
    used = sorted(set(re.findall(r"\\[A-Za-z]+", body)))
    unregistered = [m for m in used if m not in macros and m not in {"\\frac", "\\text", "\\mathrm", "\\cdot", "\\ldots",
                    "\\le", "\\ge", "\\ne", "\\sum", "\\qquad", "\\quad", "\\bigl", "\\bigr", "\\in", "\\ast",
                    "\\varepsilon", "\\lambda", "\\mu", "\\pi", "\\psi", "\\theta", "\\iota", "\\delta", "\\sigma",
                    "\\bar", "\\tfrac", "\\mathcal", "\\min", "\\max", "\\left", "\\right", "\\partial", "\\infty",
                    "\\cdots", "\\operatorname", "\\mathbf", "\\prime", "\\alpha", "\\beta", "\\zeta", "\\rho", "\\phi",
                    "\\subset", "\\exp", "\\ln", "\\log", "\\text", "\\neq", "\\to", "\\times", "\\geq", "\\leq",
                    "\\varsigma", "\\gamma", "\\nu", "\\tau", "\\eta", "\\omega", "\\kappa", "\\xi", "\\Omega",
                    "\\Sigma", "\\Gamma", "\\Theta", "\\Lambda", "\\approx", "\\sim", "\\dfrac", "\\mid", "\\{", "\\}",
                    "\\,", "\;", "\\!", "\\over", "\\displaystyle", "\\bigg", "\\Big", "\\big", "\\cap", "\\cup",
                    "\\in", "\\notin", "\\forall", "\\exists", "\\Rightarrow", "\\Leftrightarrow", "\\iff", "\\implies"}]
    print(f"{name}: macros used {used}")
    print(f"{name}: not in registry or standard set {unregistered}")
    print(f"{name}: \\mathbb occurrences {len(re.findall(r'mathbb', body))}")
    print(f"{name}: \\mathbb{{R}} in raw html {len(re.findall(r'mathbb\\{R\\}', text))}")
