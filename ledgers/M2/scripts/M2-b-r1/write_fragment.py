# Writes ledgers/M2/M2-b.json (round 1). Run with python -I from the checkout root.
import json
S = "ledgers/M2/scripts/M2-b-r1/"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

LABEV = ("run_labs.py --unit M2 printed 'run_labs M2: PASS (27/27)' (" + S + "run_labs_M2.txt); twin run as "
         "python -I -W error exit 0 with 0 stderr bytes (" + S + "twin_LNN.err); ruff check, ruff format --check and "
         "mypy --no-incremental clean (" + S + "ruff.txt, " + S + "mypy.txt); pytest tests/test_labs.py -k M2: 27 passed "
         "(" + S + "pytest_labs_M2.txt); page_smoke --pages LNN PASS, lab under 0.1 s in Pyodide (" + S + "page_smoke_L07-L12.txt); "
         "expected block equals twin output (run_labs). ")
row("LAB-L07", "2.5 labs", "course/modules/M/M2/L07.html lab 1; tests/labs/M2/lab-M2-L07-1.py", "PASS",
    LABEV.replace("LNN", "L07") + "Hypothesis parts A-D match the code: A 27 checks (3 points x k=0..8), B ratio x at n=0..10, "
    "C errors -2 to -2048 at x=2, D quotients +2/-2 at h=1e-1..1e-6 (" + S + "check_L07_numbers.out).")
row("LAB-L08", "2.5 labs", "course/modules/M/M2/L08.html lab 1; tests/labs/M2/lab-M2-L08-1.py", "PASS",
    LABEV.replace("LNN", "L08") + "Hypothesis counts match the code: 19 x 7 = 133 pairs (part A), 10 x 7 = 70 pairs with x<=1/2 (part B); "
    "part C rows recomputed (xi 0.034511 at x=0.1, n=1; R_1(0.9)=8.1) in " + S + "check_L08_L12_numbers.out.")
row("LAB-L09", "2.5 labs", "course/modules/M/M2/L09.html lab 1; tests/labs/M2/lab-M2-L09-1.py", "PASS",
    LABEV.replace("LNN", "L09") + "Hypothesis matches the code: U_n-L_n=1/n exactly at n=1..128 (part A); nonuniform U-L=0.159334 <= mesh 0.19 "
    "(part B, recomputed with Fraction in " + S + "check_L08_L12_numbers.out); part C midpoint and right sums within 1/n at n=8,16,32.")
row("LAB-L10", "2.5 labs", "course/modules/M/M2/L10.html lab 1; tests/labs/M2/lab-M2-L10-1.py", "PASS",
    LABEV.replace("LNN", "L10") + "Hypothesis matches the code: bracket of -1 at n=1..256 with U-L=3/n (part A); bracket of 1/2 with U-L=3/(4n) at n=1..128 (part B); "
    "central difference at x=0.3, h=1e-6 within 1e-7 (part C).")
row("LAB-L11", "2.5 labs", "course/modules/M/M2/L11.html lab 1; tests/labs/M2/lab-M2-L11-1.py", "PASS",
    LABEV.replace("LNN", "L11") + "Hypothesis matches the code: midpoint with N=100000 agrees with 1/60 (part A), with 8/3 for both sides (part B), "
    "and the unchanged-limit value is 1/3 (part C); printed values in the expected block equal the twin output.")
row("LAB-L12", "2.5 labs", "course/modules/M/M2/L12.html lab 1; tests/labs/M2/lab-M2-L12-1.py", "PASS",
    LABEV.replace("LNN", "L12") + "Hypothesis matches the code: error 1/b and b*error=1 at b=10..10000 (part A); b^2*error=1/2 at b=10..1000 (part B); "
    "H_N-1 >= m/2 for N=2^m, m=1..14 (part C; H_16384-1 = 9.281306710 recomputed in " + S + "check_L08_L12_numbers.out).")

