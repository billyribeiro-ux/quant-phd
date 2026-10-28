"""Writes ledgers/CF1/CF1-d.json (round 6) from the verifier's rows and mutant table, then prints the validation result.

Usage (from the checkout): .venv/bin/python ledgers/CF1/scripts/CF1-d-r6/write_fragment_r6.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path("/tmp/verify6-CF1-d")
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

C5 = "Carried from round 5 (project.html and grader/test_project.py cited lines byte-identical since the previous pin 00745fe): "
CARD = "course/modules/CF/CF1/cards.json"
PROJ = "course/modules/CF/CF1/project.html"
TEST = "course/modules/CF/CF1/grader/test_project.py"
ROUND5 = json.loads(Path("/tmp/fanout-frags/CF1-d.round5.json").read_text(encoding="utf-8"))
R5 = {r["id"]: r for r in ROUND5["rows"]}
S = "ledgers/CF1/scripts/CF1-d-r6/"
MUT = "ledgers/CF1/mutants/"
MUTATE = "tools/mutate_graders.py --unit CF1 --seeds 0-9 (output /tmp/cf1-v/d/r6/mutate.out: 39 of 40 killed; m36 survives)"

rows = [
    # ---- carried from round 5: cited subject byte-identical (spec line 214, 188; tests unchanged)
    dict(id="proj-npv-empty-overconstraint", check="2.6-spec / ruling (b): NPV over an empty list is a named error",
         location=f"{PROJ} line 214; {TEST} lines 108-109", status="PASS",
         evidence=C5 + "test_npv_rejects_empty_flows is in the 50-seed reference run (run_graders --seeds 0-49: 50/50); the named error is in the spec at line 214."),
    dict(id="proj-capex-float-overconstraint", check="2.6-spec / ruling (a),(b): capex 1000.0 refused, integer cents",
         location=f"{PROJ} line 188 and 214; {TEST} params capex-zero, capex-negative, capex-float (lines 373-376)", status="PASS",
         evidence=C5 + "the float case is tested by test_invalid_project_raises_a_named_error[capex-float]; m40 (float capex accepted) is KILLED in the round-6 mutation run."),
    dict(id="proj-named-errors-untested", check="2.6-spec / ruling (a): each named error has a test",
         location=f"{PROJ} line 214; {TEST} test functions for capex, life, revenue, cost, tax, share, inflation, rates, NPV, IRR, payback, Monte Carlo", status="PASS",
         evidence=C5 + "each named error on line 214 maps to a test (checked by name against the 73 collected tests on seeds 0-49)."),
    dict(id="proj-capex-negative-untested", check="2.6-spec / mutation: negative capex",
         location=f"{TEST} param capex-negative; reference.py line 36", status="PASS",
         evidence=C5 + "m18 (negative capex accepted) KILLED by test_invalid_project_raises_a_named_error[capex-negative] in " + MUTATE + "."),
    dict(id="proj-wc-timing-unenforced", check="2.6-spec / ruling (a): working-capital timing",
         location=f"{PROJ} line 202; {TEST} test_working_capital_* and test_single_year_project_has_no_working_capital", status="PASS",
         evidence=C5 + "tests unchanged; m02, m17, m21 KILLED in " + MUTATE + "."),
    dict(id="proj-exemplar-b-locator", check="2.2/2.6 page: Exemplar B cash-flow locators",
         location=f"{PROJ} line 428 (Exemplar B, 2 Cash flows)", status="PASS",
         evidence=C5 + "line 428 is byte-identical; its locators (Lab 1 steps 3, 5, 6, 8) were re-read this round against the Lab 1 twin output: -600/-50/+650 (step 3), sum zero (step 5), flows (step 6), shield PV 1,865.14 (step 8)."),
    dict(id="proj-rung1-step-line-wording", check="2.9 prose: rung 1 description and Lab 1 hypothesis",
         location=f"{PROJ} lines 44 and 55", status="PASS",
         evidence=C5 + "lines 44 and 55 are byte-identical since 00745fe; Lab 1 output (run_labs CF1, twin tests/labs/CF1/lab-CF1-project-1.py) prints nine steps, step 7 = 926.00 and step 8 = 1865.14, as the hypothesis says."),
    dict(id="proj-browser-storage-claim", check="2.9 prose: autograder saves code in the browser",
         location=f"{PROJ} line 238; course/assets/js/grader.js lines 30-34 and 61", status="PASS",
         evidence=C5 + "line 238 and grader.js are unchanged since 00745fe (git diff --stat 00745fe d57df1e lists neither)."),
    dict(id="proj-must-raise-text-claim", check="2.6-spec / ruling (a): message wording not graded",
         location=f"{TEST} lines 53-59 (must_raise)", status="PASS",
         evidence=C5 + "must_raise catches ValueError and calls pytest.fail otherwise; no message text is compared."),
    dict(id="proj-exemplar-b-crossing-claim", check="2.4 / 2.9: Exemplar B, NPV crossing argument",
         location=f"{PROJ} line 425 (Exemplar B, 1 Recommendation)", status="PASS",
         evidence=C5 + "line 425 is byte-identical. Re-derived: flows after t = 0 are positive (3,150, 4,000, 5,000), so each discount term falls with the rate and NPV(-1+) is +infinity, NPV(+infinity) is the outlay; one zero, at 15.3177 percent (Lab 3 line 364). Checked with reference.npv in the round-6 run."),
    dict(id="proj-error-message-unenforced", check="2.6-spec / ruling (a): message wording not graded",
         location=f"{PROJ} lines 192 and 214; {TEST} must_raise lines 53-59", status="PASS",
         evidence="Re-verified on the changed line 192: the sentence 'the autograder checks the exception type; the wording of a message is not graded' is present, and must_raise compares no text. Fresh in round 6."),
    dict(id="proj-never-prints-or-mutates-unenforced", check="2.6-spec / mutation: no printing, no argument mutation, fresh objects",
         location=f"{PROJ} line 192; {TEST} test_functions_never_print, test_input_project_is_not_changed, test_flow_list_arguments_are_not_changed, test_returned_lists_are_fresh_objects", status="PASS",
         evidence="Fresh in round 6 (line 192 changed this round; its no-print, no-mutation and fresh-object sentence is unchanged): the four tests pass on reference (73 passed, seed 0); m10 KILLED in " + MUTATE + "."),
    dict(id="proj-tangent-root-claim", check="2.6-spec / ruling (a),(g): tangent root not reported",
         location=f"{PROJ} line 207; {TEST} test_irr_does_not_report_a_tangent_root (lines 140-144) and ..._at_the_window_end (147-152)", status="PASS",
         evidence="Fresh in round 6 on the changed line 207: both tests pass on reference; m09 (tangent reported) and m24 (tangent within tolerance reported) KILLED in " + MUTATE + "; m37 (zero samples reported) KILLED."),
    dict(id="proj-tangent-endpoint-reported", check="2.6-spec / mutation: zero at a window end not reported",
         location=f"{PROJ} line 207; {TEST} lines 147-160; reference.py lines 111, 133-135", status="PASS",
         evidence="Fresh in round 6: test_irr_does_not_report_a_tangent_root_at_the_window_end and test_irr_does_not_report_a_zero_at_the_high_end_of_the_window pass on reference; m23 (high-end zero reported) KILLED in " + MUTATE + "."),
    dict(id="proj-spec-formulas-and-window", check="2.4-math / 2.6-spec: formulas and conventions (window bounds in proj-irr-window-unenforced)",
         location=f"{PROJ} lines 199-210 (Conventions); reference.py lines 60-188", status="PASS",
         evidence="Fresh in round 6: EBITDA, depreciation, tax, working capital, real flows, NPV, Fisher, payback and Monte Carlo formulas match reference.py (reference.py unchanged) and the 73 tests; Lab 3 numbers reproduced by the reference engine (script " + S + "lab3_vs_engine.py: mean 885.85, sd 2445.52, se 54.68, 787 negative, min -4808.83, max 13800.44, zero-volatility mean 926.00, IRR 0.153177, payback 2.37 and 2.7535). The window bounds are scored in proj-irr-window-unenforced (FAIL)."),
    dict(id="proj-mc-draw-method-unenforced", check="2.6-spec / ruling (a),(b): Monte Carlo draw method",
         location=f"{PROJ} line 209; {TEST} test_monte_carlo_* (lines 454-505)", status="PASS",
         evidence="Fresh in round 6 on the changed line 209: the mean-one identity E[exp(s z - s^2/2)] = 1 holds for every s (the affine-in-m claim is correct: flows are linear in m). test_monte_carlo_draws_follow_the_seeded_gauss_stream, the zero-volatility test and the three-SE test pass on reference; m06, m14, m25, m26, m33, m35 KILLED in " + MUTATE + ". Wording note: 'the expected NPV over the draws equals the deterministic NPV' is the population expectation, which is what the identity proves; the sample mean is only checked within three standard errors."),
    dict(id="proj-mutant-tangent-survivor", check="2.6-spec / mutation: tangent-reporting mutants",
         location=f"{MUT}m09_tangent_root_reported.py, {MUT}m24_tangent_within_tolerance_reported.py", status="PASS",
         evidence="Both KILLED in " + MUTATE + "."),
    dict(id="proj-lab1-twin-output", check="2.5 labs: Lab 1 twin and page output",
         location=f"{PROJ} lines 56-131; tests/labs/CF1/lab-CF1-project-1.py", status="PASS",
         evidence="run_labs --unit CF1: PASS (9/9); the twin ran under python -I -W error with empty stderr (/tmp/cf1-v/d/r6/labs/lab-CF1-project-1/out.txt)."),
    dict(id="proj-lab2-completion-twin", check="2.5 labs: Lab 2 completion, blanks and twin output",
         location=f"{PROJ} lines 134-179; tests/labs/CF1/lab-CF1-project-2.py", status="PASS",
         evidence="Lab 2 docstring changed this round (twin only); run_labs --unit CF1: PASS (9/9), which checks every page line equals the twin line or holds one of the three ___ blanks (lines 167-169); twin output matches the page's expected lines (flows -9000.00, 3150.00, 4000.00, 5000.00; NPV 926.00)."),
    dict(id="proj-lab3-sanity-run", check="2.5 labs: Lab 3 reference numbers",
         location=f"{PROJ} lines 249-375; tests/labs/CF1/lab-CF1-project-3.py", status="PASS",
         evidence="run_labs CF1: PASS; twin output (/tmp/cf1-v/d/r6/labs/lab-CF1-project-3/out.txt) equals the page's expected block; every engine-side number was reproduced by reference.py in " + S + "lab3_vs_engine.py."),
    dict(id="proj-exemplar-a-quote", check="2.9 prose: Exemplar A quoted sentences and annotations",
         location=f"{PROJ} lines 401-419 (Exemplar A); line 417 changed this round", status="PASS",
         evidence="Fresh in round 6: line 417 'Practitioners use payback.' carries the annotation 'a practice claim with no key, no grade and no locator' (line 418), which matches the level-2 score; the other sentences quote Lab 1 steps 3 and 5 and Lab 3 (885.85 at seed 42, 2,000 draws, volatility 0.2)."),
    dict(id="proj-exemplar-numbers", check="2.2 numbers in prose: exemplar and page figures",
         location=f"{PROJ} lines 401-439", status="PASS",
         evidence="Recomputed in round 6: 926.00 - 885.85 = 40.15; 40.15/54.68 = 0.734 -> 0.73; 787/2000 = 39.35 percent; 2445.52/885.85 = 2.76; 15.32 percent is 0.153177 rounded; payback 2.37 (Lab 3); discounted payback 2.7535 (2,830.58/3,756.57 = 0.7535 on the year-3 flow, Lab 3 prints 2.753500)."),
    dict(id="proj-about-39-percent", check="2.2 numbers in prose: 39.35 percent negative draws",
         location=f"{PROJ} line 374 (Lab 3 interpretation)", status="PASS",
         evidence="Recomputed: 787 / 2000 = 0.3935 -> 39.35 percent; Lab 3 prints 'draws with a negative NPV: 787 of 2000'; reference.py run with seed 42 gives 787 negative."),
    dict(id="proj-registry-reading-list", check="2.1 citations: reading list keys",
         location=f"{PROJ} lines 456-463; references/references.json", status="PASS",
         evidence="All three keys are in references/references.json (graham2001theory, glasserman2003monte, damodaran2012investment) and tools/verify_refs.py --offline: 560 entries, 0 problems. Registry flags for used_by are listed in registry_flags (not a row)."),
    dict(id="proj-registry-graham-glasserman", check="2.1 citations: Exemplar B evidence section",
         location=f"{PROJ} line 437 (Exemplar B, 5 Evidence); course/modules/CF/CF1/L06.html Remark 2.4", status="PASS",
         evidence="Read in references/references.json: graham2001theory title 'The theory and practice of corporate finance: evidence from the field', Journal of Financial Economics, volume 60, issue 2-3, pages 187-243 (matches line 437 exactly); glasserman2003monte title 'Monte Carlo Methods in Financial Engineering', 2003 (matches). Curriculum CF1 sources (curriculum/02-economics-finance-core.yaml) name 'Graham & Harvey (2001), JFE 60(2-3)'. No paper content is quoted."),
    dict(id="proj-hours-table", check="2.9 structure: time budget arithmetic",
         location=f"{PROJ} lines 217-234 (Time budget; line 227 changed this round); course/modules/CF/CF1/index.html line 29-38", status="PASS",
         evidence="Rows 1+1+4+2+1+1+2 = 12 = data-hours-project; lessons L01-L06 each data-hours=8 (6 x 8 = 48 = data-hours-lessons); 48 + 12 = 60 = curriculum CF1 hours (curriculum/02-economics-finance-core.yaml). Hub split 80.0% / 20.0% matches. Pace not judged (architect ruling)."),
    dict(id="proj-banned-phrases", check="2.9 structure: banned phrases and scope words",
         location=f"{PROJ} (whole file); {CARD} (whole file)", status="PASS",
         evidence="Script " + S + "scans_r6.py: scan for TODO, TBD, lorem, ellipsis, 'for brevity', 'details omitted', 'beyond the scope', 'roughly half', 'about 6%', 'historically', 'It can be shown', 'studies show', 'it is important to note' and similar: 0 hits in project.html and cards.json. Scope words (only, same, most, all, raises) were read in context (round-6 scan)."),
    dict(id="proj-structure-and-gates", check="2.8 commands: check_projects, check_pages, check_dag",
         location="tools/check_projects.py --all; tools/check_pages.py --unit CF1; tools/check_dag.py --all", status="PASS",
         evidence="Round 6 output: 'check_projects CF1: PASS', 'check_pages CF1: PASS', 'check_dag CF1: PASS' (all units PASS)."),
    dict(id="proj-pytest-lab-helper", check="2.8 commands: lab helper and twin checks",
         location="tests/labs/CF1/*.py; tools/run_labs.py --unit CF1", status="PASS",
         evidence="run_labs --unit CF1: PASS (9/9). Each twin also run as python -I -W error: exit 0, stderr 0 bytes (/tmp/cf1-v/d/r6/labs/*/err.txt)."),
    dict(id="proj-test-count-72", check="2.8 commands: the page's collected-test count equals the real count (id kept from round 5; the page now says 73)",
         location=f"{PROJ} line 194 ('collects 73 checks'); {TEST}", status="PASS",
         evidence="pytest --collect-only -q on the reference solution: 73 tests for every seed 0-49 (50 runs). Page says 73. Round-5 count of 72 was before the new test test_irr_finds_a_root_at_the_low_end_of_the_discount_factor_window (test file lines 174-181)."),
    dict(id="proj-grader-reference-50-seeds", check="2.5/2.8 grader: reference passes 50 seeds",
         location="tools/run_graders.py --unit CF1 --seeds 0-49", status="PASS",
         evidence="Round 6: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)'."),
    dict(id="proj-mutants-round4-new", check="2.6-spec / mutation (project slice): round-4 mutants",
         location=f"{MUT}m25 .. m30 (byte copies from /tmp/verify5-CF1-d)", status="PASS",
         evidence="m25-m30 all KILLED in " + MUTATE + "."),
    dict(id="proj-mutants-round5-new", check="2.6-spec / mutation (project slice): round-5 mutants",
         location=f"{MUT}m31 .. m35", status="PASS",
         evidence="m31, m33, m34, m35 KILLED; m32 (IRR window low end at 1e-3) is KILLED in round 6 by test_irr_finds_a_root_at_the_low_end_of_the_discount_factor_window on all 50 seeds (run_variants_r6.py: 50 of 50 failing)."),
    dict(id="proj-mutants-round6-new", check="2.6-spec / mutation (project slice): NEW student-error mutants of round 6 (m37-m40)",
         location=f"{MUT}m37_zero_samples_counted_as_sign_changes.py, m38_bisection_absolute_tolerance_in_discount_factor.py, m39_discounted_payback_fraction_uses_undiscounted_flow.py, m40_capex_float_accepted.py (written by " + S + "make_mutants_r6.py)", status="PASS",
         evidence="Four new plausible student errors: all KILLED on seed 0 in " + MUTATE + " (m37 by test_irr_does_not_report_a_tangent_root; m38 by test_irr_finds_roots_across_the_whole_search_window; m39 by test_discounted_payback_uses_discounted_flows; m40 by capex-float). The fifth new mutant, m36 (window extended low), survives: see proj-irr-window-unenforced."),
    dict(id="proj-equivalent-mutant-proof", check="2.6 mutation: equivalent mutants",
         location=f"{MUT} (no equivalent mutant kept)", status="PASS",
         evidence="All 40 mutants are non-equivalent: 39 are killed, and m36 changes the output (witness: irr_roots([-1.0, 1e5]) returns [99999.00000000001] on m36 and [] on reference, script " + S + "witness_r6.py). No equivalence proof is needed."),
    dict(id="proj-alternatives-correct", check="2.6-spec / ruling (b): alternative correct engines are accepted",
         location=f"{S}alts/alt_r5_1..6, {S}alts/alt_r6_1..5, ledgers/CF1/scripts/CF1-d-r5/alts_r4_copy/alt1, alt3-alt6 (round-4 alternatives)", status="PASS",
         evidence="run_variants_r6.py over seeds 0-49: alt_r5_1..6, alt_r6_1..5 (8,001-point log grid; algebraic flows and Fisher expansion; exp-ratio multiplier; inverse-power discounting; Illinois regula falsi with 1e-13 bracket) and alt1, alt3-alt6: 0 failing seeds each. Round-4 alt2 (linear-x grid, 200,001 points) fails test_irr_finds_roots_across_the_whole_search_window on all 50 seeds: it violates the page's log-x grid convention and misses the root at rate 500, between the window end and its first sample; a correct test on an engine that departs from the stated convention."),
    dict(id="proj-high-end-test-spec-justified", check="2.6-spec / ruling (b): the high-end zero test is spec-justified",
         location=f"{TEST} lines 155-160; {PROJ} line 207", status="PASS",
         evidence="Line 207 states 'neither is a zero exactly at an end of the window'; test_irr_does_not_report_a_zero_at_the_high_end_of_the_window tests exactly that sentence. m23 KILLED."),
    dict(id="proj-page-smoke", check="2.8 commands: page_smoke on the project page",
         location="tools/page_smoke.py --unit CF1 --pages project", status="PASS",
         evidence="Round 6 output: 'page_smoke modules/CF/CF1/project.html: PASS', 'page_smoke CF1: PASS' (in-browser grader: all 73 tests pass on the reference seed run). Output /tmp/cf1-v/d/r6/page_smoke.out."),
    dict(id="proj-verify-refs", check="2.1 citations: verify_refs offline and live for CF1",
         location="tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1", status="PASS",
         evidence="Round 6: 'offline integrity: 560 entries, 0 problems'; 'live re-verification of CF1: 2 of 560 entries, 0 problems'."),
    dict(id="proj-check-dag", check="2.7 DAG and concepts", location="tools/check_dag.py --all", status="PASS",
         evidence="Round 6: 'check_dag CF1: PASS' (all units PASS). The CF1 curriculum entry (curriculum/02-economics-finance-core.yaml, module CF1) lists prereqs [M1, AC1]; the DAG check passes on that entry."),
    dict(id="proj-ruff-format", check="2.8 commands: ruff check and format on grader and labs",
         location="course/modules/CF/CF1/grader; tests/labs/CF1", status="PASS",
         evidence="Round 6: 'All checks passed!' and '13 files already formatted'. mypy --no-incremental on tests/labs/CF1 and grader: 'Success: no issues found in 13 source files'."),
    dict(id="proj-lab3-recomputed-numbers", check="2.2/2.4 numbers in prose: Lab 3 interpretation and exemplar numbers",
         location=f"{PROJ} lines 374 and 434", status="PASS",
         evidence="Recomputed by reference.py (" + S + "lab3_vs_engine.py): 885.85, 2,445.52, 54.68, 787, -4,808.83, 13,800.44; 2.76 times the mean; 39.35 percent; 0.73 standard errors (40.15 / 54.68)."),
    dict(id="proj-two-root-witness", check="2.4-math: the two-root flow and its interpretation",
         location=f"{PROJ} line 374 (Lab 3 interpretation); tests/labs/CF1/lab-CF1-project-3.py", status="PASS",
         evidence="reference.irr_roots([-100, 230, -132]) returns [0.1, 0.2] (round-6 run, close_roots.py); the NPV is positive between the roots (NPV(0.15) = 0.19 dollars) and negative outside (NPV(0) = -2, NPV(0.3) = -1.2) as the interpretation says."),
    dict(id="proj-lessons-cross-ref", check="2.7 cross-references: lesson and remark citations in the page",
         location=f"{PROJ} line 431 (Exemplar B, 3 IRR and payback: 'Lesson 4, Remark 4.3'); course/modules/CF/CF1/L04.html line 139", status="PASS",
         evidence="Fresh in round 6 (line 431 changed this round): L04.html line 139 is 'Remark 4.3 (scale)': the IRR does not register the extra 100,000 USD of outlay, the NPV does. Lesson 4 covers the NPV-IRR ranking conflict (L04 section 4, Theorem 4.1). The 'one sign change bounds the IRRs at one' statement is flagged in the page as not proved."),
    dict(id="proj-irr-close-roots-missed", check="2.6-spec / claim vs implementation: close roots, 1e-7 claim",
         location=f"{PROJ} line 207 (changed); reference.py lines 97-101 and 107-115", status="PASS",
         evidence="Witness run in round 6 (" + S + "close_roots.py, reference.irr_roots): flows [0.825696, -1.817356, 1.0] (roots 0.1 and 0.101) return []; flows for roots 0.1 and 0.11 return [0.10000000000003, 0.10999999999996]; 0.1 and 0.102 both return (within the grid's resolution). Grid step factor 1.0046158 (page: 1.0046). The page's 'missed' claim holds for the reference grid; close-root behaviour is disclaimed in line 192 and is not tested."),
    dict(id="proj-irr-grid-convention-unenforced", check="2.6-spec / ruling (a),(b): the 4,001-point log grid and its close-root behaviour",
         location=f"{PROJ} lines 192 and 207 (both changed this round)", status="PASS",
         evidence="Round-5 FAIL resolved by scoping: line 192 now says the conventions define every number 'except the IRR roots that lie closer together than one step of the search grid: there the grid decides, and the autograder does not test that case', and line 207 states the close-pair example 'from this grid'. The 40,001-point alternative (alt_r5_1) returns both close roots, which the page now permits; no test pins close pairs. The window part is not resolved (see proj-irr-window-unenforced)."),
    dict(id="proj-irr-window-unenforced", check="2.6-spec / ruling (a) mutation: the search window 0.0001 to 10000 (rates -0.9999 to 9999)",
         location=f"{PROJ} line 207 ('searches the discount factor x = 1/(1+r) over the interval from 0.0001 to 10000 ... only a sign change between two samples inside the window is reported'); {TEST} lines 163-180 and 155-160; mutant m36", status="FAIL",
         evidence="Lower bound, narrowing side: m32 (_X_LOW = 1e-3) is now KILLED on all 50 seeds by the new test test_irr_finds_a_root_at_the_low_end_of_the_discount_factor_window (run_variants_r6.py: 50 of 50 failing). Lower bound, extension side: m36 (_X_LOW = 1e-6) SURVIVES on all 50 seeds (run_variants_r6.py: 0 of 50 failing; mutate_graders seed 0: SURVIVED). Witness: irr_roots([-1.0, 1e5]) returns [] on reference and [99999.00000000001] on m36, a root outside the specified window that the page says is not reported. No test checks a root below x = 1e-4. The upper-bound extension is killed by test_irr_does_not_report_a_zero_at_the_high_end_of_the_window (not separately mutated).",
         fix="Add a grader test (e.g. irr_roots([-1.0, 1e5]) == [] with x = 1e-5 outside the window, plus the matching sentence 'a root below discount factor 0.0001 is not reported'), or remove the claim that the conventions define every number returned (line 192) for roots outside the window. Then re-run mutate_graders so m36 is killed."),
    dict(id="proj-tolerance-relative-only", check="2.9 prose / 2.6-spec: the stated tolerance equals the one the tests apply",
         location=f"{PROJ} line 210 ('NPVs and flows are compared to a relative 1e-9'); {TEST} lines 305, 321, 330, 344, 364, 476 (absolute=1e-6) and close() default absolute=1e-9 (line 62)", status="FAIL",
         evidence="Six flow tests accept an absolute error up to 1e-6 cents besides the relative 1e-9 (e.g. test_depreciation_shield... line 305: close(flows[t], expected, rel=1e-9, absolute=1e-6)); the NPV default is relative 1e-9 with an absolute floor of 1e-9. The page states relative 1e-9 only, so it claims a tolerance stricter than the one enforced (ruling (a): a requirement the tests do not enforce must not be claimed). Fisher uses rel 1e-12 with absolute 1e-12 (line 264, 285).",
         fix="In line 210, state the tolerances the tests apply: relative 1e-9 with an absolute floor of 1e-9 cents for NPVs, and relative 1e-9 with an absolute floor of 1e-6 cents for flows; or tighten the six tests (grader change, a separate decision)."),
    dict(id="proj-mutants-killed", check="2.6-spec / mutation (project slice): every mutant killed",
         location=f"ledgers/CF1/mutants/m01..m40; {MUTATE}", status="FAIL",
         evidence="mutate_graders CF1 seeds 0-9: 'mutate_graders CF1: FAIL (39/40 killed)'. Sole survivor: m36_window_low_end_extended_to_one_millionth.py (see proj-irr-window-unenforced).",
         fix="Add the test in proj-irr-window-unenforced; re-run mutate_graders --unit CF1 --seeds 0-9 so that m36 is killed."),
    dict(id="proj-ladder-skip-condition", check="2.9 prose / 2.7 cross-reference: rung 1 and 2 skip condition",
         location=f"{PROJ} line 42 (changed this round); course/modules/CF/CF1/index.html line 66 (placement section) and line 149 (ladder)", status="PASS",
         evidence="Fresh in round 6: line 42 'If you reach the placement bar on the module hub and answer both skill checks, you may skip them and go to rung 3, as the hub states.' The hub says 'Skip rungs 1 and 2 only if you reach the bar and answer both skill checks' (index.html line 66) and 'You skip them only by reaching the placement bar and answering both skill checks' (line 149). Consistent."),
    dict(id="proj-mypy-grader-gate", check="2.8 commands: mypy on grader and labs",
         location="plans/CF1-build-plan.md line 205; .venv/bin/mypy --no-incremental tests/labs/CF1 course/modules/CF/CF1/grader", status="PASS",
         evidence="Round 6: 'Success: no issues found in 13 source files'."),
    dict(id="proj-window-end-high-unenforced", check="2.6-spec / ruling (a): zero at the high end of the window is not reported",
         location=f"{PROJ} line 207; {TEST} lines 155-160; reference.py lines 111, 133-134; mutant m23", status="PASS",
         evidence="test_irr_does_not_report_a_zero_at_the_high_end_of_the_window passes on reference (73 passed); m23 (high-end zero reported) KILLED in " + MUTATE + "."),
    dict(id="proj-irr-window-high-end-cover", check="2.6-spec: window high end (x = 1e4) enforced", location=f"{TEST} lines 155-160; m23", status="PASS",
         evidence="m23 (high-end zero reported) KILLED; the high end of the window is enforced for the zero at exactly x = 1e4."),
    dict(id="proj-stdlib-and-no-instance-import-unenforced", check="2.6-spec / ruling (a): standard library only, no instance import",
         location=f"{PROJ} line 192; {TEST} test_engine_imports_only_the_standard_library (lines 520-532)", status="PASS",
         evidence="Fresh in round 6 (line 192 changed this round; the stdlib sentence is unchanged): the test runs on the reference (73 passed); sys.stdlib_module_names is the check; capbudget.py may not import instance.py (the test would count the import as non-stdlib)."),
    dict(id="proj-cards-c071-not-established", check="2.7-cards: card CF1-c071 against L05 section 4",
         location=f"{CARD} CF1-c071 (lines 521-528, changed this round); course/modules/CF/CF1/L05.html section 4 (evidence paragraph)", status="PASS",
         evidence="Card back: 'No. It states no finding from its registered source on corporate practice, Graham and Harvey (2001), and quotes no passage from that paper, so no share of firms and no ranking of methods is stated.' L05 section 4 (headed 'Where the canon breaks, and what firms use'; the card's basis 'Section 4' matches): 'Graham and Harvey (2001) is the registered source on corporate practice, under graham2001theory. This lesson states no finding from it. It quotes no passage from that paper...' Registry key graham2001theory is in references.json. Grade C: the card states no practice fact, and the L05 evidence table row for this question reads 'Open' with 'Not stated in this lesson'."),
    dict(id="cards-missing-grade-or-basis", check="2.7 cards: every card has a grade and a key or basis (plan section 12 rule)",
         location=f"{CARD} (100 cards); plans/CF1-build-plan.md line 240 ('Every card cites a key or names its basis')", status="FAIL",
         evidence="Every card has a valid grade (74 T, 26 C) and every C card has a basis or cite. But 55 cards have neither cite nor basis (e.g. CF1-c004, c009, c011, c015, c016, c017, c043, c055, c067, c080, c094). Some are theorem or definition statements, which BUILDER_RULES section 7 allows without a key; others rest on a worked example, a problem (R1, R2, R3, P2, P3) or a misconception, and the plan's sentence 'Every card cites a key or names its basis' requires a basis for them. The two rules disagree on this point.",
         fix="Architect ruling: either amend plan section 12 to the BUILDER_RULES section 7 rule (theorem and definition statements need no key or basis), or give each card that rests on an example, a problem or a misconception a basis naming it (e.g. 'Problem R3', 'Example 4.2')."),
    dict(id="cards-misconception-locator", check="2.7 cards: misconception cards point to the right misconception section",
         location=f"{CARD} CF1-c011, c014, c029, c032, c086; L01.html section 7; L02.html section 6; L06.html section 5", status="PASS",
         evidence="Round 6 re-read: c011 -> L01 section 7 first misconception (1,000 outlay, 600 + 600, NPV -83.33 at 20 percent); c014 -> L01 section 7 third misconception (loan rate); c029 -> L02 section 6 first misconception (750.00 shield); c032 -> L02 section 6 third misconception (-130.50, unrounded -130.4952); c086 -> L06 section 5 second misconception (band is not a confidence interval). All five match the current text."),
    dict(id="cards-numbers-in-lesson", check="2.7 cards: every card number appears in its lesson or lab output",
         location=f"{CARD} (100 cards) vs L01.html-L06.html text and the nine lab twin outputs", status="PASS",
         evidence="Scripts " + S + "scans_r6.py and " + S + "cards_arith.py: every number (ignoring 0-10 and 20, 30, 100) in every card back appears in the stripped lesson text of L01-L06 or in the outputs of the nine twins: 0 missing."),
    dict(id="cards-arithmetic-recomputed", check="2.4 cards: arithmetic recomputed independently",
         location=f"{CARD} CF1-c009, c011, c013, c016, c017, c032, c043, c046, c058, c060, c081, c082, c083, c094, c097", status="PASS",
         evidence="Recomputed with fractions/floats (" + S + "cards_arith.py): c009 exact 13,452.6152 and NPV 3,452.6152 -> 3,452.62; c011 -83.33; c016 -0.009434 and +0.019417; c017 difference (1+r)^-2 (10-120r) = 0 at r = 1/12; c032 PV -130.4952; c043 9.18 percent vs 9 percent; c046 30,900,000 and 33,765,264.30; c058 -680.27; c060 189.04; c081 z = 0.625; c082 1.0008; c083 SE 0.00102; c094 27,272.73 and 18,181.82; c097 385,535.69 equals the PV of A's years 4 to 6."),
    dict(id="cards-lab-derived-numbers", check="2.2 cards: numbers taken from labs (SIMULATED)",
         location=f"{CARD} CF1-c010, c013, c027, c041, c042, c045, c056, c068-c070, c074, c081-c083, c097, c098", status="PASS",
         evidence="Each number matches the twin output run in round 6 (/tmp/cf1-v/d/r6/labs/*/out.txt): e.g. L01 -46.94 at 20 percent; L02 534.24 and -1,465.76; L03 113,637.49 at 3 percent and 161,465.80; L04 A 30 percent vs B 25 percent; L05 2.750, 3.469, 289,367.40, -132,231.40, 385,535.69, 121,251.71 to 693,692.91; L06 79,216.82, 79,078.68, 49,419.62, 0.0552. Each card is graded C and names its lab as the basis."),
    dict(id="cards-prose-garbled-c067", check="2.9 prose: card CF1-c067 reads correctly",
         location=f"{CARD} CF1-c067; L05.html problem R2 (Research)", status="PASS",
         evidence="Round 6 re-read: front 'For conventional flows within a horizon of N years, when is the discounted payback reached by year N?' back 'If and only if the NPV at the rate r is zero or more. ...' matches R2's proved statement (Research problem R2 solution: D_N = NPV(r); the two directions are proved)."),
    dict(id="cards-grade-semantics", check="2.3 grades: T grades for the 74 T cards are proved on the page",
         location=f"{CARD} grade fields (74 T, 26 C)", status="UNVERIFIABLE",
         evidence="Partial, structural check in round 6 (" + S + "t_card_proof_check.py): 40 T cards cite a Theorem, Proposition or Corollary label; each label exists in its lesson, its block carries class claim and data-grade T, and a proof block follows it (40/40, 0 missing, 0 without a proof). The other 34 T cards are definitions, worked examples, problem solutions (R2 proved; P2, P3, R1, R3) or misconceptions; their proofs were not all re-derived in this round. Honest gap: UNVERIFIABLE.",
         fix="A later round should re-derive the remaining T cards from their lesson proofs, examples and problem solutions, or downgrade any that the page does not prove."),
    dict(id="cards-count-vs-plan", check="2.7 cards: card count per lesson against plan section 12",
         location="plans/CF1-build-plan.md line 240 ('the planner expects four to six per lesson'); cards.json per-lesson counts L01 18, L02 16, L03 15, L04 20, L05 16, L06 15 (100 total)", status="FAIL",
         evidence="Re-counted this round: 100 cards, 15 to 20 per lesson, against the plan's four to six per lesson. BUILDER_RULES section 7 asks for one card per definition, theorem statement, key formula, key result and misconception, which gives more than six for these lessons. The plan's figure is the only stated expectation and it conflicts with BUILDER_RULES.",
         fix="Architect: either amend plan section 12 to the BUILDER_RULES card rule, or prune the cards to the plan's range."),
    dict(id="cards-duplicate-scan", check="2.7 cards: duplicate scan",
         location=f"{CARD}", status="PASS",
         evidence="Round 6 (" + S + "scans_r6.py): 0 duplicate ids; 0 duplicate fronts or backs; near-duplicate fronts (difflib ratio > 0.8): CF1-c017/c090, c028/c089, c049/c091 are different questions (rate of crossing vs which NPV is higher; tax credit vs working capital; first vs second part of the multiple-IRR problem)."),
    dict(id="cards-cite-keys-and-locators", check="2.1 cards: cited keys are in the registry",
         location=f"{CARD} CF1-c071 (graham2001theory), CF1-c084 (glasserman2003monte)", status="PASS",
         evidence="Round 6: every cite key in cards.json is in references/references.json (0 missing). c071 and c084 name the lesson section or remark that carries the locator (L05 section 4; L06 Remark 2.4) and state no result from the source."),
    dict(id="cards-changed-c071-c084", check="2.7 cards: changed cards c071 and c084 against the current lesson text",
         location=f"{CARD} CF1-c071 (lines 521-528) and CF1-c084 (lines 622 onward); L05.html section 4 and L06.html Remark 2.4", status="PASS",
         evidence="c071 verified against L05 section 4 (see proj-cards-c071-not-established). c084 back 'The lesson names the registered Monte Carlo text, Glasserman (2003), and states no result from it (Remark 2.4)': L06 Remark 2.4 says 'The registry records Glasserman (2003), Monte Carlo Methods in Financial Engineering' and no result from it is stated."),
    dict(id="cards-changed-c014-c037-c047-c057", check="2.7 cards: cards whose lesson passages moved this round",
         location=f"{CARD} CF1-c014, c037, c047, c057; L01.html line 323, L03.html lines 242, 469 (wording only), L04.html Remark 5.1", status="PASS",
         evidence="c014 matches the changed L01 line 323 ('the proof of Proposition 4.1 does not apply') and Section 7 misconception 3 (read this round). c037 cites Theorem 2.2; the L03 change is 'as Theorem 2.2 states' (wording only), the card's claim is unchanged. c047 and c057: no lesson line in those cards changed; Remark 5.1 (terminal value zero at an IRR) is in L04 and unchanged."),
    dict(id="cards-changed-c016-c044-c051-c052", check="2.7 cards: cards whose lesson passages are unchanged or moved",
         location=f"{CARD} CF1-c016, c044, c051, c052; L01 Problem R3, L03 Theorem 2.3, L04 Theorem 2.1 and Corollary 2.2", status="PASS",
         evidence="Round 6 re-read: c016 (Problem R3 numbers -0.009434 and +0.019417, recomputed); c044 (Theorem 2.3 in L03 'as Theorem 2.3 states' wording, the card's claim: nominal flows at the real rate overstate, lab 377,346.63 vs 263,709.14); c051 and c052 (Theorem 2.1 exactly one IRR; Corollary 2.2 NPV sign relative to IRR) match L04."),
    dict(id="cards-c080-positive-variance-dropped", check="2.7 cards: CF1-c080 against the changed P2 solution (L06 line 352)",
         location=f"{CARD} CF1-c080 (front and back); L06.html Problem P2 (line 352, changed this round)", status="PASS",
         evidence="The P2 solution now says 'a common demand shock whose loadings are all non-zero and of one sign makes every pair of receipts positively correlated'. c080's back 'With N at least 2 and a positive variance, it raises it. Each covariance term has the sign of the correlation, and the expectation does not depend on correlation (Problem P2).' is consistent with the expansion Var(NPV) = sum v_t^2 sigma^2 + 2 sum_{s<t} v_s v_t Cov."),
    dict(id="cards-changed-c071-lesson-agreement", check="2.7 cards: lesson changes this round against the cards that cite those passages",
         location="L01 line 323; L02 lines 51, 148, 300; L03 lines 242, 469; L04 line 312; L05 lines 70, 217, 233, 243, 296, 314-316, 374, 447; L06 lines 72, 263, 327, 338, 352, 382-384", status="PASS",
         evidence="Each changed passage read in the current text (round 6, /tmp/cf1-v/d/r6/lesson_delta.diff). Cards depending on them: c002 and c014 (L01 323), c032 and c029 (L02 300, 51), c038-c040 and c044 (L03 242, 469), c052 (L04 312), c065, c072, c073 and c098 (L05 70, 217, 243, 316), c071 (L05 233, 374), c077, c083 and c086 (L06 72, 327, 338, 352), c080 (L06 352). No card number is changed by a wording edit, and every card still matches its lesson text."),
    dict(id="proj-lab2-docstring-claim", check="2.9 prose: Lab 2 twin docstring against the page blanks",
         location="tests/labs/CF1/lab-CF1-project-2.py lines 6-8 (changed this round); project.html lines 137-145", status="PASS",
         evidence="The twin's docstring now says the page blanks the three lines that assign tax, operating and working_capital (page lines 167-169 are exactly those three ___ lines); run_labs confirms every other page line equals the twin line."),
]

rows.append(dict(id="proj-tolerance-claim-note", check="2.9 prose: Fisher and Monte Carlo tolerance wording", location=f"{PROJ} line 210", status="PASS",
                 evidence="Fisher identity: close(..., rel=1e-12, absolute=1e-12) (test lines 264, 285) matches 'a relative 1e-12' up to the same absolute floor; the Monte Carlo three-SE check uses the sample standard deviation with n - 1 degrees of freedom divided by sqrt(n) (test lines 497-500), as line 210 states. The absolute floors for flows are recorded in proj-tolerance-relative-only (FAIL)."))

# Round-5 rows that no longer exist in the round-6 table are kept by id: check for any round-5 id missing here
missing = [rid for rid in R5 if rid not in {r["id"] for r in rows}]

mutants = []
for name in sorted(p.name for p in (ROOT / "ledgers/CF1/mutants").glob("m*.py")):
    text = (ROOT / "ledgers/CF1/mutants" / name).read_text(encoding="utf-8")
    doc = text.splitlines()[0].strip().strip('"')
    r5 = next((m for m in ROUND5["mutants"] if m["file"].endswith(name)), None)
    killed_by = None
    if name.startswith("m36"):
        killed_by = None
    elif name in ("m37_zero_samples_counted_as_sign_changes.py", "m38_bisection_absolute_tolerance_in_discount_factor.py",
                  "m39_discounted_payback_fraction_uses_undiscounted_flow.py", "m40_capex_float_accepted.py"):
        killed_by = {"m37": "test_irr_does_not_report_a_tangent_root (seed 0)", "m38": "test_irr_finds_roots_across_the_whole_search_window (seed 0)",
                     "m39": "test_discounted_payback_uses_discounted_flows (seed 0)", "m40": "test_invalid_project_raises_a_named_error[capex-float] (seed 0)"}[name[:3]]
    elif name.startswith("m32"):
        killed_by = "test_irr_finds_a_root_at_the_low_end_of_the_discount_factor_window (seed 0; all 50 seeds)"
    else:
        killed_by = r5["killed_by"] if r5 else None
    mutants.append({"file": MUT + name, "description": doc, "killed_by": killed_by})

fragment = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 6,
    "verifier": "Claude Haiku 5.5 (independent verifier, CF1-d round 6; did not build CF1; no shared context with builders or earlier verifiers)",
    "pin": "d57df1e (detached, /tmp/verify6-CF1-d)",
    "base": "00745fe (round-5 pin; previous fragment /tmp/fanout-frags/CF1-d.round5.json). Delta in slice: project.html lines 142-144, 192, 194, 207, 209-210, 227, 417, 431; grader/test_project.py (new test lines 174-181; message lines 503-505); tests/labs/CF1/lab-CF1-project-2.py docstring; cards.json CF1-c071 (back and basis); L01-L06 wording (context for cards).",
    "checkout": "/tmp/verify6-CF1-d",
    "scratch": "/tmp/cf1-v/d/r6",
    "verified_at": "2026-10-27",
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "glasserman2003monte: used_by is [M8]; CF1 cites it (project.html line 437; L06.html Remark 2.4; cards CF1-c084). Add CF1 with tools/add_reference.py or confirm the architect's ruling.",
        "damodaran2012investment: used_by is [CF4]; CF1 lists it in the project reading list (project.html line 461). Same action.",
    ],
    "freshness_flags": [],
    "notes": (
        "Commands run this round: check_projects, check_pages, check_dag (CF1 PASS); run_labs --unit CF1 (9/9); run_graders --unit CF1 --seeds 0-49 (50/50); "
        "pytest --collect-only for seeds 0-49 (73 each); mutate_graders --unit CF1 --seeds 0-9 (39/40, m36 survives); run_variants_r6.py over 16 alternative engines and m32, m36 (seeds 0-49); "
        "ruff check, ruff format --check, mypy --no-incremental on tests/labs/CF1 and grader; verify_refs --offline and --unit CF1 (live); page_smoke --unit CF1 --pages project (PASS); lab twins under python -I -W error. "
        "Not run: the full repository gate; pytest over tests/ beyond run_labs; any browser test beyond page_smoke. "
        "Not verified: the proofs of the 34 non-theorem T cards (row cards-grade-semantics). Hub index.html line 161 changed this round (outside this slice; not assessed). "
        "Hours are not judged on pace (architect ruling). The memo's 600-900 word target is not checked (a memo is a learner deliverable, not a page claim). "
        "Round-5 round-4 alternative alt2 fails by design (it breaks the log-x convention)."
    ),
    "summary": "CF1-d round 6: FAIL. Five new mutants (m36-m40); m36 (window extended at the low end) survives on all 50 seeds and is a FAIL row; the relative-only tolerance statement (line 210) and the card basis rule (plan line 240) are FAIL rows; the card count vs plan and the T-card grade check remain FAIL and UNVERIFIABLE. Round-5 FAILs on the m32 window narrowing and the close-root grid claim are resolved.",
}
out = ROOT / "ledgers/CF1/CF1-d.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("missing round-5 ids:", missing)
print("rows", len(rows), "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
print("validate:", ledger.validate(json.loads(out.read_text(encoding="utf-8")), "CF1-d"))
