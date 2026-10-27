"""Round 28 fresh derivation of the numbers quoted in S7 L07 and L08 (independent of the pages' own code).

Every check states the page value and its printed precision; the computed value is rounded to that precision and
compared. Closed-form values use the standard library only; Phi and Phi^-1 use statistics.NormalDist; the maximum
of n normals uses trapezoidal quadrature (no simulation). Run: .venv/bin/python -I <this file>.
Output lines: CHECK <id> | page <value> | computed <value> | PASS|FAIL
"""

from __future__ import annotations

import math
from statistics import NormalDist

PHI = NormalDist()
G = 0.5772156649015329  # Euler-Mascheroni constant, as in the pages
RESULTS: list[tuple[str, bool]] = []


def check(cid: str, computed: float, page: float, digits: int) -> None:
    ok = abs(round(computed, digits) - page) < 0.5 * 10 ** (-digits) + 1e-12
    RESULTS.append((cid, ok))
    print(f"CHECK {cid} | page {page} | computed {round(computed, digits)} (raw {computed:.10g}) | {'PASS' if ok else 'FAIL'}")


def bracket3(n: float) -> float:
    """Approximation (3) of Lesson 1 / L07 Definition 3.1: expected maximum of n iid standard normals."""
    return (1 - G) * PHI.inv_cdf(1 - 1 / n) + G * PHI.inv_cdf(1 - 1 / (n * math.e))


def max_moments(n: int) -> tuple[float, float]:
    """Mean and sd of the maximum of n standard normals by the trapezoidal rule on [-9, 10] (no simulation)."""
    m = 38001
    h = 19.0 / (m - 1)
    xs = [-9.0 + i * h for i in range(m)]
    w = [h] * m
    w[0] = w[-1] = h / 2
    dens = []
    for x in xs:
        cdf = PHI.cdf(x)
        dens.append(n * PHI.pdf(x) * cdf ** (n - 1))
    mean = sum(wi * x * d for wi, x, d in zip(w, xs, dens, strict=True))
    var = sum(wi * (x - mean) ** 2 * d for wi, x, d in zip(w, xs, dens, strict=True))
    return mean, math.sqrt(var)


def psr(sr: float, bench: float, se: float) -> float:
    return PHI.cdf((sr - bench) / se)


