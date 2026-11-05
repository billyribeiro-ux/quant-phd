"""Build ledgers/E3/E3-g.json for round 11 (unit E3, slice g). Every row cites the scripts and outputs in ledgers/E3/scripts/E3-g-r11/."""
import json
import subprocess
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD11-E3-g"
S = "ledgers/E3/scripts/E3-g-r11"
PIN = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
PREV = "47a36d8c78633793ccc762ae19dcd5e19b780d19"
BASE = "2d755599d8d74df292e3e43025f0458c4053802e"

GATES = (f"check_pages ({S}/check_pages_L05.out..L08.out: PASS each); check_dag ({S}/check_dag.out: PASS); "
         f"check_projects ({S}/check_projects.out: PASS); run_labs ({S}/run_labs_L05.out..L08.out: PASS); "
         f"page_smoke L05-L08 alone ({S}/page_smoke_L05-L08.out: PASS); ruff ({S}/ruff.out: PASS); mypy --no-incremental "
         f"({S}/mypy.out: no issues); pytest relevant suites ({S}/pytest_relevant.out: exit 0); verify_refs --offline "
         f"({S}/verify_refs_offline.out: 560 entries, 0 problems)")
TWIN = (f"lab twins run alone under python -I -W error: tests/labs/E3/lab-E3-L05-1.py..L08-1.py exit 0, stderr 0 bytes "
        f"({S}/twin-L05.out..L08.out, .err); page code equals twin and expected block equals output (run_labs, above)")
DERIV = f"{S}/l07_numbers_r11.py + .out (decimal, 60 digits) and {S}/l08_numbers_r11.py + .out (Fractions)"
CARDS = f"{S}/cards_L05.txt..cards_L08.txt (dump_cards.py of cards.json)"
LESS = f"{S}/L05.txt..L08.txt (strip.py of course/modules/E/E3/L0x.html, read in full)"

rows = []
def R(id_, check, location, status, evidence, fix=""):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

# ---- round-10 row ids, re-verified this round (every subject below changed or was re-read in full) ----
P = "PASS"
R("E3g-notation-c138", "2.4 notation (E3-c138 uses tau, not alpha)", "cards.json E3-c138; L08.html Definition 1.2",
  P, f"Re-read L08 Def 1.2 in full ({LESS}): weight written tau, alpha reserved for Lesson 6 (L06 Def 1.2 alpha = gains exponent). "
     "notation/notation.json has no tau or alpha (both local per its 'about' field). E3-c138 matches Proposition 1.3.")
R("E3g-grade-c142", "2.3 grades (E3-c142 is the strict case of Theorem 2.2)", "cards.json E3-c142; L08.html Theorem 2.2 proof",
  P, "L08.txt line 49: strict case re-derived (numbers not all equal -> max > m -> average > m -> strict). E3-c142 (T) states A2 and A3. Read in full this round.")
R("E3g-grade-c090", "2.3-grades (E3-c090 is T; lab pair is E3-c095 grade C)", "cards.json E3-c090; L05.txt Corollary 3.3, Remark 3.4",
  P, f"L05.txt lines 65-70 (Cor 3.3, Remark 3.4) re-read; E3-c090 (T) names Cor 3.3 needs psi=1/gamma and Remark 3.4 off-restriction; grade T is the theorem reading. E3-c095 carries C. Re-derived MRS exponents gamma vs 1/psi.")
R("E3g-r2-c145-V1", "2.9 structure (E3-c145 cites its lesson)", "cards.json E3-c145; L08.html Definition 3.1", P,
  f"L08.txt Def 3.1 (timing convention: gamble pays at date 1 only; a=1-1/psi): E3-c145 matches. Read in full.")
R("E3g-r2-L05-G1", "2.4 math / 2.6 cards (E3-c078..c087)", "cards.json E3-c078..c087; L05.txt Def 1.1..Thm 3.2", P,
  f"Re-derived Def 1.1, Remark 1.2, Thm 1.3 (a),(b) (sign of a), Cor 1.4, Def 2.1, Prop 2.2 (chain rule: dV0/dc0 = (1-beta)c0^(a-1)K^(1/a-1), dV0/dc1 = beta c1^(a-1)K^(1/a-1); MRS=(1-beta)/beta (c1/c0)^(1-a)), Remark 2.3, Remark 3.1, Thm 3.2 (sign conditions gamma>0). {CARDS}. Numbers in lab output checked against {S}/L05.txt lines 204-226.")
R("E3g-r2-L05-G3", "2.4 math / 2.6 cards (E3-c098..c105 and L05-side refs)", "cards.json E3-c098..c105 (L06 cards); L06.txt Prop 1.4, Rem 1.5, Props 2.1, 2.2", P,
  f"L06 cards and L06.html are byte-identical to 2d755599 (cards.json per-id diff in {S}/checks_r11.out section 1), but the L05 text they cite was re-read. Props 1.4, 2.1, 2.2 re-derived (L06.txt lines 33, 41-47). Card E3-c105 hypotheses (alpha, delta, lambda > 0, 0<p<1) match Prop 2.2.")
R("E3g-r2-L06-G4", "2.4 math / 2.3 grades (E3-c107..c113, c163)", "cards.json E3-c107, c108, c109..c113, c163; L06.txt Remarks 2.4, 2.5, 3.1, 3.2", P,
  f"Remark 2.5 numbers re-derived: combined 700-300 lambda (=100 at 2), separate 1000-600 lambda (=-200). Remark 3.2 lambda_R: 1 for the Example 2.3 gamble; sqrt(2)/2 = 0.7071 for p=1/3, g=1000, l=300 (recomputed). Grades match: T for algebra, None for definitions. {CARDS}.")
R("E3g-r2-L07-G5", "2.4 math / 2.6 cards (E3-c118..c126)", "cards.json E3-c118..c126 (E3-c121 changed, see E3g6-c121-unrounded); L07.txt Def 1.1..Remark 2.3", P,
  f"Example 1.4 derivative formula re-derived and checked numerically (l07_numbers_r11.out: finite difference vs (q+2p^2)/(2 sqrt(p) q (1+2q)^2) at six p). Prop 2.2 threshold 1/(1+2^-alpha) re-derived (0.66667 and 0.58578644). Remark 2.3 V(A)=45, V(B)=60 at identity weighting. {CARDS}.")
R("E3g-r2-L08-G7", "2.4 math / 2.3 grades (E3-c137..c143)", "cards.json E3-c137..c143; L08.txt Def 1.2, Prop 1.3, Ex 1.4, Thm 2.2, Prop 2.4", P,
  "Thm 2.2 proof and strict case re-read (L08.txt lines 47-49). Prop 2.4 proof: E_p u = u(w_no)+p(u(w_red)-u(w_no)), bracket > 0 by A2,A3, so minimum at P_0 (red) and P_90 (black) (L08.txt line 59). Ex 1.4: sum_{k=30}^{60} k = 1395, average 45/90 = 1/2 (recomputed). Grades T match.")
