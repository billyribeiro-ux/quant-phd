"""Write the round-3 fragment for M2 slice b (run from the checkout root with -I)."""
import json
from datetime import UTC, datetime

S = "ledgers/M2/scripts/M2-b-r3"
rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> None:
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or ""
    rows.append(r)


LABS = {
    "07": ("L07.html lab section (line 133); twin lab-M2-L07-1.py",
           "hypothesis (line 135) matches parts A-D: 27 checks of closed form vs recursion; exact error x^(n+1)/(1-x) at every n=0..10 and ratio 3/10 (part B); errors -2,-4,...,-2048 at x=2 (part C); quotients +2/-2 at h=1e-1..1e-6 (part D); interpretation (lines 251-252) matches the printed output (v3_text_L07.txt lines 208-250)"),
    "08": ("L08.html lab section (line 128); twin lab-M2-L08-1.py",
           "hypothesis (line 129) matches output: 133 (x,n) pairs (19 x 7) with 0<xi<x and Lagrange form = exact remainder to 1e-9 (part A); 70 pairs with x<=1/2 (10 x 7) for the bound (part B); part C rows reproduce xi=1-(1-x)^(1/(n+2)) and R_n exactly (recomputed in v3_recompute.out)"),
    "09": ("L09.html lab section (line 141); twin lab-M2-L09-1.py",
           "hypothesis (line 142) matches output: U_n-L_n=1/n exactly for n=1..128 and 1/3 in [L_n,U_n] (part A; U_128=0.33724976 = 1/3+385/98304 recomputed); part B mesh 0.19, U-L=0.15933400 <= 0.19; part C errors +0.06510417 (=25/384), -0.00130208, -0.00032552 (=-1/(12*16^2)) match recomputation (v3_recompute.out)"),
    "10": ("L10.html lab section (line 116); twin lab-M2-L10-1.py",
           "hypothesis (line 117) matches output: U_n-L_n=3/n for F=x^3-2x, n=1..256, bracket -1 (part A); U_n-L_n=3/(4n), n=1..128, bracket 1/2 (part B); central difference 0.59171598 = 1/1.69 within 1e-7 (part C); recomputed in v3_recompute.out"),
    "11": ("L11.html lab section (line 138); twin lab-M2-L11-1.py",
           "hypothesis (line 139) matches output: midpoint 0.0166666667 vs 1/60 (part A); 2.6666666663 vs 8/3 for both sides of Theorem 3.1 (part B); 0.3333333333 with limits unchanged (part C); recomputed exactly in v3_recompute.out"),
    "12": ("L12.html lab section (line 100); twin lab-M2-L12-1.py",
           "hypothesis (line 101) matches output: b*error=1 at b=10..10000 (part A); b^2*error=1/2 (part B); H_N-1 >= m/2 for m=1..14, e.g. H_16384-1=9.28130671 (part C; recomputed); interpretation (line 154) matches"),
}
for n, (loc, ev) in LABS.items():
    row(f"LAB-L{n}", "2.5 labs", loc,
        "PASS",
        "run_labs --unit M2: PASS 27/27 (v3_run_labs_M2.txt); twin run alone with python -I -W error: exit 0, empty stderr (v3_twin_isolated.txt, v3_twin_out/); page code and expected block equal the twin and the saved stdout and a fresh rerun (v3_lab_exact.txt: ALL OK). " + ev + ".")

