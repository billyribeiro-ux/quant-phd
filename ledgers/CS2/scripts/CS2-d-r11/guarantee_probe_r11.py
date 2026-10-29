import sys; sys.path.insert(0, "/tmp/cs2r11probe")
import random, math, importlib, sys
from fractions import Fraction
mods = {n: importlib.import_module(n) for n in ["ref","d8_01_sketch_cap_counts_previous_value","d8_02_sketch_insert_bisect_left","d9_04_sketch_cap_without_plus_one"]}
def check(mod, stream, eps, probes):
    s = mod.QuantileSketch(eps)
    for x in stream: s.add(x)
    n=len(stream); E=Fraction(eps)
    ok=True
    for q in probes:
        v=s.quantile(q); Q=Fraction(q)
        below=sum(1 for x in stream if x < v); atmost=sum(1 for x in stream if x <= v)
        if not (below <= Q*n + E*n and atmost >= Q*n - E*n): return False, (q, v, below, atmost)
    return True, None
rng=random.Random(1)
probes=[0,0.01,0.1,0.25,0.5,0.75,0.9,0.99,1]+[i/101 for i in range(101)]
res={}
for name,mod in mods.items():
    fails=[]
    for trial in range(400):
        n=rng.randint(1,300); eps=rng.choice([0.05,0.1,0.2,0.01,0.3])
        kind=rng.random()
        if kind<0.3: stream=[float(rng.randint(0,20)) for _ in range(n)]
        elif kind<0.5: stream=sorted(rng.uniform(0,1) for _ in range(n))
        else: stream=[rng.uniform(0,1) for _ in range(n)]
        ok,info=check(mod,stream,eps,probes)
        if not ok: fails.append((n,eps,info))
    res[name]=len(fails)
    print(name, 'guarantee violations', len(fails), fails[:2])
