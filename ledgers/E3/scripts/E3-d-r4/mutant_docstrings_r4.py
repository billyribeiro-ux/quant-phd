"""Round-4 verifier (E3-d): every mutant under ledgers/E3/mutants has a first docstring line that names a student error,
is not a 'Reference' line, and the mutant parses. Also counts the mutant files."""
import ast
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
files = sorted((ROOT / "ledgers/E3/mutants").glob("*.py"))
bad = []
for f in files:
    tree = ast.parse(f.read_text(encoding="utf-8"))
    doc = ast.get_docstring(tree) or ""
    first = doc.splitlines()[0] if doc else ""
    if not first or first.lower().startswith(("reference", "single-change", "student-error")):
        bad.append((f.name, first[:80]))
print("mutant files:", len(files))
print("first-line problems:", bad if bad else "none")
