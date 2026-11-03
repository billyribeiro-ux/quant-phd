"""Build five correct alternative engines (round 2) as reference.py plus overriding definitions at the end.

Each alternative is a different style of a correct implementation (VERIFIER_RULES 2.6, plan 5.1):
alt1 Richardson-extrapolated central difference; alt2 complex-step derivative in ad_derivative;
alt3 reverse-mode automatic differentiation on a tape; alt4 closed-form sensitivities by a running recursion;
alt5 NumPy-vectorized price and sensitivities. Usage: python3 -I make_alts.py <checkout>
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path(root / "ledgers/M2/scripts/M2-e-r2/alts")
out.mkdir(parents=True, exist_ok=True)

ALT1 = '''

# ---- alt1: Richardson-extrapolated central difference (overrides fd_derivative) ----
def fd_derivative(f, x, h, scheme):
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        def central(s):
            return (f(x + s) - f(x - s)) / (2 * s)
        return (4.0 * central(step / 2) - central(step)) / 3.0
    raise ValueError("scheme must be 'forward' or 'central'")
'''

ALT2 = '''

# ---- alt2: complex-step derivative (overrides ad_derivative) ----
def ad_derivative(f, x):
    h = 1e-20
    z = f(complex(float(x), h))
    if isinstance(z, complex):
        return float(z.imag / h)
    return 0.0
'''

ALT3 = '''

# ---- alt3: reverse-mode automatic differentiation on a tape (overrides ad_derivative) ----
class _Var:
    __slots__ = ("value", "parents")

    def __init__(self, value, parents=()):
        self.value = float(value)
        self.parents = parents  # tuple of (parent _Var, local partial)

    def __add__(self, other):
        if isinstance(other, _Var):
            return _Var(self.value + other.value, ((self, 1.0), (other, 1.0)))
        return _Var(self.value + float(other), ((self, 1.0),))

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, _Var):
            return _Var(self.value - other.value, ((self, 1.0), (other, -1.0)))
        return _Var(self.value - float(other), ((self, 1.0),))

    def __rsub__(self, other):
        return _Var(float(other) - self.value, ((self, -1.0),))

    def __mul__(self, other):
        if isinstance(other, _Var):
            return _Var(self.value * other.value, ((self, other.value), (other, self.value)))
        return _Var(self.value * float(other), ((self, float(other)),))

    __rmul__ = __mul__


def ad_derivative(f, x):
    root = _Var(float(x))
    result = f(root)
    if not isinstance(result, _Var):
        return 0.0
    order, seen = [], set()

    def visit(node):
        if id(node) in seen:
            return
        seen.add(id(node))
        for parent, _ in node.parents:
            visit(parent)
        order.append(node)

    visit(result)
    adjoint = {id(result): 1.0}
    for node in reversed(order):
        a = adjoint.get(id(node), 0.0)
        for parent, partial in node.parents:
            adjoint[id(parent)] = adjoint.get(id(parent), 0.0) + a * partial
    return float(adjoint.get(id(root), 0.0))
'''

ALT4 = '''

# ---- alt4: closed-form sensitivities by a running recursion (overrides sensitivities and bond_price_cents) ----
def _recursive_sums(instance):
    flows, rate = _cash_flows(instance)
    v = 1 / (1 + rate)
    price = 0.0
    first = 0.0
    second = 0.0
    vt = 1.0  # v**t, built up by repeated multiplication
    for t, cash in flows:
        vt = vt * v
        price += cash * vt
        first -= t * cash * vt * v
        second += t * (t + 1) * cash * vt * v * v
    return price, first, second


def bond_price_cents(instance):
    price, _, _ = _recursive_sums(instance)
    return round(price)


def sensitivities(instance):
    price, first, second = _recursive_sums(instance)
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
'''

ALT5 = '''

# ---- alt5: NumPy-vectorized price and sensitivities (overrides bond_price_cents and sensitivities) ----
import numpy as np


def _vector_sums(instance):
    rate = _yield_rate(instance)
    flows, _ = _cash_flows(instance)
    t = np.array([float(k) for k, _ in flows])
    cash = np.array([c for _, c in flows], dtype=float)
    v = 1.0 / (1.0 + rate)
    d = v ** t
    price = float(np.dot(cash, d))
    first = float(-np.dot(t * cash, d * v))
    second = float(np.dot(t * (t + 1.0) * cash, d * v * v))
    return price, first, second


def bond_price_cents(instance):
    price, _, _ = _vector_sums(instance)
    return round(price)


def sensitivities(instance):
    price, first, second = _vector_sums(instance)
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
'''

for name, block in (
    ("alt1_richardson_central.py", ALT1),
    ("alt2_complex_step_ad.py", ALT2),
    ("alt3_reverse_mode_ad.py", ALT3),
    ("alt4_recursive_sensitivities.py", ALT4),
    ("alt5_numpy_vectorized.py", ALT5),
):
    (out / name).write_text(ref + block, encoding="utf-8")
print("alts written:", sorted(p.name for p in out.glob("alt*.py")))