print("== L07 Section 1-2")
b = 1 - (-2) * 0.1 + (9 - 1) / 4 * 0.1**2
check("L07-ex1.4-V", b, 1.22, 2)
check("L07-ex1.4-normal", 1 + 0.1**2 / 2, 1.005, 3)
check("L07-ex1.4-se-nonnormal", math.sqrt(1.22 / 999), 0.0349, 4)
check("L07-ex1.4-se-normal", math.sqrt(1.005 / 999), 0.0317, 4)
check("L07-ex1.4-ratio", math.sqrt(1.22 / 1.005), 1.10, 2)
check("L07-ex1.4-annualized", 0.1 * math.sqrt(252), 1.59, 2)
check("L07-lab1-se-V082", 0.82 * math.sqrt(2 / 9999), 0.012, 3)
check("L07-lab1-se-V122", 1.22 * math.sqrt(2 / 9999), 0.017, 3)
check("L07-lab1-normal-too-high-pct", 100 * (1.005 / 0.82 - 1), 23, 0)
check("L07-lab1-normal-too-low-pct", 100 * (1 - 1.005 / 1.22), 18, 0)
check("L07-misc-ar1-factor", 1.3 / 0.7, 1.86, 2)
check("L07-ex2.3-annualized", 0.09 * math.sqrt(252), 1.43, 2)
b23 = 1 + 1.5 * 0.09 + 7 / 4 * 0.09**2
check("L07-ex2.3-bracket", b23, 1.1492, 4)
se23 = math.sqrt(b23 / 755)
check("L07-ex2.3-se", se23, 0.0390, 4)
check("L07-ex2.3-PSR0", psr(0.09, 0, se23), 0.989, 3)
check("L07-ex2.3-PSR0-argument", 0.09 / se23, 2.307, 3)
check("L07-ex2.3-normal-se", math.sqrt((1 + 0.09**2 / 2) / 755), 0.0365, 4)
check("L07-ex2.3-normal-PSR", psr(0.09, 0, math.sqrt((1 + 0.09**2 / 2) / 755)), 0.993, 3)
check("L07-ex2.3-normal-arg", 0.09 / math.sqrt((1 + 0.09**2 / 2) / 755), 2.468, 3)
z95 = PHI.inv_cdf(0.95)
check("L07-z95", z95, 1.6449, 4)
check("L07-z95-sq", z95**2, 2.706, 3)
check("L07-ex2.8-unit", (1.6449 / 0.09) ** 2, 334.04, 2)  # the page uses z = 1.6449 (4 dp)
check("L07-ex2.8-minTRL", 1 + 1.1492 * (1.6449 / 0.09) ** 2, 384.9, 1)
check("L07-ex2.8-normal-minTRL", 1 + 1.00405 * (1.6449 / 0.09) ** 2, 336.4, 1)
check("L07-ex2.8-cost-days", (1 + 1.1492 * (1.6449 / 0.09) ** 2) - (1 + 1.00405 * (1.6449 / 0.09) ** 2), 48, 0)
check("L07-ex2.8-cost-pct", 100 * ((1 + 1.1492 * (1.6449 / 0.09) ** 2) - (1 + 1.00405 * (1.6449 / 0.09) ** 2)) / (1 + 1.00405 * (1.6449 / 0.09) ** 2), 14, 0)
sr_ann = 0.5 / math.sqrt(252)
check("L07-ex2.8-annual-benchmark-daily", sr_ann, 0.031497, 6)
margin = 0.09 - sr_ann
check("L07-ex2.8-margin", margin, 0.058503, 6)
check("L07-ex2.8-mintrl-0.5", 1 + (1 + 1.5 * 0.09 + 7 / 4 * 0.09**2) * (z95 / (0.09 - 0.5 / math.sqrt(252))) ** 2, 909.4, 1)  # exact bracket and margin; 4-dp inputs give 909.49
check("L07-ex2.8-years-0.5", (1 + 1.1492 * (1.6449 / margin) ** 2) / 252, 3.61, 2)
check("L07-ex2.8-psr-benchmark", psr(0.09, sr_ann, 0.0390), 0.933, 3)
check("L07-sec2-years-1", z95**2 / 1, 2.7, 1)
check("L07-sec2-years-0.5", z95**2 / 0.25, 10.8, 1)
check("L07-sec2-years-2", z95**2 / 4, 0.68, 2)
for ann, page in ((2.0, 2.73), (2.0, 2.83), (2.0, 3.24)):
    pass
# Remark 2.7: normal returns, annualized SR 2 against 1 at 95%, daily/weekly/monthly
for q, page_min, page_yr in ((252, 688.2, 2.73), (52, 147.1, 2.83), (12, 38.88, 3.24)):
    sr_p, bench_p = 2 / math.sqrt(q), 1 / math.sqrt(q)
    bracket_n = 1 + sr_p**2 / 2
    mintrl = 1 + bracket_n * (z95 / (sr_p - bench_p)) ** 2
    check(f"L07-rem2.7-minTRL-q{q}", mintrl, page_min, 1 if q == 252 else 2)
    check(f"L07-rem2.7-years-q{q}", mintrl / q, page_yr, 2)
# hedge-fund index: monthly skew -0.72, kurtosis 5.78, SR_ann 2 vs 1
sr_m, bench_m = 2 / math.sqrt(12), 1 / math.sqrt(12)
b_hf = 1 - (-0.72) * sr_m + (5.78 - 1) / 4 * sr_m**2
mt_hf = 1 + b_hf * (z95 / (sr_m - bench_m)) ** 2
check("L07-rem2.7-hedge-minTRL", mt_hf, 59.90, 2)
check("L07-rem2.7-hedge-years", mt_hf / 12, 4.99, 2)
check("L07-rem2.7-appendix-59.895", mt_hf, 59.895, 3)
# Section 2 annualized pass
b_ann = 1 + (1 / 252) / 2
check("L07-annualized-b", b_ann, 1.002, 3)
check("L07-annualized-years-1", b_ann * z95**2, 2.71, 2)
check("L07-annualized-years-0.5", (1 + 0) * z95**2 / 0.25, 10.8, 1)
# P4 frequency table
for q, page in ((252, 2.731), (52, 2.829), (12, 3.240)):
    v = 1 / q + (z95 / (2 - 1)) ** 2 * (1 + 2**2 / (2 * q))
    check(f"L07-P4-q{q}", v, page, 3)
