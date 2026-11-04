"""Check that the page's Lab 1 replay() prints nothing and returns the oracle values (the round-2 FAIL row)."""
import ast
import contextlib
import io
import sys

WS = "/tmp/pc3c-r3-ws"  # scratch workspace holding engine.py, instance.py, test_project.py, market_maker.py (reference)
sys.path.insert(0, WS)
src = open("/tmp/pc3c-r3-lab-PC3-project-1-page.py", encoding="utf-8").read()
tree = ast.parse(src)
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == "replay":
        prints = [n for n in ast.walk(node) if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "print"]
        print("print calls inside replay():", len(prints))
ns: dict = {"__name__": "lab1_page"}
exec(compile(src.replace("\nmain()", "\n"), "lab1_page", "exec"), ns)
import test_project as tp  # noqa: E402
for seed in (0, 1, 2, 3, 4, 5):
    log = ns["play"](seed)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = ns["replay"](log)
    print(f"seed {seed}: replay output chars {len(buf.getvalue())}, equals oracle {out == tp.oracle(log)}")
