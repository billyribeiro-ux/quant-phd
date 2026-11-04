"""Candidate grader test for the surviving round-5 mutant g5_02 (zero prize counted as a gain).

Not written into course/modules/E/E3/grader/test_project.py (the verifier does not edit course files). Appended to a
scratch copy of test_project.py in /tmp/e3e_r5/cand2: it passes on grader/reference.py (as elicit.py) and fails on
ledgers/E3/mutants/g5_02_mixed_check_counts_a_zero_prize_as_a_gain.py, with QF_SEED=0.
The page states the condition at project.html:197 and in the exception table at project.html:227 (a prize above zero and
a prize below zero, each with positive probability).
"""


def test_a_zero_prize_is_not_a_gain_for_mixed_sign_identification() -> None:
    """Candidate round-5 test: a prize of zero cents is neither a gain nor a loss, so responses whose lotteries hold
    only zero prizes and losses, or only zero prizes and gains, are refused."""
    no_mix = [
        {
            "pair_id": 0,
            "choice": "A",
            "prizes_a": [0, -100],
            "probs_a": ["1/2", "1/2"],
            "prizes_b": [200],
            "probs_b": ["1"],
        },
        {
            "pair_id": 1,
            "choice": "B",
            "prizes_a": [500],
            "probs_a": ["1"],
            "prizes_b": [0, 300],
            "probs_b": ["1/2", "1/2"],
        },
    ]
    must_raise(lambda: sol.estimate(no_mix), "a zero prize with a loss is not a mixed-sign lottery")
