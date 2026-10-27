"""Independent re-derivation for the two AC2 L07/L08 labs.
The generators (generate_firm, _clean_pair, _planted_pair, base_rate_table inputs) are imported from the
repository twins, with their trailing main() call removed; every signal, index, score, median and table value
below is recomputed here by separate code using exact Fractions on the exact float inputs."""
import ast, random, statistics, sys
from fractions import Fraction as Fr

root = sys.argv[1]

def load_without_main(path):
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)
    tree.body = [n for n in tree.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                                             and getattr(n.value.func, "id", "") == "main")]
    import types
    mod = types.ModuleType("twin_" + str(abs(hash(path))))
    sys.modules[mod.__name__] = mod
    ns = mod.__dict__
    exec(compile(tree, path, "exec"), ns)
    return ns

# ---------- L07 ----------
ns7 = load_without_main(f"{root}/tests/labs/AC2/lab-AC2-L07-1.py")
N = ns7["N_FIRMS"]; SEED = ns7["SEED"]
rng = random.Random(SEED)
firms = [ns7["generate_firm"](rng) for _ in range(N)]

def F(x): return Fr(x)  # exact binary value of the float

def signals7(y2, y1, y0):
    ta2, ta1, ta0 = F(y2.total_assets), F(y1.total_assets), F(y0.total_assets)
    roa0 = F(y0.net_income) / F(y1.total_assets); roa1 = F(y1.net_income) / F(y2.total_assets)
    cfo0 = F(y0.cfo) / F(y1.total_assets)
    lev0 = F(y0.long_term_debt) / ((ta0 + F(y1.total_assets)) / 2)
    lev1 = F(y1.long_term_debt) / ((F(y1.total_assets) + ta2) / 2)
    cr0 = F(y0.current_assets) / F(y0.current_liabilities); cr1 = F(y1.current_assets) / F(y1.current_liabilities)
    gm0 = (F(y0.revenue) - F(y0.cogs)) / F(y0.revenue); gm1 = (F(y1.revenue) - F(y1.cogs)) / F(y1.revenue)
    ato0 = F(y0.revenue) / F(y1.total_assets); ato1 = F(y1.revenue) / F(y2.total_assets)
    return (int(roa0 > 0), int(cfo0 > 0), int(roa0 > roa1), int(cfo0 > roa0), int(lev0 < lev1),
            int(cr0 > cr1), int(F(y0.shares) <= F(y1.shares)), int(gm0 > gm1), int(ato0 > ato1))

sigs = [signals7(*f) for f in firms]
dist = [0] * 10
for s in sigs:
    dist[sum(s)] += 1
print("L07 independent score distribution:", dist, "mean", round(sum(sum(s) for s in sigs) / N, 4))
print("L07 first six:", [("".join(map(str, s)), sum(s)) for s in sigs[:6]])
# scale invariance on exact values
scaled_ok = 0
for f in firms:
    y2, y1, y0 = f
    k = 1000
    sc = lambda y: ns7["YearStatement"](revenue=y.revenue*k, cogs=y.cogs*k, net_income=y.net_income*k, cfo=y.cfo*k,
                                         total_assets=y.total_assets*k, current_assets=y.current_assets*k,
                                         current_liabilities=y.current_liabilities*k, long_term_debt=y.long_term_debt*k,
                                         shares=y.shares)
    if signals7(y2, y1, y0) == signals7(sc(y2), sc(y1), sc(y0)):
        scaled_ok += 1
print("L07 independent scale-invariance:", scaled_ok, "/", N)

# worked firm (section 4) exact signals
t_ta = {2: 1000, 1: 1100, 0: 1200}
W = dict(rev1=1320, rev0=1560, cogs1=924, cogs0=1014, ni1=66, ni0=117, cfo1=90, cfo0=96, ltd1=330, ltd0=264,
         ca1=440, ca0=528, cl1=220, cl0=240, sh1=50, sh0=50)
ta2, ta1, ta0 = Fr(1000), Fr(1100), Fr(1200)
roa0 = Fr(117) / ta1; roa1 = Fr(66) / ta2
signals_worked = (int(roa0 > 0), int(Fr(96) / ta1 > 0), int(roa0 > roa1), int(Fr(96) / ta1 > roa0),
                  int(Fr(264) / ((ta0 + ta1) / 2) < Fr(330) / ((ta1 + ta2) / 2)),
                  int(Fr(528, 240) > Fr(440, 220)), int(50 <= 50),
                  int(Fr(546, 1560) > Fr(396, 1320)), int(Fr(1560) / ta1 > Fr(1320) / ta2))
print("L07 worked-firm signals (exact):", signals_worked, "F =", sum(signals_worked))
# M2: NI_t = -20
roa0m = Fr(-20) / ta1
sm = (int(roa0m > 0), int(Fr(96) / ta1 > 0), int(roa0m > roa1), int(Fr(96) / ta1 > roa0m),
      1, 1, 1, 1, 1)
