"""Build the round-3 fragment ledgers/E3/E3-g.json from the round-2 ids and the round-3 rows (evidence in this folder)."""
import json

S = "ledgers/E3/scripts/E3-g-r3"
R2 = "ledgers/E3/scripts/E3-g-r3"  # round-3 re-verification scripts; the round-2 scripts are not relied on

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- rows carried by id from round 2 (keys kept), each re-verified in round 3
row("E3g-dup-scan", "2.7-duplicates (full scan)", "course/modules/E/E3/cards.json (170 cards; 85 in L05-L08)", "PASS",
    f"{S}/cross_slice_near_dup.py -> {S}/cross_slice_near_dup.out: 170 cards, 170 distinct ids, 0 exact duplicate fronts, 0 exact duplicate backs. Within the slice, word-set Jaccard >= 0.5 only for E3-c137/E3-c172 (0.52: general alpha-MEU value vs the tau=1 value V_1) and E3-c164/E3-c165 (0.51: a CE value vs a preference); against other lessons >= 0.4 only E3-c124/E3-c070 (different examples) and E3-c172/E3-c002 (different objects). None is a duplicate.")
row("E3g-notation-c138", "2.4-notation / 2.3", "course/modules/E/E3/cards.json E3-c138", "PASS",
    f"Card asks what a one-element prior set gives 'for every tau'; L08 Definition 1.2 (text/L08.txt lines 0019-0020) writes the weight as tau and Proposition 1.3 (lines 0021-0027) proves V_tau = E_P u(f) for every tau in [0,1]. No alpha.")
row("E3g-grade-c142", "2.3-grades / 2.4-math", "course/modules/E/E3/cards.json E3-c142; L08.html Theorem 2.2 proof", "PASS",
    f"text/L08.txt line 0041: the proof's 'Strict case' paragraph (not all E_{{P_i}}u(f) equal => one exceeds m => average > m => strict). Re-derived. T grade correct.")
row("E3g-grade-c090", "2.3-grades", "course/modules/E/E3/cards.json E3-c090", "PASS",
    f"Back is Corollary 3.3 hypothesis (psi = 1/gamma) plus Remark 3.4 statement; no lab-read pair on the card (text/L05.txt lines 0063-0064 and 0079-0080). T grade matches the derivation.")
row("E3g-r2-V-symbol", "2.2 / notation: card agrees with lesson text (prospect value symbol)", "cards.json E3-c100, c105, c107, c116", "PASS",
    f"Fixed at a007712: all four backs now write W. L06 Definition 1.3 (text/L06.txt line 0023) defines W := sum p_i v(x_i); Proposition 2.2 (line 0039) and Remark 2.4 (line 0045) use W; Lab 1 prints 'W = -8.6835' (run output in twin_L06.out). No V symbol remains on L06 cards (scope_and_process_scan.out). Arithmetic re-derived (verify_numbers.out, L06 block).")
row("E3g-r2-c145-V1", "2.9 / card cites what its lesson says", "cards.json E3-c145", "PASS",
    f"Fixed at a007712: back no longer cites V1; it says 'the value uses the exponent a = 1 - 1/psi (Definition 3.1)'. L08 Definition 3.1 (text/L08.txt lines 0057-0058) defines a = 1 - 1/psi and has no V1.")
row("E3g-r2-L05-G1", "2.2 / 2.4 / 2.3 (E3-c078 to E3-c087)", "cards.json E3-c078..c087; L05.html Def 1.1, Rem 1.2, Thm 1.3, Cor 1.4, Rem 1.5, Def 2.1, Prop 2.2, Rem 2.3, Rem 3.1, Thm 3.2, Cor 3.3", "PASS",
    f"Every proof re-read (text/L05.txt lines 0031-0037, 0046-0048, 0057-0058, 0061-0062, 0063-0064): Thm 1.3(a),(b) incl. both sign cases of a; Prop 2.2 MRS = ((1-beta)/beta)(c1/c0)^(1/psi) and EIS = psi; Thm 3.2 (1-gamma)U = V0^(1-gamma); Cor 3.3 derivative h'(u) > 0. Numbers: verify_numbers.out (L05 block: CE1 8/5, 12/5 for Remark 1.5, V0 80/49, U -49/80, E2 16/7 and 160/71). Grades T correct.")
