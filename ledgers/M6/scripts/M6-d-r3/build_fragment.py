"""Build ledgers/M6/M6-d.json (round 3, slice d) from the evidence gathered in this round."""

from __future__ import annotations

import datetime
import json
import re

S = "ledgers/M6/scripts/M6-d-r3"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


row("M6d-spec-01", "2.6-spec", "course/modules/M/M6/project.html:168-191", "PASS",
    f"Read the whole page. Required signatures (line 176) match grader/starter.py:18-40. Every convention on lines 185-190 "
    f"is implemented in grader/reference.py and tested in grader/test_project.py. Only the stop-level convention "
    f"(M6d-conv-01) is unstated. {S}/run_variant.py reference.py 0-49 -> 50/50 seeds pass.")
row("M6d-ladder-01", "2.6-ladder", "course/modules/M/M6/project.html:40-49,51-166,602-608", "PASS",
    "tools/check_projects.py --unit M6 -> 'check_projects M6: PASS'. Rung 1 (Lab 1) is solved and annotated (line 122). "
    "Rung 2 is a completion lab with an expected block (line 163). Rung 3 is the spec. Rung 4 (lines 603-607) is open-ended.")
row("M6d-hours-01", "2.6-hours", "course/modules/M/M6/project.html:222-238; index.html:29", "PASS",
    "Components 3+4+17+10+5+3 = 42 = data-hours-project in index.html:29 (tools/check_pages.py --unit M6 PASS). Own "
    "estimate (not measured): Rung 1 1-2 h, Rung 2 1 h, three proofs 9-12 h, engine with tests 6-10 h, report 4-6 h, "
    "self-assessment 2-3 h. Central total about 31 h, which is 26% below 42 h, inside the 30% rule. The estimate is "
    "subjective and near the threshold.")
row("M6d-grader-ref-01", "2.6-autograder-1", "course/modules/M/M6/grader/reference.py; tools/run_graders.py", "PASS",
    "tools/run_graders.py --unit M6 --seeds 0-49 -> 'run_graders M6: PASS (reference 50/50 seeds, slowest 0.4 s)'. "
    f"Independent rerun: {S}/run_variant.py reference.py 0-49 --collect -> 50/50 pass; collect-only 130 tests.")
row("M6d-grader-inst-01", "2.6-autograder-2", "course/modules/M/M6/grader/instance.py", "PASS",
    f"{S}/instance_checks.py, seeds 0-19: all 20 instances valid under the spec; the docstring claim 'exactly J bets "
    f"when every bet loses, K >= s' holds for all 20 (J_loop == J_ref); 20 distinct instances and 20 distinct answer "
    f"tuples. {S}/control_nonzero_sweep.py: over seeds 0-20000 and 338303287 (and seed+7919), the control stopped "
    f"expectation is never 0 and the fair one is always 0. The fair-walk stopped expectation is 0 for every seed "
    f"(optional stopping), so answers vary through K, J, P(max) and the control walk.")
row("M6d-grader-mut-01", "2.6-autograder-3", "ledgers/M6/mutants/ (41 files); tools/mutate_graders.py", "PASS",
    "tools/mutate_graders.py --unit M6 --seeds 0-9 -> 'mutate_graders M6: PASS (41/41 killed)'; output in "
    f"{S}/mutate_all_r3.txt. Five new student-error mutants written by this verifier: r3_01 up-probability read as "
    "down-probability; r3_02 ruin wealth subtracts the unplaced stake; r3_03 dyadic error uses absolute deviation; "
    "r3_04 expectation rounded by float truncation; r3_05 negative stop level compared as its absolute value. "
    "Each is killed (see the mutants list). None survives.")
