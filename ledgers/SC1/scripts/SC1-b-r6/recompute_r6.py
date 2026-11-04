"""Independent recomputation of every number printed or quoted in SC1 L04-L06 (round 6, verifier independent of tools/)."""
import math
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 50

print("== L04")
for theta in (-1.0, 0.5, 2.0):
    t = 2.0
    print(f"theta={theta}: exp(theta^2 t/2)={math.exp(theta*theta*t/2):.9f}")
print("e^1", f"{math.e:.9f}", "e^0.25", f"{math.exp(0.25):.9f}", "e^4", f"{math.exp(4):.9f}", "e^8", f"{math.exp(8):.6f}", f"{math.exp(8):.9f}")
print("E1 e^{0.25}->", f"{math.exp(0.25):.9f}")
print("M2 E[Z_2]=e^-1*e=", math.exp(-1)*math.exp(1))
print("Var(Z_t) theta=0 ->", math.exp(0)-1)
print("E2 e^8 approx:", f"{math.exp(8):.6f}")

print("== L05")
def dens(u, x, y):
    return math.exp(-((y - x) ** 2) / (2 * u)) / math.sqrt(2 * math.pi * u)
# independent quadrature: trapezoid with many nodes on [-12,12], and Gauss-Legendre-free check via fine trapezoid
def trap(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b)) + sum(f(a + i * h) for i in range(1, n))
    return s * h
TIMES = (0.5, 1.0, 2.0)
POINTS = (-1.0, -0.25, 0.0, 0.5, 1.0)
worst = 0.0
cnt = 0
for s in TIMES:
    for t in TIMES:
        for x in POINTS:
            for y in POINTS:
                val = trap(lambda z: dens(s, x, z) * dens(t, z, y), -12.0, 12.0, 4000)
                worst = max(worst, abs(val - dens(s + t, x, y)))
                cnt += 1
print("cases", cnt, "trap(4000) worst gap", f"{worst:.3e}")
ex = trap(lambda z: dens(1.0, 0.5, z) * dens(2.0, z, -0.25), -12.0, 12.0, 4000) - dens(3.0, 0.5, -0.25)
print("example gap (trap4000)", f"{ex:+.3e}")
for t in TIMES:
    print("mass p_%g(0,.) on [-12,12] (trap4000)" % t, f"{trap(lambda y: dens(t, 0.0, y), -12.0, 12.0, 4000):.12f}")
# tail mass (independent): 12<=|z|<=40 for all 225 cases, use trapezoid
worst_tail = 0.0
for s in TIMES:
    for t in TIMES:
        for x in POINTS:
            for y in POINTS:
                f = lambda z: dens(s, x, z) * dens(t, z, y)
                tail = trap(f, 12.0, 40.0, 4000) + trap(f, -40.0, -12.0, 4000)
                worst_tail = max(worst_tail, tail)
print("worst tail mass (trap, 12<=|z|<=40) %.3e" % worst_tail)
print("ratio gap/tail ~", f"{5.55e-16/3.81e-29:.4e}")
print("eps ratio 5.55e-16/2.22e-16 =", 5.55e-16/2.220446049250313e-16, " 3.05e-16/eps=", 3.05e-16/2.220446049250313e-16)
print("p_1(0,0)=", f"{dens(1.0,0.0,0.0):.10f}")
print("(2pi)^-1/2=", f"{(2*math.pi)**-0.5:.10f}")
def Phi(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))
print("Phi(-1/sqrt2)=", f"{Phi(-1/math.sqrt(2)):.10f}")
print("M1 L05 (u=v=1, x=y=0): integral", f"{(2*math.pi)**-1*math.sqrt(math.pi):.10f}", "p2(0,0)", f"{dens(2.0,0.0,0.0):.10f}")
print("P2 check: 1/(2 sqrt pi)=", f"{1/(2*math.sqrt(math.pi)):.10f}")
print("M2 L05: psi(x)=x^2+2, x^3+6x (Z~N(0,2))")

print("== L06")
def summaries(n):
    # DP over (position, running max) counts with exact integers
    from collections import defaultdict
    states = {(0, 0): 1}  # (S, M) -> count
    for _ in range(n):
        nxt = defaultdict(int)
        for (s, m), c in states.items():
            for e in (1, -1):
                s2 = s + e
                nxt[(s2, max(m, s2))] += c
        states = nxt
    return states  # (S_N, M_N) -> count
for N in range(1, 13):
    st = summaries(N)
    tot = sum(st.values())
    assert tot == 2 ** N
# Part A/B independent via DP
trip = eq = 0
for N in range(1, 13):
    st = summaries(N)
    for a in range(1, N + 1):
        for b in range(-N, a):
            trip += 1
            lhs = sum(c for (e, m), c in st.items() if m >= a and e == b)
            rhs = sum(c for (e, m), c in st.items() if e == 2 * a - b)
            eq += lhs == rhs
print("triples", trip, "equal", eq)
pairs = 0; teq = 0
for N in range(1, 13):
    st = summaries(N)
    for a in range(1, N + 1):
        pairs += 1
        lhs = sum(c for (e, m), c in st.items() if m >= a)
        rhs = sum(c for (e, m), c in st.items() if e >= a) + sum(c for (e, m), c in st.items() if e > a)
        teq += lhs == rhs
print("tail pairs", pairs, "equal", teq)
st12 = summaries(12)
print("M_12>=3:", sum(c for (e, m), c in st12.items() if m >= 3), "of 4096")
print("M_12>=3 & S_12=2:", sum(c for (e, m), c in st12.items() if m >= 3 and e == 2))
print("S_12=4:", sum(c for (e, m), c in st12.items() if e == 4))
st10 = summaries(10)
tail = Fraction(sum(c for (e, m), c in st10.items() if m >= 2), 1024)
above = Fraction(sum(c for (e, m), c in st10.items() if e > 2), 1024)
at = Fraction(sum(c for (e, m), c in st10.items() if e == 2), 1024)
print("P(M10>=2)", tail, float(tail), "2P(S10>2)", 2*above, float(2*above), "P(S10=2)", at, float(at), "diff==at", tail-2*above == at)
print("binom(10,6)/1024 =", Fraction(math.comb(10, 6), 1024))
print("erfc(1/sqrt2)=", f"{math.erfc(1/math.sqrt(2)):.10f}", " half=", f"{math.erfc(1/math.sqrt(2))/2:.12f}")
print("P(B1>=1) rounded 4dp:", f"{math.erfc(1/math.sqrt(2))/2:.4f}", " 2P rounded:", f"{math.erfc(1/math.sqrt(2)):.4f}")
print("P(M1>=1) via Phi:", f"{2*(1-Phi(1.0)):.10f}")
print("78 pairs check: sum n=1..12 =", sum(range(1, 13)))
print("1014 triples check:", sum(n*(n+1)//2 + n*n for n in range(1, 13)))