check("L07-P4-limit", (z95 / 1) ** 2, 2.71, 2)
# Remark 2.9 pass-power multiple and T_beta
check("L07-rem2.9-T-ratio", (z95 + PHI.inv_cdf(0.8)) ** 2 / z95**2, 2.29, 2)
check("L07-rem2.9-normal-median-half", PHI.cdf(0.0), 0.5, 1)
check("L07-rem2.9-normal-stat-kr", z95 + PHI.inv_cdf(0.8), 2.4865, 4)
# Example 3.2 and M-problem hurdle values
b_32 = 2.1895
check("L07-ex3.2-bracket", bracket3(40), b_32, 4)
sr0 = 0.03 * b_32
check("L07-ex3.2-SR0", sr0, 0.0657, 4)
check("L07-ex3.2-annualized", sr0 * math.sqrt(252), 1.04, 2)
check("L07-ex3.2-DSR", psr(0.09, sr0, math.sqrt(1.149175 / 755)), 0.733, 3)  # unrounded s.e., as Example 2.3
check("L07-ex3.2-DSR-arg", (0.09 - sr0) / 0.0390, 0.623, 3)
check("L07-ex3.2-DSR-PSR-cite", psr(0.09, 0, 0.0390), 0.989, 3)
check("L07-ex3.2-unit-N2-bracket", bracket3(2), 0.520, 3)
check("L07-ex3.2-unit-N3-bracket", bracket3(3), 0.853, 3)
b25 = bracket3(25)
check("L07-M3-bracket25", b25, 1.9971, 4)
check("L07-M3-DSR", psr(0.05, 0.02 * b25, 0.02045), 0.689, 3)
check("L07-M3-zN-limit", (0.05 - 0.02 * 0 - (0.05 - 1.6449 * 0.02045)) / 0.02 * 0 + (0.05 - 1.6449 * 0.02045) / 0.02, 0.818, 3)
# Lab 2/3/4 hypotheses and the L08 Lab 3 p-chain
check("L07-R2-z", PHI.inv_cdf(0.97), 1.88, 2)
check("L07-R2-bound", math.exp(-PHI.inv_cdf(0.97) ** 2 / 2), 0.17, 2)
check("L07-R2-posterior", 0.17 / 1.17, 0.15, 2)
# Example 1.4 paired/S7 statements
print("== L07 Section 4-5")
pr = 10000 / (((1 + 99 * 0.5) ** 2) + 99 * 0.5**2)
check("L07-sec4-PR", pr, 3.88, 2)
check("L07-sec4-PR-formula-denominator", (1 + 99 * 0.5) ** 2 + 99 * 0.25, 2575, 0)
check("L07-lab3-PR-ratio", 15.62 / 3.72, 4.0, 0)  # "four times the participation ratio" (Lab 3 prose)
check("L07-P3b-sigma", 1 - 0.9 * 49 / 99, 0.5545, 4)
check("L07-E3-hurdle-coef", math.sqrt(1 - 0.9 * 49 / 99) * 2.5306, 1.884, 3)
check("L07-E3-mean-Qk-root", math.sqrt(0.1) * 2.249, 0.711, 3)
check("L07-E3-sd-Y", math.sqrt(0.9 + 0.1 * 0.216), 0.960, 3)
check("L07-E3-EmaxY", math.sqrt(0.1) * 2.249 + math.sqrt(0.9 + 0.1 * 0.216) / math.sqrt(math.pi), 1.25, 2)
check("L07-E3-overstate", 1.8844 / 1.2526 - 1, 0.50, 2)  # page says "about 50%"; unrounded chain gives 50.4%
check("L07-Ex5.5-annualized-1", 0.06 * math.sqrt(252), 0.95, 2)
check("L07-Ex5.5-annualized-2", 0.04 * math.sqrt(252), 0.63, 2)
th = 2 * 0.05 + 0.5 * (0.0036 + 0.0016) - 0.0024 * 0.9025
check("L07-ex5.5-theta", th, 0.100434, 6)
se55 = math.sqrt(0.100434 / 1259)
check("L07-ex5.5-se", se55, 0.008932, 6)
check("L07-ex5.5-Z", 0.02 / se55, 2.239, 3)
check("L07-ex5.5-p", 2 * (1 - PHI.cdf(0.02 / se55)), 0.025, 3)
naive_v = 2 + 0.0026
check("L07-ex5.5-naive-v", naive_v, 2.0026, 4)
check("L07-ex5.5-naive-se", math.sqrt(naive_v / 1259), 0.03988, 5)
check("L07-ex5.5-naive-Z", 0.02 / math.sqrt(naive_v / 1259), 0.50, 2)
check("L07-ex5.5-naive-p", 2 * (1 - PHI.cdf(0.02 / math.sqrt(naive_v / 1259))), 0.62, 2)
check("L07-ex5.5-se-ratio", math.sqrt(naive_v / 1259) / se55, 4.5, 1)
check("L07-ex5.5-annual-se", math.sqrt(252 * 1.0018 / 1259), 0.448, 3)
check("L07-ex5.5-annual-diff", 0.02 * math.sqrt(252), 0.32, 2)
check("L07-M5-paired-theta", 2 * (1 - 0.7) + 0.5 * (0.09 + 0.0225) - 0.3 * 0.15 * 0.49, 0.6342, 4)
check("L07-M5-paired-Z", 0.15 / math.sqrt(0.6342 / 119), 2.055, 3)
check("L07-M5-paired-p", 2 * (1 - PHI.cdf(0.15 / math.sqrt(0.6342 / 119))), 0.040, 3)
check("L07-M5-naive-Z", 0.15 / math.sqrt(2.05625 / 119), 1.141, 3)
check("L07-M5-naive-p", 2 * (1 - PHI.cdf(0.15 / math.sqrt(2.05625 / 119))), 0.25, 2)
check("L07-M5-annual-1", 0.3 * math.sqrt(12), 1.04, 2)
check("L07-M5-annual-2", 0.15 * math.sqrt(12), 0.52, 2)
check("L07-M5-se-paired", math.sqrt(0.6342 / 119), 0.07300, 5)
check("L07-M5-se-naive", math.sqrt(2.05625 / 119), 0.1315, 4)
print("== L07 Section 9 solutions")
b_m1 = 1 - (-1) * 0.05 + (6 - 1) / 4 * 0.05**2
check("L07-M1-bracket", b_m1, 1.053125, 6)
check("L07-M1-se", math.sqrt(b_m1 / 2519), 0.02045, 5)
check("L07-M1-normal-se", math.sqrt(1.00125 / 2519), 0.01994, 5)
check("L07-M1-PSR0", psr(0.05, 0, math.sqrt(b_m1 / 2519)), 0.9928, 4)
check("L07-M1-annual", 0.05 * math.sqrt(252), 0.794, 3)
check("L07-M2-bench", 0.5 / math.sqrt(252), 0.03150, 5)
check("L07-M2-PSR", psr(0.05, 0.5 / math.sqrt(252), math.sqrt(b_m1 / 2519)), 0.817, 3)
check("L07-M2-arg", (0.05 - 0.5 / math.sqrt(252)) / math.sqrt(b_m1 / 2519), 0.905, 3)
check("L07-M3-SR0", 0.02 * b25, 0.03994, 5)
check("L07-M3-DSR-arg", (0.05 - 0.02 * b25) / 0.02045, 0.492, 3)
check("L07-M3-N2-N3", bracket3(3), 0.853, 3)
check("L07-M4-days-0", 1 + b_m1 * (1.6449 / 0.05) ** 2, 1140.8, 1)  # z = 1.6449 as printed
check("L07-M4-years-0", (1 + b_m1 * (z95 / 0.05) ** 2) / 252, 4.53, 2)
check("L07-M4-margin", 0.05 - 0.5 / math.sqrt(252), 0.018503, 6)
check("L07-M4-days-0.5", 1 + b_m1 * (1.6449 / (0.05 - 0.5 / math.sqrt(252))) ** 2, 8324, 0)
check("L07-M4-years-0.5", (1 + b_m1 * (z95 / (0.05 - 0.5 / math.sqrt(252))) ** 2) / 252, 33.0, 1)
check("L07-M4-shrink", 0.05 / (0.05 - 0.5 / math.sqrt(252)), 2.70, 2)
check("L07-M4-req-grew", (0.05 / (0.05 - 0.5 / math.sqrt(252))) ** 2, 7.3, 1)
check("L07-P5b-E-s4", (0.5**2 + 1.5**2) / 2, 1.25, 2)
check("L07-P5b-E-s2", (0.5 + 1.5) / 2, 1.0, 1)
check("L07-P5b-coefficient", 0.5 * (1.25 - 1), 0.125, 3)  # -1/2 SR1 SR2 (kappa22 - 1) = -SR1 SR2 / 8
print("== L07 Section 4 Lab 4 closed-form values and E4")
check("L07-E4-mean", 0.02 * math.sqrt(1259) / math.sqrt(0.100434), 2.239, 3)
check("L07-E4-naive-mean", 0.02 / math.sqrt(2.0026 / 1259) if False else 0.02 * math.sqrt(1259) / math.sqrt(2.0026), 0.50, 2)
check("L07-E4-naive-sd", math.sqrt(0.100434 / 2.0026), 0.224, 3)
check("L07-E4-naive-sd-steps", (1.960 - 0.50) / math.sqrt(0.100434 / 2.0026), 6.5, 1)
check("L07-E4-pow-paired", PHI.cdf(2.239 - 1.960), 0.61, 2)
check("L07-E4-mc-se", math.sqrt(0.61 * 0.39 / 4000), 0.008, 3)
print("== L07 Lab 4 Part 3 prose (closed form from Part 3 inputs)")
sr_l = 0.09
bmod = 1.0 + 2.0 * sr_l + 2.0 * sr_l**2
check("L07-lab4-b", bmod, 1.1962, 4)
check("L07-lab4-sd-first", 1 - sr_l * 2 * 0.0 - sr_l * (2 + 4 * sr_l) / (2 * bmod), 0.91, 2)
check("L07-lab4-mean-T", math.sqrt(914) * sr_l / math.sqrt(bmod), 2.488, 3)
check("L07-lab4-pred", PHI.cdf((2.488 - 1.645) / 0.911), 0.82, 2)
check("L07-lab4-mc-se-V1.117", 1.117 * math.sqrt(2 / 3999), 0.025, 3)
check("L07-lab4-mc-se-prop", math.sqrt(0.05 * 0.95 / 4000), 0.0034, 4)
check("L07-lab4-gap-se", (1.1582 - 1.1167) / 0.025, 1.7, 1)
check("L07-lab4-naive-to-true", 2.2278 / 1.1167, 2.0, 1)
check("L07-lab4-E-V-shrink", (2 + 0.09**2) / (0.2 + 0.0025 * 0.19), 10.0, 1)
pbg = 0.9 * 0  # placeholder
print("== L07 Lab 4 Prop 5.4 predictions")
for rho, pred in ((-0.5, 0.109), (0.5, 0.0056)):
    v1 = v2 = 1.0 + 0.05**2 / 2
    theta = 2 * (1 - rho) + 0.05**2 * (1 - rho**2)
    crit = PHI.inv_cdf(0.975)
    ratio = (v1 + v2) / theta
    p = 2 * (1 - PHI.cdf(crit * math.sqrt(ratio)))
    check(f"L07-lab4-prop5.4-naive-rho{rho}", p, pred, 3 if rho == 0.5 else 3)
