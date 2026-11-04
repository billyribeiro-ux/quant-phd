import json, sys
P = "PASS"; F = "FAIL"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)

S = "course/modules/SC/SC1/"
row("SC1e-structure-ids", "2.7 structure: ids, keys, duplicates, grade/basis pairing",
    S + "cards.json (187 cards)", P,
    "ledgers/SC1/scripts/SC1-e-r4/dump.py -> out/cards_dump.txt: 187 cards, 187 distinct ids; keys {id,lesson,front,back,cite} on 46 ungraded cards and plus grade,basis on 141; cite empty on all 187; per lesson L01 17, L02 26, L03 22, L04 22, L05 24, L06 28, L07 26, L08 22. Id gaps c158, c160, c163, c177, c190 absent. check_pages SC1 PASS (out/check_pages.out).")
row("SC1e-near-duplicate-scan", "2.7 full duplicate scan (difflib ratio >= 0.6 on front and back)",
    S + "cards.json (all pairs)", P,
    "ledgers/SC1/scripts/SC1-e-r4/dup_scan.py -> out/dup_schema.out: 0 duplicate fronts, 0 duplicate backs; 48 pairs with a ratio >= 0.6, each read; none is a verbatim or near-verbatim copy. Semantic duplicates are in row SC1e-semantic-duplicates.")
row("SC1e-L01-statements", "2.7 cards c001 to c017 against L01 text",
    S + "cards.json SC1-c001 to c017; L01.html sections 1 to 5, Lab 1, Key results", P,
    "L01 re-read in full (/tmp/sc1e_r4/L01.txt; L01.html changed since round 3). Checked D1 to D3 (c004), Var(B_t)=t (c005), Prop 1.2 with H2 A1(a) and min(s,t) (c007), Remark 1.3 (c008), Example 1.4 and 1/sqrt(1/100)=10 (c009, c016), Lab 1 15 of 15 and 81 of 81 (c010; out/labs/lab-SC1-L01-1.stdout), Section 4 counterexample (c011 to c013, c017), Section 5 misconceptions (c015). All match.")
row("SC1e-L02-statements", "2.7 cards c018 to c041, c184, c185 against L02 text",
    S + "cards.json SC1-c018 to c041, c184, c185; L02.html sections 1 to 6, Lab 1", P,
    "L02 read in full (/tmp/sc1e_r4/L02_full.txt, escaped copy). Statements match: Lambda (c018, c021), Lemma 2.2 (c022 to c024), Lemma 2.1 (c025), Lemma 2.3 variance 2^-(n+2)+2^-(n+2)=2^-(n+1) (c027, c028), P(E_m^c)<=2^-m and M_m=sqrt(2 log 2) sqrt(m) 2^(-m/2) (c029, c030), c032 now carries the Omega* qualifier (round-3 FAIL fixed), Lab 1 216 = 2*9+3*8+5*7+9*6+17*5 with 36 pairs over 17 points (c037), levels 8 of 8 (c038), harmonic bound 1+k/2 (c039). Lab E3 recomputed: unrounded level-1 sup 0.11658934, doubled 0.2331787, rounds to 0.233179 as the page says. Hypothesis omissions are in SC1e-hypotheses-carried.")
row("SC1e-L03-statements", "2.7 cards c042 to c060, c186 to c188 against L03 text",
    S + "cards.json SC1-c042 to c060, c186, c187, c188; L03.html sections 1 to 6, Lab 1", P,
    "L03 read in full. Thm 2.3 bounds (c046 to c048), Prop 2.4(a),(b) (c049, c050), M_k and Lemma 2.2 (c044, c045), canon breaks (c053, c054), misconceptions (c056 to c058; c058 'Not settled' agrees with the page's no-pathwise-claim statement), R2 constant 2 (c059), Assumption 3.2 and 3.1 (c060, c188). Lab 1: max |z| 2.39 at H=1,N=2 and no other |z| above 1.84 (c051; out/labs/lab-SC1-L03-1.stdout). c187 gap table recomputed in out/l03_gap.out: largest gap +13.21% at H=2,N=1, smallest -6.6%, all |gap| < 14%.")
