# Builds ledgers/E3/E3-g.json for round 6. Rows carried from round 5 keep their ids and carry the round-5 evidence
# only where the cited subject is byte-identical since the round-5 pin (440ed3c8). Every other row is re-verified here.
import json, copy, datetime
PIN = "142ecfc2bd27061de18bd67e83df81e69f5c249d"
BASE = "440ed3c8216725d498d9c6d7c746907d4d418198"
r5 = json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-g.round5.json"))
r5rows = {r["id"]: r for r in r5["rows"]}
SC = "ledgers/E3/scripts/E3-g-r6/"
CARRY_NOTE = "Carried from round 5 (subject byte-identical since the round-5 pin 440ed3c8: "
def carry(rid, subject, extra=""):
    src = r5rows[rid]
    row = {"id": rid, "check": src["check"], "location": src["location"], "status": "PASS",
           "evidence": CARRY_NOTE + subject + "): " + src["evidence"] + (" " + extra if extra else "")}
    return row
def fresh(rid, check, location, evidence, status="PASS", fix=None):
    row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    return row
CARD_BYTE = "cards E3-c078..c087, c093..c097, c098..c107, c109..c117, c118..c128, c130, c131, c133..c147, c149, c150, c153..c158, c163..c166, c169..c172 as objects"
rows = []
# ---- carried PASS rows (subjects unchanged since 440ed3c8) ----
rows.append(carry("E3g-notation-c138", "card E3-c138 and L08 Definition 1.2 text"))
rows.append(carry("E3g-grade-c142", "card E3-c142 and L08 Theorem 2.2 strict case"))
rows.append(carry("E3g-grade-c090", "card E3-c090 and L05 Corollary 3.3 / Remark 3.4 text (only the Corollary 3.3 line changed, and E3-c090 cites no line of it)"))
rows.append(carry("E3g-r2-c145-V1", "card E3-c145 and L08 Definition 3.1"))
rows.append(carry("E3g-r2-L05-G1", "cards E3-c078..c087 and L05 Definition 1.1 to Theorem 3.2 text (not the changed line 147)"))
rows.append(carry("E3g-r2-L05-G3", "cards E3-c098..c105 and L06 Proposition 1.4, Remark 1.5, Propositions 2.1 and 2.2, and L05 Remark 1.5"))
rows.append(carry("E3g-r2-L06-G4", "cards E3-c107..c113 and c163; L06 Remarks 2.4, 2.5, 3.1, 3.2 (L06.html unchanged since 440ed3c8)"))
rows.append(carry("E3g-r2-L07-G5", "cards E3-c118..c126 and L07 Definition 1.1 to Proposition 2.2 (the changed L07 line 52 is the chapter introduction, not cited)"))
rows.append(carry("E3g-r2-L08-G7", "cards E3-c137..c143 and L08 Definition 1.2 to Theorem 2.2 / Proposition 2.4 text"))
rows.append(carry("E3g-r2-L08-G9", "cards E3-c144, c164, c165, c166 and L08 Example 2.5, Model 2 text (Model 2 paragraph unchanged)"))
rows.append(carry("E3g-r2-refs-cross", "cards E3-c081, c112, c129, c146, c154 and L04 Theorem 1.5 (L04.html unchanged since 440ed3c8; re-read this round at L04.html lines 89-90)"))
rows.append(carry("E3g-r2-registry", "cards E3-c134, c157, c158 and references/references.json (unchanged since 440ed3c8; titles re-read this round: kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk' 1979; ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' 1961; gilboa1989maxmin 'Maxmin expected utility with non-unique prior' 1989)"))
rows.append(carry("E3g3-c135-terminology", "card E3-c135 and L07 Section 3 text"))
rows.append(carry("E3g3-c091-gamma", "card E3-c091 and L05 Remark 3.4, Theorem 3.2"))
rows.append(carry("E3g3-c132-omega", "card E3-c132 and L07 Misconception 3 (numbers re-derived this round: 49.832775, EV 50.5, overweight 7.3403, underweight 8.0075, net -0.6672; ledgers/E3/scripts/E3-g-r6/numbers_g6.out)"))
rows.append(carry("E3g3-c097-trivia", "the card id list of the unit (no E3-c097 at either pin)"))
rows.append(carry("E3g3-basis-wording", "cards E3-c094, c095, c106, c117, c122, c153 and their lab twins"))
rows.append(carry("E3g3-L06-proofs", "L06 Proposition 1.4, Propositions 2.1, 2.2, Remarks 1.5, 2.4, 2.5, 3.1, 3.2 (L06.html unchanged)", "Re-derived again this round, all agree; see ledgers/E3/scripts/E3-g-r6/numbers_g6.out."))
rows.append(carry("E3g3-L07-proofs", "L07 Definition 1.2, Example 1.4, Remark 1.3, Remark 1.6, Proposition 2.2, Problems R1, R2, M1, E1, E2, E3 (the changed L07 line 52 is not in this list)"))
rows.append(carry("E3g3-attribution", "cards E3-c134, c157, c158 and references/references.json"))
rows.append(carry("E3g3-delta-r3", "round-3 delta a007712f..440ed3c8 of the slice files (a historical diff, unchanged by later commits)"))
rows.append(carry("E3g4-c082-hypotheses", "card E3-c082 and L05 Remark 1.5"))
rows.append(carry("E3g4-c085-hypotheses", "card E3-c085 and L05 Remark 2.3, Proposition 2.2"))
rows.append(carry("E3g4-c091-hypotheses", "card E3-c091 and L05 Remark 3.4"))
rows.append(carry("E3g4-c108-hypotheses", "card E3-c108 and L06 Remark 2.5"))
rows.append(carry("E3g4-c130-argument", "card E3-c130 and L07 Proposition 2.2, Remark 1.6, Lab 1 part C"))
rows.append(carry("E3g4-c142-hypotheses", "card E3-c142 and L08 Theorem 2.2"))
rows.append(carry("E3g4-c155-notation", "card E3-c155 and L08 Problem R3"))
rows.append(carry("E3g4-c096-context", "card E3-c096 and L05 Lab 1 predicted block (re-derived: CE1 2.2500, 1.6000, 1.3720; ledgers/E3/scripts/E3-g-r6/numbers_g6.out)"))
rows.append(carry("E3g4-c172-definition", "card E3-c172 and L08 Definition 1.2"))
rows.append(carry("E3g4-lab-observations", "cards E3-c101, c117, c128, c129, c146, c153 and their L06, L07, L08 text"))
rows.append(carry("E3g5-c169-c170-basis", "cards E3-c169, c170 and L05 Lab 1 predicted block / Remark 1.5"))
# ---- re-verified this round (PASS) ----
rows.append(fresh("E3g-dup-scan", "2.7 duplicates (full scan of the unit's 171 cards, and the slice's 84)",
 "course/modules/E/E3/cards.json (slice L05-L08, E3-c176 absent, E3-c179 added)",
 "ledgers/E3/scripts/E3-g-r6/card_checks_g6.py -> card_checks_g6.out: exact duplicate fronts: none; exact duplicate backs: none; unit ids unique (171 of 171); near pairs with difflib ratio >= 0.55 touching the slice: E3-c169/c170 (0.62, distinct facts U and CE1), E3-c070/c124 (0.57, L04 Example 1.7 card vs L07 Example 2.1 card: same question form, different lotteries, distinct), E3-c109/c163 (0.57, narrow framing vs integrated evaluation, distinct), E3-c137/c172 (0.56, alpha-MEU definition vs its tau=1 value, distinct). Overlapping-fact pairs judged distinct questions: c143/c164/c154 (Proposition 2.4 worst priors used in three questions), c146/c179 (c179 is the four-model table row for the Section 4 gamble, c146 is the general statement), c106/c112 (values 50 at lambda 3/2 used in two questions)."))