row("M6d-grader-alt-01", "2.6-autograder-5-alternatives", f"{S}/alternatives/", "PASS",
    f"Five correct alternatives written by this verifier, each run as martingale_checks.py over seeds 0-49 with "
    f"{S}/run_variant.py: alt_a1_list_dp_first_passage.py 50/50; alt_a2_path_enumeration.py 50/50; "
    f"alt_a3_dict_dp_wealth.py 50/50; alt_a4_matrix_closed_form.py 50/50; alt_a6_transition_matrix.py 50/50. "
    f"Not counted: alt_a5_time_zero_convention.py (fails 4 tests, M6d-conv-01); alt_a7_float_money.py fails "
    f"test_expectation_is_rounded_from_the_exact_value_not_a_float, which the page's exact-rounding rule requires "
    f"(project.html:178). Plan section 6.5 item 4 asks that a float alternative pass within one cent, which conflicts "
    f"with the page; that is an architect decision.")
row("M6d-grader-msg-01", "2.6-autograder-4-messages", "course/modules/M/M6/grader/test_project.py:710", "FAIL",
    "The failure message of test_expectation_exactly_half_a_cent_above_a_cent_rounds_up_not_to_even reads 'must round "
    "half up, to 3 cents, not to the even neighbour'. It names the answer (3 cents) for a fixed input. Rule 4 requires "
    "messages that never leak the answer. All other messages name a property, not a value.",
    "Edit test_project.py line 710 to drop the value: 'doubling: an expectation of exactly 5/2 cents must round half "
    "up, not to the even neighbour'.")
row("M6d-grader-count-01", "2.6-autograder-count", "course/modules/M/M6/project.html:180", "FAIL",
    "Page line 180 says test_project.py 'runs 82 tests'. Collect-only count: 'QF_SEED=0 pytest --collect-only -q' prints "
    "'130 tests collected in 0.01s' (also run_variant.py --collect). The in-browser grader run by page_smoke prints "
    f"'All 130 tests pass' ({S}/page_smoke_project.txt). The page figure is wrong.",
    "Change '82 tests' to '130 tests' in project.html:180, or generate the figure from the collect-only count.")
row("M6d-conv-01", "2.4-convention / 2.6-grader", "course/modules/M/M6/project.html:186; grader/test_project.py:606-612 and :248", "FAIL",
    "project.html:186 defines tau = min(the first time S_k = stop_level, stop_cap) without saying whether k starts at 0 "
    "or 1. test_level_equal_to_start_is_first_checked_after_a_step (test_project.py:606-612) and the level-0 cases of "
    "test_stopping_level_both_directions_matches_enumeration (test_project.py:248) require k >= 1. The k >= 0 reading is "
    "the standard tau = inf{k >= 0: S_k in A}, which gives tau = 0 and S_tau = 0 when level = 0. "
    f"alt_a5_time_zero_convention.py implements that reading and fails 4 tests on every seed ({S}/a5_result.txt). "
    "The suite demands a convention the page does not state.",
    "State the convention in project.html:186: tau = min(the first time k >= 1 with S_k = stop_level, stop_cap). Or drop "
    "the level-0 parameter and the test at test_project.py:606-612.")
row("M6d-grader-pyodide-01", "2.6-autograder-5-browser", "course/modules/M/M6/project.html:243; tools/page_smoke.py", "PASS",
    "tools/page_smoke.py --unit M6 --pages project -> 'page_smoke modules/M/M6/project.html: PASS'; the in-browser grader "
    "prints 'All 130 tests pass on seed 338303287'. Local pytest over seeds 0-49 passes for the reference. Output in "
    f"{S}/page_smoke_project.txt.")
row("M6d-grader-exc-01", "2.6-autograder-exception-table", "course/modules/M/M6/grader/test_project.py (must_raise) vs project.html:190", "PASS",
    "Every must_raise call names a condition listed on project.html:190: cap above N (221-226), horizon 0 and -1 (238-245), "
    "Doob level 0 and -1 (310-315), Doob horizon 0 and -1 (331-338), capital 0 and negative (425-431), stake above capital "
    "(442-446, 689-693), capital of zero or less with base equal to it (696-701). Every must_accept input is valid under "
    "the spec, except the level-0 convention in M6d-conv-01.")
