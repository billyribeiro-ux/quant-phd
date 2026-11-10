"""Lab CF4-L01-1: Free Cash Flow to the Firm (FCFF) and Reinvestment Articulation.

Computes NOPAT, gross capital expenditures, working capital changes, FCFF,
and the fundamental reinvestment rate across a 5-year operating profile.
"""

from __future__ import annotations

import numpy as np


def compute_fcff_schedule(
    ebit: np.ndarray,
    tax_rate: float,
    depreciation: np.ndarray,
    capex: np.ndarray,
    delta_nwc: np.ndarray,
) -> dict[str, np.ndarray]:
    """Calculate detailed components of FCFF and reinvestment rate."""
    nopat = ebit * (1.0 - tax_rate)
    net_capex = capex - depreciation
    reinvestment = net_capex + delta_nwc
    fcff = nopat - reinvestment
    reinvestment_rate = reinvestment / nopat

    return {
        "ebit": ebit,
        "nopat": nopat,
        "depreciation": depreciation,
        "capex": capex,
        "net_capex": net_capex,
        "delta_nwc": delta_nwc,
        "reinvestment": reinvestment,
        "fcff": fcff,
        "reinvestment_rate": reinvestment_rate,
    }


def main() -> None:
    print("CF4 Lab L01-1: FCFF & Reinvestment Schedule")
    print("===========================================")

    # 5-year corporate operating forecast ($M)
    ebit = np.array([200.0, 220.0, 245.0, 270.0, 300.0])
    tax_rate = 0.25
    depr = np.array([45.0, 48.0, 52.0, 56.0, 60.0])
    capex = np.array([70.0, 75.0, 82.0, 88.0, 95.0])
    dnwc = np.array([15.0, 16.5, 18.0, 20.0, 22.0])

    res = compute_fcff_schedule(ebit, tax_rate, depr, capex, dnwc)

    print("Year   EBIT   NOPAT  Depr  CapEx  dNWC   Reinv   FCFF    RR (%)")
    print("---------------------------------------------------------------")
    for t in range(len(ebit)):
        print(
            f"T+{t + 1}   {res['ebit'][t]:5.1f}  {res['nopat'][t]:5.1f}  "
            f"{res['depreciation'][t]:4.1f}  {res['capex'][t]:5.1f}  "
            f"{res['delta_nwc'][t]:4.1f}  {res['reinvestment'][t]:5.1f}  "
            f"{res['fcff'][t]:5.1f}   {res['reinvestment_rate'][t] * 100:5.2f}%"
        )

    # Fundamental verification: FCFF == NOPAT * (1 - RR)
    for t in range(len(ebit)):
        expected_fcff = res["nopat"][t] * (1.0 - res["reinvestment_rate"][t])
        assert abs(res["fcff"][t] - expected_fcff) < 1e-9

    print("---------------------------------------------------------------")
    print("Reinvestment articulation identity NOPAT * (1 - RR) verified: True")


main()
