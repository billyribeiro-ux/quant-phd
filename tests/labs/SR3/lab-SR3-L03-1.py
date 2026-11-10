"""Lab SR3-L03-1: SRISK and Systemic Capital Shortfall Index.

SIMULATED: calculates individual conditional capital shortfalls, non-negative SRISK,
aggregate systemic shortfall indices, and systemic risk percentage contributions
following Brownlees and Engle (2017).
"""

from __future__ import annotations


def compute_srisk(w: float, d: float, lrmes: float, k: float) -> tuple[float, float]:
    """Calculate gross capital shortfall and non-negative SRISK."""
    cs = k * d - (1.0 - k) * (1.0 - lrmes) * w
    srisk = max(0.0, cs)
    return cs, srisk


def main() -> None:
    # Stylized 4-institution financial system (values in billions USD)
    firms = [
        {"name": "Megabank Alpha", "W": 150.0, "D": 1850.0, "LRMES": 0.52},
        {"name": "Broker Beta", "W": 45.0, "D": 720.0, "LRMES": 0.60},
        {"name": "Regional Gamma", "W": 80.0, "D": 600.0, "LRMES": 0.38},
        {"name": "Insurer Delta", "W": 110.0, "D": 450.0, "LRMES": 0.25},
    ]

    k_prudential = 0.08  # 8% regulatory capital requirement

    print("=== SRISK Conditional Capital Shortfall Index (Brownlees & Engle 2017) ===")
    print(f"Prudential Capital Ratio (k): {k_prudential * 100:.1f}%")
    print("-" * 75)
    print(f"{'Institution':<18} {'Equity (W)':<12} {'Debt (D)':<12} {'LRMES':<10} {'CS ($B)':<10} {'SRISK ($B)':<10}")
    print("-" * 75)

    cs_list: list[float] = []
    srisk_list: list[float] = []

    for f in firms:
        w_val = float(str(f["W"]))
        d_val = float(str(f["D"]))
        lrmes_val = float(str(f["LRMES"]))
        name_val = str(f["name"])
        cs, srisk = compute_srisk(w_val, d_val, lrmes_val, k_prudential)
        cs_list.append(cs)
        srisk_list.append(srisk)
        print(f"{name_val:<18} ${w_val:<11.1f} ${d_val:<11.1f} {lrmes_val * 100:<9.1f}% ${cs:<9.2f} ${srisk:<9.2f}")

    total_srisk = sum(srisk_list)
    print("-" * 75)
    print(f"Total Aggregate SRISK (SRISK_sys): ${total_srisk:.2f}B")
    print("=" * 75)
    print(f"{'Institution':<18} {'Quasi-Leverage (A/W)':<24} {'SRISK Contribution (%)':<24}")
    print("-" * 75)

    for f, srisk in zip(firms, srisk_list, strict=True):
        w_val = float(str(f["W"]))
        d_val = float(str(f["D"]))
        name_val = str(f["name"])
        leverage = (w_val + d_val) / w_val
        srisk_pct = (srisk / total_srisk * 100.0) if total_srisk > 0 else 0.0
        print(f"{name_val:<18} {leverage:<24.2f} {srisk_pct:<24.2f}%")

    print("-" * 75)
    print("Comparative Statics Verification:")
    # Sensitivity of Megabank Alpha SRISK to +$10B debt: dSRISK/dD = k = 0.08
    _cs_d_shock, srisk_d_shock = compute_srisk(150.0, 1860.0, 0.52, k_prudential)
    delta_srisk = srisk_d_shock - srisk_list[0]
    print(f"Megabank Alpha +$10B Debt Shock: dSRISK = ${delta_srisk:.2f}B (Expected k*10 = $0.80B)")


main()
