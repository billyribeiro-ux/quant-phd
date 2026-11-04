# Round 4 verifier scan, SC1 slice b: LaTeX commands used in L04-L06 (page math and twins) against notation.json macros.
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
reg = json.load(open(ROOT / "notation/notation.json", encoding="utf-8"))
macros = set(reg["macros"].keys())
counts: collections.Counter[str] = collections.Counter()
for page in ("L04", "L05", "L06"):
    text = (ROOT / f"course/modules/SC/SC1/{page}.html").read_text(encoding="utf-8")
    math = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    flat = " ".join(a or b for a, b in math)
    cmds = re.findall(r"\\([A-Za-z]+)", flat)
    for c in cmds:
        counts[f"{page}:\\{c}"] += 1
print("registered macros:", sorted(macros))
used = sorted({k.split(":", 1)[1] for k in counts})
print("commands used in slice math:")
for c in used:
    print(" ", c, {p: counts[f"{p}:{c}"] for p in ("L04", "L05", "L06") if counts[f"{p}:{c}"]})
print("non-registered commands:", [c for c in used if c.lstrip("\\") not in {m.lstrip("\\") for m in macros}])
