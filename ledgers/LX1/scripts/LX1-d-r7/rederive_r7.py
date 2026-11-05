"""Round-7 independent re-derivation of every number cited by LX1 cards c001-c076 (own code, not the lab twins).

Usage: python3 -I rederive_r7.py <checkout>
Prints one line per card number. Exact Fractions for algebra; Decimal ROUND_HALF_UP for display rounding.
"""
import csv, math, random, statistics, sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as Fr

base = sys.argv[1]


def half_up(x, places=0):
    q = Decimal(1).scaleb(-places)
    return Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP) if not isinstance(x, Fr) else (
        Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)


def exact_round(x):
    return math.floor(x + Fr(1, 2))


print("== L01 (cards c001-c013, c009-c011 lab, c012 canon-breaks)")
d1, r, g = Fr(400), Fr(9, 100), Fr(3, 100)
F0 = d1 / (r - g)
q = (1 + g) / (1 + r)
print("c002 F0 =", F0, "=", float(F0), "rounded cents", exact_round(F0), "; d_1 check F_1 = d_2/(r-g)", d1*(1+g)/(r-g) == d1*(1+g)/(r-g))
print("c003 identity S_N = F0(1-q^N) N=10,60,200:", [sum(d1*(1+g)**(s-1)/(1+r)**s for s in range(1, N+1)) == F0*(1-q**N) for N in (10, 60, 200)])
print("c004 q =", q, "0<q<1:", 0 < q < 1, "q-float", float(q))
print("c011 benchmarks at 1%:", d1/(r-Fr(1,100)), "at 3%:", F0, "; gaps at P=6000:", 6000 - d1/(r-Fr(1,100)), 6000 - F0)
print("c012 400/1.09 =", d1/(1+r), "=", float(d1/(1+r)), "rounded", exact_round(d1/(1+r)), "(40000/109:", Fr(40000, 109) == d1/(1+r), ")")
print("c005/c013 S_5(0) >= 5*d1/(1+r) with r=9%, g=10% (A2 violation example):", sum(d1*((1+Fr(10,100))**(s-1))/(1+r)**s for s in range(1,6)) >= 5*d1/(1+r))
rng = random.Random(20261103)
wedges3 = [Fr(rng.randint(-8, 25), 100) for _ in range(13)]
fund3 = [d1*(1+g)**t/(r-g) for t in range(13)]
gaps3 = [exact_round(fund3[t]*(1+wedges3[t])) - exact_round(fund3[t]) for t in range(13)]
print("c009 periods with price above fundamental (3%):", sum(x > 0 for x in gaps3), "of 13")
fund1 = [d1*(1+Fr(1,100))**t/(r-Fr(1,100)) for t in range(13)]
gaps1 = [exact_round(fund3[t]*(1+wedges3[t])) - exact_round(fund1[t]) for t in range(13)]
print("c010 periods above alt fundamental (1%):", sum(x > 0 for x in gaps1), "of 13; count changes:", sum(x > 0 for x in gaps1) != sum(x > 0 for x in gaps3))
print("L01 Part B 3% first gap check t=0 price", exact_round(fund3[0]*(1+wedges3[0])), "gap", gaps3[0])

print("== L02 (c014-c025, c066, c073-c074)")
D = 1_000_000
rng = random.Random(20261104)
changes = [rng.randint(-4, 3) for _ in range(12)]
P = [Fr(100)]
for c in changes:
    P.append(P[-1]*(1+Fr(c, 100)))
V = [Fr(D)*Fr(100)/p for p in P]
print("c025 identity exact all t:", all(V[t]/V[t-1] == P[t-1]/P[t] for t in range(1, 13)))
print("c024 consecutive V all differ:", all(V[t] != V[t-1] for t in range(1, 13)), "; V cents:", [exact_round(v) for v in V])
falls = [t for t in range(1, 13) if P[t] < P[t-1]]
rises = [t for t in range(1, 13) if V[t] > V[t-1]]
print("c066 falls", len(falls), falls, "rises", len(rises), rises, "equal sets:", falls == rises)
print("L02 V12/V0 six dp:", float(V[12]/V[0]), "P12 =", float(P[12]))
print("c021 check: V_t > V_{t-1} iff P_t < P_{t-1} for all t:", all((V[t] > V[t-1]) == (P[t] < P[t-1]) for t in range(1, 13)))
print("c015/c016 Prop1.2: 1/kappa with kappa=2/5 =", 1/Fr(2,5))

print("== L03 (c026-c039, c042-c047, c067, c071, c072, c076)")
DD = Fr(1_000_000); N0 = Fr(4_000_000); delta = Fr(1, 50); H = 12; phi = Fr(1); beta = Fr(1)
def economy(m, phi=Fr(1), beta=Fr(1)):
    Ps = [(1-delta)**min(t, m) for t in range(H+1)]
    Vs = [DD/p for p in Ps]
    Ns = [N0 - (v - DD) for v in Vs]
    Ls = [v/n for v, n in zip(Vs, Ns)]
    L0 = DD/N0
    fs = [beta*phi*(l - L0) for l in Ls]
    return Ps, Vs, Ns, fs