row("SC1e-L04-statements", "2.7 cards c061 to c082 against L04 text",
    S + "cards.json SC1-c061 to c082; L04.html sections 1 to 5, Lab 1", P,
    "L04 read in full. Def 1.2 (c065), Lemma 2.1 (c066), Props 2.2 to 2.4 (c067 to c071; E[B^4]=3t^2 in c068; E[Z_t^2]=e^(-th^2 t) E[e^(2 th B_t)]=e^(th^2 t) in c071), misconceptions (c073, c076 with E[B_t^3|F_s]=B_s^3+3(t-s)B_s re-derived, c077), Lab 1 values e^1, e^(1/4), e^4 and E[Z_t]=1 (c072; out/labs/lab-SC1-L04-1.stdout), R1 to R2 (c079, c080), P2 to P3 (c081, c082).")
row("SC1e-L05-statements", "2.7 cards c083 to c105, c189 against L05 text",
    S + "cards.json SC1-c083 to c105, c189; L05.html sections 1 to 6, Lab 1", P,
    "L05 read in full (escaped copy /tmp/sc1e_r4/L05_full.txt). Statements of Def 1.1, 1.2, A4(a) to (h) (c085 content), Lemma 1.3 (c086), Thm 1.4 (c087), Remark 1.5 (c088), Lemma 2.2 and Thm 2.1 (c089, c090), Lab 1 225 cases, gap 5.55e-16, 10^-11 digit bound (c091, c092; out/labs/lab-SC1-L05-1.stdout), A3 and R1 to R3 (c093 to c099), misconceptions (c100 to c102), M2 E[B_3^2|F_1]=B_1^2+2 (c103), P2 (c104), M3 (c105), F_rho (c189). Atomicity of c085 is a separate row. Rendering of the Thm 1.4 proof's last sentence is row SC1e-render-raw-lt.")
row("SC1e-L06-statements", "2.7 cards c106 to c133 against L06 text",
    S + "cards.json SC1-c106 to c133; L06.html sections 1 to 6, Lab 1", P,
    "L06 read in full (escaped copy /tmp/sc1e_r4/L06_full.txt, restores the text hidden by raw '<'). Lemma 1.2 (c108), Prop 1.3 (c109), Cor 1.4 (c110), Lab 1 Part A 1014 triples and Part B 78 pairs (c111, c112; out/indep_numbers.out), Part D 281/512, 11/32, 105/512 (c113), Part C 495 and 495 (c114), erfc(1/sqrt2)=0.3173105 (c115), Lemma 2.1 (i) to (iii) (c116 to c118), Def 2.2 and Prop 2.3 (c119 to c121), Remark 2.4 (c122), Thm 2.5 (c123), Cor 2.6 (c124), jump example (c125), misconceptions (c126 to c128), M1 (c129), R1 to R3 (c130 to c132), c133. Hidden text is row SC1e-render-raw-lt.")
row("SC1e-L07-statements", "2.7 cards c134 to c159, c191 against L07 text",
    S + "cards.json SC1-c134 to c159, c191; L07.html sections 1 to 6, Lab 1", P,
    "L07 read in full. Thm 1.3 (c137), Remark 1.4 (c138), Cor 1.5 (c139, c140) with int(1-Phi)=1/sqrt(2 pi) re-derived (c141), Prop 2.2 and Cor 2.3 (c143 to c145), Remark 2.4 (c146), Part A 21778 = 14893 + 6885 and 0.332306 (c148; out/indep_numbers.out), Part B counts 91, 107, 113, 121 and SE 0.0210, 0.0230 (c149), Part C 0.7586, SE 0.0317, gap 0.0393 = 1.2 SE (c150), M2, R1, R2, E3 SE sqrt(33759/63840000)=0.0230 (c155 to c159). Def 2.1 notation defect is row SC1e-L07-def21-notation. c191 duplicate of c126 is row SC1e-c126-c160-duplicate.")
