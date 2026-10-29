import random
from fractions import Fraction
rng = random.Random(7)
bad = 0
for trial in range(20000):
    h = rng.randint(1, 5)               # one half-spread for the whole sequence (A1 as revised)
    n = rng.randint(1, 8)
    trades = []
    mid = rng.randint(9000, 11000)
    for _ in range(n):
        mid += rng.randint(-4, 4)
        trades.append((rng.choice([1, -1]), rng.randint(1, 30), mid))
    m_n = trades[-1][2]
    C = sum(s * q * (m + s * h) for s, q, m in trades)
    I = -sum(s * q for s, q, _ in trades)
    V = sum(q for _, q, _ in trades)
    P = C + I * m_n
    rhs = h * V + sum(s * q * (m - m_n) for s, q, m in trades)
    if P != rhs:
        bad += 1
print("Prop 2.3 identity mismatches under constant h:", bad, "of 20000")
print("round-4 counterexample cash with two different half-spreads (buy at 10001, sell at 9997):", 1*(10000+1) + (-1)*(10000-3))
