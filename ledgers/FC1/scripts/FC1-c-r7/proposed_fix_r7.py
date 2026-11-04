"""Verifier's proposed grader fix for FC1-c round 7 (validated in a scratch copy only; not applied to the repo).

Usage: python3 -I proposed_fix_r7.py <source test_project.py> <output test_project.py>
Changes: (1) the wrapper loop that names NotImplementedError moves to the end of the module, so that the four
tests added after it are wrapped too; (2) three first docstring lines that state a hidden test's answer are
reworded so that the starter failure text does not print that answer; (3) one test for a 1001-period bond is added.
"""
import pathlib
import sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
loop = (
    "for _name, _value in list(globals().items()):\n"
    "    if _name.startswith(\"test_\") and callable(_value):\n"
    "        globals()[_name] = _named_when_unimplemented(_value)\n"
)
assert src.count(loop) == 1, "wrapper loop not found exactly once"
src = src.replace("\n" + loop, "")
replacements = [
    (
        "    \"\"\"Zero-coupon bond, face 300075005 cents, three periods, yield 1 bps: the exact price is 299985000 plus 1/2 minus\n"
        "    1/(2 * 1000300030001) cents, a hair under a half cent, which rounds down to 299985000 (the nearest cent).\"\"\"",
        "    \"\"\"Zero-coupon bond, three periods, yield 1 bps: an exact price a hair under a half cent rounds down to the nearest cent.\n"
        "    Face 300075005 cents: the exact price is 299985000 plus 1/2 minus 1/(2 * 1000300030001) cents.\"\"\"",
    ),
    (
        "    \"\"\"Hand check: 2**40 + 1 units at 9851 cents is (2**40 + 1) * 9851 = 10831289045231227 cents, an odd integer above\n",
        "    \"\"\"Hand check: a trade of 2**40 + 1 units at 9851 cents has a cash flow above 2**53, which a binary float cannot hold.\n"
        "    The product (2**40 + 1) * 9851 is an odd integer, so the amount must be exact.\n"
        "    (The exact product is checked below.)\n"
        "    ",
    ),
    (
        "    \"\"\"Hand check: Bond(13, 0, 1) at 400 bps has the one event (1, 13) and exact present value 13 / 1.04 = 25/2 cents,\n",
        "    \"\"\"Hand check: Bond(13, 0, 1) at 400 bps has one event and an exact half cent of present value, which rounds away\n",
    ),
    (
        "    \"\"\"Accepted-input check: a yield of 30000 bps (300 % per period) is not named as refused: 10500 / 4 = 2625 cents.\"\"\"",
        "    \"\"\"Accepted-input check: a yield of 30000 bps (300 % per period) is not named as refused; the price is the discounted event.\"\"\"",
    ),
]
for old, new in replacements:
    count = src.count(old)
    assert count == 1, f"docstring anchor found {count} times: {old[:60]!r}"
    src = src.replace(old, new)
src = src.rstrip("\n") + "\n\n\n" + '''def test_bond_schedule_of_one_thousand_and_one_periods_is_accepted() -> None:
    """Accepted-input check: the page refuses only periods below 1 and gives every period 1..periods a coupon, so a
    1001-period bond has one event per period 1..1001 and its price at 400 bps is the exact sum, rounded once."""
    __tracebackhide__ = True
    bond = sol.Bond(10_000, 500, 1_001)
    rows = checked_events(bond.events(), "Bond.events")
    assert rows == oracle_events(10_000, 500, 1_001), "every period 1..1001 must carry its coupon, and the face the last one"
    got = checked_int(sol.bond_price_cents(bond, 400), "bond_price_cents")
    assert got == oracle_price(oracle_events(10_000, 500, 1_001), 400), (
        "all 1001 events must be discounted by (1 + y) ** -t for their own periods, and the sum rounded once"
    )


''' + loop
pathlib.Path(sys.argv[2]).write_text(src, encoding="utf-8")
print("wrote", sys.argv[2])
