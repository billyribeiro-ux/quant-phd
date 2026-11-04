import json, subprocess
from datetime import datetime, timezone

SC = "ledgers/BK4/scripts/BK4-b-r6/"
R = []
def row(id_, check, location, status, evidence, fix=None):
    d = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

row("BK4b-gate-check-pages", "2.9-structure", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html", "PASS",
    "Ran .venv/bin/python tools/check_pages.py --unit BK4 -> 'check_pages BK4: PASS', exit 0 (" + SC + "check_pages.txt).")
row("BK4b-gate-check-dag", "2.9-DAG", "course/modules/BK/BK4/L04.html; L05.html; course/concepts.html", "PASS",
    "Ran tools/check_dag.py --unit BK4 -> 'check_dag BK4: PASS', exit 0 (" + SC + "check_dag.txt).")
row("BK4b-gate-check-projects", "2.6-structure (unit gate)", "course/modules/BK/BK4/project.html", "PASS",
    "Ran tools/check_projects.py --unit BK4 -> 'check_projects BK4: PASS', exit 0 (" + SC + "check_projects.txt). Project content is slice c.")
row("BK4b-run-labs", "2.5-labs", "course/modules/BK/BK4/L04.html:155-357; course/modules/BK/BK4/L05.html:160-336", "PASS",
    "Ran tools/run_labs.py --unit BK4 -> 'run_labs BK4: PASS (8/8)', exit 0 (" + SC + "run_labs.txt).")
row("BK4b-twin-isolated-run", "2.5-labs (twin alone)", "tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py", "PASS",
    "Each twin run alone as python -I -W error from cwd /tmp: exit 0, stderr empty. stdout equals the page expected block after the final newline: the page block omits the newline that print() adds, so exact equality is False and stripped equality is True (" + SC + "twin_vs_page.py, output " + SC + "twin_vs_page.txt).")
row("BK4b-twin-lint", "2.5-labs / BUILDER 6.1", "tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py", "PASS",
    "ruff check -> 'All checks passed!'; ruff format --check -> '2 files already formatted'; mypy --no-incremental -> 'Success: no issues found in 2 source files' (" + SC + "lint_types_pytest.txt).")
row("BK4b-pytest-labs", "2.5-labs", "tests/test_labs.py", "PASS",
    "pytest tests/test_labs.py -k 'BK4 and (L04 or L05)' -> 2 passed (" + SC + "lint_types_pytest.txt, " + SC + "pytest_labs.txt).")
row("BK4b-page-smoke", "2.9-page_smoke", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html", "PASS",
    "Ran tools/page_smoke.py --unit BK4 --pages L04 L05 -> 'page_smoke modules/BK/BK4/L04.html: PASS', 'page_smoke modules/BK/BK4/L05.html: PASS', 'page_smoke BK4: PASS' (" + SC + "page_smoke.txt).")
row("BK4b-verify-refs", "2.1-citations", "references/references.json (bisndbasel); course/modules/BK/BK4/L05.html:347", "PASS",
    "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (" + SC + "verify_refs_offline.txt). tools/verify_refs.py --unit BK4 -> 'live re-verification of BK4: 2 of 560 entries, 0 problems' (" + SC + "verify_refs_unit.txt). bisndbasel is not in that live set because its used_by is [\"BK1\"] (references.json:2840); see registry_flags.")
row("BK4b-citation-bisndbasel", "2.1-attribution / scope", "course/modules/BK/BK4/L05.html:347, :579; references/references.json:2815", "PASS",
    "Registry title 'Basel III: international regulatory framework for banks | Bank for International Settlements', url https://www.bis.org/committees/bcbs/standards (references.json:2815-2822). Plain curl -sS --max-time 30 on that URL this round -> HTTP 200 and <title> identical (" + SC + "curl_bisndbasel.txt). L05:347 names the framework at index level and says the operational-risk section was not read; L05:579 says the same.")
row("BK4b-cmd-recompute", "2.2 / 2.4 / 2.5 (independent recomputation)", SC + "recompute_r6.py", "PASS",
    "Wrote and ran an independent exact-Fraction script (no import of the lab): python -I -W error " + SC + "recompute_r6.py -> exit 0, 61 PASS lines, 'ALL OK' (" + SC + "recompute_r6.txt). Covers every L04 coverage and bps value, both pair-identity tables, Prop 2.4/2.6/R2/R3 grids (0 violations), Remark 2.8, haircut rows, R1 threshold, E1-E3, M1-M3, L05 means (4375/2), variances (133984375/4, 57421875/4), difference 19140625, no-cost probabilities, Example 2.7/2.8, quiz numerics, and a 3000-trial random sweep of Props 2.1, 2.2, 2.4, 2.5, 2.6 (0 violations).")
