import math, csv, statistics, sys
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def rhu(x): return math.floor(x + F(1, 2))

print("== L01 ==")
d1=400; r=F(9,100); g=F(3,100); g1=F(1,100)
F0=F(d1)/(r-g); print("F0", F0, float(F0), rhu(F0))
q=(1+g)/(1+r); print("q", q, float(q))
for N in (10,60,200):
    S=sum(F(d1)*(1+g)**(s-1)/(1+r)**s for s in range(1,N+1))
    print("N",N,"S rounded",rhu(S),"identity",S==F0*(1-q**N),"F0q^N rounded",rhu(F0*q**N), float(F0*q**N))
print("F2", float(F(d1)*(1+g)**2/(r-g)), "F3 (d1=250,r=10,g=4)", float(F(250)*F(104,100)**3/F(6,100)), rhu(F(250)*F(104,100)**3/F(6,100)))
print("F0 d1=250 r10 g4 ->", F(250)/F(6,100), float(F(250)/F(6,100)), rhu(F(250)/F(6,100)))
print("PV 400/1.09", float(F(400,109)), rhu(F(400,109)))
print("closed form g=10%", F(400)/(F(9,100)-F(10,100)))
print("S10 with q=1 r=g=5%", float(sum(F(100)/F(105,100) for _ in range(10))), F(20000,21), float(F(20000,21)))
print("g* ", float(F(9,100)-F(400,6000)), F(9,100)-F(1,15))
print("Ratio 9/13", 9/13, "2175/8698", 2175/8698, "8698.49 check", float(F(400)*F(103,100)**9/F(6,100)))
print("gap as share unrounded: 0.25 ->", "exact 25.00 percent")
print("ln1.1", math.log(1.1), 0.1-math.log(1.1))
print("sec5 witness 1%:", float(F(400)/(F(9,100)-F(1,100))), "3%:", float(F(400)/(F(9,100)-F(3,100))), float(F(20000,3)-6000), float(F(6000)-F(20000,3)))
print("L01 Part B gap rounding check t=9:", rhu(F(400)*F(103,100)**9/F(6,100)))

print("== L03 ==")
D=1_000_000; K0=4_000_000; delta=F(1,50); H=12
def P(m,t): return (1-delta)**min(t,m)
def V(m,t): return F(D)/P(m,t)
def K(m,t): return K0-(V(m,t)-D)
def L(m,t): return V(m,t)/K(m,t)
def lam(x): C=K0+D; return x/(C-x)
for m in (12,4):
    fs=[(L(m,t)-L(m,0)) for t in range(H+1)]
    depth=max(fs); t_first=[t for t in range(H+1) if fs[t]==depth][0]
    print("m",m,"depth exact",float(depth)*100,"t_first",t_first, "depth rounded 2dp", rhu(depth*100*100)/100)
    print("  V_t12 exact", float(V(m,12)), float(V(m,12)) if False else '', "real debt rounded", rhu(V(m,12)))
print("V4 Y", float(V(4,4)), rhu(V(4,4)), "K4", float(K(4,4)), rhu(K(4,4)), "L4", float(L(4,4)), float(L(4,4)))
print("P4", P(4,4), float(P(4,4)))
print("L0", float(L(4,0)))
dX=max(L(12,t)-L(12,0) for t in range(H+1))*100
dY=max(L(4,t)-L(4,0) for t in range(H+1))*100
print("depthX%",float(dX),"depthY%",float(dY),"diff",float(dX-dY), "printed diff 9.20-2.69", 9.20-2.69)
print("ratio (beta phi=1)", float(dX/dY))
for phi in (F(1,2),F(3)):
    pass
# Part D with phi, beta: depth scales with beta*phi; ratio invariant
print("ratio check", float((max(L(12,t)-L(12,0) for t in range(H+1)))/(max(L(4,t)-L(4,0) for t in range(H+1)))))
print("E2 check text: 9.204597-2.686713 =", 9.204597-2.686713)
print("E1 2.6867", float(max(L(4,t)-L(4,0) for t in range(H+1))*100))
print("9.20 printed vs exact", float(dX))

print("== L04 ==")
rows=[]
with open('/Users/billyribeiro/.fanout/wt/verifyF31-LX1-d/course/assets/data/market/fx_monthly.csv', newline='') as h:
    for rec in csv.DictReader(h):
        rows.append((rec['month'], F(rec['GBP'])))
print("rows", len(rows), rows[0][0], rows[-1][0])
ch=[(rows[i][0], math.log(float(rows[i][1]/rows[i-1][1]))) for i in range(1,len(rows))]
zero=[m for i,m in [(i,rows[i][0]) for i in range(1,len(rows))] if rows[i][1]==rows[i-1][1]]
print("changes", len(ch), "zeros", zero)
w1=[c for _,c in ch]; w2=[c for m,c in ch if m>='2000-01']
print("n2", len(w2), ch[0][0], ch[-1][0])
s1=statistics.stdev(w1); s2=statistics.stdev(w2)
print("sd1", s1, "sd2", s2, "diff", s2-s1, "ratio", s2/s1)
print("max1", max(ch,key=lambda t: abs(t[1])), "max2", max([x for x in ch if x[0]>='2000-01'], key=lambda t: abs(t[1])))
print("simple change at 2008-10", math.exp(-0.0965747)-1)
print("tanh(z/2) with z=0.135846", math.tanh(0.135846/2), "bound at h=0.0678", math.log(1.0678/0.9322))
print("ratio to 4dp", round(s2/s1,4))
print("ln tie check: window 2 start rate 1999-12 index")
print("M2 mean", 0.02/3, "sd", math.sqrt(19/30000), "sum sq dev", 0.0014-3*(1/150)**2, 19/15000)
print("R2 h exact", math.tanh(0.135846/2))
print("L04 ln1.1 simple difference", 0.1-math.log(1.1))