STRUCT = ("check_pages.py --unit M2: PASS (" + S + "check_pages.txt); html_balance.py: 0 unclosed or stray tags (" + S + "html_balance.out); "
          "page_smoke PASS (both themes, 360 px, no console errors). Section order follows BUILDER 4.2 (why, core, lab, canon, misconceptions, problems, key results, quiz). "
          "Misconceptions 3; problem set 4 tiers x 3 problems, every solution in details class=solution; quiz items recomputed: ")
row("STRUCT-L07", "2.9 structure", "course/modules/M/M2/L07.html", "PASS", STRUCT +
    "9 items, answers 2, 0.128571, 0.125, 20 correct (Example 2.4, Problem L07-R2). Hours data-hours=10. why-it-matters 107 prose words.")
row("STRUCT-L08", "2.9 structure", "course/modules/M/M2/L08.html", "PASS", STRUCT +
    "10 items, answers 1, 0.0693951, 8.4375 correct (recomputed in " + S + "check_L08_L12_numbers.out). Hours 10. why-it-matters 94 words.")
row("STRUCT-L09", "2.9 structure", "course/modules/M/M2/L09.html", "PASS", STRUCT +
    "8 items, answers 0.25, 0.0651042, 0.583333 correct. Hours 10. why-it-matters 117 prose words (120 tokens with math; check_pages counts <=120).")
row("STRUCT-L10", "2.9 structure", "course/modules/M/M2/L10.html", "PASS", STRUCT +
    "9 items, answers 4, 0.5 correct. Hours 10. why-it-matters 110 prose words (check_pages count <=120). Lesson header and meta-row HTML balanced.")
row("STRUCT-L11", "2.9 structure", "course/modules/M/M2/L11.html", "PASS", STRUCT +
    "9 items, answers 0.0833333, 2.3333333, 2.6666667, 0.0166667 correct. Hours 10. why-it-matters 96 words.")
row("STRUCT-L12", "2.9 structure", "course/modules/M/M2/L12.html", "PASS", STRUCT +
    "9 items, answers 0.3333333, 0.01, 0.125, 1e-6 correct. Hours 10. why-it-matters 114 prose words (120 tokens with math).")

NUMEV = ("Every prose number recomputed by an independent script with Fraction or float (" + S + "check_L07_numbers.py/.out, " +
         S + "check_L08_L12_numbers.py/.out, " + S + "why_words.out); printed lab values compared with the expected blocks. ")
row("NUM-L07", "2.2 numbers", "course/modules/M/M2/L07.html", "PASS", NUMEV +
    "Checked: 9/70, 1.3, 10/7, 2.5307e-6, ratio 0.3000000058 (rel. diff 1.9e-8), n=9 smallest for 1e-3 at x=-1/2 (n=8 gives 0.0013), 2^19<10^6<=2^20, 1/8, 1/4, 2048, 16, 96.")
row("NUM-L08", "2.2 numbers", "course/modules/M/M2/L08.html", "PASS", NUMEV +
    "Checked: xi 0.0693951 (x=1/4, n=2), 0.129449 and 0.0496772 (0.7^(1/7)=0.9503228), 128/27, 4/27, 1/12, Remark 3.3 values 5.625, 8.4375, 0.9, 0.54, Example 2.4 ratio interval, 0.6 table 12.65625, 18.984375.")
row("NUM-L09", "2.2 numbers", "course/modules/M/M2/L09.html", "PASS", NUMEV +
    "Checked: U_8-1/3=25/384=0.0651042, U_128=0.33724976, L_128=0.32943726, 385/98304, nonuniform U-L=0.159334 and mesh 0.19, midpoint error -1/(12*256)=-0.00032552, n=51 (0.009868) and n=50 (0.010067) for tolerance 0.01, 1/3 - L_n.")
row("NUM-L10", "2.2 numbers", "course/modules/M/M2/L10.html", "PASS", NUMEV +
    "Checked: U_8-L_8=0.375, L_128=0.49707921 and U_128=0.50293859 with 3/512=0.005859375, F'''(0.3)=6/1.3^4=2.1008 and truncation 3.5e-13, rounding budget 5e-11 (each term recomputed from ulp sizes), 7/12 and 1/6 values.")
