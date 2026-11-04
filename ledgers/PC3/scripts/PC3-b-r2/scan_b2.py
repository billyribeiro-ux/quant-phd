"""Round 2 whole-page scan for PC3-b: banned strings, process words, scope words, macros, symbols, and tag balance.
Lab code and lab output blocks are excluded from prose scans. Usage: .venv/bin/python -I scan_b2.py <checkout>"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1])
pages = ["L04", "L05", "L06"]
BANNED = [
    r"\bTODO\b", r"\bTBD\b", r"\blorem\b", r"for brevity", r"details omitted", r"beyond the scope",
    r"left as an exercise", r"you can add more", r"it is important to note", r"studies show", r"experts agree",
    r"it is well known", r"\bobviously\b", r"\bclearly\b", r"\.\.\.",
]
PROCESS = [r"\bbuild", r"\bbuilder", r"\bround\b", r"\bverifier", r"REQUESTS", r"unit report"]
SCOPE = r"\b(every|all|always|any|only|same|exactly|drives|never|none)\b"
MACRO_OK = {"E", "Prob", "Var", "Cov", "Corr", "R", "N", "indic", "Normal", "se", "argmax", "argmin", "tr", "diag"}


class Balance(HTMLParser):
    VOID = {"meta", "link", "br", "img", "input", "hr", "col", "source"}

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.errors.append(f"stray </{tag}> at {self.getpos()}")
            return
        top, pos = self.stack[-1]
        if top == tag:
            self.stack.pop()
        else:
            self.errors.append(f"</{tag}> at {self.getpos()} closes open <{top}> from {pos}")
            # pop until matching tag if present
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break


for page in pages:
    path = root / f"course/modules/PC/PC3/{page}.html"
    text = path.read_text(encoding="utf-8")
    # strip lab code and expected blocks
    prose = re.sub(r'<pre class="expected".*?</pre>', "", text, flags=re.S)
    prose = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', "", prose, flags=re.S)
    prose = re.sub(r"<script.*?</script>", "", prose, flags=re.S)
    print(f"== {page}: lines={text.count(chr(10)) + 1}")
    for lineno, line in enumerate(prose.splitlines(), 1):
        for pat in BANNED + PROCESS:
            if re.search(pat, line, flags=re.I if pat in (r"\bround\b",) else 0):
                print(f"  BANNED/PROCESS {pat!r} line {lineno}: {line.strip()[:160]}")
    scope_hits = []
    for lineno, line in enumerate(prose.splitlines(), 1):
        for m in re.finditer(SCOPE, re.sub(r"<[^>]+>", " ", line), flags=re.I):
            scope_hits.append((lineno, m.group(0)))
    print(f"  scope-word hits (prose): {len(scope_hits)}")
    for lineno, w in scope_hits:
        print(f"    line {lineno}: {w}")
    macros = set(re.findall(r"\\([A-Za-z]+)", prose))
    print("  macros used in prose:", sorted(macros))
    bad = [m for m in macros if m not in MACRO_OK and m not in {
        "frac", "sum", "prod", "cdot", "dots", "ldots", "le", "ge", "lt", "gt", "ne", "left", "right", "bigl", "bigr",
        "Bigl", "Bigr", "operatorname", "tfrac", "lvert", "rvert", "ln", "max", "min", "text", "mathrm", "varepsilon",
        "sqrt", "ast", "bar", "partial", "in", "pm", "times", "approx", "to", "quad", "lbrace", "rbrace", "mid",
        "geq", "leq", "Var", "E", "exp", "log", "sigma", "mu", "alpha", "beta", "gamma", "lambda", "tau", "Delta",
        "dfrac", "displaystyle", "Big", "big", "Bigg", "not", "neq", "infty", "cdots", "vdots", "dagger", "ddots",
        "square", "hat", "mathbb", "mathbf", "mathit", "emph", "textbf", "quad", "qquad", "sim", "equiv", "mathcal",
        "lvert", "rVert", "lVert", "rvert", "lbrack", "rbrack", "lfloor", "rfloor", "to", "ell", "pi", "theta",
        "omega", "rho", "nu", "kappa", "phi", "varphi", "Phi", "eta", "xi", "Pi", "Sigma", "Omega", "delta",
        "epsilon", "zeta", "chi", "psi", "iota", "vartheta", "varsigma", "Lambda", "Gamma", "Theta", "Psi"}]
    print("  macros not in KaTeX-standard or registry set:", sorted(bad))
    parser = Balance()
    parser.feed(text)
    print(f"  tag balance errors: {len(parser.errors)}")
    for e in parser.errors[:20]:
        print("    ", e)
    print(f"  unclosed at EOF: {[t for t, _ in parser.stack][:10]}")
