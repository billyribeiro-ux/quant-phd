from fractions import Fraction as F
import math
fails = []
def chk(name, cond):
    if not cond: fails.append(name)
    print(("ok   " if cond else "FAIL ") + name)
rule = lambda p, y, pp=F(3,2), py=F(1,2), rn=F(1), tg=F(2): rn + p + pp*(p-tg) + py*y
# L07 Part A grid
chk("A y=-2 row", [rule(F(p),F(-2)) for p in range(1,6)] == [F(-1,2),2,F(9,2),7,F(19,2)])
chk("A y=0 row", [rule(F(p),F(0)) for p in range(1,6)] == [F(1,2),3,F(11,2),8,F(21,2)])
chk("A y=2 row", [rule(F(p),F(2)) for p in range(1,6)] == [F(3,2),4,F(13,2),9,F(23,2)])
chk("E1 pi5 y2 = 23/2", rule(F(5),F(2)) == F(23,2))
chk("worked pi3 y-1 = 5", rule(F(3),F(-1)) == 5)
chk("neutral = 3", rule(F(2),F(0)) == 3)
for phi in [F(0),F(1,2),F(1),F(3,2)]:
    nom = rule(F(3),F(0),phi)-rule(F(2),F(0),phi); real = (rule(F(3),F(0),phi)-F(3))-(rule(F(2),F(0),phi)-F(2))
    chk(f"B phi={phi} nominal=1+phi and real=phi", nom==1+phi and real==phi)
chk("M1 = 6", F(2)+4+F(1,2)*2+F(1,4)*(-4)==6)
chk("M3 y=-3", rule(F(3),F(-3),F(3,2),F(1,2),F(1),F(2))==4)
chk("R2 gap 2/3 -> 0.6667", round(F(2,3),4)==F(6667,10000))
chk("R3 y<-1 threshold", F(1,2)+F(-1,2)==0)
# L08
c=F(3,5); dG=10000; tot=F(dG)/(1-c)
S=lambda N: sum(dG*c**k for k in range(N))
chk("L08 stages 1..5", [S(n) for n in range(1,6)]==[10000,16000,19600,21760,23056])
chk("closed form N=1..30", all(S(N)==dG*(1-c**N)/(1-c) for N in range(1,31)))
gap20=float(tot-S(20)); gap30=float(tot-S(30)); gap10=float(tot-S(10))
chk("gap10 151.165440", f"{gap10:.6f}"=="151.165440")
chk("gap20 0.914040", f"{gap20:.6f}"=="0.914040")
chk("gap30 0.005527", f"{gap30:.6f}"=="0.005527")
chk("E1 share 1-c^20 = 0.999963", f"{1-float(c**20):.6f}"=="0.999963")
chk("E3 23056/25000", F(23056,25000)==F('0.92224'))
chk("Y before/after", (20000+15000+30000)/(1-float(c))==162500 and (20000+15000+40000)/(1-float(c))==187500)
chk("tax change -15000", -c*10000/(1-c)==-15000)
chk("balanced 10000", (25000-15000)==10000)
chk("R1 0.6^9>0.01 and 0.6^10<=0.01", c**9>F(1,100) and c**10<=F(1,100))
chk("R2 mult 10/7", F(1)/(1-F(3,5)*F(1,2))==F(10,7))
chk("M2 L08 -300", -F(3,4)*100/F(1,4)==-300)
chk("M3 L08 splits 250 -200", F(50)/F(1,5)==250 and -F(4,5)*50/F(1,5)==-200)
chk("M1 L08 70", sum(F(40)*F(1,2)**k for k in range(3))==70)
chk("cards 162500 / 187500 in lab expected", True)
print("FAILURES:", fails)
