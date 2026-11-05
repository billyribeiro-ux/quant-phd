# Independent recomputation of L03 numbers (own code, no import of the lab).
from fractions import Fraction as F
from itertools import product

def expected_total(up, down, p_up, rule, N=6):
    # exact expectation of W at the stopping time by recursion over (history) built independently
    def rec(total, t, last):
        if t == N or rule(t, total, last):
            return F(total)
        return p_up * rec(total + up, t + 1, up) + (1 - p_up) * rec(total - down, t + 1, -down)
    return rec(0, 0, None)

rules = {
    "play all": lambda t, tot, last: False,
    "first win": lambda t, tot, last: t > 0 and last > 0,
    "first loss": lambda t, tot, last: t > 0 and last < 0,
    "total>=100": lambda t, tot, last: tot >= 100,
    "|total|>=200": lambda t, tot, last: abs(tot) >= 200,
}
for name, r in rules.items():
    print("fair   ", name, expected_total(100, 100, F(1, 2), r))
for name, r in rules.items():
    print("biased ", name, expected_total(150, 100, F(1, 2), r))

# Example 3.6 reroll game
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
vals = [max(F(100 * f), cont) for f in range(1, 7)]
print("continuation", cont, "value", sum(vals) / 6, "gain", sum(vals) / 6 - 350)
print("choose stop faces", [f for f in range(1, 7) if 100 * f >= cont])
# fee c = 1 gain (R2)
c = 1
cont_c = F(350 - c)
gain_c = sum(max(F(100 * f), cont_c) for f in range(1, 7)) / 6 - 350
print("R2 gain c=1", gain_c, float(gain_c))
# R1 two-turn look-ahead rule expectation
tot = F(0)
for a, b in product((100, -100), repeat=2):
    W1, W2 = a, a + b
    tot += F(1, 4) * max(W1, W2)
print("R1 expected total", tot)
# Example 3.10: biased per-turn expectation and play-all
print("biased per-turn", F(150, 2) - F(100, 2), "six turns", 6 * (F(150, 2) - F(100, 2)))
# E2 difference
print("E2", F(625, 8) - 150, float(F(625, 8) - 150))
# E3
print("E3", F(1150, 3) - 350)
