"""Build ledgers/E3/E3-g.json (round 12, slice g: E3 cards of L05-L08 against their lessons).

Every card row was checked by reading the card (cards.json) and the lesson text (L0x.txt, the strip.py
output of course/modules/E/E3/L0x.html read in full). Row evidence names the lesson locator (line numbers
of ledgers/E3/scripts/E3-g-r12/L0x.txt) and the scripts that recompute the numbers.
"""

from __future__ import annotations

import json
from pathlib import Path

CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyD12-E3-g")
OUT = CHECKOUT / "ledgers" / "E3" / "E3-g.json"
SCR = "ledgers/E3/scripts/E3-g-r12"
RECOMP = f"{SCR}/recompute_r12.py (output {SCR}/recompute_r12.out)"
NUMS = f"{SCR}/card_numbers_bounded.py (output {SCR}/card_numbers_bounded.out)"
CARDS = "course/modules/E/E3/cards.json"

# (card id, lesson, lesson locator in L0x.txt, check note)
CARD_ROWS: list[tuple[str, str, str, str]] = [
    # ---- L05 ----
    ("E3-c078", "L05", "27-30 (Def 1.1); assumptions 22-26 (A1-A4)", "V0 formula, a = 1 - 1/psi, V1 = c1, assumptions match"),
    ("E3-c079", "L05", "32 (Remark 1.2)", "CE1 formula and identity CE1^(1-gamma) = E c1^(1-gamma) match"),
    ("E3-c080", "L05", "33-36 (Thm 1.3 a, b)", "only through CE1; strictly increasing in CE1 under A1-A4"),
    ("E3-c081", "L05", "40-43 (Cor 1.4); 239-240 (section 5, third misconception)", "risky plan = sure plan at CE1"),
    ("E3-c082", "L05", "44-45 (Remark 1.5)", "same mean, different CE1; CE 8/5 and 12/5 at gamma = 2 recomputed exactly"),
    ("E3-c083", "L05", "47-48 (Def 2.1)", "EIS definition and MRS definition match"),
    ("E3-c084", "L05", "49-54 (Prop 2.2)", "MRS = (1-b)/b (c1/c0)^(1/psi), EIS = psi"),
    ("E3-c085", "L05", "55-56 (Remark 2.3)", "CE1 = c1 for every gamma != 1; EIS psi for every gamma"),
    ("E3-c086", "L05", "58-59 (Remark 3.1)", "theta = 1 exactly when psi = 1/gamma"),
    ("E3-c087", "L05", "60-64 (Thm 3.2); A2 at 24-25 (psi > 0 gives gamma > 0)", "(1-g)U = V0^(1-g); gamma != 0 restriction stated"),
    ("E3-c088", "L05", "65-68 (Cor 3.3)", "strictly increasing function of U; same ranking for all plans"),
    ("E3-c089", "L05", "69-70 (Remark 3.4)", "CRRA MRS exponent gamma, EZ exponent 1/psi, agree iff 1/psi = gamma; MRS_U recomputed from u' = c^-gamma"),
    ("E3-c090", "L05", "69-70 (Remark 3.4); 72 (Lab predictions); 235-236 (section 5, first misconception)", "Lab 1 disagreement at psi = 2, gamma = 2 is off the restriction"),
    ("E3-c091", "L05", "69-70 (Remark 3.4)", "CRRA elasticity 1/gamma for gamma != 0, undefined at gamma = 0; EZ gives psi"),
    ("E3-c093", "L05", "205 (printed V0 = 80/49); 270-273 (Problem E1)", "V0 = 80/49 recomputed exactly; grade C matches key results row 303"),
    ("E3-c094", "L05", "223-225 (printed EIS); code 128-133 (eis_numeric over [0.999, 1.001] c1)", "0.5000, 2.0000, 0.2500 printed by twin run; grade C"),
    ("E3-c095", "L05", "219-222 (printed U, V0 for (4,4), (1,10))", "U = -0.25 / -0.55 and V0 = 4.0000 / 4.3311 recomputed; grade C"),
    ("E3-c096", "L05", "213-216 (printed CE1 at gamma 0.5, 2, 3)", "2.2500, 1.6000, 1.3720 recomputed; falling in gamma; grade C"),
    ("E3-c169", "L05", "206 (printed U = -49/80); 273 (Problem E1)", "U = -49/80 recomputed exactly; grade C matches lesson"),
    ("E3-c170", "L05", "209 (printed CE1 = 8/5); 45 (Remark 1.5)", "CE1 = 8/5 recomputed exactly; grade C"),
    ("E3-c184", "L05", "226 (printed True); code 195-198 (closed form vs numeric MRS)", "closed form 4/9 agrees with numeric MRS; grade C"),
    ("E3-c185", "L05", "209 (printed mean 5/2); 45 (Remark 1.5)", "mean of c1 = 5/2 recomputed; grade C"),
    # ---- L06 ----
    ("E3-c098", "L06", "22-23 (Def 1.1)", "gain and loss relative to r; r = 0 in cents"),
    ("E3-c099", "L06", "25-27 (Def 1.2)", "power value function with alpha, delta, lambda > 0, v(0) = 0"),
    ("E3-c100", "L06", "28-29 (Def 1.3)", "prospect value W = sum p_i v(x_i), probabilities unweighted"),
    ("E3-c101", "L06", "30-33 (Prop 1.4)", "strictly increasing, concave on [0, inf), convex on (-inf, 0]; lambda > 0"),
    ("E3-c102", "L06", "34-35 (Remark 1.5)", "|v(-x)|/v(x) = lambda when alpha = delta"),
    ("E3-c103", "L06", "36-37 (Def 1.6)", "loss aversion; lambda > 1 when alpha = delta"),
    ("E3-c104", "L06", "40-43 (Prop 2.1)", "lambda* = pg/((1-p) l); W decreasing in lambda; recomputed"),
    ("E3-c105", "L06", "44-47 (Prop 2.2)", "lambda* = p g^alpha/((1-p) l^delta) and the sign pattern"),
    ("E3-c106", "L06", "48-49 (Ex 2.3); 156-161 (printed W values)", "W = 200, 50, -100 and lambda* = 5/3 recomputed; grade C"),
    ("E3-c107", "L06", "50-51 (Remark 2.4)", "CE and W have the same sign for every alpha, delta, lambda > 0"),
    ("E3-c108", "L06", "52-53 (Remark 2.5)", "combined 700 - 300 lambda, separate 1000 - 600 lambda; 100 and -200 at lambda = 2"),
    ("E3-c109", "L06", "53 (Remark 2.5)", "narrow framing definition matches"),
    ("E3-c110", "L06", "175-176 (Remark 3.1)", "no result of Sections 1-2 needs lambda > 1"),
    ("E3-c111", "L06", "178 (Remark 3.2)", "value (1/2) 800^alpha (1 - lambda); sign changes at lambda = 1"),
    ("E3-c112", "L06", "186-187 (section 5, first misconception)", "negative only above lambda*; W = 50 at lambda = 3/2"),
    ("E3-c113", "L06", "178 (Remark 3.2)", "lambda_R = sqrt(2)/2 = 0.7071 recomputed from the Remark formula"),
    ("E3-c116", "L06", "167-169 (printed threshold 1.2910, W = -8.6835); code 121-127", "sqrt(5/3) = 1.29099 and W = -8.68351 recomputed; grade C"),
    ("E3-c117", "L06", "170-172 (printed grid checks); code 128-153", "four gains and four losses; finite checks, grade C"),
    ("E3-c163", "L06", "53 (Remark 2.5)", "integrated evaluation definition matches"),
    # ---- L07 ----
    ("E3-c118", "L07", "23-24 (Def 1.1)", "weighting function: nondecreasing, omega(0) = 0, omega(1) = 1"),
    ("E3-c119", "L07", "25-28 (Def 1.2)", "V_omega = sum omega(p_i) v(x_i); EU is the case omega(p) = p"),
    ("E3-c120", "L07", "29-32 (Remark 1.3)", "identity weighting gives expected value of v(X)"),
    ("E3-c121", "L07", "35-40 (Ex 1.4)", "closed form; omega(3/10) = 0.2857908849, omega(3/5) = 0.3912507700, omega(1/2) = 0.3535533906 recomputed"),
    ("E3-c122", "L07", "41-42 (Obs 1.5); 196 (printed sign changes 1, last point 0.278)", "finite-grid check recomputed; grade C"),
    ("E3-c123", "L07", "44-45 (Remark 1.6)", "2 omega(3/10) = 0.57158177 vs 0.6 under identity; sum 0.89103669 recomputed"),
    ("E3-c124", "L07", "47-54 (Ex 2.1 table)", "F_B <= F_A at 0, 50, 100; strict at 50 (7/10 vs 2/5)"),
    ("E3-c125", "L07", "55-64 (Prop 2.2)", "ratio 0.7304544982 exceeds 2/3 and 0.58578644; recomputed"),
    ("E3-c126", "L07", "65-66 (Remark 2.3)", "identity gives 45 (A) and 60 (B) at alpha = 1"),
    ("E3-c127", "L07", "202-203 (printed Part C values)", "42.8686, 39.1251, 4.8788, 3.9125 recomputed; grade C"),
    ("E3-c128", "L07", "165-179 code part_d; 204 (printed 10 of 10); 205 (limits)", "ten nondecreasing utilities, all agree; finite family"),
    ("E3-c129", "L07", "47 (Lesson 4 Theorem 1.5 cited)", "Lesson 4 Thm 1.5 (course/modules/E/E3/L04.html line 89) gives the FOSD equivalence on finite support"),
    ("E3-c130", "L07", "44-45 (Remark 1.6); 211-212 (section 4, first misconception)", "re-checked after the round-11 change: only derived values, recomputed to 8 decimals; grade T matches"),
    ("E3-c131", "L07", "250-253 (E2 solution: 40-digit values, 8-decimal values)", "3.74355573 (40-digit) and 3.74355574 (8-decimal) recomputed by Decimal; both give 3.7436"),
    ("E3-c132", "L07", "216 (section 4, third misconception)", "49.83277 against EV 50.5 recomputed; graded T as the lesson states"),
    ("E3-c133", "L07", "207 (section 3); 260-262 (Problem R1)", "affine weighting with the endpoints is the identity; omega(1/2) != 1/2"),
    ("E3-c134", "L07", "33 (Kahneman and Tversky used for the title only)", "registry kahneman1979prospect: Crossref title 'Prospect Theory: An Analysis of Decision under Risk', 1979"),
    ("E3-c135", "L07", "263-266 (Problem R2)", "Tail_A(50) = Tail_B(50) = 3/5, Tail_B(100) = 3/5 > 3/10 recomputed"),
    ("E3-c187", "L07", "250-253 (E2); 205 (printed values)", "printed 42.8686 - 39.1251 = 3.7435 while unrounded gives 3.7436; grade C"),
    # ---- L08 ----
    ("E3-c136", "L08", "23-24 (Def 1.1)", "prior set; two-outcome prior is p in [0, 1]"),
    ("E3-c137", "L08", "26-27 (Def 1.2)", "V_tau = tau min + (1 - tau) max of E_P u(f)"),
    ("E3-c138", "L08", "29-35 (Prop 1.3)", "one-element prior set gives expected utility for every tau"),
    ("E3-c139", "L08", "36-37 (Ex 1.4)", "average prior P(red) = 45/90 = 1/2 recomputed"),
    ("E3-c140", "L08", "41 (Def 2.1)", "ambiguity aversion: CE(f) <= CE at the average prior"),
    ("E3-c141", "L08", "43-47 (Thm 2.2 with A1-A3)", "maxmin CE at most the average-prior CE"),
    ("E3-c142", "L08", "49 (strict case of proof); 50-51 (Remark 2.3)", "one prior: equality; strict with different expected utilities"),
    ("E3-c143", "L08", "54-57 (Prop 2.4 with A1-A3); 59 (proof)", "worst prior P_0 for red, P_90 for black"),
    ("E3-c144", "L08", "61 (Ex 2.5)", "30 red of 90, CE = 103125 recomputed exactly"),
    ("E3-c145", "L08", "66-68 (Def 3.1 and timing convention)", "date-1 gamble, a = 1 - 1/psi"),
    ("E3-c146", "L08", "70-76 (Prop 3.2 A1-A5); 324-325 (section 6, third misconception)", "EZ CE equals CRRA CE; no psi, beta, c0"),
    ("E3-c147", "L08", "80 (Remark 3.3)", "earlier resolution: random continuation value; dependence an untested hypothesis"),
    ("E3-c148", "L08", "303 (Model 4); 311-312 (Remark 4.2); 318", "alpha-MEU at tau = 1/2 equals EU at the midpoint 1/2; not general"),
    ("E3-c149", "L08", "297 (Model 1)", "4180000/41 = 101951.2195 recomputed exactly"),
    ("E3-c150", "L08", "299 (Model 2)", "5 - sqrt(50) = -2.071068 recomputed"),
    ("E3-c151", "L08", "303 (Model 4)", "maxmin CE 99523.8095 at P(red) = 1/3 recomputed exactly"),
    ("E3-c152", "L08", "313 (risk premium); 366 (E3)", "548.7805 cents = 5.4878 CU recomputed (22500/41)"),
    ("E3-c153", "L08", "278-285 (printed Part B gaps); 325 (misconception 3)", "101951.219512 and max gap 2.91e-11 printed; grade C"),
    ("E3-c154", "L08", "321 (section 6, first misconception); 57 (Prop 2.4)", "worst prior depends on the bet"),
    ("E3-c155", "L08", "45 (Thm 2.2 A2); 379 (Problem R3)", "Theorem 2.2 uses u only through A2 (strictly increasing)"),
    ("E3-c157", "L08", "62 (Ex 2.5 paragraph on Ellsberg 1961)", "registry ellsberg1961risk, Crossref title 'Risk, Ambiguity, and the Savage Axioms', 1961; title-only attribution"),
    ("E3-c158", "L08", "28 (Def 1.2 paragraph on Gilboa and Schmeidler)", "registry gilboa1989maxmin, Crossref title 'Maxmin expected utility with non-unique prior', 1989; title-only"),
    ("E3-c164", "L08", "61 (Ex 2.5); 289 (printed maxmin 100000.0000)", "100000 for both colours; worst priors P_0 and P_90"),
    ("E3-c165", "L08", "61 (Ex 2.5); 290 (printed preference True)", "known urn preferred for both colours"),
    ("E3-c166", "L08", "299 (Model 2); 307 (table)", "-107.2330 cents change; wealth 99892.7670 recomputed"),
    ("E3-c172", "L08", "28 (Def 1.2, tau = 1 gives the minimum)", "V at tau = 1 is the minimum expected utility"),
    ("E3-c179", "L08", "301 (Model 3); 273 (printed CE); 70-76 (Prop 3.2)", "101951.2195 at psi = 1/2, beta = 0.95, gamma = 2"),
    ("E3-c182", "L08", "61 (Ex 2.5)", "known black CE 1/((2/3)/110000 + (1/3)/100000) = 106451.6129 recomputed"),
]

