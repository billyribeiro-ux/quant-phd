"""For every mutant in ledgers/FC2/mutants: the first docstring line, and whether it differs from reference.py.

Usage: python3 -I ledgers/FC2/scripts/FC2-d-r5/mutant_docstrings_r5.py <repo_root>
Also prints the number of lines that differ from reference.py (a mutant with zero differing lines would be the
reference itself, and a mutant with a differing line count over 1 is listed for review).
"""

import ast
import difflib
import glob
import os
import sys

root = sys.argv[1]
ref_path = os.path.join(root, "course", "modules", "FC", "FC2", "grader", "reference.py")
ref = open(ref_path, encoding="utf-8").read()
ref_doc = ast.get_docstring(ast.parse(ref))
for path in sorted(glob.glob(os.path.join(root, "ledgers", "FC2", "mutants", "*.py"))):
    text = open(path, encoding="utf-8").read()
    tree = ast.parse(text)
    doc = ast.get_docstring(tree) or ""
    first = doc.splitlines()[0] if doc else ""
    changed = [l for l in difflib.unified_diff(ref.splitlines(), text.splitlines(), lineterm="", n=0)
               if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    n_changed = sum(1 for l in changed if l.startswith("+"))
    flag = "" if (first and first != ref_doc.splitlines()[0] and n_changed >= 1) else "  <-- REVIEW"
    print(os.path.basename(path), "| changed lines:", n_changed, "| first doc line:", first[:110] + flag)
