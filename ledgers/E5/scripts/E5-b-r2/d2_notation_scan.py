"""Round 2 verifier notation scan (E5-b): every TeX symbol in L04-L06 prose math vs notation/notation.json.

Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r2/d2_notation_scan.py
"""
from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REGISTERED = {"T", r"\Phi", r"\gamma_3", r"\gamma_4", r"R^\ast", r"R^{e\ast}", "R_f", r"\mathbb{Q}", r"\E", r"\R",
              r"\Prob", r"\Var", r"\Cov", r"\Corr", r"\SR", r"\se", r"\tr", r"\diag", r"\indic", r"\Normal"}
nj = json.loads((ROOT / "notation/notation.json").read_text(encoding="utf-8"))
macro_names = set(nj["macros"].keys())
for p in ["L04", "L05", "L06"]:
    raw = (ROOT / f"course/modules/E/E5/{p}.html").read_text(encoding="utf-8")
    raw = re.sub(r'<pre><code class="language-python" data-run>.*?</code></pre>', " ", raw, flags=re.S)
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", raw, flags=re.S)
    segs = [a or b for a, b in maths]
    cnt = Counter()
    for seg in segs:
        for m in re.finditer(r"\\[A-Za-z]+|\\[{}]|[A-Za-z]+(?:_\{?\w+\}?)?(?:\^\{?\\?\w+\}?)?", seg):
            cnt[m.group(0)] += 1
    print(f"== {p}: {len(segs)} math segments")
    print("commands used:", sorted(k for k in cnt if k.startswith("\\")))
    hits = {k: v for k, v in cnt.items() if k in REGISTERED or k in ("T", "E", "Q", "R", "N", "Phi", "gamma")}
    print("registered or risky tokens:", hits)
    print("single-letter tokens:", sorted(k for k in cnt if len(k) == 1 and k.isalpha()))
    for seg in segs:
        if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", seg) or re.search(r"\\E\b|\\mathbb", seg):
            print("  T/E/mathbb in:", seg[:120])
print("macros registered:", sorted(macro_names)[:40])
