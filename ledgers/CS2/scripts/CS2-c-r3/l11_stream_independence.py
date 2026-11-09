"""Check that stored count and compaction count do not depend on the stream values (L11 Section 3 / E2 / R3 claims)."""
import sys, random
sys.argv = sys.argv[:1]
exec(open(__file__.replace("l11_stream_independence.py", "l11_numbers.py"), encoding="utf-8").read().split('print("capacities')[0])
for eps in (F(1, 20), F(1, 10)):
    res = set()
    for seed in (1, 2, 3, 2026):
        rng = random.Random(seed)
        xs = [rng.random() for _ in range(5000)] if seed != 3 else [float(5000 - i) for i in range(5000)]
        sk = Sk(eps)
        for x in xs: sk.add(x)
        res.add((sk.stored(), sum(sk.C.values())))
    print("eps", eps, "(stored, compactions) over 4 streams:", res)
