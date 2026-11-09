"""Reference gamma_hat, lambda_hat and kappa_hat on each fixed fixture of test_project.py."""
import ast
import json
import sys
from pathlib import Path

GRADER = Path("/Users/billyribeiro/dev/quant-phd/course/modules/E/E3/grader")
sys.path.insert(0, str(GRADER))
import reference as sol  # noqa: E402
from instance import make_instance  # noqa: E402

tree = ast.parse((GRADER / "test_project.py").read_text(encoding="utf-8"))
consts = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        consts[node.targets[0].id] = node
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        consts[node.target.id] = node
# the B-side twelve-response set (built from B_SIDE_SURE_A, B_SIDE_CHOICES, B_SIDE_LOTTERIES)
sure = ast.literal_eval(consts["B_SIDE_SURE_A"].value)
choices = ast.literal_eval(consts["B_SIDE_CHOICES"].value)
lots = ast.literal_eval(consts["B_SIDE_LOTTERIES"].value)
b_side = [{"pair_id": i, "choice": choices[i], "prizes_a": [sure[i]], "probs_a": ["1"], "prizes_b": lots[i][0], "probs_b": lots[i][1]} for i in range(12)]
rows = ast.literal_eval(consts["FIXED_26_ANSWERS"].value)
f26 = [{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in rows]
for name, resp in (("FIXED_26", f26), ("B_SIDE_12", b_side),
                   ("LOW_KAPPA(30)", json.loads(str(make_instance(30)["responses_json"]))),
                   ("LARGE_LAMBDA(49)", json.loads(str(make_instance(49)["responses_json"])))):
    try:
        fit = sol.estimate(resp)
        print(name, {k: round(v, 6) for k, v in fit.items()})
    except Exception as err:  # noqa: BLE001
        print(name, type(err).__name__, str(err)[:90])