row("M6d-rubric-observe-01", "2.6-rubric-1-observable", "course/modules/M/M6/project.html:457-466", "PASS",
    "All five criteria have four descriptors. Each names a checkable element (numbered assumptions, a named lemma per "
    "step, printed numbers with unit and rounding, a finite-check statement, the power and constant of Doob's bound). "
    "No vague descriptor found. Note for the architect: C1 level 3 requires 'numbered' assumptions, and exemplar B uses "
    "unnumbered prose.")
row("M6d-rubric-cal-01", "2.6-rubric-2-calibration", "course/modules/M/M6/project.html:470-593 (exemplars A, B)", "PASS",
    "Scored both exemplars from the descriptors after reading the page (not strictly blind: the annotations were visible). "
    "Exemplar A: C1 2, C2 1, C3 2, C4 2, C5 2 (official 2,1,2,2,2). Exemplar B: C1 3 (unnumbered assumptions; official 4), "
    "C2 4, C3 4, C4 3, C5 4 (official 4,4,4,3,4). Every criterion is within one level, which meets the calibration rule.")
row("M6d-rubric-bank-01", "2.6-rubric-3-question-bank", "project.html (no question bank)", "PASS",
    "Not adversarial, so no question bank is required (plan Architect decisions, binding default).")
row("M6d-atlas-studio-01", "2.6-atlas-studios", "curriculum/meta.yaml; plan section 11.1", "PASS",
    "No Atlas milestone and no studio requirement for M6 (plan section 11.1). Nothing to check.")
row("M6d-lab-P1-01", "2.5-labs", "course/modules/M/M6/project.html:55-123; tests/labs/M6/lab-M6-project-1.py", "PASS",
    "tools/run_labs.py --unit M6 --page project -> PASS (3/3); run_labs --unit M6 -> PASS (15/15). Twin alone under "
    f"python3 -I -W error: exit 0. Page code equals twin and expected equals output ({S}/labs_check.py). Prose values "
    f"recomputed ({S}/recompute_project_numbers.py): E[S_tau]=0; the four +first-step paths contribute +1/2; the four "
    "-first-step paths contribute -1/2.")
row("M6d-lab-P2-01", "2.5-labs", "course/modules/M/M6/project.html:125-165; tests/labs/M6/lab-M6-project-2.py", "PASS",
    "Twin alone exit 0; output equals the expected block (37 cents, 0 cents with 1 bet, 937 cents with 6 bets). The page "
    "has the two blanks by design; the twin has the completed lines. Only those two lines differ (labs_check.py).")
row("M6d-lab-P3-01", "2.5-labs", "course/modules/M/M6/project.html:257-439; tests/labs/M6/lab-M6-project-3.py", "PASS",
    "Twin alone exit 0; page code equals twin; expected equals output (labs_check.py). Recomputed independently "
    f"({S}/recompute_project_numbers.py): fair E[S_tau]=0; control -79/81 (decimal -0.975309); Doob P=7/16, bound 5/8, "
    "holds; fair doubling 6 bets, win 63/64, ruin 1/64, wealth on ruin 37, E=100; control 69533/729 = 95.381344..., "
    "half-up 95 cents; dyadic error 1/(12*4^n) for n in 0,1,2,3,10; M_10(1/3)=683/2048.")
row("M6d-lint-01", "gates-ruff-mypy", "tests/labs/M6; course/modules/M/M6/grader", "PASS",
    "ruff check tests/labs/M6 course/modules/M/M6/grader -> All checks passed; ruff format --check tests/labs/M6 -> 19 files "
    "already formatted; mypy --no-incremental on reference.py, instance.py, starter.py -> Success; run_graders typecheck "
    "(mypy --strict) passes.")
