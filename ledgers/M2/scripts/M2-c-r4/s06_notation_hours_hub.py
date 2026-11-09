"""Notation-registry, hours, figure-markup and hub cross-reference checks for M2 slice c (round 4).

Run: .venv/bin/python -I <this file> <checkout root>.
"""
import json
import re
import sys

root = sys.argv[1]
pages = {p: open(f"{root}/course/modules/M/M2/{p}.html", encoding="utf-8").read() for p in ["L13", "L14", "L15", "L16", "L17", "L18"]}
reg = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
print("registry program-wide symbols:", [s["symbol"] for s in reg["symbols"]])
print("registry macros:", len(reg["macros"]))
for p, s in pages.items():
    hits = {k: len(re.findall(pat, s)) for k, pat in {
        "Phi": r"\\Phi", "gamma": r"\\gamma", "ast": r"\\ast", "mathbb": r"\\mathbb", "Q_bb": r"\\mathbb\{Q\}",
        "R_f": r"R_f", "R_e_star": r"R\^\{?e", "SR": r"\\SR"}.items()}
    print(p, "registry-symbol and mathbb hits:", hits)
    print(p, "data-hours:", re.findall(r'data-hours="(\d+)"', s), "data-files/data-chart/figure/svg:",
          len(re.findall(r'data-files|data-chart|<figure|<svg', s)))
idx = open(f"{root}/course/modules/M/M2/index.html", encoding="utf-8").read()
print("hub data-hours-lessons/project:", re.findall(r'data-hours-(?:lessons|project)="(\d+)"', idx))
print("hub L13..L18 card kickers:", re.findall(r'L1[3-8] · (\d+) h', idx))
for n in range(13, 19):
    print(f"lesson L{n} data-hours sum matches 10 h each:", re.findall(r'data-hours="(\d+)"', pages[f"L{n}"]) == ["10"])
s13 = pages["L13"]
print("L13 expansion lines (Taylor order two):", [s13.count("\n", 0, m.start()) + 1 for m in re.finditer(r"Taylor's theorem with the Lagrange remainder of order two", s13)],
      "subtraction line:", [s13.count("\n", 0, m.start()) + 1 for m in re.finditer(r"Subtract the second from the first", s13)])
print("L13 'second difference' or adding-the-expansions wording:", re.findall(r"second difference|add the two|adding the two|sum of the two expansions", s13, re.I))
m = re.search(r"Skill check \(rung 2\)[^<]*x\^4[^<]*", idx)
print("hub rung-2 item:", (m.group(0)[:160] if m else None))
m2 = re.search(r'<div class="explain" hidden><p>\\\(\(1\.1\)\^4[^<]*', idx)
print("hub rung-2 explanation:", (m2.group(0)[:260] if m2 else None))
print("arithmetic (1.1^4+0.9^4-2)/0.01 =", round(((1.1) ** 4 + (0.9) ** 4 - 2) / 0.01, 10))
