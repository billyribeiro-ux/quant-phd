"""AC2 L04 lab 1: the two operating-accrual measures on a SIMULATED two-year panel of firms.

SIMULATED: every firm is generated here from a seeded generator. No filing is read.
Units: currency units (CU) for every money item, and ratios are unitless.

The generator draws cash and the operating items for two year-ends, takes equity as the balance-sheet
residual (assets less liabilities), and derives net income from the change in equity plus distributions
(clean surplus). The cash-flow statement is then built from the balance-sheet changes, so the statements
articulate by construction. Scenario "clean" keeps non-current operating items and long-term debt unchanged;
scenario "moving" lets them move, which is where the two measures part company.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

F64 = NDArray[np.float64]


@dataclass(frozen=True)
class Panel:
    """Two year-ends (0 = lagged, 1 = current) for N firms, all money in CU."""

    cash0: F64
    cash1: F64
    ca_other0: F64  # receivables and inventories: current assets excluding cash
    ca_other1: F64
    cl0: F64
    cl1: F64
    ppe0: F64
    ppe1: F64
    onca0: F64  # other non-current operating assets
    onca1: F64
    oncl0: F64  # other non-current operating liabilities
    oncl1: F64
    ltd0: F64  # long-term debt
    ltd1: F64
    ni: F64  # net income of the current year
    dep: F64  # depreciation of the current year
    capex: F64  # capital expenditure of the current year
    payout: F64  # net distributions to shareholders (dividends less issuance)


def total_assets(cash: F64, ca_other: F64, ppe: F64, onca: F64) -> F64:
    """Total assets in CU: cash + other current assets + PP&E + other non-current operating assets."""
    return cash + ca_other + ppe + onca


def build_panel(rng: np.random.Generator, n: int, moving: bool) -> Panel:
    """Generate n SIMULATED firm-years with articulated statements; moving=True lets non-current items move."""
    size = np.exp(rng.normal(np.log(1000.0), 0.6, n))  # scale of the firm in CU
    ca_other0 = size * rng.uniform(0.15, 0.30, n)
    ppe0 = size * rng.uniform(0.25, 0.50, n)
    onca0 = size * rng.uniform(0.05, 0.15, n)
    cl0 = size * rng.uniform(0.10, 0.20, n)
    ltd0 = size * rng.uniform(0.02, 0.12, n)
    oncl0 = size * rng.uniform(0.01, 0.04, n)
    cash0 = size * rng.uniform(0.05, 0.15, n)

    dep = ppe0 * rng.uniform(0.06, 0.12, n)
    capex = ppe0 * rng.uniform(0.05, 0.15, n)
    ppe1 = ppe0 + capex - dep  # PP&E roll-forward
    cash1 = cash0 * np.exp(rng.normal(0.03, 0.15, n))  # positive by construction
    ca_other1 = ca_other0 * (1.0 + rng.normal(0.08, 0.10, n))
    cl1 = cl0 * (1.0 + rng.normal(0.05, 0.10, n))
    if moving:
        onca1 = onca0 * (1.0 + rng.normal(0.0, 0.20, n))
        oncl1 = oncl0 * (1.0 + rng.normal(0.0, 0.25, n))
        ltd1 = ltd0 * (1.0 + rng.normal(0.02, 0.10, n))
    else:
        onca1, oncl1, ltd1 = onca0.copy(), oncl0.copy(), ltd0.copy()
    payout = size * rng.normal(0.01, 0.02, n)  # net distributions to shareholders, CU

    # Balance sheet at year-end 1 fixes equity; clean surplus then gives net income: NI = dE + payout.
    equity0 = total_assets(cash0, ca_other0, ppe0, onca0) - (cl0 + ltd0 + oncl0)
    equity1 = total_assets(cash1, ca_other1, ppe1, onca1) - (cl1 + ltd1 + oncl1)
    if np.any(equity1 <= 0.0):
        raise ValueError("generator produced non-positive equity; check the balance-sheet draws")
    ni = equity1 - equity0 + payout
    return Panel(
        cash0=cash0,
        cash1=cash1,
        ca_other0=ca_other0,
        ca_other1=ca_other1,
        cl0=cl0,
        cl1=cl1,
        ppe0=ppe0,
        ppe1=ppe1,
        onca0=onca0,
        onca1=onca1,
        oncl0=oncl0,
        oncl1=oncl1,
        ltd0=ltd0,
        ltd1=ltd1,
        ni=ni,
        dep=dep,
        capex=capex,
        payout=payout,
    )


def average_total_assets(p: Panel) -> F64:
    """Mean of the two year-end total-asset balances in CU, the scale of both accrual measures."""
    ta0 = total_assets(p.cash0, p.ca_other0, p.ppe0, p.onca0)
    ta1 = total_assets(p.cash1, p.ca_other1, p.ppe1, p.onca1)
    return (ta0 + ta1) / 2.0


def cfo_from_balance_sheet(p: Panel) -> F64:
    """Operating cash flow in CU by the cash-flow identity: CFO = d(cash) + capex - d(LTD) + payout."""
    return (p.cash1 - p.cash0) + p.capex - (p.ltd1 - p.ltd0) + p.payout


def cfo_indirect(p: Panel) -> F64:
    """Operating cash flow in CU by the indirect method: NI + D&A - d(other CA) + d(CL) - d(ONCA) + d(ONCL)."""
    return p.ni + p.dep - (p.ca_other1 - p.ca_other0) + (p.cl1 - p.cl0) - (p.onca1 - p.onca0) + (p.oncl1 - p.oncl0)


def accruals_cash_flow(p: Panel) -> F64:
    """(NI - CFO) / average total assets, the cash-flow measure of the A15 contract."""
    return (p.ni - cfo_from_balance_sheet(p)) / average_total_assets(p)


def accruals_balance_sheet(p: Panel) -> F64:
    """Sloan-style balance-sheet accruals over average total assets, the A15 contract's definition."""
    # current assets less cash: d(CA) - d(cash) = d(other current assets), since CA = cash + other current assets
    d_ca_less_cash = p.ca_other1 - p.ca_other0
    d_cl = p.cl1 - p.cl0
    return (d_ca_less_cash - d_cl - p.dep) / average_total_assets(p)