print("L07 M2 (NI_t=-20) signals:", sm, "F =", sum(sm))
# P3 example
lev_t = Fr(300) / ((Fr(900) + Fr(1000)) / 2); lev_p = Fr(310) / ((Fr(1000) + Fr(1100)) / 2)
print("L07 P3: LEV_t =", lev_t, float(lev_t), " LEV_t-1 =", lev_p, float(lev_p), " s5 =", int(lev_t < lev_p))
# E2: smallest CFO integer with CFO/1100 > 117/1100
print("L07 E2 smallest integer CFO > 117:", 117 + 1, " ratio check 118/1100 =", float(Fr(118, 1100)), "> 117/1100 =", float(Fr(117, 1100)))
# E3: LTD 300
lev_e3 = Fr(300) / ((Fr(1200) + Fr(1100)) / 2)
print("L07 E3: LEV_t =", float(lev_e3), "vs LEV_t-1 =", float(Fr(330, 1050)), "s5 =", int(lev_e3 < Fr(330, 1050)))
# E1 fraction
print("L07 E1 31/400 =", float(Fr(31, 400)), " 24+7 =", 24 + 7)
print("L07 worked-firm ratios: ROA_t", float(roa0), "ROA_t-1", float(roa1), "CFO*", float(Fr(96, 1100)),
      "accrual", float(Fr(21, 1100)), "LEV_t", float(Fr(264, 1150)), "LEV_t-1", float(Fr(330, 1050)),
      "CR", float(Fr(528, 240)), float(Fr(440, 220)), "GM", float(Fr(546, 1560)), float(Fr(396, 1320)),
      "ATO", float(Fr(1560, 1100)), float(Fr(1320, 1000)))

# ---------- L08 ----------
ns8 = load_without_main(f"{root}/tests/labs/AC2/lab-AC2-L08-1.py")
rng8 = random.Random(ns8["SEED"])
clean = [ns8["_clean_pair"](rng8) for _ in range(ns8["N_CLEAN"])]
planted = [ns8["_planted_pair"](rng8) for _ in range(ns8["N_PLANTED"])]

C = {"DSRI": Fr("0.920"), "GMI": Fr("0.528"), "AQI": Fr("0.404"), "SGI": Fr("0.892"), "DEPI": Fr("0.115"),
     "SGAI": Fr("-0.172"), "LVGI": Fr("-0.327"), "TATA": Fr("4.679")}
INT = Fr("-4.84")

def ex(x): return Fr(x)

def idx8(t, p):
    gm = lambda f: (ex(f.revenue) - ex(f.cogs)) / ex(f.revenue)
    a = lambda f: 1 - (ex(f.current_assets) + ex(f.ppe)) / ex(f.total_assets)
    dep = lambda f: ex(f.depreciation) / (ex(f.depreciation) + ex(f.ppe))
    return {
        "DSRI": (ex(t.receivables) / ex(t.revenue)) / (ex(p.receivables) / ex(p.revenue)),
        "GMI": gm(p) / gm(t),
        "AQI": a(t) / a(p),
        "SGI": ex(t.revenue) / ex(p.revenue),
        "DEPI": dep(p) / dep(t),
        "SGAI": (ex(t.sga) / ex(t.revenue)) / (ex(p.sga) / ex(p.revenue)),
        "LVGI": ((ex(t.current_liabilities) + ex(t.long_term_debt)) / ex(t.total_assets)) /
                ((ex(p.current_liabilities) + ex(p.long_term_debt)) / ex(p.total_assets)),
        "TATA": (ex(t.net_income) - ex(t.cfo)) / ex(t.total_assets),
    }

def M(ix): return INT + sum(C[k] * ix[k] for k in C)

mc = [float(M(idx8(t, p))) for p, t in clean]
mp = [float(M(idx8(t, p))) for p, t in planted]
print("L08 independent median clean:", round(statistics.median(mc), 4), " planted:", round(statistics.median(mp), 4))
print("L08 independent planted[0] M:", round(float(M(idx8(planted[0][1], planted[0][0]))), 4))
print("L08 independent planted[0] indices:", {k: round(float(v), 4) for k, v in idx8(planted[0][1], planted[0][0]).items()})

# base-rate table exact
for prev in (Fr(1, 1000), Fr(1, 100), Fr(5, 100)):
    for spec in (Fr(90, 100), Fr(95, 100), Fr(99, 100)):
        fpr = 1 - spec
        s = Fr(1, 2)
        ppv = prev * s / (prev * s + (1 - prev) * fpr)
        ff = 1000 * (1 - prev) * fpr
        print(f"L08 table prev={float(prev):.3f} spec={float(spec):.2f} PPV={float(ppv):.6f} flags/1000={float(ff):.4f}")
print("L08 E2 ratio PPV(0.05)/PPV(0.001) at spec .95:",
      float((Fr(5,100)*Fr(1,2)/(Fr(5,100)*Fr(1,2)+Fr(95,100)*Fr(5,100))) / (Fr(1,1000)*Fr(1,2)/(Fr(1,1000)*Fr(1,2)+Fr(999,1000)*Fr(5,100)))))
print("L08 PPV 0.01/0.95 exact:", float(Fr(1,100)*Fr(1,2)/(Fr(1,100)*Fr(1,2)+Fr(99,100)*Fr(5,100))))
print("L08 E1 difference:", round(statistics.median(mp) - statistics.median(mc), 4))
print("L08 AND/OR at 0.10,0.05:", float(Fr(1,10)*Fr(1,20)), float(1 - Fr(9,10)*Fr(19,20)), " disjoint OR:", float(Fr(1,10)+Fr(1,20)))
print("L08 scale invariance exact check on first 50 pairs:", sum(
    1 for p, t in (clean + planted)[:50]
    if idx8(t, p) == idx8(ns8["scale"](t, 1000), ns8["scale"](p, 1000))))