row("E3g-r2-L05-G2", "2.2 / 2.3 (E3-c088 to E3-c097, E3-c169)", "cards.json; L05.html Cor 3.3, Rem 3.4, Lab 1 output (text/L05.txt lines 0063-0073)", "PASS",
    f"Remark 3.4 MRS exponents re-derived. Lab 1 printed values: EIS 0.5000, 2.0000, 0.2500 (lab output); U(4,4) = -0.2500, U(1,10) = -0.5500, V0(4,4) = 4.0000, V0(1,10) = 4.3311 (verify_numbers.out reproduces 4.331139); CE1 2.2500, 1.6000, 1.3720 (verify_numbers.out). Grades: T cards are derivations; C cards are lab outputs with basis.")
row("E3g-r2-L05-G3", "2.2 / 2.4 (E3-c170, E3-c098 to E3-c106) against L06 and L05 Remark 1.5", "cards.json; L06.html Defs 1.1-1.6, Props 1.4, 2.1, 2.2, Ex 2.3; L05.html Rem 1.5", "PASS",
    f"L06 Proposition 1.4 derivatives re-derived (text/L06.txt line 0027): v'' = alpha(alpha-1)x^(alpha-2) < 0 on gains, lambda delta(1-delta)(-x)^(delta-2) > 0 on losses. Proposition 2.1 lambda* = 5/3 for Example 2.3 (verify_numbers.out). L05 CE1 = 8/5 (verify_numbers.out).")
row("E3g-r2-L06-G4", "2.2 / 2.4 (E3-c107 to E3-c117, E3-c163)", "cards.json; L06.html Remarks 2.4, 2.5, 3.1, 3.2; Lab 1 output", "PASS",
    f"Remark 2.5: 700 - 300 lambda and 1000 - 600 lambda, 100 and -200 at lambda = 2, 250 and 100 at lambda = 3/2 (verify_numbers.out). Remark 3.2: EV = 400/3 and lambda_R = sqrt(2)/2 for p = 1/3 (verify_numbers.out). Lab grid booleans (twin_L06.out) match the cards. c116 W = -8.683509 and threshold 1.290994 (verify_numbers.out).")
row("E3g-r2-L07-G5", "2.2 / 2.4 (E3-c118 to E3-c127)", "cards.json; L07.html Def 1.1-1.2, Rem 1.3, Ex 1.4, Obs 1.5, Rem 1.6, Ex 2.1, Prop 2.2, Rem 2.3", "PASS",
    f"{S}/l07_numbers.out: omega(3/10) = 0.285790884905, omega(3/5) = 0.391250770027, omega(1/2) = 0.353553390593, 2 omega(3/10) = 0.571581769809, ratio 0.730454498236 (card 0.73045450), thresholds 2/3 and 0.585786437627, grid crossing last point 0.278 with one sign change, 2 - sqrt3 = 0.267949192431. Lab C printed values 42.8686 / 39.1251 and 4.8788 / 3.9125 reproduced (Gamma(A) 42.86863274, Gamma(B) 39.12507700).")
row("E3g-r2-L07-G6", "2.2 / 2.9 (E3-c128 to E3-c137): numbers and content", "cards.json; L07.html Problems R1, R2, E2; Lab 1 parts B-D", "PASS",
    f"Numbers: difference 3.7435557330 -> 3.7436 (l07_numbers.out); misconception counterexample 49.832775 vs 50.5, overweight 7.340301, underweight 8.007526, net -0.667225 (l07_numbers.out); E3 identity 45 and 60 (l07_numbers.out); Lab part D 10 of 10 (twin_L07.out). Terminology on c135 is a separate FAIL row E3g3-c135-terminology.")