R("E3g-r2-L08-G9", "2.3 grades / 2.2 numbers (E3-c144, c164, c165, c166)", "cards.json E3-c144, c164, c165, c166; L08.txt Example 2.5, Model 2", P,
  f"Example 2.5 recomputed in {S}/l08_numbers_r11.out: known red 103125.0, known black 106451.6129 (= 3300000/31), ambiguous CE 100000 both colours; prospect wealth 99892.7670 (-2.071068 -> -1.072330 CU). Grades T (closed form on page).")
R("E3g-r2-refs-cross", "2.9 DAG / cross-lesson references used by the cards (re-run on new cards)", "cards.json E3-c184, E3-c185; L05.txt; checks_r11 section 2",
  P, f"Cross-references checked: 121 'Remark/Proposition/Theorem/Corollary/Definition/Example/Problem/Model/Observation/Section' mentions on slice cards ({S}/checks_r11.out section 2); only 'Problem E2' (c131, c187) is not a literal label in L07 (the heading reads 'E2 · ...'), accepted as the same problem. check_dag PASS.")
R("E3g-r2-registry", "2.1 citations: registry keys cited by L05-L08 cards", "cards.json E3-c134, c157, c158; references/references.json (generated_at and used_by of other keys changed)",
  P, f"verify_refs.py --unit E3 (live, {S}/verify_refs_unit_E3_live.out): 5 of 560 entries, 0 problems. verify_refs --offline: 560 entries, 0 problems. Keys cited by the slice (ellsberg1961risk, gilboa1989maxmin, kahneman1979prospect, epstein1989substitution) unchanged in content.")
R("E3g3-c135-terminology", "2.9 prose (E3-c135 back vs L07 Section 3)", "cards.json E3-c135; L07.html Section 3 (cumulative repair)", P,
  f"L07.txt Section 3 (line 208): cumulative repair 'not derived'; E3-c135 says the same and gives Tail_B(50)=Tail_A(50)=3/5, Tail_B(100)=3/5 > 3/10 (recomputed).")
R("E3g3-c091-gamma", "2.4-math (E3-c091: gamma != 0)", "cards.json E3-c091; L05.txt Remark 3.4, Theorem 3.2", P,
  "L05.txt Remark 3.4 (line 70): elasticity 1/gamma for gamma != 0; undefined at gamma = 0 (MRS independent of c1/c0). E3-c091 states the same with A1 to A4. Read in full.")
R("E3g3-c132-omega", "2.2 numbers (E3-c132 weighted value under omega_{1/2})", "cards.json E3-c132; L07.html Section 4 misconception 3", P,
  f"Re-derived: 0.01*100 weight term 8.34030105, 0.99*50 term 41.49247382, total 49.83277487 -> 49.8328; EV 50.5; overweight +7.34, underweight -8.01, net -0.67 ({S}/l07_numbers_r11.out). T grade is the closed-form computation the lesson states.")
R("E3g3-c097-trivia", "2.7 cards (E3-c097 removed; id list of the slice)", "cards.json id list for L05 and L06", P,
  "cards.json L05 ids: E3-c078..c091 (no c092), c093..c096, c169, c170, c184, c185; L06 ids c098..c113, c116, c117, c163 (no c097). Unit scan: 178 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs ({S}/checks_r11.out section 3).")
R("E3g3-basis-wording", "basis strings of the C cards (E3-c131 basis changed in round 10)", "cards.json E3-c131 basis",
  P, "E3-c131 basis now 'Lab 1, part C; Problem E2 (40-digit difference)'. Problem E2 (L07.txt, 'E2 · The gap between printed and unrounded values') prints 3.74355573 (40-digit difference), 42.86863274 and 39.12507700 (eight-decimal values). Each C-card basis in the slice names its lab, problem or registry record (card scan {S}/card_numbers_r11.out and checks_r11.out).")
R("E3g3-L06-proofs", "2.4-math (L06 proofs)", "L06.txt Props 1.4, 2.1, 2.2; Remarks 1.5, 2.4, 2.5, 3.1, 3.2", P,
  f"L06.html byte-identical to 2d755599 and re-read in full this round ({LESS}). Prop 1.4 derivatives v'=alpha x^(alpha-1), v''=alpha(alpha-1)x^(alpha-2) (x>0); v'=lambda delta (-x)^(delta-1), v''=lambda delta(1-delta)(-x)^(delta-2) (x<0): signs correct. Prop 2.2 threshold and slope -(1-p) l^delta re-derived.")
R("E3g3-L07-proofs", "2.4 math (L07 proofs)", "L07.html Def 1.2, Ex 1.4, Rem 1.3, Rem 1.6, Prop 2.2, P1", P,
  f"Ex 1.4: q=sqrt(p(1-p)), g=1+2q, q'=(1-2p)/(2q), g'=(1-2p)/q, numerator qg-2p(1-2p)=q+2p^2 re-derived (sympy-free, by hand and numerically in {S}/l07_numbers_r11.out). Prop 2.2 proof V(A)=omega(3/10)(50^a+100^a), V(B)=omega(3/5)100^a re-derived. Rem 1.6 sum 0.89103669 recomputed.")
R("E3g3-attribution", "2.1 / 2.9 title-only attributions (E3-c134, c157, c158)", "cards.json E3-c134, c157, c158; references/references.json", P,
  "Registry (checked by script, this round): ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' (Ellsberg, 1961) contains 'ambiguity'; gilboa1989maxmin 'Maxmin expected utility with non-unique prior' (Gilboa, Schmeidler, 1989) matches the card's name; kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk' (Kahneman, Tversky, 1979). Lessons state title-only use; no result is attributed (L07.txt line 33; L08.txt lines 28, 62).")
R("E3g3-delta-r3", "delta read (re-read on this pin, round 11)", f"git diff {PREV} {PIN} -- course/modules/E/E3/cards.json", P,
  "Per-id diff (checks_r11.out section 1): vs 47a36d8c changed c094, c096, c131, c169, c170, c184 (lesson-side text) and added c187 (L07). vs 2d755599 also added c185. All hunks read this round.")
R("E3g4-c082-hypotheses", "2.4-math / 2.6-cards (E3-c082 hypotheses)", "cards.json E3-c082; L05.txt Remark 1.5", P,
  f"E3-c082 says 'Under A1 to A4 at gamma = 2'; L05.txt line 45 example uses gamma = 2 (CE 8/5 and 12/5 recomputed: 1/E[1/c] = 1/(5/8), 1/(5/12)). Scope correct.")
