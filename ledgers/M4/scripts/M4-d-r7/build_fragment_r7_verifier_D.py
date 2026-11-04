"""Round-7 verifier (slice d): builds ledgers/M4/M4-d.json from the rows verified this round."""
import json, pathlib, re, sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-M4-d")
MUT_OUT = ROOT / "ledgers/M4/scripts/M4-d-r7/mutate_M4_0-9.out"
C6 = "Carried from round 6 (byte-identical since the previous pin 142ecfc2, verified again at this pin):"
R = []

def row(i, check, loc, status, ev):
    R.append({"id": i, "check": check, "location": loc, "status": status, "evidence": ev})

# ---- rows carried from round 6 (cited subject byte-identical since 142ecfc2) ----
row("d1-2.6-hours", "2.6 hours: component sum and own estimate within 30 %",
    "course/modules/M/M4/project.html:33 (data-hours-project=30), :234-245 (table#hours)", "PASS",
    C6 + " project.html hunks of 142ecfc2..9373ef39 touch lines 203-220 only; components 2+2+12+8+4+2 = 30 = data-hours-project.")
row("d1-2.6-instances", "2.6 instances: valid, and answers change across seeds",
    "course/modules/M/M4/grader/instance.py", "PASS",
    C6 + " grader/instance.py is not in the 142ecfc2..9373ef39 diff; the round-6 sample ledgers/M4/scripts/M4-d-r6/instance_sample_20.py stands for it.")
row("d1-2.6-starter", "2.6 starter signatures",
    "course/modules/M/M4/grader/starter.py:15-34", "PASS",
    C6 + " starter.py is not in the diff; the Rung 3 signature lines of project.html (before :203) are unchanged.")
row("d1-rubric-observable", "rubric observable levels", "course/modules/M/M4/project.html:330-343 (table#rubric)", "PASS",
    C6 + " hunks do not touch :330-343.")
row("d1-rubric-calibration", "rubric calibration exemplars", "course/modules/M/M4/project.html:348-462", "PASS",
    C6 + " hunks do not touch :348-462.")
row("d1-rubric-question-bank", "no question bank", "course/modules/M/M4/project.html; plans/M4-build-plan.md section 5.7", "PASS",
    C6 + " plan diff touches lines 246-257 (section 5.5) only.")
row("d1-atlas", "atlas entry", "curriculum/meta.yaml:194-276", "PASS", C6 + " curriculum/meta.yaml is not in the diff.")
row("d1-studio", "studio entry", "curriculum/01-foundations.yaml:73-76", "PASS", C6 + " curriculum file is not in the diff.")
row("d1-cites", "Reading citations", "course/modules/M/M4/project.html:482-486; references/references.json", "PASS",
    C6 + " hunks do not touch :482-486; references.json not in the diff; verify_refs offline re-run this round (d1-freshness-registry).")
row("d1-cards-c191-grade", "card M4-c191 grade T", "course/modules/M/M4/cards.json (M4-c191)", "PASS",
    C6 + " card M4-c191 is not among the cards changed by the diff (changed ids listed under d1-cards-math).")
row("d1-data", "data references", "course/modules/M/M4/project.html:37, 200, 271-275; grader/instance.py:1-14, 42", "PASS",
    C6 + " hunks do not touch those lines; instance.py unchanged.")
row("d1-tools-structure", "tools structure", "tools/*.py", "PASS", C6 + " no file under tools/ is in the diff.")
row("d6-2.6-equivalence-float-ceil", "float ceiling equivalence", "course/modules/M/M4/grader/reference.py:95-100; project.html:214", "PASS",
    C6 + " reference.py untouched; project.html:214 (Conventions item 4) not in a hunk.")
row("d6-prose-exemplar-words", "exemplar words", "course/modules/M/M4/project.html:348-462, 319-326", "PASS",
    C6 + " hunks do not touch those lines.")
row("d6-cards-sample", "round-6 card sample re-checked",
    "course/modules/M/M4/cards.json: M4-c001, c011, c030, c040, c063, c074, c098, c105, c120, c133, c141, c149, c157, c162", "PASS",
    "Unchanged sampled cards carried from round 6 (byte-identical since 142ecfc2). Two sampled cards changed in the diff and were re-verified this round: M4-c040 (Proposition 2.5 numbering, statement matches L03 Proposition 2.5) and M4-c162 (now n = 10 only; 1.8220 appears in L10 Lab 1 Part C output, expected block of lab-M4-L10-1).")

