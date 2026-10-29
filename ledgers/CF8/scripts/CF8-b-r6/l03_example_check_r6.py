"""Re-derive the L03 Example 2.3 arithmetic and the Theorem 1.3 closed form from the lab's own inputs (own code)."""
import random
rng = random.Random(7)
rec, dis = [], []
for w in range(1, 14):
    slump = -350_000 if 5 <= w <= 8 else 0
    rec.append(1_000_000 + rng.randint(-150_000, 150_000) + slump)
    dis.append(1_020_000 + rng.randint(-120_000, 120_000))
C0, m, K = 1_200_000, 1_000_000, 4_000_000
cash, drawn, rows = C0, 0, []
for r, d in zip(rec, dis):
    P = cash + r - d
    dr = rp = 0
    if P < m:
        dr = min(m - P, K - drawn)
    elif P > m and drawn > 0:
        rp = min(P - m, drawn)
    cash = P + dr - rp
    drawn += dr - rp
    rows.append((P, dr, rp, cash, drawn))
print("P6", rows[5][0], "expect 460095;", 1068160 + 530408 - 1138473)
print("draw6", rows[5][1], "expect 539905; end6", rows[5][3], "bal6", rows[5][4], "avail6", K - rows[5][4], "expect 3460095")
print("sum nu", sum(rec) - sum(dis), "closed form C_H", C0 + sum(rec) - sum(dis) + sum(r[1] - r[2] for r in rows), "last ending", rows[-1][3])
print("theorem 1.3 holds", rows[-1][3] == C0 + sum(rec) - sum(dis) + sum(r[1] - r[2] for r in rows))
