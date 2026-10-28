"""Verifier CS2-d round 5: writes ledgers/CS2/CS2-d.json (rows, mutants, summary). Evidence paths are in this folder."""
import json
from pathlib import Path

ROOT = Path("/tmp/verifyB5-CS2-d")
S = "ledgers/CS2/scripts/CS2-d-r5/"
CR = "[Carried from round 4 (instance.py, reference.py and starter.py byte-identical since the previous pin 2657ab5): {}]"

def row(id_, check, location, status, evidence):
    return {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}

rows = [
 row("proj-run-graders", "2.6-autograder-1", "course/modules/CS/CS2/grader/reference.py", "PASS",
     "tools/run_graders.py --unit CS2 --seeds 0-49: 'run_graders CS2: PASS (reference 50/50 seeds, slowest 0.2 s)' (" + S + "out/run_graders_r5.txt). Workspace run: reference 153 passed; starter 150 failed, 3 passed (NotImplementedError)."),
 row("proj-collect-count", "2.6-spec-count", "course/modules/CS/CS2/project.html:211 ('collects 153 checks')", "PASS",
     "pytest --collect-only on the reference in a scratch workspace: '153 tests collected' for QF_SEED default and seed 49; the parametrize lists have fixed lengths (grader/test_project.py:300, 441, 548, 582, 659, 709, 726)."),
 row("proj-pytest-pin", "2.6-spec-local", "course/modules/CS/CS2/project.html:257 ('Use Python 3.14 and pytest 9.0.2')", "PASS",
     "Local .venv: pytest 9.0.2, Python 3.14.8. requirements-dev.txt:2 pytest==9.0.2; tools/vendor_spec.yaml:50-59 pyodide 314.0.7 with pytest (same pin); course/assets/vendor/LOCK.json lists pytest-9.0.2 wheel."),
 row("proj-instances-distinct", "2.6-instances", "course/modules/CS/CS2/grader/instance.py:30-47", "PASS",
     CR.format("instance.py:30-47") + " Re-run now: 50 distinct payloads for seeds 0-49; test_instance_is_deterministic passes on every seed in run_graders."),
 row("proj-instance-labelled", "2.8-simulated-label", "course/modules/CS/CS2/grader/instance.py:47", "PASS",
     CR.format("instance.py:47") + " test_instance_is_valid_and_labelled_simulated passes on seeds 0-49 (run_graders)."),
 row("proj-mutants-killed", "2.6-mutation", "ledgers/CS2/mutants/ (70 files); course/modules/CS/CS2/grader/test_project.py", "FAIL",
     "tools/mutate_graders.py --unit CS2 --seeds 0-49: 'mutate_graders CS2: FAIL (68/70 killed)' (" + S + "out/mutate_0-49_r5.txt). SURVIVED d5_07_none_window_means_unbounded.py (RollingMinMax(None) read as unbounded; no None-window test) and d5_08_ddof_none_is_sample.py (variance(None) returns the sample variance; no None-ddof test). The page at project.html:211 says None must raise for ddof and lists None among the window types the suite checks."),
 row("proj-mutant-d4_03-not-a-fault", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_h_running_sum_mean.py (the round-4 candidate d4_03; not in mutants/ at this pin)", "PASS",
     "alt_h passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt). A running-sum mean is a correct implementation, so it is not a mutant."),
 row("proj-r4-mutants-killed", "2.6-mutation", "ledgers/CS2/mutants/r4_01..r4_05", "PASS",
     "All five killed in the 70-mutant run (" + S + "out/mutate_0-49_r5.txt)."),
 row("proj-alt-implementations-A-D", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r1/alts/alt_a..alt_d", "PASS",
     "Each passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt)."),
 row("proj-alt-F-floor-plus-one", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r3/alts/alt_f_floor_plus_one_rank.py", "PASS", "Passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt)."),
 row("proj-alt-G-count-threshold", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_g_count_threshold_no_ceiling.py", "PASS", "Passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt)."),
 row("proj-alt-I-ceil-minus-floor", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_i_ceil_minus_floor_cutoff.py", "PASS", "Passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt)."),
 row("proj-alt-K-chan-merge-welford", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_k_chan_merge_welford.py", "PASS", "Passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt)."),
 row("proj-alt-L-coerce-inputs", "2.6-over-constraint", "ledgers/CS2/scripts/CS2-d-r4/alts/alt_l_coerce_inputs_to_numbers.py", "PASS", "Passes 50/50 seeds (" + S + "out/alts_seeds_0-49_r5.txt)."),
 row("proj-alt-e-float-cutoff-is-a-fault", "2.6-spec-claim", "ledgers/CS2/scripts/CS2-d-r1/alts/alt_e_float_cutoff_sketch.py; course/modules/CS/CS2/project.html:219", "PASS",
     "alt_e fails 50/50, on test_sketch_rank_target_is_exact_where_a_float_target_is_one_short. project.html:219 states that a float rank target can fall one rank short and must be computed exactly, so the failure is a fault the page states."),
 row("proj-nearest-rank-not-a-fault", "2.6-equivalence", "ledgers/CS2/scripts/CS2-d-r1/alts/alt_c_shifted_sums_sorted_window.py; ledgers/CS2/scripts/CS2-d-r5/alts/alt_r5_nearest_rank_no_slack.py", "PASS",
     "Exact storage with nearest rank (alt_c) passes 50/50. The same nearest-rank target on the compressed sketch (alt_r5_nearest_rank_no_slack) fails 50/50 and violates the page guarantee: sorted stream n=40, epsilon 0.2, q=0.03 gives below=10 > qn+epsilon n=9.2 (" + S + "guarantee_search_r5.out.txt). So the suite is right to fail it; the no-slack target is correct only with exact storage."),
 row("proj-exact-rank-witness", "2.6-spec-claim", "course/modules/CS/CS2/project.html:219; grader/test_project.py:740-755", "PASS",
     "Recomputed: Fraction(0.1)*20 - Fraction(0.05)*20 = 18014398509481985/18014398509481984 (above 1), ceil = 2; the float expression 0.1*20 - 0.05*20 = 1.0, ceil 1."),
 row("proj-run-labs", "2.5-labs", "course/modules/CS/CS2/project.html lab-CS2-project-1..3; tests/labs/CS2/lab-CS2-project-*.py", "PASS",
     "tools/run_labs.py --unit CS2 --page project: 3/3 PASS. Twins run with python -I -W error exit 0 and their output equals the expected blocks (" + S + "out/lab-CS2-project-{1,2,3}_r5.txt)."),
 row("proj-page-smoke", "2.5-pyodide", "course/modules/CS/CS2/project.html", "PASS",
     "tools/page_smoke.py --unit CS2 --pages project: PASS; in-browser grader 'All 153 tests pass on seed 1899060177'; labs 0.0 s each."),
 row("proj-lab1-numbers", "2.2-numbers-lab", "course/modules/CS/CS2/project.html:130-144", "PASS",
     "Twin output equals the expected block; series [60, 34, ...] reproduced from random.Random(12); 44 deque operations, bound 4n = 48 (each value appended once per deque, popped at most once): recomputed."),
 row("proj-lab2-numbers", "2.2-numbers-lab", "course/modules/CS/CS2/project.html:185-187", "PASS",
     "Mean of offsets 2,5,1,4,9,3,6,0 = 3.75 -> 1000003.750000; sum of squared deviations 59.5, /7 = 8.5 (recomputed by hand, see twin output)."),
 row("proj-lab3-numbers", "2.2-numbers-lab", "course/modules/CS/CS2/project.html:329-341", "PASS",
     "Independent Fraction recomputation: sum 110046.0, exact mean 10004.181818, exact sample variance 8.313636, rank target k = max(1, ceil(5.5 - 1.1)) = 5, 5th smallest 10003.2, last four min 10001.0 max 10006.3 (python, this round)."),
 row("proj-hours-arithmetic", "2.2-hours", "course/modules/CS/CS2/project.html:233-241; index.html data-hours-lessons=100; L01-L11 data-hours", "PASS",
     "L01-L11 data-hours 8+9+10+10+9+9+10+10+10+8+7 = 100 = hub; project rationale rows 2+3+4+4+4+6+4+3 = 30 = data-hours-project; 30/130 = 23.1%. Hours not judged on pace (architect ruling)."),
 row("proj-ladder", "2.9-structure", "course/modules/CS/CS2/project.html:40-49, 51-190, 400-406", "PASS",
     "Rung 1 text (line 44) matches Lab 1: the twin carries a 'Why:' note on each deque rule (twin lines 80, 82, 88, 94, 100). Rungs 2-4 match Labs 2-3 and the sections."),
 row("proj-interface-signatures", "2.6-spec-interface", "course/modules/CS/CS2/project.html:202; grader/starter.py:10-52", "PASS",
     "starter.py defines WelfordAccumulator (update(x: float)->None, count property, mean, variance(ddof: int = 1)), RollingMinMax(window: int) with push, minimum, maximum, and QuantileSketch(epsilon: float) with add and quantile(q: float)."),
 row("proj-named-conditions-tested", "2.6-named-conditions", "course/modules/CS/CS2/project.html:209 (Constraints, conditions 1-10); grader/test_project.py", "PASS",
     "Each of the ten named conditions has a test that requires ValueError: must_raise at lines 170-179, 182, 203-210, 383-392, 403-418, 548-555, 567-585, 602-608, 647-653, 764-772."),
 row("proj-unnamed-conditions-any-exception", "2.6-unnamed", "course/modules/CS/CS2/grader/test_project.py:350-361 (test_welford_other_ddof_is_refused, ddof \"1\")", "FAIL",
     "The test requires a refusal for variance(ddof=\"1\"). project.html:211 says a string ddof is 'refused, or answered as the number it denotes', and \"1\" denotes 1. Alternative alt_r5_ddof_string_denotes_number (ddof = int(ddof) for a string) is correct under the page and fails 50/50 with test_welford_other_ddof_is_refused[1] (" + S + "out/alts_seeds_0-49_r5.txt). The builder mutant n02_variance_coerces_ddof_with_int is therefore a page-permitted behaviour counted as a fault."),
 row("proj-failure-messages", "2.6-feedback", "course/modules/CS/CS2/grader/test_project.py (every pytest.fail message)", "PASS",
     "Messages name the property and print inputs or counts, never the expected answer (read every fail message, test_project.py lines 59-772)."),
 row("proj-stdlib-only", "2.6-stdlib", "course/modules/CS/CS2/grader/test_project.py:129-140; grader/reference.py:8-13", "PASS",
     "reference.py imports math, bisect, collections, fractions only; test_standard_library_only passes on the reference."),
 row("proj-rubric-calibration", "2.3-rubric-structure", "course/modules/CS/CS2/project.html:365-373 (Exemplar A)", "PASS",
     "data-scores 1,1,2,1,1,1 equals the verdict text (C1 1, C2 1, C3 2, C4 1, C5 1, C6 1). Each annotation level matches the descriptor it cites: C1 and C2 (no hypotheses, base case and inductive step not shown), C3 (M not tied to the sum of squares), C4 (no arithmetic named), C5 (no guarantee stated), C6 (speed claim with no printed count). The round-4 mismatch is gone."),
 row("proj-rubric-exemplar-b-c1", "2.3-exemplar-claim", "course/modules/CS/CS2/project.html:379-384 (Exemplar B proof and C1 annotation)", "PASS",
     "Hypotheses H1-H3 listed before the statement and cited at their steps. Algebra re-derived: a = -delta/(n+1); sum (x_i - m_{n+1})^2 = M_n + n a^2; new deviation n delta/(n+1); total increment n delta^2/(n+1) = delta (x_{n+1} - m_{n+1}). Correct."),
 row("proj-rubric-numbers-locators", "2.2-numbers-in-exemplars", "course/modules/CS/CS2/project.html:369-390; grader/instance.py:8-13", "PASS",
     "Recomputed the instance.py docstring counts (" + S + "naive_offset_r5.out.txt): offset 0: 0 of 16 naive failures; offset 10,000: 22 of 23 (seed 41 passes); offset 1,000,000: 11 of 11. Matches the docstring."),
 row("proj-exemplar-number-provenance", "2.2-numbers-provenance", "course/modules/CS/CS2/project.html:363 (rule) vs 378-391 (Exemplar B)", "PASS",
     "The rule at line 363 now also admits fixed constants of the spec and suite. Exemplar B's probes (0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1 and one seeded value) equal instance.py:27 and 41; epsilons 0.05, 0.1, 0.2 equal instance.py:28; stream lengths 1-8 equal test_project.py:709. Other numbers are printed by Labs 1-3 (44, 48, 8.313636, 10003.2) or computed with the calculation shown."),
 row("proj-banned-phrases", "2.9-banned", "course/modules/CS/CS2/project.html (visible prose)", "PASS",
     "grep: 0 hits for ellipsis, roughly, historically, typically, 'about 6', 'it is important', clearly, obviously, 'well known', 'left as an exercise', 'beyond the scope', 'for brevity', TODO, TBD, lorem. The only 'rough' is inside 'through'."),
 row("proj-dag-concepts", "DAG-concepts", "course/modules/CS/CS2/project.html (concept links welford-algorithm, monotonic-deque, quantile-sketch, mathematical-induction)", "PASS",
     "welford-algorithm, monotonic-deque and quantile-sketch are defined in CS2 L09-L11 (own unit). mathematical-induction is defined in M1 (curriculum/01-foundations.yaml:110) and M1 is a direct prerequisite of CS2 (yaml:420, prereqs [CS1, M1]), so it is inside the closure."),
 row("proj-citation-cormen", "2.1-citations", "course/modules/CS/CS2/project.html:409-413; references/references.json:5962", "PASS",
     "Registry key cormen2022introduction, status verified, pages null: no locator exists, and project.html:413 says no step is attributed to it. Page states this correctly."),
 row("proj-lint-typecheck", "2.9-gate", "course/modules/CS/CS2/grader; tests/labs/CS2", "PASS",
     "ruff check (grader, tests/labs/CS2): All checks passed. ruff format --check: 18 files already formatted. mypy --no-incremental (same paths): no issues in 18 source files."),
 row("proj-claim-tolerance-prose", "2.6-spec-claim", "course/modules/CS/CS2/project.html:219 ('Exact counts')", "PASS",
     "Relative 1e-9 and absolute 1e-9 match close() in test_project.py:84-85; rank inequalities are exact (Fraction) with no tolerance (test_project.py:611-617); the q=0.1, n=20, epsilon 0.05 example recomputed above."),
 row("proj-named-conditions-valid-input-claim", "2.6-spec-claim", "course/modules/CS/CS2/project.html:224 ('Named errors, in brief')", "PASS",
     "Valid boundary cases exist and pass: window 1 (test_rolling_window_one_is_valid), epsilon 1e-6 (test_sketch_small_epsilon_is_valid), q 0 and 1 (test_sketch_quantile_at_both_ends_is_valid), ddof 0 on one value (test_welford_population_variance_of_one_value_is_zero)."),
 row("proj-curriculum-scope-rolling", "2.6-scope", "course/modules/CS/CS2/project.html:196, 216-217; curriculum/01-foundations.yaml:445 (project brief)", "FAIL",
     "The curriculum brief (yaml:445) says 'O(1)-update rolling mean, variance (Welford)'. project.html:216 says the Welford statistics are cumulative and the window belongs only to minimum and maximum. The two disagree on scope. Fix: change the brief wording (architect, then regenerate) or the page wording."),
 row("proj-lab3-interpretation", "2.5-lab-interpretation", "course/modules/CS/CS2/project.html:338 vs tests/labs/CS2/lab-CS2-project-3.py", "PASS",
     "Recomputed: q n - epsilon n = 4.4, target 5, 5th smallest 10003.2. The 'Welford sample variance 8.313636' and exact agreement match the twin output."),
 row("proj-lab2-every-pair", "2.5-lab-claims", "course/modules/CS/CS2/project.html:150, 188", "PASS",
     "Lab 2 twin has no blanks and its output equals the expected block exactly; interpretation (mean 1000003.75, variance 8.5, no exact arithmetic in Lab 2, exact check in Lab 3) matches the code."),
 row("proj-rubric-c5-partly", "2.3-rubric-levels", "course/modules/CS/CS2/project.html:356 (C5 descriptors)", "PASS",
     "Four levels present; level 4 names the guarantee with both inequalities, ten probes and the limits; level 3 and 2 match the stated cases."),
 row("proj-instance-docstring-claims", "2.6-docstring-claim", "course/modules/CS/CS2/grader/instance.py:8-16", "PASS",
     "Offset counts recomputed (see proj-rubric-numbers-locators). 'The reference's Welford update passes all 50 seeds' matches run_graders 50/50. 'Some streams are rounded to one decimal' matches decimals in {1, 6}."),
 row("proj-exemplar-b-constant-stream-claim", "2.6-claim-vs-test", "course/modules/CS/CS2/project.html (Exemplar B design note); grader/test_project.py test_sketch_constant_stream_returns_the_constant", "PASS",
     "The note's claim 'a constant stream is checked to return its value' matches test_sketch_constant_stream_returns_the_constant (40 copies, every probe)."),
 row("proj-rank-guarantee-claims-rechecked", "2.6-rank-claims", "course/modules/CS/CS2/grader/test_project.py (rank tests); ledgers/CS2/scripts/CS2-d-r5/guarantee_search_r5.py", "PASS",
     "Independent search: 4,000 random streams (n 1-60; uniform, ties, sorted, offset), epsilon 0.05/0.1/0.2/0.01/0.37, 416,000 queries against the reference: no violation of the two inequalities."),
 row("proj-test-docstring-short-stream", "2.6-docstring-claim", "course/modules/CS/CS2/grader/test_project.py:711-713", "PASS",
     "0.05*8 = 0.4, 0.1*8 = 0.8, 0.2*4 = 0.8 are below one; 0.2*5 = 1.0 is not, as the docstring says."),
 row("proj-check-pages-unit", "2.9-structure-gate", "course/modules/CS/CS2/project.html (tools/check_pages.py --unit CS2)", "PASS", "check_pages CS2: PASS."),
 row("cards-structure", "2.7-structure", "course/modules/CS/CS2/cards.json", "PASS", "167 cards; field sets: 129 with (back, front, grade, id, lesson), 38 with basis added; ids CS2-c001..c167."),
 row("cards-grade-field", "2.7-plan-fields", "course/modules/CS/CS2/cards.json", "PASS", "129 T (no basis), 38 C (each with a basis naming a Lab)."),
 row("cards-count-vs-plan", "2.7-plan-count", "course/modules/CS/CS2/cards.json; plans/CS2-build-plan.md:352 ('Expected total 50-80 cards')", "FAIL",
     "167 cards against the plan's expected 50-80. The plan is not amended by the Architect decisions. Fix: amend the plan's expectation (architect) or cut the deck."),
 row("cards-c075-lab-result-ungraded", "2.7-grade-rule", "course/modules/CS/CS2/cards.json CS2-c075 (L06)", "PASS", "Grade C with basis 'Lab 1, Part A (SIMULATED seeded graphs, one run)'. Lab numbers: 40 graphs, 0 mismatches (L06 lab output)."),
 row("cards-c151", "2.4-arithmetic", "course/modules/CS/CS2/cards.json CS2-c151 (grade T, lesson L11)", "PASS",
     "(L+1)(L+2)(L+3)/(3 eps) + (L+1) with L=29, eps=1/20: 198400 + 30 = 198430; L=12: 2730/0.15 + 13 = 18213, which is the closed form quoted in L11 line 65. Exact sum 18187 is also in the lesson (line 340). The card's 'it' refers to the closed form."),
 row("cards-numbers-in-lesson", "2.7-numbers-in-lesson", "course/modules/CS/CS2/cards.json (all 167 backs vs their lesson text)", "PASS",
     "Re-run this round (" + S + "cards_checks_r5.out.txt): no number in any back is absent from its lesson text. This is a presence check only; the content checks are the card rows."),
 row("cards-duplicates", "2.7-duplicate-scan", "course/modules/CS/CS2/cards.json", "PASS", "No duplicate fronts or backs (cards_checks_r5.out.txt)."),
 row("cards-theorem-section-refs", "2.7-refs", "course/modules/CS/CS2/cards.json", "PASS", "Every Definition/Proposition/Lemma/Theorem/Corollary/Remark/Example/Problem locator in a back appears in its own lesson (cards_checks_r5.out.txt: none missing)."),
 row("cards-basis-labels", "2.7-basis", "course/modules/CS/CS2/cards.json (grade C cards)", "PASS", "Every C card names a Lab in its basis (cards_checks_r5.out.txt)."),
 row("cards-changed-group", "2.7-changed-cards", "course/modules/CS/CS2/cards.json: cards that changed or were added since the round-3 pin", "FAIL",
     "cards.json is byte-identical to the round-4 pin, but the round-4 changed group still contains five cards that fail on re-check: CS2-c084, c114, c124, c155, c165 (rows below). Fix those five."),
 row("cards-c025", "2.7-card-lab-split", "course/modules/CS/CS2/cards.json CS2-c025 (T), CS2-c155 (C)", "PASS", "c025: 128/128 = 1 increase from n = 128 to 256 at m = 64, matching Proposition 2.2 (lesson L02 line 336). c155 is a separate row and fails."),
 row("cards-c035", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c035 (C, L03); L03 Lab 3 printed rows (lines 296-317)", "PASS",
     "Recomputed from the printed moves: sorted-list ratios 1002/284 = 3.5282 (N=64), 4514/1002 = 4.5050 (N=128), 17663/4514 = 3.9129, 65561/17663 = 3.7118, 269578/65561 = 4.1119, 1086043/269578 = 4.0287, 4378444/1086043 = 4.0316; heap ratios 2209/929 = 2.3778, 4933/2209 = 2.2331, 10623/4933 = 2.1535, 21095/10623 = 1.9858, 42401/21095 = 2.0100, 87863/42401 = 2.0722, 181761/87863 = 2.0687. Card ranges are the min and max of these seven doublings (N=64 to 4096). Round-4 FAIL no longer holds."),
 row("cards-c123", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c123 (C, L09)", "PASS", "Two-pass 2.819e-17, 4.357e-17, 1.269e-14 are the least errors at 0, 1e6, 1e9 (L09 lines 248-258); 7.286e-15/9.258e-16 = 7.87."),
 row("cards-c126", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c126 (C, L09)", "PASS", "9.258e-16, 7.449e-08; 1.418e-02/8.852e-11 = 1.60e8; 1.000/7.449e-08 = 1.34e7; 7.87 (recomputed)."),
 row("cards-c124", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c124 (C, L09)", "FAIL",
     "Front asks what Welford's estimate returns at offset 1e9. The back gives only Welford's relative error (7.449e-08). The lab line (L09 line 257) prints the estimate 8.728109e-02, which the back omits. Fix: add the estimate to the back."),
 row("cards-c136-c138-c154", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c136, c138, c154 (C, L10)", "PASS",
     "L10 Lab 1 output: operations min/max across windows 396 (w=30) to 399 (w=1,2); largest deque size 10 at w=30; largest single-push removals 5 at w=5 (window 5 line 254)."),
 row("cards-lab-number-cards", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c009, c022, c024, c034, c038, c039, c052, c053, c065, c066, c068, c079, c080, c097, c098, c099, c113, c115, c138, c150", "PASS",
     "Each number checked against its lab output in the lesson: c022 and c157 (L02 lines 278-286), c024, c038 (205 vs 602 at N=16; 19140 vs 21405 at N=256), c039, c052/c053 (L04 lines 395-430), c065/c066 (L05), c079/c080 (L06 lines 397-406), c097-c099 (L07 lines 588-597), c113/c115 (L08 lines 614-616), c150 (L11 line 310)."),
 row("cards-c075-check-numbers", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c075 (L06)", "PASS", "L06: 40 graphs in Part A, mismatches none (L06 line 408)."),
 row("cards-spot-proofs-T", "2.4-T-cards-proof-level", "course/modules/CS/CS2/cards.json (T cards)", "PASS",
     "All 167 backs were read (truncated print, 260-330 characters). Full re-derivation of the arithmetic or the logic for 15 T cards: c003, c004, c005, c011, c012, c017, c048, c094, c095, c142, c144, c149, c151, c152, c165. The other T proofs were not re-derived; see notes."),
 row("cards-c010-c063-c070-ungraded-ok", "2.7-ungraded-description", "course/modules/CS/CS2/cards.json CS2-c010, c063, c070", "PASS", "Grade T cards whose backs state a definition or a limit; each is consistent with its lesson text."),
 row("cards-c084", "2.7-front-back", "course/modules/CS/CS2/cards.json CS2-c084 (L07)", "FAIL",
     "Front asks 'what are its two forms?'. The back names neither form. L07 Definition 1.1 (line 77) names memoized recursion and table fill. Fix: name both forms in the back (CS2-c161 already does)."),
 row("cards-c114", "2.7-agree-with-lesson", "course/modules/CS/CS2/cards.json CS2-c114 (C, L08); L08 lab hypothesis (line 176) and twin lines 13-16, 389", "FAIL",
     "Back says the reference 'sorts its resting orders on every match'. The lesson and the twin say it sorts the crossing candidates on every match (Reference.submit, twin line 389-398). Fix the back."),
 row("cards-c155", "2.7-card-numbers", "course/modules/CS/CS2/cards.json CS2-c155 (C, L02); L02 lines 336, 431", "FAIL",
     "Back says the integer totals are 257 and 193. The totals are 257 (at n = 128) and 772 (at n = 256); 772/256 = 193/64 = 3.015625, and 193/64 is the reduced quotient, not a total (L02 line 336 names 772). Fix the back."),
 row("cards-c165", "2.4-arithmetic-direction", "course/modules/CS/CS2/cards.json CS2-c165 (T, L01)", "FAIL",
     "Back: 'so the first failure is at n = 1001'. 1000n > n^2 holds exactly for 1 <= n <= 999 (L01 lines 302, 465), so it first fails at n = 1000 (1000*1000 = 10^6, not greater). n = 1001 is the first n with n^2 > 1000n. Fix the sentence."),
 row("cards-c067", "2.7-undefined-term", "course/modules/CS/CS2/cards.json CS2-c067 (L05); L05 lines 45, 65, 75-77", "PASS",
     "'balanced' is introduced in L05 (line 45 'Introduces: balanced search tree', line 65 'A balanced search tree avoids this by restructuring itself') before the card's answer; the answer uses Remark 1.1 (sorted insertion makes a path, proof on line 77). Round-4 FAIL resolved; the formal AVL definition is Definition 2.1 (line 85), used only as a refinement."),
 row("cards-unchanged-90", "2.7-agree-with-current-lesson", "course/modules/CS/CS2/cards.json (all 167 cards; byte-identical to the round-4 pin)", "PASS",
     "Lesson text of L01-L11 changed since the pin, so the cards were re-checked: card_number_delta_r5.py flags no card with a number new in its lesson (" + S + "card_number_delta_r5.out.txt), and the cards on the changed hunks were read (c009, c022, c024, c034-c039, c052, c053, c065-c068, c079, c080, c097-c099, c113-c115, c123-c126, c136-c138, c150, c151, c154-c166)."),
 row("cards-c001-c002-c013-c017", "2.7-agree-with-current-lesson", "course/modules/CS/CS2/cards.json CS2-c001, c002, c013, c017", "PASS",
     "c001 witness c and threshold n0 (Definition 1.1); c002 scan (Definition 1.5); c013 chained table (Definition 1.1); c017 h(64j) = 0 since 2^32 is a multiple of 64 (Proposition 1.4)."),
 row("cards-c084-c161", "2.7-definition-coverage", "course/modules/CS/CS2/cards.json CS2-c161 (L07)", "PASS", "c161 names memoized recursion and table fill (Definition 1.1), matching L07 line 77."),
 row("proj-d5-new-mutants-killed", "2.6-mutation", "ledgers/CS2/mutants/d5_01, d5_02, d5_05", "PASS",
     "Three new student-error mutants, each killed: d5_01_quantile_uses_numpy_style_index (test_sketch_rank_guarantee_at_each_probe[3], seed 0); d5_02_quantile_refuses_zero (test_sketch_quantile_at_both_ends_is_valid, seed 0); d5_05_minimum_reads_deque_back (test_rolling_ties_expire_with_their_index[2], seed 0)."),
 row("proj-not-fault-survivors", "2.6-equivalence", "ledgers/CS2/scripts/CS2-d-r5/not_faults/ (d5_03, d5_04, d5_06)", "PASS",
     "Three candidate mutants survive and are not faults under the page: d5_04 (smaller compression cap) and d5_06 (delta without minus one) keep the rank guarantee on 416,000 random queries (no violation), so they are correct, larger-memory sketches; d5_03 (count incremented before a refused NaN) is not stated in the page, which says nothing about count after a refused call. Recorded as observation only, out of mutants/."),
]

mutants = [
 {"id": "d5_01_quantile_uses_numpy_style_index.py", "description": "Quantile reads the sorted values at index floor(q (n - 1)), the numpy-style index, instead of the rank target.", "killed_by": "test_sketch_rank_guarantee_at_each_probe[3] (seed 0)"},
 {"id": "d5_02_quantile_refuses_zero.py", "description": "Quantile raises for q = 0 (half-open interval at zero), though the page names [0, 1] as closed.", "killed_by": "test_sketch_quantile_at_both_ends_is_valid (seed 0)"},
 {"id": "d5_05_minimum_reads_deque_back.py", "description": "minimum() reads the newest entry of the minimum deque instead of its front.", "killed_by": "test_rolling_ties_expire_with_their_index[2] (seed 0)"},
 {"id": "d5_07_none_window_means_unbounded.py", "description": "RollingMinMax(None) treats None as an unbounded window.", "killed_by": "", "survived": "seeds 0-49: no test fails (see proj-mutants-killed)"},
 {"id": "d5_08_ddof_none_is_sample.py", "description": "variance(None) is read as ddof 1 and returns the sample variance instead of raising.", "killed_by": "", "survived": "seeds 0-49: no test fails (see proj-mutants-killed)"},
]
# existing mutants: killed as recorded in the 70-mutant run (ledgers/CS2/scripts/CS2-d-r5/out/mutate_0-49_r5.txt)
import re
for line in (ROOT / S / "out/mutate_0-49_r5.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line)
    if m and not m.group(1).startswith("d5_"):
        mutants.append({"id": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

fragment = {
    "unit": "CS2",
    "slice": "CS2-d",
    "round": 5,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 5; did not build CS2; no shared context with builders)",
    "pin": "09b8751 (detached checkout /tmp/verifyB5-CS2-d)",
    "base": "2657ab5 (round-4 pin). Delta since 2657ab5 in the slice: project.html (ladder text, Lab 2 hypothesis, Constraints, grading-mode count 153, exemplar A levels 1, exemplar rule), grader/test_project.py (ddof, None, boolean and string tests), lesson text L01-L11 (prose and lab-output hunks), tests/labs/CS2 L06 and L08 twins, ledgers/CS2/mutants (new n01-n10, r4 mutants, d5 mutants). cards.json, instance.py, reference.py and starter.py are byte-identical to 2657ab5.",
    "checkout": "/tmp/verifyB5-CS2-d",
    "scratch": "/tmp/CS2-v/d5/",
    "verified_at": "2026-10-28",
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Ran this round: tools/run_graders.py --unit CS2 --seeds 0-49 (PASS 50/50); tools/mutate_graders.py --unit CS2 --seeds 0-49 (68 of 70 killed; survivors d5_07 and d5_08); all alternatives (alt_a..alt_l, alt_r5 x2, the three not-fault candidates) over seeds 0-49; tools/run_labs.py --unit CS2 --page project (3/3); python -I -W error on the three project twins; tools/page_smoke.py --unit CS2 --pages project (PASS, in-browser 153 passed); check_pages, check_dag, check_projects, verify_refs --unit CS2 (live: 1 entry, 0 problems); ruff check, ruff format --check, mypy --no-incremental on grader and tests/labs/CS2 (clean); collect-only 153 on seeds 0 and 49; starter run (150 failed, 3 passed). Independent scripts: ledgers/CS2/scripts/CS2-d-r5/ (naive_offset_r5.py, guarantee_search_r5.py, lesson_text_r5.py, cards_checks_r5.out.txt, card_number_delta_r5.py, alts/, not_faults/, out/). "
        "NOT CHECKED: (1) all 167 card backs were read, but only 15 T proofs were re-derived; the other T proofs were not re-derived line by line; (2) card checks on the lesson text are presence checks for numbers plus hand reads of the changed hunks, not a full read of L01-L11 (other slices); (3) the rubric is scored from its descriptors only, with no second scorer; (4) no external source was read; the only citation is the textbook registry key, which has no locator; (5) the exact-zero tests (constant 5.0 variance, single value variance 0.0) were not broken by any alternative; no correct alternative with a nonzero result on a constant stream was found, recorded as an observation; (6) the 16 instance seeds at offset 0 and the Pyodide timing were run once."
    ),
    "rows": rows,
    "mutants": mutants,
}

FIXES = {
 "proj-mutants-killed": "Add a None-window test and a None-ddof test (or drop None from the grading-mode list at project.html:211), then re-run tools/mutate_graders.py: d5_07 and d5_08 must be killed.",
 "proj-unnamed-conditions-any-exception": "In test_welford_other_ddof_is_refused drop the ddof \"1\" case (or accept an answer equal to the sample variance for it); keep ddof 2, -1, 3 and 2.0 refused. Re-run: alt_r5_ddof_string_denotes_number must pass.",
 "proj-curriculum-scope-rolling": "Make curriculum/01-foundations.yaml:445 say cumulative Welford mean and variance (not rolling), or make project.html:216 match the brief; regenerate curriculum.json.",
 "cards-count-vs-plan": "Architect: amend plan section 9 expected total, or reduce cards.json to the planned 50-80.",
 "cards-changed-group": "Fix the five cards listed in the cards-c084, cards-c114, cards-c124, cards-c155 and cards-c165 rows.",
 "cards-c124": "Add the Welford estimate 8.728109e-02 (L09 line 257) to the back.",
 "cards-c084": "Name both forms in the back: memoized recursion and table fill, as CS2-c161 does.",
 "cards-c114": "Replace 'sorts its resting orders on every match' with 'sorts the crossing candidates by (price, arrival number) on every match'.",
 "cards-c155": "Replace the totals 257 and 193 with 257 and 772; 772/256 = 193/64 = 3.015625.",
 "cards-c165": "Replace 'the first failure is at n = 1001' with: 1000 n > n^2 first fails at n = 1000, and n^2 > 1000 n first holds at n = 1001.",
}
for r in rows:
    if r["status"] != "PASS":
        r["fix"] = FIXES[r["id"]]

counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": 0, "mutants": len(mutants)}
fragment["summary"] = counts
fragment["verdict"] = "PASS" if counts["fail"] == 0 and counts["unverifiable"] == 0 else "FAIL"
out = ROOT / "ledgers/CS2/CS2-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(counts, fragment["verdict"])