LESSON_ROWS: list[tuple[str, str, str, str, str]] = [
    (
        "E3g12-L05-prose-numbers",
        "2.2 numbers in L05 prose",
        f"{SCR}/L05.txt lines 45, 48-56, 209, 213-226, 240, 273-281",
        "PASS",
        f"Every number in L05 prose recomputed with Fractions and floats: {RECOMP}. The 16/7 and 160/71 variant, mean 5/2, 8/5, 12/5 (5/8 and 5/12), EIS 0.5/2/0.25, CE1 2.25/1.6/1.372, V0(4,4)=4.0, V0(1,10)=4.3311.",
    ),
    (
        "E3g12-L06-prose-numbers",
        "2.2 numbers in L06 prose",
        f"{SCR}/L06.txt lines 49, 51-53, 155-172, 178, 187, 198, 232, 241, 245",
        "PASS",
        f"Recomputed in {RECOMP}: W = 200/50/-100 at lambda 1, 3/2, 2; lambda* = 5/3; sqrt(5/3) = 1.2910; W = -8.6835; combined 100 and separate -200; lambda_R = 0.7071; M1 3/2 and -100; M2 -50.",
    ),
    (
        "E3g12-L07-prose-numbers",
        "2.2 numbers in L07 prose",
        f"{SCR}/L07.txt lines 35-64, 42-45, 186-203, 216, 223-227, 249-257, 305, 308",
        "PASS",
        f"Recomputed in {RECOMP} and {SCR}/recompute_r12.out: omega values to 10 decimals; 40-digit Decimal values of Gamma(A), Gamma(B) and their difference 3.74355573; 8-decimal difference 3.74355574; ratio 0.7304544982; eta = 1 closed-form gap 0.3126 at p = 0.862; sign changes 1 and last point 0.278; overweight 7.3403, underweight 8.0075, net -0.6672, weighted value 49.8328.",
    ),
    (
        "E3g12-L08-prose-numbers",
        "2.2 numbers in L08 prose",
        f"{SCR}/L08.txt lines 37, 51, 61-62, 82, 293, 297-313, 332-336, 358-366, 375, 401-443",
        "PASS",
        f"Recomputed in {RECOMP}: 4180000/41; 5 - sqrt(50); 99892.7670; 99523.8095; 103125; 106451.6129; 98352.94 (p = 1/4); 105822.78 (p = 3/4); 22500/41; 1/2 average prior; 4.44e-16 closed-form gap is the lab output.",
    ),
    (
        "E3g12-L05-L08-key-results",
        "2.3 grades in the Key results tables of L05-L08 against proofs and lab output",
        f"{SCR}/L05.txt 297-305; L06.txt 248-255; L07.txt 273-279; L08.txt 382-390",
        "PASS",
        "Each T row cites a proof in the same lesson that I re-read (L05 Thm 1.3, Cor 1.4, Prop 2.2, Remarks 2.3, 3.1, 3.4, Thm 3.2, Cor 3.3; L06 Prop 1.4, Remark 1.5, Props 2.1, 2.2, Remarks 2.4, 2.5; L07 Remark 1.3, Ex 1.4, Remark 1.6, Prop 2.2; L08 Prop 1.3, Thm 2.2, Prop 2.4, Prop 3.2, Remark 4.2). Each C row names its lab or example, and the lab-printed numbers match the twin output.",
    ),
    (
        "E3g12-L05-L08-problem-solutions",
        "2.4 problem solutions the cards rely on (M, P, E, R)",
        f"{SCR}/L05.txt 244-268, 270-281; L06.txt 195-216, 221-232; L07.txt 220-243, 246-257; L08.txt 329-366",
        "PASS",
        "Re-derived by hand and by script: L05 M1 (CE1 2), M2 (V0 3/2), M3 (theta -2), E1 (V0 80/49, U -49/80), E2 (16/7, 160/71), E3 (EIS procedure); L06 M1 (3/2, -100), M2 (EV 0, W -50), M3 (2 and -8); L07 M1 (1/(2+sqrt3)), M2 (35.355339), M3 (endpoints), E1 (crossing in (0.278, 0.279)), E2 (3.7436), E3 (ETA = 1 gives identity, gap 3.13e-1); L08 M1 (8360000/85), M2 (98352.94, 105822.78), M3 (105822.78), E1 (3125 cents), E3 (22500/41).",
    ),
    (
        "E3g12-L05-L08-quiz-keys",
        "2.9 retrieval quiz answer keys in L05-L08",
        f"{SCR}/L05.txt 306-367; L06.txt 256-308; L07.txt 280-335; L08.txt 391-443",
        "PASS",
        "Every quiz key read against its lesson section: correct options match Def/Prop/Remark numbers cited in the key (e.g. L05 'psi = 1/gamma' restriction, L06 'lambda_R' sign at lambda = 1, L07 'B' dominates, L08 'maxmin CE 99523.81').",
    ),
    (
        "E3g12-lab-twins-run",
        "2.5 labs: twins alone under python -I -W error (lessons whose cards are in this slice)",
        "tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L07-1.py, lab-E3-L08-1.py",
        "PASS",
        f"Each run with .venv/bin/python -I -W error: exit 0, stderr 0 bytes. stdout saved to {SCR}/twin-L0x.out. Expected blocks in the lessons compared line by line with the twin output ({SCR}/exp-L0x.txt): identical for L05, L06, L08; L07 differs only in the padding the strip script collapsed (verified against raw L07.html lines 300-315).",
    ),
    (
        "E3g12-check-pages-dag-projects",
        "2.9 structure and DAG: check_pages, check_dag, check_projects for E3",
        f"tools/check_pages.py --unit E3; tools/check_dag.py --unit E3; tools/check_projects.py --unit E3",
        "PASS",
        f"Outputs: {SCR}/check_pages_E3.out (check_pages E3: PASS), {SCR}/check_dag_E3.out (check_dag E3: PASS), {SCR}/check_projects_E3.out (check_projects E3: PASS). check_pages checks cards.json ids, lesson existence, grade validity and that every cite key is in the registry.",
    ),
    (
        "E3g12-verify-refs",
        "2.1 citations used by the cards: offline integrity and live Crossref",
        "references/references.json keys ellsberg1961risk, gilboa1989maxmin, kahneman1979prospect; tools/verify_refs.py --offline",
        "PASS",
        f"verify_refs.py --offline: 560 entries, 0 problems ({SCR}/verify_refs_offline.out). Live Crossref (plain curl, no contact data): HTTP 200 for 10.2307/1884324, 10.1016/0304-4068(89)90018-9, 10.2307/1914185; titles, years and authors match the registry records ({SCR}/crossref_titles_r12.out).",
    ),
    (
        "E3g12-L04-theorem-cross-lesson",
        "2.7/2.9 cross-lesson target of card E3-c129 (Lesson 4 Theorem 1.5)",
        "course/modules/E/E3/L04.html line 89 (Theorem 1.5, first-order dominance on a finite support)",
        "PASS",
        "The L04 theorem is stated as the FOSD equivalence on a finite support for nondecreasing u (line 89 and the reference at line 629); card E3-c129 states the direction used by L07 and cites Theorem 1.5 by number as L07 does.",
    ),
    (
        "E3g12-notation",
        "2.4/2.9 notation: symbols in L05-L08 against notation/notation.json",
        "notation/notation.json (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); L05-L08 text and cards",
        "PASS",
        f"Registered symbols searched in the L05-L08 text ({SCR}/L0x.txt) and cards: none of T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q occurs. The local symbols alpha, beta, gamma, delta, lambda, eta, omega, tau, psi, Gamma, theta and nu are conventionally local per the registry 'about' field; lambda* (L06) and R^* are different symbols. No collision.",
    ),
    (
        "E3g12-scope-words-cards",
        "2.9 scope words (only, all, always, every, any, same, exactly) in the L05-L08 cards",
        f"{CARDS} E3-c080..E3-c187 (L05-L08)",
        "PASS",
        "Every scope word in a card back checked against its lesson locator: 'every psi and beta' (Prop 3.2 A1-A5, L08 lines 70-76), 'every deterministic plan exactly when 1/psi = gamma' (Remark 3.4, L05 line 70), 'for every alpha, delta, lambda' (Remark 2.4, L06 line 51), 'every lambda > 0' (Remark 3.1, L06 line 176), 'all six gaps' (printed, L08 line 285), 'every one' (ten utilities, L07 line 204). No unsupported scope.",
    ),
    (
        "E3g12-process-words-cards",
        "2.9 process words in learner text (cards and L05-L08)",
        f"{CARDS} L05-L08 cards; {SCR}/L05.txt-L08.txt",
        "PASS",
        "grep for round, verifier, builder, ledger, fragment, checkout, pin, agent, claude over the L05-L08 cards and lesson text: the cards contain only 'Lab' (the lesson's own lab name) and 'agent' in E3-c154 (decision-theory sense); the only 'round' hit is the lab docstring sentence about rounding to whole cents (L08.txt line 88), which is not a process word.",
    ),
    (
        "E3g12-dup-scan",
        "2.7 full scan for duplicate cards (all 178 E3 cards)",
        f"{CARDS} (178 cards); {SCR}/dup_scan.py (output {SCR}/dup_scan.out)",
        "PASS",
        "178 unique ids, 178 unique fronts, 178 unique backs. No literal duplicates. Near-duplicate pairs inside L05-L08 that I read are different questions: E3-c144 (red bet 103125) vs E3-c182 (black bet 106451.6129); E3-c150 (prospect value) vs E3-c166 (wealth equivalent); E3-c164 vs E3-c165; E3-c080 vs E3-c082 (CE1 and the mean); E3-c146 (general) vs E3-c179 (the Section 4 instance); E3-c131 vs E3-c187 (3.7436 vs why 3.7435 is printed). Overlaps noted, not duplicates.",
    ),
    (
        "E3g12-card-numbers",
        "2.7 every number on a card appears in its lesson (token match)",
        f"{CARDS} L05-L08 cards; {NUMS}",
        "PASS",
        f"{SCR}/card_numbers_bounded.py: for all 88 cards in L05-L08, every number in front and back occurs as a token in its own lesson text (0 misses).",
    ),
    (
        "E3g12-delta-round12",
        "delta since ccaeeaf4 for the slice: cards, L05, L07 and their lab twin",
        "git diff ccaeeaf4..329c1d7f: course/modules/E/E3/cards.json (c049 is L03, outside; c130 changed), L05.html (1 sentence, line 165-167), L07.html (E2 solution), tests/labs/E3/lab-E3-L05-1.py (docstring)",
        "PASS",
        "Every hunk in the slice read: cards.json c130 (back text now without lab-printed numbers; re-checked, PASS), L05.html docstring-like sentence 'every value is a plain number with no units attached' (L05.txt line 76; no card depends on it), L07.html E2 solution (L07.txt lines 252-253; re-derived, PASS), lab-E3-L05-1.py docstring (L05.txt lines 73-84; re-run, PASS). L06 and L08 lessons and twins are byte-identical since ccaeeaf4 (not in the diff).",
    ),
    (
        "E3g12-r11-c130-grade-resolved",
        "prior-round FAIL E3g11-c130-grade (grade T on a card carrying lab-printed values)",
        f"{CARDS} E3-c130; {SCR}/L07.txt lines 44-45, 211-212",
        "PASS",
        "The round-11 FAIL is resolved: the back of E3-c130 no longer carries the lab-printed 42.8686 and 39.1251. The remaining numbers 0.57158177 and 0.39125077 are derived on the page from the closed form of Example 1.4 (Remark 1.6 says 'from unrounded values') and recomputed to 8 decimals here, so grade T is consistent with BLUEPRINT section 3.",
    ),
    (
        "E3g12-c131-basis-note",
        "2.3 grade of E3-c131 (C, basis Lab 1 part C and Problem E2)",
        f"{CARDS} E3-c131; {SCR}/L07.txt lines 250-253",
        "PASS",
        "The 40-digit values 42.86863274... and 39.12507700... are not printed by Lab 1 (the lab prints 4 decimals; L07.txt line 253 says so). The grade C is the conservative choice and the basis names Problem E2 and the 40-digit difference; the value itself is reproduced by Decimal in recompute_r12.py. Not a mismatch that misleads a reader; recorded so that a later round can decide whether it should be T.",
    ),
]

