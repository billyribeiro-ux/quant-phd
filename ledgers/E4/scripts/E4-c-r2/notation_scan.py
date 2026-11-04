"""E4-c round 2: scan L07-L09 math for macros outside the registry and for single-letter symbol reuse.

Usage: python -I notation_scan.py <checkout-root>
Prints every macro used in the three pages with its count, flags macros that are neither registered
(notation/notation.json macros) nor standard KaTeX/typesetting commands, and lists every occurrence of
the letters c, chi, varpi, gamma, D and b used as a bare symbol inside \\( ... \\) math spans.
"""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text())
registered = set(reg["macros"].keys())
STANDARD = {
    "frac", "dfrac", "tfrac", "sqrt", "left", "right", "bigl", "bigr", "Bigl", "Bigr", "bigg", "Bigg", "ln", "exp",
    "sigma", "varepsilon", "tau", "lambda", "kappa", "beta", "alpha", "theta", "rho", "eta", "chi", "varpi", "gamma",
    "bar", "ast", "tfrac", "cdot", "leq", "geq", "neq", "le", "ge", "ne", "in", "subseteq", "mathcal", "mathbf",
    "mathrm", "operatorname", "text", "quad", "qquad", "dfrac", "to", "infty", "lim", "sum", "int", "partial", "mid",
    "min", "max", "prod", "times", "pm", "approx", "sim", "overset", "xrightarrow", "bar", "widehat", "hat", "log",
    "Gamma", "Delta", "Sigma", "Omega", "pi", "mu", "nu", "delta", "epsilon", "omega", "phi", "psi", "xi", "zeta",
    "vartheta", "sigma", "ell", "dots", "ldots", "cdots", "sqrt", "tilde", "forall", "exists", "land", "lor", "neg",
    "left", "{", "}", ",", ";", "!", " ", "emph", "textbf", "bigm", "big", "Big", "vert", "lvert", "rvert", "lbrace",
    "rbrace", "langle", "rangle", "mathbb", "setminus", "cap", "cup", "emptyset", "varnothing", "Pr", "argmax",
    "argmin", "sup", "inf", "limsup", "liminf", "det", "sgn", "exp", "cos", "sin", "tan", "eqref", "label",
    "overline", "underline", "boldsymbol", "mathit", "hspace", "vspace", "displaystyle", "textstyle",
    "mathsf", "mathtt", "Re", "Im", "top", "perp", "propto", "equiv", "cong", "notin", "ni", "ni", "lfloor", "rfloor",
    "lceil", "rceil", "triangleq", "coloneqq", "eqqcolon", "Leftarrow", "Rightarrow", "implies", "iff", "leftrightarrow",
    "rightarrow", "leftarrow", "longrightarrow", "mapsto", "uparrow", "downarrow", "not", "vec", "dot", "ddot",
    "check", "breve", "acute", "grave", "mathring", "widetilde", "stackrel", "substack", "scriptstyle",
    "scriptscriptstyle", "quad", "smash", "phantom", "color", "class", "style", "dotsc", "dotsb", "dotsm",
    "mathop", "mathbin", "mathrel", "mathpunct", "mathord", "mathopen", "mathclose", "limits", "nolimits",
    "Vert", "lVert", "rVert", "lbrack", "rbrack", "{", "}", "|", "%", "&", "#", "\\", "_", "^", "$",
}
pages = ["course/modules/E/E4/L07.html", "course/modules/E/E4/L08.html", "course/modules/E/E4/L09.html"]
span = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
for p in pages:
    text = html.unescape((root / p).read_text())
    # keep only the math spans, drop <code> blocks (lab code is not math)
    text_nocode = re.sub(r"<pre.*?</pre>", "", text, flags=re.S)
    macros = Counter()
    bare = Counter()
    for m in span.finditer(text_nocode):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        for mac in re.findall(r"\\([A-Za-z]+|[^A-Za-z\s])", body):
            macros["\\" + mac] += 1
        for sym in re.findall(r"(?<![\\A-Za-z])(c|chi|varpi|gamma|D|b|Y|Z)(?![A-Za-z])", body):
            bare[sym] += 1
    unknown = sorted(k for k in macros if k.lstrip("\\") not in STANDARD and k not in registered)
    print(f"== {p}")
    print("macros:", dict(sorted(macros.items())))
    print("registered-or-standard check: unknown macros =", unknown)
    print("bare single-letter symbols inside math:", dict(sorted(bare.items())))