# ---- rows re-verified this round ----
row("d1-2.6-ladder", "2.6 ladder: rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open",
    "course/modules/M/M4/project.html:40-49, 51-192", "PASS",
    "Rung 2 labs run by tools/run_labs.py --unit M4: 'run_labs M4: PASS (13/13)' (ledgers/M4/scripts/M4-d-r7/gates/run_labs_M4.out). project.html:40-192 not in a diff hunk.")
row("d1-2.6-spec-questions", "2.6 spec: questions a competent student would ask",
    "course/modules/M/M4/project.html:194-229 (Rung 3 spec)", "PASS",
    "Read in full. The changed sentences (:203, :212, :220, :228) are now checkable: the 146-check count, the 300-draw negation test, the chi-square lags 1-3 and the Gaussian order are each matched by test_project.py (see the rows below). No blocking question left; the float-nu question for student_t is still not tested (stated under 'What the suite does not test' only for nu of 3 and 4).")
row("d1-2.6-autograder-reference", "2.6 autograder: run_graders seeds 0-49 on reference.py",
    "course/modules/M/M4/grader/reference.py", "PASS",
    "tools/run_graders.py --unit M4 --seeds 0-49: 'run_graders M4: PASS (reference 50/50 seeds, slowest 1.1 s)' (ledgers/M4/scripts/M4-d-r7/gates/run_graders_M4_0-49.out).")
row("d1-2.6-mut-own", "2.6 mutation: verifier-written student-error mutants, all killed",
    "ledgers/M4/mutants/v1_01..v9_04, r6d_01..03, r7d_01..04", "PASS",
    "tools/mutate_graders.py --unit M4 --seeds 0-9: 'mutate_graders M4: PASS (142/142 killed)', EXIT 0 (ledgers/M4/scripts/M4-d-r7/mutate_M4_0-9.out). Every v*, r6d_* and r7d_* line reads KILLED.")
row("d1-2.6-mut-existing", "2.6 mutation: existing mutants on seeds 0-9", "ledgers/M4/mutants/*.py (142 files)", "PASS",
    "Same run as d1-2.6-mut-own: 142 of 142 KILLED; no SURVIVED line (ledgers/M4/scripts/M4-d-r7/mutate_M4_0-9.out).")
row("d1-2.6-mut-m11", "2.6 mutation: m11 loss sign flipped", "ledgers/M4/mutants/m11_loss_sign_flipped.py", "PASS",
    "KILLED in the run above by test_gaussian_stream_is_frozen_and_the_loss_is_minus_the_weighted_return (seed 0).")
row("d1-2.6-mut-r9_03", "2.6 mutation: r9_03 chi-square reused on alternate draws",
    "ledgers/M4/mutants/r9_03_student_t_chi_square_reused_every_second_draw.py", "PASS",
    "KILLED in the run above by test_student_t_draws_do_not_share_chi_square (seed 0).")
row("d1-2.6-mut-v4_m02", "2.6 mutation: v4_m02 matched factor skipped for small nu",
    "ledgers/M4/mutants/v4_m02_matched_factor_skipped_for_small_nu.py", "PASS",
    "KILLED in the run above by test_student_t_mean_absolute_loss_matches_the_matched_scale (seed 0).")
row("d1-2.6-mut-m17", "2.6 mutation: m17 is an equivalent (conforming) mutant",
    "ledgers/M4/equivalent/m17_student_t_second_seed.py", "PASS",
    "ledgers/M4/scripts/M4-d-r7/checks/m17_run.py: 'm17 pass seeds: 50 of 50; failing: []' with the current grader. Not in mutants/ (equivalent, conforms to project.html Conventions item 5).")
row("d1-2.6-alternatives", "2.6 alternatives: five alternative correct implementations pass",
    "ledgers/M4/scripts/M4-d-r7/alts/alt1_box_muller_student.py, alt2_polar_student.py, alt3_column_cholesky.py, alt4_chi_square_sum_of_normals.py, alt5_heapq_quantile.py; plans/M4-build-plan.md:246-257", "PASS",
    "Round 6 FAILed the round-6 Box-Muller and polar files because they drew the Gaussian family with rng.random(). The plan now scopes items 1, 2 (and 4) to the Student-t family (plans/M4-build-plan.md:249-257). Rebuilt from reference.py by make_alts.py: run_alts.py seeds 0-9 gives 10/10 PASS for each of the five (ledgers/M4/scripts/M4-d-r7/alts/run_alts_0-9.out). The builder's own alt_1..alt_5 (ledgers/M4/scripts/alt_*.py) also give 10/10 PASS each (alts/run_builder_alts_0-9.out).")
