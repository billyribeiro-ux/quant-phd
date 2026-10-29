import json, pathlib
S = "ledgers/M2/scripts/M2-c-r7/"
C = "Carried from round 6 (L14.html, L15.html, L17.html, their lab twins and their cards byte-identical since pin 44f1eb6; cards compared per id in card_delta_and_dups.out): "
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

row("M2c-gate-check-pages", "2.9-structure", "tools/check_pages.py --all", "PASS",
    S + "check_pages.out: 'check_pages M2: PASS' (re-run at pin 7aa909e).")
row("M2c-gate-check-dag", "2.9-dag", "tools/check_dag.py --all", "PASS",
    S + "check_dag.out: 'check_dag M2: PASS'. The round-7 edits add no concept link; L16 R3 and L18 R3 cite Lesson L13, which is in the prerequisite closure (L16 uses L13; L18 uses L16). Prerequisite definitions: def-derivative L04, def-taylor-theorem L08, limit L01.")
row("M2c-gate-run-labs", "2.5-labs", "tools/run_labs.py --unit M2", "PASS",
    S + "run_labs_M2.out: 'run_labs M2: PASS (27/27)'.")
row("M2c-labs-twin-isolated", "2.5-labs", "tests/labs/M2/lab-M2-L13-1.py .. lab-M2-L18-1.py", "PASS",
    S + "twins_isolated.out: each twin run as .venv/bin/python -I -W error exits 0 with 0 bytes stderr. " + S + "twin_vs_page.out: page code == twin file and page expected block == twin output for L13..L18 (script twin_vs_page.py).")
row("M2c-gate-page-smoke", "2.9-smoke", "tools/page_smoke.py --unit M2 --pages L13 L14 L15 L16 L17 L18", "PASS",
    S + "page_smoke.out: 'page_smoke M2: PASS'; each of the six pages PASS; lab times 0.0 s.")
row("M2c-gate-ruff-mypy-pytest", "2.5-labs", "ruff check/format tests/labs/M2; mypy --no-incremental on the six L13-L18 twins; pytest tests/test_labs.py -k M2", "PASS",
    S + "ruff_check.out (exit 0), " + S + "ruff_format.out (exit 0), " + S + "mypy.out 'Success: no issues found in 6 source files', " + S + "pytest_labs_M2.out (27 passed, exit 0).")
