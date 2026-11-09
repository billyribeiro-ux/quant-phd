"""AST profile of every E4 mutant against grader/reference.py (round 16 verifier).

Docstrings are removed and comments are ignored (ast). For each mutant, prints the top-level or method-level
definitions whose code differs from the reference, and the number of differing unparsed statement lines.
Usage: python -I mutant_ast_profile_r16.py <checkout-root>
"""
import ast
import difflib
import sys
from pathlib import Path


def strip_doc(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                node.body = body[1:] or [ast.Pass()]
    return tree


def units(src: str) -> dict[str, str]:
    tree = strip_doc(ast.parse(src))
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = ast.unparse(node)
        elif isinstance(node, ast.Assign):
            out["assign:" + ast.unparse(node.targets[0])] = ast.unparse(node)
        else:
            out["other:" + ast.unparse(node)[:40]] = ast.unparse(node)
    return out


root = Path(sys.argv[1])
ref_src = (root / "course/modules/E/E4/grader/reference.py").read_text(encoding="utf-8")
ref = units(ref_src)
for f in sorted((root / "ledgers/E4/mutants").glob("*.py")):
    src = f.read_text(encoding="utf-8")
    mu = units(src)
    keys = sorted(set(ref) | set(mu))
    diffs = []
    for k in keys:
        if ref.get(k) != mu.get(k):
            if k not in ref or k not in mu:
                diffs.append(f"{k}:ADDED/REMOVED")
                continue
            d = [l for l in difflib.unified_diff(ref[k].splitlines(), mu[k].splitlines(), lineterm="", n=0)
                 if l[:1] in "+-" and l[:3] not in ("+++", "---")]
            diffs.append(f"{k}:{len(d)}")
    print(f"{f.name} | code_units_differing={diffs}")
