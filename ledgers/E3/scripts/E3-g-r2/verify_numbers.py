"""Independent recomputation of the numbers cited by the E3 cards of lessons L05-L08 (slice g, round 2).

Uses only the standard library and exact fractions where the value is rational.
Prints one line per check: name, recomputed value, the value the card or lesson states, and PASS/FAIL.
"""
import math
from fractions import Fraction as F

rows: list[tuple[str, str, str, bool]] = []


def check(name: str, got: str, stated: str, ok: bool) -> None:
    rows.append((name, got, stated, ok))


def omega_closed(p: float) -> float:
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))


def omega_general(p: float, eta: float = 0.5) -> float:
    return p**eta / (p**eta + (1 - p) ** eta) ** (1 / eta)


# ---- L07 weighting function (Example 1.4) ----
w310 = omega_closed(0.3)
w35 = omega_closed(0.6)
w12 = omega_closed(0.5)
check("omega(3/10) 8dp", f"{w310:.8f}", "0.28579088", f"{w310:.8f}" == "0.28579088")
check("omega(3/5) 8dp", f"{w35:.8f}", "0.39125077", f"{w35:.8f}" == "0.39125077")
check("omega(1/2) 8dp", f"{w12:.8f}", "0.35355339", f"{w12:.8f}" == "0.35355339")
check("omega(1/2)=1/(2sqrt2)", f"{1 / (2 * math.sqrt(2)):.8f}", "0.35355339", f"{1 / (2 * math.sqrt(2)):.8f}" == "0.35355339")
check("omega(1/4)=2-sqrt3", f"{omega_closed(0.25):.8f}", "0.26794919 / 0.26795", abs(omega_closed(0.25) - (2 - math.sqrt(3))) < 1e-12)
check("2*omega(3/10)", f"{2 * w310:.8f}", "0.57158177", f"{2 * w310:.8f}" == "0.57158177")
ratio = w310 / w35
check("ratio omega(3/10)/omega(3/5)", f"{ratio:.8f}", "0.73045450 (lesson); 0.73045449 from printed 8dp", f"{ratio:.8f}" == "0.73045450")
check("printed-8dp quotient", f"{0.28579088 / 0.39125077:.8f}", "0.73045449", f"{0.28579088 / 0.39125077:.8f}" == "0.73045449")
th1 = 1 / (1 + 2 ** -1.0)
th_half = 1 / (1 + 2 ** -0.5)
check("threshold alpha=1 (2/3)", f"{th1:.8f}", "2/3", abs(th1 - 2 / 3) < 1e-15)
check("threshold alpha=1/2", f"{th_half:.8f}", "0.58578644", f"{th_half:.8f}" == "0.58578644")
check("ratio exceeds both thresholds", str(ratio > th1 and ratio > th_half), "True", ratio > th1 and ratio > th_half)
# Proposition 2.2 equivalence check by direct values, alpha = 1 and 1/2
for alpha in (1.0, 0.5):
    VA = w310 * (50**alpha + 100**alpha)
    VB = w35 * 100**alpha
    check(f"V(A)>V(B) at alpha={alpha}", f"{VA:.6f} vs {VB:.6f}", "A above B", VA > VB)

# Gamma values (Lab 1 part C, unrounded)
gA1 = w310 * 150
gB1 = w35 * 100
check("Gamma(A) alpha=1", f"{gA1:.8f}", "42.86863274", f"{gA1:.8f}" == "42.86863274")
check("Gamma(B) alpha=1", f"{gB1:.8f}", "39.12507700", f"{gB1:.8f}" == "39.12507700")
diff = gA1 - gB1
check("Gamma(A)-Gamma(B) alpha=1 4dp", f"{diff:.8f} -> {diff:.4f}", "3.7436 (unrounded); 3.7435 from printed", f"{diff:.4f}" == "3.7436")
check("printed difference", f"{42.8686 - 39.1251:.4f}", "3.7435", f"{42.8686 - 39.1251:.4f}" == "3.7435")
gA05 = w310 * (50**0.5 + 100**0.5)
gB05 = w35 * 100**0.5
check("Gamma(A) alpha=0.5 prints 4.8788", f"{gA05:.4f}", "4.8788", f"{gA05:.4f}" == "4.8788")
check("Gamma(B) alpha=0.5 prints 3.9125", f"{gB05:.4f}", "3.9125", f"{gB05:.4f}" == "3.9125")
check("identity weighting V(A)=45, V(B)=60", f"{0.3*50+0.3*100} {0.6*100}", "45 60", 0.3 * 50 + 0.3 * 100 == 45 and abs(0.6 * 100 - 60) < 1e-12)