rows.append(fresh("E3g-r2-V-symbol", "3 notation: W (prospect value) collisions", "cards E3-c100, c104, c105, c107, c113, c148, c155; text/L06 Definition 1.3; text/L07, text/L08",
 "grep for a standalone symbol W in text/L07.txt and text/L08.txt returns no hit (the only W is the L06 prospect value and cards E3-c100, c104, c105, c107, c113 that use it with that meaning); E3-c148 uses E_P[1/w] and E3-c155 uses u(w) = -exp(-nu w)."))
rows.append(fresh("E3g-r2-L05-G2", "2.4/2.3 Corollary 3.3 and cards E3-c088..c091",
 "cards E3-c088 (changed this round), c089, c090, c091; course/modules/E/E3/L05.html line 147; text/L05.txt Corollary 3.3, Remark 3.4",
 "Corollary 3.3 now reads 'for any two plans X and Y ... V0(X) >= V0(Y) iff U(X) >= U(Y)'; E3-c088 back uses V0(X) >= V0(Y) and U(X) >= U(Y). Proof re-derived: h(u) = ((1-gamma) u)^(1/(1-gamma)), h'(u) = ((1-gamma)u)^(gamma/(1-gamma)) > 0 on the half-line where (1-gamma)U > 0, which contains every U since (1-gamma)U = V0^(1-gamma) > 0 (A4). Remark 3.4 MRS exponents gamma and 1/psi re-derived. The P/Q collision is gone (no P or Q plan symbol in L05 or c088)."))