row("SC1e-L08-statements", "2.7 cards c161 to c183, c192 against L08 text",
    S + "cards.json SC1-c161 to c176, c178 to c183, c192; L08.html sections 1 to 6, Lab 1", P,
    "L08 read in full (/tmp/sc1e_r4/L08_full.txt). Def 1.1 (c161), Prop 1.2 (c162), Cor 1.4 (c164), Cor 1.5 density a H^-3/2 e^(-a^2/2H)/sqrt(2 pi) (c165), Remark 1.6 (c166), Def 2.1 (c167), Props 2.2 and 2.3 (c168, c169), Part A 90114 sequences and 78 pairs and first-passage counts 512, 0, 384, 0, 288, 0, 224, 0, 180, 0 summing to 1588 (c170, c171; out/indep_numbers.out), Part B 5.480560, 11.815731, 24.557203 (c172), Part C z values (c173), Part D 0.317311, 0.479500, 0.241971, 0.109848 (c174), jump example (c175), c176, c178, M3 5/8 (c179), E1 (c180), R1 (c181), R2 (c182), R3 mode a^2/3 re-derived (c183). c192 wording problem is row SC1e-dup-tau-vs-max.")
row("SC1e-card-numbers-in-lesson", "2.7 every card number appears in its lesson or lab output",
    S + "cards.json (all 187 cards)", P,
    "ledgers/SC1/scripts/SC1-e-r4/card_numbers.py -> out/card_numbers.out: every decimal, fraction and exponent token on every card is found verbatim in its lesson (full text) or lab stdout, except notational variants (10^(-16) for 10^{-16}, 1/2 for \\tfrac12).")
row("SC1e-lab-numbers-vs-run", "Lab twins run and printed numbers equal the cards",
    "tests/labs/SC1/lab-SC1-L01-1.py to lab-SC1-L08-1.py; cards with a lab basis", P,
    "run_labs.py --unit SC1: 'run_labs SC1: PASS (11/11)' (out/run_labs.out). Each twin run as python -I -W error from a scratch directory, exit 0, empty stderr (out/labs/*.stderr, 0 bytes). Stdout in out/labs/*.stdout; card numbers equal these lines.")
row("SC1e-exact-numbers-recomputed", "2.7 exact and derived numbers re-derived by my own code",
    "cards c010, c037, c051, c052, c054, c057, c059, c091, c092, c111 to c114, c141, c147 to c150, c159, c165, c170 to c174, c183, c187", P,
    "ledgers/SC1/scripts/SC1-e-r4/indep_numbers.py -> out/indep_numbers.out (no lab code reused): 1014 triples, 78 pairs, 495 and 495, 281/512, 11/32, 105/512, 1588, [512,0,384,0,288,0,224,0,180,0], 5.480560, 11.815731, 24.557203, 21778 = 14893 + 6885, erfc(1/sqrt2)=0.3173105079, e^4, e^8=2980.957987, densities 0.241971 and 0.109848, Phi(-1/sqrt2)=0.23975006, 1/(2 sqrt pi). out/l03_gap.out recomputes the 16 SE gaps and z values of L03.")
row("SC1e-hypotheses-carried", "2.7 cards carry the hypotheses of the proposition they state",
    S + "cards.json SC1-c029, SC1-c032, SC1-c035; L02.html Prop 2.4 (H2), Remark 2.6 (H1)", F,
    "Card SC1-c029 uses Omega* in its question but its front defines only E_m; card SC1-c032 uses Omega* in its question and its front lists only H1 and Assumption 2.1. Proposition 2.4 (H2) defines E_m, A_{m0} and Omega* = union over m0 of A_{m0}, so neither card carries the event it names. Card SC1-c035 (Remark 2.6) omits (H1), that the copies B^(k) are built from their own coefficients and are mutually independent, which its answer relies on. The other cards checked (c007, c008, c025, c026, c046 to c048, c067, c068, c070, c137, c145, c162) carry their hypotheses.",
    "Add to the fronts of SC1-c029 and SC1-c032 the clause '(H2) A_{m0} = intersection of E_m over m >= m0 and Omega* = union of A_{m0}', and to SC1-c035 the clause '(H1) B^(k) are copies of Theorem 2.5 built from their own coefficients and mutually independent'. Edit cards.json only; no lesson change needed for this row.")
