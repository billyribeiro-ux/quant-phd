"""Round-9 check (slice d): numbers quoted in cards and grader comments, recomputed with the standard library.
(a) ceil(0.99 n) in floats versus the exact integer index, n = 1..2,000,000 (grader/reference.py:95-100, project.html:214)
(b) card M4-c045 (Bernoulli kurtosis 73/9 and 7/3), M4-c208 (AQ and BB^T), M4-c161 / c168 / c172 (t(3) and Cauchy tails)
(c) grader comment test_project.py:351-353 (variance of the rounded and truncated 2-cent normal loss).
Usage: python -I <this file> from the checkout root."""
import math
import statistics
from fractions import Fraction

print("(a) float ceil(0.99 n) differs from (99n+99)//100 for n in 1..2000000:",
      [n for n in range(1, 2_000_001) if math.ceil(0.99 * n) != (99 * n + 99) // 100][:5] or "none")

for label, p in (("p=1/10", Fraction(1, 10)), ("p=1/4", Fraction(1, 4))):
    pq = p * (1 - p)
    print(f"(b) c045 Bernoulli {label}: gamma4 = (1-3pq)/(pq) = {(1 - 3 * pq) / pq}")
A = [[2, 0], [1, 1]]
Q = [[0, -1], [1, 0]]
B = [[sum(A[i][k] * Q[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
BBt = [[sum(B[i][k] * B[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
AAt = [[sum(A[i][k] * A[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
AtA = [[sum(A[k][i] * A[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
print("(b) c208 B = AQ =", B, " BB^T =", BBt, " AA^T =", AAt, " A^T A =", AtA)


def t3_tail(x: float) -> float:
    y = x / math.sqrt(3)
    return (2 / math.pi) * (math.atan(1 / y) - y / (1 + y * y))


print(f"(b) c168 P(|V|>10) for t(3) = {t3_tail(10):.6f} (card 0.002128)")
print(f"(b) c172 x^3 P(|V|>x) at x = 1000 = {1000 ** 3 * t3_tail(1000):.6f} (card 2.205308); 4 sqrt3/pi = {4 * math.sqrt(3) / math.pi:.6f}")
print(f"(b) c161 10 P(|C|>10) for Cauchy = {10 * (1 - 2 / math.pi * math.atan(10)):.6f} (card 0.634510); 2/pi = {2 / math.pi:.6f}")
print(f"(b) c031 sqrt(2968750000) = {math.sqrt(2968750000):.2f} (card 54486.24)")

N = statistics.NormalDist(0, 2)
trunc_var = sum(2 * k * k * (N.cdf(k + 1) - N.cdf(k)) for k in range(1, 80))
round_var = sum(2 * k * k * (N.cdf(k + 0.5) - N.cdf(k - 0.5)) for k in range(1, 80))
print(f"(c) truncated-toward-zero variance of N(0, 4) = {trunc_var:.4f} (comment: about 2.7); "
      f"rounded variance = {round_var:.4f} (comment: 4 + 1/12 = {4 + 1 / 12:.4f})")
