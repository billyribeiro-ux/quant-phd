import math, random
G = (0.25, 0.5, 0.75, 1.0); A = 0.5; BETA = 0.9
def B(vals, beta, grid=G):
    out=[]
    for k in grid:
        o = k**A
        out.append(max(math.sqrt(o-kp)+beta*vals[j] for j,kp in enumerate(grid) if kp<=o))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
rng = random.Random(20261028); worst = 0.0
for _ in range(2000):
    v=[rng.uniform(-10.0,10.0) for _ in G]; w=[rng.uniform(-10.0,10.0) for _ in G]
    worst = max(worst, sd(B(v,BETA),B(w,BETA))/sd(v,w))
print("L08 worst ratio %.17g" % worst, "excess over beta %.4e" % (worst-BETA), "ulp(0.9)=%.4e" % (math.ulp(0.9)), "excess/ulp", (worst-BETA)/math.ulp(0.9))
# L09 four-point grid: ||V1-V0|| and a priori bound
v1 = B([0.0]*4, 0.9)
c = sd(v1,[0.0]*4)
print("L09 ||V1-V0|| %.10f  sqrt3/2 %.10f" % (c, math.sqrt(3)/2))
for n in (151,152):
    print("L09 n", n, "apriori bound %.6e" % (0.9**n/(1-0.9)*c))
n=0
while 0.9**n/(1-0.9)*c > 1e-6: n+=1
print("L09 least n with bound<=1e-6:", n)
# L09 naive stop: step, actual error
G9 = G
beta=0.9
prev=[0.0]*4; vals=[0.0]*4; k=0
tol=1e-6
while True:
    new=B(vals,beta); k+=1
    step=sd(new,vals); vals=new
    if step<=tol: break
ref=[0.0]*4
for _ in range(100000):
    nxt=B(ref,beta)
    if beta/(1-beta)*sd(nxt,ref)<=1e-12: ref=nxt; break
    ref=nxt
print("L09 naive stop n", k, "step %.10e" % step, "err_vs_ref %.10e" % sd(vals, ref), "9*step %.10e" % (9*step), "err/step", sd(vals,ref)/step)
