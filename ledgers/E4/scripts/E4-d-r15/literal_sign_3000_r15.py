"""Round-15 re-check of the literal_price_sign equivalence claim (equivalent/README.md, proof item 4).

Compares literal_price_sign.py with grader/reference.py on 3000 random inputs (noise_sd in [0.05, 3.0], info_cost in
[0, 0.4]) and reports the largest absolute difference of the three outputs. Usage: python -I literal_sign_3000_r15.py
"""
import importlib.util
import random
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load("course/modules/E/E4/grader/reference.py", "ref_mod")
lit = load("ledgers/E4/equivalent/literal_price_sign.py", "lit_mod")
rng = random.Random(15)
worst = {"informed_fraction": 0.0, "price_informativeness": 0.0, "indifference_gap": 0.0}
n = 0
for _ in range(3000):
    sd = rng.uniform(0.05, 3.0)
    c = rng.uniform(0.0, 0.4)
    a = ref.solve_model(sd, c)
    b = lit.solve_model(sd, c)
    for k in worst:
        worst[k] = max(worst[k], abs(a[k] - b[k]))
    n += 1
print("inputs", n, "largest abs difference per output:", {k: f"{v:.1e}" for k, v in worst.items()})
