"""Counterexamples and identities checked for slice M7-b (L05). Standard library only; run with python -I."""

from fractions import Fraction as F
import random

random.seed(3)


def f(Q, c, x):
    n = len(x)
    return F(1, 2) * sum(x[i] * Q[i][j] * x[j] for i in range(n) for j in range(n)) + sum(c[i] * x[i] for i in range(n))


# Prop 3.4 midpoint identity: f(z) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y), Q symmetric (PD not needed for identity)
ok = True
for _ in range(300):
    Q = [[F(0)] * 2 for _ in range(2)]
    a, b, d = (F(random.randint(-5, 5)) for _ in range(3))
    Q = [[a, b], [b, d]]
    c = [F(random.randint(-5, 5)), F(random.randint(-5, 5))]
    x = [F(random.randint(-5, 5)), F(random.randint(-5, 5))]
    y = [F(random.randint(-5, 5)), F(random.randint(-5, 5))]
    z = [(x[i] + y[i]) / 2 for i in range(2)]
    dif = [x[i] - y[i] for i in range(2)]
    q = sum(dif[i] * Q[i][j] * dif[j] for i in range(2) for j in range(2))
    ok = ok and f(Q, c, z) == (f(Q, c, x) + f(Q, c, y)) / 2 - q / 8
print("Prop 3.4 midpoint identity on 300 random rational triples:", ok)

# Lemma 1.4 says f is convex; chord identity for PSD Q: f(th x+(1-th)y) - th f(x) - (1-th) f(y) = -th(1-th)/2 (x-y)'Q(x-y)
ok2 = True
for _ in range(300):
    a, b, d = (F(random.randint(-5, 5)) for _ in range(3))
    Q = [[a, b], [b, d]]
    c = [F(random.randint(-5, 5)), F(random.randint(-5, 5))]
    x = [F(random.randint(-5, 5)), F(random.randint(-5, 5))]
    y = [F(random.randint(-5, 5)), F(random.randint(-5, 5))]
    th = F(random.randint(0, 10), 10)
    m = [th * x[i] + (1 - th) * y[i] for i in range(2)]
    dif = [x[i] - y[i] for i in range(2)]
    q = sum(dif[i] * Q[i][j] * dif[j] for i in range(2) for j in range(2))
    lhs = f(Q, c, m) - th * f(Q, c, x) - (1 - th) * f(Q, c, y)
    ok2 = ok2 and lhs == -th * (1 - th) / 2 * q
print("chord identity (basis for convexity of f when Q is PSD; not on the page) holds:", ok2)

# Misconception 3 counterexample: min (1/2) x'Qx with Q = 2I, c = 0, constraint x1 = 0 -> minimiser 0 with gradient 0
Q = [[F(2), F(0)], [F(0), F(2)]]
c = [F(0), F(0)]
xstar = [F(0), F(0)]
grad = [sum(Q[i][j] * xstar[j] for j in range(2)) + c[i] for i in range(2)]
print("MC3 counterexample: gradient at minimiser of x1=0 constrained QP =", grad, "with A=(1,0), lambda=0 (zero gradient despite a constraint)")

# Canon-break heading: indefinite Q can have a minimiser under a constraint. Q=diag(1,-1), c=0, constraint x2 = 0
Q = [[F(1), F(0)], [F(0), F(-1)]]
pts = [[F(t, 4), F(0)] for t in range(-20, 21)]
print("indefinite Q, constraint x2=0: min over sampled feasible points =", min(f(Q, c, p) for p in pts), "attained at x1 =", [str(p[0]) for p in pts if f(Q, c, p) == min(f(Q, c, q) for q in pts)])
