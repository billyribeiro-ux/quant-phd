from fractions import Fraction as F
# L04 IS-LM
c,c0,b0,b,d,h,tax,G,m = F(3,4),F(1),F(1),F(2),F(1,2),F(1),F(0),F(1),F(2)
def eq(G,m,b):
    A=c0-c*tax+b0+G; D=h*(1-c)+b*d
    return (h*A+b*m)/D, (d*A-(1-c)*m)/D, D
y0,i0,D=eq(G,m,b)
print("L04 A", y0, i0, D, "IS res", y0-(c0+c*(y0-tax)+b0-b*i0+G), "LM res", d*y0-h*i0-m)
for g in (F(11,10),F(2)):
    y1,i1,_=eq(g,m,b); print("L04 B G->",g,"dY",y1-y0,"mult",(y1-y0)/(g-G),"di",i1-i0,"ratio dI/dY",(i1-i0)/(y1-y0))
y1,i1,_=eq(G,F(5,2),b); print("L04 C dY",y1-y0,"mult",(y1-y0)/F(1,2),"di/dm",(i1-i0)/F(1,2))
y0b,_,_=eq(G,m,F(0)); y1b,_,_=eq(F(2),m,F(0)); print("L04 D mult b=0",(y1b-y0b))
print("L04 E3 share", h*(1-c)/D, "benchmark share", (F(4,5))/4)
# L05 AD-AS
a,eta,nu,yb,pe=F(1160),F(100),F(200),F(1000),F(1)
p=(a-yb+nu*pe)/(eta+nu); print("L05 A P,Y",p,a-eta*p)
p1=(a+30-yb+nu*pe)/(eta+nu); print("L05 B dP",p1-p,"dY",(a+30-eta*p1)-(a-eta*p))
for s in (50,100,200,400,800):
    s=F(s); print("L05 D nu",s,"share",s/(eta+s),"dP",F(30)/(eta+s),"dY",F(30)*s/(eta+s))
print("L05 C LR", (a-yb)/eta, (a+30-yb)/eta)
print("L05 R2", (F(1190)-yb+nu*F(13,10))/(eta+nu), F(1190)-eta*((F(1190)-yb+nu*F(13,10))/(eta+nu)))
print("L05 M1", (F(1100)-yb+F(100)*F(11,10))/F(200), "M2 share", F(150,200), "M3", (F(1140)-yb)/eta)
# L06 Phillips
kap,nuP,un,P0,pi0=F(200),F(200),F(5,100),F(6,5),F(3,100)
beta=kap/(nuP*P0); print("L06 beta",beta)
pe=P0*(1+pi0); u=F(6,100); Pn=pe-kap*(u-un)/nuP
print("L06 A pi levels",(Pn-P0)/P0, "phillips", pi0-beta*(u-un), "13/600", F(13,600))
print("L06 misc", F(5,6)*F(1,100), F(5,6)*F(-1,100), F(5,6)*F(-2,100), F(5,6)*F(1,200))
print("L06 R2 v/beta", F(1,100)/(F(5,6)), "L06 M2", F(200)/(F(200)*F(5,4))*F(-1,100))
