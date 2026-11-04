import json
S = "ledgers/E3/scripts/E3-g-r5/"
R = []
def row(i, check, loc, status, ev, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)

row("E3g-dup-scan", "2.7-duplicates (all 83 L05-L08 cards; near-duplicates against all 169 E3 cards)",
    "course/modules/E/E3/cards.json (E3-c176 absent on this pin; round-4 duplicate removed)", "PASS",
    S + "dup_scan_g5.out: 0 exact front duplicates, 0 exact back duplicates; 20 near pairs (difflib ratio >= 0.45) all distinct facts, e.g. E3-c169 (U = -49/80) vs E3-c170 (CE1 = 8/5); E3-c109 (narrow framing) vs E3-c163 (integrated evaluation); E3-c137 (V_tau definition) vs E3-c172 (its tau = 1 specialization, a different claim); E3-c149 (EU CE) vs E3-c151 (maxmin CE). E3-c176 (round 4 duplicate of E3-c146/c149/c153) is deleted.")
row("E3g-notation-c138", "2.4-notation (E3-c138 uses tau, not alpha)", "cards.json E3-c138; text/L08.txt Definition 1.2", "PASS",
    "text/L08.txt Definition 1.2: 'The weight is written tau, not alpha'; E3-c138 front 'for every tau' and Proposition 1.3 (A2: tau in [0,1]).")
row("E3g-grade-c142", "2.3-grades (E3-c142 strict case of Theorem 2.2)", "cards.json E3-c142; text/L08.txt Theorem 2.2 proof (strict case)", "PASS",
    "Theorem 2.2 strict case: non-equal E_{P_i} u(f) give a strict inequality (text/L08.txt proof). Grade T correct.")
row("E3g-grade-c090", "2.3-grades (E3-c090 is T, lab pair is E3-c095 grade C)", "cards.json E3-c090; text/L05.txt Corollary 3.3, Remark 3.4", "PASS",
    "E3-c090 back cites Corollary 3.3 (A1 to A4) and Remark 3.4 only; the lab pair is on E3-c095 (grade C).")
row("E3g-r2-V-symbol", "2.4-notation (W in L06 cards means the prospect value)", "cards.json E3-c100, c104, c105, c107, c113; text/L06.txt Definition 1.3", "PASS",
    "text/L06.txt Definition 1.3: W := sum p_i v(x_i); all L06 cards use W with that meaning. No L07 or L08 card uses W (E3-c148 and E3-c155 now use w; see E3g4-c148-notation, E3g4-c155-notation).")
row("E3g-r2-c145-V1", "2.9-structure (E3-c145 cites its lesson)", "cards.json E3-c145; text/L08.txt Definition 3.1", "PASS",
    "E3-c145 cites Definition 3.1 and a = 1 - 1/psi; no terminal V1 on L08.")
row("E3g-r2-L05-G1", "2.4-math / 2.6-cards (E3-c078 to c087)", "cards.json E3-c078..c087; text/L05.txt Definition 1.1, Remark 1.2, Theorem 1.3, Corollary 1.4, Definition 2.1, Proposition 2.2, Remark 3.1, Theorem 3.2",
    "PASS", "Each card re-derived against the lesson text. Numbers in " + S + "numbers_L05_L08_g5.out: CE1 = 8/5 and 12/5 (Remark 1.5), CE1 = 2 (Problem M1), V0 = 80/49, U = -49/80 (E3-c093, c169), V0 = 3/2 (M2), V0 = 160/71 (E2). Hypotheses on c082, c085 and c091 are now stated (rows E3g4-*).")
row("E3g-r2-L05-G2", "2.4-math / 2.3-grades (E3-c088 to c091)", "cards.json E3-c088 (line 587), c089, c090, c091 (line 608); text/L05.txt Corollary 3.3, Remark 3.4",
    "PASS", "Corollary 3.3 proof (h'(u) > 0) and Remark 3.4 (MRS exponents gamma and 1/psi; agreement iff 1/psi = gamma) re-derived; A1 to A4 and gamma != 0 stated on c088 to c091. The plan symbols P, Q on E3-c088 are a notation finding (row E3g5-notation-PQ), not a math finding.")