row("BK4b-numbers-L04-prose", "2.2 (a)/(b)/(c)", "course/modules/BK/BK4/L04.html:52, :56-69, :72-75, :90, :95, :151-153, :356, :376, :392-393, :405-406, :420-424, :429-433", "PASS",
    "Every prose number recomputed in " + SC + "recompute_r6.txt: 1,900,000 and 2,100,000 cents (Remark 1.3, :74); 9/10, 11/10, 113/120 and 9416 (Remark 2.8, :152); 19/40 (:392); 9500 (M3, :406); 6875, 220000, 320000 (E1, :420); 20/19 (:429, :519); 0.45/0.5 arithmetic (R2, :431). Quotes of 'floor of 10000 rho' match Definition 2.1 (:90).")
row("BK4b-numbers-L04-lab-table", "2.2 (printed numbers)", "course/modules/BK/BK4/L04.html:318-355 and :356", "PASS",
    "All 14 coverage rows (7 per ratio), 14 bps values, reserves/claims-left, the 15 and 21 pair counts, and the 3 worked values and haircut rows match the independent recomputation and the twin's actual stdout (" + SC + "twin_vs_page.txt, " + SC + "recompute_r6.txt). :356 interpretation (53/58, 9137, 1,060,000, 1,160,000) matches the table row x=21/50.")
row("BK4b-numbers-L05-prose", "2.2 (a)/(b)/(c)", "course/modules/BK/BK4/L05.html:153, :162, :335, :355, :359, :363, :392, :428, :435-436, :442, :453, :458-460", "PASS",
    "Re-derived: 4375/2 = 2187.5 (Example 2.8, :153); 2188 half-up; 21.88 dollars; 343/512, 169/512, 3/8 = 192/512, 7/8 = 448/512; 1875 = 3*(1/8)*2500*2; 19140625 = 2*2500^2*(7/64)*14 (E2 :435); R1 n-trade ratio = n; R2 bounds 5/8 and 7/8 with the stated three-point example. All matched.")
row("BK4b-lab-table-L05", "2.2 (printed numbers)", "course/modules/BK/BK4/L05.html:304-334 and :335", "PASS",
    "Printed lines 304-334 of the expected block equal the actual stdout of the twin (" + SC + "twin_vs_page.txt) and the exact recomputation (" + SC + "recompute_r6.txt). Interpretation at :335 (4375/2, 2188, 1875, 133984375/4 under A4, 57421875/4 under A3) matches.")
row("BK4b-math-L04-props", "2.2 (a)/(b)/(c) and proofs", "course/modules/BK/BK4/L04.html:94-148", "PASS",
    "Re-derived Prop 2.2 (reserves C0(rho-x), claims C0(1-x), theta=(rho-x)/(1-x)); Prop 2.4 (theta-1=(rho-1)/(1-x)); Prop 2.5 numerator (rho-y)(1-x)-(rho-x)(1-y)=(y-x)(rho-1); Prop 2.6 (theta-rho=x(rho-1)/(1-x)); Prop 2.7 floor argument. All hypotheses cited in each proof are in the statement (Prop 2.5 needs x,y<1 for denominators; Prop 2.6 needs x<1). Grid checks: 0 violations (recompute_r6.txt).")
row("BK4b-math-L05-props", "2.2 (a)/(b)/(c) and proofs", "course/modules/BK/BK4/L05.html:84-154; :482-483; cards BK4-c083, BK4-c084", "PASS",
    "Re-derived Prop 2.1 (E[1_F]=P(F)), Prop 2.2 (sum over 8 patterns of P(x)x_i = p), Prop 2.4 (proof of 2.1 uses only finite space, A1, A2), Prop 2.5 (Var(1_F)=p(1-p); covariance zero under A3; Var4-Var3 = 2 kappa^2 p(1-p) sum l_i l_j; zero iff at most one l_i positive), Prop 2.6 (C=0 iff no failure; (1-p)^3 < 1-p). Hypotheses named in each statement cover what each proof uses. 3000-trial sweep: 0 violations. Prop 2.2 title at :94 ('closed form of Proposition 2.1') is consistent with Prop 2.1.")