R("E3g4-c085-hypotheses", "2.4-math / 2.6-cards (E3-c085 hypotheses)", "cards.json E3-c085; L05.txt Remark 2.3, Prop 2.2", P,
  "E3-c085 carries 'Under A1 to A4 for deterministic plans, and for gamma not equal to 1'; Remark 2.3 (L05.txt line 56) states the same. Correct.")
R("E3g4-c091-hypotheses", "2.4-math / 2.6-cards (E3-c091 hypotheses)", "cards.json E3-c091; L05.txt Remark 3.4", P,
  "E3-c091 carries 'Under A1 to A4' and 'gamma not 0'; Remark 3.4 (line 70) uses the same. Correct.")
R("E3g4-c108-hypotheses", "2.4-math / 2.6-cards (E3-c108 hypotheses)", "cards.json E3-c108; L06.txt Remark 2.5", P,
  "E3-c108 states 'With alpha = delta = 1 (Remark 2.5)'; Remark 2.5 (L06.txt line 53) uses alpha = delta = 1 for the two copies. Correct.")
R("E3g4-c130-argument", "2.4 math / 2.3 grades (E3-c130 'It can')", "cards.json E3-c130; L07.html Prop 2.2, Remark 1.6", P,
  "The claim 'it can' is established by Prop 2.2 with Remark 1.6 weights (0.57158177 > 0.39125077, recomputed). The grade problem on the same card (lab-printed values under a T grade) is recorded in row E3g11-c130-grade, not here.")
R("E3g4-c142-hypotheses", "2.4 math / 2.6 cards (E3-c142 hypotheses)", "cards.json E3-c142; L08.html Theorem 2.2", P,
  "E3-c142 carries A2 (u strictly increasing) and A3 (finite outcomes) via 'Under A1 to A3 of Theorem 2.2'. Matches L08.txt lines 43-47.")
R("E3g4-c155-notation", "2.4 notation (E3-c155 symbol)", "cards.json E3-c155; L08.html Remark 4.2 / Section 4", P,
  "E3-c155 uses nu for the exponential utility (u(w) = -exp(-nu w)); nu is not a registered symbol and is local to L08 R3. Registry has no conflicting use.")
R("E3g4-c096-context", "2.9 prose (E3-c096 names its tree)", "cards.json E3-c096; L05.txt Lab 1 predicted block", P,
  "E3-c096 front now names the tree ('c1 = 1 or 4 with probability 1/2 each'). L05.txt line 72 and lab output lines 213-215 (2.2500, 1.6000, 1.3720) match; recomputed CE1 = (0.5*1+0.5*2)^2 = 2.25, 8/5, (0.5*1+0.5/16)^(-1/2) = 1.3720.")
R("E3g4-c172-definition", "2.4 math / 2.3 (E3-c172 definition)", "cards.json E3-c172; L08.html Definition 1.2", P,
  "E3-c172: V_tau at tau=1 equals min E_P u(f) (L08.txt line 28). Definition matches.")
R("E3g-r2-hypotheses", "2.4 cards carry the hypotheses of the proposition they cite (round-10 FAIL on E3-c184)", "cards.json E3-c184; L05.txt line 50 (Prop 2.2: 'Assume A1 to A4 for deterministic plans')", P,
  "Round-10 FAIL resolved: E3-c184 now reads 'Under A1 to A4 for deterministic plans, at beta = 9/10, psi = 1/2 and (c0, c1) = (2, 4)'. psi = 1/2 satisfies A2 (psi > 0, psi != 1); gamma is any value != 1 (A3, and the lab uses gamma = 2). Other citing cards (E3-c084, E3-c085) carry the same hypothesis text. Re-checked against L05.txt lines 50-56 and lab lines 197-201.")
R("E3g4-lab-observations", "2.7 lab-versus-theorem pairs (E3-c184 is a lab-versus-Proposition 2.2 pair)", "cards.json E3-c184; L05.txt lines 197-198, 226",
  P, f"Round-10 FAIL: E3-c184 stated no beta. Now: 'Under A1 to A4 for deterministic plans, at beta = 9/10, psi = 1/2 and (c0, c1) = (2, 4), the closed form ... agrees with the MRS that Lab 1 computes by central differences'. Lab line 197 uses beta = 0.9, psi = 0.5, (c0,c1) = (2,4): analytic (1/9)*4 = 0.4444; line 226 prints True. Scope now matches the lab check.")
R("E3g5-c169-c170-basis", "2.2 numbers / 2.6 cards (E3-c169, c170 'the exact tree of Lab 1')", "cards.json E3-c169, E3-c170; L05.html Lab 1 predicted block", P,
  "E3-c169 and E3-c170 fronts now state the tree's gamma, psi, beta, c0 and c1 values in full (no 'same tree' reference). U = -49/80 and CE1 = 8/5 recomputed (E1 solution; lab lines 206, 209).")
R("E3g-dup-scan", "2.7 duplicates: full scan of all 178 unit cards", "cards.json (whole unit)", P,
  f"{S}/checks_r11.out section 3: 178 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs.")
R("E3g-r2-V-symbol", "3 notation: W (prospect value) collisions", "cards E3-c100, c104, c105, c107, c116; L06.html Definition 1.3", P,
  "W is the prospect value throughout L06 (Def 1.3, Prop 2.1, Prop 2.2, Remark 2.4) and in the cards; W is not a registered symbol and no other meaning appears in L05..L08.")
R("E3g-r2-L05-G2", "2.4 / 2.3 Corollary 3.3 and cards E3-c088..c091", "cards E3-c088..c091; L05.html line 147; L05.txt Cor 3.3", P,
  "L05.txt line 66 (Cor 3.3 line, the current text): 'Under the assumptions of Theorem 3.2, for any two plans X and Y with positive consumption, V0(X) >= V0(Y) iff U(X) >= U(Y)'. E3-c088 matches (strictly increasing function of U). Proof h'(u) = ((1-gamma)u)^(gamma/(1-gamma)) > 0 re-derived.")
R("E3g-r2-numbers", "2.2 numbers in prose and cards", "cards.json E3-c131, c184, c185; L05.txt lines 45, 209, 226; L07.txt lines 202, 253", P,
  f"Re-computed in {DERIV}: CE1 8/5 and 12/5; mean 5/2; lab lines 202-203 printed 42.8686, 39.1251, 4.8788, 3.9125; Problem E2 difference 3.74355573 (40-digit) and 3.74355574 (eight-decimal) -> 3.7436. All match.")
R("E3g-r2-lab-twins", "2.5 labs: run_labs, twins under python -I -W error, page code equals twin, expected block equals output", "tests/labs/E3/lab-E3-L05-1.py..L08-1.py; L05.html..L08.html code and output blocks",
  P, f"{TWIN}. run_labs ({S}/run_labs_L05.out..L08.out) passes. Expected-block check (run_labs) passes for L05 (0.5000/2.0000/0.2500, True lines), L07 (42.8686 ...).")
