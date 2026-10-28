"""Builds ledgers/M2/M2-e.json (round 4) from the rows and logs of this verification. Run with python3 -I from the checkout."""
import json
import pathlib
import re

CK = pathlib.Path("/tmp/verifyB4-M2-e")
D = CK / "ledgers/M2/scripts/M2-e-r4"
R3 = json.loads(pathlib.Path("/tmp/fanout-frags/B-M2-e.round3.json").read_text(encoding="utf-8"))
r3_ids = [r["id"] for r in R3["rows"]]
P = "Round 4 (pin 2657ab5)"

rows = {}
def row(i, check, loc, status, ev, fix=""):
    rows[i] = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        rows[i]["fix"] = fix or "see evidence"

row("m2e-lab1-numbers", "Rung 1 lab: hypothesis numbers, twin, output, recomputation",
    "project.html Lab 1; tests/labs/M2/lab-M2-project-1.py", "PASS",
    P + ": run python3 -I -W error lab-M2-project-1.py exit 0 (D/lab-M2-project-1.out). Printed unrounded 1081108.9578, rounded 1081109, dP/dy -8514667.3953, diff 1.56e-02, d2P 83766485.1192, diff 8.36e+00, duration 7.875864. Recomputed: 1.56e-02/8514667.40 = 1.83e-9 (page 1.8e-9); 8.36/83766485.12 = 9.98e-8 (page 1.0e-7); -P'/P = 7.8759 (page 7.88). Changed text (1.8e-9, 1.0e-7 and the bracketed divisions) matches.")
row("m2e-lab2-completion", "Rung 2 completion: blanks, twin output and claims",
    "project.html Lab 2; tests/labs/M2/lab-M2-project-2.py", "PASS",
    P + ": lab-M2-project-2.py exit 0; output 4 lines (D/lab-M2-project-2.out); page Lab 2 section outside the diff; every output line occurs verbatim in project.html (script presence check, 0 missing for labs 1-3).")
row("m2e-lab3-numbers", "Note's reference lab: hypothesis numbers, twin, output",
    "project.html Lab 3; tests/labs/M2/lab-M2-project-3.py", "PASS",
    P + ": lab-M2-project-3.py exit 0, 27 lines (D/lab-M2-project-3.out); all 27 output lines occur verbatim in project.html (presence check). Lab 3 intro sentence changed only in wording; no AD value is printed (grep auto/ad_/dual on the output: no hits), so exemplar B's statement holds.")
row("m2e-lab3-report-lines", "Rung 3 instruction: report/run_report.py prints the same lines",
    "project.html Rung 3 'Required outputs'", "UNVERIFIABLE",
    P + ": no report/run_report.py exists in the checkout; the rule was not executed. The replacement fd_derivative(f, x-h, h, 'forward') = (f(x)-f(x-h))/h was checked algebraically only.",
    "Not verifiable from the checkout: a student file is required. Re-run when a reference run_report.py is committed.")
row("m2e-one-bond-claim", "Rungs 1-2 text: which lab uses which bond",
    "project.html Rungs 1 and 2 paragraph", "PASS",
    P + ": paragraph read; labs 1 and 3 use SIMULATED bonds (1000000 and 2500000 cents) and lab 2 differentiates the cubic; matches lab-M2-project-1/2/3.py.")
row("m2e-hess-tolerance-wording", "Conventions 'Tolerances' vs test_project.py",
    "project.html 'Tolerances' item; grader/test_project.py", "PASS",
    "Carried from round 3 (Tolerances item not in the round-3 to round-4 diff of project.html; test constants not in the diff of test_project.py): tolerance values 1e-6, 1e-9, 1e-5, 1e-4 as listed. Round-3 comparison of each to its test constant still applies.")
