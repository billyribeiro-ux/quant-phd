"""Round-33 re-derivation of the closed-form and scipy-derived numbers quoted in S7 L05 and L06 prose.

Independent of every page's JavaScript and of the twins. Each check recomputes a value with scipy.stats.norm /
optimize (or exact arithmetic) and compares it with the value the page shows, at the page's precision.
Run: .venv/bin/python -I ledgers/S7/scripts/L05-L06-r33/derive_numbers.py
"""

from __future__ import annotations

import math

from scipy import optimize
from scipy.stats import norm

Phi = norm.cdf
Pinv = norm.ppf
results: list[tuple[str, str, bool]] = []


def check(name: str, value: float, shown: float, decimals: int) -> None:
    ok = abs(round(value, decimals) - shown) < 1e-12
    results.append((name, f"recomputed {value:.10g}, page {shown} ({decimals} dp)", ok))


def exact(name: str, value: float, shown: float, tol: float) -> None:
    results.append((name, f"recomputed {value:.10g}, page {shown} (tol {tol})", abs(value - shown) <= tol))


def posterior(t: float, pi0: float) -> float:
    """Lower bound (4): PO e^(-t^2/2) / (1 + PO e^(-t^2/2)), PO = pi0/(1-pi0)."""
    odds = pi0 / (1 - pi0)
    mbf = math.exp(-t * t / 2)
    return odds * mbf / (1 + odds * mbf)


# --- L05: Romano-Wolf and Bonferroni/Holm quantiles (one-sided tail = alpha / n) ---
check("L05 Phi^-1(0.975)", Pinv(0.975), 1.960, 3)
check("L05 Bonferroni K=20 Phi^-1(1-0.05/40)", Pinv(1 - 0.05 / 40), 3.023, 3)
check("L05 sup-t K=20 independence Phi^-1((1+0.95^(1/20))/2)", Pinv((1 + 0.95 ** (1 / 20)) / 2), 3.016, 3)
check("L05 sup-t argument 0.998719", (1 + 0.95 ** (1 / 20)) / 2, 0.998719, 6)
check("L05 StepM n=20 Phi^-1(0.95^(1/20))", Pinv(0.95 ** (1 / 20)), 2.799, 3)
check("L05 StepM n=15 Phi^-1(0.95^(1/15))", Pinv(0.95 ** (1 / 15)), 2.705, 3)
check("L05 StepM n=10 Phi^-1(0.95^(1/10))", Pinv(0.95 ** (1 / 10)), 2.568, 3)
check("L05 Holm n=10 Phi^-1(1-0.05/10)", Pinv(1 - 0.05 / 10), 2.576, 3)
check("L05 Holm n=20 Phi^-1(1-0.05/20)", Pinv(1 - 0.05 / 20), 2.807, 3)
check("L05 Holm n=15 Phi^-1(1-0.05/15)", Pinv(1 - 0.05 / 15), 2.713, 3)
check("L05 one test Phi^-1(0.95)", Pinv(0.95), 1.645, 3)
check("L05 Bonferroni ten at 90% Phi^-1(1-0.10/20)", Pinv(1 - 0.10 / 20), 2.576, 3)
check("L05 R=2 level 0.98 Phi^-1(0.99)", Pinv(0.99), 2.326, 3)
check("L05 Lab-3 Phi^-1(0.95^(1/10)) (P2)", Pinv(0.95 ** (1 / 10)), 2.568, 3)
check("L05 R4 0.975^20 - 0.025^20 (60%)", 0.975**20 - 0.025**20, 0.603, 3)
exact("L05 R4 3.031/1.960", 3.031 / 1.960, 1.55, 0.005)
check("L05 Lab-2 1-0.95^8", 1 - 0.95**8, 0.337, 3)
check("L05 Lab-2 SE sqrt(0.05*0.95/400)", math.sqrt(0.05 * 0.95 / 400), 0.011, 3)
check("L05 Lab-2 (0.05-0.035)/SE", (0.05 - 0.035) / math.sqrt(0.05 * 0.95 / 400), 1.4, 1)

# --- L05 section 5 studentization example: c solving Phi(c) Phi(c/5) = 0.95 ---
c_star = optimize.brentq(lambda x: Phi(x) * Phi(x / 5) - 0.95, 1, 20, xtol=1e-14)
exact("L05 sec5 c", c_star, 8.224, 0.0005)
check("L05 sec5 Phi^-1(0.95^(1/2))", Pinv(0.95**0.5), 1.955, 3)
check("L05 sec5 Phi(3-1.955)", Phi(3 - 1.955), 0.852, 3)
exact("L05 sec5 1-Phi(5.224)", norm.sf(5.224), 8.7549e-8, 1e-11)

# --- L05 Problem E2: studentized block-length expressions ---
exact("L05 E2 (1+phi)/(1-phi) at phi=... 13/7 sqrt", math.sqrt(13 / 7), 1.363, 0.0005)
check("L05 E2 1-Phi(1.645/sqrt(13/7))", 1 - Phi(1.645 / math.sqrt(13 / 7)), 0.114, 3)
exact("L05 E2 expected block starts 1+499/20", 1 + 499 / 20, 25.95, 1e-12)