row("SC1e-grades-audit", "2.7 grade and basis of every graded card",
    S + "cards.json (all graded cards)", P,
    "141 graded cards: grade and basis paired on every card; T on proved statements; C only on lab-derived numeric cards (c010, c037, c038, c051, c072, c091, c092, c111 to c114, c127, c147 to c150, c170 to c173, c187), matching the lesson Key results grades (for example L05 'C Lab 1' row and L07 Part B/C rows). c127 (C, Lab 1 Part D) refutes a misconception by exact arithmetic and Corollary 1.4 (T); the grade is conservative and is not a fail.")
row("SC1e-cites-and-registry", "2.7 cite fields against references/references.json",
    S + "cards.json (cite fields); references/references.json", P,
    "cite is empty on all 187 cards, so no registry key is cited. Lesson References sections (L03, L04, L07, L08) name shreve2004stochastic without locator and attribute nothing to it; no card attributes content to a source.")
row("SC1e-learner-text-scan", "2.7 no process words in learner text",
    S + "cards.json front and back text", P,
    "Regex scan of front and back for round, verif, builder, TODO, draft, fragment, ledger, mutant, grader, we, I, our, fix, audit, reviewer: only ordinary words (fixed, fixes, rounding).")
row("SC1e-dag-and-concepts", "DAG: concepts used by cards and lessons are in the unit closure",
    S + "L01.html to L08.html 'Uses' lines; tools/check_dag.py --unit SC1", P,
    "check_dag SC1 PASS (out/check_dag.out). Cards use only concepts defined in the lessons; M4/M6 prerequisites are named in the Uses lines and in Assumptions.")
row("SC1e-notation-registry", "13. notation: symbols against notation/notation.json",
    S + "cards.json; notation/notation.json (registered: T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q)", P,
    "Phi is used only as the standard normal CDF (c104, c137, c139), matching the registry (M4). T appears only in L03 line 113 as the reserved program symbol, and H is used for the horizon. Local symbols F(H) (L08 Cor 1.5 proof, a CDF) and Q(P) (L03 quadratic variation, not the measure \\mathbb{Q}) are not registered and do not collide with a registered meaning; noted, not failed.")
row("SC1e-c126-c160-duplicate", "2.7 duplicates: misconception cards c126 (L06) and c191 (L07)",
    S + "cards.json SC1-c126 (L06 Section 4), SC1-c191 (L07 Section 4)", F,
    "c126 asks whether P(M_t>=a)=P(B_t>=a) (answer: no, Theorem 2.5 gives 2P(B_t>=a); at t=1, a=1 it is 0.3173 against 0.1587). c191 asks whether the running maximum has the same law as B_H (answer: P(M_H<=0)=0 against P(B_H<=0)=1/2, and P(M_H>=a)=2P(B_H>=a) for a>0). Both refute the same misconception with the same numbers and the same Theorem 1.3 / 2.5 identity.",
    "Keep one card. Either remove SC1-c191, or narrow it to the L07 point that P(M_H<=0)=0 while P(B_H<=0)=1/2, which c126 does not cover.")
row("SC1e-c116-c162-duplicate", "2.7 duplicates: c116 (L06 Lemma 2.1(i)) against c162 (L08 Prop 1.2)",
    S + "cards.json SC1-c116, SC1-c162", P,
    "c116 states {M_t>=a} = {tau_a<=t}; c162 states B at tau_a equals a on {tau_a<=H}. Different claims; both are needed.")
row("SC1e-c058-path-claim", "2.7 c058 (L03 misconception on a random quadratic variation)",
    S + "cards.json SC1-c058 (L03 Section 4)", P,
    "Back says 'Not settled' and that Theorem 2.3 says nothing about one path, which matches the page's statement that it makes no pathwise claim. The page also says the sums converge in mean square to the constant t; the card is correct as far as it goes.")
row("SC1e-c153-grade", "2.7 grade of c153 (L07 misconception on grid tails)",
    S + "cards.json SC1-c153 (L07 Section 4)", P,
    "c153 is graded T with basis 'Proposition 2.2(a), Corollary 2.3, Theorem 1.3', matching Key results rows for Prop 2.2 and Cor 2.3 (T).")
row("SC1e-c177-basis", "2.7 basis on the deleted card c177",
    S + "cards.json SC1-c177", P,
    "SC1-c177 is absent from cards.json, so there is no basis to check.")