row("NUM-L11", "2.2 numbers", "course/modules/M/M2/L11.html", "PASS", NUMEV +
    "Checked: 1/12, 7/3, 1/20, 1/30, 1/60, 8/3 = 1/3+1+1+1/3, 3/2 both sides of Example 3.3, midpoint error 2/(3N^2) with N=816 (1.00122e-6, fails) and N=817 (9.9877e-7, passes), residual 4e-10.")
row("NUM-L12", "2.2 numbers", "course/modules/M/M2/L12.html", "PASS", NUMEV +
    "Checked: 1/3, 1/8, 0.99, 0.0001, 9.28130671 for H_16384-1 and gap 2.28130671, 2^19 and 2^20 bracket 10^6, bound 1+1/(p-1), error 1/b at b=10^6.")

MATHEV = ("Every displayed identity and proof step re-derived by hand; theorem hypotheses compared with each statement and its uses; "
          "numeric re-checks in " + S + "check_L07_numbers.out and " + S + "check_L08_L12_numbers.out. ")
row("MATH-L07", "2.4 mathematics", "course/modules/M/M2/L07.html", "PASS", MATHEV +
    "Prop 1.4 induction (quotient rule step rechecked), Lemma 1.6, Prop 2.3 error identity, Lemma 3.1 Bernoulli bound, Theorem 3.2, Prop 4.2 one-sided quotients. Problems M1-M3, P1-P3, R1-R3 re-derived.")
row("MATH-L08", "2.4 mathematics", "course/modules/M/M2/L08.html", "PASS", MATHEV +
    "Lemma 1.1, Rolle chain in Thm 2.1 (y_j nesting, K=f^(n+1)(xi)/(n+1)!), Cor 2.2, Example 2.3 xi inside (0,x), Example 2.4 ratio 2^(n+2)(1-x) in [2^(n+1),2^(n+2)), Remark 3.3, Problems R1-R3.")
row("MATH-L09", "2.4 mathematics", "course/modules/M/M2/L09.html", "PASS", MATHEV +
    "Lemma 1.1 refinement, Lemma 1.2, Thm 2.2 telescoping bound and uniform-partition integrability, Cor 2.3, Example 3.2 closed forms U_n, L_n, Lemma 3.1 induction, Problems M1-M3, P1-P3, R1-R3.")
row("MATH-L10", "2.4 mathematics", "course/modules/M/M2/L10.html", "PASS", MATHEV +
    "Thm 2.1 sandwich and telescoping, Example 2.2 antiderivative, Cor 3.1 monotonicity of x^k, Prop 4.1, Misconception 2 values G(1)-G(0)=1/2 and G(1)=11/2, Problems M1-M3, P1-P3, R1-R3.")
row("MATH-L11", "2.4 mathematics", "course/modules/M/M2/L11.html", "PASS", MATHEV +
    "Lemma 1.1 (sup/inf of a sum, scalar case), Thm 2.1 telescoping with the product rule, Example 2.2 (1/60 via Beta), Example 2.3 (boundary term 1), Thm 3.1 three-part hypothesis proof, Problem R1 induction (I(m,n) recursion), R2, R3. Solution-level hypothesis omissions are in PROOF-L11-hyp.")
row("MATH-L12", "2.4 mathematics", "course/modules/M/M2/L12.html", "PASS", MATHEV +
    "Lemma 2.1, Thm 2.2 (F=-1/w derivative, F(b)-F(1)), Lemma 3.1 blocks, Lemma 3.2 lower sum, Thm 3.3 contradiction via Remark 1.2, Problem R3 bound 1+1/(p-1). Solution-level integrability omissions are in PROOF-L12-integrability.")

