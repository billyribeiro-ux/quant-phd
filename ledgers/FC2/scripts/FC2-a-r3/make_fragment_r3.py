import json, datetime
SCR = "ledgers/FC2/scripts/FC2-a-r3/"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/S-FC2-a.round2.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}

# status/evidence/fix for every carried id (round-2 ids kept) -- all re-verified at 8196077d this round
upd = {}
def U(i, status, evidence, fix=None, location=None):
    upd[i] = dict(status=status, evidence=evidence, fix=fix, location=location)

U("FC2a-cmd-check_pages", "PASS",
  f"Re-run at 8196077d: `.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS', exit 0 ({SCR}check_pages.out).")
U("FC2a-cmd-check_dag", "PASS",
  f"Re-run: `.venv/bin/python tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS' ({SCR}check_dag.out).")
U("FC2a-cmd-check_projects", "PASS",
  f"Re-run: `.venv/bin/python tools/check_projects.py --unit FC2` -> 'check_projects FC2: PASS' ({SCR}check_projects.out). Unit-level only; project.html is not judged in slice a.")
U("FC2a-cmd-run_labs", "PASS",
  f"Re-run: `run_labs.py --unit FC2 --page index` -> 'PASS (0/0)'; `--page L01`, `L02`, `L03` -> 'PASS (1/1)' each (exit 0; {SCR}run_labs.out).")
U("FC2a-cmd-twin-direct", "PASS",
  f"Re-run with the project interpreter `.venv/bin/python` (Python 3.14.8) as `python -I -W error tests/labs/FC2/lab-FC2-L0N-1.py` from /tmp/fc2a-r3 with env -i PATH=/usr/bin:/bin PYTHONHASHSEED=0: exit 0 for L01, L02, L03; stderr 0 bytes; 19, 26, 17 stdout lines ({SCR}twin_direct.out, twin-L0N.out/.err). Note: /usr/bin/python3 is 3.9.6 and fails on zip(strict=True) at lab-FC2-L01-1.py:69; that is the interpreter, not the twin (the pinned runtime is 3.14).")
U("FC2a-cmd-page_smoke", "PASS",
  f"Re-run: `.venv/bin/python tools/page_smoke.py --unit FC2 --pages index L01 L02 L03` -> index, L01, L02, L03 each PASS with their labs, 'page_smoke FC2: PASS', exit 0 ({SCR}page_smoke.out).")
U("FC2a-cmd-ruff-mypy", "PASS",
  f"Re-run on the three twins: `ruff check` 'All checks passed!'; `ruff format --check` '3 files already formatted'; `mypy --no-incremental` 'Success: no issues found in 3 source files' ({SCR}ruff_mypy.out).")
U("FC2a-cmd-pytest", "PASS",
  f"Re-run: `pytest -q tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py tests/test_curriculum.py` all dots, exit 0; `pytest --collect-only -q tests/test_labs.py -k FC2` -> 11 items ({SCR}pytest.out).")
U("FC2a-cmd-verify_refs", "PASS",
  f"Re-run: `verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems'; `verify_refs.py --unit FC2` -> 'live re-verification of FC2: 4 of 560 entries, 0 problems' ({SCR}verify_refs.out). references/ is byte-identical to the round-2 pin.")
U("FC2a-links", "PASS",
  f"{SCR}structure_links_r3.py (output {SCR}structure_links_r3.out): 0 failures. Every relative href resolves; every in-page anchor exists; every data-cite key (3 on index.html) is in references/references.json (560 keys); every concepts.html#id used by index/L01-L03 (11 distinct ids, 20 uses) exists as an id in course/concepts.html; no external href; no data/ or data-files reference; no banned or process word (BUILDER_RULES 1.3-1.4, 12) in the four pages.")
U("FC2a-twin-equals-page", "PASS",
  f"{SCR}page_twin.py (output {SCR}page_twin.out): for L01, L02, L03 the unescaped, stripped code block of the page equals tests/labs/FC2/lab-FC2-L0N-1.py, and the expected block equals the twin's stdout under python -I -W error (0 stderr bytes).")
U("FC2a-hub-hours", "PASS",
  "index.html data-hours-lessons=60, data-hours-project=30, sum 90 = curriculum/curriculum.json FC2 hours 90 (prereqs M4, CF1, FC1). Lesson data-hours (grep, this pin): L01 6, L02 8, L03 9, L04 7, L05 8, L06 8, L07 8, L08 6, sum 60. Hub card kickers 6/8/9/7/8/8/8/6 h match. Hub bar widths 66.7% / 33.3% = 60/90, 30/90.")
