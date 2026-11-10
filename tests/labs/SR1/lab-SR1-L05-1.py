"""Lab SR1-L05-1: Margin-Spiral Simulator and Collateral Haircut Dynamics.

SIMULATED margin-spiral dynamics following Brunnermeier and Pedersen (2009).
Simulates dynamic iterations of the coupled price-margin map under an initial price shock.
Evaluates both the convergent regime (multiplier K < 1) with its closed-form fixed point
and the explosive regime (multiplier K >= 1) where forced liquidations spiral without bound.
"""


def main() -> None:
    # Model parameters for affine price-margin iteration: y_{t+1} = delta_0 + K * y_t
    # where y_t is cumulative price drop, delta_0 is fundamental shock, K is feedback multiplier.
    delta_0 = 2.00  # Initial fundamental price shock ($2.00)

    print("=== SIMULATED MARGIN-SPIRAL DYNAMICS (Brunnermeier & Pedersen 2009) ===")

    # Regime 1: Convergent Spiral (K < 1)
    k_conv = 0.60
    y_star = delta_0 / (1.0 - k_conv)  # Closed-form fixed point: 2.00 / (1 - 0.60) = 5.00
    print(f"\n--- Regime 1: Convergent Spiral (Multiplier K = {k_conv:.2f} < 1) ---")
    print(f"Closed-form fixed point price drop: {y_star:.4f}")
    y = delta_0
    print(f"Step  0: Price drop = {y:7.4f}, Closed-form gap = {abs(y - y_star):8.6f}")
    for t in range(1, 11):
        y = delta_0 + k_conv * y
        gap = abs(y - y_star)
        print(f"Step {t:2d}: Price drop = {y:7.4f}, Closed-form gap = {gap:8.6f}")

    # Regime 2: Explosive Spiral (K >= 1)
    k_div = 1.25
    print(f"\n--- Regime 2: Explosive Spiral (Multiplier K = {k_div:.2f} >= 1) ---")
    print("Explosive threshold K >= 1.0 (no finite fixed point exists)")
    y_div = delta_0
    print(f"Step  0: Price drop = {y_div:9.4f}")
    for t in range(1, 11):
        y_div = delta_0 + k_div * y_div
        print(f"Step {t:2d}: Price drop = {y_div:9.4f} (unbounded expansion)")

    # Wholesale funding repo haircut ladder (Gorton & Metrick 2012)
    print("\n--- Repo Collateral Haircut Ladder ---")
    collateral_prices = [100.0, 95.0, 90.0, 80.0, 60.0]
    borrowing_needed = 70.0  # Cash needed per bond
    print(f"Required Cash Borrowing = {borrowing_needed:.1f}")
    print(f"{'Price':>7} | {'Implied Haircut':>16} | {'Status':>16}")
    print("-" * 45)
    for p in collateral_prices:
        if p >= borrowing_needed:
            h = (p - borrowing_needed) / p
            status = "Rollable"
            print(f"{p:7.1f} | {h * 100:15.2f}% | {status:>16}")
        else:
            status = "Run on Repo (Cut)"
            print(f"{p:7.1f} | {'N/A (Insolvent)':>16} | {status:>16}")


main()
