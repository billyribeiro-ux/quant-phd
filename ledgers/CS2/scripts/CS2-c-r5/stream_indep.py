import random, math
from fractions import Fraction
def sk(xs, eps):
    levels=[]; comp=0
    def cap(h): return 2*math.ceil(Fraction((h+1)*(h+2),1)/(2*eps))
    def push(h,x):
        nonlocal comp
        while len(levels)<=h: levels.append([])
        levels[h].append(x)
        if len(levels[h])==cap(h):
            buf=sorted(levels[h]); levels[h]=[]; comp+=1
            for y in buf[1::2]: push(h+1,y)
    for x in xs: push(0,x)
    return sum(len(b) for b in levels), comp
for seed in (2026, 1, 7, 99999):
    r=random.Random(seed); xs=[r.random() for _ in range(5000)]
    print('seed',seed, 'eps1/20 stored,comp', sk(xs,Fraction(1,20)), 'eps1/10', sk(xs,Fraction(1,10)))
r=random.Random(5); xs=[r.random()*1e6 for _ in range(5000)]; print('scaled, sorted input', sk(sorted(xs),Fraction(1,20)), sk(xs,Fraction(1,20)))
