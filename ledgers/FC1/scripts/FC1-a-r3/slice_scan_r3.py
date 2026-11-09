"""FC1-a round 3 scans: math segments, notation, banned phrases, process words, scope words, word counts.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r3/slice_scan_r3.py
"""
import html
import json
import re
import sys
from collections import Counter

ROOT = "course/modules/FC/FC1/"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
TWINS = ["tests/labs/FC1/lab-FC1-L01-1.py", "tests/labs/FC1/lab-FC1-L02-1.py", "tests/labs/FC1/lab-FC1-L03-1.py"]
NOTATION = json.load(open("notation/notation.json"))
REGISTERED_MACROS = set(NOTATION["macros"])
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = ["builder", "verifier", "round", "REQUESTS", "unit report", "ledger", "planner", "architect", "fixer",
           "verification", "build plan", "Builder"]


def visible(src: str) -> str:
    src = re.sub(r"<script.*?</script>", " ", src, flags=re.S)
    src = re.sub(r"<style.*?</style>", " ", src, flags=re.S)
    src = re.sub(r"<pre.*?</pre>", " ", src, flags=re.S)
    src = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(src)


def math_segments(src: str) -> list[str]:
    segs = re.findall(r"\\\((.+?)\\\)", src, flags=re.S)
    segs += re.findall(r"\\\[(.+?)\\\]", src, flags=re.S)
    return [html.unescape(s) for s in segs]


out = []
for page in PAGES:
    src = open(ROOT + page, encoding="utf-8").read()
    segs = math_segments(src)
    out.append(f"== {page}: math segments {len(segs)}")
    macros = Counter()
    for s in segs:
        for m in re.findall(r"\\[A-Za-z]+", s):
            macros[m] += 1
    unregistered = sorted(m for m in macros if m not in REGISTERED_MACROS and m not in {
        "\\frac", "\\sum", "\\prod", "\\cdot", "\\text", "\\qquad", "\\quad", "\\,", "\\ge", "\\le", "\\ne", "\\dots",
        "\\ldots", "\\blacksquare", "\\left", "\\right", "\\min", "\\max", "\\operatorname", "\\mathrm", "\\mathbf",
        "\\overset", "\\sqrt", "\\times", "\\infty", "\\to", "\\in", "\\approx", "\\mathbb", "\\emptyset", "\\lim",
        "\\partial", "\\exp", "\\log", "\\ln", "\\sigma", "\\rho", "\\varphi", "\\lambda", "\\kappa", "\\ell", "\\mu",
        "\\gamma", "\\alpha", "\\beta", "\\delta", "\\tau", "\\pi", "\\epsilon", "\\Delta", "\\sim", "\\neq", "\\geq",
        "\\leq", "\\pm", "\\cdots", "\\cdot", "\\sum", "\\mathcal", "\\mathit", "\\begin", "\\end", "\\hline", "\\ge",
        "\\mid", "\\colon", "\;", "\\!", "\\:", "\\}", "\\{", "\\%", "\\&", "\\prime", "\\limits"})
    out.append(f"  macros used: {dict(macros)}")
    out.append(f"  unregistered macros (outside the explicit ordinary list): {unregistered}")
    raw_mathbb = [s for s in segs if "\\mathbb" in s]
    out.append(f"  \\mathbb in math: {len(raw_mathbb)} {raw_mathbb[:5]}")
    # notation symbols: T, Q, R_f, R^\ast, Phi, gamma_3, gamma_4
    flags = []
    for s in segs:
        if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", s):
            flags.append(("T", s[:120]))
        if re.search(r"(?<![A-Za-z\\])Q(?![A-Za-z])", s):
            flags.append(("Q", s[:120]))
        if "R_f" in s or "R_{f}" in s or "R^\\ast" in s or "Phi" in s or "gamma_3" in s or "gamma_4" in s:
            flags.append(("registered-other", s[:120]))
        if "\\SR" in s or "\\hSR" in s or "\\se" in s or "\\emgamma" in s:
            flags.append(("registered-macro", s[:120]))
    out.append(f"  notation flags: {flags}")
    txt = visible(src)
    low = txt.lower()
    banned_hits = [(b, low.count(b.lower())) for b in BANNED if b.lower() in low]
    out.append(f"  banned hits: {banned_hits}")
    proc = [(p, len(re.findall(re.escape(p), txt))) for p in PROCESS if re.search(re.escape(p), txt)]
    out.append(f"  process-word hits (visible text, case-sensitive list): {proc}")
    ell = re.findall(r".{0,30}\.\.\..{0,30}", txt)
    out.append(f"  ellipses in visible text: {len(ell)} {ell[:4]}")
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', src, flags=re.S)
    if wim:
        words = len(visible(wim.group(1)).split())
        out.append(f"  why-it-matters words: {words} (limit 120)")
    ext = re.findall(r'(?:src|href)="(https?:[^"]+)"', src)
    out.append(f"  external URLs: {ext}")
    out.append(f"  <img>/<svg>/<iframe>/data-chart/data-files/assets/data: "
               f"{len(re.findall(r'<img|<svg|<iframe', src))} {src.count('data-chart')} {src.count('data-files')} {src.count('assets/data')}")
    scope = Counter()
    for w in ["every", "all", "always", "never", "any", "across", "drives", "only", "exactly", "same", "none"]:
        scope[w] = len(re.findall(r"\b" + w + r"\b", txt, flags=re.I))
    out.append(f"  scope words: {dict(scope)}")

for t in TWINS:
    src = open(t, encoding="utf-8").read()
    out.append(f"== {t}: lines {src.count(chr(10)) + 1}")
    proc = [p for p in PROCESS if re.search(re.escape(p), src)]
    out.append(f"  process words in twin: {proc}")
    out.append(f"  ellipsis in twin: {len(re.findall(r'\\.\\.\\.', src))}")

print("\n".join(out))
