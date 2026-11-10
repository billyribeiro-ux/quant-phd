"""PM2 project lab 1 (rung 1, worked example): Term-sheet economics.

SIMULATED: A complete 3-round capitalization table and exit waterfall calculation.
Rounds:
- Founding: 10,000,000 common shares held by founders.
- Series A: $5.0M invested at $15.0M pre-money; 15% unallocated option pool created post-money.
- Series B: $10.0M invested at $30.0M pre-money; 5% option pool top-up.
- Series C (Down-Round): $15.0M invested at $25.0M pre-money; Broad-Based Weighted Average anti-dilution.

Evaluates cap table share counts, conversion ratios, and exit waterfall payoffs at
exit valuations of $10.0M (partial preference recovery), $30.0M (full preference recovery),
and $100.0M (common conversion upside).
Standard library and NumPy only; fully deterministic.
"""

from __future__ import annotations


def main() -> None:
    founders_sh = 10_000_000.0

    # 1. Series A Round ($5M on $15M pre -> $20M post; 15% pool post-money)
    pre_a = 15_000_000.0
    inv_a = 5_000_000.0
    post_a = pre_a + inv_a
    pool_a_pct = 0.15

    # Post-A shares = founders / (1 - inv/post - pool_pct)
    tot_a = founders_sh / (1.0 - (inv_a / post_a) - pool_a_pct)
    pool_a = pool_a_pct * tot_a
    price_a = pre_a / (founders_sh + pool_a)
    sh_a = inv_a / price_a
    cp_a = price_a
    cr_a = 1.0

    # 2. Series B Round ($10M on $30M pre -> $40M post; 5% pool top-up)
    pre_b = 30_000_000.0
    inv_b = 10_000_000.0
    post_b = pre_b + inv_b
    pool_b_pct = 0.05
    prior_b = founders_sh + pool_a + sh_a
    tot_b = prior_b / (1.0 - (inv_b / post_b) - pool_b_pct)
    delta_pool_b = pool_b_pct * tot_b
    pool_b = pool_a + delta_pool_b
    price_b = pre_b / (prior_b + delta_pool_b)
    sh_b = inv_b / price_b
    cp_b = price_b
    cr_b = 1.0

    # 3. Series C Down-Round ($15M on $25M pre -> $40M post; 0% pool top-up)
    pre_c = 25_000_000.0
    inv_c = 15_000_000.0
    prior_c = founders_sh + pool_b + sh_a + sh_b
    price_c = pre_c / prior_c
    sh_c = inv_c / price_c

    # Anti-dilution adjustment for Series A and Series B (price_c < price_a and price_c < price_b)
    # Broad-based weighted average formula
    # Series A:
    hypo_a = inv_c / cp_a
    cp_a = cp_a * (prior_c + hypo_a) / (prior_c + sh_c)
    cr_a = price_a / cp_a

    # Series B:
    hypo_b = inv_c / cp_b
    cp_b = cp_b * (prior_c + hypo_b) / (prior_c + sh_c)
    cr_b = price_b / cp_b

    tot_final = founders_sh + pool_b + sh_a + sh_b + sh_c

    print("--- Capitalization Table Post-Series C ---")
    print(f"Founders: {founders_sh:,.0f} shares ({founders_sh / tot_final * 100:.1f}%)")
    print(f"Option Pool: {pool_b:,.0f} shares ({pool_b / tot_final * 100:.1f}%)")
    print(f"Series A: {sh_a:,.0f} shares (Issue: ${price_a:.2f}, CR: {cr_a:.3f})")
    print(f"Series B: {sh_b:,.0f} shares (Issue: ${price_b:.2f}, CR: {cr_b:.3f})")
    print(f"Series C: {sh_c:,.0f} shares (Issue: ${price_c:.2f}, CR: 1.000)")
    print(f"Total Fully Diluted Shares: {tot_final:,.0f}")

    # 4. Exit Waterfall Payoffs (Standard Seniority: C > B > A > Common)
    # Liquidation preferences: C=$15M, B=$10M, A=$5M (Total pref = $30M)
    print("\n--- Exit Waterfall Allocation (Standard Seniority: C > B > A > Common) ---")
    for ev in [10_000_000.0, 30_000_000.0, 100_000_000.0]:
        # At $10M: C gets $10M, B=0, A=0, Common=0
        # At $30M: C gets $15M, B gets $10M, A gets $5M, Common=0
        # At $100M: Preferred holders convert to common since pro-rata shares exceed preferences
        if ev <= 15_000_000.0:
            c_pay = ev
            b_pay, a_pay, f_pay, opt_pay = 0.0, 0.0, 0.0, 0.0
        elif ev <= 25_000_000.0:
            c_pay = 15_000_000.0
            b_pay = ev - 15_000_000.0
            a_pay, f_pay, opt_pay = 0.0, 0.0, 0.0
        elif ev <= 30_000_000.0:
            c_pay = 15_000_000.0
            b_pay = 10_000_000.0
            a_pay = ev - 25_000_000.0
            f_pay, opt_pay = 0.0, 0.0
        else:
            # At $100M: all convert to common at their adjusted conversion ratios
            as_conv_sh = founders_sh + pool_b + (sh_a * cr_a) + (sh_b * cr_b) + sh_c
            f_pay = ev * (founders_sh / as_conv_sh)
            opt_pay = ev * (pool_b / as_conv_sh)
            a_pay = ev * ((sh_a * cr_a) / as_conv_sh)
            b_pay = ev * ((sh_b * cr_b) / as_conv_sh)
            c_pay = ev * (sh_c / as_conv_sh)

        print(
            f"Exit ${ev / 1e6:.0f}M: C=${c_pay / 1e6:.2f}M | "
            f"B=${b_pay / 1e6:.2f}M | A=${a_pay / 1e6:.2f}M | "
            f"Founders=${f_pay / 1e6:.2f}M | Options=${opt_pay / 1e6:.2f}M"
        )


main()