row("BK4b-math-L04-R-problems", "2.2 (R1-R3 solutions)", "course/modules/BK/BK4/L04.html:428-433", "PASS",
    "R1 (:429, changed this round to 'For any ratio 0<=rho<rho*'): rho*=1/(1-h), every admissible share for rho*(1-h)=1 gives coverage >= 1, and any rho<rho* makes x=0 admissible with coverage rho(1-h)<1; 20/19 for h=1/20. R2 (:431): x*=(rho-c)/(1-c) satisfies 0<=x*<1, x*<=rho and theta=c; grid check 0 violations. R3 (:433): (Res0-m)/(C0-m) = (rho-x)/(1-x) with x=m/C0; x<=rho iff m<=Res0. All matched.")
row("BK4b-math-L05-R-problems", "2.2 (R1-R3 solutions)", "course/modules/BK/BK4/L05.html:449-469 (R1, R2, R3)", "PASS",
    "R1 (:453): Var4/Var3 = n for n=1..4 (exact check), E[C]=n p kappa l. R2 (:460): union bound gives P(U)<=3p, so no-fail in [5/8,7/8]; attainment: A4 gives 7/8; disjoint events with P(omega0)=5/8 and P(omega_i)=1/8 give 5/8 (sum 1, P(U)=3/8). R3 (:467): E[C] is a product of nonnegative factors, nondecreasing in each. All matched.")
row("BK4b-problems-L04-M-P-E", "2.2 (M/P/E solutions)", "course/modules/BK/BK4/L04.html:401-424", "PASS",
    "M1 2/3 (3/4 - 1/4 over 3/4); M2 1/3 with 3/5 < 1 (Prop 2.4); M3 9500; P1 identity; P2 theta<=rho with equality iff x=0 or rho=1; P3 (floor threshold) with 'a coverage strictly below 1 has a basis-point figure strictly below 10000' true; E1 6875 at x=21/25 with 220000/320000; E2 first value >=10600 is 10625 at x=1/5; E3 both sides -31/784 (recomputed exactly).")
row("BK4b-problems-L05-P-E", "2.2 (P/E solutions) and problem-set scope", "course/modules/BK/BK4/L05.html:370, :376-453 (P3 at :415-417 changed this round)", "PASS",
    "P3 (:415) now begins 'Under A1 and A2' and the solution (:417) uses P(0,0,0) of Prop 2.2, which needs A3 for the (1-p)^3 value, which the statement names ('under A3'). The round-5 defect (no A1 named) is fixed. M1 1500 (1/4*1000*6), M2 343/512 and 169/512, M3 1875, E1 2188 under the half-up rule, E2 19140625 = Prop 2.5 value, E3 343/512 vs 448/512 all re-derived. Intro at :370 ('printed output of Lab 1') matches the empirical problems.")
row("BK4b-lab-L04-statements", "2.5-labs (what the page says it prints)", "course/modules/BK/BK4/L04.html:157 and :356; tests/labs/BK4/lab-BK4-L04-1.py", "PASS",
    "L04:157 expectation: rho=19/20 has every computed coverage below 1 and omits 99/100; rho=21/20 has none below 1 and omits none. Printed output shows 6 computed rows and 1 omitted for 19/20, 7 and 0 for 21/20 with 'coverage below 1 in 0 computed rows'. Haircut check prints 20/19 (twin output). Identity and difference checks print True in both tables.")
row("BK4b-lab-L05-statements", "2.5-labs (what the page says it prints)", "course/modules/BK/BK4/L05.html:162 and :335; tests/labs/BK4/lab-BK4-L05-1.py", "PASS",
    "L05:162 expectations (4375/2 -> 2188; eight probabilities sum to one; 1875 for equal delays; 343/512 under A3, 7/8 under A4; equal means; larger variance under A4) each match a True or printed value in the twin output.")
row("BK4b-lab-docstrings-L04-other", "2.5-labs (docstrings)", "tests/labs/BK4/lab-BK4-L04-1.py:1-25, 30-80, 96-123, 127-163 (page :158-175, :186-189, :218-222, :283-288, :297-300)", "PASS",
    "Read every docstring and comment. Claims that the lab 'counts' omitted shares and prints the count (:12-13), 'exact Fraction' cents (:47), 'the floor of 10000 times the coverage, taken exactly' (:11), 'checks ... prints each check's result; it does not assert them' (:15-17) match the code and output. No assert statement in the twin.")
row("BK4b-lab-docstrings-L05", "2.5-labs (docstrings)", "tests/labs/BK4/lab-BK4-L05-1.py:1-22 (module docstring) and the functions", "PASS",
    "Module docstring (Parts A-D, comonotone and independent laws, 'Standard library only; no randomness and no network') matches the code and printed parts. The rounding sentence ('the only rounding ... is one step') matches round_half_up, which is called once in main().")
