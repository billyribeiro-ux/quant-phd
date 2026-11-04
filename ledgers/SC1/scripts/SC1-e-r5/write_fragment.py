"""Writes the round-5 fragment ledgers/SC1/SC1-e.json (rows, notes, summary). Run from the checkout root."""
import json

S = "ledgers/SC1/scripts/SC1-e-r5"
O = f"{S}/out"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


CARDS = "course/modules/SC/SC1/cards.json"

row("SC1e-structure-ids", "2.7 structure: ids, keys, lesson counts, grade/basis pairing", CARDS, "PASS",
    f"{S}/dump_cards.py -> {O}/cards_dump.txt: 196 cards, 196 distinct ids (c001 to c204). Absent ids 36, 85, 125, 158, 160, 163, 177, 190. Keys: 140 graded cards carry grade and basis; 56 ungraded carry neither; cite is [] on all 196. Per lesson L01 18, L02 25, L03 21, L04 25, L05 31, L06 27, L07 26, L08 23 (sum 196). check_pages SC1 PASS (out/check_pages.out).")

row("SC1e-near-duplicate-scan", "2.7 full pairwise duplicate scan of fronts and backs", f"{CARDS} (all 19110 pairs)", "PASS",
    f"{S}/dup_and_numbers.py -> {O}/dup_and_numbers.out. difflib ratios on front, back and joined text. No pair is a copy. Highest is SC1-c064/c202 (front 0.78, back 0.81), which test different parts (a) and (b) of Assumption 4.2. Semantic overlaps are in the rows SC1e-semantic-duplicates, SC1e-c116-c192-event-identity and the overlap rows.")

row("SC1e-learner-text-scan", "2.7 no process words in learner text", f"{CARDS} front and back", "PASS",
    "Regex scan (round, verif, builder, TODO, draft, fragment, ledger, mutant, grader, we, our, I, fix, audit, reviewer, pending) over 196 cards: 27 hits, all benign ('fixed' as a mathematical state, index 'i' in t_i, 'fix' in 'fixed').")

row("SC1e-card-numbers-in-lesson", "2.7 every card number appears in its lesson text or lab stdout", CARDS, "PASS",
    f"{S}/dup_and_numbers.py -> {O}/dup_and_numbers.out: 1494 number tokens on the 196 cards; each token occurs in its own lesson text ({O}/L01.txt to L08.txt, from {S}/lesson_text.py) or in its lab stdout ({O}/labs/). Zero misses.")

row("SC1e-lab-numbers-vs-run", "2.5 lab twins run; card numbers equal the printed lab output", "tests/labs/SC1/lab-SC1-L01-1.py to L08-1.py; cards with a lab basis", "PASS",
    f"tools/run_labs.py --unit SC1: 'run_labs SC1: PASS (11/11)' ({O}/run_labs.out). Each twin run as python -I -W error from /tmp: exit 0, stderr 0 bytes ({O}/labs/*.stderr), second run byte-identical to first. Every stdout line of the eight lesson twins occurs verbatim in its lesson text ({O}/L0n.txt; zero misses).")

row("SC1e-exact-numbers-recomputed", "2.7 exact and derived numbers re-derived by my own code (no lab code reused)", f"cards c010, c027, c030, c039, c052, c057, c059, c111 to c114, c140, c141, c148, c149, c150, c159, c165, c170 to c174, c179, c181, c183", "PASS",
    f"{S}/indep_numbers.py -> {O}/indep_numbers.out: 1014 triples (c111, and the identity holds on 1014 of 1014 by my enumeration); 78 pairs (c112); 281/512, 11/32, 105/512 and C(10,6)/1024 (c113); 495 and 495 (c114); 5 of 8 (c129); 14893 + 6885 = 21778 = 0.332306 (c148); 90114 pairs and 8190 sequences (c170); first-passage counts [512,0,384,0,288,0,224,0,180,0] summing to 1588, P(nu_3<=12)=397/1024 and P(S_12>=3)=397/2048 (c171, corrected in this round); truncated means 5.480560, 11.815731, 24.557203 (c172); P(tau_1<=1)=0.317311, density 0.241971 at H=1, 0.479500 and 0.109848 at H=2 (c174); erfc(1/sqrt2)=0.3173105079 (c115); sqrt(2/pi)=0.797885 with gap 0.0393 = 1.24 SE (c150); SE sqrt(33759/63840000)=0.0230 (c159); E[M_1]=sqrt(2/pi) by quadrature (c140); integral of 1-Phi on [0,13] = 1/sqrt(2 pi) (c141); central difference of 2(1-Phi(a/sqrt H)) matches the density (c165).")

