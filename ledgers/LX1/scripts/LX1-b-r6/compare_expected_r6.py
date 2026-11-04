# Compare the page's L03 expected block with the independent Fraction recomputation (own code, no twin import).
import re, html, math, subprocess
from fractions import Fraction as F
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE6-LX1-b"
src = html.unescape(open(f"{ROOT}/course/modules/LX/LX1/L03.html", encoding="utf-8").read())
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1).split("\n")
D, N0, DELTA, H = 1_000_000, 4_000_000, F(1, 50), 12
def hu(x, p):
    n = math.floor(x * 10**p + F(1, 2)); w, fr = divmod(n, 10**p); return f"{w}.{fr:0{p}d}"
def hi(x): return math.floor(x + F(1, 2))
def P(m, t): return (1 - DELTA) ** min(t, m)
def V(m, t): return F(D) / P(m, t)
def L(m, t):
    v = V(m, t); return v / (N0 - (v - D))
L0 = F(D, N0)
mine = ["Part A: SIMULATED model, parameters and paths",
        f"D = {D} cents; N_0 = {N0} cents; deflation per period on parity = 1/50; H = {H} periods; phi = 1; beta = 1",
        f"baseline leverage L_0 = V_0 / N_0 = {hu(L0,4)}"]
for lab, m in (("X", 12), ("Y", 4)):
    mine.append(f"economy {lab}, parity held for {m} of {H} periods:")
    for t in range(H + 1):
        f = L(m, t) - L0
        mine.append(f"  t = {t:2d}: index {hu(P(m,t),4)}; real debt {hi(V(m,t))} cents; leverage {hu(L(m,t),4)}; premium {hu(f,4)}; output fall {hu(100*f,2)} percent")
dep = {m: max(L(m, t) - L0 for t in range(H + 1)) for m in range(H + 1)}
first = {m: next(t for t in range(H + 1) if (L(m, t) - L0) == dep[m]) for m in (4, 12)}
mine.append("Part B: output depth of each economy")
mine.append(f"economy X depth {hu(100*dep[12],2)} percent of baseline output, first reached at t = {first[12]}")
mine.append(f"economy Y depth {hu(100*dep[4],2)} percent of baseline output, first reached at t = {first[4]}")
mine.append(f"X is deeper than Y: {dep[12] > dep[4]}")
mine.append(f"difference X minus Y: {hu(100*(dep[12]-dep[4]),2)} percentage points")
mine.append("Part C: depth by parity duration m, in percent of baseline output")
for m in range(H + 1):
    mine.append(f"m = {m:2d}: depth {hu(100*dep[m],2)} percent")
mine.append(f"depth never falls as the parity duration rises: {all(dep[m] <= dep[m+1] for m in range(H))}")
mine.append(f"depth rises at every step from m to m + 1 for m = 0 to {H-1}: {all(dep[m] < dep[m+1] for m in range(H))}")
mine.append("Part D: the ratio of the two depths does not depend on the product beta * phi")
for ph, lab in ((F(1,2), "1/2"), (F(1), "1"), (F(3), "3")):
    mine.append(f"phi = {lab}, beta = 1, product {lab}: ratio of depths X to Y {hu(dep[12]/dep[4],4)}")
print("lines page", len(exp), "lines mine", len(mine))
mism = [(i, a, b) for i, (a, b) in enumerate(zip(exp, mine)) if a != b]
print("mismatches", len(mism))
for x in mism[:10]: print(x)
