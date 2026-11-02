"""Lists assert statements in grader/test_project.py that have no message and compare against a numeric literal.

Such a failing assert prints its source line in the traceback, so the literal (the answer) is shown to the learner.
Usage: python -I bare_asserts.py <path to test_project.py>
"""

from __future__ import annotations

import ast
import sys

src = open(sys.argv[1], encoding="utf-8").read()
tree = ast.parse(src)
lines = src.splitlines()
for func in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]:
    for node in ast.walk(func):
        if isinstance(node, ast.Assert) and node.msg is None:
            literals = [
                c.value
                for c in ast.walk(node.test)
                if isinstance(c, ast.Constant) and isinstance(c.value, (int, float)) and not isinstance(c.value, bool)
            ]
            if literals:
                print(f"{func.name} line {node.lineno}: literals {literals} | {lines[node.lineno - 1].strip()}")
