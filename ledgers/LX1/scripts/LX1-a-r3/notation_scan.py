"""Round-3 notation scan: every TeX macro and single-letter symbol in the slice's math, compared with notation/notation.json."""
import json
import re
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE3-LX1-a/"
pages = ["course/modules/LX/LX1/index.html", "course/modules/LX/LX1/L01.html", "course/modules/LX/LX1/L02.html",
         "tests/labs/LX1/lab-LX1-L01-1.py", "tests/labs/LX1/lab-LX1-L02-1.py"]
reg = json.load(open(ROOT + "notation/notation.json"))
registered = [s["symbol"] for s in reg["symbols"]]
print("registered:", registered)
macros_reg = reg.get("macros")
print("macros in registry:", json.dumps(macros_reg)[:600])
for p in pages:
    t = open(ROOT + p, encoding="utf-8").read()
    segs = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, re.S)
    math = " ".join(a or b for a, b in segs)
    cmds = sorted(set(re.findall(r"\\[A-Za-z]+", math)))
    letters = sorted(set(re.findall(r"(?<![A-Za-z\\])([A-Za-z])(?![A-Za-z])", math)))
    print(p, "\n  commands:", cmds, "\n  single letters:", letters)
    tcount = [m.start() for m in re.finditer(r"(?<![A-Za-z\\])T(?![A-Za-z])", math)]
    print("  bare T in math segments:", len(tcount))
    for m in re.finditer(r"(?<![A-Za-z\\])T(?![A-Za-z])", t):
        print("    ", t[:m.start()].count("\n") + 1, t[max(0, m.start()-60):m.start()+20].replace("\n", " ")[:120])
