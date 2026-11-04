"""Writes ledgers/SC1/SC1-e.json (round 6) from the rows verified in this round. Usage: write_fragment.py <pin> <verified_at>"""
import json
import sys
from pathlib import Path

PIN, VERIFIED_AT = sys.argv[1], sys.argv[2]
ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE6-SC1-e")
R = "ledgers/SC1/scripts/SC1-e-r6"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


row("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json", "PASS",
    f"{R}/dump_cards.py -> {R}/out/cards_dump.txt: 194 cards, 194 distinct ids, SC1-c001 to c204; absent ids 36, 85, 125, "
    "147, 158, 160, 163, 177, 190, 192 (round 6 removed c147 and c192 since round 5). Keys: 138 graded cards carry grade and "
    "basis (117 T, 21 C), 56 ungraded cards carry neither; cite is [] on all 194. Per lesson: L01 18, L02 25, L03 21, L04 25, "
    "L05 31, L06 27, L07 25, L08 22. Every card was read against its lesson text in the statement rows below.")

row("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all 18721 pairs)", "PASS",
    f"{R}/dup_and_numbers.py -> {R}/out/dup_and_numbers.out: difflib ratios on front, back and joined text; 281 pairs pass the "
    "loose threshold. The four highest joined ratios were read: c064/c202 (Assumption 4.2(a) and (b), different parts), "
    "c117/c118 (inclusion and sample-path statement, different claims), c161/c167 (tau_a and nu_a, different objects), "
    "c196/c198 (A4(d) and A4(f), different parts). The rest share wording, not claims. The same-claim pair is c116/c162 "
    "(row SC1e-c116-c162-duplicate).")

row("SC1e-learner-text-scan", "2.9-prose", "cards front and back; lesson text L01 to L08", "PASS",
    f"Regex over the cards and {R}/out/L01.txt to L08.txt for round, verif*, builder, fixer, ledger, mutant, grader, TODO, lorem, "
    "draft, fragment, we, our, I: the only hits are mathematical ('we have', 'verify the limit', 'fixed' as a state), no process words.")

row("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a number token", "PASS",
    f"{R}/out/dup_and_numbers.out: 1495 number tokens on the 194 cards; the script reports none that is absent from the card's "
    "lesson text ({R}/out/L0n.txt from lesson_text.py) and its lab stdout ({R}/out/labs/).")

row("SC1e-lab-numbers-vs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to L08-1.py", "PASS",
    f"tools/run_labs.py --unit SC1: 'run_labs SC1: PASS (11/11)' ({R}/out/run_labs.out). Each lesson twin run as python -I -W error "
    f"from /tmp: exit 0 and stderr 0 bytes ({R}/out/labs/*.stderr). Every stdout line of the eight lesson twins occurs in its lesson "
    "text (grep -F over out/L0n.txt: 6, 12, 35, 7, 8, 17, 23, 20 lines, 0 missing). The L02 twin changed in its docstring only; the "
    "run output is unchanged. Lab-derived card numbers were recomputed in the rows below.")

row("SC1e-exact-numbers-recomputed", "2.2-numbers", "cards c010, c027, c030, c039, c052, c057, c059, c111 to c114, c129, c140, c141, c148 to c150, c159, c165, c170 to c174, c179 to c183, c187, c201", "PASS",
    f"{R}/indep_numbers.py -> {R}/out/indep_numbers.out: c111 1014 triples, identity on 1014 of 1014; c112 78 pairs; c113 281/512, "
    "11/32, 105/512 = C(10,6)/1024; c114 495 and 495; c148 14893 + 6885 = 21778, 21778/65536 = 0.332306; c171 counts "
    "512, 0, 384, 0, 288, 0, 224, 0, 180, 0, sum 1588, 1588/4096 = 0.387695 and 794/4096 = 0.193848; c172 5.480560, 11.815731, "
    "24.557203; c174 0.317311 and 0.241971 at H=1, 0.479500 and 0.109848 at H=2; c201 0.1586552539 and 0.3173105079; c159 SE "
    "0.0230; c150 gap 0.0393 = 1.24 SE; c141 1/sqrt(2 pi); c165 density central difference agrees. "
    f"{R}/indep_walks.py -> {R}/out/indep_walks.out (exact dynamic programming, no lab code): L07 Part A tails 0.375000, 0.332306, "
    "0.321084, 0.318255, 0.317547 for N = 4, 16, 64, 256, 1024; L08 Part B 5.480560, 11.815731, 24.557203; L08 Part A first-passage "
    "counts equal 2^(12-k) times (1, 3, 9, 28, 90) for k = 3, 5, 7, 9, 11; L06 Part D 281/512 and 11/32. "
    f"{R}/l02_numbers.py: L02 Lab 1 per-level sup and bound to six decimals, 2 x unrounded sup = 0.23317869 which rounds to 0.233179, "
    "2 x printed 0.116589 = 0.233178 (E3 correct), 0.832555 = sqrt(4 log 2)/2, grid sup 0.348139, bound sum 1.309399. "
    "Phi(-1/sqrt 2) = 0.23975006 (c104, L05 quiz). e^8 = 2980.957987 (L04 E2, E3).")