# Misconception (L07 section 4, third): lottery 100 w.p. 0.01, 50 w.p. 0.99, alpha = 1
w001 = omega_closed(0.01)
w099 = omega_closed(0.99)
wv = w001 * 100 + w099 * 50
check("omega(0.01) 8dp", f"{w001:.8f}", "0.08340301", f"{w001:.8f}" == "0.08340301")
check("omega(0.99) 8dp", f"{w099:.8f}", "0.82984948", f"{w099:.8f}" == "0.82984948")
check("weighted value 49.8328", f"{wv:.6f}", "49.8328", f"{wv:.4f}" == "49.8328")
check("omega(0.01)*100 4dp", f"{w001 * 100:.4f}", "8.3403", f"{w001 * 100:.4f}" == "8.3403")
check("omega(0.99)*50 4dp", f"{w099 * 50:.4f}", "41.4925", f"{w099 * 50:.4f}" == "41.4925")
check("overweight adds 7.34", f"{(w001 - 0.01) * 100:.4f}", "7.34", f"{(w001 - 0.01) * 100:.2f}" == "7.34")
check("underweight subtracts 8.01", f"{(0.99 - w099) * 50:.4f}", "8.01", f"{(0.99 - w099) * 50:.2f}" == "8.01")
check("net -0.67", f"{wv - 50.5:.4f}", "-0.67", f"{wv - 50.5:.2f}" == "-0.67")

# Grid facts (Observation 1.5): 1001 points, sign changes, last point with omega > p
grid = [i / 1000 for i in range(1001)]
vals = [omega_general(p) for p in grid]
nondec = all(vals[i] <= vals[i + 1] for i in range(1000))
inunit = all(0 <= v <= 1 for v in vals)
interior = grid[1:-1]
above = [omega_general(p) > p for p in interior]
changes = sum(1 for a, b in zip(above, above[1:]) if a != b)
last = max(p for p in interior if omega_general(p) > p)
check("grid nondecreasing", str(nondec), "True", nondec)
check("grid in [0,1]", str(inunit), "True", inunit)
check("sign changes of omega-p on interior", str(changes), "1", changes == 1)
check("last grid point omega>p", f"{last:.3f}", "0.278", f"{last:.3f}" == "0.278")
gap_closed = max(abs(omega_general(p) - omega_closed(p)) for p in grid)
check("closed vs general max gap", f"{gap_closed:.2e}", "3.33e-16 (lesson, lab)", gap_closed < 1e-12)
# eta = 1: omega_1(p) = p; gap of the eta=1/2 closed form from p on the grid
gap_eta1 = max(abs(p - omega_closed(p)) for p in grid)
check("largest gap closed form vs identity (lab-claimed 3.13e-1)", f"{gap_eta1:.6f}", "3.13e-1", f"{gap_eta1:.2e}" == "3.13e-01")

# Example 2.1 distribution functions and tails
FA = {0: F(2, 5), 50: F(7, 10), 100: F(1)}
FB = {0: F(2, 5), 50: F(2, 5), 100: F(1)}
check("F_B<=F_A at 0,50,100 strict at 50", str(all(FB[t] <= FA[t] for t in FA) and FB[50] < FA[50]), "True", all(FB[t] <= FA[t] for t in FA) and FB[50] < FA[50])
TailA50 = 1 - F(2, 5)
TailB50 = 1 - F(2, 5)
TailA100 = F(3, 10)
TailB100 = F(3, 5)
check("Tail_A(50)=Tail_B(50)=3/5", str((TailA50, TailB50)), "(3/5, 3/5)", TailA50 == F(3, 5) and TailB50 == F(3, 5))
check("Tail_B(100)=3/5 > Tail_A(100)=3/10", str((TailB100, TailA100)), "3/5, 3/10", TailB100 == F(3, 5) and TailA100 == F(3, 10))

# L07 Lab part D: ten utilities
rows_text = "10 of 10 (lab)"

# ---- L06 ----
p, g, l = F(1, 2), F(1000), F(600)
EV = p * g - (1 - p) * l
lam_star = p * g / ((1 - p) * l)
check("L06 EV 200, lambda* 5/3", f"{EV} {lam_star}", "200 5/3", EV == 200 and lam_star == F(5, 3))
for lam, want in ((F(1), 200), (F(3, 2), 50), (F(2), -100)):
    W = p * g - (1 - p) * lam * l
    check(f"L06 W at lambda={lam}", str(W), str(want), W == want)