row("E3g-r2-L05-G3", "2.4-math / 2.6-cards (E3-c098 to c105)", "cards.json E3-c098..c105; text/L06.txt Proposition 1.4, Remark 1.5, Propositions 2.1 and 2.2; text/L05.txt Remark 1.5",
    "PASS", "Proposition 1.4 hypotheses (0 < alpha, delta < 1, lambda > 0) on E3-c101; alpha = delta on c102; alpha = delta = 1 on c104; general powers on c105. Numbers: lam* = 5/3 (c106); sqrt(5/3) = 1.2909944487 (numbers_L05_L08_g5.out).")
row("E3g-r2-L06-G4", "2.4-math / 2.3-grades (E3-c107, c108, c109 to c113, c163)", "cards.json E3-c107, c108 (line 714), c109..c113, c163; text/L06.txt Remarks 2.4, 2.5, 3.1, 3.2",
    "PASS", "E3-c108 now begins 'With alpha = delta = 1 (Remark 2.5)'; 700 - 300 lambda and 1000 - 600 lambda re-derived (numbers_L05_L08_g5.out: 100 and -200 at lambda = 2). E3-c113 lambda_R = sqrt(2)/2 = 0.70710678 (p = 1/3, g = 1000, l = 300, alpha = delta = 1/2). E3-c111 value (1/2) 800^alpha (1 - lambda) re-derived.")
row("E3g-r2-L07-G5", "2.4-math / 2.6-cards (E3-c118 to c126)", "cards.json E3-c118..c126; text/L07.txt Definition 1.1 to Remark 2.3, Example 1.4, Observation 1.5, Proposition 2.2",
    "PASS", S + "numbers_g5.out: omega(3/10) = 0.2857908849, omega(3/5) = 0.3912507700, omega(2/5) = 0.3194549160, omega(1/2) = 0.3535533906; 2 omega(3/10) = 0.57158177; omega(2/5) + 2 omega(3/10) = 0.89103669; ratio 0.73045450; thresholds 2/3 and 0.58578644; last grid point with omega > p is 0.278 with exactly one sign change, between 0.278 and 0.279 (dup-free recomputation on the 1001-point grid). Identity values 45 and 60 (c126).")
row("E3g-r2-L07-G6", "2.3-grades / 2.5-labs (E3-c127, c128, c131, c133, c135)", "cards.json E3-c127 (line 833), c128 (841), c131 (863), c133 (878), c135 (895); text/L07.txt Lab 1 parts A to D",
    "PASS", "twin run (ledgers/E3/scripts/E3-g-r5/twin_L07.out): Gamma(A) 42.8686, Gamma(B) 39.1251 (alpha = 1), 4.8788 and 3.9125 (alpha = 0.5), 10 of 10 utilities. Unrounded difference 3.74355573299 -> 3.7436 (numbers_g5.out); 8-decimal values subtract to 3.74355574 (same rounding). c133: affine weights with the endpoint values must be the identity (Problem R1).")
row("E3g-r2-L08-G7", "2.4-math / 2.3-grades (E3-c137 to c143)", "cards.json E3-c137..c143; text/L08.txt Definition 1.2, Proposition 1.3, Example 1.4, Definition 2.1, Theorem 2.2, Proposition 2.4",
    "PASS", "E3-c142 now carries A1 to A3 and A2 (strict increase), see E3g4-c142-hypotheses. E3-c141 and E3-c143 hypotheses are stated. Example 1.4: sum_{k=30}^{60} k / 90 / 31 = 1/2 re-derived.")
row("E3g-r2-L08-G8", "2.4-math / 2.3-grades (E3-c146, c148 to c153)", "cards.json E3-c146 (line 968), c148 (981), c149 (988), c150, c151 (line 1002), c152, c153 (1016); text/L08.txt Proposition 3.2, Remark 4.2, Model 1 to 4",
    "FAIL", "Numbers all re-derived (numbers_L05_L08_g5.out: 4180000/41 = 101951.2195; maxmin 99523.8095; p = 1/4 gives 98352.94; p = 3/4 gives 105822.78; premium 548.7805 cents = 5.4878 CU; prospect 5 - sqrt(50); wealth equivalent 99892.7670). Proposition 3.2 hypotheses A1 to A5 stated on c146. Two T cards omit the utility their numbers and claims need: E3-c148 and E3-c151 (rows E3g5-c148-utility, E3g5-c151-utility). E3-c176 is deleted (E3g-dup-scan).",
    "See E3g5-c148-utility and E3g5-c151-utility.")
