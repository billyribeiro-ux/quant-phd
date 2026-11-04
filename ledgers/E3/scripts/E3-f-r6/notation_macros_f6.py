"""Macro and registered-symbol check for E3 L01-L04 against notation/notation.json (verifier E3-f round 6)."""
import json, re, collections
reg = json.load(open("notation/notation.json", encoding="utf-8"))
macros = set(reg["macros"].keys())
symbols = [s["symbol"] for s in reg["symbols"]]
for L in ("L01", "L02", "L03", "L04"):
    src = open(f"course/modules/E/E3/{L}.html", encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, flags=re.S)
    toks = collections.Counter()
    for a, b in maths:
        for m in re.findall(r"\\[A-Za-z]+", a or b):
            toks[m] += 1
    custom = sorted(t for t in toks if t in macros)
    print(L, "registered macros used:", custom)
    print(L, "registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) appearing in math:",
          [s for s in ("\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}") if s in " ".join(a or b for a, b in maths)],
          " bare T in math:", [m for a, b in maths for m in re.findall(r"(?<![A-Za-z\\])T(?![A-Za-z])", a or b)][:3])
print("registry macros:", sorted(macros))
print("registry symbols:", symbols)
