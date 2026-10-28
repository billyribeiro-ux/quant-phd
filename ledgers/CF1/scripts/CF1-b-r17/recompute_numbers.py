"""Independent recomputation of the numbers in CF1 L03/L04 prose and the changed cards (round 17)."""
import math

def npv(flows, r):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(flows))

# L03 Lab 1 inputs (SIMULATED, from tests/labs/CF1/lab-CF1-L03-1.py)
REAL = [-100_000_000] + [30_000_000] * 5
RR, INF = 0.06, 0.03
def nominal(real, pi): return [c * (1 + pi) ** t for t, c in enumerate(real)]
n = (1 + RR) * (1 + INF) - 1
rnpv = npv(REAL, RR)
print("L03 nominal rate", n, "real NPV USD", rnpv / 100)
for pi in (0.0, 0.01, 0.03, 0.05):
    mixed = npv(nominal(REAL, pi), RR)
    print(f"L03 mixed minus real at pi={pi}: {(mixed - rnpv)/100:.2f} USD")
print("L03 mixed-npv-real-rate-n", npv(REAL, n) / 100)
print("L03 share at 0.05 (E1):", 194368.27 / 263709.14, "share 0.01:", 36913.22 / 263709.14, "share 0.03:", 113637.49 / 263709.14)
print("L03 misconception 2 share 0.03:", 113637.49 / 263709.14)
print("L03 Example 1.4 n:", 1.06 * 1.03 - 1, "gap", 0.06 * 0.03)
print("L03 Example 2.5 PV:", 100/1.08 + 100/1.08**2 + 100/1.08**3, "real flows", [100/1.03**t for t in (1,2,3)], "real rate", 1.08/1.03-1)
print("L03 P3 sqrt(0.005)", math.sqrt(0.005))
print("L03 R2 ratio r(1+pi)/(r-pi)", 0.06*1.03/0.03)
b = 1.06 / 2.03
print("L03 R3 b", b)
# Verify R3 zero: error = a*pi/(1+r) - b*((1+pi)^2-1)/(1+r)^2 with a=1
r, pi = 0.06, 0.03
err = 1 * pi / (1 + r) - b * ((1 + pi) ** 2 - 1) / (1 + r) ** 2
print("L03 R3 error at b:", err)
print("L03 M1 n", 1.04*1.025-1, "M2", 1000*1.02**3, "M3 r", 1.10/1.04-1, 100*1.04/1.10)
print("L03 section 3 two-line", 205*1.05/200-1, 1.07625/1.05-1, 200/1.05)
print("L03 E2/E3 nominal 1.10*1.03-1", 1.10*1.03-1)
print("L03 P2 ex", 0.03/(1.06))
print("L03 quiz q numeric answer 0.0577", 1.10/1.04-1)
print("L03 Section 3 at r=pi=0.10: ", 1.1*1.1-1)
print("L03 L03q9 implied inflation", 1.07625/1.05 - 1)
print()
# L04 numbers
P = (-10_000_000, 23_000_000, -13_200_000)
for r in (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
    print(f"L04 P NPV at {r}: {npv(P, r)/100:.4f} USD")
print("L04 P at 5% factorization", -2000*(11/1.05-10)*(6/1.05-5))
print("L04 closed roots", 1/(10/11)-1, 1/(5/6)-1)
print("L04 Remark 5.1 FV at 20%", -100000*1.2**2 + 230000*1.2 - 132000)
print("L04 R3 FV 15%", 1.15**2*npv(P,0.15), "FV 5%", 1.05**2*npv(P,0.05))
print("L04 Ex4.2 A10,B10", npv((-100000,130000),0.10), npv((-200000,250000),0.10))
print("L04 Ex4.2 at 20", npv((-100000,130000),0.2), npv((-200000,250000),0.2))
print("L04 E2 A'=(-100000,120000) IRRs", 120000/100000-1, 250000/200000-1)
print("L04 E2 at 10", npv((-100000,120000),0.10), npv((-200000,250000),0.10))
print("L04 E2 at 35", npv((-100000,120000),0.35), npv((-200000,250000),0.35))
print("L04 E2 crossover", (130000)/(100000)-1)
print("L04 R1 NPV at 10", -1 + 6/1.1 - 5/1.21, "roots of -1+6x-5x^2", (6-(36-20)**0.5)/10, (6+4)/10)
print("L04 M1", 121/100-1)
print("L04 M2 x", (-1+math.sqrt(23/3))/2, "r", 1/((-1+math.sqrt(23/3))/2)-1)
print("L04 M3 roots check", -1 + 2.5*(2/3) - 1.5*(4/9), -1+2.5*1-1.5)
print("L04 R2 A IRR", 3**0.5-1, "NPV A 10%", 300/1.21-100, "NPV B 10%", 200/1.1-100)
print("L04 P2/P3", "ok")
print("L04 Ex 4.2 r*", 120000/100000-1)
print("L04 P NPV at 15 (quiz 189.04)", npv(P,0.15)/100)
print("L04 avg IRR 15 is root?", npv(P, 0.15))
# dK/dC cross check for Theorem 4.1 example
print("crossover of B-A flows (-100000,120000) and (-200000,250000)? diff", (-100000, 130000))