rows.append(fresh("E3g-r2-numbers", "2.2 numbers in prose and cards (every number in the slice's cards and lessons)",
 "text/L05..L08; cards.json slice; ledgers/E3/scripts/E3-g-r6/numbers_g6.py -> numbers_g6.out",
 "Independent Fraction and 60-digit Decimal recomputation (numbers_g6.out): omega(3/10)=0.285790884905, omega(3/5)=0.391250770027, omega(1/2)=0.353553390593, omega(2/5)=0.319454916012, omega(1/4)=2-sqrt3=0.267949192431; ratio 0.7304544982 (8dp 0.73045450); 8dp display ratio 0.7304544858 (0.73045449); Remark 1.6 sum 0.8910366858 (0.89103669); Gamma(A) 42.86863274, Gamma(B) 39.12507700, difference 3.74355573 (8dp difference 3.74355574, both 3.7436); crossing omega(p)=p at 0.27813; eta=1 gap 0.31256 at p=0.862. L05: 8/5, 12/5, 80/49, -49/80, 160/71, 16/7, 2.2500, 1.6000, 1.3720, 4.3311, theta=-2, 3/2. L06: 1.2910, -8.6835, 700-300 lambda=100, 1000-600 lambda=-200, lambda_R=sqrt2/2. L08: 4180000/41=101951.2195, 98352.94, 105822.78, 99523.8095, 99892.7670 (-1.072330 CU), 103125, 106451.6129, 548.7805 = 22500/41, 476.1905, 3125 cents. All agree with the printed numbers of the lessons and the labs. The unrounded-wording defects are separate rows."))
rows.append(fresh("E3g-r2-lab-twins", "2.5 labs: run_labs, twins under python -I -W error, page code equals twin, expected block equals output",
 "tests/labs/E3/lab-E3-L05-1.py .. lab-E3-L08-1.py; course/modules/E/E3/L05.html .. L08.html",
 "tools/run_labs.py --unit E3 --page L0n (n=5..8) -> ledgers/E3/scripts/E3-g-r6/run_labs_L0n.out: 'run_labs E3: PASS (1/1)' each, exit 0. Twins alone: python -I -W error tests/labs/E3/lab-E3-L0n-1.py exit 0 (twin_L0n.out). pytest -k 'E3 or lab or page' over tests/test_labs.py, test_run_labs.py, test_page_checks.py: 100% pass (pytest_labs_r6.out). The four labs use no randomness and no network. Lab outputs read against the lesson prose: Lab 1 CE1 2.2500/1.6000/1.3720, EIS 0.5000/2.0000/0.2500, Gamma 42.8686/39.1251 and 4.8788/3.9125, Part D 10 of 10, Model 1-4 values, two-urn 103125.0000/100000.0000."))
rows.append(fresh("E3g-r2-coverage", "2.9/2.7 retrieval: every key result, definition and misconception has a card",
 "L05..L08 Key results tables and misconception sections; cards.json slice",
 "Key results: L05 Theorem 1.3 (c080), Corollary 1.4 (c081), Proposition 2.2 (c084), Remark 3.1 (c086), Theorem 3.2 (c087), Corollary 3.3 (c088), Remark 3.4 (c089), Lab 1 rows (c093, c094, c095, c169, c170). L06 Proposition 1.4 (c101), Remark 1.5 (c102), Proposition 2.1 (c104), Proposition 2.2 (c105), Remark 2.4 (c107), Remark 2.5 (c108), Remark 3.1 (c110), Lab rows (c106, c116, c117). L07 Example 1.4 (c121), Remark 1.3 (c120), Observation 1.5 (c122), Remark 1.6 (c123), Proposition 2.2 (c125), Lab/part D (c127, c128), misconceptions (c130, c132, c123). L08 Proposition 1.3 (c138), Theorem 2.2 (c141, c142), Proposition 2.4 (c143), Example 2.5 (c144, c164, c165), Proposition 3.2 (c146), Remark 4.2 (c148), Models 1, 2, 3, 4 (c149, c150, c179, c151), misconceptions (c154, c142, c146), Ellsberg and Gilboa (c157, c158). Each misconception has a card: L05 (c088, c085, c081), L06 (c112, c110, c108), L07 (c130, c123, c132), L08 (c154, c142, c146)."))
rows.append(fresh("E3g-r2-grades", "2.3 grades: card grades against the lesson key-results grades",
 "cards.json slice (L05 20, L06 19, L07 18, L08 27); lessons' key-results tables",
 "Counts from cards_L05_L08.txt: 50 T, 17 C, 17 ungraded definition cards (no grade needed for a definition, BUILDER_RULES section 7). Every C card names its basis (lab part, Problem, or cite key): c093, c094, c095, c096, c106, c116, c117, c122, c127, c128, c131, c134, c153, c157, c158, c169, c170. Each key-results T row matches a T card and each key-results C row matches a C card (see E3g-r2-coverage)."))
