"""M7-a round 1 witness: optimum-point superscripts on the slice pages vs the registered notation (notation/notation.json)."""
import json
import re
import sys

root = sys.argv[1]
reg = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
print("registered symbols:", [s["symbol"] for s in reg["symbols"]])
for s in reg["symbols"]:
    if "x^" in s["meaning"] or "x^\\ast" in s["meaning"]:
        print("registry text naming x^ast:", s["symbol"], "->", s["meaning"][:120])
ap1 = open(f"{root}/course/modules/AP/AP1/L04.html", encoding="utf-8").read()
print("AP1 L04 occurrences of x^\\ast:", len(re.findall(r"x\^\\ast", ap1)))
for f in ("index", "L01", "L02", "L03"):
    t = open(f"{root}/course/modules/M/M7/{f}.html", encoding="utf-8").read()
    print(f, "x^\\ast:", len(re.findall(r"x\^\\ast", t)), " x^* (plain):", len(re.findall(r"x\^\*", t)),
          " operatorname{diag}:", t.count("operatorname{diag}"), " registered \\diag used:", len(re.findall(r"\\diag\b", t)))
