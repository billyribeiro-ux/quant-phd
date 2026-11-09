# CS2-c round 5 verifier script: re-derives every unrounded number cited on L09-L11 (independent of the page).
import math, random, bisect
from fractions import Fraction

def stream(offset, n=2000, seed=90):
    rng = random.Random(seed)
    return [offset + rng.random() for _ in range(n)]

def welford(xs):
    c=0; m=0.0; s=0.0
    for x in xs:
        c+=1; d=x-m; m+=d/c; s+=d*(x-m)
    return s/(c-1), s, m

def twopass(xs):
    m=sum(xs)/len(xs); return sum((x-m)**2 for x in xs)/(len(xs)-1)

def naive_parts(xs):
    t=0.0; tq=0.0
    for x in xs:
        t+=x; tq+=x*x
    n=len(xs)
    return (tq - t*t/n)/(n-1), t, tq

def exact(xs):
    v=[Fraction(x) for x in xs]; n=len(v)
    m=sum(v,Fraction(0))/n
    return sum(((x-m)**2 for x in v),Fraction(0))/(n-1), m, v

print("== L09 ==")
for off in (0.0, 1e6, 1e9):
    xs=stream(off)
    ex,mean_ex,vals=exact(xs)
    w,_,_=welford(xs); tp=twopass(xs); nv,tot,totsq=naive_parts(xs)
    rel=lambda est: float(abs(Fraction(est)-ex)/ex)
    print(f"offset {off!r}: exact={float(ex):.17g} exact_sci={float(ex):.13e}")
    print(f"  rel W={rel(w):.6e} TP={rel(tp):.6e} NV={rel(nv):.6e}  ratio NV/W={rel(nv)/rel(w):.6e}")
    print(f"  est W={w:.6e} TP={tp:.6e} NV={nv:.6e}")
    if off==1e9:
        sum_sq_exact=sum((Fraction(x)**2 for x in xs),Fraction(0))
        print(f"  exact sum x^2 = {float(sum_sq_exact):.13e}")
        print(f"  computed running sum_sq = {totsq!r}  diff = {float(Fraction(totsq)-sum_sq_exact):.6e}")
        print(f"  (n-1)*exact var = {1999*float(ex):.6f}  exact var 13dp={float(ex):.13f}")
        print(f"  math.ulp(2e21) = {math.ulp(2e21)!r}  2**18={2**18}")
        print(f"  computed naive: total={tot!r} totsq={totsq!r}")
    if off==0.0:
        print(f"  E2: exact var (unrounded) = {float(ex)!r}; rel W unrounded = {rel(w)!r}; abs err W = {float(abs(Fraction(w)-ex)):.6e}")
        print(f"  E2 product rel*exact = {rel(w)*float(ex):.6e}; printed 9.26e-16*0.087281 = {9.26e-16*0.087281:.6e}")
