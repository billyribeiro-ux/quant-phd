import importlib.util, sys, json, math
sys.path.insert(0, "/tmp/E3d_r10_ws/ref")
import instance as inst_mod
import test_project as tp  # imports ref elicit as sol (harmless)
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
alt = load("/tmp/E3d_r10_ws/alt6/elicit.py", "alt6_elicit")
ref = load("/tmp/E3d_r10_ws/ref/elicit.py", "ref_elicit")
inst = inst_mod.make_instance(2)
resp = json.loads(inst["responses_json"])
parsed = [tp.parse(r) for r in resp]
for name, mod in (("ref", ref), ("alt6", alt)):
    e = mod.estimate(resp)
    print(name, {k: round(v, 6) for k, v in e.items()})
    print("  score comp 1e-5 / 1e-6:", tp._largest_score_component(parsed, e["gamma_hat"], e["lambda_hat"], e["kappa_hat"], 1e-5), tp._largest_score_component(parsed, e["gamma_hat"], e["lambda_hat"], e["kappa_hat"], 1e-6))
