"""Round-12 slice e static checks on the E3 project page, grader, lab twins and lessons (run from checkout root).
Banned strings (check_pages.py lines 58-73), process words (BUILDER_RULES / plan 2.2), notation macros used in math
against notation/notation.json, and internal links/anchors on project.html and index.html."""
import glob
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(".")
E3 = ROOT / "course/modules/E/E3"
files = sorted(glob.glob(str(E3 / "*.html"))) + sorted(glob.glob(str(E3 / "grader/*.py"))) + sorted(glob.glob(str(ROOT / "tests/labs/E3/*.py")))
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly"]
PROCESS = re.compile(r"\b(builder|verifier|REQUESTS?|unit report|round \d|round-\d|the build|we build)\b", re.I)
print("== banned strings and ellipsis outside code")
for f in files:
    text = open(f, encoding="utf-8").read()
    for b in BANNED:
        for m in re.finditer(re.escape(b), text, re.I):
            line = text.count("\n", 0, m.start()) + 1
            print(f"BANNED {b!r} {f}:{line}")
    for m in re.finditer(r"\.\.\.", text):
        line = text.count("\n", 0, m.start()) + 1
        ctx = text.splitlines()[line - 1].strip()
        print(f"ELLIPSIS {f}:{line}: {ctx[:110]}")
print("== process words (learner-visible text and code docstrings/comments)")
for f in files:
    for i, l in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
        if PROCESS.search(l):
            print(f"PROCESS {f}:{i}: {l.strip()[:140]}")
print("== macros used in E3 math vs notation/notation.json")
nj = json.load(open(ROOT / "notation/notation.json", encoding="utf-8"))
registered = set()
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and v.startswith("\\"):
                registered.add(v.split("{")[0].split(" ")[0])
            walk(v)
    elif isinstance(o, list):
        for x in o:
            walk(x)
walk(nj)
used = {}
for f in sorted(glob.glob(str(E3 / "*.html"))):
    for mm in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", open(f, encoding="utf-8").read(), re.S):
        body = mm.group(1) or mm.group(2) or ""
        for cmd in re.findall(r"\\[A-Za-z]+", body):
            used.setdefault(cmd, set()).add(Path(f).name)
print("macros used:", sorted(used))
print("notation.json top-level keys:", list(nj.keys())[:10])
