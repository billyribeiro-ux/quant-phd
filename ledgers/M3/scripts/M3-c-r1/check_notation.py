# Lists every LaTeX macro used in L07-L09 (pages and lab twins) and checks it against notation/notation.json.
import json, re, sys
root = sys.argv[1]
reg = json.load(open(f"{root}/notation/notation.json"))
macros = set(reg["macros"].keys())
symbols = reg.get("symbols", {})
print("registry macros:", len(macros), "symbols keys:", list(symbols.keys())[:40] if isinstance(symbols, dict) else type(symbols))
used = {}
for L in ["L07", "L08", "L09"]:
    txt = open(f"{root}/course/modules/M/M3/{L}.html", encoding="utf-8").read()
    for m in re.findall(r"\\[A-Za-z]+", txt):
        used.setdefault(m, set()).add(L)
for m in sorted(used):
    flag = "REGISTERED" if m in macros else "not-registered"
    print(f"{m:14s} {flag:15s} {sorted(used[m])}")