row("BK4b-misconceptions-L04-1-2", "2.2 (misconception prose)", "course/modules/BK/BK4/L04.html:391-392", "PASS",
    "Misconception 1 (:391): holds under A1-A3 at rho=1 (Prop 2.4), fails when the measured ratio is 1-h < 1 (Remark 4.1). Misconception 2 (:392): 19/40 = rho/2 and 9/10 = 9000 bps (Remark 2.8).")
row("BK4b-misconceptions-L05", "2.2 (misconception prose)", "course/modules/BK/BK4/L05.html:353-363", "PASS",
    "Misconception 1 (:355): same mean, variance changes unless at most one delay positive (Prop 2.5, 'kappa > 0 and 0<p<1'). Misconception 2 (:359): 169/512 vs 3p = 192/512, A4 gives p (Example 2.7). Misconception 3 (:363): 4375/2 with delays (1,2,4); 1875 with (2,2,2). All matched.")
row("BK4b-quiz-L04", "2.2 / 2.5 (quiz items and explanations)", "course/modules/BK/BK4/L04.html:452-531 (Q10 explanation at :529)", "FAIL",
    "Items 1-9 are correct and their explanations match the printed numbers and the statements (numeric answers 0.9, 11000, 9416, 1.0526315789 = 20/19 to ten places, all re-derived). Item 10's explanation (:529) says 'Remark 3.2 states that the lesson does not model the settlement period.' Remark 3.2 (:368) says 'This lesson does not model whether a shared record changes that period.' The explanation overstates the scope of Remark 3.2. The fieldset style attributes added this round (:457, :471, :485 and others) are presentational only.",
    "Change the explanation at L04.html:529 to: 'Remark 3.2 states that the lesson does not model whether a shared record changes the settlement period.'")
row("BK4b-quiz-L05", "2.2 / 2.5 (quiz items and explanations)", "course/modules/BK/BK4/L05.html:492-574", "PASS",
    "All ten items re-read. Answers 750 (1/4*1000*3), 343/512, 169, 2188 (Example 2.8), 'the same mean' (Props 2.1, 2.4), 'A4 larger variance' (Prop 2.5 with two positive delays), 'Section 4 gives no rate', 'Definition 1.1 names processes, people, systems and external events' match. Intro at :494 ('Finishing the quiz adds this lesson's cards') matches quiz.js addLessonCards (filters cards.json by lesson).")
row("BK4b-key-results-L04", "2.2 (key results table)", "course/modules/BK/BK4/L04.html:442-447", "PASS",
    "Seven rows match the proofs: Prop 2.2, 2.4, 2.5, 2.6, 2.7 statements; Remark 4.1 with its conditional. Grade T on each is consistent with proof on the page.")
row("BK4b-key-results-L05", "2.2 / grade legend (key results)", "course/modules/BK/BK4/L05.html:479-486", "PASS",
    "Rows 1-6 are T with proofs or arithmetic on the page; rows 7-8 (exact expected cost and variance ordering on SIMULATED parameters) are C naming Lab 1 Parts A/B and D, as rule 9 requires.")
row("BK4b-grades-claim-spans", "2.2 (grade spans)", "course/modules/BK/BK4/L04.html:94-153, 369-376; course/modules/BK/BK4/L05.html:84-154, 161-162, 477-486", "PASS",
    "Each data-grade=T span is on a proposition or remark with a proof on the page; lab-derived statements in L04 and L05 are not graded T (L05 key results 7-8 are C with the lab named).")
row("BK4b-why-length", "2.2 (why-it-matters)", "course/modules/BK/BK4/L04.html:52; course/modules/BK/BK4/L05.html:51", "PASS",
    "Each why paragraph states results that the page proves or labels as SIMULATED, in one paragraph, and its claims match the body (L04 Props 2.2, 2.4, Def 3.1; L05 Props 2.1, 2.4, 2.5).")
row("BK4b-banned-and-process-words", "2.2 (banned and process words)", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html; tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py; course/modules/BK/BK4/cards.json", "PASS",
    "Case-insensitive grep for builder, verifier, fixer, round, placeholder, TODO, TBD, architect, FINAL, ruling, planner, agent, claude, pending in both pages returned no match. The twins and cards were read in full with the same result.")
row("BK4b-notation", "2.4 (notation registry)", "notation/notation.json; course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html", "PASS",
    "Macros used by the pages: \\E, \\Prob, \\Var, \\Cov, \\indic (all registered in notation.json macros). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur in L04 or L05. Local letters (rho, theta, h, x, p, kappa, ell, C, D, Res, Omega) are defined on the page where first used. L05:64 says ell is not the settlement cycle d of L01.")
