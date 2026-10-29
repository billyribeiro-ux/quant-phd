from fractions import Fraction as F
import math
def cents(x): return math.floor(x + F(1, 2))
# L04 threshold enumeration with parameters
def l04(yl, yh, cl, ch, grid=range(0, 7)):
    def w(e, t): return yh if e >= t else yl
    def u(c, e, t): return w(e, t) - c * e
    seps = []
    for t in grid:
        if t == 0: continue
        uh = u(ch, t, t); bh = max(u(ch, e, t) for e in grid)
        ul = u(cl, 0, t); bl = max(u(cl, e, t) for e in grid)
        if uh == bh and ul == bl: seps.append(t)
    lo, hi = F(yh - yl, cl), F(yh - yl, ch)
    interval = [t for t in grid if lo <= t <= hi and t > 0]
    return seps, interval, lo, hi
print("L04 base", l04(4_000_000, 6_000_000, 1_000_000, 500_000))
print("L04-e1 c_H=400000", l04(4_000_000, 6_000_000, 1_000_000, 400_000))
print("L04-e2 y_H=5e6", l04(4_000_000, 5_000_000, 1_000_000, 500_000))
print("L04-m3 Delta=1.5e6 (y_H=5.5e6)", l04(4_000_000, 5_500_000, 1_000_000, 500_000))
# L04-m1 with c_H=250000 grid 0..8 (text says thresholds 2..8)
print("L04-m1 c_H=250000 grid 0..8", l04(4_000_000, 6_000_000, 1_000_000, 250_000, grid=range(0, 9)))
# L04-m2 values
ch=250_000; print("m2 u_H(3)", 6_000_000-3*ch, "low at 3 (wage y_H)", 6_000_000-3*1_000_000)
# L05
def l05(pl, ph, tl=3000, th=6000, grid_l=range(0,6001), grid_h=range(0,12001,1000), ql=2000, qh=6000):
    pl, ph = F(pl), F(ph)
    def prof(q_l, q_h):
        tl_m = tl*q_l; th_m = th*q_h - (th-tl)*q_l
        return pl*(tl_m - F(q_l)**2/2) + ph*(th_m - F(q_h)**2/2)
    bl = max(grid_l, key=lambda q: (prof(F(q), F(qh)), -q))
    bh = max(grid_h, key=lambda q: (prof(F(ql), F(q)), -q))
    fb = pl*(tl*F(tl) - F(tl)**2/2) + ph*(th*F(th) - F(th)**2/2)
    return dict(best_low=bl, best_high=bh, menu=cents(prof(F(ql),F(qh))), menu_exact=prof(F(ql),F(qh)), first_best=cents(fb), gap=cents(fb-prof(F(ql),F(qh))), qlstar=tl - F(ph,pl)*(th-tl), prof_at_best_low_with_qh6000=prof(F(bl),F(6000)))
print("L05 base", l05(F(3,4), F(1,4)))
print("L05-e1 pH=1/3", l05(F(2,3), F(1,3)))
print("L05-e1 profit at q_L=1500", float(F(2,3)*(F(4500000)-F(1500)**2/2)+F(1,3)*(F(31500000)-F(6000)**2/2)) )
print("L05-m1 p=1/2 profit at (0,6000)", F(1,2)*(F(36000000)-F(6000)**2/2))
print("L05-m3 profit", F(3,4)*(F(3000000)-F(1000)**2/2)+F(1,4)*(F(33000000)-F(6000)**2/2))
print("L05 loss pct", float((F(7875000)-F(6000000))/F(7875000)*100), float((F(7875000)/F(6000000)-1)*100))
# L05 rent pH 1/3
print("L05-e2 rents", 3000*2000, 3000*1500)
# L06
def l06(pH=F(3,4), pL=F(1,4), X=1_000_000, cH=100_000, cL=0, beta_grid=None):
    EH, EL = pH*X, pL*X
    best=None
    for k in range(0,101):
        b=F(k,100)
        uH=b*EH-cH; uL=b*EL-cL
        if uH>=uL and uH>=0: act='high'; pr=EH-b*EH
        elif uL>=0: act='low'; pr=EL-b*EL
        else: act='refuses'; pr=F(0)
        if best is None or (pr, -b) > (best[0], -best[1]): best=(pr,b,act)
    fb=EH-cH
    return dict(best_share=str(best[1]), best_profit=cents(best[0]), exact=best[0], act=best[2], first_best=cents(fb), agency=cents(fb-best[0]))
print("L06 base", l06())
print("L06-e1 cH=150000", l06(cH=150_000))
print("L06-e2 pH=0.8,pL=0.2", l06(pH=F(4,5), pL=F(1,5)))
print("L06 m1 beta=1/4 u_H,u_L,profit", F(1,4)*750000-100000, F(1,4)*250000, 750000*(1-F(1,4)))
print("L06 m2 beta=2/15", F(2,15)*750000-100000, float(F(2,15)*250000))
print("L06 part C alpha", [(str(b), 100000-b*750000, 750000-(100000-b*750000)-b*750000) for b in (F(1,5),F(1,2),F(1))])
print("L06 p1 counter", F(-1000000)+F(1,2)*750000-100000, -1000000+F(1,2)*250000)
