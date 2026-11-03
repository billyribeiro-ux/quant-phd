"""Scan test_project.py: list every assert (message present?, numeric literals in its source) and every pytest.fail text."""
import ast
import sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
tree = ast.parse(src)
lines = src.splitlines()
bare = []
with_msg = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assert):
        seg = ast.get_source_segment(src, node) or ""
        lits = sorted({str(n.value) for n in ast.walk(node.test) if isinstance(n, ast.Constant) and isinstance(n.value, int) and not isinstance(n.value, bool) and abs(n.value) > 9})
        rec = (node.lineno, "msg" if node.msg is not None else "NO-MSG", lits)
        (with_msg if node.msg is not None else bare).append(rec)
print("asserts with message:", len(with_msg), " bare asserts:", len(bare))
print("bare:", bare)
print("messages with literal ints >9 in the test (source-line leak candidates):")
for ln, kind, lits in with_msg:
    if lits:
        print("  line", ln, lits, "|", lines[ln - 1].strip()[:110])
fails = [(n.lineno) for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "fail"]
print("pytest.fail calls:", len(fails))