row("SC1e-L03-gap", "2.7 c187: printed SE versus H*sqrt(2/N)/20", "SC1-c187; tests/labs/SC1/lab-SC1-L03-1.py", "PASS",
    f"{S}/l03_gap.py on {O}/labs/lab-SC1-L03-1.stdout -> {O}/l03_gap.out: 16 printed SEs. Largest signed gap +13.21 percent at H=2, N=1; smallest -6.60 percent at H=2, N=2; max |gap| 13.2 percent, within the card's 14 percent.")

row("SC1e-L01-statements", "2.7 cards c001 to c017 and c186 against the L01 text", "SC1-c001 to c017, c186; course/modules/SC/SC1/L01.html", "PASS",
    f"L01 read in full ({O}/L01.txt, 484 lines). Checked D1 to D3 (c004), Var(B_t)=t (c005), Prop 1.2 with H2 A1(a) and min(s,t) (c007), Remark 1.3 with H2 A1(b),(a) (c008), Example 1.4 and 1/sqrt(1/100)=10 (c009, c016), Lab 1 15 of 15 and 81 of 81 (c010; labs/lab-SC1-L01-1.stdout), Section 4 construction B-tilde (c011 to c013, c017), Section 5 misconceptions (c015, c017), dyadic partition (c186). Proof of Prop 1.2 read at L01 lines 96 to 102: it uses D1 to D3 and A1(a) only (c014).")

row("SC1e-L02-statements", "2.7 cards c018 to c041, c184, c185 against the L02 text", "SC1-c018 to c041, c184, c185; L02.html", "PASS",
    f"L02 read in full ({O}/L02.txt, 603 lines). Checked Definition 2.1 (c018, c019), H1 (c020), Lemma 2.2(a) to (e) (c021 to c024, c185), Lemma 2.1 (c025), Lemma 2.3 with variances 2^(-(n+2))+2^(-(n+2))=2^(-(n+1)) and covariance 0 (c026 to c028), Prop 2.4(a) with P(E_m^c)<=2^(-m) and P(Omega*)=1 (c029), step 1 to 2 with M_m=sqrt(2 log 2) sqrt(m) 2^(-m/2) (c030, c031), Prop 2.4(b) (c032), A2 (c033), Thm 2.5 (c034), Remark 2.6 (c035), misconceptions (c039 to c041), Lab 1 216 = 2*9+3*8+5*7+9*6+17*5 with 36 pairs and 17 points (c037; {O}/labs/lab-SC1-L02-1.stdout) and 8 of 8 (c038). c184 matches the L02 definition of a dyadic time.")

row("SC1e-L03-statements", "2.7 cards c042 to c060, c187, c188 against the L03 text", "SC1-c042 to c060, c187, c188; L03.html", "PASS",
    f"L03 read in full ({O}/L03.txt, 529 lines). Checked Lemma 2.1 and 2.2 (c044, c045), Thm 2.3 mean, variance and error bound (c046 to c048), Prop 2.4(a),(b) with S(N)=N(4N^2-1)/3 re-derived (c049, c050), Lab 1 largest |z| 2.39 at H=1, N=2 and next 1.84 (c051; labs stdout), c052 SE formula, canon breaks (c053, c054 with Var(Q)=2t^2 re-derived), c055 to c058 (c058 'Not settled' matches the no-pathwise-claim sentence), R2 constant 2 (c059), Assumption 3.2 and 3.1 (c060, c188), c057 sqrt(2Nt/pi) re-derived.")

row("SC1e-L04-statements", "2.7 cards c061 to c082, c202 to c204 against the L04 text", "SC1-c061 to c082, c202 to c204; L04.html", "PASS",
    f"L04 read in full ({O}/L04.txt, 517 lines). Checked Def 1.1, 1.2 (c061, c062, c065), Assumption 4.1 (c063), Assumption 4.2(a) to (d) (c064, c202, c203, c204 match the lesson's (a) to (d)), Lemma 2.1 (c066), Props 2.2 to 2.4 (c067, c068, c070, c071; E[Z_t^2]=e^(theta^2 t) re-derived), remark (c069), Lab 1 54.598150033 and 1.000000000 (c072; labs stdout), misconceptions (c073 to c078; E[B_t^3 | F_s]=B_s^3+3(t-s)B_s re-derived), R1 to R3 (c079 to c082), P2 and P3 (c081, c082).")