row("E3g-r2-L08-G9", "2.3-grades / 2.2-numbers (E3-c144, c164, c165, c166)", "cards.json E3-c144 (line 955), c164 (1092), c165 (1099), c166 (1106); text/L08.txt Example 2.5, Model 2",
    "PASS", "numbers_L05_L08_g5.out: known urn red 103125.0 and black 106451.6129 (CRRA, u = -1/w); maxmin 100000 for both colours holds for any strictly increasing u (Example 2.5); -107.2330 cents and 99892.7670 cents (Model 2). twin_L08.out Part C reproduces 103125.0000, 106451.6129, 100000.0000.")
row("E3g-r2-numbers", "2.2-numbers (every number on the 83 L05-L08 cards)", S + "numbers_g5.py, numbers_L05_L08_g5.py -> numbers_g5.out, numbers_L05_L08_g5.out", "PASS",
    "Fraction and 40-digit Decimal recomputation of every card number (L05: 80/49, -49/80, 8/5, 12/5, 2, 3/2, 160/71; L06: 5/3, -100, sqrt(5/3), -8.6835, sqrt(2)/2, 700-300 lambda, 1000-600 lambda; L07: all omega values, 3.7436, 49.8328, 0.73045450; L08: all CEs and premiums). The one wrong sign in my own helper printout is in my script, not in the lesson (100000 - 107.2330 = 99892.7670 is right).")
row("E3g-r2-lab-twins", "2.5-labs (L05-L08 twins and pages)", "tests/labs/E3/lab-E3-L05-1.py .. lab-E3-L08-1.py; course/modules/E/E3/L05.html .. L08.html", "PASS",
    "run_labs_L05-L08_r5.out: 'run_labs E3: PASS (1/1)' for L05, L06, L07 and L08; the tool compares page code with twin and expected block with output, and it passed. Twins run alone under python -I -W error: exit 0 (twin_L05..L08.out). ruff_r5.out: ruff check and format pass on the four twins. mypy_r5.out: mypy --no-incremental passes on the four twins. pytest_labs_r5.out: tests/test_labs.py and tests/test_run_labs.py -k E3 pass.")
row("E3g-r2-refs-cross", "2.9-DAG / cross-lesson references used by the cards", "cards.json E3-c081, c112, c129, c146, c154; text/L04 Theorem 1.5 (course/modules/E/E3/L04.html lines 89-90)", "PASS",
    "L04 Theorem 1.5 (lines 89-90): F_X <= F_Y everywhere iff E u(X) >= E u(Y) for every nondecreasing u, with A1 (finite support). E3-c129 applies it with X = A, Y = B in the card's direction: B dominates A, so E u(B) >= E u(A). Section references (L05 section 5 third misconception, L06 section 5 first misconception, L08 section 6 first and third) match the texts.")
row("E3g-r2-registry", "2.1-citations (registry keys cited by L05-L08 cards)", "cards.json E3-c134 (kahneman1979prospect), E3-c157 (ellsberg1961risk), E3-c158 (gilboa1989maxmin); references/references.json", "PASS",
    S + "verify_refs_offline_r5.out: '560 entries, 0 problems'. references.json titles: ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' (1961); gilboa1989maxmin 'Maxmin expected utility with non-unique prior' (1989); kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk' (1979). Cards and lesson use the titles only. Live verify_refs not run (no network needed; no reference changed).")
row("E3g-r2-coverage", "2.7-cards cover the graded key results", "L05 text Key results table; L06 Key results; L07 Key results; L08 Key results", "PASS",
    "Each graded key result has a card: L05 Theorem 1.3 (c080), Corollary 1.4 (c081), Proposition 2.2 (c084), Remark 3.1 (c086), Theorem 3.2 (c087), Corollary 3.3 (c088), Remark 3.4 (c089), lab rows (c093 to c096); L06 Proposition 1.4 (c101), Remark 1.5 (c102), Propositions 2.1, 2.2 (c104, c105), Example 2.3 (c106), Remark 2.4 (c107), Remark 2.5 (c108), lab rows (c116, c117); L07 Remark 1.3 (c120), Example 1.4 (c121), Remark 1.6 (c123), Proposition 2.2 (c125), Lab rows (c127, c128); L08 Proposition 1.3 (c138), Theorem 2.2 (c141), Proposition 2.4 (c143), Example 2.5 (c144, c164, c165), Proposition 3.2 (c146), Remark 4.2 (c148), Model 2 (c150, c166), Model 4 (c151), Lab B (c153).")
