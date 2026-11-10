"""Lab FI3-project-2 (Rung 2, Completion): Forward rate, excess return, and roll-down calculation.

SIMULATED: complete solution for the Rung 2 completion problem.
Calculates 1-year forward rates, 1-year holding-period excess return, and roll-down.
Standard library and NumPy only; no network.
"""

from __future__ import annotations


def main() -> None:
    # 2-period yield inputs
    tau1, tau2 = 1.0, 2.0
    y1, y2 = 0.035, 0.042

    # Step 1: Forward rate between 1y and 2y
    fwd_1_2 = (tau2 * y2 - tau1 * y1) / (tau2 - tau1)

    # Step 2: Next-period yield realization and excess return
    y1_next = 0.038
    rx_2 = -(tau2 - 1.0) * y1_next + tau2 * y2 - y1

    # Step 3: Roll-down return on static curve over horizon = 1.0 year
    roll_down = (tau2 - 1.0) * (y2 - y1)

    print(f"Calculated 1y1y forward rate: {fwd_1_2:.4%}")
    print(f"Realized excess return rx_2: {rx_2:.4%}")
    print(f"Roll-down return on static curve: {roll_down:.4%}")


main()
