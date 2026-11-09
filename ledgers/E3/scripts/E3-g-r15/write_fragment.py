"""Round-15 verifier: write the E3 slice g fragment (L05-L08, cards, lab twins). Evidence cites the round-15 scripts and outputs."""
import datetime
import json
import sys

ROOT = sys.argv[1]
OUT = f"{ROOT}/ledgers/E3/scripts/E3-g-r15/out"
SC = "ledgers/E3/scripts/E3-g-r15"
CARDS = "course/modules/E/E3/cards.json"

rows = []


def row(rid, check, location, evidence, status="PASS"):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence})


RE = "Round 15 re-verification (full re-read of the card and the current lesson text; no carry):"

# ---- card rows (88 ids carried from round 14; every card re-read against current lesson text) ----
cards = {
 "E3g12-c078": ("L05", "Definition 1.1 (V0 formula, a = 1 - 1/psi, V1 = c1); A1-A4 (Section 1 assumptions)", "card text matches Definition 1.1 and A1-A4"),
 "E3g12-c079": ("L05", "Remark 1.2 (CE1 definition and identity CE1^(1-gamma) = E c1^(1-gamma))", "card matches Remark 1.2"),
 "E3g12-c080": ("L05", "Theorem 1.3(a),(b): value through CE1 only; strictly increasing in CE1", "card matches Theorem 1.3"),
 "E3g12-c081": ("L05", "Corollary 1.4 (risky plan = sure plan at CE1); section 5 third misconception", "card matches Corollary 1.4 and the misconception"),
 "E3g12-c082": ("L05", "Remark 1.5 (lower CE, lower value; same mean different values; 8/5 and 12/5 from E[1/c] = 5/8, 5/12)", "card matches Remark 1.5; numbers recomputed in numbers_L05_L08.out (CE 1.6, 2.4)"),
 "E3g12-c083": ("L05", "Definition 2.1 as changed in dde0486b: EIS := dln(c1/c0)/dln MRS, MRS = (dV0/dc0)/(dV0/dc1)", "card (changed by dde0486b, back now uses EIS) matches the changed Definition 2.1"),
 "E3g12-c084": ("L05", "Proposition 2.2 (MRS = (1-beta)/beta (c1/c0)^(1/psi); EIS = psi) and its proof", "card matches Proposition 2.2 and the proof"),
 "E3g12-c085": ("L05", "Remark 2.3 (CE1 = c1 for gamma != 1; EIS = psi at every gamma; Lab 1 three-gamma check)", "card matches Remark 2.3"),
 "E3g12-c086": ("L05", "Remark 3.1 (theta = 1 exactly when psi = 1/gamma under A1-A4)", "card matches Remark 3.1"),
 "E3g12-c087": ("L05", "Theorem 3.2 ((1-gamma)U = V0^(1-gamma) at psi = 1/gamma; gamma > 0 by A2)", "card matches Theorem 3.2"),
 "E3g12-c088": ("L05", "Corollary 3.3 (V0 strictly increasing in U; same ranking)", "card matches Corollary 3.3 and its proof"),
 "E3g12-c089": ("L05", "Remark 3.4 (MRS_U exponent gamma; EZ exponent 1/psi; agree iff 1/psi = gamma)", "card matches Remark 3.4"),
 "E3g12-c090": ("L05", "Corollary 3.3 (needs psi = 1/gamma); Remark 3.4; Lab 1 pair at psi = 2 (stripped lab output lines 412-415)", "card matches; disagreement is off the restriction"),
 "E3g12-c091": ("L05", "Remark 3.4 (elasticity 1/gamma, undefined at gamma = 0); Proposition 2.2 (EZ gives psi)", "card matches Remark 3.4 and Proposition 2.2"),
 "E3g12-c093": ("L05", "Lab 1 printed V0 = 80/49 (lab output line 398); Problem E1 solution (V0^-1 = 1/20 + 9/16)", "card matches; 80/49 recomputed by hand and in numbers_L05_L08.out"),
 "E3g12-c094": ("L05", "Lab 1 EIS lines 416-418; E3 solution (c1 in [0.999,1.001] times 4, MRS relative step 1e-6); twin eis_numeric and mrs_numeric", "card matches the twin code and the printed values 0.5000, 2.0000, 0.2500"),
 "E3g12-c095": ("L05", "Lab 1 lines 412-415 (U(4,4) = -0.25, U(1,10) = -0.55, V0(4,4) = 4.0, V0(1,10) = 4.3311)", "card matches printed values; recomputed by hand"),
 "E3g12-c096": ("L05", "Lab 1 lines 406-409 (CE1 = 2.2500, 1.6000, 1.3720)", "card matches; 1.3719887 rounds to 1.3720 (numbers_L05_L08.out)"),
 "E3g12-c169": ("L05", "Lab 1 line 399 (U = -49/80); Problem E1 solution", "card matches"),
 "E3g12-c170": ("L05", "Remark 1.5 (CE1 = 8/5 for the 1 or 4 tree); Lab 1 line 402", "card matches"),
 "E3g12-c184": ("L05", "Lab 1 line 419 (closed-form MRS agrees: True); Proposition 2.2; twin line 161 tolerance rel 1e-6", "card matches"),
 "E3g12-c185": ("L05", "Remark 1.5 (mean 5/2); Lab 1 line 402 (mean of c1 = 5/2)", "card matches"),
 "E3g12-c098": ("L06", "Definition 1.1 (gain and loss relative to r; r = 0 in Lab 1)", "card matches Definition 1.1"),
 "E3g12-c099": ("L06", "Definition 1.2 (v with alpha, delta, lambda > 0; v(0) = 0)", "card matches Definition 1.2"),
 "E3g12-c100": ("L06", "Definition 1.3 (W = sum p_i v(x_i); weighting in L07)", "card matches Definition 1.3"),
 "E3g12-c101": ("L06", "Proposition 1.4 as changed in dde0486b (v'' < 0 on x > 0; v'' >= 0 on x < 0; strictly increasing) and its proof", "card (changed) matches the changed statement and proof"),
 "E3g12-c102": ("L06", "Remark 1.5 (|v(-x)|/v(x) = lambda when alpha = delta)", "card matches Remark 1.5"),
 "E3g12-c103": ("L06", "Definition 1.6 (loss aversion; lambda > 1 by Remark 1.5)", "card matches Definition 1.6"),
 "E3g12-c104": ("L06", "Proposition 2.1 (lambda* = p g/((1-p) l); W decreasing; sign pattern)", "card matches Proposition 2.1"),
 "E3g12-c105": ("L06", "Proposition 2.2 (lambda* = p g^alpha/((1-p) l^delta))", "card matches Proposition 2.2"),
 "E3g12-c106": ("L06", "Example 2.3 (EV 200; lambda* = 5/3; W = 200, 50, -100); changed grade C -> T in dde0486b", "card (grade now T, basis Example 2.3) matches Example 2.3; arithmetic 500 - 300 lambda recomputed in numbers_L05_L08.out"),
 "E3g12-c107": ("L06", "Remark 2.4 (same sign as CE; v continuous, strictly increasing, v(0) = 0)", "card matches Remark 2.4"),
 "E3g12-c108": ("L06", "Remark 2.5 (700 - 300 lambda; 2(500 - 300 lambda); 100 and -200 at lambda = 2)", "card matches Remark 2.5"),
 "E3g12-c109": ("L06", "Remark 2.5 (narrow framing definition)", "card matches Remark 2.5"),
 "E3g12-c110": ("L06", "Remark 3.1 (lambda > 1 is a restriction; Props 1.4, 2.1, 2.2 need only lambda > 0)", "card matches Remark 3.1"),
 "E3g12-c111": ("L06", "Remark 3.2 (EV reference point; for Example 2.3 the value (1/2) 800^alpha (1 - lambda); lambda_R)", "card matches Remark 3.2"),
 "E3g12-c112": ("L06", "Section 5 first misconception (positive EV always rejected); Example 2.3", "card matches the misconception"),
 "E3g12-c113": ("L06", "Remark 3.2 (p = 1/3, g = 1000, l = 300, alpha = delta = 1/2: lambda_R = sqrt(2)/2)", "card matches Remark 3.2; 0.7071 recomputed (numbers_L05_L08.out)"),
 "E3g12-c116": ("L06", "Lab 1 power block: threshold 1.2910 and W = -8.6835 at lambda = 2 (lab output lines 323-325)", "card matches printed output; sqrt(5/3) = 1.2909944 recomputed"),
 "E3g12-c117": ("L06", "Lab 1 grid lines 326-328; twin midpoint inequality code (losses_second_derivative_nonneg)", "card (changed label to midpoint test) matches the code; the check is a finite midpoint convexity inequality, graded C"),
 "E3g12-c163": ("L06", "Remark 2.5 (integrated evaluation of the combined lottery)", "card matches Remark 2.5"),
 "E3g12-c118": ("L07", "Definition 1.1 (weighting function: nondecreasing, omega(0) = 0, omega(1) = 1)", "card matches Definition 1.1"),
 "E3g12-c119": ("L07", "Definition 1.2 (non-cumulative value; EU as special case)", "card matches Definition 1.2"),
 "E3g12-c120": ("L07", "Remark 1.3 (identity weighting gives the expected value of v(X))", "card matches Remark 1.3"),
 "E3g12-c121": ("L07", "Example 1.4 closed form; omega values 0.28579088, 0.39125077, 0.35355339", "card matches; values recomputed to 10 digits (numbers_L05_L08.out)"),
 "E3g12-c122": ("L07", "Observation 1.5 (last grid point 0.278; one sign change); Lab 1 part A lines 367-368", "card matches printed output; graded C (finite grid)"),
 "E3g12-c123": ("L07", "Remark 1.6 (sum 0.89103669; 2 omega(3/10) = 0.57158177); section 4 second misconception", "card matches Remark 1.6"),
 "E3g12-c124": ("L07", "Example 2.1 (F_A and F_B at 0, 50, 100 CU)", "card matches Example 2.1"),
 "E3g12-c125": ("L07", "Proposition 2.2 (threshold 2/3 and 0.58578644; ratio 0.7304544982 recomputed)", "card matches Proposition 2.2"),
 "E3g12-c126": ("L07", "Remark 2.3 (identity weighting: V(A) = 45, V(B) = 60)", "card matches Remark 2.3"),
 "E3g12-c127": ("L07", "Lab 1 part C lines 374-375 (42.8686, 39.1251, 4.8788, 3.9125; A above B)", "card matches printed output; graded C"),
 "E3g12-c128": ("L07", "Lab 1 part D line 376 (10 of 10); Lesson 4 Theorem 1.5", "card matches; graded C"),
 "E3g12-c129": ("L07", "Lesson 4 Theorem 1.5 (F_X <= F_Y iff E u(X) >= E u(Y) for every nondecreasing u); L04 theorem text unchanged in the pin delta", "card matches the L04 theorem"),
 "E3g12-c130": ("L07", "Remark 1.6; section 4 first misconception (weights respect the order of single probabilities only)", "card matches; T grade supported by the arithmetic in Remark 1.6"),
 "E3g12-c132": ("L07", "Section 4 third misconception: 49.8328 against 50.5 (recomputed 49.8327749; over 7.34, under 8.01, net -0.67)", "card matches the misconception and the numbers"),
 "E3g12-c133": ("L07", "Problem R1 (affine weighting with endpoints is the identity); omega(1/2) = 0.35355339", "card matches Problem R1"),
 "E3g12-c134": ("L07", "Section 1 after Remark 1.3 (name in the title of the 1979 paper); registry kahneman1979prospect (title 'Prospect Theory: An Analysis of Decision under Risk', year 1979, Kahneman and Tversky)", "card matches the registry record and the page's title-only use"),
 "E3g12-c135": ("L07", "Problem R2 (Tail_B >= Tail_A at 50 and 100; 3/5 against 3/5 and 3/5 against 3/10)", "card matches Problem R2"),
 "E3g12-c187": ("L07", "Problem E2 (40-digit values 42.86863274 and 39.12507700; difference 3.74355573 rounds to 3.7436; printed difference 3.7435)", "card matches Problem E2; recomputed in numbers_L05_L08.out"),
 "E3g12-c136": ("L08", "Definition 1.1 (prior set)", "card matches Definition 1.1"),
 "E3g12-c137": ("L08", "Definition 1.2 (alpha-MEU value and certainty equivalent)", "card matches Definition 1.2"),
 "E3g12-c138": ("L08", "Proposition 1.3 (one-element prior set gives expected utility)", "card matches Proposition 1.3"),
 "E3g12-c139": ("L08", "Example 1.4 (k = 30 to 60; average 45/90 = 1/2)", "card matches Example 1.4"),
 "E3g12-c140": ("L08", "Definition 2.1 (ambiguity aversion)", "card matches Definition 2.1"),
 "E3g12-c141": ("L08", "Theorem 2.2 (A1-A3; maxmin CE at most average-prior CE)", "card matches Theorem 2.2"),
 "E3g12-c142": ("L08", "Remark 2.3 and the strict case in the proof of Theorem 2.2", "card matches Remark 2.3"),
 "E3g12-c143": ("L08", "Proposition 2.4 (A1-A3; worst priors P_0 and P_90; proof line 176 monotone in p)", "card matches Proposition 2.4 including A3 (w_red > w_no)"),
 "E3g12-c144": ("L08", "Example 2.5 (known urn CE 103125 for red; recomputed 1650000/16)", "card matches Example 2.5"),
 "E3g12-c145": ("L08", "Definition 3.1 (two-date value and timing convention)", "card matches Definition 3.1"),
 "E3g12-c146": ("L08", "Proposition 3.2 (A1-A5) and section 6 third misconception", "card matches Proposition 3.2 and the misconception"),
 "E3g12-c147": ("L08", "Remark 3.3 (earlier-resolving gamble; dependence untested)", "card matches Remark 3.3"),
 "E3g12-c148": ("L08", "Remark 4.2 (midpoint of extreme priors equals average prior; affine g)", "card matches Remark 4.2"),
 "E3g12-c149": ("L08", "Section 4 Model 1 (4180000/41 = 101951.2195)", "card matches Model 1; recomputed"),
 "E3g12-c150": ("L08", "Section 4 Model 2 (V = 5 - sqrt(50) = -2.071068)", "card matches Model 2"),
 "E3g12-c151": ("L08", "Section 4 Model 4 (99523.8095 at P(red) = 1/3)", "card matches Model 4; recomputed"),
 "E3g12-c152": ("L08", "Section 4 risk premium (548.7805 cents; 5.4878 CU; exact 22500/41)", "card matches; recomputed"),
 "E3g12-c153": ("L08", "Lab 1 part B lines 486-493 (101951.219512; largest gap 2.91e-11; all below 1e-6)", "card matches printed output; graded C"),
 "E3g12-c154": ("L08", "Proposition 2.4 (A1-A3) and section 6 first misconception, line 597 (both now carry A3)", "ROUND-14 FAIL RE-VERIFIED: the card now states A3 (bets pay their prize on their own colour, w_red > w_no), matching Proposition 2.4 and the misconception text; worst priors P_0 and P_90 follow from the proof at line 176. PASS"),
 "E3g12-c155": ("L08", "Theorem 2.2 (A2: u strictly increasing); R3 solution line 785", "card matches Theorem 2.2"),
 "E3g12-c157": ("L08", "Registry ellsberg1961risk (title 'Risk, Ambiguity, and the Savage Axioms', 1961); L08 line 186", "card matches the registry title-only attribution"),
 "E3g12-c158": ("L08", "Registry gilboa1989maxmin (title 'Maxmin expected utility with non-unique prior'; Gilboa and Schmeidler; 1989); L08 lines 86 and 821", "card matches the registry title-only attribution"),
 "E3g12-c164": ("L08", "Example 2.5 with Proposition 2.4 (100000 cents for both colours)", "card matches Example 2.5"),
 "E3g12-c165": ("L08", "Example 2.5 (known-urn CE above 100000 for both colours)", "card matches Example 2.5"),
 "E3g12-c166": ("L08", "Section 4 Model 2 (99892.7670 cents)", "card matches Model 2"),
 "E3g12-c172": ("L08", "Definition 1.2 (tau = 1 gives the minimum over the prior set)", "card matches Definition 1.2"),
 "E3g12-c179": ("L08", "Section 4 Model 3 and Proposition 3.2 (101951.2195)", "card matches Model 3"),
 "E3g12-c182": ("L08", "Example 2.5 (black-bet CE 3300000/31 = 106451.6129)", "card matches Example 2.5"),
}
card_order = list(cards.keys())
for rid in card_order:
    lesson, loc, note = cards[rid]
    cid = "E3-c" + rid.split("-c")[1]
    rows.append({
        "id": rid,
        "check": f"2.7 retrieval card {cid} against {lesson}",
        "location": f"course/modules/E/E3/cards.json {cid}; course/modules/E/E3/{lesson}.html: {loc}",
        "status": "PASS",
        "evidence": f"{RE} {note}. Card text checked in cards.json; lesson text from the stripped page (L0x.txt via {SC}/strip.py).",
    })