row("d1-2.6-messages", "2.6 messages: check() and expect_value_error() wording",
    "course/modules/M/M4/grader/test_project.py (all messages, incl. the two new tests at :559-590)", "PASS",
    "Read the new messages: 'a one-position covariance with a tiny positive variance must be accepted' and 'a 2 x 2 positive definite covariance with tiny entries must be accepted'. They state the requirement; no process words.")
row("d1-2.6-count-and-pyodide", "2.6 test count and Pyodide statement",
    "course/modules/M/M4/grader/test_project.py; project.html:203-206", "PASS",
    "pytest --collect-only: '146 tests collected'. Reference run: '145 passed, 1 skipped' (the skip is the Student-t variance check at nu 3 or 4, test_project.py:158). project.html:206 says 146 checks and 145 passed plus one skipped on such an instance: matches. page_smoke project: 'All 146 tests pass ... in-browser grader' (ledgers/M4/scripts/M4-d-r7/gates/page_smoke_project.out).")
row("d1-2.6-grader-comment-numbers", "2.6 grader comment numbers",
    "course/modules/M/M4/grader/test_project.py:43-45", "FAIL",
    "Comment: 'The reference's largest relative error over seeds 0 to 49 is 0.024. A matched factor applied to one asset only, or one chi-square variable per asset, moves the cross term by about 29 % and 15 % (measured at seeds 0 to 9).' Measured this round (checks/cross_measure.py): reference max relative error over seeds 0-49 = 0.0239 (matches 0.024); one chi-square per asset (ledgers/M4/mutants/r9_02) = 0.141-0.161 on seeds 0-9 (matches 15 %); matched factor on the first asset only (ledgers/M4/mutants/r8_03) = 0.068-0.086 on seeds 0-9. The 29 % figure is not reproduced by either mutant. Fix: state 7 % to 9 % for the one-asset mutant (ledgers/M4/mutants/r8_03), or name the mutant that gives 29 %. The 0.05 tolerance still lies between 0.024 and 0.068. The 347/317-seed sweep claims at :31-48 were not re-run.")
row("d1-prose-numbers", "prose numbers vs measured values",
    "course/modules/M/M4/project.html:203-206, 212, 215, 220, 228", "FAIL",
    "Verified: 146 checks and 145 passed + 1 skipped (collect and run, above); 39 of 50 seeds for 6j/6j+3 and 44 of 50 for even-indexed sharing, 50 of 50 for 2k/2k+1 and 4j/4j+2 (checks/run_seeds.sh, seeds 0-49); 40,000 draws at nu = 3; 100,000 draws, correlation 0.8, tolerance 0.05 (test_project.py:43-48, 166-198). FAIL on project.html:228: 'so a cross-term error of up to about 5 % of the target is not detected'. Measured (checks/cross_sweep.py, seeds 0-49, the cross-term test only): a +5 % error is detected on 19 of 50 seeds and a -5 % error on 31 of 50 seeds; a +3 % error is detected on 0 of 50 seeds. Fix: 'up to about 3 %'.")
row("d1-prose-scope", "scope words backed by a computation",
    "course/modules/M/M4/project.html:206 ('the independence of the Student-t chi-square variables at draws one, two and three apart'), :215 ('checks the independence of the chi-square variables at lags one to three')", "FAIL",
    "The check (test_project.py:205-226) computes one statistic per block: the share of pairs (i, i+d) with both |loss| above the median, which must lie within 5 standard errors of 1/4. That is one necessary consequence of pairwise independence; it is not an independence test, and a dependence that leaves this one joint share at 1/4 passes. The sentences say the suite 'checks the independence'. Fix: 'checks that the share of pairs at lags one to three with both |loss| above the median is 1/4, which pairwise independence requires'. Line :228 ('must each be independent, with a share of 1/4') is already phrased as a share test and passes.")
row("d1-prose-process-words", "no process words in learner text",
    "course/modules/M/M4/project.html; L01-L04.html; cards.json; grader/test_project.py", "PASS",
    "grep for round, verifier, builder, slice, audit in those files: only 'rounded'/'round()' (arithmetic).")
row("d1-prose-banned-phrases", "banned strings", "course/modules/M/M4/project.html; L01-L04.html", "PASS",
    "tools/check_pages.py --unit M4: 'check_pages M4: PASS' (ledgers/M4/scripts/M4-d-r7/gates/check_pages_M4.out).")