row("SC1e-L03-gap", "2.5-labs", "card c187; tests/labs/SC1/lab-SC1-L03-1.py", "PASS",
    f"{R}/l03_gap.py on {R}/out/labs/lab-SC1-L03-1.stdout (16 printed SEs against H sqrt(2/N)/20): largest signed gap +13.21% at "
    "H=2, N=1; smallest -6.60% at H=2, N=2; max |gap| 13.2% < 14%, as c187 says.")

row("SC1e-L01-statements", "2.9-prose", "course/modules/SC/SC1/L01.html; cards c001 to c017, c186", "PASS",
    f"L01 read in full ({R}/out/L01.txt, 484 lines). Checked D1 to D3 (c004), Var(B_t)=t (c005), the Gaussian-process paragraph (c006 "
    "matches it word for word in substance), Proposition 1.2 hypotheses H1, H2 (c007), Remark 1.3 (c008), Example 1.4 (c009, c016: "
    "1/sqrt(1/100)=10), Lab 1 15 of 15 and 81 of 81 (c010), Section 4 items 2 and 3 and the misconception answers (c011 to c013, "
    "c014, c015, c017), dyadic partition definition (c186), Problems M1 to M3, P1 to P3, E1 to E3, R1 to R3 and the quiz. "
    "Defects in this lesson are the separate rows SC1e-render-raw-lt (line 115) and SC1e-L01-U-existence.")

row("SC1e-L02-statements", "2.9-prose", "course/modules/SC/SC1/L02.html; cards c018 to c041, c184, c185", "PASS",
    f"L02 read in full ({R}/out/L02.txt, 603 lines). Re-derived Lemma 2.2(a) to (e) including the parity argument in (c) (c021 to c024, c185), "
    "Lemma 2.1 (c025), Lemma 2.3 variances 2^-(n+2) + 2^-(n+2) = 2^-(n+1) and covariance 2^-(n+2) - 2^-(n+2) = 0 (c026 to c028), "
    "Proposition 2.4(a) P(E_m^c) <= 2^-m and P(A^c) <= 2^(1-m0) (c029), 2.4(b) M_m = sqrt(2 log 2) sqrt(m) 2^(-m/2) and "
    "sum m r^m = r/(1-r)^2 (c030, c031), steps 3 and 4 (c032), Theorem 2.5 (c034), Remark 2.6 steps W continuous and D2, D3 (c035), "
    "Section 4 dyadic counterexample arithmetic, Section 5 harmonic bound 1 + k/2 (c039), scale 2^-(m+1)/2 (c040), f_n = t^n (c041), "
    "Lab 1 216 of 216, True, the eight level bounds and 8 of 8, and the last line (SC1e-L02 twin checked by l02_numbers.py). "
    "Exercises M1 to M3, P1 to P3, E1 to E3 and R1 to R3 checked. The raw '<' at line 313 is row SC1e-render-raw-lt.")

row("SC1e-L03-statements", "2.9-prose", "course/modules/SC/SC1/L03.html; cards c042 to c060, c187, c188", "PASS",
    f"L03 read in full ({R}/out/L03.txt, 529 lines). Re-derived Lemma 2.1 (integration by parts, boundary term tends to 0), Lemma 2.2, "
    "Theorem 2.3 (mean, variance 2 sum Delta^2, bound 2 t |P|) (c044 to c048), Proposition 2.4(a) and (b) with S(N) = N(4N^2-1)/3 by "
    "induction (c049, c050), Section 3 canon breaks (Gaussian fourth-moment constant 3, c053; variance 2t^2, c054), Section 4 "
    "misconceptions (E|Z| = sqrt(2/pi), sqrt(2Nt/pi), c056 to c058), Problems M1 to M3, P1 to P3, E1 to E3 (SE 0.0707 and 0.0125), "
    "R1 to R3, quiz values 0.625 and 2.65625; c055, c059, c060 match their lesson parts.")