row("M2c-verify-refs", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    S + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems'. The References sections of L13-L18 cite no registry key (text re-read; unchanged in round 7).")
row("M2c-banned-scan", "1.3-1.4-banned", "course/modules/M/M2/L13..L18.html visible text and cards.json L13-L18 entries", "PASS",
    S + "banned_scan_r7.py / banned_scan_r7.out: 51 pattern hits, all of three kinds: 'approximation' (mathematical term), 'previous' (lesson-nav link), and an ellipsis in an L15 lab docstring (unchanged page). No TODO, TBD, placeholder, process word (verifier, builder, round, revised, corrected, changed, now) in visible text or cards.")
row("M2c-scope-words", "2.9-scope-words", "changed sentences in L13 (Sec 3, Cor 4.1, M3, Sec 5, Misconception 2), L16 (R3, Lab hypothesis), L18 (Assumption 1, R3, M2, R1)", "PASS",
    "Changed scope words re-checked in context: L13 'all three are stated in it' (the proof uses exactly the three hypotheses: triangle inequality needs no hypothesis, evaluation bound, exact subtraction/division, exact points); L13 Cor 4.1 'smallest ... provided h* <= h0' and 'for delta > 0 and M > 0' (B''>0 gives the minimum); L13 M3 'needs sin to be increasing on [0,0.01], which this page does not state' (honest); L18 R3 'provided M bounds the third derivatives of every component in the same neighborhood'. Carried for L14, L15, L17 (byte-identical).")
row("M2c-notation", "2.4-notation", "notation/notation.json vs L13-L18 text", "PASS",
    "notation.json registers T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q. grep over L13, L16, L18 (round-7 pages) finds 0 uses of each; L14 uses \\ast in its own (unchanged) text. \\R is used only as the real numbers. New symbols in the round-7 text (delta, xi, M_3, h_0, f-tilde, D-tilde_h, C-tilde_h, B, B_c, J_F, K, omega) are each defined where used.")
row("M2c-structure-order", "2.9-structure", "BUILDER_RULES 4.2 order in L13-L18", "PASS",
    S + "structure_r7.out: all six pages in order why-it-matters, core s1, lab, canon-breaks, misconceptions, problem-set, key-results, quiz, references.")
row("M2c-why-it-matters-length", "2.9-structure", "why-it-matters paragraph of L13-L18", "PASS",
    S + "structure_r7.out: word counts 106, 102, 89, 95, 83, 107 (all at most 120); the L13, L16, L18 paragraphs are unchanged by the round-7 diff.")
row("M2c-misconceptions", "2.9-structure", "misconceptions sections of L13-L18", "PASS",
    S + "structure_r7.out and the page text: three misconception items per page. L13 Misconception 2 re-computed: unrounded forward/central ratio 301.0010 (numcheck_L13.out), printed-digit ratio 301.10 (printed values 1.364e-2/4.530e-5). L13 Misconception 1: 2.154e-7/6.603e-9 = 32.62 (numcheck_L13.out).")
row("M2c-problem-tiers", "2.9-structure", "problem-set tiers of L13-L18", "PASS",
    S + "structure_r7.out: 12 problem blocks and 12 details.solution blocks per page (3 each in Mechanics, Proof, Empirical, Research).")
row("M2c-quiz", "2.9-structure", "retrieval quizzes of L13-L18", "PASS",
    "Carried from round 6 for L14, L15, L17 (byte-identical pages). Re-verified in round 7 for L13, L16, L18: " + S + "structure_r7.out shows quiz items L13 10, L16 10, L18 9 (8-15 required) and an explain div per item; every numeric answer re-derived: L13 2.5 (f(1.5)=2.25, f(1)=1), 2 (two values), 0.1 (f''=2, 0.1/2*2); L16 5, 2, 0.25, 4; L18 3 ((2,3) entry 2,1 of J = y = 3), 1 (cos 0). Correct option of each mc item re-read against its explain text.")
row("M2c-hours", "2.9-hours", "data-hours on L13-L18; hub index.html", "PASS",
    "All six pages carry data-hours=10 (structure_r7.out). Hub course/modules/M/M2/index.html line 29: data-hours-lessons=240, data-hours-project=60; 24 lessons x 10 h = 240 and 240 + 60 = 300. The round-7 hub diff changes only the L11 card title (outside this slice).")
row("M2c-card-duplicates", "2.7-cards", "course/modules/M/M2/cards.json (all 380 cards)", "PASS",
    S + "card_delta_and_dups.out: 380 cards, 0 duplicate ids, 0 duplicate fronts, 0 duplicate backs. Slice counts: L13 23, L14 18, L15 19, L16 11, L17 14, L18 15.")
row("M2c-cards-L13", "2.7-cards", "cards.json, lesson L13 (M2-c181..c201, c380, c381)", "FAIL",
    "Card M2-c187 (cards.json line 1308) gives the balanced central bound's derivative and its zero at h* = (3 delta/M_3)^(1/3) with no hypotheses. Lesson L13 line 143 (round-7 edit) now states 'For delta > 0 and M_3 > 0, its smallest value is at h*', and P3 (line 301) states 'delta > 0 and M_3 > 0'. The card's claim divides by M_3 and is false for delta = 0 (the bound has no interior minimum), so it fails rule 10 (cards carry the proposition's hypotheses). Cards c185 (line 1294), c186, c194, c196 and the new c380, c381 were re-read against the lesson and are correct.",
    "In M2-c187 back (cards.json line 1308), prefix the statement with the hypotheses: 'For delta > 0 and M_3 > 0 (Lesson L13, Section 4), the bound (M_3/6) h^2 + delta/h has derivative (M_3/3) h - delta/h^2, which vanishes at h* = (3 delta/M_3)^(1/3), the minimizer.' Keep the rest of the back.")
row("M2c-cards-L14", "2.7-cards", "cards.json, lesson L14 (M2-c202..c219)", "PASS",
    C + "per-card comparison with the pin shows no L14 card changed (card_delta_and_dups.out lists only L02, L04, L05, L06, L07, L09, L12, L13, L18, L20, L22, L23, L24 ids as changed).")
row("M2c-cards-L15", "2.7-cards", "cards.json, lesson L15 (M2-c220..c238)", "PASS",
    C + "no L15 card changed (card_delta_and_dups.out).")
row("M2c-cards-L16", "2.7-cards", "cards.json, lesson L16 (M2-c239..c249)", "PASS",
    "Round 7 removed card M2-c250 (L16 canon-break 3 content remains in the lesson text). The 11 remaining cards were re-read against L16 text: c241 F_x, F_y and 18.778112198 / 8.389056099 (Example 1.3, Assumption 1 stated); c242 hypotheses match Prop 2.1; c243 matches Prop 3.1 and Example 3.4 of L15; c244 matches lab output 18.778112 / 8.389056 and 'below 1e-06' (lab True); c245 matches axis quotients 0.0; c247 f(x,x)=x^2, derivative 2 at 1 (Misconception 2); c248 Misconception 1; c249 Misconception 3. No card number is absent from L16.")
row("M2c-cards-L17", "2.7-cards", "cards.json, lesson L17 (M2-c251..c264)", "PASS",
    C + "no L17 card changed.")
row("M2c-cards-L18", "2.7-cards", "cards.json, lesson L18 (M2-c265..c279)", "PASS",
    "All 15 cards re-read. Changed card M2-c277 (line 1956) now says 'under Assumption 1 (the derivatives of sin and cos)', matching L18 line 250 (Assumption 1 with both derivatives) and Problem R1 (line 333). Remainder card c270 ([[2,-4],[4,2]], |h|^2) matches Example 4.2; c271/c272/c273 match lab output rows and remainder ratios; c269 hypotheses match Theorem 4.1.")
row("M2c-L13-numbers", "2.2-numbers", "L13 prose numbers: Example 2.3, E1, E2, E3, R1, R3, Section 5, Misconceptions, Key results", "PASS",
    S + "numcheck_L13.py / numcheck_L13.out: exp at 1, h=1e-2: forward error 0.0136368 (interval 0.0135914..0.0137280), central error 4.53049e-5 (interval 4.4854e-5..4.5760e-5); h*_fwd=1.80760e-8 (text 1.8e-8); h*_cen=6.25781e-6 (text 6.3e-6, nearer 1e-5 on log scale); 2^-53/1e-8=1.1102e-8 and e times it = 3.0179e-8 (R3, Section 5 '3.0e-8'); 2sqrt(M delta)=4.9136e-8 ('4.9e-8'); 2delta/h at 1e-9 = 4.4409e-7, truncation 1.3591e-9, ratio 326.7 (E2 'about 327'); R1 h* = 0.0383604 ('0.038360'); E3 3delta/e=2.45057e-16, cube root 6.2578e-6; Ex 2.3 intervals; E1 bounds 10e^{-0.001}=9.990, 10e^{0.01}=10.101, 100e^{-0.011}=98.91, 100e^{0.011}=101.11. Misconception 1 ratio 32.6; Misconception 2 unrounded 301.0, printed 301.1.")
row("M2c-L13-lab1", "2.5-labs", "L13 Lab 1 hypothesis, expected block, interpretation", "PASS",
    S + "twin_vs_page.out (expected == output). Interpretation re-checked against the expected block: forward column falls ~10x per decade from 1e-1 to 1e-7 (values 1.359e-4 .. 1.399e-7); smallest forward 6.603e-9 at 1e-8, 2.154e-7 at 1e-9, 1.548e-6 at 1e-10; central falls ~100x from 1e-1 to 1e-4; smallest central 5.858691e-11 at 1e-5 vs 5.858736e-11 at 1e-7 (difference 4.5e-16 < 1e-15, as the text says, computed by numcheck_L13.py). Ratios 10.03 in (9.990,10.101), 100.00 in (98.91,101.11).")
row("M2c-L13-theorems", "2.4-mathematics", "L13 Theorem 2.1, 2.2, Corollary 4.1, Proposition 3.2 (proof), P1, P2, P3, M1..M3 solutions", "PASS",
    "Re-derived by hand: Taylor order 1 gives (h/2) f''(xi); order 2 subtraction gives (h^2/12)(f'''(xi+)+f'''(xi-)), IVT point in (x-h,x+h); Prop 3.2 numerator difference <= 2 delta, divided by h or 2h; B'(h)=M/2-2delta/h^2, zero at h=2sqrt(delta/M), B''=4delta/h^3>0, B(h*)=2sqrt(M delta); B_c'=(M3/3)h-delta/h^2, h*=(3delta/M3)^(1/3), B_c(h*)=3delta/(2h*); P1 (3x^2+h^2, error h^2 = h^2/6*6); P2 (error h = h/2*2); M1 (2.1, 0.1); M2 (2ax+b); M3 sin(0.01)/0.01 - 1 = -1.66666e-5 (numcheck_L13.out), bound 0.005 (|sin|<=1), sharper 5.0e-5.")
row("M2c-L13-prop32-hypotheses", "2.4-mathematics", "course/modules/M/M2/L13.html lines 116, 122, 125, 133, 229, 367, 458; card M2-c185; card M2-c186", "PASS",
    "Round-6 FAIL resolved. Proposition 3.2 (line 116) now lists three hypotheses: evaluation error <= delta at x-h, x, x+h; subtraction and division exact; the three values taken at the exact points x-h, x, x+h. The proof (line 122) uses the nominal points; line 125 says 'three hypotheses ... all three are stated in it'; Corollary 4.1 (line 133) and Section 5 bullet 1 (line 229) name the third hypothesis as stated; Key-results row (line 367) and quiz Q10 explanation (line 458) agree. Cards M2-c185 and M2-c186 carry the same hypotheses.")
row("M2c-L14-numbers", "2.2-numbers", "L14 Example 4.1, Lab 1, E1, E3, key results", "PASS",
    C + "L14 numbers re-derived in round 6 (numcheck_L14.py); page and twin byte-identical.")
row("M2c-L14-lab1", "2.5-labs", "L14 Lab 1 hypothesis, expected block, interpretation", "PASS",
    C + "twin_vs_page.out confirms page code == twin and expected == output for L14 in round 7.")
row("M2c-L14-theorems", "2.4-mathematics", "L14 Definition 2.1, Prop 3.1, Prop 5.2, Example 5.1, Section 6", "PASS",
    C + "page and cards unchanged.")
row("M2c-L15-numbers", "2.2-numbers", "L15 Prop 3.5, Lab 1, E1, E2, E3", "PASS",
    C + "page and twin unchanged.")
row("M2c-L15-theorems", "2.4-mathematics", "L15 Prop 2.1, 2.2, Example 2.4, 3.3, 3.4, Prop 3.1, Cor 3.2, Problems", "PASS",
    C + "page unchanged; Corollary 3.2 and Proposition 2.1 exist as cited by L16 and L18 (xref_r7.out).")
row("M2c-L15-lab1", "2.5-labs", "L15 Lab 1", "PASS",
    C + "twin_vs_page.out confirms L15 page code == twin and expected == output.")
row("M2c-L16-numbers", "2.2-numbers", "L16 Example 1.3, Lab 1 hypothesis and interpretation, E1, E3, R3 numbers", "PASS",
    "Re-derived: e^2 = 7.389056; F_x(1,2)=4+2e^2=18.778112, F_y=1+e^2=8.389056; F_xxx = y^3 e^{xy}, at (2,1) max e^2 = 7.389 on the segment, truncation (1e-10/6)*7.39 = 1.23e-10 (E1); delta = 2^-52*... half spacing near 11.39 is 8.9e-16 (spacing 2^-49 in [8,16)), rounding 8.9e-11 (E1); F_yyy = x^3 e^{xy} at (2,1) = 8e^2 = 59.1, error 9.9e-10 (lab hypothesis); E3 F_xy = F_yx = 2x + e^{xy} + xy e^{xy}, 2+3e^2 = 24.167168 at (1,2); R3 truncation (1e-10/6)*20 = 3.33e-10, rounding 1e-10, total 4.33e-10. Lab expected output verified by twin_vs_page.out.")
row("M2c-L16-prop21-31", "2.4-mathematics", "L16 Remark 1.2, Proposition 2.1 proof (lines 86-89), Proposition 3.1 (lines 97-105), canon-breaks, misconceptions", "PASS",
    "Re-read. Prop 2.1 proof: phi(t)=f(t,a2), phi'(a1)=partial, C_h phi = central difference of L13, Theorem 2.2 hypothesis is the third-derivative continuity stated in Prop 2.1. Prop 3.1: g(t,0)=g(0,t)=0 for t != 0 so both quotients are 0; non-continuity by L15 Example 3.4 along (1/k,1/k), g=1/2 (L15 line 132). Canon bullet 1 (f=y gives -1 at fixed s) and Misconception 2 (xy: partial y, diagonal derivative 2 at (1,1), partial 1) re-computed.")
row("M2c-L16-R3-dependence", "2.4-mathematics", "course/modules/M/M2/L16.html line 326 (R3 statement) and line 328 (R3 solution)", "PASS",
    "Round-6 FAIL resolved in substance. The R3 solution names the third hypothesis of L13 Proposition 3.2 (exactness of the evaluation points, line 328 'the three evaluations are taken at the exact points a1-h, a1, a1+h') and says the rounding of a1 +/- h violates it. Arithmetic re-derived: 3.33e-10 + 1e-10 = 4.33e-10.")
row("M2c-L16-R3-xref", "2.9-structure", "course/modules/M/M2/L16.html line 326 (R3 statement): 'Bound the total error using Proposition 2.1 and Proposition 3.2 of Lesson L13'", "FAIL",
    "Proposition 2.1 is not in Lesson L13. grep finds no 'Proposition 2.1' in L13.html; L13 has Theorems 2.1, 2.2, Definition 3.1, Proposition 3.2 and Corollary 4.1. Proposition 2.1 is the central difference of a partial in THIS lesson (L16.html line 79). The R3 solution's truncation step uses L16 Proposition 2.1, so the statement points a reader to a nonexistent L13 result (xref_r7.out shows the scan found every other numbered reference resolves).",
    "In L16.html line 326 change 'Proposition 2.1 and Proposition 3.2 of Lesson L13' to 'Proposition 2.1 of this lesson and Proposition 3.2 of Lesson L13'.")
row("M2c-L17-numbers", "2.2-numbers", "L17 Example 1.2, Lab 1, E2, E3, R1, Section 4", "PASS",
    C + "page and twin unchanged.")
row("M2c-L17-theorems", "2.4-mathematics", "L17 Definition 2.1, Theorem 2.2 proof, Theorem 3.1 proof, Section 4", "PASS",
    C + "page unchanged; R2 cross-reference from L18 canon bullet 2 (f=x^2y/(x^2+y^4), D_u f(0)=sin theta) matches L17 line 314-318.")
row("M2c-L17-lab1", "2.5-labs", "L17 Lab 1 hypothesis, output, interpretation", "PASS",
    C + "twin_vs_page.out confirms L17 page code == twin and expected == output.")
row("M2c-L18-numbers", "2.2-numbers", "L18 Example 4.2, P3, E1, E2, E3, R3, Lab 1 hypothesis", "PASS",
    "Re-derived: J_F(1,2)=[[2,-4],[4,2]]; F(a+h)-F(a)-Jh = (s1^2-s2^2, 2 s1 s2), length |h|^2; ratio |k| for u=(0.6,0.8) (remainder_ratio in the twin) matches the printed 1.0000e-01..1.0000e-04 (twin_vs_page.out); E1 half spacing of doubles near 4 is 4.44e-16, rounding 4.44e-11; E3 grid argument; R3 minimizer (3delta/M)^(1/3) with delta>0, M>0 (the round-7 added hypotheses) matches L13 P3.")
row("M2c-L18-theorems", "2.4-mathematics", "L18 Definition 3.1, Proposition 3.2 proof, Proposition 3.3 proof, Theorem 4.1 proof, R1, R2, P2", "PASS",
    "Proposition 3.2: h=te_j gives the partial; uniqueness by the triangle inequality for unit v; Proposition 3.3 bound |Ah| <= (sum |A_ij|)|h|; Theorem 4.1 telescoping with the MVT on each segment (partials exist on the ball), omega(rho) -> 0 by continuity at a, bound sqrt(m) n omega(|h|)|h|. R1: |f|/|h| <= r, so differentiable with array 0; partial in x equals (2 rho sin(1/rho) - cos(1/rho)) x/rho (chain rule uses Assumption 1), along (rho,0) at rho_k = 1/(2 pi k) it tends to -1 != 0 = partial(0). Canon bullet 1 partial of g computed = y(y^2-x^2)/(x^2+y^2)^2, equals 1/y on the y-axis.")
row("M2c-L18-assumption1", "2.4-mathematics", "course/modules/M/M2/L18.html line 250 (Assumption 1), line 265 (M2), line 333 (R1); card M2-c277", "PASS",
    "Round-6 FAIL resolved. Assumption 1 (line 250) now states both derivative of sin is cos and derivative of cos is -sin, and says 'Problems M2 and R1 use them, and each says so'. M2 solution (line 265) opens 'Under Assumption 1, the derivative of cos is -sin and of sin is cos'; R1 (line 333) says 'Under Assumption 1'. No other L18 item differentiates sin or cos (canon bullet 2 uses sin theta as a value only).")
row("M2c-L18-lab1", "2.5-labs", "L18 Lab 1 hypothesis, expected block, interpretation", "PASS",
    S + "twin_vs_page.out (expected == output for L18). Interpretation: 25 grid points, True, rows 2.000000 -4.000000 / 4.000000 2.000000, remainder ratios |k| (the lab checks one direction at one point, which the text says).")
row("M2c-grades", "2.3-grades", "grade tags in L13-L18", "PASS",
    "Re-read in round 7 for L13, L16, L18: every T-tagged block is proved on the page (Theorems 2.1, 2.2, Props 3.2, 3.3, Cor 4.1, Prop 2.1, Prop 3.1, Thm 4.1, Example 1.3 and Example 4.2 algebra, key-results rows), every C-tagged row cites Lab 1 as basis. L14, L15, L17 carried: " + C.split(': ')[0].lstrip('Carried from round 6 (') + ".")
row("M2c-attribution", "2.1-citations", "references sections of L13-L18 and any attributed claim", "PASS",
    "References sections of L13 (line 465), L16 (line 433), L18 (line 453) re-read: no registry key cited; the spivak and hubbard keys are named only. No bibliographic data, theorem number or locator is attributed to a source. The rounding model of L13 Section 3 is stated as the page's own assumption.")
row("M2c-labs-data", "2.5-labs", "L13-L18 lab blocks and data-files", "PASS",
    "No data-files attribute on L13-L18 (grep). Each lab is standard library only and deterministic: the twins contain no random call (grep for random/seed/fetch returns none in the six twins).")

frag = {
    "unit": "M2",
    "slice": "c",
    "round": 7,
    "verifier": "Haiku 5.5 independent verifier (B7)",
    "pin": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
    "base": "44f1eb6a417ce687a9b88c7ee917e72566b29892 (round-6 pin; round-6 fragment /Users/billyribeiro/.fanout/frags/B-M2-c.round6.json used as context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB7-M2-c",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyB7-M2-c/ledgers/M2/scripts/M2-c-r7",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Slice is lessons L13-L18 and their six lab twins. No project grader, so no mutation test. Round-7 delta for the slice: course/modules/M/M2/L13.html, L16.html, L18.html and cards.json (cards M2-c185, c186, c194, c277 changed; c250 removed; c380, c381 added); L14, L15, L17 and all six twins byte-identical to the pin 44f1eb6. Carried rows are labelled. Round-6 FAIL rows M2c-L13-prop32-hypotheses and M2c-L18-assumption1 re-verified and now PASS; M2c-L16-R3-dependence substance fixed, but a new cross-reference FAIL M2c-L16-R3-xref and card M2c-cards-L13 (M2-c187 missing hypotheses) remain. Not checked: the live verify_refs --unit M2 (network, no key cited in slice); a line-by-line re-read of L14, L15, L17 (carried by byte identity, per rule); Pyodide-specific execution beyond page_smoke; the rendered visual pages (no figures on these pages).",
    "summary": "2 FAIL rows: M2-c187 card omits the delta>0, M_3>0 hypothesis that the lesson now states; L16 R3 statement cites a nonexistent 'Proposition 2.1 of Lesson L13'. All gates pass. Round-6 FAILs on L13 Prop 3.2 hypotheses and L18 Assumption 1 are fixed."
}
out = pathlib.Path("ledgers/M2/M2-c.json")
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "status counts", {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL")})
