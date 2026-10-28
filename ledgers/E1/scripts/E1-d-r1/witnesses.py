"""Witnesses for the E1 project-page findings (run: .venv/bin/python -I <this file>). Standard library only."""

from fractions import Fraction as F

# Prop 3, case f1 = c < f2: the page's deviator (exchange 2) gains nothing by charging (c+f2)/2.
a, b, c = 120, 1, 20
f2 = 30
g = F(c + f2, 2)
ex2_profit_at_g = F(0)  # exchange 1 stays at c < g and takes the whole demand, so exchange 2 trades nothing
ex1_profit_if_raises_to_g = (g - c) * (a - b * g)  # exchange 1 raising its fee to g takes the whole demand
print("Prop 3 witness: exchange 2 at g =", g, "earns", ex2_profit_at_g)
print("Prop 3 witness: exchange 1 at c raising to g earns", ex1_profit_if_raises_to_g, "cents (the gain is exchange 1's)")

# Prop 2 sign (algebra, no script needed): q1 = (d-q2)/2 and q2 = (d-q1)/2 subtract to q1 - q2 = (q1 - q2)/2,
# so the page's displayed q1 - q2 = -(q1 - q2)/2 is a wrong equation (both forms give q1 = q2 = d/3).

# Prop 5 with a real b: a=4, b=1/2, c=1 gives d = 3.5 > 6b = 3, but the printed volumes tie.
a5, b5, c5 = F(4), F(1, 2), F(1)
d5 = a5 - b5 * c5
def half_up(x): return (x + F(1, 2)).__floor__()
print("Prop 5 witness: d =", d5, "6b =", 6 * b5, "monopoly volume", d5 / 2, "->", half_up(d5 / 2),
      "Cournot volume", 2 * d5 / 3, "->", half_up(2 * d5 / 3))

# Bertrand tie rule: at (c, c) the total volume and the fee do not depend on how the tie is split.
d = a - b * c
for share in (F(1, 2), F(1), F(0)):
    print("Bertrand at (c,c), exchange 1 share", share, ": total volume", d, "fee", c, "profit each", (c - c) * d * share)
