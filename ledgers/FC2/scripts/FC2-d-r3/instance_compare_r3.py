import importlib.util, json, sys
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
old = load("/tmp/fc2d-r3-instance_old.py", "inst_old")
new = load(sys.argv[1] + "/course/modules/FC/FC2/grader/instance.py", "inst_new")
same = 0; diff = []
for seed in range(0, 1000):
    a = json.dumps(old.make_instance(seed), sort_keys=True); b = json.dumps(new.make_instance(seed), sort_keys=True)
    if a == b: same += 1
    else: diff.append(seed)
print("seeds 0..999 identical output:", same, "differing:", diff[:10])
# no half-cent ties among the accepted chains (the rule the docstring states)
from fractions import Fraction
bad = []
for seed in range(0, 1000):
    i = new.make_instance(seed)
    s = i["spot_cents"]; df = i["df_ppm"]; K = i["strikes_cents"]; C = i["call_cents"]; P = i["put_cents"]
    gaps = [new._parity_gap(C[k], P[k], s, K[k], df) for k in range(6)]
    secs = [new._second_difference(K, C, j) for j in range(1, 5)]
    if any(new._is_half_cent(x) for x in gaps + secs): bad.append(seed)
print("accepted chains with a half-cent tie in the gaps or second differences:", bad)
print("planted kinds:", {k: sum(1 for s in range(1000) if new.make_instance(s)["planted_kind"] == k) for k in ("parity","convexity","none")})