def describe(name: str, x: F64) -> str:
    """One printed line: mean and standard deviation of a ratio, to four decimals."""
    return f"{name:<28} mean {x.mean():+.4f}  sd {x.std(ddof=1):.4f}"


def main() -> None:
    n = 400
    clean = build_panel(np.random.default_rng(2604), n, moving=False)
    moving = build_panel(np.random.default_rng(2604), n, moving=True)

    # 1. Articulation: the indirect method reproduces the cash-flow identity to floating-point precision.
    art = float(np.max(np.abs(cfo_indirect(clean) - cfo_from_balance_sheet(clean))))
    print(f"articulation_max_abs_residual_clean {art:.6f}")
    art_m = float(np.max(np.abs(cfo_indirect(moving) - cfo_from_balance_sheet(moving))))
    print(f"articulation_max_abs_residual_moving {art_m:.6f}")

    # 2. Clean scenario: the two measures coincide, because the gap is d(ONCA) - d(ONCL) by identity.
    cf_c = accruals_cash_flow(clean)
    bs_c = accruals_balance_sheet(clean)
    avg_c = average_total_assets(clean)
    # Identity: (NI - CFO) - [d(CA) - d(cash) - d(CL) - D&A] = d(ONCA) - d(ONCL), in CU.
    identity_c = (cf_c - bs_c) * avg_c - ((clean.onca1 - clean.onca0) - (clean.oncl1 - clean.oncl0))
    print(f"clean_identity_max_abs_residual {float(np.max(np.abs(identity_c))):.6f}")
    print(f"clean_max_abs_difference {float(np.max(np.abs(cf_c - bs_c))):.6f}")

    # 3. Moving scenario: the gap is exactly the non-current operating items, and the measures diverge.
    cf_m = accruals_cash_flow(moving)
    bs_m = accruals_balance_sheet(moving)
    avg = average_total_assets(moving)
    identity_m = (cf_m - bs_m) * avg - ((moving.onca1 - moving.onca0) - (moving.oncl1 - moving.oncl0))
    print(f"moving_identity_max_abs_residual {float(np.max(np.abs(identity_m))):.6f}")
    print(describe("cash_flow_accruals_moving", cf_m))
    print(describe("balance_sheet_accruals_moving", bs_m))
    print(f"correlation_moving {float(np.corrcoef(cf_m, bs_m)[0, 1]):.4f}")
    print(f"share_of_firms_gap_above_0.01 {float(np.mean(np.abs(cf_m - bs_m) > 0.01)):.4f}")


main()