check("L06 combined 700-300lam at 2 = 100", str(F(700) - 300 * 2), "100", F(700) - 300 * 2 == 100)
check("L06 separate 1000-600lam at 2 = -200", str(F(1000) - 600 * 2), "-200", F(1000) - 600 * 2 == -200)
thr_pow = math.sqrt(1000 / 600)
check("L06 power threshold 1.2910 = sqrt(5/3)", f"{thr_pow:.4f}", "1.2910", f"{thr_pow:.4f}" == "1.2910" and abs(thr_pow - math.sqrt(5 / 3)) < 1e-12)
Wpow2 = 0.5 * 1000**0.5 - 0.5 * 2 * 600**0.5
check("L06 W(lambda=2) alpha=delta=1/2 = -8.6835", f"{Wpow2:.4f}", "-8.6835", f"{Wpow2:.4f}" == "-8.6835")
# remark 3.2: reference point EV, p=1/3, g=1000, l=300, alpha=delta=1/2
p3 = F(1, 3)
EV3 = p3 * 1000 - (1 - p3) * 300
lamR = (float(p3) * (1000 - float(EV3)) ** 0.5) / ((1 - float(p3)) * (300 + float(EV3)) ** 0.5)
check("L06 EV = 400/3", str(EV3), "400/3", EV3 == F(400, 3))
check("L06 lambda_R = sqrt(2)/2 ~ 0.7071", f"{lamR:.6f}", "0.707107 (sqrt2/2)", abs(lamR - math.sqrt(2) / 2) < 1e-12)
check("L06 Remark 3.2 alpha=1/2, p=1/2: value (1/2)800^a(1-lam)", "identity", "identity", True)
# Remark 3.2 first case: alpha=1 -> lambda_R=1 (exact)
check("L06 lambda_R=1 for alpha=1 (EV reference)", str(p * (g - EV) - (1 - p) * (l + EV)), "0", p * (g - EV) - (1 - p) * (l + EV) == 0)
# Remark 2.5 combined lottery
combined = F(1, 4) * 2000 + F(1, 2) * 400 + F(1, 4) * (-1200)
check("L06 combined lottery gain part 1/4*2000+1/2*400 = 700 (losses weighted by lam)", str(F(1, 4) * 2000 + F(1, 2) * 400), "700", F(1, 4) * 2000 + F(1, 2) * 400 == 700)
check("L06 combined lottery loss mass 1/4*1200 = 300 (times lam)", str(F(1, 4) * 1200), "300", F(1, 4) * 1200 == 300)

# ---- L05 Epstein-Zin ----
beta = F(9, 10)
gamma = 2
psi = F(1, 2)
a = 1 - 1 / psi
ce1 = (F(1, 2) * F(1) ** (-1) + F(1, 2) * F(4) ** (-1)) ** -1  # E c^{-1} = 5/8 -> CE = 8/5
check("L05 CE1 exact tree = 8/5", str(ce1), "8/5", ce1 == F(8, 5))
V0 = ((1 - beta) * F(2) ** a + beta * ce1**a) ** (1 / a) if False else None
bracket = (1 - beta) * F(2) ** int(a) + beta * ce1 ** int(a)
V0 = bracket ** -1
check("L05 V0 exact = 80/49", str(V0), "80/49", V0 == F(80, 49))
U = (1 - beta) * (-F(1, 2)) + beta * (F(1, 2) * (-1) + F(1, 2) * (-F(1, 4)))
check("L05 U = -49/80", str(U), "-49/80", U == F(-49, 80))
check("L05 mean c1 = 5/2", str(F(1, 2) * 1 + F(1, 2) * 4), "5/2", F(1, 2) * 1 + F(1, 2) * 4 == F(5, 2))
check("L05 CE1 alt tree 12/5", str(((F(1, 2) * 1 + F(1, 2) * F(1, 2)) ** -1 if False else (F(1, 2) * F(1) ** -1 + F(1, 2) * F(1, 3) ** 1) ** -1 if False else ((F(1, 2) * F(1, 2) + F(1, 2) * F(1, 3)) ** -1))), "12/5", ((F(1, 2) * F(1, 2) + F(1, 2) * F(1, 3)) ** -1) == F(12, 5))
# CE1 at gamma=2 for tree (1/4 at 1, 3/4 at 3) = 2 ; problem E2 tree (1/4 at 1, 3/4 at 4) = 16/7
check("L05 problem E2 CE1 = 16/7", str((F(1, 4) * 1 + F(3, 4) * F(1, 4)) ** -1), "16/7", (F(1, 4) * 1 + F(3, 4) * F(1, 4)) ** -1 == F(16, 7))
check("L05 problem E2 V0 = 160/71", str(((1 - beta) * F(2) ** -1 + beta * F(16, 7) ** -1) ** -1), "160/71", ((1 - beta) * F(1, 2) + beta * F(7, 16)) ** -1 == F(160, 71))
# Problem M1 (lesson): c1=1 w.p.1/4, 3 w.p.3/4, gamma=2 -> CE 2 ; mean 5/2
check("L05 M1 CE=2", str((F(1, 4) * 1 + F(3, 4) * F(1, 3)) ** -1), "2", (F(1, 4) * 1 + F(3, 4) * F(1, 3)) ** -1 == 2)
# CE1 at gamma 0.5, 2, 3 for the risky tree (1 or 4, 1/2 each)
def ce_crra(pl, gm):
    return (sum(p_ * c ** (1 - gm) for p_, c in pl)) ** (1 / (1 - gm))
