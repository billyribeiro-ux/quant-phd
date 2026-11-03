"""List every LaTeX control word used in the M3 pages and cards and flag those not registered in notation/notation.json."""
import glob
import json
import re
import sys

root = sys.argv[1]
reg = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
macros = set(reg["macros"].keys())
used: dict[str, set[str]] = {}
for path in sorted(glob.glob(f"{root}/course/modules/M/M3/*.html")) + [f"{root}/course/modules/M/M3/cards.json"]:
    name = path.rsplit("/", 1)[1]
    txt = open(path, encoding="utf-8").read()
    for m in re.findall(r"\\[A-Za-z]+", txt):
        used.setdefault(m, set()).add(name)
for m in sorted(used):
    flag = "REGISTERED" if m in macros else "NOT-REGISTERED"
    print(f"{m:16s} {flag:15s} {sorted(used[m])}")
print("registry macros:", sorted(macros))