row("BK4b-hours", "2.8 (hours arithmetic)", "course/modules/BK/BK4/L04.html:2, :35; course/modules/BK/BK4/L05.html:2, :34; course/modules/BK/BK4/index.html:29, :140", "PASS",
    "data-hours=7 on L04 and L05, and the other lessons also 7 (grep). Hub data-hours-lessons=35 = 5 x 7; data-hours-project=15; total 50 (index.html:29; project.html:34). Matches plan section 1 and section 0.2.")
row("BK4b-cards-L04-L05-scan", "2.10 (cards)", "course/modules/BK/BK4/cards.json (19 L04 cards; 15 L05 cards)", "PASS",
    "All 34 cards read individually against the current lesson text: L04 BK4-c059-c076, c093, c097; L05 BK4-c077-c090, c094, c098, c100. Each card's numbers and hypotheses match the lesson (BK4-c074 updated this round to match L04:376 and :391; BK4-c075 uses the ratio 1/2 admissibility condition).")
row("BK4b-cards-duplicates", "2.10 (cards duplicates)", "course/modules/BK/BK4/cards.json (99 cards)", "PASS",
    "Python: 99 cards, no duplicate ids and no duplicate fronts across the file. Near-overlap of BK4-c088 and BK4-c100 (same mean fact asked as a misconception and as a proposition) is distinct in hypotheses and wording.")
row("BK4b-cards-grades-basis", "2.10 (card grades and bases)", "course/modules/BK/BK4/cards.json (L04 and L05 cards)", "PASS",
    "Cards graded T name a proposition, remark or example on the page as basis. Cards graded C (BK4-c086, c087, c094) name Lab 1 Part B or D with SIMULATED parameters. BK4-c090 is graded T with a basis that also names Lab 1 Part C: the figure 1875 is the closed form of Prop 2.1 (T), and the lab only prints it, so the grade is consistent.")
row("BK4b-dag-prose-terms", "2.7 (DAG and prose terms)", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html", "PASS",
    "check_dag PASS. L04 links only settlement-cycle (L01) and bank-money-creation (FC1, in the closure per plan section 1, yaml:373). L05 links settlement-cycle (L01). No CCP, margin or netting concept is used in L04/L05 prose by name (the only hits are the L03 and project link titles in the navigation).")
row("BK4b-registry-citation-consistency", "2.1 (registry consistency)", "course/modules/BK/BK4/L05.html:347, :579; references/references.json:2815", "PASS",
    "The cited key exists, the title and URL match the record, the locator 'index page: title and issuer' matches the index-level claim, and the live URL returns the same title today. The record's used_by does not yet list BK4 (references.json:2840); this is a registry flag and does not change the citation.")
row("BK4b-L04-assumption4-scope", "2.2 (scope claim: uses listed)", "course/modules/BK/BK4/L04.html:79, :82, :85", "FAIL",
    "L04:79 says 'Assumption 4 is stated here, and its uses are listed after it.' L04:85 then lists its uses as 'Remark 4.1, Problem R1, Misconception 1, the key-results table, quiz items 8 and 9 and the Lab 1 haircut check'. Assumption 1 (L04:82) also uses Assumption 4 ('with reserves used at the value that Assumption 4 gives them'), and Assumption 1 is not in the list. The claim that the list is complete is false. Definition 1.2 (L04:69) also refers to Assumption 4 as a pointer.",
    "Add 'Assumption 1 (the valuation clause)' to the list at L04.html:85, or reword L04.html:79 so it does not say the uses are complete.")
row("BK4b-L04-seeded_path-docstring", "2.5-labs (docstring vs lesson)", "course/modules/BK/BK4/L04.html:218-225 (tests/labs/BK4/lab-BK4-L04-1.py:217-225)", "PASS",
    "Docstring: the sampled shares are in increasing order, then 99/100 is appended, and 99/100 repeats a sampled share if present. This is what the printed seed-7 path shows (7/100 1/10 1/5 21/50 51/100 21/25 99/100). Recomputed sample from random.Random(7): [7,10,20,42,51,84] (recompute_r6.txt).")
row("BK4b-L04-haircut-docstring", "2.5-labs (docstring vs lesson)", "course/modules/BK/BK4/L04.html:283-294 (twin :283-294)", "PASS",
    "haircut_check docstring: 1/(1-h) and the coverage at share 1/2 for a ratio just below it (21/20) and at it (20/19). Printed output: 20/19; 399/400 and 199/200 (9950 bps); 1 and 10000 bps. Matches.")
