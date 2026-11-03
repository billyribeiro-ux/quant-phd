"""List every assert in the FC1 project suite with no message, and every pytest.fail (verifier r4)."""
import ast
from pathlib import Path

src = Path("/Users/billyribeiro/.fanout/wt/verifyD4-FC1-c/course/modules/FC/FC1/grader/test_project.py").read_text(encoding="utf-8")
tree = ast.parse(src)
no_msg = []
fails = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assert):
        if node.msg is None:
            no_msg.append(node.lineno)
    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "fail":
        fails.append(node.lineno)
print("asserts without message:", no_msg)
print("pytest.fail call lines:", len(fails))
funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
print("top-level test functions:", len(funcs))

# Messages that contain digits could leak a value; list them for reading.
digit_msgs = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assert) and isinstance(node.msg, ast.Constant) and isinstance(node.msg.value, str):
        if any(ch.isdigit() for ch in node.msg.value):
            digit_msgs.append((node.lineno, node.msg.value[:110]))
    if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "fail":
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and any(ch.isdigit() for ch in arg.value):
                digit_msgs.append((node.lineno, arg.value[:110]))
print("messages with digits:", len(digit_msgs))
for d in digit_msgs:
    print("  ", d)