row("d1-dag", "DAG: prerequisite closure and dfn assignment", "course/modules/M/M4/*.html", "PASS",
    "tools/check_dag.py --unit M4: 'check_dag M4: PASS'. The use of 'standard normal law' before Lesson 6 is not a link, so check_dag cannot see it; it is graded under d1-cards-forward-reference.")
row("d1-notation", "notation registry symbols", "notation/notation.json; L03.html; L09.html; project.html", "PASS",
    "Registry: gamma_3 and gamma_4 (module M4) are used with their registered meaning in L03 (Definition 2.2, Proposition 2.3). The density is written f in L03 (Assumption 2.7); f is not a registered symbol, and L02 uses f for the density in the same way. No symbol reused with another meaning found.")
row("d1-structure", "project structure and rungs", "course/modules/M/M4/project.html", "PASS",
    "tools/check_projects.py --unit M4: 'check_projects M4: PASS' (ledgers/M4/scripts/M4-d-r7/gates/check_projects_M4.out).")
row("d1-cards-schema", "card schema", "course/modules/M/M4/cards.json", "PASS",
    "229 cards (204 T, 25 C); no duplicate ids or duplicate fronts; every C card has basis; 9 T cards carry a basis naming a lab or closed form (allowed: BUILDER_RULES names basis for non-T cards; a T card may name its source). Checked by checks/cards_check.py.")
row("d1-cards-numbers-in-lesson", "card numbers appear in the card's lesson",
    "course/modules/M/M4/cards.json vs L01-L10.html", "PASS",
    "checks/cards_check.py: every decimal in every card back appears verbatim in its own lesson, including M4-c237 (1.8838, L10), M4-c238 (0.8518, L09), M4-c241 (0.00016257, L05). The fraction forms (5/3, 2/5, 1/4, 3/4, 1/2) appear as \\tfrac in the lesson source (L03, L09, L10); 2/2 is a regex artefact of e^(-z^2/2).")
row("d1-cards-labs", "card lab results match the lab output",
    "course/modules/M/M4/cards.json (C cards and the lab-basis T cards); expected blocks in L05, L09, L10", "PASS",
    "Expected blocks = lab output (run_labs PASS). L05 max_entry_error 0.00016257 (n=100) and 0.00002223 (n=20000) are the (2,2) entry: 0.0009-0.00073743 and 0.0009-0.00087777 (lab printed s_22). L09: P(Z_n<=1) exact 0.833333, 0.847994, 0.843496, 0.835793, 0.833926; estimates 0.8548 and 0.8518 with SE 0.0056. L10: IQR 1.8220 (n=10) and 1.8838 (n=100); standardized variances 0.8807/1.1987 (t3) and 1.0211/0.9396 (normal) at n=10 and 100. All match the cards.")
row("d1-cards-math", "card mathematics re-derived",
    "course/modules/M/M4/cards.json: changed/new T cards M4-c040, c041, c043, c045, c048, c137, c160, c161, c168, c172, c185, c220, c226, c233-c236", "PASS",
    "Re-derived with python (checks/): P(|V|>10) t(3) = 0.002128; 10 P(|C|>10) = 0.634510 and 2/pi = 0.636620; x^3 P(|V|>1000) = 2.205308 (50-digit series, decimal module); Cauchy IQR = 2; gamma_4 of {-2,1,3} with 2/5, 1/2, 1/10 = 5/3; Bernoulli gamma_3 = 8/3 and gamma_4 = 73/9 at p = 1/10, 7/3 at p = 1/4; gamma_4 = 3 at pq = 1/6; Chebyshev bound 2 for n=2, eps=1/2, sigma^2=1; quartiles -1 and 1. Unchanged cards carried in d6-cards-sample.")
row("d1-cards-lesson-statements", "cards agree with current lesson text",
    "course/modules/M/M4/cards.json (M4-c038, c039, c040, c046, c214, c215, c220, c229); L03.html", "PASS",
    "Each card's Proposition, Example and Assumption number matches the renumbered L03 blocks (Prop 2.3 standardized moments, 2.4 affine, 2.5 kurtosis >= 1, Example 2.6 Bernoulli, Assumption 2.7, Prop 2.8 normal).")
row("d1-cards-hypotheses", "card hypotheses carry the proposition's hypotheses",
    "course/modules/M/M4/cards.json: M4-c038, c225, c039, c215", "PASS",
    "M4-c038/c225 (Proposition 2.3) state at least two values and positive weights; M4-c039/c215 (Proposition 2.4) add a is not 0, as the affine statement requires. M4-c140 (CLT) is not in this slice's changed set and is not claimed here.")
