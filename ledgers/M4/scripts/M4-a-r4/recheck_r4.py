"""Exact recomputation (fractions) of the numbers on the M4-a slice pages. Run: python -I recheck_r4.py"""
import math
from fractions import Fraction as F

ok = []


def check(label: str, got: object, want: object) -> None:
    status = "OK" if got == want else "MISMATCH"
    ok.append(status)
    print(f"{status:8s} {label}: got {got} want {want}")


# L01 Example 3.6 and the M2/M3 problems, Example 3.5
law = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]
check("L01 sum weights", sum(p for _, p in law), 1)
cum, acc = [], F(0)
for _, p in law:
    acc += p
    cum.append(acc)
check("L01 F values", cum, [F(1, 10), F(3, 10), F(3, 5), F(4, 5), F(9, 10), F(1)])
check("L01 mean of table", sum(v * p for v, p in law), F(3, 10))
check("L01 (-2-2+0+2+2+3)/10", F(-2 - 2 + 0 + 2 + 2 + 3, 10), F(3, 10))
check("L01 148/150 = 74/75", F(148, 150), F(74, 75))
check("L01 74/75 decimal rounds 0.987", round(74 / 75, 3), 0.987)
check("L01 ceil(148.5)", math.ceil(F(99, 100) * 150), 149)
check("L01 ceil(198)", math.ceil(F(99, 100) * 200), 198)
check("L01 M2 F(5)", F(1, 5) + F(1, 2), F(7, 10))
check("L01 M3 40*0.901", float(F(901, 1000) * 40), 36.04)
check("L01 M3 ceil(36.04)", math.ceil(F(901, 1000) * 40), 37)

# L02 numbers
die = [(k, F(1, 6)) for k in range(1, 7)]
mu = sum(v * p for v, p in die)
ex2 = sum(v * v * p for v, p in die)
check("L02 die E[X]", mu, F(7, 2))
check("L02 die E[X^2]", ex2, F(91, 6))
check("L02 die Var", ex2 - mu * mu, F(35, 12))
check("L02 sd die 1.708", round(math.sqrt(35 / 12), 3), 1.708)
check("L02 Var(2X)", 4 * (ex2 - mu * mu), F(35, 3))
loss_e = F(250000) * F(1, 20)
loss_e2 = F(250000) ** 2 * F(1, 20)
check("L02 loss E[L]", loss_e, 12500)
check("L02 loss E[L^2]", loss_e2, 3125000000)
check("L02 loss Var", loss_e2 - loss_e * loss_e, 2968750000)
check("L02 sd loss to 2dp", f"{math.sqrt(2968750000):.2f}", "54486.24")
check("L02 sd loss /100 to 4dp", f"{math.sqrt(2968750000) / 100:.4f}", "544.8624")
check("L02 Var(D) = Var(L)/10^4", F(2968750000, 10000), 296875)
check("L02 misc: 91/6 about 15.17", f"{float(F(91, 6)):.2f}", "15.17")
check("L02 misc: 35/12 about 2.92", f"{float(F(35, 12)):.2f}", "2.92")
check("L02 M1 Var", F(3, 10) - F(9, 100), F(21, 100))
check("L02 M2 var", F(50000) ** 2 * F(1, 10) - F(5000) ** 2, F(225000000))
check("L02 M2 sd", math.isqrt(225000000), 15000)
check("L02 M3 var 3X-2", 9 * 4, 36)
check("L02 E2 expected count", 10000 * F(1, 20), 500)
check("L02 E2 gap 489", 500 - 489, 11)
check("L02 die sample mean gap 3.5-3.469", round(3.5 - 3.469, 3), 0.031)

# L03 numbers
SK = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu3 = sum(v * p for v, p in SK)
check("L03 mean", mu3, F(7, 4))
m2 = sum((v - mu3) ** 2 * p for v, p in SK)
m3 = sum((v - mu3) ** 3 * p for v, p in SK)
m4 = sum((v - mu3) ** 4 * p for v, p in SK)
check("L03 m2", m2, F(163, 16))
check("L03 m3", m3, F(2157, 32))
check("L03 m4", m4, F(149461, 256))
terms = [(v - mu3) ** 3 * p for v, p in SK]
check("L03 m3 terms", terms, [F(-1372, 512), F(-54, 512), F(1, 512), F(35937, 512)])
check("L03 10-term minus m3", F(35937, 512) - m3, F(1425, 512))
check("L03 squared skewness", m3 * m3 / m2**3, F(18610596, 4330747))
check("L03 skewness 2.073", f"{float(m3) / float(m2) ** 1.5:.4f}", "2.0730")
check("L03 kurtosis", m4 / (m2 * m2), F(149461, 26569))
check("L03 kurtosis 5.6254", f"{float(m4 / (m2 * m2)):.4f}", "5.6254")
check("L03 gap skew 2.073-2.065", round(2.073 - 2.065, 3), 0.008)
check("L03 gap kurt 5.625-5.580", round(5.625 - 5.580, 3), 0.045)
p = F(1, 10)
q = 1 - p
check("L03 Bern skew^2", (1 - 2 * p) ** 2 / (p * q), F(64, 9))
check("L03 Bern kurt", (1 - 3 * p * q) / (p * q), F(73, 9))
check("L03 Bern kurt 8.11", f"{float(F(73, 9)):.2f}", "8.11")
check("L03 Bern gamma", (1 - 2 * p) / math.sqrt(float(p * q)), 8 / 3)
p4 = F(1, 4)
check("L03 p=1/4 kurt", (1 - 3 * p4 * (1 - p4)) / (p4 * (1 - p4)), F(7, 3))
check("L03 p=1/4 gamma 1.155", f"{(1 - 2 * float(p4)) / math.sqrt(3 / 16):.3f}", "1.155")
# section 4 zero-skew law
Z = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
mz = sum(v * p for v, p in Z)
m2z = sum(v * v * p for v, p in Z)
m3z = sum(v**3 * p for v, p in Z)
m4z = sum(v**4 * p for v, p in Z)
check("L03 S4 mean", mz, 0)
check("L03 S4 m3", m3z, 0)
check("L03 S4 m2", m2z, 3)
check("L03 S4 m4", m4z, 15)
check("L03 S4 kappa", m4z / m2z**2, F(5, 3))
# M1 and M2 in L03
check("L03 M1 kappa p=1/4", F(7, 3), (1 - 3 * F(3, 16)) / F(3, 16))
check("L03 Bern p=1/10 gamma 8/3", F(4, 5) / F(3, 10), F(8, 3))
check("L03 Bern p=1/10 gamma 2.6667 display", f"{float(F(8, 3)):.4f}", "2.6667")

print(f"TOTAL {len(ok)} checks, {ok.count('MISMATCH')} mismatches")
