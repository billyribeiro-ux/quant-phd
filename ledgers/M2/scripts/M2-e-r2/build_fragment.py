"""Builds ledgers/M2/M2-e.json (round 2) from the outputs and checks cited in the round-2 verification."""
import json, re, sys
from pathlib import Path
ck = Path(sys.argv[1])
S = "ledgers/M2/scripts/M2-e-r2/"
mut = []
for line in (ck / S / "mutate_output.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*) -> (.*)$", line)
    if m:
        killed = None if m.group(1) == "SURVIVED" else m.group(4)
        mut.append({"id": m.group(2).split("_")[0], "file": m.group(2) + ".py", "description": m.group(3), "killed_by": killed})
ROWS = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    ROWS.append(r)

row("m2e-lab1-numbers", "Rung 1 lab: hypothesis numbers, twin, output, recomputation",
    "course/modules/M/M2/project.html lines 57-76 (#lab-M2-project-1)", "PASS",
    "Page code == tests/labs/M2/lab-M2-project-1.py (twin_equals_page_code True). python -I -W error stdout == page expected block (extract_labs.py). Exact Fraction recompute: P=1081108.9577935503, round 1081109, dP/dy=-8514667.395285616, d2P=83766485.11919491, duration 7.875864; relative differences 1.83e-9 and 9.98e-8 as the hypothesis states. Script: " + S + "extract_labs.py")
row("m2e-lab2-completion", "Rung 2 completion: blanks, twin output and claims",
    "project.html Lab 2 (#lab-M2-project-2); tests/labs/M2/lab-M2-project-2.py", "PASS",
    "Page code keeps the ___ blanks (not runnable, by design); twin output equals the page expected block (run with -I -W error, rc 0). 5.11e-08 is the central-difference error of a cubic (fourth derivative zero, round-off only); 4.44e-16 is the AD round-off. Analytic 8.4 and 3.76 recomputed by hand from the cubic.")
row("m2e-lab3-numbers", "Note's reference lab: hypothesis numbers, twin, output, recomputation",
    "project.html lines ~268-300 (#lab-M2-project-3)", "PASS",
    "Page code == tests/labs/M2/lab-M2-project-3.py; stdout == expected block (extract_labs.py). Exact recompute P=2721581.29091122, round 2721581, dP/dy=-23407826.80547466 (printed -23407826.805475). Smallest central error at 1e-6, orders 0.984 and 2.000, kink +1/-1/0 and cancellation rows all match the printed block.")
row("m2e-lab3-report-lines", "Rung 3 instruction: report/run_report.py built from Lab 3 by the stated rules prints the same lines",
    "project.html Rung 3 'Required outputs' and Lab 3 hypothesis", "PASS",
    "build_report.py applied the page's rules (difference -> fd_derivative; backward kink line -> fd_derivative(f, x-h, h, 'forward'); exact -> sensitivities(...)['dprice_dy']; unrounded price kept) and ran with the reference engine: rc 0, stdout identical to Lab 3 expected block (no diff). Script: " + S + "build_report.py")
row("m2e-one-bond-claim", "Rungs 1-2 text: which lab uses which bond",
    "project.html line 53 (#rungs paragraph)", "PASS",
    "Text: Labs 1 and 3 use two SIMULATED bonds (1000000 and 2500000 cents), Lab 2 a test cubic. Matches lab code (Lab 1 face_cents 1_000_000, Lab 3 face_cents 2_500_000; Lab 2 cubic 1 - 2x + 3x^2 + 0.5x^3).")
row("m2e-hess-tolerance-wording", "Conventions 'Tolerances' vs test_project.py",
    "project.html Conventions 'Tolerances' (#conventions)", "PASS",
    "Each stated tolerance matches the grader: 1e-6 central 1e-5 step (test_central_difference_matches...); 1e-9 AD; 1e-5 Hessian entries at h=1e-4; 1e-6 forward quotient at 1e-3; 1e-6 symmetry with 1+max scale; 1e-6 dprice at 1e-5; 1e-4 d2price; 1e-9 ratios; order steps 1e-2 and 5e-3 with bounds 1.9-2.1 and >=3.8. Grader: course/modules/M/M2/grader/test_project.py.")