row("m2e-rubric-c1-vague-level4", "Rubric C1 level 4 is observable and matches the exemplars",
    "project.html rubric row C1", "PASS",
    "Carried from round 3 (rubric row C1 is a context line in the round-3 to round-4 diff, unchanged): level 4 names 1/h proportionality and the step below which the central error rises; exemplar B cites rows 1e-6, 1e-7, 1e-12.")
row("m2e-exemplar-b-C3-calibration", "Exemplar B scores and annotations",
    "project.html #exemplar-b", "PASS",
    P + ": scores data-scores 4,4,2,3,4 unchanged; verdict sentence now says Lab 3 prints no automatic-differentiation value (grep of lab-M2-project-3.out for auto/ad_/dual: no hits). Numbers 2721581.2909, 7.111207e-04, 1.33e-01, 5.32e-05, 8.78e-01 occur in lab 3 output (presence check).")
row("m2e-exemplar-a-C3-annotation", "Exemplar A scores and annotations",
    "project.html #exemplar-a", "PASS",
    P + ": scores 2,1,2,2,2 unchanged; verdict sentence now reads 'stated without derivation' which matches the C4 level-2 cell.")
row("m2e-richardson-claim", "'What the suite does not check' names the alternatives and the suite accepts each",
    "project.html 'What the suite does not check'; grader/test_project.py", "UNVERIFIABLE",
    P + ": the page names four accepted implementations: Richardson central quotient, complex-step AD, exact rational cash-flow sum, and reverse-mode AD or a NumPy vector sum. Richardson, complex step, exact rational sums and closed-form sums were run (alt1, alt2, alt4, alt5; 79 passed on seeds 0-49). Reverse-mode AD (Lesson 14) and a NumPy vector sum were NOT run, so 'the same suite accepts each of them' is unverified for those two.",
    "Write one reverse-mode AD and one NumPy-sum implementation and run the suite on seeds 0-49, or narrow the sentence to the implementations that were run.")
row("m2e-forward-value-untested", "Forward estimate value is tested",
    "grader/test_project.py test_forward_estimate_is_the_forward_quotient", "PASS",
    P + ": test unchanged in diff; m11 and m12 (forward-quotient errors) killed on seeds 0-49 (D/mutate_M2_seeds0-49.txt).")
row("m2e-mutants-existing-suite", "Every existing mutant is killed by the current suite",
    "ledgers/M2/mutants/ (55 files before this round); tools/mutate_graders.py --unit M2 --seeds 0-49", "PASS",
    P + ": python3 tools/mutate_graders.py --unit M2 --seeds 0-49 -> 'mutate_graders M2: PASS (55/55 killed)' (D/mutate_M2_seeds0-49.txt). The three new mutants m17-m19 were run separately (see m2e-fd-any-size-untested and m2e-mutants-new-killed).")
row("m2e-mutants-own-killed", "Verifier-written student-error mutants x01-x14 are killed",
    "ledgers/M2/mutants/x01-x14", "PASS",
    P + ": x01-x14 all KILLED in D/mutate_M2_seeds0-49.txt (e.g. x05 by test_negative_infinite_step_raises_value_error, x07 by test_scheme_that_is_not_a_name_raises_value_error[None]).")
row("m2e-mutants-own-survivors", "Previously surviving mutants m11 and m12 are killed",
    "ledgers/M2/mutants/m11_*.py, m12_*.py", "PASS",
    P + ": KILLED m11 by test_forward_estimate_is_the_forward_quotient[inst0], KILLED m12 by the same (D/mutate_M2_seeds0-49.txt).")
row("m2e-alt-impls-pass", "Alternative correct implementations pass 50 seeds",
    "ledgers/M2/scripts/M2-e-r2/alts/alt1-5, M2-e-r3/alts/alt1-3, M2-e-r4/alts/alt4-5 vs current grader", "PASS",
    P + ": verifier_run_alts_r4.sh over r2 alt1-5 and r3 alt1-3: each '50 79 passed' (79 tests, seeds 0-49). Extra r4 alt4 and alt5 (in M2-e-r4/alts, not authored by this verifier): '50 79 passed' each. Ten alternatives, all pass the current grader including the new negative-infinity and scheme-type tests.")
