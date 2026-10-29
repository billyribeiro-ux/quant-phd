"""Build the round-14 fragment for M2 slice e from the evidence collected in this round."""
import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

S = "ledgers/M2/scripts/M2-e-r14"
CARRY_CARDS = ("Carried from round 13 (cards of L01-L20 and lessons L01-L20 byte-identical since the round-13 pin fca6bb1; "
               "M2-c394 is re-checked in this round): ")
CARRY_PROJ = "Carried from round 13 (course/modules/M/M2/project.html, grader/ and tests/labs/M2/lab-M2-project-*.py byte-identical since the round-13 pin fca6bb1): "
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)


row("e-auto-run", "reference.py passes the whole suite on seeds 0-49 under browser flags", "course/modules/M/M2/grader/reference.py", "PASS",
    f"tools/run_graders.py --unit M2 --seeds 0-49 -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' ({S}/run_graders_M2.out, rc=0)")
row("e-auto-instances", "instance.py deterministic per seed and varies across seeds", "course/modules/M/M2/grader/instance.py", "PASS",
    f"read in full; the seeded draw, rejection rules (half-cent margin 1e-6, cubic conditioning 1 and 0.1) match its docstring; run_graders M2 PASS on seeds 0-49 ({S}/run_graders_M2.out)")
row("e-mut-existing", "all 113 existing grader mutants killed", "ledgers/M2/mutants/ (113 files)", "PASS",
    f"tools/mutate_graders.py --unit M2 --seeds 0-49 before the new mutants: 'mutate_graders M2: PASS (113/113 killed)' ({S}/mutate_M2_all.out); the same 113 are KILLED in the 116-mutant run ({S}/mutate_M2_new_r14.out)")
row("e-mut-r6_01", "student-error mutant r6_01 (fd step silently capped at one) killed", "course/modules/M/M2/grader/test_project.py:282-308", "PASS",
    f"KILLED r6_01_fd_step_silently_capped_at_one.py (test_large_positive_step_is_accepted, seed 0) in {S}/mutate_M2_new_r14.out")
row("e-mut-r6_02", "student-error mutant r6_02 (hessian step capped at a thousandth) killed", "course/modules/M/M2/grader/test_project.py:546-580", "PASS",
    f"KILLED r6_02_hessian_step_silently_capped_at_a_thousandth.py (test_hessian_positive_step_is_accepted, seed 0) in {S}/mutate_M2_new_r14.out")
row("e-mut-new-killed", "round-12 mutants r12_01..03 and round-13 mutants r13_01..03 killed", "ledgers/M2/mutants/r12_01..r12_03, r13_01..r13_03", "PASS",
    f"KILLED lines for all six in {S}/mutate_M2_new_r14.out (for example r13_01 by test_price_is_the_half_even_rounding_of_the_exact_price[inst0], r13_02 by test_first_derivative_matches_the_central_difference_of_the_price[inst0], r13_03 by test_hessian_positive_step_is_accepted)")
row("e-mut-r14", "three new student-error mutants (round 14) killed by the suite; purity coverage checked",
    "course/modules/M/M2/grader/test_project.py (test_module_prints_nothing_and_warns_nothing, lines ~806-829); course/modules/M/M2/project.html Constraints ('No function prints or warns.')",
    "FAIL",
    f"r14_03_ad_lifts_plain_numbers_with_unit_derivative.py KILLED (test_forward_mode_matches_the_analytic_derivative[inst0]). SURVIVED: r14_01_negative_yield_prints_a_note.py (a print in _yield_rate for yields in (-1, 0)) and r14_02_fd_prints_a_note_for_large_steps.py (a print in fd_derivative for steps above 1000); both pass every test on seeds 0-49, so the suite run reports 114/116 ({S}/mutate_M2_new_r14.out: 'mutate_graders M2: FAIL (114/116 killed)'). The purity test's calls use only INST (positive yield, step 1e-3), and no test captures stdout for ordinary calls; the test message claims 'on any branch of any function', which is not true.",
    "Make the purity guarantee hold for every test: add an autouse fixture that wraps each test in contextlib.redirect_stdout/redirect_stderr and asserts the captured text is empty, and add to test_module_prints_nothing_and_warns_nothing calls that reach the negative-yield branch (bond_price_cents and sensitivities at yield_bps=-9999 and at a negative positive yield such as -5000) and a forward and a central fd_derivative call at step 1e6. Then re-run mutate_graders M2; both new mutants must be KILLED.")