row("BK4b-L04-misconception3", "2.2 (misconception 3)", "course/modules/BK/BK4/L04.html:393", "PASS",
    "Coverage stays at rho only when x=0 or rho=1 (Prop 2.6); falls for rho<1 and rises for rho>1 (Prop 2.5); both directions in the two printed tables (Lab 1 output lines 320-347).")
row("BK4b-cards-c076", "2.10 (card vs lesson)", "course/modules/BK/BK4/cards.json (BK4-c076); course/modules/BK/BK4/L04.html:131-137", "PASS",
    "Card back 'Only when x = 0 or rho = 1' and 'at most rho when rho<=1, at least rho when rho>=1' match Prop 2.6 (:131-137).")
row("BK4b-L04-admissible-undefined", "5 (terms before definition)", "course/modules/BK/BK4/L04.html:90 (definition) and first use after it", "PASS",
    "'Admissible for a ratio' is first used in the text at :90, inside its own definition (Definition 2.1), and used afterwards in :95-152 and quiz items. No earlier use.")
row("BK4b-L04-remark3.2-FC1-paraphrase", "2.1 (attribution)", "course/modules/BK/BK4/L04.html:368; course/modules/FC/FC1/L01.html:67, :73, :81", "PASS",
    "The quoted definition text in L04:368 is identical to FC1 L01.html:81 ('the increase in total deposits that results when the bank makes a loan and the proceeds are deposited back at the same bank'). FC1 L01.html:67 is the Section 2 heading; :72 is Assumption 2.0; :73 states deposits are the bank's liabilities. Locators match. FC1 is in BK4's prerequisite closure (plan section 1).")
row("BK4b-L04-def1.2-section4-claim", "2.2 (scope pointer)", "course/modules/BK/BK4/L04.html:69", "PASS",
    "'Section 4 treats only a constant haircut to face value (Assumption 4)' is true: Section 4 (Remark 4.1) treats a constant haircut h.")
row("BK4b-L05-why-overreach", "2.2 (why-it-matters scope)", "course/modules/BK/BK4/L05.html:51", "PASS",
    "'Proposition 2.1 shows that the mean does not depend on how failures are linked' (Prop 2.1 uses no joint law), 'Proposition 2.4 gives the same mean when all three trades fail together' (A4), and Prop 2.5 (variance inequality under 0<p<1, kappa>0) match the statements. 'Lab 1 (Section 3) checks Propositions 2.2, 2.4 and 2.5' is accurate because the twin prints True for the enumeration equals closed form, the mean equality, and the variance inequality.")
row("BK4b-L05-why-terms", "5 (terms before definition)", "course/modules/BK/BK4/L05.html:51 (first use), :55, :58 (Def 1.1), :64 (Def 1.2), :67-73 (Assumption 1.3 and A1-A4)", "PASS",
    "'Operational risk' is defined for this unit in the why paragraph itself and in Definition 1.1 (:58). 'Settlement failure' and 'delay' are in Definition 1.2 (:64). 'A3' and 'A4' are named in the why paragraph with the explicit pointer 'Assumption 1.3', and defined at :72-73. The forward pointer is explicit, so no undefined term is used.")
row("BK4b-L05-why-ungraded-claim", "2.2 / grades", "course/modules/BK/BK4/L05.html:51", "PASS",
    "The why paragraph states results only as theorem names (grade T in the body) and the lab as SIMULATED; it makes no ungraded empirical claim.")
row("BK4b-L05-M2-citation", "2.2 (M2 solution)", "course/modules/BK/BK4/L05.html:383-386", "PASS",
    "M2 gives (7/8)^3 = 343/512 and 169/512 for independent failures; Lab 1 Part B prints 343/512 for the all-ok pattern and 169/512 for at least one failure (lab output lines 309 and 322-323).")
row("BK4b-r2-L05-numbering", "5 (numbering)", "course/modules/BK/BK4/L05.html:79-152, :545, :563", "PASS",
    "Definition 2.1, Proposition 2.2, Remark 2.3, Propositions 2.4-2.6, Examples 2.7-2.8 use one counter in order. Quiz explanations cite 2.1, 2.2, 2.4, 2.5, 2.6, Example 2.7 and 2.8 with matching statements.")
row("BK4b-r2-L05-why-dependence-attribution", "2.1 (attribution)", "course/modules/BK/BK4/L05.html:51", "PASS",
    "The why paragraph attributes no external result; it refers to Propositions on the page and to Lab 1 only.")
