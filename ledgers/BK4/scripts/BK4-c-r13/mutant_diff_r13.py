"""Round-13 BK4-c: count the changed lines of every mutant against grader/reference.py (after the docstring).

A mutant that changes nothing executable would be equivalent (it must then be moved to ledgers/BK4/equivalent/).
Run: python3 -I ledgers/BK4/scripts/BK4-c-r13/mutant_diff_r13.py   (from the checkout root)
"""

import ast
import difflib
import glob
import os

ROOT = os.getcwd()
ref = open(os.path.join(ROOT, "course/modules/BK/BK4/grader/reference.py"), encoding="utf-8").read()


def code_lines(src):
    tree = ast.parse(src)
    body = tree.body[1:] if (tree.body and isinstance(tree.body[0], ast.Expr)) else tree.body
    return [ast.unparse(node) for node in body]


ref_code = code_lines(ref)
zero_diff = []
rows = []
for path in sorted(glob.glob(os.path.join(ROOT, "ledgers/BK4/mutants/*.py"))):
    src = open(path, encoding="utf-8").read()
    mut_code = code_lines(src)
    changed = [l for l in difflib.unified_diff(ref_code, mut_code, lineterm="", n=0)
               if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))]
    name = os.path.basename(path)
    rows.append((name, len(changed)))
    if not changed:
        zero_diff.append(name)
print("mutants:", len(rows), "| zero executable difference (equivalent candidates):", zero_diff)
for name, n in rows:
    if n != 2:
        print("changed-lines", n, name)
print("max changed lines:", max(n for _, n in rows), "| mutants with exactly one changed statement pair:", sum(1 for _, n in rows if n == 2))
