"""Write three alternative correct implementations of the M2 contract, each a different valid algorithm, into a scratch dir."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
ref = (ROOT / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
OUT.mkdir(parents=True, exist_ok=True)

def edit(src, pairs):
    for old, new in pairs:
        assert src.count(old) == 1, old[:60]
        src = src.replace(old, new)
    return src

# alt1: central estimate by Richardson extrapolation of two central quotients; ad_derivative by the complex step.
alt1 = edit(ref, [
    ('    return (f(x + step) - f(x - step)) / (2 * step)\n    raise',
     '    return (4 * ((f(x + step / 2) - f(x - step / 2)) / step) - (f(x + step) - f(x - step)) / (2 * step)) / 3\n    raise'),
    ('    result = _lift(f(_Dual(float(x), 1.0)))\n    return float(result.dot)',
     '    return complex(f(complex(float(x), 1e-20))).imag / 1e-20'),
])
(OUT / "alt1_richardson_and_complex_step.py").write_text(alt1, encoding="utf-8")

# alt2: exact rational arithmetic for the price and the sensitivities; the sensitivities as floats of the exact sums.
alt2 = edit(ref, [
    ('    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    return round(price)',
     '    face = Fraction(instance["face_cents"])\n    coupon = face * instance["coupon_bps"] / 10_000\n    years = int(instance["maturity_years"])\n    if int(instance["yield_bps"]) <= -10_000:\n        raise ValueError("the yield must be above -1 (-10000 basis points)")\n    v = 1 / (1 + Fraction(instance["yield_bps"], 10_000))\n    price = sum(((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1)), Fraction(0))\n    return round(price)'),
    ('    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    first = -sum(t * cash * v ** (t + 1) for t, cash in flows)\n    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)',
     '    _yield_rate(instance)\n    face = Fraction(instance["face_cents"])\n    coupon = face * instance["coupon_bps"] / 10_000\n    years = int(instance["maturity_years"])\n    v = 1 / (1 + Fraction(instance["yield_bps"], 10_000))\n    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]\n    price = sum((cash * v**t for t, cash in flows), Fraction(0))\n    first = -sum((t * cash * v ** (t + 1) for t, cash in flows), Fraction(0))\n    second = sum((t * (t + 1) * cash * v ** (t + 2) for t, cash in flows), Fraction(0))\n    price, first, second = float(price), float(first), float(second)'),
])
alt2 = alt2.replace("from collections.abc import Callable\n", "from collections.abc import Callable\nfrom fractions import Fraction\n", 1)
(OUT / "alt2_exact_rational_price.py").write_text(alt2, encoding="utf-8")

# alt3: Hessian as the central difference of the central first derivative (a different formula for the mixed entries),
# and the cash-flow sum by math.fsum.
alt3 = edit(ref, [
    ('        for j in range(i + 1, n):\n            mixed = (\n                f(_moved(base, {i: step, j: step}))\n                - f(_moved(base, {i: step, j: -step}))\n                - f(_moved(base, {i: -step, j: step}))\n                + f(_moved(base, {i: -step, j: -step}))\n            )\n            hessian[i][j] = mixed / (4 * step * step)\n            hessian[j][i] = hessian[i][j]',
     '        for j in range(i + 1, n):\n            def grad_i(p: list[float]) -> float:\n                return (f(_moved(p, {i: step})) - f(_moved(p, {i: -step}))) / (2 * step)\n            mixed = (grad_i(_moved(base, {j: step})) - grad_i(_moved(base, {j: -step}))) / (2 * step)\n            hessian[i][j] = mixed\n            hessian[j][i] = hessian[i][j]'),
    ('    price = sum(cash * v**t for t, cash in flows)\n    return round(price)',
     '    import math\n    price = math.fsum(cash * v**t for t, cash in flows)\n    return round(price)'),
])
(OUT / "alt3_hessian_by_gradient_and_fsum.py").write_text(alt3, encoding="utf-8")
print("wrote", sorted(p.name for p in OUT.iterdir()))
