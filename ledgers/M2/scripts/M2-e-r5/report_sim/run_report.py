"""
The bond is SIMULATED, not market data: face value 2500000 cents (25000.00), an annual coupon of 6.00 %, twelve
annual payments, and a yield of 5.00 %. The program prints the unrounded price, the analytic dP/dy with its forward
and central differences over a sweep of steps from 1e-1 to 1e-12, the step with the smallest central error, the
observed orders from a tenfold cut in the step, a kink case |x - 0.3| at x = 0.3 by forward, backward and central
differences, and a cancellation case 1e8 + sin(x) at x = 0.5 by the central difference. Standard library only.
"""

import math
from collections.abc import Callable

from sensitivity_engine import fd_derivative, sensitivities

Flow = tuple[int, float]


def bond_price(flows: list[Flow], y: float) -> float:
    """The unrounded price in cents at the annual yield y."""
    v = 1 / (1 + y)
    return sum(cash * v**t for t, cash in flows)


def difference(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """Replaced by fd_derivative (the page rule)."""
    return fd_derivative(f, x, h, scheme)


def main() -> None:
    face_cents = 2_500_000  # SIMULATED face value, 25000.00 in cents
    coupon = face_cents * 0.06  # cents paid at the end of each year
    years = 12
    y = 0.05
    flows = [(t, coupon + (face_cents if t == years else 0)) for t in range(1, years + 1)]
    price = bond_price(flows, y)
    v = 1 / (1 + y)
    inst = {"face_cents": 2500000, "coupon_bps": 600, "maturity_years": 12, "yield_bps": 500}
    exact = sensitivities(inst)["dprice_dy"]
    print("unrounded price (cents):", f"{price:.4f}")
    print("rounded price (cents, half to even):", round(price))
    print("dP/dy analytic (cents per unit yield):", f"{exact:.6f}")

    def price_of(yield_rate: float) -> float:
        return bond_price(flows, yield_rate)

    steps = [10.0**-k for k in range(1, 13)]
    errors: dict[float, tuple[float, float]] = {}
    print("step h | forward error | central error")
    for h in steps:
        fwd = abs(difference(price_of, y, h, "forward") - exact)
        cen = abs(difference(price_of, y, h, "central") - exact)
        errors[h] = (fwd, cen)
        print(f"{h:.0e} | {fwd:.6e} | {cen:.6e}")
    best = min(steps, key=lambda h: errors[h][1])
    print("smallest central error at step:", f"{best:.0e}", "| error:", f"{errors[best][1]:.6e}")
    fwd_order = math.log10(errors[1e-2][0] / errors[1e-3][0])
    cen_order = math.log10(errors[1e-2][1] / errors[1e-3][1])
    print("observed order, forward (log10 of the error ratio, steps 1e-2 to 1e-3):", f"{fwd_order:.3f}")
    print("observed order, central (log10 of the error ratio, steps 1e-2 to 1e-3):", f"{cen_order:.3f}")

    def kink(x: float) -> float:
        return abs(x - 0.3)

    print("kink |x - 0.3| at x = 0.3, step 1e-3: forward", f"{difference(kink, 0.3, 1e-3, 'forward'):.1f}")
    print("kink at x = 0.3, step 1e-3: backward", f"{fd_derivative(kink, 0.3 - 1e-3, 1e-3, 'forward'):.1f}")
    print("kink at x = 0.3, step 1e-3: central", f"{difference(kink, 0.3, 1e-3, 'central'):.1f}")
    print("kink at x = 0.3, step 1e-6: central", f"{difference(kink, 0.3, 1e-6, 'central'):.1f}")

    def offset(x: float) -> float:
        return 1e8 + math.sin(x)

    truth = math.cos(0.5)
    print("cancellation 1e8 + sin(x) at x = 0.5, exact f' =", f"{truth:.10f}")
    for h in (1e-4, 1e-8, 1e-12):
        cen = difference(offset, 0.5, h, "central")
        print(f"cancellation, central at step {h:.0e}:", f"{cen:.6f}", "| error:", f"{abs(cen - truth):.2e}")


main()
