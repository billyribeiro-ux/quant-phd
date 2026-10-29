"""Checks the L05 canon claims: another seed moves the quantile and counts; mean and spread move the frequency."""
import itertools
import random

def freq(seed, mean=0, spread=100_000, buffer=250_000, years=2000):
    rng = random.Random(seed)
    minima = []
    for _ in range(years):
        flows = [mean + rng.randint(-spread, spread) for _ in range(12)]
        minima.append(min(itertools.accumulate(flows)))
    srt = sorted(minima)
    q = srt[-((-5 * years) // 100) - 1]
    return sum(1 for m in minima if m < -buffer), sum(1 for m in minima if m < q), q

for s in (2026, 1, 2, 3):
    print("seed", s, "counts(250000, quantile-buffer count), quantile", freq(s))
for mean in (0, -50_000):
    print("mean", mean, "buffer 250000 count", freq(2026, mean=mean)[0])
for spread in (100_000, 150_000):
    print("spread", spread, "buffer 250000 count", freq(2026, spread=spread)[0])