row("SC1e-L04-statements", "2.9-prose", "course/modules/SC/SC1/L04.html; cards c061 to c082, c202 to c204", "PASS",
    f"L04 read in full ({R}/out/L04.txt, 517 lines). Re-derived Lemma 2.1, Propositions 2.2 to 2.4 (E B_t^4 = 3t^2; E(B_t^2 - t)^2 = "
    "2t^2; E Z_t^2 = e^(theta^2 t) via E W^2 = e^(theta^2 h), E W = 1), the link remark (c069), Section 3 drift counterexample, "
    "Section 4 misconceptions (E[B_t^3 | F_s] = B_s^3 + 3(t-s) B_s, E e^(theta B_t) = e^(theta^2 t/2)), Lab 1 values e^1, e^(1/4), e^4 "
    "and 1.000000000, Problems M1 to M3, P1 to P3, E1 to E3, R1 to R3, quiz (3t^2 = 27 at t = 3). c064, c202, c203, c204 match "
    "Assumption 4.2(a) to (d) item by item.")

row("SC1e-L05-statements", "2.9-prose", "course/modules/SC/SC1/L05.html; cards c083 to c105, c189, c193 to c200", "PASS",
    f"L05 read in full ({R}/out/L05.txt, 562 lines). Re-derived Lemma 1.3 (grouping; pi-system of cylinder events), Theorem 1.4 "
    "(freezing and substitution y = z + w), Remark 1.5 (no continuity used), Lemma 2.2 (expansion; constant terms), Theorem 2.1 "
    "(Gaussian integral gives p_{u+v}), Section 3 A3 sketch (rho_n bounds, countable values), R1 (paths 1 and 2 agree on [0, 1/2] "
    "with sigma* = 1/4 and 3/4), R3 (k = floor(2^n r)), M1 (1/(2 sqrt pi)), M2 (psi(x) = x^2 + 2 and x^3 + 6x), M3, P1 (Lemma 2.2 at "
    "u = 1, v = 3, x = 0, y = 1), P2, P3, E1 (ratio 1.457e13), E2 (5e-11), E3 (3.05e-16 is 1.4 eps), quiz values. A4(a) to (h) items "
    "match c193 to c200 one per card. c189 matches Section 3.")

row("SC1e-L06-statements", "2.9-prose", "course/modules/SC/SC1/L06.html; cards c106 to c124, c126 to c133", "PASS",
    f"L06 read in full ({R}/out/L06.txt, 587 lines). Re-derived Lemma 1.2 (S'_k = 2a - S_k), Proposition 1.3 (bijection), Corollary 1.4 "
    "(map b -> 2a - b onto integers above a), Lemma 2.1(i) to (iii) (IVT), Proposition 2.3 explicit form and proof (rho = tau_a and t, "
    "X_{t-rho}, h_- = h_+ by symmetry), Theorem 2.5 (E = {W_t > a}, no atom), Corollary 2.6 (z = sqrt2 w), M1 (1/(2 sqrt pi) = "
    "p_2(0,0)), M3 (S = (0,1,2,1,0,1), kappa = 2, S' = (0,1,2,3,4,3)), P1 to P3, R1 (parity), R2 (min B), R3, E1 to E3. Part A "
    "1014 triples, Part B 78 pairs and Part C 1588 and 495 re-derived by reflection counts; Part D 281/512, 11/32, 105/512; Part E "
    "0.3173105079 and 0.1586552539.")

row("SC1e-L07-statements", "2.9-prose", "course/modules/SC/SC1/L07.html; cards c134 to c159, c191", "PASS",
    f"L07 read in full ({R}/out/L07.txt, 629 lines). Re-derived Theorem 1.3 (erfc form), Remark 1.4, Corollary 1.5(a) (limit from "
    "below, m = 0 case) and (b) (integration by parts; 0 <= R(1 - Phi(R)) <= phi(R); E M_H = sqrt(2H/pi)), Definition 2.1 with s_k, "
    "Proposition 2.2(a) and (b), Corollary 2.3, Remark 2.4 (max(0, B_H)), Part A exact tails (indep_walks.out), Part B counts 91, 107, "
    "113, 121 and gaps -0.0898, -0.0498, -0.0348, -0.0148 (labs_L07.stdout), Part C means and the 0.0393 gap (1.24 SE), Part D "
    "0.1586552539 by erfc and by Simpson, E2 (21778 = 14893 + 6885), E3 (33759/63840000, SE 0.0230), R1 to R3, M1 to M3, P1 to P3, "
    "E1 and the quiz answers except the decimal request, which is row SC1e-L07-quiz-digits.")

