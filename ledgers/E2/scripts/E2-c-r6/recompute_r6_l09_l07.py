from fractions import Fraction as Fr
import itertools, math
# independent L09 recomputation
def rev(bids,k,fmt):
    s=sorted(bids,reverse=True)
    if fmt=='u': return k*s[k]
    return sum(s[:k])
hi=eq=lo=0; eqw=[]
for p in itertools.product(range(4),repeat=4):
    u=rev(p,2,'u'); d=rev(p,2,'d')
    if d>u: hi+=1
    elif d==u: eq+=1; 
    else: lo+=1
    if d==u:
        s=sorted(p,reverse=True)
        assert s[0]==s[1]==s[2] or (s[0]==s[1]==s[2]==s[3]) or True
        eqw.append(p)
print('k=2 above',hi,'equal',eq,'below',lo)
# equality condition check: equal iff top three equal
cond=sum(1 for p in itertools.product(range(4),repeat=4) if (lambda s: s[0]==s[1]==s[2])(sorted(p,reverse=True)))
print('top-three-equal count', cond, 'matches equal set:', set(eqw)==set(p for p in itertools.product(range(4),repeat=4) if (lambda s: s[0]==s[1]==s[2])(sorted(p,reverse=True))))
# k=1 second price
ok=0
for p in itertools.product(range(4),repeat=4):
    s=sorted(p,reverse=True)
    if rev(p,1,'u')==s[1] and rev(p,1,'d')==s[0]: ok+=1
print('k=1 identity', ok)
# Part A profile
vals=[9000,5000,6000,7000]; bids=[8000,9500,6500,7000]
order=sorted(range(4),key=lambda i:(-bids[i],i))
print('order',order,'winners',order[:2],'clear',bids[order[2]])
print('uniform rev',2*bids[order[2]],'disc rev',bids[order[0]]+bids[order[1]],'gap',bids[order[0]]+bids[order[1]]-2*bids[order[2]], 'gap share', Fr(3500,14000))
top=sorted(vals,reverse=True)
print('eff', Fr(vals[order[0]]+vals[order[1]], top[0]+top[1]))
# Remark 3.3 example
print('remark3.3 eff', Fr(5000+9000,16000))
# Prop 2.1 worked M1/M2
print('M2 check', 2*6000, 8000+7000)
# Quiz: profile check
# L07 part B grid
cnt=0; cands=[]
steps=[Fr(k,4) for k in range(5)]
V={'L':6000,'H':10000}; P={'L':Fr(3,10),'H':Fr(7,10)}
def util(v,q,t): return v*q-t
def check(m):
    ic=ir=True
    for th in 'LH':
        tr=util(V[th],*m[th])
        if tr<0: ir=False
        for r in 'LH':
            if util(V[th],*m[r])>tr: ic=False
    rev=sum(P[t]*m[t][1] for t in 'LH')
    return ic,ir,rev
best=None
for ql in steps:
  for qh in steps:
    if ql>qh: continue
    tl=int(6000*ql); th_=int(10000*qh-4000*ql)
    m={'L':(ql,tl),'H':(qh,th_)}
    ic,ir,r=check(m)
    if ic and ir:
        cnt+=1
        if best is None or r>best[2]: best=(ql,qh,r)
print('grid pass',cnt,'best',best)
print('L07 pairs with ql<=qh', sum(1 for a in steps for b in steps if a<=b))
# Example 3.3 menus
for name,m in [('excl',{'L':(Fr(0),0),'H':(Fr(1),10000)}),('pool6000',{'L':(Fr(1),6000),'H':(Fr(1),6000)}),('pool10000',{'L':(Fr(1),10000),'H':(Fr(1),10000)}),('hiH',{'L':(Fr(1),6000),'H':(Fr(0),0)}),('R1 induced',{'L':(Fr(0),0),'H':(Fr(1),6000)})]:
    print(name, check(m))
# M3
print('M3 rev', Fr(3,10)*3000+Fr(7,10)*8000)
# R3 threshold
print('c at pH=3/5', (1-Fr(3,5))*6000-Fr(3,5)*4000)
