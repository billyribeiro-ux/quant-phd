"""Verifier CS2-d round 4: the row table for ledgers/CS2/CS2-d.json (every round 3 id kept, plus new ids)."""

import json
from pathlib import Path

P, F, U = "PASS", "FAIL", "UNVERIFIABLE"
R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        d["fix"] = fix
    R.append(d)


# ---------------------------------------------------------------- project slice
row("proj-run-graders", "2.6-autograder-1", "course/modules/CS/CS2/grader/reference.py", P,
    "python tools/run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds)'; out/run_graders.txt")
row("proj-collect-count", "2.6-spec-count", "course/modules/CS/CS2/project.html:211 ('collects 141 checks')", P,
    "pytest --collect-only with QF_SEED = 0 to 49 on the reference: 141 collected for all 50 seeds; the page's pytest command with QF_SEED=3 on the reference: 141 passed; on the starter: 138 failed, 3 passed")
row("proj-pytest-pin", "2.6-spec-local", "course/modules/CS/CS2/project.html:257 ('Use Python 3.14 and pytest 9.0.2')", P,
    "requirements-dev.txt:2 pytest==9.0.2; course/assets/vendor/LOCK.json:432 pyodide/pytest-9.0.2 wheel; .venv pytest 9.0.2")
row("proj-instances-distinct", "2.6-instances", "course/modules/CS/CS2/grader/instance.py:30-47", P,
    "python -I: 50 distinct payloads for seeds 0-49; instance.py is byte-identical since aa3c26c")
row("proj-instance-labelled", "2.8-simulated-label", "course/modules/CS/CS2/grader/instance.py:47", P,
    "label f'SIMULATED stream {seed}'; test_instance_is_valid_and_labelled_simulated passes on seeds 0-49 (collection and reference run)")
row("proj-mutants-killed", "2.6-mutation", "ledgers/CS2/mutants/ (56 files); course/modules/CS/CS2/grader/test_project.py", P,
    "tools/mutate_graders.py --unit CS2 --seeds 0-49: 55 of 55 student-error mutants killed (out/mutate_0-49_r2.txt). The one survivor, d4_03, is an alternative correct implementation, not a student error (row proj-mutant-d4_03-not-a-fault); the tool's FAIL line is caused by that file alone")
row("proj-mutant-d4_03-not-a-fault", "2.6-over-constraint", "ledgers/CS2/mutants/d4_03_mean_is_running_sum_over_count.py", P,
    "candidate run: ledgers/CS2/scripts/CS2-d-r1/run_candidates.py 0-49 on d4_03: 50/50 seeds pass (out/alts_existing.txt). The page never requires mean() to be computed by the Welford update: project.html:37 asks for 'the online mean and variance without a second pass', and a running sum divided by the count is online",
    None)
row("proj-r4-mutants-killed", "2.6-mutation", "ledgers/CS2/mutants/r4_01..r4_05", P,
    "five verifier mutants: r4_01 decimal-text rank rationals (killed by test_sketch_rank_guarantee_on_short_streams[2-0.1]); r4_02 rank target floor(qn - eps n) (killed, [2-0.05]); r4_03 variance(1) with n=2 divides by 2 (killed by test_welford_sample_variance_of_two_values_is_defined); r4_04 M2 increment from the updated mean (killed, same test); r4_05 expiry compares values not indices (killed by test_rolling_ties_expire_with_their_index[2])")
row("proj-alt-implementations-A-D", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r1/alts/alt_a..alt_d", P,
    "run_candidates.py 0-49: alt A 50/50, alt B 50/50, alt C 50/50, alt D 50/50 (out/alts_existing.txt)")
row("proj-alt-F-floor-plus-one", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r3/alts/alt_f_floor_plus_one_rank.py", P,
    "run_candidates.py 0-49: 50/50 seeds pass (out/alts_existing.txt)")
row("proj-alt-G-count-threshold", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_g_count_threshold_no_ceiling.py", P,
    "new in round 4: exact sorted list; answer is the smallest stored value whose exact count reaches qn - eps n, no ceiling. run_candidates.py 0-49: 50/50 (out/alts_new.txt)")