row("e-alternatives", "alternative correct engines pass the suite on seeds 0-49", "course/modules/M/M2/grader/test_project.py", "PASS",
    f"alt1_exact_engine.py: '50/50 seeds pass, 0 fail'; alt2_float_reordered_engine.py: '50/50 seeds pass, 0 fail'; alt3_richardson_complex_rational.py (Richardson central estimate, complex-step ad_derivative, exact Fraction price): '50/50 seeds pass, 0 fail' (sh {S}/run_alt_r14.sh)")
row("e-messages", "failure messages name a property and never print the expected value", "course/modules/M/M2/grader/test_project.py", "PASS",
    CARRY_PROJ + "test_project.py identical; read in full this round (829 lines); every require/must_raise message names a property and no message formats an expected value; full suite passes in browser (page_smoke PASS)")
row("e-pyodide-local", "suite runs in the browser grader with local files", "course/modules/M/M2/project.html", "PASS",
    f"tools/page_smoke.py --unit M2 --pages project -> 'page_smoke M2: PASS' ({S}/page_smoke_M2_project.out, rc=0)")
row("e-test-count", "test count on page equals collect-only count", "course/modules/M/M2/project.html (Grading mode: 'runs 85 tests')", "PASS",
    "pytest --collect-only -q in a scratch copy with the reference engine: '85 tests collected'; project.html states 85")
row("e-valueerror-scope", "ValueError only for conditions the page names", "course/modules/M/M2/grader/test_project.py; course/modules/M/M2/project.html (Conventions, 'The three ValueError conditions')", "PASS",
    "read in full: the three named conditions are step not above zero (zero, negative zero, NaN, negative infinity, tiny negatives), scheme not 'forward' or 'central', and yield at or below -1 (-10000 bps); must_raise is used only for those; no test demands a ValueError elsewhere")
row("e-scheme-types", "scheme argument types named on page", "course/modules/M/M2/project.html (Grading mode and Conventions)", "PASS",
    "page names None, the integer 1, True, the float 1.0 and bytes b'central'; test_scheme_that_is_not_a_name_raises_value_error parametrises exactly these")
row("e-hours", "hours design targets", "course/modules/M/M2/project.html (Time budget)", "PASS",
    "read in full; rows 4, 6, 22, 6, 14, 8 are design targets; no hour row is contradicted by the lesson or grader text")
row("e-hours-arith", "hours arithmetic between hub split and lesson hours", "course/modules/M/M2/project.html (Time budget); course/modules/M/M2/index.html", "PASS",
    "rows sum to 4+6+22+6+14+8 = 60; project.html 'Total 60' and the hub 'the module's 300' with '240 h lessons · 60 h project (20%)' agree")
row("e-ladder", "four-rung ladder in order", "course/modules/M/M2/project.html:40-48", "PASS",
    f"read in full (Rung 1 worked example, Rung 2 completion, Rung 3 independent project, Rung 4 stretch); tools/check_projects.py --unit M2 -> 'check_projects M2: PASS' ({S}/check_projects.out)")
row("e-spec-questions", "specification names context, inputs, outputs, constraints, grading mode", "course/modules/M/M2/project.html Rung 3 specification (lines ~200-220)", "PASS",
    "read in full: Context, Inputs, Required outputs (five functions and three note files), Constraints, Grading mode, Conventions all present")
row("e-rubric-calibration", "rubric calibrated with two exemplars", "course/modules/M/M2/project.html (The rubric and Two exemplars)", "PASS",
    "read in full; each exemplar's official scoring (A: C1 2, C2 1, C3 2, C4 2, C5 2; B: C1 4, C2 4, C3 2, C4 3, C5 4) matches its per-criterion annotations, checked element by element")
row("e-rubric-observable", "rubric rows observable", "course/modules/M/M2/project.html rubric table", "PASS",
    "each of the five criteria has four levels with named elements (sweep, derivation, unit, tolerance, case rows) that a reader can check in the note")
