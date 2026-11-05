"""Write five correct alternative implementations of the M2 sensitivity engine (each a different algorithm or style).

Each alternative is the reference with one part replaced. Output: <outdir>/alt<k>/sensitivity_engine.py.
"""
import pathlib
import sys

ref = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old[:60]
    return text.replace(old, new)


def fn_block(text: str, name: str) -> tuple[int, int]:
    start = text.index(f"def {name}(")
    nxt = text.find("\ndef ", start + 1)
    nxt2 = text.find("\nclass ", start + 1)
    ends = [e for e in (nxt, nxt2) if e != -1]
    return start, min(ends) if ends else len(text)


def swap_fn(text: str, name: str, body: str) -> str:
    s, e = fn_block(text, name)
    return text[:s] + body.strip("\n") + "\n\n\n" + text[e:].lstrip("\n")


alts = {}

# alt1: Richardson-extrapolated central estimate (accepted per page), other parts reference.
alts["alt1_richardson_central"] = swap_fn(
    ref,
    "fd_derivative",
    '''
def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """Forward quotient, or the Richardson extrapolation of two central quotients at steps h and h/2."""
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        d1 = (f(x + step) - f(x - step)) / (2 * step)
        d2 = (f(x + step / 2) - f(x - step / 2)) / step
        return float((4 * d2 - d1) / 3)
    raise ValueError("scheme must be 'forward' or 'central'")
''',
)

# alt2: complex-step derivative for ad_derivative (accepted per page), others reference.
alts["alt2_complex_step_ad"] = swap_fn(
    ref,
    "ad_derivative",
    '''
def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    """The derivative by the complex step: Im f(x + i h) / h with h = 1e-30, for a function real on the real line."""
    step = 1e-30
    value = f(complex(float(x), step))
    return float(complex(value).imag / step)
''',
)

# alt3: exact rational price and sensitivities (accepted per page), others reference.
alts["alt3_exact_rational_price"] = swap_fn(
    ref,
    "bond_price_cents",
    '''
def bond_price_cents(instance: dict[str, Any]) -> int:
    """The price in exact rational arithmetic, rounded half to even by round() on a Fraction."""
    from fractions import Fraction

    rate = _yield_rate(instance)
    face = Fraction(instance["face_cents"])
    coupon = face * Fraction(instance["coupon_bps"], 10_000)
    years = int(instance["maturity_years"])
    v = 1 / (1 + Fraction(instance["yield_bps"], 10_000))
    total = sum(((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1)), Fraction(0))
    del rate
    return round(total)
''',
)

# alt4: price by backward recurrence, sensitivities by a numpy dot product (different summation order).
alts["alt4_backward_recurrence_numpy"] = swap_fn(
    ref,
    "sensitivities",
    '''
def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    """The sensitivities by numpy dot products over the cash flows (a different summation order)."""
    import numpy as np

    flows, rate = _cash_flows(instance)
    t = np.array([float(k) for k, _ in flows])
    cash = np.array([c for _, c in flows])
    v = 1.0 / (1.0 + rate)
    price = float(np.dot(cash, v**t))
    first = float(-np.dot(t * cash, v ** (t + 1)))
    second = float(np.dot(t * (t + 1) * cash, v ** (t + 2)))
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
''',
)

# alt5: fsum in the forward numerator and the effective step (x + h) - x, the step as it is represented.
alts["alt5_effective_step_fsum"] = swap_fn(
    ref,
    "fd_derivative",
    '''
def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """Forward and central quotients with the represented step (x + h) - x, and math.fsum for the numerator."""
    import math

    step = _positive_step(h)
    if scheme == "forward":
        eff = ((x + step) - x) or step
        return math.fsum([f(x + step), -f(x)]) / eff
    if scheme == "central":
        eff = ((x + step) - (x - step)) or 2 * step
        return math.fsum([f(x + step), -f(x - step)]) / eff
    raise ValueError("scheme must be 'forward' or 'central'")
''',
)

for name, text in alts.items():
    d = out / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "sensitivity_engine.py").write_text(text, encoding="utf-8")
    print("wrote", d / "sensitivity_engine.py")