row("SC1e-L08-statements", "2.9-prose", "course/modules/SC/SC1/L08.html; cards c161 to c183, c201", "PASS",
    f"L08 read in full ({R}/out/L08.txt, 614 lines). Re-derived Proposition 1.2 both directions (IVT, B at tau_a = a), Corollary 1.3, "
    "Corollary 1.4 (limit of 2(1 - Phi(a/sqrt n)) = 1), Corollary 1.5 density (derivative of F(H) = 2(1 - Phi(a H^(-1/2))) gives "
    "f_a), Remark 1.6, Proposition 2.2 (S_{nu} = a at first hit), Proposition 2.3 (indicator sum), Part A (90114 pairs, 8190 "
    "sequences, 1588), Part B and Part C z values, Part D values and densities (0.241971, 0.109848), E1 to E3, M1 to M3, P1 to P3, "
    "R1 (2 x 794 = 1588), R2, R3 (mode a^2/3), Section 3 jump example, Section 4 misconceptions. The quiz decimal requests are row "
    "SC1e-L08-quiz-digits.")

row("SC1e-hypotheses-carried", "2.9-prose", "cards c029, c032, c035, c006, c008, c040, c145, c153, c162", "PASS",
    "L02 Proposition 2.4 (H2) and Remark 2.6 (H1) match c029, c032 and c035 (round-4 fixes still present). c006 and c008 match the "
    "L01 Gaussian-process paragraph. c040, c145 and c153 state the hypotheses of their lesson results. c162 states Proposition 1.2 "
    "H1 and H2 correctly; its wrong content is row SC1e-c116-c162-duplicate.")

row("SC1e-grades-audit", "2.3-grades", "cards with grade and basis", "PASS",
    f"{R}/out/cards_dump.txt grade/basis counter: (T, basis) 117, (C, basis) 21, (None, no basis) 56. The 21 C cards are c010, c037, "
    "c038, c051, c072, c091, c092, c111, c112, c113, c114, c127, c148, c149, c150, c170 to c174, c187; each is a lab-derived number "
    "and names its lab (Lab 1 of L01 to L08), as BLUEPRINT grade C requires. T cards cite a proof, a derivation or a lab-free "
    "argument in basis.")

row("SC1e-cites-and-registry", "2.1-citations", "cards (cite field); lesson References sections", "PASS",
    "cite is [] on all 194 cards (dump_cards.py). No lesson attributes a result to a registry key. L03 and L07 name Shreve, "
    "Stochastic Calculus for Finance II, as the curriculum source with registry key shreve2004stochastic and no locator; that title "
    "equals references/references.json line 20737. verify_refs.py was not re-run: the registry is untouched and no card cites a key.")

row("SC1e-dag-and-concepts", "2.9-dag", "course/modules/SC/SC1/L0[1-8].html; cards", "PASS",
    f"{R}/out/check_dag.out: 'check_dag SC1: PASS'. Cards name no concept link. Two lessons name results of a later or earlier "
    "lesson without linking a concept: L01 Section 4 uses Remark 2.6 of Lesson 2 (a construction), and L06 Section 2 and L05 Section 3 "
    "name Lesson 8 and Lesson 6 results. These are result references, the pages say so, and no concept is used before definition. "
    "Noted, not failed.")

row("SC1e-notation-registry", "2.9-notation", "notation/notation.json; course/modules/SC/SC1/L03.html, L07.html; cards", "PASS",
    "T appears only in the reserved-symbol notes (out/L03.txt line 113, out/L07.txt line 54), not as a horizon. Phi appears only as the "
    "standard normal CDF. No use of \\mathbb{Q}, \\gamma_3, \\gamma_4, R_f, R^\\ast or R^{e\\ast}. Local symbols (M_H, tau_a, nu_a, "
    "S_k, Sigma_M, Lambda_{m,j}, F(H), f_a) are not registered and do not collide with a registered meaning.")

row("SC1e-c126-c160-duplicate", "2.7-cards", "cards c126, c191 (c160 absent)", "PASS",
    "c126 tests the tail misconception P(M_t >= a) = P(B_t >= a); c191 tests P(M_H <= 0) against P(B_H <= 0). Different claims that "
    "share a misconception wording, accepted under the round-4 ruling on misconception restatements.")