R("E3g-r2-coverage", "2.9 / 2.7 retrieval: every key result, definition and misconception of L05-L08 has a card", "cards.json L05 (22), L06 (19), L07 (19), L08 (28) = 88; the four lessons' key-results tables and misconception sections",
  P, f"Key-results rows mapped to cards: L05 rows 297-305 (c080, c081, c084, c086, c089, c093, c094, c095, c184, c185); L06 rows 248-255 (c101, c102, c104, c105, c106, c107, c108, c116/c117); L07 rows 273-278 (c121, c120, c123, c124, c125, c129, c122); L08 rows 382-390 (c138, c141, c143, c146, c148, c149..c152, c179, c153, c157, c158, c164, c165). Misconceptions covered (c081, c082, c112, c132, c146, c154, c142). {CARDS}.")
R("E3g-r2-grades", "2.3 grades: card grades against the lesson key-results grades (re-run on new cards)", "cards.json E3-c131 (C), E3-c184 (C), E3-c185 (C); L05.txt line 227", P,
  "Grades match the lesson's key-results tables: E3-c131 C, E3-c184 C, E3-c185 C, E3-c187 C. The lab-convention line (L05.txt line 227) and the key-results row 303-305 grades are C. Remaining grade mismatch on E3-c130 is recorded separately (E3g11-c130-grade).")
R("E3g-r2-scope-words", "2.4 / 2.9 scope words in the slice (re-run on changed and new cards)", "cards.json E3-c131, c184, c185, c187 (front and back); L05..L08 lesson hunks", P,
  "Scope words in changed hunks now carry their scope: L05 line 238 'at the one plan'; L05 key row 304 'at the one plan ... not a result for other plans, values of beta, or values of psi'; L07 Remark 2.3 'reverses the ranking at alpha = 1'; L08 misconception 3 'for every psi > 0 ...'. Each is backed by the output or the proof.")
R("E3g-r2-process-words", "1.3 / 1.4 banned and process phrases (re-run on changed cards)", "cards.json E3-c131, c184, c185, c187; lab hypothesis lines in L06 and L07 and L08", P,
  f"check_pages banned-string check PASS (L05..L08). 'Stated/Predicted before running' is the hypothesis line that BUILDER_RULES section 6 template mandates (BUILDER_RULES.md line 279: 'stated before running'), so it is not a process word in learner text. No banned phrase in changed cards (checks in {S}/checks_r11.out).")
R("E3g-r2-gates", "2.9 gates: check_pages (L05-L08 each), check_dag, check_projects, page_smoke, ruff, mypy, verify_refs", "ledgers/E3/scripts/E3-g-r10/*.out and E3-g-r11/*.out", P,
  GATES)
R("E3g-r2-delta", "delta of the slice since the previous pin (round-10 pin 47a36d8c to ccaeeaf)", f"git diff {PREV} {PIN} -- course/modules/E/E3 tests/labs/E3 notation references", P,
  f"Slice-subject delta read in full: L05.html (4 lines), L07.html (8), L08.html (4), cards.json (per-id: c094, c096, c131, c169, c170, c184 changed; c187 added), references.json (BK4/LX1 used_by; no E3 key changed), tests/labs/E3 (L05..L08 twins unchanged; L01 and project-3 twins outside the slice). Every hunk re-read this round.")
R("E3g3-L05-proofs", "2.4 mathematics: L05 Theorem 1.3, Corollary 1.4, Prop 2.2, Remark 3.1, Thm 3.2, Cor 3.3, Remark 3.4", "L05.txt (line 147 changed: Cor 3.3)", P,
  f"L05.html re-read in full ({LESS}). Thm 1.3(b) (sign of a in H(x)), Cor 1.4, Prop 2.2 chain rule, Remark 3.1 (theta=1 iff psi=1/gamma), Thm 3.2 (1-gamma)U = V0^(1-gamma), Cor 3.3 derivative positivity, Remark 3.4 exponents all re-derived by hand; M2 (3/2), M3 (theta=-2), E1 (80/49, -49/80), E2 (16/7, 160/71) recomputed.")
R("E3g3-L08-proofs", "2.4 mathematics: L08 Prop 1.3, Thm 2.2, Prop 2.4, Ex 2.5, Prop 3.2", "L08.html Model 4 and Remark 4.2 (lines 451, 468); L08.txt", P,
  f"L08.html re-read in full. Prop 3.2 proof (injectivity of x^(1/a) on positives, a != 0) re-derived. Remark 4.2 rewritten this round: decreasing E_p[1/w] in p (coefficient 1/w1-1/wL < 0) and affinity give the midpoint identity (re-derived). Ex 2.5 values recomputed in {S}/l08_numbers_r11.out.")
R("E3g3-c148-scope", "2.3 / 2.4 card E3-c148 scope (Remark 4.2 and Section 5 bullet)", "cards.json E3-c148; L08.html Remark 4.2, Section 5", P,
  "E3-c148 says 'With u(w) = -1/w ... for a two-outcome gamble E_P[1/w] is affine in p' and 'This is not a general property of alpha-MEU (Remark 4.2)'. Section 5 (L08.txt line 318) says the same. Scope correct.")
R("E3g3-page-smoke", "2.5 / 2.9 page_smoke for L05..L08 (re-run alone)", "tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08", P,
  f"{S}/page_smoke_L05-L08.out: each page PASS, 'page_smoke E3: PASS', exit 0 (zero console errors, all math rendered, no external requests, 360 px scroll check).")
R("E3g3-gates-projects-ruff", "2.6 project gates and ruff for the slice's twins", "tools/check_projects.py --unit E3; ruff", P,
  f"check_projects E3: PASS ({S}/check_projects.out); ruff check (tests/labs/E3, course/modules/E/E3, tools) exit 0 and ruff format --check: 11 files formatted ({S}/ruff.out).")
R("E3g3-notation-registry", "3 notation: registered symbols and macros", "notation/notation.json (unchanged since 2d755599); L05..L08 TeX", P,
  "Registered symbols T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q: none used in L05..L08 as a symbol (the '\\ast' in L06 is lambda^\\ast, a different symbol; the T tokens are grade cells). Registered macros \\E, \\Prob, \\R used with the registered meanings (TeX count of L05..L08 this round).")
R("E3g3-notation-collisions", "3 notation: local letters reused with another meaning inside the slice", "cards.json; L05.txt, L06.txt, L07.txt, L08.txt", P,
  "a (exponent 1-1/psi) in L05 and L08 with the same meaning; alpha (gains exponent) in L06, L07 and L08 with the same meaning, and L08 explicitly avoids alpha for tau; lambda (loss coefficient) in L06 and L08 with the same meaning; g is the prize in L06 and a local function in the L07 Example 1.4 proof and L08 Model 4, each within its own lesson. No collision inside a lesson.")
