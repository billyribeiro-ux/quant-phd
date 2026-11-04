"""Re-derive the numeric claims of PC3 cards c087-c100, c142-c146, c169-c170 with the lab twin's own functions.

Usage: python -I ledgers/PC3/scripts/PC3-d-r6/l05_card_checks_r6.py <checkout>
"""
import contextlib
import importlib.util
import io
import pathlib
import random
import sys

root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("lab05", root / "tests/labs/PC3/lab-PC3-L05-1.py")
lab = importlib.util.module_from_spec(spec)
sys.modules["lab05"] = lab
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(lab)  # the twin calls main() at import; output is discarded here

# c093: x=(3,1,4,1,5), k=3 -> (4,4,5)
print("c093 outputs", lab.deque_maxima([3, 1, 4, 1, 5], 3)[0])
# c094: x=(2,5,1,0,3), k=2 -> (5,5,1,3)
print("c094 outputs", lab.deque_maxima([2, 5, 1, 0, 3], 2)[0])
# c092: x=(k,k-1,...,2,k+1), n=k: comparisons at step k, pops at step k
for k in range(2, 8):
    xs = list(range(k, 1, -1)) + [k + 1]
    _, ops = lab.deque_maxima(xs, k)
    # run prefix to isolate step k
    _, ops_prev = lab.deque_maxima(xs[:-1], k) if k > 1 else (None, None)
    print(f"c092 k={k} removals at step k = {ops.pops - ops_prev.pops} (expected {k - 1})")
# c095: strictly increasing, n values, every k: comparisons = n - 1
bad = []
for n in range(1, 25):
    xs = list(range(1, n + 1))
    for k in range(1, n + 1):
        _, ops = lab.deque_maxima(xs, k)
        if ops.comparisons != n - 1:
            bad.append((n, k, ops.comparisons))
print("c095 strictly increasing comparisons != n-1 cases:", bad)
# c091 / c098 / Prop 3.3: over random inputs, pushes = n, pops <= n, comparisons <= 2n
worst = 0
ok = True
rng = random.Random(12345)
for trial in range(300):
    n = rng.randint(1, 60)
    xs = [rng.randint(0, 9) for _ in range(n)]
    k = rng.randint(1, n)
    out, ops = lab.deque_maxima(xs, k)
    naive, _ = lab.naive_maxima(xs, k)
    if out != naive or ops.pushes != n or ops.pops > n or ops.comparisons > 2 * n:
        ok = False
    worst = max(worst, ops.comparisons / (2 * n))
print("random trials (300) deque==naive, pushes=n, pops<=n, comps<=2n:", ok, "max comps/2n =", round(worst, 3))
# c087 / c088: naive comparison count and maximiser
for n in (6, 10, 20):
    best = max(((n - k + 1) * (k - 1), k) for k in range(1, n + 1))
    print(f"c088 n={n}: max naive count {best[0]} at k={best[1]}, n^2/4={n*n/4}")
# c096 / c097 / c142-c146 on the seed-5 sequence
xs = lab.make_sequence(5, 200) if hasattr(lab, "make_sequence") else None
for k in (8, 32, 200):
    out, ops = lab.deque_maxima(xs, k)
    _, nv = lab.naive_maxima(xs, k)
    print(f"seed5 k={k}: naive={nv} formula={(200-k+1)*(k-1)} deque_comps={ops.comparisons} pushes={ops.pushes} pops={ops.pops}")
print("c101 window 1..20 outputs equal:", all(lab.deque_maxima(xs, k)[0] == lab.naive_maxima(xs, k)[0] for k in range(1, 21)))
print("c170 heap bound 3n floor(log2 n) at n=200:", 3 * 200 * 7, "(floor(log2 200) = 7)")
# c087: naive comparison count equals (n-k+1)(k-1) for every n <= 30 and every 1 <= k <= n (exhaustive)
bad_naive = [(n, k) for n in range(1, 31) for k in range(1, n + 1)
             if lab.naive_maxima(list(range(n)), k)[1] != (n - k + 1) * (k - 1)]
print("c087 naive count != (n-k+1)(k-1) cases for n<=30 (exhaustive):", bad_naive)
