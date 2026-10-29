import math
phi=(1+math.sqrt(5))/2
print("ln377",math.log(377),"lnphi",math.log(phi),"ln377/lnphi",math.log(377)/math.log(phi))
print("ln8/lnphi",math.log(8)/math.log(phi),"ln3/lnphi",math.log(3)/math.log(phi))
print("log_phi65",math.log(65)/math.log(phi),"log_phi501",math.log(501)/math.log(phi))
print("1/log2phi",1/math.log2(phi), "ln2?", math.log2(phi))
print("272/500",272/500, "63+53+2*(55+57)",63+53+2*(55+57))
N=[0,1]
for h in range(2,13): N.append(1+N[h-1]+N[h-2])
for h in range(0,13): print(h,N[h], round(phi**h,4), (N[h]+1)>=phi**h)
print("phi^2-phi-1",phi*phi-phi-1, "phi<2",phi<2)
print("ln(1+sqrt5)^2/4 check", (1+math.sqrt(5))**2/4 - (phi+1))
# independent AVL: recursive build from sorted with height tracking; insertion by rebuilding via dict-based implementation
def ins(t,k):
    # t: None or (key,left,right); returns new tree with rebalance, nodes as tuples; height via function
    def H(t): return 0 if t is None else t[3]
    def mk(k,l,r): return (k,l,r,1+max(H(l),H(r)))
    def bf(t): return H(t[1])-H(t[2])
    def rl(t):
        x=t[2]; return mk(x[0],mk(t[0],t[1],x[1]),x[2])
    def rr(t):
        x=t[1]; return mk(x[0],x[1],mk(t[0],x[2],t[2]))
    if t is None: return (k,None,None,1)
    if k<t[0]: t=mk(t[0],ins(t[1],k),t[2])
    else: t=mk(t[0],t[1],ins(t[2],k))
    b=bf(t)
    if b>1:
        if bf(t[1])<0: t=mk(t[0],rl(t[1]),t[2])
        t=rr(t)
    elif b<-1:
        if bf(t[2])>0: t=mk(t[0],t[1],rr(t[2]))
        t=rl(t)
    return t
t=None
for k in range(1,65): t=ins(t,k)
print("AVL height 1..64 sorted:", t[3])
import random
rng=random.Random(20261028)
keys=rng.sample(range(1,1_000_000),500)
t=None
for k in keys: t=ins(t,k)
print("AVL final height random 500 (independent, different seed use is same sample):",t[3])