row("E3g-r2-grades", "2.3-grades (grade field of the 83 slice cards)", "cards.json L05 20, L06 19, L07 18, L08 26", "PASS",
    S + "numbers_L05_L08_g5.out (grade counts): 49 T, 17 C, 17 ungraded. The 17 C cards each carry a basis (lab part or Problem) or, for E3-c134, c157, c158, a registry cite with title-only scope. Each T card is a theorem, remark, example or closed-form computation on the page (rows above).")
row("E3g-r2-hypotheses", "2.4-math / 2.6-cards (carry the proposition's hypotheses on every T card)", "cards.json T cards; E3-c148 (line 981) and E3-c151 (line 1002) are the two open cases", "FAIL",
    "All other T cards carry their hypotheses: A1 to A4 on c080, c081, c082, c084, c085, c086, c087, c088, c089, c090, c091; A1 to A3 on c125, c141, c143; alpha, delta on c101, c102, c104, c105, c108, c111, c113, c150, c166; A1 to A5 on c146; alpha = 1 on c126, c132. Open: c148 and c151 need u(w) = -1/w (rows E3g5-c148-utility, E3g5-c151-utility).",
    "See E3g5-c148-utility and E3g5-c151-utility.")
row("E3g-r2-scope-words", "2.9-scope words (only, every, any, all, always, exactly, same, once)", "cards.json L05-L08; text/L05.txt Remark 2.3, Remark 3.4", "PASS",
    "c085 'every such gamma' (Remark 2.3, every gamma != 1); c089 'exactly when' (Remark 3.4); c107 'for every alpha, delta, lambda > 0' (Remark 2.4); c122 'changes sign once' (twin_L07.out: sign changes = 1); c153 'all six gaps' (twin_L08.out part B: six gaps).")
row("E3g-r2-process-words", "2.9-prose / banned process words in learner text", "cards.json L05-L08; text/L05..L08", "PASS",
    "grep over the card file for we, our, let's, TODO, verifier, builder: no hits. The L05 lesson's 'We write' (section 1) is mathematical exposition, not process language.")
row("E3g-r2-gates", "2.9 / gates on this pin (run by this verifier)", S, "PASS",
    "check_pages_L05-L08_r5.out: E3 L05..L08 PASS. check_dag_r5.out: 'check_dag E3: PASS'. check_projects_r5.out: 'check_projects E3: PASS'. page_smoke_r5.out: 'page_smoke E3: PASS' (--pages L05 L06 L07 L08 --skip-sweep; the figure control sweep was not run). ruff_r5.out and mypy_r5.out as above.")
row("E3g-r2-delta", "delta read (round-4 pin 4eb6788 to 440ed3c) for the slice", "git diff 4eb6788f 440ed3c8 -- course/modules/E/E3/cards.json, L05.html, L07.html, L08.html; tests/labs/E3/", "PASS",
    "Every slice hunk read: cards c082, c085, c091, c108, c130, c142, c148, c155 (fixed), E3-c176 deleted, E3-c177 added (lesson L03: out of this slice, not verified here); L05 'why-it-matters' and section 4 bullet; L07 Remark 1.6, E2 and E3 solutions; L08 section 5 bullets 2 and 4, misconception 3, R2 solution, quiz item 8. No change to the L05-L08 twins in this range.")
row("E3g3-c135-terminology", "2.9-prose (E3-c135 back vs L07 Section 3)", "cards.json E3-c135; text/L07.txt Section 3", "PASS",
    "Back: 'The cumulative repair of Section 3 is not derived', matching L07 Section 3 'This lesson does not derive that repair'.")
row("E3g3-notation-collisions", "2.4-notation (one meaning per letter in E3)", "cards.json E3-c088, c148, c155; L05 Corollary 3.3", "FAIL",
    "W collision resolved: E3-c148 uses E_P[1/w] and E3-c155 uses u(w) = -exp(-nu w) (lowercase w, final wealth as in L08 text Remark 4.2 and Problem R3). V_1 / V_tau resolved. Still open: the plans P and Q of L05 Corollary 3.3 and E3-c088 collide with the registered symbols \\mathbb{Q} and \\mathbb{P} (\\Prob) in notation/notation.json.",
    "See E3g5-notation-PQ.")