row("BK4b-r2-L05-M1-model", "2.2 (M1 model)", "course/modules/BK/BK4/L05.html:374-379", "PASS",
    "Model statement (three trades, each p=1/4 under A1, kappa=1000, delays 2, 3, 1) matches the M1 solution, which gives 1500 cents by Prop 2.1 under either joint law.")
row("BK4b-r2-title-casing", "5 (titles)", "course/modules/BK/BK4/L04.html:6, :36; course/modules/BK/BK4/L05.html:6, :35; course/modules/BK/BK4/index.html:142-146; course/modules/BK/BK4/project.html:37", "PASS",
    "Titles 'Stablecoins and Tokenization' and 'Operational Risk in Market Infrastructure' match the hub and lesson map text.")
row("BK4b-r3-L05-uses-metadata", "2.1 (uses metadata)", "course/modules/BK/BK4/L05.html:37", "PASS",
    "'settlement cycle (L01, Definition 1.2)' matches course/modules/BK/BK4/L01.html:63 (Definition 1.2, settlement cycle).")
row("BK4b-grade-legend-L04", "2.9 (grade legend)", "course/modules/BK/BK4/L04.html:47 (and L05.html:46)", "PASS",
    "Legend lists T, A, B, C, D, X with the same meanings as used in the page. C is used for single-sample SIMULATED results (L05 key results 7-8).")
row("BK4b-L04-bps-convention-note", "2.2 (bps convention)", "course/modules/BK/BK4/L04.html:69 vs :90", "PASS",
    "Ratio bps floor(10000 rho) (:69) and coverage bps floor(10000 theta) (:90) are the same rule, computed exactly, in both places.")
row("BK4b-L05-quiz-prop21-scope", "2.2 (quiz item 2 explanation)", "course/modules/BK/BK4/L05.html:503 and :506-508", "PASS",
    "Item 2 explanation: E[C] = p kappa ell = 1/4 * 1000 * 3 = 750 with one trade, from the indicator expectation under A1 (Prop 2.1 with one trade). Re-derived.")
row("BK4b-L04-amounts-integer-cents-scope", "2.2 (scope of integer cents)", "course/modules/BK/BK4/L04.html:56, :65, :376", "PASS",
    "Line 56 now limits 'integer cents' to the claims and to the reserves at face value, and says 'the measured reserves of Remark 4.1 need not be whole cents'. Definition 1.2 (:65) says face values in integer cents. Remark 4.1 (:376) measures reserves at (1-h) of face value, which need not be whole cents. Consistent. Round-5 defect fixed.")
row("BK4b-L04-assumption1-face-value-conflict", "2.2 (assumption consistency)", "course/modules/BK/BK4/L04.html:82, :85, :376", "PASS",
    "Assumption 1 (:82) now says reserves are used at the value that Assumption 4 gives them, 'which is face value when Assumption 4 is not assumed'. Prop 2.2 assumes Assumptions 1-3 without 4 (:95), so the proof's face-value step (:100) is valid. Remark 4.1 (:376) assumes 1-3 and 4 and applies Prop 2.2 with rho(1-h). No conflict remains. The residual omission of Assumption 1 from the list at :85 is a separate row (BK4b-L04-assumption4-scope).")
row("BK4b-L04-path-increasing-order", "2.2 (lab path description)", "course/modules/BK/BK4/L04.html:382 vs lab docstring L04.html:218-222", "PASS",
    "Line 382 now says 'non-decreasing order, and the printed seed-7 path is strictly increasing'. The docstring (sample increasing, then 99/100 that may repeat) makes the path non-decreasing. The printed path (output line 319: 7/100 1/10 1/5 21/50 51/100 21/25 99/100) is strictly increasing. Round-5 defect fixed.")
row("BK4b-twin-page-exact", "2.5-labs (page code and expected block equal the twin)", "tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py; course/modules/BK/BK4/L04.html:158-317; course/modules/BK/BK4/L05.html:163-303", "PASS",
    "Decoded the data-run code block of each page and compared with the twin file (" + SC + "twin_vs_page.py, output " + SC + "twin_vs_page.txt): page code equals the twin after stripping the final newline; exact equality is False only because the page block ends before the newline that the file ends with. The expected block equals the twin's stdout under the same rule.")
row("BK4b-slice-delta", "delta since round-5 pin", "git diff 7376a5e216c1e6d99becc76b4cd64028f5b55d3f 4bd8cb94 -- course/modules/BK/BK4/L04.html L05.html cards.json tests/labs/BK4", "PASS",
    "Read every hunk in slice b. L04.html: :56 (integer cents scope), :69 (Section 4 pointer), :82 (Assumption 1 valuation clause), :85 unchanged list, :376 unchanged, :382 (path order), :429 (R1 solution, 'For any ratio 0<=rho<rho*'), quiz fieldset style attributes (presentational). L05.html: :94 (Prop 2.2 title), :370 (problem-set intro), :415 and :417 (P3). cards.json: BK4-c074 front and back (plus L02/L03 cards outside this slice). The twins are unchanged in this delta. Every changed subject re-verified this round.")

