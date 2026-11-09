"""FC1-a round 4: banned phrases, process words, ellipses, external URLs, notation symbols and macros, on the slice pages and twins.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r4/slice_scan_r4.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path.cwd()
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
TWINS = ["tests/labs/FC1/lab-FC1-L01-1.py", "tests/labs/FC1/lab-FC1-L02-1.py", "tests/labs/FC1/lab-FC1-L03-1.py"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = ["builder", "verifier", "verification", "REQUESTS", "ledger", "unit report", "fixer", "round",
           "architect", "planner", "campaign"]
SCOPE = ["every", "all", "always", "never", "any", "across", "only", "exactly", "same", "drives"]
NOTATION_BAD = [r"\\mathbb", r"R_f", r"R_\{f\}", r"\\Phi", r"\\gamma_3", r"\\gamma_4", r"\\SR", r"\\emgamma",
                r"R\^\\ast", r"R\^\{e\\ast\}", r"\\mathbb\{Q\}"]
MACROS_OK = {r"\(", r"\["}
ellipsis = re.compile(r"\.\.\.|…")

for name in PAGES:
    raw = (ROOT / "course/modules/FC/FC1" / name).read_text(encoding="utf-8")
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    math = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, flags=re.S)
    math_src = " ".join(a or b for a, b in math)
    visible = html.unescape(re.sub(r"<pre class=\"expected\".*?</pre>|<code class=\"language-python\".*?</code>", " ", text, flags=re.S))
    visible = re.sub(r"<[^>]+>", " ", visible)
    low = visible.lower()
    hits = {p: low.count(p.lower()) for p in BANNED if p.lower() in low}
    proc = {p: len(re.findall(r"\b" + re.escape(p) + r"\b", visible, flags=re.I)) for p in PROCESS}
    proc = {k: v for k, v in proc.items() if v}
    scope = {p: len(re.findall(r"\b" + p + r"\b", visible, flags=re.I)) for p in SCOPE}
    ell = len(ellipsis.findall(visible))
    ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', raw)
    notation = {p: len(re.findall(p, math_src)) for p in NOTATION_BAD}
    notation = {k: v for k, v in notation.items() if v}
    single_T = re.findall(r"(?<![A-Za-z\\])T(?![A-Za-z])", math_src)
    print(f"{name}: banned={hits} process={proc} ellipses={ell} external={ext} notation_bad={notation} "
          f"math_segments={len(math)} bare_T_in_math={len(single_T)}")
    print(f"{name}: scope-word counts {scope}")
    print(f"{name}: why-it-matters words: ", end="")
    wim = re.search(r'<p class="why-it-matters">(.*?)</p>', raw, re.S)
    if wim:
        print(len(re.sub(r"<[^>]+>", " ", wim.group(1)).split()))
    else:
        print("none")

for t in TWINS:
    src = (ROOT / t).read_text(encoding="utf-8")
    low = src.lower()
    hits = {p: low.count(p.lower()) for p in BANNED if p.lower() in low}
    proc = {p: len(re.findall(r"\b" + re.escape(p) + r"\b", src, flags=re.I)) for p in PROCESS}
    proc = {k: v for k, v in proc.items() if v}
    print(f"{t}: banned={hits} process={proc} ellipses={len(ellipsis.findall(src))}")
