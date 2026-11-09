"""Round-17 verifier: symbols used in project.html TeX spans, against notation/notation.json (collisions only)."""
import json
import re
import sys
import pathlib

root = pathlib.Path(sys.argv[1])
nt = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered = set()
for s in nt["symbols"]:
    for part in s["symbol"].split(","):
        registered.add(part.strip().replace("^\\ast", "").replace("^{e\\ast}", "").replace("^\\ast", ""))
src = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
maths = re.findall(r"\\\((.+?)\\\)", src, re.S) + re.findall(r"\\\[(.+?)\\\]", src, re.S)
used = set()
for m in maths:
    for tok in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\{?[A-Za-z0-9]+\}?)?", m):
        used.add(tok)
print("TeX spans:", len(maths))
print("symbols used:", sorted(used))
print("registered symbols:", sorted(registered))
print("collisions (used symbol that the registry defines with another meaning):", sorted(used & registered))