U("FC2a-hub-placement-arithmetic", "PASS",
  f"Hub #placement items Pq1-Pq9 recomputed (Fraction/Decimal, {SCR}numbers_r3.py): E[X]=3.5; Var=0.25; Pr(Z<=0)=1/2; Var(X+Y)=VarX+VarY; NPV=4.1322 -> 4.13; DF=1/1.1025=0.9070; Pq7 clearing house (matches L03 Definition 1.1); skill 1 gap 10-4-(100-105*0.95)=5.75; skill 2 (index.html line 124) gap 312-240-(5000-5200*0.95)=12. Mastery 0.8 of 9 = 8 right; 7/9=77.8%, 8/9=88.9%. The rung-2 blanks in project.html (lines 226, 228, 241) include the parity-gap line that Pq9 and the ladder text name.")
U("FC2a-hub-prose", "PASS",
  "coursekit.prerequisite_closure('FC2') (run this round) = [AC1, CF1, E1, FC1, M1, M2, M4, P0.1]; the hub's 'Their closure adds M1, M2, AC1, E1 and P0.1' matches. FC1 is a direct prerequisite (curriculum.json prereqs [M4, CF1, FC1]). Ladder text matches project.html rung 2 (three blanks, lines 226/228/241). Lede 'the one price consistent with no riskless profit' is the Proposition 2.2 claim under A1-A4 (see FC2a-L02-why-only-price).")
U("FC2a-structure-lessons", "PASS",
  f"{SCR}structure_links_r3.out: why-it-matters 114/116/118 words (<=120); sections 1-3 then lab, canon-breaks, misconceptions (3 each), problem set (3 per tier each: mechanics, proof, empirical, research), key-results table, quiz (10/9/10 items, 8-15 required), references, in that order on L01, L02, L03. Hub: 6 objectives; placement with 9 items, 2 data-skill, data-mastery 0.8; lesson map; 4 ladder rungs in order.")
U("FC2a-numbers-prose", "PASS",
  f"{SCR}numbers_r3.py recomputes every displayed value with Fraction/Decimal/float: 50e^0.025=51.265756 -> 51.2658 / 51.27; 5126.58 cents; 73.42 (5200-5126.5756); 237.11 (237.1077; discounted 5062.8923); replication -2126.58, -626.58, 873.42, 2373.42; R3 e^0.1-1.1025=0.002671 -> 0.0027, e^0.1=1.105171 -> 1.1052; M3 100e^-0.015=98.5112, value 5.4888 -> 5.49; M2 80e^0.01=80.804013, profit 0.195987 -> 0.20; M1 e^0.025=1.0253151205; DF 0.970874, 0.933511, 0.888996, 0.838561, 0.783526 (sum 4.415468); unrounded par 0.0490262450 -> 0.049026 (4.9026%); payment 4902624.503 cents -> 4902625 (half-up); value -4415468.36 -> -4415468; M2 DF3 0.839619; M3 DFs 0.943396+0.889996+0.839619 = 2.673011 displayed, 2.6730119 unrounded, value 0.026730119 -> 0.0267301, 2.67 dollars; E1 margins 39 31 34 -35 34 -13 -36 23 29 -22; R3 DF2 0.924642, par 0.039756 (3.9756%), flat-3% DF2 0.942596; hub 33.3%=30/90 and 7/9=77.8%. No prose number differs from its unrounded value at the stated rounding.")
U("FC2a-L01-math", "PASS",
  "L01.html Sections 1-3 read in full (lines 53-146) and every displayed result re-derived: Def 1.1; Prop 2.1 (proof via -theta); Prop 2.2 (weak and strict parts); Remark 2.3; Example 2.4 (a=(0,2) cost 2, pays (6,2); b=(1,1) cost 19/10, pays (4,2)); Def 3.1; Prop 3.2 (A3 not assumed; proof sums psi_s (X theta)_s); Example 3.4 (psi_u=(q-9/10)/2, psi_d=(27/10-q)/2; q=1 gives 1/20, 17/20); Prop 3.5 (if: Prop 3.2; only if: (-1,1) at q<=9/10 and (3,-1) at q>=27/10); Remark 3.3 (det -2); Remark 3.6 (boundary portfolios). Hypotheses complete for every T result; R1, R2, R3 re-derived (problem set, FC2a-L01-problems). Hunk since 9294b914 (A3 block, why-it-matters 'within its search box') read; no mathematical change.")
