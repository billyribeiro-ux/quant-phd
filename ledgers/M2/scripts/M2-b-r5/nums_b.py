from fractions import Fraction as F
import math
print("L08 E2 xi x=0.3 n=5:", 1-0.7**(1/7))
print("L08 E1 xi x=0.5 n=3:", 1-0.5**(1/5), "R:", 0.5**4/0.5)
print("L08 P2 xi x=1/4 n=2:", 1-(0.75)**0.25)
print("L08 E3 bounds:", [ (0.6**(n+1)/0.4**(n+2), 0.6**(n+1)/0.4) for n in range(1,5)])
print("L09 U128-1/3 frac:", F(385,98304), float(F(385,98304)), float(F(1,3)+F(385,98304)))
# L09 part B exact
n=10; pts=[F(i*i,n*n) for i in range(n+1)]
w=[pts[i]-pts[i-1] for i in range(1,n+1)]
U=sum(pts[i]**2*w[i-1] for i in range(1,n+1)); L=sum(pts[i-1]**2*w[i-1] for i in range(1,n+1))
print("L09 partB U-L:", float(U-L), "mesh", float(max(w)))
print("L09 E2 1/(12*256):", 1/(12*256))
print("L09 E3 n=50,51:", F(151,15000), float(F(151,15000)), F(154,15606), float(F(154,15606)))
print("L09 E1 25/384:", 25/384)
# L10 central difference: float value vs exact
x=0.3; h=1e-6
c=((x+h)/(1+x+h)-(x-h)/(1+x-h))/(2*h)
ex=F(3,10)
def Fr(v): return v/(1+v)
cex=(Fr(F(3,10)+F(1,10**6))-Fr(F(3,10)-F(1,10**6)))/(2*F(1,10**6))
print("L10 float central - exact f(0.3):", c-float(1/(1.3)**2), "float central - exact central:", c-float(cex))
print("L10 exact central - f(0.3):", float(cex-1/(F(13,10))**2))
print("L10 F'''(0.3)=6/1.3^4:", 6/1.3**4, "trunc:", 1e-12*6/1.3**4/6)
# L11 E1
for N in (816,817): print("L11 E1", N, 2/(3*N*N))
# L12 values
print("L12 H16384-1:", sum(1/j for j in range(2,16385)))
print("L07 E2 n=8,9:", (2/3)/512, (2/3)/1024)
