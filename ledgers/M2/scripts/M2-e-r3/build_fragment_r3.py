"""Round-3 verifier (M2 slice e): builds ledgers/M2/M2-e.json from the round-2 row ids, the round-3 evidence and the mutant runs.
Usage: .venv/bin/python ledgers/M2/scripts/M2-e-r3/build_fragment_r3.py  (run from the checkout root)
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

PREV = json.loads(pathlib.Path("/tmp/fanout-frags/B-M2-e.round2.json").read_text())
prev_rows = {r["id"]: r for r in PREV["rows"]}
mut_out = pathlib.Path("/tmp/M2-v/M2-e-r3/mutate_M2_r3.txt").read_text().splitlines()
mutants = []
for line in mut_out:
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killed = m.groups()
    mid = fname.split("_")[0]
    entry = {"id": mid, "file": fname, "description": desc}
    if status == "KILLED":
        entry["killed_by"] = killed.strip()
    else:
        entry["survived"] = True
        entry["note"] = "SURVIVED: no test fails on seeds 0-49; see row m2e-purity-forward-survivor"
    mutants.append(entry)

CARRY = "Carried from round 2 (files byte-identical since the previous pin): "
R3 = "Round 3 (re-run or re-read this round, pin aa3c26c): "
NOT = "Not re-verified this round (subject changed or not checked line by line); honest gap: "


def row(rid, status, location, check, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or "see evidence"
    return r


rows = [
    row("m2e-lab1-numbers", "PASS", "project.html Lab 1; tests/labs/M2/lab-M2-project-1.py",
        "Rung 1 lab: hypothesis numbers, twin, output, recomputation",
        R3 + "python3 -I -W error tests/labs/M2/lab-M2-project-1.py (exit 0). Printed: unrounded 1081108.9578 (page 1081108.96); rounded 1081109; dP/dy -8514667.3953 (page -8514667.40); diff 1.56e-02 = 1.8e-9 relative (page 2e-9); d2P 83766485.1192 (page 83766485.12), diff 8.36e+00 = 1.0e-7 relative (page 1e-7); duration 7.875864 (page 7.88)."),
    row("m2e-lab2-completion", "PASS", "project.html Lab 2; tests/labs/M2/lab-M2-project-2.py",
        "Rung 2 completion: blanks, twin output and claims",
        R3 + "lab-M2-project-2.py exit 0: second difference 8.400000 vs 8.400000, diff 5.11e-08; AD 3.760000 vs 3.760000, diff 4.44e-16. Page claims (1e-7, 1e-15) hold. Cubic 1+x(-2+x(3+0.5x)) gives f''(0.8)=6+3(0.8)=8.4 and f'(0.8)=3.76 by hand."),
    row("m2e-lab3-numbers", "PASS", "project.html Lab 3; tests/labs/M2/lab-M2-project-3.py",
        "Note's reference lab: hypothesis numbers, twin, output, recomputation",
        R3 + "lab-M2-project-3.py exit 0 (27 lines). Page Lab 3 'Stated before running' values equal the output: 2721581.2909 -> 2721581; -23407826.805475 (page -23407826.81); smallest central error 7.111207e-04 at 1e-6; observed orders 0.984 (page about 1) and 2.000; kink +1/-1/0; cancellation rows 5.32e-05, 1.33e-01, 8.78e-01 match. Forward error falls ~tenfold for 1e-3..1e-6 (1.297e5, 1.302e4, 1.303e3, 1.303e2). Central error below 1e-6 exceeds 7.1e-4 at every printed step. Page output block read visually against the run (not diffed by script)."),
    row("m2e-lab3-report-lines", "UNVERIFIABLE", "project.html Rung 3 'Required outputs'",
        "Rung 3 instruction: report/run_report.py built from Lab 3 by the stated rules prints the same lines",
        NOT + "no student report/run_report.py exists in the checkout; the rule was not executed. The stated replacement (fd_derivative 'forward' at x - h for the backward quotient) was checked algebraically: fd_derivative(f, x-h, h, 'forward') = (f(x)-f(x-h))/h."),
    row("m2e-one-bond-claim", "PASS", "project.html Rungs 1 and 2 paragraph",
        "Rungs 1-2 text: which lab uses which bond",
        R3 + "paragraph read: Lab 1 and Lab 3 use SIMULATED bonds (1000000 and 2500000 cents); Lab 2 differentiates the test cubic. Matches lab-M2-project-1/2/3.py."),
    row("m2e-hess-tolerance-wording", "PASS", "project.html 'Tolerances' paragraph; grader/test_project.py",
        "Conventions 'Tolerances' vs test_project.py",
        R3 + "each stated tolerance matched to its test constant: 1e-6 cubic central; 1e-9 forward-mode; 1e-5 Hessian; 1e-6 forward quotient; 1e-6 symmetry; 1e-6 dprice_dy; 1e-4 d2price_dy2; 1e-9 ratios; step 1e-5, 1e-4, 1e-3 as stated."),
    row("m2e-rubric-c1-vague-level4", "PASS", "project.html rubric row C1",
        "Rubric C1 level 4 is observable and matches the exemplars",
        R3 + "C1 level 4 names 1/h proportionality with its reason and the step below which the printed central error rises; Exemplar B meets it and its text cites rows 1e-6, 1e-7, 1e-12."),
    row("m2e-exemplar-b-C3-calibration", "PASS", "project.html #exemplar-b",
        "Exemplar B scores and annotations",
        R3 + "official scores C1 4, C2 4, C3 2, C4 3, C5 4 agree with each annotation (C1 L3 and L4 met; C2 L4 met; C3 L2 met, L3 missed for no AD value; C4 L3 met, L4 missed; C5 L4 and L3 met). Numbers checked: 2721581.2909, 7.111207e-04, 3e-11 relative, 2^-31 spacing, 1.33e-01, 5.32e-05, 8.78e-01."),
    row("m2e-exemplar-a-C3-annotation", "PASS", "project.html #exemplar-a",
        "Exemplar A scores and annotations",
        R3 + "official scores C1 2, C2 1, C3 2, C4 2, C5 2 agree with the annotations (C5 L2 met, L3 missed; C1 L2 met, L3 missed; C2 L1; C3 L2; C4 L2). The C4 level-1 versus level-2 cell overlap is a separate FAIL row."),
    row("m2e-richardson-claim", "PASS", "project.html 'What the suite does not check'; grader/test_project.py",
        "'What the suite does not check' names Richardson and the grader accepts it",
        R3 + "alt1 (Richardson central fd_derivative, complex-step ad_derivative, Fraction price) passes 75/75 on seeds 0-49 (ledgers/M2/scripts/M2-e-r3/run_alts_r3.sh)."),
    row("m2e-forward-value-untested", "PASS", "grader/test_project.py test_forward_estimate_is_the_forward_quotient (lines 188-199)",
        "Forward estimate value is tested",
        R3 + "test read: compares fd_derivative forward at h=1e-3 with f'(x)+h f''(x)/2 + h^2 p3 at 1e-6; alt implementations with a wrong forward quotient (m11, m12) are killed."),
    row("m2e-mutants-existing-suite", "PASS", "ledgers/M2/mutants/ e01-e11, f01-f10, m01-m16, x01-x04 (41 files); tools/mutate_graders.py --unit M2 --seeds 0-49",
        "Every existing mutant is killed by the current suite",
        R3 + "mutate_graders M2 seeds 0-49: 41 of 41 existing mutants killed (log /tmp/M2-v/M2-e-r3/mutate_M2_r3.txt). The one survivor (g01) is a new mutant, see its row."),
    row("m2e-mutants-own-killed", "PASS", "ledgers/M2/mutants/x01-x04 (round 2)",
        "Verifier-written student-error mutants are killed",
        R3 + "x01-x04 killed on seed 0-49 run (mutate_graders M2)."),
    row("m2e-mutants-own-survivors", "PASS", "ledgers/M2/mutants/m11_*.py, m12_*.py",
        "Previously surviving mutants m11 and m12 now killed",
        R3 + "m11 killed by test_forward_estimate_is_the_forward_quotient; m12 killed by the same test (mutate_graders M2 run)."),
    row("m2e-alt-impls-pass", "PASS", "ledgers/M2/scripts/M2-e-r2/alts/alt1..alt5 and ledgers/M2/scripts/M2-e-r3/alts/alt1..alt3 vs grader/test_project.py",
        "Alternative correct implementations pass 50 seeds",
        R3 + "eight alternatives, each 75 passed on all of seeds 0-49 (run_alts.sh and run_alts_r3.sh). Not run: reverse-mode AD and a NumPy vector sum, which the page names; a closed-form sum is covered in spirit by alt2 (Fraction sums)."),
    row("m2e-alt-richardson-fails", "PASS", "alt1 vs test_central_error_is_at_least_of_order_h_squared",
        "Richardson alternative no longer fails the order test",
        R3 + "alt1 passes the central-order test on all 50 seeds (75 passed each)."),
    row("m2e-mutants-existing-suite-old", "PASS", "course/modules/M/M2/grader/reference.py",
        "reference.py",
        CARRY + "reference.py (byte-identical to 1817191). " + "reference.py byte-identical to round-2 pin; run_graders M2 seeds 0-49: reference 50/50 (log run_graders_M2_0-49.txt); collect-only 75 tests."),
    row("m2e-instances", "PASS", "course/modules/M/M2/grader/instance.py",
        "instance.py",
        CARRY + "instance.py is byte-identical since the previous pin (git diff --quiet 1817191 aa3c26c). The suite passes the reference on seeds 0-49, so the instances are accepted; the cubic conditioning (|f''(x0)|>=1, |p3|>=0.1) is in the docstring and is what keeps the forward ratio inside [1.9, 2.1]."),
    row("m2e-starter-fails", "PASS", "course/modules/M/M2/grader/starter.py",
        "starter.py",
        CARRY + "starter.py byte-identical; run_graders M2 checks that the starter fails the suite (the run returned PASS, so the starter failed)."),
    row("m2e-test-count", "PASS", "project.html 'Grading mode' ('runs 75 tests')",
        "Test count on the page equals the real collect-only count",
        R3 + "pytest --collect-only with QF_SEED=0 and the reference: '75 tests collected'. Page says 75."),
    row("m2e-tolerances-match-code", "PASS", "project.html Conventions vs grader/test_project.py",
        "Stated tolerances equal the code's tolerances",
        R3 + "same check as m2e-hess-tolerance-wording."),
    row("m2e-order-ratio-bounds", "PASS", "grader/test_project.py test_forward_error_is_not_of_order_h_squared, test_forward_error_is_at_least_of_order_h, test_central_error_is_at_least_of_order_h_squared",
        "Order-check bounds are not over-constraining",
        R3 + "the forward ratio bound is conditioned by instance.py (|f''(x0)|>=1 and |p3|>=0.1 give B/A <= 2 in the test's algebra, well inside [1.9, 2.1]); the sin central bound 3.8 accepts Richardson (alt1). Not over-constraining on the tested seeds."),
    row("m2e-valueerror-conditions", "PASS", "grader/test_project.py ValueError tests; project.html conditions (a)-(c)",
        "The three ValueError conditions are exactly those the page names, in both directions",
        R3 + "must_raise is used only for: step 0, -0.0, -1e-300, -1e-3, NaN (fd and hessian); scheme names outside forward/central; yield -1, -1.0001, -2. A yield of -0.9999 and a step 1e-300 are required to be accepted, as the page says. No ValueError is demanded elsewhere."),
    row("m2e-messages-no-leak", "PASS", "grader/test_project.py require/must_raise/must_accept",
        "Failure messages do not print the expected value",
        R3 + "read all helper messages and every require() message: they name properties and hints, with no expected value interpolated (the only f-string messages interpolate the step h or a scheme name, not an expected value)."),
    row("m2e-pyodide", "PASS", "tools/page_smoke.py --unit M2 --pages project.html --skip-sweep",
        "Suite runs in the browser within limits",
        R3 + "page_smoke M2 (project.html) reported PASS (log page_smoke_project.txt); run took 0.6 s wall time. The in-browser run of the suite was not separately observed."),
    row("m2e-timeout-120s", "PASS", "course/assets/js/python.js line 4 (TIMEOUT_MS = 120000) and line 36",
        "'A run in your browser stops after 120 seconds'",
        R3 + "python.js line 4: const TIMEOUT_MS = 120000; line 36 message 'Stopped after ${TIMEOUT_MS / 1000} s'."),
    row("m2e-hours", "PASS", "project.html Time budget; course/modules/M/M2/index.html; L01-L24 headers",
        "Hours: hub split, time-budget table, lesson hours",
        R3 + "project table 4+6+22+6+14+8 = 60 (table row 'Total 60'). Hub index: '240 h lessons · 60 h project'. Each L01-L24 header declares 10 study hours (24 x 10 = 240). Curriculum entry M2 hours 300 = 240 + 60. Arithmetic consistent; pace not judged."),
    row("m2e-ladder", "UNVERIFIABLE", "project.html section 'The ladder'",
        "Ladder: four rungs in order with working links",
        NOT + "rung order read (Rung 1 worked example, Rung 2 completion, Rung 3 independent project, Rung 4 stretch) and matches; the link targets were not clicked or checked."),
    row("m2e-rubric-banned-words", "PASS", "project.html full text; cards.json",
        "Banned phrases and omissions in the rubric and project text",
        R3 + "grep over project.html text and cards.json for historically, roughly half, about 6%, '...', the ellipsis character, builder, verifier, verification, unit report: no hits. Scope words only/every/any/always/same reviewed in context (see m2e-scope-words)."),
    row("m2e-exemplar-a-blind", "UNVERIFIABLE", "project.html #exemplar-a, #exemplar-b (data-reveal, aside.annotation)",
        "Exemplars: scores hidden until the reveal",
        NOT + "the reveal is JavaScript; the data attributes were not inspected in a browser this round, so the hidden-annotation behaviour is not verified."),
    row("m2e-exemplar-level-overlap", "FAIL", "project.html rubric row C4 (cells 'Developing' level 2 and 'Beginning' level 1)",
        "Rubric levels distinguish the two exemplar-A descriptors (C4 level 1 vs 2)",
        "Level 1 cell: 'Asserts the orders with no derivation and no sweep.' Level 2 cell: 'Gives the orders with a derivation for one scheme only, or states them with no derivation, and no comparison with the sweep.' A note that states both orders with no derivation and no sweep satisfies both cells as written. Exemplar A is scored 2 officially and its annotation says 'states the orders, with no derivation', so the score rests on wording the cells do not separate.",
        "Make the level-1 cell name an absence (for example 'gives no order for either scheme, or gives an order with no derivation and no statement of the scheme') so that stating both orders without derivation is unambiguously level 2."),
    row("m2e-dag", "PASS", "tools/check_dag.py --unit M2",
        "DAG: links and concepts used by the project are in the prerequisite closure",
        R3 + "check_dag M2: PASS. Project cites Lessons 4, 8, 13, 14 and 19 only, all in M2 or its prerequisite closure (AC1, S0, S2 per the unit contract)."),
    row("m2e-references", "UNVERIFIABLE", "project.html #reading and #references",
        "References: keys and reading statements",
        NOT + "the reference list is not present in the static text dump; the registry entries were not checked this round."),
    row("m2e-lint", "PASS", "course/modules/M/M2/grader; tests/labs/M2/lab-M2-project-*.py",
        "ruff check and format on grader and labs",
        R3 + "ruff check: All checks passed; ruff format --check: 7 files already formatted."),
    row("m2e-run-labs", "PASS", "tools/run_labs.py --unit M2",
        "All M2 labs run and match their expected output",
        R3 + "run_labs M2: PASS (27/27)."),
    row("m2e-cards-count-coverage", "PASS", "course/modules/M/M2/cards.json (376 cards, was 377)",
        "cards.json covers L01-L24 and counts",
        R3 + "376 cards; ids unique; all 24 lessons represented (11 to 22 cards each); M2-c164 removed since the previous pin. Fronts unique (no duplicates)."),
    row("m2e-cards-numbers-in-lesson", "PASS", "cards.json vs course/modules/M/M2/L01..L24.html text",
        "Every number on a card appears in its lesson",
        R3 + "script scan of all 376 cards: every numeric token in front and back appears in the text of its own lesson page (0 missing). Presence check only; semantic check is a separate row."),
    row("m2e-cards-dup-scan", "PASS", "course/modules/M/M2/cards.json",
        "Duplicate scan of cards (ids and fronts)",
        R3 + "0 duplicate ids; 0 duplicate fronts (lowercased, stripped)."),
    row("m2e-cards-numeric-rederive", "UNVERIFIABLE", "cards.json changed set (19 entries)",
        "Numbers on the changed cards re-derived",
        NOT + "re-derived this round: c370 (2 sqrt(delta/e) = 1.807e-8; (3 delta/e)^(1/3) = 6.257e-6, delta = 2.22e-16) and c188 (interval values appear in L13 text). Not re-derived: the other changed cards' numbers, and any figure in the 322 unchanged cards."),
    row("m2e-cards-grade-C-basis", "PASS", "cards.json grade C entries (78)",
        "Grade-C cards name their basis",
        R3 + "all 78 grade-C cards carry a non-empty basis field; 58 cards carry no grade and are definitions or statements the lesson itself proves, consistent with BUILDER_RULES section 7 (grade is for graded results)."),
    row("m2e-cards-unchanged-322", "UNVERIFIABLE", "cards.json (unchanged entries), L01-L24",
        "The 322 unchanged cards agree with the CURRENT lesson text",
        NOT + "the lesson pages changed in 21 files since the previous pin, so no unchanged card carries forward. Only the presence check (0 missing numbers) was run on them. A semantic card-by-card pass against the current lesson text was not completed."),
    row("m2e-cards-T-hypotheses-c131", "UNVERIFIABLE", "cards.json M2-c131; L09 Section 4",
        "T card M2-c131 (L09 Section 4): statement and hypotheses",
        NOT + "L09 changed since the previous pin and the card was not re-read against the new text this round."),
    row("m2e-cards-T-hypotheses-c205", "FAIL", "cards.json M2-c205; L14 Proposition 3.1 (line 39) and Assumption 1 (line 35)",
        "T card M2-c205 (L14 Proposition 3.1): proof needs no unlisted assumption",
        "The card's hypotheses now include Assumption 1 but describe it as 'the derivative of exp is exp'. L14 line 35 states Assumption 1 as two facts: the derivative of exp is exp and the derivative of sin is cos. The statement uses sin, so the card drops half of the assumed fact.",
        "Change the card to: 'Assumption 1 holds: the derivatives of exp and sin are exp and cos (assumed, not proved)'."),
    row("m2e-cards-T-needed-c319", "FAIL", "cards.json M2-c319; L21 line 106 and Example 3.2 (line 109-112)",
        "T card M2-c319 (L21 Section 3): 'sufficient, not necessary' example supports the claim",
        "Card now says 'this example does not show it necessary'. L21 line 106 says 'It is sufficient, not necessary: for F = y^3 - x at the origin, F_y = 0, yet the zero set is the graph y = x^(1/3) over all of R'. The card contradicts the lesson text, which uses this example for non-necessity.",
        "Restore the card's claim to match L21 line 106 ('sufficient, not necessary, as the example shows: F_y = 0 at the origin and the zero set is still a graph'), or make the lesson and card say the same thing in the other direction."),
    row("m2e-cards-T-needed-c292", "PASS", "cards.json M2-c292; L19 Theorem 2.1 (lines 31-32) and example (line 39-40)",
        "T card M2-c292 (L19 Theorem 2.1): stated sufficient condition carries all hypotheses",
        R3 + "card states: f_x, f_y, f_xy exist on an open disc about the point and f_xy continuous at it. Theorem 2.1 (line 32): f on an open disc N centred at p, f_x, f_y, f_xy exist on N, f_xy continuous at p. Matches. Example values -1 and 1 at the origin: f_xy(0)=-1 from f_x(0,y)=-y, f_yx(0)=1 from f_y(x,0)=x (L19 lines 39-40)."),
    row("m2e-cards-lab-as-T-c294", "UNVERIFIABLE", "cards.json M2-c294 (grade C, basis 'Lab 1, one run at step 1e-5 (L19)')",
        "Lab-based card M2-c294 is graded C with its basis",
        NOT + "grade C with a basis is present; the card was not re-read against the changed L19 text."),
    row("m2e-cards-lab-as-T-c371", "FAIL", "cards.json M2-c371; L24 Proposition 4.2 and line 56",
        "Card M2-c371 graded T relies on a lab-type claim and an upper bound",
        "Card: 'No. Proposition 4.2 bounds the error by (1/2) M_2 h + 2 delta/h, which increases as h falls below h* ... '. The bound increasing does not show that the true error increases, and L24 line 56 says 'Proposition 4.2 gives an upper bound, and the true error at h* is only guaranteed to be at most the bound'. The 'No' needs a counterexample to 'a smaller step always gives a better derivative'. The only one on the page is Lab 1 Part B (1e-9 forward error 2.154e-07 above 1e-8's 6.603e-09), a SIMULATED-lab result, which is grade C.",
        "Grade the card C with basis 'Lab 1 Part B, rows 1e-8 and 1e-9 (SIMULATED)', or restate the T claim as about the worst-case bound only ('the bound of Proposition 4.2 increases as h falls below h*')."),
    row("m2e-cards-c370-notation", "FAIL", "cards.json M2-c370; L24 line 58 (prediction) and Proposition 4.3 (line 51)",
        "Card M2-c370: central quotient uses the correct third-derivative bound",
        "The card's central-step bound now uses M_3 and is grade C with basis. Its wording 'M_3 = e as well' is an equality; the lesson (line 58) says 'M_3 approximately e' and the card's own forward wording says 'approximately'. sup of f''' = e^x over [1-h, 1+h] is e^(1+h), which is approximately e, not equal to it. The numbers 1.8e-8 and 6.3e-6 were re-derived and are correct.",
        "Replace 'so M_3 = e as well' with 'so M_3 approximately e, since sup of e^x over [1-h, 1+h] is e^(1+h)'."),
    row("m2e-lesson-L19-theorem-proof", "UNVERIFIABLE", "L19 line 161; L11 lines 119-125",
        "Lesson-level prose checked against the cards: L19 mixed partials and L11 misconceptions",
        NOT + "L11 and L19 changed since the previous pin; not re-read this round."),
    row("m2e-project-lede", "PASS", "project.html lede (lines 34-37)",
        "Project lede claim: finite differences lose accuracy at small steps",
        R3 + "Lab 3 sweep: the central error rises below 1e-6 (7.1e-4 at 1e-6, 2.3e-2 at 1e-7, 5.0e2 at 1e-12), so the lede's claim holds on the printed evidence."),
    row("m2e-scope-words", "PASS", "project.html full text (only, every, any, always, same, drives, never)",
        "Scope words are backed by a computation or a stated hypothesis",
        R3 + "'only' contexts read: 'Lab 3 shows that it is accurate only over a range of steps' (sweep rows 1e-6..1e-12); 'the order from steps 1e-2 and 1e-3 only' (explicit); 'differs ... only by round-off' (for + - * dual arithmetic, exact derivative formulas); 'returns only the rounded integer' (bond_price_cents). 'every negative step', 'every step h > 0' (Section Rung 3 and Lab 3 note) follow from the stated ValueError rule and the kink computation."),
    row("m2e-cards-changed-restated-PASS", "PASS", "cards.json changed entries M2-c011, c020, c074, c099, c110, c134, c163, c188, c218, c299, c315, c337, c351, c363, c364",
        "Changed cards agree with the current lesson text",
        R3 + "each read against its lesson text: c011 (L01 Prop 3.1 hypothesis a_n -> L), c020 (L02 Section 2 definition), c074 (L06 Section 3 wording), c099 and c134 (L08/L10 Remark 1.3, equal-endpoint and assumed-EVT wording), c110 (L08 Remark 3.3), c163 (L11 Corollary 1.2 with b >= 0 and Fact 2.1 of Lesson 6), c188 (L13 Example 2.3 and Assumption 1), c218 (L14 Misconception 3, branch example), c299 (L20 Remark 2.3), c315 (L21 Theorem 1.2 proof uses MVT in step 2), c337 and c351 (wording only), c363 and c364 (M_2 > 0, M_3 > 0 as in L24 lines 47 and 51)."),
    row("m2e-cards-changed-c370-PASS-numbers", "PASS", "cards.json M2-c370 numbers only",
        "Minimizing-step numbers on c370",
        R3 + "2 sqrt(2.22e-16/e) = 1.8074e-8; (3*2.22e-16/e)^(1/3) = 6.2574e-6; both match the card and L24 line 58."),
    row("m2e-proj-numbers-recomputed", "PASS", "project.html Labs 1-3 and exemplars",
        "Every printed number in the page's prose matches a lab output or a recomputation",
        R3 + "recomputed in Python: Lab 1 duration 7.875864 (7.88); Lab 3 analytic -23407826.805475 (-23407826.81); float spacing at 2.72e6 = 2^-31 = 4.66e-10 (2^21 <= value < 2^22); spacing at 1e8 = 2^-26 = 1.49e-8; 1/(2e-12) = 5e11; exemplar relative error 7.111207e-4/2.3407826805e7 = 3.04e-11."),
    row("m2e-purity-forward-survivor", "FAIL", "course/modules/M/M2/grader/test_project.py test_module_prints_nothing_and_warns_nothing (line ~691); project.html 'Grading mode' ('the purity of the module, which covers every function')",
        "Purity test covers every function, including every branch",
        "New mutant g01 (ledgers/M2/mutants/g01_forward_scheme_prints_a_trace.py) prints the forward estimate in the forward branch of fd_derivative. It SURVIVES mutate_graders M2 on seeds 0-49 (log: mutate_M2_r3.txt, 'SURVIVED g01'). The purity test calls fd_derivative only with scheme 'central'. The page says 'the purity of the module, which covers every function' and the spec says 'No function prints or warns'.",
        "In test_module_prints_nothing_and_warns_nothing, also call sol.fd_derivative(..., 'forward'), and call each named ValueError path (for example a zero step and an unknown scheme) inside the redirect and warning capture, so every branch of every function is exercised."),
    row("m2e-mutants-r3-killed", "PASS", "ledgers/M2/mutants/g02, g03, g04",
        "Round-3 student-error mutants other than g01 are killed",
        R3 + "g02 (coupon truncated to whole cents) killed by test_price_is_the_half_even_rounding_of_the_exact_price; g03 (dprice_dy's d2 replaced by a numerical second difference at 1e-3) killed by test_named_ratios_are_the_stated_formulas (1e-9 check on convexity); g04 (yield check strict at -1) killed by test_yield_at_minus_one_raises_for_price_and_sensitivities."),
    row("m2e-alt-numerical-cutoff", "PASS", "ledgers/M2/scripts/M2-e-r3/alts/alt1..alt3 (Richardson, complex step, Fraction price, Richardson Hessian diagonal)",
        "Different numerical cutoffs and valid algorithms are not over-constrained",
        R3 + "alt1 (Richardson central, complex-step AD, exact Fraction rounding), alt2 (exact Fraction sensitivities), alt3 (Richardson Hessian diagonal) each pass 75/75 on seeds 0-49."),
]

fragment = {
    "unit": "M2",
    "slice": "M2-e",
    "round": 3,
    "verifier": "Claude Haiku 5.5 (independent verifier, round 3; did not build M2; no shared context with builders)",
    "pin": "aa3c26c (detached worktree /tmp/verifyB3-M2-e)",
    "base": "1817191 (round 2 pin); delta in slice files: project.html, cards.json, grader/test_project.py changed; grader/instance.py, reference.py, starter.py and project labs 1-3 byte-identical",
    "checkout": "/tmp/verifyB3-M2-e",
    "scratch": "/tmp/M2-v/M2-e-r3",
    "verified_at": "2026-10-28",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Scripts: ledgers/M2/scripts/M2-e-r3/ (make_r3.py, run_alts_r3.sh, build_fragment_r3.py). Alternatives run from the round-2 scripts too. Not done: a semantic card-by-card pass over the 322 unchanged cards (presence check only); reverse-mode AD and NumPy alternatives; the browser run of the suite; the self-assessment JavaScript reveal; reference list links; the report/run_report.py rule (no student file). No git commit or push.",
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
killed = sum(1 for m in mutants if m.get("killed_by"))
fragment["summary"] = {"rows": len(rows), **{k.lower(): v for k, v in counts.items()}, "mutants": len(mutants), "mutants_killed": killed}
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 and killed == len(mutants) else "FAIL"
out = ROOT / "ledgers/M2/M2-e.json"
out.write_text(json.dumps(fragment, indent=1, ensure_ascii=False) + "\n")
print(json.dumps(fragment["summary"]), fragment["verdict"])
print("validate:", ledger.validate(fragment, "M2-e"))
