# Round 4 verifier recomputation, SC1 slice b (L04-L06): every number quoted in prose, expected blocks, quiz and cards.
import itertools
import math
from fractions import Fraction

print("== L04")
print("e^(1/4) =", f"{math.exp(0.25):.9f}", "(L04 E1 and expected block: 1.284025417)")
print("e^1 =", f"{math.exp(1):.9f}", "e^4 =", f"{math.exp(4):.9f}", "(expected: 2.718281828, 54.598150033)")
print("e^8 =", f"{math.exp(8):.6f}", "(L04 E2/E3: 2980.957987)")
print("theta^2 t/2 for theta=2,t=2:", 4 * 2 / 2, "; for theta=-1:", 1 * 2 / 2, "; theta=0.5:", 0.25 * 2 / 2)
print("E[W^2] check e^{theta^2 h} for theta=1,h=1 :", math.exp(1), "vs E[e^{2 Y}] e^{-1}:", math.exp(-1) * math.exp(2))
print("L04 Q4: E[B_3^4] =", 3 * 3**2, "; Q3: E[B_3^2] =", 3)
print("L04 Q7/M2: e^(1) to 9dp:", f"{math.e:.9f}", " |2.718281828-e| =", abs(2.718281828 - math.e))
print("L04 Q10 |54.598150033 - e^4| =", abs(54.598150033 - math.exp(4)))

print("== L05")
print("cases:", 3 * 3 * 5 * 5)
print("5.55e-16/3.81e-29 =", f"{5.55e-16 / 3.81e-29:.4e}", "(E1: about 1.5e13)")
print("5.55e-16/2.22e-16 =", f"{5.55e-16 / 2.22e-16:.3f}", "(interpretation: about 2.5)")
print("3.05e-16/2.22e-16 =", f"{3.05e-16 / 2.22e-16:.3f}", "(E3: about 1.4)")
print("(2 pi)^(-1/2) =", f"{(2 * math.pi) ** -0.5:.9f}", "(Q4 0.3989)")
print("Phi(-1/sqrt2) =", f"{0.5 * math.erfc((1 / math.sqrt(2)) / math.sqrt(2)):.10f}", "(Q9 0.23975006)")
print("M2: E[(x+Z)^3] with Z~N(0,2): x^3 + 6x ; check at x=1:", 1 + 6, "by Monte-free exact moment: E[Z^3]=0, E[Z^2]=2")
# exact check of the Z-moments by integrating against the N(0,2) density numerically
def gauss_moment(k, var):
    # E[Z^k] for N(0,var), exact via recursion
    if k % 2:
        return 0.0
    m = 1.0
    for j in range(1, k, 2):
        m *= j * var
    return m
print("E[Z^2], E[Z^3] for N(0,2):", gauss_moment(2, 2.0), gauss_moment(3, 2.0))
print("P1 check: lhs=(4z^2-2z+1)/3 at z=0.3 ->", (4 * 0.09 - 0.6 + 1) / 3, " rhs=", (4 / 3) * (0.3 - 0.25) ** 2 + 0.25)
print("E1 integral check: Chapman-Kolmogorov one case numeric; see lab twin output")
print("Simpson vs erfc sanity: P(B_1 >= 1) =", f"{0.5 * math.erfc(1 / math.sqrt(2)):.10f}")
print("M1 (L05): 1/(2 sqrt pi)=", f"{1 / (2 * math.sqrt(math.pi)):.10f}", " p_2(0,0)=", f"{(4 * math.pi) ** -0.5:.10f}")

print("== L06")
def paths(n):
    for steps in itertools.product((1, -1), repeat=n):
        s = 0
        mx = 0
        for e in steps:
            s += e
            mx = max(mx, s)
        yield mx, s
p12 = list(paths(12))
print("Part C: #M12>=3:", sum(1 for m, s in p12 if m >= 3), "of", 2**12, "; #M12>=3&S12=2:", sum(1 for m, s in p12 if m >= 3 and s == 2), "; #S12=4:", sum(1 for m, s in p12 if s == 4))
p10 = list(paths(10))
tot = 2**10
print("Part D: P(M10>=2)=", Fraction(sum(1 for m, s in p10 if m >= 2), tot), "; 2P(S10>2)=", 2 * Fraction(sum(1 for m, s in p10 if s > 2), tot), "; P(S10=2)=", Fraction(sum(1 for m, s in p10 if s == 2), tot))
print("binomial C(10,6)/1024 =", Fraction(math.comb(10, 6), 1024))
print("M3>=1 count among 8:", sum(1 for m, s in paths(3) if m >= 1), "; M2>=2 among 4:", sum(1 for m, s in paths(2) if m >= 2))
print("erfc(1/sqrt2) =", f"{math.erfc(1 / math.sqrt(2)):.10f}", "; half =", f"{math.erfc(1 / math.sqrt(2)) / 2:.11f}")
print("Halved printed value:", f"{0.3173105079 / 2:.11f}")
print("Quiz Q4 |0.3173105079-0.3173|:", abs(0.3173105079 - 0.3173))
print("Quiz Q8 |0.15865525393 - 0.1587|:", abs(0.15865525393 - 0.1587))
print("Parts A/B counts: triples", sum(n + a for n in range(1, 13) for a in range(1, n + 1)), "pairs", sum(range(1, 13)))
print("E2 arithmetic: 281/512 - 11/32 =", Fraction(281, 512) - Fraction(11, 32), "; 105/512 =", Fraction(105, 512))
print("M-1 (L06) Part E pair: P(M1>=1)=", f"{math.erfc(1 / math.sqrt(2)):.4f}", "P(B1>=1)=", f"{math.erfc(1 / math.sqrt(2)) / 2:.4f}")
