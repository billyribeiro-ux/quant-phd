"""Round-1 closing-delta checks for E5 slice a cards c033, c034, c141 (exact fractions)."""

from fractions import Fraction as F


def res(dy: F, dk: F, dl: F, alpha: F) -> F:
    # Definition 2.1: Res_t(alpha) = dlnY - alpha dlnK - (1 - alpha) dlnL
    return dy - alpha * dk - (1 - alpha) * dl


# Counterexample to the per-period reading of E5-c034: average growth of K and L differ,
# but in period 1 the growth rates are equal, so Res_1 does not depend on alpha.
dy = [F(3, 100), F(5, 100)]
dk = [F(2, 100), F(4, 100)]
dl = [F(2, 100), F(0, 100)]
avg_k = sum(dk) / len(dk)
avg_l = sum(dl) / len(dl)
print("average growth K", avg_k, "L", avg_l, "differ", avg_k != avg_l)
for a, b in [(F(1, 5), F(2, 5)), (F(3, 10), F(7, 10))]:
    print("alpha", a, b)
    print("  Res_1(a) =", res(dy[0], dk[0], dl[0], a), " Res_1(b) =", res(dy[0], dk[0], dl[0], b),
          " equal in period 1:", res(dy[0], dk[0], dl[0], a) == res(dy[0], dk[0], dl[0], b))
    avg_res_a = sum(res(y, k, lab, a) for y, k, lab in zip(dy, dk, dl)) / 2
    avg_res_b = sum(res(y, k, lab, b) for y, k, lab in zip(dy, dk, dl)) / 2
    print("  average residual a", avg_res_a, "b", avg_res_b, "differ:", avg_res_a != avg_res_b)
    # Proposition 2.4 identity: Res_t(a) - Res_t(b) = -(a - b)(dK - dL)
    for t in range(2):
        lhs = res(dy[t], dk[t], dl[t], a) - res(dy[t], dk[t], dl[t], b)
        rhs = -(a - b) * (dk[t] - dl[t])
        print("  Prop 2.4 identity t", t + 1, lhs == rhs)

# E5-c141 arithmetic and E5-c141 lab numbers
print("difference of printed average residuals:", F("0.016254") - F("0.010665"),
      "as decimal", float(F("0.016254") - F("0.010665")))
