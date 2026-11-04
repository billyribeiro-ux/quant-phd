"""E4-b round 5 independent checks (L04-L06). Run as: python -I -S <this file> <checkout-root>.

1. Page expected blocks equal the stdout of each twin run under python -I -W error (stderr must be empty).
2. Page code blocks equal the twin file byte for byte (after HTML unescape).
3. Independent recomputation of every printed number in Parts A-E, using fractions and a separate OLS.
4. Recomputation of the displayed derivations: M1-M3, E2 arithmetic, Example 6.9, Part D residual, Prop 3.3, L05 ratios.
"""
import html
import random
import math
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
ok = True


def check(name, cond, detail=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (("  " + detail) if detail else ""))
    ok = ok and bool(cond)


def page_blocks(page):
    text = (root / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
    return html.unescape(code), html.unescape(expected)


for page, twin in (("L04", "lab-E4-L04-1"), ("L05", "lab-E4-L05-1"), ("L06", "lab-E4-L06-1")):
    code, expected = page_blocks(page)
    twin_src = (root / f"tests/labs/E4/{twin}.py").read_text(encoding="utf-8")
    check(f"{page} page code equals twin file", code.strip() == twin_src.strip())
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E4/{twin}.py")],
                       capture_output=True, text=True)
    check(f"{page} twin exit 0 and stderr empty", p.returncode == 0 and p.stderr == "", f"exit={p.returncode} stderr_bytes={len(p.stderr)}")
    check(f"{page} expected block equals twin stdout", expected.strip() == p.stdout.strip())