U("FC2a-L01-problems", "PASS",
  "L01.html problem set (lines 319-422) re-derived: M1 cost 4/5, payoff (-1,1); M2 psi (1/10, 7/10); M3 zero-cost set t(-5,9), payoff t(22,4); P1-P3 proofs; E1 values (-5,9), 0, 22, 4 from Lab 1 Part B; E2 (box count vs infinitely many by scaling); E3; R1 (psi_w = eps, interval 0<eps<min(q-9/10, 27/10-q), payoffs (2,1,0) and (0,1,2)); R2 (scaling); R3 (bond short-sale ban, all four cases incl. q<=9/10 with y<0 and q=9/10 equality case). Misconception numbers (-4/5; (1,-1); 1/20+17/20=9/10) recomputed.")
U("FC2a-L02-math", "PASS",
  "L02.html Sections 1-3 read in full (lines 53-267). Definition 2.1; Prop 2.2 Case 1 (sell forward, buy unit with loan S; net 0; payoff F - S e^{r tau} > 0 excluded; so F <= F*) and Case 2 (buy forward, short unit, lend S; payoff S e^{r tau} - F; so F >= F*) re-derived with A1 (no income), A2 (short and lend), A3, A4. Prop 3.1 (V_t = S_t - F e^{-r(tau-t)}) and Corollary 3.2 (V_0 = 0; sign statement) re-derived; hypotheses complete for Prop 2.2, Prop 3.1 and Corollary 3.2. The A2 forward pointer to A4 is a separate row (FC2a-r3-L02-sec1-forward-ref).")
U("FC2a-L02-problems", "FAIL",
  "L02.html line 332, Problem P1: 'Drop A1 and suppose the asset pays a known income I ... Keep A2 to A4.' A3 is not kept, but the solution invokes the argument of Proposition 2.2, which needs A3 to exclude the arbitrage (Prop 2.2 line 93: 'Assume A1 to A4 ... and the market has no arbitrage opportunity'). Card FC2-c028 (cards.json line 187) states the same problem as 'A2 to A4 and A3 kept', so the card and the page disagree. The key-results row (L02.html line 414) grades P1 T. The other problems were re-derived: M1 50e^0.025=51.265756; M2 80.804013 and 0.195987; M3 98.5112 and 5.4888; P2 monotonicity (partial derivatives S tau e^{r tau}, S r e^{r tau}, e^{r tau}); P3 (F2 - F1 > 0); E1-E3 (5126.58; 73.42 = 5200 - 5126.58; 237.1077); R1 (interval [S e^{r_l tau}, S e^{r_b tau}]; the solution says it does not prove the converse); R2; R3 (0.0027 unrounded 0.002671).",
  fix="Problem P1 statement at L02.html line 332: 'Keep A2 to A4 and A3.' (The key-results row at line 414 is then T with A3 stated.)")
U("FC2a-L03-math", "FAIL",
  "L03.html Sections 1-3 read in full (lines 53-150). Re-derived: Def 1.2; Prop 1.3 telescoping (B_i = F_i - F_0, Assume A8'); Prop 3.2 coupon PV DF_{i-1}-DF_i telescoping to 1 - DF_n; Prop 3.3 R_par = (1-DF_n)/sum DF_i, unique because sum > 0 under A8 (counterexample n=2, DF_1=1/2, DF_2=-1/2: sum 0 and equation reads 0 = 3/2, checked); Prop 3.5 sign. Two defects: (a) Example 3.4 (lines 133-135) states DF_i=(1+rho)^{-i} for rho != 0 with no A8 and no rho > -1, but its proof uses Prop 3.3 (which 'Assume A8') and divides by sum DF_i. Own check ({SCR}numbers_r3.py, inline run): rho=-2, n=2 gives DF=(-1, 1), sum 0, formula 0/0, so R_par = rho is not established; see row FC2a-r3-ex34-hypothesis. (b) Proposition 3.2 title (line 109) '(the floating leg is worth par)' contradicts its statement 1 - DF_n; see row FC2a-r3-prop32-title. Also FC2a-r3-L03-def31-forward-ref (Definition 3.1 uses L_i before A8 defines it).",
  fix="Fix the two rows FC2a-r3-ex34-hypothesis and FC2a-r3-prop32-title. Derivations otherwise PASS.")