row("e-rubric-adversarial", "self-assessment and rubric resist adversarial answers", "course/modules/M/M2/project.html (Scoring; Self-assessment and calibration)", "PASS",
    "'Each level contains the one below it' and 'the highest level whose every element the note shows' make a level 3 claim require the named elements; the self-assessment form compares to official scores after the learner scores")
row("e-atlas-studio", "curriculum entry and build plan agree with project", "curriculum/meta.yaml; plans/M2-build-plan.md", "PASS",
    "git diff fca6bb1..HEAD -- curriculum/meta.yaml plans/M2-build-plan.md is empty")
row("e-labs-run", "all project labs run", "tests/labs/M2/lab-M2-project-{1,2,3}.py", "PASS",
    f"tools/run_labs.py --unit M2 -> 'run_labs M2: PASS (27/27)' ({S}/run_labs_M2.out); python -I -W error on each twin: rc=0, empty stderr ({S}/twin_project_{{1,2,3}}.out/.err)")
row("e-labs-page-twin", "page lab code equals twin; expected block equals output", "course/modules/M/M2/project.html Lab 1-3 blocks", "PASS",
    f"run_labs M2 PASS (page code equals twin; expected output matches) ({S}/run_labs_M2.out)")
row("e-lab1-numbers", "Lab 1 numbers in prose match output", "course/modules/M/M2/project.html Lab 1 prose and comments", "PASS",
    "re-derived with python -I: unrounded 1081108.9578 (prose 1081108.96), rounded 1081109, dP/dy -8514667.3953 (prose -8514667.40), second 83766485.1192 (prose 83766485.12), diffs 1.56e-02 (1.8e-9 relative) and 8.36e+00 (1.0e-7 relative), duration 7.875864 (prose 7.88); Lab 2 differences 5.11e-08 and 4.44e-16 agree with 'better than 1e-7' and '1e-15'")
row("e-lab2-numbers", "Lab 2 numbers in prose match output", "course/modules/M/M2/project.html Lab 2 prose and comments", "PASS",
    "analytic second 8.4 and first 3.76 for the cubic 1 - 2x + 3x^2 + 0.5x^3 at 0.8 (6 + 3x and -2 + 6x + 1.5x^2) re-derived; printed differences 5.11e-08 and 4.44e-16 match the comment")
row("e-lab3-numbers", "Lab 3 numbers in prose match output", "course/modules/M/M2/project.html Lab 3 prose (lines ~267-377)", "PASS",
    "Lab 3 prose re-checked against the printed block: unrounded 2721581.29, rounded 2721581, dP/dy -23407826.81 (printed -23407826.805475), smallest central error 7.111207e-04 at 1e-6, orders 0.984 and 2.000, kink +1/-1/0, cancellation 0.0 at 1e-12 with error 8.78e-01; the 'forward error smallest at 1.490103 at 1e-8' sentence matches the forward column; 'central smaller than forward at all 12 steps' checked row by row")
row("e-lab3-interpretation", "Lab 3 interpretation sentence", "course/modules/M/M2/project.html Lab 3 prose after the block", "PASS",
    "the sentences on the forward order near tenfold between 1e-3 and 1e-6 (1.297e5 to 1.3027e2), on the central error rising below 1e-6, and on 'the lab does not test the module' match the printed block")
row("e-report-spec", "report specification", "course/modules/M/M2/project.html Required outputs and Numbers", "PASS",
    "report/run_report.py, error_analysis.md and self_assessment.md named consistently; the kink backward-quotient rewrite fd_derivative(f, x - h, h, 'forward') equals the backward quotient exactly; the bond instance in the spec matches the Lab 3 bond")
row("e-exemplar-numbers", "exemplar numbers", "course/modules/M/M2/project.html Two exemplars (Exemplar A and B)", "PASS",
    "every exemplar number checked against the Lab 3 block: 2721581.2909, 7.111207e-04, -23407826.805475, 1.302673e+02 forward at 1e-6, 2.329569e-02 at 1e-7, 5.004462e+02 at 1e-12, 4.7e-10 spacing (2^-31), 1/(2h)=5e11, 2^-26=1.49e-8, kink values, cancellation 5.32e-05/1.33e-01/8.78e-01, relative error 3e-11; exemplar A's claim that central is smaller at all 12 steps holds")