rows.append(fresh("E3g-r2-hypotheses", "2.4 cards carry the hypotheses of the proposition they cite",
 "cards.json slice T cards; cards E3-c148 (changed) and E3-c151 (changed); L08.html Model 1, Model 4, Remark 4.2",
 "All T cards carry their hypotheses (A1 to A4 on c080 to c091; A1 to A3 on c125, c138, c141, c142, c143; A1 to A5 on c146; alpha = delta on c102, c111, c113; lambda > 0 on c101 and c107; psi = 1/gamma with gamma not 0 on c087, c088; u(w) = -1/w on c148, c151, c152 (added this round). The round-5 hypothesis gap is closed. Re-derived: L08 Model 4 claim 99523.8095 = 1/(1/3/110000 + 2/3/95000) requires u(w) = -1/w (Model 1), now stated in L08.html line 451 and Remark 4.2 line 468."))
rows.append(fresh("E3g-r2-scope-words", "2.4/2.9 scope words in the slice (only, all, always, every, any, same, exactly, drives)",
 "text/L05..L08 and cards (grep, scoped reading of each hit)",
 "Every hit read in context: L05 'only through CE1' (Theorem 1.3(a)); 'depends on c0, c1, beta, psi only' (Remark 2.3); 'every gamma != 1' (A3); 'exactly when psi = 1/gamma' (Remark 3.1, algebra); 'for three values of gamma only' (lab). L06 'for this value function only' (Remark 1.5); 'every value is exact' (lab block, exact Fraction). L07 'every nondecreasing u' (Lesson 4 theorem), 'every finite lottery' (Remark 1.3). L08 'for every such f' (Theorem 2.2 A1 to A3), 'the same prize' (Proposition 2.4 A3). All scope words are scoped by a hypothesis or a computation, except the psi domain in L08 (separate row E3g6-psi-domain)."))
rows.append(fresh("E3g-r2-process-words", "1.3/1.4 banned and process phrases", "text/L05..L08; cards slice",
 "grep for TODO, TBD, lorem, for brevity, omitted, beyond the scope, verifier, builder, round, draft, we will, let us, obviously, clearly, it can be shown: no hit in text/L05..L08 or the slice cards (ledgers/E3/scripts/E3-g-r6/phrase_delta_checks_g6.out). The one card hit (E3-c050, 'round', a rounding rule) is an L03 card, outside the slice. 'We write' (L05 Section 1) is mathematical exposition."))
rows.append(fresh("E3g-r2-gates", "2.9 gates: check_pages, check_dag, check_projects, page_smoke, ruff, mypy, verify_refs (pages alone)",
 "course/modules/E/E3/L05..L08.html; tools/*",
 "tools/check_pages.py --unit E3 --page L05..L08: PASS each (check_pages_L0n.out). tools/check_dag.py --unit E3: PASS (check_dag.out). tools/check_projects.py --unit E3: PASS (check_projects.out). tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08 --skip-sweep: 'page_smoke E3: PASS', zero failures (page_smoke.out; the four pages contain no SVG or figure, so the figure sweep has nothing to run). ruff check and ruff format --check on the four twins: PASS (ruff_check.out, ruff_format.out). mypy --no-incremental on the four twins: 'Success: no issues found in 4 source files' (mypy.out)."))
rows.append(fresh("E3g-r2-delta", "delta of the slice since the round-5 pin (440ed3c8..142ecfc2)",
 "git diff 440ed3c8 142ecfc2 for course/modules/E/E3/cards.json, L05.html, L07.html, L08.html, tests/labs/E3/",
 "Every slice hunk read. cards.json: E3-c088 (X,Y in place of P,Q), E3-c148 and E3-c151 (u(w) = -1/w added), E3-c152 (u(w) = -1/w added), E3-c179 added (L08, Model 3 row: Epstein-Zin 101951.2195 at psi = 1/2, beta = 0.95, gamma = 2; checked against Proposition 3.2 A1 to A5 and the Model 3 text), E3-c178 added and E3-c175 reworded (both L03, outside this slice; not verified here). L05.html line 147 (Corollary 3.3 X,Y), L07.html line 52 (introduction: 'its weights are values of Example 1.4'), L08.html lines 451 (Model 4) and 468 (Remark 4.2): u(w) = -1/w stated. tests/labs/E3: lab-E3-project-1/3 only (not in this slice). Carry-forward rows above name the subjects they depend on."))
