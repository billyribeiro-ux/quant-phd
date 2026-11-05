"""Round-10 independent recomputation for SC1 slice b (L04-L06). Own code, no twin imports."""
import math
from fractions import Fraction
from functools import lru_cache

def erfc(x): return math.erfc(x)
def Phi(x): return 0.5 * math.erfc(-x / math.sqrt(2.0))

print("L04 closed forms (9 dp):")
print(f"  e^1 = {math.exp(1):.9f}  (L04 expected 2.718281828)")
print(f"  e^0.25 = {math.exp(0.25):.9f}  (E1 expected 1.284025417)")
print(f"  e^4 = {math.exp(4):.9f}  (expected 54.598150033)")
print(f"  e^8 = {math.exp(8):.6f}  (E2/E3 expected 2980.957987)")
print(f"  e^(4*2)=e^8 check theta=2,t=2: theta^2 t = {4*2} -> e^8 = {math.exp(8):.10f}")

print("L05 numbers:")
print(f"  Phi(-1/sqrt2) = {Phi(-1/math.sqrt(2)):.10f} (expected 0.2397500611; Q9 tol 1e-5 around 0.23975)")
print(f"  p_1(0,0) = {1/math.sqrt(2*math.pi):.10f} (Q p_1(0,0) expected 0.3989 to 4 dp)")
print(f"  1/(2 sqrt pi) = {1/(2*math.sqrt(math.pi)):.10f}; p_2(0,0) = {1/math.sqrt(4*math.pi):.10f}")
print(f"  ratio 5.55e-16/3.81e-29 = {5.55e-16/3.81e-29:.4e} (E1 says ~1.457e13, 1.5e13 to 2 sf)")
print(f"  5.55e-16 / eps(2.22e-16) = {5.55e-16/2.22e-16:.3f} (interpretation says about 2.5)")
print(f"  3.05e-16 / 2.22e-16 = {3.05e-16/2.22e-16:.3f} (E3 says about 1.4)")
print(f"  unrounded half-width of 10dp printed value: [{1-5e-11:.11f}, {1+5e-11:.11f}]")
print(f"  int_(-12)^12 p_2(0,y)dy exact = erf(6) = {math.erf(6.0):.17f} (printed 1.0000000000)")
print(f"  int_(-12)^12 p_1(0,y)dy exact = erf(12/sqrt2) = {math.erf(12/math.sqrt(2)):.17f}")
print(f"  2^-52 machine eps = {2**-52:.3e}")

print("L06 numbers:")
print(f"  erfc(1/sqrt2) = {erfc(1/math.sqrt(2)):.12f} (expected 0.3173105079, printed 0.3173105079)")
print(f"  P(B_1>1) = {erfc(1/math.sqrt(2))/2:.12f}; half of printed 0.3173105079 = {0.3173105079/2:.11f}")
print(f"  P(B_1>=1) to 4dp = {round(erfc(1/math.sqrt(2))/2,4)}")
print(f"  2P(B_1>1)=0.3173 vs erfc 4dp: {round(erfc(1/math.sqrt(2)),4)}")
print(f"  |0.3173105079-0.3173| = {abs(erfc(1/math.sqrt(2))-0.3173):.2e} (tol 1e-4)")
print(f"  |P(B_1>=1)-0.1587| = {abs(erfc(1/math.sqrt(2))/2-0.1587):.2e} (tol 1e-4)")

# Independent DP over the random walk: count of paths by (max>=a, endpoint).
def dist(N):
    # returns dict (max, end) -> count using DP over (position, running max)
    states = {(0, 0): 1}
    for _ in range(N):
        nxt = {}
        for (pos, mx), c in states.items():
            for step in (1, -1):
                p2 = pos + step
                m2 = max(mx, p2)
                nxt[(p2, m2)] = nxt.get((p2, m2), 0) + c
        states = nxt
    out = {}
    for (pos, mx), c in states.items():
        out[(mx, pos)] = out.get((mx, pos), 0) + c
    return out

A = B = 0
Aeq = Beq = 0
for N in range(1, 13):
    d = dist(N)
    endc = {}
    for (mx, e), c in d.items():
        endc[e] = endc.get(e, 0) + c
    for a in range(1, N + 1):
        # Part B
        maxima = sum(c for (mx, e), c in d.items() if mx >= a)
        atl = sum(c for (mx, e), c in d.items() if e >= a)
        ab = sum(c for (mx, e), c in d.items() if e > a)
        B += 1
        Beq += (maxima == atl + ab)
        for b in range(-N, a):
            A += 1
            lhs = sum(c for (mx, e), c in d.items() if mx >= a and e == b)
            Aeq += (lhs == endc.get(2 * a - b, 0))
print(f"independent DP: Part A triples {A} equal {Aeq}; Part B pairs {B} equal {Beq}")

d12 = dist(12)
print("Part C N=12 a=3: M>=3:", sum(c for (mx, e), c in d12.items() if mx >= 3), "of 4096;",
      "M>=3 & S=2:", sum(c for (mx, e), c in d12.items() if mx >= 3 and e == 2),
      "; S=4:", sum(c for (mx, e), c in d12.items() if e == 4))
d10 = dist(10)
tail = Fraction(sum(c for (mx, e), c in d10.items() if mx >= 2), 1024)
above = Fraction(sum(c for (mx, e), c in d10.items() if e > 2), 1024)
at = Fraction(sum(c for (mx, e), c in d10.items() if e == 2), 1024)
print(f"Part D N=10 a=2: P(M>=2)={tail} P(S>2)={above} 2P(S>2)={2*above} P(S=2)={at} diff_ok={tail-2*above==at}")
print("binom(10,6)/1024 =", Fraction(math.comb(10, 6), 1024))
print("M1 (N=3,a=1) count:", sum(c for (mx, e), c in dist(3).items() if mx >= 1), "of 8")
print("M2 (N=2,a=2) P:", Fraction(sum(c for (mx, e), c in dist(2).items() if mx >= 2), 4))
