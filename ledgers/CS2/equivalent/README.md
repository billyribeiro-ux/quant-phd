# CS2 project: mutants ruled not to violate the specification

Six mutants are kept here, outside `mutants/`, so that `tools/mutate_graders.py` measures only student errors
that the specification forbids. Four of them are proved equivalent or are shown to meet the stated guarantee by a
lemma; two (r15_04 and r15_06) are measured, not proved. Each file is
a single-change copy of the reference `course/modules/CS/CS2/grader/reference.py`.

The specification (`course/modules/CS/CS2/project.html`, Constraints and Conventions) states, for the sketch, the rank
guarantee of Conventions at every probe quantile q with the quantile non-decreasing in q; the named `ValueError`
conditions (7) to (10) for the sketch (epsilon, `add` with NaN, `quantile` with q outside [0, 1], and `quantile` on an
empty sketch); and the grader's other sketch checks, which the variants below pass. It states no bound on the memory
of the sketch (Conventions: "the autograder does not test memory") and no internal invariant of the sketch.

## Shared notation for the sketch

The reference keeps tuples (v_i, g_i, Delta_i), i = 1..m, with v_1 <= ... <= v_m, g_i >= 1 and Delta_i >= 0. After n
values, set R_i = g_1 + ... + g_i and M_i = R_i + Delta_i. Call g_i + Delta_i the band of
tuple i, so that the band is M_i - R_{i-1}. Here eps is the epsilon of the sketch. Insertion puts a new value x at
position p, found by
`bisect_right` (reference) or `bisect_left` (d8_02). Its tuple gets g = 1 and Delta = 0 when p is the first or past the
last position, and Delta = g_s + Delta_s - 1 otherwise, where s is the successor. Compression, after each insertion,
removes an interior tuple i (1 < i < m) and adds its g to tuple i+1 when g_i + g_{i+1} + Delta_{i+1} <= C_n, scanning
from the right. Write C_n for the cap used at count n:

- reference: C_n = floor(2 eps n) + 1
- d8_01: C_n = floor(2 eps (n-1)) + 1
- d9_04: C_n = floor(2 eps n)
- d8_02: C_n = floor(2 eps n) + 1, with `bisect_left` insertion

All three sketch variants change one thing only (the cap or the side of ties), so the lemmas below cover them together.
Every cap used here is nondecreasing in n, and every cap satisfies C_n <= floor(2 eps n) + 1.

**Lemma 0 (bookkeeping).** (a) The g values sum to n. (b) The first tuple has g_1 = 1 and Delta_1 = 0. (c) v_1 is the
minimum of the values added so far and v_m is the maximum.

Proof. (a) Each add increases n by 1 and adds one tuple with g = 1; a merge moves g from the removed tuple to its
successor. (b) Merges remove only interior tuples and change only the tuple after a removed one, which has index at
least 3, so tuple 1 is changed by nothing after its creation, and a creation at position 0 gives g = 1, Delta = 0.
(c) Tuple 1 is never removed. An insertion at position 0 happens only when x is below v_1 (`bisect_right`) or not above
v_1 (`bisect_left`), so the minimum is kept by induction. The same argument applies to tuple m, which is never removed,
and to insertion past the last position.

**Lemma 1 (copy invariant).** For every tuple i there is an integer rho_i with R_i <= rho_i <= M_i such that the
rho_i-th smallest of the n values added so far equals v_i.

Proof, by induction over the operations. Start with n = 1: one tuple with R = M = 1 and the one value at rank 1.

*Insertion.* Let c be the number of old values that precede the new value in the sorted order: c = #(<= x) for
`bisect_right`, c = #(< x) for `bisect_left`. The new value has rank c + 1 in the new sorted list.
- Tuples before p: their values are <= x (or < x), so their copies have rank <= c. Their rank is unchanged and so are
  their R and M, which do not involve the new tuple.
- Tuples after p: their values are > x (or >= x), so every value counted by c has rank below their copies. The copy
  moves to rho_j + 1, and R_j and M_j each increase by 1 because the new tuple precedes them.
- The new tuple at p = 0 or p = last: Delta = 0. For p = 0, c = 0 by Lemma 0(c), so rho = 1 = R = M. For p past the last
  position, R = n = c + 1 by Lemma 0(c) and Lemma 0(a), so rho = n = R = M.
- The new tuple at an interior p with successor s: Delta = g_s + Delta_s - 1, so R_new = R_q + 1 (q the predecessor, with
  R_q = R_{p-1}) and M_new = R_q + g_s + Delta_s = M_s (old). The predecessor has value <= x (or < x), so c >= rho_q >=
  R_q. The successor has value > x (or >= x), so c + 1 <= rho_s <= M_s. Hence c + 1 lies in [R_new, M_new].

