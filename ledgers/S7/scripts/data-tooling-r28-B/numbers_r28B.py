"""Round 28 (part B) independent recomputation of page numbers in the changed hunks. Usage: python -I numbers_r28B.py <checkout>
Exact expectations by scipy quad (no simulation); Phi^-1 by scipy.stats.norm.ppf; BH by hand on Example 2.2's p-values."""
import math
import sys
from fractions import Fraction
from scipy import integrate, stats

N = stats.norm
def emax_density(n):
    f = lambda x: n * N.pdf(x) * N.cdf(x) ** (n - 1)
    m = integrate.quad(lambda x: x * f(x), -12, 12, limit=500)[0]
    v = integrate.quad(lambda x: x * x * f(x), -12, 12, limit=500)[0] - m * m
    return m, math.sqrt(v)
def approx3(n):
    g = 0.5772156649015329
    return (1 - g) * N.ppf(1 - 1 / n) + g * N.ppf(1 - 1 / (n * math.e))

print("== L01 Lab 1 second table (exact mean, sd of the maximum of N normals) vs page 1.5388/0.5868, 1.8675/0.5251, 2.5076/0.4294, 3.2414/0.3514")
for n in (10, 20, 100, 1000):
    m, s = emax_density(n)
    print(f"N={n}: mean {m:.4f} sd {s:.4f}   approx(3) {approx3(n):.4f}")
print("== L01 M1 (page 504-505): bound, estimate, exact-mean route")
bound = math.sqrt(2 * math.log(20)); per = 1 / math.sqrt(756); ann = math.sqrt(252)
print(f"(a) sqrt(2 ln 20)={bound:.6f} (2.4477); 1/sqrt(756)={per:.6f} (0.03637); sqrt(252)={ann:.4f} (15.875); bound={bound*per*ann:.5f} (1.413)")
br = 0.4228 * N.ppf(0.95) + 0.5772 * N.ppf(1 - 1 / (20 * math.e))
print(f"(b) Phi^-1(0.95)={N.ppf(0.95):.6f} (1.6449); Phi^-1(1-1/(20e))={N.ppf(1 - 1/(20*math.e)):.6f} (2.0881); bracket={0.4228*N.ppf(0.95)+0.5772*N.ppf(1-1/(20*math.e)):.4f} (1.9007); est={br*per*ann:.4f} (1.097)")
m20, _ = emax_density(20)
print(f"(c) exact E[max 20]={m20:.4f} (1.8675); x per x ann = {m20*per*ann:.4f} (1.078); approx(3) at 20 annualised = {approx3(20)*per*ann:.4f} (1.10)")
print("== L01 M2 (page 512-513): 60 monthly obs, 50 configs, annualised by sqrt(12)")
per2 = 1 / math.sqrt(60); ann2 = math.sqrt(12)
print(f"bound sqrt(2 ln 50)={math.sqrt(2*math.log(50)):.6f} (2.7971); x {per2:.5f} x {ann2:.4f} = {math.sqrt(2*math.log(50))*per2*ann2:.4f} (1.251)")
print(f"bracket(50)={0.4228*N.ppf(0.98)+0.5772*N.ppf(1-1/(50*math.e)):.4f} (2.2763); estimate {(0.4228*N.ppf(0.98)+0.5772*N.ppf(1-1/(50*math.e)))*per2*ann2:.4f} (1.018)")
print("== L01 E1 solution (page 588): sqrt(252/630) and products")
k = math.sqrt(252 / 630)
print(f"sqrt(252/630)={k:.9f} (0.632456)")
for n in (10, 100, 1000):
    a = approx3(n)
    m, s = emax_density(n)
    print(f"N={n}: approx3 {a:.4f} x k = {a*k:.4f}; exact {m:.4f} x k = {m*k:.4f}; gap {a*k - m*k:.4f}; sd {s:.4f} * k / 10 = {s*k/10:.4f}")
print("== L02 Example 2.4 (line 126) and misconception (356)")
sid = 1 - 0.95 ** (1 / 20)
print(f"Sidak 1-0.95^(1/20)={sid:.10f} (0.0025614); gain {sid/0.0025-1:.5f} (2.46%); Bonferroni FWER(indep, all null) 1-(1-0.0025)^20={1-(1-0.0025)**20:.5f} (0.0488)")
print("== L03 BH on Example 2.2 p-values (page 95 caption)")
p = [0.001, 0.008, 0.012, 0.021, 0.024, 0.046, 0.060, 0.074, 0.205, 0.212]
q, m = 0.05, len(p)
ks = [k for k in range(1, m + 1) if p[k - 1] <= k * q / m]
kstar = max(ks)
rej = list(range(1, kstar + 1))
print(f"BH line k*q/m: {[round(k*q/m,3) for k in range(1,m+1)]}")
print(f"largest k with p(k) <= k q/m: {kstar}; rejected ranks {rej}; rank 4 p={p[3]} > its line {4*q/m:.3f}: rejected={4 in rej}")
print("== L06 Prop 3.2 proof constants (page 276)")
c = math.sqrt(math.pi / 2) / math.e
zs = N.ppf(1 - (1 / math.e) / 2)
print(f"c={c:.8f} (0.46107); z*=Phi^-1(1-p/2) at p=1/e: {zs:.6f} (0.9005); z*+1/z*={zs+1/zs:.6f} (2.01101); u(z*)=1-c(z*+1/z*)={1-c*(zs+1/zs):.6f} (0.0728)")
z = N.ppf(0.7)
print(f"p=0.6: z=Phi^-1(0.7)={z:.6f} (0.5244); z^2/2={z*z/2:.6f} (0.1375); -ln 0.6={-math.log(0.6):.6f} (0.5108)")
print("== L07 E3 (page 683)")
m50, s50 = emax_density(50)
print(f"Q50 mean {m50:.6f} (2.249), var {s50*s50:.6f} (0.216)")
rho_bar = 2 * math.comb(50, 2) * 0.9 / math.comb(100, 2)
print(f"avg pairwise corr {rho_bar:.5f}; 1-rho={1-rho_bar:.5f} (0.5545); sqrt*2.5306 = {math.sqrt(1-rho_bar)*2.5306:.4f} (1.884); approx3(100)={approx3(100):.5f} (2.5306)")
mu_y = math.sqrt(0.1) * m50; sd_y = math.sqrt(0.9 + 0.1 * s50 * s50)
print(f"Y mean {mu_y:.4f} (0.711), sd {sd_y:.4f} (0.960); E max approx {mu_y + sd_y/math.sqrt(math.pi):.4f} (1.25); overstatement {1.884/1.25-1:.3f} (about 50%)")
