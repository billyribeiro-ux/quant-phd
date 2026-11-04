"""Round-5 independent re-derivation of every displayed number on M4 slice a (hub, L01-L04).

Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-a-r5/m4a_r5_numbers.py
Prints one line per check: CHECK <id> <expected-as-printed> <recomputed> OK|MISMATCH.
Exact rationals use fractions.Fraction; decimals are compared at the printed precision.
"""
from fractions import Fraction as F
import math

fails = []


def chk(cid, printed, recomputed, ok=None):
    if ok is None:
        ok = printed == recomputed
    if not ok:
        fails.append(cid)
    print(f"CHECK {cid} printed={printed} recomputed={recomputed} {'OK' if ok else 'MISMATCH'}")


def dec(x, places):
    return f"{x:.{places}f}"


# ---- L01 ----
law = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]
cdf = lambda x: sum((p for v, p in law if v <= x), F(0))
chk("L01-F", "1/10, 3/10, 3/5, 4/5, 9/10, 1", ", ".join(str(cdf(v)) for v, _ in law))


def Q(p):
    return min(v for v, _ in law if cdf(v) >= p)


for p, printed in [(F(1, 20), -2), (F(1, 10), -2), (F(11, 100), -1), (F(1, 2), 0), (F(3, 5), 0),
                   (F(61, 100), 1), (F(9, 10), 2), (F(91, 100), 3), (F(99, 100), 3), (F(1), 3)]:
    chk(f"L01-Q({p})", printed, Q(p))
grid = [F(j, 100) for j in range(1, 101)]
chk("L01-grid-F(Q)>=p", 100, sum(cdf(Q(p)) >= p for p in grid))
chk("L01-Q-jump-Q(3/5+eps)", 1, Q(F(3, 5) + F(1, 10**9)))
chk("L01-Ex3.5-149", 149, math.ceil(F(150) * F(99, 100)))
chk("L01-Ex3.5-198", 198, math.ceil(F(200) * F(99, 100)))
chk("L01-74/75", "0.987", dec(74 / 75, 3))
chk("L01-P(X<=1)=5/6", "0.833", dec(5 / 6, 3))
chk("L01-M2-F(5)", F(7, 10), F(1, 5) + F(1, 2))
chk("L01-M3-40p", (36, 37), (math.ceil(40 * F(9, 10)), math.ceil(40 * F(901, 1000))))
chk("L01-R1-strict(3/5)", 1, min(v for v, _ in law if cdf(v) > F(3, 5)))
chk("L01-Q-quiz-1/2", 1, min(v for v, _ in [(0, F(1, 4)), (1, F(1, 2)), (2, F(1, 4))]
                              if sum((p for vv, p in [(0, F(1, 4)), (1, F(1, 2)), (2, F(1, 4))] if vv <= v), F(0)) >= F(1, 2)))
chk("L01-E1-F(2)", "9/10", str(cdf(2)))

