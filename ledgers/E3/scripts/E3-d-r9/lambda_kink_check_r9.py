# Round 9: is the certainty equivalent kinked in lambda at the sign change of W? Lottery +1000 w.p. 1/2 and -500 w.p. 1/2;
# W = 0 at lambda = 2. Left and right slopes in lambda (step h) for several gamma in the estimator's domain (0, 1) and at 0.
def ce(lam, g):
    a = 1 / (1 - g)
    W = 0.5 * (1000 ** (1 - g)) - 0.5 * lam * (500 ** (1 - g))
    return W ** a if W >= 0 else -((-W / lam) ** a)
for g in (0.0, 0.2, 0.4, 0.6):
    for h in (1e-3, 1e-5):
        lft = (ce(2, g) - ce(2 - h, g)) / h
        rgt = (ce(2 + h, g) - ce(2, g)) / h
        print(f"gamma={g} h={h}: left-slope={lft:.6g} right-slope={rgt:.6g}")