row("SC1e-L05-statements", "2.7 cards c083 to c105, c189, c193 to c200 against the L05 text", "SC1-c083 to c105, c189, c193 to c200; L05.html", "PASS",
    f"L05 read in full ({O}/L05.txt, 562 lines). Checked Def 1.1, 1.2 (c083, c084), A4(a) to (h) (c193 to c200, one part per card, matching the lesson's items (a) to (h)), Lemma 1.3, Thm 1.4, Remark 1.5 (c086 to c088), Lemma 2.2 completing-the-square identity re-derived and Thm 2.1 (c089, c090), Lab 1 225 cases, 5.55e-16, 1.0000000000 (c091, c092; labs stdout), A3 and R1 to R3 (c093 to c099; sigma* example re-checked), misconceptions (c100 to c102), M2 with B_1^2+2 (c103), P2 with Phi (c104), M3 (c105), F_rho (c189).")

row("SC1e-L06-statements", "2.7 cards c106 to c133 against the L06 text", "SC1-c106 to c133; L06.html", "PASS",
    f"L06 read in full ({O}/L06.txt, 587 lines). Checked Def 1.1 (c107), Lemma 1.2 (c108), Prop 1.3 (c109), Cor 1.4 (c110), Lab 1 Parts A to D (c111 to c114; labs stdout 1014, 78, 281/512, 11/32, 105/512, 495, 495), Lemma 2.1(i) to (iii) (c116 to c118), Def 2.2 and Prop 2.3 (c119 to c121), Remark 2.4 (c122), Thm 2.5 (c123), Cor 2.6 (c124), misconceptions (c126 to c128), M1 5 of 8 (c129), R1 to R3 (c130 to c132), c133. Passage-level hidden text in this lesson is row SC1e-render-raw-lt; no card depends on a hidden span alone.")

row("SC1e-L07-statements", "2.7 cards c134 to c157, c159, c191 against the L07 text", "SC1-c134 to c157, c159, c191; L07.html", "PASS",
    f"L07 read in full ({O}/L07.txt, 629 lines). Checked Def 1.1 (c134, c135), Def 1.2 (c136), Thm 1.3 (c137), Remark 1.4 (c138), Cor 1.5(a) and (b) with int(1-Phi)=1/sqrt(2 pi) (c139 to c141), Def 2.1 with s_k (c142), Prop 2.2(a),(b) (c143, c144), Cor 2.3 (c145), Remark 2.4 (c146), Lab 1 Part A 78 of 78 (c147), Part A exact 21778 and 0.332306 (c148), Part B 0.2275, 0.3025, SE 0.0210, 0.0230, 0 violations (c149), Part C 0.7586, SE 0.0317 (c150), misconceptions (c151 to c154), M2 (c155), R1, R2 (c156, c157), E3 SE (c159), c191 with P(M_H<=0)=0 and P(B_H<=0)=1/2 from Cor 1.5(a) at m=0. c158 is absent.")

row("SC1e-L08-statements", "2.7 cards c161 to c176, c178 to c183, c201 against the L08 text", "SC1-c161 to c176, c178 to c183, c201; L08.html", "PASS",
    f"L08 read in full ({O}/L08.txt, 614 lines). Checked Def 1.1 (c161), Prop 1.2 (c162), Cor 1.4 (c164), Cor 1.5 density (c165), Remark 1.6 (c166), Def 2.1 (c167), Prop 2.2 and 2.3 (c168, c169), Lab 1 Part A 90114 and 78 (c170), first-passage counts and 1588 (c171), Part B truncated means (c172), Part C z values -1.05, -0.69, -0.77 (c173; labs stdout), Part D (c174; labs stdout), jump example (c175), misconceptions (c176, c178), M3 5/8 (c179), E1 parity (c180), R1 (c181), R2 (c182), R3 mode a^2/3 (c183), and c201 (misconception, locators checked: 0.317311 is printed by L08 Part D, 0.1586552539 by L07 Part D). c177 is absent. The closed-form wording of c192 is row SC1e-dup-tau-vs-max.")

row("SC1e-hypotheses-carried", "2.7 cards carry the hypotheses of the proposition they state", "SC1-c029, c032, c035; L02.html Prop 2.4 (H2), Remark 2.6 (H1)", "PASS",
    f"Round-4 FAIL is fixed. The fronts of c029 and c032 now define (H2) with E_m, A_(m0)=cap E_m and Omega*=union A_(m0) ({O}/cards_dump.txt). The front of c035 carries (H1): copies built from their own coefficients and mutually independent. Checked against L02 lines for Prop 2.4 (H2) and Remark 2.6 (H1). Cards c007, c008, c046 to c048, c067, c068, c070, c137, c145, c162 also carry their hypotheses.")