R("E3g4-c148-notation", "2.4 notation (card E3-c148: E_P[1/w])", "cards.json E3-c148; L08.html Remark 4.2", P,
  "E_P and 1/w use the registered \\E macro and ordinary notation; consistent with L08 Remark 4.2.")
R("E3g5-c148-utility", "2.4 hypotheses of card E3-c148 (utility for the affine identity)", "cards.json E3-c148; L08.html Remark 4.2, Model 1", P,
  "u(w) = -1/w stated in the card and in Remark 4.2; the affine identity needs only that u is -1/w (E[1/w] affine in p). Correct.")
R("E3g5-c151-utility", "2.4 hypotheses of card E3-c151 (maxmin value 99523.8095)", "cards.json E3-c151; L08.html Model 4", P,
  f"u(w)=-1/w stated; maxmin = 1/((1/3)/110000 + (2/3)/95000) = 99523.8095 (recomputed, {S}/l08_numbers_r11.out and Fractions). Worst prior 1/3 = 30/90 (smallest prior).")
R("E3g5-c152-utility", "2.4 hypotheses of card E3-c152 (risk premium 548.7805)", "cards.json E3-c152; L08.html Model 1 and Section 4", P,
  "102500 - 4180000/41 = 22500/41 = 548.780488 cents = 548.7805 (recomputed). Card states u(w) = -1/w and P(red)=1/2. Correct.")
R("E3g5-notation-PQ", "3 notation: plans P and Q against the registered \\mathbb{Q}", "L05.txt Corollary 3.3; L08 priors; notation/notation.json", P,
  "No \\mathbb{Q} in L05..L08 TeX (grep count 0 in each HTML); P denotes priors (L08, local) and plans are X, Y (L05 Cor 3.3). No collision with the registered Q.")
R("E3g-r2-L08-G8", "2.2 / 2.3 / 2.4 L08 numbers and grades for cards E3-c146, c148, c149, c150, c151, c152", "cards.json E3-c146, c148..c152; L08.html Section 4", P,
  f"Model 1 4180000/41; Model 2 5-sqrt(50); Model 4 99523.8095 and 1/(0.5 g(1/3)+0.5 g(2/3)) = 101951.2195; risk premium 548.7805; all recomputed ({S}/l08_numbers_r11.out). Grades T (closed form).")
R("E3g-r2-L07-G6", "L07 lab part C and cards E3-c127, c128, c131, c133, c135 (round-10 FAIL on c131)", "cards.json E3-c127, c128, c131, c133, c135; L07.txt lines 202-203", P,
  "c127 matches lab lines 202-203 (42.8686, 39.1251, 4.8788, 3.9125); c128 matches line 204 (10 of 10). c131 now matches Problem E2 (difference 3.74355573, eight-decimal roundings subtract to 3.74355574, both give 3.7436). c133 and c135 recomputed. Round-10 FAIL on c131 is resolved.")
R("E3g4-c131-unrounded", "2.2 numbers vs unrounded values: E3-c131 unrounded difference to four decimals", "cards.json E3-c131; L07.html Problem E2",
  P, f"Recomputed at 60 digits ({DERIV}): Gamma(A) = 150*omega(3/10) = 42.8686327356757356..., Gamma(B) = 100*omega(3/5) = 39.1250770026808434..., difference 3.7435557329948922... -> 3.7436. Printed 42.8686 - 39.1251 = 3.7435 (lab line 202). Answer 3.7436 correct.")
R("E3g6-psi-domain", "2.4 scope: 'for every psi != 1' carries psi > 0", "L08.html Section 5 bullet 2, misconception 3, quiz option; cards.json E3-c146", P,
  "L08.txt line 316 (Section 5), line 325 (misconception 3), quiz option (line 684 in html) and E3-c146 all read 'psi > 0 and psi not 1'. Round-6 FAIL stays fixed.")
R("E3g6-L07-ex14-unrounded", "2.2 numbers vs unrounded values: L07 Example 1.4 labels", "course/modules/E/E3/L07.html Example 1.4 paragraph", P,
  f"L07.txt lines 40-43: 8-decimal values are roundings of the 10-decimal values 0.2857908849, 0.3912507700, 0.3535533906 (recomputed in {S}/l07_numbers_r11.out). The 40-digit difference and its basis are stated; the 'computed outside the lab' wording is accepted as a recomputable number (E3g11-E2-outside-lab-note).")
R("E3g6-c121-unrounded", "2.2 numbers vs unrounded values: card E3-c121 back", "cards.json E3-c121", P,
  "E3-c121 back: 0.28579088, 0.39125077, 0.35355339 are the eight-decimal roundings of 0.2857908849, 0.3912507700, 0.3535533906 (recomputed). Correct.")
R("E3g6-c179", "2.7 card E3-c179: Epstein-Zin CE of the Section 4 gamble (Model 3)", "cards.json E3-c179; L08.html Model 3 and Proposition 3.2", P,
  "E3-c179 gives 101951.2195 cents at psi=1/2, beta=0.95, gamma=2 (Model 3, Prop 3.2). Matches L08.txt line 301 and lab line 273.")
R("E3g6-L07-intro-hunk", "2.9 prose: L07 introduction paragraph", "course/modules/E/E3/L07.html introduction (L07.txt line 20)", P,
  "Introduction unchanged since 2d755599 (not in the 47a36d8c..ccaeeaf hunks). It says the lesson gives weights that change the ranking, and that 'Expected utility with a nondecreasing utility cannot do this on a finite set of outcomes (Lesson 4, Theorem 1.5)'. Lesson 4 Theorem 1.5 (L04.txt lines 35-36, A1 finite support, line 336) confirms. check_pages word-count PASS.")
R("E3g6-L08-model4-hunk", "2.4 / 2.9 L08 Model 4 and Remark 4.2 hunks", "course/modules/E/E3/L08.html Model 4 and Remark 4.2", P,
  "Remark 4.2 now includes the monotonicity step (coefficient 1/w1-1/wL < 0) before the midpoint identity; re-derived: E_p[1/w] decreasing in p, so the extreme priors are the max and min and the average of their E[1/w] is E at the midpoint. Model 4 (L08.txt lines 303) matches.")
R("E3g6-L05-cor33-hunk", "2.4 prose: L05 Corollary 3.3 line changed", "course/modules/E/E3/L05.html line 147; L05.txt Corollary 3.3", P,
  "The Cor 3.3 line in L05.txt (line 66) matches E3-c088 and the proof (line 68). Re-read in full.")