row("proj-alt-I-ceil-minus-floor", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_i_ceil_minus_floor_cutoff.py", P,
    "new in round 4: target max(1, ceil(qn) - floor(eps n)), a different valid cutoff (rank k-1 <= qn+eps n and k >= qn-eps n). run_candidates.py 0-49: 50/50 (out/alts_new.txt)")
row("proj-alt-K-chan-merge-welford", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_k_chan_merge_welford.py", P,
    "new in round 4: Welford state merged one value at a time with Chan's pairwise formula. run_candidates.py 0-49: 50/50 (out/alts_new.txt)")
row("proj-alt-L-coerce-inputs", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_l_coerce_inputs_to_numbers.py", P,
    "new in round 4: float() on values, int() on the window, so True, ' 2.5 ' and 3.0 are answered for the number they denote; run_candidates.py 0-49: 50/50 (out/alt_l_coerce.txt). Shows the window and value rules do not reject a correct coercing implementation")
row("proj-alt-e-float-cutoff-is-a-fault", "2.6-spec-claim", "ledgers/CS2/scripts/CS2-d-r1/alts/alt_e_float_cutoff_sketch.py; course/modules/CS/CS2/project.html:219", P,
    "alt E fails 50/50 seeds, on test_sketch_rank_target_is_exact_where_a_float_target_is_one_short (all seeds) and the rank guarantee tests. The page says the rank inequalities 'have no tolerance' and that 'a rank target computed in floating point can fall one rank short' (line 219), so E violates a stated rule")
row("proj-nearest-rank-not-a-fault", "2.6-equivalence", "ledgers/CS2/scripts/CS2-d-r1/alts/alt_c_shifted_sums_sorted_window.py", P,
    "alt C (shifted sums, sorted-window rolling, exact sketch with target ceil(qn)) passes 50/50 (out/alts_existing.txt)")
row("proj-exact-rank-witness", "2.6-spec-claim", "course/modules/CS/CS2/project.html:219; grader/test_project.py test_sketch_rank_target_is_exact_where_a_float_target_is_one_short", P,
    "python3 -I: ceil(Fraction(0.1)*20 - Fraction(0.05)*20) = 2 and float 0.1*20 - 0.05*20 = 1.0, ceil 1; the page's 'exact target is 2' and 'gives 1' both match")
row("proj-run-labs", "2.5-labs", "course/modules/CS/CS2/project.html lab-CS2-project-1..3; tests/labs/CS2/lab-CS2-project-*.py", P,
    "tools/run_labs.py --unit CS2 --page project: PASS (3/3); python -I -W error on lab-CS2-project-1 runs cleanly (out/lab-CS2-project-*.txt)")
row("proj-page-smoke", "2.5-pyodide", "course/modules/CS/CS2/project.html", P,
    "tools/page_smoke.py --unit CS2 --pages project: PASS; 'in-browser grader: All 141 tests pass on seed 1099113635'; out/page_smoke_project.txt")
row("proj-lab1-numbers", "2.2-numbers-lab", "course/modules/CS/CS2/project.html:130-144", P,
    "every printed line of the page block (lines 130-144) is present verbatim in the fresh run of lab-CS2-project-1 (out/lab-CS2-project-1.txt); 44 deque operations <= 4n = 48 (line 144) matches the run")
row("proj-lab2-numbers", "2.2-numbers-lab", "course/modules/CS/CS2/project.html:185-187", P,
    "lines 185-187 (count 8, mean 1000003.750000, sample variance 8.500000) match the completed lab-CS2-project-2 run; the mean 1000003.75 and variance 8.5 recomputed from the eight offsets 2,5,1,4,9,3,6,0 (sum of squared deviations 59.5, divided by 7)")
row("proj-lab3-numbers", "2.2-numbers-lab", "course/modules/CS/CS2/project.html:329-341", P,
    "lines 329-337 match the fresh run of lab-CS2-project-3 verbatim; recomputed: sum 110046.0, mean 10004.181818, exact sample variance 8.313636, median target 5 (ceil(5.5-1.1)=5), 5th smallest 50016/5 = 10003.2 (python3 -I with Fraction)")