*Compression.* Removing an interior tuple i and adding g_i to tuple i+1 leaves R_{i+1} unchanged (the prefix sum up to
i+1 does not change), leaves M_{i+1} unchanged, and leaves every other R and M unchanged. The stream values and their
ranks do not move. So each surviving tuple keeps a valid copy. The invariant holds. (Proof complete.)

**Lemma 2 (band bound).** After every add, each tuple satisfies g_i + Delta_i <= max(1, C_n).

Proof, by induction on n. A new interior tuple has band g + Delta = 1 + (g_s + Delta_s - 1) = g_s + Delta_s, which is the
old band of its successor and so is at most max(1, C_{n-1}) <= max(1, C_n), since C is nondecreasing. A new end tuple has
band 1. Insertion changes no other tuple's g or Delta. In compression the only changed band is the one of tuple i+1,
which becomes g_i + g_{i+1} + Delta_{i+1}, and the merge condition makes that at most C_n. Every other tuple keeps its
band, which is at most max(1, C_{n-1}) <= max(1, C_n). (Proof complete.)

**Lemma 3 (rank guarantee for all four sketches).** Let q be a probe, t = qn - eps n (exact rational), and
K = max(1, ceil(t)). Let i be the first index with R_i >= K; it exists because R_m = n >= K. Then the stored value v_i
satisfies both inequalities of Conventions, #(< v_i) <= qn + eps n and #(<= v_i) >= qn - eps n.

Proof. *Lower inequality.* By Lemma 1, at least rho_i values are <= v_i, and rho_i >= R_i >= K >= t.

*Upper inequality.* Values strictly below v_i have rank below rho_i, so #(< v_i) <= rho_i - 1 <= M_i - 1.
- If i = 1, M_1 = R_1 + Delta_1 = 1 by Lemma 0(b), so #(< v_1) = 0.
- If i >= 2, then R_{i-1} >= 1 (every g is at least 1) and R_{i-1} < K by minimality. So K >= 2, which means K = ceil(t), and
  K - 1 <= floor(t) because ceil(t) - 1 < t and the left side is an integer. Using Lemma 2 for the band of tuple i,
  #(< v_i) <= M_i - 1 = R_{i-1} + band_i - 1 <= K - 2 + max(1, C_n) <= (floor(t) - 1) + (floor(2 eps n) + 1)
  = floor(t) + floor(2 eps n) <= floor(t + 2 eps n) = floor(qn + eps n).
  The integer count is therefore at most qn + eps n.

The target is nondecreasing in q, so i is nondecreasing in q, and the stored values are sorted, so quantile(q) is
nondecreasing in q. (Proof complete.)

Consequently the reference, d8_01, d9_04 and d8_02 all satisfy the rank guarantee of Conventions for every stream and
every probe q. None of them violates the specification, so none is a student error. Their differences are confined to
the cap and to ties, and the only cap property used above is `max(1, C_n) <= floor(2 eps n) + 1`. d9_04 has C_n one smaller than the
reference, and d8_01 has C_n no larger than the reference at every n.

Scratch check. `ledgers/CS2/scripts/CS2-d-r9/readme_guarantee_check.py` (output in `readme_guarantee_check.out.txt`)
runs the reference and the three variants on 200 seeded streams of up to 60 values, with ties, sorted and reversed
runs and values rounded to one decimal, and epsilon in {0.05, 0.1, 0.2, 0.3}. After every add it checks the sum of the
g values against n, the first tuple (g = 1, Delta = 0), and both inequalities of Conventions at 41 probes (q = k/40),
with exact Fraction counts. Each of the four sketches gave 0 rank violations over 252,437 (add, probe) pairs and 0
bookkeeping failures. The script does not check the band bound of Lemma 2 or the copy invariant of Lemma 1; those rest
on the proofs above only. This is a sanity check on the lemmas, not a substitute for them.

## rank_target_without_clamp.py (m14_01): the rank target is not clamped to at least 1

Claim: `quantile` returns the same value with and without `max(1, ...)` around the rank target, so the mutant
satisfies every stated outcome.

