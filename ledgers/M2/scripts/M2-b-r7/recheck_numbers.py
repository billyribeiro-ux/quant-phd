import math
from fractions import Fraction as Fr
# L07 E1
print("L07 E1 ratio", 0.0010414286/0.0034714286, abs(0.0010414286/0.0034714286-0.3)/0.3)
# L07 E2 at x=-1/2 tolerance 1e-3
for n in range(7,11):
    print("L07 E2 n",n, (2/3)*(0.5)**(n+1))
# L07 R2 smallest n with 2^n>=1e6
n=0
while 2**n < 10**6: n+=1
print("L07 R2 n", n)
# L08 E1, E2, Ex 2.4 etc
print("L08 xi x=.5 n=3", 1-(0.5)**(1/5))
print("L08 xi x=.3 n=5", 1-(0.7)**(1/7))
print("L08 1-(3/4)^(1/4)", 1-(0.75)**0.25)
print("L08 1-(3/4)^(1/4) 7dp", round(1-(0.75)**0.25,7))
for n in range(1,5):
    print("L08 E3 n",n, 0.6**(n+1)/0.4**(n+2), 0.6**(n+1)/0.4)
# L08 part C rows
for x in (0.1,0.3,0.5,0.9):
    for n in (1,3,5):
        xi=1-(1-x)**(1/(n+2)); R=x**(n+1)/(1-x)
        print(f"L08C {x} {n} {xi:.6f} {R:.8f}")
# L09 numbers
print("L09 E2", 1/(12*256), 1/3072)
print("L09 E3 n=50", 151/15000, "n=51", 154/15606, "n=50 vs n=51 (3n+1)/(6n^2)")
print("L09 B gap", )
pts=[Fr(i*i,100) for i in range(11)]
w=[pts[i]-pts[i-1] for i in range(1,11)]
U=sum(pts[i]**1*0+ (pts[i]*0) for i in range(0))
Up=sum(float(pts[i])**2*float(w[i-1]) for i in range(1,11))
Lo=sum(float(pts[i-1])**2*float(w[i-1]) for i in range(1,11))
print("L09 B U-L", Up-Lo, "mesh", float(max(w)))
# L10 E3 rounding model
x=0.3; h=1e-6
F3=6/(1.3**4); print("F'''",F3, "trunc", h*h*F3/6)
ulp03=math.ulp(0.3); print("half ulp 0.3", ulp03/2)
ulp13=math.ulp(1.3); print("half ulp 1.3", ulp13/2)
ulp023=math.ulp(0.23); print("half ulp .23", ulp023/2)
print("F(0.3)=", 0.3/1.3, "F'(0.3)", 1/1.3**2, "dF/dd", 0.3/1.3**2)
# observed central diff error
F=lambda t: t/(1+t)
c=(F(x+h)-F(x-h))/(2*h)
print("central", c, "exact", 1/1.3**2, "obs err", c-1/1.3**2)
# L10 E3 bound per the solution
print("rounding bound", 2*(1.6e-17+2.0e-17+1.4e-17)/(2*h))
# L11 E1
for N in (816,817):
    print("L11 E1 N",N, 2/(3*N*N))
print("L11 E1 N^2>=", 2/(3*1e-6))
# L11 E2
print("L11 residual", 8/3-2.6666666663)
# L12 numbers
print("L12 H16384-1", sum(1/k for k in range(2,16385)))
print("L12 H2^14 -1 vs m/2", sum(1/k for k in range(2,16385))-7)
