"""Lab SR4-L02-1: Central Clearing and Multilateral Netting Efficiency.

SIMULATED. Demonstrates the mathematics of bilateral vs. multilateral netting
under the central clearing mandate (Duffie & Zhu, 2011). Analyzes a network of
5 primary swap dealers, computing gross exposures, bilateral netted exposures,
and central counterparty (CCP) multilateral netted exposures.
"""

from __future__ import annotations


def calculate_network_exposures(
    dealers: list[str],
    cash_flows: list[list[float]],
) -> dict[str, float]:
    """Calculate gross, bilateral net, and multilateral net exposures across a dealer network.

    cash_flows[i][j] represents the net mark-to-market exposure of dealer i to dealer j
    (positive means i is owed money by j; negative means i owes money to j).
    By no-arbitrage/accounting consistency, cash_flows[j][i] = -cash_flows[i][j].
    """
    n = len(dealers)
    if any(len(row) != n for row in cash_flows):
        raise ValueError("cash_flows matrix must be square")

    # 1. Gross bilateral exposure (total credit risk without netting agreements)
    gross_exposure = 0.0
    for i in range(n):
        for j in range(n):
            if i != j and cash_flows[i][j] > 0:
                gross_exposure += cash_flows[i][j]

    # 2. Bilateral netted exposure (netting pairwise between each dealer pair)
    # Under standard ISDA Master Agreement netting
    bilateral_net_exposure = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            net_ij = cash_flows[i][j]
            bilateral_net_exposure += abs(net_ij)

    # 3. Multilateral netted exposure (novating all contracts to a central clearinghouse)
    # Each dealer's net position against the CCP is sum_j cash_flows[i][j]
    ccp_net_positions = [sum(cash_flows[i][j] for j in range(n)) for i in range(n)]

    # Total exposure to the CCP across all net-creditor dealers:
    # (By conservation of cash flows, sum of ccp_net_positions is 0)
    multilateral_net_exposure = sum(max(0.0, pos) for pos in ccp_net_positions)

    # Netting efficiencies
    bilateral_efficiency = (1.0 - bilateral_net_exposure / gross_exposure) * 100.0 if gross_exposure > 0 else 0.0
    ccp_efficiency = (1.0 - multilateral_net_exposure / gross_exposure) * 100.0 if gross_exposure > 0 else 0.0
    incremental_ccp_benefit = (
        (1.0 - multilateral_net_exposure / bilateral_net_exposure) * 100.0 if bilateral_net_exposure > 0 else 0.0
    )

    return {
        "gross_exposure": gross_exposure,
        "bilateral_net": bilateral_net_exposure,
        "multilateral_net": multilateral_net_exposure,
        "bilateral_efficiency": bilateral_efficiency,
        "ccp_efficiency": ccp_efficiency,
        "incremental_ccp_benefit": incremental_ccp_benefit,
    }


def main() -> None:
    dealers = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E"]

    # Bilateral OTC swap mark-to-market positions ($ billions)
    # Positive: row dealer is owed by column dealer.
    matrix = [
        [0.0, 12.0, -8.0, 15.0, -10.0],  # Net A: +9.0
        [-12.0, 0.0, 14.0, -6.0, 5.0],  # Net B: +1.0
        [8.0, -14.0, 0.0, 10.0, -12.0],  # Net C: -8.0
        [-15.0, 6.0, -10.0, 0.0, 16.0],  # Net D: -3.0
        [10.0, -5.0, 12.0, -16.0, 0.0],  # Net E: +1.0
    ]

    metrics = calculate_network_exposures(dealers, matrix)

    print("=== OTC DERIVATIVES CENTRAL CLEARING NETTING EFFICIENCY (SIMULATED) ===")
    print(f"Network Size: {len(dealers)} Dealers")
    print(f"Total Gross Bilateral Exposure: ${metrics['gross_exposure']:.2f}B")
    print(
        f"Total Bilateral Netted Exposure (ISDA): ${metrics['bilateral_net']:.2f}B "
        f"(Netting Reduction: {metrics['bilateral_efficiency']:.1f}%)"
    )
    print(
        f"Total Multilateral Netted Exposure (CCP): ${metrics['multilateral_net']:.2f}B "
        f"(Netting Reduction: {metrics['ccp_efficiency']:.1f}%)"
    )
    print(
        f"Incremental Counterparty Risk Reduction of CCP over Bilateral Netting: "
        f"{metrics['incremental_ccp_benefit']:.1f}%"
    )


main()
