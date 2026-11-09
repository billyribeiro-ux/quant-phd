# FC2 project: mutants that the stated behaviour does not separate (ruling 9, ruling 34)

The page requires each scan explanation to be non-empty and to name the rules it relies on (parity: P1, P2, P3, P4, P6;
convexity: P1, P2, P5, P6). It states no content for the explanation text beyond that. The grader checks exactly that, by
asserting that the set of rule labels in each explanation equals the spec's list (`test_scan_explanations_are_nonempty_and_name_the_rule`).

The three mutants here keep every output and every rule label of the reference and change only the free text of an explanation:

- `r15_a_parity_explanation_reverses_the_positive_gap_trade.py`: the explanation text describes the reverse trade.
- `r15_c_parity_explanation_prints_gross_where_net_belongs.py`: the explanation prints a gross amount where the reference prints the net.
- `r15_d_convexity_explanation_reverses_the_chord_side.py`: the explanation names the other side of the chord.

Why no test separates them: the page does not say what an explanation's wording must be, so a test on the wording would
assert something the learner was never told. If the page is later amended to state the explanation content, these three
move back to `mutants/` with a test (verifier round 15 ruled them non-findings for the same reason).

All three pass the grader on seeds 0-9, as the equivalent-mutant rule expects.
