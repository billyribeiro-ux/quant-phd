from fractions import Fraction as F
from math import isclose
ok = []
def chk(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

# ---- L07 rule, independent formula i = rn + pi + pp*(pi-tg) + py*y
rn, tg, py = F(1), F(2), F(1, 2)
def i_(pi, y, pp): return rn + pi + pp*(pi - tg) + py*y
def r_(pi, y, pp): return i_(pi, y, pp) - pi
grid_y0 = [i_(F(p), F(0), F(3, 2)) for p in range(1, 6)]
chk("L07 PartA y0 row = 1/2,3,11/2,8,21/2", grid_y0 == [F(1, 2), F(3), F(11, 2), F(8), F(21, 2)])
chk("L07 PartA y-2 row = -1/2,2,9/2,7,19/2", [i_(F(p), F(-2), F(3, 2)) for p in range(1, 6)] == [F(-1, 2), F(2), F(9, 2), F(7), F(19, 2)])
chk("L07 PartA y2 row = 3/2,4,13/2,9,23/2", [i_(F(p), F(2), F(3, 2)) for p in range(1, 6)] == [F(3, 2), F(4), F(13, 2), F(9), F(23, 2)])
for pp in [F(0), F(1, 2), F(1), F(3, 2)]:
    chk(f"L07 PartB nominal/real response pp={pp}", i_(F(3), F(0), pp) - i_(F(2), F(0), pp) == 1 + pp and r_(F(3), F(0), pp) - r_(F(2), F(0), pp) == pp)
chk("L07 real rate rises iff pp>0 (grid)", all(((all(r_(F(b), F(0), pp) > r_(F(a), F(0), pp) for a, b in zip(range(1, 5), range(2, 6)))) == (pp > 0)) for pp in [F(0), F(1, 2), F(1), F(3, 2)]))
chk("L07 worked pi3 y-1 = 5", i_(F(3), F(-1), F(3, 2)) == 5)
chk("L07 neutral pi2 y0 = 3, real 1", i_(F(2), F(0), F(3, 2)) == 3 and r_(F(2), F(0), F(3, 2)) == 1)
chk("L07 M1 = 6", F(2) + 4 + F(1, 2)*(4-2) + F(1, 4)*(-4) == 6)
chk("L07 M2 nominal 5/4 real 1/4", 1 + F(1, 4) == F(5, 4))
chk("L07 M3 y=-3", (1 + 3 + F(3, 2)*1 + F(1, 2)*(-3)) == 4)
chk("L07 E1 pi5 y2 = 23/2", i_(F(5), F(2), F(3, 2)) == F(23, 2))
chk("L07 E2 change -1", i_(F(3), F(-2), F(3, 2)) - i_(F(3), F(0), F(3, 2)) == -1)
chk("L07 R2 gap 2/3 ~ 0.6667 (tol 5e-5)", abs(float(F(2, 3)) - 0.6667) < 0.00005)
chk("L07 R3 pi1 y-2 = -1/2; negative iff y<-1", i_(F(1), F(-2), F(3, 2)) == F(-1, 2) and all((i_(F(1), F(y, 4), F(3, 2)) < 0) == (F(y, 4) < -1) for y in range(-12, 13)))
chk("L07 quiz q2 = 5", 1 + 3 + F(3, 2)*1 + F(1, 2)*(-1) == 5)
chk("L07 quiz q6 = 6", 2 + 4 + F(1, 2)*2 + F(1, 4)*(-4) == 6)
chk("L07 quiz q9 2/3 within tol", abs(float(F(2, 3)) - 0.6667) <= 0.00005)
chk("L07 10 pct: gap 2 at trend 10 = 20%, gap 3 at trend 100 = 3%", F(100)*2/10 == 20 and F(100)*3/100 == 3)

# ---- L08
c = F(3, 5); a, I, G, dG, dT = 20000, 15000, 30000, 10000, 10000
def S(n): return sum((dG * c**k for k in range(n)), F(0))
def closed(n): return dG * (1 - c**n) / (1 - c)
chk("L08 stage amounts 10000 6000 3600 2160 1296", [dG*c**k for k in range(5)] == [10000, 6000, 3600, 2160, 1296])
chk("L08 running totals 10000 16000 19600 21760 23056", [S(n) for n in range(1, 6)] == [10000, 16000, 19600, 21760, 23056])
chk("L08 closed form N=1..30", all(S(n) == closed(n) for n in range(1, 31)))
tot = F(dG) / (1 - c)
chk("L08 multiplier total 25000", tot == 25000)
for n in (1, 5, 10, 20, 30):
    g = tot - S(n)
    print("   gap N=%d exact=%s float6=%.6f" % (n, g, float(g)))
chk("L08 gaps N=1 15000", tot - S(1) == 15000)
chk("L08 gap N=5 1944", tot - S(5) == 1944)
chk("L08 gap N=10 151.165440", f"{float(tot - S(10)):.6f}" == "151.165440")
chk("L08 gap N=20 0.914040", f"{float(tot - S(20)):.6f}" == "0.914040")
chk("L08 gap N=30 0.005527", f"{float(tot - S(30)):.6f}" == "0.005527")
chk("L08 gap identity exact", all(tot - S(n) == dG*c**n/(1-c) for n in range(1, 31)))
def Ystar(G_, T_): return (a - c*T_ + I + G_) / (1 - c)
y0, y1 = Ystar(G, 0), Ystar(G + dG, 0)
chk("L08 Y before 162500 after 187500 change 25000", (y0, y1, y1 - y0) == (162500, 187500, 25000))
chk("L08 Y after satisfies fixed point", y1 == a + I + G + dG + c*y1)
chk("L08 per-cent change 5/2", Ystar(G+1, 0) - y0 == F(5, 2))
ttax = Ystar(G, dT) - y0
chk("L08 tax change -15000", ttax == -15000)
chk("L08 balanced change 10000", (y1 - y0) + ttax == dG)
chk("L08 tax stages -6000 -3600 -2160", [-c*dT*c**k for k in range(3)] == [-6000, -3600, -2160])
chk("L08 tax closed form N=1..30", all(sum((-c*dT*c**k for k in range(n)), F(0)) == (-c*dT)*(1-c**n)/(1-c) for n in range(1, 31)))
chk("L08 E1 share 1-c^20 6dp 0.999963", f"{float(1 - c**20):.6f}" == "0.999963")
chk("L08 E1 c^20 = 0.00003656 (8dp from 0.914040/25000)", f"{0.914040/25000:.8f}" == "0.00003656")
chk("L08 E1 running total 25000-0.914040 = 24999.085960", f"{25000-0.914040:.6f}" == "24999.085960")
chk("L08 E2 ratio -15000/25000 = -3/5", F(-15000, 25000) == -c)
chk("L08 E3 23056/25000 = 0.92224 = 92.224%", F(23056, 25000) == F(92224, 100000))
chk("L08 R1 at c=1 S_N=N dG", True)
chk("L08 R2 1/(1-c(1-tau)) = 10/7; lump 5/2", 1/(1 - c*(1 - F(1, 2))) == F(10, 7) and F(5, 2) == 1/(1-c))
chk("L08 R3 N=10", c**9 > F(1, 100) and c**10 <= F(1, 100) and float(c**9) == 0.010077696 and float(c**10) == 0.0060466176)
chk("L08 quiz q4 23056 (tol .5)", abs(10000*(1 - 0.6**5)/0.4 - 23056) <= 0.5)
chk("L08 quiz q6 -15000", -(F(3,5))*10000/(F(2,5)) == -15000)
chk("L08 quiz q9 0.4", 1 - c == F(2, 5))
chk("L08 M1 c=1/2: mult 2, change 80, 3-stage sum 70, closed 70", F(1)/(1-F(1,2)) == 2 and 2*40 == 80 and 40+20+10 == 70 and 40*(1-F(1,8))/F(1,2) == 70)
chk("L08 M2 c=3/4 dT=100: -300", -(F(3,4))*100/(F(1,4)) == -300)
chk("L08 M3 c=4/5 dG=dT=50: 250, -200, sum 50", F(50)/(F(1,5)) == 250 and -(F(4,5))*50/(F(1,5)) == -200 and 250-200 == 50)
chk("L08 P1 identity 1+c+c^2 at c=3/5 symbolic", (1-c)*(1+c+c*c) == 1 - c**3)
chk("L08 Prop2.3 bound c^N <= 1/(1+N(1/c-1)) N=1..199", all(c**n <= 1/(1 + n*(1/c - 1)) for n in range(1, 200)))
chk("L08 Bernoulli b^N >= 1+N d N=1..199", all((1/c)**n >= 1 + n*(1/c - 1) for n in range(1, 200)))
print("FAILS:", [n for n, v in ok if not v], "TOTAL", len(ok))