row("SC1e-c116-c162-duplicate", "2.7-cards", "cards c116 (course/modules/SC/SC1/L06.html Lemma 2.1(i)) and c162 (L08.html Proposition 1.2)", "FAIL",
    f"c116 states {{M_t >= a}} = {{tau_a <= t}} (continuous path, B_0 = 0, a > 0). c162 now states, in its front, that Proposition 1.2 "
    "gives {tau_a <= H} = {M_H >= a} on every path with those hypotheses, and asks whether P(tau_a <= H) = P(M_H >= a) needs A3 or "
    f"A4; its back says the events coincide on every such path. It is the same identity, tested twice in two lessons. The round-5 "
    f"ruling (row SC1e-c116-c192-event-identity, c192 rewritten) forbids this. Evidence: {R}/out/cards_dump.txt and "
    f"{R}/out/cards_round5_pin.json (the 7376a5e2 text).",
    "Restore c162 to its text at 7376a5e2 (git show 7376a5e2:course/modules/SC/SC1/cards.json): front 'Proposition 1.2. Hypotheses: "
    "for a fixed outcome, s->B_s is continuous and B_0=0; a>0 and H>=0 are fixed. On the event {tau_a<=H}, what is the value of B at "
    "tau_a?', back 'B_(tau_a)=a. On {tau_a<=H}, tau_a is finite and is the infimum of the closed set {s: B_s=a}, so it belongs to "
    "that set.', grade T, basis 'Proof of Proposition 1.2, Section 1'.")

row("SC1e-c058-path-claim", "2.9-prose", "card c058; course/modules/SC/SC1/L03.html Section 4", "PASS",
    "c058 back says nothing about a single path is established and that Theorem 2.3 makes no pathwise claim; this matches L03 "
    "Section 4 third item and the paragraph after Theorem 2.3.")

row("SC1e-c153-grade", "2.3-grades", "card c153; course/modules/SC/SC1/L07.html Section 4", "PASS",
    "c153 is graded T with its basis naming Proposition 2.2(a), Corollary 2.3 and Theorem 1.3, which are the results its back uses.")

row("SC1e-c177-basis", "2.7-cards", "card c177 (absent)", "PASS",
    "c177 is absent from cards.json (absent id list in SC1e-structure-ids), so no basis exists to check.")

row("SC1e-c030-typo", "2.2-numbers", "card c030; course/modules/SC/SC1/L02.html Proposition 2.4(b) step 2", "PASS",
    "M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2) re-derived by hand; sum m r^m = r/(1-r)^2 with r = 2^(-1/2) "
    "re-derived. Also l02_numbers.py: the printed bound column equals sqrt(4 m log 2) 2^(-(m+1)/2) for m = 1 to 8.")

row("SC1e-c035-remark-2.6", "2.9-prose", "card c035; course/modules/SC/SC1/L02.html Remark 2.6", "PASS",
    "The back (copies glued over unit intervals; D1 to D3 for W; continuous paths) matches the lesson's Conclusion and proof, and "
    "the hypotheses (H1 copies, A1(a), A1(b), A1(e), A2, Assumption 2.1) are on the front.")

row("SC1e-c145-hypothesis", "2.9-prose", "card c145; course/modules/SC/SC1/L07.html Corollary 2.3", "PASS",
    "The front states H1 (continuous paths) and the grid event inclusion, matching Corollary 2.3 and its proof.")

row("SC1e-c153-hypothesis", "2.9-prose", "card c153; course/modules/SC/SC1/L07.html Section 4", "PASS",
    "The front names the continuous-path hypothesis (Proposition 2.2(a)) and the closed form of Theorem 1.3, matching the lesson's answer.")

row("SC1e-c176-hypothesis", "2.9-prose", "card c176; course/modules/SC/SC1/L08.html Corollary 1.4", "PASS",
    "The back states A3 and A4 of Lesson 5, and A3 is stated for a standard Brownian motion with continuous paths, so the continuity "
    "hypothesis H1 of Proposition 1.2 is carried by the assumption the card names.")

row("SC1e-c126-c177-duplicate", "2.7-cards", "cards c126 and c177 (absent)", "PASS",
    "c177 is absent; no pair remains.")

row("SC1e-c125-c175-jump-example", "2.7-cards", "card c175; course/modules/SC/SC1/L08.html Section 3", "PASS",
    "c125 is absent. c175 is the only card on the jump counterexample: 0 on [0, 1/2), jump to 2, stays at 2, so M_1 = 2 and tau_1 = "
    "infinity; this matches L08 Section 3 first item.")

row("SC1e-c155-c158-assumption-carried", "2.9-prose", "card c155; course/modules/SC/SC1/L07.html Problem M2 (c158 absent)", "PASS",
    "c155 matches Problem M2: P(M_H >= a) depends on (a, H) only through a/sqrt(H), with closed form 2(1 - Phi(a/sqrt H)). c158 is absent.")