row("m2e-rubric-c1-vague-level4", "Rubric C1 level 4 is observable and matches the exemplars",
    "project.html rubric table row C1 (#rubric)", "PASS",
    "Level 4 names a 1/h floating-point dependence with reason and a named step; exemplar B meets it (its 1/(2h) magnification and step 1e-6 line up with Lab 3 rows). Spacing 2^-31 = 4.66e-10 recomputed.")
row("m2e-exemplar-b-C3-calibration", "Exemplar B scores and annotations",
    "project.html #exemplar-b (data-scores 4,4,2,3,4)", "PASS",
    "Each annotation checked against the rubric cell: C1 4 (sweep over 11 decades, 1/h and named step), C2 4 (kink values 1,-1,0; cancellation rows at 1e-4, 1e-8, 1e-12 with error 5.32e-05, 1.33e-01, 8.78e-01), C3 2 (no AD value), C4 3 (Lagrange remainders, no bound), C5 4. Printed numbers and ratios recomputed (3e-11 relative error, 1.34 spacings).")
row("m2e-exemplar-a-C3-annotation", "Exemplar A scores and annotations",
    "project.html #exemplar-a (data-scores 2,1,2,2,2)", "PASS",
    "C1 2 (orders, no sweep), C2 1 (no case), C3 2 (analytic and central value, no AD value, no tolerance), C4 2 (orders stated without derivation and without sweep: the level-2 cell covers it; the level-1 cell 'asserts ... no sweep' is not separately triggered under the highest-level rule), C5 2 (price unit given, derivative unit missing). Matches the rubric's highest-level rule.")
row("m2e-richardson-claim", "'What the suite does not check' names Richardson and the grader accepts it",
    "project.html #conventions-check; grader/test_project.py test_central_error_is_at_least_of_order_h_squared", "PASS",
    "Alternative 1 (central with Richardson extrapolation) passes 56/56 on seeds 0-49 (run_alts.sh, ledgers/M2/scripts/M2-e-r2/alts/alt1).")
row("m2e-forward-value-untested", "Forward estimate value is tested",
    "project.html line for forward estimate (#conventions); grader test_forward_estimate_is_the_forward_quotient", "PASS",
    "The test asserts (f(x+h)-f(x))/h = f'(x) + h f''(x)/2 + h^2 p3 to 1e-6 (exact identity for a cubic). Killed m11 and m12 (see mutants).")
row("m2e-mutants-existing-suite", "Every existing mutant is killed by the current suite",
    "ledgers/M2/mutants/ (e01-e11, m01-m16); tools/mutate_graders.py --unit M2 --seeds 0-9", "PASS",
    "mutate_graders M2: PASS (31/31 killed); output in " + S + "mutate_output.txt.")
row("m2e-mutants-own-killed", "Verifier-written student-error mutants are killed",
    "ledgers/M2/mutants/x01-x04 (round 2, written by this verifier)", "PASS",
    "x01 half-up rounding killed by test_exact_halves_round_to_the_even_cent; x02 forward mixed Hessian entry killed by test_hessian_matches_the_analytic_hessian; x03 central scheme without step check killed by test_zero_step_raises_value_error; x04 dual product multiplying derivatives killed by test_forward_mode_matches_the_analytic_derivative. Generator: " + S + "make_mutants.py.")
row("m2e-mutants-own-survivors", "Previously surviving mutants m11 and m12 now killed",
    "ledgers/M2/mutants/m11_*.py, m12_*.py", "PASS",
    "Both killed by test_forward_estimate_is_the_forward_quotient[inst0] (seed 0).")
row("m2e-alt-impls-pass", "Five alternative correct implementations pass 50 seeds",
    "ledgers/M2/scripts/M2-e-r2/alts/alt1..alt5 vs grader/test_project.py", "PASS",
    "run_alts.sh: each of alt1 (Richardson), alt2 (complex-step AD), alt3 (reverse-mode tape), alt4 (closed-form cash-flow sum), alt5 (NumPy-vectorised) gives '50 56 passed' (seeds 0-49, all 56 tests).")
