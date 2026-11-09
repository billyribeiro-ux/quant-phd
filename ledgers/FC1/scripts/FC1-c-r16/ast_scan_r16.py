"""Round 16, FC1-c: AST scan of grader/test_project.py: asserts without messages, tests without docstrings, must_raise/must_accept calls without a condition string."""
import ast, sys
path = sys.argv[1]
tree = ast.parse(open(path, encoding="utf-8").read())
n_tests = 0
bad_assert, no_doc, bad_call = [], [], []
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
        n_tests += 1
        if ast.get_docstring(node) is None:
            no_doc.append((node.name, node.lineno))
    if isinstance(node, ast.Assert) and node.msg is None:
        bad_assert.append(node.lineno)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("must_raise", "must_accept"):
        if len(node.args) < 2:
            bad_call.append(node.lineno)
print("test functions:", n_tests)
print("tests without docstring:", no_doc)
print("asserts without message:", bad_assert)
print("must_raise/must_accept calls without condition string:", bad_call)
