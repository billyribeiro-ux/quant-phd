"""Round 28 independent recomputation of the L02 numbers touched by the delta and the rewritten sentences (Fractions only)."""
from fractions import Fraction as Fr

p, v, F, S, T = Fr(25), Fr("11.5"), Fr(1200), Fr(27000), 2000   # USD, Lab 1 inputs (cents /100)
m = p - v
print("m (USD/unit)", m, "ratio", m / p)
Qs = F / m
print("single-formula break-even", float(Qs), "first whole", -(-Qs.numerator // Qs.denominator))
print("formula with step", float((F + S) / m))
def oi(q):  # USD, integer units
    return m * q - F - (S if q > T else 0)
print("OI(88)", float(oi(88)), "OI(89)", float(oi(89)), "OI(2000)", float(oi(2000)), "OI(2001)", float(oi(2001)), "OI(2089)", float(oi(2089)))
runs, start = [], None
for q in range(5001):
    neg = oi(q) < 0
    if neg and start is None: start = q
    if not neg and start is not None: runs.append((start, q - 1)); start = None
if start is not None: runs.append((start, 5000))
print("loss runs", runs)
R_be = p * Qs
print("R_BE (USD)", float(R_be), "= F/(m/p)", float(F / (m / p)), "= pF/m", float(p * F / m))
print("identity F/(m/p) = pF/m exact:", F / (m / p) == p * F / m)
print("multiplying num and den by p: (F*p)/((m/p)*p) =", (F * p) / ((m / p) * p), " ; by 1/p gives (F/p)/((m/p)/p) =", (F / p) / ((m / p) / p))
planned = Fr(2500)
print("OI(2500)", float(oi(2500)), "margin of safety", float(planned - (F + S) / m), "share", float((planned - (F + S) / m) / planned * 100))
print("DOL", float(m * planned / oi(2500)), "OI(2525)/OI(2500)-1 %", float((oi(2525) - oi(2500)) / oi(2500) * 100))
print("fixed +100 USD shifts break-even by", float(((F + 100) / m) - Qs))
print("R2 derivative per USD", float(-F / (m ** 2)), "per cent", float(-F / (m ** 2)) / 100 * 1)
print("R2 exact 1 USD rise", float(F / (m + 1) - F / m))
print("E2 margin from first BE", float(planned - Qs))
print("M1 BE", 45000 / 30, "revenue", 45000 / (30 / 80), "check", 80 * 1500)
print("M2", float(Fr(10000, 7)), 7 * 1429 - 10000, 7 * 1428 - 10000)
print("Q_BE from 10000 fixed, 13.50 margin, 0.01 cents", float(Fr(10000) / Fr("13.5")), float(Fr(100) / Fr("13.5")))
print("Ex 2.4 R", Fr(60000) / (Fr(20) / Fr(50)), "Q", Fr(60000) / 20)
print("P3", Fr(60000) / (Fr(10) * Fr(1, 2) + Fr(30) * Fr(1, 2)))
print("R3 below 1000 break-even", Fr(60000) / 10, "above", Fr(60000) / 20)