row("SC1e-c030-typo", "2.7 formula on c030 (L02 Prop 2.4(b) step 2)",
    S + "cards.json SC1-c030", P,
    "M_m = lambda_m 2^(-(m+1)/2) = sqrt(2 log 2) sqrt(m) 2^(-m/2) re-derived; sum of m r^m = r/(1-r)^2 with r = 2^(-1/2) re-derived. Correct.")
row("SC1e-c035-remark-2.6", "2.7 card c035 against Remark 2.6 and its proof",
    S + "cards.json SC1-c035; L02.html Remark 2.6", P,
    "The back (glues independent copies, proves D1 to D3 and continuous paths) matches the Conclusion and proof. The hypothesis omission is in SC1e-hypotheses-carried; the proof's displayed formula is hidden by a raw '<' (SC1e-render-raw-lt).")
row("SC1e-c145-hypothesis", "2.7 hypothesis of c145 (L07 Cor 2.3)",
    S + "cards.json SC1-c145", P,
    "Front states H1 (continuous paths) and the grid event inclusion; matches Corollary 2.3's hypothesis H1 and proof.")
row("SC1e-c153-hypothesis", "2.7 hypothesis of c153 (L07 Section 4)",
    S + "cards.json SC1-c153", P,
    "Front states Prop 2.2(a), Corollary 2.3 and Theorem 1.3 (closed form under A3, A4); matches the lesson's misconception answer.")
row("SC1e-c176-hypothesis", "2.7 hypothesis of c176 (L08 Section 4)",
    S + "cards.json SC1-c176", P,
    "Front states Corollary 1.4 under A3 and A4 of Lesson 5; matches the lesson.")
row("SC1e-c126-c177-duplicate", "2.7 duplicate check for c126 against deleted c177",
    S + "cards.json SC1-c126; SC1-c177 absent", P,
    "c177 is absent, so no pair remains. The c126 vs c191 pair is row SC1e-c126-c160-duplicate.")
row("SC1e-c125-c175-jump-example", "2.7 duplicates: jump counterexample on c125 (L06) and c175 (L08)",
    S + "cards.json SC1-c125 (L06 Section 3), SC1-c175 (L08 Section 3)", F,
    "Both cards ask whether a path that jumps over the level a can break the identity between a maximum event and a first-passage event, and both answer with the same jump-over-a example (c125: jump from below a to above a; c175: 0 on [0,1/2), jump to 2, so M_1=2 but tau_1=infinity). Two cards test one counterexample.",
    "Keep c175 (it has the concrete example and the event that fails). Reword c125 so it asks only the Lemma 2.1 consequence for M_t, or delete it.")
row("SC1e-c155-c158-assumption-carried", "2.7 c155 (L07 M2) and the absent c158",
    S + "cards.json SC1-c155; SC1-c158 absent", P,
    "c155 matches M2 (depends on (a,H) only through a/sqrt(H), closed form 2(1-Phi(a/sqrt H))). c158 is absent.")
row("SC1e-c184-c187-new-cards", "2.7 newly appended cards c184 to c187",
    S + "cards.json SC1-c184, c185 (L02), SC1-c186, c187 (L03)", P,
    "c184 (dyadic time of depth n), c185 (Lemma 2.2(c)), c186 (dyadic partition of depth k), c187 (gap +13.2% at H=2, N=1) match their lessons and are recomputed.")
row("SC1e-c188-c189-new-cards", "2.7 newly appended cards c188 and c189",
    S + "cards.json SC1-c188 (L03 Assumption 3.1), SC1-c189 (L05 Section 3)", P,
    "c188 (|P_n| to 0) and c189 (F_rho is the events A with A cap {rho<=r} in F_r for all r) match the lessons.")
row("SC1e-c032-prop24b-scope", "2.7 round-3 FAIL: c032 drops the M >= m0 qualifier",
    S + "cards.json SC1-c032; L02.html Prop 2.4(b) steps 3 and 4", P,
    "Fixed since round 3. The back now reads 'On Omega*, S_M converges uniformly ... If the outcome lies in A_{m0}, sup|S - S_M| <= sum_{m>M} M_m for every M >= m0', matching Step 3 of the proof. The remaining Omega* hypothesis gap is in SC1e-hypotheses-carried.")
