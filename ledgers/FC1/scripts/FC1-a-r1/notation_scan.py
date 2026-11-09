"""Round-1 FC1-a notation scan: macros and reserved symbols used inside KaTeX math on the hub and L01-L03 pages."""

from __future__ import annotations

import html
import json
import pathlib
import re

ROOT = pathlib.Path(".").resolve()
FILES = ["index.html", "L01.html", "L02.html", "L03.html"]
reg = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
maths: list[tuple[str, str]] = []
for f in FILES:
    text = (ROOT / "course/modules/FC/FC1" / f).read_text(encoding="utf-8")
    text = html.unescape(text)
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        maths.append((f, body))
print("math segments:", len(maths))
cmds: dict[str, set[str]] = {}
for f, body in maths:
    for c in re.findall(r"\\([A-Za-z]+)", body):
        cmds.setdefault(c, set()).add(f)
print("distinct commands in math:", sorted(cmds))
reserved_hits = []
for f, body in maths:
    for pat, label in [
        (r"\\mathbb\{Q\}", "mathbb-Q"),
        (r"\\Phi", "Phi"),
        (r"\\gamma", "gamma"),
        (r"R\^\\ast|R\^\{e\\ast\}|\\ast", "ast"),
        (r"R_f|R_\{f\}", "R_f"),
        (r"(?<![A-Za-z\\])T(?![A-Za-z])", "T"),
        (r"(?<![A-Za-z\\])Q(?![A-Za-z])", "Q"),
        (r"\\mathbb\{R\}", "mathbb-R"),
        (r"\\SR|\\hSR|\\se\b|\\emgamma", "SR-se-emgamma"),
    ]:
        if re.search(pat, body):
            reserved_hits.append((f, label, body[:140]))
print("reserved-symbol hits:", len(reserved_hits))
for h in reserved_hits:
    print(" ", h)
unknown = {c for c in cmds if c not in macros and c not in {"frac", "cdot", "sum", "prod", "dots", "text", "mathbb", "mathcal", "mathrm", "operatorname", "ldots", "sqrt", "le", "ge", "ne", "in", "sim", "to", "left", "right", "quad", "qquad", "mathbf", "widehat", "overset", "xrightarrow", "bigl", "bigr", "log", "exp", "min", "max", "pm", "times", "ell", "Pr", "lim", "partial", "sigma", "mu", "rho", "varphi", "kappa", "lambda", "alpha", "beta", "pi", "delta", "theta", "tau", "varepsilon", "epsilon", "eta", "nu", "gamma", "phi", "omega", "Delta", "Sigma", "Phi", "Pi", "ast", "prime", "dfrac", "tfrac", "hat", "bar", "vert", "mid", "cdots", "mathsf", ",", "lbrace", "rbrace", "blacksquare", "approx", "neq", "geq", "leq", "infty", "cup", "cap", "subseteq", "forall", "exists", "lvert", "rvert", "vdots", "dot", "Big", "big", "langle", "rangle", "emptyset", "setminus", "in", "notin", "circ", "int", "limits", "mathit", "boldsymbol", "underbrace", "overline", "underline", "stackrel", "begin", "end", "cases", "ddot", "operatorname*", "color", "textbf", "tilde", "vec", "varnothing", "prec", "succ", "sim", "simeq", "equiv", "Rightarrow", "Leftarrow", "rightarrow", "leftarrow", "iff", "implies", "Leftrightarrow", "bullet", "star", "oplus", "otimes", "rceil", "lceil", "rfloor", "lfloor", "vee", "wedge", "neg", "lnot", "land", "lor", "angle", "triangle", "parallel", "perp", "mapsto", "hookrightarrow", "longrightarrow", "Longrightarrow", "not", "nabla", "top", "bot", "aleph", "hbar", "imath", "jmath", "ell", "wp", "Re", "Im", "arg", "deg", "det", "dim", "ker", "gcd", "sup", "inf", "liminf", "limsup", "cos", "sin", "tan", "cot", "sec", "csc", "arccos", "arcsin", "arctan", "cosh", "sinh", "tanh", "coth", "ln", "lg", "hom", "Pr", "quad", "space", ",", ";", ":", "!", " ", "{", "}", "[", "]", "(", ")", "|", "%", "&", "#", "$", "_", "^", "\\"}}
print("commands not in registry and not in the standard allow-list:", sorted(unknown))
for c in sorted(unknown):
    print("  ", c, sorted(cmds[c]))