row("m2e-alt-richardson-fails", "Richardson alternative passes the order test",
    "alt1 vs test_central_error_is_at_least_of_order_h_squared", "PASS",
    P + ": r3 alt1 (Richardson central) 50 x 79 passed.")
row("m2e-mutants-existing-suite-old", "reference.py",
    "course/modules/M/M2/grader/reference.py", "PASS",
    P + ": reference.py byte-identical to 2657ab5 vs aa3c26c (git diff --quiet). tools/run_graders.py --unit M2 --seeds 0-49: 'run_graders M2: PASS (reference 50/50 seeds)' (D/run_graders_M2_seeds0-49.txt).")
row("m2e-instances", "instance.py",
    "course/modules/M/M2/grader/instance.py", "PASS",
    "Carried from round 3 (instance.py byte-identical since aa3c26c, git diff --quiet): reference passes 50/50 seeds (run_graders this round).")
row("m2e-starter-fails", "starter.py",
    "course/modules/M/M2/grader/starter.py", "PASS",
    "Carried from round 3 (starter.py byte-identical since aa3c26c, git diff --quiet); run_graders M2 PASS this round includes the starter-fails check.")
row("m2e-test-count", "Test count on the page equals the real collect-only count",
    "project.html 'Grading mode' ('runs 79 tests')", "PASS",
    P + ": copy of grader with reference.py as sensitivity_engine.py, QF_SEED=0: pytest --collect-only -> '79 tests collected'. Page says 79.")
row("m2e-tolerances-match-code", "Stated tolerances equal the code's tolerances",
    "project.html Conventions vs grader/test_project.py", "PASS",
    "Same check as m2e-hess-tolerance-wording; no tolerance constant changed in the round-3 to round-4 diff.")
row("m2e-order-ratio-bounds", "Order-check bounds are not over-constraining",
    "grader/test_project.py forward and central order tests", "PASS",
    "Carried from round 3 (order tests not in the diff): alt1 and alt4 (Richardson) pass the central order test on 50 seeds; the forward ratio bounds pass for reference and all ten alternatives.")
row("m2e-valueerror-conditions", "The ValueError conditions are exactly those the page names, both directions",
    "grader/test_project.py ValueError tests; project.html conditions (a)-(c)", "PASS",
    P + ": refusals tested for steps 0, -0.0, -1e-300, -1e-3, NaN, -inf (fd and hessian; hessian -inf test added); schemes None, 1, 'backward', 'Central', unknown names; yield -10000 and -1 in bond price and sensitivities. Accepted: yield -0.9999, step 1e-300 (positive), steps 1 and 5 for fd. The page's 'a step above zero is accepted at any size' is tested only at 1 and 5, see m2e-fd-any-size-untested.")
row("m2e-messages-no-leak", "Failure messages do not print the expected value",
    "grader/test_project.py require/must_raise/must_accept", "PASS",
    P + ": new messages read (negative-infinity, scheme-not-a-name, Hessian positive step); they interpolate the step or a scheme, never an expected value.")
row("m2e-pyodide", "Suite runs in the browser within limits",
    "tools/page_smoke.py --unit M2 --pages project.html --skip-sweep", "PASS",
    P + ": page_smoke M2: PASS. The in-browser run of the suite itself was not observed.")
row("m2e-timeout-120s", "'A run in your browser stops after 120 seconds'",
    "course/assets/js/python.js line 4", "PASS",
    "Carried from round 3 (python.js not in the diff): line 4 TIMEOUT_MS = 120000.")
