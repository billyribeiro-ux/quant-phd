import math
from statistics import NormalDist

# Minimum Bayes factor exp(-t^2/2) and the implied lower bound on the probability
# that the null is true, for several prior probabilities of the null.
phi = NormalDist()
priors = (0.5, 0.8, 0.95, 0.99)

print("t  p_two_sided  MBF  " + "  ".join(f"pi0={pi:.2f}" for pi in priors))
for t in (1.96, 2.5, 3.0, 3.5, 4.0):
    p = 2.0 * (1.0 - phi.cdf(t))
    mbf = math.exp(-t * t / 2.0)
    bounds = []
    for pi0 in priors:
        odds = pi0 / (1.0 - pi0) * mbf  # posterior odds of the null, at their smallest
        bounds.append(odds / (1.0 + odds))
    print(f"{t:.2f} {p:.4f} {mbf:.4f} " + " ".join(f"{b:.4f}" for b in bounds))
