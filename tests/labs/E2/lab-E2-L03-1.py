"""E2 lab L03: adverse selection in a two-quality market, with exact prices in integer cents.

Standard library only: fractions.Fraction for every share and price comparison. No randomness and no network.
Sellers hold one unit each. A seller is high quality (H) with population share alpha, and low quality (L)
with share 1 - alpha. The buyer's value of a unit is VALUE[H] = 12000 cents or VALUE[L] = 6000 cents, and the seller's
cost is COST[H] = 10000 cents or COST[L] = 4000 cents. The buyer cannot observe quality, so it pays the expected
value of the units that are offered at the price p. A price p is market-consistent when p equals that
expected value, taken over the sellers whose cost is at most p. Every whole-cent price from 0 to 15000 is
tested, so each printed price list is exact for that grid.

The full-information benchmark gives each seller's gain from trade as VALUE - COST for its own type, with no
withholding. The lab prints the gains, the share of sellers who trade at each market-consistent price, and
the gains lost to the withheld sellers, in cents per seller, for alpha = k/10 with k from 0 to 10.
"""

from __future__ import annotations

from fractions import Fraction

VALUE = {"H": 12000, "L": 6000}
COST = {"H": 10000, "L": 4000}
MAX_PRICE = 15000


def offered_mass(alpha: Fraction, price: int) -> dict[str, Fraction]:
    """Population share of sellers whose cost is at most price, by quality."""
    share = {"H": alpha, "L": 1 - alpha}
    return {t: share[t] for t in ("H", "L") if COST[t] <= price}


def consistent_prices(alpha: Fraction) -> list[tuple[int, Fraction]]:
    """Each market-consistent price with the share of sellers who trade at it."""
    found: list[tuple[int, Fraction]] = []
    for price in range(MAX_PRICE + 1):
        mass = offered_mass(alpha, price)
        total = sum(mass.values(), Fraction(0))
        if total == 0:
            continue
        expected_value = sum((mass[t] * VALUE[t] for t in mass), Fraction(0)) / total
        if expected_value == price:
            found.append((price, total))
    return found


def main() -> None:
    gains = {t: VALUE[t] - COST[t] for t in ("H", "L")}
    print(f"cents: value H {VALUE['H']}, value L {VALUE['L']}, cost H {COST['H']}, cost L {COST['L']}")
    print(f"gain from trade H {gains['H']}, gain from trade L {gains['L']}")
    threshold = Fraction(COST["H"] - VALUE["L"], VALUE["H"] - VALUE["L"])
    print(f"share of high quality at which a price at cost H first clears: {threshold}")
    print(f"price grid 0 to {MAX_PRICE} cents, {MAX_PRICE + 1} prices tested per share")
    for k in range(11):
        alpha = Fraction(k, 10)
        found = consistent_prices(alpha)
        full = alpha * gains["H"] + (1 - alpha) * gains["L"]
        prices = [p for p, _ in found]
        traded = [str(share) for _, share in found]
        losses = [int(full - full * share) for _, share in found]
        print(
            f"alpha = {alpha}: market-consistent prices {prices}, traded share {traded}, "
            f"gains lost per seller in cents {losses}, full-information gains per seller {int(full)}"
        )
    naive = Fraction(1, 2) * VALUE["H"] + Fraction(1, 2) * VALUE["L"]
    print(f"average value at alpha = 1/2: {int(naive)}; high-quality cost {COST['H']} is above it: {COST['H'] > naive}")


main()