GRADEEV = ("Every theorem, lemma, proposition, corollary block carries data-grade T with a proof on the page or a named cited result (Lesson 6 Assumption 2.1, Theorem 2.2, 2.3, Corollary 3.1; Lesson 9; Lesson 10). Lab-only results carry grade C with basis (cards and key tables). Named assumptions carry no grade (L08 Assumption 1.1 says so; L12 Assumption 2.2 is named in R3). "
           "No registry key is cited in the slice (verify_refs --offline: " + S + "verify_refs_offline.txt, 560 entries, 0 problems). ")
row("GRADE-L07-L12", "2.3 grades", "course/modules/M/M2/L07.html to L12.html", "PASS", GRADEEV +
    "Re-graded independently: T for all proved statements, no A/B claims made; key-results tables match the statements they cite.")

row("CARD-L07", "2.7 cards", "course/modules/M/M2/cards.json ids M2-c075..c096, M2-c395", "PASS",
    "All 23 L07 cards read in full. Each card checked against the lesson text for statement, hypotheses (cards c078, c083, c088, c101 etc.), numbers (cards_check.out: every number of length >= 4 appears in the lesson), grade and basis (c085, c086, c092, c093 grade C with basis). No card is trivia. No defects.")
row("CARD-L08", "2.7 cards", "course/modules/M/M2/cards.json ids M2-c097..c114", "PASS",
    "All 19 L08 cards read in full and checked against Theorem 2.1 hypotheses (x != x0, derivatives on open I), Corollary 2.2, Example 2.3 xi, Example 2.4 bound, Remark 3.1-3.3, Problem L08-R2 iff, misconceptions 1-3. No defects.")
row("CARD-L09", "2.7 cards", "course/modules/M/M2/cards.json id M2-c129 (line 905)", "FAIL",
    "All 18 L09 cards read in full; 17 pass. Card M2-c129 states that the integral of x(1-x) is 1/6 'by Lesson 10, Theorem 2.1, under Assumption 2.1 of Lesson 6' but omits that Theorem 2.1 requires f = x - x^2 to be integrable on [0,1], the hypothesis the lesson itself stresses (L10 Misconception 1); the back does not carry the proposition's hypotheses.",
    "Rewrite the back of M2-c129 to state the hypothesis: 'Lesson 10, Theorem 2.1 gives 1/6, provided x - x^2 is integrable on [0,1]; this lesson does not prove that (Misconception 2).'")
row("CARD-L10", "2.7 cards", "course/modules/M/M2/cards.json ids M2-c133..c147", "PASS",
    "All 15 L10 cards read in full. Theorem 2.1 card carries F continuous on [a,b], F'=f on (a,b), f integrable; Prop 4.1 and Corollary 3.1 cards carry hypotheses; section references (Section 5, Remark 1.3) resolve. No defects.")
row("CARD-L11", "2.7 cards", "course/modules/M/M2/cards.json ids M2-c148..c163", "PASS",
    "All 16 L11 cards read in full. Theorem 2.1 and Theorem 3.1 cards carry all hypotheses (u,v differentiable on I containing [a,b]; g(a)<=g(b), antiderivative on J, integrability of f and of the composite). Lab grade-C cards name their basis. No defects.")
row("CARD-L12", "2.7 cards", "course/modules/M/M2/cards.json ids M2-c165..c180, M2-c398", "PASS",
    "All 17 L12 cards read in full. Theorem 2.2 and Theorem 3.3 cards carry hypotheses; Lemma 3.1 and Remark 1.2 correct; Assumption 2.2 card marked as assumed. No defects.")
row("CARD-DUP", "2.7 cards", "course/modules/M/M2/cards.json (all 394 cards)", "PASS",
    "cards_check.py output (" + S + "cards_check.out): 394 cards, no duplicate ids, no duplicate fronts; 108 cards for L07-L12 (23/19/18/15/16/17); no card number absent from its lesson; no grade-C card without basis.")

