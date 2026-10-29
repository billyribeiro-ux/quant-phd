"""Round 5 FC2-d: re-derive the numbers printed on FC2 cards with independent float/Decimal arithmetic."""
import math
from decimal import Decimal, getcontext
getcontext().prec = 50
def N(x):  # standard normal CDF
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))
S, K, r, sig, tau = 100.0, 100.0, 0.05, 0.2, 1.0
d1 = (math.log(S/K) + (r + sig*sig/2)*tau) / (sig*math.sqrt(tau)); d2 = d1 - sig*math.sqrt(tau)
C = S*N(d1) - K*math.exp(-r*tau)*N(d2)
print("c109 BS call", round(C, 6), "cents", round(C*100, 2), "N(d1)", round(N(d1), 6), "N(d2)", round(N(d2), 6), "d1", round(d1,6), "d2", round(d2,6))
print("c118 put", round(C - S + K*math.exp(-r*tau), 6))
print("c126 L", round(K*0 + S - K*math.exp(-r*tau), 6), "c131 120e^-0.05", round(120*math.exp(-0.05), 4))
def tree(n, S=100.0, K=100.0, r=0.05, sig=0.2, tau=1.0):
    h = tau/n; u = math.exp(sig*math.sqrt(h)); d = 1/u; R = math.exp(r*h); q = (R-d)/(u-d)
    v = [max(S*u**k*d**(n-k)-K, 0.0) for k in range(n+1)]
    for _ in range(n):
        v = [(q*v[k+1]+(1-q)*v[k])/R for k in range(len(v)-1)]
    return v[0], u, d, R, q
for n in (1, 2, 4, 5, 10, 25, 50, 100, 200, 400):
    p, u, d, R, q = tree(n)
    print("n", n, "tree", round(p, 9), "err_cents", round((p - C)*100, 6))
p4, u, d, R, q = tree(4)
print("c115 4-step u d R q", round(u,6), round(d,6), round(R,6), round(q,6), "h", 0.25, "sigma^2/r^2", 0.04/0.0025)
p1, u1, d1_, R1, q1 = tree(1)
print("c116 1-step u q V1", round(math.exp(0.2),6), round(q1,6), round(p1,6))
# c027: value of fair forward after 0.25y, spot 5300, fair price 5000 e^{0.025}
F = 5000*math.exp(0.05*0.5)
print("c027 value cents", round(5300 - F*math.exp(-0.05*0.25), 4), "fair F", round(F, 6))
print("c021 forward", round(50*math.exp(0.025), 6))
print("c024 quote 5200 minus fair", round(5200 - F, 4))
print("c076 put bound", round(100*math.exp(-0.1) - 50, 4))
# c110 unrounded 2-step error in cents
p2 = tree(2)[0]; print("c110 2-step unrounded error cents", round((p2 - C)*100, 4))
# c117 400-step unrounded error
p400 = tree(400)[0]; print("c117 400-step error currency", round(p400 - C, 7), "cents", round((p400-C)*100, 5))
# c125 bisection halvings
W, tol = 10 - 1e-6, 1e-10
k = 0
while W / 2**k > tol: k += 1
print("c125 halvings", k, "width at 36", 10/2**36, "width at 37", 10/2**37)
print("c123 ceil log2 check", math.ceil(math.log2(10/1e-10)))
# c112 algebra check d1 split
print("c112 split", abs(d1 - ((math.log(S/K)+r*tau)/(sig*math.sqrt(tau)) + sig*math.sqrt(tau)/2)) < 1e-12)
# c106 check: h < sigma^2/r^2 with (u,d) ordering: d<R<u
for n in (1, 2, 4, 400):
    h = tau/n; u_ = math.exp(sig*math.sqrt(h)); d_ = 1/u_; R_ = math.exp(r*h)
    print("c106 n", n, "d<R<u", d_ < R_ < u_, "h<s2/r2", h < sig*sig/(r*r))
