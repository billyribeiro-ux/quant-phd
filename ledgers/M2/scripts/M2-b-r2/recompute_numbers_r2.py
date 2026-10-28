from fractions import Fraction as F
from decimal import Decimal, getcontext
getcontext().prec=60
print("L07 ratio", 0.0010414286/0.0034714286, 0.0010414286/0.0034714286-0.3)
print("L07 exact ratio of printed", F('0.0010414286')/F('0.0034714286'))
print("L11 2/(3*816^2)", 2/(3*816**2), "N=817", 2/(3*817**2), "816^2*3", 3*816**2, "2/(3N^2)<=1e-6 at 816:", 2/(3*816**2)<=1e-6)
print("L11 residual", 2.6666666667-2.6666666663)
for n in (50,51):
    print("n",n,"(3n+1)/(6n^2)", F(3*n+1,6*n*n), float(F(3*n+1,6*n*n)), "(3n-1)/6n^2",float(F(3*n-1,6*n*n)))
print("U128", float(F(129*257,6*128*128)), float(F(385,98304)), F(385,98304)==F(129*257,6*128*128)-F(1,3))
print("U128 decimal check", 0.33724976-1/3, 385/98304)
# L09 Riemann check over uniform partitions of x^2: sup/inf for monotone x^2
def U(n): return sum(F(k,n)**2 for k in range(1,n+1))/n  # right endpoint upper for increasing
def L(n): return sum(F(k-1,n)**2 for k in range(1,n+1))/n
for n in (50,51,100):
    print(n, float(U(n)-F(1,3)), float(F(1,3)-L(n)), float(max(U(n)-F(1,3),F(1,3)-L(n))))
print("L09 U128", float(U(128)))
print("L08 1-(3/4)^(1/4)", 1-(0.75)**0.25, "(1/2)^(1/5)", 0.5**0.2, 1-0.5**0.2,"0.7^(1/7)", 0.7**(1/7), 1-0.7**(1/7))
