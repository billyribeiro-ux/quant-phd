"""Lab AC1-L07-1: stock-based compensation schedules on generated grants.

Every grant and every operating income figure here is SIMULATED: a seeded generator
draws them, no company is represented, and no output estimates any real firm. Money
is in integer cents of simulated currency units (SCU). The model has no income tax,
no forfeitures, no performance conditions and no share issuance at vesting, so the
lab's checks are the schedule sums and the Section 2 identities.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 20260701
N_GRANTS = 4
HORIZON = 6  # fiscal years 1 to 6; the latest vesting year any grant can have is 3 + 4 - 1 = 6


@dataclass(frozen=True)
class Grant:
    """One SIMULATED equity grant. Money in cents; shares as a count."""

    grant_year: int
    shares: int
    fair_value_cents: int  # grant-date fair value per share, in cents
    vest_years: int

    @property
    def value_cents(self) -> int:
        """Total grant value in cents: shares times grant-date fair value per share."""
        return self.shares * self.fair_value_cents


def yearly_expense(grant: Grant, year: int) -> int:
    """Expense recognized for one grant in one fiscal year, in integer cents.

    Straight-line over vest_years, starting in grant_year. Integer division gives the
    base amount for each vesting year; the final vesting year takes the remainder, so
    the schedule sums to value_cents exactly. Years outside the vesting period give 0.
    """
    index = year - grant.grant_year
    if index < 0 or index >= grant.vest_years:
        return 0
    base = grant.value_cents // grant.vest_years
    if index == grant.vest_years - 1:
        return grant.value_cents - base * (grant.vest_years - 1)
    return base


def generate_grants(rng: random.Random) -> list[Grant]:
    """Draw N_GRANTS SIMULATED grants: 100 to 5,000 shares, $5.00 to $40.00 per share, 3 or 4 vesting years."""
    grants: list[Grant] = []
    for _ in range(N_GRANTS):
        grant_year = rng.randint(1, 3)
        shares = rng.randrange(100, 5001, 100)
        fair_value_cents = rng.randint(500, 4000)
        vest_years = rng.choice((3, 4))
        grants.append(Grant(grant_year, shares, fair_value_cents, vest_years))
    return grants


def cents_text(cents: int) -> str:
    """Format integer cents as SCU dollars and cents, for example 1234567 gives 12,345.67."""
    sign = "-" if cents < 0 else ""
    whole, frac = divmod(abs(cents), 100)
    return f"{sign}{whole:,}.{frac:02d}"


def main() -> None:
    """Draw the grants and operating income, schedule the expense, and check the identities."""
    rng = random.Random(SEED)
    grants = generate_grants(rng)
    operating_income = [rng.randrange(40_000_000, 90_000_001, 100) for _ in range(HORIZON)]

    print(f"SIMULATED grants (seed {SEED}): grant year, shares, fair value per share, vest years, total SCU")
    for number, grant in enumerate(grants, start=1):
        print(
            f"G{number}  grant_year={grant.grant_year}  shares={grant.shares:,}  "
            f"fair_value={cents_text(grant.fair_value_cents)}  vest_years={grant.vest_years}  "
            f"total={cents_text(grant.value_cents)}"
        )

    schedule_ok = 0
    for grant in grants:
        expensed = sum(yearly_expense(grant, year) for year in range(1, HORIZON + 1))
        schedule_ok += expensed == grant.value_cents

    sbc = [sum(yearly_expense(g, year) for g in grants) for year in range(1, HORIZON + 1)]
    print("SIMULATED statements, SCU; years 1 to 6 (operating income is before SBC, no tax):")
    print("year  operating_income  sbc_expense  net_income  cfo  apic_change  cash_change")
    apic_ok = 0
    cash_ok = 0
    balance_ok = 0
    cfo_ok = 0
    for index, year in enumerate(range(1, HORIZON + 1)):
        oi = operating_income[index]
        expense = sbc[index]
        net_income = oi - expense
        cfo = net_income + expense
        apic_change = expense
        retained_change = net_income
        cash_change = cfo
        equity_change = apic_change + retained_change
        apic_ok += apic_change == expense
        cash_ok += cash_change == oi
        balance_ok += cash_change == equity_change
        cfo_ok += cfo == net_income + expense
        print(
            f"{year:>4}  {cents_text(oi):>16}  {cents_text(expense):>11}  {cents_text(net_income):>10}  "
            f"{cents_text(cfo):>9}  {cents_text(apic_change):>11}  {cents_text(cash_change):>11}"
        )

    print(f"schedule sums equal grant totals: {schedule_ok}/{N_GRANTS}")
    print(f"CFO equals net income plus SBC in every year: {cfo_ok}/{HORIZON}")
    print(f"cash change equals operating income in every year: {cash_ok}/{HORIZON}")
    print(f"assets change equals equity change in every year: {balance_ok}/{HORIZON}")
    print(f"APIC change equals SBC expense in every year: {apic_ok}/{HORIZON}")
    assert schedule_ok == N_GRANTS
    assert cfo_ok == cash_ok == balance_ok == apic_ok == HORIZON


main()
