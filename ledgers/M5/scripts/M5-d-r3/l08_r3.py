import sys, re, random, math
src = open('/tmp/verifyB3-M5-d/tests/labs/M5/lab-M5-L08-1.py', encoding='utf-8').read()
src = src.rsplit('\nmain()', 1)[0]
ns = {'__name__': 'labmod'}
exec(compile(src, 'lab-M5-L08-1.py', 'exec'), ns)
bellman, GRID, BETA, SEED, PAIRS = ns['bellman'], ns['GRID'], ns['BETA'], ns['SEED'], ns['PAIRS']
rng = random.Random(SEED); worst = 0.0
for _ in range(PAIRS):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]; w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = bellman(v, GRID, BETA); bw, _ = bellman(w, GRID, BETA)
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True)); den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    worst = max(worst, num / den)
print('L08 partB worst repr', repr(worst), 'minus beta', worst - BETA, 'in ulps-ish', (worst-BETA)/2.220446049250313e-16)
print('seed', SEED, 'pairs', PAIRS, 'grid', GRID, 'beta', BETA)
