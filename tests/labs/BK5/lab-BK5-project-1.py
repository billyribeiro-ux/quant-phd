"""Rung 1 worked example: household wealth plan and Monte Carlo withdrawal analysis, step by step.

Standard library only. All inputs are SIMULATED illustrative values.
Demonstrates human capital valuation, tax-optimal asset location, and moving-block bootstrap decumulation.
"""

import random


def main() -> None:
    # -------------------------------------------------------------
    # Step 1: Human Capital Valuation
    # -------------------------------------------------------------
    working_years = 25
    base_salary_cents = 10_000_000  # $100,000.00
    salary_growth = 0.015  # 1.5%
    discount_bps = 350  # 3.50%
    r = discount_bps / 10_000.0

    earnings_cents: list[int] = []
    curr = float(base_salary_cents)
    for _ in range(working_years):
        earnings_cents.append(round(curr))
        curr *= 1.0 + salary_growth

    human_capital_cents = round(sum(e / ((1.0 + r) ** t) for t, e in enumerate(earnings_cents, start=1)))
    print(f"Human capital PV: ${human_capital_cents / 100:,.2f} ({human_capital_cents} cents)")

    # -------------------------------------------------------------
    # Step 2: Optimal Asset Location
    # -------------------------------------------------------------
    total_wealth_cents = 100_000_000  # $1,000,000
    bond_target_cents = 40_000_000  # 40%

    taxable_cap_cents = 40_000_000  # $400k
    tda_cap_cents = 40_000_000  # $400k
    roth_cap_cents = 20_000_000  # $200k

    # Rule: Bonds to TDA first
    tda_bond = min(bond_target_cents, tda_cap_cents)
    rem_bond = bond_target_cents - tda_bond
    taxable_bond = min(rem_bond, taxable_cap_cents)
    roth_bond = rem_bond - taxable_bond

    tda_eq = tda_cap_cents - tda_bond
    taxable_eq = taxable_cap_cents - taxable_bond
    roth_eq = roth_cap_cents - roth_bond

    print(f"Location - Taxable: Equity ${taxable_eq / 100:,.0f} | Bond ${taxable_bond / 100:,.0f}")
    print(f"Location - TDA:     Equity ${tda_eq / 100:,.0f} | Bond ${tda_bond / 100:,.0f}")
    print(f"Location - Roth:    Equity ${roth_eq / 100:,.0f} | Bond ${roth_bond / 100:,.0f}")

    # -------------------------------------------------------------
    # Step 3: Moving-Block Bootstrap and Withdrawal Sustainability
    # -------------------------------------------------------------
    rng_hist = random.Random(101)
    hist_returns: list[float] = []
    prev_r = 0.05
    for _ in range(50):
        shock = rng_hist.gauss(0.0, 0.11)
        ret = 0.05 + 0.15 * (prev_r - 0.05) + shock
        hist_returns.append(round(ret, 4))
        prev_r = ret

    block_length = 5
    horizon = 30
    n_sims = 200
    rng_boot = random.Random(42)
    num_blocks = len(hist_returns) - block_length + 1

    paths: list[list[float]] = []
    for _ in range(n_sims):
        p: list[float] = []
        while len(p) < horizon:
            idx = rng_boot.randint(0, num_blocks - 1)
            p.extend(hist_returns[idx : idx + block_length])
        paths.append(p[:horizon])

    rates_bps = [350, 400, 450, 500]
    for w_bps in rates_bps:
        w_dollar = (total_wealth_cents * w_bps) // 10_000
        ruin_count = 0
        terminal_wealths: list[float] = []
        for path in paths:
            w = float(total_wealth_cents)
            ruined = False
            for ret in path:
                w -= w_dollar
                if w <= 0.0:
                    ruined = True
                    break
                w *= 1.0 + ret
                if w <= 0.0:
                    ruined = True
                    break
            if ruined:
                ruin_count += 1
                terminal_wealths.append(0.0)
            else:
                terminal_wealths.append(w)

        ruin_prob = ruin_count / n_sims
        sorted_tw = sorted(terminal_wealths)
        med_tw = sorted_tw[n_sims // 2]
        print(
            f"Withdrawal {w_bps / 100:4.2f}% (${w_dollar / 100:6,.0f}/yr) | "
            f"Ruin prob: {ruin_prob * 100:4.1f}% | Median terminal: ${med_tw / 100:10,.0f}"
        )


main()