row("e-sin-ratio", "sin central-difference ratio statement", "course/modules/M/M2/project.html (Tolerances, line ~226)", "PASS",
    "recomputed in python -I over make_instance(s) and make_instance(s+7919) for seeds 0-49: min 3.9999842, max 3.9999851 (rounded to seven places) matching the page")
row("e-formulas", "formulas in the Hessian, AD and ratio bullets", "course/modules/M/M2/project.html Conventions", "PASS",
    "read in full: P'(y) = -sum t C_t (1+y)^(-t-1), P''(y) = sum t(t+1) C_t (1+y)^(-t-2), duration -P'/P, convexity P''/P, Hessian off-diagonal (4h^2) and diagonal (h^2) match reference.py hessian_fd and sensitivities; tolerances match test_project.py")
row("e-cards-correct", "every card agrees with its current lesson text", "course/modules/M/M2/cards.json (395 cards); lessons L01-L24", "PASS",
    CARRY_CARDS + "all 72 cards of L21-L24 and all 16 new cards were read against the lessons in this round (L21, L22, L23 and L24 text re-read where changed); the round-13 failures are fixed: M2-c163 (examples on [0,1], L11 lines 41-45, 134), M2-c386 ('at par' now defined in L23 Definition 1.1, line 59), M2-c394 (L06 R3 at lines 160-163 asks for and gives a proof). Per-card lesson re-read of L01-L20 was not repeated this round (mechanical check passes on all 395 cards); see notes.")
row("e-cards-delta", "cards changed since round-13 pin agree with lessons", "course/modules/M/M2/cards.json (M2-c163, M2-c394)", "PASS",
    "git diff fca6bb1..HEAD -- cards.json changes exactly two cards: c163 ([0, b] -> [0, 1]) and c394 ('Problem R3 proves' -> 'asks for a proof ... worked solution gives one'); both read against L11 and L06 and agree")
row("e-cards-new-390-405", "16 new cards agree with lesson text", "course/modules/M/M2/cards.json (M2-c390..c405)", "PASS",
    CARRY_CARDS + "c390-c402 cite L01, L03, L05, L07, L08, L12, L14, L17, L18 and L20, whose text is byte-identical; c403 (L21 Assumption 1.3, line 26), c404 (L22 Assumption 1.1, line 39) and c405 (L24 Assumption 4.1, line 56) re-read against the changed lessons and agree")
row("e-cards-L21-L23", "cards of the changed lessons L21 to L23 agree with the changed text and lab outputs", "course/modules/M/M2/cards.json (L21, L22, L23 cards); L21.html:198, :319; L22.html:370; L23.html:82, :96-99, :375-379", "PASS",
    f"all 16 L21 cards, 16 L22 cards and 23 L23 cards read against the current text. Numbers re-derived with python -I: L23 P 108110.895779, P' -851466.739529, P'' 8376648.511919, first-order error 4.037716e+02, second-order -1.506081e+01, ratios 3.9279/7.8807 and 3.9634/7.9396, +0.01 exact 100000 vs 100015 (-15), -0.01 exact 117060 vs 117044 (16); L21 slopes at x=0.25, 1, 2 and the x=1 root 0.6823278038 / -0.2846930800; L22 errors 1.9e-13, 1.0e-12, 5.4e-12 and central differences 0.40546511 to 1.38629436. Misconception labels checked against the Misconceptions blocks (L21 items 1-3 at lines 117-122; L22 items 1-3 at lines 164-169; L23 items 1-3)")
row("e-cards-at-par", "card M2-c386 cites a definition of 'at par' in L23 Section 1", "course/modules/M/M2/cards.json (M2-c386); course/modules/M/M2/L23.html:38-59", "PASS",
    "L23 Definition 1.1 (text line 24 of the dump) now reads 'a bond whose price equals its face value is said to be at par'; the Introduces note (line 13) says the phrase is defined in Section 1, which is now true; card back 'said to be at par (Section 1)' agrees")
