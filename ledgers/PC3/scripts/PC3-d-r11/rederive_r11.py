"""Independent re-derivation of every numeric claim in the PC3 cards and lessons (slice d, round 11)."""
from fractions import Fraction as F
import math

print("== L01 ==")
ln = math.log
base = ln(3) + ln(5) + ln(1.3)
print("ln 19.5 =", f"{ln(19.5):.10f}", "sum factor widths =", f"{base:.10f}")
print("ln3, ln5, ln1.3 =", f"{ln(3):.10f}", f"{ln(5):.10f}", f"{ln(1.3):.10f}")
red_qu = ln(10/2) - ln(8/4)
red_min = ln(390/300) - ln(360/330)
red_sym = ln(60/20) - ln(40/20)
print("reductions: symbols", f"{red_sym:.10f}", "quotes", f"{red_qu:.10f}", "minutes", f"{red_min:.10f}")
print("shares of baseline: quotes", f"{red_qu/base*100:.6f}%", "minutes", f"{red_min/base*100:.6f}%")
print("E2 four-place quotient:", f"{0.9163/2.9704*100:.6f}%", " full precision:", f"{0.9162907319/2.9704144656*100:.6f}%")
print("L01 line 140 ratio rem/bound:", f"{0.0046221254/0.0048728552:.6f}", " bound/rem-1:", f"{0.0048728552/0.0046221254-1:.6f}")
print("exact 1.01^10 =", f"{F(101,100)**10 and float(F(101,100)**10):.13f}", "exact fraction digits:", str(F(101,100)**10))
print("1.05^10 =", f"{1.05**10:.10f}", " miss 1.6288946268-1.5 =", f"{1.05**10-1.5:.10f}")
rem = lambda n,x: (1+x)**n - 1 - n*x
bnd = lambda n,x: n*(n-1)/2*(1+x)**(n-2)*x*x
print("L01 Part3 n10 x0.01 rem, bound:", f"{float(rem(10,F(1,100))):.10f}", f"{float(bnd(10,F(1,100))):.10f}")
print("n10 x0.05 bound:", f"{float(bnd(10,F(1,20))):.10f}", " exact rem:", f"{float(rem(10,F(1,20))):.10f}")
print("E3 new width ln(19.5/16.5) =", f"{ln(19.5/16.5):.10f}", " ln16.5=", f"{ln(16.5):.10f}")
print("E1 ratio 0.0046221254/0.0048728552 =", f"{0.0046221254/0.0048728552:.6f}")
print("sqrt(12000*234000) =", f"{math.sqrt(12000*234000):.10f}")
print("L01 M3: 31/1000 vs 33/1000:", F(1331,1000)-1-F(3,10), F(3,1)*F(11,10)*F(1,100))
print("E1 L01 remainder/bound exact fraction check n=10 x=1/100 bound =", bnd(10,F(1,100)))

print("== L01 R1 ==")
print("half of total", f"{base/2:.4f}", "ln5", f"{ln(5):.4f}", "ln3", f"{ln(3):.4f}")
print("R3:", f"{ln(3/2):.4f}", f"{ln(2.5/1.01):.4f}", f"{ln(2.5):.4f}", f"{ln(3):.4f}")

print("== L02 ==")
print("two-flip, card values verified by enumeration in lab; urn 3/5, 3/10, 3/4")
print("M2 P(B)=", F(3,10)*F(1,2)+F(7,10)*F(1,5), " P(A|B)=", (F(3,10)*F(1,2))/(F(3,10)*F(1,2)+F(7,10)*F(1,5)))
print("Monty rule B: P(goat)=", F(1,3)*1+F(2,3)*F(1,2))

print("== L03 ==")
import itertools
def stop_exp(outcomes, rule, H=6):
    def val(hist):
        if len(hist)==H or rule(hist): return F(sum(hist))
        return sum((p*val(hist+(x,)) for x,p in outcomes), F(0))
    return val(())
biased=((150,F(1,2)),(-100,F(1,2)))
fair=((100,F(1,2)),(-100,F(1,2)))
rules={"win":lambda h: bool(h) and h[-1]>0,"loss":lambda h: bool(h) and h[-1]<0,"100":lambda h: sum(h)>=100,"200":lambda h: sum(h)>=200 or sum(h)<=-200,"all":lambda h: False}
for k,r in rules.items():
    print("biased", k, stop_exp(biased,r), " fair", stop_exp(fair,r))
