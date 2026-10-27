import math
from scipy import stats, optimize
from scipy.stats import norm
Phi_inv = norm.ppf
print("M1(a) bound =", round(math.sqrt(2*math.log(20))*(1/math.sqrt(756))*math.sqrt(252), 4))
br = 0.4228*Phi_inv(0.95) + 0.5772*Phi_inv(1-1/(20*math.e))
print("M1(b) Phi^-1(0.95)=%.4f Phi^-1(1-1/(20e))=%.4f bracket=%.4f est=%.4f" % (Phi_inv(0.95), Phi_inv(1-1/(20*math.e)), br, br*(1/math.sqrt(756))*math.sqrt(252)))
Z = 60/math.sqrt(504)
M = math.sqrt(252/756)*math.exp(60**2/(2*756))
b = math.sqrt(756*(2*math.log(20)+math.log(3)))
print("M4(a) Z=%.4f  (1.960 cut)" % Z, " M4(b) M504=%.4f b504=%.4f" % (M, b))
print("M4(c) C=[%.5f, %.5f] annualized [%.2f, %.2f] point %.2f; fixed half-width %.5f" % ((60-b)/504, (60+b)/504, math.sqrt(252)*(60-b)/504, math.sqrt(252)*(60+b)/504, math.sqrt(252)*60/504, 1.959964/math.sqrt(504)))
# M5
l = 2*math.log(20)
u = optimize.brentq(lambda u: u - l - math.log(1+u), 1, 50)
print("M5 l=%.6f u*=%.6f sqrt(1+u*)=%.6f kappa=756/u*=%.4f" % (l, u, math.sqrt(1+u), 756/u))
# L02 M3
for m in (10, 100, 1000):
    crit = Phi_inv(1-0.025/m*2/2 if False else 1-0.05/(2*m))
    crit2 = Phi_inv(1-0.05/(2*m))
    bound = math.sqrt(2*math.log(m*10)) if False else None
for m, bnd_n in ((10, 100), (100, 1000), (1000, 10000)):
    c = Phi_inv(1-0.05/(2*m))
    print("L02-M3 m=%d crit=%.6f bound sqrt(2 ln %d)=%.6f overstate=%.4f" % (m, c, bnd_n, math.sqrt(2*math.log(bnd_n)), math.sqrt(2*math.log(bnd_n))-c))
# Ex 4.2 power
for m in (1, 10, 100, 1000):
    c = Phi_inv(1-0.05/(2*m))
    print("Ex4.2 m=%d crit=%.4f power=%.6f" % (m, c, norm.cdf(3.5-c)))