rows.append(fresh("E3g3-L05-proofs", "2.4 mathematics: L05 Theorem 1.3, Corollary 1.4, Proposition 2.2, Remark 3.1, Theorem 3.2, Corollary 3.3, Remark 3.4",
 "text/L05.txt (line 147 changed this round for Corollary 3.3)",
 "Re-derived: Theorem 1.3(a) and (b) (H(x) and the two monotone cases with 1/a sign); Corollary 1.4; Proposition 2.2 MRS = (1-beta)/beta (c1/c0)^(1/psi) and EIS = psi; Remark 3.1 theta = 1 iff psi = 1/gamma; Theorem 3.2 (1-gamma)U = V0^(1-gamma); Corollary 3.3 for X and Y, derivative of h positive on the half-line; Remark 3.4 exponents gamma and 1/psi with the 'only if' step (r^gamma = r^(1/psi) with r != 1). No defect."))
rows.append(fresh("E3g3-L08-proofs", "2.4 mathematics: L08 Proposition 1.3, Theorem 2.2, Proposition 2.4, Example 2.5, Proposition 3.2, Remark 4.2, Models 1 to 4, Problems M1 to M3, E1 to E3, R2",
 "text/L08.txt (Model 4 and Remark 4.2 changed this round)",
 "Re-derived in numbers_g6.out: Proposition 3.2 (injectivity of x -> x^(1/a) on positive numbers, a != 0); Proposition 2.4 (P_0 and P_90 with A3); Example 2.5 (103125 and 106451.6129; 100000 for both maxmin colours; for any strictly increasing u each known-urn CE exceeds 100000); Remark 4.2 (affine g, midpoint 1/2); Model 2 (5 - sqrt50, -1.072330 CU, 99892.7670); Model 4 (1/3 minimal prior, 99523.8095); Problem M1 (1672000/17 = 98352.94), M2 (105822.78), M3, E3 (22500/41 = 548.7805, 5.4878 CU), R2 (30 to 60 gives 103125 for red and black indifference, 106451.6129 known black), R3 (Theorem 2.2 A2 only). No defect in the mathematics; the psi-domain scope is a separate row."))
rows.append(fresh("E3g3-c148-scope", "2.3/2.4 card E3-c148 scope (Remark 4.2 and Section 5 bullet 4)", "cards E3-c148 (line 984); text/L08.txt Remark 4.2, Section 5",
 "Back now states u(w) = -1/w (Model 1) before the affine argument; scope sentence 'not a general property of alpha-MEU (Remark 4.2)' matches Remark 4.2 and Section 5 bullet 4."))
rows.append(fresh("E3g3-page-smoke", "2.5/2.9 page_smoke for L05..L08 (zero console errors, math rendered, no external requests)",
 "course/modules/E/E3/L05..L08.html", "tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08 --skip-sweep -> page_smoke.out: 'page_smoke E3: PASS', exit 0 (the pages contain no figures, so the skipped sweep has no content)."))
rows.append(fresh("E3g3-gates-projects-ruff", "2.6 project gates and ruff for the slice's twins", "tools/check_projects.py; tests/labs/E3/lab-E3-L05..L08-1.py",
 "check_projects.py --unit E3: PASS (check_projects.out); ruff check and ruff format --check on the four twins: PASS (ruff_check.out, ruff_format.out)."))
rows.append(fresh("E3g3-notation-registry", "3 notation: registered symbols and macros (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, mathbb Q, Prob, E, R) against L05..L08",
 "notation/notation.json; course/modules/E/E3/L05..L08.html; cards slice",
 "grep of the four lesson HTML files and the slice cards: no \\mathbb{Q}, no \\Phi, no \\gamma_3 or \\gamma_4, no R_f, no R^\\ast or R^{e\\ast}, no standalone T symbol. \\Prob appears in L07 only, with its registered meaning (probability of X <= t). Plain P is a prior measure in L08 (\\mathcal{P} set, E_P, \\bar P) and is not a registered symbol. The former P and Q plans in L05 Corollary 3.3 and E3-c088 are now X and Y (ledgers/E3/scripts/E3-g-r6/phrase_delta_checks_g6.out, macro survey)."))
rows.append(fresh("E3g3-notation-collisions", "3 notation: local letters reused with another meaning inside the slice",
 "cards E3-c088, c148, c155; L05 Corollary 3.3; L08 Remark 4.2",
 "W is the prospect value only in L06 (no W in L07 or L08 text or cards). w is final wealth in L08 (E3-c148, E3-c151, E3-c155). V_0 (Epstein-Zin, L05 and L08 Definition 3.1) and V_tau(f) (alpha-MEU, L08) are distinct subscripts with stated definitions. alpha, delta, lambda are the L06 and L08 Model 2 parameters, and tau is the L08 alpha-MEU weight. No collision with a registered meaning (see E3g3-notation-registry)."))