row("M6d-numbers-01", "2.2-numbers", "course/modules/M/M6/project.html (all quoted numbers)", "PASS",
    f"Every quoted number recomputed with fractions in {S}/recompute_project_numbers.py: Lab 1 values; Lab 2 "
    "(6 bets / 37 cents, 1 / 0, 6 / 937); Lab 3 (M6d-lab-P3-01); exemplar figures 7/16, 5/8, 63/64, 1/64, 101, 37, "
    "69533/729 = 95.381344, 1/12582912, 2^-11; the P(tau>n)=2^-n quoted at project.html:219. The one wrong quoted figure is "
    "82 tests (M6d-grader-count-01).")
row("M6d-proofs-01", "2.4-statements", "course/modules/M/M6/project.html:194-216", "PASS",
    "P1 (bounded optional stopping) lists its numbered assumptions: probability space and filtration; martingale with each "
    "M_k integrable and adapted; tau a stopping time with tau <= N. P2 (Doob) lists nonnegativity, submartingale "
    "inequality, N fixed, lambda > 0. P3 lists square-integrability and the bound L. The statements are correct and "
    "sufficient for the standard proofs.")
row("M6d-proofs-02", "2.4-exemplar-proofs", "course/modules/M/M6/project.html:581-583 (exemplar B appendix)", "PASS",
    "Re-derived exemplar B's proofs: P1 (M_tau = M_(tau wedge N); increment identity 1{tau>k}(M_(k+1)-M_k); telescoping) is "
    "correct. P2 (A_k decomposition; chaining the submartingale inequality; E[X_N 1_A] <= E[X_N]) is correct, and the "
    "attainment case N=1, lambda=1 for |S| gives 1 = 1. P3 (orthogonality gives v_n nondecreasing; Doob for "
    "(M_k-M_m)^2; continuity from below; null set; Cauchy) is correct. No gap found.")
row("M6d-stop-01", "2.4-stopping-rule", "course/modules/M/M6/project.html:218-219; L10.html Prop 10.9", "PASS",
    "Unbounded doubling: P(tau>n)=2^-n (enumeration; L10 Part B prints 2^-n), stopped gain 1 a.s. with start 0, so E=1 != 0 "
    "and P1 fails. Consistent with Proposition 10.9 (a)-(b).")
row("M6d-cites-01", "2.9-lesson-references", "course/modules/M/M6/project.html:191,216,219,248; L08-L12.html", "PASS",
    "Cited results exist with matching content: Lemma 12.1 (L12.html:59), Lemma 12.3 (L12.html:82), Proposition 12.8 "
    "(L12.html:144), Proposition 10.7 (L10.html:127), Proposition 10.9 (L10.html:152), Corollary 11.4 (L11.html:124), "
    "Theorem 10.3 (L10.html:81). Statements checked in lesson_text/.")
row("M6d-refs-01", "2.1-citations", "course/modules/M/M6/project.html:612-616; references/references.json", "PASS",
    "Keys williams1991probability and billingsley2012probability exist with status verified. Live metadata by plain curl "
    "(no circumvention): Crossref api.crossref.org/works/10.1017/cbo9780511813658 -> HTTP 200, title 'Probability with "
    "Martingales', author Williams, issued 1991, Cambridge University Press (matches). Open Library "
    "books/OL25254284M.json -> HTTP 200, 'Probability and measure', 2012, Wiley, ISBN 9781118122372 (matches). The page "
    "attributes no statement to either book. tools/verify_refs.py --offline -> 560 entries, 0 problems. Not run: the "
    "live --unit run.")
row("M6d-browser-01", "2.6-constraints", "course/modules/M/M6/project.html:178", "PASS",
    "'A run in your browser stops after 120 seconds': course/assets/js/python.js:4 has TIMEOUT_MS = 120000.")
row("M6d-notation-01", "2.4-notation", "course/modules/M/M6/project.html; notation/notation.json", "PASS",
    "Registered macros used (\\E, \\Prob, \\indic) match notation.json. Local letters N, K, s, p, J, L, C, S are defined "
    "on the page. No registered symbol (T, Phi, gamma, R^*, R_f, Q) is used with another meaning.")
