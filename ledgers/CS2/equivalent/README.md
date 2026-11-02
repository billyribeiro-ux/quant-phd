# CS2 project: mutants ruled not to violate the specification

Four mutants survive the project grader on seeds 0-9 and are kept here, outside `mutants/`, so that
`tools/mutate_graders.py` measures only student errors that the specification forbids. Each file is
a single-change copy of the reference `course/modules/CS/CS2/grader/reference.py`.

The specification (`course/modules/CS/CS2/project.html`, Constraints and Conventions) states outcomes only for: the
ten named `ValueError` conditions, the Welford statistics against the exact `Fraction` reference, the rolling
minimum and maximum against brute force, and the rank guarantee of Conventions at every probe quantile q, with the
quantile non-decreasing in q. It states no bound on the memory of the sketch (Conventions: "the autograder does not
test memory") and no internal invariant of the sketch.

## m14_01_rank_target_no_clamp.py: the rank target is not clamped to at least 1

Claim: `quantile` returns the same value with and without `max(1, ...)` around the rank target, so the mutant
satisfies every stated outcome.

Proof. Every stored tuple has g >= 1, so after the first tuple the running rank is at least 1. The loop returns the
first stored value whose running rank is at least the target T. The clamp changes T only when the unclamped T is below
1, and then the clamped value is 1. In that case the first tuple already has running rank g_0 >= 1, and both targets (the clamped 1 and the
unclamped value below 1) are at most 1, so the loop returns `values[0]` in both versions. If the
unclamped T is at least 1, both versions use the same T. The two functions are identical on every input with n >= 1. The empty-sketch guard precedes the target and is unchanged. Hence the mutant is extensionally equal to
the reference. (The spec's "at least 1" describes the target, not an observable behaviour.)

## d8_01_sketch_cap_counts_previous_value.py and d9_04_sketch_cap_without_plus_one.py: compression cap smaller by one

Claim: the compression cap of the reference is `cap(n) = floor(2 eps n) + 1`. The mutants use
`cap(n) = floor(2 eps (n-1)) + 1` (d8_01) and `cap(n) = floor(2 eps n)` (d9_04). Both are nondecreasing in n and at
most the reference cap, so each merges fewer tuples.

Band lemma (induction on the number of values added). Write b_i = g_i + delta_i for the band of stored tuple i. Claim:
at every time b_i <= max(1, cap(n)) for all i.
- A merge happens only when the merged band g_i + g_{i+1} + delta_{i+1} is at most cap(n), so the merged tuple
  satisfies the bound.
- An interior insertion at position p creates a tuple with g = 1 and delta = b_succ - 1, so its band is b_succ,
  which is at most max(1, cap(n-1)) <= max(1, cap(n)) by the induction hypothesis. Insertion at either end has
  delta = 0 and band 1.
- Untouched tuples keep their bands.
Hence every delta_i <= max(0, cap(n) - 1) <= floor(2 eps n), which is the only property of the compression cap that
the rank argument uses (the rank argument for the reference, as in design.md, needs delta_i <= floor(2 eps n) and
nothing else from the cap).

Reduction, stated as a claim about the reference's proof rather than re-derived here: the rank argument needs
rmax_{i-1} = rmin_{i-1} + delta_{i-1} < qn + eps n for the tuple before the answer, which holds whenever
delta_{i-1} <= 2 eps n. Both mutants satisfy that bound, so the two rank inequalities hold for them wherever they hold
for the reference. The lower inequality uses only rmin_i, which the merges preserve.

Evidence (not a substitute for the reduction above): with the exact rank battery of
`ledgers/CS2/scripts/CS2-d-r15/guarantee_battery.py`, 20,000 random trials (n up to 400, eps 0.05, 0.1, 0.2), both
mutants give 0 violations, as does the reference. A dense search over every q on a grid of 1/200 plus 20 random q,
with eps in {0.01, 0.05, 0.07, 0.1, 0.2, 0.3, 0.45} and streams of up to 160 values (duplicates, sorted, reversed,
alternating), gives 0 violations for each mutant over 4,500 trials.

## d8_02_sketch_insert_bisect_left.py: insertion before equal stored values

Claim: inserting a new value at `bisect_left` instead of `bisect_right` places it before any equal stored values.
The insertion band is still b_succ (the successor is the tuple at the insertion point in both variants), so the band
lemma above holds unchanged, and the reduction and the lower inequality apply as for d8_01 and d9_04. The stored values
are the same multiset in both variants; only which of several equal tuples carries which g and delta differs. The
rank guarantee counts every copy of a value, so the two inequalities depend only on the multiset of values and the
bands, not on which copy holds the band.

Evidence: the same batteries as above, with duplicate-heavy streams (values in {0, 1, 2} and {0, ..., 4}) and streams
up to 160 values, give 0 violations over 1,500 + 3,000 trials.

## Status

These four are not killed by the grader, and no stated behaviour of the specification is violated in the checks
above. If the architect finds a violation, the matching test must name the condition in project.html first. The
reduction in the band lemma is argued here, and the reference's own rank proof (design note) is assumed to use
the band bound only, which is the step a reviewer should check.