row("d1-cards-duplicates", "no duplicate cards", "course/modules/M/M4/cards.json", "PASS", "checks/cards_check.py: duplicate ids: set(); duplicate fronts: [].")
row("d1-cards-forward-reference", "no use before definition inside the lesson",
    "course/modules/M/M4/L03.html:118, :122-123, :262, :276, :401; cards.json M4-c220", "FAIL",
    "Card M4-c220 no longer cites Lesson 6 and its front is now about a density f. But L03 still uses the name 'standard normal law' six times (L03.html:118 Assumption 2.7, :122-123 Proposition 2.8, :262, :276, :401 table row). The standard normal law is defined in L06 (Definition 1.1, concept normal-distribution). So a term is used before its lesson defines it, which BUILDER_RULES and VERIFIER rule 5 forbid. Round 6 FAIL still open. Fix: state Assumption 2.7 and Proposition 2.8 for the density f only, and drop the name in L03 (or define it in L03).")
row("d1-freshness-registry", "registry freshness", "references/references.json; ledgers/M4/scripts/M4-d-r7/gates/verify_refs_offline.out", "PASS",
    "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems', EXIT 0.")
row("d1-gates-repo", "gates: ruff, mypy, pytest, configuration",
    "pyproject.toml; tests/test_run_labs.py, tests/test_labs.py, tests/test_memo_exemplars.py, tests/test_curriculum.py", "PASS",
    "ruff check and ruff format --check on course/modules/M/M4/grader and tests/labs/M4: 'All checks passed!', '17 files already formatted'. mypy --no-incremental: 'Success: no issues found in 385 source files'. pytest on the four files: all pass (ledgers/M4/scripts/M4-d-r7/gates/pytest_relevant.out). pyproject.toml change in the diff only adds ledgers/*/retired to extend-exclude.")
row("d2-2.6-constraints-exceptions", "2.6 constraints and exceptions match the code",
    "course/modules/M/M4/project.html:203-206 (Constraints, Grading mode), :212-220 (conventions and conditions)", "PASS",
    "Each raise in project.html:220 matches reference.py: matched_scale rejects non-int nu (type is int), nu <= 2; simulate_losses rejects family, nu None rule, n_draws <= 0 or non-int, empty or non-int positions, non-square/asymmetric/non-positive-definite cov; quantile_99 rejects empty and non-int. Accepts n_draws=1, nu None for gaussian, nu=3, one position, negative position. 'No function prints or warns': test_no_function_prints passes.")
row("d3-2.6-mut-new-student-error", "round-5/7 student-error mutants are killed",
    "ledgers/M4/mutants/v9_01..v9_04, d5_01, r7d_01..r7d_04", "PASS",
    "All KILLED in the mutate run (ledgers/M4/scripts/M4-d-r7/mutate_M4_0-9.out).")
row("d1-2.6-contract-notes-chi-claim", "contract notes: chi-square sharing counts",
    "course/modules/M/M4/project.html:228; grader/test_project.py:205-226", "PASS",
    "checks/run_seeds.sh over seeds 0-49: 2k/2k+1 sharing fails 50 of 50; 4j/4j+2 fails 50 of 50; 6j/6j+3 fails 39 of 50; all-even sharing fails 44 of 50. All four match the page. (Wording of 'independence' is graded under d1-prose-scope.)")
row("d1-2.6-mut-pairwise-survivor", "pairwise survivor d5_01 killed", "ledgers/M4/mutants/d5_01_chi_square_shared_by_draws_two_apart.py", "PASS",
    "KILLED in the mutate run by test_student_t_draws_do_not_share_chi_square (seed 0).")
row("d6-2.6-mut-integer-division-chi", "r6d_02 integer division chi shape", "ledgers/M4/mutants/r6d_02_integer_division_chi_shape.py", "PASS",
    "KILLED in the mutate run (ledgers/M4/scripts/M4-d-r7/mutate_M4_0-9.out).")
row("d6-2.6-mut-pivot-tolerance", "r6d_01 pivot tolerance 1e-15 (round-6 survivor)",
    "ledgers/M4/mutants/r6d_01_pivot_tolerance_1e15_rejects_tiny_variance.py; grader/test_project.py:541-", "PASS",
    "Round 6 survived; the tests added in 9373ef39 (test_one_position_with_a_variance_of_1e16_or_1e30_is_accepted) now kill it: 'KILLED ... -> test_one_position_with_a_variance_of_1e16_or_1e30_is_accepted[...]' (mutate run).")
