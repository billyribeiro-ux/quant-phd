import math
G=[0.25,0.5,0.75,1.0]; A=0.5
def run(beta):
    V=[0.0]*4; n=0
    while True:
        n+=1
        new=[max(math.sqrt(k**A-kp)+beta*V[j] for j,kp in enumerate(G) if kp<=k**A) for k in G]
        gap=max(abs(a-b) for a,b in zip(new,V)); V=new
        if gap<=1e-12: return n
for b in (0.5,0.9,0.95): print("beta",b,"iters",run(b))
V1=[max(math.sqrt(k**A-kp) for kp in G if kp<=k**A) for k in G]
d=max(V1); print("norm V1-V0",d, math.sqrt(3)/2)
n=0
while 0.9**n/(0.1)*d>1e-6: n+=1
print("apriori n",n, "bound n-1", 0.9**(n-1)/0.1*d, "bound n", 0.9**n/0.1*d)
