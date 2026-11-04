"""Counts the entries of the refusals list in test_refused_inputs_print_nothing_before_they_raise, and the test docstring.

Usage: python -I count_refusals_r5.py <path to test_project.py>
"""

from __future__ import annotations

import ast
import sys

tree = ast.parse(open(sys.argv[1], encoding="utf-8").read())
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name == "test_refused_inputs_print_nothing_before_they_raise":
        doc = ast.get_docstring(node)
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.value, ast.List):
                print("docstring:", doc)
                print("refusal entries:", len(stmt.value.elts))