U("FC2a-L03-problems", "PASS",
  "L03.html problem set (lines 311-414) re-derived: M1 margins 3, -4, 2; balances -1 and 1 dollars; M2 DF_3 = 1.06^-3 = 0.839619; M3 sum DF 2.6730119 (displayed 2.673011), value 0.026730119 per unit, 2.67 dollars on 100; P1 n=2 telescoping; P2 (value -h sum DF; -4415468 cents is lab-printed, see FC2a-cards-trivia); P3 with eta > -1: B_n = sum Delta_i (1+eta)^{n-i}, and the path Delta_1=1 gives B_n=(1+eta)^{n-1}, equal to 1 only when eta=0; E1 largest loss 36 on day 7 (prices 5090 -> 5054); E2; E3 (4.9026%, 49,026.25 dollars, between 4% and 5%); R1 (G_1, equality iff G_1 = DF_1); R2 (weights DF_1/(DF_1+DF_2), DF_2/(DF_1+DF_2)); R3 (DF_2 = 0.924642; R_par = 0.039756 = 3.9756%; flat-3% DF_2 = 0.942596).")
U("FC2a-lab-L01-claims", "PASS",
  f"Lab 1 hypothesis, interpretation and misconceptions 1-3 checked against {SCR}numbers_r3.out (own brute force over box -10..10 with Fraction): Part A arbitrage count 0; state prices 1/20, 17/20; dominance pairs 302 with 0 misordered. Part B arbitrage count 30; state prices -1/5, 11/10; dominance pairs 302 with 38 misordered; first zero-cost positive-payoff holding (-5, 9) with payoffs 22 and 4 (also re-run: twin output). Hypothesis claims match the twin output exactly (page_twin.out). Interpretation does not claim real prices.")
U("FC2a-lab-L02-claims", "PASS",
  "Lab 2 hypothesis and interpretation match the twin output: Part A 5126.58 cents; Part B four outcomes with gap below 1e-6 (boolean True); Part C 73.42 cents in each of four states, date-0 legs 0, -5000, 5000 (constants written in the code, which the interpretation states); Part D zero; Part E 237.11 (recomputed 237.1077). Misconception 1 ('one forward price against four outcomes') and misconception 3 ('Lab 2, Part C shows one above it') match.")
U("FC2a-lab-L03-claims", "PASS",
  f"Lab 3 hypothesis and interpretation match the twin output: Part A margins 39 31 34 -35 34 -13 -36 23 29 -22; balance 84 = settlement minus initial; 4 loss days; both identities True. Part B DFs 0.970874 ... 0.783526; par 0.049026; payment 4902625; value to payer -4415468 = -1% x annuity x notional (own recomputation, {SCR}numbers_r3.out). The hypothesis says the par rate lies in the range of the typed zero rates (3-5%) and equals none of them: true: 4.9026% lies between the 3% and 5% zero rates and equals none of 3, 3.5, 4, 4.5 and 5%. Part A labelled SIMULATED (lines 154, 157-158, 277); Part B typed-in zero rates and 'does not state that they are market rates'.")
U("FC2a-grades", "FAIL",
  "Re-grade of every T claim against BLUEPRINT 3 and ruling 13: L01 Props 2.1, 2.2, 3.2, 3.5, Example 3.4 row, Problem P3 row: OK. L02 Prop 2.2, Prop 3.1, Cor 3.2, Problem P3 row, Problem R1 row: OK; Problem P1 row (line 414) is graded T without A3 that its proof needs (FC2a-L02-problems). L03 Prop 1.3, Prop 3.2 (grade OK; title wrong, FC2a-r3-prop32-title), Prop 3.3, Prop 3.5, Problem P3 row: OK; key-results row 'On a flat curve the par rate equals the flat rate (Example 3.4)' (line 425) is graded T but the example omits A8 and rho > -1 (FC2a-r3-ex34-hypothesis). No empirical claim is graded above C; lab-only numbers are C naming the lab except card FC2-c046 (FC2a-cards-trivia).",
  fix="Apply the fixes of FC2a-L02-problems (P1 statement: 'Keep A2 to A4 and A3') and FC2a-r3-ex34-hypothesis (Example 3.4 hypotheses); the key-results rows at L02.html line 414 and L03.html line 425 are then T with complete hypotheses.")
