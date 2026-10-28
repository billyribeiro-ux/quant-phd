# Recompute Theorem 2.3 (closed binomial sum) and compare with backward induction; Lemma 2.2 boundary; r=0 witness.
import math
from math import comb
S,K,r,t,s=100.0,100.0,0.05,1.0,0.2
def tree_bi(n):
    h=t/n; u=math.exp(s*math.sqrt(h)); d=1/u; R=math.exp(r*h); q=(R-d)/(u-d)
    vals=[max(S*u**j*d**(n-j)-K,0.0) for j in range(n+1)]
    for _ in range(n): vals=[(q*vals[j+1]+(1-q)*vals[j])/R for j in range(len(vals)-1)]
    return vals[0]
def thm23(n):
    h=t/n; u=math.exp(s*math.sqrt(h)); d=1/u; R=math.exp(r*h); q=(R-d)/(u-d)
    return math.exp(-r*t)*sum(comb(n,k)*q**k*(1-q)**(n-k)*max(S*u**k*d**(n-k)-K,0.0) for k in range(n+1))
for n in (1,2,5,20,100):
    print(n, tree_bi(n), thm23(n), abs(tree_bi(n)-thm23(n)))
# Lemma 2.2 boundary: condition h < s^2/r^2 with h = t/n
for n in (1,2,5,10):
    h=t/n; u=math.exp(s*math.sqrt(h)); d=1/u; R=math.exp(r*h)
    print("n",n,"0<d<R<u", 0<d<R<u, "h<s2/r2", h<s*s/(r*r))
# Witness: r = 0, condition h < sigma^2/r^2 is undefined (division by zero)
try:
    print(s*s/(0.0*0.0))
except ZeroDivisionError as e:
    print("r=0 -> ZeroDivisionError in h < sigma^2/r^2")
# r=0 tree still gives 0<d<R<u for any h (so theorem holds but its stated condition is undefined)
h=0.25; u=math.exp(s*math.sqrt(h)); d=1/u; R=1.0
print("r=0 h=0.25 0<d<R<u:", 0<d<R<u)
