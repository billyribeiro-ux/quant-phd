"""Round 16: sample 20 seeds of grader/instance.py, check validity and that answers change (reference solver).

Usage: python -I instances_sample_r16.py <checkout-root>
"""
import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


inst = load(root / "course/modules/E/E4/grader/instance.py", "inst")
ref = load(root / "course/modules/E/E4/grader/reference.py", "ref")
fr = []
ok = True
for s in range(20):
    a = inst.make_instance(s)
    b = inst.make_instance(s)
    ok &= a == b
    ok &= 0.5 <= a["noise_sd"] <= 0.75 and 0.12 <= a["info_cost"] <= 0.15
    out = ref.solve_model(a["noise_sd"], a["info_cost"])
    fr.append(out["informed_fraction"])
    print(s, a, f"lam={out['informed_fraction']:.8f} pi={out['price_informativeness']:.8f} gap={out['indifference_gap']:+.2e}")
print("deterministic and in box:", ok, "| distinct informed fractions among 20 seeds:", len({round(x, 9) for x in fr}))