U("FC2a-notation", "PASS",
  f"notation/notation.json symbols: T (S1), Phi, gamma_3, gamma_4, R^\\ast, R^{{e\\ast}}, R_f, Q; macros include \\E, \\Prob, \\Var, \\R. Slice pages use \\E (index), \\Var (index, L01), \\Prob (index), \\ast only on F (F^\\ast local, not R). grep: no \\mathbb in the slice (ruling 1 satisfied), no Phi, gamma, Q, R_f or R^\\ast in the slice math. T appears only as the reserved symbol in text (L02.html line 55). Local symbols (tau, theta, psi, eta, rho, ell, eps, DF, R_par, F^\\ast, L_i, G_1) are defined where first used, except the forward uses listed in FC2a-r3-L02-sec1-forward-ref and FC2a-r3-L03-def31-forward-ref. Source: {SCR}structure_links_r3.py and grep.")
U("FC2a-dag-closure", "PASS",
  "check_dag FC2 PASS. Concept links in the slice: annuity, clearing-and-settlement, continuous-compounding, discount-factor, exchange-vs-otc, expectation, geometric-series, net-present-value, normal-distribution, present-value, variance (all in the closure; FC1's two concepts via the direct prerequisite FC1). Own definitions (one dfn each): arbitrage-opportunity (L01), forward-contract and cost-of-carry-forward-price (L02), futures-contract, futures-margining, interest-rate-swap (L03). Plain prose, no link, no dfn for outside-closure terms (law of one price, short sale, par rate, bid-ask), as the architect defaults allow. L02 and L03 link L01 and L02 definitions only backwards.")
U("FC2a-data", "PASS",
  "grep for data-files and data/ in index, L01, L02, L03: no match. Hub 'Data status' is accurate for the slice: no options quote, no market file; L03 Part A is SIMULATED (seeded); L01, L02 and L03 Part B use typed-in inputs that the pages state. No figure or chart in the slice (no figures-*.js).")
U("FC2a-lab-hypothesis-SIMULATED", "PASS",
  "L03 lab hypothesis (line 154), docstring (lines 157-158) and interpretation (line 277) label Part A SIMULATED; Part B is typed-in and 'does not state that they are market rates'. Hub 'Data status' says no real data is used. No real data is presented as market data in the slice.")
U("FC2a-L02-why-only-price", "PASS",
  "L02 why-it-matters (line 51): 'Under stated conditions it is the only price consistent with no arbitrage.' Prop 2.2 (Cases 1 and 2) shows that under A1-A4 any F different from F* admits an arbitrage, so F = F* is the unique no-arbitrage price in a market that satisfies the no-arbitrage hypothesis. The hypothesis-scoped claim is accepted.")
U("FC2a-cards-accuracy", "PASS",
  "All 60 L01-L03 cards (18 + 22 + 20) read in full against the current lesson text (see FC2a-cards-coverage). FC2-c050 now says 'R_par is the ratio of Proposition 3.3, which uses all the discount factors, and it equals none of the typed-in zero rates (Lab 3, Part B)', matching L03 misconception 3 (line 306) and Prop 3.3; the earlier 'weighted summary' wording is gone. FC2-c022 says 'Only a price different from F* is a mispricing (Remark 2.5; Section 5, misconception 3)', matching L02 Remark 2.5 (line 116) and misconception 3 (line 294). Card-vs-lesson mismatch found this round on FC2-c037 is in row FC2a-r3-card-c037-remark14.")
U("FC2a-cards-coverage", "PASS",
  f"{SCR}cards_r3.py (output {SCR}cards_r3.out): cards.json has 165 cards and 165 distinct ids (non-sequential ids are allowed, ruling 2); no duplicate fronts or backs; L01 18, L02 22, L03 20 cards; every number on every L01-L03 card occurs in its lesson HTML (0 misses). Coverage: Def 1.1 (L01, L02, L03), Def 2.1, Def 3.1, Def 1.2, A1-A4, A8, A8', Props 1.3, 2.1, 2.2, 3.1, 3.2, 3.3, 3.5, Cor 3.2, Example 3.4, Remarks 1.4, 1.5, 2.3, 2.5, 3.3, 3.6, Problems M3, P1, P2, P3, R1, E2, E3, and each misconception. Near-duplicate pairs (token Jaccard >= 0.4) reviewed: c168/c169 (above and below F*), c008/c138 (q=1 and q=1/2), c025/c026/c172 (value formula, zero at inception, zero later), c036/c170 (c170 is the i=n case of c036; observation only), c160/c162/c161/c066 are L05-L08 and out of slice. All pairs state distinct facts except the observation noted.")
