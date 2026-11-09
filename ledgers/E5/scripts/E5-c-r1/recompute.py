from fractions import Fraction as F
checks = []
def chk(name, cond):
    checks.append((name, bool(cond)))

# L07 Part A/B/D and worked numbers (rule i = rn + pi + phi_pi (pi - pibar) + phi_y y)
def rule(rn, pibar, phip, phiy, pi, y):
    return rn + pi + phip * (pi - pibar) + phiy * y
rn, pibar, phip, phiy = F(1), F(2), F(3, 2), F(1, 2)
chk("L07 A y=-2 pi=1 -> -1/2", rule(rn, pibar, phip, phiy, F(1), F(-2)) == F(-1, 2))
chk("L07 A y=0 pi=1..5", [rule(rn, pibar, phip, phiy, F(p), F(0)) for p in range(1, 6)] == [F(1,2), F(3), F(11,2), F(8), F(21,2)])
chk("L07 A y=2 pi=5 -> 23/2 (E1)", rule(rn, pibar, phip, phiy, F(5), F(2)) == F(23, 2))
chk("L07 A y=-2 pi=3 -> 9/2 (E2)", rule(rn, pibar, phip, phiy, F(3), F(-2)) == F(9, 2))
chk("L07 D worked pi=3 y=-1 -> 5", rule(rn, pibar, phip, phiy, F(3), F(-1)) == 5)
chk("L07 D neutral pi=2 y=0 -> 3", rule(rn, pibar, phip, phiy, F(2), F(0)) == 3)
chk("L07 Q2 1+3+3/2*1+1/2*(-1)=5", 1 + 3 + F(3,2) + F(1,2)*(-1) == 5)
chk("L07 M1 =6", 2 + 4 + F(1,2)*(4-2) + F(1,4)*(-4) == 6)
chk("L07 M3 y=-3 gives 4", rule(F(1), F(2), F(3,2), F(1,2), F(3), F(-3)) == 4)
chk("L07 R2 1/phi = 2/3", 1 / F(3, 2) == F(2, 3))
chk("L07 Part B nominal response 1+phi, real response phi (pi 2->3, y=0)", all(((rule(rn,pibar,F(p),phiy,F(3),F(0))-rule(rn,pibar,F(p),phiy,F(2),F(0)))==1+F(p)) and (((rule(rn,pibar,F(p),phiy,F(3),F(0))-F(3))-(rule(rn,pibar,F(p),phiy,F(2),F(0))-F(2)))==F(p)) for p in [F(0),F(1,2),F(1),F(3,2)]))
chk("L07 P2 real rate = rn at pi=pibar,y=0 (any phi)", all(rn + F(p)*(pibar-pibar) + phiy*0 == rn for p in [F(0), F(1,2), F(7,3)]))
chk("L07 P1 slope 1+phi, alpha = rn - phi*pibar + phiy*y", all(rule(rn,pibar,F(p),phiy,F(7),F(0)) - rule(rn,pibar,F(p),phiy,F(6),F(0)) == 1+F(p) for p in [F(0), F(3,2)]))

# L08
c = F(3, 5); a = 20000; I = 15000; G = 30000; dG = 10000; dT = 10000
def S(n, x=F(dG)): return sum((x * c**k for k in range(n)), F(0))
chk("L08 stages 10000 6000 3600 2160 1296", [dG*c**k for k in range(5)] == [10000, 6000, 3600, 2160, 1296])
chk("L08 running totals 23056 after 5 (E3)", S(5) == 23056)
chk("L08 running totals 10000 16000", S(1) == 10000 and S(2) == 16000)
chk("L08 closed form N=1..30", all(S(n) == dG*(1-c**n)/(1-c) for n in range(1, 31)))
mt = F(dG)/(1-c)
chk("L08 multiplier total 25000", mt == 25000)
chk("L08 gap N=1 15000", mt - S(1) == 15000)
chk("L08 gap N=5 1944", mt - S(5) == 1944)
chk("L08 gap N=20 ~0.914040", round(float(mt - S(20)), 6) == 0.914040)
chk("L08 E1 share c^20 = 0.0000365616", round(float(c**20), 10) == 0.0000365616)
chk("L08 E1 share 0.999963", round(float(1 - c**20), 6) == 0.999963)
chk("L08 E3 23056/25000 = 0.92224", F(23056, 25000) == F(92224, 100000))
chk("L08 Y_before 162500", (a + I + G) / (1 - c) == 162500)
chk("L08 Y_after 187500", (a + I + G + dG) / (1 - c) == 187500)
chk("L08 spending change 25000 = 5/2 * dG", (a+I+G+dG)/(1-c) - (a+I+G)/(1-c) == F(5,2)*dG)
chk("L08 tax change -15000", -c*dT/(1-c) == -15000)
chk("L08 balanced budget 10000", -c*dT/(1-c) + dG/(1-c) == 10000 if dT == dG else True)
chk("L08 R3 0.6^9 > 0.01", F(3,5)**9 > F(1,100))
chk("L08 R3 0.6^10 <= 0.01", F(3,5)**10 <= F(1,100))
chk("L08 R3 0.6^9 = 0.010077696", F(3,5)**9 == F(10077696, 10**9))
chk("L08 R3 0.6^10 = 0.0060466176", F(3,5)**10 == F(60466176, 10**10))
chk("L08 R2 multiplier 10/7", 1/(1 - F(3,5)*(1-F(1,2))) == F(10,7))
chk("L08 M1 70 CU", F(40)*(1-F(1,2)**3)/(1-F(1,2)) == 70)
chk("L08 M2 -300 CU", -F(3,4)*100/(1-F(3,4)) == -300)
chk("L08 M3 250 -200 50", (F(50)/(1-F(4,5)), -F(4,5)*50/(1-F(4,5))) == (250, -200))
chk("L08 quiz 2.5 = 1/(1-3/5)", 1/(1-c) == F(5,2))
chk("L08 quiz S1/(dG/(1-c)) = 0.4", S(1)/mt == F(2,5))
chk("L08 P1 (1-c)(1+c+c^2)=1-c^3", (1-c)*(1+c+c*c) == 1-c**3)

bad = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(("OK   " if ok else "FAIL ") + n)
print(f"{len(checks)} checks, {len(bad)} failures")