row("E3g-r2-L08-G7", "2.4 / 2.3 (E3-c138 to E3-c147)", "cards.json; L08.html Def 1.2, Prop 1.3, Ex 1.4, Def 2.1, Thm 2.2, Prop 2.4, Ex 2.5, Def 3.1, Prop 3.2, Rem 3.3", "PASS",
    f"Proofs re-read (text/L08.txt lines 0027, 0041, 0051, 0068). c139 4180000/41 etc. recomputed (verify_numbers.out). c145 now PASS (see fixed row E3g-r2-c145-V1). c142 'never for a one-element prior' follows from Prop 1.3.")
row("E3g-r2-L08-G8", "2.4 / 2.6 (E3-c148 to E3-c158)", "cards.json; L08.html Rem 4.2, Models 1-4, Lab 1 part B, Problem E3, Section 4 numbers", "PASS",
    f"c148 'not a general property' supported by a three-prior counterexample: priors {{0.2,0.3,0.9}} give alpha-MEU tau=1/2 CE 102702.70 vs EU CE at the average prior 101456.31 (c148_counterexample.out), so the coincidence needs the midpoint to equal the average prior (Remark 4.2). c149 4180000/41, c150 5 - sqrt50, c151 99523.8095, c152 548.7805 cents = 22500/41 (verify_numbers.out). c153 gaps (twin_L08.out).")
row("E3g-r2-L08-G9", "2.2 / 2.4 (E3-c164, E3-c165, E3-c166, E3-c172)", "cards.json; L08.html Ex 2.5, Model 2, Def 1.2", "PASS",
    f"Known urn CEs 103125 and 106451.6129 (verify_numbers.out); worst priors P_0 and P_90 each give 100000 cents surely (Prop 2.4 proof, text/L08.txt line 0051). Model 2: prospect CE -107.2330 cents, wealth 99892.7670 (verify_numbers.out). c172 is Definition 1.2's V_1 (text/L08.txt line 0020).")
row("E3g-r2-numbers", "2.2 numbers (all 85 slice cards)", "cards.json L05-L08", "PASS",
    f"{S}/verify_numbers.py -> verify_numbers.out (exact Fractions and floats reproduce every rational and float number on the cards checked: 8/5, 12/5, 80/49, -49/80, 16/7, 160/71, 2.2500, 1.6000, 1.3720, 4.3311, 0.5/2/0.25 EIS, 80/49, E3 identity values). {S}/token_numbers.py -> token_numbers.out: 643 numbers on 85 cards, 0 absent as whole tokens from the card's lesson dump.")
row("E3g-r2-lab-twins", "2.5 labs (L05-L08 twins)", "tests/labs/E3/lab-E3-L05-1.py ... lab-E3-L08-1.py; L05-L08.html lab sections", "PASS",
    f"run_labs_E3.out: 'run_labs E3: PASS (11/11)'. Each twin run alone as python -I -W error: exit 0, empty stderr (twin_L05.err ... twin_L08.err, 0 bytes). {S}/page_vs_twin.py -> page_vs_twin.out: page code block == twin source and page expected block == twin stdout for L05, L06, L07, L08. Predicted-before-running text on each lab matches the printed output (text/L05.txt 0066 vs lab lines; text/L06.txt 0049; text/L07.txt 0053; text/L08.txt 0072).")
row("E3g-r2-refs-cross", "2.6 cross-references on cards", "cards.json; L05-L08.html; L04.html Theorem 1.5", "PASS",
    f"{S}/card_refs_resolve.py -> card_refs_resolve.out: 107 block references (Definition, Theorem, Proposition, Corollary, Remark, Example, Observation, Assumption, Problem, Model) on the 85 cards, 0 unresolved in their lesson. The one cross-lesson card E3-c129 ('Theorem 1.5 of Lesson 4') resolves to L04 Theorem 1.5 (text/L04.txt line 0029-0030: F_X <= F_Y for all t iff E u(X) >= E u(Y) for every nondecreasing u on S), with X = B, Y = A.")