U("FC2a-cards-trivia", "FAIL",
  "FC2-c046 (cards.json line 291): front asks 'what is the value to the payer ... in cents?', back '-h sum DF_i with h one percentage point, which is -4415468 cents (Problem P2; Lab 3, Part B)', grade T, basis 'Problem P2; Lab 3, Part B (exact)'. The number -4415468 is printed only by the lab (lab-FC2-L03-1 output). The Part B discount factors DF_1 to DF_5 appear only in the printed lab output block (L03.html line 270); no derivation on the page computes their sum 4.415468, so the number is not derived on the page. Ruling 13: a value that appears only in lab output is graded C naming the lab, and a lab-recall number on a card is the trivia class of the round-2 finding (c045 and c134 were removed for the same reason). The round-2 trivia cards c013, c023 and c138 are now T derivations and are resolved.",
  fix="Either (a) change FC2-c046 to grade C with basis 'Lab 3, Part B (exact)' and keep the number, or (b) ask only the formula: 'What is the value to the fixed payer at R_par + h?' with back '-h sum DF_i (Proposition 3.5 with K = R_par + h; Problem P2)', grade T.")
U("FC2a-cards-hypotheses", "PASS",
  "FC2-c168, FC2-c169 and FC2-c172 now name 'Under A1 to A4' (and A3 at each date for c172); c169 names A2 for the short sale and lending; c028 names A2 to A4 and A3, which the statement of Problem P1 does not yet (FC2a-L02-problems); c140 and c141 match the A2 and A3 blocks. The Example 3.4 card FC2-c043 (no A8) is handled under FC2a-r3-ex34-hypothesis. FC2-c021 names A1 only; Example 2.4 states no hypotheses, so this is recorded as an observation, not a defect.")
U("FC2a-L01-assumption-first-use", "PASS",
  "Round-2 FAIL closed at this pin. L01.html line 66 now reads 'Assumptions A1 and A2 ... are defined in Lesson 2, Section 1, and first used in Lesson 2, Section 2 (Proposition 2.2).' L02 Section 1 (lines 64-72) defines A1 and A2 and uses neither in its own text (A2 uses only the rate of A4, which is a separate pointer, FC2a-r3-L02-sec1-forward-ref). The first uses are Proposition 2.2's 'Assume A1 to A4' (L02 line 93) and Case 2's 'A2 allows both' (line 100), both in Section 2.")

