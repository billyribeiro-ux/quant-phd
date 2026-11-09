"""Round-15 hunk listing: every mutant in ledgers/E4/mutants/ against grader/reference.py, with all docstrings and
comments removed (AST normalisation), so only executable differences remain.

Prints, per mutant, the changed code lines ('-' reference, '+' mutant). Usage: python -I mutant_hunks_r15.py
"""
import ast
import difflib
import glob
from pathlib import Path


def normalised(text: str) -> list[str]:
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
    return ast.unparse(tree).split("\n")


ref = normalised(Path("course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8"))
for path in sorted(glob.glob("ledgers/E4/mutants/*.py")):
    mut = normalised(Path(path).read_text(encoding="utf-8"))
    changes = [d for d in difflib.unified_diff(ref, mut, lineterm="", n=0) if d[:1] in "+-" and not d.startswith(("+++", "---"))]
    name = Path(path).name
    if not changes:
        print(f"{name}: NO EXECUTABLE CHANGE")
        continue
    print(f"{name}: {len(changes)} changed line(s)")
    for c in changes:
        print("   " + c[:190])
