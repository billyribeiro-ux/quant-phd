"""For seeds in a range, compute the z of the grader's Monte Carlo mean test on the reference solution (no pytest)."""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
G = ROOT / "course/modules/CF/CF1/grader"
sys.path.insert(0, str(G))
import instance  # noqa: E402
import reference as ref  # noqa: E402

lo, hi = int(sys.argv[2]), int(sys.argv[3])
fails = []
worst = (0.0, None)
for seed in range(lo, hi):
    inst = instance.make_instance(seed)
    project = json.loads(inst["payload"])
    rate = inst["nominal_rate"]
    n = inst["mc_draws"]
    draws = ref.npv_monte_carlo(project, rate, n, seed, inst["volatility"])
    mean = sum(draws) / n
    var = sum((d - mean) ** 2 for d in draws) / (n - 1)
    se = math.sqrt(var / n)
    det = ref.npv(rate, ref.after_tax_cash_flows(project))
    z = (mean - det) / se if se > 0 else float("nan")
    if abs(z) > 3.0:
        fails.append((seed, round(z, 3)))
    if abs(z) > abs(worst[0]) or worst[1] is None:
        worst = (z, seed)
print(f"seeds {lo}..{hi-1}: |z|>3 for {len(fails)} seeds; first: {fails[:8]}; worst |z| {abs(worst[0]):.3f} at seed {worst[1]}")
if len(sys.argv) > 4:
    s = int(sys.argv[4])
    inst = instance.make_instance(s)
    print("seed", s, "mc_draws", inst["mc_draws"], "volatility", inst["volatility"], "nominal_rate", inst["nominal_rate"])