row("proj-hours-arithmetic", "2.2-hours", "course/modules/CS/CS2/project.html:233-241; index.html data-hours-lessons=100, data-hours-project=30; L01-L11 data-hours", P,
    "project table 2+3+4+4+4+6+4+3 = 30; lesson data-hours 8+9+10+10+9+9+10+10+10+8+7 = 100; 100 + 30 = 130 as the page states. Pace not judged (architect ruling)")
row("proj-ladder", "2.9-structure", "course/modules/CS/CS2/project.html:40-49, 51-190, 400-406", P,
    "tools/check_projects.py --unit CS2: PASS; rungs 1 (worked example), 2 (completion, class lab completion), 3 (independent), 4 (stretch) in order")
row("proj-interface-signatures", "2.6-spec-interface", "course/modules/CS/CS2/project.html:202; grader/starter.py:13-52", P,
    "starter signatures: WelfordAccumulator.update(x: float) -> None, count property, mean(), variance(self, ddof: int = 1); RollingMinMax(window: int) with push/minimum/maximum; QuantileSketch(epsilon: float) with add/quantile; the page's line 202 matches (ddof 0 and 1 described under Conventions)")
row("proj-named-conditions-tested", "2.6-named-conditions", "course/modules/CS/CS2/project.html:209 (Constraints, conditions 1-10); grader/test_project.py", P,
    "each of the ten named conditions has a test that expects ValueError: (1) test_welford_mean/variance_before_any_value_raises; (2) test_welford_sample_variance_of_one_value_raises; (3) test_welford_nan_update_raises; (4) test_rolling_window_zero_raises; (5) test_rolling_nan_push_raises; (6) test_rolling_minimum/maximum_before_push_raises; (7) test_sketch_epsilon_outside_open_interval_raises; (8) test_sketch_nan_add_raises; (9) test_sketch_quantile_outside_closed_interval_raises; (10) test_sketch_quantile_on_empty_sketch_raises")
row("proj-unnamed-conditions-any-exception", "2.6-unnamed", "course/modules/CS/CS2/grader/test_project.py (refuse_or_correct and the ddof, infinity, bool, string and float tests)", P,
    "every test that is not a named condition goes through refuse_or_correct or accepts 'any exception' (ddof, infinity); no unnamed condition requires ValueError (grep of must_raise calls: all arguments are named conditions)")
row("proj-failure-messages", "2.6-feedback", "course/modules/CS/CS2/grader/test_project.py (every pytest.fail message)", P,
    "every message names the property and none prints an expected value; read in full (lines 1-695)")
row("proj-stdlib-only", "2.6-stdlib", "course/modules/CS/CS2/grader/test_project.py test_standard_library_only; grader/reference.py imports", P,
    "reference.py imports math, bisect, collections, fractions; test passes on the reference")
row("proj-rubric-calibration", "2.3-rubric-structure", "course/modules/CS/CS2/project.html:362-391 (Exemplar A official scoring and annotations)", F,
    "Exemplar A is officially scored C1 2, C2 2, C4 2, C5 2, C6 2, but its own annotations state the rubric's level-1 descriptors. Rubric C1 level 1: 'No hypotheses are listed'; the exemplar says 'C1, level 2: no hypotheses are listed'. Rubric C2 level 2 needs 'Shows both cases'; the exemplar says 'The base case is clear' and shows none. Rubric C4 level 1: 'Does not state an arithmetic'; the exemplar says 'C4 is not met here, because the proof does not name an arithmetic'. Rubric C5 level 1: 'No guarantee is stated'; the exemplar says 'the guarantee is not stated and no probe set is given'. Rubric C6 level 1: 'Asserts speed or stability with no measurement'; the exemplar's 'fast' claim has no measurement. Exemplar B scores (all 4) match the level-4 descriptors (checked line by line)",
    "Set Exemplar A's official scores to the rubric level its annotations describe: C1 1, C2 1, C4 1, C5 1, C6 1 (C3 2 stays, since M is named but not tied to a sum of squares, which is level 2). Re-check the self-assessment divergence text against the new scores.")