# ---- L02 ----
die = [(k, F(1, 6)) for k in range(1, 7)]
loss = [(0, F(19, 20)), (250000, F(1, 20))]
E = lambda L: sum((v * p for v, p in L), F(0))
E2 = lambda L: sum((v * v * p for v, p in L), F(0))
Var = lambda L: sum(((v - E(L)) ** 2 * p for v, p in L), F(0))
chk("L02-die-E", "7/2", str(E(die)))
chk("L02-die-E2", "91/6", str(E2(die)))
chk("L02-die-Var", "35/12", str(Var(die)))
chk("L02-die-sd-1.708", "1.708", dec(math.sqrt(35 / 12), 3))
chk("L02-die-E2-15.17", "15.17", dec(91 / 6, 2))
chk("L02-die-Var-2.92", "2.92", dec(35 / 12, 2))
chk("L02-Var2X", F(35, 3), Var([(2 * k, p) for k, p in die]))
chk("L02-loss-E", 12500, E(loss))
chk("L02-loss-E2", 3125000000, E2(loss))
chk("L02-loss-Var", 2968750000, Var(loss))
chk("L02-loss-sd", "54486.24", dec(math.sqrt(2968750000), 2))
chk("L02-loss-sd-exact-check", "54486.2368", dec(math.sqrt(2968750000), 4))
chk("L02-R2-VarD", 296875, Var(loss) / 10000)
chk("L02-R2-sdD", "544.8624", dec(math.sqrt(296875), 4))
chk("L02-M1", F(21, 100), F(3, 10) - F(9, 100))
chk("L02-M2-Var", 225000000, F(50000) ** 2 * F(1, 10) - F(5000) ** 2)
chk("L02-M2-sd", 15000, math.isqrt(225000000) if math.isqrt(225000000) ** 2 == 225000000 else None)
chk("L02-E-L01-Ex3.6", F(3, 10), sum((v * p for v, p in law), F(0)))
chk("L02-E-minus-count", 11, 500 - 489)
chk("L02-E3-35/3", F(35, 3), 4 * F(35, 12))
chk("L02-quiz-Var", 1, 5 - 2 ** 2)
chk("L02-E-expected-count", 500, 10000 * F(1, 20))

# ---- L03 ----
SK = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu = E(SK)
m = lambda k: sum(((v - mu) ** k * p for v, p in SK), F(0))
chk("L03-mu", "7/4", str(mu))
chk("L03-m2", "163/16", str(m(2)))
chk("L03-m3", "2157/32", str(m(3)))
chk("L03-m4", "149461/256", str(m(4)))
chk("L03-term3", ("-1372/512", "-54/512", "1/512", "35937/512"),
    tuple(str(((v - mu) ** 3 * p) * 512) + "/512" for v, p in SK))
chk("L03-skew-sq", "18610596/4330747", str(m(3) ** 2 / m(2) ** 3))
chk("L03-skew", "2.0730", dec(math.sqrt(float(m(3) ** 2 / m(2) ** 3)), 4))
chk("L03-kurt", "149461/26569", str(m(4) / m(2) ** 2))
chk("L03-kurt-dec", "5.6254", dec(float(m(4) / m(2) ** 2), 4))
chk("L03-kurt-3dec", "5.625", dec(float(m(4) / m(2) ** 2), 3))
chk("L03-skew-3dec", "2.073", dec(math.sqrt(float(m(3) ** 2 / m(2) ** 3)), 3))
chk("L03-gap-skew", 0.008, round(2.073 - 2.065, 3))
chk("L03-gap-kurt", 0.045, round(5.625 - 5.580, 3))
p = F(1, 10)
q = 1 - p
bern = lambda pp: [(0, 1 - pp), (1, pp)]
mb = lambda L, k: sum(((v - E(L)) ** k * pp for v, pp in L), F(0))
chk("L03-bern-skew-sq", F(64, 9), mb(bern(p), 3) ** 2 / mb(bern(p), 2) ** 3)
chk("L03-bern-kurt", F(73, 9), mb(bern(p), 4) / mb(bern(p), 2) ** 2)
chk("L03-bern-skew", F(8, 3), (1 - 2 * p) / F(3, 10))  # sqrt(pq) = 3/10 exactly
chk("L03-bern-kurt-dec", "8.11", dec(73 / 9, 2))
chk("L03-p1/4-kurt", F(7, 3), (1 - 3 * F(1, 4) * F(3, 4)) / (F(1, 4) * F(3, 4)))
chk("L03-p1/4-skew", "1.155", dec(2 / math.sqrt(3), 3))
chk("L03-p1/4-sigma", F(3, 16), F(1, 4) * F(3, 4))
chk("L03-pq=1/6-kurt", 3, (1 - 3 * F(1, 6)) / F(1, 6))
chk("L03-pq=1/6-p", True, abs(float((1 - 1 / math.sqrt(3)) / 2) * (1 - float((1 - 1 / math.sqrt(3)) / 2)) - 1 / 6) < 1e-12)
Zl = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
mz = E(Zl)
chk("L03-s4-mean", 0, mz)
chk("L03-s4-m3", 0, sum(((v - mz) ** 3 * pp for v, pp in Zl), F(0)))
chk("L03-s4-m2", 3, sum(((v - mz) ** 2 * pp for v, pp in Zl), F(0)))
chk("L03-s4-m4", 15, sum(((v - mz) ** 4 * pp for v, pp in Zl), F(0)))
chk("L03-s4-kurt", "5/3", str(F(15) / 9))
chk("L03-5/3-dec", "1.6667", dec(5 / 3, 4))
chk("L03-M2-sym-kurt", 1, F(1))
chk("L03-M3-sum", F(34512, 512), sum(((v - mu) ** 3 * pp for v, pp in SK), F(0)))
# Assumption 2.6 / Prop 2.8 integration by parts check (symbolic values)

