from fractions import Fraction as F
n=256
L=sum(F(3*(i)**2, n*n) for i in range(0,n))  # placeholder not used
Lsum=sum((3*(F(i,n))**2-2)*F(1,n) for i in range(0,n))
Usum=sum((3*(F(i,n))**2-2)*F(1,n) for i in range(1,n+1))
print('L256', float(Lsum), 'U256', float(Usum), 'U-L', float(Usum-Lsum), 3/256)
xs=[(i/10)**2 for i in range(11)]
import math
d=sum((xs[i]**2-xs[i-1]**2)*(xs[i]-xs[i-1]) for i in range(1,11))
print('U-L nonuniform', f"{d:.8f}", 'mesh', max(xs[i]-xs[i-1] for i in range(1,11)))
print('U128', float(F(129*257,6*128*128)), 'L128', float(F(127*255,6*128*128)))
n=8
M=sum(((2*i-1)/(2*n))**2*(1/n) for i in range(1,n+1))
print('midpoint n=8 err', f"{M-1/3:.8f}")