row("proj-rubric-exemplar-b-c1", "2.3-exemplar-claim", "course/modules/CS/CS2/project.html:379-384 (Exemplar B proof and C1 annotation)", P,
    "the hypotheses H1 (n positive), H2 (values real), H3 (exact arithmetic) are listed before the statement and each is cited at its step ('By H2, x_{n+1} and m_n are real numbers', H1 at the division, H3 for the algebra); the algebra was re-derived: a = -delta/(n+1), sum of 2a*(deviations) = 0, M_n + n delta^2/(n+1)^2 + n^2 delta^2/(n+1)^2 = M_n + n delta^2/(n+1), and delta*(x_{n+1}-m_{n+1}) = n delta^2/(n+1). The round 3 failure (H2 uncited) is fixed")
row("proj-rubric-numbers-locators", "2.2-numbers-in-exemplars", "course/modules/CS/CS2/project.html:369-390; grader/instance.py:8-11", P,
    "numbers in the exemplars: 8.313636 (= Lab 3 exact sample variance, recomputed), 44 and 48 (Lab 1, recomputed), ceiling rule and 'at least 1' (= reference.py quantile), probe set = PROBES_FIXED + one seeded value (instance.py:27-28). Provenance of the probe set and the epsilon values is a separate row")
row("proj-exemplar-number-provenance", "2.2-numbers-provenance", "course/modules/CS/CS2/project.html:363 (rule) vs 386-387 (exemplar B design note)", F,
    "project.html:363 says 'Each number in them is printed by Lab 1, Lab 2 or Lab 3, or is computed from those printed values with the calculation shown'. Exemplar B's design note (line 386) gives the probe set (0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1, one seeded value), the epsilons 0.05, 0.1, 0.2 and the streams of one to eight values. None of these is printed by a lab or computed from a printed value; they are grader constants (instance.py:27-29)",
    "Either change line 363 to say that the probe set and epsilon values are the specification's constants (instance.py), or cite them as such in exemplar B. The rubric's C5 needs the probe set named, so the exemplar content stays.")
row("proj-banned-phrases", "2.9-banned", "course/modules/CS/CS2/project.html (visible prose)", P,
    "scan for roughly, about, historically, typically, usually, generally, ellipsis and process words (build, builder, round, verifier, REQUEST): no banned phrase; scope words (every, only, any, same, never, about) were each checked against a computation or a test (see proj-named-conditions-valid-input-claim, proj-rank-guarantee-claims-rechecked)")
row("proj-dag-concepts", "DAG-concepts", "course/modules/CS/CS2/project.html (concept links welford-algorithm, monotonic-deque, quantile-sketch, mathematical-induction)", P,
    "tools/check_dag.py --unit CS2: PASS. The three algorithm concepts are introduced by CS2's own lessons L09, L10, L11 (concept links point to those lessons)")
row("proj-citation-cormen", "2.1-citations", "course/modules/CS/CS2/project.html:409-413 (Reading); references/references.json:5962", P,
    "tools/verify_refs.py --unit CS2 (live): 1 of 560 entries re-verified, 0 problems (out/verify_refs_live.txt); --offline: 560 entries, 0 problems. The record has pages null and no section field, so 'names no page or section' is true. No content of the textbook is read or quoted")
row("proj-lint-typecheck", "2.9-gate", "course/modules/CS/CS2/grader; tests/labs/CS2 project labs", P,
    "ruff check (grader and project labs): All checks passed; ruff format --check: 4 files already formatted; mypy --no-incremental on reference.py, instance.py, starter.py: no issues; mypy --no-incremental on test_project.py: no issues")
row("proj-claim-tolerance-prose", "2.6-spec-claim", "course/modules/CS/CS2/project.html:219 ('Exact counts')", P,
    "the mean and variance use the relative 1e-9 and absolute 1e-9 tolerance (close() in test_project.py); rank inequalities have no tolerance (test_sketch_rank_guarantee_at_each_probe uses Fraction)")
row("proj-named-conditions-valid-input-claim", "2.6-spec-claim", "course/modules/CS/CS2/project.html:224 ('Named errors, in brief')", P,
    "'A value just inside a bound is valid: a window of 1, an epsilon of 0.000001, a q of 0 and of 1, and a variance with ddof 0 on a single value each return an answer': tests test_rolling_window_one_is_valid, test_sketch_small_epsilon_is_valid, test_sketch_quantile_at_both_ends_is_valid, test_welford_population_variance_of_one_value_is_zero pass on the reference and on alternatives A-L")