row("SC1e-grades-audit", "2.7 grade and basis of every graded card", "graded cards (140: 118 T, 22 C)", "PASS",
    f"{S}/dump_cards.py -> {O}/cards_dump.txt grade/basis counter: 118 T with basis, 22 C with basis, 56 ungraded with no basis. C is used only on lab-derived numeric cards (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c147 to c150, c170 to c174, c187), which matches the Key-results grade of the same lab row in each lesson. c127 is C although Cor 1.4 is T; the grade is conservative and is not a fail.")

row("SC1e-cites-and-registry", "2.7 cite fields against references/references.json", CARDS, "PASS",
    "cite is [] on all 196 cards; no registry key is cited, so there is no registry key to check. No lesson attributes a result to a registry key (each lesson's References section states this).")

row("SC1e-dag-and-concepts", "DAG: concepts used by cards and lessons are in the unit closure", "course/modules/SC/SC1/L01.html to L08.html; cards", "PASS",
    f"check_dag SC1 PASS ({O}/check_dag.out). Cards name no concept link. Each card's concept is defined in its own lesson or in an earlier SC1 lesson (checked card by card during the L01 to L08 reads).")

row("SC1e-notation-registry", "13. notation: symbols against notation/notation.json", "notation/notation.json; cards", "PASS",
    "Registry symbols: T, \\Phi (and \\Phi^{-1}), gamma_3, gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. Cards use T only in the reserved-symbol note (in lesson text, L03 line 113 and L07 line 54, not on any card). Phi appears only as the standard normal CDF (c104, c137, c139, c155), which the registry allows. \\mathbb{Q} does not appear. Plain Q is the quadratic variation (c042 and L03), not registered and not \\mathbb{Q}. F(H) in c165 and in the L08 Cor 1.5 proof is a CDF while \\mathcal F is the sigma-field in L04 to L06: F is not registered, so this is a noted overlap, not a registry collision.")

row("SC1e-c126-c160-duplicate", "2.7 duplicates: misconception cards c126 (L06) and c191 (L07)", "SC1-c126; SC1-c191", "PASS",
    "Round-4 FAIL is fixed by the narrowing that round-4 asked for. c191 now asks P(M_H<=0)=0 against P(B_H<=0)=1/2 (Cor 1.5(a) at m=0), a fact c126 does not test. c126 keeps the tail misconception P(M_t>=a)=P(B_t>=a). The two cards share the misconception wording, which the round-4 ruling on misconception restatements allows.")

row("SC1e-c116-c162-duplicate", "2.7 duplicates: c116 (L06 Lemma 2.1(i)) against c162 (L08 Prop 1.2)", "SC1-c116, SC1-c162", "PASS",
    "c116 states {M_t>=a}={tau_a<=t}. c162 states B at tau_a equals a on {tau_a<=H}. Different claims. The second identity duplicate, c192 against c116, is row SC1e-c116-c192-event-identity.")

row("SC1e-c058-path-claim", "2.7 c058 (L03 misconception on a random quadratic variation)", "SC1-c058; L03.html Section 4", "PASS",
    "Back says 'Nothing about a single path is established' and that Theorem 2.3 makes no pathwise claim, which matches L03 Section 4 third item and the sentence after Theorem 2.3.")

row("SC1e-c153-grade", "2.7 grade of c153 (L07 misconception on grid tails)", "SC1-c153; L07.html Section 4", "PASS",
    "c153 is graded T with basis 'Proposition 2.2(a), Corollary 2.3, Theorem 1.3', matching the Key-results rows for Prop 2.2 and Cor 2.3 (T).")

row("SC1e-c177-basis", "2.7 basis on the deleted card c177", CARDS, "PASS",
    "SC1-c177 is absent from cards.json, so there is no basis to check.")

row("SC1e-c030-typo", "2.7 formula on c030 (L02 Prop 2.4(b) step 2)", "SC1-c030; L02 Section 3, Proposition 2.4(b) step 2 (out/L02.txt)", "PASS",
    "M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2) re-derived by hand (2*2^(-(m+1)/2)=2^((1-m)/2)); sum of m r^m = r/(1-r)^2 with r=2^(-1/2) re-derived. Correct.")

