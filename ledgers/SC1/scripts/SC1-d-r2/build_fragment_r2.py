"""Write the round-2 verifier fragment for SC1 slice d (ledgers/SC1/SC1-d.json) from the verification results."""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(sys.argv[1])
R = "ledgers/SC1/scripts/SC1-d-r2"
OUT = f"{R}/out"
PAGE = "course/modules/SC/SC1/project.html"
GR = "course/modules/SC/SC1/grader"
LAB = "tests/labs/SC1"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> dict[str, str]:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    return item


rows = [
    row("SC1-d-ladder", "2.6-ladder", f"{PAGE}:40-49, 156-202, 205-257, 592-599", "PASS",
        "Ladder rung 1 (Lab 1, annotated in the interpretation at :154), rung 2 (Lab 2, class completion), rung 3 (spec, "
        "autograder and rubric), rung 4 (stretch, :601-607). `tools/check_projects.py --unit SC1` -> 'check_projects SC1: "
        "PASS' (out/check_projects.txt)."),
    row("SC1-d-grading-mode", "2.6-grading", f"{PAGE}:217-218; curriculum/03-markets.yaml (SC1 project grading: both)", "PASS",
        f"{PAGE}:218 'Both the autograder and the rubric apply'; the curriculum project entry grading is 'both'. "
        "check_projects PASS (out/check_projects.txt)."),
    row("SC1-d-spec-signatures", "2.6-spec", f"{PAGE}:214 vs {GR}/starter.py:16-38", "PASS",
        "The five names, parameter lists and return types on :214 equal starter.py:16, 21, 26, 31, 36 (reflection_tail(a: float, "
        "t: float) -> float; discrete_max_exceedance(instance: dict, n_steps: int) -> tuple[float, float]; nested_grid_counts "
        "-> tuple[int, int]; srw_max_count and srw_terminal_count -> int)."),
    row("SC1-d-hours", "2.6-hours", f"{PAGE}:33, 263-273", "PASS",
        "data-hours-project=28 (:33). Table rows 2+3+10+8+3+2 = 28 (:267-272, total :273). My own estimates, per component: "
        "rung 1 1.5-2.5 h; rung 2 2-3 h; three proofs 8-12 h; engine with tests 6-10 h; report 2-4 h; self-assessment 1-2 h; "
        "midpoint sum 27.0 h, 3.6% from 28 (within 30%)."),
    row("SC1-d-spec-grid-table", "2.6-spec", f"{PAGE}:430, 448", "PASS",
        "Round-1 FAIL resolved. The brief (:430) lists the grids 1, 4, 16, 64, 256 with a standard error at each; C5 level 4 (:448) "
        "says 'for every grid the brief lists'. No table is referenced."),
    row("SC1-d-spec-tolerance-statement", "2.6-spec", f"{PAGE}:227; {GR}/test_project.py:140", "PASS",
        "Round-1 FAIL resolved. :227 states the tolerance 1e-10 and the test at test_project.py:140 uses 1e-10. Quadrature test "
        "tolerance 1e-8 is stated where it is used (:146 in the test, not on the page)."),
    row("SC1-d-ag-reference", "2.6-autograder", f"{GR}/reference.py; tools/run_graders.py", "PASS",
        "`.venv/bin/python tools/run_graders.py --unit SC1 --seeds 0-49` -> 'run_graders SC1: PASS (reference 50/50 seeds, slowest "
        "0.4 s)', exit 0 (out/run_graders.txt)."),
    row("SC1-d-ag-starter", "2.6-autograder", f"{GR}/starter.py", "PASS",
        "starter.py copied as bm_checks.py with the suite: '123 failed, 4 passed' (out/starter_run.txt). The 4 passing tests are "
        "instance-only tests that never call the engine."),
    row("SC1-d-ag-instances", "2.6-autograder", f"{GR}/instance.py; ledgers/SC1/scripts/SC1-d-r2/instance_survey_r2.py", "PASS",
        "All 50 seeds valid (invalid seeds: []), 49 distinct levels, 50 distinct horizons, 50 distinct continuous tails at 6 dp "
        "(out/instance_survey_r2.txt). Labels all SIMULATED. Second instance is seed 7919 (test_project.py:33)."),
    row("SC1-d-ag-count", "2.6-autograder", f"{GR}/test_project.py; {PAGE}:7, 218, 289", "PASS",
        "`pytest --collect-only -q` in a clean workspace: '127 tests collected' (out/collect_only.txt). Page states 127 at :7, :218 "
        "and :289."),
    row("SC1-d-ag-messages", "2.6-autograder", f"{GR}/test_project.py:40-69 and all tests :109-452", "PASS",
        "Read every failure message. Helpers carry __tracebackhide__ (:44, :51, :61, :71). No message prints an expected value. "
        "Messages that interpolate, e.g. :410 and :428, echo the inputs only. Named ValueError tests (must_raise) cover only the "
        "conditions in project.html:230."),
    row("SC1-d-ag-overconstraint", "2.6-autograder", f"{GR}/test_project.py:244-245; {PAGE}:229-230",
        "FAIL",
        "Round-1 quadrature issue resolved: the 4000-panel Simpson alternative passes 50/50 under the 1e-10 test "
        "(out/alternatives_r2.txt, alt2_simpson_only_tail.py). NEW: an implementation that counts srw_max_count and "
        "srw_terminal_count by enumerating the 2**n walks (alternatives/alt2b_enumeration_srw.py, the method Lab 2 teaches at "
        f"{PAGE}:158-198) times out: seed 0 'TIMEOUT after 240s' (out/alt2b_enumeration_probe.txt). The cause is "
        "test_srw_integers_are_exact_for_a_long_odd_walk calling srw_terminal_count(41, 1) (test_project.py:245). Page :229-230 "
        "names no method, so enumeration is a correct implementation of the stated counts.",
        "Either state on project.html (Constraints, :215-216) that the counts must be computed without listing the 2**n walks "
        "(the reflection identity or a recurrence), or move the n=41 check to a closed form that does not depend on the method "
        "and keep only n <= 12 enumeration tests. Re-run alt2b on seed 0 after the change."),
    row("SC1-d-ag-alternatives-ok", "2.6-autograder", f"ledgers/SC1/scripts/SC1-d-r2/alternatives/*.py", "PASS",
        "run_alternatives_r2.py over seeds 0-49: alt1 NormalDist 50/50; alt2 Simpson 4000 panels 50/50; alt3 DP over "
        "(position, maximum) 50/50; alt4 Box-Muller step-major draws 50/50; alt5 cumsum and index subsampling 50/50; reference "
        "50/50 (out/alternatives_r2.txt)."),
    row("SC1-d-ag-mutants-plan", "2.6-mutation", "ledgers/SC1/mutants/m01-m10", "PASS",
        "`tools/mutate_graders.py --unit SC1 --seeds 0-9` (out/mutate_graders_r2.txt): m01-m10 each KILLED, killed_by listed in "
        "the mutants array."),
    row("SC1-d-ag-mutants-own", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21", "PASS",
        "m11-m15 (round 1) KILLED. Four new mutants written this round (generator ledgers/SC1/scripts/SC1-d-r2/"
        "make_mutants_r2.py): m18 nested coarse count copied from fine KILLED (test_one_step_coarse_grid_tracks_the_terminal_law, "
        "seed 1); m19 endpoint-only grid test KILLED (test_fine_count_is_the_discrete_estimate_times_n); m21 coarse stride = "
        "n_coarse KILLED (test_equal_grids_give_equal_counts). m20 is recorded separately (SC1-d-ag-mutants-seed)."),
    row("SC1-d-ag-mutants-survivors", "2.6-mutation", f"{GR}/test_project.py:418-423; ledgers/SC1/mutants/m16, m17", "PASS",
        "Round-1 survivors resolved: m16 KILLED by test_fine_grid_of_zero_steps_raises_value_error (ZeroDivisionError, which "
        "is not the named ValueError), m17 KILLED by test_coarse_grid_of_zero_steps_raises_value_error (out/mutate_graders_r2.txt; "
        "checked with a direct run, out/ and scripts unchanged)."),
    row("SC1-d-ag-mutants-seed", "2.6-mutation", f"ledgers/SC1/mutants/m20_draws_seeded_with_zero_for_every_instance.py; "
        f"{GR}/test_project.py", "FAIL",
        "m20 (draws seeded with 0 for every instance) SURVIVES all seeds 0-9 (out/mutate_graders_r2.txt). It violates "
        f"{PAGE}:225, which states 'draws its increments with random.Random(instance[\"seed\"])'. A candidate test that changes "
        "only the instance seed and requires a different sample (scripts/candidate_seed_test.py): reference fails 0 of 50 seeds, "
        "m20 fails 50 of 50 (out/candidate_seed_test.txt).",
        "Add to test_project.py a test that changing only instance['seed'] changes (estimate, standard error) for grid 4 or "
        "grid n_steps, as in candidate_seed_test.py; or remove the seed sentence at project.html:225 (only the order would then "
        "be free)."),
    row("SC1-d-ag-page-smoke", "2.5/2.6-gate", f"{PAGE}; tools/page_smoke.py", "PASS",
        "`tools/page_smoke.py --unit SC1 --pages project.html` -> 'page_smoke SC1: PASS' (out/page_smoke_project.txt). The tool "
        "runs every lab in Pyodide and pastes grader/reference.py into the in-browser grader (page_smoke.py:291-309)."),
    row("SC1-d-ag-docstring", "2.9-docstring", f"{GR}/test_project.py:9-13 vs :338-341 and :217-220, :309-315, :385-388",
        "FAIL",
        "The module docstring says 'no test compares the engine with its own earlier output' (:12-13). test_estimate_is_"
        "reproducible_for_the_same_instance (:338-341) asserts first == second, where both are engine outputs, the second taken "
        "after the first. The docstring also says 'Two tests compare two of the engine's own functions with each other' (:11). "
        "At least six tests compare two engine functions (:217-220, :309-315, :318-324, :328-335, :385-388, :396-405).",
        "Reword :11-13 so the sentence matches the code, e.g. 'one test checks that the same instance gives the same estimate, and "
        "several tests compare engine functions with each other on the same paths or by identity'."),
    row("SC1-d-rubric-observable", "2.6-rubric", f"{PAGE}:440-450", "PASS",
        "All 20 level cells read. Descriptors are checkable: numbered assumptions per result (C1), a named gap for each skipped "
        "step (C2), rounding statements and standard errors (C3), what a single seed and finite paths do not show (C4), grid "
        "table against the tail with nested inequality (C5)."),
    row("SC1-d-calib-A", "2.6-rubric-calibration", f"{PAGE}:456-508 (exemplar A)", "PASS",
        "Blind scores from the rubric and the passage text only: C1 1 (no numbered assumptions anywhere in the appendix), C2 2 "
        "(P1 has one unnamed 'by symmetry' step), C3 2 (decimals with no rounding statement, estimate with se), C4 2 (grid "
        "result as proof for every grid), C5 1 (no numbers). Official 2,2,2,2,1: every criterion within one level."),
    row("SC1-d-calib-B", "2.6-rubric-calibration", f"{PAGE}:510-591 (exemplar B)", "PASS",
        "Blind scores: C1 4 (A3, A4(b), A4(c) and the normal law each tied to a step; assumption lists precede P1, P2, P3), C2 3 "
        "(one step unnamed: the A4(b) step evaluates a path at the random time t-rho, which needs A4(g) joint measurability, "
        "L05.html:67, and A4(g) is not named), C3 4, C4 3 (no statement of what the nested comparison leaves open about the "
        "continuum), C5 4. Official 4,4,4,3,4: within one level on every criterion. Round-1 FAIL (blind C1 2) no longer holds "
        "on the current text (:574-581)."),
    row("SC1-d-exemplarA-claim", "2.9-prose", f"{PAGE}:499 and annotation :503-504", "PASS",
        "Exemplar A's sentence 'Finer grids give estimates closer ... falls as the grid refines' is an annotated defect. "
        "Annotation :504 is correct: tail minus estimate is 0.004361 at 256 steps and -0.001799 at 64 steps (out/recompute_r2.txt), "
        "and the lab says one seed cannot order the rows (:421). Not a page assertion."),
    row("SC1-d-exemplarB-proof", "2.4-mathematics", f"{PAGE}:576-582 (exemplar B appendix)", "PASS",
        "Re-derived step by step. A = {tau<=t} = {M_t>=a} by continuity and IVT (B_0=0<a); P(tau=t)<=P(B_t=a)=0; B~ is a standard "
        "BM independent of F_rho (A3); P(A, B_t<a)=1/2 P(A, rho<t) by A4(b) with the path-valued Y; {B_t>=a} subset of A gives "
        "P(A)=2P(B_t>=a). P2: erfc(x)=2(1-Phi(x sqrt2)) by substitution w=z/sqrt2, with x=a/sqrt(2t). P3: continuity from below "
        "and P2 give P(tau<inf)=1. The only gap is the unnamed A4(g) step recorded at SC1-d-calib-B."),
    row("SC1-d-exemplarB-numbers", "2.2-numbers", f"{PAGE}:527 vs {PAGE}:150 and {LAB}/lab-SC1-project-1.py:141", "FAIL",
        "Every number on exemplar B matches my unrounded recomputation (out/recompute_r2.txt): tail 0.086497, tail/2 0.043248, "
        "one-step 0.059548 and se 0.010735, band 0.055726, difference 0.016300 (1.52 se), grid rows, nested 35/29/27/22, walk "
        "1588/794. But :527 says the Simpson difference 'is given to two significant digits', while Lab 1 prints 9.13e-15 "
        "(:150), which has three significant digits, because the twin formats with {:.2e}.",
        "Change :527 to 'three significant digits', or change the lab format to {:.1e} and the printed line to match, and keep "
        "the spec (:216) consistent with whichever is chosen."),
    row("SC1-d-lab1-run", "2.5-labs", f"{PAGE}:55-153; {LAB}/lab-SC1-project-1.py", "PASS",
        f"Page code equals the twin (0 diff lines). `python -I -W error lab-SC1-project-1.py` exit 0, stderr 0 bytes; stdout "
        "equals the expected block up to the final newline (out/labs_check.txt). tools/run_labs.py --unit SC1: PASS (11/11)."),
    row("SC1-d-lab1-docstring", "2.2-prose-vs-output", f"{PAGE}:64-66, {LAB}/lab-SC1-project-1.py:7-8, :65-66, :139-141", "FAIL",
        "The docstring (twin lines 65-66, identical on the page) says 'Every printed number is rounded to six decimal places ... "
        "except the Simpson difference, which is printed to two significant digits'. Printed output (:139) shows H = 2.083 and "
        "a = 2.474, which are the generator's three-decimal values, not six-decimal numbers. The Simpson difference is printed "
        "with {:.2e} (:141) as 9.13e-15, which is three significant digits. The Simpson carve-out from round 1 is present, so "
        "only the two claims above remain.",
        "Say that H and a are printed as generated (three decimals) and N as an integer, and change 'two significant digits' to "
        "match the format actually used (three, or change {:.2e} to {:.1e})."),
    row("SC1-d-lab2-run", "2.5-labs", f"{PAGE}:157-203; {LAB}/lab-SC1-project-2.py", "PASS",
        "Page code differs from the twin only at page lines 33 and 36 (the two blanks; 8 diff lines, out/labs_check.txt). The twin "
        "runs with exit 0 and stderr 0 bytes; stdout equals the expected block (29, 22, 7, True). Enumeration re-derived: 29 / 22 / "
        "7 for n=6, a=2 (out/recompute_r2.txt)."),
    row("SC1-d-lab2-attribution", "2.2-attribution", f"{PAGE}:202 vs course/modules/SC/SC1/L06.html:75-97", "PASS",
        "Round-1 FAIL resolved. The page cites 'Corollary 1.4 of Lesson 6' (discrete tail identity: #{M_N>=a} = #{S_N>=a} + "
        "#{S_N>a}, L06.html:87-88) and 'the discrete reflection identity of Proposition 1.3' (L06.html:75-76, which it proves). "
        "Both numbers and the statement exist at the locators read; the claim that it holds for every n and a>=1 matches "
        "Corollary 1.4's assumptions. P1 is no longer cited for the identity."),
    row("SC1-d-lab3-run", "2.5-labs", f"{PAGE}:296-422; {LAB}/lab-SC1-project-3.py", "PASS",
        "Page code equals the twin (0 diff lines); twin exit 0, stderr 0 bytes; stdout equals the expected block (out/labs_check.txt)."
        " Values re-derived in out/recompute_r2.txt: hits 29, 24, 32, 43, 40; se 0.010735, 0.009819, 0.011239, 0.012870, "
        "0.012455; tail minus estimate 0.026948, 0.037215, 0.020788, -0.001799, 0.004361; nested 35, 29, 27, 22 vs fine 40; walk "
        "1588, 794."),
    row("SC1-d-lab3-docstring", "2.2-prose-vs-output", f"{LAB}/lab-SC1-project-3.py:307-308 (same text on the page at :307-308)",
        "FAIL",
        "The docstring says 'Every printed number is rounded to six decimal places ... The walk line is an exact count'. The "
        "printed line 'seed 0: H = 2.083, a = 2.474, N = 487' (:391) prints the generator's three-decimal H and a, not six-decimal "
        "numbers, so the claim is false as written.",
        "Say that H and a are printed as generated and N as an integer, and keep the six-decimal claim for the computed values only."),
    row("SC1-d-labs-pytest", "2.5-labs", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py; "
        "tests/test_memo_exemplars.py", "PASS",
        "`.venv/bin/pytest -q -p no:cacheprovider tests/test_labs.py -k SC1 tests/test_run_labs.py tests/test_page_checks.py "
        "tests/test_memo_exemplars.py` -> exit 0 (out/pytest_relevant.txt)."),
    row("SC1-d-statements", "2.4-mathematics", f"{PAGE}:232-256", "PASS",
        "P1: P(M_t>=a)=2P(B_t>=a) re-derived (the proof at exemplar B :576 is complete). P2: erfc(a/sqrt(2t))=2(1-Phi(a/sqrt t)); "
        "numeric check at seed 0: erfc form 0.08649666086033343 vs 2(1-Phi) 0.08649666086033347, difference 4.2e-17 "
        "(out/recompute_r2.txt). P3: P(tau_a<=t)=P(M_t>=a) and P(tau_a<inf)=1 follow from continuity and P2."),
    row("SC1-d-A1-label", "2.4-assumptions", f"{PAGE}:235-241", "PASS",
        "Round-1 FAIL resolved: the page now names A0 as the definition of standard Brownian motion (Definition 1.1 of L01.html:58) "
        "and A3, A4 as Lesson 5's Assumptions 3 and 4 (L05.html:59, :268)."),
    row("SC1-d-A3-A4-usage", "2.4-assumptions", f"{PAGE}:235-239, 571-578; {LAB.replace('tests/labs/SC1','course/modules/SC/SC1')}/L05.html:59-67, 268-274", "PASS",
        "A3 is stated for a bounded stopping time (L05.html:268-274, rho <= c); the page applies it to rho = tau_a wedge t <= t "
        "(:239, :576). A4(c) gives the stopping-time property of tau_a (L05.html:65). A4(b) freezing is used with a path-valued Y "
        "(L05.html:62 allows a random continuous path)."),
    row("SC1-d-notation", "2.4-notation", f"{PAGE} passim; notation/notation.json", "PASS",
        "notation.json has 8 symbols and 26 macros. T is defined there as a sample size in S1, and the page uses T only in its "
        "disclaimer (:223). Phi is the standard normal CDF (notation.json M4 entry; page :223, :248). \\Normal is N(mu, sigma^2) "
        "and the page writes \\Normal(0,t) for variance t (:246, :578), consistent. \\Prob and \\se are macros; no page symbol "
        "collides with a registry meaning (H, a, N, B, M_t, tau_a, rho, se are not registry symbols)."),
    row("SC1-d-define-before-use", "2.9-define-before-use", f"{PAGE}:45 and :37 vs definitions at :159 and :53", "FAIL",
        "Round-1 items resolved: N is defined at its first use (:57, 'N is the path count') and 'almost surely' is defined in "
        "parentheses at its first use (:447). NEW: 'simple random walk' is named at :45 (the ladder) with no meaning, and is first "
        "explained at :159 ('A walk takes n steps of +1 or -1'). 'grid maximum' is used in the lede at :37 and defined at :53.",
        "At :45, add a plain-words gloss ('a walk of n steps, each +1 or -1 with probability 1/2'). At :37, gloss 'grid maximum' "
        "or move the phrase after :53."),
    row("SC1-d-discretization-bias", "2.9-DAG-D9", f"{PAGE}:228 (dfn), :421, :448", "PASS",
        "Round-1 FAIL resolved. A plain <dfn>discretization bias</dfn> (no data-concept) is defined at :228, which is its first "
        "use. This is the D9 resolution in plan section 4."),
    row("SC1-d-monte-carlo-term", "2.9-DAG-D8", f"{PAGE}", "PASS",
        "Round-1 FAIL resolved: the page no longer uses 'Monte Carlo'. It says 'seeded simulation' in plain prose (D8 resolution)."),
    row("SC1-d-dag", "2.9-DAG", f"{PAGE}; tools/check_dag.py --unit SC1", "PASS",
        "`tools/check_dag.py --unit SC1` -> PASS (out/check_dag.txt). Linked concepts stopping-time (M6) and normal-distribution "
        "(M4) are in the closure. grep over project.html for the D1-D9 names (Ito, SDE, Euler, Milstein, Ornstein, Girsanov, "
        "Feynman, Poisson, Levy, Black-Scholes, barrier, Donsker, bias-variance, Monte Carlo, pseudo-random) found none."),
    row("SC1-d-scope-words", "2.9-scope", f"{PAGE} passim (every, all, never, any, almost surely)", "PASS",
        "Each scope word in visible prose is either a proof statement (:223 'never negative' with the pathwise reason; :226 coarse "
        "never larger; :252 'for every t>=0' proved in P3), a computed statement from Lab 3 (:296 'every coarse count'), or an "
        "explicit limit (:447, :562). The only unsupported 'for every grid' is inside exemplar A and is annotated (:466)."),
    row("SC1-d-process-words", "2.9-process-words", f"{PAGE}; grader/*.py; {LAB}/lab-SC1-project-*.py", "PASS",
        "Case-insensitive grep for build, builder, verifier, round, fixer, planner, architect, REQUEST, draft, Q[0-9]: no hits in "
        "learner-facing text. 'rounding' is the statistical sense."),
    row("SC1-d-banned-structure", "2.9-structure", f"{PAGE}; tools/check_pages.py --unit SC1", "PASS",
        "`tools/check_pages.py --unit SC1` -> PASS (out/check_pages.txt). BUILDER_RULES §1.3-1.4 phrases grepped in project.html and "
        "the grader/labs: TODO, TBD, lorem, for brevity, beyond the scope, clearly, obviously, it is important to note, studies "
        "show, experts agree, historically, roughly, ellipsis: no hits. The only 'about' is inside exemplar A (:462, :467), annotated "
        "as a defect."),
    row("SC1-d-registry", "2.1-citations", f"{PAGE}:603-606, 611-614; references/references.json (shreve2004stochastic)", "PASS",
        "`tools/verify_refs.py --unit SC1` live: 'live re-verification of SC1: 1 of 560 entries, 0 problems' (out/verify_refs_live.txt); "
        "offline 560 entries 0 problems. The page cites Shreve (2004) at book level with no locator. Curriculum sources (03-markets.yaml:523-524) "
        "are two; Karatzas & Shreve (1991) has no registry key (references.json has no match), so the page's statement at :611 is "
        "true."),
    row("SC1-d-privacy-claim", "2.9-claims", f"{PAGE}:281, 596, 628", "PASS",
        "Round-1 UNVERIFIABLE resolved by reading code: course/assets/js/grader.js:33-61 derives the seed from the workspace ID and "
        "stores the draft via store.put('files') after a 400 ms debounce on input; grader.js:112 stores the result; store.js header "
        "(lines 1-10) says IndexedDB in the learner's browser and 'Nothing here ever leaves the browser'; rubric.js:8, 95-97 store "
        "scores with store.put('kv'). Not observed: a live browser session and its network log."),
    row("SC1-d-tools-gates", "2.5/2.6-gates", "ruff, mypy, pytest (see evidence)", "PASS",
        "ruff check and ruff format --check on course/modules/SC/SC1/grader and tests/labs/SC1: 'All checks passed!', '15 files "
        "already formatted' (out/ruff.txt). mypy --no-incremental: 'Success: no issues found in 385 source files' (out/mypy.txt). "
        "check_projects, check_pages, check_dag, run_labs (11/11), page_smoke: PASS (out/)."),
    row("SC1-d-numbers-prose", "2.2-numbers", f"{PAGE}:57, 154, 202, 258, 421, 550-553 (student prose and Lab 3 figures)", "PASS",
        "Every number on the page recomputed from unrounded values (out/recompute_r2.txt, scripts/recompute_r2.py): H=2.083, a=2.474, "
        "N=487, tail 0.086497, one-step 0.059548 / 0.010735, band 0.055726, half tail 0.043248, difference 0.016300 (1.52 se), grid "
        "rows, nested 35/29/27/22 vs 40, walk 1588/794 of 4096, Lab 2 29/22/7. All match the printed values to the displayed digit."),
]

