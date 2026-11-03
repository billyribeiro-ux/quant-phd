import importlib.util, random, math
from fractions import Fraction
spec = importlib.util.spec_from_file_location('ref', '/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader/reference.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
rng = random.Random(7)
states = 0; viol_sum = viol_cap = viol_copy = 0
for trial in range(300):
    eps = rng.choice([0.05, 0.1, 0.2, 0.3])
    sk = ref.QuantileSketch(eps)
    stream = []
    for _ in range(rng.randint(1, 120)):
        x = float(rng.choice([rng.randint(0, 5), round(rng.uniform(0, 3), rng.choice([1, 6]))]))
        stream.append(x)
        sk.add(x)
        states += 1
        n = len(stream)
        if sum(sk._g) != n: viol_sum += 1
        cap = math.floor(2 * Fraction(eps) * n) + 1
        if any(g + d > cap for g, d in zip(sk._g, sk._delta)): viol_cap += 1
        # copy invariant: for each stored tuple i, some copy of v_i has exact rank in [R_i, R_i + delta_i]
        srt = sorted(stream)
        R = 0
        for v, g, d in zip(sk._values, sk._g, sk._delta):
            R += g
            ok = any(srt[r - 1] == v for r in range(R, R + d + 1) if 1 <= r <= n)
            if not ok: viol_copy += 1
print('states', states, 'sum(g)!=n', viol_sum, 'g+delta>floor(2 eps n)+1', viol_cap, 'copy-rank invariant failures', viol_copy)