row("d6-2.6-mut-lag3-sharing", "r6d_03 lag-three chi sharing (round-6 survivor)",
    "ledgers/M4/mutants/r6d_03_chi_square_shared_by_draws_six_apart_lag_three.py; project.html:215, :228", "PASS",
    "Round 6 survived; the lag-3 block added to test_student_t_draws_do_not_share_chi_square now kills it (KILLED in the mutate run).")
row("d1-lab-project-1", "project lab 1 (rung 1 worked example)", "course/modules/M/M4/project.html:55-145; tests/labs/M4/lab-M4-project-1.py", "PASS",
    "Twin unchanged in the diff; project.html:55-145 not in a hunk; run_labs M4: PASS (13/13) includes lab-M4-project-1 (gates/run_labs_M4.out).")
row("d1-lab-project-2", "project lab 2 (rung 2 completion)", "course/modules/M/M4/project.html:147-191; tests/labs/M4/lab-M4-project-2.py", "PASS",
    "Twin unchanged in the diff; run_labs M4: PASS (13/13) includes lab-M4-project-2 (gates/run_labs_M4.out).")
row("d1-lab-project-3", "project lab 3 (rung 4 stretch or interpretation)", "course/modules/M/M4/project.html:266-314; tests/labs/M4/lab-M4-project-3.py", "PASS",
    "Twin unchanged in the diff; project.html:266-314 not in a hunk; run_labs M4: PASS (13/13) includes lab-M4-project-3 (gates/run_labs_M4.out).")
row("d6-gate-mutate-m4", "gate: tools/mutate_graders.py --unit M4 --seeds 0-9 exits 0",
    "tools/mutate_graders.py; ledgers/M4/mutants/ (142 files)", "PASS",
    "'mutate_graders M4: PASS (142/142 killed)', EXIT 0 (ledgers/M4/scripts/M4-d-r7/mutate_M4_0-9.out).")
row("d6-gate-unit-checks", "gate: check_pages, check_dag, check_projects", "tools/check_*.py --unit M4", "PASS",
    "check_pages M4: PASS; check_dag M4: PASS; check_projects M4: PASS (ledgers/M4/scripts/M4-d-r7/gates/).")
row("d6-gate-labs", "gate: run_labs M4", "tests/labs/M4; course/modules/M/M4/*.html", "PASS",
    "run_labs M4: PASS (13/13) (gates/run_labs_M4.out).")
row("d6-gate-grader-reference", "gate: run_graders M4 seeds 0-49", "course/modules/M/M4/grader/reference.py", "PASS",
    "run_graders M4: PASS (reference 50/50 seeds, slowest 1.1 s) (gates/run_graders_M4_0-49.out).")
row("d6-gate-lint-types", "gate: ruff and mypy", "course/modules/M/M4/grader; tests/labs/M4; tools; tests", "PASS",
    "ruff check: All checks passed; ruff format --check: 17 files already formatted; mypy --no-incremental: no issues in 385 files.")
row("d6-gate-tests", "gate: relevant pytest", "tests/test_run_labs.py, tests/test_labs.py, tests/test_memo_exemplars.py, tests/test_curriculum.py", "PASS",
    "pytest -q: all pass, EXIT 0 (gates/pytest_relevant.out). Full suite not run (not needed for a grader and lab slice).")
row("d6-gate-refs", "gate: verify_refs --offline", "tools/verify_refs.py", "PASS", "560 entries, 0 problems (gates/verify_refs_offline.out).")
row("d6-gate-page-smoke", "gate: page_smoke for the project page (alone)", "course/modules/M/M4/project.html", "PASS",
    "tools/page_smoke.py --unit M4 --pages project: 'page_smoke modules/M/M4/project.html: PASS', 'page_smoke M4: PASS' (gates/page_smoke_project.out). Other pages of M4 not run.")
row("d6-2.6-alt-root-set", "alternatives: the other alternative roots", "ledgers/M4/scripts/alt_1..alt_5.py", "PASS",
    "Re-run this round for seeds 0-9: 10/10 PASS each (ledgers/M4/scripts/M4-d-r7/alts/run_builder_alts_0-9.out).")

# ---- new rows this round ----
row("d7-2.6-cross-term-threshold", "cross-term tolerance claim (the threshold)",
    "course/modules/M/M4/project.html:228", "FAIL",
    "Covered in d1-prose-numbers (the 5 % detection claim). Fix: 'up to about 3 %'.")