row("proj-curriculum-scope-rolling", "2.6-scope", "course/modules/CS/CS2/project.html:196, 216-217; curriculum/01-foundations.yaml:445 (project brief); curriculum/curriculum.json (CS2 project.brief)", F,
    "The curriculum brief says 'Implement O(1)-update rolling mean, variance (Welford), min/max ...'. The page says 'Both describe every value added so far, not a window' (line 216: the Welford statistics are cumulative). The plan (6.3) and the page agree; the curriculum's word 'rolling' does not",
    "Edit curriculum/01-foundations.yaml line 445 to 'running (cumulative) mean and variance (Welford)', regenerate curriculum.json with tools/render_curriculum.py, and re-run check_projects. This is an upstream text change for the owner of the curriculum, not a page change.")
row("proj-lab3-interpretation", "2.5-lab-interpretation", "course/modules/CS/CS2/project.html:338 vs tests/labs/CS2/lab-CS2-project-3.py", P,
    "'the True line compares the float Welford mean with the float of the exact mean, using the unrounded values' matches the code (abs(mean_w - float(mean_exact)) <= 1e-9); 'The lab does not show a sketch' matches the code; 'The median target is rank 5' matches target = max(1, ceil(q n - eps n)) = 5")
row("proj-lab2-every-pair", "2.5-lab-claims", "course/modules/CS/CS2/project.html:150, 188", P,
    "'When both blanks are right, the output lines match the expected output below exactly': the completed lab-CS2-project-2 (mean = mean + delta / count; m2 = m2 + delta * (x - mean)) prints the three lines of line 185-187 exactly. 'The lab does not compare its result with exact arithmetic' is true of the code")
row("proj-rubric-c5-partly", "2.3-rubric-levels", "course/modules/CS/CS2/project.html:356 (C5 descriptors)", P,
    "rubric row C5 read in full: level 4 names both inequalities, probe set, streams and the three limits; level 3 names the guarantee and the probe set with one or two limits; level 2 and 1 are as stated. The level descriptors are complete and mutually exclusive, and no level text is vague")
row("proj-instance-docstring-claims", "2.6-docstring-claim", "course/modules/CS/CS2/grader/instance.py:8-16", P,
    "recomputed with ledgers/CS2/scripts/CS2-d-r4/naive_by_offset_r4.py (out/naive_by_offset_r4.out.txt): offset 0: 16 seeds, 0 naive failures; offset 10,000: 23 seeds, 22 naive failures (seed 41 passes); offset 1,000,000: 11 seeds, 11 failures; Welford passes all 50 seeds. The formula order in the docstring is the order used")
row("proj-exemplar-b-constant-stream-claim", "2.6-claim-vs-test", "course/modules/CS/CS2/project.html (Exemplar B design note); grader/test_project.py test_sketch_constant_stream_returns_the_constant", P,
    "exemplar B says 'a constant stream is checked to return its value': test_sketch_constant_stream_returns_the_constant uses 40 copies and every probe; passes on the reference and alternatives")
row("proj-rank-guarantee-claims-rechecked", "2.6-rank-claims", "course/modules/CS/CS2/grader/test_project.py (rank tests, 'rank guarantee' block, the new witness)", P,
    "each rank test checks both inequalities with Fraction qn and eps n (lines 'if not (below <= qn + slack)' and 'at_or_below >= qn - slack'); alternatives G, I, K, L, A-D, F pass 50/50; E fails as the page requires")
row("proj-test-docstring-short-stream", "2.6-docstring-claim", "course/modules/CS/CS2/grader/test_project.py test_sketch_rank_guarantee_on_short_streams docstring", P,
    "docstring: 'With epsilon 0.05 and 0.1 the slack is below one rank at every length here; with epsilon 0.2 it is below one up to length four'. Recomputed: 0.1*8 = 0.8, 0.05*8 = 0.4, 0.2*4 = 0.8, 0.2*5 = 1.0 (not below one), so the docstring is correct")
row("proj-check-pages-unit", "2.9-structure-gate", "course/modules/CS/CS2/project.html (tools/check_pages.py --unit CS2)", P,
    "tools/check_pages.py --unit CS2: PASS")