rows.append(fresh("E3g4-c148-notation", "card E3-c148 notation (E_P[1/w] as in Remark 4.2)", "cards E3-c148 (line 984); text/L08.txt Remark 4.2",
 "Back reads E_P[1/w], matching Remark 4.2 (final wealth w), and states u(w) = -1/w (Model 1)."))
rows.append(fresh("E3g5-c148-utility", "2.4 hypotheses of card E3-c148 (utility for the affine identity)", "cards E3-c148 (line 984); text/L08.txt Remark 4.2, Model 1",
 "Back now begins 'With u(w) = -1/w (CRRA, gamma = 2, Model 1), for a two-outcome gamble E_P[1/w] is affine in p.' The common value 101951.2195 holds only for u(w) = -1/w; the affine identity is Remark 4.2's hypothesis. Closed."))
rows.append(fresh("E3g5-c151-utility", "2.4 hypotheses of card E3-c151 (maxmin value 99523.8095)", "cards E3-c151 (line 1002); text/L08.txt Model 4 (line 451)",
 "Back now begins 'With u(w) = -1/w (CRRA, gamma = 2, Model 1), the maxmin certainty equivalent is 99523.8095 cents'. Model 4 (L08.html line 451) now reads 'Under u(w) = -1/w (Model 1), the certainty equivalent at a prior p is 1/(p/w_1 + (1 - p)/w_L)'. Closed."))
rows.append(fresh("E3g5-c152-utility", "2.4 hypotheses of card E3-c152 (risk premium 548.7805)", "cards E3-c152 (line 1009); text/L08.txt Section 4 Model 1",
 "Back begins 'With u(w) = -1/w (Model 1) and P(red) = 1/2'. 102500 - 101951.2195 = 548.7805 = 22500/41 re-derived (numbers_g6.out). PASS."))
rows.append(fresh("E3g5-notation-PQ", "3 notation: plans P and Q against the registered \\mathbb{Q}", "text/L05.txt Corollary 3.3; cards E3-c088; notation/notation.json",
 "Corollary 3.3 (L05.html line 147) and E3-c088 now use plans X and Y; no P or Q plan symbol remains in L05 or the slice cards; \\mathbb{Q} is not used in the slice (grep in phrase_delta_checks_g6.out)."))
rows.append(fresh("E3g-r2-L08-G8", "2.2/2.3/2.4 L08 numbers and grades for cards E3-c146, c148, c149, c150, c151, c152, c153",
 "cards.json E3-c146, c148 (changed), c149, c150, c151 (changed), c152 (changed), c153; text/L08.txt Proposition 3.2, Remark 4.2, Models 1 to 4",
 "Every number re-derived (numbers_g6.out): 4180000/41 = 101951.2195; maxmin 99523.8095; prospect 99892.7670; tau = 1/2 equals EU; premium 548.7805 = 22500/41. The round-5 FAIL was the missing utility on E3-c148 and E3-c151; both now state u(w) = -1/w (Model 1), and E3-c152 states it too. Grades: T for closed forms and proved claims, C for the lab-based one (c153). Closed."))
# ---- FAIL rows (new this round or still open) ----
rows.append(fresh("E3g-r2-L07-G6", "2.6/2.8 L07 lab part C and cards E3-c127, c128, c131, c133, c135",
 "cards E3-c127, c128, c131 (see E3g4-c131-unrounded), c133, c135; L07 Lab 1 parts C and D",
 "Lab values and Part D checked against the twin output (twin_L07.out): Gamma(A) 42.8686, Gamma(B) 39.1251 at alpha = 1; 4.8788, 3.9125 at alpha = 0.5; 10 of 10 utilities. Card E3-c131 back mislabels the eight-decimal values as unrounded (row E3g4-c131-unrounded), so this row fails with it.",
 status="FAIL", fix="Fix card E3-c131 back as stated in row E3g4-c131-unrounded; the other cards in this row pass."))
rows.append(fresh("E3g4-c131-unrounded", "2.2 numbers: card E3-c131 (unrounded difference)",
 "cards.json E3-c131 (line 863); text/L07.txt E2 solution (line 362)",
 "The number 3.7436 is right: the 40-digit difference 3.74355573 rounds to 3.7436 (numbers_g6.out), and the 8dp displayed values 42.86863274 - 39.12507700 = 3.74355574 also round to 3.7436. But the back says '3.7436, from the unrounded values 42.86863274 and 39.12507700'. Those two numbers are the eight-decimal roundings, and the lesson's own E2 solution says so ('each rounded from its 40-digit value').",
 status="FAIL", fix="Change the E3-c131 back to: '3.7436, from the unrounded 40-digit values, whose difference is 3.74355573 (the eight-decimal values 42.86863274 and 39.12507700 subtract to 3.74355574; both round to 3.7436). The printed values differ by 3.7435 because each was rounded separately (Lab 1, part C).'"))
