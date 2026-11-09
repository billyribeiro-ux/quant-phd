"""Round 17 (BK4 slice c): banned-phrase, filler, process-word, concept-markup, registered-symbol and scope-word scan.
Usage: python -I banned_scan_r17.py <checkout-root>. Prints every hit with its line number."""
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1]) / "course/modules/BK/BK4"
FILES = [ROOT / "project.html", ROOT / "grader/test_project.py", ROOT / "grader/instance.py",
         ROOT / "grader/starter.py", ROOT / "grader/reference.py",
         pathlib.Path(sys.argv[1]) / "tests/labs/BK4/lab-BK4-project-1.py",
         pathlib.Path(sys.argv[1]) / "tests/labs/BK4/lab-BK4-project-2.py",
         pathlib.Path(sys.argv[1]) / "tests/labs/BK4/lab-BK4-project-3.py"]
BANNED = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "well known", "obviously",
          "clearly", "roughly", "historically", "it can be shown", "...", "\u2026"]
PROCESS = r"\b(round|verifier|builder|architect|ruling|fixer|ledger|mutant|agent|batch|slice)\b"
SCOPE = r"\b(every|all|any|always|never|only|exactly|same|drives|each)\b"
SYMBOLS = [r"\bT\b", r"\\Phi", r"gamma_[34]", r"R_f", r"R\^\\ast", r"\\mathbb\{Q\}"]
for f in FILES:
    lines = f.read_text(encoding="utf-8").splitlines()
    print(f"== {f.relative_to(pathlib.Path(sys.argv[1]))}: {len(lines)} lines")
    for n, line in enumerate(lines, 1):
        low = line.lower()
        for p in BANNED:
            if p.lower() in low:
                print(f"banned {p!r} line {n}: {line.strip()[:110]}")
        for m in re.finditer(PROCESS, line, re.I):
            print(f"process {m.group(0)!r} line {n}: {line.strip()[:110]}")
        for p in SYMBOLS:
            if re.search(p, line) and f.name == "project.html":
                print(f"registered symbol {p!r} line {n}: {line.strip()[:110]}")
        if "class=\"concept\"" in line or "<dfn" in line:
            print(f"concept/dfn markup line {n}: {line.strip()[:110]}")
    if f.name == "project.html":
        counts = {}
        for n, line in enumerate(lines, 1):
            for m in re.finditer(SCOPE, line, re.I):
                counts.setdefault(m.group(0).lower(), []).append(n)
        for w, ns in sorted(counts.items()):
            print(f"scope word {w!r}: {len(ns)} hits at lines {ns}")
print("scan done")
