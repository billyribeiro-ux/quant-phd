import math
from fractions import Fraction
# L19 ratios from printed errors
e1=[6.215110e-03,1.573092e-03,3.957416e-04,9.924735e-05]
e2=[1.568275e-04,1.989281e-05,2.504483e-06,3.141716e-07]
print("L19 first ratios", [round(e1[i]/e1[i+1],4) for i in range(3)] if False else [round(e1[i]/e1[i+1],4) for i in range(3)])
print("L19 second ratios", [round(e2[i]/e2[i+1],4) for i in range(3)])
print("L19 hess", math.exp(0.5)/4, math.exp(0.5)+0.5)
# L22 numbers
print("L22 f_xx at a=1.5", -1.5/(1.5)**2, "0.5*0.666667*1e-16=", 0.5*0.666667*1e-16, "0.5*(2/3)*1e-16=", 0.5*(2/3)*1e-16)
print("L22 sqrt eps", math.sqrt(2.220446049250313e-16))
# L22 Part B: V(a)=a^2/4 derivative check and envelope
for a in (1.0,2.0,3.0):
    print("L22 partB a",a,"a/2",a/2)
# L22 Part A printed V' vs ln a at a=1.5 : 
print("ln1.5", math.log(1.5), "ln2", math.log(2), "ln3", math.log(3), "ln4", math.log(4))
# L23 Proposition 2.2 sanity: price with y=0.05, N=10, F=100000
def price(c,N,F,y):
    return sum(yF*(1+y)**(-t) for t,yF in [(t,F*y) for t in range(1,N)]) 
F=100000; y=0.05; N=10
p=sum(F*y*(1+y)**(-t) for t in range(1,N+1))+F*(1+y)**(-N)
print("L23 price at 0.05", p)
# L22 Example 2.3/E1 : value error at distance 1e-8
print("E1 value diff", 0.5*0.666667*(1e-8)**2)
# L22 M3 at a=1: V=a^2/8, V'=a/4=0.25
print("M3 V'(1)", 1/4)