STRUCT = {
    "07": ("L07.html", "107 words; 12 solutions; 3 problems per tier; quiz 9 items; 3 misconceptions; key-results table (v3_text_L07.txt)"),
    "08": ("L08.html", "94 words; 12 solutions; 3 per tier; quiz 9 items; 3 misconceptions; key-results (v3_text_L08.txt)"),
    "09": ("L09.html", "117 words; 12 solutions; 3 per tier; quiz 8 items; 3 misconceptions; key-results (v3_text_L09.txt)"),
    "10": ("L10.html", "118 words; 12 solutions; 3 per tier; quiz 10 items; 3 misconceptions; key-results (v3_text_L10.txt)"),
    "11": ("L11.html", "96 words; 12 solutions; 3 per tier; quiz 9 items; 3 misconceptions; key-results (v3_text_L11.txt)"),
    "12": ("L12.html", "120 words (limit 120); 12 solutions; 3 per tier; quiz 9 items; 3 misconceptions; key-results (v3_text_L12.txt)"),
}
for n, (f, ev) in STRUCT.items():
    extra = ""
    if n == "12":
        extra = (" Round-2 FAIL at line 38 (Uses meta-row) is resolved: it now cites Lesson 5 Problem P1 (power rule; "
                 "v3_text_L05.txt line 256) and Lesson 5 Proposition 1.3 (quotient rule; v3_text_L05.txt line 80), both verified.")
    row(f"STRUCT-L{n}", "2.9 structure", f"course/modules/M/M2/{f}", "PASS",
        "check_pages --unit M2: PASS (check_pages_M2.txt); section order per BUILDER 4.2 (v3_text file); " + ev +
        "; why-it-matters word count from v3_delta_words.txt." + extra)

NUM = {
    "07": "9/70; 2.5307e-6 at degree 10; 0.3000000058 ratio (rel. diff 1.9e-8); 0.0013 and 0.00065 at n=8,9 for x=-1/2; n=20 for 10^-6 at x=1/2; f''(1/2)=16, f'''(1/2)=96; P_2(1/2)=7/4, error 1/4",
    "08": "xi=0.0693951 (1/4, n=2), 0.1294494 (1/2, n=3), 0.0496772 (0.3, n=5); 4/27 and 1/12 at x=1/4,n=1; 128/27; Remark 3.3 bounds 5.625, 8.4375, 12.65625, 18.984375 and exact 0.9, 0.54, 0.324, 0.1944; 133 and 70 pairs",
    "09": "U_128=0.33724976, L_128=0.32943726; 385/98304; 25/384=0.06510417; 1/3072=0.00032552; 151/15000=0.010067 and 154/15606=0.009868 (n=50,51); 7/12=0.583333; 0.19 mesh",
    "10": "U_8=-0.80468750, L_8=-1.17968750 (gap 3/8); L_128=0.49707921, U_128=0.50293859 (gap 3/512=0.005859375); F'''(0.3)=2.1; truncation 3.5e-13; rounding bound 5e-11; 1/1.69=0.591715976",
    "11": "1/60=1/2*(1/30); 1/12; 7/3; 1/20; 2/(3N^2) with N=816 giving 1.0012e-6 and N=817 giving 9.988e-7 (smallest N=817); residual 4e-10",
    "12": "0.99 and 0.01 (b=100); 1/8 for p=2 at 2; error 1/b at b=10^4 and 10^6; H_16384-1=9.28130671 (gap 2.28130671); 1/3 and 1/(p-1)",
}
for n, ev in NUM.items():
    row(f"NUM-L{n}", "2.2 numbers", f"course/modules/M/M2/L{n}.html (prose and displayed numbers)", "PASS",
        f"Each number recomputed independently with exact fractions and float by ledgers/M2/scripts/M2-b-r3/v3_recompute.py (output v3_recompute.out): {ev}. Lab-printed digits match (v3_run_labs output, twin stdout).")

