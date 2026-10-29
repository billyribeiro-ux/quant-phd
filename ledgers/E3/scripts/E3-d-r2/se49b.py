import sys, json, importlib.util, types
ROOT = "/tmp/verifyC2-E3-d"
sys.path.insert(0, ROOT + "/course/modules/E/E3/grader")
from instance import make_instance
spec = importlib.util.spec_from_file_location("ra", ROOT + "/ledgers/E3/scripts/run_alternatives.py")
ra = importlib.util.module_from_spec(spec); spec.loader.exec_module(ra)
def load(name, src):
    m = types.ModuleType(name); exec(compile(src, name, "exec"), m.__dict__); return m
ref = load("ref", open(ROOT + "/course/modules/E/E3/grader/reference.py").read())
alt1 = load("alt1", ra.build("alt1"))
for seed in (49,):
    inst = make_instance(seed)
    resp = json.loads(inst["responses_json"])
    print("TRUE", {k: inst[k] for k in ("gamma","lambda","kappa")})
    for name, m in (("ref", ref), ("alt1", alt1)):
        e = m.estimate(resp)
        print(name, "loglik field", e["log_likelihood"], "gamma", e["gamma_hat"], "lam", e["lambda_hat"], "kap", e["kappa_hat"])
    # mixed-sign count and a grid scan of loglik to see the global max
    import itertools
    parsed = [ref._parse(r) for r in resp]
    best = None
    for g in [0.05*i for i in range(1,20)]:
        for lam in [0.5,1,1.5,2,3,4,6,8,12,16,20,25,30]:
            for kap in [0.5,1,1.5,2,2.5,3,4,5]:
                v = ref._logit_sum(parsed, g, lam, kap)
                if best is None or v > best[0]: best = (v,g,lam,kap)
    print("grid best", best)
