import json, sys
from datetime import datetime, UTC
R = []
def row(id, check, location, status, evidence, fix=None):
    r = {"id": id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

S = "ledgers/FC2/scripts/FC2-a-r2/"
# ---------- hub ----------
row("FC2a-hub-structure", "2.9-structure", "course/modules/FC/FC2/index.html", "PASS",
    "tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS' re-run on e22feb3 (index changed: lede line 33, objective 3 line 50).")
row("FC2a-hub-dag", "DAG", "course/modules/FC/FC2/index.html:35", "PASS",
    "tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS'. Closure via coursekit.prerequisite_closure('FC2') = [AC1, CF1, E1, FC1, M1, M2, M4, P0.1] (" + S + "closure.py); hub line 35 names M1, M2, AC1, E1, P0.1, all present.")
row("FC2a-hub-hours", "hours", "index.html:29,41,132-142; L01-L08 data-hours", "PASS",
    "data-hours: L01=6 L02=8 L03=9 L04=7 L05=8 L06=8 L07=8 L08=6, sum 60 = data-hours-lessons=60 (index.html:29); 60+30=90; 30/90=33.3% (index.html:41). Hub card text 6/8/9/7/8/8/8/6 matches. Pace not judged (architect ruling).")
row("FC2a-hub-placement-numbers", "2.2/2.4 numbers", "index.html:69,72-126", "PASS",
    "Recomputed in " + S + "l01_recompute.py and l02_l03_recompute.py: NPV -100+60/1.1+60/1.21 = 4.1322 -> 4.13; 1/1.05^2 = 0.907029 -> 0.9070; 1/2 variance 0.25; Prob(Z<=0)=1/2; skill check 1 gap 10-4-(100-105*0.95)=5.75; skill check 2 100e^0.05 = 105.1271 -> 105.13. Nine items: 8/9=88.9% >= 80%, 7/9=77.8% (text says 78%) correct.")
row("FC2a-hub-reading-refs", "2.1 citations", "index.html:163-171 (data-cite hull2021options, stoll1969relationship, cox1979option)", "PASS",
    "tools/verify_refs.py --unit FC2 -> 'live re-verification of FC2: 3 of 560 entries, 0 problems'; tools/verify_refs.py --offline -> '560 entries, 0 problems'. All three keys present in references/references.json (cox1979option DOI 10.1016/0304-405x(79)90015-1; stoll1969relationship DOI 10.1111/j.1540-6261.1969.tb01694.x; hull2021options ISBN 9780136940166). Hub quotes no figure from them. Page content of the entries not read beyond the registry record.")
row("FC2a-hub-lessons-claim", "2.9 structure", "index.html:133; L01-L08.html", "PASS",
    "Every lesson file has one class=lab (count 1 each), one Retrieval quiz heading, one problem-set heading (grep over L01-L08). Claim 'every lesson has ... a runnable lab, a problem set with worked solutions and a retrieval quiz' holds structurally; the worked solutions were read for L01-L03 only.")
row("FC2a-hub-data-status", "data claims", "index.html:158-159; all FC2 pages", "PASS",
    "grep -l 'data-files' over course/modules/FC/FC2/*.html and index.html returns no file (exit 1): no page embeds a dataset. L01 and L02 are typed-in; L03 Part A is labelled SIMULATED (L03.html lab prediction and docstring lines 153-159).")
row("FC2a-hub-objectives-ladder", "2.9 structure", "index.html:44-55,146-155", "PASS",
    "Six objectives with measurable verbs; ladder rungs in order Worked example, Completion problem, Independent project, Stretch (index.html:150-153). Skip rule matches placement text (index.html:69,148).")
row("FC2a-hub-ladder-wording", "2.2 numbers and claims about the project", "index.html:44 vs course/modules/FC/FC2/project.html:44", "FAIL",
    "Hub line 150 says Lab 1 scans 'a six-contract SIMULATED chain'; project.html:44 says 'one six-strike SIMULATED chain'. The two pages describe the same lab with different units (strikes vs contracts).",
    "Use the project page's term in the hub (six-strike chain) or state how strikes and contracts relate, in index.html line 150.")

# ---------- L01 ----------
row("FC2a-L01-prop2.1-2.2", "2.4 mathematics", "L01.html:59,74-90 (Def 1.1; Prop 2.1; Prop 2.2)", "PASS",
    "Raw lines re-read: Def 1.1 line 59 'p.theta <= 0; (X theta)_s >= 0; p.theta < 0 or (X theta)_s > 0 for some s'. Prop 2.1 proof line 80 and Prop 2.2 proof line 90 re-derived by hand: each uses A3 on theta=a-b and -theta; strict part uses p.theta=0 with all payoffs positive. Both correct, hypotheses stated.")
row("FC2a-L01-prop3.2-3.5", "2.4 mathematics", "L01.html:111-119,128-140 (Def 3.1; Prop 3.2; Ex 3.4; Prop 3.5)", "PASS",
    "Prop 3.2 proof re-derived (p.theta = sum_s psi_s (X theta)_s). Example 3.4: psi_u=(q-9/10)/2, psi_d=(27/10-q)/2, gives 1/20, 17/20 at q=1 (" + S + "l01_recompute.py). Prop 3.5 if/only-if (lines 139-140): portfolios (-1,1) payoff (2,0) and (3,-1) payoff (0,2) verified.")
row("FC2a-L01-R1-R3", "2.4 mathematics", "L01.html:401-403, 410, 415-417 (R1-R3 solutions)", "PASS",
    "R1: psi_u=(q-9/10-eps)/2, psi_d=(27/10-q-eps)/2 re-derived; positivity interval nonempty iff 9/10<q<27/10; arbitrage portfolios (-1,1) payoff (2,1,0) and (3,-1) payoff (0,1,2) verified. R2: scaling argument line 410 correct. R3 line 417: case analysis covers q>=27/10, 9/10<q<27/10, 0<q<=9/10 (x>=|y| argument, cost >= (9/10-q)|y| >= 0 forces q=9/10 and x=|y|, payoff u = -2|y| < 0), and q<=0 (portfolio (0,1)). Complete and correct.")
row("FC2a-L01-numbers", "2.2 numbers", "L01.html:100,111-119,305,328,335,342,353,367,378,385,392,401,410,470,482,496,498", "PASS",
    "Recomputed exact fractions in " + S + "l01_recompute.py: misconception cost 1-2*9/10=-4/5, payoff (1,-1); M1 cost 4/5, payoff (-1,1); M2 psi=(1/10,7/10); M3 t(-5,9) payoff t(22,4); P3 sum 9/10; Q 1 bond minus 2 stocks cost -11/10. All match.")
row("FC2a-L01-lab", "2.5 labs", "tests/labs/FC2/lab-FC2-L01-1.py; L01.html lab section lines 149-285", "PASS",
    "tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'. python -I -W error on the twin exits 0. Printed output (L01.html:266-284) reproduced by " + S + "l01_recompute.py: 0 arbitrage in Part A; 30 in Part B (box -10..10); 302 dominance pairs both parts, 0 misordered in A and 38 in B; state prices 1/20, 17/20 and -1/5, 11/10. Prediction text (L01:150) matches these.")
row("FC2a-L01-keyresult-433", "2.3 grades (hypotheses)", "L01.html:433 (Key results row, grade T)", "FAIL",
    "Row reads 'With the bond at 9/10, the market has no arbitrage opportunity if and only if the stock price lies strictly between 9/10 and 27/10 (Proposition 3.5)'. Proposition 3.5 (L01.html:134) is stated 'In the market of Example 3.4', i.e. the payoff matrix bond (1,1), stock (3,1) is a hypothesis the row drops. Witness: bond (1,1), stock (2,2), bond 9/10, stock 1 (inside the row's interval): theta=(-2,1) costs -0.8 and pays (0,0), so an arbitrage exists although 9/10<1<27/10.",
    "Restore 'In the market of Example 3.4' at the start of the row text (L01.html line 433).")
row("FC2a-L01-scope-words", "2.9 structure and scope", "L01.html:59,95,129,285,296,385", "PASS",
    "Every, all, any, only, always occurrences in L01 checked: 'for every state' claims are proof-level (Def 1.1, Prop 2.2); 'for any holdings whatever' (L01:129) follows from Prop 3.2; 'infinitely many' (E2) follows from scaling; 'no arbitrage in that box only' (L01:285) is bounded by the box.")
row("FC2a-L01-quiz", "2.9 structure", "L01.html section 8, lines 441-516", "PASS",
    "All ten quiz items checked against their explain blocks: correct answers Def 1.1 (cost 0, payoff (22,4)), psi_u=1/20, Prop 2.1 under A3, zero-cost holding (-5,9), Prop 3.5 open interval, upper end 27/10 with (3,-1), Lab 1 box count, A3 hypothesis, cost -1 arbitrage (strictly negative cost meets third condition), cost -11/10.")
row("FC2a-L01-notation-m", "notation", "L01.html:55 and :401-403 (symbol m)", "FAIL",
    "L01.html:55 defines m as 'the number of states' ('exactly one of m states occurs'). R1 (L01.html:401) introduces 'a third state m' and uses 'm' as a state label in psi_m and payoffs (2,1,0) in states u, m, d. One symbol with two meanings on the same page; the notation registry has no entry for m, but the lesson's own definition is contradicted.",
    "Rename the R1 state, for example to 'v' or 'h', in L01.html lines 401-403 and the explain text.")

# ---------- L02 ----------
row("FC2a-L02-A3-scope", "2.4 mathematics (hypotheses)", "L02.html:76 (A3), :93, :242", "PASS",
    "A3 now reads 'in the one-period market of Lesson 1 ... for the dates indicated: dates 0 and tau for Proposition 2.2, and dates t and tau for Proposition 3.1'. Lesson 1's market has dates 0 and 1 (L01.html:55); the relabelling to tau and t is stated. Prop 2.2 Case 1 and Case 2 (L02.html:99-100) use only dates 0 and tau.")
row("FC2a-L02-A2-canon", "2.4 mathematics (hypotheses)", "L02.html:71, 277", "PASS",
    "A2 (L02.html:71) states 'with no default risk' for the loan and deposit; canon item (L02.html:277) now says 'A2 assumes no default risk on the loan and deposit at rate r. It does not say that the forward's counterparties perform'. Consistent with A2 text.")
row("FC2a-L02-prop2.2", "2.4 mathematics", "L02.html:93-101", "PASS",
    "Re-derived both cases: Case 1 (sell forward at F, buy unit with loan S) net 0 at date 0 and F - S e^{r tau} > 0 at expiry in every state; Case 2 (buy forward, short unit, lend S) net S e^{r tau} - F > 0. Both excluded by A3; F = F*. Correct under A1-A4.")
row("FC2a-L02-prop3.1-value", "2.7 terms before definition", "L02.html:121 (Lab 2 prediction 'Part E values a fair forward'), :235 (printed 'value 237.11'), :242 (definition of value), :245-256", "FAIL",
    "The definition 'Define the value of a long forward at date t ...' is at L02.html:242, in Section 3, after Lab 2 (lines 120-236). Lab 2 Part E and the Introduction (L02:51 'values a forward during its life') use the term before the definition. The Prop 3.1 statement (L02:245-248) is correct under its hypotheses.",
    "Move the definition of value to Section 2 (before Lab 2) or add 'defined in Section 3' at first use in the Introduction and in the Lab 2 prediction.")
row("FC2a-L02-rounding-M1-M2", "2.2 numbers", "L02.html:309,316,323", "PASS",
    "M1: e^{0.025} = 1.0253151205 (exact 1.02531512052), 50 x 1.0253151205 = 51.265756025 -> 51.265756, 51.27. M2: e^{0.01} = 1.0100501671, 80 x = 80.80401337 -> 80.804013; 81-80.804013 = 0.195987 -> 0.20. M3: e^{-0.015} = 0.985112 (exact 0.98511194), 100 x = 98.511194 -> 98.5112; 104-98.5112 = 5.4888 -> 5.49. All recomputed in " + S + "l02_l03_recompute.py.")
row("FC2a-L02-E3-value", "2.2 numbers (unrounded basis)", "L02.html:373", "PASS",
    "F = 5000 e^{0.025} = 5126.575603 (unrounded), displayed 5126.58. e^{-0.0125} = 0.98757780 (exact 0.9875778005). F e^{-0.0125} = 5062.892258 -> 5062.8923. Value 5300 - 5062.892258 = 237.107742 -> 237.11 (and 237.1077 as written). Computed from unrounded F, as the page now states.")
row("FC2a-L02-lab-partC", "2.5 labs (printed vs code)", "tests/labs/FC2/lab-FC2-L02-1.py:181-185; L02.html:121,221-223", "PASS",
    "The code prints 'date-0 cash legs ... 0 -5000 5000' and 'net cash today ... zero by construction: 0' (lab lines 181-185), built from constants; the page prediction (L02:121) and interpretation (L02:237) say so. Previous defect (net_today = SPOT - SPOT) removed.")
row("FC2a-L02-lab-run", "2.5 labs", "tests/labs/FC2/lab-FC2-L02-1.py", "PASS",
    "tools/run_labs.py --unit FC2 -> PASS (11/11). python -I -W error exit 0. mypy --no-incremental on the twin: Success. Printed output L02.html:211-236 equals the run (run_labs embed check). Parts A-E values recomputed: 5126.58; -2126.58, -626.58, 873.42, 2373.42; 73.42 each state; 0 at fair; 237.11.")
row("FC2a-L02-R1-R3-P1-P3", "2.4 mathematics", "L02.html:332-348, 382-400", "PASS",
    "P1: F = S e^{r tau} - I e^{r(tau-t1)} = (S - I e^{-r t1}) e^{r tau} re-derived. P2 partial derivatives S tau e^{r tau}, S r e^{r tau}, e^{r tau} recomputed. P3 payoff F2-F1 > 0 re-derived. R1 both arbitrage constructions re-derived (net F - S e^{r_b tau} > 0; S e^{r_l tau} - F > 0). R3: (1.05)^2 = 1.1025 and e^{0.1} = 1.105171 gap 0.00267 -> 0.0027 correct.")
row("FC2a-L02-cards-numbers", "2.2 numbers in prose", "L02.html:111,116,475,489", "PASS",
    "Example 2.4 51.2658 and 51.27; Remark 2.5 e^{r tau} > 1; quiz 5.4888 -> 5.49; quiz e^{0.1} = 1.105171 -> 1.1052 (fifth decimal 7). Recomputed in l02_l03_recompute.py. Cards.json is outside this slice and was not read.")
row("FC2a-L02-quiz-wording", "2.9 structure", "L02.html:441-447", "PASS",
    "Question now 'Which input does the no-arbitrage forward price NOT depend on?' with options spot, rate r, expected spot; answer third, explained by Remark 2.3 (L02:106). Correct and unambiguous over the three options.")
row("FC2a-L02-plan-exact-lab", "plan conformance", "plans/FC2-build-plan.md section 5.7 (line 'Exact labs (L01-L06 ...) print exact values') and section 6.1 ('computed from Fractions or stated as a model input')", "FAIL",
    "Lab 2 (L02, in the L01-L06 exact-lab list) computes its values with math.exp in floating point (tests/labs/FC2/lab-FC2-L02-1.py:146, 165-203) and prints them to 2 decimals. The page states this honestly (L02.html:237), so the learner text is not misleading; the plan's stated rule is not met.",
    "Architect to amend plan 5.7 for L02 (closed forms with exp print to a stated number of decimals, as plan 5.7 already allows for L07), or the builder to use Decimal with stated precision. No page change required beyond the amendment.")
row("FC2a-L02-line294-cost-of-carry", "2.6 causal and directional claims", "L02.html:294 ('A price above spot is the cost of carry.')", "FAIL",
    "The sentence is a general claim that any price above spot is the cost of carry. The same paragraph (L02:294) says a mispricing is 'a price different from F* in either direction', and a price above spot can be a mispricing (Lab 2 Part C, quote 5200 > F* = 5126.58 > S = 5000 is one). Only the excess F* - S is the cost of carry.",
    "Replace 'A price above spot is the cost of carry' with 'The excess of the fair price F* over spot is the cost of carry' in L02.html line 294.")
row("FC2a-L02-keyresults-hypotheses", "2.3 grades: hypotheses omitted in T rows", "L02.html:411,412,413,414,416 (Key results)", "FAIL",
    "Row 411 'The forward price depends only on S, r and tau' omits A1-A4 (Remark 2.3 uses Prop 2.2). Counterexample: with a known income (Problem P1, L02.html:332) the price is (S - I e^{-r t1}) e^{r tau}, which depends on I. Row 412 (Prop 3.1) omits A1-A4 and A3 at each date t (L02:245-246). Row 413 (Cor 3.2) omits the same plus F = F*. Row 414 (P1) omits A2-A4 and A3. Row 416 (R1) omits A1 and A3. Witness: S = 100, r = 0, tau = 1, income I = 5 at t1 = 0.5 (the no-arbitrage price by Problem P1 is S - I = 95). F = 95 lies below S e^{r_l tau} = 100, so it is outside the R1 interval, yet it admits no arbitrage: buy the forward at 95 and sell the unit short (receive 100, pay the income 5 at t1, hold 95 to tau, pay 95 at tau) gives 0 at tau in every state; sell the forward at 95 and buy the unit with a loan of 100 (receive the income 5, receive 95 at tau, repay 100) gives 0 at tau in every state. The row's 'admits arbitrage' claim is false without A1.",
    "Add the hypotheses to rows 411-414 and 416 in the Key results table: 'Under A1 to A4 and A3' for 411-413, 'Under A2 to A4 and A3, dropping A1' for 414, 'Under A1 (no income), A3 and A4 with rates r_l, r_b' for 416.")

# ---------- L03 ----------
row("FC2a-L03-notation-Rstar", "notation", "L03.html:122-151 (R_par), notation/notation.json symbols[4]", "PASS",
    "The page now uses R_par; grep finds no R^\\ast in L03.html. notation.json registers R^\\ast only as the AP1 SDF return; R_par is not registered and is defined locally at L03.html:122.")
row("FC2a-L03-DF-positivity", "2.4 mathematics (hypotheses)", "L03.html:105 (A8), :128 (Prop 3.3 proof)", "PASS",
    "A8 now requires DF_i > 0; the Prop 3.3 proof derives sum DF_i > 0 from A8 (L03:128). Counterexample L03:105 re-verified: n=2, DF_1=1/2, DF_2=-1/2 gives L_1 = 1, L_2 = -2 by the coupon relation, sum DF = 0, and the Prop 3.3 equation reads 0 = 3/2.")
row("FC2a-L03-prop1.3", "2.4 mathematics", "L03.html:71-77,81-82", "PASS",
    "Telescoping re-derived: B_i = sum_{k<=i} (F_k - F_{k-1}) = F_i - F_0 under A8' (B_0=0). Remark 1.4 claims (identity, no price model, no F_n-spot relation) follow from the proof.")
row("FC2a-L03-prop3.2", "2.4 mathematics", "L03.html:110-117", "PASS",
    "DF_i L_i = DF_i(DF_{i-1}/DF_i - 1) = DF_{i-1} - DF_i (uses DF_i != 0 from A8), summed to 1 - DF_n using DF_0 = 1. Correct under A8.")
row("FC2a-L03-example3.4", "2.4 mathematics", "L03.html:133", "PASS",
    "Geometric sum x(1-x^n)/(1-x) = (1-x^n)/rho with x/(1-x) = 1/rho (rho != 0), giving rho sum DF = 1 - DF_n and R_par = rho. rho = 0 handled separately: (1-1)/n = 0. Correct. The 'M1' ambiguity is resolved (concept geometric-series, module M1).")
row("FC2a-L03-prop3.5-value", "2.4 mathematics", "L03.html:138-143 (Prop 3.5)", "PASS",
    "Value (R_par - K) sum DF_i re-derived (floating leg 1 - DF_n minus K sum DF_i, with Prop 3.3). Sign claim uses sum DF_i > 0 from A8 (L03:143). Correct.")
row("FC2a-L03-R1-R3", "2.4 mathematics", "L03.html:393-395, 400-402, 407-409", "PASS",
    "R1: PV = DF_1/G_1 - DF_1 = 1 - DF_1 iff G_1 = DF_1 re-derived. R2: weights DF_i/(DF_1+DF_2) positive under A8, sum 1, value strictly between f_1 and f_2 when f_1 != f_2. R3: DF_1 = 0.970874, DF_2 = 0.924642, R_par = 0.0397561 -> 3.9756 percent (recomputed); flat 3% DF_2 = 0.942596 correct.")
row("FC2a-L03-keyresult-P3", "2.3 grades", "L03.html:426 (Key results, grade T)", "PASS",
    "Row says 'With interest at a rate rho != 0 on the margin account the balance is sum Delta_i (1+rho)^{n-i}, which differs from F_n - F_0 on some price paths (Problem P3)'. P3 (L03:357-359) gives the formula by induction and the witness Delta_1=1, Delta_2=0 with B_2 = 1+rho. Hypotheses now stated.")
row("FC2a-L03-keyresult-425", "2.3 grades (hypotheses omitted)", "L03.html:425 (Key results, grade T)", "FAIL",
    "Row reads 'The value to the fixed payer is (R_par - K) sum DF_i per unit of notional (Proposition 3.5)'. Proposition 3.5 (L03.html:138) is 'Assume A8'. Row 422 and 423 carry 'Under A8'; row 425 does not. Witness: with n = 2, DF_1 = 1/2, DF_2 = -1/2 (A8 fails), sum DF_i = 0 and the stated sign rule ('positive when K < R_par') has no meaning since R_par is undefined.",
    "Prefix row 425 with 'Under A8' (L03.html line 425).")
row("FC2a-L03-M3-rounding", "2.2 numbers (displayed digits)", "L03.html:334, 490", "PASS",
    "Unrounded sum 2.6730119495 (exact 1/1.06 + 1/1.06^2 + 1/1.06^3). Displayed digits 0.943396 + 0.889996 + 0.839619 = 2.673011, and the page now says so. Value 100 x 0.01 x 2.6730119 = 2.6730119 -> 2.67; per unit 0.026730119 -> 0.0267301 to seven places.")
row("FC2a-L03-lab-run", "2.5 labs", "tests/labs/FC2/lab-FC2-L03-1.py; L03.html:259-275", "PASS",
    "tools/run_labs.py --unit FC2 PASS; python -I -W error exit 0; mypy on the twin success. Path 5000 5039 5070 5104 5069 5103 5090 5054 5077 5106 5084 reproduced from seed 20261028 (" + S + "l02_l03_recompute.py). Margins sum 84; 4 loss days; DF values 0.970874 0.933511 0.888996 0.838561 0.783526; par 0.049026 (4.90262450 percent); payment 4902624.50 -> 4902625 cents; value -4415468.36 -> -4415468 cents. All printed values match.")
row("FC2a-L03-E1-E3", "2.9 structure and printed-output claims", "L03.html:370-384", "PASS",
    "E1: largest loss 36 on day 7 (margin -36; prices 5090 -> 5054) recomputed. E2: exact integer comparisons, labelled SIMULATED. E3: 0.049026 -> 4.9026 percent to four places; 4902625 cents = 49,026.25 dollars; par lies between 4% and 5% and equals neither zero rate.")
row("FC2a-L03-annuity-zero-rate", "2.7 terms before definition", "L03.html:153 (prediction: 'annual zero rates', 'the annuity'), :162, :203 (code docstring defines zero rate), :254/:275 (printed 'the annuity')", "FAIL",
    "'Annuity' is never defined in the lesson text: it appears first in the Lab 3 prediction (L03.html:153) and the printed label (L03.html:275), and the only definition is the code variable 'annuity = sum(dfs[1:])' (lab line 240). 'Zero rate' is used in the Lab 3 prediction (L03.html:153) before any definition; it is defined only inside the lab docstring (lab line 203, displayed after the prediction).",
    "Define 'annuity' as A = sum_i DF_i in Section 3 next to Proposition 3.5, and define 'zero rate' (rate z_i with DF_i = (1+z_i)^{-i}) in Section 3 before Lab 3.")
row("FC2a-L03-lab-rounding-claim", "2.5 labs (what the lab says it does)", "L03.html:276", "FAIL",
    "L03.html:276 states 'the only rounding is the half-up rounding of the payment and value to the cent'. The lab also prints discount factors and the par rate 'to six places' (lab lines 239, 245 via f'{...:.6f}'), which is rounding of displayed values. The computation is exact as stated; the sentence claims more than the output.",
    "Change to 'In the computation the only rounding is the half-up rounding of the payment and value to the cent; the six-place printed values are display rounding.' (L03.html line 276).")
row("FC2a-L03-notation-rho", "notation", "L03.html:133 (rho annual rate) and :357 (rho per day), :426", "FAIL",
    "rho is the annual flat rate in Example 3.4 (DF_i = (1+rho)^{-i}, annual periods, L03:133) and the per-day rate in Problem P3 (B_i = (1+rho) B_{i-1} + Delta_i, L03:357). The same symbol carries two meanings with different periods in one lesson. Not a registry symbol; a local conflict.",
    "Rename the per-day rate in P3 and Key results row 426 to a new symbol such as r_d (L03.html lines 357-359 and 426).")

# ---------- cross-cutting ----------
row("FC2a-prose-banned-process", "2.9 banned phrases and process words", "index.html, L01.html, L02.html, L03.html", "PASS",
    "check_pages FC2 PASS (banned strings). grep for builder, verifier, round, request, unit report, planner, ledger, TODO, roughly, historically, about 6%, ellipsis: only 'round trip' (index.html:142) which is a finance term.")
row("FC2a-dag-concepts", "DAG", "L01-L03.html and index.html", "PASS",
    "check_dag FC2 PASS. Terms outside the prerequisite closure (forward rate, day count, projection curve, bid-ask spread, yield, law of one price, cost of carry, accrual) appear as plain prose with no link and no dfn (grep of href/data-concept over the four pages). L03 links geometric-series (module M1, inside the closure).")
row("FC2a-labs-gate", "gates", "tests/labs/FC2/lab-FC2-L0{1,2,3}-1.py", "PASS",
    "ruff check on the three twins: 'All checks passed!'; ruff format --check: '3 files already formatted'; mypy --no-incremental on L01, L02, L03 twins: success (run in this checkout); run_labs FC2 PASS (11/11).")
row("FC2a-page-smoke", "2.5 labs in Pyodide and browser", "course/modules/FC/FC2/index.html, L01-L03.html", "PASS",
    "tools/page_smoke.py --unit FC2 --pages index.html L01.html L02.html L03.html -> 'page_smoke FC2: PASS'. The tool serves course/ and loads each page in Chromium; the four slice pages pass. The 10 s Pyodide bound for each lab was not timed separately.")

frag = {
  "unit": "FC2", "slice": "FC2-a", "round": 2,
  "verifier": "independent Haiku verifier, FC2 slice a, round 2 (hub index.html, L01-L03, lab twins L01-L03); shares no context with the builders",
  "pin": "e22feb3", "base": "55b5634 (round-1 pin; delta computed from git diff -U0 55b5634 e22feb3)",
  "previous_ledger": "/tmp/fanout-frags/C-FC2-a.round1.json",
  "checkout": "/tmp/verifyC2-FC2-a (detached at e22feb3; .venv symlinked)",
  "scratch": "/tmp/fc2a-v",
  "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
  "verdict": "FAIL",
  "rows": R,
  "mutants": [],
  "registry_flags": [],
  "freshness_flags": [],
  "notes": [
    "Delta since 55b5634 for this slice: index.html (lede line 33, objective 3 line 50); L01.html (lines 51, 69, 296, 309, 434); L02.html (lines 51, 76, 106, 237, 242-256, 266-278, 294, 309-316, 323, 339-341, 373, 411-416, 441, 475); L03.html (lines 105, 122-151, 305-334, 357-359, 384, 407-426, 490); tests/labs/FC2/lab-FC2-L02-1.py (lines 57-62, and the Part C block). lab-FC2-L01-1.py and lab-FC2-L03-1.py are byte-identical to 55b5634 but were re-run.",
    "Carry-forward: none used. Every round-1 row was re-verified because its subject changed or its command was re-run; row ids are kept. All round-1 FAIL rows were re-checked from scratch and are now PASS except L02-prop3.1-value (now FAIL for ordering, see row) and L02-plan-exact-lab (still FAIL).",
    "Round-1 FAIL rows now PASS: L02-A3-scope, L02-A2-canon, L02-rounding-M1-M2, L02-E3-value, L02-lab-partC, L02-quiz-wording, L03-notation-Rstar, L03-DF-positivity, L03-example3.4, L03-keyresult-P3, L03-M3-rounding.",
    "Not checked (outside this slice): cards.json, project.html content beyond the hub's references to it (hub lines 150-153), L04-L08 pages (only their lab/quiz/problem-set headings were counted for the hub claim), plan sections other than 5.7 and 6.1, and the Atlas contract (none named for this slice).",
    "Hypothesis sweep: every Key results row in L01-L03 was compared with its proposition's Assume line; the four rows listed as FAIL are the omissions found. Witnesses are reproduced in the row evidence (exact fraction arithmetic by hand, plus " + S + "l01_recompute.py for the L01 witness counts)."
  ],
  "summary": {}
}
import collections
c = collections.Counter(r["status"] for r in R)
frag["summary"] = {"rows": len(R), "pass": c["PASS"], "fail": c["FAIL"], "unverifiable": c["UNVERIFIABLE"], "mutants": 0}
json.dump(frag, open("/tmp/verifyC2-FC2-a/ledgers/FC2/FC2-a.json", "w"), indent=2, ensure_ascii=False)
print(frag["summary"])