# ---------------------------------------------------------------- cards.json
row("cards-structure", "2.7-structure", "course/modules/CS/CS2/cards.json", P,
    "167 cards, 129 T and 38 C; field sets: {id, lesson, front, back, grade} for 129, plus basis for 38; no duplicate ids; ledgers/CS2/scripts/CS2-d-r4/cards_checks_r4.py (out/cards_checks_r4.out.txt)")
row("cards-grade-field", "2.7-plan-fields", "course/modules/CS/CS2/cards.json", P,
    "every card has a grade (round 3's 42 missing grades are fixed); no T card has a basis; every C card has a basis that names a lab")
row("cards-count-vs-plan", "2.7-plan-count", "course/modules/CS/CS2/cards.json; plans/CS2-build-plan.md section 9", F,
    "plan section 9: 'Expected total 50-80 cards'. The file has 167 cards (129 T, 38 C); round 3 had 155. The count is outside the plan's band",
    "Either cut the deck to the plan's 50-80 cards or amend plan section 9 with the reason the deck is larger; the architect decides which. Not a text error in any card.")
row("cards-c075-lab-result-ungraded", "2.7-grade-rule", "course/modules/CS/CS2/cards.json CS2-c075 (L06)", P,
    "CS2-c075 is now grade C with basis 'Lab 1, Part A (SIMULATED seeded graphs, one run)', as architect ruling (e) requires for a SIMULATED lab result")
row("cards-c151", "2.4-arithmetic", "course/modules/CS/CS2/cards.json CS2-c151 (grade T, lesson L11)", P,
    "(L+1)(L+2)(L+3)/(3 eps) + (L+1) with L = 29, eps = 1/20: 29760/0.15 + 30 = 198430 (recomputed); L = 12: 2730/0.15 + 13 = 18213 (recomputed); both match L11's line 59. The round 3 value 18187 is the exact sum (line 225), now correctly named as the bound's upper estimate. The back answers the front by the two regimes (far below n at 1e9, above n at 5000), so no fix is needed")
row("cards-numbers-in-lesson", "2.7-numbers-in-lesson", "course/modules/CS/CS2/cards.json (all 167 backs vs their lesson text)", P,
    "automated (cards_checks_r4.py): every number in every back occurs in its own lesson's extracted text; 0 misses")
row("cards-duplicates", "2.7-duplicate-scan", "course/modules/CS/CS2/cards.json", P,
    "no duplicate fronts or backs (cards_checks_r4.py); no two cards share a front or a back; c008 (correct) and c165 (fails, see cards-c165) both concern the same inequality")
row("cards-theorem-section-refs", "2.7-refs", "course/modules/CS/CS2/cards.json", P,
    "every Definition, Proposition, Lemma, Theorem, Corollary, Remark, Assumption, Problem and Example locator in a back appears in its own lesson (cards_checks_r4.py: 0 absent)")
row("cards-basis-labels", "2.7-basis", "course/modules/CS/CS2/cards.json (grade C cards)", P,
    "all 38 C cards have a basis that names Lab (cards_checks_r4.py); the basis matches the lab named in the lesson for each checked card")
row("cards-changed-group", "2.7-changed-cards", "course/modules/CS/CS2/cards.json: 65 changed and 12 added cards", F,
    "all 77 changed or added cards were read against their lesson text. Four of them fail on their own rows (cards-c035, cards-c084, cards-c155, cards-c165), and cards-c114 and cards-c124 are minor failures; the rest agree with the lesson text",
    "Fix the rows cards-c035, cards-c084, cards-c155, cards-c165, cards-c114, cards-c124, then re-run this group.")
row("cards-c025", "2.7-card-lab-split", "course/modules/CS/CS2/cards.json CS2-c025 (T), CS2-c155 (C)", P,
    "CS2-c025 (T): 1 + (n-1)/(2m) at m = 64 gives 1.9921875 at n = 128 and 2.9921875 at n = 256, an increase of exactly 1 (recomputed); the card states the formula 1 + (n-1)/(2m) (the average of Proposition 2.2(c)); the increase is exact")
