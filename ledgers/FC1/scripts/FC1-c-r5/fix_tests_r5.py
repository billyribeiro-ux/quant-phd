"""Round 5 verifier: the two proposed grader tests, appended to a SCRATCH copy of test_project.py (never the course file)."""
import pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
extra = '''

def test_bond_price_just_under_a_half_cent_rounds_down() -> None:
    """Zero-coupon bond, face 300075005 cents, three periods, yield 1 bps: the exact price is 299985000 plus 1/2 minus
    1/(2 * 1000300030001) cents, a hair under a half cent, which rounds down to 299985000 (the nearest cent)."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(300_075_005, 0, 3), 1) == 299_985_000, (
        "a price a hair under a half cent must round down to the nearest cent, with no tolerance"
    )


def test_yield_above_one_hundred_percent_is_accepted() -> None:
    """The page names one yield limit, yield_bps at or below -10000. A yield of 15000 bps (150 % per period) is valid:
    Bond(10000, 500, 1) at 15000 bps has the one event (1, 10500), and its price is 10500 / 2.5 = 4200 cents exactly."""
    __tracebackhide__ = True
    assert sol.bond_price_cents(sol.Bond(10_000, 500, 1), 15_000) == 4_200, (
        "a yield above 100 % per period is not named as refused; the price is the discounted event"
    )
'''
pathlib.Path(sys.argv[2]).write_text(src + extra, encoding="utf-8")
