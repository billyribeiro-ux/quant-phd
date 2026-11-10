"""Lab L02-1: Forensic accounting audit: Sloan accruals and Beneish M-Score."""

from __future__ import annotations


def main() -> None:
    # Year 1 (t-1) and Year 2 (t) financial data for an audited industrial firm
    ta_1 = 1100.0
    ta_2 = 1250.0
    avg_ta = (ta_1 + ta_2) / 2.0

    rev_1 = 1000.0
    rev_2 = 1180.0
    gp_1 = 450.0
    gp_2 = 510.0
    ar_1 = 120.0
    ar_2 = 165.0
    ca_1 = 420.0
    ca_2 = 490.0
    cash_1 = 90.0
    cash_2 = 80.0
    cl_1 = 180.0
    cl_2 = 210.0
    std_1 = 30.0
    std_2 = 35.0
    ltd_1 = 280.0
    ltd_2 = 300.0
    depr_1 = 55.0
    depr_2 = 62.0
    ppe_1 = 540.0
    ppe_2 = 610.0
    sga_1 = 160.0
    sga_2 = 185.0
    ni_2 = 115.0
    cfo_2 = 135.0

    # 1. Sloan Accruals
    delta_ca = ca_2 - ca_1
    delta_cash = cash_2 - cash_1
    delta_cl = cl_2 - cl_1
    delta_std = std_2 - std_1
    sloan_accruals = (delta_ca - delta_cash) - (delta_cl - delta_std) - depr_2
    sloan_ratio = sloan_accruals / avg_ta
    cf_accruals = ni_2 - cfo_2
    cf_ratio = cf_accruals / avg_ta

    print(f"Sloan Operating Accruals: ${sloan_accruals:.2f}M (Ratio: {sloan_ratio:+.4f})")
    print(f"Cash Flow Accruals:      ${cf_accruals:.2f}M (Ratio: {cf_ratio:+.4f})")

    # 2. Beneish 8-Variable Indices
    dsri = (ar_2 / rev_2) / (ar_1 / rev_1)
    gmi = (gp_1 / rev_1) / (gp_2 / rev_2)
    non_ca_ppe_1 = 1.0 - ((ca_1 + ppe_1) / ta_1)
    non_ca_ppe_2 = 1.0 - ((ca_2 + ppe_2) / ta_2)
    aqi = non_ca_ppe_2 / max(1e-6, non_ca_ppe_1)
    sgi = rev_2 / rev_1
    depi = (depr_1 / (ppe_1 + depr_1)) / (depr_2 / (ppe_2 + depr_2))
    sgai = (sga_2 / rev_2) / (sga_1 / rev_1)
    lvgi = ((std_2 + ltd_2) / ta_2) / ((std_1 + ltd_1) / ta_1)
    tata = (ni_2 - cfo_2) / ta_2

    m_score = (
        -4.84
        + 0.920 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
        - 0.172 * sgai
        + 4.037 * tata
        + 0.0327 * lvgi
    )

    print("\nBeneish 8-Variable Indices:")
    print(f"  DSRI: {dsri:.4f} | GMI:  {gmi:.4f} | AQI:  {aqi:.4f} | SGI:  {sgi:.4f}")
    print(f"  DEPI: {depi:.4f} | SGAI: {sgai:.4f} | LVGI: {lvgi:.4f} | TATA: {tata:.4f}")
    print(f"\nBeneish M-Score: {m_score:.4f}")
    print(f"Manipulation Flag (Cutoff > -1.78): {m_score > -1.78}")


main()
