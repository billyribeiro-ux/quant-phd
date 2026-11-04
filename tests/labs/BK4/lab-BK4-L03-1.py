"""BK4 lab L03: the CCP default waterfall and margin cover, in integer cents.

Standard library only; no network. Every input is generated from a fixed seed, so the inputs are SIMULATED and
every run prints the same numbers. All money is an int in cents, and every cover is an integer count of basis
points. Part A runs the layer order of Definition 1.1 on a fixture with hand-checkable amounts, on the remainder
rule with a three-survivor fixture, and on three seeded scenarios. Part B sizes the defaulter's margin for two cover
targets from seeded scenario losses with the order statistic of Proposition 2.3, then checks each sized margin by a
brute-force search over the integer margins 0, 1, 2, and so on.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

SEED = 2026
MEMBERS = (1, 2, 3, 4)
DEFAULTER = 3
TARGETS_BPS = (9900, 9975)
SCENARIOS = 200
MAX_LOSS_CENTS = 3000


@dataclass(frozen=True)
class Waterfall:
    """The payments for one loss, in cents, by layer.

    margin_cents, default_fund_cents and ccp_capital_cents are the three layers a1, a2 and a3 of Definition 1.1.
    survivor_cents maps each surviving member id to its payment from its default fund. uncovered_cents is the
    part of the loss that no layer pays.
    """

    margin_cents: int
    default_fund_cents: int
    ccp_capital_cents: int
    survivor_cents: dict[int, int]
    uncovered_cents: int

    def total_cents(self) -> int:
        """All payments for the loss, in cents. Proposition 1.2 says this equals the loss."""
        return (
            self.margin_cents
            + self.default_fund_cents
            + self.ccp_capital_cents
            + sum(self.survivor_cents.values())
            + self.uncovered_cents
        )


def survivor_payments(
    residual_cents: int, df_cents: dict[int, int], survivors: list[int]
) -> tuple[dict[int, int], int]:
    """Split the residual loss over the surviving default funds, in cents.

    If the residual is at least the total of the survivors' default funds, each survivor pays its whole default
    fund and the excess is uncovered. Otherwise each survivor pays its floor share of the residual in proportion
    to its default fund, and the leftover cents go one each to the first survivors, in ascending id order, that
    have a positive default fund. Returns the payments and the uncovered loss.
    """
    total = sum(df_cents[i] for i in survivors)
    if residual_cents >= total:
        return {i: df_cents[i] for i in survivors}, residual_cents - total
    pay = {i: residual_cents * df_cents[i] // total for i in survivors}
    leftover = residual_cents - sum(pay.values())
    for i in survivors:
        if leftover == 0:
            break
        if df_cents[i] > 0:
            pay[i] += 1
            leftover -= 1
    if leftover != 0:
        raise RuntimeError("the leftover cents were not all assigned")
    return pay, 0


def waterfall(
    loss_cents: int,
    defaulter: int,
    im_cents: dict[int, int],
    df_cents: dict[int, int],
    capital_cents: int,
) -> Waterfall:
    """Pay one loss in the layer order of Definition 1.1.

    The layers are the defaulter's initial margin, then the defaulter's default fund, then the CCP capital, then
    the surviving default funds. Each layer pays the smaller of the loss left and its own size. Inputs are
    non-negative integers in cents.
    """
    if loss_cents < 0:
        raise ValueError("loss cannot be negative")
    margin = min(loss_cents, im_cents[defaulter])
    fund = min(loss_cents - margin, df_cents[defaulter])
    capital = min(loss_cents - margin - fund, capital_cents)
    residual = loss_cents - margin - fund - capital
    survivors = sorted(i for i in df_cents if i != defaulter)
    pay, uncovered = survivor_payments(residual, df_cents, survivors)
    return Waterfall(margin, fund, capital, pay, uncovered)


def cover_count(losses_cents: list[int], margin_cents: int) -> int:
    """Number of scenarios whose loss the margin covers in full, that is the losses with loss <= margin."""
    return sum(1 for loss in losses_cents if loss <= margin_cents)


def cover_bps(losses_cents: list[int], margin_cents: int) -> int:
    """Margin cover in basis points, floored: 10000 times the covered count, divided by the scenario count."""
    return 10000 * cover_count(losses_cents, margin_cents) // len(losses_cents)


def sized_margin(losses_cents: list[int], target_bps: int) -> tuple[int, int]:
    """The smallest margin with cover at least target_bps, by the order statistic of Proposition 2.3.

    Returns the margin in cents and the index k = ceil(target_bps * S / 10000), computed in integers as
    -((-target_bps * S) // 10000), where S is the scenario count. The margin is the k-th smallest loss.
    """
    k = -((-target_bps * len(losses_cents)) // 10000)
    return sorted(losses_cents)[k - 1], k


def brute_force_margin(losses_cents: list[int], target_bps: int) -> int:
    """The smallest integer margin with cover at least target_bps, found by testing 0, 1, 2 in turn.

    The search uses no sorting and no formula. The largest loss covers every scenario, so the search always ends
    at or before the largest loss.
    """
    for margin in range(max(losses_cents) + 1):
        if cover_bps(losses_cents, margin) >= target_bps:
            return margin
    raise RuntimeError("no integer margin reaches the target")


def show(label: str, loss: int, w: Waterfall) -> None:
    """Print the layers of one loss and whether they sum to it."""
    survivors = ", ".join(f"member {i} {v}" for i, v in sorted(w.survivor_cents.items()))
    print(
        f"{label}: loss {loss}; margin {w.margin_cents}, default fund {w.default_fund_cents}, "
        f"CCP capital {w.ccp_capital_cents}; survivors {survivors}; uncovered {w.uncovered_cents}; "
        f"layers sum to the loss: {w.total_cents() == loss}"
    )


def main() -> None:
    rng = random.Random(SEED)
    im = {i: rng.randint(1000, 5000) for i in MEMBERS}
    df = {i: rng.randint(100, 900) for i in MEMBERS}
    capital = rng.randint(500, 2000)
    im_line = ", ".join(f"member {i} {im[i]}" for i in MEMBERS)
    df_line = ", ".join(f"member {i} {df[i]}" for i in MEMBERS)
    print(f"SIMULATED inputs from seed {SEED}, in cents. Initial margins: {im_line}.")
    print(f"Default funds: {df_line}. CCP capital: {capital}. Defaulter: member {DEFAULTER}.")

    fixture_im = {1: 0, 2: 0, 3: 100}
    fixture_df = {1: 40, 2: 60, 3: 50}
    print("Part A1, fixture: defaulter 3 with margin 100, default fund 50, CCP capital 30; survivors 1 and 2 with")
    print("default funds 40 and 60. Each row is one loss.")
    fixture_ok = True
    for loss in (80, 120, 170, 180, 181, 200, 205, 300):
        w = waterfall(loss, 3, fixture_im, fixture_df, 30)
        fixture_ok = fixture_ok and w.total_cents() == loss
        show(f"loss {loss}", loss, w)
    print(f"every fixture row sums to its loss: {fixture_ok}")

    print("Part A2, remainder rule: defaulter 4 with no margin and no default fund; survivors 1, 2 and 3 with")
    print("default fund 1 each; CCP capital 0. Each row is one loss.")
    for loss in (1, 2):
        show(f"loss {loss}", loss, waterfall(loss, 4, {4: 0, 1: 0, 2: 0, 3: 0}, {1: 1, 2: 1, 3: 1, 4: 0}, 0))

    d = DEFAULTER
    survivors_df = sum(df[i] for i in MEMBERS if i != d)
    scenarios = (
        ("Part A3, within the margin", im[d] // 2),
        ("Part A3, reaching the default fund", im[d] + df[d] // 2),
        ("Part A3, reaching the surviving members", im[d] + df[d] + capital + survivors_df // 2),
    )
    print("Part A3, seeded scenarios for defaulter 3:")
    for label, loss in scenarios:
        show(label, loss, waterfall(loss, d, im, df, capital))

    losses = [rng.randint(0, MAX_LOSS_CENTS) for _ in range(SCENARIOS)]
    print(f"Part B, sizing: {SCENARIOS} seeded scenario losses from 0 to {MAX_LOSS_CENTS} cents (SIMULATED).")
    for target in TARGETS_BPS:
        margin, k = sized_margin(losses, target)
        brute = brute_force_margin(losses, target)
        print(f"target {target} bps: k = {k} of {SCENARIOS}; sized margin {margin} cents")
        print(
            f"cover at the sized margin {cover_bps(losses, margin)} bps; "
            f"cover one cent below {cover_bps(losses, margin - 1)} bps"
        )
        print(f"brute-force minimal margin {brute} cents; agrees with the sized margin: {brute == margin}")


main()