row("SC1e-dup-tau-vs-max", "2.7 duplicates and wording: c192 (L08 Cor 1.3) against c137 (L07 Thm 1.3)",
    S + "cards.json SC1-c192 (L08 Corollary 1.3), SC1-c137 (L07 Theorem 1.3)", F,
    "c192 asks which of the two equalities of Corollary 1.3 needs no probability assumption; its answer repeats the closed form 2(1-Phi)=erfc that c137 already tests. Also c192's back says 'P(tau_a<=H)=P(M_H>=a) holds on every path', which equates probabilities as if they were pathwise; the page's Proposition 1.2 is the pathwise event identity {tau_a<=H}={M_H>=a}. Round 3 flagged the same pair as c163/c137 and c190/c126; those ids were removed, and the same pattern returned under c192 and c191.",
    "Rewrite c192 back as: 'The event identity {tau_a<=H}={M_H>=a} holds on every continuous path with B_0=0 (Proposition 1.2), so the probabilities agree with no probability assumption; the closed form needs A3 and A4 (Theorem 1.3 of Lesson 7).' Drop the closed-form repetition, which c137 covers.")
row("SC1e-render-raw-lt", "Lesson markup: raw '<' inside math spans hides proof text in the browser",
    "course/modules/SC/SC1/L02.html line 310; L05.html line 121; L06.html lines 82, 83, 107, 114, 135, 168, 169, 369, 376, 470; L08.html line 137", F,
    "ledgers/SC1/scripts/SC1-e-r4/raw_lt.py -> out/raw_lt_math_spans.out lists every raw '<' inside \\( \\) that is followed by an ASCII letter. Each opens an HTML tag, so the browser swallows text up to the next '>'. Examples: L06 line 107 renders Lemma 2.1(iii) as 'On {tau_a>t}, B_t' with 'a.' swallowed; L05 line 121 loses the last sentence of the Theorem 1.4 proof ('this gives the Markov property ... for all 0<=s<=t'); L02 line 310 loses the displayed formula W_t=sum_{j<k}... of Remark 2.6's proof; L06 line 470 truncates a quiz option. Extracted text (ledgers/SC1/scripts/SC1-e-r4/lesson_text.py on the raw files) shows the same truncation. check_pages and page_smoke (below) do not catch it.",
    "In those spans replace '<' with '&lt;' (or write \\lt in the TeX source if the build supports it), then rebuild the SC1 pages. Add a check_pages rule that fails on '<' followed by a letter inside math.")
row("SC1e-c085-atomicity", "2.7 atomicity of c085 (A4 parts (a) to (h))",
    S + "cards.json SC1-c085; L05.html Assumption A4", F,
    "The back of c085 lists eight distinct facts, (a) to (h), in one answer. Each card must be atomic (2.7). Each part is correct against the lesson, so this is a structure fail, not a content fail.",
    "Split into cards per part (or keep one card for a single part such as A4(a) extension of independence, or A4(h) measurability at a stopping time) and remove the eight-part card.")
row("SC1e-semantic-duplicates", "2.7 semantic duplicates across the deck",
    S + "cards.json SC1-c028 and c036; SC1-c125 and c175; SC1-c126 and c191; SC1-c137 and c192", F,
    "Four pairs ask the same question with the same answer: c028 and c036 (zero covariance plus joint normality gives independence in Lemma 2.3's induction step, via A1(b) and A1(c)); c125 and c175 (the jump counterexample); c126 and c191 (running maximum tail or law versus B); c137 and c192 (the closed form 2(1-Phi(a/sqrt H)) = erfc under A3, A4). Rule 2.7 and the no-duplicates rule apply.",
    "Merge c028 and c036 into one card (keep the research-problem wording if it is the more useful one). Apply the fixes in SC1e-c125-c175-jump-example, SC1e-c126-c160-duplicate and SC1e-dup-tau-vs-max.")
row("SC1e-L07-def21-notation", "Lesson notation: Definition 2.1 of L07 uses an undefined index",
    S + "L07.html Definition 2.1 (raw line 116)", F,
    "The text reads 'M^(N)_H = max_{0<=k<=N} B_{H_k}', but the same sentence defines the grid times as s_k = kH/N. H_k is undefined and the index should be s_k (card SC1-c142 correctly uses s_k).",
    "Change B_{H_k} to B_{s_k} in the Definition 2.1 source, then rebuild; no other text changes.")