row("m2e-alt-richardson-fails", "Richardson alternative no longer fails the order test",
    "alt1 vs test_central_error_is_at_least_of_order_h_squared", "PASS",
    "alt1 passes all 56 tests on all 50 seeds (see m2e-alt-impls-pass). The test now requires a ratio >= 3.8, which Richardson satisfies.")
row("m2e-mutants-existing-suite-old", "Carried check: reference solution passes 50 seeds",
    "course/modules/M/M2/grader/reference.py", "PASS",
    "Carried from round 1 (reference.py byte-identical since the previous pin); re-run this round: run_graders M2 --seeds 0-49 PASS 50/50 (" + S + "run_graders_output.txt).")
row("m2e-instances", "instance.py generates valid, varied SIMULATED instances",
    "course/modules/M/M2/grader/instance.py", "PASS",
    "Carried from round 1 (instance.py byte-identical since the previous pin). Re-checked the draw constraints: the cubic's second derivative at x0 is >= 1 in size and |p3| >= 0.1 (so the forward-order ratio stays in (1.98, 2.02)); bond draws avoid half-cent ties by 1e-6 (exact Fraction).")
row("m2e-starter-fails", "Starter file fails the whole suite",
    "course/modules/M/M2/grader/starter.py", "PASS",
    "Copied starter.py as sensitivity_engine.py next to the current test_project.py and instance.py: 56 failed (QF_SEED=0, pytest -W error). Re-run because test_project.py changed.")
row("m2e-test-count", "Test count on the page equals the real collect-only count",
    "project.html 'Grading mode' ('runs 56 tests')", "PASS",
    "pytest --collect-only: 56 tests collected; the in-browser run (page_smoke) reports 'All 56 tests pass'.")
row("m2e-tolerances-match-code", "Stated tolerances equal the code's tolerances",
    "project.html Conventions vs grader/test_project.py", "PASS",
    "See m2e-hess-tolerance-wording; every tolerance in the text is a literal in test_project.py.")
row("m2e-order-ratio-bounds", "Order-check bounds are not over-constraining",
    "grader/test_project.py test_forward_error_is_of_order_h and test_central_error_is_at_least_of_order_h_squared", "PASS",
    "Forward: error = (h/2)f''(x) + h^2 p3 exactly for a cubic; with |f''| >= 1 and |p3| >= 0.1 (instance.py) the ratio at (1e-2, 5e-3) stays between 1.98 and 2.02. Central sin: ratio ~ 4 and larger when h^2 term vanishes; both fine. Alternatives pass.")
row("m2e-valueerror-conditions", "The three ValueError conditions are exactly those the page names, in both directions",
    "grader/test_project.py ValueError tests; project.html conventions (a)-(c)", "PASS",
    "Tests cover step 0 and negative for fd and Hessian, unknown schemes (incl. case and whitespace variants), yield -1 and below (price and sensitivities), and accept yield -0.9999 and tiny positive steps. Each condition is named on the page.")
row("m2e-messages-no-leak", "Failure messages do not print the expected value",
    "grader/test_project.py require()/must_raise()/must_accept() messages", "PASS",
    "Messages name properties and hints (Lesson numbers), no expected numeric value is formatted into a message (grep of f-strings in the file: only the parameter name is interpolated).")
row("m2e-pyodide", "Suite runs in the browser within limits",
    "page_smoke --unit M2 --pages project", "PASS",
    "page_smoke modules/M/M2/project.html PASS; in-browser grader: All 56 tests pass (0.8 s); labs 0.0 s each.")
row("m2e-timeout-120s", "'A run in your browser stops after 120 seconds'",
    "course/assets/js/python.js line 4 (TIMEOUT_MS = 120000) and line 36 (message)", "PASS",
    "python.js line 4 sets TIMEOUT_MS = 120000 and line 36 reports 'Stopped after 120 s'.")
row("m2e-hours", "Hours: hub split, time-budget table, lesson hours",
    "project.html Time budget table; index.html data-hours-*", "PASS",
    "Table rows 4+6+22+6+14+8 = 60 = data-hours-project (index.html); hub 240 + 60 = 300; 24 lessons x 10 h = 240 (plan). Check_pages PASS. No pace judgement made (architect ruling).")