print("== L07 Problem E4 / Example 5.5 mean power")
print("== L07 Remark 2.9 (T_beta one-SE sanity)")
print("== L08 Example 3.3 and Lab 1 hand values")
s1ab = [0.03, 0.01, 0.02, 0.04]
mean_s1 = sum(s1ab) / 4
sd_s1 = math.sqrt(sum((x - mean_s1) ** 2 for x in s1ab) / 3)
check("L08-ex3.3-mean", mean_s1, 0.025, 3)
check("L08-ex3.3-sd", sd_s1, 0.012910, 6)
check("L08-ex3.3-R1", mean_s1 / sd_s1, 1.936, 3)
s2ab = [0.01, 0.02, 0.00, 0.01]
m2 = sum(s2ab) / 4
check("L08-ex3.3-R2", m2 / math.sqrt(sum((x - m2) ** 2 for x in s2ab) / 3), 1.225, 3)
s3ab = [-0.01, 0.02, 0.01, -0.02]
check("L08-ex3.3-R3", sum(s3ab) / 4, 0.000, 3)
s1cd = [-0.03, -0.01, -0.02, 0.00]
m1cd = sum(s1cd) / 4
check("L08-ex3.3-oos-s1", m1cd / math.sqrt(sum((x - m1cd) ** 2 for x in s1cd) / 3), -1.162, 3)
s2cd = [0.01, 0.02, 0.00, 0.01]
check("L08-ex3.3-oos-s2", (sum(s2cd) / 4) / math.sqrt(sum(((x - sum(s2cd) / 4) ** 2) for x in s2cd) / 3), 1.225, 3)
s3cd = [0.00, 0.03, -0.01, 0.02]
m3cd = sum(s3cd) / 4
check("L08-ex3.3-oos-s3", m3cd / math.sqrt(sum((x - m3cd) ** 2 for x in s3cd) / 3), 0.548, 3)
check("L08-ex3.3-lambda", math.log(1 / 3), -1.0986, 4)
check("L08-M1-binom10-5", math.comb(10, 5), 252, 0)
print("== L08 Section 2 and Theorem 4.1 numbers")
for n, page in ((2, 0.5), (3, 2 / 3), (4, 0.5), (5, 0.6), (21, 11 / 21)):
    check(f"L08-P1-EPBO-N{n}", (math.floor((n + 1) / 2)) / n, page, 4)