row("SC1e-page-smoke-L05-L06", "page_smoke on the pages where cards carry proof text",
    S + "L05.html, L06.html (page_smoke --pages L05 L06 --skip-sweep)", P,
    "page_smoke SC1: PASS (out/page_smoke_L05_L06.out, both pages PASS, labs run). Note: this check passed while the raw '<' defect hides text, so it does not detect SC1e-render-raw-lt.")

frag = {
    "unit": "SC1",
    "slice": "e",
    "round": 4,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e (all 187 cards of course/modules/SC/SC1/cards.json against lessons L01 to L08); round 4; did not build SC1",
    "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
    "base": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b (round-3 pin; round-3 fragment /Users/billyribeiro/.fanout/frags/E-SC1-e.round3.json). Delta: cards.json changed (c158, c160, c163, c177, c190 absent; c188, c189, c191, c192 present; wording changed); L01 to L08 changed. No round-3 PASS row is carried: every subject changed, so every row was re-verified from scratch.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-SC1-e (detached at 9a02b1a, .venv symlinked, vendor copied)",
    "scratch": "/tmp/sc1e_r4 (lesson_text L01.txt to L08.txt; L02_full, L05_full, L06_full, L08_full = escaped '<' copies; cards_dump.txt). Repo copies of every output: ledgers/SC1/scripts/SC1-e-r4/out/",
    "verified_at": "2026-11-04T12:30:00Z",
    "verdict": "FAIL",
    "scope_note": "Slice e = all 187 cards of course/modules/SC/SC1/cards.json at 9a02b1a (SC1-c001 to c192 with c158, c160, c163, c177, c190 absent), checked against L01 to L08 full text.",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: not applicable to a cards slice (no grader). The list is empty by design.",
        "Lesson-side, not a card row: L08 Corollary 1.5 proof writes F'(H)=2 phi(a H^(-1/2)) (a/2) H^(-3/2) without showing the two minus signs from d/dH[1-Phi]; the displayed value a H^(-3/2) phi is correct.",
        "Lesson-side, not a card row: L06 Lab 1 Part E and the M1 solution agree (2(1-Phi(1))=0.3173105079; 0.1586552539 is half of the printed 2-tail after rounding).",
        "Misconception restatements kept (not FAIL): c123 and c126 (L06), c145 and c153 (L07), c100 and c101 (L05) restate a theorem as a misconception with a different wrong belief each.",
        "Lab 1 Part B of L03 and the grid-tail numbers of L07 are seeded single-sample quantities; the cards say so (c051, c149, c150, c173, c187).",
        "Ordering (not a rule): appended cards c184 to c192 sit outside lesson order; ids remain unique and check_pages passes.",
        "Cross-unit reference not checked: L04 Section 3 cites 'Lesson 8 of M6' for the optional stopping theorem; the M6 text is outside this slice.",
    ],
    "summary": "SC1-e round 4: all 187 cards read against full L01 to L08 text. 41 rows: 33 PASS, 8 FAIL. FAIL: SC1e-hypotheses-carried (c029, c032 use Omega* without its definition; c035 omits H1), SC1e-c126-c160-duplicate (c191 duplicates c126), SC1e-c125-c175-jump-example (duplicate jump counterexample), SC1e-dup-tau-vs-max (c192 duplicates c137 closed form and states a probability identity 'on every path'), SC1e-render-raw-lt (raw '<' inside math in L02 l.310, L05 l.121, L06 ten lines, L08 l.137 hides proof and statement text in the browser; check_pages and page_smoke pass), SC1e-c085-atomicity (eight facts on one card), SC1e-semantic-duplicates (four pairs), SC1e-L07-def21-notation (B_{H_k} undefined index in Definition 2.1). Every card number, lab output and exact derived value was recomputed; all 11 lab twins pass under python -I -W error.",
}
json.dump(frag, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), "FAIL", sum(1 for r in rows if r["status"] == F), "PASS", sum(1 for r in rows if r["status"] == P))
