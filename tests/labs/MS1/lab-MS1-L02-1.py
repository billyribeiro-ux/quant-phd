"""Lab MS1-L02-1: Glosten-Milgrom quotes and Bayesian updating.

Sequential trade model with informed and uninformed traders.
All calculations use exact Fraction arithmetic, demonstrating that adverse
selection generates an endogenous bid-ask spread even with zero order-processing cost.
"""

from __future__ import annotations

from fractions import Fraction


def glosten_milgrom_step(
    v_l: Fraction, v_h: Fraction, alpha: Fraction, pi: Fraction
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction]:
    """Compute ask, bid, posteriors, and check the law of iterated expectations."""
    # Probabilities of order signs conditional on state and unconditional
    p_buy = (1 - alpha + 2 * alpha * pi) / 2
    p_sell = (1 + alpha - 2 * alpha * pi) / 2

    # Bayes rule posteriors
    pi_plus = (pi * (1 + alpha)) / (1 - alpha + 2 * alpha * pi)
    pi_minus = (pi * (1 - alpha)) / (1 + alpha - 2 * alpha * pi)

    # Market maker quotes: expected value conditional on incoming trade direction
    ask = v_l + pi_plus * (v_h - v_l)
    bid = v_l + pi_minus * (v_h - v_l)

    # Law of iterated expectations check: E[pi_{t} | pi_{t-1}] == pi_{t-1}
    expected_posterior = p_buy * pi_plus + p_sell * pi_minus
    if expected_posterior != pi:
        raise ValueError("Law of iterated expectations violated in posterior calculation.")

    return ask, bid, pi_plus, pi_minus, ask - bid


def main() -> None:
    v_l = Fraction(10, 1)
    v_h = Fraction(20, 1)
    alpha = Fraction(1, 4)
    pi = Fraction(1, 2)
    trade_sequence = ["buy", "buy", "sell", "buy"]

    print("Initial state:")
    print(f"  v_L = {v_l}, v_H = {v_h}, alpha = {alpha}, initial prior pi_0 = {pi}")
    print("Sequential quote updating:")

    for step, trade in enumerate(trade_sequence, start=1):
        ask, bid, pi_plus, pi_minus, spread = glosten_milgrom_step(v_l, v_h, alpha, pi)
        print(
            f"Step {step} before trade ({trade}): "
            f"Ask={ask} ({float(ask):.4f}), Bid={bid} ({float(bid):.4f}), Spread={spread} ({float(spread):.4f})"
        )
        pi = pi_plus if trade == "buy" else pi_minus

    print(f"Final posterior probability pi_{len(trade_sequence)}: {pi} ({float(pi):.4f})")
    term_plus = (pi * (1 + alpha)) / (1 - alpha + 2 * alpha * pi)
    term_minus = (pi * (1 - alpha)) / (1 + alpha - 2 * alpha * pi)
    final_spread = (v_h - v_l) * (term_plus - term_minus)
    print(f"Adverse-selection spread at final state: {final_spread} ({float(final_spread):.4f})")


main()
