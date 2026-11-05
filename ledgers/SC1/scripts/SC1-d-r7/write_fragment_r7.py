"""Round 7 (SC1-d): write the slice fragment ledgers/SC1/SC1-d.json from the round-7 evidence in out/.

Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-d-r7/write_fragment_r7.py
Carried rows keep their round-6 ids; a carried PASS row is prefixed with the round it was carried from and the files
it depends on, which are byte-identical since the round-6 pin (4bd8cb9).
"""
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/SC1/scripts/SC1-d-r7/out"
R6 = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-d.round6.json").read_text(encoding="utf-8"))
r6_rows = {r["id"]: r for r in R6["rows"]}

CARRY = "Carried from round 6 (grader/reference.py, grader/instance.py, grader/starter.py, tests/labs/SC1/, project.html lines cited byte-identical since 4bd8cb9):"
REVER = "Re-verified round 7."

# Round-6 row id -> (round-7 status, check, location, evidence, fix)
# Only rows whose subject changed, or that a round-7 command re-ran, are marked re-verified. The rest are carried.
ROW7 = {
    "SC1-d-ladder": ("PASS", "2.6-ladder", "course/modules/SC/SC1/project.html:40-49, 155, 297-300, 602-609",
                     CARRY + " rungs 1-4 present; rung 1 solved and annotated (:44, :55-160); rung 2 graded by the lab-completion class (:45, :164); rung 3 covers the three proofs and the engine (:46); rung 4 open-ended (:47, :608-615)."),
    "SC1-d-grading-mode": ("PASS", "2.6-grading", "course/modules/SC/SC1/project.html:225; curriculum/03-markets.yaml:532",
                           REVER + " project.html:225 states 132 tests; `pytest --collect-only -q` on a scratch copy of grader/ prints '132 tests collected' (ledgers/SC1/scripts/SC1-d-r7/out/collect_test_project_r7.txt); grading is 'both' per the plan."),
    "SC1-d-spec-signatures": ("PASS", "2.6-spec", "course/modules/SC/SC1/project.html:221 vs grader/starter.py:16-36",
                              CARRY + " the five signatures in project.html:221 equal starter.py:16, 21, 26, 31, 36 (names, parameter types, return types)."),
    "SC1-d-spec-rounding-statement": ("PASS", "2.2-numbers / 2.9-prose", "course/modules/SC/SC1/project.html:223 vs labs at :154-160, :206-208, :418-428",
                                      CARRY + " every printed decimal in the three labs is :.6f or :.2e from the unrounded value (page_vs_twin.py output)."),
    "SC1-d-hours": ("PASS", "2.6-hours", "course/modules/SC/SC1/project.html:33, 274-280; course/modules/SC/SC1/index.html:29",
                    CARRY + " hours 2+3+10+8+3+2 = 28 (:274-280); hub data-hours-project=28, data-hours-lessons=72. My own estimate for a competent student is 22-32 h, inside the 30% band (plan 5.3 rows are plausible)."),
    "SC1-d-spec-grid-table": ("PASS", "2.6-spec", "course/modules/SC/SC1/project.html:213-265, 433-445",
                              REVER + " the spec, conventions and brief were read in full; the changed lines (:217, :235, :242, :245) match the engine and the labs; every constraint in :222-223 is reflected in grader/test_project.py."),
    "SC1-d-spec-tolerance-statement": ("PASS", "2.6-spec", "course/modules/SC/SC1/project.html:234, 238; grader/test_project.py:75-84 (simulation_band), :145-153",
                                       CARRY + " :234 (reflection_tail 1e-10) matches test_project.py:147; :238 (5 se + 1/N) matches simulation_band at :81-84."),
    "SC1-d-ag-reference": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/reference.py; tools/run_graders.py",
                           REVER + " run_graders SC1 0-49: PASS (50/50); my sweep of reference.py over seeds 0-499 and 50-499: 450/450 (out/reference_sweep_50_499_r7.txt); seed 0 and seed 7 suites: 132 passed each."),
    "SC1-d-ag-starter": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/starter.py",
                         REVER + " starter.py: suite on seed 0 gives 128 failed, 4 passed (out/suite_starter_seed0_r7.txt); the 4 that pass do not call the engine (instance tests). Starter fails on seeds 0-2 (out/starter_sweep_0_2_r7.txt)."),
    "SC1-d-ag-instances": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/instance.py",
                          REVER + " 50/50 seeds valid, 49 distinct levels (>=45 required); 20 sampled seeds give 20 distinct (tail, one-step estimate, nested counts) rows (out/instances_r7.txt)."),
    "SC1-d-ag-count": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py; course/modules/SC/SC1/project.html:7, 225, 296",
                       REVER + " collect-only = 132 (out/collect_test_project_r7.txt) = the page count at :7, :225 and :296; page_smoke runs 132 in the browser (out/page_smoke_project_r7.txt)."),
    "SC1-d-ag-messages": ("FAIL", "2.6-autograder (failure messages never leak the answer)", "course/modules/SC/SC1/grader/test_project.py:243 and :252",
                          REVER + " With srw_terminal_count returning 0 the suite prints, on failure, 'Failed: #{S_n >= 1} must equal (2**n - #{S_n = 0}) / 2' (:243) and 'Failed: for odd n the endpoint count at level 1 is 2**(n-1)' (:252); the second is the expected value 2**40 of the n = 41 assertion. Probes: out/message_leak_probe_r7.txt, out/message_leak_probe_odd_r7.txt. project.html:223 states the counting methods, not these closed forms."),
    "SC1-d-ag-overconstraint": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py (test_one_step_draws_are_the_seeded_gaussians; the tie tests; test_srw_integers...)",
                                REVER + " every tested engine property is stated on project.html (:223, :225, :232-238); conforming alternatives 1,2,3,5,6,7,8,9 pass 50/50 (out/alternatives_sweep_0_49_r7.txt); the only rejected alternative is the Box-Muller one (see SC1-d-r7-alt4-ruling10)."),
    "SC1-d-ag-alternatives-ok": ("PASS", "2.6-autograder", "ledgers/SC1/scripts/SC1-d-r7/alternatives/ (alt1, alt2, alt3, alt5, alt6, alt7, alt8, alt9)",
                                 REVER + " each run through sweep_r7.py on the current suite, seeds 0-49: 50/50 each (out/alternatives_sweep_0_49_r7.txt)."),
    "SC1-d-ag-mutants-plan": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m01-m10",
                              REVER + " mutate_graders SC1 0-9: KILLED (out/mutate_graders_SC1_0-9_r7.txt)."),
    "SC1-d-ag-mutants-own": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m11-m15, m18, m19, m21",
                             REVER + " all KILLED in out/mutate_graders_SC1_0-9_r7.txt."),
    "SC1-d-ag-mutants-survivors": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m16, m17; course/modules/SC/SC1/grader/test_project.py",
                                   REVER + " m16 killed by test_fine_grid_of_zero_steps_raises_value_error, m17 by test_coarse_grid_of_zero_steps_raises_value_error (out/mutate_graders_SC1_0-9_r7.txt)."),
    "SC1-d-ag-mutants-seed": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m20", REVER + " m20 KILLED (out/mutate_graders_SC1_0-9_r7.txt)."),
    "SC1-d-ag-mutants-seed-offset": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m22_seed_offset_by_one.py",
                                     REVER + " m22 KILLED by test_one_step_draws_are_the_seeded_gaussians (seed 0)."),
    "SC1-d-ag-mutants-r3": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m23-m26", REVER + " all KILLED."),
    "SC1-d-ag-mutants-r4-new": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m27-m31", REVER + " all KILLED."),
    "SC1-d-ag-mutants-r5-new": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m32, m33, m34", REVER + " all KILLED."),
    "SC1-d-ag-page-smoke": ("PASS", "2.6-autograder", "course/modules/SC/SC1/project.html; tools/page_smoke.py --unit SC1 --pages project",
                            REVER + " out/page_smoke_project_r7.txt: 'in-browser grader: All 132 tests pass'; 'page_smoke modules/SC/SC1/project.html: PASS'; exit 0 with 'PASS' for the page (the console and external-request checks are enforced by the tool; its output lists only timings); labs 0.0-0.2 s."),
    "SC1-d-ag-docstring": ("FAIL", "2.6-autograder (docstring matches the tests)", "course/modules/SC/SC1/grader/test_project.py:19",
                           REVER + " the docstring says 'It never prints the expected value.' The messages at :243 and :252 print the closed form of the expected value (see SC1-d-ag-messages). Every other docstring claim checked (cross-checks at :11-12, pinned draws :13, the tie tests :14-15, band at :16-17) holds."),
    "SC1-d-rubric-observable": ("PASS", "2.9-prose", "course/modules/SC/SC1/project.html:446-457", CARRY + " every level descriptor names an observable element; no vague 'convincing' or 'some caveats' descriptor remains."),
    "SC1-d-calib-A": ("PASS", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:464-516 (exemplar A passages with the annotations hidden)",
                      REVER + " I scored exemplar A from its passages with the annotation asides removed: C1 1 (no numbered assumptions), C2 2 (P1 symmetry step skipped without a gap), C3 2 (decimals without rounding statement), C4 2 (sample presented as holding for every grid), C5 1 (words, no numbers): 1,2,2,2,1 = official scores in :466 and data-scores at :464. Within one level on every criterion."),
    "SC1-d-exemplarA-claim": ("PASS", "2.9-prose", "course/modules/SC/SC1/project.html:470, 474-475, 482, 499, 503-508, 512",
                              CARRY + " the checks paragraph (:482) quotes 0.0865, 1588, 0.0595, 0.0107, 0.0163, 0.0432 and 1.52: recomputed (out/recompute_numbers_r7.txt) to the printed digits."),
    "SC1-d-exemplarB-onestep-claim": ("PASS", "2.9-prose / 2.2-numbers", "course/modules/SC/SC1/project.html:558",
                                      CARRY + " 0.026948 = tail minus the 1-step estimate, 0.043248 = tail/2, -0.016300 and 1.52 SE (recomputed in out/recompute_numbers_r7.txt)."),
    "SC1-d-exemplarB-numbers": ("PASS", "2.2-numbers", "course/modules/SC/SC1/project.html:524, 546, 558 vs Lab 1 and Lab 3 output (:154-160, :418-428)",
                                CARRY + " every number matches the labs' printed output and the independent recomputation: 0.086497, 0.059548, 0.010735, 0.043248, 0.048142, 9.13e-15 (my Simpson sum gives 8.73e-15 by a different summation order; both are below 1e-14), SE list, nested 35/29/27/22 vs 40."),
    "SC1-d-exemplarB-proof": ("PASS", "2.4-proof / 2.9-prose", "course/modules/SC/SC1/project.html:582-595 (exemplar B appendix)",
                              REVER + " re-derived every step of P1 (stopping time of rho; A = {M_t >= a}; P(tau = t) = 0; freezing via A4(b) with Z=(t-rho, 1_A), Y=B~; the 1/2 from f-bar; P(A) = P(B_t>=a) + P(A)/2), P2 (the w = z/sqrt2 substitution) and P3 (limit of erfc(a/sqrt(2n))). No gap beyond the implicit attainment of the infimum tau in 'B_tau = a by continuity', which A4(c) covers."),
    "SC1-d-exemplarB-p1-assumptions": ("PASS", "2.9-prose / 2.4-proof", "course/modules/SC/SC1/project.html:246, 249, 583-584 vs L05.html A3, A4(b), A4(c), A4(g), A4(h); L01.html:58-63",
                                       REVER + " current L05.html lists A4(b) freezing, (c) hitting times, (g) joint measurability, (h) measurability at a stopping time; A3 is the strong Markov property for bounded stopping times (conclusion: standard BM independent of F_rho); L01 Definition 1.1 is D1-D2 (B_0 = 0, normal increments). All cited letters and items match."),
    "SC1-d-lab1-run": ("PASS", "2.5-labs", "course/modules/SC/SC1/project.html:55-160; tests/labs/SC1/lab-SC1-project-1.py",
                       REVER + " page code equals the twin; run under python -I -W error prints the expected block exactly (out/page_vs_twin.txt; run_labs 11/11)."),
    "SC1-d-lab1-docstring": ("PASS", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:58-68; tests/labs/SC1/lab-SC1-project-1.py:3-",
                             REVER + " docstring: four numbers drawn in the same order as grader/instance.py (same formulas); rounding statement matches the code (:.6f, :.2e); H and a printed as generated."),
    "SC1-d-lab2-run": ("PASS", "2.5-labs", "course/modules/SC/SC1/project.html:164-210; tests/labs/SC1/lab-SC1-project-2.py",
                       REVER + " twin completed; page is the twin with two ___ blanks (every page line equals its twin line or contains a blank); output 29/22/7/True matches :206-208."),
    "SC1-d-lab2-attribution": ("PASS", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:209 vs course/modules/SC/SC1/L06.html (Proposition 1.3, Corollary 1.4)",
                               REVER + " L06 Proposition 1.3 (discrete reflection identity) and Corollary 1.4 (#{M_N>=a} = #{S_N>=a} + #{S_N>a}) exist in the current L06.html; the statement at :209 cites them correctly; the engine tests every n up to 12."),
    "SC1-d-lab3-run": ("PASS", "2.5-labs", "course/modules/SC/SC1/project.html:303-430; tests/labs/SC1/lab-SC1-project-3.py",
                       REVER + " page code equals the twin; output equals the expected block (out/page_vs_twin.txt); recomputed with grader/reference.py (out/recompute_numbers_r7.txt): identical to the digit."),
    "SC1-d-lab3-onestep-interp": ("PASS", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:429 vs tests/labs/SC1/lab-SC1-project-3.py:99",
                                  REVER + " 0.001799 above the tail = 0.14 SE (0.001799/0.012870 = 0.140); one-step bias tail/2 = 0.043248; estimate error -0.016300 = 1.52 SE (0.016300/0.010735 = 1.518); SE range 0.009819-0.012870; coarse counts 35, 29, 27, 22 <= 40; 1588 of 4096 walks. All match the printed output."),
    "SC1-d-lab3-docstring": ("PASS", "2.5-labs / 2.9-prose", "tests/labs/SC1/lab-SC1-project-3.py:3-11 (page :306-317)",
                             CARRY + " the docstring describes path_maxima (N paths, n Gaussian increments of variance H/n, path by path, from random.Random(seed)) and the stride-based nested maxima; both match the code."),
    "SC1-d-labs-pytest": ("PASS", "2.5-labs / tooling", "tests/test_labs.py -k SC1; tests/test_run_labs.py; tests/test_page_checks.py",
                          REVER + " out/pytest_related_r7.txt: exit 0; out/pytest_memo_exemplars_r7.txt: 14 passed."),
    "SC1-d-calib-B": ("PASS", "2.9-prose / rubric scoring", "course/modules/SC/SC1/project.html:518-599 (exemplar B passages, annotations hidden)",
                      REVER + " scored from the passages with the annotations removed: C1 4 (A0, A3, A4(b,c,g,h) listed and tied to steps), C2 4 (each step justified; none skipped), C3 4 (decimals rounded once and stated; counts exact), C4 3 (sample and a.s. limits named; the continuum limit of the nested comparison not stated), C5 4 (all five grids with SE, direction from the nested inequality, separate paths). 4,4,4,3,4 = official :520 and data-scores. Within one level."),
    "SC1-d-statements": ("PASS", "2.6-spec / 2.4-proof", "course/modules/SC/SC1/project.html:241-262",
                         REVER + " P1, P2, P3 statements and assumption lists re-derived; the statements are correct (P1: 2P(B_t>a) = 2P(B_t>=a) uses A0's normal marginals; P2: erfc(a/sqrt(2t)) = 2(1 - Phi(a/sqrt t)); P3: {tau_a<=t} = {M_t>=a} and P(tau_a<inf) = 1 from P2)."),
    "SC1-d-A1-label": ("PASS", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:236-242, 577-580; course/modules/SC/SC1/L01.html:58-63; L02.html Theorem 2.5, Remark 2.6",
                       REVER + " project.html has no A1 label (A0 and A3/A4 only); A0 cites Definition 1.1 of Lesson 1 and continuous paths as in Theorem 2.5 and Remark 2.6 of Lesson 2; all present in the current lesson files."),
    "SC1-d-A3-A4-usage": ("PASS", "2.6-spec / attribution", "course/modules/SC/SC1/project.html:242, 246, 249; course/modules/SC/SC1/L05.html (Assumptions A3, A4)",
                          REVER + " A3 = strong Markov property for bounded stopping times (L05.html 'Assumption A3'); A4 items (a)-(h) at L05.html; the page uses (b), (c), (g), (h) for the steps stated, and each use matches the item text."),
    "SC1-d-dag": ("PASS", "2.9-DAG", "course/modules/SC/SC1/project.html; tools/check_dag.py --unit SC1",
                  REVER + " check_dag SC1: PASS (out/check_dag_SC1.txt). Only two concept links on the page (normal-distribution, stopping-time), both in the closure of SC1; SC1's own concept markov-property is named without a link."),
    "SC1-d-notation": ("PASS", "2.8-notation", "course/modules/SC/SC1/project.html passim; notation/notation.json",
                       REVER + " every registered macro used (\\Prob, \\Normal, \\indic, \\Phi) is in notation.json, and the other commands are standard TeX (operatorname, mathcal, tilde, tfrac, wedge); T is not used (H is the horizon, :230); \\Phi is the standard normal CDF as registered; N and n are local letters."),
    "SC1-d-define-before-use": ("PASS", "2.5-labs / 2.9-prose", "course/modules/SC/SC1/project.html:37, 45, 53, 57, 230",
                                CARRY + " grid maximum (:37), erfc and Phi (:53, :230), tau_a (:230), first-passage time deferred to the conventions (:217) with the forward reference marked."),
    "SC1-d-discretization-bias": ("PASS", "2.9-prose", "course/modules/SC/SC1/project.html:225, 229, 235",
                                 REVER + " discretization bias defined with dfn at :235; the 'never negative' claim holds (grid event is a subset of the continuous event on each path)."),
    "SC1-d-monte-carlo-term": ("PASS", "2.9-prose", "course/modules/SC/SC1/project.html:231-232, 235, 375-379",
                               REVER + " grep finds no 'Monte Carlo' on the page; estimates are described in plain words (simulation, standard error, sample)."),
    "SC1-d-scope-words": ("PASS", "2.9-prose", "course/modules/SC/SC1/project.html:217, 223, 231-238, 429, 455, 570",
                          REVER + " grep of every 'never/always/every/almost surely/exactly' on the page: each is a pathwise identity by construction, a proved statement under its assumptions, or a stated limit (:455, :570). No unsupported scope claim."),
    "SC1-d-process-words": ("PASS", "2.9-prose / 12", "course/modules/SC/SC1/project.html:619-622 (former round-4 location) and whole page",
                            REVER + " grep for build, builder, round (as a process word), verifier, REQUESTS, planner, fixer, architect, TODO, TBD and banned phrases: no hit. 'rounded' is the arithmetic word."),
    "SC1-d-banned-structure": ("PASS", "2.9-prose / structure", "course/modules/SC/SC1/project.html; tools/check_pages.py --unit SC1",
                               REVER + " check_pages SC1: PASS (out/check_pages_SC1.txt); check_projects SC1: PASS (out/check_projects_SC1.txt)."),
    "SC1-d-registry": ("PASS", "2.8-references", "course/modules/SC/SC1/project.html:619-622; references/references.json:20732",
                       REVER + " the reading list cites shreve2004stochastic at book level only; registry record title, author and year 2004 match; live check: verify_refs --unit SC1 '1 of 560 entries, 0 problems'; plain curl of openlibrary.org/books/OL51662040M.json returned HTTP 200 with title 'Stochastic Calculus for Finance II' and publish year 2004."),
    "SC1-d-privacy-claim": ("PASS", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:288, 603, 636",
                            CARRY + " code: course/assets/js/store.js:2 keeps workspace files in IndexedDB in the learner's browser; grader.js:53 derives the seed from the workspace ID. Live browser behaviour not run (see notes)."),
    "SC1-d-tools-gates": ("PASS", "tooling", "course/modules/SC/SC1/grader; tests/test_labs.py -k SC1 and related; references",
                          REVER + " see SC1-d-r7-gates-full."),
    "SC1-d-numbers-prose": ("PASS", "2.2-numbers", "course/modules/SC/SC1/project.html:57, 154-160, 209, 219, 225, 305-317, 418-429",
                            REVER + " every number in the prose (2.083, 2.474, 487, 0.086497, 0.059548, 0.010735, 0.043248, 0.048142, 0.016300, 1.52, 0.001799, 0.14, 1588, 794, 29, 22, 7, 132, 28) recomputed or read from the printed output (out/recompute_numbers_r7.txt; page_vs_twin.txt)."),
    "SC1-d-spec-n41-method": ("PASS", "2.6-spec / 2.6-autograder", "course/modules/SC/SC1/project.html:223; grader/reference.py:79-97; grader/test_project.py (n = 41 test)",
                              REVER + " reference computes both counts by math.comb and the reflection identity (no walk listing); the n = 41 test (only a = 1) passes. The must-not-list rule has no bounded test (see notes)."),
    "SC1-d-ag-draws-depend-overconstraint": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py (test_draws_depend_on_the_instance_seed, text byte-identical since 4bd8cb9)",
                                             CARRY + " the test passes on the reference for seeds 0-499 and is not over-constraining: alternatives 1-3, 5-9 change nothing it checks."),
    "SC1-d-ag-band-overconstraint": ("PASS", "2.6-autograder", "course/modules/SC/SC1/grader/test_project.py (simulation_band and the seeded band tests; text byte-identical since 4bd8cb9)",
                                     REVER + " the band tests pass on the reference for 500 seeds (out/reference_sweep_50_499_r7.txt) and for 8 conforming alternatives on 0-49; the band uses the target's SE, not the sample's."),
    "SC1-d-reading-disclosure": ("PASS", "2.9-prose / attribution", "course/modules/SC/SC1/project.html:619-622; course/modules/SC/SC1/index.html:183",
                                 CARRY + " reading list = shreve2004stochastic at book level, no locator; karatzas string absent from the project page (grep: 0 hits)."),
    "SC1-d-delta-r5-read": ("PASS", "2.9-prose / 2.6 (round-5 delta)", "course/modules/SC/SC1/project.html:217, 232, 233, 246, 249, 261, 466, 570, 583, 590, 619",
                            REVER + " the round-5 hunks are re-read at their current lines; the round-6 pin (4bd8cb9) carries them unchanged except the round-6 edits at :235, :242, :245 that are now read in full."),
    "SC1-d-ag-level-equality-survivors": ("PASS", "2.6-mutation", "course/modules/SC/SC1/grader/test_project.py:347-366, 444-452; ledgers/SC1/mutants/m35_grid_exceedance_strictly_above_level.py; m36_nested_counts_strictly_above_level.py",
                                          REVER + " the round-6 FAIL is fixed. m35 is KILLED by test_path_whose_maximum_equals_the_level_counts_as_reaching_it (seed 0) and m36 by test_nested_counts_include_a_path_whose_maximum_equals_the_level (seed 0) in out/mutate_graders_SC1_0-9_r7.txt. The reference passes both new tests on seeds 0-499."),
    "SC1-d-ag-mutants-r6-new": ("PASS", "2.6-mutation", "ledgers/SC1/mutants/m37_one_path_accepted_with_zero_error.py",
                                REVER + " m37 KILLED by test_one_path_raises_value_error (seed 0)."),
    "SC1-d-exemplar-naming": ("PASS", "2.9-prose (plan naming)", "course/modules/SC/SC1/project.html:464 (exemplar-a, data-level 2), :518 (exemplar-b, data-level 4); plans/SC1-build-plan.md section 5.4",
                              CARRY + " the plan's section 5.4 names exemplar-a at data-level 4 and exemplar-b at data-level 2; the page reverses the two. Recorded as a note, not a failing row (no learner-facing requirement depends on the names; both levels are present; calibration holds)."),
    "SC1-d-delta-r6-read": ("PASS", "2.9-prose / 2.6 (round-6 delta)", "course/modules/SC/SC1/project.html (hunks at :7, :217, :225, :235, :242, :245, :296); course/modules/SC/SC1/grader/test_project.py (insertions at :14-15, :341-368, :444-452); ledgers/SC1/mutants/m35-m37",
                              REVER + " the whole 4bd8cb9..06994db delta for this slice was read; each changed hunk is covered by a row in this fragment."),
}