row("m2e-ladder", "Ladder: four rungs in order with working links",
    "project.html section#ladder", "PASS",
    "Four ol.ladder items in order (rung 1 Lab 1, rung 2 Lab 2, rung 3 spec, rung 4 stretch); links to #spec, #grader-section, #report, #stretch exist (ids present).")
row("m2e-rubric-banned-words", "Banned phrases and omissions in the rubric and project text",
    "project.html full text", "PASS",
    "Scanned for 'roughly half', 'about 6%', 'historically', ellipsis, 'obviously', 'clearly', 'trivially'; none found. Every 'about' in a lab hypothesis is followed by the computed value (shown calculation).")
row("m2e-exemplar-a-blind", "Exemplars: scores hidden until the reveal",
    "project.html #exemplar-a, #exemplar-b (data-reveal, aside.annotation)", "PASS",
    "Official scoring sits in p.exemplar-verdict[data-reveal]; annotations in aside.annotation; data-scores agree with the verdict text.")
row("m2e-exemplar-level-overlap", "Rubric levels distinguish the two exemplar-A descriptors (C4 level 1 vs 2)",
    "project.html rubric C4 cells", "PASS",
    "Level 2 ('states them with no derivation, and no comparison with the sweep') and level 1 ('asserts the orders with no derivation and no sweep') overlap for a note with no sweep; the stated highest-level rule resolves it to level 2, as exemplar A's official score does. Noted, not a FAIL.")
row("m2e-dag", "DAG: links and concepts used by the project are in the prerequisite closure",
    "check_dag --unit M2; project.html links L13.html#def-finite-difference-derivative, L19.html#def-hessian", "PASS",
    "check_dag M2 PASS; the two dfn anchors exist (L13 and L19 are M2 lessons in the closure of its own concepts).")
row("m2e-references", "References: keys and reading statements",
    "project.html #reading and #references; references/references.json", "PASS",
    "verify_refs --unit M2 (live): 2 of 560 entries, 0 problems; verify_refs --offline: 560 entries, 0 problems. The page attributes no statement to either source.")
row("m2e-lint", "ruff check and format on grader and labs",
    "course/modules/M/M2/grader, tests/labs/M2", "PASS",
    "ruff check: All checks passed; ruff format --check: 31 files already formatted.")
row("m2e-run-labs", "All M2 labs run and match their expected output",
    "tools/run_labs.py --unit M2", "PASS",
    "run_labs M2: PASS (27/27).")
row("m2e-cards-count-coverage", "cards.json covers L01-L24 and counts",
    "course/modules/M/M2/cards.json (377 cards)", "PASS",
    "377 cards (375 before, 2 added: M2-c376 L01, M2-c377 L24); every lesson L01-L24 has 11-22 cards; grades T 241, C 78, none other (no card lacks a grade).")
row("m2e-cards-numbers-in-lesson", "Every number on a card appears in its lesson",
    "cards.json vs course/modules/M/M2/L01..L24.html text", "PASS",
    "cards_numbers.py: token-level check; 7 numbers are not written in the identical form (0.1 for 1e-1 in M2-c092; 8.1 for 8.10000000 in M2-c107; 0.125 for 0.12500000 in M2-c127; 'Lesson 15' for 'Lesson L15' in M2-c263/c275; 12 in 12n^2 in M2-c300; 'Lesson 21' for 'Lesson L21' in M2-c326). Each value is printed in its lesson (value identity checked by hand). Notation only.")
row("m2e-cards-dup-scan", "Duplicate scan of cards (ids and fronts)",
    "cards.json", "PASS",
    "No duplicate id; no duplicate front text (python scan). Near-duplicate scan by eye only for the 55 changed cards.")
