"""List the single-letter symbols in every inline math span of CF8 L03-L05, their line numbers, and any registry collision."""
import json
import re
import sys

ROOT = sys.argv[1]
reg = [s["symbol"] for s in json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))["symbols"]]
reg_letters = {"T", "Phi", "gamma", "R", "Q", "R_f"}
for lesson in ("L03", "L04", "L05"):
    lines = open(f"{ROOT}/course/modules/CF/CF8/{lesson}.html", encoding="utf-8").read().split("\n")
    seen: dict[str, set[int]] = {}
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"\\\((.*?)\\\)", line, re.S):
            body = re.sub(r"\\[A-Za-z]+", "", m.group(1))
            for sym in re.findall(r"(?<![A-Za-z])([A-Za-z])(?![A-Za-z])", body):
                seen.setdefault(sym, set()).add(i)
    print(lesson, {k: sorted(v)[:6] for k, v in sorted(seen.items())})
    print(lesson, "registry symbols (raw):", reg)
    print(lesson, "collisions with registered single letters:", sorted(set(seen) & reg_letters))