row("SC1e-c184-c187-new-cards", "2.9-prose", "cards c184, c185 (L02), c186 (L01), c187 (L03)", "PASS",
    "c184 matches the L02 dyadic-time definition; c185 matches Lemma 2.2(c) and its proof; c186 matches the L01 dyadic-partition "
    "definition; c187 is the L03 gap (row SC1e-L03-gap).")

row("SC1e-c188-c189-new-cards", "2.9-prose", "cards c188 (L03 Assumption 3.1), c189 (L05 Section 3)", "PASS",
    "c188 states |P_n| -> 0 as Assumption 3.1 does. c189 gives the definition of F_rho in Section 3 of L05 (A in F with A cap {rho <= r} "
    "in F_r for all r).")

row("SC1e-c032-prop24b-scope", "2.9-prose", "card c032; course/modules/SC/SC1/L02.html Proposition 2.4(b) steps 3 and 4", "PASS",
    "The back says sup_t |Sigma - Sigma_M| <= sum over m > M of M_m for every M >= m0 on A_(m0), matching Step 3 of the proof.")

row("SC1e-c085-atomicity", "2.7-cards", "card c085 (absent); cards c193 to c200", "PASS",
    "c085 is absent and each A4 part has its own card (c193 to c200), matching the lesson's items (a) to (h).")

row("SC1e-c028-c036-duplicate", "2.7-cards", "card c028; card c036 (absent)", "PASS",
    "c036 is absent. c028 (zero covariance with joint normality gives independence) is the only card on that step.")

row("SC1e-c055-c058-overlap", "2.7-cards", "cards c055, c058", "PASS",
    "Both mention that no pathwise claim is established. c055 asks it as a fact; c058 is a misconception with a different wrong belief "
    "(the quadratic variation is a random number). Accepted under the round-4 ruling. Noted, not failed.")

row("SC1e-c151-c154-overlap", "2.7-cards", "cards c151, c154", "PASS",
    "Both say the tail formula does not apply to B-tilde. c154 is a misconception with a different wrong belief (any process with "
    "normal one-time marginals has the tail). Accepted under the round-4 ruling. Noted, not failed.")

row("SC1e-c009-c016-overlap", "2.7-cards", "cards c009, c016", "PASS",
    "c009 gives the standard deviation sqrt(h); c016 is the misconception 'order h' with the same fact. Different wrong belief; accepted.")

row("SC1e-c129-c179-overlap", "2.7-cards", "cards c129 (L06), c179 (L08)", "PASS",
    "Same walk and same count 5/8 for P(nu_1 <= 3) and M_3 >= 1, but c129 asks the running-maximum count and c179 asks the first-passage "
    "probability. Different objects; noted.")

row("SC1e-c164-c176-overlap", "2.7-cards", "cards c164, c176", "PASS",
    "c164 asks the value of P(tau_a < infinity) (1). c176 tests the misconception that finiteness means every path is finite. Different claims.")

row("SC1e-A4-assumption-cards", "2.9-prose", "cards c193 to c200 (L05 A4(a) to (h)); c064, c202 to c204 (L04 Assumption 4.2)", "PASS",
    "Each card states one part of the named assumption with the lesson's wording ('standard fact, not proved here'). The L05 set is "
    "complete for (a) to (h); the L04 set (a) to (d) is complete.")

row("SC1e-c201-locator", "2.2-numbers", "card c201; L07 Lab 1 Part D; L08 Lab 1 Part D", "PASS",
    f"0.317311 is printed by the L08 twin (out/labs/lab-SC1-L08-1.stdout, Part D). 0.1586552539 is printed by the L07 twin (out/labs/lab-SC1-L07-1.stdout, Part D). "
    "The back cites both; the closed form 2(1 - Phi(a/sqrt H)) = erfc(a/sqrt(2H)) is Corollary 1.3.")

row("SC1e-L07-def21-notation", "2.9-prose", "course/modules/SC/SC1/L07.html Definition 2.1; card c142", "PASS",
    "Definition 2.1 uses s_k = kH/N for k = 0 to N and M^(N)_H = max_k B_(s_k); c142 matches it. The round-4 notation fix stays.")

