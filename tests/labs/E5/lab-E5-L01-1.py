"""E5 L01 lab 1: the accounting identities, two price indices, the deflator and the log convention.

Standard library only (fractions, math). No randomness and no network, so every run prints the same lines.
The accounts table and the basket prices are SIMULATED: they are illustrative integers typed for this lab in
currency units (CU). They are not taken from any statistical agency, and no claim about any real economy rests on them.

Part A: the expenditure-side and income-side identities for one accounts table, and the closed-economy saving identity.
Part B: two price indices on two-good baskets, Laspeyres and Paasche, as exact fractions, with the gap between them.
Part C: simple and log inflation from one index, the deflator identity for real and nominal growth, and the
chain product of link ratios.

Every index value is a Fraction. Floats appear only in the decimal companions, which print six decimal places.
"""

from __future__ import annotations

import math
from fractions import Fraction


def expenditure_gdp(c: int, i: int, g: int, exports: int, imports: int) -> int:
    """Expenditure-side GDP in CU: Y = C + I + G + (X - M), with net exports X - M."""
    return c + i + g + (exports - imports)


def income_gdp(wages: int, operating_surplus: int, taxes_less_subsidies: int, depreciation: int) -> int:
    """Income-side GDP in CU: compensation of employees, operating surplus, taxes less subsidies and depreciation."""
    return wages + operating_surplus + taxes_less_subsidies + depreciation


def laspeyres(p0: tuple[int, ...], q0: tuple[int, ...], p1: tuple[int, ...]) -> Fraction:
    """Laspeyres price index of period 1 on base period 0: sum of p1 * q0 over sum of p0 * q0.

    The quantities are fixed at the base period, so the weights do not change when prices do.
    """
    numerator = sum(a * b for a, b in zip(p1, q0, strict=True))
    denominator = sum(a * b for a, b in zip(p0, q0, strict=True))
    return Fraction(numerator, denominator)


def paasche(p0: tuple[int, ...], p1: tuple[int, ...], q1: tuple[int, ...]) -> Fraction:
    """Paasche price index of period 1 on base period 0: sum of p1 * q1 over sum of p0 * q1.

    The quantities are those of period 1, so the weights move with the quantities bought.
    """
    numerator = sum(a * b for a, b in zip(p1, q1, strict=True))
    denominator = sum(a * b for a, b in zip(p0, q1, strict=True))
    return Fraction(numerator, denominator)


def simple_rate(index_now: Fraction, index_before: Fraction) -> Fraction:
    """Simple growth rate of an index: index_now / index_before - 1, an exact fraction."""
    return index_now / index_before - 1