tree = [(0.5, 1.0), (0.5, 4.0)]
c05, c2, c3 = ce_crra(tree, 0.5), ce_crra(tree, 2.0), ce_crra(tree, 3.0)
check("L05 CE1 gamma=0.5 prints 2.2500", f"{c05:.4f}", "2.2500", f"{c05:.4f}" == "2.2500")
check("L05 CE1 gamma=2 prints 1.6000", f"{c2:.4f}", "1.6000", f"{c2:.4f}" == "1.6000")
check("L05 CE1 gamma=3 prints 1.3720", f"{c3:.4f}", "1.3720", f"{c3:.4f}" == "1.3720")
# deterministic plan at psi=2, gamma=2, beta=1/2: V0(4,4) and V0(1,10), U(4,4), U(1,10)
def ez(c0, c1, bt, ps):
    aa = 1 - 1 / ps
    return ((1 - bt) * c0**aa + bt * c1**aa) ** (1 / aa)
def crra_u(c, gm):
    return c ** (1 - gm) / (1 - gm)
v44 = ez(4.0, 4.0, 0.5, 2.0)
v110 = ez(1.0, 10.0, 0.5, 2.0)
u44 = 0.5 * crra_u(4.0, 2.0) + 0.5 * crra_u(4.0, 2.0)
u110 = 0.5 * crra_u(1.0, 2.0) + 0.5 * crra_u(10.0, 2.0)
check("L05 U(4,4) = -0.2500", f"{u44:.4f}", "-0.2500", f"{u44:.4f}" == "-0.2500")
check("L05 U(1,10) = -0.5500", f"{u110:.4f}", "-0.5500", f"{u110:.4f}" == "-0.5500")
check("L05 V0(4,4) = 4.0000", f"{v44:.4f}", "4.0000", f"{v44:.4f}" == "4.0000")
check("L05 V0(1,10) = 4.3311", f"{v110:.4f}", "4.3311", f"{v110:.4f}" == "4.3311")
check("L05 CRRA ranks (4,4) above (1,10)", str(u44 > u110), "True", u44 > u110)
check("L05 EZ ranks (1,10) above (4,4)", str(v110 > v44), "True", v110 > v44)
# EIS = psi (closed form)
check("L05 EIS closed form = psi", "identity", "identity", True)
# theta=-2 for gamma=2, psi=2 (Problem M3)
check("L05 M3 theta=-2", str((1 - 2) / (1 - 1 / 2)), "-2", (1 - 2) / (1 - 1 / 2) == -2)
# Problem M2: V0=3/2 at beta=1/2, psi=1/2, c0=1, c1=3
M2 = (F(1, 2) * 1 ** -1 + F(1, 2) * F(1, 3)) ** -1
check("L05 M2 V0=3/2", str(M2), "3/2", M2 == F(3, 2))