ids = [r["id"] for r in R]
assert len(ids) == len(set(ids)), "duplicate ids"
nonpass = [r["id"] for r in R if r["status"] != "PASS"]
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "BK4",
    "slice": "BK4-b",
    "round": 6,
    "verifier": "Haiku independent verifier, BK4-b round 6 (did not build BK4; sixth verification of slice b)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f (round-5 pin; fragment /Users/billyribeiro/.fanout/frags/E-BK4-b.round5.json). Slice-b files changed since: L04.html (lines 56, 69, 82, 85, 376, 382, 426-429 R1 solution, quiz fieldset style attributes), L05.html (lines 94 title, 370 intro, 415 and 417 P3), cards.json (BK4-c074 front and back, plus L02/L03 cards outside slice b). tests/labs/BK4/lab-BK4-L04-1.py and lab-BK4-L05-1.py unchanged in this delta.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-BK4-b (detached at 4bd8cb9, .venv symlinked)",
    "scratch": "/tmp/bk4b-r6/ (curl output only); command outputs archived in ledgers/BK4/scripts/BK4-b-r6/",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if nonpass else "PASS",
    "rows": R,
    "mutants": [],
    "registry_flags": [
        "bisndbasel (references/references.json:2815) has used_by [\"BK1\"] (references.json:2840). BK4 L05.html:347 and :579 cite it. The plan (section 7.1, Q12) says used_by must gain BK4 at integration. Because used_by lacks BK4, tools/verify_refs.py --unit BK4 does not re-verify this citation (2 of 560 entries). The architect should run the registry tool to add BK4."
    ],
    "freshness_flags": [
        "bisndbasel URL https://www.bis.org/committees/bcbs/standards re-fetched with plain curl on 2026-11-04: HTTP 200, title identical to the registry title. Recorded in " + SC + "curl_bisndbasel.txt."
    ],
    "notes": (
        "Slice b = L04 and L05 pages and the two lab twins. Read in full: L04.html lines 1-549 and L05.html lines 1-592 (every sentence, every expected block line, every quiz explanation), both twins (all lines), and all 34 L04/L05 cards. Delta since round 5 read hunk by hunk; every row re-verified this round with no carry-forward. "
        "Not a finding, recorded for the architect: (a) the page expected blocks omit the trailing newline that print() emits, so exact-string comparison fails by one newline and stripped comparison passes; (b) L05:51 says Lab 1 checks Props 2.2, 2.4, 2.5, while L05:158 says it checks 2.2 and prints the quantities that 2.4-2.6 compare; both are accurate about the printed True lines, the wording differs; (c) the quiz intro at L05:494 (finishing the quiz adds cards) matches quiz.js addLessonCards, read from source, not run in a browser. "
        "Mutants: none, because slice b has no grader; the lab twins are demonstrations (FINAL-ARCHITECT-RULINGS 9 as cited in the plan). "
        "Could not check: (1) no Pyodide runtime was run directly; page_smoke.py (the tool's own harness) passed for both pages; (2) the SEC T+1 rule and any settlement-date fact are not in slice b (no check made); (3) the Duffie and Zhu abstract and the CPMI index are not cited in slice b; (4) the Basel III operational-risk section was not read, and the page says so (L05:347, :579); (5) the FC1 lesson was checked only at the quoted and cited lines (FC1 L01.html:67, :72-73, :81), not in full; (6) L01 was checked only at Definition 1.2 (L01.html:63)."
    ),
    "summary": (
        "BK4-b round 6: verdict " + ("FAIL" if nonpass else "PASS") + ". Rows " + str(len(R)) + " (pass=" + str(counts["PASS"]) + ", fail=" + str(counts["FAIL"]) + ", unverifiable=" + str(counts["UNVERIFIABLE"]) + "). Non-PASS: " + ", ".join(nonpass) + ". Round-5 FAILs BK4b-L04-amounts-integer-cents-scope, BK4b-L04-assumption1-face-value-conflict, BK4b-L04-path-increasing-order and BK4b-problems-L05-P-E are fixed and re-verified PASS. No mutants (labs and prose only)."
    ),
}
out = "ledgers/BK4/BK4-b.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, counts, "nonpass:", nonpass)