R("E3g6-verify-refs", "2.1 citations: registry integrity (re-run offline and live for E3)", "tools/verify_refs.py --offline; --unit E3", P,
  f"{S}/verify_refs_offline.out: 560 entries, 0 problems. {S}/verify_refs_unit_E3_live.out: 5 of 560 entries, 0 problems, exit 0.")
R("E3g6-banned-phrases", "1.3 / 1.4 banned and process phrases; placeholders in the four lesson texts and slice cards", "L05..L08 text and slice cards; tools/check_pages.py banned-string check", P,
  f"check_pages L05..L08 PASS ({S}/check_pages_L0x.out). Card scan {S}/card_numbers_r11.out: no placeholder strings. 'Predicted/Stated before running' is the BUILDER_RULES section 6 hypothesis wording (see E3g-r2-process-words).")
R("E3g6-pytest", "2.5 relevant pytest over the lab and page tooling", "tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_curriculum.py, test_docs_figures.py, test_build_site.py, test_refs.py, tests/labs/E3", P,
  f"{S}/pytest_relevant.out: exit 0 (all selected tests pass; test_page_smoke.py not selected here, page_smoke run separately).")
R("E3g7-ex14-monotone", "2.4 math / 2.9 structure: omega_{1/2} called a weighting function (Def 1.1 requires nondecreasing)", "course/modules/E/E3/L07.html Example 1.4 title and derivative paragraph", P,
  "L07.txt line 35: 'a weighting function with eta = 1/2'; the derivative is positive on (0,1) (recomputed, l07_numbers_r11.out), continuous on [0,1], so nondecreasing (MVT). Correct.")
R("E3g7-card-xrefs", "2.9 structure: every 'Remark x.y', 'Proposition x.y', 'Example x.y', 'Model', 'Problem', section and misconception reference on the cards", "cards.json L05..L08 (88 cards)", P,
  f"{S}/checks_r11.out section 2: 121 mentions checked; 119 found in own lesson text; 2 'Problem E2' (c131, c187) refer to the problem labelled 'E2 · ...' in L07 (no literal 'Problem E2' label; accepted, see E3g11-problem-E2-label).")
R("E3g7-hours", "2.10 hours arithmetic: hub split against lesson study-hour labels", "course/modules/E/E3/index.html (data-hours-lessons 56, data-hours-project 14); L05..L08 headers", P,
  f"{S}/checks_r11.out section 5: hub 56 + 14; four lessons each '7 study hours' (8 lessons x 7 = 56 per hub text). Hub and headers unchanged.")
R("E3g8-delta", "delta 2d755599..ccaeeaf for every slice subject", f"git diff --stat {BASE} {PIN} -- course/modules/E/E3 tests/labs/E3 notation references", P,
  "L05, L07, L08 htmls and cards.json changed since 2d755599 (see E3g-r2-delta); L06.html and tests/labs/E3 L05..L08 twins unchanged; notation unchanged.")
R("E3g8-L07-ex14-derivative", "Mathematics of the new derivative proof in Example 1.4", "course/modules/E/E3/L07.html lines 83-92", P,
  f"Derivative formula (q+2p^2)/(2 sqrt(p) q (1+2q)^2) matches finite differences at p = 0.01, 0.1, 0.3, 0.5, 0.7, 0.99 ({S}/l07_numbers_r11.out, to about 8 decimals of finite-difference error). Steps re-derived by hand (qg - 2p(1-2p) = q + 2p^2 using q^2 = p - p^2).")
R("E3g8-obs15", "Observation 1.5 wording and the printed grid facts", "course/modules/E/E3/L07.html Observation 1.5; L07.txt lines 42-43", P,
  f"Lab lines 194-196: nondecreasing True, in [0,1] True, 1 sign change, last point with omega > p = 0.278. Recomputed: omega(0.278)-0.278 = +8.5e-5, omega(0.279)-0.279 = -5.6e-4, crossing ~0.27813 ({S}/l07_numbers_r11.out). Correct.")
R("E3g8-L07-numbers", "Numbers in the new and changed L07 prose", "course/modules/E/E3/L07.html Example 1.4 values, Remark 1.6, Proposition 2.2, section 4, section 5 problems", P,
  f"All recomputed: 0.31945492, 0.57158177, 0.89103669 (Remark 1.6); 0.73045450 (8dp of 0.7304544982) and 0.73045449 (quotient of printed values, recomputed 0.7304544858); thresholds 2/3 and 0.58578644; M1 1/(2+sqrt3)=0.26794919, E1 crossing in (0.278, 0.279), E2 values, E3 eta=1 gap 3.125625e-1 at p=0.862 ({S}/l07_eta1_r11.out).")
R("E3g8-L08-interp-q10", "Wording change 'expectation of 1/w is affine in p' in the Section 4 interpretation paragraph and quiz option", "course/modules/E/E3/L08.html line 427 and quiz option L08q10", P,
  "L08.txt Section 4 interpretation and quiz item 10 (correct option: 'because the prior set is symmetric about 1/2 and the expectation of 1/w is affine in p (Remark 4.2)'). Symmetry holds: {30,...,60} is symmetric about 45/90 (30+60=90). Correct.")
R("E3g8-c131-basis", "E3-c131 back and basis (round-10 FAIL: 'the 40-digit values are Problem E2')", "cards.json E3-c131 back and basis; L07.html Problem E2", P,
  "Round-10 FAIL resolved: E3-c131 back now says 'The unrounded values differ by 3.74355573 ... (Problem E2)' and Problem E2 (L07.txt lines 251-253) prints the 40-digit DIFFERENCE 3.74355573 and the eight-decimal values 42.86863274, 39.12507700 (not the 40-digit values). Basis 'Lab 1, part C; Problem E2 (40-digit difference)'. Recomputed in l07_numbers_r11.out.")
R("E3g8-c144-c182", "E3-c144 (red CE) and E3-c182 (black CE) against Example 2.5", "cards.json E3-c144, E3-c182; L08.html Example 2.5", P,
  f"Example 2.5 text: 103125 cents and 106451.6129 cents; recomputed exactly (3300000/31 = 106451.6129...). Cards agree.")
R("E3g8-L08-numbers", "Numbers in L08 Section 4 table, Remark 4.2, Problems M1 to M3, E1 to E3, R2, quiz", "course/modules/E/E3/L08.html", P,
  f"Section 4 table (101951.2195/101951/1951.2195; 99892.7670/99893/-107.2330; 99523.8095/99524/-476.1905); M1 8360000/85 = 98352.94; M2 105822.78 at 3/4; E1 3125 cents = 31.25 CU; E3 22500/41 = 548.78 cents = 5.4878 CU; R2 103125 and 106451.6129; quiz 101951.22, 99523.81, 99892.77 (all recomputed, {S}/l08_numbers_r11.out).")