row("cards-c035", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c035 (C, L03); lesson L03 Lab 3 output", F,
    "the card says 'In the printed rows from N = 64 to N = 4096 ... between 3.5282 and 4.5050' and 'between 1.9858 and 2.3778'. The ratio 3.5282 (sorted list) and 2.3778 (heap) are printed on the N = 64 row, which compares N = 64 with N = 32. Read as doublings from N = 64 to N = 4096 (the ratios printed at N = 128 to 4096), the ranges are 3.7118 to 4.5050 and 1.9858 to 2.2331 (recomputed from the L03 run: out/lab-CS2-L03-1.txt)",
    "State the basis: either 'the printed ratios on the rows N = 64 to N = 4096 (each compares that row with the row above)', giving 3.5282 to 4.5050 and 1.9858 to 2.3778, or use the doublings 64 to 4096 and give 3.7118 to 4.5050 and 1.9858 to 2.2331.")
row("cards-c123", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c123 (C, L09)", P,
    "two-pass errors 2.819e-17, 4.357e-17, 1.269e-14 at offsets 0, 1e6, 1e9 match the L09 run (lab-CS2-L09-1, offsets 0.0, 1e6, 1e9); 7.286e-15/9.258e-16 = 7.87 (recomputed); Welford error rises with offset and stays below naive at each offset")
row("cards-c126", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c126 (C, L09)", P,
    "Welford 9.258e-16 (offset 0) and 7.449e-08 (1e9); ratios 1.418e-2/8.852e-11 = 1.60e8 and 1.000/7.449e-8 = 1.34e7 (recomputed) match the card; 'Theorem 2.2 assumes exact arithmetic' matches L09 hypothesis (3)")
row("cards-c124", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c124 (C, L09)", F,
    "the card says 'a stream whose true sample variance is 0.0872811' with basis 'Lab 1 ... offset 1e9 lines'. The lab prints 'exact sample variance 0.087281' (six decimals, L09 run line 'offset 1000000000.0: exact sample variance 0.087281'). 0.0872811 is the unrounded value 0.08728110122738864 rounded to seven decimals, which the lab does not print",
    "Quote the printed value 0.087281 with the lab as basis, or give 0.08728110 with the calculation 'unrounded value, not printed by the lab'.")
row("cards-c136-c138-c154", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c136, c138, c154 (C, L10)", P,
    "run output: operations min/max per window 399/399, 398/399, 398/398, 397/398, 396/397 (windows 1,2,5,13,30): range 396 to 399 under bound 400; deque sizes 1,2,5,8,10; single-push removals 1,2,5,6,6 (matches c154's 5 for window 5)")
row("cards-lab-number-cards", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c009, c022, c024, c034, c038, c039, c052, c053, c065, c066, c068, c079, c080, c097, c098, c099, c113, c115, c138, c150", P,
    "each number checked against its lesson's embedded lab output: c038 205 vs 602 and 19140 vs 21405 (107+98, 241+361, 8517+10623, 3742+17663); c039 4933/4514 and 10623/17663; c052 21, 14, 13, 21; c053 1023 and 5120; c065 height 64, 7, 8.6747; c066 height 11, 12.9186, 340, 272; c079 619, 1238; c080 1 hop weight 10 vs 2 hops weight 2; c097-c099 47, 28, 183, LCS 3 and 49 interior cells (recomputed); c113 185, 177, 8 levels, 10 orders; c115 185/177/362/4; c150 and c166 match lab output")
row("cards-c075-check-numbers", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c075 (L06)", P,
    "'40 seeded graphs and every source ... 0 mismatches': run output graphs 40, sources_checked 200, bfs_mismatches 0 (L06 run lines 236-238); the lab loops over every source (lab code)")
row("cards-spot-proofs-T", "2.4-T-cards-proof-level", "course/modules/CS/CS2/cards.json (T cards)", P,
    "about 25 T cards re-derived or compared with the proposition's hypotheses: c047 and c055 list the five hypotheses of Proposition 2.1; c094 A >= 1 and A+1 > 2^(b-1); c106 lists Assumptions 1 and 2 of Proposition 2.2; c032 lists the hold-run hypotheses of Proposition 1.5; c144 telescoping sum; c148 R^-(v) <= qn + E <= qn + eps n follows from Theorem 2.4 (R^- weight < qn); c152 counts 500 <= 550 and 1000 >= 450; c089, c095 coin counts (recomputed: f(6) = 2, first greedy failure at 6). Not all 129 T proofs were re-derived")