def main() -> None:
    """Print Parts A, B and C in a fixed order."""
    # Part A: one accounts table, all entries SIMULATED integers in CU.
    consumption, investment, government = 620, 180, 210
    exports, imports = 95, 110
    wages, taxes_less_subsidies, depreciation = 640, 40, 15
    gdp_expenditure = expenditure_gdp(consumption, investment, government, exports, imports)
    # The operating surplus is the balancing entry on the income side, so the two sides agree by construction.
    surplus_residual = gdp_expenditure - (wages + taxes_less_subsidies + depreciation)
    gdp_income = income_gdp(wages, surplus_residual, taxes_less_subsidies, depreciation)
    print(f"expenditure GDP {gdp_expenditure} CU; income GDP {gdp_income} CU")
    print(f"expenditure and income sides agree: {gdp_expenditure == gdp_income}")
    print(f"operating surplus as the balancing entry {surplus_residual} CU")

    # Closed economy with the same C, I and G: no exports or imports, and a tax of 230 CU.
    tax = 230
    closed_y = consumption + investment + government
    private_saving = closed_y - tax - consumption
    public_saving = tax - government
    total_saving = private_saving + public_saving
    print(f"closed economy Y {closed_y} CU; private saving {private_saving}; public saving {public_saving}")
    print(f"total saving {total_saving} equals investment {investment}: {total_saving == investment}")

    # Part B: two baskets of two goods, prices p0 and p1 and quantities q0 and q1, in CU per unit.
    p0_a, q0_a = (2, 5), (10, 4)
    p1_a, q1_a = (3, 5), (8, 6)
    lasp_a = laspeyres(p0_a, q0_a, p1_a)
    pasc_a = paasche(p0_a, p1_a, q1_a)
    gap_a = lasp_a - pasc_a
    print(f"basket A: Laspeyres {lasp_a} ({float(lasp_a):.6f}); Paasche {pasc_a} ({float(pasc_a):.6f})")
    print(f"basket A: Laspeyres minus Paasche {gap_a} ({float(gap_a):.6f}); Laspeyres is larger: {gap_a > 0}")

    p0_b, q0_b = (1, 1), (1, 9)
    p1_b, q1_b = (2, 1), (9, 1)
    lasp_b = laspeyres(p0_b, q0_b, p1_b)
    pasc_b = paasche(p0_b, p1_b, q1_b)
    gap_b = lasp_b - pasc_b
    print(f"basket B: Laspeyres {lasp_b} ({float(lasp_b):.6f}); Paasche {pasc_b} ({float(pasc_b):.6f})")
    print(f"basket B: Laspeyres minus Paasche {gap_b} ({float(gap_b):.6f}); Laspeyres is larger: {gap_b > 0}")

    # Part C: inflation conventions and the deflator identity, on basket A.
    simple_lasp = simple_rate(lasp_a, Fraction(1))
    simple_pasc = simple_rate(pasc_a, Fraction(1))
    print(f"simple inflation, Laspeyres basis: {float(simple_lasp):.6f}")
    print(f"simple inflation, Paasche basis: {float(simple_pasc):.6f}")
    print(f"log inflation, Laspeyres basis: {math.log(float(lasp_a)):.6f}")
    print(f"log inflation, Paasche basis: {math.log(float(pasc_a)):.6f}")

    # Deflator identity: real GDP = nominal GDP / deflator, so (1 + g_nominal) = (1 + g_real)(1 + pi) exactly.
    nominal_0, nominal_1 = Fraction(995), Fraction(1100)
    deflator_0, deflator_1 = Fraction(1), pasc_a
    real_0, real_1 = nominal_0 / deflator_0, nominal_1 / deflator_1
    g_nominal = nominal_1 / nominal_0 - 1
    g_real = real_1 / real_0 - 1
    pi = deflator_1 / deflator_0 - 1
    identity = (1 + g_nominal) == (1 + g_real) * (1 + pi)
    print(f"nominal growth {float(g_nominal):.6f}; real growth {float(g_real):.6f}; deflator inflation {float(pi):.6f}")
    print(f"(1 + nominal) equals (1 + real)(1 + inflation) exactly: {identity}")

    # Simple and log growth: ln(1 + x) <= x for x > -1, so x - ln(1 + x) is non-negative on the grid.
    grid = (Fraction(1, 100), Fraction(5, 100), Fraction(25, 100))
    gaps = [float(x) - math.log(1 + float(x)) for x in grid]
    print("x - ln(1 + x) at x = 0.01, 0.05, 0.25: " + ", ".join(f"{g:.6f}" for g in gaps))
    print(f"all gaps non-negative: {all(g >= 0 for g in gaps)}")

    # Chain: the product of link ratios over three periods equals the direct ratio of the index.
    levels = (Fraction(1), Fraction(5, 4), Fraction(27, 23), Fraction(3, 2))
    links = [levels[k] / levels[k - 1] for k in range(1, len(levels))]
    product = Fraction(1)
    for link in links:
        product *= link
    print(
        f"chain product of link ratios {product} equals direct ratio {levels[-1] / levels[0]}: "
        f"{product == levels[-1] / levels[0]}"
    )


main()