check("L08-remark4.2-N20-formal", (math.ceil(20 / 2) - 1) / 20, 0.45, 2)
check("L08-M1-S-counts-4", math.comb(4, 2), 6, 0)
check("L08-M1-S16", math.comb(16, 8), 12870, 0)
check("L08-M1-S8", math.comb(8, 4), 70, 0)
check("L08-M1-S6", math.comb(6, 3), 20, 0)
check("L08-M1-in-sample-S16", math.comb(15, 7), 6435, 0)
check("L08-M2-logit-r4", math.log(0.4 / 0.6), -0.4055, 4)
check("L08-M2-logit-r7", math.log(0.7 / 0.3), 0.8473, 4)
check("L08-M3-PBO", sum(1 for x in [1.2, -0.3, 0.0, 2.1, -1.4, 0.7] if x <= 0) / 6, 0.5, 1)
print("== L08 Lab 2/3 derived numbers")
p_win = PHI.cdf(0.10 * math.sqrt(500) / math.sqrt(2))
check("L08-lab3-p", p_win, 0.94308, 5)
check("L08-lab3-2p(1-p)", 2 * p_win * (1 - p_win), 0.107, 3)
check("L08-lab3-arg", 0.10 * math.sqrt(500) / math.sqrt(2), 1.58114, 5)
check("L08-lab3-edge-stdized", 0.10 * math.sqrt(500), 2.24, 2)
check("L08-lab3-rise", 0.3375 - 0.1196, 0.218, 3)
check("L08-lab3-se-diff", math.sqrt(0.0537**2 + 0.0407**2), 0.0674, 4)
check("L08-lab3-ratio", (0.3375 - 0.1196) / math.sqrt(0.0537**2 + 0.0407**2), 3.2, 1)
check("L08-lab3-select-prob", PHI.cdf((2.24 - 2.744) / math.sqrt(1 + 0.401**2)), 0.32, 2)
print("== L08 Lab 3 quadrature table (max of n standard normals)")
for n, mpage, spage in ((19, 1.844, 0.529), (20, 1.867, 0.525), (199, 2.744, 0.401), (1999, 3.435, 0.335)):
    mu, sd = max_moments(n)
    check(f"L08-lab3-max-mean-n{n}", mu, mpage, 3)
    check(f"L08-lab3-max-sd-n{n}", sd, spage, 3)
