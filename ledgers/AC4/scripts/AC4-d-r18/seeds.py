import random
def gen(seed,n):
    rng=random.Random(seed); out=[]
    for _ in range(n):
        v=rng.randrange(3000,5001,100); p=v+rng.randrange(500,3001,100)
        K=rng.randrange(6000,12001,500); E=rng.randint(4000,min(9000,K))
        q=rng.randint(1000,8000); r=v+rng.randint(-1500,4000)
        out.append((v,p,K,E,q,r))
    return out
def stats(cases):
    fits=[c for c in cases if c[4]<=c[2]]
    empty=0; feas=0; bind=0
    for v,p,K,E,q,r in fits:
        D=max(0,q+E-K); lo=v+D*(p-v)/q  # exact via fraction below
        from fractions import Fraction
        lo=Fraction(v)+Fraction(D*(p-v),q)
        if lo>r: empty+=1
        else:
            feas+=1
            if D>0: bind+=1
    over=len(cases)-len(fits)
    return over,len(fits),empty,feas,bind
print('seed 20261027 gen-only', stats(gen(20261027,200)))
hits=[]
for s in range(1,41):
    st=stats(gen(s,200))
    if st[1]==186 and st[2]==75: hits.append(s)
    print(s,st)
print('seeds 1-40 with 186 q<=K and 75 empty:',hits)
# boundary check on generated: any with lo==r (equality)?
eq=0
for s in [20261027]:
    for v,p,K,E,q,r in gen(s,200):
        if q<=K:
            D=max(0,q+E-K)
            from fractions import Fraction
            if Fraction(v)+Fraction(D*(p-v),q)==r: eq+=1
print('equality cases in generated seed', eq)
