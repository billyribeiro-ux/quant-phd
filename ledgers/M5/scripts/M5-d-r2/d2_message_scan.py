"""Scan every failure message in the M5 grader for digits that could leak an answer, and check that
no message quotes a computed value (round 2). Prints each message that contains a digit, and the count of messages."""

import ast
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
PATH = os.path.join(REPO, "course/modules/M/M5/grader/test_project.py")

with open(PATH, encoding="utf-8") as fh:
    tree = ast.parse(fh.read())

total = 0
for node in ast.walk(tree):
    if not isinstance(node, ast.Call):
        continue
    name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
    if name not in ("expect", "must_raise", "fail"):
        continue
    for arg in node.args:
        text = None
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            text = arg.value
        elif isinstance(arg, ast.JoinedStr):
            text = "".join(v.value if isinstance(v, ast.Constant) else "{...}" for v in arg.values)
        if text is None:
            continue
        total += 1
        if any(ch.isdigit() for ch in text):
            print(f"line {node.lineno}: {text}")
print(f"messages scanned: {total}")
