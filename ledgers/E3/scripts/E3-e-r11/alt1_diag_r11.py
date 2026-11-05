# Diagnoses alt1 (grid, zoom, Newton polish) on seed 0: compares its best likelihood with the reference's maximum.
import importlib.util, sys, json
W = "/tmp/e3e_r11/ws_alt1_diag"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
alt = load("alt", sys.argv[1]); ref = load("ref", sys.argv[2]); inst = load("inst", sys.argv[3])
for seed in (0, 1):
    I = inst.make_instance(seed)
    resp = json.loads(str(I["responses_json"]))
    parsed_a = [alt._parse(r) for r in resp]
    xi_a = alt._maximise(parsed_a)
    va = alt._objective(xi_a, parsed_a)
    parsed_r = [ref._parse(r) for r in resp]
    xi_r = ref._maximise(parsed_r)
    vr = ref._objective(xi_r, parsed_r)
    print(f"seed {seed}: alt best loglik {va:.10f} at gamma {1/(1+__import__('math').exp(-xi_a[0])):.6f} lam {__import__('math').exp(xi_a[1]):.6f} kappa {__import__('math').exp(xi_a[2]):.6f}")
    print(f"seed {seed}: ref best loglik {vr:.10f} at gamma {1/(1+__import__('math').exp(-xi_r[0])):.6f} lam {__import__('math').exp(xi_r[1]):.6f} kappa {__import__('math').exp(xi_r[2]):.6f}")
    print(f"seed {seed}: alt minus ref = {va - vr:.3e}")
