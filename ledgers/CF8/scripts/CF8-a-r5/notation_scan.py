import json, re, sys, collections
root = sys.argv[1]
files = ["course/modules/CF/CF8/index.html", "course/modules/CF/CF8/L01.html", "course/modules/CF/CF8/L02.html",
         "tests/labs/CF8/lab-CF8-L01-1.py", "tests/labs/CF8/lab-CF8-L02-1.py"]
reg = json.load(open(f"{root}/notation/notation.json"))
macros = set(reg["macros"])
used = collections.Counter()
for f in files:
    txt = open(f"{root}/{f}", encoding="utf-8").read()
    for m in re.findall(r"\\[A-Za-z]+", txt):
        used[m] += 1
print("macros used not registered:", sorted(m for m in used if m not in macros and m not in {"\\mathrm","\\cdot","\\frac","\\qquad","\\ldots","\\blacksquare","\\operatorname","\\mathbb","\\mathbf","\\mathcal","\\Delta","\\text","\\left","\\right","\\,","\\sqrt","\\ast"}))
print("macros used (all):", sorted(used.items(), key=lambda x: -x[1])[:60])
hits = {}
pats = {"Phi": r"\\Phi", "gamma3/4": r"\\gamma_[34]", "R_f": r"R_f", "Q": r"\\mathbb\{Q\}", "R^ast": r"R\^\\ast", "Re_ast": r"R\^\{e\\ast\}", "T obs": r"(?<![A-Za-z\\])T(?![A-Za-z])"}
for f in files:
    txt = open(f"{root}/{f}", encoding="utf-8").read()
    for name, p in pats.items():
        for m in re.finditer(p, txt):
            ln = txt[:m.start()].count("\n") + 1
            hits.setdefault(name, []).append(f"{f}:{ln}")
for k, v in hits.items():
    print(k, len(v), v[:12])
