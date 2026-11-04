"""Round-5 checks: fixed-seed path distinctness (0..49), instance draw order vs Lesson 4 page, and test counts by marker.

Run with: python3 -I <this file> <grader_dir>. Reads grader files only; writes nothing into the repo.
"""
import ast
import sys

grader = sys.argv[1]
sys.path.insert(0, grader)
import instance  # noqa: E402

paths = {tuple(instance.make_instance(s)["fair_path_cents"]) for s in range(50)}
print("fixed seeds 0..49 distinct fair paths:", len(paths))
window_pairs = []
for a in range(50):
    for b in range(a + 1, 50):
        if instance.make_instance(a)["fair_path_cents"] == instance.make_instance(b)["fair_path_cents"]:
            window_pairs.append((a, b))
print("identical pairs among seeds 0..49:", window_pairs)
p = instance.make_instance(0)
print("seed 0 settlement:", p["settlement_cents"], "arrivals counts:", {k: p["arrivals"].count(k) for k in set(p["arrivals"])})

src = open(grader + "/test_project.py", encoding="utf-8").read()
tree = ast.parse(src)
tests = [n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
print("top-level test functions:", len(tests))