# --- L05 M2, M4, R1 integers ---
for name, value, shown in [
    ("L05 M2 ceil(0.95*999)", math.ceil(0.95 * 999), 950),
    ("L05 M2 ceil(0.95*1000)", math.ceil(0.95 * 1000), 950),
    ("L05 M2 ceil(0.9*499)", math.ceil(0.9 * 499), 450),
    ("L05 M2 ceil(0.95*19)", math.ceil(0.95 * 19), 19),
    ("L05 R1 5*252", 5 * 252, 1260),
]:
    exact(name, value, shown, 0)
for z, shown in zip(
    [3.4, 3.0, 2.7, 2.5, 2.2, 1.6, 1.2, 0.8, 0.4, -0.3],
    [0.00067, 0.0027, 0.00693, 0.01242, 0.02781, 0.1096, 0.23014, 0.42371, 0.68916, 0.76418],
    strict=True,
):
    check(f"L05 M4 two-sided p at z={z}", 2 * norm.sf(abs(z)), shown, 5)

# --- L05 Lab 5 harmonic numbers c(101), c(500) ---
exact("L05 H_101", sum(1 / j for j in range(1, 102)), 5.197, 0.0005)
exact("L05 H_500", sum(1 / j for j in range(1, 501)), 6.793, 0.0005)

# --- L06 Definition 2.1: Bonferroni hurdles Phi^-1(1 - 0.025/M) ---
for M, shown in [(1, 1.960), (10, 2.807), (100, 3.481), (316, 3.778), (1000, 4.056), (10**4, 4.565)]:
    check(f"L06 hurdle M={M} Phi^-1(1-0.025/M)", Pinv(1 - 0.025 / M), shown, 3)
check("L06 bound sqrt(2 ln 40)", math.sqrt(2 * math.log(40)), 2.716, 3)
check("L06 Euler-Mascheroni 0.577", 0.5772156649015329, 0.577, 3)
check("L06 H_316 - ln 316 = 0.5788", sum(1 / j for j in range(1, 317)) - math.log(316), 0.5788, 4)

# --- L06 Section 5 posterior bounds, Section 4 and Problem M2/M3 ---
check("L06 bound t=1.96, PO=1 (percent, 13%)", 100 * posterior(1.96, 0.5), 13, 0)
exact("L06 bound t=1.96, PO=1", posterior(1.96, 0.5), 0.12777, 1e-5)
check("L06 bound t=3, prior 0.99 (percent, 52%)", 100 * posterior(3.0, 0.99), 52, 0)
exact("L06 bound t=3, prior 0.99", posterior(3.0, 0.99), 0.52376, 1e-5)
check("L06 M2 p = 2(1-Phi(2.8))", 2 * norm.sf(2.8), 0.0051, 4)
check("L06 M2 MBF e^(-2.8^2/2)", math.exp(-2.8**2 / 2), 0.01984, 5)
check("L06 M2 bound PO=1", posterior(2.8, 0.5), 0.0195, 4)
check("L06 M2 bound PO=2", posterior(2.8, 2 / 3), 0.0382, 4)
exact("L06 M2 bound/p ratio", posterior(2.8, 2 / 3) / (2 * norm.sf(2.8)), 7.47, 0.005)
check("L06 M3 -e*0.01*ln(0.01)", -math.e * 0.01 * math.log(0.01), 0.1252, 4)
check("L06 M3 z = Phi^-1(0.995)", Pinv(0.995), 2.576, 3)
check("L06 M3 MBF at z", math.exp(-Pinv(0.995) ** 2 / 2), 0.0362, 4)
check("L06 P2 sqrt(2 ln 19)", math.sqrt(2 * math.log(19)), 2.427, 3)
check("L06 P2 sqrt(2 ln 171)", math.sqrt(2 * math.log(171)), 3.207, 3)
check("L06 P2 sqrt(2 ln 1881)", math.sqrt(2 * math.log(1881)), 3.883, 3)
check("L06 P3 1-0.95^2", 1 - 0.95**2, 0.0975, 4)
check("L06 Lab-2 1-0.95^36", 1 - 0.95**36, 0.842, 3)
check("L06 Lab-2 SE 0.05 over 300", math.sqrt(0.05 * 0.95 / 300), 0.013, 3)
check("L06 MC SE 0.24 over 300", math.sqrt(0.24 * 0.76 / 300), 0.025, 3)
check("L06 kappa = Phi^-1(0.975)", Pinv(0.975), 1.96, 2)
check("L06 forking-paths K=10 rho=0 (closed form)", 1 - 0.95**10, 0.401, 3)