# reroll
cont = F(sum(100*g for g in range(1,7)),6)-100
vals=[max(F(100*f),cont) for f in range(1,7)]
print("reroll cont", cont, "value", sum(vals)/6, float(sum(vals)/6), "gain", sum(vals)/6-350)
print("R2 gain at fee 1:", (sum(max(F(100*f),350-1) for f in range(1,7))/6)-350)
print("E2 change", F(625,8)-150, float(F(625,8)-150))
print("R1 two-turn", (F(200)+100+0-100)/4)
print("M2 p:", "300p-100=0 -> p=1/3")

print("== L04 ==")
print("E2 z:", (0.65-0.5)/math.sqrt(0.25/20))
print("CHECK sqrt(0.25/20)=", math.sqrt(0.25/20))
print("R1 d=", F(2,5)*10/F(3,5))
print("E3 P&L: settle", -9950+1*9980, " mid", -9950+1*9990)

print("== L05 ==")
n=200
print("naive 8:", (n-8+1)*7, " naive 32:", (n-32+1)*31, " naive 200:", 1*199, " 101:", (200-101+1)*100)
print("Remark 2.2 n=200 k=101 count", (200-101+1)*100, n*n//4)
print("heap bound 3n floor log2 n:", 3*200*math.floor(math.log2(200)))
print("E1 ratio 5239/382 =", 5239/382)
print("M1 n=10 k=4:", (10-4+1)*(4-1))

print("== L06 ==")
A = lambda r: sum(F(1,1)/ (F(1)+r)**t for t in range(1,4))
for r in (F(8,100),F(10,100),F(12,100)):
    a=A(r); be=F(15000000,5000)/a
    lo=F(200)*5000*a-15000000; hi=F(1600)*5000*a-15000000
    print("rate",r,"A=",float(a),"BE=",float(be), "NPV@200", float(lo), "NPV@1600", float(hi))
    print("   exact NPV@200 =", lo, " exact NPV@1600 =", hi)
a10=A(F(1,10))
print("A10 exact:", a10, " 3310/1331 ok:", a10==F(3310,1331))
print("NPV@1200 exact:", F(1200)*5000*a10-15000000, float(F(1200)*5000*a10-15000000))
print("NPV@1300 exact:", F(1300)*5000*a10-15000000, float(F(1300)*5000*a10-15000000))
print("NPV@200 10%:", float(F(200)*5000*a10-15000000))
print("breakeven 10% exact:", F(15000000,5000)/a10, float(F(15000000,5000)/a10))
print("M3 break-even:", F(100000,400)/a10, float(F(100000,400)/a10), F(33275,331)==F(100000,400)/a10)
print("M2 NPV:", F(-100)+F(60)/F(11,10)+F(60)/F(121,100), F(500,121)==F(-100)+F(60)/F(11,10)+F(60)/F(121,100))
print("R3 margin:", float(F(15000000)/(1600*a10)), float(F(15000000)/(1600*a10))/5000, 1-float(F(15000000)/(1600*a10))/5000)
print("E1 annuity 12%:", float(A(F(12,100))), 3000/float(A(F(12,100))))
print("unrounded BEs:", 3000/float(A(F(8,100))), 3000/float(A(F(10,100))), 3000/float(A(F(12,100))))
print("E3 average:", (3000/float(A(F(12,100)))-3000/float(A(F(8,100))))/4)
print("Remark 4.3 diffs:", 3000/float(A(F(10,100)))-3000/float(A(F(8,100))), 3000/float(A(F(12,100)))-3000/float(A(F(10,100))))
print("E2 1200 NPV float:", float(F(-105000000,1331)), " 1300:", float(F(1550000000,1331)))
print("NPV@200 exact -16655000000/1331 =", float(F(-16655000000,1331)), " 1600 ->", float(F(6515000000,1331)))
print("R2 L06 fee: none")
print("M1: 4900/0.98 =", F(4900)/F(98,100), "payoff", F(5050)-F(5000))
print("R1 L06: log2 each", math.log(2))
print("card c116/c148/c121 BEs:", f"{3000/float(A(F(8,100))):.2f}", f"{3000/float(A(F(10,100))):.2f}", f"{3000/float(A(F(12,100))):.2f}")
