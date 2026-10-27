"""Round-28 part C: closed-form re-derivations with the standard library only (statistics.NormalDist, math, fractions).
Covers: L03 line 59 (Bonferroni), L03 line 584 (pooled-check tail arithmetic), L03 Problem M4 (lines 663-672),
L07 Example 5.5 (lines 438-440) and Problem E4 (line 710). Run: python -I closed_forms_C.py"""
import math
from fractions import Fraction
from statistics import NormalDist

N = NormalDist()
Phi = N.cdf
phi = N.pdf
out = []


def show(label, value, shown):
    out.append(f"{label}: {value} (page: {shown})")


# L03 line 59: Bonferroni, m = 1000, alpha 0.05, effect mean 3
crit = N.inv_cdf(1 - 0.05 / 1000)
show("L03 l59 Phi^-1(1-0.05/1000)", f"{crit:.6f}", "3.8906")
show("L03 l59 1-Phi(3.8906-3)", f"{1 - Phi(3.8906 - 3):.6f}", "0.187")
show("L03 l59 1-Phi(1.645-3)", f"{1 - Phi(1.645 - 3):.6f}", "0.912")

# L03 line 584: 200 x 450 x (1-Phi(3)) etc.
a = 200 * 450 * (1 - Phi(3))
show("L03 l584 200*450*(1-Phi(3))", f"{a:.4f}", "about 121")
b = 200 * 50 * (1 - Phi((3 - math.sqrt(5)) / math.sqrt(1.3125)))
show("L03 l584 200*50*(1-Phi((3-sqrt5)/sqrt1.3125))", f"{b:.3f}", "2,524 (0.2524)")
show("L03 l584 a+b", f"{a + b:.3f}", "2,645 (sum of 121 and 2,524)")
show("L03 l584 sqrt(121)/2645", f"{math.sqrt(121) / 2645:.6f}", "0.004")

# L03 Problem M4: pi0 = 0.9, f0 = N(0,1), f1 = N(3,1), z = 2.5
z = 2.5
l0 = 0.9 * phi(z)
l1 = 0.1 * phi(z - 3)
show("M4 lfdr(2.5)", f"{l0 / (l0 + l1):.6f}", "0.309")
show("M4 phi(2.5)", f"{phi(2.5):.6f}", "0.017528")
show("M4 phi(-0.5)", f"{phi(-0.5):.6f}", "0.352065")
S0 = 1 - Phi(2.5)
S1 = 1 - Phi(-0.5)
show("M4 S0(2.5)", f"{S0:.5f}", "0.00621")
show("M4 S1(2.5)", f"{S1:.5f}", "0.69146")
p0S0, p1S1 = 0.9 * S0, 0.1 * S1
show("M4 pi0*S0", f"{p0S0:.6f}", "0.005589")
show("M4 pi1*S1", f"{p1S1:.6f}", "0.069146")
S = p0S0 + p1S1
show("M4 S(2.5) = Fdr denominator", f"{S:.6f}", "0.074735")
show("M4 Fdr(2.5)", f"{p0S0 / S:.5f}", "0.0748")
show("M4 BH limit S0/S", f"{S0 / S:.5f}", "0.0831")
show("M4 Fdr/pi0", f"{p0S0 / S / 0.9:.5f}", "0.0831")
show("M4 lfdr / Fdr", f"{(l0 / (l0 + l1)) / (p0S0 / S):.3f}", "four times (4.14)")

# L07 Example 5.5 (lines 438-440), exact arithmetic
theta = Fraction(2) * Fraction(5, 100) + Fraction(1, 2) * (Fraction(36, 10000) + Fraction(16, 10000)) - Fraction(24, 10000) * Fraction(9025, 10000)
show("L07 Ex5.5 theta exact", f"{theta} = {float(theta):.6f}", "0.100434")
se = math.sqrt(float(theta) / 1259)
show("L07 Ex5.5 SE paired sqrt(theta/1259)", f"{se:.6f}", "0.008932")
Z = 0.02 / se
show("L07 Ex5.5 Z", f"{Z:.4f}", "2.239")
show("L07 Ex5.5 two-sided p", f"{2 * (1 - Phi(Z)):.5f}", "0.025")
naive_var = 2 + 0.5 * (0.06**2 + 0.04**2)
show("L07 Ex5.5 naive variance 2+0.0026", f"{naive_var:.4f}", "2.0026")
se_n = math.sqrt(naive_var / 1259)
show("L07 Ex5.5 naive SE", f"{se_n:.5f}", "0.03988")
show("L07 Ex5.5 naive Z", f"{0.02 / se_n:.4f}", "0.50")
show("L07 Ex5.5 naive p", f"{2 * (1 - Phi(0.02 / se_n)):.4f}", "0.62")
show("L07 Ex5.5 naive SE / paired SE", f"{se_n / se:.3f}", "4.5 times smaller")
show("L07 Ex5.5 annual SE sqrt(252*1.0018/1259)", f"{math.sqrt(252 * 1.0018 / 1259):.4f}", "0.448")
show("L07 Ex5.5 annualized SRs", f"{0.06 * math.sqrt(252):.3f} and {0.04 * math.sqrt(252):.3f}", "0.95 and 0.63")

# L07 Problem E4 (line 710): mean of the paired statistic, rejection probability, naive sd and MC error
mean_paired = 0.02 * math.sqrt(1259) / math.sqrt(0.100434)
show("L07 E4 mean 0.02 sqrt(1259)/sqrt(0.100434)", f"{mean_paired:.4f}", "2.239")
rej = Phi(2.239 - 1.960) + Phi(-2.239 - 1.960)
show("L07 E4 rejection Phi(2.239-1.96)+Phi(-2.239-1.96)", f"{rej:.5f}", "about 0.61 (Phi(0.279)=0.61)")
show("L07 E4 Phi(0.279)", f"{Phi(0.279):.5f}", "0.61")
sd_naive = math.sqrt(0.100434 / 2.0026)
show("L07 E4 naive sd sqrt(0.100434/2.0026)", f"{sd_naive:.4f}", "0.224")
show("L07 E4 naive standardised distance (1.960-0.50)/0.224", f"{(1.960 - 0.50) / 0.224:.2f}", "6.5")
show("L07 E4 MC error sqrt(0.61*0.39/4000)", f"{math.sqrt(0.61 * 0.39 / 4000):.5f}", "0.008")

print("\n".join(out))