row("SC1e-c035-remark-2.6", "2.7 card c035 against Remark 2.6 and its proof", "SC1-c035; L02.html Remark 2.6", "PASS",
    "The back (glues independent copies, proves D1 to D3 and continuous paths) matches the Conclusion and proof. The hypothesis is now on the front (see SC1e-hypotheses-carried).")

row("SC1e-c145-hypothesis", "2.7 hypothesis of c145 (L07 Cor 2.3)", "SC1-c145; L07.html Cor 2.3", "PASS",
    "Front states H1 (continuous paths) and the grid event inclusion, matching Corollary 2.3 and its proof.")

row("SC1e-c153-hypothesis", "2.7 hypothesis of c153 (L07 Section 4)", "SC1-c153", "PASS",
    "Front states 'On continuous paths' and Prop 2.2(a), Cor 2.3 and Thm 1.3 (closed form under A3, A4), matching the lesson's answer.")

row("SC1e-c176-hypothesis", "2.7 hypothesis of c176 (L08 Section 4)", "SC1-c176; L08.html Cor 1.4", "PASS",
    "Back states A3 and A4 of Lesson 5. Cor 1.4 also needs H1 and H2 of Prop 1.2 (continuous paths). A3 is stated for a standard BM with continuous paths, so continuity is carried by the stated assumption.")

row("SC1e-c126-c177-duplicate", "2.7 duplicate check for c126 against deleted c177", "SC1-c126; SC1-c177 absent", "PASS",
    "c177 is absent, so no pair remains. The c126 vs c191 pair is row SC1e-c126-c160-duplicate.")

row("SC1e-c125-c175-jump-example", "2.7 duplicates: jump counterexample on c125 (L06) and c175 (L08)", "SC1-c125 (absent), SC1-c175", "PASS",
    "Round-4 FAIL is fixed: c125 is absent. c175 is the only card on the jump counterexample; its example (0 on [0,1/2), jump to 2, stays at 2; M_1=2 but tau_1 = infinity) matches L08 Section 3 first item.")

row("SC1e-c155-c158-assumption-carried", "2.7 c155 (L07 M2) and the absent c158", "SC1-c155; SC1-c158 absent", "PASS",
    "c155 matches L07 Problem M2: P(M_H>=a) depends on (a,H) only through a/sqrt(H), closed form 2(1-Phi(a/sqrt H)). c158 is absent.")

row("SC1e-c184-c187-new-cards", "2.7 newly appended cards c184 to c187", "SC1-c184, c185 (L02); SC1-c186 (L01); SC1-c187 (L03)", "PASS",
    "c184 (dyadic time of depth n) matches L02 Section 1. c185 (Lemma 2.2(c)) matches L02 Lemma 2.2(c) and its proof: t = 2i 2^(-m) with 2i-(2j-1) odd. c186 matches L01 Section 3. c187 gap +13.2 percent at H=2, N=1 (row SC1e-L03-gap).")

row("SC1e-c188-c189-new-cards", "2.7 newly appended cards c188 and c189", "SC1-c188 (L03 Assumption 3.1), SC1-c189 (L05 Section 3)", "PASS",
    "c188 (|P_n| to 0) matches Assumption 3.1. c189 (F_rho = events A in F with A cap {rho<=r} in F_r for all r) matches L05 Section 3.")

row("SC1e-c032-prop24b-scope", "2.7 round-3 FAIL: c032 drops the M >= m0 qualifier", "SC1-c032; L02.html Prop 2.4(b) steps 3 and 4", "PASS",
    "The back reads 'On Omega*, S_M converges uniformly ... If the outcome lies in A_(m0), sup|S-S_M| <= sum_{m>M} M_m for every M >= m0', matching Step 3 of the proof.")

row("SC1e-c085-atomicity", "2.7 atomicity of the eight-part card c085 (A4 (a) to (h))", "SC1-c085 (absent); SC1-c193 to c200", "PASS",
    "Round-4 FAIL is fixed. c085 is absent and each A4 part has its own card (c193 to c200), matching L05 Assumption A4 items (a) to (h).")

row("SC1e-c028-c036-duplicate", "2.7 duplicates: c028 and c036 (round-4 FAIL)", "SC1-c028; SC1-c036 (absent)", "PASS",
    "Round-4 FAIL is fixed: c036 is absent. c028 (Lemma 2.3 covariance zero plus joint normality gives independence) is the only card on that step.")

