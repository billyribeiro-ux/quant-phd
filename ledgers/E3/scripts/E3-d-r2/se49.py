import sys, json, importlib.util, types
ROOT = "/tmp/verifyC2-E3-d"
sys.path.insert(0, ROOT + "/course/modules/E/E3/grader")
from instance import make_instance
spec = importlib.util.spec_from_file_location("ra", ROOT + "/ledgers/E3/scripts/run_alternatives.py")
ra = importlib.util.module_from_spec(spec); spec.loader.exec_module(ra)
def load(name, src):
    m = types.ModuleType(name); exec(compile(src, name, "exec"), m.__dict__); return m
mods = {"reference": load("ref", open(ROOT + "/course/modules/E/E3/grader/reference.py").read())}
for n in ra.ALTERNATIVES:
    mods[n] = load(n, ra.build(n))
for seed in (49, 0, 1):
    resp = json.loads(make_instance(seed)["responses_json"])
    for n, m in mods.items():
        e = m.estimate(resp)
        print(seed, n, {k: round(v, 6) for k, v in e.items() if k.startswith("se_") or k in ("gamma_hat","lambda_hat","kappa_hat")})