row("E3g3-c091-gamma", "2.4-math (E3-c091 gamma != 0)", "cards.json E3-c091 (line 611); text/L05.txt Remark 3.4, Theorem 3.2", "PASS",
    "Remark 3.4: '1/gamma for gamma != 0'; Theorem 3.2: 'The restriction needs gamma != 0'. The card matches.")
row("E3g3-c132-omega", "2.2-numbers (E3-c132 weighted value under omega_{1/2})", "cards.json E3-c132 (line 871); text/L07.txt misconception 3", "PASS",
    "numbers_g5.out: omega(0.01) = 0.0834030105, omega(0.99) = 0.8298494764; 100 omega(0.01) + 50 omega(0.99) = 49.8328 against EV 50.5; overweight +7.3403, underweight -8.0075, net -0.67 (lesson text agrees).")
row("E3g3-c097-trivia", "2.7-cards (E3-c097 removed)", "cards.json id list", "PASS",
    "No E3-c097 on this pin (id gap; no defect by itself).")
row("E3g3-basis-wording", "2.3-grades (basis strings of the C cards)", "cards.json E3-c094, c095, c106, c117, c122, c153", "PASS",
    "Each basis names the lab part and the case it covers, and matches the twin output in twin_L05..L08.out.")
row("E3g3-L05-proofs", "2.4-math (L05 proofs)", "text/L05.txt Theorem 1.3, Corollary 1.4, Proposition 2.2, Remark 3.1, Theorem 3.2, Corollary 3.3, Remark 3.4", "PASS",
    "All re-derived in this round: Theorem 1.3(b) (monotone in CE1 for a > 0 and a < 0), Corollary 1.4, Proposition 2.2 (MRS = (1-beta)/beta (c1/c0)^(1/psi)), Theorem 3.2, Corollary 3.3, Remark 3.4 (the 'only if' step r^gamma = r^(1/psi) gives gamma = 1/psi when r != 1). Lesson text claims about the lab (predicted block and misconceptions) agree with twin_L05 output.")
row("E3g3-L06-proofs", "2.4-math (L06 proofs)", "text/L06.txt Proposition 1.4, Propositions 2.1, 2.2, Remarks 1.5, 2.4, 2.5, 3.1, 3.2", "PASS",
    "Re-derived: Proposition 1.4 derivatives and concavity, Remark 1.5, Proposition 2.1 and 2.2 thresholds, Remark 3.2 lambda_R = 1 for alpha = delta at the expected-value reference, Remark 2.5 combined and separate values. twin_L06.out matches the printed claims.")
row("E3g3-L07-proofs", "2.4-math (L07 proofs)", "text/L07.txt Definition 1.2, Example 1.4, Remark 1.3, Remark 1.6, Proposition 2.2, Problems R1, R2, M1, E1, E2, E3", "PASS",
    "Re-derived: Example 1.4 closed form and omega(1/4) = 2 - sqrt(3) = 0.26794919; Remark 1.6; Proposition 2.2 algebra; Problem R2 tails (3/5 = 3/5 at 50; 3/10 vs 3/5 at 100). E3 solution: eta = 1 gap 0.31256245 at p = 0.862 (numbers_g5.out), prose '3.13e-1' and 'p = 0.862' agree; E2 solution 40-digit difference 3.74355573 agrees.")
row("E3g3-L08-proofs", "2.4-math (L08 proofs)", "text/L08.txt Proposition 1.3, Theorem 2.2, Proposition 2.4, Example 2.5, Proposition 3.2, Remark 4.2, Models 1 to 4, Problems M1 to M3, E1 to E3, R2", "PASS",
    "Re-derived in numbers_L05_L08_g5.out and by hand: Proposition 3.2 proof (injectivity of x -> x^(1/a) for a != 0); Proposition 2.4 (P_0 and P_90); Example 2.5 CEs; Remark 4.2 affinity; Model 2 inverse -(-V/2)^2; the revised R2 solution (black worst at black probability 1/3, value 103125 cents); Problem M1 98352.94; M2 105822.78; E3 premium 548.7805 cents = 5.4878 CU.")
