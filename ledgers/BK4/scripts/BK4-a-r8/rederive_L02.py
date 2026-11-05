"""Independent re-derivation of BK4 L02 Lab 1 printed values and the worked numbers (exact integers and Fraction)."""
import random
from fractions import Fraction

rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    payer, rec = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((seq, payer, rec, 100 * dollars))
for seq, p, r, c in trades:
    print(f"trade {seq}: member {p + 1} owes member {r + 1} {c:>8d} cents")
G = sum(c for *_, c in trades)
rec = [sum(c for _, p, r, c in trades if r == m) for m in range(4)]
pay = [sum(c for _, p, r, c in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
print("receivable", rec, "payable", pay)
print("G", G, "sum rec", sum(rec), "n", n, "sum n", sum(n), "A", A, "sum max(0,-n)", sum(max(0, -x) for x in n))
bp = (10000 * (G - A)) // G
print("reduction", G - A, "bp floor", bp, "exact", float(Fraction(10000 * (G - A), G)))
print("A + reduction == G", A + (G - A) == G, "A <= G", A <= G)
ok = (G == 7596300 and rec == [314500, 2067800, 3340300, 1873700] and pay == [3941500, 314500, 0, 3340300]
      and n == [-3627000, 1753300, 3340300, -1466600] and A == 5093600 and G - A == 2502700 and bp == 3294)
print("MATCHES_L02_PART_B_TO_D", ok)
# Example 2.4 and problems
def red(nets_trades):
    G = sum(a for _, _, a in nets_trades)
    m_ids = sorted({x for p, r, _ in nets_trades for x in (p, r)})
    n = {m: sum(a for p, r, a in nets_trades if r == m) - sum(a for p, r, a in nets_trades if p == m) for m in m_ids}
    A = sum(max(0, v) for v in n.values())
    return G, A, n, (10000 * (G - A)) // G
print("Ex2.4", red([(1, 2, 100), (2, 3, 80), (3, 1, 50)]))
print("M1", red([(1, 2, 50), (2, 3, 70), (3, 4, 20), (4, 1, 40)]))
print("M2", red([(1, 2, 200), (2, 3, 160), (3, 1, 100)]))
print("M3", red([(1, 2, 100), (1, 3, 100)]))
print("R2 Y", red([(1, 2, 100), (3, 4, 50), (4, 3, 50)]))
print("Ex2.4 exact share", Fraction(10000 * 180, 230), float(Fraction(10000 * 180, 230)))
