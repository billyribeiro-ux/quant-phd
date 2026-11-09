"""Round 19 (BK4 slice c): check that every test function in grader/test_project.py hides its own traceback.

Usage: python -I tracebackhide_check.py <path-to-test_project.py>
Prints each test name that lacks a `__tracebackhide__ = True` statement in its body, then the totals.
"""

import ast
import sys

tree = ast.parse(open(sys.argv[1], encoding="utf-8").read(), filename=sys.argv[1])
tests = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
missing = []
for fn in tests:
    hidden = any(
        isinstance(s, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "__tracebackhide__" for t in s.targets)
        and isinstance(s.value, ast.Constant)
        and s.value.value is True
        for s in fn.body
    )
    if not hidden:
        missing.append(fn.name)
print("test functions defined at module level:", len(tests))
print("without __tracebackhide__ = True:", len(missing))
for name in missing:
    print("  MISSING", name)
