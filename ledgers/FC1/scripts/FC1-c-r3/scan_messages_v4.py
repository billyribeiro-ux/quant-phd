"""List every assert / pytest.fail in the FC1 grader suite: bare asserts, short messages, and messages with numeric literals."""
import ast
import re
import sys
from pathlib import Path

src_path = Path(sys.argv[1])
src = src_path.read_text()
tree = ast.parse(src)
bare, short, numeric = [], [], []
for node in ast.walk(tree):
    if isinstance(node, ast.Assert):
        if node.msg is None:
            bare.append(node.lineno)
            continue
        msg = ast.get_source_segment(src, node.msg) or ""
        words = re.findall(r"[A-Za-z]+", msg)
        if len(words) <= 4:
            short.append((node.lineno, msg))
        if re.search(r"\b\d{2,}\b", msg):
            numeric.append((node.lineno, msg[:120]))
    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "fail":
        msg = ast.get_source_segment(src, node) or ""
        if re.search(r"\b\d{2,}\b", msg):
            numeric.append((node.lineno, "pytest.fail: " + msg[:120]))
print("bare asserts:", bare)
print("short messages (<=4 words):", short)
print("messages containing a number of 2+ digits (check for leaks):")
for ln, m in numeric:
    print("  ", ln, m)
