"""Round-3 verifier: writes new student-error mutants (g01..g04) and three alternative correct
implementations (alt1..alt3) derived from grader/reference.py by exact text replacement.
Usage: python3 ledgers/M2/scripts/M2-e-r3/make_r3.py <checkout>   (writes into the checkout's ledgers/M2 and scripts dirs)
"""

import pathlib
import sys

ck = pathlib.Path(sys.argv[1])
ref = (ck / "course/modules/M/M2/grader/reference.py").read_text()
out_m = ck / "ledgers/M2/mutants"
out_a = ck / "ledgers/M2/scripts/M2-e-r3/alts"


def rep(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, (old[:60], src.count(old))
    return src.replace(old, new)


mutants = {
    "g01_forward_scheme_prints_a_trace.py": (
        "The forward branch of fd_derivative prints its estimate, which the specification forbids; the purity test only calls the central scheme.",
        [(
            '        return (f(x + step) - f(x)) / step\n    if scheme == "central":',
            '        est = (f(x + step) - f(x)) / step\n        print("forward estimate", est)\n        return est\n    if scheme == "central":',
        )],
    ),
    "g02_coupon_truncated_to_whole_cents.py": (
        "The annual coupon is truncated to whole cents before the cash flows are summed, so a fractional cent of coupon is lost each year.",
        [("    coupon = face * instance[\"coupon_bps\"] / 10_000\n", "    coupon = float(int(face * instance[\"coupon_bps\"] / 10_000))\n")],
    ),
    "g03_dprice_dy_numerical_not_formula.py": (
        "The second sensitivity is taken as a central second difference of the unrounded price at step 1e-3 instead of the stated sum t(t+1) C_t (1+y)^(-t-2).",
        [(
            '        "d2price_dy2": second,',
            '        "d2price_dy2": (sum(cash * (1 / (1 + rate + 1e-3)) ** t for t, cash in flows)'
            " - 2 * price + sum(cash * (1 / (1 + rate - 1e-3)) ** t for t, cash in flows)) / (1e-3 * 1e-3),",
        )],
    ),
    "g04_yield_check_uses_strict_inequality.py": (
        "The yield check refuses only a yield strictly below -1, so a yield of exactly -1 reaches the discount factor and fails with ZeroDivisionError instead of ValueError.",
        [("    if yield_bps <= -10_000:", "    if yield_bps < -10_000:")],
    ),
}
for name, (doc, reps) in mutants.items():
    src = ref
    for old, new in reps:
        src = rep(src, old, new)
    body = src.split('"""', 2)[2].lstrip("\n")  # drop the reference's module docstring; keep the code
    (out_m / name).write_text(f'"""{doc}"""\n' + body)

# Alternative correct implementations (none may fail the suite on seeds 0-49).
alt1 = ref
# Richardson-extrapolated central estimate (uses steps h and h/2), complex-step AD, exact Fraction price.
alt1 = rep(
    alt1,
    '        return (f(x + step) - f(x - step)) / (2 * step)\n    raise',
    "        c1 = (f(x + step) - f(x - step)) / (2 * step)\n"
    "        c2 = (f(x + step / 2) - f(x - step / 2)) / (step)\n"
    "        return (4 * c2 - c1) / 3\n    raise",
)
alt1 = rep(
    alt1,
    "    result = _lift(f(_Dual(float(x), 1.0)))\n    return float(result.dot)",
    "    step = 1e-30\n    return float(f(complex(float(x), step)).imag / step)",
)
alt1 = rep(
    alt1,
    "    price = sum(cash * v**t for t, cash in flows)\n    return round(price)",
    "    from fractions import Fraction\n    exact = sum((Fraction(cash) * Fraction(1, 1) / (1 + Fraction(instance['yield_bps'], 10_000)) ** t"
    " for t, cash in flows), Fraction(0))\n    return round(exact)",
)

# alt2: reference structure, sensitivities from exact Fraction arithmetic converted to float.
alt2 = rep(
    ref,
    "    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    first = -sum(t * cash * v ** (t + 1) for t, cash in flows)\n    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)\n",
    "    from fractions import Fraction\n    flows, rate = _cash_flows(instance)\n    yq = 1 / (1 + Fraction(instance['yield_bps'], 10_000))\n"
    "    price_q = sum((Fraction(c) * yq**t for t, c in flows), Fraction(0))\n"
    "    first_q = -sum((t * Fraction(c) * yq ** (t + 1) for t, c in flows), Fraction(0))\n"
    "    second_q = sum((t * (t + 1) * Fraction(c) * yq ** (t + 2) for t, c in flows), Fraction(0))\n"
    "    price, first, second = float(price_q), float(first_q), float(second_q)\n",
)
alt2 = rep(alt2, "    return round(price)", "    return round(Fraction(price))" if False else "    return round(price)")
(out_a / "alt2").mkdir(parents=True, exist_ok=True)
(out_a / "alt2" / "sensitivity_engine.py").write_text(alt2)

# alt3: Richardson-extrapolated Hessian entries (steps h and h/2) for the diagonal, reference mixed differences.
alt3 = rep(
    ref,
    "        hessian[i][i] = (up - 2 * f0 + down) / (step * step)\n",
    "        hessian[i][i] = (up - 2 * f0 + down) / (step * step)\n"
    "        up2 = f(_moved(base, {i: step / 2}))\n"
    "        down2 = f(_moved(base, {i: -step / 2}))\n"
    "        half = (up2 - 2 * f0 + down2) / ((step / 2) * (step / 2))\n"
    "        hessian[i][i] = (4 * half - hessian[i][i]) / 3\n",
)
(out_a / "alt3").mkdir(parents=True, exist_ok=True)
(out_a / "alt3" / "sensitivity_engine.py").write_text(alt3)
(out_a / "alt1").mkdir(parents=True, exist_ok=True)
(out_a / "alt1" / "sensitivity_engine.py").write_text(alt1)
print("wrote", sorted(mutants), "and alt1..alt3")
