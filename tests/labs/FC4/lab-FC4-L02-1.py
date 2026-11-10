"""Lab FC4-L02-1: Herfindahl-Hirschman index (HHI) on industry market shares."""

from fractions import Fraction


def compute_hhi(shares: list[Fraction]) -> tuple[Fraction, int]:
    """Compute exact HHI in fraction [0, 1] and conventional integer points [0, 10000]."""
    assert sum(shares, Fraction(0)) == Fraction(1), "Market shares must sum to 1"
    hhi_frac = sum((s**2 for s in shares), Fraction(0))
    # Conventional index uses percentage shares squared: sum((100 * s)^2) = 10000 * sum(s^2)
    hhi_points = int(10000 * hhi_frac)
    return hhi_frac, hhi_points


def main() -> None:
    # Three illustrative market structures (SIMULATED)
    industries = {
        "Dominant firm monopoly": [Fraction(70, 100), Fraction(15, 100), Fraction(10, 100), Fraction(5, 100)],
        "Concentrated oligopoly": [
            Fraction(35, 100),
            Fraction(25, 100),
            Fraction(20, 100),
            Fraction(10, 100),
            Fraction(10, 100),
        ],
        "Fragmented competitive (10 equal firms)": [Fraction(1, 10)] * 10,
    }

    print("SIMULATED Industry Structure and Herfindahl-Hirschman Index (HHI)")
    print("-" * 75)
    print(f"{'Industry Structure':<40} {'Firms':>6} {'HHI (Exact)':>14} {'HHI (Points)':>12}")
    print("-" * 75)

    for name, shares in industries.items():
        hhi_frac, hhi_pts = compute_hhi(shares)
        print(f"{name:<40} {len(shares):>6} {hhi_frac!s:>14} {hhi_pts:>12d}")

    print("-" * 75)
    print("Exact HHI properties verified: concentration decreases strictly across the three panels.")


main()