# Card rows: one row per card, all checked by reading card and lesson.
rows: list[dict[str, str]] = []
for cid, lesson, locator, note in CARD_ROWS:
    rows.append(
        {
            "id": f"E3g12-{cid.split('-')[1]}",
            "check": f"2.7 retrieval card {cid} against {lesson}",
            "location": f"{CARDS} {cid}; course/modules/E/E3/{lesson}.html via {SCR}/{lesson}.txt lines {locator}",
            "status": "PASS",
            "evidence": f"Read the card and {lesson} lines {locator} (strip.py of {lesson}.html, read in full). {note}. Numbers in the card recomputed (see E3g12-card-numbers, {RECOMP}).",
        }
    )
for rid, check, location, status, evidence in LESSON_ROWS:
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})

assert len({r["id"] for r in rows}) == len(rows), "duplicate row ids"

fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 12,
    "verifier": "Haiku 5.5 independent verifier, E3-g round 12 (did not build E3)",
    "pin": "329c1d7feac5479403c351e64587c867278452cc",
    "base": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87 (round-11 pin; delta from it read in full)",
    "checkout": str(CHECKOUT),
    "scratch": f"{CHECKOUT}/{SCR}",
    "verified_at": "2026-11-09T00:22:40+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: the E3 retrieval cards of L05-L08 (88 cards: L05 22, L06 19, L07 19, L08 28), each read against its lesson, plus the lesson-level checks needed to ground them (numbers, key-results grades, problem solutions, quiz keys, lab twins, structure, references, notation, duplicates).",
        "Delta ccaeeaf4 to 329c1d7f inside the slice: cards.json c130 (round-11 FAIL, now resolved), L05.html one sentence, L07.html E2 solution, lab-E3-L05-1.py docstring. L06.html and L08.html, and the L06, L07 and L08 lab twins, are unchanged since the round-11 pin (git diff); L07.html changed (E2 solution hunk, read in full).",
        "Round-11 rows: none carried. Every card row was re-verified this round from the current text; the round-11 FAIL E3g11-c130-grade is re-checked and now PASS.",
        "No mutants: this slice is lessons and retrieval cards, not a project grader. Lab twins are demonstrations (VERIFIER rulings), so no mutation test applies.",
        "Not checked in this slice: the L05-L08 page code against the twins beyond the expected-block comparison (run_labs.py was not run as a tool); page_smoke.py on L05-L08 pages; L01-L04 cards; the E3 project and its grader (other slices); ruff, mypy and pytest (no Python tool or test changed in this slice's scope); render_curriculum and build_site --check (CURRICULUM.md, site data are not in this slice); hub hours arithmetic (hub index.html is not in this slice's delta).",
        "Lesson-level rows (E3g12-L0x-prose-numbers etc.) cover the claims the cards rely on; they do not re-grade every lesson paragraph. Lesson prose outside the cards' subject matter (for example L05 section 4 and L08 section 5 commentary) was read in full but not row-by-row.",
        "Live Crossref was reached with plain curl for the three cited DOIs only; no bot check, login or paywall was encountered.",
    ],
    "summary": {},
}

from collections import Counter  # noqa: E402

counts = Counter(r["status"] for r in rows)
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts.get("PASS", 0),
    "fail": counts.get("FAIL", 0),
    "unverifiable": counts.get("UNVERIFIABLE", 0),
    "card_rows": len(CARD_ROWS),
    "lesson_rows": len(LESSON_ROWS),
    "mutants": 0,
    "mutants_killed": 0,
}
OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {OUT} rows={len(rows)} pass={counts.get('PASS', 0)}")
