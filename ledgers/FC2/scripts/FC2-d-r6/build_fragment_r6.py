"""Round 6 FC2-d fragment builder: writes ledgers/FC2/FC2-d.json in the verifier checkout.

Every row is a verdict the verifier reached by running the cited command or reading the cited locator in this
checkout (pin 9fd6aed). Rows carried from round 5 name the byte-identical subject they rest on.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
CARRY5 = "Carried from round 5 (course/modules/FC/FC2/project.html block byte-identical since 04626e9; line numbers +1 after line 335): "
S = "ledgers/FC2/scripts/FC2-d-r6/"

rows = []
MUTANTS = []
for line in (ROOT / "ledgers/FC2/scripts/FC2-d-r6/mutate_all_r6_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*?) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    killed_by = killed.strip() if status == "KILLED" else None
    MUTANTS.append({"id": fname[:-3], "description": desc.strip(), "killed_by": killed_by})


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


# ---- gates, re-run on 9fd6aed ----
row("fc2d-gate-check-projects", "tools/check_projects.py --all", "tools/check_projects.py", "PASS",
    S + "gate_check_projects.out: 'check_projects FC2: PASS', rc=0.")
row("fc2d-gate-check-pages", "tools/check_pages.py --all", "tools/check_pages.py", "PASS",
    S + "gate_check_pages.out: 'check_pages FC2: PASS', rc=0.")
row("fc2d-gate-check-dag", "tools/check_dag.py --all", "tools/check_dag.py", "PASS",
    S + "gate_check_dag.out: 'check_dag FC2: PASS', rc=0.")
row("fc2d-gate-run-labs", "tools/run_labs.py --unit FC2", "project labs lab-FC2-project-1..3", "PASS",
    S + "run_labs_r6.out: 'run_labs FC2: PASS (11/11)', rc=0.")
row("fc2d-gate-page-smoke", "tools/page_smoke.py --unit FC2", "course/modules/FC/FC2/project.html", "PASS",
    S + "page_smoke_r6.out: 'page_smoke modules/FC/FC2/project.html: PASS'; in-browser grader 'All 90 tests pass on seed 858040591'; 'page_smoke FC2: PASS', rc=0.")
row("fc2d-gate-run-graders", "tools/run_graders.py --unit FC2 --seeds 0-49", "course/modules/FC/FC2/grader", "PASS",
    S + "run_graders_r6.out: 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)', rc=0.")
row("fc2d-gate-ruff-mypy", "ruff check, ruff format --check, mypy --strict on FC2 grader and tests/labs/FC2", "course/modules/FC/FC2/grader/*.py", "PASS",
    S + "ruff_mypy_r6.out: 'All checks passed!', '15 files already formatted', 'Success: no issues found in 3 source files'. Scoped to FC2; the full-repo gate was not run.")
row("fc2d-gate-pytest", "pytest tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_memo_exemplars.py", "tests/", "PASS",
    S + "pytest_labs_r6.out (rc 0); " + S + "pytest_pagechecks_memo_r6.out (rc 0, 54 passed).")
row("fc2d-gate-verify-refs", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    S + "verify_refs_r6.out: 'offline integrity: 560 entries, 0 problems', rc=0. The live run was not repeated.")

# ---- grader: counts, seeds, starter, alternatives ----
row("fc2d-collect-count", "pytest --collect-only per seed vs the page count", "course/modules/FC/FC2/project.html:320 ('collects 90 checks')", "PASS",
    S + "count_out.txt: 'seed N collect: 90 tests collected' for all 50 seeds 0..49 (0 lines differ). The page states 90 (line 320), so the round-5 count of 87 is updated and matches.")
row("fc2d-seeds-84", "reference passes every seed in the window", "course/modules/FC/FC2/grader/test_project.py", "PASS",
    S + "run_graders_r6.out: reference 50/50 seeds pass under --assert=plain -W error; count_out.txt shows 90 collected on each seed.")
row("fc2d-starter-fails", "the suite fails on the starter", "course/modules/FC/FC2/grader/starter.py:19,24,29", "PASS",
    S + "count_out.txt last line: '82 failed, 8 passed' on starter.py as scanner.py, seed 0; each function raises NotImplementedError, as project.html line 297 states.")
row("fc2d-alternatives", "five alternative correct scanners and one new integer-only alternative pass", "ledgers/FC2/scripts/FC2-d-r5/alts/ and " + S + "alt6_integer_crossmul.py", "PASS",
    S + "alts_r6.out: alt1_integer_only, alt2_slope_test, alt3_decimal, alt4_validate_first, alt5_floor_half all pass seeds 0-19. " + S + "alt6_r6.out: alt6 (integer cross-multiplied parity and convexity, built by make_alt6.py from reference.py) passes seeds 0-49, 0 seeds with failures.")
row("fc2d-mutate-builder", "tools/mutate_graders.py --unit FC2 (seeds 0-9 and 0-49)", "ledgers/FC2/mutants/", "PASS",
    S + "mutate_all_r6_seeds0-9.out: 47/48 killed; mutate_all_r6_seeds0-49.out and mutate_all_r6_final.out: 47/48 killed. The one survivor, r5_d_explanation_direction_reversed, is ruled a non-finding in row fc2d-r5-mut-direction. Every other mutant is killed.")
row("fc2d-mut-v03", "existing mutant v03", "ledgers/FC2/mutants/v03_parity_gross_bankers_round.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_half_cent_gross_rounds_once_up (seed 0).")
row("fc2d-mut-v04", "existing mutant v04", "ledgers/FC2/mutants/v04_convexity_returns_one_based_index.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_convexity_matches_exhaustive_oracle_second_chain (seed 0).")
row("fc2d-mut-v05", "existing mutant v05", "ledgers/FC2/mutants/v05_convexity_findings_before_parity.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_findings_are_in_parity_then_convexity_order (seed 0).")
row("fc2d-mut-v06", "existing mutant v06", "ledgers/FC2/mutants/v06_gross_rounds_signed_gap_then_abs.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_negative_half_cent_gross_rounds_once_up_in_magnitude (seed 0).")
row("fc2d-mut-v01-boundary", "existing mutant v01 (net exactly zero)", "ledgers/FC2/mutants/v01_convexity_zero_net_kept.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_convexity_finding_with_net_exactly_zero_is_not_returned (seed 0). Boundary re-derived: chord 30, call 75, gross 45 = 3*(10+5), net 0.")
row("fc2d-mut-v02-labels", "existing mutant v02 (labels)", "ledgers/FC2/mutants/v02_parity_explanation_names_P1_only.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1).")
row("fc2d-r5-mut-swap-weights", "round-5 mutant r5_b", "ledgers/FC2/mutants/r5_b_swapped_chord_weights.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_unequal_grid_no_false_positive (seed 0).")
row("fc2d-r5-mut-skip-first", "round-5 mutant r5_c", "ledgers/FC2/mutants/r5_c_parity_loop_skips_first_strike.py", "PASS",
    S + "mutate_all_r6_final.out: KILLED by test_cost_is_charged_per_leg_not_once (seed 0).")
row("fc2d-r5-mut-direction", "round-5 mutant r5_d (explanation direction)", "ledgers/FC2/mutants/r5_d_explanation_direction_reversed.py; course/modules/FC/FC2/project.html:301", "PASS",
    "The mutant survives all seeds 0-49 (" + S + "mutate_all_r6_final.out). Ruling: project.html:301 requires the explanation to name the rule and the labels P1-P6 ('names the rule and the assumptions the finding depends on, by the labels'); it states nothing about the direction of the trade, so the mutant violates no stated behaviour. Not a FAIL under the ruling. The mutate tool's exit status is still non-zero because of this mutant; recorded as a builder note, not a defect.")
row("fc2d-r5-grader-exact-ties", "round-5 FAIL: float discount scanner survives (r5_a)", "course/modules/FC/FC2/grader/test_project.py:273-279 and 713-727", "PASS",
    "Round-5 FAIL is fixed. r5_a_float_discount_ties is now KILLED by test_parity_exact_tie_at_a_non_dyadic_discount_factor (seed 0) in " + S + "mutate_all_r6_final.out. The reference passes the new tests on seeds 0-49.")
row("fc2d-r6-new-tie-tests", "three new round-6 tests: non-dyadic exact ties", "course/modules/FC/FC2/grader/test_project.py:273-279, 713-727", "PASS",
    "Arithmetic re-derived: parity_gap_cents(0,0,0,25,580000): 0-0-(0-25*0.58)=14.5 exactly, rounds up to 15 (asserted 15); parity_gap_cents(0,29,0,25,580000): -14.5 ties toward +inf to -14 (asserted -14); scan of hand_chain([25],[0],[0],spot=0,df=580000) gives gross 15. Convexity tie (chord (50+51)/2=50.5, call 53, violation 2.5, rounds once up to 3; df 950000 not applied). Python float check: 25*0.58 = 14.499999999999998, so the test comment's claim that a float computation gives 14 holds. Reference passes all 50 seeds.")
row("fc2d-r6-alt6-overconstraint", "over-constraint check with an independent integer algorithm", S + "alt6_integer_crossmul.py", "PASS",
    "alt6 uses integer cross-multiplication, no Fraction, and passes all 90 checks on seeds 0-49 (" + S + "alt6_r6.out).")
row("fc2d-r6-mut-new", "three new student-error mutants r6_a, r6_b, r6_c", "ledgers/FC2/mutants/r6_a_ties_away_from_zero_on_negative_gap.py; r6_b_convexity_strike_is_left_neighbour.py; r6_c_zero_fee_rejected.py", "PASS",
    S + "mutate_all_r6_final.out: r6_a KILLED by test_parity_negative_tie_of_one_half_goes_toward_plus_infinity (seed 0); r6_b KILLED by test_scan_matches_exhaustive_oracle_second_chain (seed 0); r6_c KILLED by test_strictly_increasing_strikes_are_accepted (seed 0). Each is a one-line difference from the reference; generator " + S + "make_r6_mutants.py.")

# ---- grader files carried or re-verified ----
row("fc2d-grader-stdlib", "standard library only; no grader import in the module", "course/modules/FC/FC2/grader/instance.py, reference.py, test_project.py", "PASS",
    "The round-6 diff adds only test functions (no new import). test_module_imports_standard_library_only passes on the reference in the full suite run (" + S + "run_graders_r6.out); mypy --strict clean (" + S + "ruff_mypy_r6.out).")
row("fc2d-grader-messages", "named error messages and ValueError only for named conditions",
    "course/modules/FC/FC2/grader/test_project.py (message tests, round-5 locations 534-553 and 427-502, now +8 lines)", "PASS",
    CARRY5 + "the message tests are byte-identical in the round-6 diff, which adds only three tests at 273-279 and 713-727. Messages match project.html:311-314 and reference.py:24-47; the suite passes on the reference.")
row("fc2d-grader-instance-validity", "instances are valid under L05 Theorem 2.2", "course/modules/FC/FC2/grader/instance.py:46-59, 102, 109-110", "PASS",
    "Carried from round 5 (instance.py byte-identical since 04626e9; run_graders_r6.out re-runs the instance generator on seeds 0-49 with all tests passing).")
row("fc2d-grader-instance-diversity", "instances differ across seeds and match the docstring ranges", "course/modules/FC/FC2/grader/instance.py:6-9, 74-80", "PASS",
    "Carried from round 5 (instance.py byte-identical since 04626e9); run_graders_r6.out: 50/50 seeds pass, with distinct per-seed chains.")
row("fc2d-lab1", "lab-FC2-project-1 (code, expected block, hypothesis, interpretation)", "course/modules/FC/FC2/project.html lab-FC2-project-1; tests/labs/FC2/lab-FC2-project-1.py", "PASS",
    CARRY5 + "the lab code, expected block and hypothesis line 55 are unchanged; run_labs_r6.out 11/11 PASS; twin run alone: " + S + "twin_p1.out, rc 0, stderr 0 bytes.")
row("fc2d-lab2", "lab-FC2-project-2 (blanks, expected block)", "course/modules/FC/FC2/project.html lab-FC2-project-2; tests/labs/FC2/lab-FC2-project-2.py", "PASS",
    CARRY5 + "blank lines and expected block unchanged; run_labs_r6.out 11/11; twin run alone rc 0 (" + S + "twin_p2.out).")
row("fc2d-lab3", "lab-FC2-project-3 (hypothesis, expected block, interpretation)", "course/modules/FC/FC2/project.html lab-FC2-project-3; tests/labs/FC2/lab-FC2-project-3.py", "PASS",
    CARRY5 + "unchanged; run_labs_r6.out 11/11; twin run alone rc 0 (" + S + "twin_p3.out).")
row("fc2d-lab-twins-pure", "twins alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS",
    "Each twin run as python -I -W error: rc 0, stderr 0 bytes (" + S + "twin_p1.err, twin_p2.err, twin_p3.err all empty).")
row("fc2d-rubric-observable", "every rubric descriptor observable", "course/modules/FC/FC2/project.html rubric table (round-5 lines 503-514, now 504-515)", "PASS",
    CARRY5 + "rubric table content unchanged; C4 row at line 511 matches.")
row("fc2d-rubric-calib-A", "exemplar A calibration", "course/modules/FC/FC2/project.html article#exemplar-a (round-5 lines 583-633, now 584-634)", "PASS",
    CARRY5 + "exemplar A annotations and data-scores unchanged.")
row("fc2d-rubric-calib-B", "exemplar B calibration", "course/modules/FC/FC2/project.html article#exemplar-b", "PASS",
    CARRY5 + "exemplar B annotations and data-scores unchanged.")
row("fc2d-exemplar-numbers", "exemplar numbers re-derived", "course/modules/FC/FC2/project.html exemplar-a and exemplar-b blocks", "PASS",
    CARRY5 + "the exemplar numbers (226, 540, 63, 3, 60, 6175, 6650) are unchanged; they re-derive from the unchanged lab output.")
row("fc2d-exemplar-annotations", "exemplar annotations cite passage text", "course/modules/FC/FC2/project.html annotation blocks", "PASS",
    CARRY5 + "annotation text unchanged.")
row("fc2d-spec-explanation-labels", "explanation labels P1-P6 match the spec", "course/modules/FC/FC2/project.html:301; grader/test_project.py PARITY_LABELS, CONVEXITY_LABELS; grader/reference.py:79-99", "PASS",
    "project.html:301 lists P1,P2,P3,P4,P6 (parity) and P1,P2,P5,P6 (convexity); reference.py _explain_parity and _explain_convexity name exactly those sets (verified by the suite run in " + S + "run_graders_r6.out).")
row("fc2d-spec-errors-scope", "named errors and scope of ValueError", "course/modules/FC/FC2/project.html:306-316", "PASS",
    "Four named conditions and messages at project.html:306-316 match reference.py _check_* and the suite; 'Any other invalid input may raise any exception' (line 316) is respected.")
row("fc2d-hours", "hours split sums to the figure", "course/modules/FC/FC2/project.html #hours table; course/modules/FC/FC2/index.html:29, 41, 133", "PASS",
    "Project components 2+3+5+9+3+5+3 = 30 (page total 30). Hub: data-hours-lessons=60, data-hours-project=30, '60 h lessons · 30 h project (33.3% of the 90 module hours)'; 60+30 = 90.")
row("fc2d-cards-sample", "every card read, sampled numeric and grade checks", "course/modules/FC/FC2/cards.json (143 cards)", "PASS",
    "All 143 cards read in this round against their lessons. Numbers re-derived by hand: c023 (3000..7500 payoffs), c024 (73.42), c027 (237.11 with the unrounded fair price, 237.108), c046/c134 labs, c097 (25/4), c098 (56.25 and 36), c098, c109-c118 (BS and tree values, d1/d2, u,d,R,q), c125 (37 halvings, 10/2^36 = 1.46e-10), c126, c131, c136-c137, c138 (state prices -1/5, 11/10), c009 (9/10 < q < 27/10 for payoffs (3,1)), c075 (0, 100, 800 cents from lab output at synthetic strikes). Lesson text checked for the cited Theorem, Proposition, Remark and Lab references (" + S + "cards_check_r6.out). Counterexample: none beyond the dup and grade rows below.")
row("fc2d-cards-dups", "no duplicate cards (exact, near, and substantive)", "course/modules/FC/FC2/cards.json FC2-c064 and FC2-c145", "FAIL",
    "No exact duplicate id or front (" + S + "cards_check_r6.out: unique ids True, unique fronts True; difflib ratio >= 0.80 pairs: 0). But FC2-c145 ('Does put-call parity hold only for at-the-money options?', back: 'No. Theorem 1.2 holds for every strike K > 0, and its proof uses no property of the strike') repeats the fact of FC2-c064 ('Under A1 to A5, does put-call parity hold for every strike?', back: 'Yes: C − P = S − e^{−rτ}K for every strike K > 0 (Theorem 1.2)...'). Same theorem, same strike claim, same proof point. Under VERIFIER_RULES rule 10 and the no-duplicate-cards rule this is a duplicate card.",
    "Delete FC2-c145 from course/modules/FC/FC2/cards.json (FC2-c064 already tests the same fact), or replace it with a card on a fact that is not already on the card list.")
row("fc2d-cards-numbers", "every card number appears in its lesson", "course/modules/FC/FC2/cards.json", "PASS",
    "cards_check_r6.out: decimals on card faces all appear in their lesson text; integers 2+ digits all appear in the lesson or project text, except the basis locator '302' in FC2-c049 basis ('L03.html line 302'). The basis field is internal metadata: no js file reads 'basis' (grep of course/assets/js), and check_pages.py:392 reads it only as a grounding string. Not a learner-facing number. Noted, not a FAIL.")
row("fc2d-cards-grades", "grades agree with BLUEPRINT (conventions C with basis)", "course/modules/FC/FC2/cards.json FC2-c049; L03.html:302, A8′ at L03.html:66, Definition 1.2 at L03.html:61", "PASS",
    "Round-5 FAIL fixed: FC2-c049 is now grade C with basis 'Lesson 3, model convention (L03.html line 302; A8′, Definition 1.2)'. L03.html:302 reads 'In the model of this lesson the position costs nothing to enter, and the only cash flows are the daily variation margins of Definition 1.2.' Locators verified. FC2-c145 is grade T and its claim is stated at L05.html:64 and L05.html:325.")
row("fc2d-cards-ids", "unique ids and prefixes", "course/modules/FC/FC2/cards.json", "PASS",
    S + "cards_check_r6.out: cards: 143, unique ids True. Gaps c031 and c077 are absent (cosmetic, not a rule breach); FC2-c145 extends the sequence.")
row("fc2d-cards-c132", "card c132 against Remark 4.2", "course/modules/FC/FC2/cards.json FC2-c132; course/modules/FC/FC2/L05.html Remark 4.2", "PASS",
    CARRY5.replace("project.html block", "cards.json entry") + "FC2-c132 is unchanged and matches Remark 4.2 (as round 5 verified).")
row("fc2d-reading-theorem-locator", "reading list theorem locators", "course/modules/FC/FC2/project.html #reading; course/modules/FC/FC2/L05.html:63, :115", "PASS",
    "Carried from round 5 (L05.html byte-identical in the cited lines: Theorem 1.2 at L05.html:63, Theorem 3.2 at L05.html:115, both re-read this round).")
row("fc2d-references-no-locator", "reading list cites registry keys with no locator", "course/modules/FC/FC2/project.html #reading and data-cite (round-5 lines 650-658, now +1)", "PASS",
    CARRY5 + "only hull2021options, stoll1969relationship, cox1979option; verify_refs_r6.out 0 problems.")
row("fc2d-notation", "symbols vs notation/notation.json", "course/modules/FC/FC2/project.html (C, P, S, K, df, D, P1..P6, R_f); notation/notation.json", "PASS",
    "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q (and macros \\Prob for the probability measure). The new line 335 uses C, P, S, K, df and D as in L05.html:59 (D = e^{-r tau}). R_f and Q keep their registry meanings in FC2. Plain P (put price) is not \\Prob, and the page states the labels P1-P6 are not the put price (line 335). No collision.")
row("fc2d-simulated-label", "every chain labelled SIMULATED", "course/modules/FC/FC2/project.html:35, 37, 285-289; grader/instance.py:119", "PASS",
    CARRY5 + "labels unchanged; instance label 'SIMULATED' at instance.py:119 unchanged.")
row("fc2d-process-banned", "no process words in learner text", "course/modules/FC/FC2/project.html, cards.json, grader/*.py", "PASS",
    "Regex (builder, verifier, ledger, fragment, TODO, placeholder, round N, pinned, this build, agent, reviewer, verification, fixture, mock) over project.html and cards.json: no hits. Grader code hits are identifiers only ('CaptureFixture' in test_project.py:171), not learner text.")
row("fc2d-ladder-claims", "ladder rungs match the labs", "course/modules/FC/FC2/project.html #ladder (round-5 lines 41-50)", "PASS",
    CARRY5 + "ladder unchanged.")
row("fc2d-curriculum-scope", "scope vs curriculum brief", "curriculum/02-economics-finance-core.yaml:425-431; project.html:37, 285", "PASS",
    "Carried from round 5 (curriculum yaml and project.html:37, 285 byte-identical in the cited lines). The SIMULATED chain choice is the recorded honest-pending choice (plans/FC2-open-items.md).")
row("fc2d-no-external", "no external requests from the project page or grader", "course/modules/FC/FC2/project.html; grader/*.py", "PASS",
    "grep -c http course/modules/FC/FC2/project.html = 0; page_smoke_r6.out reports the project page PASS (zero external requests).")
row("fc2d-new-tests", "boundary tests from round 5 (convexity, net zero, half-cent gross)", "course/modules/FC/FC2/grader/test_project.py (round-5 lines 370-381, 656-683, 698-737)", "PASS",
    "Carried from round 5 for the round-5 tests (content byte-identical in the round-6 diff, which only inserts two blocks at 273-279 and 713-727). Suite passes on the reference (run_graders_r6.out).")
row("fc2d-lab1-hypothesis-terms", "round-4 FAIL: lab-1 hypothesis terms defined in P6", "course/modules/FC/FC2/project.html:55 and :333", "PASS",
    "Carried from round 5: P6 at project.html:333 defines the fee and the half-spread; line 55 is unchanged.")

# ---- round-6 project text ----
row("fc2d-r6-project-line335", "new conventions paragraph (C, P, S, K, df; model-free and model-dependent)", "course/modules/FC/FC2/project.html:335", "PASS",
    "Re-read this round. 'model-free' is defined at line 335 before its use in the rubric (line 495, C4 at lines 511 and 549-554). The parity finding uses P4 (model-dependent) and the convexity finding uses P1, P2, P5 (model-free), as the grader's labels (test_project.py:40-41) and reference.py say. df = df_ppm / 1,000,000 matches L05.html:59 (D = e^{-r tau}).")

notes = (
    "Round 6 on pin 9fd6aed (round-5 pin 04626e9). Delta: FC2 project.html (one count changed 87->90 at line 320, one paragraph added at 335), grader/test_project.py (three tests added: 273-279, 713-727), cards.json (FC2-c030 text, FC2-c049 grade and basis, FC2-c145 added), L01-L06 and index.html text edits (FC2 lessons are not this slice; the cards were checked against the current lesson text). Round-5 FAILs: fc2d-r5-grader-exact-ties is FIXED (r5_a now killed); fc2d-cards-grades is FIXED (c049 now C with basis). New FAIL: fc2d-cards-dups (FC2-c145 repeats FC2-c064). Mutants: 48 listed (45 from round 5 and 3 new, r6_a..c); 47 killed; r5_d survives and is a recorded non-finding by ruling. The mutate tool exits non-zero because of r5_d. Not run: the full repo gate, verify_refs live run, a browser self-assessment form check, mypy on test_project.py (it imports scanner, which is not present in the checkout)."
)

fragment = {
    "unit": "FC2",
    "slice": "FC2-d",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 6 (did not build FC2)",
    "pin": "9fd6aed",
    "base": "04626e9 (round-5 pin); the delta is listed in notes; carries are marked",
    "checkout": str(ROOT),
    "scratch": "/tmp/fc2d-r6-* (per-seed suite copies, alt6 copy, count and twin scratch; removed after each run)",
    "verified_at": "2026-10-29T06:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": MUTANTS,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "FC2-d round 6: verdict FAIL. One non-PASS row: fc2d-cards-dups (FC2-c145 repeats FC2-c064). Round-5 FAILs fc2d-r5-grader-exact-ties and fc2d-cards-grades are fixed. The mutant survivor r5_d is recorded as a ruled non-finding."
}

json_path = ROOT / "ledgers/FC2/FC2-d.json"
json_path.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"rows": len(rows), "mutants": len(MUTANTS), "path": str(json_path)}))
