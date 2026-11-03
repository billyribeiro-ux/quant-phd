"""Build the round-4 fragment ledgers/E3/E3-g.json for E3 slice g (cards of L05-L08). Stdlib only.

Usage: python -I ledgers/E3/scripts/E3-g-r4/build_fragment_g4.py   (run from the checkout root)
Every evidence string names the script or command output under ledgers/E3/scripts/E3-g-r4/ or the file and line read.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E3/scripts/E3-g-r4/"

rows = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# ---- rows carried by id from round 3, re-verified on pin 4eb6788 ----
row("E3g-dup-scan", "2.7-duplicates (full scan of the L05-L08 cards)",
    "course/modules/E/E3/cards.json E3-c176 (line 1175); duplicates E3-c153 (line 1016), E3-c146 (line 968), E3-c149 (line 988)",
    "FAIL",
    f"{S}dup_scan_g4.out: 0 exact duplicate fronts and 0 exact duplicate backs over 169 cards; 17 near pairs listed, all distinct facts "
    "except E3-c176. Round 4 re-targeted c176 to the bisection method, but its back still states the value 101951.2195 cents at "
    "psi = 1/2, beta = 0.95, gamma = 2, P(red) = 1/2 (the Model 3 point). That value is the psi = 1/2, beta = 0.95 pair of E3-c153 "
    "(101951.219512, Lab 1 part B, lab output in L08 text line 0316) and the last-date fact of E3-c146 (Proposition 3.2); "
    "the 101951.2195 figure is also E3-c149's expected-utility CE. The bisection detail is Model 3's numerical procedure "
    "(L08 text lines 0087-0088, 0339), which is not a T-grade result.",
    "Delete E3-c176 (every fact it states is on E3-c146, E3-c149 or E3-c153), or re-target it at a fact no card states.")

row("E3g-notation-c138", "2.4-notation (E3-c138 uses tau, not alpha)",
    "course/modules/E/E3/cards.json E3-c138 (line 933)", "PASS",
    "L08 text line 0020 (Definition 1.2): 'The weight is written tau, not alpha'; E3-c138 front 'for every tau' matches "
    "Proposition 1.3 (A2: tau in [0, 1]), re-read on this pin.")

row("E3g-grade-c142", "2.3-grades (E3-c142 strict case of Theorem 2.2)",
    "course/modules/E/E3/cards.json E3-c142 (line 941); L08 text line 0041", "PASS",
    "Theorem 2.2 strict case in L08 text line 0041 (non-equal E_{P_i} u(f) force a strict inequality); grade T is correct. "
    "The hypothesis omission on the same card is a separate row (E3g4-c142-hypotheses).")

row("E3g-grade-c090", "2.3-grades (E3-c090 is T and carries no lab number)",
    "course/modules/E/E3/cards.json E3-c090; L05 text lines 0060 and 0064", "PASS",
    "Back states Corollary 3.3 (A1-A4) and Remark 3.4 only; the lab-read pair is E3-c095 (grade C). Re-read on this pin.")

row("E3g-r2-V-symbol", "2.2-numbers / notation (L06 cards use W for the prospect value)",
    "course/modules/E/E3/cards.json E3-c100, E3-c104, E3-c105, E3-c107, E3-c116", "PASS",
    "L06 text line 0023 (Definition 1.3) defines W := sum p_i v(x_i); the L06 cards use W with that meaning. "
    "Round-2 bare-V fault is absent on this pin.")

row("E3g-r2-c145-V1", "2.9-structure / card cites its lesson (E3-c145)",
    "course/modules/E/E3/cards.json E3-c145 (line 968 area)", "PASS",
    "Back cites Definition 3.1 and a = 1 - 1/psi; no terminal V1 on L08 (L08 text line 0058).")

row("E3g-r2-L05-G1", "2.4-math / 2.6-cards (E3-c078, c079, c080, c081, c083, c084, c086, c087)",
    "cards.json L05 cards; L05 text lines 0022-0059, 0064", "PASS",
    f"Read each card against Definition 1.1, Remark 1.2, Theorem 1.3, Corollary 1.4, Definition 2.1, Proposition 2.2, Remark 3.1, "
    f"Theorem 3.2 (L05 text). Numbers: {S}numbers_g4.out (CE1 = 8/5 and 12/5, CE1 at gamma = 0.5 and 3, V0 = 80/49, "
    "U = -49/80, V0 = 160/71 at p = 1/4). Hypothesis gaps on c082, c085, c091 are separate rows.")

row("E3g-r2-L05-G2", "2.4-math / 2.3-grades (E3-c088 to E3-c091, Remark 3.4)",
    "course/modules/E/E3/cards.json E3-c088 (line 587), E3-c089 (594), E3-c090 (601), E3-c091 (608)", "FAIL",
    "E3-c088, c089, c090 verified (A1-A4 stated; Corollary 3.3 and Remark 3.4 re-derived). The round-3 gamma != 0 fault on E3-c091 "
    "is fixed (back now reads 'for gamma not 0'), but E3-c091 still omits the standing assumptions A1-A4 that Proposition 2.2 "
    "needs for 'Epstein-Zin gives psi'. See E3g4-c091-hypotheses.",
    "See E3g4-c091-hypotheses.")

row("E3g-r2-L05-G3", "2.4-math / 2.6-cards (L06 definitions and L05 Remark 1.5)",
    "cards.json E3-c098 to E3-c105; L06 text lines 0016-0045; L05 text line 0039", "PASS",
    f"Proposition 1.4 derivatives, Proposition 2.1/2.2 thresholds and Remark 1.5 ratio re-derived in {S}numbers_g4.out "
    "(M1 threshold 3/2 at p = 1/3, g = 900, l = 300; sign-change thresholds 5/3, sqrt(5/3) = 1.290994). Hypotheses on E3-c101 "
    "(alpha, delta in (0,1), lambda > 0) and E3-c104 (alpha = delta = 1) are present.")

row("E3g-r2-L06-G4", "2.4-math / 2.3-grades (E3-c107 to E3-c113, E3-c163)",
    "cards.json E3-c107, c108 (line 714), c109 to c113, c163; L06 text lines 0044-0047, 0195-0202",
    "FAIL",
    "E3-c107, c109, c110, c111, c112, c113, c163 verified (Remarks 2.4, 3.1, 3.2 re-derived: lambda_R = sqrt(2)/2 = 0.70710678 "
    "at p = 1/3, g = 1000, l = 300, alpha = delta = 1/2; 1/2 * 800^alpha (1 - lambda)). E3-c108 states the combined value 700 - 300 lambda "
    "and the separate value 1000 - 600 lambda, which hold only with alpha = delta = 1 (L06 text line 0047: 'with alpha = delta = 1'); "
    "the card omits that hypothesis. See E3g4-c108-hypotheses.",
    "See E3g4-c108-hypotheses.")

row("E3g-r2-L07-G5", "2.4-math / 2.6-cards (E3-c118 to E3-c126)",
    "cards.json E3-c118 to E3-c126; L07 text lines 0017-0060, 0062-0063", "PASS",
    f"{S}numbers_g4.out: omega(3/10) = 0.28579088, omega(3/5) = 0.39125077, omega(1/2) = 0.35355339, "
    "2*omega(3/10) = 0.57158177, omega(2/5) + 2*omega(3/10) = 0.89103669, ratio 0.7304544982 -> 0.73045450, thresholds 2/3 and "
    "0.58578644, identity values 45 and 60. Proposition 2.2 algebra re-read (L07 text line 0059). E3-c130 separately fails (E3g4-c130-argument).")

row("E3g-r2-L07-G6", "2.3-grades / 2.5-labs (E3-c127, c128, c131, c133, c135)",
    "cards.json E3-c127 (line 833), c128 (line 841), c131 (863), c133 (878), c135 (895); L07 text lines 0221-0240, 0297-0301",
    "PASS",
    f"Lab 1 part C and part D output (L07 text lines 0237-0239) reproduced in {S}numbers_g4.out (Gamma(A) 42.86863274, "
    "Gamma(B) 39.12507700, alpha = 1/2 values 4.87875558 and 3.91250770; 10 of 10 utilities). E3-c131: 40-digit difference "
    "3.74355573299 rounds to 3.7436; the 8-digit values the card names subtract to 3.74355574, which rounds to the same 3.7436. "
    "Card labels the 8-digit values 'unrounded', the same convention as L07 text line 0027. E3-c133 and E3-c135 re-derived (Problem R1, R2).")

row("E3g-r2-L08-G7", "2.4-math / 2.3-grades (E3-c137 to E3-c143)",
    "cards.json E3-c137 to E3-c143; L08 text lines 0017-0043", "FAIL",
    "E3-c137, c138, c139, c140, c141, c143 verified (Definition 1.2, Proposition 1.3, Example 1.4: sum_{k=30}^{60} k/90 / 31 = 1/2). "
    "E3-c142 states the strict-case result without Theorem 2.2's hypotheses A1-A3 (strictly increasing u is A2). See E3g4-c142-hypotheses.",
    "See E3g4-c142-hypotheses.")

row("E3g-r2-L08-G8", "2.4-math / 2.3-grades (E3-c146, c148 to c153, c176)",
    "cards.json E3-c146 (line 968), c148 (981), c149 (988), c150, c151, c152, c153 (1016), c176 (1175); L08 text lines 0058-0066, 0333-0375",
    "FAIL",
    f"E3-c146 (Proposition 3.2 hypotheses A1-A5 stated), c149, c150, c151, c152 (548.7805 cents, 5.4878 CU) and c153 "
    f"(Lab 1 part B) verified; numbers in {S}numbers_g4.out (EU CE 101951.21951219512; maxmin 99523.80952380953; "
    "prospect 5 - sqrt(50) = -2.071067811865475; wealth equivalent 99892.76695296636881). E3-c148 uses E_P[1/W] for final wealth, "
    "and W is the L06 prospect-value symbol (See E3g4-c148-notation). E3-c176 duplicates the Model 3 value (See E3g-dup-scan).",
    "See E3g4-c148-notation and E3g-dup-scan.")

row("E3g-r2-L08-G9", "2.3-grades / 2.2-numbers (E3-c144, c164, c165, c166)",
    "cards.json E3-c144 (line 955), c164 (line 1092), c165 (1099), c166 (1106); L08 text lines 0053-0054, 0336-0337", "PASS",
    f"{S}numbers_g4.out: known urn CE red 103125.0, black 106451.6129; worst-prior CE 100000 for both colours; "
    "prospect CE of the change -107.2330 cents and wealth equivalent 99892.7670 cents. Example 2.5 argument (any strictly increasing u) re-read.")

row("E3g-r2-numbers", "2.2-numbers (every number on the L05-L08 cards)",
    f"{S}numbers_g4.py -> {S}numbers_g4.out", "PASS",
    "Re-derived with fractions and 40-digit Decimal: every card number (listed in the numbers_g4.out printout) agrees with its "
    "printed digits, including 101951.2195, 99523.8095, 98352.94, 105822.78, 548.7805, 5.4878, 49.8328, 0.73045450, 0.89103669, "
    "3.7436, 1.2910, -8.6835, 2.2500, 1.6000, 1.3720, 80/49, -49/80, 8/5, 160/71, 103125, 106451.6129, 99892.7670.")

row("E3g-r2-lab-twins", "2.5-labs (L05-L08 labs and their pages)",
    f"tests/labs/E3/lab-E3-L05-1.py .. lab-E3-L08-1.py; course/modules/E/E3/L05.html .. L08.html", "PASS",
    f"{S}run_labs_E3_r4.out: 'run_labs E3: PASS (11/11)', exit 0. {S}ruff_twins_L05-L08_r4.out: ruff check and format pass on "
    f"the four twins. {S}mypy_L08_twin_r4.out: mypy --no-incremental passes on lab-E3-L08-1.py. The printed lab output "
    "(L05 text lines 0234-0256, L06 0175-0192, L07 0221-0239, L08 0306-0330) matches the numbers the cards quote.")

row("E3g-r2-refs-cross", "2.9-DAG / cross-lesson references used by the cards",
    "cards.json E3-c081 (section 5), E3-c112 (section 5), E3-c146 (section 6), E3-c154 (section 6), E3-c129 (Lesson 4 Theorem 1.5)",
    "PASS",
    "L05 text line 0269 (section 5 third misconception); L06 text line 0207 (section 5 first misconception); L08 text lines 0382, 0386 "
    "(section 6 first and third misconceptions); L04.html lines 89-91 (Theorem 1.5: F_X <= F_Y everywhere iff E u(X) >= E u(Y) for every "
    "nondecreasing u on S; E3-c129 applies it with Y = B, X = A, which matches the card's direction).")

row("E3g-r2-registry", "2.1-citations (registry keys cited by L05-L08 cards)",
    "cards.json E3-c134 (kahneman1979prospect), E3-c157 (ellsberg1961risk), E3-c158 (gilboa1989maxmin); references/references.json",
    "PASS",
    "references/references.json entries: ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms' (1961, contains 'Ambiguity'); "
    "gilboa1989maxmin 'Maxmin expected utility with non-unique prior' (1989); kahneman1979prospect 'Prospect Theory: An Analysis of "
    "Decision under Risk' (1979); all status 'verified'. Offline integrity: "
    f"{S}verify_refs_offline_r4.out -> '560 entries, 0 problems'. Live verify_refs not run (no reference changed; network not used).")

row("E3g-r2-coverage", "2.7-cards coverage of lesson results",
    "cards.json L05-L08 vs the Key results tables in L05 text lines 0329-0355, L06 0270-0291, L07 0310-0325, L08 0446-0472",
    "PASS",
    "Each graded key result has a card: L05 Theorem 1.3 (E3-c080), Corollary 1.4 (c081), Proposition 2.2 (c084), Remark 3.1 (c086), "
    "Theorem 3.2 (c087), Corollary 3.3 (c088), Remark 3.4 (c089); L06 Proposition 1.4 (c101), Remark 1.5 (c102), Propositions 2.1 and 2.2 "
    "(c104, c105), Example 2.3 (c106), Remark 2.4 (c107), Remark 2.5 (c108); L07 Remark 1.3 (c120), Example 1.4 (c121), "
    "Remark 1.6 (c123), Proposition 2.2 (c125), Theorem 1.5 of L04 (c129); L08 Proposition 1.3 (c138), Theorem 2.2 (c141), "
    "Proposition 2.4 (c143), Proposition 3.2 (c146), Remark 4.2 (c148), Example 2.5 (c144, c164, c165).")

row("E3g-r2-grades", "2.3-grades (grade field of the 84 slice cards)",
    "cards.json L05-L08 (84 cards: L05 20, L06 19, L07 18, L08 27)", "PASS",
    "Counted with a script: 50 T, 17 C (each with basis or cite), 17 ungraded definitions. Each T card is a theorem, a remark, "
    "an example or a closed-form computation on the page; each C card names a lab part or a registry record (title only).")

row("E3g-r2-hypotheses", "2.4-math / 2.6-cards (carry the proposition's hypotheses on every T card)",
    "cards.json E3-c082, c085, c091, c108, c142 (see the E3g4 rows)", "FAIL",
    "Every other T card states its hypotheses (A1-A4 on c080, c081, c084, c086, c087, c088, c089, c090; A1-A3 on c125, c141, c143; "
    "alpha, delta on c101, c102, c104, c105, c111, c113, c150, c166). Five T cards do not: c082, c085, c091, c108, c142.",
    "See the E3g4 hypothesis rows.")

row("E3g-r2-scope-words", "2.9-scope words (only, every, any, all, always, exactly, same, once)",
    "cards.json L05-L08 fronts and backs (for example c085, c089, c107, c122, c153)", "PASS",
    "Each scope word was checked against its source: c085 'every such gamma' (Remark 2.3: every gamma != 1); c089 'exactly when' "
    "(Remark 3.4); c107 'for every alpha, delta, lambda > 0' (Remark 2.4); c122 'changes sign once' (lab output: sign changes = 1, "
    f"{S}run_labs_E3_r4.out via the L07 lab output lines 0229-0231); c153 'all six gaps' (L08 lab output line 0323).")

row("E3g-r2-process-words", "2.9-prose / banned process words in learner text",
    "cards.json L05-L08; check_pages E3 output", "PASS",
    f"grep over the card file for we, our, let's, TODO, verifier, builder: no hits ({S}cards_L05_L08.txt). "
    f"{S}check_pages_E3_r4.out: 'check_pages E3: PASS' (banned strings in visible prose).")

row("E3g-r2-gates", "2.9 / gates on this pin (run by this verifier)",
    f"{S}", "PASS",
    f"{S}check_pages_E3_r4.out 'PASS'; {S}check_dag_E3_r4.out 'PASS'; {S}check_projects_E3_r4.out 'PASS'; "
    f"{S}run_labs_E3_r4.out 'PASS (11/11)'; {S}page_smoke_L05-L08_r4.out 'PASS' (zero console errors on L05-L08); "
    f"{S}ruff_twins_L05-L08_r4.out; {S}mypy_L08_twin_r4.out; {S}verify_refs_offline_r4.out.")

row("E3g-r2-delta", "delta read (a007712..4eb6788) for the slice",
    "git diff a007712f..4eb6788f -- course/modules/E/E3/cards.json course/modules/E/E3/L05.html .. L08.html tests/labs/E3/lab-E3-L08-1.py",
    "PASS",
    "Every hunk of cards.json (E3-c021, c039, c087, c088, c091, c094, c095, c096 removed, c097 deleted, c099-c102 wording, c132, c135, "
    "c144, c149, c153, c172, c176) and of L05-L08.html (Remark 3.4, A2 pointer, reference paragraphs, V_tau at tau = 1 in Definition 1.2, "
    "the Proposition 2.4 wording) was read and checked against the current text. Delta in other slices (L02-L04, project, grader) not read.")

row("E3g3-c135-terminology", "2.9-prose (E3-c135 back vs L07 Section 3)",
    "course/modules/E/E3/cards.json E3-c135 (line 895); L07 text line 0243", "PASS",
    "Back now reads 'The cumulative repair of Section 3 is not derived', matching L07 Section 3 ('This lesson does not derive that repair').")

row("E3g3-notation-collisions", "2.4-notation (one meaning per letter in E3)",
    "cards.json E3-c148 (line 981), E3-c155 (line 1031); L06 text line 0023; L05 text line 0023; L08 text line 0020",
    "FAIL",
    "V_1 is resolved: the L08 maxmin value is now V_tau(f) at tau = 1 (L08 text line 0020; E3-c172 'V_tau(f) at tau = 1'), so V_1 "
    "means only the L05 terminal value c_1 (L05 text line 0023). The W collision remains: W is the prospect value in L06 (Definition 1.3, "
    "E3-c100, c104, c105, c107, c116), and final wealth in E3-c148 ('E_P[1/W]') and E3-c155 ('u(W) = -exp(-nu W)'). The lesson text uses w "
    "(L08 text lines 0083, 0128, 0335). The notation registry (notation/notation.json) registers T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q "
    "only, so the unit's own rule applies.",
    "Rename final wealth to w in E3-c148 and E3-c155 (see the E3g4 notation rows).")

row("E3g3-c091-gamma", "2.4-math (E3-c091 gamma != 0)",
    "course/modules/E/E3/cards.json E3-c091 (line 608); L05 text lines 0055, 0064", "PASS",
    "Remark 3.4 (L05 text line 0064): '1/gamma for gamma != 0; at gamma = 0 the marginal rate of substitution does not depend on c1/c0'; "
    "Theorem 3.2 (line 0055) 'The restriction needs gamma != 0'. The card's gamma != 0 condition now matches. The A1-A4 gap is a separate row.")

row("E3g3-c132-omega", "2.2-numbers (E3-c132 weighted value under omega_{1/2})",
    "course/modules/E/E3/cards.json E3-c132 (line 871); L07 text line 0251", "PASS",
    f"Back names omega_{{1/2}} (Example 1.4) and alpha = 1; {S}numbers_g4.out: omega(0.01) = 0.08340301, omega(0.99) = 0.82984948, "
    "weighted value 49.83277 -> 49.8328 against EV 50.5 (L07 misconception 3 arithmetic: +7.34 and -8.01, net -0.67 re-derived).")

row("E3g3-c097-trivia", "2.7-cards (E3-c097 removed; no trivia card)",
    "course/modules/E/E3/cards.json (id list); L05 text line 0395", "PASS",
    "E3-c097 is absent from cards.json on this pin; L05 references (text line 0395) now state the registry-only holding of "
    "epstein1989substitution. E3-c092 is also absent (an id gap, not a defect by itself).")

row("E3g3-basis-wording", "2.3-grades (basis strings of the C cards)",
    "cards.json E3-c094 (line 623), c095 (631), c106 (699), c117 (763), c122 (797), c153 (1016)", "PASS",
    "Each basis names the lab part and the case it covers: c094 finite differences at c1 in [0.999, 1.001] c1 with c1 = 4; c095 one pair; "
    "c106 one gamble; c117 the four-gain and four-loss grid; c122 the 1001-point grid (L07 Observation 1.5); c153 six (psi, beta) pairs. "
    "Each matches the lab code and output (L05 text lines 0190-0229; L08 text lines 0316-0323).")

row("E3g3-L05-proofs", "2.4-math (L05 proofs and displayed formulas)",
    "course/modules/E/E3/L05.html; ledgers/E3/scripts/E3-g-r4/text/L05.txt", "PASS",
    "Re-derived Theorem 1.3(a), (b) (monotonicity for a < 0), Corollary 1.4, Proposition 2.2 (chain rule and MRS = (1-beta)/beta (c1/c0)^(1/psi)), "
    "Remark 3.1, Theorem 3.2, Corollary 3.3 (h'(u) > 0), Remark 3.4 (r^gamma = r^(1/psi) only if gamma = 1/psi). Note: L05 text line 0014 "
    "says the restriction makes the form 'reduce to CRRA expected utility' where Theorem 3.2 gives a power transform; prose note for the L05 verifier.")

row("E3g3-L06-proofs", "2.4-math (L06 proofs)",
    "course/modules/E/E3/L06.html; text/L06.txt", "PASS",
    "Proposition 1.4 (derivatives, continuity at 0, concavity and convexity), Propositions 2.1 and 2.2 (W decreasing in lambda, sign threshold), "
    "Remark 2.4 (monotonicity without bounds on the powers), Remark 2.5 (700 - 300 lambda and 1000 - 600 lambda), Remark 3.2 "
    f"(lambda_R = sqrt(2)/2 at p = 1/3) re-derived; {S}numbers_g4.out.")

row("E3g3-L07-proofs", "2.4-math (L07 proofs and closed forms)",
    "course/modules/E/E3/L07.html; text/L07.txt", "PASS",
    "Example 1.4 closed form (P1 derivation), Remark 1.3, Remark 1.6 sum 0.89103669, Proposition 2.2 threshold algebra, Observation 1.5 "
    f"(one sign change; last grid point 0.278, re-run in the lab output), misconception 3 arithmetic. {S}numbers_g4.out; "
    f"{S}l07_eta1_gap_g4.out (E3 exercise claim: eta = 1 gap 3.125625e-1, prose says 3.13e-1, matches).")

row("E3g3-L08-proofs", "2.4-math (L08 proofs and worked numbers)",
    "course/modules/E/E3/L08.html; text/L08.txt", "PASS",
    "Proposition 1.3, Theorem 2.2 (strict case), Proposition 2.4 (worst priors P_0 and P_90), Example 2.5 (103125, 106451.6129, 100000), "
    "Proposition 3.2 (injectivity of x -> x^(1/a) for a != 0), Remark 4.2 (affinity of E_P[1/w] in p, midpoint 1/2), Model 2 and Model 4 "
    f"numbers, all re-derived in {S}numbers_g4.out.")

row("E3g3-c148-scope", "2.9-scope (E3-c148 'not a general property')",
    "course/modules/E/E3/cards.json E3-c148 (line 981); L08 text line 0375-0380", "PASS",
    "Scope sentence matches Remark 4.2 and the L08 section 5 text ('Its coincidence ... holds because g is affine and the midpoint ... equals the average prior'). "
    "The symbol fault on the same card is a separate row (E3g4-c148-notation).")

row("E3g3-attribution", "2.1-attribution (E3-c134, c137, c157, c158)",
    "cards.json E3-c134, E3-c157, E3-c158; references/references.json", "PASS",
    "Titles read from references/references.json (see E3g-r2-registry). Cards state title-only attributions and 'not reproduced' scope, "
    "matching L07 text line 0025 and L08 text lines 0020, 0054.")

row("E3g3-notation-registry", "2.4-notation (notation/notation.json)",
    "notation/notation.json (8 registered symbols)", "PASS",
    "Registered symbols: T, Phi, Phi^-1, gamma_3, gamma_4, R*, R^e*, R_f, Q. No slice card uses a registered symbol with another meaning. "
    "V, W and U are not registered, so the unit-level rule in the collision row applies.")

row("E3g3-page-smoke", "2.5/2.9 page_smoke for L05-L08 (run alone)",
    f"{S}page_smoke_L05-L08_r4.out", "PASS",
    "'page_smoke E3: PASS' for the four lesson pages (zero console errors, math rendered, no external requests), run with --pages L05 L06 L07 L08.")

row("E3g3-gates-projects-ruff", "gates touching the slice (check_projects, ruff on twins)",
    f"{S}check_projects_E3_r4.out; {S}ruff_twins_L05-L08_r4.out", "PASS",
    "check_projects E3: PASS; ruff check and format on the four L05-L08 twins: PASS.")

row("E3g3-delta-r3", "delta read a007712..4eb6788 (slice files)",
    "git diff a007712f..4eb6788f -- course/modules/E/E3/cards.json course/modules/E/E3/L0[5-8].html tests/labs/E3/lab-E3-L08-1.py", "PASS",
    "Read in full on this pin (see E3g-r2-delta). Slice changes: E3-c097 deleted, c091 gamma != 0, c176 re-targeted, notation and "
    "basis rewording, Remark 3.4 and Definition 1.2 hunks.")

# ---- new round-4 rows ----
row("E3g4-c082-hypotheses", "2.4-math / 2.6-cards (carry the hypotheses of the claim)",
    "course/modules/E/E3/cards.json E3-c082 (line 546); L05 text line 0039", "FAIL",
    "Back: 'No. The value depends on the lottery through CE1 ... so two lotteries with the same mean can have different values (Remark 1.5).' "
    "The claim needs the value V0 to exist (A1-A4) and the example uses gamma = 2 (CE1 = 8/5 and 12/5, Remark 1.5; "
    f"{S}numbers_g4.out). Neither the assumptions nor gamma = 2 is on the card.",
    "Prefix the back with 'Under A1 to A4, at gamma = 2 (Remark 1.5),'.")

row("E3g4-c085-hypotheses", "2.4-math (EIS = psi needs Proposition 2.2's hypotheses)",
    "course/modules/E/E3/cards.json E3-c085 (line 566); L05 text lines 0049-0050", "FAIL",
    "Back: 'For gamma not equal to 1 ... the EIS is psi for every such gamma (Remark 2.3).' The EIS = psi step is Proposition 2.2, stated "
    "'Assume A1 to A4 for deterministic plans' (L05 text line 0043). The card cites only A3.",
    "Change to: 'Under A1 to A4 for deterministic plans, ... (Remark 2.3, Proposition 2.2).'")

row("E3g4-c091-hypotheses", "2.4-math / 2.6-cards (E3-c091 hypotheses)",
    "course/modules/E/E3/cards.json E3-c091 (line 608); L05 text lines 0016, 0064", "FAIL",
    "The gamma != 0 condition is correct (Remark 3.4), but the back's second claim, 'Epstein-Zin gives psi instead', is Proposition 2.2 and needs "
    "A1-A4. L05 text line 0016 states A1-A4 as standing assumptions for Sections 1 to 3, and the card omits them.",
    "Change to: 'Under A1 to A4, 1/gamma for gamma not 0 (Remark 3.4); at gamma = 0 it is undefined. Epstein-Zin gives psi instead.'")

row("E3g4-c108-hypotheses", "2.4-math (E3-c108 hypothesis alpha = delta = 1)",
    "course/modules/E/E3/cards.json E3-c108 (line 714); L06 text line 0047 (Remark 2.5)", "FAIL",
    "Remark 2.5 opens 'with alpha = delta = 1'. The combined value 700 - 300 lambda and the separate value 1000 - 600 lambda follow from "
    "v(x) = x and v(-x) = -lambda x. With other powers the numbers differ, and the card states neither the value function nor its powers.",
    "Prefix the back with 'With alpha = delta = 1 (Remark 2.5),'.")

row("E3g4-c130-argument", "2.4-math / 2.6-cards (E3-c130 supporting argument)",
    "course/modules/E/E3/cards.json E3-c130 (line 856); L07 text lines 0246-0247", "FAIL",
    "The answer 'It can' is correct: Proposition 2.2 gives V(A) > V(B) at alpha = 1 (42.8686 > 39.1251) and alpha = 1/2 (4.8788 > 3.9125). "
    "The card's support is only the weight comparison 0.57158177 > 0.39125077 (Remark 1.6). That comparison does not decide the ranking, "
    "because A's two positive outcomes are 50 and 100 CU and B's is 100 CU, so the values v(x_i) differ. The card does not cite Proposition 2.2.",
    "Cite Proposition 2.2 and the values V(A) = 42.8686 > V(B) = 39.1251 at alpha = 1 (Lab 1 part C), keeping the weight comparison as the reason.")

row("E3g4-c142-hypotheses", "2.4-math (E3-c142 hypotheses of Theorem 2.2)",
    "course/modules/E/E3/cards.json E3-c142 (line 941); L08 text lines 0035-0041", "FAIL",
    "The strict case uses A2 (u strictly increasing, so u^-1 is strictly increasing) and A1-A3 of Theorem 2.2 (L08 text line 0036-0038). "
    "The card states none of them.",
    "Prefix the back with 'Under A1 to A3 of Theorem 2.2, with u strictly increasing (A2),'.")

row("E3g4-c148-notation", "2.4-notation (E3-c148 symbol W)",
    "course/modules/E/E3/cards.json E3-c148 (line 981); L06 text line 0023; L08 text line 0335", "FAIL",
    "Back: 'For a two-outcome gamble E_P[1/W] is affine in p.' W is the L06 prospect value (Definition 1.3). L08 writes final wealth as w "
    "(Remark 4.2: E_P[1/w]; Model 1: u(w) = -1/w).",
    "Replace E_P[1/W] with E_P[1/w].")

row("E3g4-c155-notation", "2.4-notation (E3-c155 symbol W)",
    "course/modules/E/E3/cards.json E3-c155 (line 1031); L08 text lines 0439-0441 (R3 question and solution)", "FAIL",
    "Back: 'holds for u(W) = -exp(-nu W) with any nu > 0.' W is the L06 prospect value; L08's R3 question (line 0439) and solution (line 0441) write u(w) = -e^{-nu w}.",
    "Replace u(W) = -exp(-nu W) with u(w) = -exp(-nu w).")

row("E3g4-c096-context", "2.5 / 2.6-cards (E3-c096 'the risky tree')",
    "course/modules/E/E3/cards.json E3-c096 (line 639); L05 text lines 0066, 0190-0193", "PASS",
    "The card's answer 2.2500, 1.6000, 1.3720 matches the lab output (L05 text lines 0243-0245) and the code (risky_float = (0.5, 1.0), (0.5, 4.0)). "
    "The card does not define 'the risky tree' on its own; the lesson's prediction (line 0066) names it as the c1 = 1 or 4 tree. "
    "Observation for the card author: name the tree in the front. Not a failure of the card's content.")

row("E3g4-c131-unrounded", "2.2-numbers (E3-c131 'unrounded' values)",
    "course/modules/E/E3/cards.json E3-c131 (line 863); L07 text lines 0286-0288", "PASS",
    f"{S}numbers_g4.out: the unrounded difference is 3.74355573299 -> 3.7436. The card's 8-digit values 42.86863274 and 39.12507700 are the "
    "8-decimal displays, as in the lesson's own E2 solution; their difference 3.74355574 also rounds to 3.7436. Same convention as L07 "
    "Example 1.4 (line 0027). No numeric defect.")

row("E3g4-c172-definition", "2.4-math (E3-c172 tau = 1 specialization)",
    "course/modules/E/E3/cards.json E3-c172 (line 1150); L08 text line 0020", "PASS",
    "Definition 1.2 text: 'The maxmin expected utility value is V_tau(f) at tau = 1, which equals min over P of E_P u(f)'. Card matches.")

row("E3g4-lab-observations", "2.5 / 2.7 (observations outside the card rows)",
    f"{S}numbers_g4.out; {S}dup_scan_g4.out", "PASS",
    "Recorded in notes: lab-versus-theorem pairs (E3-c101 and c117; E3-c128 and c129; E3-c146 and c153) state the same property at different grades "
    "and are not duplicates by content; they are reported for the L06/L07/L08 verifiers.")

fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 4,
    "verifier": "Haiku independent verifier, E3-g round 4 (did not build E3)",
    "pin": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "base": "a007712fdbfc8b4851123f4de76b5310ac5a9e64 (round-3 pin; delta a007712..4eb6788 read for this slice)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD4-E3-g (detached at 4eb6788)",
    "scratch": "ledgers/E3/scripts/E3-g-r4/ (scripts, outputs and text dumps; text/ holds the L05-L08 lesson text read in full)",
    "verified_at": "2026-11-03T16:24:57Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice g is the 84 cards of L05-L08 (L05 20, L06 19, L07 18, L08 27; 50 T, 17 C, 17 ungraded definitions) against the four lesson texts. "
        "Every lesson text was read in full (text/L05.txt 397 lines, L06 329, L07 368, L08 510) and every card was read against it.",
        "Not a project slice: no student-error mutants were written and no alternative implementations were run (VERIFIER_RULES 2.6 applies to project slices). mutants is empty by design.",
        "Round-3 PASS rows were not carried: each was re-derived on this pin. Round-3 FAIL rows are kept with their ids and re-checked: E3g-dup-scan (still FAIL), E3g-r2-L05-G2 (gamma fixed, hypotheses still open), E3g-r2-L06-G4 (c108 new), E3g-r2-hypotheses (still open), E3g3-notation-collisions (V_1 fixed, W still open).",
        "Outside this slice, noted for the other verifiers: (a) the L08 retrieval quiz (text line 0482) mislabels the prior options: 'the average prior P(red) = 1/3' and 'the smallest prior in the set P(red) = 2/3' (the smallest prior is 1/3; the answer is 1/3). (b) L05 text line 0014 says the restriction makes the form 'reduce to CRRA expected utility', while Theorem 3.2 gives a power transform. (c) L05 text line 0260 'a restriction at one point' is loose. (d) L07 E2 solution labels 8-decimal values 'unrounded' (same convention as Example 1.4; no numeric error).",
        "Not checked: live verify_refs (network; no reference changed in the slice); pytest (the lab checks run through run_labs and page_smoke, which cover the same twins; tests/test_labs.py not run separately); mypy and pytest across the repository (no Python tool in the slice changed except the L08 twin, which passes mypy and ruff); run_graders and mutate_graders (project slices, not this one); other slices' hunks (L02-L04, project, grader, cards E3-c021, c039, c094 etc. belong to other slices, though c094 is read here).",
    ],
    "summary": {},
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants": 0,
    "mutants_killed": 0,
}

out = ROOT / "ledgers" / "E3" / "E3-g.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out, fragment["summary"])
