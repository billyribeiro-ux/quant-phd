import math
from fractions import Fraction as Fr
# L02 Example 2.4 / M1 / M2 / M3 / E3 / P1-style checks
F = 50 * math.exp(0.025); print("L02 Ex2.4 F*=", F, "to cent", round(F, 2), "cents", round(5000*math.exp(0.025), 2))
print("L02 C: quote - fair =", 5200 - 5000*math.exp(0.025))
Fair = 5000*math.exp(0.025)
print("L02 E3 value =", 5300 - Fair*math.exp(-0.0125), " e^-0.0125=", math.exp(-0.0125))
print("L02 M2 F*=", 80*math.exp(0.01), " profit=", 81-80*math.exp(0.01))
print("L02 M3 value=", 104 - 100*math.exp(-0.015), " e^-0.015=", math.exp(-0.015))
print("L02 P1 identity check (S - I e^{-r t1}) e^{r tau} vs S e^{r tau} - I e^{r(tau-t1)} with S=50,I=1,r=.05,t1=.25,tau=.5:")
S_,I_,r_,t1,tau = 50.0,1.0,0.05,0.25,0.5
print("   ", (S_ - I_*math.exp(-r_*t1))*math.exp(r_*tau), S_*math.exp(r_*tau) - I_*math.exp(r_*(tau-t1)))
# L03 Lab numbers: zero rates 3,3.5,4,4.5,5 percent; DF_i=(1+z_i)^-i
z = [Fr(3,100), Fr(7,200), Fr(4,100), Fr(9,200), Fr(5,100)]
DF = [Fr(1)] + [1/(1+zi)**i for i,zi in enumerate(z,1)]
ann = sum(DF[1:], Fr(0)); par = (1-DF[-1])/ann
print("L03 DF1..5 =", [round(float(d),6) for d in DF[1:]], "par=", float(par), "par% =", round(float(par)*100, 4))
print("L03 par not one of typed rates:", all(par != zi for zi in z))
N = 100_000_000
val = (par - (par + Fr(1,100))) * ann * N
import math as m
print("L03 value to payer 1pp above par (cents) exact =", float(val), "round-half-up:", m.floor(val + Fr(1,2)))
print("L03 fixed payment cents =", m.floor(par*N + Fr(1,2)))
# L03 M3 check
ds = [1/1.06, 1/1.06**2, 1/1.06**3]
print("L03 M3 sum DF =", sum(ds), "value on 100 =", 100*(0.06-0.05)*sum(ds))
# L03 M2 DF3
print("L03 M2 DF3 =", 1/1.06**3, 1.06**3)
# L03 E3 par rate and payment
print("L03 E3 payment dollars =", 4902625/100)
# L03 Lab A: margin path sanity
path=[5000,5039,5070,5104,5069,5103,5090,5054,5077,5106,5084]
m_=[path[i]-path[i-1] for i in range(1,len(path))]
print("L03 A margins", m_, "sum", sum(m_), "losses", sum(1 for x in m_ if x<0), "balances", [path[i]-path[0] for i in range(1,len(path))])
print("L03 P3 eta counterexample: B_n=(1+eta)^(n-1) =1 only eta=0 for n>=2 (verified analytically)")
# L02 cards c021 numbers
print("c021:", 50*math.exp(0.025), round(50*math.exp(0.025),2))
# L01 cards
print("c008 psi:", Fr(1,20), Fr(17,20), Fr(1,20)+Fr(17,20))
print("c013 cost of (-5,9) at bond 9/10 stock 1/2:", Fr(-5,1)*Fr(9,10)+9*Fr(1,2), "payoff u:", -5+9*3, "d:", -5+9*1)
print("c011 cost:", 1 - 2*Fr(9,10), "payoff u:", -2*1+1*3, "d:", -2+1)
print("c138 psi_u at q=1/2:", (Fr(1,2)-Fr(9,10))/2, "psi_d:", (Fr(27,10)-Fr(1,2))/2)
print("c164 det:", 1*1-1*3)