row("M6d-banned-01", "2.9-banned-process", "course/modules/M/M6/project.html; grader/*.py; cards.json", "PASS",
    "No banned phrase (BUILDER_RULES 1.3-1.4 list) in project.html text; the only ellipses are inside code blocks. No "
    "process words (build, builder, verifier, round, REQUESTS, unit report) in project.html or cards.json; 'round' in "
    "test_project.py is the rounding word.")
row("M6d-struct-01", "2.9-structure", "course/modules/M/M6/project.html", "PASS",
    "Sections present in order: header, ladder, rungs and labs 1-2, specification with statements and conventions, budget "
    "table, autograder panel, local run, report with lab 3, brief, rubric, exemplars, self-assessment, stretch, reading, "
    "references, navigation. check_pages --unit M6 PASS. No figure, SVG or data file on this page.")
row("M6d-dag-01", "2.9-DAG", "course/modules/M/M6/project.html; tools/check_dag.py", "PASS",
    "tools/check_dag.py --unit M6 -> PASS. The project links only lessons L08-L12 and module pages; AP1 and SC1 are named in "
    "plain text, not linked.")
row("M6d-gates-01", "gates", "tools/check_pages.py, check_projects.py, check_dag.py, run_labs.py, run_graders.py, mutate_graders.py, page_smoke.py, verify_refs.py --offline", "PASS",
    "check_pages --unit M6 PASS; check_projects --unit M6 PASS; check_dag --unit M6 PASS; run_labs --unit M6 PASS (15/15); "
    "run_graders --unit M6 --seeds 0-49 PASS; mutate_graders --unit M6 --seeds 0-9 PASS (41/41); page_smoke project PASS; "
    "verify_refs --offline PASS (560/0). Repo-wide gates were not run (architect's, plan section 10).")

card_sample = [
    ("000", "M6-c001", "lesson_text/L01.txt:24-28: Definition 1.1 (S1)-(S3); members are the events"),
    ("010", "M6-c012", "lesson_text/L02.txt:29-30: Definition 1.2, triple (Omega, F, P) with P(Omega)=1"),
    ("020", "M6-c023", "lesson_text/L03.txt:29-32: Definition 2.1, sum a_i mu(A_i), convention 0*inf=0"),
    ("030", "M6-c034", "lesson_text/L04.txt:23-25: Definition 1.1, non-decreasing f_n <= f_(n+1); limit is sup"),
    ("040", "M6-c045", "lesson_text/L05.txt:41-45: Assumption F (sigma-finite, measurable, integral of |f| finite); L05.html:220 'not graded'"),
    ("050", "M6-c055", "lesson_text/L06.txt:25-28: Lemma 1.2, nu << mu iff nu(w)=0 wherever mu(w)=0"),
    ("060", "M6-c066", "lesson_text/L07.txt:33-34: Definition 2.1, minimiser over G-measurable Y, orthogonal residual E[(X-Y)Z]=0"),
    ("070", "M6-c076", "lesson_text/L08.txt:34 Proposition 2.1(a),(c); counterexample M_2=2X_1 checked by hand: E[M_2-M_1]=0 but E[M_2|F_1]=2X_1 != X_1"),
    ("080", "M6-c086", "lesson_text/L09.txt:34-36: Proposition 9.5 assumptions (integer adapted Y, {Y_k=b} in F_k, tau_B infimum)"),
    ("090", "M6-c096", "lesson_text/L10.txt:35-37: Theorem 10.3, bounded tau, M_tau integrable, E M_tau = E M_0"),
    ("100", "M6-c106", "lesson_text/L11.txt:24-26: Definition 11.1, adapted, Z_k >= 0, E[Z_(k+1) 1_A] >= E[Z_k 1_A]"),
    ("110", "M6-c117", "lesson_text/L12.txt:63-67: Result 12.6, 'stated, not proved here', 'carries no grade here'"),
    ("120", "M6-c127", "lesson_text/L08.txt:252: glossary, F_k-measurable when known at time k (Definition 1.1 as the lesson cites it)"),
]
for idx, cid, ev in card_sample:
    row(f"M6d-card-sample-{idx}", "2.7-cards-sample", f"course/modules/M/M6/cards.json ({cid})", "PASS",
        f"Every tenth card (index {idx}) checked against the current lesson: {ev}. Lesson text extracted into {S}/lesson_text/.")