row("E3g-r2-registry", "2.1 citations (keys and titles cited by the slice)", "references/references.json: kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin (epstein1989substitution not cited by any card)", "PASS",
    "tools/verify_refs.py --offline -> verify_refs_offline.out: 560 entries, 0 problems. tools/verify_refs.py --unit E3 (live Crossref) -> verify_refs_E3_live.out: 5 entries, 0 problems. Registry records read: kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk' (Kahneman, Tversky, 1979); ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' (1961); gilboa1989maxmin 'Maxmin expected utility with non-unique prior' (Gilboa, Schmeidler, 1989). Cards attribute only these titles and years.")
row("E3g-r2-coverage", "2.7 cards: one card per definition, theorem, key formula, key result, misconception", "cards.json; L05-L08.html key-results tables and misconception blocks", "PASS",
    "Mapped every Definition, Theorem, Proposition, Corollary, Remark, Example, Observation, Problem R/E item that carries a result and every key-results row of L05-L08 to card ids (L05: c078-c091, c093-c097, c169, c170; L06: c098-c113, c116, c117, c163; L07: c118-c128, c131-c135; L08: c136-c158, c164-c166, c172, c176). Misconceptions: L05 c081/c082/c085/c090; L06 c110/c112/c108; L07 c123/c130/c132; L08 c142/c146/c154. Gaps in card id numbering (c092, c114, c115, c156 inside the slice range; c042 and c069 removed in round 1) are not content gaps: each such gap sits between cards of one lesson and every block of that lesson has a card.")
row("E3g-r2-grades", "2.3 grades (independent re-grade against BLUEPRINT section 3 and each lesson key-results table)", "cards.json (85 slice cards)", "PASS",
    "Every T card is a derivation or theorem on the page (checked row by row above). Every C card is a lab output or a cite-only title, and matches its lesson key-results grade (e.g., c093, c094, c095, c096, c106, c117, c122, c127, c153, c169, c170 C; c134, c157, c158 C with cite). Ungraded cards are definitions, conventions, and attributions with no result. check_pages_E3.out: every non-T card has cite or basis.")
row("E3g-r2-hypotheses", "2.4 hypotheses of T cards", "cards.json T cards; A1-A5 of Props 1.3, 2.4, 3.2, Thm 1.3, 2.2, Prop 2.2, Prop 1.4, 2.1, 2.2, Cor 3.3", "PASS",
    "Each card carrying a Proposition, Theorem or Corollary result states its numbered assumptions (c080, c081, c084, c086, c087, c088, c089, c090, c101, c104, c105, c107, c141, c143, c146, c154, c155). Cards that rest on a standing or example condition (c082, c085, c091, c108, c112, c142, c148) cite the lesson's standing assumptions A1-A4 (L05 text line 0016-0020), the example's parameters (L06 Example 2.3 line 0043; L08 Example 1.4), or Theorem 2.2's assumptions; accepted as PASS with this note.")
row("E3g-r2-scope-words", "2.4 / 2.9 scope words on cards", "cards.json (every, all, any, only, never, always, exactly, same, each, in general, most, people)", "PASS",
    f"{S}/scope_and_process_scan.py -> scope_and_process_scan.out lists every scope word on a slice card; each was checked against its proof or lab: c085/c089/c107/c146 (every gamma, every lambda > 0, every psi and beta: proofs read), c110 (proofs need lambda > 0 only, Remark 3.1), c112 (negative only above lambda*, Prop 2.2), c123 and c148 (counterexamples), c142 (never, one-element set: Prop 1.3), c154 (Prop 2.4), c155 (A2 only).")
row("E3g-r2-process-words", "2.9 banned and process phrases", "cards.json slice", "PASS",
    f"{S}/scope_and_process_scan.py: no TODO, TBD, lorem, builder, verifier, round, REQUEST or 'checked directly' on any slice card. No ellipses or chatter.")
