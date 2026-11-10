"""Lab 1 for PM2 L03: Cap Tables, Option Pool Shuffle, and Anti-Dilution Protection.

SIMULATED: A capitalization table subjected to a Series B down-round.
Pre-Series B capitalization:
- Common (Founders): 7,500,000 shares
- Option Pool (Reserved): 2,000,000 shares
- Series A Preferred: 2,500,000 shares issued at $2.00 ($5.0M invested, 1.0x preference)
Total pre-round fully diluted shares = 12,000,000 shares (common + preferred = 10,000,000).

Series B Down-Round:
$6.0M invested at $1.00 per share (6,000,000 new shares issued).
Evaluates adjusted conversion price, conversion ratio, and founder ownership dilution under:
(1) No anti-dilution protection.
(2) Broad-Based Weighted Average (BBWA).
(3) Narrow-Based Weighted Average (NBWA).
(4) Full Ratchet anti-dilution.

Standard library and NumPy only; fully deterministic.
"""

from __future__ import annotations


def main() -> None:
    founders_sh = 7_500_000.0
    options_sh = 2_000_000.0
    series_a_sh = 2_500_000.0

    fd_pre = founders_sh + options_sh + series_a_sh  # 12,000,000
    cp_pre = founders_sh + series_a_sh  # 10,000,000 (excluding unissued options)

    p_a_orig = 2.00
    p_b_issue = 1.00
    inv_b = 6_000_000.0
    new_shares_b = inv_b / p_b_issue  # 6,000,000 shares

    # 1. No Anti-Dilution (Baseline)
    cp_none = p_a_orig
    cr_none = 1.0
    a_conv_none = series_a_sh * cr_none
    tot_none = founders_sh + options_sh + a_conv_none + new_shares_b
    founder_pct_none = (founders_sh / tot_none) * 100.0

    # 2. Broad-Based Weighted Average (BBWA)
    # CP_new = CP_old * (FD_pre + Inv / CP_old) / (FD_pre + New_shares)
    hypothetical_sh = inv_b / p_a_orig  # 3,000,000 shares
    cp_bbwa = p_a_orig * (fd_pre + hypothetical_sh) / (fd_pre + new_shares_b)
    cr_bbwa = p_a_orig / cp_bbwa
    a_conv_bbwa = series_a_sh * cr_bbwa
    tot_bbwa = founders_sh + options_sh + a_conv_bbwa + new_shares_b
    founder_pct_bbwa = (founders_sh / tot_bbwa) * 100.0

    # 3. Narrow-Based Weighted Average (NBWA)
    cp_nbwa = p_a_orig * (cp_pre + hypothetical_sh) / (cp_pre + new_shares_b)
    cr_nbwa = p_a_orig / cp_nbwa
    a_conv_nbwa = series_a_sh * cr_nbwa
    tot_nbwa = founders_sh + options_sh + a_conv_nbwa + new_shares_b
    founder_pct_nbwa = (founders_sh / tot_nbwa) * 100.0

    # 4. Full Ratchet
    cp_fr = p_b_issue
    cr_fr = p_a_orig / cp_fr
    a_conv_fr = series_a_sh * cr_fr
    tot_fr = founders_sh + options_sh + a_conv_fr + new_shares_b
    founder_pct_fr = (founders_sh / tot_fr) * 100.0

    print(f"Baseline (No Protection): CP=${cp_none:.4f}, CR={cr_none:.4f}, Founder Own={founder_pct_none:.2f}%")
    print(f"Broad-Based WA: CP=${cp_bbwa:.4f}, CR={cr_bbwa:.4f}, Founder Own={founder_pct_bbwa:.2f}%")
    print(f"Narrow-Based WA: CP=${cp_nbwa:.4f}, CR={cr_nbwa:.4f}, Founder Own={founder_pct_nbwa:.2f}%")
    print(f"Full Ratchet: CP=${cp_fr:.4f}, CR={cr_fr:.4f}, Founder Own={founder_pct_fr:.2f}%")
    print(f"Series A Converted Shares (BBWA vs Full Ratchet): {a_conv_bbwa:,.0f} vs {a_conv_fr:,.0f}")


main()
