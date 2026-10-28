from decimal import Decimal, getcontext
getcontext().prec=50
print("gap pv 4-6:", 300000/1.1**4+200000/1.1**5+100000/1.1**6)
print("E2 ratio:", 385535.69/289367.40, "pct", 100*385535.69/289367.40)
print("A-B:", 289367.40+96168.29)
print("range:", 693692.91-121251.71)
print("3.019:", 3+5.26/273.21)
print("M2 terms", 400/1.1, 400/1.21, 400/1.331, 400/1.4641, 400/1.1+400/1.21+400/1.331)
print("M2 cum", -1000+400/1.1+400/1.21+400/1.331, "after4", -1000+400/1.1+400/1.21+400/1.331+400/1.4641)
print("R3 check P3: ", 2+200/300)
print("sec3 example1", -1000+1/1.1**4+1/1.1**5, "example2", -1000+1000/1.1**4)
# lab-equivalent computations
A=(-1_000_000, 300_000, 400_000, 400_000, 300_000, 200_000, 100_000)
B=(-1_000_000, 300_000, 400_000, 400_000, 0, 0, 0)
def disc(f,r): return [x/(1+r)**t for t,x in enumerate(f)]
import math
print("B discounted cum:", [round(sum(disc(B,0.1)[:k+1]),2) for k in range(7)])
print("A discounted cum:", [round(sum(disc(A,0.1)[:k+1]),2) for k in range(7)])
print("npvA", math.fsum(disc(A,0.1)), "npvB", math.fsum(disc(B,0.1)), "gap", math.fsum(disc(A,0.1))-math.fsum(disc(B,0.1)))
