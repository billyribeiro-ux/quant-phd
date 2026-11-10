"""Alternative implementation 3: Object-oriented style with Valuation engine class."""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction


class EquityValuationEngine:
    @staticmethod
    def gordon(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
        if d1 < 0 or r <= g:
            raise ValueError("invalid gordon parameters")
        return d1 / (r - g)

    @classmethod
    def ddm(cls, dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction:
        if not dividends or any(d < 0 for d in dividends) or r <= g or r <= -1:
            raise ValueError("invalid ddm parameters")
        factor = Fraction(1) + r
        pv = Fraction(0)
        disc = Fraction(1)
        for d in dividends:
            disc *= factor
            pv += d / disc
        terminal_d = dividends[-1] * (Fraction(1) + g)
        tv = cls.gordon(terminal_d, r, g)
        return pv + tv / (factor ** len(dividends))

    @classmethod
    def fcfe(cls, fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
        if not fcfe or shares <= 0 or r <= g or r <= -1:
            raise ValueError("invalid fcfe parameters")
        factor = Fraction(1) + r
        pv = Fraction(0)
        disc = Fraction(1)
        for f in fcfe:
            disc *= factor
            pv += f / disc
        terminal_f = fcfe[-1] * (Fraction(1) + g)
        tv = cls.gordon(terminal_f, r, g)
        total_equity = pv + tv / (factor ** len(fcfe))
        return total_equity / shares

    @staticmethod
    def residual_income(
        book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
    ) -> Fraction:
        if not earnings or len(earnings) != len(dividends) or r <= -1:
            raise ValueError("invalid residual income parameters")
        factor = Fraction(1) + r
        pv_ri = Fraction(0)
        b = book_value_0
        disc = Fraction(1)
        for ni, d in zip(earnings, dividends, strict=True):
            ri = ni - r * b
            disc *= factor
            pv_ri += ri / disc
            b = b + ni - d
        return book_value_0 + pv_ri

    @staticmethod
    def target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
        if not scenarios or any(p < 0 or v < 0 for p, v in scenarios):
            raise ValueError("invalid scenarios")
        total_p = sum((p for p, _ in scenarios), Fraction(0))
        if total_p != Fraction(1):
            raise ValueError("probabilities must sum to 1")
        ev = sum((p * v for p, v in scenarios), Fraction(0))
        return (2 * ev.numerator + ev.denominator) // (2 * ev.denominator)


def gordon_value(d1: Fraction, r: Fraction, g: Fraction) -> Fraction:
    return EquityValuationEngine.gordon(d1, r, g)


def ddm_value(dividends: Sequence[Fraction], r: Fraction, g: Fraction) -> Fraction:
    return EquityValuationEngine.ddm(dividends, r, g)


def fcfe_value_per_share(fcfe: Sequence[Fraction], shares: Fraction, r: Fraction, g: Fraction) -> Fraction:
    return EquityValuationEngine.fcfe(fcfe, shares, r, g)


def residual_income_value(
    book_value_0: Fraction, earnings: Sequence[Fraction], dividends: Sequence[Fraction], r: Fraction
) -> Fraction:
    return EquityValuationEngine.residual_income(book_value_0, earnings, dividends, r)


def scenario_price_target_cents(scenarios: Sequence[tuple[Fraction, int]]) -> int:
    return EquityValuationEngine.target_cents(scenarios)