row("e-cards-c163", "card M2-c163 describes the worked examples' intervals", "course/modules/M/M2/cards.json (M2-c163); course/modules/M/M2/L11.html (Misconception 3, line ~134)", "PASS",
    "L11 Misconception 3 and card M2-c163 now say polynomials on [0, 1] (Corollary 1.2); the Section 2 worked examples (Example 2.2, text line 41 and Example 2.3, line 45) integrate on [0, 1]; Example 3.2 on [0, 2] is Section 3 and is not cited")
row("e-cards-c394", "card M2-c394 describes Problem R3 of Lesson 6 correctly", "course/modules/M/M2/cards.json (M2-c394); course/modules/M/M2/L06.html R3 (dump lines 160-163)", "PASS",
    "R3 asks 'prove that |f(x) - f(y)| <= M|x - y|' (line 161) and has a worked solution (lines 162-163, 'Every problem has a full worked solution', line 111); the card's new wording agrees")
row("e-cards-dup", "no duplicate cards", "course/modules/M/M2/cards.json", "PASS",
    "python3: 395 unique ids, 0 duplicate fronts, 0 duplicate backs")
row("e-cards-numbers", "every card number appears in its lesson", "course/modules/M/M2/cards.json", "PASS",
    f"ledgers/M2/scripts/M2-e-r14/check_cards_mech.py (lesson dump from tools/dump_text.py equivalent, {S}/check_cards_mech.out): 395 cards, 50 flags, all of the form 'Misconception N not in L..' (list-item labels, verified by hand); zero number flags")
row("e-cards-atomic", "cards are atomic (one checkable fact each)", "course/modules/M/M2/cards.json", "PASS",
    CARRY_CARDS + "cards read in this round for L21-L24 are single facts; the two changed cards are single facts")
row("e-cards-labels", "every card's label (Theorem, Assumption, Example, Misconception) exists in its lesson", "course/modules/M/M2/cards.json", "PASS",
    f"check_cards_mech.py label checks: only the 50 'Misconception N' list-item flags, all verified by hand against the Misconceptions blocks; no Theorem, Assumption, Example, Remark or Lesson label is missing ({S}/check_cards_mech.out)")
row("e-cards-grades", "grades and bases consistent", "course/modules/M/M2/cards.json", "PASS",
    "grades: T 241, C 76, no grade 78 (python3 Counter); every C card has a basis naming Lab 1 or SIMULATED data and no non-C card has a basis")
row("e-cards-delta-removed", "no card from the round-13 pin removed", "course/modules/M/M2/cards.json", "PASS",
    "395 ids in the round-13 pin and in d2b4a87 (git diff shows two modified lines and no deleted ids)")
row("e-data-figures", "no data or figure claims on the project page", "course/modules/M/M2/project.html", "PASS",
    CARRY_PROJ + "no data file is read, and the page states the bonds are SIMULATED")
row("e-structure", "page and card structure checks", "course/modules/M/M2/", "PASS",
    f"tools/check_pages.py --unit M2 -> 'check_pages M2: PASS' ({S}/check_pages.out)")
row("e-banned-phrases", "no process words in learner text", "course/modules/M/M2/*.html, cards.json", "PASS",
    f"tools/check_pages.py --unit M2 PASS (banned strings checked in visible prose) ({S}/check_pages.out); the project prose and changed cards were also read for process words")
row("e-dag", "concepts used only within the prerequisite closure", "course/modules/M/M2/", "PASS",
    f"tools/check_dag.py --unit M2 -> 'check_dag M2: PASS' ({S}/check_dag.out)")
row("e-notation", "every symbol agrees with notation/notation.json", "course/modules/M/M2/cards.json (M2-c284 line, M2-c285 line); notation/notation.json", "FAIL",
    "notation.json registers T as 'number of return observations (periods) in a sample'. Cards M2-c284 ('h^T H(p) h') and M2-c285 ('d^T H(p) d') use the letter T as the transpose superscript, a second meaning for a registered symbol. The lesson L19 writes \\(h^{\\top}\\) and \\(d^{\\top}\\) (L19.html:99), so the card is out of line with its lesson's notation. The project page and cards otherwise use no registered symbol (checked against the eight registered entries; no \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f or \\mathbb{Q}).",
    "In cards.json, write the transpose as 'h-top' or 'h^top' (the L19 \\top notation) in M2-c284 and M2-c285, or spell it 'the transpose of d' (no letter T as a superscript), then re-run the card check.")