rows.append(fresh("E3g6-psi-domain", "2.4 scope: 'for every psi != 1' stated without psi > 0 (Definition 3.1 and Proposition 3.2 A1)",
 "text/L08.txt line 424 (course/modules/E/E3/L08.html Section 5), line 442 (Misconceptions), quiz option at line 620",
 "L08 Definition 3.1 and Proposition 3.2 A1 both require psi > 0 and psi != 1 (text/L08.txt lines 115 and 122), and the Epstein-Zin value is undefined in the lesson for psi <= 0. But line 424 says Proposition 3.2 'makes the Epstein-Zin row equal to the CRRA row for every psi != 1 and beta in (0,1)', line 442 says 'equal for every psi != 1 and beta in (0,1) (Proposition 3.2)', and the quiz option at line 620 says 'for every psi != 1 and beta in (0,1)'. The domain stated is wider than the hypotheses. Line 424's parenthetical 'the hypotheses of that proposition' does not restate psi > 0. The grep of the card E3-c146 is clean: it states psi > 0 and psi not 1 (cards line 195).",
 status="FAIL", fix="At L08.html line 424, line 442 and the quiz option for the Epstein-Zin/CRRA identity, replace 'every psi != 1' with 'every psi > 0 with psi != 1' (and in line 424 drop the parenthetical or keep it after the explicit domain)."))
rows.append(fresh("E3g6-L07-ex14-unrounded", "2.2 numbers vs unrounded values: L07 Example 1.4 labels 8dp values as unrounded",
 "course/modules/E/E3/L07.html Example 1.4 paragraph (text/L07.txt line 63)",
 "The paragraph reads 'The unrounded values used below are omega(3/10) = 0.28579088, omega(3/5) = 0.39125077 and omega(1/2) = 1/(2 sqrt2) = 0.35355339'. Recomputed (numbers_g6.out): omega(3/10) = 0.285790884905, omega(3/5) = 0.391250770027, omega(1/2) = 0.353553390593. The three quoted numbers are eight-decimal roundings, not unrounded values; the same paragraph's next sentence says so ('Values quoted to eight decimals on this page are rounded from unrounded values'). The label contradicts the sentence it introduces.",
 status="FAIL", fix="Replace 'The unrounded values used below are' with 'The values used below, rounded to eight decimals, are'. The 40-digit values are 0.2857908849, 0.3912507700 and 0.3535533906."))
rows.append(fresh("E3g6-c121-unrounded", "2.2 numbers vs unrounded values: card E3-c121 labels 8dp values as unrounded",
 "cards.json E3-c121 (back)", "The back reads 'The unrounded values are omega(3/10) = 0.28579088, omega(3/5) = 0.39125077 and omega(1/2) = 0.35355339'. These are the eight-decimal roundings (numbers_g6.out gives 0.285790884905, 0.391250770027, 0.353553390593). The label is false; the numbers are right to eight decimals.",
 status="FAIL", fix="In the E3-c121 back, replace 'The unrounded values are' with 'To eight decimals, omega(3/10) = 0.28579088, omega(3/5) = 0.39125077 and omega(1/2) = 0.35355339 (Example 1.4)'."))
# ---- new PASS rows (this round) ----
rows.append(fresh("E3g6-c179", "2.7 card E3-c179 (new this round): Epstein-Zin CE of the Section 4 gamble, Model 3",
 "cards.json E3-c179 (new); text/L08.txt Model 3 and Proposition 3.2",
 "Back: 101951.2195 cents at psi = 1/2, beta = 0.95, gamma = 2 (Model 3, Proposition 3.2). Model 3 text (L08.html Section 4) states the same value; Proposition 3.2 A1 to A5 hold (psi = 1/2 > 0, gamma = 2 != 1, beta in (0,1), c0 = 100000 > 0, finite support 110000 and 95000 both positive); the value equals the EU value 4180000/41 (numbers_g6.out). Atomic: one fact about the Model 3 row. Not an exact duplicate of E3-c146 (the general statement) or E3-c149 (the EU value); it is the Model 3 row of the key-results table, which the round-5 coverage row required."))
rows.append(fresh("E3g6-L07-intro-hunk", "2.9 prose: L07 introduction line changed this round", "course/modules/E/E3/L07.html line 52 (the why-it-matters paragraph)",
 "New sentence 'its weights are values of Example 1.4' matches Example 1.4 (the weight function omega_{1/2}) and the quantities in Remark 1.6. The sentence 'it quotes no empirical magnitude' is the same claim as Section 3. PASS."))