R("E3g8-card-numbers", "every number on a slice card appears in its lesson; no duplicate cards (re-run on 88 slice cards)", "cards.json L05..L08 (88); L05..L08 text", P,
  f"{S}/card_numbers_r11.out: cards checked 88; numbers not found in own lesson text 0; duplicate fronts 0; duplicate ids 0.")
R("E3g8-notation-local", "Local symbols q and g in Example 1.4 and g(p) in Model 4 against notation/notation.json", "course/modules/E/E3/L07.html Example 1.4; L08.html Model 4", P,
  "Local (no registry entry, notation.json 'about': letters conventionally local are defined where used). q = sqrt(p(1-p)) and g = 1+2q are defined in the L07 proof; g(p) = E_p[1/w] is defined in L08 Model 4. No registered symbol reused.")
R("E3g8-gates", "Gate commands re-run on the current pin", "course/modules/E/E3/L07.html, L08.html, cards.json; tools/*", P,
  GATES)
R("E3g8-lab-twins-run", "lab twins under python -I -W error; page code equals twin; expected block equals output (L07, L08)", "tests/labs/E3/lab-E3-L07-1.py, lab-E3-L08-1.py; L07.html, L08.html", P,
  TWIN)
R("E3g8-scope-process", "Scope words and process words in the changed hunks", "course/modules/E/E3/L07.html Example 1.4 and Observation 1.5; L08.html Def 1.2 and Remark 4.2", P,
  "Changed hunks: 'states no weighting function ... which is not read here' (L07 line 33), 'at that value of alpha' (L07 Remark 2.3), 'states no axiom or result from that paper' (L08 Def 1.2), Remark 4.2 monotonicity step. No banned scope or process words introduced (check_pages PASS).")

# ---- rows new in round 11 ----
R("E3g11-c130-grade", "2.3 grades / BUILDER_RULES 7 (card grade T carries lab-printed values)", "cards.json E3-c130 (grade T, back 'At alpha = 1 the values are 42.8686 for A and 39.1251 for B (Lab 1, part C; section 4, first misconception)'); L07.txt lines 202, 251-253",
  "FAIL",
  "Per BLUEPRINT section 3 grade table and the lesson's own convention (key-results row 254: lab-printed values are C; L07 Key results), the numbers 42.8686 and 39.1251 are read off Lab 1 part C (L07.txt line 202, the only printed source) and must carry grade C. The card is graded T and has no basis field (BUILDER_RULES section 7). The locator 'section 4, first misconception' does not contain 42.8686 or 39.1251 (L07.txt lines 211-212 cite only the Remark 1.6 weights 0.57158177 and 0.39125077). The card's argument ('It can') is correct on its own (Prop 2.2).",
  "Either (a) keep grade T and delete the sentence 'At alpha = 1 the values are 42.8686 for A and 39.1251 for B (Lab 1, part C; section 4, first misconception).' so the back reads 'It can. The weights respect the order of single probabilities, not of lotteries. Under omega_{1/2} (Proposition 2.2), A's two positive outcomes carry total weight 0.57158177, more than B's weight 0.39125077 (Remark 1.6).'; or (b) keep the sentence and grade the card C with basis 'Lab 1, part C; section 4, first misconception' corrected to name the lab for 42.8686 and 39.1251.")
R("E3g11-c187-new", "2.3 / 2.7 card E3-c187 (new in round 10; re-checked)", "cards.json E3-c187; L07.txt lines 202, 251-253", P,
  "Printed difference 42.8686 - 39.1251 = 3.7435 (recomputed); unrounded difference 3.74355573 rounds to 3.7436 (l07_numbers_r11.out). Each printed value rounded separately explains the last digit (errors -0.0000327 and +0.0000230). Grade C with basis 'Lab 1, part C; Problem E2' matches the lesson.")
R("E3g11-changed-cards-c094-c096-c169-c170", "2.6 / 2.7 changed fronts and backs (E3-c094, c096, c169, c170)", "cards.json E3-c094, c096, c169, c170; L05.txt lines 197-226", P,
  "c094 back: 0.5000, 2.0000, 0.2500 from finite differences at (c0,c1)=(2,4), beta=9/10, gamma=2 (lab lines 223-225, eis_numeric uses gamma = 2.0, c1 in [0.999,1.001]*4). c096 values 2.2500, 1.6000, 1.3720 match lab lines 213-215 (recomputed). c169 U = -49/80 and c170 CE1 = 8/5 match lines 206, 209 and E1. All front facts now state their parameters.")
R("E3g11-L05-hunks", "2.4 / 2.9 L05 hunks: misconception 2 (line 238) and key-results row 304", "course/modules/E/E3/L05.html lines 374, 501; L05.txt lines 238, 304", P,
  "Line 238 'at the one plan (c0, c1) = (2, 4)' matches lab lines 194-196 (gamma = 2 hard-coded; c1 = 4). Row 304 scopes the EIS and MRS claims to beta = 9/10, gamma = 2, (c0,c1)=(2,4) and psi in {1/2, 2, 1/4}. Both are the lab's checks (run_labs PASS).")
R("E3g11-L07-hunks", "2.4 / 2.9 L07 hunks: Remark 2.3 (line 66), Example 1.4 (lines 77, 83-92), E2 solution (line 253), R3 solution (line 270)", "course/modules/E/E3/L07.html lines 77, 137, 410, 442; L07.txt", P,
  f"Remark 2.3: the reversal at alpha = 1 (checked: Gamma(A)=42.87 > Gamma(B)=39.13 with weights, 45 < 60 with identity). E2: 40-digit values and difference recomputed (l07_numbers_r11.out). R3: the two prediction sentences are the non-cumulative and dominance-respecting predictions, as in Prop 2.2 and Thm 1.5 of L04 (L04.txt lines 35-36). No number changed.")
R("E3g11-L08-hunks", "2.4 / 2.9 L08 hunks: Def 1.2 (line 26) and Remark 4.2 (line 312)", "course/modules/E/E3/L08.html lines 64-66, 465-468; L08.txt", P,
  "Def 1.2 now says the lesson 'states no axiom or result from that paper' (Gilboa-Schmeidler title only, registry gilboa1989maxmin). Remark 4.2 monotonicity step and midpoint identity re-derived (coefficient 1/w1 - 1/wL < 0 with w1 = 110000 > wL = 95000).")
R("E3g11-L04-theorem", "2.9 DAG / 2.4: Lesson 4 Theorem 1.5 cited by L07 and card E3-c129", "course/modules/E/E3/L04.html Theorem 1.5 (A1 finite support); L07.html lines 20, 47; cards.json E3-c129", P,
  f"L04.txt lines 35-36: F_X <= F_Y for every real t iff E u(X) >= E u(Y) for every nondecreasing u on S, under A1 (finite support; L04.txt line 336). L07's use (B FOSD A, so E u(B) >= E u(A)) is the 'only if' direction with X=B, Y=A. Correct. check_dag PASS.")