row("m2e-cards-numeric-rederive", "Numbers on the 55 changed cards re-derived",
    "cards.json M2-c001..M2-c377 (changed set), lesson outputs in L04, L07, L08, L09, L11, L13, L14, L15, L16, L18, L19, L20, L21, L22, L24", "PASS",
    "Re-derived in Python/Fraction: M2-c047 (3h+h^2 at h=1e-6: 3.000001e-06, /h 3.000001); M2-c189/190/192/193 (e*h/2 and e*h^2/6 intervals; 10 e^(xi1-xi2) bounds 9.990, 10.101; central 98.91, 101.11); M2-c197 (1.364e-2/4.530e-5 = 301); M2-c196 (2.154e-7/6.603e-9 = 32.6); M2-c199 (2^-53/1e-8 = 1.1e-8); M2-c206 (f(2)=15.232760911, f'(2)=21.731770522); M2-c127 (-1/768 = -0.00130208, 1/8 = 0.125); M2-c131 (385/98304, (3n+1)/(6n^2)); M2-c233 (2/(3 sqrt 3) = 0.38490018); M2-c232/234 (1/(2k)); M2-c370 (2 sqrt(e*... ) = 1.8e-8 and (3 delta/e)^(1/3) = 6.3e-6 recomputed); M2-c288 and c294 printed values; M2-c366-c369, c377 against the L24 expected block.")
row("m2e-cards-unchanged-322", "The 322 unchanged cards agree with the CURRENT lesson text",
    "cards.json (unchanged entries), L01-L24", "UNVERIFIABLE",
    "Only the changed set (55 cards plus the 2 added, 57 total) was read against the current lesson text; the other 320 card rows were checked only by the numbers-in-lesson token scan and the grade-basis scan (all 78 grade-C cards have a basis). Not read line by line against all 24 lesson pages.",
    "Read each unchanged card against the current lesson text (L01-L24) and record a row per lesson; the verifier had no budget for the full pass.")
row("m2e-cards-grade-C-basis", "Grade-C cards name their basis",
    "cards.json grade C entries (78)", "PASS",
    "Python check: all 78 cards with grade C have a non-empty basis field; none of the 78 is a lab result presented as T (lab cards: M2-c191..c195, c288, c294, c336, c366-c369, c377 carry grade C with the lab named).")
row("m2e-cards-T-hypotheses-c131", "T card M2-c131 (L09 Section 4): statement and hypotheses",
    "cards.json M2-c131; L09 Section 4 (line 160-165)", "PASS",
    "The card now asks about x^2 on [0,1] only; L09 says the same (line 160). U_n - 1/3 = (3n+1)/(6n^2) > 0 and L_n - 1/3 = -(3n-1)/(6n^2) < 0 for every n >= 1, verified in Fraction.")
row("m2e-cards-T-hypotheses-c205", "T card M2-c205 (L14 Proposition 3.1): proof needs no unlisted assumption",
    "cards.json M2-c205; L14 Proposition 3.1 (line 38) and proof paragraph (line 45)", "FAIL",
    "The proof uses 'the derivative of exp is exp', which L14 line 45 says is 'assumed here ... and not proved on this page'. The card and the proposition are graded T, and the proposition's statement (line 38) does not list it. Proposition 3.1's T grade rests on an unproved fact.",
    "Either grade Proposition 3.1 as T conditional on d/dx exp = exp (add it as a stated hypothesis or prove it from its definition), or change the grade of the card and the lesson's proposition to a stated-assumption grade. Make the card's hypothesis list match.")
row("m2e-cards-T-needed-c319", "T card M2-c319 (L21 Section 3): 'sufficient, not necessary' example supports the claim",
    "cards.json M2-c319; L21 line 105 and Example 3.2 (line 108)", "FAIL",
    "The example F = y^3 - x has zero set the graph y = x^(1/3) (verified), with F_y(0,0)=0. But Theorem 1.2 gives a continuously differentiable g (L21 line 26-27); the graph x^(1/3) is not differentiable at 0, so the example does not show that F_y != 0 is unnecessary for the theorem's conclusion. Only a continuous graph exists there.",
    "Use an example whose implicit function is C^1 with F_y = 0 at the point, for instance F = y^3 - x^3 (graph y = x, F_y(0,0)=0), in both L21 line 105 and M2-c319; or state the claim as 'unnecessary for a graph, not for a C^1 graph'.")