row("E3g-r2-gates", "gates: check_pages, check_dag, check_projects, run_labs, page_smoke", "tools/check_pages.py, check_dag.py, check_projects.py, run_labs.py, page_smoke.py (L05-L08 pages)", "PASS",
    f"check_pages_E3.out: PASS (exit 0). check_dag_E3.out: PASS. check_projects_E3.out: PASS. run_labs_E3.out: 'run_labs E3: PASS (11/11)'. page_smoke_L05-L08.out: 'page_smoke E3: PASS' for modules/E/E3/L05.html, L06, L07, L08 (zero console errors, math rendered, 360 px, labs in Pyodide).")
row("E3g-r2-delta", "delta since round-2 pin: every hunk touching the slice", "git diff c737272f..a007712f -- cards.json (L05-L08 cards), L08.html", "PASS",
    "Read every hunk. Slice changes: E3-c091 (dropped the clause 'and the two agree only when 1/psi = gamma'; still correct, Remark 3.4), E3-c100, c105, c107, c116 (V -> W, verified above), E3-c145 (V1 removed, verified above), E3-c155 (kappa -> nu, verified against L08 R3 and the L08 solution), E3-c176 (new, verified under E3g3-c176), L08.html Problem R3 and its solution (kappa -> nu; text/L08.txt lines 0161-0163). L05, L06, L07 page text and labs: no change since the round-2 pin (git diff --stat: only L02, L03, L04, L08, cards.json, grader and project files changed in the E3 tree; tests/labs/E3 changed only for project-1 and project-3).")

# ---- new round-3 rows
row("E3g3-c135-terminology", "2.9 / 2.7: card agrees with its lesson text (terms defined in the lesson)", "course/modules/E/E3/cards.json E3-c135 (back, last sentence); L07.html Section 3 and Problem R2", "FAIL",
    f"The back says 'The full rank-dependent value is not derived.' The term 'rank-dependent' occurs nowhere in L07 (grep of {S}/text/L07.txt). The lesson names the construction 'cumulative' (Section 3, text/L07.txt line 0061: 'One repair is cumulative ... This lesson does not derive that repair'; Problem R2 solution, line 0119: 'A full cumulative value is not defined here'). scope_and_process_scan.out line 58: 'E3-c135 L07 ['derived', 'rank-dependent']'.",
    fix="In E3-c135 replace 'The full rank-dependent value is not derived.' with 'The full cumulative value is not derived (Lesson L07, Section 3).' The rest of the card is correct: Tail_B(50) = Tail_A(50) = 3/5 and Tail_B(100) = 3/5 > Tail_A(100) = 3/10 (Problem R2).")
row("E3g3-notation-collisions", "2.4 notation: local letters reused with one meaning across the unit (BUILDER_RULES 2.1 item 7; notation.json has no entry for them)", "L05.html Def 1.1 (V_1 := c_1), Rem 1.2; L08.html Def 1.2 (V_1(f)); cards E3-c078 (V1 = c1), E3-c172 (V_1(f)); L06.html Def 1.3 (W := sum p_i v(x_i)) and cards E3-c100, c105, c107, c116 (W); L08.html wealth W_0, W_1, W_L and u(W) = -1/W (Example 2.5, Model 1, Model 4); L05.html Remark 3.1 (theta = (1-gamma)/(1-1/psi)) vs L08.html Problem P2 (mixture weight theta); L06.html Section 2 (g = gain prize) vs L08.html Remark 4.2 and Problem P3 (g(p) = E_p[1/W])", "FAIL",
    f"Four symbols carry two meanings inside E3 (evidence: {S}/text/L05.txt dump label 0023 'V_1 := c_1'; {S}/text/L08.txt dump label 0020 'V_1(f) = min ...'; {S}/text/L06.txt dump label 0023 'W := sum ...'; {S}/text/L08.txt dump labels 0081, 0085 and 0137 with W_0, W_1 and u(W) = -1/W; {S}/text/L05.txt dump label 0052 'theta := (1-gamma)/(1-1/psi)'; {S}/text/L08.txt dump label 0131 'a mixture theta P_1 + (1 - theta) P_2'; {S}/text/L08.txt dump label 0137 'g(p) = E_p[1/W]'). The plan's local letters must keep one meaning across the unit (plans/E3-build-plan.md section 2.1 item 7). Note that the round-2 change V -> W (prospect value) collides with W as final wealth in L08, which is the older use.",
    fix="Give each meaning its own symbol and change every use on the page and on the cards: maxmin value in L08 Def 1.2 and E3-c172 to V_{\\max\\min}(f) (or \\underline V(f)); terminal convention in L05 Def 1.1 to 'c_1 is the date-1 value' (drop V_1 := c_1) and E3-c078 accordingly; prospect value in L06 Def 1.3, Props 2.1-2.2, Rem 2.4-2.5 and E3-c100, c105, c107, c116 to PV(G) (or another unused symbol); L08 Problem P2 mixture weight to a letter not used elsewhere in E3 (for example s); L08 Remark 4.2 and Problem P3 function g(p) to h(p) if h is unused in E3 (check notation/notation.json and the unit's lessons before choosing).")