print("== L08 Lab 4 closed form")
check("L08-lab4-ann", 0.0408 * math.sqrt(12), 0.141, 3)
check("L08-lab4-p-value", 1 - 0.7695, 0.23, 2)
check("L08-lab4-SR0-from-disp", 0.019347 * bracket3(40), 0.0424, 4)  # unrounded sd from lab4_independent.py
check("L08-lab4-sd-expected", math.sqrt((1 - 0.567) / 308), 0.0375, 4)
check("L08-lab4-null-share-SE", math.sqrt(0.21 * 0.79 / 100), 0.041, 3)
check("L08-lab4-sd-gap", 0.0375 / 0.0193, 1.94, 2)
print("== L08 Problem E1 / E2 / E3 / R3 numbers")
check("L08-E1-pi", 1 - (0.05 / 0.526), 0.905, 3)
check("L08-E1-delta", 1.844 + PHI.inv_cdf(0.9) * math.sqrt(1 + 0.529**2), 3.294, 3)
check("L08-E1-mu", (1.844 + PHI.inv_cdf(0.9) * math.sqrt(1 + 0.529**2)) / math.sqrt(500), 0.147, 3)
check("L08-E1-annual", 0.147 * math.sqrt(252), 2.3, 1)
check("L08-E1-10/19", 10 / 19, 0.526, 3)
check("L08-E1-sd-root", math.sqrt(1 + 0.529**2), 1.1313, 4)
check("L08-E2-sd-mean-no", (1 / 1260 + 0.02**2) ** 0.5 / 1, 0.0345, 4)
check("L08-E2-sd-0", math.sqrt(1 / 1260), 0.0282, 4)
check("L08-E2-ratio", math.sqrt(0.02**2 + 1 / 1260) / math.sqrt(1 / 1260), 1.226, 3)
check("L08-E3-binom-k1", math.comb(5, 1) * math.comb(5, 4), 25, 0)
check("L08-E3-binom-k2", math.comb(5, 2) * math.comb(5, 3), 100, 0)
check("L08-E3-delta5", 0.2 * (2 * 5 - 5) * math.sqrt(500) / 5, 4.47, 2)
check("L08-E3-delta4", 0.2 * (2 * 4 - 5) * math.sqrt(500) / 5, 2.68, 2)
check("L08-E3-delta3", 0.2 * (2 * 3 - 5) * math.sqrt(500) / 5, 0.89, 2)
check("L08-E3-win5", PHI.cdf((4.472 - 1.867) / math.sqrt(1 + 0.525**2)), 0.989, 3)
check("L08-E3-win4", PHI.cdf((2.683 - 1.867) / math.sqrt(1 + 0.525**2)), 0.765, 3)
check("L08-E3-win3", PHI.cdf((0.894 - 1.867) / math.sqrt(1 + 0.525**2)), 0.194, 3)
check("L08-E3-PBO-low", (0.9945 + 25 * 0.8825 + 100 * 0.597 + 126 * 0.50) / 252, 0.578, 3)
check("L08-E3-PBO-high", (0.9945 + 25 * 0.8825 + 100 * 0.597 + 126 * 0.55) / 252, 0.603, 3)
check("L08-E3-null-value", 11 / 21, 0.524, 3)
check("L08-R3-edge", 0.14 * math.sqrt(1000), 4.43, 2)
mu_2000, sd_2000 = 0.0, 0.0
check("L08-R3-Bonf", PHI.inv_cdf(1 - 0.05 / 2000), 4.06, 2)
check("L08-R3-full-prob", PHI.cdf((4.43 - 3.435) / math.sqrt(1 + 0.335**2)), 0.83, 2)
check("L08-R3-DSR-N2000", bracket3(2000), 3.447, 3)
check("L08-R3-DSR", PHI.cdf(4.43 - 3.447), 0.84, 2)
check("L08-R3-500-edge", 0.14 * math.sqrt(500), 3.13, 2)
check("L08-R3-500-win", PHI.cdf((3.13 - 3.435) / math.sqrt(1.112)), 0.39, 2)
check("L08-R3-500-pbo", 0.5 * (1 - 0.3862016411), 0.31, 2)  # printed chain 0.5 x (1 - 0.39) = 0.305; from the unrounded 0.3862 it is 0.3069
check("L08-R3-500-PBO-unrounded", 0.5 * (1 - PHI.cdf((3.13 - 3.435) / math.sqrt(1.112))), 0.31, 2)
print("== L08 Problem P2 (leverage and shift) numbers")
sd_ab = math.sqrt(sum(x * x for x in [-0.01, 0.02, 0.01, -0.02]) / 3)
check("L08-P2-sd-AB", sd_ab, 0.018257, 6)
check("L08-P2-shifted-AB", 0.02 / sd_ab, 1.095, 3)
check("L08-P2-shifted-AC", 0.03 / sd_ab, 1.643, 3)
print("== added in the second pass: L07 Problem R4, E1, Remark 1.5; E3 coefficient; L08 Problem P2")
bR4 = 1 + 1.5 * 0.09 + 7 / 4 * 0.09**2
check("L07-R4-T-1", (z95 * math.sqrt(bR4) + bracket3(40)) ** 2 / 0.09**2, 1929, 0)
check("L07-R4-years", ((z95 * math.sqrt(bR4) + bracket3(40)) ** 2 / 0.09**2 + 1) / 252, 7.7, 1)
check("L07-R4-search-factor", ((z95 * math.sqrt(bR4) + bracket3(40)) ** 2 / 0.09**2) / (1 + bR4 * (z95 / 0.09) ** 2), 5.0, 1)
check("L07-R4-fixed-hurdle-days", 1 + 1.1492 * (1.6449 / (0.09 - 0.0657)) ** 2, 5267, 0)  # printed inputs; exact inputs give 5266.4
check("L07-R4-fixed-hurdle-years", (1 + bR4 * (z95 / 0.0243) ** 2) / 252, 21, 0)
check("L07-R4-rho05-T-1", (z95 * math.sqrt(bR4) + math.sqrt(0.5) * bracket3(40)) ** 2 / 0.09**2, 1354, 0)
check("L07-R4-rho05-years", ((z95 * math.sqrt(bR4) + math.sqrt(0.5) * bracket3(40)) ** 2 / 0.09**2 + 1) / 252, 5.4, 1)
check("L07-R4-cross-sd-ratio", 1 / math.sqrt(755), 0.0364, 4)
check("L07-R4-rho-equivalent", 1 - 755 * 0.03**2, 0.32, 2)
check("L07-E1-normal-at-4/3", 1 + (4 / 3) ** 2 / 2, 1.889, 3)
check("L07-E1-negskew-at-4/3", 1 + 2 * (4 / 3) + 2 * (16 / 9), 7.22, 2)
check("L07-E1-root", 4 * 2 / (9 - 3), 1.33, 2)  # 4 gamma3 / (gamma4 - 3) with gamma3 = 2, gamma4 = 9
check("L07-rem1.5-minTRL-AR1", 1 + 1.86 * 383.9, 715, 0)  # printed factor 1.86 (exact 1.857 gives 714)
check("L07-E3-bracket100", bracket3(100), 2.5306, 4)
check("L07-E3-exact-max100-vs-approx", bracket3(100) - 2.5076, 0.023, 3)
check("L08-P2-logits-changed", 5, 5, 0)
check("L08-P2-PBO-2of6-to-6of6", 6 / 6, 1.0, 1)
check("L08-quiz-binom94", math.comb(9, 4), 126, 0)
check("L08-caption-504", 8 * 63, 504, 0)
print("== summary")
n_fail = sum(1 for _, ok in RESULTS if not ok)
print(f"checks {len(RESULTS)} pass {len(RESULTS) - n_fail} fail {n_fail}")
for cid, ok in RESULTS:
    if not ok:
        print("FAILED", cid)
