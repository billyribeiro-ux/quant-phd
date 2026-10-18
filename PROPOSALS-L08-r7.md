# PROPOSALS-L08-r7: central edits after the round-7 L08 fixes

The branch fixes the six L08 rows of round 7 (L08-math-lab4-thm4.1-scope,
L08-math-canon-p2-every-logit, L08-lab-4-preregistration,
L08-struct-unlinked-concepts, L08-prose-sec6-every-lab, and card S7-c168
below) in `L08.html`, `L05.html`, `project.html`, the twins
`lab-S7-L08-4.py`, `lab-S7-L05-6.py` and `lab-S7-project-3.py`, and
`tests/test_memo_exemplars.py`. The following edits touch shared files and
need central action. Every old string below occurs exactly once in its file.

## Cards in `course/modules/S/S7/cards.json`

### S7-c168

Old:

```
An omitted return that is roughly constant for each trial shifts that trial's column, and adding a constant to a column can change every logit (Problem P2). A PBO on spot returns audits the selection of spot-return rules, not of the strategies a desk would trade.
```

New:

```
An omitted return that is roughly constant for each trial shifts that trial's column, and such a shift can change the logits and the PBO: in Problem P2, adding a constant to one column changes five of the six logits and moves the estimate from 2/6 to 6/6. A PBO on spot returns audits the selection of spot-return rules, not of the strategies a desk would trade.
```

### S7-c167

This supersedes section 1 of `PROPOSALS-project-r7.md`: "whose expected PBO
is one half" restates Theorem 4.1, whose assumptions this grid does not meet.

Front, old:

```
Lesson 8, Lab 4: what are the DSR of the best of 40 currency momentum rules on H.10 spot rates (2001-02 to 2026-09), and the grid's PBO?
```

Front, new:

```
Lesson 8, Lab 4: what are the DSR of the best of 40 currency sign rules on H.10 spot rates (2001-02 to 2026-09), and the grid's PBO?
```

Back, old:

```
DSR 0.489 (0.228 with the effective number of trials and variance 1/T) and PBO 0.733 with 16 blocks: what an uninformative selection produces. It is not a 73% chance of losing money.
```

Back, new:

```
DSR 0.489 (0.228 with the effective number of trials and variance 1/T) and PBO 0.733 with 16 blocks. One half is only a reference value for this grid, but 21 of the lab's 100 grids rebuilt on resampled months, which no rule can time, reach 0.733 or more, so the PBO is consistent with an uninformative selection. It is not a 73% chance of losing money.
```

The figures come from the Lab 4 output embedded on the page: `share at or
above 0.7330: 0.210` over `100 grids`.

### Optional new card (lesson L08, grade T)

The coordinator asked for the lower-bound reading to be a teaching point. If
a card is wanted:

- front: `Why does Lesson 8 read Lab 4's N = 40 as a lower bound on the search?`
- back: `Nothing on the page can show that the grid was fixed before the data were seen, or that no other grid was tried first: the count of trials is unobserved (Lesson 1, Section 7) unless a trial log records it (Lesson 1, Problem R1). A larger true search would only raise the DSR hurdle.`

## Hub `course/modules/S/S7/index.html`

"Currency momentum" is X2's concept (`fx-momentum`) and time-series momentum
is F3's; neither is in S7's closure, so the pages now say "sign rules".

| Old | New |
|---|---|
| `and PBO and DSR on a currency momentum grid.</span>` | `and PBO and DSR on a grid of currency sign rules.</span>` |
| `then an integrity memo on a real currency momentum grid, graded by rubric` | `then an integrity memo on a real grid of currency sign rules, graded by rubric` |

## Curriculum `curriculum/01-foundations.yaml` (S7 project brief)

Old: `integrity memo to an investment committee on a real currency-momentum grid`

New: `integrity memo to an investment committee on a real grid of currency sign rules`

The line rewraps in the folded block; then run `tools/render_curriculum.py`
and `tools/build_site.py` to regenerate `CURRICULUM.md`,
`curriculum/curriculum.json` and `course/assets/data/program.json`. No hours
change.

## Withdrawn claim

`PROPOSALS-G1-G3.md` (now merged) and the G1 report said the L08 Lab 4 grid
and the L05 Lab 6 universe were fixed before the code was first run. That
cannot be verified: each twin and its output entered git together. The pages
no longer make the claim. They state what a reader can check (the grid's
horizons lie within the 1-to-12-month range of `moskowitz2012time`; the code
builds the full product of the grid's lists and drops none; the output reports
every trial) and read N = 40 and K = 30 as lower bounds on the search
(Lesson 1, Section 7 and Problem R1).