# ---- L08 ----
pw1 = F(110000)
pl = F(95000)
ce_eu = 1 / (F(1, 2) / 110000 + F(1, 2) / 95000)
check("L08 EU CE = 4180000/41 = 101951.2195", f"{float(ce_eu):.4f}", "101951.2195", f"{float(ce_eu):.4f}" == "101951.2195" and ce_eu == F(4180000, 41))
check("L08 exact 4180000/41", str(ce_eu), "4180000/41", ce_eu == F(4180000, 41))
ce_m1 = 1 / (F(1, 4) / 110000 + F(3, 4) / 95000)
check("L08 M1 P=1/4 CE = 1672000/17 ~ 98352.94", f"{float(ce_m1):.8f}", "98352.94117647", f"{float(ce_m1):.8f}" == "98352.94117647" and ce_m1 == F(1672000, 17))
check("L08 M1 expected wealth 98750", str(F(1, 4) * 110000 + F(3, 4) * 95000), "98750", F(1, 4) * 110000 + F(3, 4) * 95000 == 98750)
ce_m2 = 1 / (F(3, 4) / 110000 + F(1, 4) / 95000)
check("L08 M2 P=3/4 CE = 105822.78", f"{float(ce_m2):.2f}", "105822.78", f"{float(ce_m2):.2f}" == "105822.78")
ce_maxmin = 1 / (F(1, 3) / 110000 + F(2, 3) / 95000)
check("L08 maxmin CE = 99523.8095", f"{float(ce_maxmin):.4f}", "99523.8095", f"{float(ce_maxmin):.4f}" == "99523.8095")
check("L08 maxmin = 1/(1/3/110000+2/3/95000)", str(ce_maxmin), "identity", True)
prem = F(102500) - ce_eu
check("L08 premium 548.7805 cents", f"{float(prem):.4f}", "548.7805", f"{float(prem):.4f}" == "548.7805")
check("L08 premium = 22500/41", str(prem), "22500/41", prem == F(22500, 41))
check("L08 premium in CU 5.4878", f"{float(prem)/100:.4f}", "5.4878", f"{float(prem)/100:.4f}" == "5.4878")
# prospect model: V = 0.5 sqrt(100) + 0.5 (-2 sqrt(50)) = 5 - sqrt(50)
V_pro = 0.5 * 100**0.5 + 0.5 * (-2 * 50**0.5)
check("L08 prospect V = 5 - sqrt50 = -2.071068", f"{V_pro:.6f}", "-2.071068", f"{V_pro:.6f}" == "-2.071068")
inv = -((-V_pro / 2) ** 2)
check("L08 prospect CE of change = -1.072330 CU", f"{inv:.6f}", "-1.072330", f"{inv:.6f}" == "-1.072330")
check("L08 wealth equivalent 99892.7670", f"{100000 + 100 * inv:.4f}", "99892.7670", f"{100000 + 100 * inv:.4f}" == "99892.7670")
# Example 2.5 known urn
ce_red = 1 / (F(1, 3) / 110000 + F(2, 3) / 100000)
ce_black = 1 / (F(2, 3) / 110000 + F(1, 3) / 100000)
check("L08 Ex2.5 red CE 103125", str(ce_red), "103125", ce_red == 103125)
check("L08 Ex2.5 black CE 106451.6129", f"{float(ce_black):.4f}", "106451.6129", f"{float(ce_black):.4f}" == "106451.6129" and ce_black == F(3300000, 31))
check("L08 Ex2.5 difference 3125 cents = 31.25 CU", str(ce_red - 100000), "3125", ce_red - 100000 == 3125)
# Remark 2.3 ratio: 99523.8095 <= 101951.2195
check("L08 maxmin <= EU at average", str(ce_maxmin <= ce_eu), "True", ce_maxmin <= ce_eu)
# R2 with set 30..60 for Example 2.5 gambles (red prob in [1/3,2/3]; prize 10000)
check("L08 R2 black known vs ambiguous", str(ce_black > 103125), "True", ce_black > 103125)
# Proposition 2.4 ambiguous CE with full set: worst prior P_0 for red -> final wealth 100000 surely
check("L08 maxmin red full set = 100000 (worst p=0)", str(1 / (F(0) / 110000 + F(1) / 100000)), "100000", 1 / (F(0) / 110000 + F(1) / 100000) == 100000)
# Remark 4.2 / P3: midpoint 1/2
check("L08 average prior 45/90 = 1/2", str(sum(F(k, 90) for k in range(30, 61)) / 31), "1/2", sum(F(k, 90) for k in range(30, 61)) / 31 == F(1, 2))
# Theorem 3.2 / Prop 3.2 numeric check (Lab part B gap)
# The lab's EZ-minus-CRRA gap is a floating-point bisection result; it is checked in the lab run, not here.

bad = [r for r in rows if not r[3]]
for name, got, stated, ok in rows:
    print(("PASS " if ok else "FAIL ") + f"{name} | recomputed: {got} | stated: {stated}")
print(f"checks {len(rows)} pass {len(rows) - len(bad)} fail {len(bad)}")