row("m2e-hours", "Hours: hub split, time-budget table, lesson hours",
    "project.html Time budget (lines 236-246); course/modules/M/M2/index.html; L01-L24 data-hours", "PASS",
    P + ": table 4+6+22+6+14+8 = 60 (Total 60; hunk-free region). Hub eyebrow '240 h lessons · 60 h project'. 24 lesson pages declare data-hours=\"10\" (grep count 24) = 240. 240+60 = 300 = curriculum M2 hours. Pace not judged.")
row("m2e-ladder", "Ladder: four rungs in order with working links",
    "project.html section 'The ladder'", "UNVERIFIABLE",
    P + ": not re-read this round; link targets not checked.",
    "Read the ladder section and check its four links against the section ids this round.")
row("m2e-rubric-banned-words", "Banned phrases and omissions in the rubric and project text",
    "project.html full text; cards.json", "PASS",
    P + ": project.html text: historically 0, roughly half 0, about 6% 0, ellipsis 0 (both forms), builder 0, verifier 0, 'round ' 0. cards.json: 1 hit 'around' (M2-c316) is a substring false positive, not a phrase hit.")
row("m2e-exemplar-a-blind", "Exemplars: scores hidden until the reveal",
    "project.html #exemplar-a, #exemplar-b (data-reveal, aside.annotation)", "UNVERIFIABLE",
    P + ": JavaScript reveal not run in a browser; data attributes read in source only.",
    "Open the page in a browser with JavaScript on and confirm the annotations are hidden until the form is used.")
row("m2e-exemplar-level-overlap", "Rubric levels distinguish exemplar A's C4 descriptors",
    "project.html rubric row C4 (level 1 cell 'Gives no order for either scheme.'; level 2 cell 'states them with no derivation')", "PASS",
    P + ": round-3 FAIL resolved. Level 1 now names an absence ('Gives no order for either scheme'); level 2 names 'states them with no derivation, and no comparison with the sweep'. Exemplar A states both orders with no derivation and is scored 2, which the cells now separate.")
row("m2e-dag", "DAG: links and concepts used by the project are in the prerequisite closure",
    "tools/check_dag.py --unit M2", "PASS",
    P + ": python3 tools/check_dag.py --unit M2 -> 'check_dag M2: PASS'. Project cites Lessons 4, 5, 8, 13, 14, 19 (all in M2 or AC1/S0/S2 closure).")
row("m2e-references", "References: keys and reading statements",
    "project.html #reading and #references", "UNVERIFIABLE",
    P + ": registry entries not checked this round.",
    "Run tools/verify_refs.py --unit M2 and read the registry entries for the project's references.")
row("m2e-lint", "ruff check and format on grader and labs",
    "course/modules/M/M2/grader; tests/labs/M2/lab-M2-project-*.py", "PASS",
    P + ": ruff check: All checks passed; ruff format --check: 7 files already formatted.")
row("m2e-run-labs", "All M2 labs run and match their expected output",
    "tools/run_labs.py --unit M2", "PASS",
    P + ": run_labs M2: PASS (27/27).")
row("m2e-cards-count-coverage", "cards.json covers L01-L24 and counts",
    "course/modules/M/M2/cards.json (376 cards)", "PASS",
    P + ": scripts/cards_check.py: 376 cards, 0 duplicate ids, 0 duplicate fronts; lesson counts L01 14 ... L24 19 (all 24 present).")
row("m2e-cards-numbers-in-lesson", "Every number on a card appears in its lesson",
    "cards.json vs course/modules/M/M2/L01..L24.html text", "PASS",
    P + ": cards_check.py: numeric tokens absent from own lesson = 0 (presence check only).")
row("m2e-cards-dup-scan", "Duplicate scan of cards",
    "course/modules/M/M2/cards.json", "PASS",
    P + ": 0 duplicate ids; 0 duplicate fronts (lowercased, stripped).")