# c131: the card was removed before the pin 1431aa1d; the row is kept with its id.
rows.append({
    "id": "E3g12-c131",
    "check": "2.7 retrieval card E3-c131 against L07 (card removed)",
    "location": f"{CARDS} (no E3-c131); course/modules/E/E3/L07.html",
    "status": "PASS",
    "evidence": "Round 15: grep -c '\"E3-c131\"' course/modules/E/E3/cards.json = 0 at dde0486b (and 0 at 1431aa1d, git show 1431aa1d:course/modules/E/E3/cards.json); no course or test file references E3-c131 (grep). Nothing remains to verify for the removed card.",
})

# ---- lesson-level rows (re-verified in full this round) ----
rows += [
 {"id": "E3g12-L05-prose-numbers", "check": "2.2 numbers in L05 prose", "location": "course/modules/E/E3/L05.html Remark 1.5, Definition 2.1, Proposition 2.2 proof, Remark 2.3, Remark 3.4, Problems P1-E3 (stripped L05 text)",
  "status": "PASS", "evidence": "Round 15 re-verification of every number in changed and unchanged L05 prose: 8/5 and 12/5 (CE from E c^-1 = 5/8 and 5/12), 5/2, 80/49, 160/71, 16/7, and the Problem M1 and M3 values; script ledgers/E3/scripts/E3-g-r15/numbers_L05_L08.py and out/numbers_L05_L08.out; all match."},
 {"id": "E3g12-L06-prose-numbers", "check": "2.2 numbers in L06 prose", "location": "course/modules/E/E3/L06.html Proposition 1.4, Example 2.3, Remarks 2.4, 2.5, 3.2, misconceptions, problems M1, M2, E2, E3, R2, quiz", "status": "PASS",
  "evidence": "Round 15: EV 200, lambda* 5/3, W = 200, 50, -100, combined 700 - 300 lambda (100 at 2), separate -200, lambda_R = 1 (EV reference, alpha = delta) and sqrt(2)/2 (p = 1/3 case), sqrt(5/3) = 1.2910, W(2) = -8.6835; all recomputed in numbers_L05_L08.out."},
 {"id": "E3g12-L07-prose-numbers", "check": "2.2 numbers in L07 prose", "location": "course/modules/E/E3/L07.html Example 1.4, Observation 1.5, Remarks 1.6, 2.3, Proposition 2.2, section 4, Problems M1, E1, E2, E3, R2, quiz", "status": "PASS",
  "evidence": "Round 15: omega(3/10), omega(3/5), omega(1/2), omega(1/4) = 0.26794919, omega(0.01) = 0.0834030105, omega(0.99) = 0.8298494764, sum 0.89103669, ratio 0.7304544982 (rounds 0.73045450; quotient of printed 8-digit values 0.73045449), 40-digit difference 3.74355573, grid crossing between 0.278 and 0.279, gap 3.33e-16, gap 3.13e-1 at p = 0.862 for eta = 1; all in numbers_L05_L08.out."},
 {"id": "E3g12-L08-prose-numbers", "check": "2.2 numbers in L08 prose", "location": "course/modules/E/E3/L08.html Example 1.4, Example 2.5, Remark 2.3, section 4 (Models 1-4), Remark 4.2, misconceptions, problems M1-M3, E1-E3, R2, R3, quiz", "status": "PASS",
  "evidence": "Round 15: 4180000/41 = 101951.2195; prospect 5 - sqrt(50) = -2.071068 and 99892.7670; maxmin 99523.8095 (P = 1/3); 103125 and 106451.6129; 102500 - 101951.2195 = 548.7805 = 22500/41; M1 98352.94; M2 105822.78; 4.8788 CU; all recomputed by hand and by Fraction arithmetic (ledgers/E3/scripts/E3-g-r15/out/numbers_L05_L08.out and lab output)."},
 {"id": "E3g12-L05-L08-key-results", "check": "2.3 grades in the Key results tables of L05-L08 against proofs and lab output", "location": "course/modules/E/E3/L05.html section 7, L06.html section 7 (changed rows), L07.html section 6, L08.html section 8", "status": "PASS",
  "evidence": "Round 15: each row re-read. L06 rows changed in dde0486b: 'v'' >= 0 on losses' (Proposition 1.4, T, proved), Example 2.3 row graded T (source Example 2.3; the values follow from Proposition 2.1 by arithmetic), midpoint row graded C (finite grid). All other grades agree with the proofs or the printed Lab 1 output."},
 {"id": "E3g12-L05-L08-problem-solutions", "check": "2.4 problem solutions the cards rely on (M, P, E, R)", "location": "course/modules/E/E3/L05.html, L06.html, L07.html, L08.html problem sets", "status": "PASS",
  "evidence": "Round 15: every solution re-read; L05 M1 (CE 2, mean 5/2), M2 (V0 = 3/2), M3 (theta = -2), E1 (80/49, -49/80), E2 (16/7, 160/71); L06 M1 (lambda* 3/2, W = -100), M2 (EV 0, W = -50), E2, E3 (250 and 100), R2 (lambda_R = 1); L07 M1, M2, E2, R2, R3 checked; L08 M1 (98352.94), M2 (98352.94), M3 (105822.78), E1 (103125 - 100000 = 3125 cents), E3 (548.7805), R2, R3 checked; all arithmetic matches."},
 {"id": "E3g12-L05-L08-quiz-keys", "check": "2.9 retrieval quiz answer keys in L05-L08", "location": "course/modules/E/E3/L05.html, L06.html, L07.html, L08.html quiz items (data-correct and data-answer)", "status": "PASS",
  "evidence": "Round 15: keys extracted by script (quiz parse, output in this round): L05 numeric 2, -2, 1.632653 (tol 5e-7; 80/49 = 1.6326531), 4; L06 numeric 1.6667 (tol 1e-4; 5/3), -100, 1.2910 (tol 1e-4); L07 0.26795, 39.1251, 0.35355, 0.278; L08 101951.22, 99523.81, 103125 (tol 0.5), 548.78, 99892.77 (all within tolerance); every multiple-choice key matches its lesson proof (L06 q2 'Concavity' correct after the dde0486b option change)."},
 {"id": "E3g12-lab-twins-run", "check": "2.5 labs: twins alone under python -I -W error (lessons whose cards are in this slice)", "location": "tests/labs/E3/lab-E3-L05-1.py, lab-E3-L06-1.py, lab-E3-L07-1.py, lab-E3-L08-1.py", "status": "PASS",
  "evidence": f"Round 15: .venv/bin/python -I -W error on each twin; {SC}/twin_check.py output out/twin_check.out: page code equals twin byte for byte and expected block equals stdout for L05, L06, L07, L08 (rc 0, no stderr)."},
 {"id": "E3g12-check-pages-dag-projects", "check": "2.9 structure and DAG: check_pages, check_dag, check_projects for E3", "location": "tools/check_pages.py --unit E3 --page L05..L08; tools/check_dag.py --unit E3; tools/check_projects.py --unit E3", "status": "PASS",
  "evidence": "Round 15 gates.sh outputs: 'check_pages E3 L05: PASS' (and L06, L07, L08 PASS); 'check_dag E3: PASS'; 'check_projects E3: PASS' (out/check_pages_L0x.out, out/check_dag_unit.out, out/check_projects_unit.out)."},
 {"id": "E3g12-verify-refs", "check": "2.1 citations used by the cards: offline integrity and live Crossref", "location": "tools/verify_refs.py --offline; references/references.json (kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin, epstein1989substitution)", "status": "PASS",
  "evidence": "Round 15: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (out/verify_refs_offline.out). references/ unchanged between 1431aa1d and dde0486b (git diff --stat empty). Registry titles/authors/years for the four keys re-read and match the page text. The live Crossref run was not repeated this round (see notes)."},
 {"id": "E3g12-L04-theorem-cross-lesson", "check": "2.7/2.9 cross-lesson target of card E3-c129 (Lesson 4 Theorem 1.5)", "location": "course/modules/E/E3/L04.html Theorem 1.5; course/modules/E/E3/L07.html section 0 and Section 2; cards E3-c129", "status": "PASS",
  "evidence": "Round 15: L04 Theorem 1.5 text re-read (first-order dominance on finite support: F_X <= F_Y iff E u(X) >= E u(Y) for every nondecreasing u); the pin delta changes only an L04 quiz option (L04q4 wording), not the theorem; L04 Definition 1.3 defines first-order dominance by distribution functions as L07 states."},
 {"id": "E3g12-notation", "check": "2.4/2.9 notation: symbols in L05-L08 against notation/notation.json", "location": "notation/notation.json (8 symbols, 26 macros); course/modules/E/E3/L05.html-L08.html and cards.json", "status": "PASS",
  "evidence": "Round 15: registered macros used in L05-L08 are \\E, \\Prob and \\R with their registered meanings (expectation, probability, reals); no registered symbol (T, gamma_3, gamma_4, macros) appears in L05-L08 with another meaning (grep of LaTeX macros per lesson). Local letters (gamma, psi, beta, theta, lambda, alpha, delta, omega, eta, tau, nu, ell, varpi) are defined per lesson as the notation file allows. The dde0486b change renames epsilon to the defined name EIS (Definition 2.1, Proposition 2.2 proof, quiz explanation, card E3-c083); grep finds no remaining epsilon symbol in L05-L08 or their cards."},
 {"id": "E3g12-scope-words-cards", "check": "2.9 scope words (only, all, always, every, any, same, exactly) in the L05-L08 cards", "location": "cards.json cards of L05-L08 (E3-c107, c110, c117, c155, c154, c143, c083)", "status": "PASS",
  "evidence": "Round 15 re-read: 'for every alpha, delta and lambda > 0' (Remark 2.4 states the same), 'every grid point' (Lab 1 checks each grid point, finite), 'any nu > 0' (Theorem 2.2 uses only strict monotonicity), 'only through CE1' (Theorem 1.3(a)), 'not the worst for both bets' (P_0 != P_90). Each scope word is backed by a proof, a computation or an explicit finite-grid qualifier."},
 {"id": "E3g12-process-words-cards", "check": "2.9 process words in learner text (cards and L05-L08)", "location": "cards.json (L05-L08) and course/modules/E/E3/L05.html-L08.html changed text", "status": "PASS",
  "evidence": "Round 15: grep of added lines in the pin delta for round/verifier/fragment/builder/fixed-type words: no process words (the only hit, 'fixed c0', is the mathematical term). Card and lesson text describes the content only."},
 {"id": "E3g12-dup-scan", "check": "2.7 full scan for duplicate cards (all 178 E3 cards)", "location": f"{CARDS} (178 cards)", "status": "PASS",
  "evidence": f"Round 15: {SC}/card_numbers.py: 'cards 178 unique ids True', 'duplicate fronts []'. Cards E3-c188 (L03) added at the pin delta is out of this slice."},
 {"id": "E3g12-card-numbers", "check": "2.7 every number on a card appears in its lesson (token match)", "location": f"{CARDS} (L05-L08 cards); stripped lesson text", "status": "PASS",
  "evidence": f"Round 15: {SC}/card_numbers.py output out/card_numbers.out: no number token of any L05-L08 card missing from its lesson text (integers 0-3 excluded)."},
 {"id": "E3g12-delta-round12", "check": "delta since ccaeeaf4 for the slice: cards, L05, L07 and their lab twin", "location": "history: ccaeeaf4..329c1d7f (round 12 delta)", "status": "PASS",
  "evidence": "The round-12 delta is superseded: every card and every L05-L08 lesson and twin was re-read in full in round 15 at dde0486b (rows E3g12-c* and the lesson rows). No row relies on that older delta."},
 {"id": "E3g12-r11-c130-grade-resolved", "check": "prior-round FAIL E3g11-c130-grade (grade T on a card carrying lab-printed values)", "location": "course/modules/E/E3/cards.json E3-c130", "status": "PASS",
  "evidence": "Round 15: card E3-c130 (T) cites Remark 1.6 arithmetic (2 omega(3/10) = 0.57158177 against 0.6 and 0.39125077) and section 4 first misconception; the grade is supported by proved or hand arithmetic, not by printed lab output. Still PASS."},
 {"id": "E3g12-c131-basis-note", "check": "2.3 grade of E3-c131 (C, basis Lab 1 part C and Problem E2)", "location": f"{CARDS} (E3-c131 absent)", "status": "PASS",
  "evidence": "Round 15: E3-c131 is absent at dde0486b and at 1431aa1d (count 0); no basis note remains to check. Row kept by id."},
 {"id": "E3g14-delta-round14", "check": "2.9 delta 329c1d7f..1431aa1d within the slice", "location": "history: 329c1d7f..1431aa1d", "status": "PASS",
  "evidence": "Superseded by E3g15-delta (1431aa1d..dde0486b) and by the full round-15 re-read of every card and lesson in the slice; the round-14 FAIL on E3-c154 is re-verified PASS (row E3g12-c154)."},
 {"id": "E3g14-lab-L05-printed", "check": "2.5 lab printed values recomputed", "location": "tests/labs/E3/lab-E3-L05-1.py; course/modules/E/E3/L05.html expected block", "status": "PASS",
  "evidence": "Round 15: twin_check.py (expected block equals stdout, rc 0) and recomputation of the printed values in numbers_L05_L08.out; the L05 twin is unchanged in the pin delta."},
 {"id": "E3g14-lab-L06-printed", "check": "2.5 lab printed values recomputed", "location": "tests/labs/E3/lab-E3-L06-1.py; course/modules/E/E3/L06.html expected block", "status": "PASS",
  "evidence": "Round 15: the changed twin (midpoint label and print line) runs with rc 0 under python -I -W error; page code equals the twin; expected block equals stdout (lines '...loss part with v'' >= 0 (midpoint test) on the grid: True'); the printed values 200, 50, -100, 100, -200, 1.2910, -8.6835 match the hypothesis paragraph."},
 {"id": "E3g14-lab-L07-printed", "check": "2.5 lab printed values recomputed", "location": "tests/labs/E3/lab-E3-L07-1.py; course/modules/E/E3/L07.html expected block", "status": "PASS",
  "evidence": "Round 15: twin_check.py PASS for L07; printed values 0.0834, 0.1557, 0.2858, 0.3536, 0.3913, 0.6788, 0.8298, gap 3.33e-16, 0.278, 42.8686, 39.1251, 4.8788, 3.9125, 10 of 10 recomputed independently."},
 {"id": "E3g14-lab-L08-printed", "check": "2.5 lab printed values recomputed", "location": "tests/labs/E3/lab-E3-L08-1.py; course/modules/E/E3/L08.html expected block", "status": "PASS",
  "evidence": "Round 15: twin_check.py PASS for L08; printed 101951.2195, 99892.7670, 99523.8095, 4.44e-16, EZ gaps up to 2.91e-11, 103125.0000, 106451.6129, 100000.0000 recomputed independently."},
 {"id": "E3g14-page-smoke", "check": "2.5 lab timing and 2.9 render checks", "location": "tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08", "status": "PASS",
  "evidence": "Round 15 gates.sh: 'page_smoke modules/E/E3/L08.html: PASS', 'page_smoke E3: PASS' (out/page_smoke_L05_L08.out, rc 0)."},
 {"id": "E3g14-ruff-mypy", "check": "gates: ruff, mypy", "location": "tests/labs/E3; course/modules/E/E3/grader; mypy strict config", "status": "PASS",
  "evidence": "Round 15 gates.sh: 'ruff check tests/labs/E3 course/modules/E/E3/grader' -> 'All checks passed!'; 'ruff format --check tests/labs/E3' -> '11 files already formatted'; '.venv/bin/mypy --no-incremental' -> 'Success: no issues found in 385 source files' (rc 0 each)."},
 {"id": "E3g14-pytest-relevant", "check": "gates: relevant pytest", "location": "tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py, tests/test_curriculum.py; tests/test_docs_figures.py, tests/test_refs.py", "status": "PASS",
  "evidence": f"Round 15: .venv/bin/pytest -q (lab, run_labs, page_checks, curriculum modules) rc 0 (out/pytest_relevant.out, 100%); pytest -q tests/test_docs_figures.py tests/test_refs.py rc 0 (out/pytest_docs.out)."},
 {"id": "E3g14-hours-arithmetic", "check": "2.9 hours arithmetic", "location": "course/modules/E/E3/index.html ('Module E3 · 70 hours'; 'Eight lessons of seven study hours each, which is 56 hours'); project.html (14 hours); L01-L08 headers (7 study hours)", "status": "PASS",
  "evidence": "Round 15: 8 x 7 = 56; project 14; 56 + 14 = 70 matches the hub; every lesson header reads 7 study hours. index.html changed in the pin delta only in the prerequisite paragraph and the worked-example rung text, not in hours."},
]

