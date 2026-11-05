"""For each mutant: a one-line description docstring exists, and the code differs from grader/reference.py.
Usage: python3 -I mutant_docstrings_r11.py <root>"""
import ast
import glob
import sys

root = sys.argv[1]
ref = open(f"{root}/course/modules/E/E4/grader/reference.py", encoding="utf-8").read()
ref_body = ast.unparse(ast.parse(ref).body[1:]) if False else None
ref_tree = ast.parse(ref)
ref_code = ast.unparse(ast.Module(body=ref_tree.body[1:], type_ignores=[]))
bad = []
n = 0
for path in sorted(glob.glob(f"{root}/ledgers/E4/mutants/*.py")):
    n += 1
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    doc = ast.get_docstring(tree)
    code = ast.unparse(ast.Module(body=tree.body[1:], type_ignores=[]))
    if not doc or "\n" in doc.strip().split("\n")[0] and False:
        bad.append((path, "no docstring"))
    if code == ref_code:
        bad.append((path, "identical to reference"))
print(f"mutants: {n}; problems: {len(bad)}")
for b in bad:
    print(" ", b)
