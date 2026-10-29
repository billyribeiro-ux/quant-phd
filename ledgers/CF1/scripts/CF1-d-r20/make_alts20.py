"""Round 20 alternative correct engines, derived from the reference by exact text replacement (each old string must occur once)."""
import pathlib
import sys

REF = pathlib.Path("/tmp/verify20-CF1-d/course/modules/CF/CF1/grader/reference.py")
OUT = pathlib.Path("/tmp/verify20-CF1-d/ledgers/CF1/scripts/CF1-d-r20/alts")
src = REF.read_text()


def derive(name: str, edits: list[tuple[str, str]], doc: str) -> None:
    text = src
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{name}: expected one occurrence, found {n}: {old[:60]!r}")
        text = text.replace(old, new)
    header = f'"""{doc}"""\n'
    text = text.replace(src.split('"""', 2)[1] and src[: src.index('"""', src.index('"""') + 3) + 3], header.rstrip("\n") + "\n", 1)
    (OUT / name).write_text(text)


# A: IRR search on a finer grid of 20001 samples, in the rate, with a bisection to the last bit; NPV Horner form.
derive(
    "alt_r20_a_irr_fine_grid_and_horner_npv.py",
    [
        ("_GRID_POINTS = 4001", "_GRID_POINTS = 20001"),
        (
            "    def poly(x: float) -> float:\n        return sum(cf * x**t for t, cf in enumerate(flows))\n",
            "    def poly(x: float) -> float:\n        acc = 0.0\n        for cf in reversed(flows):\n            acc = acc * x + cf\n        return acc\n",
        ),
        ("            for _ in range(200):", "            for _ in range(400):"),
    ],
    "Alternative correct engine (round 20): IRR grid of 20001 samples, Horner polynomial, longer bisection.",
)

# B: payback with a 1e-12 absolute tolerance on the recovery test, NPV accumulated from the last flow.
derive(
    "alt_r20_b_payback_tolerance_and_accumulated_npv.py",
    [
        ("        if cumulative + discounted[t] >= 0.0:", "        if cumulative + discounted[t] >= -1e-12:"),
        (
            '    return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))\n',
            "    value = 0.0\n    for t in range(len(flows) - 1, -1, -1):\n        value = value / (1.0 + rate) + flows[t]\n    return value\n",
        ),
    ],
    "Alternative correct engine (round 20): payback recovery tested with a 1e-12 tolerance; NPV by backward accumulation.",
)

# C: real flows by a running discount factor; Fisher by the logarithm form; Monte Carlo by the affine identity.
derive(
    "alt_r20_c_running_factor_and_affine_monte_carlo.py",
    [
        (
            "        flows = [cf / (1.0 + inflation) ** t for t, cf in enumerate(flows)]\n",
            "        factor = 1.0\n        out = [flows[0]]\n        for cf in flows[1:]:\n            factor = factor * (1.0 + inflation)\n            out.append(cf / factor)\n        flows = out\n",
        ),
        (
            "    return (1.0 + real) * (1.0 + inflation) - 1.0\n",
            "    import math as _m\n\n    return _m.expm1(_m.log1p(real) + _m.log1p(inflation))\n",
        ),
        (
            "    rng = random.Random(seed)\n    out: list[float] = []\n    for _ in range(n_draws):\n        z = rng.gauss(0.0, 1.0)\n        m = math.exp(volatility * z - volatility * volatility / 2.0)\n        scaled = dict(project)\n        scaled[\"revenue\"] = [m * float(x) for x in project[\"revenue\"]]\n        out.append(npv(rate, after_tax_cash_flows(scaled)))\n    return out",
            "    rng = random.Random(seed)\n    zero = dict(project)\n    zero[\"revenue\"] = [0.0 for _ in project[\"revenue\"]]\n    at_zero = npv(rate, after_tax_cash_flows(zero))\n    at_one = npv(rate, after_tax_cash_flows(project))\n    out: list[float] = []\n    for _ in range(n_draws):\n        z = rng.gauss(0.0, 1.0)\n        m = math.exp(volatility * z - volatility * volatility / 2.0)\n        out.append(at_zero + (at_one - at_zero) * m)\n    return out",
        ),
    ],
    "Alternative correct engine (round 20): running discount factor for real flows; Fisher by logarithms; Monte Carlo by the affine identity.",
)
print("written")