R("E3g11-quiz-keys", "2.4 / 2.9 quiz: correct options against explanations (L05..L08, 28 questions with keys)", "course/modules/E/E3/L05.html..L08.html quiz blocks", P,
  f"Correct-option labels extracted ({S}/checks_r11.out section 4) and matched to each explanation: e.g. L06 item 7 'At lambda = 1' (Remark 3.2), L07 item 5 'above 2/3' (Prop 2.2), L08 item 3 '1/3' (Model 4), L08 item 10 'symmetric about 1/2 and affine' (Remark 4.2). No wrong key found.")
R("E3g11-numbers-recompute", "2.2 numbers: independent recomputation of all slice numbers (Decimal 60 digits, Fractions, floats)", f"{S}/l07_numbers_r11.py, l07_eta1_r11.py, l08_numbers_r11.py", P,
  f"Outputs {S}/l07_numbers_r11.out, l07_eta1_r11.out, l08_numbers_r11.out. Every number in the Remark, Example, Problem, quiz and key-results text of L05..L08 that I checked agrees to the stated digits (the card numbers are string-matched in card_numbers_r11.out).")
R("E3g11-registry-titles", "2.1 attribution: titles, authors and years of the registry keys cited in the slice", "references/references.json entries ellsberg1961risk, gilboa1989maxmin, kahneman1979prospect, epstein1989substitution", P,
  f"Read from the registry ({S}/l08_numbers_r11.out tail): 'Risk, Ambiguity, and the Savage Axioms' (Ellsberg, 1961); 'Maxmin expected utility with non-unique prior' (Gilboa, Schmeidler, 1989); 'Prospect Theory: An Analysis of Decision under Risk' (Kahneman, Tversky, 1979); 'Substitution, Risk Aversion, and the Temporal Behavior of Consumption and Asset Returns: A Theoretical Framework' (Epstein, Zin, 1989). Lesson claims about these are title-only; the papers were not read, and no result is attributed.")
R("E3g11-unit-dup-scan", "2.7 full-unit duplicate scan", f"{S}/checks_r11.py section 3", P,
  f"{S}/checks_r11.out: 178 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs.")
R("E3g11-hub-hours", "2.10 hours: hub split against lesson hours", "course/modules/E/E3/index.html; L05..L08 headers", P,
  f"{S}/checks_r11.out section 5: data-hours-lessons 56 and data-hours-project 14; L05..L08 headers say 7 study hours each (4 x 7 = 28 of the hub's 56 = 8 x 7); L01..L04 headers are outside this slice.")
R("E3g11-problem-E2-label", "2.9 cross-reference label form: 'Problem E2' on cards E3-c131, E3-c187", "cards.json E3-c131, E3-c187; L07.html problem E2 heading", P,
  "Labels in L07 are 'E2 · The gap between printed and unrounded values' under Problem set. Cards call it 'Problem E2' (as L05 and L08 cards call their problems). Same problem; no content issue.")
R("E3g11-E2-outside-lab-note", "2.2 (c) derived on the page: L07 E2 solution says the 40-digit values were 'computed outside the lab'", "course/modules/E/E3/L07.html Problem E2 solution (L07.txt line 253)", P,
  f"The page does not show the 60-digit evaluation, so the 40-digit difference 3.74355573 is not derivable from the page text alone. It is recomputable from the shown closed form (omega(3/10) and omega(3/5), Example 1.4), and the verifier recomputed it ({S}/l07_numbers_r11.out, 3.7435557329948922...). The 4-decimal answer 3.7436 is derivable from the page's own eight-decimal values. Accepted as (c); advisory: state that the 40-digit values come from the closed form evaluated at 40 digits.")
R("E3g11-lab-run", "2.5 labs: run_labs per lesson, twins alone under python -I -W error (this round)", "tests/labs/E3/lab-E3-L05-1.py..L08-1.py", P,
  TWIN)

# ---- sanity on ids: round-10 ids must all be present ----
r10 = [r["id"] for r in json.load(open("/Users/billyribeiro/.fanout/frags/D-E3-g.round10.json", encoding="utf-8"))["rows"]]
have = {r["id"] for r in rows}
missing = [i for i in r10 if i not in have]
assert not missing, f"round-10 ids not carried: {missing}"

frag = {
    "unit": "E3",
    "slice": "g",
    "round": 11,
    "verifier": "Haiku 5.5 independent verifier, E3-g round 11 (did not build E3)",
    "pin": PIN,
    "base": f"{PREV} (round-10 pin; delta also read from {BASE})",
    "checkout": ROOT,
    "scratch": f"{ROOT}/{S}",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round-10 pin 47a36d8c to ccaeeaf: lessons L05, L07, L08 htmls changed (text re-read in full this round), cards.json changed (c094, c096, c131, c169, c170, c184, c187 added), references.json changed (no E3 key content changed). L06 html and all four lab twins are byte-identical since 2d755599.",
        "Round-9 fragment absent; baseline is the round-8 pin 2d755599 (all 85 round-10 rows re-verified or carried with their subjects re-read).",
        "Round-10 FAIL rows E3g3-basis-wording, E3g4-lab-observations, E3g-r2-hypotheses, E3g-r2-L07-G6 and E3g8-c131-basis now PASS: the card text and basis were corrected and recomputed.",
        "New FAIL in round 11: E3g11-c130-grade (grade T on a card carrying lab-printed values).",
        "Mutants: none. This slice is lessons and retrieval cards, not a project grader; lab twins are demonstrations (VERIFIER rulings), so no mutants are required.",
        "Not a row: the L07 E2 solution's 'computed outside the lab' wording is advisory only (E3g11-E2-outside-lab-note).",
        "Not checked: Epstein-Zin (1989), Kahneman-Tversky (1979), Gilboa-Schmeidler (1989), Ellsberg (1961) full texts (registry title-only; no result attributed). Full repository gate (tests/ outside the relevant subset, render_curriculum, build_site --check, fetch_data --check, run_graders, mutate_graders) not run: not in this slice's scope; L05-L08 pages and twins were gated individually.",
        "Round-10 hours and DAG rows re-checked on the current pin (hub index.html unchanged since 2d755599).",
    ],
}
frag["summary"] = {
    "rows": len(rows),
    "pass": sum(1 for r in rows if r["status"] == "PASS"),
    "fail": sum(1 for r in rows if r["status"] == "FAIL"),
    "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    "carried_from_round_10_ids": len(r10),
    "mutants": 0,
    "mutants_killed": 0,
}
out = f"{ROOT}/ledgers/E3/E3-g.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, "rows", len(rows), "verdict", frag["verdict"])