MATH = {
    "07": "Prop 1.4 (quotient-rule step, (k+1)! identity), Lemma 1.6, Prop 2.3 (telescoping identity), Lemma 3.1 (Bernoulli step), Thm 3.2, Ex 4.1 and Prop 4.2 (one-sided quotients), Remark 4.3; problem solutions (cubic Taylor polynomial, 1/4 error, 1/(1-x)^2 limit, degree 9 and 20 bounds, expansion at 1/2) re-derived",
    "08": "Lemma 1.1, Rolle use in Thm 2.1 proof (repeated application, xi = y_(n+1) strictly inside), Cor 2.2, Ex 2.3 (xi solves (1-xi)^(n+2)=1-x), Ex 2.4 (factor 2^(n+2)(1-x) in [2^(n+1),2^(n+2))), Remark 3.3 values, Problem proofs (xi in (0,x), xi->0, B_n->0 iff x<1/2)",
    "09": "Lemma 1.1 and 1.2 (refinement, common refinement), Thm 2.2 (telescoping, uniform partition choice n > (b-a)|f(b)-f(a)|/eps), Cor 2.3, Lemma 3.1 algebra ((n+1)(n+2)(2n+3)/6), Ex 3.2 (U_n, L_n, U_n-1/3=(3n+1)/(6n^2), 1/3-L_n=(3n-1)/(6n^2)), problem solutions (sums of x, x^3, 1/(1+x); 51 parts)",
    "10": "Thm 1.2 use, Thm 2.1 proof (c_i from MVT, sandwich, sup/inf), Ex 2.2 (quotient rule, 1/2), Cor 3.1 (power integral, nonnegative derivative monotone), Ex 3.2 (-1), Prop 4.1 (H' = 0), canon counterexample F(x)=x on (0,1) with F(0)=5, F(1)=1 (integral 1, F(1)-F(0)=-4), problem solutions (4, 26/3, 1/6, power rule by product rule)",
    "11": "Lemma 1.1 proof (refinement, c>=0 and c<0 cases), Cor 1.2, Thm 2.1 proof, Ex 2.2 (u'v and uv', boundary term 0, 1/60 via 1/30), Ex 2.3 (boundary term 1), Thm 3.1 proof (case g(a)=g(b) and g(a)<g(b)), Ex 3.2 (3t^8+7t^6+5t^4+t^2 expansion, value 8/3), Ex 3.3 (2t+2t^3, value 3/2), Beta induction step B(m,n+1)=(n+1)/(m+1) B(m+1,n)",
    "12": "Lemma 2.1 induction, Thm 2.2 (F=-1/w, F'=x^(-p)), Ex 2.3, Lemma 3.1 block bound, Lemma 3.2 lower sum H_N-1, Thm 3.3 (subsequence argument), Remark 3.4, problems (int x^-4 = 1/3; int from 2 = 1/8; int_0^1 x^-2 diverges; series bounded by 1+1/(p-1) under Assumption 2.2)",
}
for n, ev in MATH.items():
    row(f"MATH-L{n}", "2.4 mathematics", f"course/modules/M/M2/L{n}.html (statements, proofs, worked solutions)", "PASS",
        "Every theorem, proof and displayed derivation on the page re-derived by hand, numeric checks in v3_recompute.out; hypotheses checked against statements: " + ev + ". Notation scan v3_notation_scan.txt.")

GRADE_EV = ("v3_grades.txt lists every block-title: every Theorem, Proposition, Lemma and Corollary carries class claim and data-grade T; "
            "Assumption 1.1 (L08) carries no grade by design (stated in its text); Definitions, Examples, Remarks carry no claim span; "
            "key-results tables grade T rows with sources. No B or C claim appears in lesson prose; C grades occur only on cards with a basis naming the lab (cards.json).")
row("GRADE-L07-L12", "2.3 grades", "course/modules/M/M2/L07.html to L12.html", "PASS", GRADE_EV)

