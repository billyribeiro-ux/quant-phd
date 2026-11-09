"""Probe: the reference estimate on the fixed 26-response participant, and its observed information margin."""
import ast
import math
import sys
from pathlib import Path

GRADER = Path("/Users/billyribeiro/dev/quant-phd/course/modules/E/E3/grader")
sys.path.insert(0, str(GRADER))
import reference as sol  # noqa: E402

src = (GRADER / "test_project.py").read_text(encoding="utf-8")
tree = ast.parse(src)
rows = None
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "FIXED_26_ANSWERS":
        rows = ast.literal_eval(node.value)
responses = [
    {"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb}
    for i, c, pa, qa, pb, qb in rows
]
try:
    fit = sol.estimate(responses)
    print({k: fit[k] for k in fit})
except RuntimeError as err:
    print("RuntimeError:", err)
parsed = [sol._parse(r) for r in responses]
xi = sol._maximise(parsed)
print("xi", xi)
_, hess = sol._gradient_and_hessian(lambda t: sol._objective(t, parsed), xi)
print("hess", hess)
print("neg hess diag", [-hess[i][i] for i in range(3)])
