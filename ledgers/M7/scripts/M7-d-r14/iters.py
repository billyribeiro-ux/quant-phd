import sys, json
sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/quant-b2/course/modules/M/M7/grader")
import instance, reference as R
calls = {"n": 0}
orig = R._kkt_step
def counting(*a, **k):
    calls["n"] += 1
    return orig(*a, **k)
R._kkt_step = counting
mx = 0; eq_w0 = []
for seed in range(300):
    case = json.loads(instance.make_instance(seed)["payload"])
    calls["n"] = 0
    p = R._parse(case)
    sol = R._solve(p)
    if seed < 50:
        mx = max(mx, calls["n"])
    if sol["w"] == p.w0:
        eq_w0.append(seed)
print("max kkt_step calls on seeds 0-49:", mx)
print("seeds (of 0-299) where answer equals w0:", eq_w0)