NEW_ROWS = [
    {"id": "SC1-d-r7-mutants-new", "check": "2.6-mutation", "location": "ledgers/SC1/mutants/m38-m41; ledgers/SC1/scripts/SC1-d-r7/make_mutants_r7.py",
     "status": "PASS",
     "evidence": "Four new student-error mutants, each one textual change of reference.py (script asserts the target text occurs once): m38 boundary a < 0 (accepts a = 0), m39 standard error divided by sqrt(N-1), m40 Box-Muller draws instead of rng.gauss, m41 reflection tail as 2(1 - Phi(a/sqrt(2t))). tools/mutate_graders.py --unit SC1 --seeds 0-9 KILLED all four: m38 by test_reflection_tail_rejects_zero_level, m39 by test_standard_error_uses_divisor_n_minus_one, m40 by test_one_step_draws_are_the_seeded_gaussians, m41 by test_reflection_tail_is_the_erfc_closed_form (out/mutate_graders_SC1_0-9_r7.txt)."},
    {"id": "SC1-d-r7-mutants-all", "check": "2.6-mutation", "location": "ledgers/SC1/mutants/ (m01-m41)",
     "status": "PASS",
     "evidence": "mutate_graders SC1 0-9 re-run on the pin: 47 of 47 files KILLED = m01-m41 (41 slice mutants) + 6 lab-twin files SC1a-* (slice a; listed in the output, not counted here). out/mutate_graders_SC1_0-9_r7.txt, exit 0."},
    {"id": "SC1-d-r7-alternatives-sweep", "check": "2.6-autograder (five alternatives)", "location": "ledgers/SC1/scripts/SC1-d-r7/alternatives/*.py; sweep_r7.py",
     "status": "PASS",
     "evidence": "Eight conforming alternatives pass the current suite on seeds 0-49, 50/50 each: alt1 (NormalDist tail), alt2 (Simpson only), alt3 (DP srw counts), alt5 (cumulative-sum subsample), alt6 (Pascal row), alt7 (gauss step-major), alt8 (1 - erf), alt9 (closed-form SE). Alt4 (Box-Muller) fails 50/50 (4 tests) and is excluded as a stated-rule violation (FINAL-ARCHITECT-RULINGS 10). alt2b (enumeration at n = 41) is not run: it forbids the n = 41 listing that project.html:223 prohibits. out/alternatives_sweep_0_49_r7.txt."},
    {"id": "SC1-d-r7-reference-sweep-500", "check": "2.6-autograder", "location": "course/modules/SC/SC1/grader/reference.py",
     "status": "PASS",
     "evidence": "sweep_r7.py reference.py over seeds 0-499 (50-499 for the second run): 500/500 seeds pass the 132-test suite with -W error (out/reference_sweep_50_499_r7.txt; run_graders SC1 0-49 PASS in out/run_graders_SC1_0-49.txt)."},
    {"id": "SC1-d-r7-starter-fails", "check": "2.6-autograder", "location": "course/modules/SC/SC1/grader/starter.py",
     "status": "PASS",
     "evidence": "Suite on starter.py: 128 failed, 4 passed (seed 0, out/suite_starter_seed0_r7.txt); seeds 0-2 all fail (out/starter_sweep_0_2_r7.txt). The four passing tests are the instance tests that do not call the engine."},
    {"id": "SC1-d-r7-instances-sample", "check": "2.6-autograder (instances)", "location": "course/modules/SC/SC1/grader/instance.py; ledgers/SC1/scripts/SC1-d-r7/instances_r7.py",
     "status": "PASS",
     "evidence": "50/50 seeds valid (H>0, a>0, 4<=n_steps<=256, 400<=n_paths<=800, n_steps*n_paths<=200000, label SIMULATED); 49 distinct levels (>=45 required). Sample of 20 seeds (0,1,2,3,5,8,13,21,34,42,49,77,101,250,333,499,1000,2024,4096,9999): 20 distinct (tail, one-step estimate, nested-count) rows (out/instances_r7.txt)."},
    {"id": "SC1-d-r7-numbers-recompute", "check": "2.2-numbers / 2.4-math", "location": "course/modules/SC/SC1/project.html:154-160, 418-428, 524-558; ledgers/SC1/scripts/SC1-d-r7/recompute_numbers_r7.py",
     "status": "PASS",
     "evidence": "Independent recomputation through grader/reference.py and a fresh Simpson sum: tail 0.086497; one-step est 0.059548, SE 0.010735, est - tail/2 = 0.016300, 1.518 SE; grid 1/4/16/64/256 estimates and SEs and tail-minus-estimate (0.026948, 0.037215, 0.020788, -0.001799, 0.004361) all match; nested 40 vs 35/29/27/22; srw(12,3) 1588/794; srw(6,2) 29/22 and terminal>=3 7. Simpson difference: 8.73e-15 in my summation order vs 9.13e-15 printed by Lab 1 (round-off; both < 1e-14). out/recompute_numbers_r7.txt."},
    {"id": "SC1-d-r7-page-vs-twin", "check": "2.5-labs", "location": "course/modules/SC/SC1/project.html:55-210, 303-430; tests/labs/SC1/lab-SC1-project-{1,2,3}.py",
     "status": "PASS",
     "evidence": "ledgers/SC1/scripts/SC1-d-r7/page_vs_twin.py: lab 1 and lab 3 page code equals the twin byte for byte (after strip); lab 2 page equals the twin except the two ___ blanks; each twin under python -I -W error exits 0 and its stdout equals the page's expected block. out/page_vs_twin.txt: ALL OK."},
    {"id": "SC1-d-r7-gates-full", "check": "tooling (ruff, mypy, pytest, verify_refs, run_labs, check_*)", "location": "repository root; ledgers/SC1/scripts/SC1-d-r7/run_gates.sh",
     "status": "PASS",
     "evidence": "ruff check . : All checks passed (out/ruff_check_full_r7.txt); ruff format --check . : 553 files already formatted (out/ruff_format_full_r7.txt); mypy --no-incremental: no issues in 385 files (out/mypy_full_r7.txt); pytest tests/test_labs.py -k SC1 tests/test_run_labs.py tests/test_page_checks.py: exit 0 (out/pytest_related_r7.txt); pytest tests/test_memo_exemplars.py: 14 passed; run_labs SC1 11/11; check_pages SC1, check_dag SC1, check_projects SC1: PASS; run_graders SC1 0-49 PASS; verify_refs --offline (all): 560 entries, 0 problems."},
    {"id": "SC1-d-r7-registry-live", "check": "2.8-references", "location": "references/references.json:20732 (shreve2004stochastic)",
     "status": "PASS",
     "evidence": "verify_refs.py --unit SC1 (live): '1 of 560 entries, 0 problems' (out/verify_refs_live_SC1_r7.txt). Plain curl https://openlibrary.org/books/OL51662040M.json: HTTP 200, title 'Stochastic Calculus for Finance II', publish year 2004, ISBN 9781475742961 (matches the record)."},
    {"id": "SC1-d-r7-page-smoke", "check": "2.9-structure / 2.6-autograder", "location": "course/modules/SC/SC1/project.html",
     "status": "PASS",
     "evidence": "tools/page_smoke.py --unit SC1 --pages project: 'in-browser grader: All 132 tests pass'; labs run; 'page_smoke modules/SC/SC1/project.html: PASS' (out/page_smoke_project_r7.txt)."},
    {"id": "SC1-d-r7-alt4-ruling10", "check": "2.6-autograder (plan 5.7 item 4)", "location": "plans/SC1-build-plan.md section 5.7(4); plans/FINAL-ARCHITECT-RULINGS.md item 10; course/modules/SC/SC1/project.html:232",
     "status": "PASS",
     "evidence": "The plan asks for a Box-Muller alternative whose estimate differs from the reference. project.html:232 states the increments are random.Random(seed).gauss(0.0, sqrt(H/n_steps)) and the pinned test test_one_step_draws_are_the_seeded_gaussians checks that draw. Under ruling 10 a float alternative wrong on a stated exact rule is a mutant, not an alternative; it is now m40 and is killed. PASS with a note for the architect to confirm the exclusion."},
    {"id": "SC1-d-r7-delta-read", "check": "2.9-prose / 2.6 (round-7 delta)", "location": "git diff 4bd8cb94..06994db for course/modules/SC/SC1 grader, project.html, tests/labs/SC1, ledgers/SC1/mutants",
     "status": "PASS",
     "evidence": "Changed in this slice: project.html lines 7, 217, 225, 235, 242, 245, 296 (git diff -U0); grader/test_project.py insertions at 14-15, 341-368, 444-452; mutants m35, m36, m37 (added). Unchanged: reference.py, instance.py, starter.py, tests/labs/SC1/*, m01-m34. Every changed line was read and is covered by a row above."},
]

