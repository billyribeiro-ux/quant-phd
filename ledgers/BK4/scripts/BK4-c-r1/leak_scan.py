"""List test_project.py tests whose docstring or failing assert line shows an expected value (BK4-c r1).

A failure prints the test's docstring and the asserting statement, so a digit there that is the expected answer leaks it.
Run: .venv/bin/python ledgers/BK4/scripts/BK4-c-r1/leak_scan.py
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = (ROOT / "course" / "modules" / "BK" / "BK4" / "grader" / "test_project.py").read_text(encoding="utf-8")
tree = ast.parse(SRC)
lines = SRC.splitlines()
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
        doc = ast.get_docstring(node) or ""
        first = doc.splitlines()[0] if doc else ""
        doc_digits = re.findall(r"\b\d[\d_.,]*\b", first)
        assert_lines = []
        for sub in ast.walk(node):
            if isinstance(sub, ast.Assert) or (isinstance(sub, ast.Expr) and isinstance(sub.value, ast.Call)):
                text = ast.get_source_segment(SRC, sub) or ""
                if re.search(r"==\s*-?\d", text) or re.search(r"\(\s*-?\d", text):
                    assert_lines.append(text.splitlines()[0][:90])
        if doc_digits or assert_lines:
            print(f"{node.lineno} {node.name}: docstring digits {doc_digits} | literal asserts {assert_lines[:2]}")
