"""Round-3 BK4-a notation scan: math on index, L01-L03 against notation/notation.json (registered symbols and macros).

Usage (repo root): python3 -I ledgers/BK4/scripts/BK4-a-r3/notation_scan_r3.py
Prints the registered symbols found in math (expected none), the commands used, and the single letters used.
"""

import collections
import html
import json
import re

nb = json.load(open("notation/notation.json", encoding="utf-8"))
registered = [s["symbol"] for s in nb["symbols"]]
macros = nb["macros"]
pages = [f"course/modules/BK/BK4/{p}.html" for p in ("index", "L01", "L02", "L03")]
chunks = []
for p in pages:
    t = open(p, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]|\$\$(.*?)\$\$", t, flags=re.S):
        c = next(g for g in m.groups() if g is not None)
        chunks.append((p, html.unescape(c)))
print("math chunks:", len(chunks))
hits = []
for p, c in chunks:
    for sym in ("\\Phi", "\\gamma", "\\ast", "\\mathbb", "R_f", "R^", "T", "\\Prob", "\\mathbb{R}"):
        if sym == "T":
            if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", c):
                hits.append((p, sym, c[:80]))
        elif sym in c:
            hits.append((p, sym, c[:80]))
print("registered-symbol or \\mathbb hits in math:", hits)
cmds = collections.Counter()
letters = collections.Counter()
for _, c in chunks:
    cmds.update(re.findall(r"\\[A-Za-z]+", c))
    stripped = re.sub(r"\\[A-Za-z]+", "", c)
    letters.update(re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", stripped))
print("commands:", sorted(cmds))
print("macros used that are registered:", sorted(m for m in cmds if m in macros))
print("single letters:", sorted(letters))
print("registered symbols:", registered)
