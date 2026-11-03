import importlib.util, itertools, random, sys
from fractions import Fraction
from bisect import bisect_right, bisect_left
import math
BASE = '/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/ledgers/CS2/equivalent/'
REF = '/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader/reference.py'
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
mods = {'reference': load(REF, 'ref'),
        'd8_01': load(BASE + 'd8_01_sketch_cap_counts_previous_value.py', 'd801'),
        'd9_04': load(BASE + 'd9_04_sketch_cap_without_plus_one.py', 'd904'),
        'd8_02': load(BASE + 'd8_02_sketch_insert_bisect_left.py', 'd802'),
        'rank_target_without_clamp': load(BASE + 'rank_target_without_clamp.py', 'rtw')}
def guarantee(stream, v, q, eps):
    qn = Fraction(q) * len(stream); slack = Fraction(eps) * len(stream)
    below = sum(1 for x in stream if x < v); atb = sum(1 for x in stream if x <= v)
    return below <= qn + slack and atb >= qn - slack
probes = [Fraction(k, 40) for k in range(41)]
results = {}
def check(name, streams):
    m = mods[name]; bad = 0; checks = 0
    for stream, eps in streams:
        sk = m.QuantileSketch(eps); seen = []
        for x in stream:
            sk.add(x); seen.append(x)
            for q in probes:
                checks += 1
                v = sk.quantile(float(q))
                if not guarantee(seen, v, Fraction(float(q)), eps):
                    bad += 1
    return checks, bad
# exhaustive small streams over {0,1,2}, length 1..7
streams = []
for L in range(1, 8):
    for t in itertools.product([0.0, 1.0, 2.0], repeat=L):
        for eps in (0.05, 0.1, 0.2, 0.3):
            streams.append((list(t), eps))
rng = random.Random(4242)
for _ in range(400):
    L = rng.randint(1, 80)
    s = [round(rng.uniform(0, 10), rng.choice([0, 1, 6])) for _ in range(L)]
    if rng.random() < 0.3:
        s = [float(rng.randint(0, 3)) for _ in range(L)]
    streams.append((s, rng.choice([0.05, 0.1, 0.2, 0.3])))
for name in ['reference', 'd8_01', 'd9_04', 'd8_02', 'rank_target_without_clamp']:
    if name == 'rank_target_without_clamp':
        print(name, 'skipped here (sketch identical except target; see target equivalence check)')
        continue
    c, b = check(name, streams)
    print(f'{name}: streams {len(streams)}, guarantee checks {c}, violations {b}')
# target equivalence for m14_01: compare quantile answers with and without clamp
ref = mods['reference']; mut = mods['rank_target_without_clamp']
diff = 0; tot = 0
for stream, eps in streams[:20000]:
    a = ref.QuantileSketch(eps); b = mut.QuantileSketch(eps)
    for x in stream:
        a.add(x); b.add(x)
        for q in probes:
            tot += 1
            if a.quantile(float(q)) != b.quantile(float(q)):
                diff += 1
print('rank_target_without_clamp vs reference: queries', tot, 'differences', diff)