row("E3g3-L05-proofs", "2.4 mathematics: proofs of the L05 results cited by slice cards", "L05.html Def 1.1, Rem 1.2, Thm 1.3 (a)(b), Cor 1.4, Rem 1.5, Prop 2.2, Rem 2.3, Rem 3.1, Thm 3.2, Cor 3.3, Rem 3.4", "PASS",
    f"Each proof read in full (text/L05.txt lines 0031-0068). Re-derived with Fractions in {S}/verify_numbers.py: CE1 for {{1,4}} = 8/5 and for {{2,3}} = 12/5; V0 = 80/49 and U = -49/80 with (1-gamma)U = V0^(1-gamma) True; E2 CE1 16/7, V0 160/71; E1 V0^-1 = 49/80. MRS and EIS chain rule re-derived by hand (ln MRS slope 1/psi). Remark 3.4 'only if' argument (r^gamma = r^(1/psi) forces gamma = 1/psi when r != 1) re-checked. Assumption use: A1-A4 on every result that cites them.")
row("E3g3-L06-proofs", "2.4 mathematics: L06 results cited by slice cards", "L06.html Def 1.2-1.6, Prop 1.4, Rem 1.5, Prop 2.1, Prop 2.2, Ex 2.3, Rem 2.4, Rem 2.5, Rem 3.1, Rem 3.2", "PASS",
    f"Prop 1.4 derivatives re-derived (v' = alpha x^(alpha-1) > 0; v'' = alpha(alpha-1)x^(alpha-2) < 0 on gains; on losses v' = lambda delta (-x)^(delta-1) > 0 and v'' = lambda delta(1-delta)(-x)^(delta-2) > 0) (text/L06.txt line 0027). Prop 2.1 W = pg - (1-p) lambda l, lambda* = 5/3 for Example 2.3 (verify_numbers.out). Prop 2.2 threshold sqrt(5/3) at alpha = delta = 1/2 (verify_numbers.out 1.290994). Rem 2.4 monotonicity argument needs no bound on the powers (correct). Rem 3.2 lambda_R: numerator p(g - EV) = (1-p)(l + EV) at alpha = 1 is EV - EV = 0 (correct). EV = 400/3 and lambda_R = sqrt(2)/2 for p = 1/3 (verify_numbers.out).")
row("E3g3-L07-proofs", "2.4 mathematics: L07 results cited by slice cards", "L07.html Def 1.1-1.2, Rem 1.3, Ex 1.4, Obs 1.5, Rem 1.6, Ex 2.1, Prop 2.2, Rem 2.3, Lemma/Theorem reference to L04 Thm 1.5", "PASS",
    f"Ex 1.4 closed form: (sqrt p + sqrt(1-p))^2 = 1 + 2 sqrt(p(1-p)) (text/L07.txt line 0027) re-derived; omega values at 3/10, 3/5, 1/2, 1/4, 0.01, 0.99 recomputed to 12 digits ({S}/l07_numbers.out). Prop 2.2 proof: V_omega(A) = omega(3/10)(50^alpha + 100^alpha), V_omega(B) = omega(3/5) 100^alpha, ratio test re-derived; thresholds 2/3 and 0.585786437627. Ex 2.1 distribution functions (text/L07.txt lines 0036-0041) match. Rem 2.3 identity weights 45 and 60 correct.")