row("DAG-L07-L12", "2.9 DAG", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "check_dag.py --unit M2: PASS (" + S + "check_dag.txt). dag_links.py output (" + S + "dag_links.out): every concept link targets an anchor that exists (def-limit L01, def-derivative L04, def-taylor-theorem L08, def-definite-integral L09, mathematical-induction M1); no link to a later-module concept; taylor-theorem and definite-integral defined once each in their lessons. Later-module names used in prose only (Riemann sum, continuity, monotone convergence property) as Architect Q5-Q7 allow.")
row("XREF-L07-L12", "2.9 structure", "cross-lesson references in L07-L12", "PASS",
    "Each cross reference resolved by grep in the target: L01 Problem M3 (proves |(-1)^n/n|<eps, i.e. 1/n -> 0); L02 Prop 1.1 limit laws; L03 Prop 2.2 two-sided limit; L04 Prop 2.1 differentiable implies continuous; L05 Prop 1.2, Prop 1.3, Prop 2.1 and Problem P1 (power rule); L06 Assumption 2.1 (EVT), Theorem 2.2 (Rolle), Theorem 2.3 (MVT), Corollary 3.1 (sign of derivative); L07 Prop 1.4, Problem L07-P3, Example 1.3; L08 Theorem 2.1; L09 Lemma 1.1, Definition 1.3, Theorem 2.2; L10 Theorem 2.1, Corollary 3.1; L11 Lemma 1.1 and Corollary 1.2.")
row("NOT-L09-R", "2.9 notation (rule 13)", "course/modules/M/M2/L09.html line 62 and line 81; Corollary 2.3", "FAIL",
    "Within one lesson the letter R denotes a Riemann sum (line 62: 'the sum R = sum f(t_i) Delta x_i is a Riemann sum'; Corollary 2.3 'R be any Riemann sum') and a partition (line 81, Lemma 1.2 proof: 'Let R be the partition formed by all the points of P and Q'). No registry symbol is involved (notation/notation.json has no R), but one letter with two meanings in one lesson breaks the notation discipline of BUILDER 3.2.",
    "In the Lemma 1.2 proof (line 81 paragraph, five uses of R) rename the common refinement to S, so that R means a Riemann sum throughout L09.")
row("NOT-GLOBAL", "2.4 / 2.9 notation", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "notation/notation.json macros: the only registry macro used is \\R (L11). Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and \\mathbb{Q} do not occur in L07-L12 (grep). Remainder R_n, harmonic H_N, Darboux I_*, I^*, U, L are not registered and are defined where used.")
row("PROSE-BANNED", "2.9 prose", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "grep -i for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, in practice, typically: no hits in learner text (only 'significant figures' and math). Scope words (always, every, any, exactly) each sit next to a proof or a computation; checked at L09 'always L<=U' (proved, Section 1), L08 'always gives a smaller bound' (labelled misconception).")
row("PROSE-PROCESS", "2.9 prose", "course/modules/M/M2/L07.html to L12.html", "PASS",
    "grep -i for verifier, builder, ledger, fragment, orchestrat, round N, haiku, rung: no hits in lesson or lab text.")
row("HOURS-L07-L12", "1 hours", "data-hours on L07 to L12; index.html split", "PASS",
    "Six lessons at data-hours=10 (60 h of the 240 h lesson total). check_pages.py --unit M2 verifies the hub split and lesson hour range (6-12) and passes.")

row("LINK-L11-chain", "2.9 structure / DAG", "course/modules/M/M2/L11.html line 38 (meta-row Uses)", "FAIL",
    "Anchor text 'chain rule' is a concept link with data-concept='derivative' href='L04.html#def-derivative'. The link text names the chain rule (Lesson 5, Proposition 2.1) but the target is the derivative definition in Lesson 4. Confirmed by grep and dag_links.out (" + S + "dag_links.out, row L11 concept=derivative text='chain rule').",
    "Change the anchor to a plain link to L05.html (Proposition 2.1), without class concept and data-concept derivative; or keep the concept link and change the text to 'derivative'.")
