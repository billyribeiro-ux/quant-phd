"""Write three alternative correct engines (CF1 round 19, slice d) from grader/reference.py by text edits.

Each replacement must match exactly once. The alternatives keep the contract (validation rules, 4001 log-spaced grid
over [1e-4, 1e4], 1e-7 root precision, seeded draw order) and change only the numerical algorithm.
"""

import sys
from pathlib import Path

ref = Path(sys.argv[1]) / "course/modules/CF/CF1/grader/reference.py"
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
src = ref.read_text(encoding="utf-8")


def edit(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        assert text.count(old) == 1, old
        text = text.replace(old, new)
    return text


# A: NPV by Horner's rule from the last flow back to the outlay (same value, different arithmetic).
alt_a = edit(
    src,
    [
        (
            "    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
            "    acc = float(flows[-1])\n"
            "    for cf in reversed(flows[:-1]):\n"
            "        acc = float(cf) + acc / (1.0 + rate)\n"
            "    return acc",
        ),
    ],
)

# B: Fisher through logarithms: (1 + n) = exp(log1p(r) + log1p(pi)), so n = expm1(...).
alt_b = edit(
    src,
    [
        (
            "    return (1.0 + real) * (1.0 + inflation) - 1.0",
            "    return math.expm1(math.log1p(real) + math.log1p(inflation))",
        ),
    ],
)

# C: Monte Carlo through the affine identity: NPV(m) = NPV(0) + m * (NPV(1) - NPV(0)), the same draws.
alt_c = edit(
    src,
    [
        (
            "    rng = random.Random(seed)\n    out: list[float] = []\n    for _ in range(n_draws):\n"
            "        z = rng.gauss(0.0, 1.0)\n"
            "        m = math.exp(volatility * z - volatility * volatility / 2.0)\n"
            "        scaled = dict(project)\n"
            "        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]\n"
            "        out.append(npv(rate, after_tax_cash_flows(scaled)))\n"
            "    return out",
            "    rng = random.Random(seed)\n"
            "    at_zero = dict(project)\n"
            "    at_zero[\"revenue\"] = [0.0 for _ in project[\"revenue\"]]\n"
            "    npv_zero = npv(rate, after_tax_cash_flows(at_zero))\n"
            "    npv_one = npv(rate, after_tax_cash_flows(project))\n"
            "    out: list[float] = []\n"
            "    for _ in range(n_draws):\n"
            "        z = rng.gauss(0.0, 1.0)\n"
            "        m = math.exp(volatility * z - volatility * volatility / 2.0)\n"
            "        out.append(npv_zero + m * (npv_one - npv_zero))\n"
            "    return out",
        ),
    ],
)

for name, text in [
    ("alt_d19_a_horner_npv.py", alt_a),
    ("alt_d19_b_fisher_logarithms.py", alt_b),
    ("alt_d19_c_monte_carlo_affine.py", alt_c),
]:
    (out / name).write_text(text, encoding="utf-8")
print("wrote 3 alternatives")
