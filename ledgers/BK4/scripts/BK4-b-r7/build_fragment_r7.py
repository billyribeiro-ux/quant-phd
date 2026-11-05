"""Builds ledgers/BK4/BK4-b.json for verifier round 7 (slice b: L04, L05 and their lab twins).

Run from the checkout: .venv/bin/python ledgers/BK4/scripts/BK4-b-r7/build_fragment_r7.py
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = "ledgers/BK4/scripts/BK4-b-r7/"

def row(rid, check, location, evidence, status="PASS", fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    row("BK4b-gate-check-pages", "2.9-structure", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html",
        f"tools/check_pages.py --unit BK4 -> 'check_pages BK4: PASS', exit 0 ({S}check_pages.txt)."),
    row("BK4b-gate-check-dag", "2.9-dag", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html; course/concepts.html",
        f"tools/check_dag.py --unit BK4 -> 'check_dag BK4: PASS', exit 0 ({S}check_dag.txt). Links in L04: settlement-cycle (L01.html#def-settlement-cycle) and bank-money-creation (concepts.html, FC1, in closure). L05 links settlement-cycle only. The L04 'Previous' link text (L04.html:542) equals the L03 h1 (L03.html:35). Plain-prose names of out-of-closure concepts found by grep: 'haircut' (D2, prose), 'variance' (D10, prose), 'credit default' (L05.html:569, a quiz distractor only)."),
    row("BK4b-gate-check-projects", "2.6-projects", "course/modules/BK/BK4/project.html",
        f"tools/check_projects.py --unit BK4 -> 'check_projects BK4: PASS', exit 0 ({S}check_projects.txt). Project content is slice c; recorded for the gate only."),
    row("BK4b-run-labs", "2.5-labs", "course/modules/BK/BK4/L04.html:155-357; course/modules/BK/BK4/L05.html:160-336",
        f"tools/run_labs.py --unit BK4 -> 'run_labs BK4: PASS (8/8)', exit 0 ({S}run_labs.txt)."),
    row("BK4b-twin-isolated-run", "2.5-labs", "tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py",
        f"{S}twin_vs_page.py run as python -I -W error from the checkout ({S}twin_vs_page.txt): L04 exit 0, stderr empty; L05 exit 0, stderr empty. Stripped stdout equals the page expected block for both (exact string comparison differs only by the trailing newline that print() adds and the expected block omits; see BK4b-twin-page-exact)."),
    row("BK4b-twin-lint", "2.5-labs", "tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py",
        f"ruff check -> 'All checks passed!' ({S}ruff_check.txt); ruff format --check -> '2 files already formatted' ({S}ruff_format.txt); mypy --no-incremental -> 'Success: no issues found in 2 source files' ({S}mypy.txt)."),
    row("BK4b-pytest-labs", "2.5-labs", "tests/test_labs.py",
        f"pytest tests/test_labs.py -k 'BK4 and (L04 or L05)' -v -> '2 passed, 357 deselected' ({S}pytest_labs_verbose.txt)."),
    row("BK4b-page-smoke", "2.9-structure", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html",
        f"tools/page_smoke.py --unit BK4 --pages L04 L05 -> 'page_smoke modules/BK/BK4/L04.html: PASS', 'page_smoke modules/BK/BK4/L05.html: PASS', 'page_smoke BK4: PASS' ({S}page_smoke.txt). This is the tool's own harness; no separate Pyodide session was run."),
    row("BK4b-verify-refs", "2.1-citations", "references/references.json (bisndbasel); course/modules/BK/BK4/L05.html:347",
        f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' ({S}verify_refs_offline.txt). tools/verify_refs.py --unit BK4 -> 'live re-verification of BK4: 2 of 560 entries, 0 problems' ({S}verify_refs_unit.txt)."),
    row("BK4b-citation-bisndbasel", "2.1-citations", "course/modules/BK/BK4/L05.html:347, :579; references/references.json:2815-2822",
        f"Registry title 'Basel III: international regulatory framework for banks | Bank for International Settlements', url https://www.bis.org/committees/bcbs/standards (references.json:2815-2822). Plain curl -sS -L on 2026-11-04: HTTP 200, final URL unchanged, <title> identical ({S}curl_bisndbasel.txt). The page's locator 'index page: title and issuer' supports only the index-level sentence at L05.html:347; the operational-risk section is not stated (L05.html:347, :579)."),
    row("BK4b-cmd-recompute", "2.2-numbers", "ledgers/BK4/scripts/BK4-b-r7/recompute_r7.py",
        f"Independent exact-Fraction script, no import of the lab: python -I -W error {S}recompute_r7.py -> 156 PASS lines, 'ALL OK' ({S}recompute_r7.txt). Covers every prose number, quiz numeric answer, worked example, problem solution and both lab tables that this slice states."),
    row("BK4b-numbers-L04-prose", "2.2-numbers", "course/modules/BK/BK4/L04.html:52, :56-69, :72-75, :90, :95, :151-153, :356, :376, :392-393, :405-406, :420-424, :429-433",
        f"Each prose number recomputed in {S}recompute_r7.txt: 1,900,000 and 2,100,000 cents (Remark 1.3, :74); 9/10, 11/10, 113/120 and 9416 (Remark 2.8, :152); 19/40 (:392); 9500 (M3); 6875 at x=21/25 and 10625 at x=1/5 (E1, E2); -31/784 (E3); 20/19 and 399/400, 199/200 (9950 bps) and 10000 bps (Lab haircut check). Coverage bps floors are exact."),
    row("BK4b-numbers-L04-lab-table", "2.2-numbers", "course/modules/BK/BK4/L04.html:318-355 and :356",
        f"All computed rows of both tables (6 for 19/20 with 1 omitted; 7 for 21/20 with 0 omitted), their reserves, claims, coverage and bps values, the 15 and 21 pair counts, and the haircut rows, match the recomputation ({S}recompute_r7.txt, 'L04 19/20 bps list', 'L04 21/20 bps list') and the stdout of the twin (twin_vs_page.txt)."),
    row("BK4b-numbers-L05-prose", "2.2-numbers", "course/modules/BK/BK4/L05.html:153, :162, :335, :355, :359, :363, :392, :428, :435-436, :442, :453, :458-460",
        f"Recomputed in {S}recompute_r7.txt: 4375/2 = 2187.5 (Example 2.8, :152-153); 2188 half-up; 21.88 dollars; 343/512, 169/512, 192/512 = 3/8, 448/512 = 7/8; 1875 = 3*(1/8)*2500*2; 19140625 = 2*2500^2*(7/64)*14 (E2, :435); 133984375/4 and 57421875/4 variances; R1 ratio n; R2 bounds 5/8 and 7/8."),
    row("BK4b-lab-table-L05", "2.2-numbers", "course/modules/BK/BK4/L05.html:304-334 and :335",
        f"Printed lines 304-334 of the expected block equal the twin's stdout ({S}twin_vs_page.txt). The values equal the recomputation: 'L05 probabilities list', 'L05 comonotone variance 133984375/4', 'L05 independent variance 57421875/4', 'L05 Part D no-cost' checks (all PASS in {S}recompute_r7.txt)."),
    row("BK4b-math-L04-props", "2.4-math", "course/modules/BK/BK4/L04.html:94-153",
        f"Re-derived Prop 2.2 (reserves C0(rho-x), claims C0(1-x), theta=(rho-x)/(1-x)); Prop 2.4 (theta-1=(rho-1)/(1-x)); Prop 2.5 numerator (rho-y)(1-x)-(rho-x)(1-y)=(y-x)(rho-1); Prop 2.6 (theta-rho=x(rho-1)/(1-x)); Prop 2.7 (floor threshold). Hypotheses (1)-(3) of each are stated and used ({S}recompute_r7.txt, 'Prop2.6 theta-rho identity', 'Prop2.4 theta-1 identity', 'Prop2.5' and 'Prop2.7' checks). Remark 2.3 (x<=rho needed for nonnegative reserves) matches the proof of 2.2 at :101-103."),
    row("BK4b-math-L05-props", "2.4-math", "course/modules/BK/BK4/L05.html:84-154; course/modules/BK/BK4/L05.html:467; cards BK4-c083, BK4-c084",
        f"Re-derived Prop 2.1 (E[1_F]=P(F) on a finite space); Prop 2.2 (sum over the 8 patterns of P(x)x_i = p); Prop 2.4 (A4 gives the same marginals); Prop 2.5 (Var(1_F)=p(1-p); covariance zero under A3; Var4-Var3 = kappa^2 p(1-p)[(sum l)^2 - sum l^2] = 2 kappa^2 p(1-p) times the sum over pairs i<j of l_i l_j, checked on 20 random cases in {S}recompute_r7.py 'Prop2.5 identity'); Prop 2.6 ((1-p)^3 < 1-p). Hypotheses of 2.5 and 2.6 are stated (A3 vs A4, l_i>=1, kappa>=1)."),
    row("BK4b-math-L04-R-problems", "2.4-math", "course/modules/BK/BK4/L04.html:428-433",
        f"R1 (:429): rho*=1/(1-h); for rho*(1-h)=1 every share is admissible; any rho<rho* makes x=0 admissible with measured coverage rho(1-h)<1 ({S}recompute_r7.txt 'R1 rho* = 20/19', 'R1 measured coverage'). R2 (:431): x*=(rho-c)/(1-c) satisfies 0<=x*<=rho<1 and returns coverage c ('R2 theta at x*', 'R2 x* <= rho'). R3 (:433): whole-cent coverage (Res0-m)/(C0-m) equals (rho-x)/(1-x) with x=m/C0 ('R3 coverage identity')."),
    row("BK4b-math-L05-R-problems", "2.4-math", "course/modules/BK/BK4/L05.html:449-469",
        f"R1 (:453): Var4/Var3 = n for n=1..4 ('R1 Var4/Var3 = n'), E[C]=n p kappa l. R2 (:457): union bound gives P(U)<=3p=3/8, so no-fail in [5/8,7/8]; 7/8 attained under A4; 5/8 attained by the disjoint construction with P(omega0)=5/8 and P(omega_i)=1/8 ('R2 union bound 3p', 'R2 lower bound 5/8', 'R2 total prob of disjoint outcome'). R3 (:463-469): monotonicity of p*kappa*sum(l) on the nonnegative domain; the proof of Prop 2.1 uses the marginals and the finite space, A2 only as constants (wording changed this round at :467, re-read, sound)."),
    row("BK4b-problems-L04-M-P-E", "2.4-math", "course/modules/BK/BK4/L04.html:401-424",
        f"M1 2/3 (two forms); M2 1/3 with 3/5<1 (Prop 2.4); M3 9500 (floor of 10000*19/20). P1 identity; P2 theta<=rho with equality iff x=0 or rho=1; P3 floor threshold and 'strictly below 10000'. E1: printed bps 9462, 9444, 9375, 9137, 8979, 6875; lowest 6875 at x=21/25 with 220000/320000 ({S}recompute_r7.txt). E2: 10537, 10555, 10625 ...; first >=10600 is 10625 at x=1/5 ('L04 21/20 bps list'). E3: -31/784 both sides ('E3 left', 'E3 right'). R1-R3 are at :428-433 (row BK4b-math-L04-R-problems)."),
    row("BK4b-problems-L05-P-E", "2.4-math", "course/modules/BK/BK4/L05.html:370, :374-456",
        f"M1 1500 cents ('M1 mean 1/4*1000*6'); M2 343/512 and 169/512; M3 1875 ('Misc3 mean', 'Part C'). P1 (indicator expectation) and P2 (covariance step uses A3 only) are proofs re-read. P3 (:413-417) now names 'Under A1 and A2' and uses A3 and A4 as the statement names them; the solution's P(0,0,0)=(1-p)^3 needs A3 and is stated under A3 ('Prop2.6 (7/8)^3 = 343/512'). E1 4375/2 -> 2188 (Part B). E2 difference 19140625 = Prop 2.5 value ('L05 E2 difference', 'L05 E2 Prop 2.5 value'). E3 448/512 = 7/8 ('L05 E3 A4 no-fail 448/512')."),
    row("BK4b-lab-L04-statements", "2.5-labs", "course/modules/BK/BK4/L04.html:157 and :356; tests/labs/BK4/lab-BK4-L04-1.py",
        f"Hypothesis (:157): rho=19/20 has every computed coverage below 1 and omits 99/100; rho=21/20 has none below 1 and omits none. Printed output: rho=19/20 computed rows 6, omitted 1, coverage below 1 in 6; rho=21/20 computed 7, omitted 0, below 1 in 0 (twin_vs_page.txt; recompute_r7.txt 'L04 rho 19/20 computed rows', 'L04 rho 21/20 omitted'). Identity, sign rule and difference identity printed True for both tables."),
    row("BK4b-lab-L05-statements", "2.5-labs", "course/modules/BK/BK4/L05.html:162 and :335; tests/labs/BK4/lab-BK4-L05-1.py",
        "Each prediction at L05.html:162 (4375/2 -> 2188; eight probabilities sum to one; 1875 for equal delays; 343/512 under A3 and 7/8 under A4; equal means; larger variance under A4) matches a True or printed value in the expected block at L05.html:304-334."),
    row("BK4b-lab-docstrings-L04-other", "2.5-labs", "tests/labs/BK4/lab-BK4-L04-1.py:1-25, 30-80, 96-123, 127-163 (page :158-175, :186-189, :218-222, :283-288, :297-300)",
        "Read every docstring and comment. 'counts omitted shares and prints the count' (print_path_table prints 'omitted rows'); 'does not assert them' (the only 'assert' token is in this docstring, no assert statement exists); cents are int (cents() raises otherwise); 'the floor of 10000 times the coverage, taken exactly' (math.floor(BPS*coverage) on a Fraction); seeded_path docstring matches the code and the printed path (recompute_r7 'L04 lab path')."),
    row("BK4b-lab-docstrings-L05", "2.5-labs", "tests/labs/BK4/lab-BK4-L05-1.py:1-22 (module docstring) and the functions",
        "Module docstring Parts A-D matches the print statements in main(). 'Standard library only; no randomness and no network' (imports: itertools, math, fractions). 'The only rounding ... one step' (round_half_up is called once, on the closed form). 'Every probability is an exact Fraction' and 'Every cost is an integer number of cents, except an expected cost' (pattern_cost_cents returns int; mean returns Fraction)."),
    row("BK4b-misconceptions-L04-1-2", "2.9-structure", "course/modules/BK/BK4/L04.html:389-393",
        "Misconception 1 (:391): holds under A1-A3 at rho=1 (Prop 2.4), fails when reserves are measured at (1-h) with h>0 (Remark 4.1; measured ratio 1-h<1). Misconception 2 (:392): 19/40 = rho/2 and 9/10 = 9000 bps (Remark 2.8). Misconception 3 (:393): see BK4b-L04-misconception3."),
    row("BK4b-misconceptions-L05", "2.9-structure", "course/modules/BK/BK4/L05.html:351-368",
        "Misconception 1: same mean under both laws (Props 2.1, 2.4); variance changes unless at most one delay is positive (Prop 2.5); Part D prints 4375/2 under both. Misconception 2: 169/512 under A3 vs 3p = 192/512 (Example 2.7); under A4 the chance is p. Misconception 3: E[C] depends on kappa and every l_i (Prop 2.1); Part B 4375/2 and Part C 1875 ({S}recompute_r7.txt)."),
    row("BK4b-quiz-L04", "2.9-structure", "course/modules/BK/BK4/L04.html:453-531 (Q10 explanation at :529)",
        "PREVIOUSLY FAIL (round 6): the Q10 explanation claimed Remark 3.2 says the lesson does not model the settlement period, which is not Remark 3.2's text. Round-7 fix is present at L04.html:529: 'Remark 3.2 states that the lesson does not model whether a shared record changes the settlement period.' Remark 3.2 (L04.html:367) reads 'This lesson does not model whether a shared record changes that period.' Items 1-9 re-read: answers (rho-x)/(1-x); 0.9; exactly 1; 11000; falls; 9416; payments would exceed reserves; below 1; 1.0526315789 = 20/19 (recompute_r7); explanations match the printed numbers and statements."),
    row("BK4b-quiz-L05", "2.9-structure", "course/modules/BK/BK4/L05.html:493-574",
        "All ten items re-read: answers and explanations match the lesson. Item 2 (750 = 1/4*1000*3, Prop 2.1 with one trade), item 3 (343/512), item 4 (169), item 5 (same mean; explanation at :531 now reads 'uses only the marginal probabilities and the fixed costs, so it applies under A4 as under A3'), item 6 (A4 larger; difference positive when two delays are positive), item 7 (2188, Example 2.8), item 8 (A3, Prop 2.2), item 9 (no rate; Section 4), item 10 (Def 1.1). 'Only' at :531 is not a defect: the finite space, a standing hypothesis under both laws, is not in the list, and the claim concerns the joint law."),
    row("BK4b-key-results-L04", "2.3-grades", "course/modules/BK/BK4/L04.html:438-447",
        "Seven rows match the proofs and remarks: Prop 2.2, 2.4, 2.5, 2.6, 2.7; Remark 4.1 with its conditional; R1 cited. Grade T on each is consistent with the proof on the page."),
    row("BK4b-key-results-L05", "2.3-grades", "course/modules/BK/BK4/L05.html:474-486",
        "Rows 1-6 are T with proofs or arithmetic on the page; rows 7-8 (exact expected cost and the variance comparison on SIMULATED parameters) are C naming Lab 1 Parts A/B and D, as the grade rules require."),
    row("BK4b-grades-claim-spans", "2.3-grades", "course/modules/BK/BK4/L04.html:94-153, 367-376; course/modules/BK/BK4/L05.html:84-154, 161-162, 477-486",
        "Each data-grade=T span is on a Proposition, Remark or Example with a proof or arithmetic on the page (Remark 4.1 at L04.html:376 is the T span for theta_h). Lab-derived statements are not graded T (L05 key results 7-8 are C with Lab 1 named)."),
    row("BK4b-why-length", "2.9-structure", "course/modules/BK/BK4/L04.html:52; course/modules/BK/BK4/L05.html:51",
        "Word count of the why-it-matters paragraphs (python, tags stripped): L04 119 words, L05 117 words, both at most 120. Each states only results that the page proves or labels SIMULATED, and the claims match the body (L04 Props 2.2, 2.4, Def 2.1; L05 Props 2.1, 2.4, 2.5, Lab 1)."),
    row("BK4b-banned-and-process-words", "2.9-structure", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html; tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py; course/modules/BK/BK4/cards.json",
        "Case-insensitive grep for builder, verifier, fixer, round (as a word), placeholder, TODO, TBD, architect, FINAL, ruling, planner, agent, claude, pending, lorem, obviously, clearly, studies show, it is well known: no hit in the four pages and twins. Cards: 'round' hits only the word 'rounding' in card text of another lesson. check_pages.py BANNED list passes (BK4b-gate-check-pages)."),
    row("BK4b-notation", "2.9-structure", "notation/notation.json; course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html",
        "Macros used by the two pages: \\E, \\Prob, \\Var, \\Cov, \\indic. Each is present in notation/notation.json (checked by python this round). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur. Local symbols (rho, theta, x, y, h, C_0, Res_0, D, C, m, c in L04; p, kappa, ell, C, F_i, A1-A4 in L05) are defined on their lesson. ell is explicitly not the L01 symbol d (L05.html:55-64; L01.html:64)."),
    row("BK4b-hours", "2.9-structure", "course/modules/BK/BK4/L04.html:2; course/modules/BK/BK4/L05.html:2; course/modules/BK/BK4/index.html:29; course/modules/BK/BK4/project.html:34",
        "data-hours=7 on L04 and L05 (and every BK4 lesson). Hub data-hours-lessons=35 = 5 x 7; data-hours-project=15 (index.html:29; project.html:34); total 50. Matches plan §1 and §2.1."),
    row("BK4b-cards-L04-L05-scan", "2.7-cards", "course/modules/BK/BK4/cards.json (19 L04 cards; 15 L05 cards)",
        f"All 34 cards read individually against the current lesson text this round ({S}cards_check.txt for the counts). L04 BK4-c059 to c076, c093, c097; L05 BK4-c077 to c090, c094, c098, c100. Each card's numbers and hypotheses match the lesson. The cards changed since round 6 (BK4-c011, c041, c043, c044, c104) are L01 and L03 cards outside slice b; none of the 34 slice-b cards changed. BK4-c078 'settlement cycle d of Lesson 1' matches L01.html:64."),
    row("BK4b-cards-duplicates", "2.7-cards", "course/modules/BK/BK4/cards.json (99 cards)",
        f"python: 99 cards, no duplicate ids, no duplicate fronts ({S}cards_check.txt). BK4-c088 and BK4-c100 both concern the mean but ask distinct questions (the misconception vs the Prop 2.4 value)."),
    row("BK4b-cards-grades-basis", "2.7-cards", "course/modules/BK/BK4/cards.json (L04 and L05 cards)",
        "Cards graded T name a Proposition, Remark or Example on the page as basis. Cards graded C (BK4-c086, c087, c094) name Lab 1 Parts B or D with SIMULATED parameters."),
    row("BK4b-dag-prose-terms", "2.9-dag", "course/modules/BK/BK4/L04.html; course/modules/BK/BK4/L05.html",
        "check_dag PASS (BK4b-gate-check-dag). L04 links only settlement-cycle (L01) and bank-money-creation (FC1, in the closure). L05 links settlement-cycle (L01). No CCP, margin, netting or stablecoin-run concept is linked; any mention is plain prose (see BK4b-gate-check-dag)."),
    row("BK4b-registry-citation-consistency", "2.1-citations", "course/modules/BK/BK4/L05.html:347, :579; references/references.json:2815, :2840",
        "The cited key exists; title and URL match the record; the locator 'index page: title and issuer' matches the index-level claim; the live URL returns the same title (BK4b-citation-bisndbasel). Registry flag: used_by is ['BK1'] (references.json:2840) and does not list BK4. Plan §7.1 assigns the used_by update to integration (Q12). Not a slice-b defect; recorded in registry_flags."),
    row("BK4b-L04-assumption4-scope", "2.9-structure", "course/modules/BK/BK4/L04.html:79, :82, :85",
        f"PREVIOUSLY FAIL (round 6). Fixed: the list at L04.html:85 now names Assumption 1 (the valuation clause, :82) and Definition 1.2 (a pointer, :69), and keeps Remark 4.1, Problem R1, Misconception 1, the key-results table, quiz items 8 and 9, and the Lab 1 haircut check. Every use found by a line-numbered grep of L04.html for 'assumption 4|valuation|haircut|1-h|A4' lies in that list: :69 (Def 1.2), :82 (Assumption 1), :157 (Lab 1 check), :189 (twin comment), :356 (interpretation), :376 (Remark 4.1), :380 and :391 (canon list and Misconception 1), :428-429 (R1), :447 (key results), :508 and :515 (quiz 8), :518-519 (quiz 9). Re-verified this round."),
    row("BK4b-L04-seeded_path-docstring", "2.5-labs", "course/modules/BK/BK4/L04.html:218-225 (tests/labs/BK4/lab-BK4-L04-1.py:217-225)",
        "Docstring: the sampled shares are in increasing order, then 99/100 is appended, and 99/100 repeats a sampled share if present. This matches the code and the printed seed-7 path 7/100 1/10 1/5 21/50 51/100 21/25 99/100 (recompute_r7 'L04 lab path'). The path is non-decreasing, as the canon bullet at :382 says."),
    row("BK4b-L04-haircut-docstring", "2.5-labs", "course/modules/BK/BK4/L04.html:283-294 (twin :283-294)",
        "haircut_check docstring: 1/(1-h) and the coverage at share 1/2 for a ratio just below it (21/20) and at it (20/19). Printed output: 20/19; 399/400 and 199/200 (9950 bps); 1 and 10000 bps. Matches (recompute_r7 'Haircut ...' checks)."),
    row("BK4b-L04-misconception3", "2.9-structure", "course/modules/BK/BK4/L04.html:393",
        "Coverage stays at rho only when x=0 or rho=1 (Prop 2.6); falls for rho<1 and rises for rho>1 (Prop 2.5); both directions appear in the two printed tables (Lab 1 output lines 320-347 of the expected block)."),
    row("BK4b-cards-c076", "2.7-cards", "course/modules/BK/BK4/cards.json (BK4-c076); course/modules/BK/BK4/L04.html:131-137",
        "Card back 'Only when x = 0 or rho = 1' and 'at most rho when rho<=1, at least rho when rho>=1' match Prop 2.6 (:131-137)."),
    row("BK4b-L04-admissible-undefined", "2.9-structure", "course/modules/BK/BK4/L04.html:90 (Definition 2.1) and first use after it",
        "'admissible for a ratio' is first used in the text in Definition 2.1 (L04.html:90), where it is defined, and used afterwards (:95-152, quiz). No earlier use."),
    row("BK4b-L04-remark3.2-FC1-paraphrase", "2.1-citations", "course/modules/BK/BK4/L04.html:367; course/modules/FC/FC1/L01.html:73, :81",
        "The quoted definition in L04.html:367 is identical to FC1 L01.html:81 ('the increase in total deposits that results when the bank makes a loan and the proceeds are deposited back at the same bank'). FC1 L01.html:72-73 (Assumption 2.0) states that the bank's deposits are its liabilities, matching 'deposits are the bank's liabilities (FC1, Section 2)'. Read this round."),
    row("BK4b-L04-def1.2-section4-claim", "2.9-structure", "course/modules/BK/BK4/L04.html:69",
        "'Section 4 treats a constant haircut to face value (Assumption 4)' is true: Section 4 (Remark 4.1) treats a constant haircut h. The round-7 edit removed 'only' (no scope loss: Remark 4.1 is the only treatment in Section 4)."),
    row("BK4b-L05-why-overreach", "2.9-structure", "course/modules/BK/BK4/L05.html:51",
        "'Proposition 2.1 shows that the mean does not depend on how failures are linked' (Prop 2.1 uses no joint law); 'Proposition 2.4 gives the same mean when all three trades fail together' (A4); 'Proposition 2.5 shows ... the variance ... is at least the variance under independence' (kappa>0, 0<p<1). Round-7 edit: 'Lab 1 checks Proposition 2.2 and prints the quantities of Propositions 2.4 to 2.6' is supported: the expected block prints 'enumeration equals closed form: True' (2.2), 'the two means are equal: True' (2.4), 'the comonotone variance is larger: True' and the variances (2.5), and 'probability of no cost' (2.6), L05.html:304-334."),
    row("BK4b-L05-why-terms", "2.9-structure", "course/modules/BK/BK4/L05.html:51, :55, :58, :64, :67-73",
        "'Operational risk' is defined for this unit in the why paragraph and in Definition 1.1 (:58). 'Settlement failure' and 'delay' are in Definition 1.2 (:64). 'A3' and 'A4' are named in the why paragraph and in Assumption 1.3 (:67-73)."),
    row("BK4b-L05-why-ungraded-claim", "2.3-grades", "course/modules/BK/BK4/L05.html:51",
        "The why paragraph states results only as proposition names (grade T in the body) and the lab as SIMULATED; it makes no ungraded empirical claim."),
    row("BK4b-L05-M2-citation", "2.2-numbers", "course/modules/BK/BK4/L05.html:381-386",
        "M2 gives (7/8)^3 = 343/512 and 169/512 for independent failures; Lab 1 Part B prints 343/512 for the all-ok pattern and 169/512 for at least one failure (expected block, L05.html:304-334)."),
    row("BK4b-r2-L05-numbering", "2.9-structure", "course/modules/BK/BK4/L05.html:84-152 (Props at :84, :94, :113, :123, :137; Examples at :147, :152)",
        "Definition 2.1, Proposition 2.2, Remark 2.3, Propositions 2.4-2.6, Examples 2.7-2.8 use one counter in order (line numbers read this round). Quiz and key-results citations match."),
    row("BK4b-r2-L05-why-dependence-attribution", "2.1-citations", "course/modules/BK/BK4/L05.html:51",
        "The why paragraph attributes no external result. It refers to Propositions on the page and to Lab 1 only."),
    row("BK4b-r2-L05-M1-model", "2.9-structure", "course/modules/BK/BK4/L05.html:374-379",
        "Model statement (three trades, each p=1/4 under A1, kappa=1000, delays 2, 3, 1) matches the M1 solution, which gives 1500 cents by Prop 2.1 under either joint law ('M1 mean 1/4*1000*6')."),
    row("BK4b-r2-title-casing", "2.9-structure", "course/modules/BK/BK4/L04.html:6, :36; course/modules/BK/BK4/L05.html:6, :35; course/modules/BK/BK4/index.html:142-146; course/modules/BK/BK4/project.html:37",
        "Titles 'Stablecoins and Tokenization' and 'Operational Risk in Market Infrastructure' match the hub map and the lesson h1 elements (L04.html:36, L05.html:35)."),
    row("BK4b-r3-L05-uses-metadata", "2.9-structure", "course/modules/BK/BK4/L05.html:37",
        "'settlement cycle (L01, Definition 1.2)' matches course/modules/BK/BK4/L01.html:63-64 (Definition 1.2, settlement cycle, symbol d)."),
    row("BK4b-grade-legend-L04", "2.3-grades", "course/modules/BK/BK4/L04.html:43-50 (and L05.html:42)",
        "The grade legend lists T, A, B, C, D, X with the meanings used in the page. C is used for single-sample SIMULATED results (L05 key results 7-8)."),
    row("BK4b-L04-bps-convention-note", "2.2-numbers", "course/modules/BK/BK4/L04.html:69 vs :90",
        "Ratio bps floor(10000 rho) (:69) and coverage bps floor(10000 theta) (:90) are the same rule computed exactly, in both places."),
    row("BK4b-L05-quiz-prop21-scope", "2.9-structure", "course/modules/BK/BK4/L05.html:503, :506-508, :531",
        "Item 2 explanation: E[C] = 1/4 * 1000 * 3 = 750 from the indicator expectation under A1 (Prop 2.1 with one trade). Re-derived (recompute_r7 'Quiz single trade'). Item 5 explanation at :531 re-read (see BK4b-quiz-L05)."),
    row("BK4b-L04-amounts-integer-cents-scope", "2.9-structure", "course/modules/BK/BK4/L04.html:56, :64-69, :376",
        "Line 56 limits 'integer cents' to the claims and to the reserves at face value, and says the measured reserves of Remark 4.1 need not be whole cents. Definition 1.2 (:64-69) states both amounts 'in integer cents at face value'. Remark 4.1 (:376) uses the measured ratio rho(1-h), with no integer-cent claim."),
    row("BK4b-L04-assumption1-face-value-conflict", "2.9-structure", "course/modules/BK/BK4/L04.html:82, :85, :101-103",
        "Assumption 1 (:82) says reserves are used at the value Assumption 4 gives them, which is face value when Assumption 4 is not assumed. Prop 2.2 assumes 1-3 without 4 (:94-97), and its proof uses face value (:101-103). Consistent."),
    row("BK4b-L04-path-increasing-order", "2.5-labs", "course/modules/BK/BK4/L04.html:382 vs lab docstring L04.html:218-222",
        "L04.html:382 says 'non-decreasing order, and the printed seed-7 path is strictly increasing'. The docstring (sample increasing, then 99/100 which may repeat) makes the path non-decreasing; the printed path is strictly increasing (recompute_r7 'L04 lab path')."),
    row("BK4b-twin-page-exact", "2.5-labs", "tests/labs/BK4/lab-BK4-L04-1.py; tests/labs/BK4/lab-BK4-L05-1.py; course/modules/BK/BK4/L04.html:158-317; course/modules/BK/BK4/L05.html:163-303",
        f"Decoded the data-run code block of each page and compared with the twin ({S}twin_vs_page.py, output {S}twin_vs_page.txt): page code equals the twin after trailing-newline removal (tools/embed_labs.py:117 and tools/run_labs.py:74-75 use rstrip('\\n') by design). Expected blocks equal stdout after the same convention. Byte-level difference is the final newline only."),
    row("BK4b-slice-delta", "2.9-structure", "git diff 4bd8cb94 06994db1 -- course/modules/BK/BK4/L04.html L05.html cards.json tests/labs/BK4",
        f"Diff hunks in slice b (git diff -U0): L04.html @@ -69, -85, -529; L05.html @@ -51, -467, -531 (each re-read and re-verified in rows BK4b-L04-def1.2-section4-claim, BK4b-L04-assumption4-scope, BK4b-quiz-L04, BK4b-L05-why-overreach, BK4b-math-L05-R-problems, BK4b-quiz-L05). cards.json hunks: BK4-c011, c041, c043, c044, c104, all L01/L03 (outside slice b); no slice-b card changed. tests/labs/BK4/lab-BK4-L04-1.py and lab-BK4-L05-1.py are unchanged since 4bd8cb94 (git diff empty). Other changes in the commit (L01, L02, L03, project, grader, plans/FINAL-ARCHITECT-RULINGS.md ruling 12 for M3) do not touch slice b."),
]

fragment = {
    "unit": "BK4",
    "slice": "BK4-b",
    "round": 7,
    "verifier": "Haiku independent verifier, BK4-b round 7 (did not build BK4; seventh verification of slice b)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin; fragment /Users/billyribeiro/.fanout/frags/E-BK4-b.round6.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-BK4-b (detached at 06994db, .venv symlinked)",
    "scratch": "/tmp/bk4b_r7_bis.html (curl output only); command outputs and scripts archived in ledgers/BK4/scripts/BK4-b-r7/",
    "verified_at": "2026-11-04T22:10:00+00:00",
    "verdict": "",
    "rows": rows,
    "mutants": [],
    "registry_flags": [
        "bisndbasel (references/references.json:2815) has used_by [\"BK1\"] (references.json:2840). BK4 L05.html:347 and :579 cite it. Plan §7.1 says used_by must gain BK4 at integration (Q12). Until then tools/verify_refs.py --unit BK4 does not re-verify this citation (2 of 560 entries). The architect should run the registry tool to add BK4."
    ],
    "freshness_flags": [
        "bisndbasel URL https://www.bis.org/committees/bcbs/standards re-fetched with plain curl on 2026-11-04 (HTTP 200, title identical to the registry title; ledgers/BK4/scripts/BK4-b-r7/curl_bisndbasel.txt). No 2025-2026 work is needed by slice b: the page states no operational-risk standard."
    ],
    "notes": (
        "Slice b = L04 and L05 pages and the two lab twins, plus their 34 cards. Read in full this round: L04.html lines 1-549 and L05.html lines 1-592, every sentence, every expected-block line and every quiz explanation; both twins (every line, via the page code); all 34 cards individually. Delta since round 6 read hunk by hunk; rows re-verified from scratch this round, no carry-forward. Every round-6 non-PASS row (BK4b-quiz-L04, BK4b-L04-assumption4-scope) was re-verified and is now PASS. "
        "Not a finding, recorded for the architect: (a) the page expected blocks and the page code omit the trailing newline that print() emits; the tools compare with rstrip('\\n') by design, so exact-string comparison would fail by one newline (tools/embed_labs.py:117, tools/run_labs.py:74-75); (b) the L05 why-paragraph and Section 3 both describe Lab 1 as checking Proposition 2.2 and printing the quantities of 2.4 to 2.6; the printed lines support this; (c) the quiz intro at L05.html:494 (finishing the quiz adds cards) matches quiz.js addLessonCards, read from source in round 6; not re-read this round. Mutants: none, because slice b has no grader; the lab twins are demonstrations (FINAL-ARCHITECT-RULINGS 9 as cited in the plan). "
        "Could not check: (1) no Pyodide runtime was run directly; page_smoke.py (the tool's own harness) passed for both pages; (2) the SEC T+1 rule and any settlement-date fact are not in slice b, and no check was made; (3) the Duffie and Zhu abstract and the CPMI index are not cited in slice b; (4) the Basel III operational-risk section was not read, and the page says so (L05.html:347, :579); (5) FC1 L01 was checked only at the quoted and cited lines (FC1 L01.html:63-64 is not used; :72-73, :81 are); (6) the interactive quiz script (quiz.js) was not run in a browser, so quiz behaviour is checked from the page markup only; (7) the Pyodide interpreter version was not confirmed separately; run_labs.py and pytest ran under CPython 3.14.8 (pytest header in ledgers/BK4/scripts/BK4-b-r7/pytest_labs_verbose.txt)."
    ),
    "summary": "",
}

statuses = [r["status"] for r in rows]
fragment["verdict"] = "PASS" if all(s == "PASS" for s in statuses) else "FAIL"
counts = {s: statuses.count(s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
fragment["summary"] = (
    f"BK4-b round 7: verdict {fragment['verdict']}. Rows {len(rows)} (pass={counts['PASS']} fail={counts['FAIL']} "
    f"unverifiable={counts['UNVERIFIABLE']}). Round-6 FAILs BK4b-quiz-L04 and BK4b-L04-assumption4-scope are fixed and re-verified PASS. "
    "No mutants (labs and prose only). Gates re-run on the pin: check_pages, check_dag, check_projects, run_labs, page_smoke (L04, L05), ruff, mypy, pytest lab tests, verify_refs offline and unit, twin isolated runs."
)

out = ROOT / "ledgers" / "BK4" / "BK4-b.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "verdict", fragment["verdict"], counts)
