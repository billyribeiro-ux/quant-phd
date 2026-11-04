"""Candidate tests for the grader gap found in round 5 (zero-loss scenarios). Appended to a scratch copy only.

Each expected value is hand-computed from the page's rules: the sizing index is ceil(target * S / 10000) with S counting
every scenario, and the cover divides by all S scenarios, zero losses included.
"""


def test_zero_losses_count_as_scenarios_in_the_sizing() -> None:
    """A zero loss is a scenario: with four scenarios and a target of 5000 bps, k = 2 and the margin is the second smallest."""
    __tracebackhide__ = True
    got = sol.margin_for_cover([0, 10, 20, 30], 5_000)
    assert got == 10, "a zero loss is one of the S scenarios; the index counts it, so the margin is the k-th smallest of all S"


def test_zero_losses_count_in_the_cover_denominator() -> None:
    """Two of four scenarios are at or below a margin of zero, the two zero losses; the cover divides by all four."""
    __tracebackhide__ = True
    got = sol.cover_bps([0, 0, 5, 9], 0)
    assert got == 5_000, "the cover divides by all S scenarios, zero losses included"
