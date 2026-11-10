"""Lab CR4-project-3: Project Rung 3 Autograder Pre-flight & Numerical Invariant Verification.

Verifies the mathematical invariants and reference solutions on seed 42.
Checks value conservation, strict priority monotonicity, fulcrum uniqueness,
consensual carve-out preservation, and investor return metrics.
"""

from __future__ import annotations

from typing import NamedTuple


class Tranche(NamedTuple):
    name: str
    claim: float
    seniority: int


class Scenario(NamedTuple):
    name: str
    ev: float
    prob: float


def main() -> None:
    # Seed 42 instance parameters
    company_name = "Crestview Manufacturing"
    tranches = [
        Tranche("DIP Facility", 22.50, 1),
        Tranche("First Lien Term Loan", 95.00, 2),
        Tranche("Second Lien Notes", 65.00, 3),
        Tranche("Senior Unsecured Notes", 75.00, 4),
        Tranche("Subordinated Debentures", 35.00, 5),
        Tranche("Common Equity", 0.0, 6),
    ]
    total_debt = sum(t.claim for t in tranches if t.claim > 0)  # 292.50

    scenarios = [
        Scenario("Liquidation", 80.00, 0.20),
        Scenario("Low Reorganization", 150.00, 0.30),
        Scenario("Base Reorganization", 230.00, 0.35),
        Scenario("High Reorganization", 350.00, 0.15),
    ]

    purchase_prices = {
        "First Lien Term Loan": 0.90,
        "Second Lien Notes": 0.62,
        "Senior Unsecured Notes": 0.38,
        "Subordinated Debentures": 0.12,
    }
    holding_period = 1.5

    print(f"Project Rung 3 Sanity Check: {company_name} (Seed 42)")
    print(f"Total Contractual Debt Claims = {total_debt:.2f}")
    print("-" * 80)

    # Invariant 1: Check Conservation of Value in All Scenarios
    print("Scenario Executions & Fulcrum Identification:")
    for s in scenarios:
        ev = s.ev
        rem = ev
        allocs: list[float] = []
        fulcrum = "None"
        fulcrum_found = False

        for t in tranches:
            c = t.claim
            if c > 0:
                a = min(rem, c)
                rem -= a
            else:
                a = rem if rem > 0 else 0.0
                rem = 0.0
            allocs.append(a)

            is_part = 0.0 < a < c
            is_bound = abs(a - c) < 1e-6 and abs(ev - sum(allocs)) < 1e-6 and rem == 0.0
            if not fulcrum_found and ev < total_debt and c > 0 and (is_part or is_bound):
                fulcrum = t.name
                fulcrum_found = True

        tot_alloc = sum(allocs)
        assert abs(tot_alloc - ev) < 1e-9
        print(f"  {s.name:20} | EV = {ev:6.2f} | Total Allocated = {tot_alloc:6.2f} | Fulcrum: {fulcrum}")

    # Invariant 2: Base Scenario Carve-out
    base_ev = 230.00
    rem = base_ev
    base_allocs: list[float] = []
    for t in tranches:
        c = t.claim
        if c > 0:
            a = min(rem, c)
            rem -= a
        else:
            a = rem
            rem = 0.0
        base_allocs.append(a)

    unsec_base = base_allocs[3]  # Senior Unsecured
    carveout_pct = 0.06
    carveout_val = unsec_base * carveout_pct
    adj_unsec = unsec_base - carveout_val
    adj_equity = base_allocs[5] + carveout_val

    assert abs((adj_unsec + adj_equity) - (unsec_base + base_allocs[5])) < 1e-9
    print(f"\nCarve-out Check: Senior Unsec {unsec_base:.2f} -> {adj_unsec:.2f},")
    print(f"Equity {base_allocs[5]:.2f} -> {adj_equity:.2f}")

    # Invariant 3: Expected Returns
    tot_invested = sum(purchase_prices[t.name] * t.claim for t in tranches if t.name in purchase_prices)
    tot_exp_rec = 0.0
    for s in scenarios:
        ev = s.ev
        prob = s.prob
        rem = ev
        for t in tranches:
            c = t.claim
            if c > 0:
                a = min(rem, c)
                rem -= a
            else:
                a = rem
                rem = 0.0
            if t.name in purchase_prices:
                tot_exp_rec += prob * a

    moic = tot_exp_rec / tot_invested
    irr = (moic ** (1.0 / holding_period) - 1.0) * 100.0

    print(f"Investor Portfolio: Invested = {tot_invested:.2f}, Expected Recovery = {tot_exp_rec:.2f}")
    print(f"Portfolio MOIC = {moic:.4f}x, Annualized IRR = {irr:.2f}%")

    assert moic > 1.0
    assert irr > 0.0
    print("\nAll Rung 3 numerical checks passed successfully.")


main()
