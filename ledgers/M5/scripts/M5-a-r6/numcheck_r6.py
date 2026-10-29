from fractions import Fraction as F
import math
# hub: placement percentages
print("7/9 =", round(100*7/9, 4), " 8/9 =", round(100*8/9, 4))
print("1/1.05 =", 1/1.05, " |diff to 0.952381| =", abs(1/1.05-0.952381), "tol 0.001 ok:", abs(1/1.05-0.952381) <= 0.001)
print("sum k=0..3 2^k =", sum(2**k for k in range(4)))
print("sum n=0..4 (1/2)^n =", sum(F(1,2**n) for n in range(5)))
# L01 E1 / E2
a,b=F(181,128),F(2897,2048)
print("a^2<2:", a*a<2, " b^2>=2:", b*b>=2, " width:", b-a, " = 1/2048:", b-a==F(1,2048))
print("181^2, 2*128^2:", 181**2, 2*128**2, " 2897^2, 2*2048^2:", 2897**2, 2*2048**2)
print("first n with 2^(1-n) < 1/1000:", min(n for n in range(1,100) if F(2,2**n) < F(1,1000)))
# L01 quiz: 7/5 in S, 3/2 upper bound
print("(7/5)^2<2:", F(7,5)**2<2, " (3/2)^2>=2:", F(3,2)**2>=2, " 1001 least n>1000.5:", math.floor(1000.5)+1)
# L01 bisection: check widths and brackets independently
S=lambda x: x>=0 and x*x<2
lo,hi=F(0),F(2)
ok=True
for n in range(1,13):
    m=(lo+hi)/2
    lo,hi=(m,hi) if S(m) else (lo,m)
print("step12:",lo,hi, hi-lo)
# L02 numbers
H=lambda n: sum(F(1,k) for k in range(1,n+1))
print("H2-H1",H(2)-H(1)," H4-H2",H(4)-H(2), " min gap N1..200 at N:", min((H(2*n)-H(n),n) for n in range(1,201)))
print("pairs 0<=n<m<=60:", sum(1 for n in range(0,60) for m in range(n+1,61)))
print("threshold N s.t. G-tail bound 2^-n <= 2^-10 for n>=N:", min(N for N in range(0,30) if F(1,2**N)<=F(1,2**10)))
print("G3", F(1,2)+F(1,4)+F(1,8), " G3-G1", (F(1,2)+F(1,4)+F(1,8))-F(1,2))
# L03 numbers
X0=F(2)
pts=[X0+F(k,200) for k in range(-200,201)]
print("grid", len(pts), "bound holds", sum(abs(x*x-4)<=5*abs(x-X0) for x in pts))
print("delta=1/50 admits", [k for k in range(-200,201) if abs(F(k,200))<F(1,50)])
fails=[x for x in pts if abs(x-X0)<F(1,10) and abs(x*x-4)>=F(1,10)]
print("count fail(1/10)", len(fails), " first", fails[0], abs(fails[0]**2-4))
pos=[k for k in range(1,20) if abs((X0+F(k,200))**2-4)>=F(1,10)]
neg=[k for k in range(-19,0) if abs((X0+F(k,200))**2-4)>=F(1,10)]
print("E3 positive k:", pos[0], pos[-1], len(pos), " negative k:", neg[0], neg[-1], len(neg))
print("E1 bound at 381/200:", abs(F(381,200)**2-4), 5*abs(F(381,200)-2), float(abs(F(381,200)**2-4)))
print("E3 values k=4,5 (k>0):", float(4*(4+F(4,200))), float(5*(4+F(5,200))), " j=5,6:", float(5*(4-F(5,200))), float(6*(4-F(6,200))))
