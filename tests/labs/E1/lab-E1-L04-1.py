"""E1 L04 lab 1: a demand-intercept shift in a market with linear demand and quadratic supply.

Inputs are illustrative parameters, not data. Demand is Q_d(p) = a - b p units, with a = 120 units, b = 2 units per
cent. Supply is Q_s(p) = d p^2 units, with d = 1 unit per cent squared. The price p is in cents per unit. No random
draws are used, and no file is read.

The equilibrium price p(a) is the positive root of a - b p = d p^2, namely p(a) = (-b + S) / (2 d) with
S = sqrt(b^2 + 4 a d). Part A prints the equilibrium at a = 120 and checks that demand equals supply there.
Part B prints the implicit-function derivative dp/da = -F_a / F_p, for F(p, a) = a - b p - d p^2, beside the
derivative of the closed form, and the elasticity of the equilibrium price with respect to a.
Part C prints forward and central finite-difference quotients of p(a) at a = 120 for step sizes 1, 0.1, 0.01 and
0.001, with the error of each against dp/da.
Part D prints the price elasticities of demand and supply at the equilibrium.

Every value is a Decimal computed at 50 significant digits. Errors are printed in scientific notation.
"""

from __future__ import annotations

from decimal import Decimal, getcontext

getcontext().prec = 50

A_INTERCEPT = Decimal(120)
B_SLOPE = Decimal(2)
D_SUPPLY = Decimal(1)
STEPS = (Decimal(1), Decimal("0.1"), Decimal("0.01"), Decimal("0.001"))


def equilibrium_price(a: Decimal) -> Decimal:
    """The positive root of a - b p - d p^2 = 0, in cents per unit, for demand intercept a."""
    return (-B_SLOPE + (B_SLOPE * B_SLOPE + 4 * a * D_SUPPLY).sqrt()) / (2 * D_SUPPLY)


def demand(price: Decimal, a: Decimal) -> Decimal:
    """Quantity demanded in units at a price in cents per unit: a - b p."""
    return a - B_SLOPE * price


def supply(price: Decimal) -> Decimal:
    """Quantity supplied in units at a price in cents per unit: d p^2."""
    return D_SUPPLY * price * price


def implicit_derivative(price: Decimal) -> Decimal:
    """dp/da = -F_a / F_p at the equilibrium, with F_a = 1 and F_p = -(b + 2 d p) for F = a - b p - d p^2."""
    return 1 / (B_SLOPE + 2 * D_SUPPLY * price)


def closed_form_derivative(a: Decimal) -> Decimal:
    """d/da of p(a) = (-b + S) / (2 d). Since dS/da = 2 d / S, the derivative is 1 / S with S = sqrt(b^2 + 4 a d)."""
    return 1 / (B_SLOPE * B_SLOPE + 4 * a * D_SUPPLY).sqrt()


def main() -> None:
    """Print Parts A to D. Each line is a fixed label or a number, so the output is reproducible."""
    print("Part A: equilibrium at demand intercept a = 120")
    p0 = equilibrium_price(A_INTERCEPT)
    q0 = demand(p0, A_INTERCEPT)
    print(f"equilibrium_price_cents {p0:.10f}")
    print(f"equilibrium_quantity {q0:.10f}")
    print(f"supply_at_equilibrium {supply(p0):.10f}")
    print(f"demand_equals_supply {abs(q0 - supply(p0)) < Decimal('1e-30')}")

    print("Part B: implicit-function derivative dp/da beside the derivative of the closed form")
    dp_implicit = implicit_derivative(p0)
    dp_closed = closed_form_derivative(A_INTERCEPT)
    print(f"dp_da_implicit {dp_implicit:.10f}")
    print(f"dp_da_closed_form {dp_closed:.10f}")
    print(f"implicit_equals_closed_form {abs(dp_implicit - dp_closed) < Decimal('1e-30')}")
    print(f"price_elasticity_of_equilibrium_in_a {A_INTERCEPT / p0 * dp_implicit:.10f}")

    print("Part C: finite-difference quotients of p(a) at a = 120 against dp/da")
    for h in STEPS:
        upper = equilibrium_price(A_INTERCEPT + h)
        lower = equilibrium_price(A_INTERCEPT - h)
        forward = (upper - p0) / h
        central = (upper - lower) / (2 * h)
        print(
            f"step {h} forward {forward:.10f} forward_error {abs(forward - dp_implicit):.6e} "
            f"central {central:.10f} central_error {abs(central - dp_implicit):.6e}"
        )

    print("Part D: price elasticities at the equilibrium")
    demand_elasticity = -B_SLOPE * p0 / demand(p0, A_INTERCEPT)
    supply_elasticity = (2 * D_SUPPLY * p0) * p0 / supply(p0)
    print(f"demand_elasticity {demand_elasticity:.10f}")
    print(f"supply_elasticity {supply_elasticity:.10f}")


main()