row("SC1e-page-smoke-L05-L06", "2.9-structure", "course/modules/SC/SC1/L01.html to L08.html", "PASS",
    f"tools/page_smoke.py --unit SC1 --pages L01 ... L08 --skip-labs: all eight pages PASS, 'page_smoke SC1: PASS' ({R}/out/page_smoke_L01_L08.out). "
    f"This PASS does not detect the hidden-text defect in SC1e-render-raw-lt: see {R}/out/raw_tags_L01.out and raw_tags_L05.out.")

row("SC1e-gates-check-pages-dag", "2.9-structure", "course/modules/SC/SC1/", "PASS",
    f"tools/check_pages.py --unit SC1: PASS ({R}/out/check_pages.out). tools/check_dag.py --unit SC1: PASS ({R}/out/check_dag.out). "
    f"pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py: all pass ({R}/out/pytest_labs_pages.out). "
    f"ruff check and ruff format --check on tests/labs/SC1/: pass ({R}/out/ruff_check_labs.out).")

row("SC1e-render-raw-lt", "2.9-structure", "course/modules/SC/SC1/L01.html line 115; L02.html line 313; L05.html lines 121, 398; L06.html lines 82, 83, 107, 114, 135, 168, 169 (two), 369 (three), 376, 470; L08.html line 137", "FAIL",
    f"{R}/raw_lt.py over all eight pages -> {R}/out/raw_lt.out: 19 raw '<' followed by a letter inside \\( \\) spans (L01 2, L02 1, "
    "L05 2, L06 13, L08 1). Each one starts an HTML start tag. {R}/raw_tags.py (out/raw_tags_L01.out, raw_tags_L05.out, "
    "raw_tags_L02.out, raw_tags_L08.out and raw_tags.out (L06)) shows the parser's start tags with non-HTML names, e.g. 't_1<\\dots<t_r\\)' at L01 "
    "line 115 (new in round 6, introduced by the rewritten Gaussian-process paragraph) and 'a)\\)<' at L06 line 470. The text up to the "
    "next '>' is swallowed by the browser. page_smoke passes, so it does not catch this.",
    "In each listed math span replace the literal '<' with '&lt;' (for example '0&lt;t_1&lt;\\dots&lt;t_r', 'j&lt;k', 'B_t&lt;a'); "
    "MathJax then sees the same '<'. Then rerun raw_lt.py on all eight pages (must print 0) and page_smoke.")

row("SC1e-c116-c192-event-identity", "2.7-cards", "cards c116 (L06), c192 (absent), c162 (L08)", "PASS",
    "c192 is absent, so the round-5 pair (c116 and c192, both stating the event identity) no longer exists. The identity "
    "{M_t>=a} = {tau_a<=t} is tested on c116; the residual repeat through c162 is row SC1e-c116-c162-duplicate, which is FAIL. "
    "This row is PASS with respect to c192 only.")

row("SC1e-dup-tau-vs-max", "2.7-cards", "cards c192 (removed), c137, c201", "PASS",
    "c192 is absent (round 6 removed it). c201 now states the misconception answer with the closed form and the A3/A4 hypothesis, "
    "matching the Corollary 1.3 closed form that c137 states for the running maximum. The two are different questions (first passage "
    "versus terminal value and running maximum); no card asks the same question twice.")

row("SC1e-semantic-duplicates", "2.7-cards", "cards c112 (L06), c147 (absent)", "PASS",
    "c147 is absent. c112 is the only card that asks how many (N, a) pairs the tail identity checks; its answer 78 matches Part B.")

row("SC1e-L01-U-existence", "2.9-prose", "course/modules/SC/SC1/L01.html Section 4, first item (line 215); cards c011 to c013, c017", "FAIL",
    "The first item says Remark 2.6 of Lesson 2 gives a continuous-path B 'on a probability space that carries independent "
    "coefficient families', and then says 'Let U be uniform on (0,1) and independent of B' and defines B-tilde with U. Nothing in the "
    "text shows that the space carries such a U; Lesson 2 H1 and Remark 2.6 H1 only assume the coefficient families and copies. The "
    "counterexample, its cards and its Key result row need the existence of U. Evidence: L01.html line 215 and "
    f"{R}/out/L01.txt; the statement is a proof gap, not a numerical one.",
    "Add to the sentence: 'on a probability space that carries independent coefficient families and also a uniform U independent of "
    "B (for example the product of the space of Remark 2.6 with ((0,1), uniform law), which leaves the law and the continuous paths of "
    "B unchanged)'. Keep the rest of the item.")