row("PROOF-L11-hyp", "2.4 mathematics (solutions)", "course/modules/M/M2/L11.html line 260 (Problem L11-M1) and line 267 (Problem L11-M2)", "FAIL",
    "Problem L11-M1 says 'Theorem 2.1 applies' and Problem L11-M2 says 'Theorem 3.1 gives' the integral, without checking the hypotheses. M1 needs u'v and uv' integrable on [0,1] (they are polynomials, Corollary 1.2). M2 needs F(x)=x^3/3 to be an antiderivative of x^2 on an open interval J containing g(I), x^2 integrable on [g(0),g(1)]=[1,2] and 2t(1+t^2)^2 integrable on [0,1] (polynomials, Corollary 1.2). Lesson Examples 2.2 and 3.2 state these checks; the two solutions omit them.",
    "Add one sentence per solution naming each hypothesis and why it holds: for M1, u'v and uv' are polynomials on [0,1] (Corollary 1.2); for M2, F(x)=x^3/3 is an antiderivative of x^2 on J=R, x^2 is integrable on [1,2] and 2t(1+t^2)^2 is a polynomial, integrable on [0,1] (Corollary 1.2).")
row("PROOF-L12-integrability", "2.4 mathematics (solutions)", "course/modules/M/M2/L12.html line 288 (Problem L12-M3), line 349 (Problem L12-R1), line 356 (Problem L12-R2)", "FAIL",
    "Three worked solutions apply Lesson 10, Theorem 2.1 to x^(-p) on [2,b], [a,b] (a>0) and [eps,1] without checking its hypothesis that the integrand is integrable there. Theorem 2.1 of Lesson 10 lists integrability as a hypothesis, and Lesson 10 Misconception 1 says it must be checked. The fact holds (x^(-p) is positive and nonincreasing on each interval, Lesson 9 Theorem 2.2) but is not stated in these solutions.",
    "Before each application insert: x^(-p) is positive and nonincreasing on [2,b] (M3), on [a,b] (R1) and on [eps,1] (R2), hence integrable by Lesson 9, Theorem 2.2.")

fragment = {
    "unit": "M2",
    "slice": "b",
    "round": 1,
    "verifier": "independent Haiku verifier, M2 slice b (L07-L12, lab twins and cards), round 1; fresh context",
    "pin": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f",
    "base": "none (round 1 as instructed). A previous ledgers/M2/M2-b.json (round 10, pin e8b10b8, verdict PASS) existed in git and is overwritten by this round-1 fragment",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS1-M2-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS1-M2-b/ledgers/M2/scripts/M2-b-r1",
    "verified_at": "2026-11-08T00:00:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice is lessons only (no project grader), so the mutation rule and run_graders do not apply; mutants is empty by design.",
        "Five non-PASS rows, all low severity: no number, theorem statement or lab output is wrong. They are a hypothesis-check omission (PROOF-L11-hyp, PROOF-L12-integrability), a card hypothesis omission (CARD-L09), a mislabelled concept link (LINK-L11-chain) and a symbol reused in one lesson (NOT-L09-R).",
        "Row LINK-L11-chain: L11 meta-row anchor text 'chain rule' carries data-concept='derivative' and links to L04 def-derivative.",
        "Lab docstring wording (L07 part D: 'tested through that formula') and Corollary 1.2 (statement b>0, proof handles b=0) are harmless and not counted.",
        "Card ids are unique but not contiguous within the file (M2-c379, c395, c397, c398 sit among lesson groups); not a defect.",
        "L09 Misconception 2 relies on L10 Theorem 2.1 and L11 Lemma 1.1 as labelled forward references; the value 1/6 is not derived in L09 and the lesson says so.",
        "Lesson 1 Problem M3 is cited for 1/n -> 0 in L07 Lemma 3.1 and L09 Example 3.2; that problem proves |(-1)^n/n| = 1/n < eps for n > 1/eps, so the citation is adequate.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    },
}
with open("ledgers/M2/M2-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "pass", fragment["summary"]["pass"], "fail", fragment["summary"]["fail"])