row("E3g3-L08-proofs", "2.4 mathematics: L08 results cited by slice cards", "L08.html Prop 1.3, Thm 2.2, Prop 2.4, Ex 2.5, Def 3.1, Prop 3.2, Rem 4.2", "PASS",
    f"Thm 2.2 proof (average of n numbers each >= m is >= m; strict when not all equal) and Prop 2.4 proof (E_p u(f) = u(W_no) + p(u(W_red)-u(W_no)) increasing in p; black case by q = 1-p) re-derived (text/L08.txt lines 0041, 0051). Prop 3.2 proof injectivity of x^(1/a) with a != 0 and beta > 0 re-derived (line 0068). Rem 4.2: E[1/W] = p/W1 + (1-p)/WL affine, midpoint identity re-derived; g decreasing because W1 > WL (P3 solution). Numbers: verify_numbers.out (4180000/41, 99523.8095, 548.7805 = 22500/41, 98352.94117647, 105822.78481013, 103125, 106451.6129).")
row("E3g3-c176", "2.3 / 2.4: new card E3-c176 (added at a007712)", "cards.json E3-c176 (lesson L08)", "PASS",
    f"Front: EZ CE of the Section 4 gamble at psi = 1/2, beta = 0.95, gamma = 2. Back: 101951.2195 cents, equal to the EU CE because the gamble is at the last date (Model 3; Proposition 3.2). Model 3 text (text/L08.txt line 0085) states c0 = W0, c1 = final wealth, a = -1; Lab 1 part A prints 101951.2195 (run output). Re-derived by Proposition 3.2 (c^a = K argument) and verify_numbers.out (4180000/41). Grade T correct.")
row("E3g3-c148-scope", "2.4 scope claim: 'not a general property' (E3-c148)", "cards.json E3-c148; L08.html Remark 4.2", "PASS",
    f"{S}/c148_counterexample.py -> c148_counterexample.out: with priors {{0.2, 0.3, 0.9}} the tau = 1/2 alpha-MEU CE is 102702.70 cents and the EU CE at the average prior 0.4667 is 101456.31 cents, so the two differ. Remark 4.2 gives the condition (midpoint equal to the average prior); the claim is supported.")
row("E3g3-attribution", "2.1 attribution of cited sources (titles and years only)", "cards.json E3-c134, E3-c137, E3-c157, E3-c158, E3-c097; references/references.json", "PASS",
    "Titles, authors and years from the registry and live Crossref (verify_refs_E3_live.out, 5 entries, 0 problems) match what the cards state: Kahneman and Tversky 1979 'Prospect Theory'; Ellsberg 1961 'Risk, Ambiguity, and the Savage Axioms'; Gilboa and Schmeidler 1989 'Maxmin expected utility with non-unique prior'. The papers' bodies and abstracts were not read; the cards attribute titles only, graded C with cite. E3-c097 (naming of the recursion after Epstein and Zin) is ungraded and attributes no result; epstein1989substitution is in the registry and is not cited by any card.")
row("E3g3-notation-registry", "2.4 notation.json: registered symbols and macros", "notation/notation.json (macros \\E, \\Prob, \\R, ...; symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q})", "PASS",
    f"grep of course/modules/E/E3/L05-L08.html: only \\E, \\Prob and \\R macros are used, and no raw \\mathbb{{E}} or \\mathbb{{R}}. No registered symbol T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f or \\mathbb{{Q}} appears in L05-L08 math (the single 'T' hits are grade badges). gamma is the CRRA coefficient in every lesson; beta, psi, lambda, alpha, delta, theta, tau, nu, omega, eta are local (notation.json 'about' leaves them local). Local-letter collisions are in row E3g3-notation-collisions.")
