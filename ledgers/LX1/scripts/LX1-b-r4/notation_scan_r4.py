"""Round-4 notation scan for L03 and L04 math segments against notation/notation.json. Usage: python -I notation_scan_r4.py <checkout>"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
print("registered symbols:", [s["symbol"] for s in reg["symbols"]])
print("registered macros:", sorted(reg["macros"]))
seg = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
bad = re.compile(r"(?<![A-Za-z])T(?![A-Za-z])|\\Phi|\\gamma|\\ast|R_f|R\^\{?e|\\mathbb\{Q\}|\\Prob|\\mathbb\{P\}|\\E\b|\\R\b|\\N\b")
for p in ("course/modules/LX/LX1/L03.html", "course/modules/LX/LX1/L04.html"):
    t = (root / p).read_text(encoding="utf-8")
    segs = [m.group(1) or m.group(2) for m in seg.finditer(t)]
    macros = sorted({m for s in segs for m in re.findall(r"\\[A-Za-z]+", s)})
    print(p, "math segments", len(segs), "hits", [s for s in segs if bad.search(s)])
    print("  macros used:", macros)