row("d7-2.6-negation-claim", "negating every position negates every loss",
    "course/modules/M/M4/grader/test_project.py:231-241; project.html:212, :220", "PASS",
    "test_a_short_position_is_valid_and_reverses_its_loss: 300 draws, two positions with cov [[4e-4,1e-4],[1e-4,9e-4]], both families; flipped == -long. Passes for the reference on seeds 0-49 (run_graders). The page's 'two-position example at 300 draws in both families' matches.")
row("d7-2.6-tiny-variance-claims", "tiny-variance claims in the new tests",
    "course/modules/M/M4/grader/test_project.py:559-590", "PASS",
    "Reference accepts variance 1e-16 and 1e-30 and the 2x2 covariance of order 1e-16 and 1e-30 (suite passes 50/50). Test comment 'a pivot check with an absolute tolerance above these values (for example pivot > 1e-15) would wrongly reject it' is true: r6d_01 (1e-15) is rejected on exactly those inputs. Mutants r7d_01 (pivot > 1e-30) and r7d_03 (later pivots > 1e-20) are both KILLED.")
row("d7-L01-L04-prose", "changed prose in L01-L04",
    "course/modules/M/M4/L01.html:51; L02.html:270, :347; L03.html:262; L04.html:52, :99", "PASS",
    "L01: 'a value at or below which the loss falls with at least a stated probability' matches Definition 3.1 (Q(p) = inf{x: F(x) >= p}). L02: the only mention of infinite moments is the caveat; no lesson-6 or lesson-10 forward reference remains; 'This lesson does not develop that term' is true. L04: the correlation is said to be developed later in the module, which L05 does; the covariance sentence no longer cites L05 by number.")
row("d7-L03-numerics", "L03 numerics and numbering after the renumbering",
    "course/modules/M/M4/L03.html (Sections 1-4, Problems, Misconceptions)", "PASS",
    "Recomputed: m3 = 67.40625 = 2157/32 and m4 = 583.83203125 = 149461/256 for the four-point law; the four terms of m3 sum to 34512/512; gamma_3 and gamma_4 of {-2,1,3} with 2/5, 1/2, 1/10: mean 0, gamma_3 = 0, gamma_4 = 15/9 = 5/3; Bernoulli p=1/10: gamma_4 = 73/9, p=1/4: 7/3, p=(1-1/sqrt3)/2: pq=1/6, gamma_4=3. Numbering: Definitions 2.1-2.2, Propositions 2.3-2.5, Example 2.6, Assumption 2.7, Proposition 2.8; every internal and cross-lesson reference (Lesson 2 Propositions 2.2, 2.4; Lesson 10 Proposition 2.3 cited from L06) matches its label.")
row("d7-cards-exact-lab-grade", "grade T only for values the page proves",
    "course/modules/M/M4/cards.json: M4-c185, M4-c233, M4-c234, M4-c235, M4-c236 (basis: Lab 1, Part A, exact Fraction arithmetic)", "FAIL",
    "These five cards are graded T. Their answers (P(Z_n <= 1) at n = 5, 10, 20, 40 and the gaps from Phi(1)) appear on the page only as printed output of the exact-arithmetic lab (L09 expected block); the page gives no closed form or hand derivation of those values, and Phi(1) = 0.841345 is not derived on the page. By the grading rule (VERIFIER ruling 9: results proved on the page are T; read off a lab are C naming the lab), grade them C with basis 'Lab 1, Part A (exact Fraction arithmetic on the die; no simulation)', or add the derivation to the page and keep T. M4-c165 (n = 1, 5/6, hand-derivable) and M4-c161/c168/c172 (closed form of Propositions 1.4 and 1.7 evaluated at a point) are not flagged.")

