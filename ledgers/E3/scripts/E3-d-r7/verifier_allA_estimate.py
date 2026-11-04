import sys, ast, math
sys.path.insert(0, "/Users/billyribeiro/.fanout/scratch-E3-d-r7/work")
import elicit as sol
src = open("/Users/billyribeiro/.fanout/wt/verifyD7-E3-d/course/modules/E/E3/grader/test_project.py", encoding="utf-8").read()
tree = ast.parse(src)
env = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("B_SIDE_SURE_A", "B_SIDE_CHOICES", "B_SIDE_LOTTERIES"):
        env[node.targets[0].id] = ast.literal_eval(node.value)
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id in ("B_SIDE_SURE_A", "B_SIDE_CHOICES", "B_SIDE_LOTTERIES"):
        env[node.target.id] = ast.literal_eval(node.value)
A, C, L = env["B_SIDE_SURE_A"], env["B_SIDE_CHOICES"], env["B_SIDE_LOTTERIES"]
print("B side pairs", len(A), len(C), len(L))
resp = [{"pair_id": i, "choice": "A", "prizes_a": [A[i]], "probs_a": ["1"], "prizes_b": L[i][0], "probs_b": L[i][1]} for i in range(len(A))]
try:
    r = sol.estimate(resp)
    print("all-A estimate:", r)
except Exception as e:
    print("all-A raised", type(e).__name__, str(e)[:200])
resp2 = [{"pair_id": i, "choice": C[i], "prizes_a": [A[i]], "probs_a": ["1"], "prizes_b": L[i][0], "probs_b": L[i][1]} for i in range(len(A))]
try:
    print("B-side mixed (true choices):", sol.estimate(resp2))
except Exception as e:
    print("B-side raised", type(e).__name__, str(e)[:200])
