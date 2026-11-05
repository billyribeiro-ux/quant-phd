# Independent re-derivation of the numbers quoted on PC3 cards (not using the lab code).
import math
from fractions import Fraction as F
from itertools import product

# L01
print("ln19.5", round(math.log(19.5), 10), "ln3+ln5+ln1.3", round(math.log(3)+math.log(5)+math.log(1.3), 10))
print("red QU [4,8]", round(math.log(10/2) - 0 + 0, 4) if False else round(math.log(2.5)-math.log(2.5),4))
print("QU reduction ln(10/2)->ln(8/4): width change", round(math.log(10/2)-math.log(8/4),10))  # 2 -> 8/4 ratio
print("ln(3/2)", round(math.log(3/2),4), "ln(2.5/1.01)", round(math.log(2.5/1.01),4), "ln2.5", round(math.log(2.5),4))
print("symbols reduction ln(60/40)", round(math.log(60/40),10), "minutes reduction ln(390/360)?", round(math.log(390/330)-0,4))
print("total after minutes narrowing 330-360:", round(math.log(60*10*390/(20*2*300)) - math.log(390/330) + math.log(360/330) - 0,10))
# product check for narrowings directly
base=math.log(234000/12000)
for name,(lo,hi) in {"sym":(20,40),"qu":(4,8),"min":(330,360)}.items():
    lw=(60/20)*(10/2)*(390/300)
    if name=="sym": tot=math.log(40*10*390/(20*2*300))
    if name=="qu": tot=math.log(60*8*390/(20*4*300))
    if name=="min": tot=math.log(60*10*360/(20*2*330))
    print(name, round(tot,10), "reduction", round(base-tot,10), "share%", round((base-tot)/base*100,2))
print("1.01^10", float(F(101,100)**10), "rem", float(F(101,100)**10-1-F(1,10)), "bound", float(F(45)*F(101,100)**8*F(1,10000)))
print("1.05^10", float(F(105,100)**10), "miss", float(F(105,100)**10-1-F(1,2)), "bound", float(F(45)*F(105,100)**8*F(1,400)))
print("miss share", round((float(F(105,100)**10-1-F(1,2)))/float(F(105,100)**10)*100,2))
print("geo mid", round(math.sqrt(12000*234000),2))

# L02 numbers
print("L02 P(bag1|red)", F(1,2)*F(3,4)/(F(1,2)))
# L03 expectations: independent recomputation by full path enumeration with rule first-hit
def expect(outcomes, rule, N=6):
    tot=F(0)
    for seq in product(outcomes, repeat=N):
        w=F(1); h=[]
        stopped=False
        for x,p in seq:
            w*=p; h.append(x)
            if rule(tuple(h)): break
        tot+=w*sum(h)
    return tot
fair=((100,F(1,2)),(-100,F(1,2)))
biased=((150,F(1,2)),(-100,F(1,2)))
rules={"all":lambda h: False,"first win":lambda h: h[-1]>0,"first loss":lambda h: h[-1]<0,
"100":lambda h: sum(h)>=100,"200":lambda h: abs(sum(h))>=200}
for nm,r in rules.items():
    print("fair",nm, expect(fair,r), " biased", expect(biased,r))
# reroll game
g=[F(100*f) for f in range(1,7)]
cont=sum(g)/6-100
vals=[max(F(100*f),cont) for f in range(1,7)]
print("reroll cont", cont, "value", sum(vals)/6, float(sum(vals)/6), "gain", sum(vals)/6-350, "threshold faces", [f for f in range(1,7) if 100*f<cont])
# break-evens
def A(r): return sum(1/(1+r)**t for t in range(1,4))
for r in (0.08,0.10,0.12):
    print("breakeven", r, 3000/A(r), round(3000/A(r),2))
print("diff 8->12 per point", (3000/A(0.12)-3000/A(0.08))/4)
print("8->10", 3000/A(0.10)-3000/A(0.08), "10->12", 3000/A(0.12)-3000/A(0.10))
print("399300/331", 399300/331, "33275/331", 33275/331, "u* M3", 100000/(400*A(0.10)))
print("R3 margin", (15000000/(1600*A(0.10)))/5000, 1-(15000000/(1600*A(0.10)))/5000)
print("E2 NPV at 1200", 5000*1200*A(0.10)-15000000, -105000000/1331)
print("E2 NPV at 1300", 5000*1300*A(0.10)-15000000, 1550000000/1331)
print("NPV 200 @10", 5000*200*A(0.10)-15000000, "1600", 5000*1600*A(0.10)-15000000)
print("NPV 200 @8", 5000*200*A(0.08)-15000000, "1600 @8", 5000*1600*A(0.08)-15000000)
print("NPV 200 @12", 5000*200*A(0.12)-15000000, "1600 @12", 5000*1600*A(0.12)-15000000)
print("NPV 1200 @8", 5000*1200*A(0.08)-15000000)
print("M2 NPV", -100+60/1.1+60/1.21, F(500,121))
print("E1 annuity 12", A(0.12), 3000/A(0.12))
print("A(10) exact", F(3310,1331), float(F(3310,1331)))
# L04 numbers
print("sd at 3", 5*3, "sd at 10", 5*10, "var I=10", 25*100)
print("R1 d", (1-0.6)*10/0.6)
print("R3 variance", [I for I in range(-3,4) if 25*I*I<100])
print("E2 L04 se", math.sqrt(0.25/20), (13/20-0.5)/math.sqrt(0.25/20))
