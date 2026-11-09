# Candidate tests (verifier-written, r19) for the one-strike scan gap: scan validates df_ppm and the strike
# only in multi-strike chains. Appended to a copy of test_project.py; the fixer may use them as written.


@pytest.mark.parametrize("bad_df", [0, PPM + 1])
def test_one_strike_scan_rejects_df_outside_the_range(bad_df: int) -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="df_ppm"):
        sol.scan(hand_chain([100], [5], [1], df=bad_df))


def test_one_strike_scan_rejects_a_zero_strike() -> None:
    __tracebackhide__ = True
    with pytest.raises(ValueError, match="strictly increasing"):
        sol.scan(hand_chain([0], [5], [1]))


def test_one_strike_scan_accepts_df_at_the_range_ends() -> None:
    __tracebackhide__ = True
    assert isinstance(sol.scan(hand_chain([100], [5], [1], df=1)), list), "df_ppm = 1 is valid for one strike"
    assert isinstance(sol.scan(hand_chain([100], [5], [1], df=PPM)), list), "df_ppm = 1000000 is valid for one strike"