row("E3g3-c148-scope", "2.9-scope (E3-c148 sentence vs Remark 4.2 and L08 Section 5)", "cards.json E3-c148 (line 981); text/L08.txt Remark 4.2, Section 5 bullet 4", "PASS",
    "Scope sentence ('not a general property of alpha-MEU') matches Remark 4.2 and Section 5 bullet 4. The utility hypothesis missing on this card is row E3g5-c148-utility.")
row("E3g3-attribution", "2.1 / 2.9 (title-only attributions on E3-c134, c157, c158)", "cards.json E3-c134, c157, c158; references/references.json", "PASS",
    "Titles read from references/references.json (see E3g-r2-registry); cards state title-only attribution and 'not reproduced' scope, matching L07 text line on Kahneman and Tversky, L08 text Section 2 and Definition 1.2.")
row("E3g3-notation-registry", "2.4-notation (notation/notation.json registered symbols)", "notation/notation.json (T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, \\mathbb{Q}; \\Prob macro); course/modules/E/E3/L05.html line 147, cards E3-c088", "FAIL",
    "The slice's cards and lessons use plain P and Q for two plans in L05 Corollary 3.3 and E3-c088; \\mathbb{Q} is registered as a probability measure ('by default an equivalent martingale (risk-neutral) measure') and \\Prob (\\mathbb{P}) as the probability measure. The rule that a registered symbol never takes another meaning is therefore broken by the letters P and Q. Other registered symbols (T, Phi, gamma_3, gamma_4, R*, R^e*, R_f) do not occur in the slice.",
    "See E3g5-notation-PQ.")
row("E3g3-page-smoke", "2.9 page smoke", S + "page_smoke_r5.out", "PASS",
    "'page_smoke E3: PASS' for L05, L06, L07 and L08 (zero console errors, math rendered; the figure control sweep was skipped by --skip-sweep).")
row("E3g3-gates-projects-ruff", "2.9 gates (check_projects, ruff)", S + "check_projects_r5.out; " + S + "ruff_r5.out", "PASS",
    "check_projects E3: PASS; ruff check and ruff format pass on the four L05-L08 twins.")
row("E3g3-delta-r3", "delta read (round-3 row kept; re-read on this pin)", "git diff a007712f..440ed3c8 for the slice files", "PASS",
    "Round-3 slice changes re-read on this pin: E3-c097 deleted, c091 gamma != 0, c176 re-targeted then deleted, notation and basis rewording, Remark 3.4 and Definition 1.2 hunks.")
row("E3g4-c082-hypotheses", "2.4-math / 2.6-cards (E3-c082 hypotheses)", "cards.json E3-c082 (line 549); text/L05.txt Remark 1.5", "PASS",
    "Back now reads 'No. Under A1 to A4 at gamma = 2, the value depends on the lottery through CE1 ...'. The example (CE1 = 8/5 and 12/5 at gamma = 2) is re-derived (numbers_L05_L08_g5.out).")
row("E3g4-c085-hypotheses", "2.4-math / 2.6-cards (E3-c085 hypotheses)", "cards.json E3-c085 (line 569); text/L05.txt Remark 2.3, Proposition 2.2", "PASS",
    "Back now reads 'Under A1 to A4 for deterministic plans, and for gamma not equal to 1 (the values A3 allows), CE1 = c1 ...'. Remark 2.3 states gamma != 1; Proposition 2.2 needs A1 to A4 for deterministic plans.")
row("E3g4-c091-hypotheses", "2.4-math / 2.6-cards (E3-c091 hypotheses)", "cards.json E3-c091 (line 611); text/L05.txt Remark 3.4", "PASS",
    "Back now reads 'Under A1 to A4, 1/gamma for gamma not 0 (Remark 3.4); at gamma = 0 it is undefined. Epstein-Zin gives psi instead (Proposition 2.2).'")
row("E3g4-c108-hypotheses", "2.4-math / 2.6-cards (E3-c108 hypotheses)", "cards.json E3-c108 (line 717); text/L06.txt Remark 2.5", "PASS",
    "Back now begins 'With alpha = delta = 1 (Remark 2.5)'; the combined and separate values are re-derived (100 and -200 at lambda = 2).")