Proof. Every stored tuple has g >= 1, so after the first tuple the running rank is at least 1. The loop returns the
first stored value whose running rank is at least the target K. The clamp changes K only when the unclamped K is below
1, and then the clamped value is 1. In that case the first tuple already has running rank g_0 >= 1, and both targets
(the clamped 1 and the unclamped value below 1) are at most 1, so the loop returns `values[0]` in both versions. If the
unclamped K is at least 1, both versions use the same K. The two functions are identical on every input with n >= 1.
The empty-sketch guard precedes the target and is unchanged. Hence the mutant is extensionally equal to the reference.
(The spec's "at least 1" describes the target, not an observable behaviour.)

## r15_04_sketch_interior_delta_without_minus_one.py (r15_04): the inserted tuple's delta drops the minus one

Claim: when a new interior tuple is inserted with successor s, the mutant sets its delta to g_s + Delta_s instead of
g_s + Delta_s - 1. No search below found a violation of the rank guarantee of Conventions for this mutant. This is
measured, not proved (rulings 9, 25 and 40). No proof is claimed for it.

Evidence, three searches. The same three searches cover r15_06 (next section), and each found 0 violations for the
reference as a control.

(i) Exhaustive small streams. `ledgers/CS2/scripts/CS2-d-r1/r15_04_06_extra.py` (output `r15_04_06_extra.txt`) runs
every stream of length 1 to 7 over the values {0, 1, 2, 3} (4 + 16 + ... + 4^7 = 21,844 streams) at each of the
epsilons 0.3 and 0.2: 43,688 streams in all. After every add it checks both inequalities of Conventions at the 41
probes q = k/40 (k = 0 to 40), with exact Fraction counts, and the monotonicity of quantile(q) in q. Output:
`r15_04 exhaustive small streams 43688 violations 0`.

(ii) Randomised long streams. The same script runs 120 seeded streams of 60 to 160 values (epsilon chosen from 0.3,
0.2 and 0.1; values rounded to zero or one decimal; every third stream sorted), checked after every add at the same 41
probes. Output: `r15_04 random long streams 120 violations 0`.

(iii) Randomised final-state battery. `ledgers/CS2/scripts/CS2-d-r15/guarantee_battery_r15.py` (output
`guarantee_battery_r15.txt`) checks the final state of a sketch after n values, at 51 probes per stream (q = k/40 for
k = 0 to 40, and 10 random q), on 300 streams (5 epsilons times 60 trials, n up to 300, with ties, sorted runs and values
rounded to one or six decimals). Output: `checks=15300 violations=0` for the reference, for r15_04 and for r15_06.

Scope of the evidence. Search (i) covers only the 4-value alphabet and streams of length at most 7, at two epsilons.
Search (ii) and (iii) are random samples. The battery checks the final state only. None of the searches checks the band
bound of Lemma 2 or the copy invariant of Lemma 1. A violation outside these domains is not excluded.

Why the lemmas above do not cover it. The new tuple's band is g_s + Delta_s + 1, one more than the successor's band.
The argument of Lemma 2 gives the successor a band of at most max(1, C_{n-1}), so it gives this tuple at most
max(1, C_{n-1}) + 1. That is not at most max(1, C_n) when the cap does not grow from n - 1 to n, so the bound is not
established by these lemmas. The upper inequality of Lemma 3 depends on that bound, so for this mutant the measurement
is the only evidence.

## r15_06_sketch_interior_delta_is_floor_2en.py (r15_06): the inserted tuple's delta is the cap, not g + delta - 1

Claim: when a new interior tuple is inserted, the mutant sets its delta to floor(2 eps n), with n the count after the
insertion, instead of g_s + Delta_s - 1. No search below found a violation of the rank guarantee of Conventions for this mutant.
This is measured, not proved (rulings 9, 25 and 40). No proof is claimed for it.

Evidence, the same three searches as for r15_04 (see that section for the scripts, the streams and the counts):
(i) exhaustive small streams: 43,688 streams, 0 violations; (ii) randomised long streams checked after every add:
120 streams, 0 violations; (iii) randomised final-state battery: `checks=15300 violations=0`.
The scope limits of (i) to (iii) given for r15_04 apply here too.

What the lemmas give for this mutant. The band of the inserted tuple is 1 + floor(2 eps n) = C_n, so Lemma 2 holds for
that tuple. The steps of Lemmas 1 and 3 that concern its copy were not written out for this mutant, so the claim rests on
the measurement.

## Status

The six files here are not killed by the grader, and none is shown to violate a behaviour that the specification
states. m14_01 is extensionally equal to the reference. d8_01, d9_04 and d8_02 satisfy Lemmas 1 to 3 above, which prove
the rank guarantee of Conventions for each of them. r15_04 and r15_06 are measured, not proved (rulings 9, 25 and 40):
the searches above found no violation, and no proof is claimed for either. If a reviewer finds a gap in a lemma, or a
violation for r15_04 or r15_06, the matching test must name the condition in project.html first, and the file moves
back to `mutants/` only if it violates a stated outcome.

The non-equivalent survivor r15_07 (the NaN check runs after count, mean and M2 change) is not here. After a refused
`update(nan)` it leaves the state altered, and Conventions (project.html:216) requires the statistics to describe every
value added so far. It is a student error in `mutants/`, killed by `test_welford_refused_nan_leaves_the_accepted_state`.
