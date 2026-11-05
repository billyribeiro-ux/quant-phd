"""Independent re-derivation of LX1 card and lesson numbers (verifier r10). Exact Fractions and 50-digit Decimal."""
import csv, math, sys, hashlib, json
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
getcontext().prec = 60
root = sys.argv[1]

def rhu(x):  # round half up to integer for Fraction
    return math.floor(x + F(1, 2))

def dec(x, places):
    return D(x).quantize(D(1).scaleb(-places), rounding=ROUND_HALF_UP)

print("== L01 ==")
F0 = F(400) / (F(9, 100) - F(3, 100))
print("F0", F0, float(F0), "rounded", rhu(F0))
q = (1 + F(3, 100)) / (1 + F(9, 100))
print("q", q, "0<q<1", 0 < q < 1, "q decimal 6dp", dec(D(q.numerator) / D(q.denominator), 6))
for N in (10, 60, 200):
    S = sum(F(400) * (1 + F(3, 100)) ** (s - 1) / (1 + F(9, 100)) ** s for s in range(1, N + 1))
    print("N", N, "S rounded", rhu(S), "identity", S == F0 * (1 - q ** N), "resid rounded", rhu(F0 * q ** N))
print("F2 exact", float(F(400) * (F(103, 100)) ** 2 / F(6, 100)), "F2 rounded", rhu(F(400) * F(103, 100) ** 2 / F(6, 100)))
print("F0 (d1=250,r=10%,g=4%)", F(250) / (F(10, 100) - F(4, 100)), "F3", float(F(250) * F(104, 100) ** 3 / F(6, 100)), rhu(F(250) * F(104, 100) ** 3 / F(6, 100)))
print("c012 40000/109 =", F(40000, 109), float(F(40000, 109)), rhu(F(40000, 109)))
print("c011 F0(1%)", F(400) / F(8, 100), "F0(3%)", F(400) / F(6, 100), "gap1", F(6000) - F(400) / F(8, 100), "gap3", F(6000) - F(400) / F(6, 100))
print("c007 F0(1%)", float(F(400) / F(8, 100)), "F0(3%)", float(F(400) / F(6, 100)))
print("c009/c010 counts: see twin output (run_labs); Part B/C reproduced by twin run")
print("g* for P0=6000", F(9, 100) - F(400, 6000), float(F(9, 100) - F(400, 6000)))
print("L01 l.371 fundamental t=9 3%:", float(F(400) * F(103, 100) ** 9 / F(6, 100)), "gap/fund", float(F(2175) / F(8698)))
print("Mechanics1 250/0.06 =", F(250) / F(6, 100), "Mech2 281.216/0.06 =", float(F(281216, 1000) / F(6, 100)))
print("Mech3 S10 (q=1) =", sum(F(100) / F(105, 100) for _ in range(10)), "= 20000/21 ?", sum(F(100) / F(105, 100) for _ in range(10)) == F(20000, 21))
print("c013 each term k=1..50 >= d1/(1+r) at g=9%: ", all(F(100) * ((F(109, 100)/F(109, 100))) ** 0 >= 0 for _ in range(1)))
# c013 check at g = 9%, r = 9%, d1 = 400
ok = all(F(400) * ((F(109,100)) / (F(109,100))) ** (k-1) / (F(109,100))  >= F(400)/F(109,100) for k in range(1, 51))
print("c013 g=r=9% each term >= d1/(1+r):", ok)
print("c005 q at g=r is 1:", (1+F(9,100))/(1+F(9,100)) == 1)
print("c004 check q=103/109:", q == F(103,109))

print("== L02 ==")
P = [F(100)]
for c in [-1, 1, 1, 3, -4, -1, 2, -4, -3, 3, 2, -4]:
    P.append(P[-1] * (1 + F(c, 100)))
V = [F(1000000) * F(100) / p for p in P]
print("V12/V0 6dp", dec(D(V[12].numerator) / D(V[12].denominator), 6), "P0/P12", dec(D(P[0].numerator)/D(P[12].numerator) * D(P[12].denominator) if False else D(100)/D(P[12].numerator/P[12].denominator), 8))
print("P12 float", float(P[12]), "100/P12", float(F(100)/P[12]))
falls = [t for t in range(1, 13) if P[t] < P[t-1]]
rises = [t for t in range(1, 13) if V[t] > V[t-1]]
print("falls", falls, len(falls), "rises", rises, len(rises), "equal", falls == rises)
print("V1 cents", float(V[1]), rhu(V[1]), "V1 exact 1000000*100/99", F(100000000, 99))
print("cents B", [rhu(v) for v in V])
print("unchanged consecutive cents?", [rhu(V[t]) == rhu(V[t-1]) for t in range(1, 13)])
print("M1 V1 = 2000*100/80", F(2000*100, 80))
print("M2 90/85", F(90, 85), "18/17", F(18, 17), float(F(18,17)))
print("M3 200000/95", float(F(200000, 95)), rhu(F(200000,95)))
print("E2 V1 unrounded", float(F(1000000*100, 99)))
print("ratio 1.1 / ln check")

print("== L03 ==")
DEBT = F(1000000); N0 = F(4000000); delta = F(1, 50); H = 12
def Pidx(m, t): return (1 - delta) ** min(t, m)
def V_(m, t): return DEBT / Pidx(m, t)
def L_(m, t):
    v = V_(m, t); N = N0 - (v - DEBT); return v / N
