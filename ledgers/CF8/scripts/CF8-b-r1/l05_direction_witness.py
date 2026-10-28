import random, itertools
def freq(mean, spread, buf, n=2000, seed=2026):
    rng = random.Random(seed)
    minima=[]
    for _ in range(n):
        flows=[mean+rng.randint(-spread,spread) for _ in range(12)]
        minima.append(min(itertools.accumulate(flows)))
    return sum(1 for m in minima if m < -buf)/n
print("mean 0, spread 100000, buffer 250000:", freq(0,100000,250000))
print("mean -50000, spread 100000, buffer 250000:", freq(-50000,100000,250000))
print("mean 0, spread 50000, buffer 250000:", freq(0,50000,250000))