CARDS_OK = {
    "07": ("c075-c096, c395 (23 cards)", "read in full in v3_cards_slice.txt; each atomic, matches the L07 text at cited locations (Definitions 1.1, 1.2, 2.1; Proposition 1.4; Lemma 1.6; Prop 2.3; Lab 1 parts A-D; Ex 3.3; Ex 4.1; Prop 4.2; Misconceptions 1-3; Remark 4.3)"),
    "09": ("c115-c132 (18 cards)", "read in full; each matches L09 text; c129 matches the current Misconception 2 wording (1/6 is a forward reference, not derived); c126/c127 match Lab 1 parts B and C"),
    "11": ("c148-c163 (16 cards)", "read in full; each matches L11 text; c163 matches the current Misconception 3 wording; c160 'Section 4' resolves to Where the canon breaks"),
    "12": ("c165-c180, c398 (17 cards)", "read in full; each matches L12 text; c175/c176/c180 consistent with Theorem 3.3, Remark 3.4 and Problem R3 (Assumption 2.2 stated in c398)"),
}
for n, (ids, ev) in CARDS_OK.items():
    row(f"CARD-L{n}", "2.7 cards", f"course/modules/M/M2/cards.json {ids}", "PASS",
        "Sampled at least one card in ten and read all cards in the slice (v3_cards_slice.txt): " + ev + ". Card grades C carry a basis naming the lab (checked).")

row("CARD-L08", "2.7 cards", "course/modules/M/M2/cards.json M2-c416, M2-c417 (L08 cards c097-c114 PASS)", "FAIL",
    "Cards c097-c114 PASS (read in full; v3_cards_slice.txt). M2-c416 asks 'Is Assumption 1.1 (the extreme value theorem) proved in Lesson 8?' and answers 'No. It is assumed, as Assumption 2.1 of Lesson 6 is...'; M2-c064 asks 'Is Assumption 2.1 (extreme value theorem) proved?' with the same answer. M2-c417 states Rolle's theorem under Assumption 1.1 with the same hypotheses and conclusion as M2-c065 ('Theorem 2.2 (Rolle's theorem)'). Both pairs found by the duplicate scan (v3_card_dupes_slice.txt, front similarity 0.84 and 0.81).",
    "Delete M2-c416 and M2-c417 from course/modules/M/M2/cards.json (their facts are already carded by M2-c064 and M2-c065), or rewrite M2-c417 to test what Lesson 8 adds (Remark 1.3: this lesson uses Rolle's theorem only in its equal-endpoint case). Keep the ids of all other cards.")
row("CARD-L10", "2.7 cards", "course/modules/M/M2/cards.json M2-c418 (other L10 cards PASS)", "FAIL",
    "M2-c418 states the mean value theorem under Assumption 2.1 of Lesson 6 (p<q, continuous on [p,q], differentiable on (p,q), phi(q)-phi(p)=phi'(c)(q-p)); M2-c066 states the same theorem (Theorem 2.3 of Lesson 6) with the same hypotheses and conclusion. Duplicate fact (v3_card_dupes_slice.txt, front similarity 0.83). Other L10 cards c133-c147 PASS; removal of M2-c144 leaves no dangling reference (checked).",
    "Delete M2-c418 from course/modules/M/M2/cards.json (the use of the mean value theorem in L10 is already tested by M2-c134 and M2-c142).")
row("CARD-DUP", "2.7 cards (full scan)", "course/modules/M/M2/cards.json (all 394 cards)", "FAIL",
    "Exact (front, back) duplicate scan over all 394 cards: none. Near-duplicate scan (difflib front ratio >0.6, v3_card_dupes_slice.txt): three cross-lesson restatements of one fact each, (M2-c416, M2-c064), (M2-c417, M2-c065), (M2-c418, M2-c066). Pairs reviewed and judged distinct questions: (c085,c086), (c124,c131), (c136,c138), (c175,c176), (c178,c180), (c125,c139).",
    "Remove or rewrite M2-c416, M2-c417 and M2-c418 as stated in rows CARD-L08 and CARD-L10. After that the scan finds no restated fact in the slice.")