rows = []
for rid, row in r6_rows.items():
    if rid in ROW7:
        status, check, location, evidence, *rest = ROW7[rid]
        fix = ""
        if status != "PASS":
            fix = rest[0] if rest else ""
    else:
        raise SystemExit(f"round-6 row {rid} has no round-7 disposition")
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        out["fix"] = (
            "test_project.py:243 and :252: reword the two failure messages so they name the property without the closed "
            "form of the expected value, e.g. ':243 \"#{S_n >= 1} must follow from the symmetry of the steps, not from "
            "listing the walks\"' and ':252 \"the endpoint count at level 1 for n = 41 must follow from the symmetry of "
            "the steps, not from listing the walks\"'. Expected values, assertions and the other messages stay unchanged. "
            "Then the docstring sentence at test_project.py:19 is true."
        )
    rows.append(out)
rows += NEW_ROWS
for r in NEW_ROWS:
    r.setdefault("fix", "") if r["status"] == "PASS" else None

# The FAIL rows carry the fix above; PASS rows need no fix.
for r in rows:
    if r["status"] == "PASS":
        r.pop("fix", None)

mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+\.py): (.*) -> (.*?)$")
for line in (OUT / "mutate_graders_SC1_0-9_r7.txt").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    if fname.startswith("SC1a-"):
        continue  # slice a's lab-twin mutants are not counted in this fragment
    killed_by = killer.strip() if status == "KILLED" else None
    mutants.append({"id": fname[:-3], "description": desc.strip(), "file": f"ledgers/SC1/mutants/{fname}",
                    "killed_by": killed_by})

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) and all(m["killed_by"] for m in mutants) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment = {
    "unit": "SC1",
    "slice": "d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-d, round 7 (did not build SC1; re-verified the round-6 rows and the round-6-to-06994db delta)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin); delta 4bd8cb9..06994db read for the slice",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-SC1-d",
    "scratch": "/tmp/sc1d-r7-* (suite and sweep copies, removed after each run); scripts and outputs under ledgers/SC1/scripts/SC1-d-r7/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Verdict FAIL: two rows, one root cause. course/modules/SC/SC1/grader/test_project.py:243 and :252 print the closed form of the "
        "expected value on failure ('(2**n - #{S_n = 0}) / 2' for n = 1..12; '2**(n-1)' for n = 41, i.e. 2**40), which "
        "contradicts the docstring at :19 ('It never prints the expected value'). Probes: out/message_leak_probe_r7.txt, "
        "out/message_leak_probe_odd_r7.txt. Round-6 FAIL SC1-d-ag-level-equality-survivors is fixed: m35 and m36 are killed. "
        "Mutants: 41 slice mutants (m01-m41), all killed; 6 lab-twin files SC1a-* in the same directory are slice a's and are not "
        "listed here. Alternatives: 8 conforming pass 50/50 on seeds 0-49. Alt4 Box-Muller is excluded (ruling 10; the page "
        "states the gauss draw at project.html:232) and is now mutant m40. The plan's 5.7(4) item therefore cannot be met as "
        "written; the architect should confirm the exclusion. Plan 5.4 exemplar IDs are reversed on the page (exemplar-a is "
        "data-level 2, exemplar-b is data-level 4): noted, not failing. n = 41 rule: 'the counts must not list the walks' "
        "(project.html:223) has no bounded test; a brute-force srw_terminal_count would hang at n = 41 (2^41 walks), so it is "
        "rejected by timeout rather than by a failing assertion. Lab 1 interpretation line (project.html:161) says 'Lab 3 and "
        "the engine test the grid'; Lab 3 prints checks (coarse at most fine: True) but asserts nothing, read as loose wording, "
        "not failing. Simpson difference printed by Lab 1 (9.13e-15) depends on summation order (mine gives 8.73e-15); both are "
        "below the page's 1e-14 claim. Not checked: the in-browser grader panel UI, the self-assessment form, live localStorage / "
        "IndexedDB behaviour, the Rung 2 'graded instantly' UI, the timing of alt2b (not run), seeds beyond 499 for the suite, "
        "a blind re-reading by a second reader (I read the annotations in the same session before scoring; I re-scored from the "
        "passages with the asides removed, and both exemplars matched their official scores), and the 'Your code is saved in this "
        "browser' claim beyond the code path (store.js:2, grader.js:53)."
    ),
    "summary": (
        f"SC1 slice d round 7 (project.html proofs/rubric/exemplars, bm_checks grader, project labs, mutants, alternatives): {verdict}. "
        f"Rows: {len(rows)} ({counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE). "
        f"Mutants: {sum(1 for m in mutants if m['killed_by'])}/{len(mutants)} killed (m01-m41). "
        "Failing: SC1-d-ag-messages and SC1-d-ag-docstring (test_project.py:243, :252, :19: failure messages print the closed form of expected values)."
    ),
}
dest = ROOT / "ledgers/SC1/SC1-d.json"
dest.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", dest, "rows", len(rows), counts, "mutants", len(mutants), "verdict", verdict)
