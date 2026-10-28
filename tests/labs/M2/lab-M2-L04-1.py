"""M2 lab L04: the difference quotient of f(x) = x^3 at a = 1 converges to f'(1) = 3, with an exact error column.

Standard library only. No randomness and no network. The difference quotient is
Q(h) = (f(1 + h) - f(1)) / h, which expands exactly to 3 + 3h + h^2 for f(x) = x^3, so its error from 3 is exactly
3h + h^2. The script computes Q(h) as an exact rational number (fractions.Fraction) for h = 10^-1 to 10^-6, and
checks the expansion at each step. The derivative 3 is the limit of Q(h) as h tends to 0. The limit is established
on the page from the expansion, and the table only displays the values of Q at the listed steps.
"""

from __future__ import annotations

from fractions import Fraction


def f(x: Fraction) -> Fraction:
    """The cube x^3 for a rational x."""
    return x * x * x


def quotient(h: Fraction) -> Fraction:
    """The difference quotient (f(1 + h) - f(1)) / h at a = 1, for a non-zero rational h."""
    if h == 0:
        raise ValueError("the difference quotient needs h != 0")
    return (f(Fraction(1) + h) - f(Fraction(1))) / h


def expansion_holds(h: Fraction) -> bool:
    """True when quotient(h) equals 3 + 3h + h^2 exactly."""
    return quotient(h) == 3 + 3 * h + h * h


def main() -> None:
    print("h, difference quotient, error from 3")
    for k in range(1, 7):
        h = Fraction(1, 10**k)
        q = quotient(h)
        print(f"{float(h):g}, {float(q):.6f}, {float(abs(q - 3)):.6e}")
    steps = [Fraction(1, 10**k) for k in range(1, 7)]
    print(f"expansion 3 + 3h + h^2 holds at every listed h: {all(expansion_holds(h) for h in steps)}")
    print(f"error divided by h at h = 1e-6: {float(abs(quotient(steps[-1]) - 3) / steps[-1]):.6f}")


main()
