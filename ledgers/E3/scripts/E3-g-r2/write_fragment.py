"""Write the round-2 verifier fragment for E3 slice g (cards of L05-L08) to ledgers/E3/E3-g.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
S = "ledgers/E3/scripts/E3-g-r2"
C = "course/modules/E/E3/cards.json"
L4, L5, L6, L7, L8 = (f"course/modules/E/E3/L0{n}.html" for n in (4, 5, 6, 7, 8))

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- rows kept from round 1 (re-verified against the round-2 pin) ----
row("E3g-dup-scan", "2.7-duplicates",
    f"{C} (E3-c078, E3-c173 removed)", "PASS",
    "Round 1 FAIL: E3-c078 and E3-c173 stated the same two-date Epstein-Zin value. E3-c173 is absent from the round-2 file "
    "(168 cards, 168 distinct ids; the diff of c737272 deletes it). Full scan of all 168 cards with "
    f"{S}/dup_scan.py -> {S}/dup_scan.out: 0 exact duplicate fronts, 0 exact duplicate backs. Pairwise review of the 84 "
    "L05-L08 cards: the closest pairs (E3-c137/E3-c172 general tau versus tau = 1; E3-c143/E3-c154 worst prior of "
    "Proposition 2.4; E3-c109/E3-c163; E3-c169/E3-c170) test different facts. The two-date formula appears on E3-c078 "
    "(full recursion) and E3-c080 (CE1 form, Theorem 1.3(a)), both in L05, and on no L08 card.")
row("E3g-notation-c138", "2.4-notation",
    f"{C} E3-c138 (line 933)", "PASS",
    "Round 1 FAIL: front said 'for every alpha', but L08 Definition 1.2 writes the weight as tau (L08.html: 'The weight is "
    "written tau, not alpha'). Round-2 front reads 'What does a one-element prior set give for every tau?'. Re-read against "
    f"L08 Definition 1.2 and Proposition 1.3 ({S}/text/E3g_r2_L08.txt lines 0062, 0068-0077). PASS.")
row("E3g-grade-c142", "2.3-grades",
    f"{C} E3-c142 (line 960); {L8} Theorem 2.2 proof (line 108)", "PASS",
    "Round 1 FAIL: graded T for a strict case the Theorem 2.2 proof did not give. The round-2 proof (L08.html line 108) "
    "adds the strict case: if the E_{P_i} u(f) are not all equal, one exceeds m = min, so their average exceeds m, and "
    "strict monotonicity of u^-1 makes the inequality strict. Re-derived: correct (average of numbers >= m with one > m is > m). "
    "Card T, Remark 2.3 cited as the example. PASS.")
row("E3g-grade-c090", "2.3-grades",
    f"{C} E3-c090 (line 614)", "PASS",
    "Round 1 FAIL: a T card carried a lab-read pair (psi = 2, gamma = 2). The round-2 back has only the Corollary 3.3 "
    "hypothesis (psi = 1/gamma) and the Remark 3.4 MRS statement, with no lab number. The lab-read pair is carried by "
    f"E3-c095, graded C with basis 'Lab 1 (one explicit pair)'. Checked against {L5} Remark 3.4 and Corollary 3.3. PASS.")

# ---- new defects (round 2) ----
row("E3g-r2-V-symbol", "2.2-numbers / notation: card agrees with lesson text",
    f"{C} E3-c100 (line 678), E3-c105 (line 711), E3-c107 (line 726), E3-c116 (line 774)", "FAIL",
    "Four L06 cards write the prospect value as V. L06 never defines V. Definition 1.3 defines W := sum p_i v(x_i) "
    f"({L6} Definition 1.3 block; text dump {S}/text/E3g_r2_L06.txt line 0069); Proposition 2.1, Proposition 2.2 and Remark 2.4 use W; "
    "Lab 1 prints 'W at lam = 2 with alpha = delta = 0.5: -8.6835' ({S}/text/E3g_r2_L06.txt line 0262). The arithmetic in "
    "all four cards is correct (verify_numbers.out), so only the symbol differs from the lesson.",
    fix="Replace V by W in the four backs: E3-c100 'W = sum of p_i v(x_i)...'; E3-c105 'The value W = p g^alpha - (1 - p) "
        "lambda l^delta is zero at lambda*...'; E3-c107 '...positive exactly when W is positive'; E3-c116 'W = -8.6835 at "
        "lambda = 2. The sign of W changes at the threshold.'")
row("E3g-r2-c145-V1", "2.9-structure / card cites what its lesson says",
    f"{C} E3-c145 (line 981)", "FAIL",
    "E3-c145 says the gamble has 'terminal value V1 = c1' and cites Definition 3.1. L08 Definition 3.1 "
    f"({L8} Definition 3.1 block, starting line 141) defines V0 with E c1^(1-gamma) and never states V1. 'V1' occurs in L08 only in the lab "
    f"docstring ({S}/text/E3g_r2_L08.txt line 0291). The terminal convention V1 = c1 is stated in L05 Definition 1.1 "
    "({S}/text/E3g_r2_L05.txt lines 0065-0069), not in L08. The content is consistent with the lesson, but the citation is not.",
    fix="Reword the back to: 'Date 0 consumes a sure c0, and date 1 consumes c1, which may be random; the date-1 term "
        "enters the value as E c1^(1 - gamma) (Definition 3.1). The value uses the exponent 1 - 1/psi.' "
        "Or cite L05 Definition 1.1 for the terminal convention V1 = c1.")

# ---- card-group reviews (every card of the slice read against its lesson block) ----
row("E3g-r2-L05-G1", "2.4-math / 2.6-cards (E3-c078 to E3-c087)",
    f"{C} (E3-c078 to E3-c087); {L5} Definition 1.1, Remark 1.2, Theorem 1.3, Corollary 1.4, Remark 1.5, Definition 2.1, Proposition 2.2, Remark 2.3, Remark 3.1, Theorem 3.2, Corollary 3.3", "PASS",
    "Read each card against its block. Recomputed with exact fractions and floats in verify_numbers.py (verify_numbers.out): "
    "CE1 = 8/5 and 12/5 for the two mean-5/2 lotteries (c082); MRS and EIS = psi by the chain rule (c084, Prop 2.2 proof); "
    "theta = 1 iff psi = 1/gamma (c086); (1-gamma)U = V0^(1-gamma) at psi = 1/gamma (c087). Hypotheses A1-A4 are stated on "
    "each card that needs them. Grades T match the lesson's proofs. PASS.")
row("E3g-r2-L05-G2", "2.2-numbers / 2.3-grades (E3-c088 to E3-c097, E3-c169)",
    f"{C} (E3-c088 to E3-c097, E3-c169); {L5} Corollary 3.3, Remark 3.4, Lab 1 (output in {S}/text/E3g_r2_L05.txt lines 0324-0346), Problem E1, References section", "PASS",
    "c088 (Corollary 3.3 proof: h' > 0 where (1-gamma)U > 0). c089 and c091 (Remark 3.4 exponents gamma and 1/psi, "
    "'exactly when 1/psi = gamma'; checked). c093 V0 = 80/49 and c169 U = -49/80 recomputed exactly (verify_numbers.out). "
    "c094 EIS lines 0.5000, 2.0000, 0.2500 and c096 CE1 lines 2.2500, 1.6000, 1.3720 match the twin output "
    "(twin_vs_page.out) and the recomputation. c095 U(4,4) = -0.2500, U(1,10) = -0.5500, V0(4,4) = 4.0000, "
    "V0(1,10) = 4.3311 match. c097 attribution matches L05 section 9. Grades C on lab-read cards with a basis. PASS.")
row("E3g-r2-L05-G3", "2.2-numbers / 2.4-math (E3-c170, E3-c098 to E3-c106)",
    f"{C} (E3-c170, E3-c098 to E3-c106); {L5} Remark 1.5; {L6} Definitions 1.1-1.6, Propositions 1.4, 2.1, 2.2, Example 2.3", "PASS",
    "c170 CE1 = 8/5 exact. c101 Proposition 1.4: v''(x) = alpha(alpha-1) x^(alpha-2) < 0 on gains and lambda delta (1-delta)(-x)^(delta-2) > 0 on losses, both recomputed from the definition. "
    "c102 Remark 1.5 ratio lambda. c103 Definition 1.6. c104 Proposition 2.1 lambda* = 5/3 for Example 2.3 (verify_numbers.out). "
    "c106 values 200, 50, -100 and lambda* = 5/3 recomputed. Content PASS; the symbol W versus V on c100 and c105 is "
    "recorded in E3g-r2-V-symbol. Other items PASS.")
row("E3g-r2-L06-G4", "2.2-numbers / 2.4-math (E3-c107 to E3-c113, E3-c116, E3-c117, E3-c163)",
    f"{C} (E3-c107 to E3-c113, E3-c116, E3-c117, E3-c163); {L6} Remarks 2.4, 2.5, 3.1, 3.2; Lab 1 output lines 0262-0265", "PASS",
    "c108: combined value 700 - 300 lambda and separate 1000 - 600 lambda, equal to 100 and -200 at lambda = 2 (recomputed). "
    "c110: the proofs of Propositions 1.4, 2.1, 2.2 use only lambda > 0, read from the proofs. c111 and c113: the reference point "
    "EV gives (1/2) 800^alpha (1 - lambda) and lambda_R = sqrt(2)/2 = 0.7071 for p = 1/3, g = 1000, l = 300, EV = 400/3 "
    "(recomputed). c116: sqrt(5/3) = 1.2910 and W = -8.6835 recomputed; symbol per E3g-r2-V-symbol. c117: grid checks match the "
    "lab's printed True lines (L06 dump 0263-0265). PASS.")
row("E3g-r2-L07-G5", "2.2-numbers / 2.4-math (E3-c118 to E3-c127)",
    f"{C} (E3-c118 to E3-c127); {L7} Definition 1.1, Definition 1.2, Remark 1.3, Example 1.4, Observation 1.5, Remark 1.6, Example 2.1, Proposition 2.2, Remark 2.3, Lab 1 part C", "PASS",
    "omega(3/10) = 0.28579088, omega(3/5) = 0.39125077, omega(1/2) = 0.35355339, 2 omega(3/10) = 0.57158177, "
    "ratio 0.73045450 and thresholds 2/3, 0.58578644, omega(1/4) = 2 - sqrt3 = 0.26795 (verify_numbers.out). "
    "c121 closed form equals the general formula to 3.33e-16 (verify_numbers.py grid). c122: one sign change, last grid point 0.278. "
    "c127 printed values 42.8686, 39.1251, 4.8788, 3.9125 equal the rounded unrounded values. c126 identity 45 and 60 PASS. PASS.")
row("E3g-r2-L07-G6", "2.2-numbers / 2.9-structure (E3-c128 to E3-c137)",
    f"{C} (E3-c128 to E3-c137); {L4} Theorem 1.5 (line 89); {L7} Problems R1, R2, E2; Lab 1 parts B-D", "PASS",
    "c128: lab part D prints 10 of 10 (run_labs output and twin run). c129: L04 Theorem 1.5 (finite support S: F_X <= F_Y for all t iff E u(X) >= E u(Y) for every nondecreasing u) "
    "gives the card's statement with X = B, Y = A (check: card_refs.out resolves it to L04.html). c130 weights 0.57158177 > 0.39125077. "
    "c131: unrounded difference 3.74355574 -> 3.7436; printed difference 3.7435 (verify_numbers.out). c132: 49.8328 = 8.340301 + 41.492474, below 50.5 "
    "(recomputed). c133 affine argument. c135 tails 3/5 and 3/5 at 50, 3/5 and 3/10 at 100 (exact, Problem R2). c134 and "
    "the title claim: registry title of kahneman1979prospect is 'Prospect Theory: An Analysis of Decision under Risk' "
    "(references.json; live check E3g-r2-registry). c136 Definition 1.1 matches. PASS.")
row("E3g-r2-L08-G7", "2.4-math / 2.3-grades (E3-c138 to E3-c147)",
    f"{C} (E3-c138 to E3-c147); {L8} Definition 1.2, Proposition 1.3, Example 1.4, Definition 2.1, Theorem 2.2, Proposition 2.4, Example 2.5, Definition 3.1, Proposition 3.2, Remark 3.3", "PASS",
    "c139: average of k/90, k = 30..60, is 45/90 = 1/2 (exact). c141: Theorem 2.2 proof and hypotheses A1-A3 read. c143: proof of Proposition 2.4: E_p u = u(W_no) + p(u(W_red) - u(W_no)), so the minimum is at P_0 for red and P_90 for black. "
    "c144: 103125 and 3300000/31 = 106451.6129 (exact, verify_numbers.out). c146: Proposition 3.2 proof injectivity of x^(1/a) for a != 0 read and checked; hypotheses A1-A5 match. "
    "c147 matches Remark 3.3. c138 and c142 per round-1 rows above. c145: see E3g-r2-c145-V1. PASS except c145 (FAIL row).")
row("E3g-r2-L08-G8", "2.4-math / 2.6-cards (E3-c148 to E3-c158)",
    f"{C} (E3-c148 to E3-c158); {L8} Remark 4.2, Model 1-4, Lab 1 part B, Problem E3, Section 4 numbers", "PASS",
    "c148: E_P[1/W] affine in p, so the tau = 1/2 value equals EU at the midpoint of the extreme priors. The card's 'not a general property' "
    "is a scope claim with support: the lesson's Remark 4.2 condition, and a three-prior set {0.2, 0.3, 0.9} gives tau = 1/2 CE "
    "102702.70 against EU CE at the average prior 101456.31 (computed in this round, not on the page). "
    "c149 4180000/41 = 101951.2195 exact. c150 5 - sqrt50 = -2.071068 and -1.072330 CU (verify_numbers.out). c151 99523.8095 at p = 1/3. "
    "c152 548.7805 cents = 22500/41, 5.4878 CU. c153: lab part B six pairs, largest gap 2.91e-11 (run). c154 and c155: "
    "Theorem 2.2 uses u only through A2 (the proof, read). c157 registry title 'Risk, Ambiguity, and the Savage Axioms' "
    "contains 'ambiguity'. c158 registry title 'Maxmin expected utility with non-unique prior'. PASS.")
row("E3g-r2-L08-G9", "2.2-numbers / 2.4-math (E3-c164, E3-c165, E3-c166, E3-c172)",
    f"{C} (E3-c164, E3-c165, E3-c166, E3-c172); {L8} Example 2.5, Model 2, Definition 1.2", "PASS",
    "c164: worst priors give 100000 cents surely (P_0 for red, P_90 for black). c165: 103125 and 106451.6 exceed 100000. "
    "c166: -107.2330 cents and 99892.7670 (recomputed). c172: V_1 = min E_P u(f) (Definition 1.2). PASS.")

# ---- scans and gates ----
row("E3g-r2-numbers", "2.2-numbers (all cards)",
    f"{C} (84 cards of L05-L08)", "PASS",
    f"{S}/verify_numbers.py -> {S}/verify_numbers.out: 91 of 91 recomputed numbers match the cards and lesson text (exact Fractions where rational, floats printed at the cited precision). "
    f"{S}/card_numbers_in_lesson.py -> {S}/card_numbers.out: every multi-digit number on the 84 cards occurs in its own lesson's text, including the printed lab outputs.")
row("E3g-r2-lab-twins", "2.5-labs (labs behind card claims)",
    "tests/labs/E3/lab-E3-L05-1.py ... lab-E3-L08-1.py; course/modules/E/E3/L05.html ... L08.html", "PASS",
    f"tools/run_labs.py --unit E3 -> run_labs_E3.out: 'run_labs E3: PASS (11/11)'. Each L05-L08 twin run alone as python -I -W error: exit 0, empty stderr "
    f"({S}/twin_vs_page.py -> twin_vs_page.out). Page expected block equals twin stdout for all four lessons; page code block equals twin source ({S}/code_vs_twin.out).")
row("E3g-r2-refs-cross", "2.6-cross-references (card references resolve)",
    f"{C}; {L5}-{L8}; {L4} line 89", "PASS",
    f"{S}/card_refs_exist.py -> card_refs.out: each Remark/Proposition/Corollary/Definition/Example/Observation/Problem/Model reference on a card resolves in its own lesson. "
    "The one cross-lesson reference (E3-c129, 'Theorem 1.5 of Lesson 4') resolves to L04.html line 89 and matches its statement.")
row("E3g-r2-registry", "2.1-citations (keys cited by the cards)",
    "references/references.json: kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin, epstein1989substitution", "PASS",
    "tools/verify_refs.py --offline -> verify_refs_offline.out: 560 entries, 0 problems. tools/verify_refs.py --unit E3 (live, Crossref) -> verify_refs_E3_live.out: 5 entries, 0 problems. "
    "Titles: kahneman1979prospect 'Prospect Theory: An Analysis of Decision under Risk'; ellsberg1961risk 'Risk, Ambiguity, and the Savage Axioms'; "
    "gilboa1989maxmin 'Maxmin expected utility with non-unique prior'. The cards attribute only these titles and no result, locator or number.")
row("E3g-r2-coverage", "2.7-cards: one card per definition, theorem, key formula, key result, misconception",
    f"{C}; {L5}-{L8}", "PASS",
    "Block-by-block read of L05-L08: Definitions 1.1-1.6, 2.1, 3.1, 1.2 (L07), 1.3 (L08), 2.1 (L08) and Propositions 1.3, 1.4, 2.1, 2.2, 2.4, 3.2 have cards; "
    "Theorems 1.3, 2.2, 3.2, Corollaries 1.4, 3.3 have cards; Remarks 1.2, 1.3, 1.5, 1.6, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 4.2 have cards; "
    "Examples 1.4, 2.1, 2.3, 2.5 have cards; the Lab 1 figures and the three misconceptions of L05-L08 have cards. "
    "Id gaps (E3-c092, c114, c115, c156) are not content gaps: no lesson block lacks a card. PASS.")
row("E3g-r2-grades", "2.3-grades (independent re-grade, BLUEPRINT §3)",
    f"{C} (84 cards)", "PASS",
    "T: 49 cards, each a derivation or theorem on the page (checked in the card rows above). C: 17 cards, each on lab output or a single "
    "worked example with basis or cite (E3-c093, c094, c095, c096, c106, c116, c117, c122, c127, c128, c131, c134, c153, c157, c158, c169, c170). "
    "Ungraded cards are definitions, conventions, or attributions. The C grade on the exact lab values (c093, c106, c169, c170) is conservative and matches the lesson's own key-results grade. PASS.")
row("E3g-r2-hypotheses", "2.4-math (propositions carry their hypotheses)",
    f"{C} cards E3-c080, c081, c084-c089, c101, c104, c105, c107, c141, c143, c146, c155", "PASS",
    "Each card for a Proposition, Theorem or Corollary states or names its numbered assumptions (A1-A5 of Proposition 3.2, A1-A3 of Theorem 2.2 and of Proposition 2.4, "
    "A1-A4 of Theorem 1.3 and Proposition 2.2, and the alpha, delta, lambda restrictions of Propositions 1.4, 2.1, 2.2). Read against the Assumption blocks in the lessons. PASS.")
row("E3g-r2-scope-words", "2.4 / 2.9-prose: scope words on cards",
    f"{C} E3-c085, c107, c110, c142, c148, c155", "PASS",
    "'every', 'any', 'only', 'never' and 'not a general property' were each checked: E3-c085 and c107 (proved for every gamma != 1 or every lambda > 0), c110 "
    "(proofs use lambda > 0 only), c142 (one-element set is never strict), c155 (Theorem 2.2 uses u only through A2), c148 (three-prior counterexample in the row above). PASS.")
row("E3g-r2-process-words", "2.9-prose: banned phrases and process words",
    f"{C}", "PASS",
    "grep for TODO, TBD, lorem, 'for brevity', 'beyond the scope', 'it is important', 'studies show', 'experts agree', 'well known', "
    "'obviously', 'clearly', ellipses, builder, verifier, round, REQUEST: no hit in the card file for L05-L08.")
row("E3g-r2-gates", "2.9-structure / check_pages cards check",
    "tools/check_pages.py --unit E3; tools/check_dag.py --unit E3; tools/check_projects.py --unit E3", "PASS",
    f"check_pages E3: PASS (check_cards: ids, lesson names, grades, cite keys, basis for non-T grades; {S}/check_pages_E3.out). "
    f"check_dag E3: PASS ({S}/check_dag_E3.out). check_projects E3: PASS ({S}/check_projects_E3.out).")
row("E3g-r2-delta", "delta since pin: every hunk of the round-1 fix commit touching this slice",
    "git diff 9f5d9865 c737272 -- course/modules/E/E3/cards.json course/modules/E/E3/L07.html course/modules/E/E3/L08.html", "PASS",
    "Read every hunk: card wording changes (c004, c009, c012, c018, c021, c039, c042, c089, c090, c091, c097, c098, c103, c134, c138, c142, c145, c157, c158, c162, c167), "
    "the removal of c173, and the L07 solution and L08 proof, Remark 2.3, misconception 3 and key-row hunks. Each hunk in this slice is re-verified in the rows above; "
    "the L05 and L06 pages are unchanged in that commit; the L05 and L06 cards changed only at E3-c089, c090, c091, c097, c098 and c103, all re-read in the rows above. PASS.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 2,
    "verifier": "Haiku independent verifier, E3-g round 2 (did not build E3)",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "9f5d98654855cae327fec17f92626402f956faa5 (parent of the round-1 fix commit c737272; the round-1 fragment records no pin, so this is the delta read)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-E3-g",
    "scratch": "ledgers/E3/scripts/E3-g-r2/text (lesson text dumps); /tmp copies not used by any script",
    "verified_at": "2026-11-02",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: the 84 cards of L05-L08 in course/modules/E/E3/cards.json (the card-level slice g). Card claims were checked against the lesson blocks they cite and against the lab output.",
        "Lesson-page claims outside the cards (lab hypotheses, key-results table, problem solutions, misconception prose) were read only to check the cards against them. They are not graded rows here; the lesson slices own them.",
        "Not run: page_smoke.py (Chromium; page-level gate, belongs to the lesson slices). run_graders.py and mutate_graders.py (project slice only). ruff and mypy (no code in this slice changed; the repository gates belong to the architect). pytest (no test covers cards.json beyond check_pages).",
        "Attribution beyond titles is not claimed: the cards cite registry titles only, and no paper's results are attributed to the cards.",
        "The three-prior counterexample in E3g-r2-L08-G8 was computed by the verifier (formula 1/g(midpoint); g(p) = p/110000 + (1-p)/95000), not read from the lesson.",
    ],
}
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(r["status"] == "PASS" for r in rows),
    "fail": sum(r["status"] == "FAIL" for r in rows),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
}
out = ROOT / "ledgers/E3/E3-g.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"], "verdict", verdict)