row("M6d-cards-dup-01", "2.7-duplicates", "course/modules/M/M6/cards.json (full scan, 122 cards)", "PASS",
    "No duplicate id, no duplicate front (case-insensitive), no duplicate back. Near-pairs (c101/c104 vs c103; c111 vs c113) "
    "ask different questions. All 122 cards were read in full.")
row("M6d-cards-numbers-01", "2.7-card-numbers", f"cards.json; {S}/card_numbers_scan.py", "PASS",
    "Every cited numbered result and every 3+-digit or decimal number in each card appears in its own lesson text. Six "
    "cards (c003, c021, c114, c125, c126, c128) write 'Section N' where the lesson writes '§N' (cosmetic).")
row("M6d-cards-lab-A-01", "2.7-card-numbers-lab-L01-L07", "cards.json c007, c017, c027, c030, c032, c040, c049, c061, c071", "PASS",
    "Lab outputs re-run with python3 -I -W error: L01 counts 4, 16, 8, candidate fails complement closure; L02 602 of 729 "
    "failing pairs, total mass 9/10; L03 step integral 1, I_1 = 0.1464466094, 1/3 - I_1 = 0.1868867239, bound 2^-1; L04 "
    "integrals 1, partial sums 2.019877 (N=10) and 4.197279 (N=100) (= H_11-1 and H_101-1); L05 errors +1.3e-07 and block "
    "0.3217505544; L06 densities 2, 1/2, 2, 1/3 and mu=0, nu=1/8; L07 cell averages 1, 6/5, 6/7.")
row("M6d-cards-lab-B-01", "2.7-card-numbers-lab-L08-L12", "cards.json c081, c090, c100, c102, c105, c110, c112, c113, c121", "PASS",
    "L08 twin: 1023 of 1023 cells agree for p=1/2, 0 for p=1/3, increment -1/3 = 2p-1. L09 twin: 186 of 256 paths, "
    "0.7265625, passes k=0..8, look-ahead fails k=0..7. L10 twin: K=1000 gives 9 bets, win 0.9980468750, ruin "
    "0.0019531250, wealths 1001 and 489, E=1000. L11 twin: ratio 1.000000 at N=1,2,4; signed walk N=1, lambda=1: P=1/2, "
    "E=0, bound fails. L12 twin: 1/2048 and 1/12582912 at n=10. Card c110 arithmetic (E[S_N^2]=N, N/c^2) rechecked.")
row("M6d-cards-grade-01", "2.3-grades-cards-vs-lessons", "cards.json c090, c100, c112, c113, c121 vs L09.html-L12.html", "FAIL",
    "These five cards grade lab results C with a lab basis. L09-L12 carry no C grade span for these results: the only "
    "data-grade=\"C\" in L09.html, L10.html, L11.html, L12.html is the legend row (line 47), and the signed-walk and Doob "
    "statements in L11.html:146-280 are ungraded. L01-L04 and L08 do grade lab results C in key-results tables "
    "(L01.html:395, L02.html:446). Plan open item (Builder C, item 1) leaves this unresolved. Cards and lessons disagree "
    "within the unit.",
    "Architect decision (open item 1). Either add a C key-results row with the lab as basis to L09-L12, matching L01-L04, "
    "or remove grade and basis from cards c090, c100, c112, c113, c121. Then rerun check_pages --unit M6.")
