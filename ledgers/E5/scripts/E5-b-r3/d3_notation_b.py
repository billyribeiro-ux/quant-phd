"""Round 3 verifier: TeX commands in the L04-L06 math segments versus notation/notation.json.

Lists every backslash command in \\( ... \\) and \\[ ... \\] segments, flags any registered macro (notation.json macros)
or any token from the registered symbols used in the lessons, and lists single-letter symbols that the registry defines.
Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r3/d3_notation_b.py
"""

from __future__ import annotations

import collections
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E5 = ROOT / "course" / "modules" / "E" / "E5"
nt = json.loads((ROOT / "notation" / "notation.json").read_text(encoding="utf-8"))
macros = set(nt["macros"].keys())
symbols = [s["symbol"] for s in nt["symbols"]]
cmds: collections.Counter[str] = collections.Counter()
used_macros = []
for p in ("L04", "L05", "L06"):
    s = (E5 / f"{p}.html").read_text(encoding="utf-8")
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S)
    flat = " ".join(html.unescape(a or b) for a, b in segs)
    found = re.findall(r"\\[A-Za-z]+", flat)
    cmds.update(c[1:] for c in found)
    used_macros += [m for m in macros if re.search(re.escape(m) + r"(?![A-Za-z])", flat)]
    print(p, "math segments:", len(segs))
print("commands:", dict(cmds.most_common()))
print("registered macros used:", sorted(set(used_macros)))
print("registered symbols (notation.json):", symbols)
for sym in ("T", "\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\mathbb{R}"):
    hits = []
    for p in ("L04", "L05", "L06"):
        s = (E5 / f"{p}.html").read_text(encoding="utf-8")
        if sym in s:
            hits.append(p)
    print("symbol", sym, "in pages:", hits)

# bare letter T used as a symbol inside math segments (the registry symbol T is the number of observations)
for p in ("L04", "L05", "L06"):
    s = (E5 / f"{p}.html").read_text(encoding="utf-8")
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, re.S)
    flat = " ".join(html.unescape(a or b) for a, b in segs)
    print("bare T in math", p, len(re.findall(r"(?<![A-Za-z\\])T(?![A-Za-z])", flat)))