FIXES = {
    "d1-2.6-grader-comment-numbers": "test_project.py:43-45: replace 'about 29 %' with the measured 7 % to 9 % for the one-asset mutant (ledgers/M4/mutants/r8_03), or name the mutant that gives 29 %. Keep 0.024 and 15 %.",
    "d1-prose-numbers": "project.html:228: replace 'up to about 5 %' with 'up to about 3 %' (0 of 50 seeds detect +3 %; 19 of 50 detect +5 %).",
    "d1-prose-scope": "project.html:206 and :215: replace 'checks the independence' with 'checks that the share of pairs at lags one to three with both |loss| above the median is 1/4, which pairwise independence requires'.",
    "d1-cards-forward-reference": "L03.html:118, :122-123, :262, :276, :401: write Assumption 2.7 and Proposition 2.8 for the density f alone, without the name 'standard normal law', or define that law in L03 before use.",
    "d7-2.6-cross-term-threshold": "project.html:228: 'up to about 5 %' becomes 'up to about 3 %' (same fix as d1-prose-numbers).",
    "d7-cards-exact-lab-grade": "cards.json M4-c185, c233, c234, c235, c236: grade C with basis 'Lab 1, Part A (exact Fraction arithmetic on the die; no simulation)', or add the derivation to L09 and keep T.",
}
for _r in R:
    if _r["status"] != "PASS":
        _r["fix"] = FIXES[_r["id"]]
verdict = "FAIL" if any(r["status"] != "PASS" for r in R) else "PASS"

# ---- mutants: parsed from the round-7 mutate run ----
muts = []
for line in MUT_OUT.read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        muts.append({"name": name, "description": desc, "killed_by": killed if status == "KILLED" else "SURVIVED"})

counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL")}
frag = {
    "unit": "M4",
    "slice": "d",
    "round": 7,
    "verifier": "independent verifier (Haiku), unit M4, slice d, round 7; not a builder of M4",
    "pin": "9373ef39 (detached in the checkout; full hash in git rev-parse)",
    "base": "142ecfc2 (round-6 pin). Delta for slice d: course/modules/M/M4/{L01,L02,L03,L04,cards.json,project.html,grader/test_project.py}; ledgers/M4/mutants r6d_01..03 added; plans/M4-build-plan.md lines 246-257 (section 5.5); pyproject.toml extend-exclude",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD7-M4-d",
    "scratch": "/tmp/M4-d-r7-chk and /tmp/M4-d-r7-count (copied into ledgers/M4/scripts/M4-d-r7/checks/)",
    "verified_at": sys.argv[1],
    "verdict": verdict,
    "rows": R,
    "mutants": muts,
    "registry_flags": [],
    "freshness_flags": [],
    "gate_scope": "check_pages, check_dag, check_projects, run_labs, run_graders 0-49, page_smoke (project page only), ruff check and format, mypy --no-incremental, pytest on four files, verify_refs --offline, tools/mutate_graders.py --unit M4 --seeds 0-9",
    "notes": [
        "Round-6 FAILs: d1-2.6-alternatives now PASS (plan 5.5 scopes items 1, 2 to the Student-t family; my alternatives and the builder's alt_1..5 pass 10/10 seeds each). d6-2.6-mut-pivot-tolerance and d6-2.6-mut-lag3-sharing now PASS (r6d_01 and r6d_03 KILLED). d6-gate-mutate-m4 now PASS (142/142). d1-cards-forward-reference remains FAIL.",
        "New FAILs: d1-2.6-grader-comment-numbers (29 % not reproduced), d1-prose-numbers (5 % detection claim at project.html:228; measured 0 of 50 at +3 %, 19 of 50 at +5 %), d1-prose-scope ('checks the independence'), d7-cards-exact-lab-grade (five T cards read off exact lab output).",
        "Round-6 PASS rows with byte-identical subjects were carried with the prefix 'Carried from round 6'; every row whose subject changed was re-verified.",
        "Not checked: the 347/317-seed and 2000-seed sweep claims in test_project.py:31-48 (not re-run); full-suite pytest (only the four M4 files); page_smoke for other M4 pages; the card math of the 200 unchanged T cards beyond the round-6 sample.",
        "Gap outside slice d (not graded here): plans/M4-build-plan.md section 5.5 and Architect Q9 say the five alternatives live under tests/graders/M4/; that directory does not exist in the checkout. The builder files are under ledgers/M4/scripts/alt_*.py.",
        "The lag-four sharing family (checks/ and ledgers/M4/mutants/r7d_02) is killed by the cross-term and mean-absolute-loss tests on seed 0, not by the chi-square lag check, which does not read lag four (project.html:228 is accurate on that).",
    ],
    "summary": f"Slice d round 7: {len(R)} rows, {counts['PASS']} PASS, {counts['FAIL']} FAIL. Mutants: {sum(1 for m in muts if m['killed_by'] != 'SURVIVED')}/{len(muts)} killed. Non-PASS: " + "; ".join(r["id"] for r in R if r["status"] != "PASS") + ".",
}
out = ROOT / "ledgers/M4/M4-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, verdict, counts, len(muts))
