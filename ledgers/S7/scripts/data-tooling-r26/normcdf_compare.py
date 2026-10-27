"""Python side of the JS-vs-NormalDist comparison: NormalDist(0,1).cdf and pdf at the same points."""

from statistics import NormalDist

N = NormalDist()
for x in (-3, -0.5, 0, 1.2, 4):
    print(x, format(N.cdf(x), ".17g"), format(N.pdf(x), ".17g"))