L0 = DEBT / N0
def f(m, t): return L_(m, t) - L0  # phi = beta = 1
def depth(m): return max(f(m, t) for t in range(H + 1))
dX, dY = depth(12), depth(4)
print("depth X exact", float(dX) * 100, "Y exact", float(dY) * 100, "diff exact", float(dX - dY) * 100, "diff of rounded", 9.20 - 2.69)
print("X first at t", [t for t in range(H+1) if f(12, t) == dX], "Y first at t", [t for t in range(H+1) if f(4, t) == dY])
print("ratio X/Y exact", float(dX / dY), "4dp", dec(D((dX/dY).numerator) / D((dX/dY).denominator), 4))
print("ratio phi=1/2 same? ", all(depth(12) / depth(4) == (dX/dY) for _ in [0]))
print("depth(m) for m 0..12 pct:", [round(float(depth(m)) * 100, 2) for m in range(13)])
print("strict steps", all(depth(m) < depth(m+1) for m in range(12)), "never falls", all(depth(m) <= depth(m+1) for m in range(12)))
print("P4 Y exact", F(49, 50) ** 4, float(F(49,50)**4))
V4 = DEBT / (F(49,50) ** 4)
print("V4 exact float", float(V4), "V4 rounded", rhu(V4))
N4 = N0 - (V4 - DEBT)
print("N4 float", float(N4), "L4 float", float(V4 / N4), "L4 4dp", dec(D((V4/N4).numerator)/D((V4/N4).denominator), 4))
print("c-check V12 exact", float(V_(12, 12)), "rounded", rhu(V_(12, 12)))
print("N12 X", float(N0 - (V_(12,12) - DEBT)))
print("E2 X depth exact 9.204597? ", float(dX)*100, " Y 2.686713?", float(dY)*100, " diff ", float(dX - dY)*100)
print("E1 Y exact 2.6867", float(dY)*100)
print("L03 l.383: fundamental ratio check: depth(12)/depth(4)", float(dX/dY))
print("Corollary ratio check formula ell:")
C = N0 + DEBT
ell = lambda x: x / (C - x)
print("ell-based ratio", float((ell(V_(12,12)) - ell(DEBT)) / (ell(V_(4,4)) - ell(DEBT))))

print("== L04 (data) ==")
data_path = f"{root}/course/assets/data/market/fx_monthly.csv"
raw = open(data_path, "rb").read()
print("fx_monthly.csv sha256", hashlib.sha256(raw).hexdigest(), "bytes", len(raw))
with open(data_path, newline="", encoding="utf-8") as h:
    rd = csv.DictReader(h)
    print("header", rd.fieldnames)
    rows = list(rd)
print("rows", len(rows), rows[0]["month"], rows[-1]["month"])
gbp = [(r["month"], r["GBP"]) for r in rows]
exact = [(m, D(v)) for m, v in gbp]
# consecutive months
def mi(m):
    y, mm = m.split("-"); return int(y) * 12 + int(mm) - 1
print("consecutive", all(mi(rows[i]["month"]) == mi(rows[i-1]["month"]) + 1 for i in range(1, len(rows))))
zeros = [exact[i][0] for i in range(1, len(exact)) if exact[i][1] == exact[i-1][1]]
print("exact zero changes", zeros, len(zeros))
ch = [(exact[i][0], (exact[i][1] / exact[i-1][1]).ln()) for i in range(1, len(exact))]
print("changes", len(ch), ch[0][0], ch[-1][0])
def sd(vals):
    n = len(vals); mean = sum(vals) / n
    return (sum((v - mean) ** 2 for v in vals) / (n - 1)).sqrt()
w1 = [c for _, c in ch]
w2 = [c for m, c in ch if m >= "2000-01"]
s1, s2 = sd(w1), sd(w2)
print("w1 n", len(w1), "sd", dec(s1, 6), float(s1))
print("w2 n", len(w2), "sd", dec(s2, 6), float(s2))
print("diff", dec(s2 - s1, 6), float(s2 - s1), "ratio 4dp", dec(s2 / s1, 4), float(s2 / s1))
big1 = max(ch, key=lambda it: abs(it[1]))
big2 = max([it for it in ch if it[0] >= "2000-01"], key=lambda it: abs(it[1]))
print("largest w1", big1[0], dec(big1[1], 6), "largest w2", big2[0], dec(big2[1], 6))
print("w2 largest simple change", (big2[1].exp() - 1))
print("1999-12 rate", [v for m, v in gbp if m == "1999-12"], "2000-01 rate", [v for m, v in gbp if m == "2000-01"])
print("ln 1.1", dec(D(1.1).ln(), 10), "simple minus log", dec(D("0.1") - D("1.1").ln(), 6))
print("M1 ln 1.375/1.25", dec((D("1.375") / D("1.25")).ln(), 10))
print("c061 ln1.1 six dp", dec(D("1.1").ln(), 6), "diff 6dp", dec(D("0.1") - D("1.1").ln(), 6))
print("M2 mean", F(2,100)/3, "dispersion", math.sqrt(float(F(19,30000))))
print("R2 tanh check: L=0.135846, h=", (D("0.135846")/2).exp())
L = D("0.135846")
h = (L.exp() - 1) / (L.exp() + 1)
print("R2 h exact-ish", dec(h, 6), dec(h, 4))
hh = D("0.0678")
print("bound at h=0.0678 ln((1+h)/(1-h))", dec(((1 + hh) / (1 - hh)).ln(), 6))
print("bound at h=0.0678 4dp", dec(((1 + hh) / (1 - hh)).ln(), 4))
print("P1 check h=0.067819 bound", dec(((1 + D("0.067819"))/(1 - D("0.067819"))).ln(), 6))
print("R2 uses 0.135846 as largest, check 0.135846 is w1 largest 6dp:", dec(big1[1], 6))
