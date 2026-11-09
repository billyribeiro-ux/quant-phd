"""FC1-c round 17: static scans of the grader test file, the project page and the mutant set (read-only)."""

import ast
import glob
import os
import re
import sys

root = sys.argv[1]
test_path = os.path.join(root, "course/modules/FC/FC1/grader/test_project.py")
tree = ast.parse(open(test_path, encoding="utf-8").read())
funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
print("test functions:", len(funcs))
print("tests without docstring:", [f.name for f in funcs if ast.get_docstring(f) is None])
no_msg_asserts = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assert) and node.msg is None:
        no_msg_asserts.append(node.lineno)
print("asserts without message (line numbers):", no_msg_asserts)
bad_helper_calls = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("must_raise", "must_accept"):
        want = 2 if node.func.id == "must_raise" else 2
        if len(node.args) < want:
            bad_helper_calls.append(node.lineno)
print("must_raise/must_accept calls without condition string (line numbers):", bad_helper_calls)
for name in ("test_bond_coupon_of_ten_to_the_eighteenth_bps_is_accepted", "test_trade_price_of_ten_to_the_eighteenth_cents_is_accepted"):
    f = next(x for x in funcs if x.name == name)
    print(f"{name}: lines {f.lineno}-{f.end_lineno}")
# test-name cross-check for the page's enumerated claims
names = {f.name for f in funcs}
print("accepted-input tests on page claims present:", sorted(n for n in names if "accepted" in n)[:0], len([n for n in names if "accepted" in n]))
page = open(os.path.join(root, "course/modules/FC/FC1/project.html"), encoding="utf-8").read()
m = re.search(r"runs (\d+) checks", page)
print("page check count:", m.group(1) if m else None)
print("math tokens on page:", len(re.findall(r"\\\(", page)), re.findall(r"\\\((.*?)\\\)", page))
print("exemplar mentions on page:", len(re.findall(r"exemplar", page, re.I)))
muts = sorted(glob.glob(os.path.join(root, "ledgers/FC1/mutants/*.py")))
print("mutant files:", len(muts))
non_student = []
for p in muts:
    doc = ast.get_docstring(ast.parse(open(p, encoding="utf-8").read())) or ""
    first = doc.splitlines()[0] if doc else ""
    if not first.startswith("Student error"):
        non_student.append((os.path.basename(p), first[:90]))
print("mutants whose first docstring line does not start 'Student error':", non_student)
for lab in sorted(glob.glob(os.path.join(root, "tests/labs/FC1/lab-FC1-project-*.py"))):
    src = open(lab, encoding="utf-8").read()
    hits = re.findall(r"open\(|read_text|urllib|requests|socket|random", src)
    print(os.path.basename(lab), "I/O or random tokens:", hits, "| SIMULATED in text:", "SIMULATED" in src)
