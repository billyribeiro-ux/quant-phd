"""Writes the FC1 slice c round-2 ledger fragment from the archived run outputs (verifier, round 2).

Run from the checkout root: .venv/bin/python ledgers/FC1/scripts/FC1-c-r2/build_fragment_r2.py
Reads /tmp/fc1-v/c2/mutate_r2.txt (tools/mutate_graders.py --unit FC1 --seeds 0-9 output).
A surviving mutant has an empty killed_by, so the merge in tools/ledger.py counts it as not killed.
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
mutants = []
for line in pathlib.Path("/tmp/fc1-v/c2/mutate_r2.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    killed_by = "" if status == "SURVIVED" else killer
    mutants.append({"id": name, "description": desc, "killed_by": killed_by, "source": f"ledgers/FC1/mutants/{name}"})

P = "PASS"
F = "FAIL"


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    return r


rows = [
    row("fc1c-cmd-check-pages", "2.9-structure", "course/modules/FC/FC1/*.html, cards.json",
        P, "tools/check_pages.py --unit FC1 printed 'check_pages FC1: PASS' (ledgers/FC1/scripts/FC1-c-r2 archive: /tmp/fc1-v/c2/check_pages.txt)."),
    row("fc1c-cmd-check-projects", "2.6-spec", "course/modules/FC/FC1/project.html",
        P, "tools/check_projects.py --unit FC1: 'check_projects FC1: PASS' (/tmp/fc1-v/c2/check_pages.txt)."),
    row("fc1c-cmd-check-dag", "DAG", "course/modules/FC/FC1/project.html concept links",
        P, "tools/check_dag.py --unit FC1: 'check_dag FC1: PASS'. project.html links discount-factor and present-value (data-concept attributes present); both are defined in M1 (closure of FC1 is {E1, M1, M2, P0.1}).")
    ,
    row("fc1c-cmd-run-labs", "2.5-labs", "tests/labs/FC1/lab-FC1-project-1..3.py",
        P, "tools/run_labs.py --unit FC1: 'run_labs FC1: PASS (8/8)'. Each project twin run as python -I -W error exits 0; printed output equals the page's expected block (ledgers/FC1/scripts/FC1-c-r2/labs_and_cards_audit_r2.py: 'expected == run: True' for all three)."),
    row("fc1c-lab-twin-sync", "2.5-labs", "project.html lab-FC1-project-1..3 vs tests/labs/FC1/",
        P, "labs_and_cards_audit_r2.py: page code equals twin for project-1 and project-3 (0 differing lines); project-2 differs from its twin only at the two ___ blanks (2 differing lines)."),
    row("fc1c-cmd-run-graders", "2.6-grader", "course/modules/FC/FC1/grader/",
        P, "tools/run_graders.py --unit FC1 --seeds 0-49: 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)' (/tmp/fc1-v/c2/run_graders_r2.txt)."),
    row("fc1c-cmd-page-smoke", "2.5-labs / browser", "project.html",
        P, "tools/page_smoke.py --unit FC1 --pages project: 'page_smoke modules/FC/FC1/project.html: PASS'; in-browser grader 'All 55 tests pass on seed 1705571975'; lab-FC1-project-3 0.0 s (/tmp/fc1-v/c2/smoke-project.txt)."),
    row("fc1c-cmd-verify-refs", "2.1-citations", "project.html reading list (mishkin2021economics, harris2002trading)",
        P, "tools/verify_refs.py --unit FC1: 'live re-verification of FC1: 2 of 560 entries, 0 problems'; tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. project.html line 322 attributes no statement to either source."),
    row("fc1c-cmd-ruff", "gates", "tests/labs/FC1, course/modules/FC/FC1/grader",
        P, "ruff check and ruff format --check on both paths: 'All checks passed!' and '12 files already formatted'."),
    row("fc1c-cmd-pytest-subset", "gates", "tests/ (FC1 and labs subset)",
        P, ".venv/bin/pytest -q -p no:cacheprovider tests -k 'FC1 or labs': 211 passed, no failures."),
    row("fc1c-count-47", "2.9-structure", "project.html line 171 ('runs 55 checks')",
        P, "The page now says 55 checks (round 1 read 47 from an earlier page). `pytest --co -q` on course/modules/FC/FC1/grader/test_project.py (scratch copy /tmp/fc1-v/c2/ref): '55 tests collected'."),
    row("fc1c-numbers-project", "2.2-numbers", "project.html lines 58, 98, 186-193, 262-274; test_project.py 259-278",
        P, "ledgers/FC1/scripts/FC1-c-r2/nums_r2.py (exact Fractions): PV 102775.09103322713 -> 102775; rounding fixture 10277.509103322713 -> 10278, terms 481, 462, 9334 (sum 10277); fixture B 210000/19 = 11052.6316 -> 11053; the displayed digits 102775.091033, 10277.509103, 11052.6316 and 480.77/462.28/9334.46 match."),
    row("fc1c-fixtures-test-map", "2.5-labs / 2.9", "project.html lines 183-193, 275; test_project.py 167-289",
        P, "Fixtures A (test_bond_one_period_fixture_is_par_coupon_plus_face, test_bond_price_one_period_at_its_coupon_rate_is_par), B (test_bond_price_negative_yield_is_above_the_undiscounted_value), C (test_bond_half_cent_coupon_rounds_away_from_zero), D (test_bond_half_cent_on_a_one_cent_face_rounds_up_not_to_zero), E (test_buyer_pays_cash_at_settlement, test_seller_receives_cash_at_settlement), F and G (test_bond_price_exact_half_cent..., test_bond_price_exact_half_at_five_thousand_point_five...), rounding fixture (test_bond_price_hand_fixture_rounds_the_sum_once). Lab 3 printed values equal these expectations (lab output lines 262-274)."),
    row("fc1c-conditions-boundaries", "2.9-structure", "project.html lines 165-167; test_project.py 188-409",
        P, "All eight named conditions are refused on the bad side and accepted on the boundary: periods 0 refused / 1 accepted; face 0 refused / 1 accepted; coupon -1 refused / 0 accepted; yield -10000 refused / -9999 accepted; quantity 0 refused / 1 accepted; price -1 refused / 0 accepted; side 0, 2, -2 refused / +1 and -1 accepted; settlement_day 0 refused / 1 accepted."),
    row("fc1c-local-run-command", "2.6-grader", "project.html line 307; grader/starter.py line 6; grader.js seedNote",
        P, "The command 'QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' ran in a scratch copy with the reference (55 passed) and with the starter (fails, as expected). grader.js builds the same command line from the suite name."),
    row("fc1c-assert-plain-claim", "2.9-structure", "project.html line 308",
        P, "Run with a wrong-price variant (reference plus 7 cents; /tmp/fc1-v/c2/wrong): failures show the test's own message and the failing source line; no computed value is printed. The source line of a hand-fixture test shows its literal (for example '== 10_278'), which is a value printed on the page. The claim 'no values' holds for computed outputs only."),
    row("fc1c-alternatives-overconstraint", "2.6-grader", "ledgers/FC1/scripts/FC1-c-r2/alt/alt1..alt5",
        P, "Five correct alternatives (list comprehension with common denominator; generator-helper with Fraction power; Fraction with floor rule; integer-only floor division; Decimal at 60 digits with ROUND_HALF_UP) pass seeds 0-49 (run_alternatives.sh; /tmp/fc1-v/c2/alts2). Before alt1, alt4 and alt5 were given a guard that rejects a non-int face, they failed only the float-face test; page line 176 ('Every amount is an int number of cents') supports that test, so the test is not an over-constraint."),
    row("fc1c-mutants-new-count", "2.6-grader", "ledgers/FC1/mutants/c2n01..c2n03",
        P, "Three new student-error mutants written by the verifier (make_mutants_r2.py): c2n01 (warns on periods > 8), c2n02 (refuses quantity > 500), c2n03 (drops periods after six from the price). Page-stated requirement: at least three new mutants (ruling g)."),
    row("fc1c-hours", "hours", "project.html lines 285-292; index.html data-hours-lessons=50, data-hours-project=20",
        P, "Project budget rows 1+2+5+4+2+3+3 = 20 = hub project hours. Lessons: 5 x 10 h = 50 (each lesson 'FC1 · Lesson n of 5 · 10 study hours'); 50 + 20 = 70, the curriculum figure. Arithmetic only (architect ruling)."),
    row("fc1c-reading-list", "2.1-citations", "project.html lines 320-327",
        P, "Only data-cite keys; the page states 'This page attributes no statement to either', and no year or locator is typed on the page. verify_refs PASS (see fc1c-cmd-verify-refs)."),
    row("fc1c-reference-panel", "2.6-grader", "project.html line 301; grader/",
        P, "Panel attributes data-suite, data-support, data-solution, data-starter present; grader files test_project.py, instance.py, starter.py, reference.py exist; check_projects PASS."),
    row("fc1c-saved-in-browser", "2.6-grader", "project.html line 300; course/assets/js/grader.js lines 18, 34, 61, 72, 79",
        P, "grader.js saves the draft to the local store on input (debounced 400 ms, line 61) and reloads it (line 34); the only fetch calls are GETs of the starter, instance and suite files (line 18). The claim 'saved in this browser as you type' holds."),
    row("fc1c-scope-words-project", "2.9-structure", "project.html lines 163, 180",
        F, "Universal claims 'On a valid input ... no function prints or warns' (line 163) and 'Each events() call returns the same list' (line 180) are not all covered: the silence claim survives mutant c2n01 (see fc1c2-silence-claim).",
        "Add a silence sweep over valid inputs (or narrow line 163 to the tested inputs); see fc1c2-silence-claim."),
    row("fc1c-card-L01", "2.9-cards", "cards.json FC1-c001..c018, c091..c094 vs L01.html",
        F, "Checked all 22 L01 cards against L01.html (Definitions 1.1, 2.1; Assumption 2.0; Propositions 2.2, 3.1, 3.5, 4.1; Examples 3.3, 3.6; Remarks 1.2, 3.2, 3.4; misconceptions 1-3; Lab 1 outputs). Failing cards: FC1-c009 (fc1c2-card-c009-hypothesis), FC1-c014 (fc1c2-card-c014-printed; fc1c-card-grade-T-lab), FC1-c091..c093 (fc1c2-card-grade-typed-lab).",
        "See the linked rows."),
    row("fc1c-card-L04", "2.9-cards", "cards.json FC1-c056..c072 vs L04.html",
        F, "Checked all 17 L04 cards against L04.html. Failing: FC1-c056 (fc1c2-card-c056-definition: states price-time priority, which the current Definition 1.1 does not use and which Definition 2.1 defines later), FC1-c067 (fc1c2-card-c067-filled: 'reduces the filled quantity' contradicts the Proposition 2.3 proof). c069 (grade C, Lab 1) agrees with lesson row 498.",
        "See the linked rows."),
    row("fc1c-card-L05", "2.9-cards", "cards.json FC1-c073..c090 vs L05.html",
        F, "Checked all 18 L05 cards against L05.html (Definitions 1.1, 1.2; Propositions 2.1, 2.2; Remark 2.3; Problem R2; misconceptions 1-4; Lab 1 outputs). FC1-c084 misstates its quotient as exact (fc1c2-card-c084-exact). All other L05 card statements, numbers and grades agree (ledgers/FC1/scripts/FC1-c-r2/nums_r2.py).",
        "See fc1c2-card-c084-exact."),
    row("fc1c-card-L03", "2.9-cards", "cards.json FC1-c035..c055, c052..c055, c097, c098 vs L03.html",
        F, "Checked all 23 L03 cards against L03.html (Definitions 1.1, 1.2, 2.1, 3.1; Remarks 1.3, 2.2, 2.6, 3.3; Propositions 2.3, 3.2; Corollary 2.4; Example 2.5; misconceptions; Lab 1 outputs). Failing: plain Q as a volume (fc1c-card-notation-Q), and c053 (fc1c-card-atomicity). The others agree.",
        "See the linked rows."),
    row("fc1c-card-L02", "2.9-cards", "cards.json FC1-c019..c034, c095, c096 vs L02.html",
        F, "All 18 L02 cards checked against L02.html (Definition 1.1, Assumption 1.3, Proposition 1.4, Definition 2.1, Remarks 2.2, 2.3, 2.6, 3.2, Proposition 2.5, Example 3.1, misconceptions 1-3, Lab 2 outputs). Wording and numbers agree; the grades of FC1-c029, c095 and c096 disagree with L02 key-results row 409 (T).",
        "Align the grades of FC1-c029, c095 and c096 with the L02 key-results table (see fc1c-card-grade-T-lab and fc1c2-card-grade-typed-lab)."),
    row("fc1c-card-cards-structure", "2.9-cards", "cards.json (98 cards)",
        P, "ledgers/FC1/scripts/FC1-c-r2/labs_and_cards_audit_r2.py: 98 cards, ids FC1-c001..c098 unique and sequential, every lesson L01-L05 has cards (22, 18, 23, 17, 18), no duplicate fronts, the closest front pairs score 0.82 or less. 55 cards have no grade field; they are definitions, assumptions, remarks and misconceptions (BUILDER_RULES 7 requires a grade only for graded results)."),
    row("fc1c-card-cite-numbers", "2.2-numbers", "cards.json backs (numbers)",
        F, "Recomputed every card number with Fractions (nums_r2.py). All agree except FC1-c084: 'an exact quotient of 0.20881' (the exact quotient is 0.2088106..., and 0.20881 is a five-decimal display).",
        "Replace 'an exact quotient of 0.20881' with 'the quotient 0.2088106..., which rounds half up to 0.209' on FC1-c084 and in L05 key-results row 544."),
    row("fc1c-mutant-print-refused-input", "2.5/2.6 mutant", "ledgers/FC1/mutants/v01_print_on_refused_quantity.py",
        P, "mutate_graders.py: KILLED by test_refused_inputs_print_nothing_before_they_raise (seed 0)."),
    row("fc1c-mutant-price-half-even", "2.6 mutant", "ledgers/FC1/mutants/v02_price_rounded_half_even.py",
        P, "mutate_graders.py: KILLED by test_bond_price_exact_half_cent_rounds_away_from_zero (seed 0)."),
    row("fc1c-mutant-float-discount", "2.6 mutant", "ledgers/FC1/mutants/v04_price_from_float_discounting.py",
        P, "mutate_graders.py: KILLED by test_bond_price_exact_half_cent_rounds_away_from_zero (seed 0)."),
    row("fc1c-mutants-run", "2.6 mutation", "tools/mutate_graders.py --unit FC1 --seeds 0-9",
        F, "'mutate_graders FC1: FAIL (27/29 killed)'. Survivors: c2n01_warns_on_long_schedule.py and c2n02_refuses_quantity_above_500.py (see fc1c2-silence-claim and fc1c2-quantity-overrefusal). The 26 existing mutants are all killed.",
        "Add tests that exercise silence and acceptance beyond the seed range (periods > 8, quantity > 500); see the linked rows."),
    row("fc1c-mypy-strict-test-file", "gates", "course/modules/FC/FC1/grader/test_project.py",
        P, "The grader's own strict check (run_graders typecheck, mypy --strict --ignore-missing-imports on reference.py, instance.py, test_project.py in a scratch copy) reports 'Success: no issues found in 3 source files'. The repository mypy (files tools and tests) reports 229 files clean; grader files are outside its scope."),
    row("fc1c-test-docstring-sign", "2.9-structure", "course/modules/FC/FC1/grader/test_project.py line 391",
        P, "Docstring 'Both allowed sides are accepted, and they give opposite signs' matches the assertion buy[0][1] == -sell[0][1]."),
    row("fc1c-reference-docstring-side", "2.4-math / conventions", "course/modules/FC/FC1/grader/reference.py lines 9-11",
        P, "The reference docstring now reads 'side +1 is the long holder, who buys and pays cash; side -1 is the short holder, who sells and receives cash', matching project.html line 179 and the code (-side * quantity * price_cents)."),
    row("fc1c-reference-exclusion-unimplemented", "deployment", "course/modules/FC/FC1/grader/reference.py; BLUEPRINT.md lines 400-401; tools/build_site.py; .gitignore",
        F, "BLUEPRINT.md line 400-401: 'Deployment publishes course/ ... and excludes every grader/reference.py'. No tool or config excludes it: grep of tools/, .github/ and .gitignore finds no exclusion, and course/ is the published tree. The docstring now says so honestly, but the requirement is not met. The gap is repository-wide, not specific to FC1.",
        "Add the exclusion to the deploy step (or move reference.py outside course/), then re-verify. Architect to decide the repository-wide fix."),
    row("fc1c-lab2-check-claim", "2.5-labs", "project.html line 149; course/assets/js/labs.js lines 42-56",
        P, "labs.js compareOutput uses tolerance * (1 + |expected|) with tolerance 1e-6 (data-tolerance): 1e-6 x 102776.09 = 0.1028 cents, so 'about 0.1 cent' is right. The same rule is in tools/coursekit.py compare_output."),
    row("fc1c-closed-form-wording", "2.9-structure", "project.html line 171; test_project.py",
        P, "grep finds no 'closed form' wording in project.html or test_project.py; the page says 'the discounted-sum price on two cases', which is what the test computes."),
    row("fc1c-spec-unenforced-requirements", "2.9-structure", "project.html lines 161-163",
        P, "The page now states that the docstring conventions block, the standard-library-only rule and the grading of the output are 'Not checked by the autograder; a reviewer reads it' (line 161 and 163), so no unenforced requirement is claimed as tested."),
    row("fc1c-card-c033-lesson-disagree", "2.9-cards", "cards.json FC1-c033 vs L02.html misconception 2",
        P, "Card and lesson now agree: the six derivative entries of the register (lab code lines 157-175) carry all five exposure values, and rates carries two (the futures on a government bond and the interest rate swap)."),
    row("fc1c-card-notation-Q", "notation", "cards.json FC1-c039, c048, c049, c055; L03.html Definition 2.1 and Assumption B3",
        F, "Plain Q is a quantity (customer volume Q, demand Q, profit (a - c)Q) on FC1 pages. project plan section 9.2 says 'Never use Q for a quantity or quote on an FC1 page'. notation.json registers only \\mathbb{Q}, which is not used, so the registry itself is not breached.",
        "Rename the quantity (for example V_buy or D) in L03 and the four cards."),
    row("fc1c-card-grade-T-lab", "2.3-grades", "cards.json FC1-c014, FC1-c029 vs L01.html key-results row 460, L02.html key-results row 409",
        F, "Both cards carry grade C with a lab basis; the current lesson key-results tables grade the same typed-in lab results T ('TLab 1, Parts A to D, exact comparisons printed as True'; 'TLab 2, Part B'). Card and lesson disagree.",
        "Decide the grade (typed-in exact labs are not SIMULATED, so T with a lab basis, or C), then make the card and the key-results row match."),
    row("fc1c-card-c030-basis", "2.9-cards", "cards.json FC1-c030 vs L02.html key-results row 408",
        P, "Card and lesson agree: T, with the basis 'Register entries 1, 3, 4 and 6 of Lab 2; Example 3.1'; those four entries are the exchange cash, exchange derivative, OTC cash and OTC derivative entries of the register (lab code lines 157-175)."),
    row("fc1c-card-atomicity", "2.9-cards", "cards.json FC1-c014, FC1-c053",
        F, "BUILDER_RULES 7: 'Each card tests one fact.' FC1-c014 asks two things (the True comparison and the multiplier 6.8619). FC1-c053 gives the spread capture and the terminal mid of 10001 in one answer.",
        "Split FC1-c014 and FC1-c053 into one-fact cards."),
    row("fc1c2-silence-claim", "2.9-structure / mutation", "project.html line 163; ledgers/FC1/mutants/c2n01_warns_on_long_schedule.py",
        F, "Page: 'On a valid input and on each named refused input, no function prints or warns.' Mutant c2n01 (Bond warns when periods > 8) SURVIVES mutate_graders.py --seeds 0-9 (and all seeds 0-49, since make_instance draws periods from 1 to 8). The suite runs silence checks only on the seed case and on the refusals.",
        "Add a sweep that records warnings and stdout over a range of valid inputs (periods 1 to 50, large faces and quantities, yields across the valid range), or narrow line 163 to the inputs the suite runs."),
    row("fc1c2-quantity-overrefusal", "2.9-structure / mutation", "project.html lines 163-167; ledgers/FC1/mutants/c2n02_refuses_quantity_above_500.py",
        F, "Mutant c2n02 refuses quantity 501 and survives. The page names one refusal for quantity (quantity less than 1, line 167) and says any other invalid input may raise or return (line 163); a 501-unit trade is valid on the page, so refusing it contradicts the stated constraints. No test uses a quantity above 500 (instance quantity is 1 to 500).",
        "Add an accept test for a large valid quantity (for example 10**6) and a large valid price, and state the accepted range on the page if one exists."),
    row("fc1c2-card-c009-hypothesis", "2.4-math / 2.3-grades", "cards.json FC1-c009; L01.html Proposition 3.5 (lines ~131-137)",
        F, "FC1-c009 grades T the claim that 'total deposits converge to d/(1 - phi(1 - rho)) ... equality if and only if phi = 1 or rho = 1'. The proof's equality step needs d != 0: with d = 0 every term is 0, so the limit 0 equals d/rho for every phi (phi = 0, rho = 1/2 is a counterexample to 'only if'). Proposition 3.5 states no d > 0 (Proposition 3.1 does). The card copies the statement without the hypothesis.",
        "Add 'with d > 0' to Proposition 3.5 in L01.html and to FC1-c009."),
    row("fc1c2-card-c056-definition", "2.9-cards / DAG", "cards.json FC1-c056 vs L04.html Definition 1.1 (line 59) and Definition 2.1 (line 83)",
        F, "FC1-c056 says a market order trades 'taking resting orders in price-time priority'. The current Definition 1.1 says 'best price first'. Price-time priority is defined later, in Definition 2.1, so the card uses a term before its definition.",
        "Change FC1-c056 to 'best price first', matching Definition 1.1."),
    row("fc1c2-card-c067-filled", "2.4-math / cards", "cards.json FC1-c067 vs L04.html Remark 2.4 and Proposition 2.3 proof",
        F, "FC1-c067: 'Each fill of q shares reduces the filled quantity of both the incoming order and the resting order by q'. The proof says a fill ADDS q to the filled amount of both orders (lesson line 111); the remark says a fill REDUCES the open quantity of each. The card reverses the filled term.",
        "Rewrite as: each fill adds q to the filled quantity of both orders (equivalently, reduces each order's open quantity by q)."),
    row("fc1c2-card-c084-exact", "2.2-numbers", "cards.json FC1-c084; L05.html key-results row 544",
        F, "The card and the lesson say 'exact quotient of 0.20881'. The exact quotient 14282414/68398886 is 0.2088106..., so 0.20881 is a five-decimal display, not exact (nums_r2.py). The three-decimal result 0.209 is right.",
        "Write 'quotient 0.2088106..., which is 0.209 rounded half up to three decimals' in the card and in L05 row 544."),
    row("fc1c2-card-c014-printed", "2.9-cards / lab output", "cards.json FC1-c014 vs tests/labs/FC1/lab-FC1-L01-1 output line 'the partial sums equal the closed form exactly for n = 0 to 10: True'",
        F, "The card says Lab 1 Part A 'prints True for the exact comparison at every stage from 0 to 10'. The lab prints ONE aggregated True for stages 0 to 10 (all_match over the loop); no per-stage True is printed.",
        "Say 'prints one True for the exact comparison of stages 0 to 10'."),
    row("fc1c2-card-grade-typed-lab", "2.3-grades", "cards.json FC1-c091, c092, c093, c095, c096 vs L01.html row 460 and L02.html row 409",
        F, "These cards grade typed-in exact lab results C with a lab basis. L01 key-results row 460 grades 'Lab 1, Parts A to D' T. L02 row 409 grades the register counts T, and FC1-c095/c096 are counts of the same typed-in register. Card and lesson disagree.",
        "Choose one grade for typed-in exact lab output and apply it to both the cards and the key-results tables."),
    row("fc1c2-scope-architect", "scope (architect decision)", "project.html lines 38, 157, 159; plans/FC1-build-plan.md 'Architect decisions'",
        F, "The architect decision (binding) says 'the project covers cash instruments only (a trade-lifecycle and order-book simulator)'. The page specifies a fixed-rate bond and one cash trade settlement event (lines 157-161). It has no trade-lifecycle or order-book simulation: the order book appears only as an ungraded stretch item (line 315).",
        "Either change the project to the architect's stated scope (lifecycle and order book simulator) or record a new architect decision that the bond-and-trade project replaces it."),
    row("fc1c2-notation-registry", "notation", "project.html; cards.json; L01-L05.html",
        P, "No registered symbol of notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears on the FC1 pages or cards; Greek letters are local and defined on use. The plain-Q issue is recorded in fc1c-card-notation-Q."),
    row("fc1c2-banned-phrases-process", "2.9-prose", "project.html, cards.json, L01-L05.html",
        P, "Grep for check_pages banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, ..., it is important to note, studies show, obviously, clearly) and process words (build, builder, verifier, REQUESTS, unit report) finds none in learner text."),
    row("fc1c2-starter-fails", "2.6-grader", "course/modules/FC/FC1/grader/starter.py",
        P, "Starter with test_project.py: 53 of 55 fail (NotImplementedError from each stub); the two that pass accept any exception by design (test_non_whole_face..., test_bool_periods...). The failure text names the stub, not the property; the page does not claim property-naming messages."),
    row("fc1c2-grader-network", "2.9-prose / claims", "project.html line 340 (footer 'nothing you write leaves it')",
        P, "grader.js and py-worker.js make GET requests for the starter, instance and suite only (grader.js line 18); the student's text is written to the local store (lines 61, 72, 79). The footer claim holds for the grader code path read."),
    row("fc1c2-lab3-lab1-claims", "2.5-labs", "project.html hypothesis and interpretation lines 58, 101, 198, 275",
        P, "Lab 1 hypothesis (line 58) states 102775.091033 and the events; the printed output (lab run) matches. Lab 3 hypothesis (line 198) gives each fixture's events and price; the printed lines (lab output lines 262-274) match, and the interpretation's test mapping matches test names in test_project.py."),
]

fragment = {
    "unit": "FC1",
    "slice": "FC1-c",
    "round": 2,
    "verifier": "Claude Haiku 5.5 (independent verifier, FC1 slice c, round 2; did not build FC1; no shared context with its builders)",
    "pin": "e22feb3 (detached checkout /tmp/verifyC2-FC1-c)",
    "base": "55b5634 (the round-1 pin; delta = e22feb3 vs 55b5634 for the slice files)",
    "previous_ledger": "/tmp/fanout-frags/C-FC1-c.round1.json (context only; its PASS rows were re-verified, not carried, because the subjects changed)",
    "checkout": "/tmp/verifyC2-FC1-c",
    "scratch": "/tmp/fc1-v/c2",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta since 55b5634 for this slice: project.html, grader/reference.py, grader/test_project.py, cards.json, "
        "tests/labs/FC1/lab-FC1-project-3.py (+6 lines); lessons L01-L05 and index.html changed in wording (read in full, "
        "checked against the cards); grader/instance.py and starter.py unchanged. Every round-1 non-PASS row was re-verified: "
        "11 now PASS (their subjects changed and the checks were re-run), 5 remain FAIL. The round-1 mutate summary counted 'SURVIVED' rows as killed (killed_by "
        "was a non-empty string); this fragment leaves killed_by empty for survivors. Not checked: the rendered project page beyond "
        "page_smoke; the hub and lesson prose beyond the cards and the project's cross-references; live deployment (none "
        "accessible); the other units' reference.py files (the exclusion gap is repository-wide). Hours judged on arithmetic only."
    ),
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == P),
        "fail": sum(1 for r in rows if r["status"] == F),
        "unverifiable": 0,
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out = ROOT / "ledgers/FC1/FC1-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
