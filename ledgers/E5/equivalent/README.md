# E5 project: mutants the instant check does not separate (rulings 9 and 41)

`m02_gap_percent_of_trend.py` and `r4_m05_gap_percent_of_trend.py` compute the output gap as a percentage of trend
output instead of as the log gap. They are student errors. The E5 project's instant check compares printed tokens, and
`course/modules/E/E5/project.html` line 45 tells the learner that this check does not separate the two gap definitions.
The mutants therefore violate no behaviour the check promises and sit here instead of in `mutants/` (ruling 9). The
ledger for slice d lists only the mutants the check kills.

Evidence that they survive: `ledgers/E5/scripts/E5-d-r5/out/mutants_r5.out` (standing mutant run).