row("E3g4-c130-argument", "2.4-math / 2.3-grades (E3-c130 'It can')", "cards.json E3-c130 (line 856); text/L07.txt Proposition 2.2, Remark 1.6, Lab 1 part C", "PASS",
    "Back now cites Proposition 2.2 and the values 42.8686 (A) and 39.1251 (B) at alpha = 1 (twin_L07.out), with the weight comparison 0.57158177 > 0.39125077 as the reason. Grade T is supported by Proposition 2.2 and the closed form.")
row("E3g4-c142-hypotheses", "2.4-math / 2.6-cards (E3-c142 hypotheses)", "cards.json E3-c142 (line 944); text/L08.txt Theorem 2.2", "PASS",
    "Back now begins 'Under A1 to A3 of Theorem 2.2, with u strictly increasing (A2),'.")
row("E3g4-c148-notation", "2.4-notation (E3-c148 symbol)", "cards.json E3-c148 (line 984); text/L08.txt Remark 4.2", "PASS",
    "Back now reads 'E_P[1/w]', as in Remark 4.2 (final wealth w). The utility hypothesis is a separate row (E3g5-c148-utility).")
row("E3g4-c155-notation", "2.4-notation (E3-c155 symbol)", "cards.json E3-c155 (line 1034); text/L08.txt Problem R3", "PASS",
    "Back now reads 'u(w) = -exp(-nu w)', matching Problem R3 (line 'u(w) = -e^{-nu w}').")
row("E3g4-c096-context", "2.9-prose (E3-c096 names its tree)", "cards.json E3-c096 (line 639); text/L05.txt Lab 1 predicted block", "PASS",
    "The card's numbers 2.2500, 1.6000, 1.3720 are re-derived (numbers_L05_L08_g5.out) for the lab's risky tree (c1 = 1 or 4, probability 1/2 each), which the Lab 1 predicted block names. Observation for the card author, not a failure: name the tree on the card front.")
row("E3g4-c131-unrounded", "2.2-numbers (E3-c131 unrounded difference)", "cards.json E3-c131 (line 863); text/L07.txt E2 solution", "PASS",
    "Unrounded difference 3.74355573299 -> 3.7436 (numbers_g5.out); the 8-decimal display subtracts to 3.74355574, which also rounds to 3.7436.")
row("E3g4-c172-definition", "2.4-math / 2.3 (E3-c172 definition)", "cards.json E3-c172 (line 1150); text/L08.txt Definition 1.2", "PASS",
    "Definition 1.2: 'The maxmin expected utility value is V_tau(f) at tau = 1, which equals min over P of E_P u(f)'. The card matches.")
row("E3g4-lab-observations", "2.7 (lab-versus-theorem pairs)", "cards.json E3-c101/c117, E3-c128/c129, E3-c146/c153", "PASS",
    "Each pair states the same property at different grades (theorem versus finite lab check) and is not a duplicate by content; reported for the L06, L07, L08 verifiers.")
row("E3g5-c148-utility", "2.4-math / 2.6-cards (E3-c148 hypothesis u(w) = -1/w)", "cards.json E3-c148 (line 984); text/L08.txt Remark 4.2 and Problem P3 (Section 6)", "FAIL",
    "The back's claim 'E_P[1/w] is affine in p' and the common value 101951.2195 cents hold only for the utility u(w) = -1/w (the value equals 1/E[1/w]; numbers_L05_L08_g5.out: 4180000/41). Problem P3 states 'for u(w) = -1/w'; Remark 4.2 does not, and the card carries neither hypothesis.",
    "Prefix the back with 'With u(w) = -1/w (CRRA, gamma = 2, Model 1), ' and add the same hypothesis to Remark 4.2 in L08.html.")
row("E3g5-c151-utility", "2.2-numbers / 2.6-cards (E3-c151 hypothesis u(w) = -1/w)", "cards.json E3-c151 (line 1002); text/L08.txt Section 4 Model 4", "FAIL",
    "The value 99523.8095 cents = 1/max_P E_P[1/w] (numbers_L05_L08_g5.out) holds only for u(w) = -1/w. Model 4 in L08.html writes '1/(1/3 / w_1 + 2/3 / w_L)' without naming u; the card gives no u.",
    "Card: prefix the back with 'With u(w) = -1/w (CRRA, gamma = 2, Model 1), '. Lesson: state u(w) = -1/w in Model 4 (L08.html).")