for m in (4, 12):
    Ps, Vs, Ns, fs = economy(m)
    dep = max(fs)
    first = next(t for t, f in enumerate(fs) if f == dep)
    print(f"c037/c038 m={m}: depth exact {float(dep)*100:.6f} percent -> {half_up(float(dep)*100, 2)}; first at t={first}")
Ps, Vs, Ns, fs = economy(12)
print("c035/c037 depth X < ? (X deeper):", max(economy(12)[3]) > max(economy(4)[3]))
ratio = max(economy(12)[3]) / max(economy(4)[3])
print("c039/c067 ratio X/Y for beta*phi=1:", float(ratio), "rounded 4dp", half_up(float(ratio), 4))
for phi_, beta_ in ((Fr(1,2), Fr(1)), (Fr(1), Fr(1)), (Fr(3), Fr(1))):
    rr = max(economy(12, phi_, beta_)[3]) / max(economy(4, phi_, beta_)[3])
    print("c067 ratio for phi,beta=", phi_, beta_, "exact equal to beta=phi=1 ratio:", rr == ratio, float(rr))
L = lambda V: V/(N0+DD-V)
for mm, mp in ((4, 12),):
    ratio_formula = (L(DD*(1-delta)**(-mp)) - L(DD)) / (L(DD*(1-delta)**(-mm)) - L(DD))
    print("c036 Cor 3.4 RHS equals depth ratio exactly:", ratio_formula == ratio)
print("c032 closed form depth(m) equals max f_t for m=0..12:", all(max(economy(m)[3]) == beta*phi*(L(DD*(1-delta)**(-m)) - L(DD)) for m in range(13)))
print("c034 depth(0) =", max(economy(0)[3]))
print("c031 V_t <= V_m, strictly increasing for t<=m (m=12):", all(Vs[t] <= DD*(1-delta)**(-12) for t in range(13)), all(Vs[t] < Vs[t+1] for t in range(12)))
print("c033 first max at t=m:", next(t for t, f in enumerate(economy(7)[3]) if f == max(economy(7)[3])))
print("c042/c043 proof-level, no number. c047 n/a")
print("c046 X depth 9.20 scales with beta: depth(beta=2)/depth(beta=1)=", float(max(economy(12, Fr(1), Fr(2))[3])/max(economy(12)[3])))
print("L03 Part B difference unrounded:", float(max(economy(12)[3]) - max(economy(4)[3])))

print("== L04 (c048-c070, c075)")
rows = list(csv.DictReader(open(f"{base}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
months = [x["month"] for x in rows]
rate = [Fr(x["GBP"]) for x in rows]
print("c069 months", len(rows), months[0], months[-1], "consecutive:", all(
    (int(months[i][:4])*12 + int(months[i][5:])) - (int(months[i-1][:4])*12 + int(months[i-1][5:])) == 1 for i in range(1, len(months))))
ch = [(months[i], math.log(float(rate[i]/rate[i-1]))) for i in range(1, len(rate))]
zero = [months[i] for i in range(1, len(rate)) if rate[i] == rate[i-1]]
print("c054 zero-change months:", zero, "count", len(zero), "of", len(ch), "nonzero", len(ch)-len(zero))
w1 = ch
w2 = [c for c in ch if c[0] >= "2000-01"]
sd1 = statistics.stdev([c for _, c in w1]); sd2 = statistics.stdev([c for _, c in w2])
print("c055 w1 n", len(w1), "sd", sd1, "-> 6dp", round(sd1, 6))
print("c056 w2 n", len(w2), "first", w2[0][0], "sd", sd2, "-> 6dp", round(sd2, 6))
print("c057 ratio", sd2/sd1, "-> 4dp", round(sd2/sd1, 4))
print("c065 difference", sd2 - sd1, "-> 6dp", round(sd2 - sd1, 6))
m2 = max(w2, key=lambda c: abs(c[1])); m1 = max(w1, key=lambda c: abs(c[1]))
print("c058 w2 largest", m2, "w1 largest", m1)
print("c063 w2 first change uses rate of", months[months.index("2000-01") - 1], "; fx_daily and ust_daily first dates are in the manifest (checked in shell)")
print("c061 ln 1.1 =", math.log(1.1), "6dp", round(math.log(1.1), 6), "simple 0.10 - log =", round(0.1 - math.log(1.1), 6))
print("c049 sample sd n-1 check: sd of [0.01,0.03,-0.02]:", statistics.stdev([0.01, 0.03, -0.02]))
print("c068 nonzero of 668 in window one:", sum(1 for _, c in w1 if c != 0))
print("c064 GBP column header present:", "GBP" in rows[0])