row("SC1e-c055-c058-overlap", "2.7 overlap: c055 (no almost-sure limit) and c058 (misconception on a random quadratic variation)", "SC1-c055; SC1-c058", "PASS",
    "Both state that no pathwise claim is established. c055 is a fact question. c058 is a misconception with a different wrong belief (QV is a random number that changes from path to path). Accepted under the round-4 ruling that misconception restatements with a different wrong belief are kept. Noted, not failed.")

row("SC1e-c151-c154-overlap", "2.7 overlap: c151 (tail not asserted for B-tilde) and c154 (misconception: same one-time laws give the same tail)", "SC1-c151; SC1-c154", "PASS",
    "Both state that the tail formula is not asserted for B-tilde, which has the same one-time laws as B and discontinuous paths. c154 is a misconception with a different wrong belief (any process with normal one-time marginals has the closed-form tail). Accepted under the round-4 ruling. Noted as an overlap for the builder to consider.")

row("SC1e-c009-c016-overlap", "2.7 overlap: c009 (SD of short increment is sqrt h) and c016 (misconception of order h)", "SC1-c009; SC1-c016", "PASS",
    "c016 is a misconception with the wrong belief 'increment of order h'; c009 is the fact. Accepted under the round-4 ruling on misconception restatements. Noted, not failed.")

row("SC1e-c129-c179-overlap", "2.7 overlap: c129 (5 of 8 for M_3>=1) and c179 (P(nu_1<=3)=5/8)", "SC1-c129 (L06); SC1-c179 (L08)", "PASS",
    "Same walk, same count 5/8, and the same event by L08 Prop 2.2. c179 asks the first-passage probability, which is the Prop 2.2 instance, while c129 asks the running-maximum count. Noted as an overlap; not failed because the questions name different objects.")

row("SC1e-c164-c176-overlap", "2.7 overlap: c164 (P(tau_a<inf)=1) and c176 (misconception: finite on every path)", "SC1-c164; SC1-c176", "PASS",
    "c164 asks the value 1. c176 tests the misconception that finiteness means every path is finite and says the event {tau_a=inf} is not shown to be empty. Different claims. Noted.")

row("SC1e-A4-assumption-cards", "2.7 assumption cards c193 to c204 (standard facts, not proved here)", "SC1-c193 to c200 (L05 A4(a) to (h)); SC1-c202 to c204 (L04 Assumption 4.2(b) to (d))", "PASS",
    "Each card states one part of the named assumption, with the lesson's own wording ('standard fact, not proved here' and 'assumed, not proved'). c064 is Assumption 4.2(a) and the new c202 to c204 are (b) to (d), so the set is complete for L04 and matches the lesson's item list.")

row("SC1e-c201-locator", "2.7 locators on c201 (misconception P(tau_a<=H)=P(B_H>=a))", "SC1-c201; L08 Lab 1 Part D; L07 Lab 1 Part D", "PASS",
    f"0.317311 is printed by L08 Lab 1 Part D ({O}/labs/lab-SC1-L08-1.stdout). 0.1586552539 is printed by L07 Lab 1 Part D (course/modules/SC/SC1/L07.html lab output; re-run in {O}/labs/lab-SC1-L07-1.stdout gives 1-Phi(1)). The back cites both, so each number has its printed source.")

row("SC1e-L07-def21-notation", "Lesson notation: Definition 2.1 of L07 uses an undefined index", "course/modules/SC/SC1/L07.html Definition 2.1; SC1-c142", "PASS",
    f"Round-4 FAIL is fixed. L07 Definition 2.1 now reads M^(N)_H = max_(0<=k<=N) B_(s_k) with s_k = kH/N ({O}/L07.txt line 112). c142 matches it.")

row("SC1e-page-smoke-L05-L06", "page_smoke on the pages where cards carry proof text", "course/modules/SC/SC1/L02, L05, L06, L08 .html", "PASS",
    f"tools/page_smoke.py --unit SC1 --pages L02 L05 L06 L08 --skip-labs: all four pages PASS ({O}/page_smoke_L02_L05_L06_L08.out). This PASS does not detect the hidden-text defect in row SC1e-render-raw-lt.")

row("SC1e-gates-check-pages-dag", "2.9 check_pages and check_dag for SC1", "course/modules/SC/SC1/", "PASS",
    f"tools/check_pages.py --unit SC1: PASS ({O}/check_pages.out). tools/check_dag.py --unit SC1: PASS ({O}/check_dag.out).")