row("DAG-L07-L12", "2.9 DAG", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "check_dag --unit M2: PASS (check_dag_M2.txt). v3_links_dag.txt: every href resolves to an existing file and anchor, no external URL, no external script; dfn only def-taylor-theorem (L08) and def-definite-integral (L09); concept links limit->L01, derivative->L04, definite-integral->L09, taylor-theorem->L08, mathematical-induction->concepts.html (owner M1, in the prerequisite closure per curriculum/curriculum.json concepts). No link or dfn for epsilon-delta-continuity, riemann-stieltjes-integral, lebesgue-integral, fubini-theorem, lagrange-multiplier, duration or convexity (grep of data-concept in the six pages); continuity appears in prose only.")

row("XREF-L07-L12", "2.9 structure (cross-references)", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "Every 'Problem Lnn-Xk' reference resolves to an element id on its page (ids listed by grep of id attributes: L07-P3, L07-R2; L08-M1, M2, P2, P3, R2, R3; L09-E1, M3, R2; L10-E1, M1, M2, P2, R3; L11-M1, M2, R1; L12-M2, M3, E2, R2, R3) and matches the referenced content. Cited results of other lessons checked in v3_text_L01/L03/L04/L05/L06: L01 Problem M3 (-1)^n/n -> 0 (v3_text_L01.txt lines 240-243); L03 Proposition 2.2 (lines 364 and 95); L04 Proposition 2.1 (line 139); L05 Proposition 1.2 (line 68), Proposition 1.3 quotient rule (line 80), Problem P1 power rule (line 256); L06 Assumption 2.1 (line 72), Theorem 2.2 Rolle (line 77), Theorem 2.3 MVT (line 87), Corollary 3.1 (i)-(iii) (lines 102-103); L09 Lemma 1.1 refinement; L10 Theorem 2.1 and Corollary 3.1; L11 Lemma 1.1.")

row("NOT-L09-R", "2.4 / 2.9 notation (rule 13)", "course/modules/M/M2/L09.html (Riemann-sum and partition notation) and L07-L12 math spans", "PASS",
    "v3_notation_scan.py / v3_notation_scan.txt: none of the registered symbols in notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) occurs in L07-L12; every macro used is standard LaTeX or a registered macro (\\R in L11). Local symbols each carry one meaning in the slice: P (partition, L09-L10), P_n (Taylor polynomial, L07-L08), R_n (remainder, L07-L08), L(f,P), U(f,P), I_*, I^* (L09 Definition 1.3), delta(P) (mesh), xi (L08), ell (limit, L12), H_N (L12), B_n (L08 research).")
row("NOT-GLOBAL", "2.4 / 2.9 notation", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "Same scan as NOT-L09-R: no symbol reuse across L07-L12 with a different meaning. Notation rule 13 satisfied for the slice.")

row("PROSE-BANNED", "2.9 prose", "course/modules/M/M2/L07.html to L12.html (visible text, v3_text_L07..L12.txt)", "PASS",
    "Scan for BUILDER 1.3-1.4 banned strings: no hit for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'it can be shown', 'let us', motivational openers. Ellipses occur only as answer blanks in quiz stems (for example 'equals...'), not as omitted content.")
row("PROSE-PROCESS", "2.9 prose", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "Visible-text scan for 'builder', 'verifier', 'architect', 'slice', 'round', 'fixed', 'ledger', 'reviewer': no hit in L07-L12.")

row("HOURS-L07-L12", "1 hours", "course/modules/M/M2/L07.html to L12.html; course/modules/M/M2/index.html", "PASS",
    "data-hours=10 on each of L07-L12 (grep); index.html data-hours-lessons=240 = 24 x 10; data-hours-project=60; 240+60=300 = the M2 curriculum figure (plans/M2-build-plan.md section 0). Slice lesson hours 60. check_pages PASS covers the sum rule.")

row("LINK-L11-chain", "2.9 structure / DAG", "course/modules/M/M2/L11.html (Uses meta-row, source line 38)", "PASS",
    "The Uses row names L09 definite integral and Darboux sums, L10 fundamental theorem, Lesson 5 product and chain rules, Lesson 4 continuity of differentiable functions (L04 Proposition 2.1), and Lesson 6 Assumption 2.1; each resolves (v3_text_L04/05/06, L09, L10). Links L11->L09 resolve (v3_links_dag.txt).")