row("cards-c010-c063-c070-ungraded-ok", "2.7-ungraded-description", "course/modules/CS/CS2/cards.json CS2-c010, c063, c070", P,
    "these three are now grade T with no basis; each back matches its lesson statement (Definition 1.1 misconception 1; Remark 3.2 and Proposition 3.1; Section 1)")
row("cards-c084", "2.7-front-back", "course/modules/CS/CS2/cards.json CS2-c084 (L07)", F,
    "the front asks 'what are the steps of dynamic programming, and what are its two forms?' The back gives the steps (Definition 1.1) and no forms. The two forms (memoized recursion and table fill) are on card CS2-c161 only",
    "Either add the two forms to the back of CS2-c084 (memoized recursion and table fill, as Definition 1.1 gives them) or drop 'and what are its two forms' from the front.")
row("cards-c114", "2.7-agree-with-lesson", "course/modules/CS/CS2/cards.json CS2-c114 (C, L08); L08 Part B text lines 93-96", F,
    "the card says the reference 'sorts its resting orders on every match'. The lesson says the reference 'keeps a flat list of resting orders and sorts the crossing candidates by (price, arrival number) on every match'",
    "Change 'sorts its resting orders' to 'sorts the crossing candidates by (price, arrival number)'.")
row("cards-c155", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c155 (C, L02); L02 line 193", F,
    "the card says 'Multiplying each by n gives the integer totals 257 and 193'. For n = 256 the total is 3.0156 x 256 = 772 (L02 lists 772 and 193/64 = 772/256 = 3.015625). The totals are 257 (n = 128) and 772 (n = 256)",
    "Replace '193' with '772' in the back of CS2-c155.")
row("cards-c165", "2.4-arithmetic-direction", "course/modules/CS/CS2/cards.json CS2-c165 (T, L01)", F,
    "the back says '1000 n > n^2 holds exactly when n < 1000, so the first failure is at n = 1001'. By Proposition 2.3 (L01 line 136) 1000 n > n^2 first fails at n = 1000 (equality). The first integer with n^2 > 1000 n is 1001 (front and lab are right); the sentence attributes the wrong inequality",
    "Change the middle of the back to: 'n^2 <= 1000 n holds exactly when n <= 1000, so the first n with n^2 > 1000 n is 1001'.")
row("cards-c067", "2.7-undefined-term", "course/modules/CS/CS2/cards.json CS2-c067 (L05)", F,
    "the front uses 'left balanced', which L05 never defines (grep 'left balanced' in the lesson: 0 matches). The term L05 defines is 'balance factor' (Definition 2.1)",
    "Change the front to 'Does sorted insertion keep a binary search tree height logarithmic?' or similar, using only the term the lesson defines.")
row("cards-unchanged-90", "2.7-agree-with-current-lesson", "course/modules/CS/CS2/cards.json (90 unchanged cards)", P,
    "the 90 cards whose text is byte-identical since aa3c26c were read against the current lesson text and checked by script (numbers, locators); each agrees with its lesson apart from CS2-c067 (its own row)")
row("cards-c001-c002-c013-c017", "2.7-agree-with-current-lesson", "course/modules/CS/CS2/cards.json (changed cards read, e.g. c001, c002, c013, c014, c015, c017, c026-c028, c040, c041, c048-c050, c055-c059, c070-c073, c083, c085, c086, c094, c100-c104, c116-c122, c128-c131, c135, c139-c153)", P,
    "each read against its lesson definition or proposition: hypotheses and statements match (for example c055 lists the five hypotheses of Proposition 2.1; c017 adds the 64-bucket assumption that Proposition 1.4 needs; c059 and c063 keep the 'recurrence values' and 'checked, not proved' limits of Lemma 2.3 and Remark 3.2)")
row("cards-c084-c161", "2.7-definition-coverage", "course/modules/CS/CS2/cards.json CS2-c161 (L07)", P,
    "CS2-c161 gives the two forms (memoized recursion, table fill) as Definition 1.1 does; the forms are not on c084 (see cards-c084)")

rows_path = Path(__file__).parent / "rows_r4.json"
rows_path.write_text(json.dumps(R, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(R), "rows;", sum(1 for r in R if r["status"] == "FAIL"), "FAIL")
