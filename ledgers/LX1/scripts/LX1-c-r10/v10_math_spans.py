"""Round-10 verifier: lists every TeX span (\\( ... \\)) in project.html with its line number, and the program-wide
symbols registered in notation/notation.json, so each symbol on the page can be compared with the registry."""
import json, re, sys
root = sys.argv[1]
src = open(f"{root}/course/modules/LX/LX1/project.html", encoding="utf-8").read().split("\n")
spans = []
for i, line in enumerate(src, 1):
    for m in re.finditer(r"\\\((.+?)\\\)", line):
        spans.append((i, m.group(1)))
print("spans:", len(spans))
for i, s in spans:
    print(i, s)
nj = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
print("notation.json top-level keys:", list(nj.keys()) if isinstance(nj, dict) else type(nj))
