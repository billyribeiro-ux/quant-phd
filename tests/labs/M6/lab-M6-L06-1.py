"""M6 L06 lab 1: densities on a finite space, computed in exact rational arithmetic.

Inputs are two fixed finite measures, not data, and no random draws are used, so every run prints the same lines.
A measure on a finite set is given by its weights on the points; the measure of an event A is the sum of the weights
of its points. An event is a subset of the points, and it is written here as a bit mask. Points are numbered from 1
in the text, so point 5 is index 4 in the code.

Part A: the points carry mu and nu with mu > 0 everywhere. The density f = nu / mu reproduces nu on all 16 events.
Part B: the fifth point (point 5) carries mu = 0 and nu > 0. The event {point 5} then has nu > 0 and mu = 0, so no
density can reproduce nu on it. Exactly one of the 32 events fails the absolute-continuity test.

Part C: for a function g on the four points, the sum of g times nu equals the sum of g times the density times mu.
Every weight, measure and density is a Fraction, so each equality test is exact. Nothing is rounded.
"""

from fractions import Fraction


def measure(weights: tuple[Fraction, ...], event: int) -> Fraction:
    """The measure of the event with bit mask `event`: the sum of the weights of the points whose bit is set."""
    return sum((w for i, w in enumerate(weights) if event >> i & 1), Fraction(0))


def integral(density: tuple[Fraction, ...], mu: tuple[Fraction, ...], event: int) -> Fraction:
    """The integral over the event of the density with respect to mu: the sum of density * mu over its points."""
    return sum((d * w for i, (d, w) in enumerate(zip(density, mu, strict=True)) if event >> i & 1), Fraction(0))


def fmt(value: Fraction) -> str:
    """A rational number as a reduced fraction with no spaces, for printing."""
    return str(value)


def part_a() -> None:
    """A four-point space with mu > 0 everywhere: the density nu/mu reproduces nu on every event."""
    mu = (Fraction(1, 8), Fraction(1, 4), Fraction(1, 4), Fraction(3, 8))
    nu = (Fraction(1, 4), Fraction(1, 8), Fraction(1, 2), Fraction(1, 8))
    density = tuple(n / m for n, m in zip(nu, mu, strict=True))
    print("Part A: density nu/mu on a four-point space with mu > 0")
    print("density " + " ".join(fmt(d) for d in density))
    events = range(2**4)
    matches = all(integral(density, mu, a) == measure(nu, a) for a in events)
    print(f"events_checked {len(events)}")
    print(f"all_events_match {matches}")
    print(f"total_mass_mu {fmt(measure(mu, 15))} total_mass_nu {fmt(measure(nu, 15))}")


def part_b() -> None:
    """A five-point space with mu = 0 at point 5 (index 4) and nu > 0 there: no density exists."""
    mu = (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(0))
    nu = (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8))
    print("Part B: a point with mu = 0 and nu > 0")
    failing = [a for a in range(2**5) if measure(mu, a) == 0 and measure(nu, a) > 0]
    print(f"events_checked {2**5}")
    print(f"absolute_continuity_failures {len(failing)}")
    for a in failing:
        print(f"failing_event_mask {a} mu {fmt(measure(mu, a))} nu {fmt(measure(nu, a))}")
    candidate = tuple(n / m if m > 0 else Fraction(0) for n, m in zip(nu, mu, strict=True))
    misses = [a for a in range(2**5) if integral(candidate, mu, a) != measure(nu, a)]
    print(f"candidate_density_misses {len(misses)}")
    print(f"candidate_reproduces_nu {len(misses) == 0}")


def part_c() -> None:
    """The integral of a function g against nu equals its integral against the density times mu (Proposition 2.2)."""
    mu = (Fraction(1, 8), Fraction(1, 4), Fraction(1, 4), Fraction(3, 8))
    nu = (Fraction(1, 4), Fraction(1, 8), Fraction(1, 2), Fraction(1, 8))
    density = tuple(n / m for n, m in zip(nu, mu, strict=True))
    g = (Fraction(3), Fraction(-1), Fraction(2), Fraction(5))
    against_nu = sum((gi * ni for gi, ni in zip(g, nu, strict=True)), Fraction(0))
    against_density = sum((gi * di * mi for gi, di, mi in zip(g, density, mu, strict=True)), Fraction(0))
    print("Part C: integral of g against nu, and against the density times mu")
    print(f"integral_against_nu {fmt(against_nu)}")
    print(f"integral_against_density {fmt(against_density)}")
    print(f"equal {against_nu == against_density}")


def main() -> None:
    """Print Parts A, B and C."""
    part_a()
    part_b()
    part_c()


main()
