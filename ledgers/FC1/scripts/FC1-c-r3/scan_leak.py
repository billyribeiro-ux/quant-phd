"""For each assert/pytest.fail in test_project.py: is the enclosing test function hiding its traceback (__tracebackhide__ = True)?
A non-hidden failing frame shows its source line under --assert=plain; the line leaks an expected literal if it contains one."""
import ast
import sys

src = open(sys.argv[1], encoding="utf-8").read()
tree = ast.parse(src)
for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef)]:
    hidden = any(isinstance(s, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__tracebackhide__" for t in s.targets) for s in fn.body)
    for node in ast.walk(fn):
        if isinstance(node, ast.Assert):
            lits = [n.value for n in ast.walk(node.test) if isinstance(n, ast.Constant) and isinstance(n.value, int) and not isinstance(n.value, bool) and abs(n.value) > 9]
            if not hidden and (lits or node.msg is None):
                print(f"VISIBLE frame: {fn.name} line {node.lineno} msg={'yes' if node.msg else 'NO'} literals={lits}")
print("scan done")
