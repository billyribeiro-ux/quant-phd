import instruments as sol
from fractions import Fraction
# exact oracle at a non-par yield, periods 13..15 (the page says 13-15 period bonds are checked)
def oracle(n, y_bps):
    y = Fraction(y_bps, 10000)
    ev = [(t, 500) for t in range(1, n + 1)]
    ev[-1] = (n, 500 + 10000)
    tot = sum((Fraction(a) / (1 + y) ** t for t, a in ev), Fraction(0))
    return int(tot + Fraction(1, 2))
for n in (13, 14, 15):
    print(n, "mutant events last 2:", sol.Bond(10000, 500, n).events()[-2:], "price@400:", sol.bond_price_cents(sol.Bond(10000, 500, n), 400), "oracle@400:", oracle(n, 400))