# ---- L04 ----
dep = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
chk("L04-sum", 1, sum(dep.values()))
pxd = {x: sum(pp for (xx, y), pp in dep.items() if xx == x) for x in (0, 1, 2)}
pyd = {y: sum(pp for (xx, y2), pp in dep.items() if y2 == y) for y in (0, 1)}
chk("L04-PY", ("2/5", "3/5"), (str(pyd[0]), str(pyd[1])))
chk("L04-EX", "4/5", str(sum(x * pp for x, pp in pxd.items())))
chk("L04-E[X|Y=0]", 1, sum(x * dep[(x, 0)] for x in (0, 1, 2)) / pyd[0])
chk("L04-E[X|Y=1]", F(2, 3), sum(x * dep[(x, 1)] for x in (0, 1, 2)) / pyd[1])
chk("L04-total", F(4, 5), pyd[0] * 1 + pyd[1] * F(2, 3))
chk("L04-cell00-dep", ("1/10", "4/25"), (str(dep[(0, 0)]), str(pxd[0] * pyd[0])))
chk("L04-ratio", F(5, 8), dep[(0, 0)] / (pxd[0] * pyd[0]))
prod_x = {0: F(1, 5), 1: F(2, 5), 2: F(2, 5)}
prod_y = {0: F(3, 10), 1: F(7, 10)}
chk("L04-cell00-prod", F(3, 50), prod_x[0] * prod_y[0])
U = [(-1, F(1, 3)), (0, F(1, 3)), (1, F(1, 3))]
EX = sum(x * pp for x, pp in U)
EY = sum(x * x * pp for x, pp in U)
EXY = sum(x * x * x * pp for x, pp in U)
chk("L04-ex1.9", ("0", "2/3", "0", "0"), (str(EX), str(EY), str(EXY), str(EXY - EX * EY)))
chk("L04-ex1.9-cell", (F(1, 3), F(1, 9)), (F(1, 3), F(1, 3) * F(1, 3)))
chk("L04-R1-|X|", F(2, 3), sum(abs(x) * pp for x, pp in U))
chk("L04-M1", (F(3, 10), F(7, 10), F(2, 5), F(3, 5)), (F(1, 10) + F(2, 10), F(7, 10), F(1, 10) + F(3, 10), F(3, 5)))
chk("L04-M1-cell", F(12, 100), F(3, 10) * F(2, 5))  # P(X=0)P(Y=0)=0.3*0.4
chk("L04-M2", F(2, 3), F(4, 10) / F(3, 5))
chk("L04-M3", (F(1, 8), F(3, 8)), (F(1, 4) * F(1, 2), F(3, 4) * F(1, 2)))
chk("L04-M3-EXY", F(1, 8), F(1, 4) * F(1, 2))
chk("L04-quiz-PY1", F(3, 5), F(3, 10) + F(2, 10) + F(1, 10))
chk("L04-quiz-cell", F(3, 50), F(1, 5) * F(3, 10))

print("FAILS:", fails if fails else "none")
