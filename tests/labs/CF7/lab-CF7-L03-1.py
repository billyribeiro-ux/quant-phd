"""Lab CF7-L03-1: Revolver Circularity: Iteration vs. Closed Form.

Demonstrates the resolution of circular interest dependencies between revolver borrowing,
net interest expense, earnings before tax, and operating cash flow using both
Gauss-Seidel fixed-point iteration and the exact analytical closed form.
"""

from __future__ import annotations


def solve_revolver_iterative(
    c_min: float,
    c_prev: float,
    r_prev: float,
    cf_core: float,
    r_rate: float,
    c_rate: float,
    tax_rate: float,
    term_int: float,
    ebit: float,
    depr: float,
    delta_nwc: float,
    capex: float,
    term_amort: float,
    div_rate: float = 0.0,
    tol: float = 1e-12,
    max_iter: int = 100,
) -> tuple[float, float, int]:
    """Resolve circularity via fixed-point iteration."""
    r_curr = r_prev
    iterations = 0

    for _k in range(max_iter):
        iterations += 1
        r_bar = 0.5 * (r_prev + r_curr)
        c_bar = 0.5 * (c_prev + c_min)
        net_int = term_int + r_rate * r_bar - c_rate * c_bar
        ebt = ebit - net_int
        tax = tax_rate * max(0.0, ebt)
        ni = ebt - tax
        div = div_rate * ni

        cfo = ni + depr - delta_nwc
        cfi = -capex
        cff = -term_amort - div + (r_curr - r_prev)
        c_projected = c_prev + cfo + cfi + cff

        # Update revolver to restore cash to c_min
        r_next = r_curr + (c_min - c_projected)
        diff = abs(r_next - r_curr)
        r_curr = r_next
        if diff < tol:
            break

    return r_curr, c_min, iterations


def solve_revolver_closed_form(
    c_min: float,
    c_prev: float,
    r_prev: float,
    cf_core: float,
    r_rate: float,
    c_rate: float,
    tax_rate: float,
    div_rate: float = 0.0,
) -> tuple[float, float]:
    """Resolve circularity via exact algebraic closed form."""
    alpha = (1.0 - div_rate) * (1.0 - tax_rate)
    c_bar = 0.5 * (c_prev + c_min)
    num = (c_min - c_prev) - cf_core - alpha * c_rate * c_bar + r_prev * (1.0 + 0.5 * alpha * r_rate)
    den = 1.0 - 0.5 * alpha * r_rate
    r_closed = num / den
    return r_closed, c_min


def main() -> None:
    c_min = 30.0
    c_prev = 20.0
    r_prev = 15.0
    ebit = 35.0
    term_int = 3.0
    depr = 8.0
    delta_nwc = 6.0
    capex = 22.0
    term_amort = 5.0
    tax_rate = 0.25
    r_rate = 0.08
    c_rate = 0.02
    div_rate = 0.10

    alpha = (1.0 - div_rate) * (1.0 - tax_rate)
    cf_core = alpha * (ebit - term_int) + depr - delta_nwc - capex - term_amort

    r_iter, _c_iter, iters = solve_revolver_iterative(
        c_min=c_min,
        c_prev=c_prev,
        r_prev=r_prev,
        cf_core=cf_core,
        r_rate=r_rate,
        c_rate=c_rate,
        tax_rate=tax_rate,
        term_int=term_int,
        ebit=ebit,
        depr=depr,
        delta_nwc=delta_nwc,
        capex=capex,
        term_amort=term_amort,
        div_rate=div_rate,
    )

    r_closed, _c_closed = solve_revolver_closed_form(
        c_min=c_min,
        c_prev=c_prev,
        r_prev=r_prev,
        cf_core=cf_core,
        r_rate=r_rate,
        c_rate=c_rate,
        tax_rate=tax_rate,
        div_rate=div_rate,
    )

    discrepancy = abs(r_closed - r_iter)
    print("Iterative Revolver Balance:", f"{r_iter:.6f}")
    print("Closed-Form Revolver Balance:", f"{r_closed:.6f}")
    print("Iteration Count:", str(iters))
    print("Absolute Discrepancy:", f"{discrepancy:.14f}")


main()
