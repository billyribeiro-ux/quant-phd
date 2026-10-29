"""Independent recomputation of the printed numbers on FC1 L01-L03 and the hub (exact Fractions)."""
from fractions import Fraction as F
import math

def half_up_cents(x):
    return math.floor(x * 100 + F(1, 2))

d, rho = F(1000), F(1, 10)
S10 = d * (1 - (1 - rho) ** 11) / rho
print("L01 Ex3.3 S10 exact", float(S10), "cents", half_up_cents(S10), "mult", float(S10 / d))
print("L01 Remark3.4 rounded mult 6.8619 x1000 =", F("6.8619") * 1000)
lim_half = d / (1 - F(1, 2) * (1 - rho))
print("L01 Ex3.6 limit", float(lim_half), "cents", half_up_cents(lim_half), "pct of full", float(lim_half / 10000 * 100))
print("L01 E2 ratio", lim_half / 10000, "== 2/11:", lim_half / 10000 == F(2, 11), "1/5.5 =", F(1) / F(11, 2))
print("L01 M2 S2", 800 * (1 - F(3, 4) ** 3) / F(1, 4), "stage deposits", 800, 600, 450)
print("L01 M3 equity", 300 - 320, "P-E", 100 - 60)
print("L01 quiz S2/d rho=1/2", (1 - F(1, 2) ** 3) / F(1, 2), "limit 1000/0.1", d / rho)
print("L01 quiz 400*1.75", 400 * F(7, 4))
print("L02 counts: exposures rates 3 credit 2 ... derivative 6 cash 6 exch 4 otc 8")
print("L02 pct derivative of exchange 3/4 =", F(3, 4) * 100)
print("hub hours split", float(F(50, 70) * 100), float(F(20, 70) * 100), "mastery 8/9", float(F(8, 9) * 100), "7/9", float(F(7, 9) * 100))
print("hub PV 110/1.1", F(110) / F(11, 10), "compound", F(1000) * F(21, 20) ** 2)
print("hub coupon", 10000 * 500 // 10000, "period-3 flow", 500 + 10000)
print("L03 Ex1.4 relative", F(30, 5000), "M3 same", F(30, 5000))
print("L03 E3 relative 6/20000 pct", F(6, 20000) * 100)
print("L03 Ex2.5 cash", -9998 * 100 + 9992 * 100, "spread term", 2 * 200, "midmove", (-1) * 100 * (10000 - 9990) + 100 * (9990 - 9990))
print("L03 R2 cash", -(9988 * 100) + 10002 * 100, "midmove", (-1) * 100 * (9990 - 10000) + 100 * 0)
print("L03 M1 cash", 10002 * 50 - 9998 * 50, "s*Q", 4 * 50)
print("L03 M2 cash", 10006 * 80 - 10008 * 80, "midmove", (-1) * 80 * (10010 - 10004), "hV", 2 * 160)
print("L03 misc2 V vs count, two 100-share trades: hV", 2 * 200, "count-based", 2 * 2)
print("L03 q7 k=3 profit", 3 * 1000 // 2, "dev 102", 2 * 1000, "R1 3-dealer (c+2)^3 share 2Q/3 vs Q")