row("e-citations", "named sources resolve in the registry", "course/modules/M/M2/project.html:547-551", "PASS",
    f"tools/verify_refs.py --offline -> '560 entries, 0 problems' ({S}/verify_refs_offline.out); spivak2008calculus and hubbard2015vector both present in references/references.json")
row("e-hours-declared-spec", "declared hours in the spec match the hub", "course/modules/M/M2/project.html:35", "PASS",
    "'M2 project · 60 hours' and 'Total 60 ... 60 of the module's 300' agree with the hub's '240 h lessons · 60 h project (20%)'")

frag = {
    "unit": "M2",
    "slice": "e",
    "round": 14,
    "verifier": "independent verifier (Haiku 5.5), slice e",
    "pin": "d2b4a874a8deeeb77ce4e2ec8bab7479eaf4f00c",
    "base": "fca6bb104984c6a724fc214d8073158e610e995a (round-13 pin); round-13 fragment /Users/billyribeiro/.fanout/frags/B-M2-e.round13.json",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB14-M2-e",
    "scratch": "/tmp/m2e_r14",
    "verified_at": "2026-10-29T00:00:00Z",
    "verdict": "FAIL",
    "mutants": [
        {"name": "r14_01_negative_yield_prints_a_note.py", "description": "The price code prints a note for every negative yield above -1, a branch the purity test never reaches.", "killed_by": "SURVIVED (114/116 killed on seeds 0-49)"},
        {"name": "r14_02_fd_prints_a_note_for_large_steps.py", "description": "fd_derivative prints a note for every step above a thousand.", "killed_by": "SURVIVED"},
        {"name": "r14_03_ad_lifts_plain_numbers_with_unit_derivative.py", "description": "ad_derivative lifts a plain number to a dual number with derivative one.", "killed_by": "test_forward_mode_matches_the_analytic_derivative[inst0] (seed 0)"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta since the round-13 pin fca6bb1 is in d2b4a87 (round-13 fix): cards.json (M2-c163, M2-c394), lessons L11, L21, L22, L23, L24 and the L22 lab twin. grader/, project.html and the project lab twins are byte-identical to the round-13 pin.",
        "Round-13 FAIL rows e-cards-at-par, e-cards-c163 and e-cards-c394 are resolved and re-verified (PASS). The round-13 PASS row e-notation was wrong: M2-c284 and M2-c285 use the registered letter T as a transpose.",
        "Scope limit: the L01-L20 card-to-lesson read was not repeated in round 14. Those cards and lessons are byte-identical to the round-13 pin, the round-13 full read found no defect there, and the mechanical check passes all 395 cards; e-cards-correct is carried on that basis and is flagged here so the orchestrator can decide.",
        "Outside this slice, not edited: none.",
        "Fix routing: r14_01 and r14_02 need a grader change (course/modules/M/M2/grader/test_project.py, owner of M2 project grader); e-notation needs a cards.json change (owner of M2 cards).",
    ],
    "rows": rows,
    "summary": "Slice e round 14: FAIL. Two grader gaps (new purity mutants r14_01 and r14_02 survive, against 'No function prints or warns.') and one notation row (M2-c284 and M2-c285 use registered symbol T as transpose). All other rows PASS: reference and grader suite 50/50, 113 existing mutants killed, three alternative correct engines 50/50 each, 85 tests collected and listed, project labs and twins clean, page_smoke PASS, check_pages/check_dag/check_projects/verify_refs PASS, ruff and repo mypy PASS, Lab 1-3 prose numbers and exemplar numbers re-derived, changed cards and L21-L24 cards re-read; round-13 card failures fixed.",
}
json.dump(frag, open("ledgers/M2/M2-e.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("written", len(rows), "rows")
print("validate:", ledger.validate(json.load(open("ledgers/M2/M2-e.json")), "M2-e"))
