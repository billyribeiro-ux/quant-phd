"""Round-16 check: raw line diff of every mutant against grader/reference.py with docstring lines removed (comments kept).
Prints the file and its differing lines. Usage (from the checkout root): python -I ledgers/E4/scripts/E4-d-r16/raw_diff_r16.py"""
import ast
import difflib
import glob
from pathlib import Path


def without_docstrings(path: str) -> list[str]:
    src = Path(path).read_text(encoding="utf-8")
    lines = src.splitlines()
    tree = ast.parse(src)
    drop: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                drop.update(range(b[0].lineno, b[0].end_lineno + 1))
    return [line for n, line in enumerate(lines, 1) if n not in drop]


ref = without_docstrings("course/modules/E/E4/grader/reference.py")
for path in sorted(glob.glob("ledgers/E4/mutants/*.py")):
    d = [x for x in difflib.unified_diff(ref, without_docstrings(path), lineterm="", n=0)
         if x[:1] in "+-" and not x.startswith(("+++", "---"))]
    print(f"{Path(path).name} {len(d)}")
    for x in d:
        print("    " + x)
