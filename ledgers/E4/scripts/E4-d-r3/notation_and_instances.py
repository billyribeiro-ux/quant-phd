"""Notation scan of project.html math spans and the lab twins against notation/notation.json, plus the instance checks.

Usage: python3 -I ledgers/E4/scripts/E4-d-r3/notation_and_instances.py <repo-root>
Pure stdlib. Prints the macros used, the registered symbols found in the math, the 'T' occurrences in labs and the
instance generator's distinctness, determinism and ranges for seeds 0-49.
"""

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
html = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
spans = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", html, flags=re.S)
maths = [a or b for a, b in spans]
macros = Counter(c for m in maths for c in re.findall(r"\\([A-Za-z]+)", m))
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered_macros = set(reg["macros"])
used_registered = sorted(f"\\{c}" for c in macros if f"\\{c}" in registered_macros)
print("macros used in project.html math:", sorted(macros))
print("registered macros used:", used_registered)
print("macros used that are registered-looking but not registered:",
      sorted(f"\\{c}" for c in macros if f"\\{c}" not in registered_macros and c in {"Corr", "Cov", "Var", "E", "Normal", "Prob", "R", "N", "SR", "indic"}))
registered_symbols = [s["symbol"] for s in reg["symbols"]]
print("registered symbols:", registered_symbols)
hits = []
for m in maths:
    for pat in (r"(?<![A-Za-z\\])T(?![A-Za-z])", r"\\Phi", r"\\gamma", r"\\mathbb", r"R_f", r"R\^", r"(?<![A-Za-z\\])R(?![A-Za-z])", r"\\mathbb\{Q\}"):
        if re.search(pat, m):
            hits.append((pat, m[:80]))
print("registered-symbol hits in project.html math spans:", hits)
for n in (1, 2, 3):
    src = (root / f"tests/labs/E4/lab-E4-project-{n}.py").read_text(encoding="utf-8")
    print(f"lab-E4-project-{n}.py: standalone capital T tokens:", len(re.findall(r"(?<![A-Za-z_])T(?![A-Za-z_])", src)))
spec = importlib.util.spec_from_file_location("instance", root / "course/modules/E/E4/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)
xs = [inst.make_instance(s) for s in range(50)]
pairs = {(x["noise_sd"], x["info_cost"]) for x in xs}
print("instances seeds 0-49: distinct pairs", len(pairs))
print("noise_sd range", min(x["noise_sd"] for x in xs), max(x["noise_sd"] for x in xs))
print("info_cost range", min(x["info_cost"] for x in xs), max(x["info_cost"] for x in xs))
print("deterministic", all(inst.make_instance(s) == inst.make_instance(s) for s in range(50)))
