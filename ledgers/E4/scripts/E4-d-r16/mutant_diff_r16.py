"""Round-16 fixer check: for every file in ledgers/E4/mutants/, compare the code (docstrings and comments removed,
normalised by ast) with grader/reference.py and print the differing lines. Usage (from the checkout root):
python -I ledgers/E4/scripts/E4-d-r16/mutant_diff_r16.py [--cap-only]"""
import ast
import difflib
import glob
import sys
from pathlib import Path


def normalised(path: str) -> list[str]:
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return ast.unparse(tree).splitlines()


ref = normalised("course/modules/E/E4/grader/reference.py")
cap_only = "--cap-only" in sys.argv
for path in sorted(glob.glob("ledgers/E4/mutants/*.py")):
    diff = [d for d in difflib.unified_diff(ref, normalised(path), lineterm="", n=0)
            if (d.startswith("+") or d.startswith("-")) and not d.startswith(("+++", "---"))]
    cap = any("MAX_BISECTION_STEPS" in d for d in diff)
    if cap_only:
        if cap:
            print(Path(path).name, "CAP")
        continue
    print(f"{Path(path).name} cap={cap} n={len(diff)}")
    for d in diff:
        print("    " + d)