row("m2e-cards-numeric-rederive", "Numbers on the changed cards re-derived",
    "cards.json changed set", "UNVERIFIABLE",
    P + ": re-derived: c370 2 sqrt(delta/e) = 1.8076e-08 and (3 delta/e)^(1/3) = 6.2578e-06 with delta = 2.22e-16 (page 1.8e-8, 6.3e-6). c188 0.005e = 0.0135914 and 0.005e^1.01 = 0.0137280 (page matches). c371 6.603e-09 and 2.154e-07 match L24 Lab 1 Part B output (k=8, k=9). c294 1.94e-11 matches lab-M2-L19-1 output. Not re-derived: the other changed cards whose numbers changed wording only (for example c163 and the P_n Taylor-notation cards) and any number in the 300+ unchanged cards.",
    "Re-derive the numbers of each remaining changed card and each card whose lesson changed.")
row("m2e-cards-grade-C-basis", "Grade-C cards name their basis",
    "cards.json grade C entries", "PASS",
    P + ": grade counts T 241, C 77, no grade 58; every C card has a non-empty basis (scripts/cards_check.py).")
row("m2e-cards-unchanged-322", "The unchanged cards agree with the CURRENT lesson text",
    "cards.json (unchanged entries), L01-L24", "UNVERIFIABLE",
    P + ": only the presence check ran. Lesson pages changed in 21 files since aa3c26c, so unchanged cards were not all re-read against current text.",
    "Read each card against its current lesson page (L01-L24), card by card.")
row("m2e-cards-T-hypotheses-c131", "T card M2-c131 (L09): statement and hypotheses",
    "cards.json M2-c131; L09 Example 3.2 and Section 4", "PASS",
    P + ": L09 Example 3.2: U_n - L_n = 1/n for the uniform partition, U_n - 1/3 = (3n+1)/(6n^2), 1/3 - L_n = (3n-1)/(6n^2), so L_n < 1/3 < U_n for every n. Card answer 'No' and its uniform-partition statement match; the Section 4 cross-reference matches.")
row("m2e-cards-T-hypotheses-c205", "T card M2-c205 (L14 Proposition 3.1): hypotheses",
    "cards.json M2-c205; L14 Assumption 1 and Proposition 3.1", "PASS",
    P + ": round-3 FAIL resolved. L14 Assumption 1 states both facts (derivative of exp is exp; derivative of sin is cos); card now says the same.")
row("m2e-cards-T-needed-c319", "T card M2-c319 (L21): 'sufficient, not necessary'",
    "cards.json M2-c319; L21 Section 3 (F = y^3 - x example)", "PASS",
    P + ": round-3 FAIL resolved. L21 text: 'It is sufficient, not necessary: for F = y^3 - x at the origin, F_y = 0, yet the zero set is the graph y = x^(1/3) over all of R.' Card matches. Check: F_y = 3y^2 = 0 at 0; y^3 = x gives y = x^(1/3) over R.")
row("m2e-cards-T-needed-c292", "T card M2-c292 (L19 Theorem 2.1): hypotheses and example values",
    "cards.json M2-c292; L19 Theorem 2.1 and example", "PASS",
    P + ": L19 Theorem 2.1 text: f on an open disc N about p, f_x, f_y, f_xy exist on N, f_xy continuous at p, then f_yx(p) = f_xy(p). Card matches. Example values checked by hand: f_x(0,y) = -y gives f_xy(0,0) = -1; f_y(x,0) = x gives f_yx(0,0) = 1.")
row("m2e-cards-lab-as-T-c294", "Lab-derived card M2-c294 carries grade C and basis",
    "cards.json M2-c294; L19 Lab 1", "PASS",
    P + ": grade C with basis 'Lab 1, one run at step 1e-5 (L19)'. lab-M2-L19-1 output: 'central-difference Hessian asymmetry |f_xy - f_yx| at the same step: 1.94e-11'. Matches.")