# --- L06 Proposition 4.3 (Section 8 proof numbers) ---
cc = math.sqrt(math.pi / 2) / math.e
check("L06 Prop4.3 c = sqrt(pi/2)/e", cc, 0.46107, 5)
# z* solves the two-sided p-value 2(1 - Phi(z*)) = 1/e, the point where -ln p = 1 (p = 1/e)
zstar = Pinv(1 - 1 / (2 * math.e))
exact("L06 Prop4.3 two-sided p at z* equals 1/e", 2 * norm.sf(zstar), 1 / math.e, 1e-12)
check("L06 Prop4.3 z*", zstar, 0.9005, 4)
check("L06 Prop4.3 z*+1/z*", zstar + 1 / zstar, 2.01101, 5)
check("L06 Prop4.3 u(z*) = 1 - c(z*+1/z*)", 1 - cc * (zstar + 1 / zstar), 0.0728, 4)
check("L06 Prop4.3 z for p=0.6 = Phi^-1(0.7)", Pinv(0.7), 0.5244, 4)
check("L06 Prop4.3 z^2/2", Pinv(0.7) ** 2 / 2, 0.1375, 4)
check("L06 Prop4.3 e^(-0.1375)", math.exp(-0.1375), 0.872, 3)
check("L06 Prop4.3 -e*0.6*ln(0.6)", -math.e * 0.6 * math.log(0.6), 0.833, 3)
check("L06 Prop4.3 -ln(0.6)", -math.log(0.6), 0.5108, 4)

# --- round 33 additions: BH rejections, interval arithmetic, Problem M1 StepM, Lab 1 SEs, L06 bounds ---
pm4 = [2 * norm.sf(abs(z)) for z in [3.4, 3.0, 2.7, 2.5, 2.2, 1.6, 1.2, 0.8, 0.4, -0.3]]
srt = sorted(pm4)
bh_r = max([k for k in range(1, 11) if srt[k - 1] <= k * 0.10 / 10] or [0])
exact("L05 M4 BH rejections at q=0.10, K=10", bh_r, 5, 0)
for name, est, se, shown in [
    ("L05 M4 interval A", 6.8, 2.0, (2.88, 10.72)),
    ("L05 M4 interval B", 4.5, 1.5, (1.56, 7.44)),
    ("L05 M4 interval C", 8.1, 3.0, (2.22, 13.98)),
    ("L05 M4 interval D", 5.0, 2.0, (1.08, 8.92)),
    ("L05 M4 interval E", 3.3, 1.5, (0.36, 6.24)),
]:
    check(name + " lower", est - 1.96 * se, shown[0], 2)
    check(name + " upper", est + 1.96 * se, shown[1], 2)
t_m1 = {1: 4.1, 2: 2.9, 3: 2.2, 4: 1.0}
exact("L05 M1 single-step rejects count (crit 2.5)", sum(1 for k in t_m1 if t_m1[k] > 2.5), 2, 0)
exact("L05 M1 step 2 rejects {3} (active {3,4}, c=2.1)", [k for k in (3, 4) if t_m1[k] > 2.1] == [3], True, 0)
exact("L05 M1 step 3 rejects nothing (active {4}, c=1.7)", [k for k in (4,) if t_m1[k] > 1.7] == [], True, 0)
exact("L05 M1 with t3=2.0 step 2 rejects nothing", [k for k in (3, 4) if {3: 2.0, 4: 1.0}[k] > 2.1] == [], True, 0)
check("L05 Lab1 SE at p=0.045, 4000 reps (about 0.003)", math.sqrt(0.045 * 0.955 / 4000), 0.003, 3)
check("L05 Lab1 SE at p=0.031, 4000 reps", math.sqrt(0.031 * 0.969 / 4000), 0.0027, 4)
check("L05 Lab1 5.798-5.596", 5.798 - 5.596, 0.202, 3)
check("L05 E2 13/7 to 3 dp", 13 / 7, 1.857, 3)
check("L05 P2 0.95^(1/10) to 5 dp", 0.95 ** (1 / 10), 0.99488, 5)
for M, bound, hurdle in [(1, 2.7162, 1.9600), (10, 3.4616, 2.8070), (100, 4.0728, 3.4808),
                         (316, 4.3462, 3.7778), (1000, 4.6036, 4.0556), (10**4, 5.0792, 4.5648)]:
    check(f"L06 bound sqrt(2 ln(40*{M}))", math.sqrt(2 * math.log(40 * M)), bound, 4)
    check(f"L06 bound minus hurdle at M={M}", math.sqrt(2 * math.log(40 * M)) - Pinv(1 - 0.025 / M), round(bound - hurdle, 2), 2)
    check(f"L06 hurdle/bound at M={M}", Pinv(1 - 0.025 / M) / math.sqrt(2 * math.log(40 * M)), round(hurdle / bound, 2), 2)

bad = [r for r in results if not r[2]]
for name, detail, ok in results:
    print(("OK       " if ok else "MISMATCH ") + name + " | " + detail)
print(f"checks={len(results)} ok={len(results) - len(bad)} mismatch={len(bad)}")