# new rows (round 3)
NEW = [
 dict(id="FC2a-r3-ex34-hypothesis", check="2.4 mathematics: assumptions complete for a T-graded result (rule 6); 2.3 grade",
      location="L03.html lines 133-135 (Example 3.4); key-results row line 425; cards.json FC2-c043 (line 277)", status="FAIL",
      evidence=f"Example 3.4 states: 'Suppose DF_i = (1+rho)^(-i) for a constant annual rate rho != 0.' It names no A8 and no restriction rho > -1. Its conclusion R_par = rho is derived by 'rho sum DF_i = 1 - DF_n' and then R_par = rho, which uses Proposition 3.3, and Proposition 3.3 'Assume A8' with DF_i > 0 (positivity makes the sum non-zero, so the par rate is unique). Own check ({SCR}numbers_r3.out, inline Fraction run): rho = -2, n = 2 gives DF = (-1, 1), sum 0, formula (1-DF_2)/sum = 0/0; the equation R * 0 = 0 holds for every R, so R_par = rho is not established. rho = -3/2 gives DF = (-2, 4), sum 2, formula -3/2 = rho (valid numerically but DF_i < 0 violates A8). The key-results row (line 425) and card FC2-c043 grade this T.",
      fix="In Example 3.4 change the first sentence to: 'Assume A8, and suppose DF_i = (1+rho)^(-i) for a constant annual rate rho > -1, rho != 0 (so that every DF_i > 0).' The rho = 0 sentence can stay. Keep the key-results row and card FC2-c043 as T with 'Assume A8' in the statement."),
 dict(id="FC2a-r3-prop32-title", check="2.4 mathematics: statement and title agree; 2.9 prose",
      location="L03.html line 109 (Proposition 3.2 title span)", status="FAIL",
      evidence="Title reads '(the floating leg is worth par)', but the statement (line 110) says the present value of the floating leg is 1 - DF_n. That equals par (1 per unit notional) only when DF_n = 0; with DF_2 = 0.924642 (the page's own R3 curve) the value is 0.075358. The key-results row (line 423) and card FC2-c041 correctly say 1 - DF_n.",
      fix="Retitle the block at L03.html line 109 to '(value of the floating leg)'."),
 dict(id="FC2a-r3-card-c037-remark14", check="2.7 cards agree with the CURRENT lesson text (rule 10)",
      location="course/modules/FC/FC2/cards.json line 244-247 (FC2-c037); L03.html lines 80-83 (Remark 1.4) and line 286 (canon-breaks)", status="FAIL",
      evidence="FC2-c037 back: 'No. Margin requirements are not modelled, and the identity holds whatever the requirements are (Remark 1.4).' The phrase 'holds whatever the requirements are' appears nowhere in the current L03 text (grep). Remark 1.4 (lines 81-83) says the identity 'says nothing about whether the account is large enough to meet them'. The current canon-breaks bullet (line 286) says 'The identity holds under A8-prime, which admits no cash flow other than the daily variation margins, so it does not cover any payment that a requirement adds.' The card's 'whatever the requirements are' therefore contradicts the lesson's current claim.",
      fix="Rewrite FC2-c037 back to: 'No. Margin requirements are not modelled (Remark 1.4). The identity says nothing about whether the account can meet them, and under A8-prime it does not cover any payment a requirement adds (Lesson 3, Section 4).' (A8-prime is the margin-account assumption of Lesson 3.)"),
 dict(id="FC2a-r3-L02-sec1-forward-ref", check="2.9 terms used before definition (defect class 5)",
      location="L02.html line 71 (Assumption A2 block) and lines 79-82 (Assumption A4)", status="FAIL",
      evidence="Assumption A2 (line 71) says 'lend or borrow any amount at the rate \\(r\\) of Assumption A4 in this lesson'. The symbol r is used, and its meaning and the rule that it is constant and continuously compounded are given only in Assumption A4 (lines 79-82), two blocks later. r has no earlier definition in the lesson, so the term is used before it is defined.",
      fix="Move the Assumption A4 block (lines 79-82) above Assumption A2 (lines 69-72), and change A2 to 'at the rate r of Assumption A4' without the phrase 'in this lesson'. Or define r in A2 itself."),
 dict(id="FC2a-r3-L03-def31-forward-ref", check="2.9 terms used before definition (defect class 5)",
      location="L03.html line 100 (Definition 3.1) and line 105 (Assumption A8)", status="FAIL",
      evidence="Definition 3.1 says the floating leg pays 'the floating coupon L_i for period i, which is set at date i - 1' and uses L_i. The coupon is defined only in Assumption A8 (line 105): '1 + L_i = DF_{i-1}/DF_i', after Definition 3.1. The term is used before its definition in the lesson.",
      fix="Either move Assumption A8 (lines 104-105) above Definition 3.1, or add 'given by the relation in Assumption A8 below' to Definition 3.1 at line 100 and state the relation there."),
]

rows = []
for rid, r in prev_rows.items():
    u = upd[rid]
    row = dict(id=rid, check=r["check"], location=u["location"] or r["location"], status=u["status"], evidence=u["evidence"])
    if u["status"] != "PASS":
        row["fix"] = u["fix"]
    rows.append(row)
for n in NEW:
    row = dict(id=n["id"], check=n["check"], location=n["location"], status=n["status"], evidence=n["evidence"])
    if n["status"] != "PASS":
        row["fix"] = n["fix"]
    rows.append(row)

assert set(upd) == set(prev_rows), set(upd) ^ set(prev_rows)
for r in rows:
    if r["status"] != "PASS":
        assert r.get("fix"), r["id"]