rows.append(fresh("E3g6-L08-model4-hunk", "2.4/2.9 L08 Model 4 and Remark 4.2 hunks changed this round", "course/modules/E/E3/L08.html lines 451 and 468; text/L08.txt Model 4, Remark 4.2",
 "Model 4 and Remark 4.2 now state u(w) = -1/w (Model 1). Re-derived: the maxmin CE 1/(1/3/110000 + 2/3/95000) = 99523.8095 and the tau = 1/2 alpha-MEU value 101951.2195 (affine g, midpoint 1/2), numbers_g6.out. The added hypothesis is the one the claim needs. PASS."))
rows.append(fresh("E3g6-L05-cor33-hunk", "2.4 prose: L05 Corollary 3.3 line changed this round", "course/modules/E/E3/L05.html line 147; text/L05.txt Corollary 3.3",
 "Corollary 3.3 now quantifies over plans X and Y with V0(X) >= V0(Y) iff U(X) >= U(Y); the proof (h increasing on the values of U) is unchanged and applies to any two plans. The notation no longer reuses the registered \\mathbb{Q} letter. PASS."))
rows.append(fresh("E3g6-verify-refs", "2.1 citations: registry integrity for the slice's keys", "references/references.json; cards E3-c134, c157, c158; L05 Section 9, L06 Section 9, L08 Section 4",
 "tools/verify_refs.py --offline -> verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. Titles of the three cited keys read from the registry (kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin) and of epstein1989substitution (cited by key in L05 Section 9). NOT CHECKED: a live Crossref resolution of these records (no plain curl run this round)."))
rows.append(fresh("E3g6-banned-phrases", "1.3/1.4 banned phrases and placeholders in the four lesson texts and slice cards",
 "ledgers/E3/scripts/E3-g-r6/phrase_delta_checks_g6.py -> phrase_delta_checks_g6.out",
 "No hit for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, historically, roughly half, interestingly, importantly, notably; no ellipsis outside code lines."))
rows.append(fresh("E3g6-pytest", "2.5 relevant pytest over the lab and page tooling", "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py (-k 'E3 or lab or page')",
 "ledgers/E3/scripts/E3-g-r6/pytest_labs_r6.out: all selected tests pass, exit 0."))
fragment = {
 "unit": "E3", "slice": "g", "round": 6,
 "verifier": "Haiku independent verifier, E3-g round 6 (did not build E3)",
 "pin": PIN, "base": BASE + " (round-5 pin; delta 440ed3c8..142ecfc2 read for this slice)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD6-E3-g (detached at 142ecfc2)",
 "scratch": SC + " (scripts, outputs, text/ holds the L05-L08 lesson text read in full, cards_L05_L08.txt holds the 84 slice cards read in full)",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
  "Slice g is the 84 E3 cards of L05 (20), L06 (19), L07 (18) and L08 (27), read against the four lesson texts in full (text/L05..L08.txt, read line by line). Every card was read; every number in the cards and lessons was recomputed (numbers_g6.py) or read from a lab output that was re-run.",
  "Round-5 FAIL rows E3g-r2-L08-G8, E3g-r2-hypotheses, E3g3-notation-collisions, E3g3-notation-registry, E3g5-c148-utility, E3g5-c151-utility and E3g5-notation-PQ are re-verified on this pin and now PASS: the utility hypotheses are on cards E3-c148, E3-c151 and E3-c152 and in L08 Model 4 and Remark 4.2; the P/Q plans are X and Y.",
  "Not a project slice: no student-error mutants and no alternative implementations are part of this slice. mutants is empty by design.",
  "Outside this slice, not verified here: cards E3-c175 (reworded), E3-c178 (new) and E3-c177 (round 5) are L03 cards of another slice.",
  "This is a finding-only round. No lesson, card, lab, notation or registry file was edited; the five FAIL rows name the exact text change."
 ],
 "summary": {"rows": len(rows), "pass": sum(r["status"]=="PASS" for r in rows), "fail": sum(r["status"]=="FAIL" for r in rows), "unverifiable": 0, "mutants": 0, "mutants_killed": 0}
}
json.dump(fragment, open("/Users/billyribeiro/.fanout/wt/verifyD6-E3-g/ledgers/E3/E3-g.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "ids unique", len({r['id'] for r in rows}) == len(rows))
print("PASS", sum(r['status']=='PASS' for r in rows), "FAIL", sum(r['status']=='FAIL' for r in rows))
missing = set(r5rows) - {r['id'] for r in rows}
print("round-5 ids missing:", sorted(missing))