# ---- delta and new round-15 rows ----
rows += [
 {"id": "E3g15-delta", "check": "2.9 delta 1431aa1d..dde0486b within the slice (lessons L05-L08, cards, L06 twin)", "location": "course/modules/E/E3/L05.html (8 lines), L06.html (29), L07.html (6), L08.html (2), cards.json (cards c083, c101, c106, c117, c154 changed; c188 added is L03), tests/labs/E3/lab-E3-L06-1.py (7)", "status": "PASS",
  "evidence": "Round 15: git diff -U2 1431aa1d..dde0486b read hunk by hunk for every slice file (output reviewed in full). Each changed statement, proof, grade, label and option was re-verified (rows E3g15-L05..L08-changes and the affected card rows). No defect found in the delta."},
 {"id": "E3g15-L05-changes", "check": "2.2/2.7 L05 changed text: Remark 1.5, Definition 2.1 (EIS), Proposition 2.2 proof, quiz explanation", "location": "course/modules/E/E3/L05.html Remark 1.5, Definition 2.1, Proposition 2.2 proof, quiz item L05q9 explanation", "status": "PASS",
  "evidence": "Round 15: Remark 1.5 cites Theorem 1.3(b) (strictly increasing in CE1 at fixed c0, beta, gamma, psi) correctly; 8/5 and 12/5 recomputed; Definition 2.1 EIS := dln(c1/c0)/dln MRS is the quantity Proposition 2.2 computes (MRS = (1-beta)/beta (c1/c0)^(1/psi) with 1 - a = 1/psi); the quiz explanation matches Definition 2.1. Symbol change is consistent across the lesson and cards."},
 {"id": "E3g15-L06-changes", "check": "2.2/2.3/2.6 L06 changed text: Proposition 1.4 and proof, Section 4 bullets, Key results rows, misconception, quiz item L06q2, lab text", "location": "course/modules/E/E3/L06.html Proposition 1.4 and proof, Remark 3.2 cross-reference, section 4, section 5 first misconception, section 7 rows, quiz item L06q2", "status": "PASS",
  "evidence": "Round 15: Proposition 1.4 (v'' < 0 on x > 0 gives strict concavity on [0, infinity) by continuity; v'' = lambda delta (1 - delta)(-x)^(delta - 2) > 0 on x < 0; strictly increasing from positive derivatives on both half-lines and continuity at 0) is proved in full by the printed proof; the sign convention reference to A2 of L02 (u'' <= 0) is a correct pointer; Remark 3.2 now restricts the threshold formula lambda_R to alpha = delta, which is the only case in which Remark 3.2 derives it; the midpoint wording describes a finite midpoint convexity check (graded C)."},
 {"id": "E3g15-L07-changes", "check": "2.2/2.3 L07 changed text: why-it-matters, Remark 1.6, Example 1.4 reference, section 4 third misconception exercise solution, Key results", "location": "course/modules/E/E3/L07.html why-it-matters paragraph, Remark 1.6, section 2 discussion solution (R3), section 6 key results", "status": "PASS",
  "evidence": "Round 15: Remark 1.6 arithmetic recomputed (0.31945492 + 0.57158177 = 0.89103669; lottery B weight 0.39125077); the Lesson 4 Theorem 1.5 pointer and the 'values of Example 1.4' pointer resolve to the right statements; the discussion solution's prediction (A under the non-cumulative form, B under dominance-respecting forms) follows from Proposition 2.2 and Theorem 1.5; no empirical claim is made."},
 {"id": "E3g15-L08-changes", "check": "2.3/2.7 L08 changed text: section 6 first misconception and its A3 reference; card E3-c154", "location": "course/modules/E/E3/L08.html section 6 first misconception (line 486 of the source); cards.json E3-c154", "status": "PASS",
  "evidence": "Round 15: the misconception now names A3 of Proposition 2.4 (w_red > w_no, bets pay on own colour); Proposition 2.4 statement and proof (line 176) support P_0 for red and P_90 for black; card E3-c154 carries the same hypothesis. Round-14 FAIL resolved."},
 {"id": "E3g15-lab-twin-L06", "check": "2.5 changed lab twin lab-E3-L06-1 (midpoint label and print line)", "location": "tests/labs/E3/lab-E3-L06-1.py; course/modules/E/E3/L06.html section 3 Lab 1", "status": "PASS",
  "evidence": f"Round 15: {SC}/twin_check.py: 'L06 lab-E3-L06-1 page_code_equals_twin=True expected_equals_stdout=True rc=0 stderr=''' (out/twin_check.out). Twin alone under python -I -W error prints the 13 expected lines."},
 {"id": "E3g15-numbers", "check": "2.2/2.5 independent recomputation of the numbers printed or stated in the slice (L05-L08)", "location": f"{SC}/numbers_L05_L08.py; out/numbers_L05_L08.out", "status": "PASS",
  "evidence": "Round 15: Fraction and Decimal (50 digits) recomputation of every number in the changed hunks and the card numbers: omega values, sums, ratio 0.7304544982, thresholds, G(A), G(B), 40-digit differences, grid crossing (sign changes 1, last point 0.278), closed-form gap 3.33e-16, eta = 1 gap 0.3126 at p = 0.862, EU and prospect and maxmin CEs, EZ identities, L06 threshold and W(2). All agree with the page text within the stated rounding."},
 {"id": "E3g15-attributions", "check": "2.3/2.5 bibliographic attributions in L07 and L08 (title-only uses)", "location": "references/references.json entries kahneman1979prospect, ellsberg1961risk, gilboa1989maxmin, epstein1989substitution; course/modules/E/E3/L07.html section 1 and references; L08.html section 1, Example 2.5, section 5 and 8", "status": "PASS",
  "evidence": "Round 15: registry records read in full: kahneman1979prospect (Kahneman, Tversky; 1979; Econometrica; 'Prospect Theory: An Analysis of Decision under Risk'), ellsberg1961risk (Ellsberg; 1961; 'Risk, Ambiguity, and the Savage Axioms'), gilboa1989maxmin (Gilboa, Schmeidler; 1989; 'Maxmin expected utility with non-unique prior'). The page claims are title-only and match these records; no theorem, locator or number is attributed to any of them."},
 {"id": "E3g15-gate-check-and-build", "check": "2.9 build and render gates for the slice", "location": "tools/build_site.py --check; tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "status": "PASS",
  "evidence": "Round 15 gates.sh: 'site data current: 6 outputs' (build_site_check); render_curriculum rc 0 and the subsequent 'git diff --exit-code' rc 0 (no generated-file drift)."},
 {"id": "E3g15-gate-run-labs", "check": "2.5 run_labs for L05-L08 (program-wide lab runner)", "location": "tools/run_labs.py --unit E3 --page L05..L08", "status": "PASS",
  "evidence": "Round 15 gates.sh: 'run_labs E3: PASS (1/1)' for each of L05, L06, L07, L08 (out/run_labs_L0x.out)."},
]

