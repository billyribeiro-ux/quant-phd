"""Round-6 independent re-derivation of the numbers cited by LX1 cards c001-c075 (own code, not the lab twins)."""
import csv, math, random, statistics, sys
from fractions import Fraction as Fr
from decimal import Decimal, ROUND_HALF_UP
def hu(x): return int(Decimal(str(float(x))).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) if not isinstance(x, Fr) else math.floor(x + Fr(1, 2))
def r6(x): return float(Decimal(repr(x)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
base = sys.argv[1]
# L01
d1, r, g = Fr(400), Fr(9, 100), Fr(3, 100)
F0 = d1 / (r - g); q = (1 + g) / (1 + r)
print("c002 F0 exact", F0, "rounded", hu(F0), "; F2 =", float(d1*(1+g)**2/(r-g)))
print("c012 400/1.09 =", Fr(400)/Fr(109,100), "=", float(Fr(400)/Fr(109,100)), "rounded", hu(Fr(400)/Fr(109,100)), "; 40000/109 check", Fr(40000,109)==Fr(400)/Fr(109,100))
print("c003/c004 q", q, float(q), "0<q<1", 0 < q < 1)
for N in (10, 60, 200):
    S = sum(d1*(1+g)**(s-1)/(1+r)**s for s in range(1, N+1))
    print("S_%d == F0(1-q^N):" % N, S == F0*(1-q**N), "rounded", hu(S))
# c009/c010/c037-c039/c054-c058/c066/c067 via independent seeded draw
rng = random.Random(20261103); gaps = []
for t in range(13):
    w = Fr(rng.randint(-8, 25), 100)
    f = d1*(1+g)**t/(r-g); p = f*(1+w)
    gaps.append(hu(p) - hu(f))
print("c009 positive gaps (3%):", sum(x > 0 for x in gaps), "of 13")
rng = random.Random(20261103); alt = 0
for t in range(13):
    w = Fr(rng.randint(-8, 25), 100)
    p = d1*(1+g)**t/(r-g)*(1+w)
    fa = d1*(1+Fr(1,100))**t/(r-r+r-Fr(1,100)-(0)) if False else d1*(1+Fr(1,100))**t/(r-Fr(1,100))
    alt += (hu(p) - hu(fa)) > 0
print("c010 positive gaps (1%):", alt, "of 13")
print("c011 witness:", 6000 - 400/0.08, 6000 - Fr(400)/Fr(9,100)/1 if False else 6000 - float(Fr(400)/(Fr(9,100)-Fr(1,100))), 6000 - float(Fr(400)/(Fr(9,100)-Fr(3,100))))
print("c013/c005 check: S_N(0) lower bound N*d1/(1+r) at N=5:", float(5*d1/(1+r)))
# L02
D = 1_000_000; P0 = Fr(100)
rng = random.Random(20261104); P = [P0]
for _ in range(12):
    c = rng.randint(-4, 3); P.append(P[-1]*(1+Fr(c,100)))
V = [Fr(D)*P0/p for p in P]
falls = [t for t in range(1,13) if P[t] < P[t-1]]; rises = [t for t in range(1,13) if V[t] > V[t-1]]
print("c066 falls", len(falls), "rises", len(rises), "equal", falls == rises, falls)
print("c024 consecutive V all differ:", all(V[t] != V[t-1] for t in range(1,13)))
print("c025 identity all t:", all(V[t]/V[t-1] == P[t-1]/P[t] for t in range(1,13)))
print("L02 V_1 rounded", hu(V[1]), "ratio V12/V0 6dp", r6(float(V[12]/V[0])), "P12 =", float(P[12]))
print("c075/c073 n/a")
# L03
DD = Fr(1_000_000); N0 = Fr(4_000_000); delta = Fr(1,50); H = 12
def depth(m, phi=Fr(1), beta=Fr(1)):
    Vm = DD*(1-delta)**(-m); L = lambda V: V/(N0+DD-V)
    return beta*phi*(L(Vm) - L(DD))
def depth_direct(m):
    best = None
    for t in range(H+1):
        Pt = (1-delta)**min(t,m); V = DD/Pt; psi = (V/(N0+DD-V)) - (DD/N0)
        best = psi if best is None or psi > best else best
    return best
for m in (0,4,12): print("depth(%d) closed %.10f direct %.10f" % (m, float(depth(m)), float(depth_direct(m))))
print("c037 X 9.20:", round(100*float(depth(12)), 2), "c038 Y 2.69:", round(100*float(depth(4)),2), "c039 ratio 3.4260:", round(float(depth(12)/depth(4)),4))
print("c039 ratio exact", float(depth(12)/depth(4)), "phi*beta=1/2 ratio", float(depth(12,Fr(1,2))/depth(4,Fr(1,2))), "phi=3", float(depth(12,Fr(3))/depth(4,Fr(3))))
print("c035 depth(4)<depth(12):", depth(4) < depth(12))
_D=Fr(1_000_000); _N0=Fr(4_000_000); _d=Fr(1,50); _ell=lambda V: V/(_N0+_D-V)
print("c036 ratio formula equal (Fractions):", depth(12)/depth(4) == (_ell(_D*(1-_d)**-12)-_ell(_D))/(_ell(_D*(1-_d)**-4)-_ell(_D)))
print("c031/c033 depth(m) monotone, first max at m:", all(depth(m) < depth(m+1) for m in range(12)))
print("c046 9.20 is beta*phi*...; c035 X>Y", depth(12) > depth(4))
print("c044/c043 n/a; c047 n/a")
print("L03 V_12 exact", float(DD*(1-delta)**-12), "V_4 exact", float(DD*(1-delta)**-4))
# L04
rows = list(csv.DictReader(open(f"{base}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="")))
print("fx_monthly columns", list(rows[0].keys())[:12], "n", len(rows), rows[0]["month"], rows[-1]["month"])