row("m2e-cards-lab-as-T-c371", "Card M2-c371 'a smaller step always better' is graded as lab-derived",
    "cards.json M2-c371; L24 Lab 1 Part B, Misconception 1", "PASS",
    P + ": round-3 FAIL resolved; card is now grade C with basis 'Lab 1, part B, rows 1e-08 and 1e-09'. lab-M2-L24-1 output rows k=8 6.603e-09 and k=9 2.154e-07 match. Misconception text states the same values.")
row("m2e-cards-c370-notation", "Card M2-c370 M_3 wording",
    "cards.json M2-c370; L24 Proposition 4.3 and prediction text", "PASS",
    P + ": round-3 FAIL resolved. Card now says M_3 approximately e on a small interval about 1. Proposition 4.3 minimizer (3 delta/M3)^(1/3) with M3 ~ e gives 6.2578e-06; Proposition 4.2 minimizer 2 sqrt(delta/M2) gives 1.8076e-08 (both recomputed).")
row("m2e-lesson-L19-theorem-proof", "L19 proof and L11 integration-by-parts lines",
    "L19 line 161; L11 lines 119-125", "UNVERIFIABLE",
    P + ": not re-read this round.",
    "Re-read L19 proof passage and L11 lines 119-125 against the statements they support.")
row("m2e-cards-changed-restated-PASS", "Changed cards agree with the current lesson text (spot checks)",
    "cards.json changed set (round-4 diff: about 60 entries, including Assumption 2.1 wording, P_n notation, L08 Remark 1.3, L11, L12, L13, L14, L19, L21, L24)", "UNVERIFIABLE",
    P + ": spot-checked against current lessons: M2-c131, c205, c319, c292, c294, c370, c371, c163 (L11 Corollary 1.2 with b > 0 and Assumption 2.1), and the L12 b = 1 card (L12 text 'for b = 1 both sides are 0 by the convention of Lesson 9, Definition 1.3'). The remaining changed cards were not re-read.",
    "Re-read every changed card against its current lesson text.")
row("m2e-project-lede", "Project lede",
    "project.html lede (lines 34-37)", "PASS",
    "Carried from round 3 (lede lines not in the round-3 to round-4 diff of project.html; diff hunks start at line 54).")
row("m2e-scope-words", "Scope words (only, all, always, every, any, same, drives) have a computation or hypothesis behind them",
    "project.html Conventions (a) and Constraints; 'What the suite does not check'", "FAIL",
    P + ": 'A step above zero is accepted by fd_derivative at any size' (Constraints and Conventions (a)) is a scope claim the suite does not check: the suite tests only steps 1 and 5 (test_large_positive_step_is_accepted) and mutant m17 (refuses steps above 10) survives seeds 0-49. Other scope words checked in context ('every criterion', 'every function', 'same suite') have a test or a stated reason; 'same suite accepts each of them' is limited by m2e-richardson-claim.",
    "See m2e-fd-any-size-untested: add a huge-step acceptance check (h = 1e6, finite result) or drop 'at any size'.")
row("m2e-cards-changed-c370-PASS-numbers", "Numbers on card M2-c370 re-derived",
    "cards.json M2-c370", "PASS",
    P + ": 2 sqrt(delta/e) = 1.8076e-08 (card 1.8e-8); (3 delta/e)^(1/3) = 6.2578e-06 (card 6.3e-6); delta = 2.22e-16 (L24 text). Computed by python.")
row("m2e-proj-numbers-recomputed", "Numbers in project.html labs and exemplars recomputed",
    "project.html Labs 1-3 and exemplars", "PASS",
    P + ": lab outputs regenerated and page-presence checked (all lines of labs 1-3 occur on the page); Lab 1 relative ratios recomputed (1.83e-9, 9.98e-8).")
row("m2e-purity-forward-survivor", "Purity test covers the forward branch (round-3 survivor g01)",
    "grader/test_project.py test_module_prints_nothing_and_warns_nothing; ledgers/M2/mutants/g01", "PASS",
    P + ": round-3 FAIL resolved. The purity test now calls fd_derivative with scheme 'forward' and every named refusal inside the capture; mutate run: 'KILLED g01_forward_scheme_prints_a_trace.py'.")
