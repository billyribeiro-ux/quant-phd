"""Round-1 FC1-a independent random check of Proposition 2.3 (any sequence) and Corollary 2.4 (closed, one mid).

Run: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r1/prop23_random.py
"""

from __future__ import annotations

import random

rng = random.Random(12345)
checked = 0
closed_checked = 0
for _ in range(20000):
    h = rng.randint(1, 50)
    n = rng.randint(1, 8)
    mids = [rng.randint(5000, 15000) for _ in range(n)]
    sides = [rng.choice((1, -1)) for _ in range(n)]
    qs = [rng.randint(1, 300) for _ in range(n)]
    m_n = mids[-1]
    cash = sum(s * q * (m + s * h) for s, q, m in zip(sides, qs, mids))
    inv = -sum(s * q for s, q in zip(sides, qs))
    profit = cash + inv * m_n
    V = sum(qs)
    rhs = h * V + sum(s * q * (m - m_n) for s, q, m in zip(sides, qs, mids))
    assert profit == rhs, (h, mids, sides, qs)
    checked += 1
    if inv == 0:
        assert profit == cash, "a closed sequence has P = C (Definition 2.1)"
        closed_checked += 1
for _ in range(5000):
    h = rng.randint(1, 50)
    m = rng.randint(5000, 15000)
    k = rng.randint(1, 6)
    buys = [rng.randint(1, 200) for _ in range(k)]
    sells = [rng.randint(1, 200) for _ in range(k)]
    if sum(buys) != sum(sells):
        sells[-1] += sum(buys) - sum(sells)
        if sells[-1] < 1:
            continue
    trades = [(1, q, m) for q in buys] + [(-1, q, m) for q in sells]
    rng.shuffle(trades)
    cash = sum(s * q * (mm + s * h) for s, q, mm in trades)
    Q = sum(buys)
    assert cash == 2 * h * Q, (h, m, buys, sells)
    closed_checked += 1
print(f"Proposition 2.3 identity held on {checked} random sequences (any sides, mids, sizes)")
print(f"Corollary 2.4 (closed, one mid) held on {closed_checked} cases")