row("E3g3-page-smoke", "2.9 page_smoke for the slice's lesson pages (L05-L08) alone", "course/modules/E/E3/L05.html, L06.html, L07.html, L08.html", "PASS",
    f"{S}/page_smoke_L05-L08.out: 'page_smoke modules/E/E3/L05.html: PASS', L06 PASS, L07 PASS, L08 PASS; 'page_smoke E3: PASS' (zero console errors, zero external requests, math rendered, no horizontal scroll at 360 px, lab outputs match in Pyodide).")
row("E3g3-gates-projects-ruff", "gates: check_projects, ruff on the four L05-L08 twins", "tools/check_projects.py --unit E3; tests/labs/E3/lab-E3-L05-1.py ... lab-E3-L08-1.py", "PASS",
    f"{S}/check_projects_E3.out: 'check_projects E3: PASS'. ruff check on the four twins: 'All checks passed!' ({S}/ruff_twins.out). Mutation testing: not applicable (no grader in this slice; ruling: mutants apply to project graders only).")
row("E3g3-delta-r3", "delta since round-2 pin for this slice", "git diff c737272f..a007712f -- course/modules/E/E3/cards.json course/modules/E/E3/L05.html L06 L07 L08 tests/labs/E3", "PASS",
    "Read every hunk of cards.json for L05-L08 cards (E3-c091, c100, c105, c107, c116, c145, c155, c176 new) and the L08.html Problem R3 hunk (kappa -> nu). No change to L05, L06 or L07 page text, and no change to any L05-L08 twin in tests/labs/E3 (only project-1 and project-3 changed). Each changed card is re-verified in the rows above.")

fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 3,
    "verifier": "Haiku independent verifier, E3-g round 3 (did not build E3)",
    "pin": "a007712fdbfc8b4851123f4de76b5310ac5a9e64",
    "base": "c737272f5bdef4a027417989cd52254555e8a0bb (round-2 pin; delta read c737272..a007712 for this slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD3-E3-g (detached at a007712)",
    "scratch": "ledgers/E3/scripts/E3-g-r3/ (scripts, outputs, text dumps)",
    "verified_at": "2026-11-02",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: the 85 cards of L05-L08 (course/modules/E/E3/cards.json), read in full, against the four lesson pages read line by line through text dumps (ledgers/E3/scripts/E3-g-r3/text/L05-L08.txt, generated by dump_text.py from the HTML).",
        "No round-2 PASS row was carried by prefix; every round-2 id is kept and re-verified in round 3 against the a007712 subjects.",
        "Round-2 FAIL rows E3g-r2-V-symbol and E3g-r2-c145-V1 are fixed at a007712 and re-verified PASS.",
        "Mutation testing is not applicable: this slice holds cards, no grader (verifier rules: mutants apply to project graders only). mutants is empty by design.",
        "Not checked: the published papers (Kahneman and Tversky 1979; Ellsberg 1961; Gilboa and Schmeidler 1989; Epstein and Zin 1989). Only registry and Crossref records were read; the cards attribute titles and years only. Paywalled bodies not fetched.",
        "Not checked (outside this slice): project.html, grader/, rubric, L01-L04 pages and their cards, index.html, figures (none on L05-L08 beyond the lab), run_graders.py. page_smoke was run for the four lesson pages only, as part of the gate.",
        "Not run: mypy (no Python changed in this slice; the four twins were ruff-checked and run under python -I -W error). pytest: no test covers cards.json beyond check_pages.",
        "Observation, not a row: L05 Remark 1.5 and L08 Remark 4.2 rely on the standing assumptions and on Theorem 2.2 respectively; the cards accept that reliance (see E3g-r2-hypotheses).",
    ],
    "summary": {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"),
                "fail": sum(1 for r in rows if r["status"] == "FAIL"), "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE")},
}

with open("ledgers/E3/E3-g.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "summary", fragment["summary"])