row("PROOF-L11-hyp", "2.4 mathematics (worked solutions)", "course/modules/M/M2/L11.html (Theorem 2.1 lines 84-95; Theorem 3.1 lines 110-117; Examples 2.2, 2.3, 3.2, 3.3)", "PASS",
    "Theorem 2.1 states u, v differentiable on an open I containing [a,b] and u'v, uv' integrable; Theorem 3.1 states g differentiable on I, F antiderivative on J with g(I) in J, f and t->f(g(t))g'(t) integrable, g(a) <= g(b). Each example checks the integrability hypotheses (Corollary 1.2 for polynomials; Lesson 9 Theorem 2.2 for x). Composite integrands 3t^8+7t^6+5t^4+t^2 and 2t+2t^3 re-derived (v3_recompute.out).")

row("PROOF-L12-integrability", "2.4 mathematics (worked solutions)", "course/modules/M/M2/L12.html (Theorem 2.2 proof; Lemma 3.2; Theorem 3.3; Problem R3)", "PASS",
    "x^(-p) is positive and nonincreasing on [1,b] and therefore integrable by Lesson 9 Theorem 2.2 (v3_text_L12.txt line 53); 1/x on [1,N] used in Lemma 3.2 with the unit partition; Theorem 3.3 uses Lemma 3.1 and 3.2; Problem R3 states Assumption 2.2 where used (v3_text_L12.txt line 362). No integrability claim outside the monotone class is made.")

row("RUN-M2-CHECKS", "2.9 gates", "tools check_pages, check_dag, check_projects (--unit M2)", "PASS",
    "check_pages.py --unit M2: 'check_pages M2: PASS' (check_pages_M2.txt); check_dag.py --unit M2: PASS (check_dag_M2.txt); check_projects.py --unit M2: PASS (check_projects_M2.txt).")
row("LAB-GATES", "2.5 labs", "tests/labs/M2 (six slice twins); tests/test_*.py relevant suites", "PASS",
    "run_labs.py --unit M2: PASS 27/27 (v3_run_labs_M2.txt). ruff check tests/labs: all checks passed (v3_ruff_check_all_tests_labs.txt); ruff format --check tests/labs/M2: 27 files formatted (v3_ruff_format.txt). mypy --no-incremental on the six slice twins: no issues (v3_mypy_M2_labs.txt). pytest tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_page_smoke.py tests/test_docs_figures.py tests/test_curriculum.py: exit 0 (v3_pytest_relevant.txt).")
row("PAGE-SMOKE-L07-L12", "2.5 labs / 2.9 browser", "page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12", "PASS",
    "v3_page_smoke_L07_L12.txt: PASS for each of the six pages and 'page_smoke M2: PASS'; lab runtimes 0.0 to 0.1 s; no FAIL line. Browser-level visual inspection was not performed (see notes).")
row("TWIN-ISOLATED", "2.5 labs", "tests/labs/M2/lab-M2-L07-1.py .. lab-M2-L12-1.py", "PASS",
    "v3_twin_isolated.sh run from a scratch copy with python -I -W error: L07..L12 exit 0 (v3_twin_isolated.txt); stderr files empty; stdout saved in v3_twin_out/.")
row("QUIZ-L07-L12", "2.9 quiz / 2.4", "course/modules/M/M2/L07.html to L12.html (quiz sections)", "PASS",
    "Quiz items extracted with the data-correct and data-answer attributes (v3_quiz.txt, v3_quiz07.txt): 9, 9, 8, 10, 9, 9 items. Every marked-correct option and numeric answer re-derived (e.g. f'''(x)=6/(1-x)^4; P_2 = 1+x+x^2; 9/70 to 6 dp; xi=1-(3/4)^(1/4)=0.0693951; 8.4375; 26/3; 1/60; 1/(p-1); smallest degree 20). Each item has an explanation that matches the lesson.")