# FAIL rows
row("SC1e-render-raw-lt", "Lesson markup: raw '<' inside math spans hides learner text in the browser",
    "course/modules/SC/SC1/L02.html raw line 313; L05.html raw lines 121, 398; L06.html raw lines 82, 83, 107, 114, 135, 168, 169 (two), 369, 376, 470; L08.html raw line 137", "FAIL",
    f"{S}/raw_lt.py -> {O}/raw_lt.out: 17 raw '<' followed by a letter inside \\( \\) spans (L02 1, L05 2, L06 13, L08 1). Each opens an HTML tag, so the parser drops text up to the next '>'. {S}/raw_vs_escaped.py -> {O}/raw_vs_escaped.out shows the text that disappears: L02 line 313 (the Remark 2.6 formula for W_t); L05 line 121 (last sentence of the Thm 1.4 proof, 'for all 0<=s<=t'); L05 line 398 (R2 solution, 'the set is empty for r<s'); L06 lines 82 and 83 (Prop 1.3 proof); L06 line 107 (Lemma 2.1 statement, part (iii)); L06 lines 114, 369 (Lemma 2.1 proofs); L06 line 135 (Prop 2.3 proof); L06 lines 168 and 169 (Thm 2.5 proof); L06 line 376 (P3 solution); L06 line 470 (quiz option, shows only '\\(\\Prob(S_N'); L08 line 137 (Prop 2.3 proof). check_pages and page_smoke pass despite this.",
    "In each listed span replace the raw '<' with '&lt;' (for example \\(s&lt;t\\)), leaving every other character unchanged. Then rerun raw_lt.py (expect 0 hits) and page_smoke --pages L02 L05 L06 L08 to confirm the hidden sentences appear in the rendered text.")

row("SC1e-dup-tau-vs-max", "2.7 wording and duplicate: c192 (L08 Corollary 1.3)", "SC1-c192 (course/modules/SC/SC1/cards.json)", "FAIL",
    "c192 asks 'which of its two equalities needs no probability assumption'. The L08 Corollary 1.3 chain has three equalities: P(tau_a<=H)=P(M_H>=a)=2(1-Phi(a/sqrt H))=erfc(a/sqrt(2H)). The back says 'the closed form 2(1-Phi(a/sqrt H))=erfc(a/sqrt(2H)) needs A3 and A4'. That attributes an assumption to an identity between two functions (Corollary 2.6 of L06 proves it with no assumption). Only the link P(M_H>=a)=2(1-Phi(a/sqrt H)) needs A3 and A4 (Theorem 1.3 of L07). The closed form repeats c137, which tests 2(1-Phi)=erfc under the same assumptions.",
    "Delete SC1-c192 (its pathwise identity is already tested by SC1-c116, and its closed form by SC1-c137). If it is kept, rewrite it to test only the link: front 'Which link in P(tau_a<=H)=P(M_H>=a)=2(1-Phi(a/sqrt H))=erfc(a/sqrt(2H)) needs no probability assumption, and which needs A3 and A4?'; back 'The first link is the pathwise identity {tau_a<=H}={M_H>=a} (Proposition 1.2) and needs none. The second needs A3 and A4 (Theorem 1.3 of Lesson 7). The erfc identity needs none (Corollary 2.6 of Lesson 6).'")

row("SC1e-c116-c192-event-identity", "2.7 duplicate: c116 (L06 Lemma 2.1(i)) and c192 (L08 Prop 1.2 / Cor 1.3) state one identity", "SC1-c116; SC1-c192", "FAIL",
    "Both state {M_t>=a}={tau_a<=t} (or {tau_a<=H}={M_H>=a}) for a continuous path with B_0=0 and a>0. c116's hypotheses are the same as Proposition 1.2's H1 and H2. The same identity is on two cards in two lessons; the deck should test it once.",
    "Delete SC1-c192 (see SC1e-dup-tau-vs-max), or delete SC1-c116 and keep the L08 statement, which the L08 chain uses.")

row("SC1e-semantic-duplicates", "2.7 semantic duplicates across the deck (surviving pairs)", "SC1-c112 (L06 Part B); SC1-c147 (L07 Part A)", "FAIL",
    "c112 asks how many (N,a) pairs the tail identity of L06 Cor 1.4 checks and whether all agree (answer: 78, all 78 agree). c147 asks how many (N,a) pairs the same identity holds for in L07 Part A (answer: all 78 pairs). Same question, same answer, same lab check. The round-4 pairs c028/c036, c125/c175 and c126/c191 are fixed or narrowed (see their PASS rows), and c137/c192 is row SC1e-dup-tau-vs-max.",
    "Delete SC1-c147 (keep SC1-c112 in L06, which is the lesson that defines the lab part), or reword c147 to a different fact about the count (for example the 21778-walk tail, which is already SC1-c148).")

