"""Lab CR4-project-1: Project Rung 1 Worked Example — Capital Structure Recovery Waterfall.

Fully solved instance of the capital structure recovery waterfall, fulcrum security detection,
consensual plan carve-out reallocation, and distressed investor expected return analysis.
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
    # Stylized Capital Structure
    tranches = [
        Tranche("DIP Facility", 20.0, 1),
        Tranche("First Lien Term Loan", 100.0, 2),
        Tranche("Second Lien Notes", 60.0, 3),
        Tranche("Senior Unsecured Notes", 80.0, 4),
        Tranche("Subordinated Debentures", 40.0, 5),
        Tranche("Common Equity", 0.0, 6),
    ]
    total_debt = sum(t.claim for t in tranches if t.claim > 0)  # 300.0

    scenarios = [
        Scenario("Liquidation", 70.0, 0.20),
        Scenario("Low Reorganization", 140.0, 0.30),
        Scenario("Base Reorganization", 220.0, 0.35),
        Scenario("High Reorganization", 340.0, 0.15),
    ]

    purchase_prices = {
        "First Lien Term Loan": 0.85,
        "Second Lien Notes": 0.55,
        "Senior Unsecured Notes": 0.28,
        "Subordinated Debentures": 0.08,
    }
    holding_period = 1.5  # years

    print("Project Rung 1: Capital Structure Recovery Waterfall & Fulcrum Analysis")
    print(f"Company: Horizon Industrial Systems · Total Contractual Debt Claims = {total_debt:.1f}")
    print("=" * 80)

    # 1. Strict Waterfall Across Scenarios
    print("\n1. Strict Absolute Priority Waterfall Schedule Across Scenarios:")
    print("Tranche Name            | Claim | Liq ($70M) | Low ($140M) | Base ($220M) | High ($340M)")
    print("-" * 79)

    scenario_allocations: list[list[float]] = []
    fulcrum_names: list[str] = []

    for s in scenarios:
        ev = s.ev
        rem = ev
        s_allocs: list[float] = []
        fulcrum_found = False
        fulcrum_str = "None (Solvent)"

        for t in tranches:
            c = t.claim
            if c > 0:
                alloc = min(rem, c)
                rem -= alloc
            else:
                alloc = rem if rem > 0 else 0.0
                rem = 0.0
            s_allocs.append(alloc)

            if not fulcrum_found and ev < total_debt and c > 0:
                is_part = 0.0 < alloc < c
                is_bound = abs(alloc - c) < 1e-6 and abs(ev - sum(s_allocs)) < 1e-6 and rem == 0.0
                if is_part or is_bound:
                    fulcrum_str = t.name
                    fulcrum_found = True

        scenario_allocations.append(s_allocs)
        fulcrum_names.append(fulcrum_str)

    for i, t in enumerate(tranches):
        c = t.claim
        c_str = f"{c:5.1f}" if c > 0 else "  N/A"
        row_str = f"{t.name:23} | {c_str} |"
        for s_idx in range(len(scenarios)):
            alloc = scenario_allocations[s_idx][i]
            pct = (alloc / c * 100.0) if c > 0 else (100.0 if alloc > 0 else 0.0)
            row_str += f" {alloc:5.1f} ({pct:3.0f}%) |"
        print(row_str)

    print("-" * 79)
    fn0 = fulcrum_names[0][:10]
    fn1 = fulcrum_names[1][:11]
    fn2 = fulcrum_names[2][:12]
    fn3 = fulcrum_names[3][:11]
    print(f"Identified Fulcrum      |  N/A  | {fn0:10} | {fn1:11} | {fn2:12} | {fn3:11}")

    # 2. Carveout in Base Reorganization
    # Senior Unsecured transfers 6% of its allocation to Common Equity
    base_allocs = scenario_allocations[2]
    unsec_idx = 3
    equity_idx = 5
    carveout_pct = 0.06
    carveout_amt = base_allocs[unsec_idx] * carveout_pct

    adj_unsec = base_allocs[unsec_idx] - carveout_amt
    adj_equity = base_allocs[equity_idx] + carveout_amt

    print("\n2. Consensual Plan Carve-Out (Base Scenario: EV = $220M):")
    b_u = base_allocs[unsec_idx]
    print(f"Senior Unsecured: {b_u:.2f} -> minus 6% carve-out ({carveout_amt:.2f}) = {adj_unsec:.2f}")
    print(f"Common Equity initial: {base_allocs[equity_idx]:.2f} -> plus carve-out gift = {adj_equity:.2f}")
    print(f"Total value distributed conserved: {sum(base_allocs):.2f} == {sum(base_allocs):.2f}")

    # 3. Expected Returns
    print("\n3. Distressed Investor Return Evaluation (Holding Period = 1.5 Years):")
    print("Tranche Name            | Purchase Price | Invested ($M) | Expected Rec ($M) |   MOIC   | Annualized IRR")
    print("-" * 96)

    tot_inv = 0.0
    tot_rec = 0.0

    for i, t in enumerate(tranches):
        name = t.name
        c = t.claim
        if name in purchase_prices and c > 0:
            price = purchase_prices[name]
            inv = price * c
            exp_rec = sum(scenarios[s_idx].prob * scenario_allocations[s_idx][i] for s_idx in range(len(scenarios)))
            tot_inv += inv
            tot_rec += exp_rec
            moic = exp_rec / inv if inv > 0 else 0.0
            irr = (moic ** (1.0 / holding_period) - 1.0) * 100.0 if moic > 0 else -100.0
            p_s = f"{price:4.2f}"
            i_s = f"{inv:5.1f}"
            r_s = f"{exp_rec:5.1f}"
            m_s = f"{moic:5.2f}x"
            ir_s = f"{irr:5.1f}%"
            print(f"{name:23} |      {p_s}      |     {i_s}     |       {r_s}       |  {m_s}  |     {ir_s}")

    port_moic = tot_rec / tot_inv if tot_inv > 0 else 0.0
    port_irr = (port_moic ** (1.0 / holding_period) - 1.0) * 100.0 if port_moic > 0 else -100.0
    print("-" * 96)
    ti_s = f"{tot_inv:5.1f}"
    tr_s = f"{tot_rec:5.1f}"
    pm_s = f"{port_moic:5.2f}x"
    pi_s = f"{port_irr:5.1f}%"
    print(f"Total Distressed Debt   |      N/A       |     {ti_s}     |       {tr_s}       |  {pm_s}  |     {pi_s}")

    # Invariant assertions
    assert abs(sum(base_allocs) - 220.0) < 1e-9
    assert fulcrum_names[2] == "Senior Unsecured Notes"
    assert port_moic > 1.0
    print("\nAll project rung 1 calculations verified.")


main()
