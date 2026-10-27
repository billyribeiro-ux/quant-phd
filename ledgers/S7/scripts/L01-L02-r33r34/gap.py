import math
from scipy import integrate, stats
def emax(N):
    f = lambda x: x * N * stats.norm.pdf(x) * stats.norm.cdf(x) ** (N - 1)
    return integrate.quad(f, -12, 12, limit=400)[0]
for N in [2, 3, 5, 10, 20, 50, 100, 252, 1000, 10000]:
    print(N, round(emax(N), 4), "gap SD", round(math.sqrt(2 * math.log(N)) - emax(N), 4))