row("E3g5-c152-utility", "2.2-numbers (E3-c152 expected-utility premium)", "cards.json E3-c152 (line 1009); text/L08.txt Section 4 Model 1 and Problem E3", "PASS",
    "The premium refers to 'the expected-utility certainty equivalent' of the gamble of Section 4, which is Model 1 with u(w) = -1/w stated there. 102500 - 101951.2195 = 548.7805 cents = 5.4878 CU (numbers_L05_L08_g5.out).")
row("E3g5-notation-PQ", "2.4-notation (plain P and Q for plans in L05; registered \\mathbb{Q} and \\Prob)", "text/L05.txt Corollary 3.3 (course/modules/E/E3/L05.html line 147); cards.json E3-c088", "FAIL",
    "L05 Corollary 3.3 reads 'for any two plans \\(P\\) and \\(Q\\)' and E3-c088 reads 'V0(P) >= V0(Q)'. notation/notation.json registers \\mathbb{Q} as a probability measure (risk-neutral) and \\Prob = \\mathbb{P} as the probability measure. The letters P and Q therefore take a second meaning, which the registry forbids.",
    "Rename the two plans in L05 Corollary 3.3 and in E3-c088 to letters not in notation/notation.json (for example X and Y), keeping the rest of the statement unchanged.")
row("E3g5-c169-c170-basis", "2.2-numbers / 2.6-cards (E3-c169, c170 'the same exact tree of Lab 1')", "cards.json E3-c169 (line 1126), E3-c170; course/modules/E/E3/L05.html Lab 1 predicted block", "PASS",
    "The referent is Lab 1's predicted block: gamma = 2, psi = 1/2, beta = 9/10, c0 = 2 and c1 = 1 or 4 with probability 1/2 each. U = -49/80 and CE1 = 8/5 are re-derived with those parameters (numbers_L05_L08_g5.out).")

fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 5,
    "verifier": "Haiku independent verifier, E3-g round 5 (did not build E3)",
    "pin": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b (round-4 pin; delta 4eb6788..440ed3c read for this slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-E3-g (detached at 440ed3c)",
    "scratch": "ledgers/E3/scripts/E3-g-r5/ (scripts, outputs, text/ holds the L05-L08 lesson text read in full)",
    "verified_at": "2026-11-03T22:39:45Z",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice g is the 83 cards of L05-L08 (L05 20, L06 19, L07 18, L08 26; 49 T, 17 C, 17 ungraded definitions) against the four lesson texts. Every lesson text was read in full (text/L05.txt, L06, L07, L08), and every card was read against it.",
        "Not a project slice: no student-error mutants were written and no alternative implementations were run; mutants is empty by design.",
        "Round-4 FAIL rows re-checked on this pin: E3g-dup-scan now PASS (E3-c176 deleted); E3g-r2-L05-G2, E3g-r2-L06-G4, E3g-r2-L08-G7, E3g4-c082, c085, c091, c108, c130, c142, c148 (notation), c155 now PASS. Still open: utility hypotheses on E3-c148 and E3-c151, and the plan letters P and Q.",
        "Lesson-side (not a card row): L08 Model 4 (section 4) states no utility; the same fix as E3g5-c151-utility belongs in L08.html.",
        "Out of slice: E3-c177 (lesson L03, added this round in place of E3-c176) is not verified here; E3-c031 and E3-c159 changed in the delta and belong to other slices.",
        "Lab output, labs and pages were not changed in the delta; the L05-L08 twins were re-run in this round.",
    ],
    "summary": "Slice g (E3 cards L05-L08, 83 cards) at 440ed3c: 3 open defects. E3-c148 and E3-c151 state utility-dependent results without u(w) = -1/w (E3g5-c148-utility, E3g5-c151-utility); the plans P and Q of L05 Corollary 3.3 and E3-c088 take letters registered as a probability measure (E3g5-notation-PQ). Round-4 hypothesis, duplicate and notation defects are fixed. All numbers, labs, gates and registry keys re-derived or re-run on this pin pass.",
}
json.dump(fragment, open("ledgers/E3/E3-g.json", "w"), ensure_ascii=False, indent=2)
from collections import Counter
print(Counter(r["status"] for r in R), len(R))