row("REFS-OFFLINE", "2.1 citations", "tools/verify_refs.py --offline; course/modules/M/M2/L07.html to L12.html", "PASS",
    "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (v3_verify_refs_offline.txt). The slice cites no registry key (no data-cite attribute in L07-L12; the references sections say so; cards carry no cite key).")
row("DELTA-HUNKS", "2.1-2.9 (round-2 to round-3 delta)", "git diff 9294b914..8196077d for the slice paths (v3_delta_words.txt)", "PASS",
    "Changed slice files: L07 (references paragraph, line 589), L09 (monotonicity bullet, line 267), L10 (why-it-matters line 33; new increment definition line 46), L11 (canon bullet, line 228), L12 (ell notation in Definition 1.1 line 58, Remark 1.2 line 65, proof line 229, Problem R3 lines 310-318; Uses line 38), cards.json (M2-c129 changed; M2-c144 removed; M2-c416, c417, c418 added; c419, c420 belong to other slices). Every slice hunk read and re-verified in this round; L08 and the lab twins L07-L12 are unchanged. The replaced sentences are correct on re-derivation, except for the duplicate cards named above.")

notes = [
    "Round-3 verdict FAIL is caused only by three duplicate cards: M2-c416 (dup of M2-c064), M2-c417 (dup of M2-c065), M2-c418 (dup of M2-c066). All lesson pages, labs and the other 106 slice cards PASS.",
    "Non-blocking, architect ruling still open: plans/M2-build-plan.md section 3 names the L07 lab 'Taylor polynomials of exp at 0'; the page uses 1/(1-x) (Builder B open item 1 asks the architect to keep it or to assume exp' = exp). No page defect: the page does not use exp anywhere; the architect must rule.",
    "Non-blocking: L11 Corollary 1.2 states 'every b > 0' but its proof opens with 'For b = 0 both sides are 0'. The extra case is true and harmless; delete it for consistency if the builder touches the page.",
    "Non-blocking: M2-c120 (Definition 1.3) bundles the definition with the reversed-limit and a=b conventions. Each fact is on the page; split only if the card set is edited anyway.",
    "Non-blocking: L08 Lemma 1.1 omits the hypothesis 'f has derivatives up to order n at x0' in its statement; it is supplied by the setting in line 36 that defines P_n. Not a defect.",
    "The checkout's ledgers/M2/M2-b.json (round 10, pin e8b10b8) and the tracked round-3 files from commit 2657ab56 in ledgers/M2/scripts/M2-b-r3/ are stale; this round's outputs use the v3_ prefix, check_*_M2.txt names, and do not rely on the tracked files.",
    "No mutants: slice b has no grader. Project mutants belong to the project slice.",
    "Could not check: rendered appearance at 360 px and in dark mode (page_smoke PASS only, no screenshot inspected); Pyodide execution was exercised only through page_smoke; no commands for other units or the full gate were run (targeted per the user's testing policy); the architect's ruling on the L07 lab function.",
]

ledger = {
    "unit": "M2",
    "slice": "b",
    "round": 3,
    "verifier": "independent Haiku verifier, M2 slice b (L07-L12, lab twins and cards), round 3; fresh context, no builder context",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin; round-2 fragment /Users/billyribeiro/.fanout/frags/S-M2-b.round2.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M2-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS3-M2-b/ledgers/M2/scripts/M2-b-r3",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "mutants_killed": 0,
        "mutants": 0,
        "non_pass_ids": [r["id"] for r in rows if r["status"] != "PASS"],
    },
}
with open("ledgers/M2/M2-b.json", "w", encoding="utf-8") as fh:
    json.dump(ledger, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "verdict", ledger["verdict"], ledger["summary"])