row("SC1e-L07-quiz-digits", "2.2-numbers", "course/modules/SC/SC1/L07.html, quiz item 'Assuming A3 and A4, what is P(M_1 >= 1) to seven decimals?'", "FAIL",
    "The question asks for seven decimal places; the answer prints 0.3173105079, which is ten decimal places. Printed-digit mismatch of the kind "
    "in BUILDER_RULES rounding: the requested precision and the displayed digits disagree. Numerical value itself is correct "
    "(out/indep_walks.out: erfc(1/sqrt 2) = 0.3173105079).",
    "Change the answer to 0.3173105 (seven decimals), or change the question to 'to ten decimals'.")

row("SC1e-L08-quiz-digits", "2.2-numbers", "course/modules/SC/SC1/L08.html, quiz items 'P(tau_1 <= 1) to seven decimals' and 'E[min(nu_1,16)] to five decimals'", "FAIL",
    "Two quiz items disagree with the printed digits. (a) 'to seven decimals' is answered with 0.3173105079 (ten decimals). (b) 'to five "
    "decimals' is answered with 5.480560 (six decimals). Values are correct (out/indep_walks.out: 5.480560; erfc(1/sqrt 2) = 0.3173105079).",
    "(a) print 0.3173105. (b) print 5.48056 or ask 'to six decimals'.")

notes = [
    "Round 6 at pin 4bd8cb9 (checkout detached). Delta since round 5 (pin 7376a5e2), saved as "
    f"{R}/out/delta_since_round5.diff: course/modules/SC/SC1/cards.json (c006, c008, c038, c040, c136, c144 reworded; c147 and c192 removed; c162 and c201 reworded), "
    "L01 to L08 html (why-it-matters, A4/A3 cross-references, the L01 Section 4 item, L02 lab-docstring-matching prose, L07 Definition "
    "and Remark wording, L08 interpretation), tests/labs/SC1/lab-SC1-L02-1.py (docstring only), index.html (outside this slice). "
    "Every lesson and every card was re-read at this pin; no round-5 PASS row is carried, because every subject changed.",
    "Round-5 rows: SC1e-render-raw-lt still FAIL (and grew by 2 in L01); SC1e-dup-tau-vs-max PASS (c192 removed); "
    "SC1e-c116-c192-event-identity PASS (c192 removed) but the identity reappears in c162, row SC1e-c116-c162-duplicate FAIL; "
    "SC1e-semantic-duplicates PASS (c147 removed). All other round-5 PASS rows are re-verified above with fresh evidence.",
    "Mutants: not applicable to a cards slice (no grader); the list is empty by design, as in rounds 4 and 5.",
    "Not checked: rendered pages in a browser (no screenshot; the hidden-text defect was established from the parser's start tags); "
    "index.html (changed line, outside slice e) and project.html and its labs (other slices); Pyodide execution of the labs "
    "(page_smoke ran with --skip-labs; run_labs ran the twins under CPython -I -W error); verify_refs (registry untouched, cards cite "
    "nothing); mypy (no typed Python source changed in this slice beyond a docstring; ruff and pytest run instead). "
    "A1(d) of L01 is listed but used by no SC1 page (noted, not a failure).",
    "Lab-derived numbers were checked two ways: by the lab twin run at this pin (out/labs) and by an independent re-derivation "
    "(indep_numbers.py, indep_walks.py, l02_numbers.py, l03_gap.py) that does not import lab code.",
]

fragment = {
    "unit": "SC1",
    "slice": "e",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e: all 194 cards of course/modules/SC/SC1/cards.json against lessons L01 to L08; round 6",
    "pin": PIN,
    "base": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "checkout": str(ROOT),
    "scratch": f"{R}/out",
    "verified_at": VERIFIED_AT,
    "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": "",
}
n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
fragment["summary"] = (
    f"SC1-e round 6 at {PIN}: {len(rows)} rows (pass={n_pass} fail={n_fail} unverifiable={n_unv}); verdict FAIL. "
    "FAILs: SC1e-render-raw-lt (19 raw '<' in math, L01 line 115 new), SC1e-c116-c162-duplicate (c162 restates c116), "
    "SC1e-L01-U-existence (U independent of B not shown to exist), SC1e-L07-quiz-digits, SC1e-L08-quiz-digits (quiz decimal request "
    "does not match the printed digits). Every card and every lesson was read in full; every lab value and card number re-derived."
)
def fill(obj):
    if isinstance(obj, str):
        return obj.replace("{R}", R)
    if isinstance(obj, list):
        return [fill(x) for x in obj]
    if isinstance(obj, dict):
        return {k: fill(v) for k, v in obj.items()}
    return obj


fragment = fill(fragment)
out = ROOT / "ledgers" / "SC1" / "SC1-e.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", n_pass, "fail", n_fail)