# ---------- L04 ----------
def rank(M):
    rows = [list(r) for r in M]
    n, m = len(rows), len(rows[0])
    used = 0
    for c in range(m):
        piv = next((i for i in range(used, n) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[used], rows[piv] = rows[piv], rows[used]
        for i in range(n):
            if i != used and rows[i][c] != 0:
                f = rows[i][c] / rows[used][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[used])]
        used += 1
    return used

V = lambda *x: [F(v) for v in x]
INC = [V(1, 1, 1), V(0, 1, 2)]
COM = [V(1, 0, 0), V(0, 1, 0), V(0, 0, 1), V(1, 2, 3)]
check("L04 rank incomplete = 2", rank(INC) == 2)
check("L04 rank complete = 3", rank(COM) == 3)
check("L04 (1,2,3) attainable in INC", rank(INC + [V(1, 2, 3)]) == rank(INC))
check("L04 (0,0,1) not attainable in INC (aug rank 3)", rank(INC + [V(0, 0, 1)]) == 3)
check("L04 (5,0,0) not attainable in INC (aug rank 3)", rank(INC + [V(5, 0, 0)]) == 3)
check("L04 all three attainable in COM", all(rank(COM + [c]) == 3 for c in (V(1, 2, 3), V(0, 0, 1), V(5, 0, 0))))
check("L04 weighted sum 1,2,3 of first three rows equals fourth", [sum(w * COM[j][k] for j, w in enumerate((1, 2, 3))) for k in range(3)] == COM[3])
t = F(1, 3)
z = [1 - t, 2 - 2 * t, 3 - 3 * t, t]
pay = [sum(z[j] * COM[j][k] for j in range(4)) for k in range(3)]
check("L04 E2 family payoff equals (1,2,3) at rational t", pay == V(1, 2, 3), str(pay))
check("L04 M1 rank of (1,2,0),(2,4,0) = 1", rank([V(1, 2, 0), V(2, 4, 0)]) == 1)
check("L04 M3 rank of r1..r4 = 2", rank([V(1, 2, 0), V(0, 1, 1), V(1, 3, 1), V(2, 5, 1)]) == 2)
check("L04 E3 rank of (1,1,0),(0,1,1),(1,2,1) = 2", rank([V(1, 1, 0), V(0, 1, 1), V(1, 2, 1)]) == 2)
check("L04 misconception 2 rows (1,1,1),(1,1,1),(0,1,2) rank 2", rank([V(1, 1, 1), V(1, 1, 1), V(0, 1, 2)]) == 2)
check("L04 M2 (0,0,1) unattainable with (1,0,1),(0,1,1)", rank([V(1, 0, 1), V(0, 1, 1), V(0, 0, 1)]) == 3)
# R3 nonnegative-holdings construction, sampled
ok_r3 = True
for x1 in range(-4, 5):
    for x2 in range(-4, 5):
        t3 = max(0, -x1, -x2)
        z1, z2, z3 = x1 + t3, x2 + t3, t3
        ok_r3 = ok_r3 and z1 >= 0 and z2 >= 0 and z3 >= 0 and (z1 - z3, z2 - z3) == (x1, x2)
check("L04 R3 nonnegative construction on a grid", ok_r3)
# Prop 4.2 counterexample: A = I_2, zeta>=0 cannot give (-1,0)

# ---------- L05 ----------
def run_L05(alpha, beta, vs, delta, start, steps):
    def Psi(c):
        return ((alpha - vs * c[0]) / beta, -(vs * c[1] + delta) / beta)
    tgt = (alpha / (beta + vs), -delta / (beta + vs))
    path = [start]
    for _ in range(steps):
        path.append(Psi(path[-1]))
    ratios0 = [(path[k + 1][0] - tgt[0]) / (path[k][0] - tgt[0]) for k in range(steps) if path[k][0] != tgt[0]]
    ratios1 = [(path[k + 1][1] - tgt[1]) / (path[k][1] - tgt[1]) for k in range(steps) if path[k][1] != tgt[1]]
    return tgt, [p[0] for p in path], [p[1] for p in path], ratios0, ratios1

tgt, c0p, c1p, r0, r1 = run_L05(F(10), F(2), F(1, 2), F(3, 4), (F(0), F(0)), 8)
check("L05 base fixed point (4,-3/10)", tgt == (F(4), F(-3, 10)))
check("L05 base c0 path printed", [str(x) for x in c0p] == ['0', '5', '15/4', '65/16', '255/64', '1025/256', '4095/1024', '16385/4096', '65535/16384'])
check("L05 base c1 path printed", [str(x) for x in c1p] == ['0', '-3/8', '-9/32', '-39/128', '-153/512', '-615/2048', '-2457/8192', '-9831/32768', '-39321/131072'])
check("L05 base ratios all -1/4", all(x == F(-1, 4) for x in r0 + r1) and len(r0) == 8)
tgt, c0p, c1p, r0, r1 = run_L05(F(10), F(2), F(2), F(3, 4), (F(0), F(0)), 6)
check("L05 equal: fixed point (5/2,-3/16), path alternates, ratio -1", tgt == (F(5, 2), F(-3, 16)) and c0p == [F(0), F(5), F(0), F(5), F(0), F(5), F(0)] and all(x == -1 for x in r0 + r1))
tgt, c0p, c1p, r0, r1 = run_L05(F(10), F(2), F(3), F(3, 4), (F(0), F(0)), 6)
check("L05 large: fixed point (2,-3/20), ratio -3/2", tgt == (F(2), F(-3, 20)) and all(x == F(-3, 2) for x in r0))
check("L05 large c0 path", [str(x) for x in c0p] == ['0', '5', '-5/2', '35/4', '-65/8', '275/16', '-665/32'])
beta, vs, alpha = F(2), F(1, 2), F(10)
w = beta / (beta + vs)
img = ((alpha - vs * 0) / beta, -(vs * 0 + F(3, 4)) / beta)
damp = ((1 - w) * 0 + w * img[0], (1 - w) * 0 + w * img[1])
check("L05 damped weight 4/5 reaches fixed point", w == F(4, 5) and damp == (F(4), F(-3, 10)))
check("L05 M1 fixed point (3,-1/2) at alpha12 beta3 vs1 delta2", (F(12) / 4, -F(2) / 4) == (3, F(-1, 2)))
check("L05 M2 ratios -1/3", (F(4) - 3) / (F(0) - 3) == F(-1, 3) and (F(-2, 3) + F(1, 2)) / F(1, 2) == F(-1, 3))
check("L05 M3 conditional variance 5/4", (F(4) + 1) / F(2) ** 2 == F(5, 4))
check("L05 E1 1025/256 - 4 = 1/256 and |e4|=1/64", F(1025, 256) - 4 == F(1, 256) and F(4, 256) == F(1, 64))
check("L05 E3 errors -2,3,-9/2,27/4 at varsigma=3", [F(0) - 2, F(5) - 2, F(-5, 2) - 2, F(35, 4) - 2] == [-2, 3, F(-9, 2), F(27, 4)])
check("L05 R1 nu=1/2, damped first component 5/2", F(2) / 4 == F(1, 2) and F(1, 2) * 5 == F(5, 2) == F(10, 4))
check("L05 Lab Part F identity on grid", all(
    (F(4) + F(-3, 10) * z) == (F(10) - F(1, 2) * (F(4) + F(-3, 10) * z) - F(3, 4) * z) / 2 for z in (-2, -1, 0, 1, 2)))

# ---------- L06 ----------
sv2, se2, a, lam, su2 = F(1), F(1), F(1), F(1, 2), F(1, 4)
tv, te = 1 / sv2, 1 / se2
kappa = a / (lam * te)
seta2 = se2 + kappa * kappa * su2
taueta = 1 / seta2
taubar = lam * te + (1 - lam) * taueta
thS = taubar / (tv + taubar)
thU = kappa * thS
check("L06 Part A values", (kappa, seta2, taueta, taubar, thS, thU) == (2, 2, F(1, 2), F(3, 4), F(3, 7), F(6, 7)))
varp = thS * thS * (sv2 + se2) + thU * thU * su2
cov = thS * sv2
slope = cov / varp
rv = sv2 - slope * cov
check("L06 Part B: Var(s)=2, Var(p)=27/49, Cov=3/7, slope 7/9, post var 2/3, rho2 1/3",
      (sv2 + se2, varp, cov, slope, rv, cov * cov / (sv2 * varp)) == (2, F(27, 49), F(3, 7), F(7, 9), F(2, 3), F(1, 3)))
omega = sv2 / (sv2 + se2)
VI = sv2 * se2 / (sv2 + se2)
def resid(s, u, ths, thu):
    price = ths * s - thu * u
    vp = ths * ths * (sv2 + se2) + thu * thu * su2
    cv = ths * sv2
    sl = cv / vp
    rvar = sv2 - sl * cv
    di = (omega * s - price) / (a * VI)
    du = (sl * price - price) / (a * rvar)
    return lam * di + (1 - lam) * du - u
GS = [F(-1), F(0), F(1), F(2)]
GU = [F(-1), F(0), F(1, 2), F(2)]
res = [resid(s, u, thS, thU) for s in GS for u in GU]
check("L06 Part C: 16 residuals all zero (independent)", len(res) == 16 and all(r == 0 for r in res))
check("L06 Part C informed demand at (1,0) = 1/7", (omega * 1 - thS) / (a * VI) == F(1, 7))
check("L06 Part D residual at (1,0) with theta_s=1/2 is -9/85", resid(F(1), F(0), F(1, 2), thU) == F(-9, 85))
# Example 6.9 uninformed demand at (1,0):
p10 = thS
xU = (slope * p10 - p10) / (a * rv)
xI = (omega * 1 - p10) / (a * VI)
check("L06 Example 6.9 x_I=1/7 and x_U=-1/7 at (1,0)", xI == F(1, 7) and xU == F(-1, 7), f"xI={xI} xU={xU}")
check("L06 Example 6.9 b = 7/9 and V_U = 2/3 by closed form", taueta / (thS * (tv + taueta)) == F(7, 9) and 1 / (tv + taueta) == F(2, 3))
# M1-M3
k1 = F(2) * 1 / F(1, 2); s1 = 1 + k1 ** 2 * F(1, 4); t1 = 1 / s1; tb1 = F(1, 2) + F(1, 2) * t1; th1 = tb1 / (1 + tb1); tu1 = k1 * th1
check("L06 M1 values kappa 4, sig_eta2 5, tau 1/5, taubar 3/5, th_s 3/8, th_u 3/2", (k1, s1, t1, tb1, th1, tu1) == (4, 5, F(1, 5), F(3, 5), F(3, 8), F(3, 2)))
vp1 = F(3, 8) ** 2 * 2 + F(3, 2) ** 2 * F(1, 4); cv1 = F(3, 8); b1 = cv1 / vp1; pv1 = 1 - b1 * cv1
check("L06 M2 Var(p)=27/32, b=4/9, post var 5/6, rho2 1/6", (vp1, b1, pv1, cv1 * cv1 / vp1) == (F(27, 32), F(4, 9), F(5, 6), F(1, 6)))
p21 = F(3, 8) * 2 - F(3, 2) * 1
Y21 = p21 / F(3, 8)
xI21 = (F(2) - 2 * p21) / 2
xU21 = (F(1, 5) * Y21 - F(6, 5) * p21) / 2
check("L06 M3 p=-3/4, x_I=7/4, x_U=1/4, clears", p21 == F(-3, 4) and xI21 == F(7, 4) and xU21 == F(1, 4) and F(1, 2) * xI21 + F(1, 2) * xU21 == 1)
# E1 hypothetical
check("L06 E1 difference 0.8-7/9 over SE 0.05 = 0.44", round((0.80 - 7 / 9) / 0.05, 2) == 0.44)
# E2 arithmetic from printed values
d = 0.426617 - 3 / 7
check("L06 E2 difference -0.001954, of tolerance -0.30, in SE -0.90", round(d, 6) == -0.001954 and round(d / 0.006497, 2) == -0.30 and round(d / (0.006497 / 3), 2) == -0.90)
# R1 limit and R2 claims are algebraic; spot-check monotonicity
mono = True
prev = None
for su2_ in [F(i, 10) for i in range(1, 30)]:
    kap = a / (lam * te)
    s_eta = se2 + kap * kap * su2_
    pvu = 1 / (tv + 1 / s_eta)
    if prev is not None and not pvu > prev:
        mono = False
    prev = pvu
check("L06 R2 posterior variance strictly increasing in sigma_u^2 (grid)", mono)

# Part E recomputation with an independent OLS
rng = random.Random(6)
N = 20000
sd_v, sd_e, sd_u = 1.0, 1.0, 0.5
ths, thu = float(thS), float(thU)
S_, P_, V_ = [], [], []
for _ in range(N):
    v = rng.gauss(0.0, sd_v)
    e = rng.gauss(0.0, sd_e)
    u = rng.gauss(0.0, sd_u)
    s = v + e
    S_.append(s); P_.append(ths * s - thu * u); V_.append(v)

def ols2(x, y):
    n = len(x)
    mx = math.fsum(x) / n
    my = math.fsum(y) / n
    sxx = math.fsum((xi - mx) ** 2 for xi in x)
    sxy = math.fsum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    b = sxy / sxx
    a0 = my - b * mx
    rss = math.fsum((yi - a0 - b * xi) ** 2 for xi, yi in zip(x, y))
    return b, math.sqrt(rss / (n - 2) / sxx)

b1_, se1_ = ols2(S_, P_)
b2_, se2_ = ols2(P_, V_)
print(f"recomputed p_on_s {b1_:.6f} tol {3*se1_:.6f} | v_on_p {b2_:.6f} tol {3*se2_:.6f}")
check("L06 Part E p_on_s printed 0.426617 tol 0.006497", f"{b1_:.6f}" == "0.426617" and f"{3*se1_:.6f}" == "0.006497")
check("L06 Part E v_on_p printed 0.761928 tol 0.023538", f"{b2_:.6f}" == "0.761928" and f"{3*se2_:.6f}" == "0.023538")
check("L06 Part E both within tolerance", abs(b1_ - 3 / 7) <= 3 * se1_ and abs(b2_ - 7 / 9) <= 3 * se2_)

print("ALL OK" if ok else "SOME FAILED")
