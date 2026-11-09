"""Round 19 (E4-d): profile every mutant against grader/reference.py at the AST level.
For each mutant: the names of top-level functions/constants whose source differs from the reference, and the number
of differing lines outside the module docstring. Prints a summary (counts of mutants by number of differing units)."""
import ast
import collections
import difflib
import glob
import os

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE19-E4-d"
REF = f"{ROOT}/course/modules/E/E4/grader/reference.py"


def units(src: str) -> dict[str, str]:
    tree = ast.parse(src)
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Constant):
            continue  # module docstring
        name = getattr(node, "name", None)
        if name is None and isinstance(node, (ast.Assign, ast.AnnAssign)):
            tgt = node.targets[0] if isinstance(node, ast.Assign) else node.target
            name = getattr(tgt, "id", None)
        if name is None and isinstance(node, (ast.Import, ast.ImportFrom)):
            name = "import:" + ast.unparse(node)
        if name is None:
            name = type(node).__name__ + ":" + ast.unparse(node)[:60]
        for sub in ast.walk(node):
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and sub.body:
                first = sub.body[0]
                if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) and isinstance(first.value.value, str):
                    sub.body = sub.body[1:] or [ast.Pass()]
        out[name] = ast.unparse(node)
    return out


ref_src = open(REF, encoding="utf-8").read()
ref_units = units(ref_src)
counts = collections.Counter()
rows = []
for path in sorted(glob.glob(f"{ROOT}/ledgers/E4/mutants/*.py")):
    src = open(path, encoding="utf-8").read()
    mu = units(src)
    changed = sorted(k for k in set(ref_units) | set(mu) if ref_units.get(k) != mu.get(k))
    body_diff = [l for l in difflib.unified_diff(ref_src.splitlines(), src.splitlines(), lineterm="", n=0)
                 if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    counts[len(changed)] += 1
    rows.append((os.path.basename(path), len(changed), changed, len(body_diff)))
for name, n, changed, nd in rows:
    if n != 1:
        print(f"{name}: units changed {n} {changed} diff_lines {nd}")
print("code-only (docstrings stripped) profile; the units listed are the ones whose code differs")
print("histogram of changed top-level units per mutant:", dict(sorted(counts.items())))
print("mutants:", len(rows))