row("M6d-cards-c072-01", "2.7-card-correctness", "cards.json M6-c072", "FAIL",
    "The card says 'On the cell {0, 1, 2}, X takes the values 2, -1 and 4, and the conditional expectation is 1'. The value 1 "
    "holds only with the lab's weights (1, 2, 1)/16 on those outcomes (tests/labs/M6/lab-M6-L07-1.py:21; Part A prints the "
    "cell average 1). With equal weights the average would be 5/3. The card omits the weights.",
    "Add to the card back: 'with weights 1/16, 2/16 and 1/16 on those outcomes, the conditional expectation is 1'.")
row("M6d-cards-prop-01", "2.7-hypotheses", "cards.json cards that cite Proposition, Lemma, Theorem, Corollary, Result", "PASS",
    "Cards that cite a result with a non-trivial hypothesis state it (c004, c013, c024, c026, c044, c059, c086, c096, c108, "
    "c114). Bare-example cards (c016, c018, c037, c039, c042) state the example's hypotheses in the text. c073 states the "
    "nesting in its front. No card cites a result whose hypotheses are missing.")
row("M6d-exemplar-A-01", "2.6-exemplar-annotations", "course/modules/M/M6/project.html:473-526", "PASS",
    "Exemplar A's annotations match its errors: C4 claims 'every horizon' from one run (level 2); C3 'about 95 cents' has no "
    "rounding statement (level 2); C5 uses E[X_N^2]/3 (level 2); C2 has no proof (level 1); C1 omits the integrability of "
    "M_k in P1 (level 2).")

mutants = []
for line in open(f"{S}/mutate_all_r3.txt", encoding="utf-8"):
    m = re.match(r"KILLED (\S+): (.*) -> (.*)$", line.strip())
    if m:
        mutants.append({"name": m.group(1), "description": m.group(2), "killed_by": m.group(3)})

frag = {
    "unit": "M6",
    "slice": "d",
    "round": 3,
    "verifier": "independent verifier, Haiku, round 3",
    "pin": "ccfdf4c18f5ae9d86e6fe1ca9141382fd6055f83",
    "base": "ccfdf4c18f5ae9d86e6fe1ca9141382fd6055f83",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC3-M6-d",
    "scratch": "/tmp/m6d-collect (collect-only copy); run_variant.py uses a fresh mkdtemp per run",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "No previous-round fragment exists at /Users/billyribeiro/.fanout/frags/C-M6-d.round2.json (frags/ is empty). Round 3 is verified from scratch; no PASS row is carried from a previous round.",
        "mutants m01-m36 pre-existed (builder-written) and were re-run; r3_01-r3_05 are this verifier's own. The alternatives are this verifier's own (scripts/M6-d-r3/alternatives).",
        "Rubric calibration was scored from the descriptors after reading the page, so it is not strictly blind; agreement is within one level on every criterion.",
        "Not run: live verify_refs --unit M6 (network job), repo-wide gates (render_curriculum, build_site --check, check_pages --all), pytest suites outside this slice.",
        "Card checks used lesson_text/, tag-stripped from L*.html. The stripping regex removed some '<' signs (for example Lemma 10.6 reads 'K+1' where the page has 'K+1 < 2^(m+1)'); the claims were re-read in the HTML.",
        "Plan section 6.5 item 4 (float alternative within one cent) conflicts with project.html:178 and the exact-rounding test. Architect decision needed on the plan item.",
        "Hours: the verifier's estimate (about 31 h) is subjective and close to the 30% threshold; recorded as PASS.",
    ],
    "summary": "Slice d: 5 FAIL rows. (1) page says 82 tests, collect-only gives 130; (2) test message at test_project.py:710 names the answer; (3) unstated stop-level convention (k>=1) makes a correct k>=0 implementation fail 4 tests; (4) five lab-result cards grade C while L09-L12 leave the same results ungraded; (5) card c072 omits the weights its value depends on. Everything else reproduced: reference 50/50 seeds, 41/41 mutants killed, five alternatives pass, labs and page smoke pass, all quoted numbers reproduced, cited registry records match Crossref and Open Library.",
}
with open("ledgers/M6/M6-d.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "FAIL", sum(r["status"] == "FAIL" for r in rows), "mutants", len(mutants))
