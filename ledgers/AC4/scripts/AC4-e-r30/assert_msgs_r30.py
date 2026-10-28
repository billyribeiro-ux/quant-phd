"""Lists assert statements without a message and f-string messages that interpolate a computed expected value."""
import ast, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
tree = ast.parse(src)
bare = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert) and n.msg is None]
print("asserts without message:", bare)
leaks = []
for n in ast.walk(tree):
    if isinstance(n, ast.Assert) and n.msg is not None:
        for sub in ast.walk(n.msg):
            if isinstance(sub, ast.FormattedValue):
                leaks.append((n.lineno, ast.unparse(sub.value)))
    if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "fail":
        for sub in ast.walk(n):
            if isinstance(sub, ast.FormattedValue):
                leaks.append((n.lineno, ast.unparse(sub.value)))
print("f-string messages interpolating values:", leaks)
