"""Independent re-derivation of every printed value in BK4 L01 Lab 1 and the worked numbers (Fraction arithmetic)."""
import random
from fractions import Fraction

EXPECT_B = {
    "A": (112500, 379800, 0),
    "B": (1533900, -1533900, 1533900),
    "C": (0, 1154100, 0),
}
rng = random.Random(20260)
day = []
for seq in range(1, 13):
    s, r = rng.sample(range(3), 2)
    dollars = rng.randint(100, 5000)
    day.append((seq, s, r, 100 * dollars))
names = "ABC"
print("day:", [(names[s], names[r], c) for _, s, r, c in day])
ok = True
for b in range(3):
    S = [0]
    for _, s, r, c in day:
        S.append(S[-1] + (c if r == b else 0) - (c if s == b else 0))
    need = max(0, -min(S))
    net = S[-1]
    debit = max(0, -net)
    exp = EXPECT_B[names[b]]
    same = (need, net, debit) == exp
    ok &= same
    print(names[b], "need", need, "net", net, "debit", debit, "need>=debit", need >= debit, "matches L01 Part B:", same)
gross = sum(c for *_, c in day)
moved = sum(max(0, -(sum((c if r == b else 0) - (c if s == b else 0) for _, s, r, c in day))) for b in range(3))
print("gross", gross, "moved", moved, "matches 2841600/1533900:", gross == 2841600 and moved == 1533900)
print("ratio", Fraction(moved, gross), float(Fraction(moved, gross)), round(float(Fraction(moved, gross)), 4))
print("cents to dollars", 2841600 // 100)
# Example 2.6 (A pays B 100; B pays C 80; C pays A 50), dollars
def peak_and_debit(seq):
    out = {}
    for b in sorted({x for s, r, _ in seq for x in (s, r)}):
        S = [0]
        for s, r, a in seq:
            d = (a if r == b else 0) - (a if s == b else 0)
            S.append(S[-1] + d)
        out[b] = (max(0, -min(S)), S[-1], max(0, -S[-1]), S)
    return out
ex = peak_and_debit([("A", "B", 100), ("B", "C", 80), ("C", "A", 50)])
print("Example 2.6 need/net/debit:", {k: v[:3] for k, v in ex.items()}, "A running", ex["A"][3], "gross", 100 + 80 + 50)
rm = peak_and_debit([("C", "A", 50), ("A", "B", 100), ("B", "C", 80)])
print("Remark 2.7 A running", rm["A"][3], "need", rm["A"][0], "debit", rm["A"][2])
r3 = peak_and_debit([("A", "B", 100), ("B", "C", 100), ("C", "A", 100)])
print("R3 nets", [r3[b][1] for b in "ABC"], "debits", [r3[b][2] for b in "ABC"], "A running", r3["A"][3], "need A", r3["A"][0])
m1 = peak_and_debit([("X", "D", 300), ("D", "X", 500)])
print("M1 D running", m1["D"][3], "need", m1["D"][0], "debit", m1["D"][2])
m3 = peak_and_debit([("X", "D", 40), ("D", "X", 70), ("X", "D", 10)])
print("M3 D running", m3["D"][3], "need", m3["D"][0], "debit", m3["D"][2])
print("ALL_PART_B_MATCH", ok)