row("m2e-mutants-r3-killed", "Round-3 mutants g02, g03, g04 killed",
    "ledgers/M2/mutants/g02-g04", "PASS",
    P + ": KILLED g02 (test_price_is_the_half_even_rounding_of_the_exact_price), g03 (test_named_ratios_are_the_stated_formulas), g04 (test_yield_at_minus_one_raises_for_price_and_sensitivities).")
row("m2e-alt-numerical-cutoff", "Different numerical cutoffs and valid algorithms are not over-constrained",
    "ledgers/M2/scripts/M2-e-r3/alts/alt1..alt3 and r4 alternatives", "PASS",
    P + ": alt1 (Richardson, complex step, Fraction price), alt2 (Fraction sensitivities), alt3 (Richardson Hessian diagonal), alt4 and alt5 all pass 50 x 79 on the current grader.")
row("m2e-fd-any-size-untested", "'A step above zero is accepted at any size' is enforced by the suite",
    "project.html Constraints and Conventions (a); grader/test_project.py test_large_positive_step_is_accepted (lines 282-292)", "FAIL",
    P + ": NEW mutant m17 (ledgers/M2/mutants/m17_fd_refuses_steps_above_ten.py: _positive_step refuses step > 10) run on seeds 0-9 against the current grader: 10 of 10 seeds 79 passed (survived). The page says 'a step above zero is accepted by fd_derivative at any size' (Conventions (a)), so the suite does not enforce a sentence the page makes.",
    "Add a huge positive step (for example h = 1e6, with the finite-float check) to test_large_positive_step_is_accepted for both schemes; check the alternatives still pass (1e6 gives a finite quotient for the cubic). Or narrow the page's sentence to 'at the sizes the suite draws'.")
row("m2e-hessian-step-range", "Hessian step sizes the suite accepts, as stated on the page",
    "project.html Constraints ('at the sizes the suite draws (from 10^-3 to 1)') and Conventions (a); grader/test_project.py test_hessian_positive_step_is_accepted (steps 1e-3, 1e-4, 1.0)", "FAIL",
    P + ": the test accepts steps 1e-3, 1e-4 and 1.0, and the Tolerances item tests the Hessian at step 1e-4. The page's 'from 10^-3 to 1' misstates the sizes the suite draws.",
    "Change 'from 10^-3 to 1' to 'from 10^-4 to 1' in Constraints and Conventions (a).")
row("m2e-mutants-new-killed", "Round-4 mutants m18 and m19 are killed",
    "ledgers/M2/mutants/m18_*.py, m19_*.py", "PASS",
    P + ": m18 (hessian refuses step >= 1) KILLED by test_hessian_positive_step_is_accepted on 10/10 seeds; m19 (yield refused at -0.5) KILLED by test_sensitivities_at_a_negative_yield_match_the_central_difference[inst0] on 10/10 seeds.")
row("m2e-negative-infinity-tests", "New negative-infinity refusal tests",
    "grader/test_project.py test_negative_infinite_step_raises_value_error, test_hessian_negative_infinite_step_raises_value_error", "PASS",
    P + ": mutants x05 (fd accepts -inf) and x06 (hessian accepts -inf) KILLED; alternatives all raise ValueError for -inf (50 x 79 passed).")
row("m2e-scheme-type-refusal", "Non-string scheme refusal test",
    "grader/test_project.py test_scheme_that_is_not_a_name_raises_value_error[None,1]", "PASS",
    P + ": x07 (None treated as central) KILLED by test_scheme_that_is_not_a_name_raises_value_error[None]. The page's condition (b) 'a scheme other than forward or central' covers None and 1.")
