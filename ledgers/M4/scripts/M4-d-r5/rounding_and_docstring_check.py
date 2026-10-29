import math, random, sys
sys.path.insert(0, "/tmp/verifyB5-M4-d/course/modules/M/M4/grader")
import reference as ref
import instance
print(repr(ref._cholesky.__doc__[:60]), "\\t" in ref._cholesky.__doc__, "\t" in ref._cholesky.__doc__, "tab-in-doc:", "\t" in ref._cholesky.__doc__)
print("instance doc tab:", "\t" in instance.__doc__)
# rounding vs truncation on 100 cents, sd 2
def sv(xs):
    m = math.fsum(xs)/len(xs); return math.fsum((x-m)**2 for x in xs)/(len(xs)-1)
rng = random.Random(0)
xs = [-100*2e-2*rng.gauss(0,1) for _ in range(2_000_000)]
print("exact var of 100*0.02*Z:", 4.0)
print("var round:", sum((round(x)-0)**2 for x in xs)/len(xs), "-> 4+1/12 =", 4+1/12)
print("var trunc:", sum(int(x)**2 for x in xs)/len(xs))
print("mean-square of round minus mean^2 is var (mean ~0)")