mutants = []
notes = [
    "Round 5 pin 7376a5e2 (base 9a02b1af, round 4). Delta since base: cards.json (now 196 cards: c036, c085, c125 removed; c193 to c204 added), L01 to L08 html, project.html, index.html, tests/labs/SC1 L02 and L08 twins. Every card and every lesson was re-read in full at this pin; no round-4 PASS row is carried, because every subject changed.",
    "Mutants: not applicable to a cards slice (no grader); the list is empty by design, as in round 4.",
    "Re-verified round-4 non-PASS rows: SC1e-hypotheses-carried (now PASS), SC1e-c126-c160-duplicate (now PASS by narrowing), SC1e-c125-c175-jump-example (now PASS, c125 removed), SC1e-c085-atomicity (now PASS, c085 removed), SC1e-c028-c036 (now PASS), SC1e-L07-def21-notation (now PASS), SC1e-render-raw-lt (still FAIL, now 17 raw '<' in L02, L05, L06, L08), SC1e-dup-tau-vs-max (still FAIL; c192 rewritten but still wrong and still overlaps c116/c137), SC1e-semantic-duplicates (still FAIL for the surviving pairs; new pair c112/c147 added).",
    "Overlap rows marked PASS under the round-4 ruling on misconception restatements: c009/c016, c055/c058, c151/c154, c129/c179, c164/c176, c126/c191. These are noted for the builder but are not failures.",
    "Counts and grades: 22 C cards are lab-derived and match the lesson Key-results grades; c127 is C while Cor 1.4 is T (conservative, not a fail).",
    "Notation: no registered symbol is reused. F(H) (CDF) in c165 and L08 is not registered; plain Q for quadratic variation is not registered (\\mathbb{Q} is). Noted only.",
    "Scope not checked: ruff, mypy and pytest (no Python source in this slice changed; the slice is cards.json and the lesson text); verify_refs (cards cite nothing, registry untouched); a browser screenshot of the hidden-text defect (the parser behaviour was checked on the raw source instead); the L04 Section 3 cross-reference to 'Lesson 8 of M6' (the M6 text is outside this slice).",
]
summary = ("SC1-e round 5 at 7376a5e2: all 196 cards read against full L01 to L08 text. "
           f"{len(rows)} rows: {sum(r['status']=='PASS' for r in rows)} PASS, {sum(r['status']=='FAIL' for r in rows)} FAIL. "
           "FAIL: SC1e-render-raw-lt (17 raw '<' in math hides text in L02, L05, L06, L08; page_smoke and check_pages pass), "
           "SC1e-dup-tau-vs-max (c192 attributes an assumption to the erfc identity and restates c137), "
           "SC1e-c116-c192-event-identity (c192 duplicates c116), "
           "SC1e-semantic-duplicates (c147 duplicates c112). "
           "Every exact number was re-derived; all 11 lab twins pass under python -I -W error and their printed lines appear in the lessons. "
           "Round-4 FAILs fixed: hypotheses on c029, c032, c035; c125, c085, c036 removed; c191 narrowed; L07 Definition 2.1 now uses s_k.")

frag = {
    "unit": "SC1",
    "slice": "e",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e (all 196 cards of course/modules/SC/SC1/cards.json against lessons L01 to L08); round 5; did not build SC1",
    "pin": "7376a5e216c1e6d99becc76b4cd64028f5b55d3f",
    "base": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba (round-4 pin; round-4 fragment /Users/billyribeiro/.fanout/frags/E-SC1-e.round4.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE5-SC1-e (detached at 7376a5e2, .venv symlinked, vendor copied)",
    "scratch": f"{S}/out (lesson_text outputs L01.txt to L08.txt, cards_dump.txt, labs/ stdout and stderr, all numeric and gate outputs)",
    "verified_at": "2026-11-04T17:56:07Z",
    "verdict": "FAIL",
    "scope_note": "Slice e = all 196 cards of course/modules/SC/SC1/cards.json at 7376a5e2 (SC1-c001 to c204; absent c036, c085, c125, c158, c160, c163, c177, c190) checked against L01 to L08 full text.",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
with open("ledgers/SC1/SC1-e.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows), "fail", sum(r["status"] == "FAIL" for r in rows))