fragment = {
    "unit": "E3",
    "slice": "g",
    "round": 15,
    "verifier": "Haiku 5.5 independent verifier, slice g, round 15 (delta verification)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "1431aa1d842a5d2d05fd5953c098500bf78a4307 (round-14 pin; previous fragment /Users/billyribeiro/.fanout/frags/D-E3-g.round14.json)",
    "checkout": ROOT,
    "scratch": "/Users/billyribeiro/.fanout/scratch/E3-g-r15",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "round_note": "Round 15 delta: slice L05-L08 lessons, cards for those lessons, and the L06 lab twin. Every card and lesson in the slice was re-read against the current text; prior rows are re-verified rather than carried.",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice: E3 L05-L08 lessons, the 87 retrieval cards of L05 (22), L06 (19), L07 (18 plus card E3-c187 kept under L07), L08 (28), and the four lab twins. Mutants: none. Lessons and cards are not a project slice, so no grader mutation applies (VERIFIER rulings: lab twins are demonstrations).",
        "Round-14 FAIL on E3-c154 (lost Proposition 2.4 hypothesis A3) is resolved at dde0486b: the card and the L08 section 6 misconception both state A3, and the worst priors P_0 (red) and P_90 (black) follow from the proof.",
        "Delta 1431aa1d..dde0486b inside the slice: L05 (Remark 1.5 wording, EIS symbol in Definition 2.1 and Proposition 2.2 proof, quiz explanation), L06 (Proposition 1.4 statement and proof, lab print and label, section 4 bullets, key results, misconception, quiz option), L07 (why-it-matters, Remark 1.6, discussion solution, key results), L08 (section 6 first misconception), cards c083, c101, c106 (grade C to T), c117, c154, and the L06 twin.",
        "Points checked and not treated as defects: the L06 midpoint check (finite convexity inequality, labelled as a midpoint test, graded C); the L02 A2 sign-convention pointer (A2 defines concavity by u'' <= 0); the L08 Section 4 Model 4 worst prior at P(red) = 1/3 is computed in Model 4, while Example 1.4 only defines the set.",
        "Out-of-slice observations (not rated): course/modules/E/E3/L01.html and cards L01 use tau for the mixture weight (renamed to rho in dde0486b; see slice E3-f); the hub index.html worked-example rung now says the participant is SIMULATED; both belong to other slices.",
        "Not checked: live Crossref run of verify_refs (references/ unchanged since round 14; the offline gate was run); run_graders and mutate_graders (no project grader in this slice; project E3 is covered by another slice); a browser screenshot beyond page_smoke; the Epstein-Zin lab grid beyond the printed values.",
    ],
    "summary": {},
}

from collections import Counter
counts = Counter(r["status"] for r in rows)
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "card_rows": len(card_order) + 1,
    "mutants": 0,
    "mutants_killed": 0,
}
path = f"{ROOT}/ledgers/E3/E3-g.json"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", path, fragment["summary"])
