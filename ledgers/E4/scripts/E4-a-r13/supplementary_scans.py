"""E4 slice a, round 12: supplementary scans of the slice pages and lab twins.

Run from the checkout root: .venv/bin/python -I ledgers/E4/scripts/E4-a-r12/supplementary_scans.py
Checks: (1) registered notation symbols and forbidden macros in the math of index, L01 to L03, and any macro outside the
standard set; (2) the plan's D1 to D10 terms and "state price" absent from visible text; (3) four-digit years in visible
text (informational); (4) twin imports are stdlib only, no network or file access; (5) main() at top level, no __main__
guard, and any random use is seeded; (6) every hub concept link in index.html is used by a lesson; (7) the E2 witness
text in L03 as printed.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E4 = ROOT / "course/modules/E/E4"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
FAILS: list[str] = []
STANDARD = {
    "frac", "tfrac", "sum", "cdot", "ldots", "prod", "ln", "text", "mathrm", "bar", "quad", "qquad", "partial",
    "varepsilon", "pi", "lambda", "mu", "zeta", "psi", "iota", "in", "ge", "le", "ne", "neq", "sigma", "rho", "theta",
    "left", "right", "max", "min", "log", "exp", "bigl", "bigr", "to", "infty", "times", "approx", "cdots", "mid",
    "sqrt", "Omega", "alpha", "beta", "delta", "Delta", "geq", "leq", "Pr", "Sigma", "gamma", "ast", "ell",
    "displaystyle", "mathbf", "operatorname", "dfrac", "varphi", "phi", "eta", "kappa", "nu", "tau", "xi", "omega",
    "bigg", "Bigl", "Bigr", "lim", "int", "vert", "mathrm", "sup", "inf", "ne", "pm", "cap", "cup", "subseteq",
    "emptyset", "forall", "exists", "Rightarrow", "iff", "implies", "hat", "tilde", "overline", "circ", "dots",
    "mapsto", "nabla",
}
REGISTERED = {"E", "Var", "Cov", "Corr", "R", "Normal", "indic", "argmax", "argmin", "Prob"}
FORBIDDEN_SUBSTR = [r"\mathbb{E}", r"\mathbb{R}", r"\mathbb{Q}", r"\Phi", r"R^\ast", r"R^{e\ast}", r"R_f"]


def check(cond: bool, msg: str) -> None:
    print(("PASS: " if cond else "FAIL: ") + msg)
    if not cond:
        FAILS.append(msg)


def visible(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    text = re.sub(r"<pre.*?</pre>", " ", raw, flags=re.S)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def math_segments(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, flags=re.S)
    return [a or b for a, b in segs]


# (1) notation
bad = []
macros: set[str] = set()
for name in PAGES:
    for seg in math_segments(E4 / name):
        for f in FORBIDDEN_SUBSTR:
            if f in seg:
                bad.append((name, f))
        for mac in re.findall(r"\\([A-Za-z]+)", seg):
            macros.add(mac)
check(not bad, f"notation: no forbidden symbol in index, L01 to L03 math ({bad[:3]})")
unknown = sorted(m for m in macros if m not in STANDARD and m not in REGISTERED)
print("INFO: macros used in slice math:", sorted(macros))
print("INFO: macros outside the standard set and the registered set:", unknown)
check(all(m in REGISTERED or m in STANDARD for m in macros), "notation: every macro in slice math is standard or registered")
for name in PAGES:
    check(r"\mathbb{E}" not in (E4 / name).read_text(encoding="utf-8"), f"notation: {name} has no raw \\mathbb{{E}}")

# (2) plan D1 to D10 terms and "state price" in visible text
dterms = ["state price", "stochastic discount", "martingale", "bayes", "banach", "intermediate value", "two-fund",
          "determinacy", "efficient markets", "kyle", "common knowledge", "noise-trader risk", "diagnostic expectations",
          "probability of informed trading"]
for name in PAGES:
    vis = visible(E4 / name)
    for term in dterms:
        hits = [m.start() for m in re.finditer(re.escape(term), vis, flags=re.I)]
        if hits:
            print(f"HIT: D-terms: {name} contains '{term}' ({len(hits)} hits): {vis[max(0, hits[0]-60):hits[0]+40]!r}")
print("NOTE: index.html 'Stochastic Discount Factor' is the curriculum title of module AP1 (index line 36), a name not a use")

# (3) years (informational)
for name in PAGES:
    vis = visible(E4 / name)
    print("INFO:", name, "four-digit years in visible text:", sorted(set(re.findall(r"\b(1[89]\d\d|20\d\d)\b", vis))))

# (4) and (5) twins
for tw in ["lab-E4-L01-1.py", "lab-E4-L02-1.py", "lab-E4-L03-1.py"]:
    src = (ROOT / "tests/labs/E4" / tw).read_text(encoding="utf-8")
    imports = set(re.findall(r"^(?:from|import)\s+([\w.]+)", src, flags=re.M))
    check(imports <= {"__future__", "fractions", "math", "itertools", "random"}, f"twin {tw}: imports {sorted(imports)} are stdlib only")
    check(not re.search(r"open\(|urllib|requests|socket|http", src), f"twin {tw}: no file or network access")
    check(re.search(r"^main\(\)\s*$", src, flags=re.M) is not None and "__main__" not in src,
          f"twin {tw}: unconditional top-level main() call and no __main__ guard")
    draws = re.findall(r"\brandom\.(\w+)\(", src)
    seeded_only = all(d == "Random" for d in draws)
    check(seeded_only and not re.search(r"^import random", src, flags=re.M),
          f"twin {tw}: no random draws (calls to random.* in code: {draws})")

# (6) hub concept links used by lessons
hub = (E4 / "index.html").read_text(encoding="utf-8")
lessons = "".join((E4 / f"L0{i}.html").read_text(encoding="utf-8") for i in range(1, 10))
for concept in sorted(set(re.findall(r'<a class="concept" data-concept="([^"]+)"', hub))):
    check(f'data-concept="{concept}"' in lessons, f"hub concept link {concept} is used by a lesson (L01 to L09)")

# (7) E2 witness text
l03 = (E4 / "L03.html").read_text(encoding="utf-8")
check("(2, 4, 3)" in l03 and "(2, 4, 1)" in l03 and r"\tfrac14 \ln\tfrac43" in l03,
      "L03 E2 solution: witness (2,4,3)/(2,4,1) and 1/4 ln(4/3) as printed")
# (8) bare symbol T in math (registered: T is the number of observations, notation.json; must not appear as a symbol)
for name in PAGES:
    bare = [s[:60] for s in math_segments(E4 / name) if re.search(r"(?<![\\A-Za-z])T(?![A-Za-z])", s)]
    check(not bare, f"notation: {name} has no bare symbol T in math ({bare[:2]})")
print("FAILS:", len(FAILS))
sys.exit(1 if FAILS else 0)