mutant_lines = (ROOT / R / "out/mutate_graders_r2.txt").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mutant_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, description, killer = m.groups()
    killed = None if status == "SURVIVED" or killer.strip() == "None" else killer.strip()
    mutants.append({"name": name.removesuffix(".py"), "description": description.strip(),
                    "killed_by": killed, "file": f"ledgers/SC1/mutants/{name}"})

fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 2,
    "verifier": "Haiku 5.5 independent verifier (slice d, round 2)",
    "pin": "67c47689",
    "base": "1c1645f3",
    "checkout": str(ROOT),
    "scratch": "/tmp/sc1d_r2_* (removed), ledgers/SC1/scripts/SC1-d-r2/out (kept)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Curriculum second source 'Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991)' "
        "(curriculum/03-markets.yaml:524) has no registry record; the page correctly omits it (project.html:611-614). "
        "Architect decision still open."
    ],
    "freshness_flags": [],
    "notes": [
        "Delta from pin 1c1645f3 read in full for project.html (64 changed lines), grader/reference.py, grader/test_project.py, "
        "tests/labs/SC1/lab-SC1-project-1.py, and ledgers/SC1/mutants (17 files, previously absent). grader/instance.py, starter.py, "
        "lab-SC1-project-2.py and lab-SC1-project-3.py are byte-identical to round 1 and were re-run anyway.",
        "Round-1 FAILs resolved: spec-grid-table, spec-tolerance-statement, ag-mutants-survivors, A1-label, lab2-attribution, "
        "calib-B (blind C1 now 4), discretization-bias, monte-carlo-term, define-before-use (N and 'almost surely' parts), "
        "privacy-claim (UNVERIFIABLE, now verified by code reading). Round-1 ag-overconstraint quadrature part is resolved; the "
        "enumeration over-constraint is new.",
        "Mutants: 21 in ledgers/SC1/mutants (m01-m17 from round 1 and earlier verifiers, m18-m21 written this round). 20 killed; "
        "m20 survives. Alternatives: 5 plus a probe (alt2b), run on seeds 0-49.",
        "Exemplar B's P1 uses the joint measurability of the path at a random time (A4(g), L05.html:67) without naming it. "
        "Within calibration tolerance, so not a row FAIL; recorded at SC1-d-calib-B.",
        "Could not check: (1) a live in-browser run of the grader panel and self-assessment form (save and submission behaviour "
        "observed only in code); (2) the 2000-panel Simpson variant from round 1 under the new 1e-10 tolerance was not re-run; "
        "(3) the slice's lessons, cards and other pages (other slices); (4) the Pyodide run time of the 127 tests beyond the "
        "page_smoke 60 s limit it enforces.",
    ],
    "summary": "SC1 slice d round 2 (project.html, grader, project labs, mutants, alternatives): FAIL. 48 rows: 40 PASS, 8 FAIL, "
               "0 UNVERIFIABLE. Mutants 20/21 killed; m20 (seed ignored) survives. Alternatives: all 5 pass 50/50; the "
               "enumeration probe times out on the n=41 test.",
}

out = ROOT / "ledgers/SC1/SC1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, len(rows), "rows", len(mutants), "mutants")
