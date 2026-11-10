"""Lab 6: Dornbusch Exchange Rate Overshooting Simulation.

Deterministic simulation. Standard library only.
Solves the discrete-time Dornbusch (1976) model with sticky prices and UIP.
Demonstrates that a monetary expansion induces an immediate spot exchange rate jump
that overshoots its long-run equilibrium before appreciating back to purchasing power parity.
"""

import math


class DornbuschModel:
    def __init__(
        self,
        lambda_interest: float,  # Interest semi-elasticity of money demand
        theta_price: float,  # Speed of price adjustment to real exchange rate
    ) -> None:
        self.lam = lambda_interest
        self.theta = theta_price

        # Derive discrete-time stable eigenvalue mu
        # Dynamics in p: p_{t+1} - p_t = theta * (s_t - p_t)
        # UIP: s_{t+1} - s_t = -(1 / lam) * (m - p_t)
        # On saddle path: s_t - s_bar = -kappa * (p_t - p_bar)
        # Substituting: p_{t+1} - p_bar = (1 - theta*(1 + kappa)) * (p_t - p_bar) = mu * (p_t - p_bar)
        # And from UIP: s_{t+1} - s_bar = -kappa * mu * (p_t - p_bar) = s_t - s_bar - (1/lam)*(p_bar - p_t)
        # => -kappa * mu = -kappa + 1/lam => kappa * (1 - mu) = 1/lam
        # Since 1 - mu = theta * (1 + kappa), we get:
        # kappa * theta * (1 + kappa) = 1/lam => theta * kappa^2 + theta * kappa - 1/lam = 0
        # Positive root for kappa:
        a = self.theta
        b = self.theta
        c = -1.0 / self.lam
        self.kappa = (-b + math.sqrt(b**2 - 4.0 * a * c)) / (2.0 * a)
        self.mu = 1.0 - self.theta * (1.0 + self.kappa)

    def simulate(
        self,
        delta_m: float,
        periods: int = 25,
    ) -> list[dict[str, float]]:
        """Simulate dynamic trajectory following a permanent monetary shock delta_m."""
        # Long-run steady state: p_bar = s_bar = delta_m, i_bar = i*
        p_bar = delta_m
        s_bar = delta_m

        # At t=0, price is sticky at p_0 = 0.0
        trajectory: list[dict[str, float]] = []
        p_t = 0.0

        for t in range(periods):
            # Saddle path saddle equation: s_t - s_bar = -kappa * (p_t - p_bar)
            s_t = s_bar - self.kappa * (p_t - p_bar)
            # Interest rate differential from money market: i_t - i* = -(1/lam)*(delta_m - p_t)
            i_diff = -(1.0 / self.lam) * (delta_m - p_t)

            trajectory.append(
                {
                    "period": t,
                    "spot": s_t,
                    "price": p_t,
                    "interest_diff": i_diff,
                    "real_fx": s_t - p_t,
                }
            )

            # Next period sticky price adjustment
            p_next = p_t + self.theta * (s_t - p_t)
            p_t = p_next

        return trajectory


def main() -> None:
    # Model parameters: lambda = 4.0, theta = 0.25
    model = DornbuschModel(lambda_interest=4.0, theta_price=0.25)
    delta_m = 0.10  # 10% permanent monetary expansion

    traj = model.simulate(delta_m=delta_m, periods=20)

    s_0 = traj[0]["spot"]
    s_bar = delta_m
    overshoot_pct = (s_0 - s_bar) / s_bar * 100.0

    print("=== Dornbusch (1976) Overshooting Dynamics ===")
    print(f"Monetary Expansion (Delta m): {delta_m * 100:.1f}%")
    print(f"Long-Run Neutral Exchange Rate (s_bar): {s_bar:.4f}")
    print(f"Initial Jump Spot Rate (s_0):           {s_0:.4f}")
    print(f"Overshooting Premium:                   {(s_0 - s_bar):.4f} ({overshoot_pct:+.1f}%)")
    print(f"Initial Interest Rate Wedge (i_0 - i*): {traj[0]['interest_diff'] * 100:.2f}%\n")

    print("Period |  Spot (s_t) |  Price (p_t) | Interest Spread | Real FX (s - p)")
    print("-----------------------------------------------------------------------")
    for row in traj[:8]:
        p = int(row["period"])
        s_val = row["spot"]
        p_val = row["price"]
        i_spread = row["interest_diff"] * 100
        r_fx = row["real_fx"]
        print(f"  {p:2d}   |   {s_val:.4f}    |    {p_val:.4f}    |     {i_spread:+.2f}%     |    {r_fx:.4f}")
    print(" ...")
    last = traj[-1]
    p_end = int(last["period"])
    s_end = last["spot"]
    p_end_val = last["price"]
    i_end = last["interest_diff"] * 100
    r_end = last["real_fx"]
    print(f"  {p_end:2d}   |   {s_end:.4f}    |    {p_end_val:.4f}    |     {i_end:+.2f}%     |    {r_end:.4f}")

    # Verifications
    assert s_0 > s_bar, f"Initial spot {s_0} must overshoot long-run equilibrium {s_bar}"
    assert traj[0]["interest_diff"] < 0, "Initial domestic interest rate must drop below world rate"
    assert abs(last["spot"] - s_bar) < 0.005, f"Spot must converge to s_bar, got {last['spot']}"
    assert abs(last["price"] - s_bar) < 0.005, f"Price must converge to s_bar, got {last['price']}"


main()
