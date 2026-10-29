from fractions import Fraction as F
import itertools, math

def half_up(x):
    return math.floor(x + F(1, 2))

ok = True
def check(name, cond):
    global ok
    ok = ok and cond
    print(("PASS " if cond else "FAIL ") + name)

# L07: closed forms for many (a,b,c) with b>0, c>0, a>bc
cases = [(120,1,20),(90,3,10),(200,4,5),(7,1,1),(11,2,3),(1000,7,13),(5,1,4)]
for a,b,c in cases:
    d = F(a-b*c)
    W = lambda Q: (2*d*Q - Q*Q)/(2*b)
    CS = lambda Q: Q*Q/(2*b)
    PS = lambda Q: (d-Q)*Q/b
    DWL = lambda Q: (d-Q)**2/(2*b)
    # direct integral check of W
    for Q in [F(0), d/2, 2*d/3, d, F(a)]:
        P = lambda x: F(a-x)/b
        integ = (F(a)*Q - Q*Q/2)/b - F(c)*Q
        check(f"W identity a={a} b={b} c={c} Q={Q}", integ == W(Q))
    m = (d/2, F(a+b*c, 2*b)); cn = (2*d/3, F(a+2*b*c, 3*b)); bt = (d, F(c))
    for name,(Q,f) in [("mono",m),("cour",cn),("bert",bt)]:
        check(f"fee {name} a={a} b={b} c={c}", F(a)-Q == f*b)
        check(f"CS+PS=W {name} a={a}", CS(Q)+PS(Q)==W(Q) and (f-c)*Q == PS(Q))
    check(f"Cor2.1 mono a={a}", CS(m[0])==d*d/(8*b) and PS(m[0])==d*d/(4*b) and DWL(m[0])==d*d/(8*b))
    check(f"Cor2.1 cour a={a}", CS(cn[0])==2*d*d/(9*b) and PS(cn[0])==2*d*d/(9*b) and DWL(cn[0])==d*d/(18*b))
    check(f"ratio DWL_M/DWL_C=9/4 a={a}", DWL(m[0])/DWL(cn[0]) == F(9,4))
    check(f"share mono 1/4 a={a}", DWL(m[0])/W(d)==F(1,4))
    check(f"share cour 1/9 a={a}", DWL(cn[0])/W(d)==F(1,9))

# L07 reference case cents
print("L07 ref cents: Cournot DWL", F(5000,9), half_up(F(5000,9)), "Cournot W", F(40000,9), half_up(F(40000,9)), "CS", half_up(F(20000,9)))
check("L07 DWL cournot cents 556", half_up(F(5000,9))==556)
check("L07 W cournot cents 4444", half_up(F(40000,9))==4444)
check("L07 CS cournot cents 2222", half_up(F(20000,9))==2222)

# L08: independent grid computation
X,Y=8,4
def uA(x,y): return x*y
def uB(x,y): return (X-x)*(Y-y)
grid=[(x,y) for x in range(X+1) for y in range(Y+1)]
def dominated(z,w):
    return uA(*z)>=uA(*w) and uB(*z)>=uB(*w) and (uA(*z)>uA(*w) or uB(*z)>uB(*w))
eff=[w for w in grid if not any(dominated(z,w) for z in grid)]
print("L08 grid-efficient:", len(eff), sorted(eff))
inter=[w for w in eff if 0<w[0]<X and 0<w[1]<Y]
check("L08 grid-efficient count 15", len(eff)==15)
check("L08 interior count 13", len(inter)==13)
diag=[w for w in inter if w[1]*X==w[0]*Y]
check("L08 interior diagonal 3", len(diag)==3)
off=[w for w in inter if w not in diag]
check("L08 off-diagonal 10", len(off)==10)
# exact improvements for off-diagonal: check the printed pair is feasible and strictly improves
printed = {(1,1):(F(6,5),F(6,7)),(2,2):(F(5,2),F(5,3)),(3,1):(F(18,7),F(6,5)),(3,2):(F(27,8),F(9,5)),
           (4,1):(F(3),F(3,2)),(4,3):(F(5),F(5,2)),(5,2):(F(37,8),F(11,5)),(5,3):(F(38,7),F(14,5)),
           (6,2):(F(11,2),F(7,3)),(7,3):(F(34,5),F(22,7))}
check("L08 printed improvements cover the 10", set(printed)==set(off))
for (x,y),(xa,ya) in printed.items():
    xb,yb = X-xa, Y-ya
    ok_feas = 0<=xa<=X and 0<=ya<=Y
    strict = xa*ya > uA(x,y) and xb*yb > uB(x,y)
    check(f"L08 improvement from {(x,y)} feasible and strict", ok_feas and strict)
# equality points of the bound
eqs=[]
for x,y in grid:
    ua,ub=F(uA(x,y)),F(uB(x,y)); slack=X*Y-ua-ub
    assert slack>=0 and 4*ua*ub<=slack*slack
    if 4*ua*ub==slack*slack: eqs.append((x,y))
check("L08 equality points = diagonal grid points", sorted(eqs)==sorted([(x,y) for x,y in grid if y*X==x*Y]))
# R3 boundary improvement
check("L08 R3 improvement", F(8,3)*1 > 0 and (F(8)-F(8,3))*(F(3))==16 and F(8,3)*1==F(8,3))
# M2 improvement
xa,ya=F(10,11),F(5,12)
check("L08 M2 utilities", (4-F(10,11))*(1+F(5,12))==F(289,66) and (6+F(10,11))*(4-F(5,12))==F(817,33))
# L08 E1 numbers
check("L08 E1 A share 3/35/3", (F(3,35)/3)==F(1,35))

# L09 numbers
a,b,e,c=1000,10,120,200
qp=F(a-c,b); qs=F(a-c-e,b)
check("L09 qp 80 qs 68", qp==80 and qs==68)
check("L09 tax unique 120", [t for t in range(0,201) if F(a-c-t,b)==qs]==[120])
check("L09 DWL 720", F(e*e,2*b)==720)
check("L09 revenue 8160", 120*68==8160)
check("L09 tax100 loss 20", F(b,2)*(F(70)-68)**2==20)
def W9(q): return F(a)*q - F(b,2)*q*q - F(c+e)*q
check("L09 W(qs)-W(qp)=720", W9(qs)-W9(qp)==720)
check("L09 completed square", all(W9(F(q))==W9(qs)-F(b,2)*(F(q)-qs)**2 for q in range(-5,20)))
# public good
def A(g): return (1000-100*g)+max(F(0),600-200*g)
def S(g):
    g=F(g); pts=[F(0)]+([F(3)] if g>3 else [])+[g]
    area=sum((A(pts[i])+A(pts[i+1]))/2*(pts[i+1]-pts[i]) for i in range(len(pts)-1))
    return area-400*g
check("L09 A(6)=400", A(6)==400)
best=max(range(0,11), key=lambda g:S(g)); check("L09 integer argmax 6", best==6)
check("L09 S(6)=2700", S(6)==2700); check("L09 S(7)=2650", S(7)==2650)
check("L09 M2 total surplus 1225", (F(1200)*F(7,2)-100*F(7,2)**2)-500*F(7,2)==1225)
check("L09 M1 numbers", F(600-100,5)==100 and F(600-150,5)==90)
check("L09 R2 quantities", F(800-400,10)==40 and abs(float(F(800,15))-53.333)<1e-3)
check("L09 E1 wedge area", F(1,2)*(0+20)*2==20)
print("ALL", "PASS" if ok else "SOME FAIL")