row("m2e-cards-T-needed-c292", "T card M2-c292 (L19 Theorem 2.1): stated sufficient condition carries all hypotheses",
    "cards.json M2-c292; L19 Theorem 2.1 (line 31-33)", "FAIL",
    "The card says 'Equality follows when f_xy is continuous at the point'. Theorem 2.1 also requires f_x, f_y and f_xy to exist at every point of an open disc about p (L19 line 32). The card drops this hypothesis.",
    "Add to M2-c292: 'provided f_x, f_y and f_xy exist on an open disc about the point and f_xy is continuous at it (Theorem 2.1)'.")
row("m2e-cards-lab-as-T-c294", "Lab-based card M2-c294 is graded C with its basis",
    "cards.json M2-c294 (grade C, basis 'Lab 1, one run at step 1e-5 (L19)')", "PASS",
    "Grade and basis now present; the inference (a smooth function has equal mixed partials, so the 1.94e-11 is a computed error) is a deduction from Theorem 2.1 (L19 line 165).")
row("m2e-cards-lab-as-T-c371", "Card M2-c371 graded T relies on a lab-type claim and an upper bound",
    "cards.json M2-c371; L24 Proposition 4.2 and line 56 ('gives an upper bound'); line 154", "FAIL",
    "The card answers 'No' to 'does a smaller step always give a better derivative' with a T grade, from Proposition 4.2. An upper bound that increases as h falls does not show that the true error increases (L24 line 56 says so). The increase is shown only by the printed lab rows (C grade). Its grade is therefore C, not T.",
    "Change the grade of M2-c371 to C with basis 'Lab 1, part B (decade steps)', or add a proof that the true error rises below h* for the stated function.")
row("m2e-cards-c370-notation", "Card M2-c370: central quotient uses the correct third-derivative bound",
    "cards.json M2-c370; L24 Proposition 4.3 (line 122) and line 150", "FAIL",
    "The card says the central step (3 delta/e)^(1/3) is computed 'using the assumed values M_2 approximately e'. The central formula uses M_3 (L24 Proposition 4.3, and line 150 says 'Proposition 4.3 needs M_3'). The value is right (f''' = e^x gives M_3 = e too), but the card names the wrong constant and the lab (line 150) takes M_2 approximately e only.",
    "Rewrite M2-c370 basis: 'M_2 approximately e for the forward quotient and M_3 approximately e for the central quotient (both are e for exp, since f'''=exp)'.")
row("m2e-lesson-L19-theorem-proof", "Lesson-level prose checked against the cards: L19 mixed partials and L11 misconceptions",
    "L19 line 161, L11 lines 119-125", "PASS",
    "Misconception numbering matches the cards (L19 Misconception 1 = mixed partials, 3 = asymmetry; L11 Misconception 3 = integration by parts).")
row("m2e-project-lede", "Project lede claim: finite differences lose accuracy at small steps",
    "project.html lede (line 34-37)", "PASS",
    "Supported by Lab 3 sweep: central error 7.111207e-04 at 1e-6 rising to 5.004462e+02 at 1e-12 (printed block).")

fragment = {
    "unit": "M2",
    "slice": "M2-e",
    "round": 2,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 2; did not build M2; no shared context with builders)",
    "pin": "1817191 (detached worktree /tmp/verifyB2-M2-e)",
    "base": "c11ae01 (round 1 pin); delta: project.html, grader/test_project.py, cards.json (+ L01-L24 HTML, not in slice)",
    "checkout": "/tmp/verifyB2-M2-e",
    "scratch": "/tmp/M2-v/M2-e-r2",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": ROWS,
    "mutants": [{"id": m["id"], "file": m["file"], "description": m["description"], "killed_by": m["killed_by"]} for m in mut],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Scripts: " + S + " (cards_numbers.py, extract_labs.py, build_report.py, txt.py, make_mutants.py, run_alts.sh, build_fragment.py, alts/). Not done: full line-by-line card pass over the 320 unchanged cards against L01-L24; no git commit or push.",
    "summary": {},
}
c = {}
for r in ROWS:
    c[r["status"]] = c.get(r["status"], 0) + 1
fragment["summary"] = {"rows": len(ROWS), "pass": c.get("PASS", 0), "fail": c.get("FAIL", 0), "unverifiable": c.get("UNVERIFIABLE", 0), "mutants": len(mut), "mutants_killed": sum(1 for m in mut if m["killed_by"])}
out = ck / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
