"""Notation scan for E1 slice a (hub and L01-L03): registry collisions, macros used, math letters used."""
import collections
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = [root / "course/modules/E/E1" / n for n in ("index.html", "L01.html", "L02.html", "L03.html")]
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
text = {p.name: p.read_text(encoding="utf-8") for p in pages}
collide = [s["symbol"] for s in reg["symbols"] if re.search(r"Phi|gamma|ast|mathbb\{Q\}|R_f|R\^\{e", s["symbol"])]
for name, t in text.items():
    cmds = collections.Counter(re.findall(r"\\[A-Za-z]+", t))
    unknown_reg = sorted(c for c in cmds if c.lstrip("\\") and ("\\" + c.lstrip("\\")) and c.lstrip("\\") in {m.lstrip("\\") for m in macros})
    print(name, "registered macros used:", unknown_reg)
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, flags=re.S)
    letters = collections.Counter()
    for a, b in maths:
        body = a or b
        body = re.sub(r"\\[A-Za-z]+", " ", body)
        letters.update(re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", body))
    print(name, "single-letter math symbols:", dict(sorted(letters.items())))
    for c in collide:
        hits = len(re.findall(re.escape(c), t))
        if hits:
            print(name, "REGISTRY SYMBOL HIT", c, hits)
    print(name, "T as math symbol:", len(re.findall(r"\\\([^)]*(?<![A-Za-z])T(?![A-Za-z])[^)]*\\\)", t)))
