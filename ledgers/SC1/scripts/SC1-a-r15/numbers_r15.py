"""Round-15 recomputation of the prose numbers in SC1 slice a (L01-L03, index).

Recomputes from the twin code (imported by path, not re-typed) and from closed forms.
Usage: python3 -I numbers_r15.py <checkout-root>
"""
import importlib.util
import itertools
import math
import sys
from fractions import Fraction

root = sys.argv[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        spec.loader.exec_module(mod)  # runs main() at import
    return mod, buf.getvalue()


# ---- L02: unrounded level-1 sup, bounds, sums ----
l2, _ = load(root + "/tests/labs/SC1/lab-SC1-L02-1.py", "l2")
import random
rng = random.Random(l2.SEED)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, l2.LEVELS + 1)]
sup1 = l2.level_term_sup(coeffs[0], 1)
print(f"L02 unrounded level-1 sup = {sup1!r}; rounded {sup1:.6f}; 2*sup = {2*sup1:.7f}; "
      f"|xi11| = {abs(coeffs[0][0])!r}")
print(f"L02 2*printed(0.116589) = {2*0.116589:.6f}; rounds of 2*sup to 6dp: {round(2*sup1, 6)}")
print(f"L02 sqrt(4 log 2) = {math.sqrt(4*math.log(2)):.6f}; half = {math.sqrt(4*math.log(2))/2:.6f}")
bounds = [l2.bound(m) for m in range(1, 9)]
print("L02 bounds:", [f"{b:.6f}" for b in bounds])
print(f"L02 sum bounds 5..8 = {sum(bounds[4:]):.6f}")
# M_m closed form check: sqrt(2 log 2) sqrt(m) 2^{-m/2} == lambda_m 2^{-(m+1)/2}
print("L02 M_m identity max err:", max(abs(math.sqrt(2*math.log(2))*math.sqrt(m)*2**(-m/2) - l2.bound(m)) for m in range(1, 60)))
print(f"L02 sum_m m r^m (r=2^-1/2) = {sum(m*(2**-0.5)**m for m in range(1, 400)):.6f}; r/(1-r)^2 = {(2**-0.5)/(1-2**-0.5)**2:.6f}")
print(f"L02 tail bound: sqrt(2log2)*sum m r^m = {math.sqrt(2*math.log(2))*sum(m*(2**-0.5)**m for m in range(1,400)):.6f}")

# ---- L02 Lemma 2.3 variance arithmetic for n=0..3 ----
for n in range(4):
    c2 = 2 ** (-(n + 2))
    var_u = 0.25 * 2 ** (-n) + c2
    print(f"L02 Var(U) n={n}: {var_u!r} == 2^-(n+1) {2**-(n+1)!r}: {var_u == 2**-(n+1)}")

# ---- L02 counts: dyadic points and cases ----
cases = sum((2**n + 1) * (8 - n + 1) for n in range(5))
pairs = sum(2**n + 1 for n in range(5))
print(f"L02 dyadic cases {cases}, points {pairs}, per depth {[2**n+1 for n in range(5)]}")

# ---- L03: z, se gaps from printed values (mean, se from the expected block) ----
txt = open(root + "/course/modules/SC/SC1/L03.html", encoding="utf-8").read()
import re
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', txt, re.S).group(1).splitlines()
rows = []
H = None
for line in exp:
    mh = re.match(r"H = (\d+): mean", line)
    if mh:
        H = float(mh.group(1))
        continue
    mm = re.match(r"\s+N =\s*(\d+) steps: mean ([\d.]+), se ([\d.]+), z = (-?[\d.]+)", line)
    if mm:
        rows.append((H, int(mm.group(1)), float(mm.group(2)), float(mm.group(3)), float(mm.group(4))))
print("L03 rows parsed:", len(rows))
zs = sorted(rows, key=lambda r: -abs(r[4]))
print("L03 top |z|:", [(r[0], r[1], r[4]) for r in zs[:3]])
gaps = []
for H_, N, mean, se, z in rows:
    theo = H_ * math.sqrt(2 / N) / 20
    gaps.append((abs(se / theo - 1), H_, N, se, theo))
gaps.sort(reverse=True)
print("L03 largest |gap|:", [(f"{g:.4%}", H_, N, se, f"{th:.6f}") for g, H_, N, se, th in gaps[:3]])
print("L03 |z|>3 count:", sum(1 for r in rows if abs(r[4]) > 3), "; z recomputed from printed mean/se:",
      max(abs((r[2]-r[0])/r[3] - r[4]) for r in rows) <= 0.01 + 1e-9)
print("L03 H=2,N=1 gap:", 0.1601 / (2 * math.sqrt(2) / 20) - 1)
print("L03 H=2 N=128 theo se:", 2 * math.sqrt(2/128) / 20, " H=1 N=1 theo:", math.sqrt(2)/20)
print("L03 E2 16*255/1536 =", 16*255/1536, "; 2^4*255/(3*512) =", 2**4*255/(3*512))
print("L03 quiz H=1,N=2 =", Fraction(1)*(4*4-1)/(3*8), float(Fraction(1)*(4*4-1)/(3*8)))
print("L03 exact sums:", [float(l3) for l3 in []])

# ---- L03 Prop 2.4(b) exact sums and closed forms for all (H,N) cells ----
l3, _ = load(root + "/tests/labs/SC1/lab-SC1-L03-1.py", "l3")
bad = 0
for H_ in (Fraction(1), Fraction(2)):
    for k in range(8):
        N = 2**k
        s = l3.t_squared_sum(H_, N)
        if s != l3.t_squared_closed_form(H_, N):
            bad += 1
print("L03 closed-form mismatches over 16 cells:", bad)
print("L03 M1 two-step: E[Q]=", 2*Fraction(1,2), " Var(Q)=", 2*2*Fraction(1,2)**2)

# ---- L03 misconception: E|Z| and sum of absolute increments ----
print("L03 sqrt(2/pi) =", math.sqrt(2/math.pi), "; 2 phi(0) =", 2/math.sqrt(2*math.pi))
print("L03 E|Z| numeric by quadrature:", sum(abs(x)*math.exp(-x*x/2)/math.sqrt(2*math.pi)*1e-4 for x in [(i+0.5)*1e-4 - 10 for i in range(200000)]))

# ---- L03 canon: equal-steps Var = 2 H^2/N and SE claim H sqrt(2/N)/20 ----
print("L03 R2 equal partition: sum Delta^2 = t|P| :", all(abs(N*(1/N)**2 - (1/N)*1.0) < 1e-15 for N in range(1, 50)))

# ---- Index rung-2 walk count: paths of n=6 steps whose max reaches a=2 ----
cnt = 0
for steps in itertools.product((-1, 1), repeat=6):
    s = 0
    mx = 0
    for e in steps:
        s += e
        mx = max(mx, s)
    cnt += mx >= 2
print("Index rung-2 n=6 a=2 reach count:", cnt)
cnt2 = 0
for steps in itertools.product((-1, 1), repeat=2):
    s = 0
    mx = 0
    for e in steps:
        s += e
        mx = max(mx, s)
    cnt2 += mx >= 1
print("Index placement n=2 a=1 reach count:", cnt2)

# ---- Placement arithmetic ----
print("placement 7/9 =", 7/9*100, " 8/9 =", 8/9*100)
# ---- hours ----
print("hours split", 72/100*100, 28/100*100, "lesson sum", 8*9)