row("m2e-purity-covers-every-function", "Purity test covers every function and branch the page names",
    "grader/test_project.py test_module_prints_nothing_and_warns_nothing (calls list of 12)", "PASS",
    P + ": the 12 calls include bond price, sensitivities, both fd schemes, hessian, ad_derivative (non-constant and constant), and five named refusals (suppressed). Warnings are recorded with simplefilter('always') and stdout and stderr are captured. Mutants f06, g01, x11, x12 KILLED.")
row("m2e-mutants-ledger-count", "Mutant ledger count",
    "ledgers/M2/mutants (58 files: e01-e11, f01-f10, g01-g04, m01-m19, x01-x14)", "PASS",
    P + ": 58 mutant files; 57 killed on seeds 0-49; m17 survives (see m2e-fd-any-size-untested).")


# ---- assemble ----
ordered = [rows[i] for i in r3_ids if i in rows]
extra = [rows[i] for i in rows if i not in r3_ids]
assert len(ordered) == len(r3_ids) == 57, len(ordered)

mutants = []
log = (D / "mutate_M2_seeds0-49.txt").read_text(encoding="utf-8").splitlines()
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$")
for line in log:
    m = pat.match(line)
    if not m:
        continue
    state, name, desc, killed = m.groups()
    entry = {"id": name.split("_")[0], "file": name + ".py", "description": desc}
    if state == "KILLED":
        entry["killed_by"] = killed
    mutants.append(entry)
mutants.append({"id": "m17", "file": "m17_fd_refuses_steps_above_ten.py",
                "description": "_positive_step refuses any step above ten, so fd_derivative raises ValueError for a large positive step.",
                "note": "SURVIVED seeds 0-9 (10/10 seeds 79 passed); see m2e-fd-any-size-untested"})
mutants.append({"id": "m18", "file": "m18_hessian_refuses_step_of_one_or_more.py",
                "description": "hessian_fd treats a step of one or more as invalid and raises ValueError.",
                "killed_by": "test_hessian_positive_step_is_accepted (seeds 0-9, 10/10)"})
mutants.append({"id": "m19", "file": "m19_yield_refused_at_minus_half.py",
                "description": "_yield_rate refuses any yield at or below -0.5, so bond_price_cents raises for a negative yield the page accepts.",
                "killed_by": "test_sensitivities_at_a_negative_yield_match_the_central_difference[inst0] (seeds 0-9, 10/10)"})

frag = {
    "unit": "M2",
    "slice": "M2-e",
    "round": 4,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 4; did not build M2; no shared context with builders)",
    "pin": "2657ab5 (detached worktree /tmp/verifyB4-M2-e)",
    "base": "aa3c26c (round 3 pin); slice files changed since then: project.html, cards.json, grader/test_project.py; grader/reference.py, instance.py, starter.py and project labs 1-3 byte-identical",
    "checkout": "/tmp/verifyB4-M2-e",
    "scratch": "/tmp/M2-v/M2-e-r4",
    "verified_at": "2026-10-28",
    "rows": ordered + extra,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Scripts: ledgers/M2/scripts/M2-e-r4/ (cards_check.py, txt.py, mk_r4_mutants.py, verifier_run_alts_r4.sh, build_fragment_r4.py; logs mutate_M2_seeds0-49.txt, run_graders_M2_seeds0-49.txt, lab-M2-project-{1,2,3}.out). Alternatives r4 alt4/alt5 under ledgers/M2/scripts/M2-e-r4/alts were run but not authored by this verifier. Not done: semantic card-by-card pass over unchanged cards; reverse-mode AD and NumPy alternatives; reference links; exemplar reveal in a browser; the report/run_report.py rule (no student file). No git commit or push.",
    "summary": "",
}
counts = {}
for r in frag["rows"]:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
frag["summary"] = {"rows": len(frag["rows"]), **counts, "mutants": len(mutants)}
out = CK / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(frag["summary"])
