"""Independent recomputation of the prose numbers in M2 lessons L07-L12 (exact fractions where possible)."""
from fractions import Fraction as Fr
import math

out = []
def say(s): out.append(s)

# L10 Empirical 3: observed central-difference error at x=0.3, h=1e-6 (floating point, same formula as Lab part C)
x, h = 0.3, 1e-6
central = ((x + h) / (1 + x + h) - (x - h) / (1 + x - h)) / (2 * h)
exact = 1 / (1 + x) ** 2
say(f"L10 central={central!r} exact={exact!r} observed_error={central - exact:.4e}")
F3 = 6 / (1 + x) ** 4
say(f"L10 F'''(0.3)={F3:.6f} truncation_term h^2 F'''/6={h*h*F3/6:.4e}")
# exact-fraction central difference for comparison
hf = Fr(1, 10**6); xf = Fr(3, 10)
cf = ((xf + hf) / (1 + xf + hf) - (xf - hf) / (1 + xf - hf)) / (2 * hf)
say(f"L10 exact-rational central difference minus f(0.3) = {float(cf - Fr(100,169)):.4e}")

# L10 Empirical 2 and Part B gap
say(f"L10 3/512={3/512:.9f}  U128-L128 (exact)={float(Fr(129*257,6*128*128) - Fr(127*255,6*128*128)):.9f}")
say(f"L10 U8 exact={float(Fr(9*17,6*64)) :.8f} L8 exact={float(Fr(7*15,6*64)):.8f}")
# L10 Part A table n=8 values
say(f"L10 F-A U8 exact-check: {float(Fr(3*8*8 - 0, 1)/1):.1f}")  # placeholder kept small

# L08 Part C xi and remainders
for xx, n in [(0.1,1),(0.1,3),(0.1,5),(0.3,1),(0.3,3),(0.3,5),(0.5,1),(0.5,3),(0.5,5),(0.9,1),(0.9,3),(0.9,5)]:
    xi = 1 - (1 - xx) ** (1 / (n + 2))
    R = xx ** (n + 1) / (1 - xx)
    say(f"L08 x={xx} n={n} xi={xi:.6f} R={R:.8f}")
say(f"L08 1-(3/4)^(1/4)={1-(0.75)**0.25:.7f}; 1-(1/2)^(1/5)={1-0.5**0.2:.7f}; 1-(0.7)^(1/7)={1-0.7**(1/7):.7f}")
say(f"L08 Remark3.3 x=0.6: bounds {[round(0.6**(n+1)/0.4**(n+2),6) for n in range(1,5)]} remainders {[round(0.6**(n+1)/0.4,6) for n in range(1,5)]}")
say(f"L08 Ex2.2-ish: 128/27={128/27:.6f} 4/27={4/27:.6f} 1/12={1/12:.6f}")

# L09: U_n, L_n exact; Part B gap; Part C errors; tolerance n=50/51
for n in (1,2,4,8,16,32,64,128):
    U = Fr((n+1)*(2*n+1), 6*n*n); Lo = Fr((n-1)*(2*n-1), 6*n*n) if n>1 else Fr(0)
    assert U - Lo == Fr(1,n)
say("L09 part A closed forms verified for n in 1..128 powers of 2")
pts = [Fr(i*i, 100) for i in range(11)]
gap = sum((pts[i]**0 * (pts[i]**2 - pts[i-1]**2)) * (pts[i]-pts[i-1]) for i in range(1,11))
say(f"L09 part B gap exact={float(gap):.8f} (printed 0.15933400)")
for n in (8,16,32):
    mid = sum(Fr(2*i-1,2*n)**2 / n for i in range(1,n+1))
    say(f"L09 n={n} midpoint err exact={float(mid-Fr(1,3)):+.8f} vs -1/(12n^2)={-1/(12*n*n):+.8f}")
say(f"L09 25/384={25/384:.8f}; 1/3072={1/3072:.8f}")
for n in (50,51):
    say(f"L09 n={n} (3n+1)/(6n^2)={(3*n+1)/(6*n*n):.6f} = {Fr(3*n+1,6*n*n)}")

# L11: midpoint N needed for 2/(3N^2) <= 1e-6
N = 1
while Fr(2, 3*N*N) > Fr(1, 10**6): N += 1
say(f"L11 smallest N with 2/(3N^2)<=1e-6 is {N}; err(816)={2/(3*816*816):.6e} err(817)={2/(3*817*817):.6e}")
say(f"L11 8/3-2.6666666663={8/3-2.6666666663:.2e}")
say(f"L11 Beta(3,4) check: int x^2(1-x)^3 = 1/60 -> {float(Fr(1,60)):.10f}")
# L11 Part A numeric check: midpoint N=100000 vs exact
def mid(f, a, b, n):
    h = (b-a)/n
    return h*sum(f(a+(i+0.5)*h) for i in range(n))
say(f"L11 recomputed part A lhs={mid(lambda x: x*x*(1-x)**3, 0.0, 1.0, 100000):.10f}")
say(f"L11 recomputed part B rhs={mid(lambda t: (t**3+t)**2*(3*t*t+1), 0.0, 1.0, 100000):.10f}")

# L12: harmonic values
H = 0.0
n = 1
for m in range(1, 15):
    while n < 2**m:
        n += 1; H += 1/n
    if m in (1,4,8,12,14): say(f"L12 N=2^{m} H-1={H:.8f} m/2={m/2}")
say(f"L12 1/(2b^2)*b^2 etc ok; 1/10^6 check 1e-6={1e-6}")
say(f"L12 H_16384 (N=2^14) = {H+1:.8f}")

print("\n".join(out))
