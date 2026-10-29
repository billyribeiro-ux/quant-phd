import random, itertools
def run(seed, spread=100000, mean=0, n=2000, months=12):
    rng = random.Random(seed)
    minima=[]
    for _ in range(n):
        flows=[mean+rng.randint(-spread,spread) for _ in range(months)]
        minima.append(min(itertools.accumulate(flows)))
    s=sorted(minima)
    q=s[100-1]
    cnt=lambda b: sum(1 for m in minima if m< -b)
    return cnt(0), cnt(250000), q, cnt(-q)
for seed in (2026, 7, 1, 2):
    print("seed",seed, run(seed))
print("spread 50000 seed 2026", run(2026, spread=50000))
print("mean -50000 seed 2026", run(2026, mean=-50000))