fails = [r["id"] for r in rows if r["status"] != "PASS"]
summary = dict(rows=len(rows), pass_=len(rows) - len(fails), fail=len(fails), unverifiable=0, fail_ids=fails)
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
frag = dict(
    unit="FC2", slice="a", round=3,
    verifier="Haiku independent verifier, FC2-a round 3 (did not build FC2; final full verification, binding rulings file)",
    pin="8196077d5f56c3919d33e69888176d197d378ad4",
    base="9294b914 (round-2 pin; round-2 fragment /Users/billyribeiro/.fanout/frags/S-FC2-a.round2.json). Delta 9294b914..8196077d for slice a: index.html (lede, placement items 7 and 9, ladder), L01 (why-it-matters, A3 block), L02 (why-it-matters, A2 text), L03 (why-it-matters, canon-breaks, Remark/P3, Prop 3.3 text, key-results P3 row), cards.json (L01-L03 and L04 cards). Lab twins L01-L03 unchanged since aeb512b; tools/, references/, notation/ unchanged in the delta.",
    checkout="/Users/billyribeiro/.fanout/wt/verifyS3-FC2-a (detached at 8196077d, .venv symlinked)",
    scratch="/tmp/fc2a-r3 (run outputs, make_fragment.py); scripts kept under ledgers/FC2/scripts/FC2-a-r3/",
    verified_at=now,
    verdict="FAIL",
    rows=rows,
    mutants=[],
    registry_flags=[
        "references/references.json: FC2 is in black1973pricing used_by (added after round 1); no slice-a page cites it. verify_refs --unit FC2 reports 4 entries, 0 problems.",
    ],
    freshness_flags=[],
    notes=[
        "Scope: slice a = index.html, L01-L03 pages, their lab twins tests/labs/FC2/lab-FC2-L01-1.py..L03-1.py, and the L01-L03 cards in cards.json. Project, L04-L08 and grader are other slices.",
        "Every round-2 row id is kept. Every row was re-verified at 8196077d this round (commands re-run, scripts saved under ledgers/FC2/scripts/FC2-a-r3/); no row is carried on a 'byte-identical' argument. Round-2 FAIL rows: FC2a-cards-accuracy (c050, c022) now PASS; FC2a-cards-hypotheses (c168, c169, c172) now PASS; FC2a-L01-assumption-first-use now PASS; FC2a-cards-trivia still FAIL (its c013, c023, c138 are fixed; c046 is the remaining lab-only card).",
        "Mutants: none. This slice has no project grader (VERIFIER 2.6 applies to grader/* in other slices), so the three-new-mutant requirement does not apply here.",
        "Ruling 13 applied: T cards with derivations on the page (c008, c010, c014, c021, c023, c024, c027, c036, c138) are accepted; c024 and c027 derive their numbers by hand in E2 and E3 solutions. c046 is the only lab-only numeric T card.",
        "Observations, not rows: c170 duplicates the i=n case of c036; c007 is graded T but states a non-claim; c032 is a definitional consequence graded T; c021 names only A1 (Example 2.4 states no hypotheses); L01 Remark 3.3 refers forward to Example 3.4 by its label (cross-reference, not a term); L03 why-it-matters uses A8-prime with an inline gloss before its block (not flagged).",
        "Pre-existing tracked files in ledgers/FC2/scripts/FC2-a-r3/ (check_L01_numbers.py, check_L02_L03_numbers.py, check_links.py, twin_vs_page.py, committed in b276325f) were not modified or run by this round; this round's scripts use the names page_twin.py, numbers_r3.py, cards_r3.py and structure_links_r3.py.",
        "Hub prose check (lede 'the one price consistent with no riskless profit') is accepted as hypothesis-scoped (Prop 2.2).",
        "Interpreter note: /usr/bin/python3 (3.9.6) cannot run the twins (zip strict); the project interpreter .venv (3.14.8) runs them cleanly. Not a defect.",
    ],
    summary=summary,
)
LOC = {
  "FC2a-cards-trivia": "course/modules/FC/FC2/cards.json line 291 (FC2-c046); lab output in tests/labs/FC2/lab-FC2-L03-1.py",
  "FC2a-L02-problems": "L02.html line 332 (Problem P1 statement), line 414 (key-results row), cards.json line 187 (FC2-c028); other problems in #problems",
  "FC2a-L03-math": "L03.html lines 109 (Prop 3.2 title), 133-135 (Example 3.4), 110-150 (Props 1.3, 3.2, 3.3, 3.5)",
  "FC2a-grades": "L02.html line 414, L03.html line 425 (key-results T rows); cards.json FC2-c046; L01-L03 claim titles",
  "FC2a-cards-hypotheses": "cards.json FC2-c168, FC2-c169, FC2-c172, FC2-c028, FC2-c140, FC2-c141",
  "FC2a-cards-accuracy": "cards.json FC2-c050, FC2-c022 and all L01-L03 cards",
}
for r in rows:
    if r["id"] in LOC:
        r["location"] = LOC[r["id"]]
out = "/Users/billyribeiro/.fanout/wt/verifyS3-FC2-a/ledgers/FC2/FC2-a.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, summary)
