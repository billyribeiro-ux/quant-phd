"""Rung 2 completed solution: asset location allocation and moving-block bootstrap block extraction.

Standard library only. All inputs are SIMULATED illustrative values.
"""


def main() -> None:
    # -------------------------------------------------------------
    # Part 1: Tax-Optimal Asset Location Priority
    # -------------------------------------------------------------
    bond_target_cents = 40_000_000  # $400,000 bonds needed
    taxable_cap_cents = 40_000_000  # $400,000 capacity
    tda_cap_cents = 40_000_000  # $400,000 capacity
    roth_cap_cents = 20_000_000  # $200,000 capacity

    # Step 1: Bonds to TDA first up to capacity
    tda_bond = min(bond_target_cents, tda_cap_cents)
    remaining_bond = bond_target_cents - tda_bond

    # Step 2: Remaining bonds to Taxable
    taxable_bond = min(remaining_bond, taxable_cap_cents)
    roth_bond = remaining_bond - taxable_bond

    # Step 3: Remaining capacity in each account holds Equities
    tda_equity = tda_cap_cents - tda_bond
    taxable_equity = taxable_cap_cents - taxable_bond
    roth_equity = roth_cap_cents - roth_bond

    print(f"TDA bonds: {tda_bond} | Taxable bonds: {taxable_bond} | Roth bonds: {roth_bond}")
    print(f"TDA equity: {tda_equity} | Taxable equity: {taxable_equity} | Roth equity: {roth_equity}")

    # -------------------------------------------------------------
    # Part 2: Moving-Block Bootstrap Slicing
    # -------------------------------------------------------------
    returns = [0.02, 0.05, -0.03, 0.08, -0.01, 0.04, 0.06, -0.02, 0.03, 0.07]
    block_length = 3
    num_blocks = len(returns) - block_length + 1
    assert num_blocks == 8

    # Extract block starting at index 2
    idx = 2
    extracted_block = returns[idx : idx + block_length]
    print(f"Extracted block at index {idx}: {extracted_block}")


main()
