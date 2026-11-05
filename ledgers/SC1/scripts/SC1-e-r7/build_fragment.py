"""Builds ledgers/SC1/SC1-e.json (round 7). Every row cites a script under ledgers/SC1/scripts/SC1-e-r7/ or a command output."""
import datetime
import json
import sys

S = "ledgers/SC1/scripts/SC1-e-r7"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-e.round6.json", encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]

P = "PASS"
F = "FAIL"
rows = {}


def row(rid, check, location, status, evidence, fix=""):
    rows[rid] = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        rows[rid]["fix"] = fix


row("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json", P,
    f"{S}/out/cards_dump.txt (dump_cards.py): 194 cards, 194 distinct ids; per lesson L01 18, L02 25, L03 21, L04 25, "
    "L05 31, L06 27, L07 25, L08 22; cite is [] on every card; all 194 cards read in this round (cards_dump.txt lines 3 to 195).")
row("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all 18721 pairs)", P,
    f"{S}/dup_scan_r7.py -> {S}/out/dup_scan_r7.out: no identical front or back; 6 pairs at joined-text ratio >= 0.6: "
    "c064/c202 (A4.2(a) vs A4.2(b)), c117/c118 (inclusion vs sample path), c161/c167 (tau_a vs nu_a), c196/c198 (A4(d) vs A4(f)), "
    "c067/c068 (Prop 2.2 vs 2.3), c081/c082 (E[Z_t] vs E[Z_s Z_t]); each pair states a different claim.")
row("SC1e-learner-text-scan", "2.9-prose", "cards front and back; L01 to L08 text", P,
    f"grep -i over {S}/out/L0{{1..8}}.txt and {S}/out/cards_dump.txt for verif*, builder, fixer, ledger, mutant, grader, "
    "TODO, lorem, draft, fragment, round N, we/our/I: only mathematical uses ('we have', 'verify the limit'), a nav label "
    "'Reflection Principle Verified' (project title) and 'verify' as a learner instruction.")
row("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a number token", P,
    f"{S}/card_numbers_r7.py -> {S}/out/card_numbers_r7.out: 321 distinct number tokens over the cards; 317 appear verbatim in "
    "the card's own lesson text or its lab stdout; the 4 others are the same value in another form (SC1-c138, c156, c191: "
    "'1/2' written as \\tfrac12 in L07; SC1-c171: '794/4096' printed as '794 / 4096' in L08 Lab 1 Part A).")
row("SC1e-lab-numbers-vs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to L08-1.py", P,
    f"run_labs.py --unit SC1: 'run_labs SC1: PASS (11/11)' ({S}/out/run_labs.out). Each lesson twin run as "
    f"python -I -W error: exit 0, stderr 0 bytes ({S}/out/labs/*.stdout, *.stderr). Lab-derived card numbers re-derived in "
    f"SC1e-exact-numbers-recomputed and checked against lab stdout: c010 81 of 81, c037 216 of 216, c038 8 of 8, c051 |z|=2.39, "
    "c072 54.598150033 and 1.000000000, c091 225 and 5.55e-16, c111 1014, c112 78, c113 281/512 11/32 105/512, c114 495, "
    "c148 0.332306, c149 0.2275/0.3025 and 0 violations, c150 0.7586 and 0.0393, c170 90114, c171 counts, c172 5.480560 11.815731 "
    "24.557203, c173 z values, c174 0.317311 0.241971 0.479500 0.109848, c187 gap.")
row("SC1e-exact-numbers-recomputed", "2.2-numbers", "cards c010, c027, c030, c039, c052, c057, c059, c111 to c114, c129, c140, c141, c148 to c150, c159, c165, c170 to c174, c179 to c183, c187, c201", P,
    f"{S}/indep_numbers_r7.py -> {S}/out/indep_numbers_r7.out (no lab code imported): L06 triples 1014 of 1014, pairs 78 of 78, "
    "N=12 a=3 M>=3 & S=2: 495 and S=4: 495, N=10 a=2: 281/512, 11/32, 105/512; L07 tails N=4,16,64,256,1024: 0.375000, 0.332306, "
    "0.321084, 0.318255, 0.317547; 21778 = 14893 + 6885, 21778/65536 = 0.332306; L08 first-passage counts at steps 3..11 odd: "
    "512, 384, 288, 224, 180 (sum 1588), P(nu_3<=12)=397/1024=0.387695, #{S_12>=3}=794; pairs n*2^n sum 90114; "
    "E[min(nu_1,16)]=179587/32768=5.480560, N=64 11.815731, N=256 24.557203; 2(1-Phi(1))=0.31731050786; f_1(1)=0.241971, "
    "f_1(2)=0.109848; erfc(1/2)=0.479500; 1-Phi(1)=0.15865525393; sqrt(2/pi)=0.797885; c187 gap at H=2,N=1 = +13.21%; "
    "c159 SE 0.0230; c057 identity; c150 gap 1.24 SE; c091 ratio 2.5 eps. c111 (1014) also re-derived as sum_N (N^2+N(N+1)/2).")
row("SC1e-L03-gap", "2.5-labs", "card c187; tests/labs/SC1/lab-SC1-L03-1.py", P,
    f"lab stdout {S}/out/labs/lab-SC1-L03-1.stdout (16 SEs) and indep_numbers_r7.py: largest signed gap +13.21% at H=2,N=1; "
    "smallest -6.60% at H=2,N=2; all 16 gaps within 14%, as c187 says.")
row("SC1e-L01-statements", "2.9-prose", "course/modules/SC/SC1/L01.html; cards c001 to c017, c186", P,
    "Changed hunks of L01 read in full (delta_since_round6.diff lines 2-79): Var(B_t)=t now from (D1) and (D2) with s=0 (matches c005); "
    "Remark 1.3 renamed and matches c008; Lab 1 hypothesis text (dyadic depth n, 15 of 15, 81 of 81) matches lab stdout; "
    "section 4 bullets match c011 to c013 and c017; Q1 explanation matches c015. Cards c001 to c004, c006, c007, c009, c014, c016, c186 re-read against the lesson.")
row("SC1e-L02-statements", "2.9-prose", "course/modules/SC/SC1/L02.html; cards c018 to c041, c184, c185", P,
    "L02 changed only in escaping (line 310) and the Lab 1 docstring is unchanged this round; all 25 cards re-read. c027 to c028 algebra "
    "recomputed (1/4*2^-n + 2^-(n+2) = 2^-(n+1)); c030 M_m = sqrt(2 log2) sqrt(m) 2^(-m/2) recomputed; c040 matches L02 Section 5 line "
    "('any other scale c gives increments of the wrong variance'); c032, c034, c035 hypotheses match the Prop 2.4, Thm 2.5, Remark 2.6 statements.")
row("SC1e-L03-statements", "2.7-cards", "course/modules/SC/SC1/L03.html; cards c042 to c060, c187, c188", F,
    "Cards c042 to c060 re-derived and read against L03 (Lemma 2.1/2.2, Thm 2.3, Prop 2.4, Section 3 "
    "and Problems); all match except card SC1-c048 (row SC1e-c048-hypothesis-mismatch). The L03 Q5 quiz change and the R3 solution "
    "change (delta lines 94-122) match the lesson and card c054.",
    "Fix row SC1e-c048-hypothesis-mismatch (card SC1-c048 front).")
row("SC1e-L04-statements", "2.9-prose", "course/modules/SC/SC1/L04.html; cards c061 to c082, c202 to c204", P,
    "R1 solution changed h->k (delta lines 123-134): k(t)=t-g(t), constant k forced by condition (iii), g(t)=t+c; matches c079. "
    "c066 to c082 re-read: c070/c071 E[Z_t^2]=e^(theta^2 t) and c077 E[e^(theta B_t)]=e^(theta^2 t/2) recomputed; c076 "
    "E[X_t|F_s]=B_s^3+3(t-s)B_s recomputed; c073, c080 checked; c072 numbers match lab stdout.")
row("SC1e-L05-statements", "2.9-prose", "course/modules/SC/SC1/L05.html; cards c083 to c105, c189, c193 to c200", P,
    "Changed hunks (delta lines 135-203) read: why-it-matters now names A4(a),(b),(f) (matches c086, c087); M6 stopping-time link "
    "(M6 L09 Definition 9.1 exists; SC1 prereqs include M6, curriculum.json); P2 names Phi (matches c104); R1 renamed eta* and "
    "matches c097 (paths verified: argmax 1/4 and 3/4); R2 solution matches c095; references paragraph matches registry (shreve2004stochastic present, count 1). "
    "A3 (rho<=c) matches c093 and c099; A4(a) to (h) statements match c193 to c200.")
row("SC1e-L06-statements", "2.9-prose", "course/modules/SC/SC1/L06.html; cards c106 to c124, c126 to c133", P,
    "Changed hunks (delta lines 204-306): Lemma 2.1 and P2 escapes only; Definition 2.2 now says A3 covers bounded stopping times and "
    "matches c119 (updated card); Proposition 2.3 and Theorem 2.5 hypotheses match c120, c121, c123, c133; misconception text matches c126 to c128 "
    "(c128 updated). Numbers: 1014, 78, 281/512, 11/32, 105/512, 495 recomputed (indep_numbers_r7.py). Lab stdout lines verbatim in page (see SC1e-r7-lab-stdout-verbatim).")
row("SC1e-L07-statements", "2.9-prose", "course/modules/SC/SC1/L07.html; cards c134 to c159, c191", P,
    "Changed hunks (delta lines 307-376) read: Theorem 1.3 has H1, H2 (A3/A4), H3 (H>0, a>0) and the cards c137, c139, c140 state these; "
    "Remark 1.4 renamed and matches c138; Corollary 1.5 (a),(b) hypotheses H1 to H3 and A5 match c139, c140; Definition 2.1 matches c142; "
    "c143 to c146, c153, c155 to c157 checked; c145 and c153 hypotheses match Prop 2.2 and Cor 2.3; interpretation paragraph numbers "
    "(Part A 0.375000 ... 0.317547, Part B 91,107,113,121 counts, Part C 0.0393 = 1.2 SE) match lab stdout; c141 1/sqrt(2pi) and c140 sqrt(2H/pi) recomputed.")
row("SC1e-L08-statements", "2.9-prose", "course/modules/SC/SC1/L08.html; cards c161 to c183, c201", P,
    "Changed hunks (delta lines 377-434) read: Corollary 1.3 adds Phi definition (matches c201, c137); Proposition 1.2 proof and "
    "statement match the new c162 (B at tau_a equals a); Corollary 1.4 and 1.5 match c164, c165 and the density recomputed; Remark 1.6 "
    "matches c166; Part D and quiz values match lab stdout (0.317311, 0.241971, 0.479500, 0.109848); c183 maximum at a^2/3 recomputed; "
    "c179 to c182 recomputed (5/8, 1588, 2 x 794).")
row("SC1e-hypotheses-carried", "2.9-prose", "cards c029, c032, c035, c006, c008, c040, c145, c153, c162", P,
    "Each card's hypotheses compared with its lesson statement at this pin: c029 (Prop 2.4(a)), c032 (Prop 2.4(b)), c035 (Remark 2.6), "
    "c006 (Gaussian process), c008 (Remark 1.3), c040 (Section 5), c145 (Cor 2.3), c153 (Prop 2.2(a), Cor 2.3), c162 (Prop 1.2) all match.")
row("SC1e-grades-audit", "2.3-grades", "cards with grade and basis", P,
    f"{S}/out/cards_dump.txt: every T card cites a proof, Problem or Section; every C card (21 cards: c010, c037, c038, c051, c072, c091, c092, "
    "c111 to c114, c127, c148 to c150, c170 to c174, c187) names a lab or numerical check; ungraded cards (e.g. c119, c166, c102) are definitions, remarks or assumptions. "
    "c174 C names the closed-form numerical evaluation; c027 and c052 T cite Lemma 2.3 and Problem R1.")
row("SC1e-cites-and-registry", "2.1-citations", "cards (cite field); lesson References sections", P,
    "cite is [] on all 194 cards. Offline registry check: `.venv/bin/python tools/verify_refs.py --offline` -> "
    "'offline integrity: 560 entries, 0 problems' (verify_refs_offline.out). shreve2004stochastic present in references/references.json "
    "(count 1); L05 and L06 References paragraphs claim no passage from it.")
row("SC1e-dag-and-concepts", "2.9-prose", "course/modules/SC/SC1/L0[1-8].html; cards", P,
    "check_dag.py --all: SC1 PASS (check_dag.out). The only cross-unit use is M6 stopping time (M6 L09 Definition 9.1, data-concept stopping-time), "
    "and M6 is in SC1 prereqs (curriculum.json: prereqs ['M6']).")
row("SC1e-notation-registry", "2.4-notation", "notation/notation.json; course/modules/SC/SC1/L03.html, L07.html; cards", P,
    f"{S}/notation_scan.py -> {S}/out/notation_scan.out. T used only as the grade letter (L03 and L07 state that T is reserved for the number of observations); "
    "Phi used only as the standard normal CDF (registered meaning); no R^*, gamma_3/4, R_f, Q used. U, eta, eta*, tau, nu, kappa, varphi are not "
    "registered, so no collision with a registered symbol.")
row("SC1e-c126-c160-duplicate", "2.7-cards", "cards c126, c191 (c160 absent)", P,
    "c160 absent. c126 (misconception on the running maximum tail) and c191 (P(M_H<=0) vs P(B_H<=0)) state different claims.")
row("SC1e-c116-c162-duplicate", "2.7-cards", "cards c116 (L06 Lemma 2.1(i)) and c162 (L08 Proposition 1.2)", P,
    "Carried from round 6 status FAIL, now re-verified PASS: card c162 was reworded at this pin (delta, cards.json line 1378 onward) "
    "and now asks the value of B at tau_a on {tau_a<=H} (B_(tau_a)=a), which is not the equality {M_t>=a}={tau_a<=t} of c116. "
    "The two cards have different claims.")
row("SC1e-c058-path-claim", "2.7-cards", "card c058; course/modules/SC/SC1/L03.html Section 4", P,
    "Card c058 says Theorem 2.3 is a mean-square statement with no pathwise claim; L03 Section 4 (line ~171) states the same. Re-read at this pin.")
row("SC1e-c153-grade", "2.3-grades", "card c153; course/modules/SC/SC1/L07.html Section 4", P,
    "Card c153 grade T; the lesson's Section 4 proves the inequality (Prop 2.2(a) and Cor 2.3) and cites the closed form under H2. Re-read at this pin.")
row("SC1e-c177-basis", "2.7-cards", "card c177 (absent)", P,
    "c177 absent from cards.json (ids c176 then c178).")
row("SC1e-c030-typo", "2.2-numbers", "card c030; course/modules/SC/SC1/L02.html Prop 2.4(b) step 2", P,
    "M_m=lambda_m 2^(-(m+1)/2)=sqrt(2 log 2) sqrt(m) 2^(-m/2) recomputed; r=2^(-1/2), sum m r^m = r/(1-r)^2 finite. Matches lesson step 2.")
row("SC1e-c035-remark-2.6", "2.9-prose", "card c035; course/modules/SC/SC1/L02.html Remark 2.6", P,
    "Card hypotheses (H1 copies, assuming A1(a), A1(b), A1(e), A2, Assumption 2.1) match L02 Remark 2.6 H1 and H2 (grep at this pin).")
row("SC1e-c145-hypothesis", "2.9-prose", "card c145; course/modules/SC/SC1/L07.html Corollary 2.3", P,
    "Card: under H1 (continuous paths); lesson Corollary 2.3 is 'Under H1 of Proposition 2.2' with H1 = continuous path on [0,H]. Match.")
row("SC1e-c153-hypothesis", "2.9-prose", "card c153; course/modules/SC/SC1/L07.html Section 4", P,
    "Card hypotheses (Prop 2.2(a), Cor 2.3, Thm 1.3 under A3 and A4) match L07 Section 4 text.")
row("SC1e-c176-hypothesis", "2.9-prose", "card c176; course/modules/SC/SC1/L08.html Corollary 1.4", P,
    "Card: assuming A3 and A4, P(tau_a<inf)=1; lesson Corollary 1.4 is 'Assuming A3 and A4 ..., Prob(tau_a<inf)=1'. Match.")
row("SC1e-c126-c177-duplicate", "2.7-cards", "cards c126 and c177 (absent)", P,
    "c177 absent; no duplicate.")
row("SC1e-c125-c175-jump-example", "2.9-prose", "card c175; course/modules/SC/SC1/L08.html Section 3", P,
    "c175 (path 0 on [0,1/2), jumps to 2, M_1=2, never equals 1, tau_1=inf) matches L08 Section 3 example; c125 absent.")
row("SC1e-c155-c158-assumption-carried", "2.9-prose", "card c155; course/modules/SC/SC1/L07.html Problem M2 (c158 absent)", P,
    "c155 states the Problem M2 result under A3 and A4; c158 absent; the lesson problem carries the same assumption.")
row("SC1e-c184-c187-new-cards", "2.7-cards", "cards c184, c185 (L02), c186 (L01), c187 (L03)", P,
    "c184 matches L02 line 32 (dyadic time); c185 matches Lemma 2.2(c); c186 matches L01 dyadic partition in Lab 1 text; c187 gap recomputed (see SC1e-L03-gap).")
row("SC1e-c188-c189-new-cards", "2.7-cards", "cards c188 (L03 Assumption 3.1), c189 (L05 Section 3)", P,
    "c188 matches L03 Assumption 3.1 (|P_n| -> 0); c189 matches L05 Section 3 definition of F_rho.")
row("SC1e-c032-prop24b-scope", "2.9-prose", "card c032; course/modules/SC/SC1/L02.html Proposition 2.4(b)", P,
    "Card c032: on Omega*, Sigma_M converges uniformly, Sigma continuous, and the tail bound sup|Sigma-Sigma_M| <= sum_{m>M} M_m on A_{m0}, M>=m0; "
    "matches the lesson's conclusion and steps 3 and 4.")
row("SC1e-c085-atomicity", "2.7-cards", "card c085 (absent); cards c193 to c200", P,
    "c085 absent; c193 to c200 are single-assumption cards matching L05 A4(a) to (h) (see SC1e-A4-assumption-cards).")
row("SC1e-c028-c036-duplicate", "2.7-cards", "card c028; card c036 (absent)", P,
    "c036 absent; c028 (uncorrelated jointly normal implies independent) is not duplicated.")
row("SC1e-c055-c058-overlap", "2.7-cards", "cards c055, c058", P,
    "Overlap in subject only: c055 asks whether an almost-sure limit is established (no); c058 asks about a path's quadratic variation. Different questions.")
row("SC1e-c151-c154-overlap", "2.7-cards", "cards c151, c154", P,
    "Both concern B-tilde and the tail formula; c151 asks whether the tail formula applies to B-tilde, c154 asks whether one-time laws determine the tail. Different questions.")
row("SC1e-c009-c016-overlap", "2.7-cards", "cards c009, c016", P,
    "Both concern the sd of increments of length h; c009 is Example 1.4 (sd sqrt(h)), c016 is the misconception 'order h'. Different questions; no duplicate.")
row("SC1e-c129-c179-overlap", "2.7-cards", "cards c129 (L06), c179 (L08)", P,
    "c129: 5 of 8 walks with M_3>=1 (L06); c179: P(nu_1<=3)=5/8 (L08). Different events (maximum vs first passage), same count 5 for the walk of 3 steps; not duplicates.")
row("SC1e-c164-c176-overlap", "2.7-cards", "cards c164, c176", P,
    "c164 states P(tau_a<inf)=1; c176 states the misconception that tau_a is finite on every path. Different questions.")
row("SC1e-A4-assumption-cards", "2.7-cards", "cards c193 to c200 (L05 A4(a) to (h)); c064, c202 to c204 (L04 Assumption 4.2)", P,
    "L05 Assumption A4 (a) to (h) read at this pin (L05.html lines 24-31): card c193 (a) pi-lambda; c194 (b) freezing; c195 (c) hitting times; "
    "c196 (d) path determination; c197 (e) Gaussian integral; c198 (f) grouping; c199 (g) joint measurability; c200 (h) measurability at a stopping time. "
    "Each card matches. L04 Assumption 4.2 (a) to (d) cards c064, c202, c203, c204 match the L04 assumption list.")
row("SC1e-c201-locator", "2.7-cards", "card c201; L07 Lab 1 Part D; L08 Lab 1 Part D", P,
    "c201: P(tau_1<=1)=0.317311 (L08 Part D stdout) and P(B_1>=1)=0.1586552539 (L07 Part D stdout, and indep_numbers_r7.py 0.15865525393).")
row("SC1e-L07-def21-notation", "2.9-prose", "course/modules/SC/SC1/L07.html Definition 2.1; card c142", P,
    "Definition 2.1 (L07.html line 51-53): s_k = kH/N, M^(N)_H = max_{0<=k<=N} B_{s_k}; card c142 matches.")
row("SC1e-page-smoke-L05-L06", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html", P,
    f"page_smoke.py --unit SC1 (run alone at pin 06994db): every SC1 page PASS including L01 to L08 with Pyodide labs "
    f"(page_smoke_SC1.out). Zero console errors, zero unrendered math, labs 0.0 to 1.3 s each.")
row("SC1e-gates-check-pages-dag", "2.9-prose", "course/modules/SC/SC1/", P,
    "check_pages.py --all: SC1 PASS (check_pages.out, exit 0). check_dag.py --all: SC1 PASS (check_dag.out, exit 0).")
row("SC1e-render-raw-lt", "2.9-prose", "course/modules/SC/SC1/L01.html line 115; L04.html line 241; L05.html line 403; L06.html lines 83, 114, 415, 417", P,
    f"Carried from round 6 status FAIL, now re-verified PASS. {S}/tag_names.py (html.parser start-tag names) reports 0 unexpected tags on "
    f"L01 to L08 (round-6 pin: 1 unexpected tag '<t_1' at L01 line 115). Literal '<' followed by a non-letter remains in 8 math spans "
    f"(raw_lt_check.py), which is text, not a tag; page_smoke (zero unrendered math) passes.")
row("SC1e-c116-c192-event-identity", "2.7-cards", "cards c116 (L06), c192 (absent), c162 (L08)", P,
    "c192 absent; c116 and reworded c162 state different claims (see SC1e-c116-c162-duplicate).")
row("SC1e-dup-tau-vs-max", "2.7-cards", "cards c192 (removed), c137, c201", P,
    "c192 absent; c137 (Thm 1.3 closed form) and c201 (P(tau_1<=1) vs P(B_1>=1)) state different claims.")
row("SC1e-semantic-duplicates", "2.7-cards", "cards c112 (L06), c147 (absent)", P,
    "c147 absent; c112 (78 pairs) is not duplicated by another card.")
row("SC1e-L01-U-existence", "2.4-mathematics", "course/modules/SC/SC1/L01.html Section 4, first item (line ~215); cards c011 to c013", P,
    "Carried from round 6 status FAIL, now re-verified PASS. The page now builds the product space (Omega x (0,1), F x Bor, P x Leb), "
    "extends B by B_t(omega,u)=B_t(omega), sets U(omega,u)=u. Checked: U uniform; sigma(B) events are A x (0,1); "
    "P((A x (0,1)) cap (Omega x C)) = P(A) Leb(C), so U is independent of B; extended B still has continuous paths. "
    "Then B-tilde = B + 1{t=U} satisfies (D1) to (D3), B-tilde_U = B_U + 1, discontinuous on every outcome.")
row("SC1e-L07-quiz-digits", "2.2-numbers", "course/modules/SC/SC1/L07.html quiz items and explanations", P,
    "Carried from round 6 status FAIL, now re-verified PASS. Quiz answer 0.3173105 with tolerance 1e-6 (unrounded 0.31731050786): "
    "the explanation now states 0.3173105 to seven decimals. Check: |0.3173105 - 0.31731050786| = 7.9e-9 < 1e-6.")
row("SC1e-L08-quiz-digits", "2.2-numbers", "course/modules/SC/SC1/L08.html quiz items 'P(tau_1<=1) to seven decimals' and density at H=1", P,
    "Carried from round 6 status FAIL, now re-verified PASS. Quiz 'P(tau_1<=1) to seven decimals' answer 0.3173105 tolerance 1e-6 (exact "
    "0.31731050786); density at H=1 answer 0.241971 tolerance 1e-6 (exact 0.24197072): |diff| 2.8e-7. Quiz E[min(nu_1,16)] 5.48056, tol 1e-5, exact 5.4805603.")
# Round-7 additions
row("SC1e-c048-hypothesis-mismatch", "2.7-cards", "course/modules/SC/SC1/cards.json line 397 (card SC1-c048 front); course/modules/SC/SC1/L03.html line 99-104 (Theorem 2.3)", F,
    "Card SC1-c048 front lists 'Hypotheses: (H1) ...; (H2) Assumption 3.2; and Assumption 3.1'. The lesson's Theorem 2.3 has only (H1) and (H2) "
    "as hypotheses, and its conclusion adds Assumption 3.1 ('Assuming also Assumption 3.1, for every sequence ... the right-hand side tends to zero'). "
    "The L03 quiz explanation (line ~443) also says Assumption 3.1 is 'added in the conclusion'. The card misclassifies a conclusion premise as a hypothesis.",
    "In cards.json SC1-c048 front, delete '; and Assumption 3.1' from the Hypotheses list and make the question read: 'Theorem 2.3, limit. Hypotheses: (H1) ...; (H2) Assumption 3.2. Assuming also Assumption 3.1, for a sequence (P_n) of partitions of [0,t], what is the limit of Q(P_n)?' Then regenerate nothing else (cards.json is not generated).")
row("SC1e-r7-L01-product-space", "2.4-mathematics", "course/modules/SC/SC1/L01.html Section 4 (line ~215)", P,
    "Same as SC1e-L01-U-existence; the product-space construction was re-derived by hand (independence and measurability of sigma(B) events) at this pin.")
row("SC1e-r7-lab-stdout-verbatim", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html", P,
    "All 128 stdout lines of the eight lab twins (run under python -I -W error) appear verbatim in their own lesson HTML (html.unescape, whitespace-normalized); 0 missing.")
row("SC1e-r7-lab-code-equals-twin", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html data-run block; tests/labs/SC1/lab-SC1-L0n-1.py", P,
    "The data-run code block of each lesson page equals its twin file line for line (8 of 8 identical; 65, 95, 84, 69, 84, 93, 202, 201 lines).")
row("SC1e-r7-quiz-numeric-tolerances", "2.2-numbers", "course/modules/SC/SC1/L07.html, L08.html quiz data-answer attributes", P,
    "Every quiz numeric answer changed this round (L07 0.3173105, L08 0.3173105, 0.241971, 5.48056) lies within its tolerance of the recomputed exact value (indep_numbers_r7.py).")
row("SC1e-r7-L04-R1-solution", "2.4-mathematics", "course/modules/SC/SC1/L04.html R1 solution (line ~131)", P,
    "B_t^2-g(t) = (B_t^2-t)+k(t), k(t)=t-g(t) deterministic; martingale iff k(t)=k(s) for all s<=t, so k constant; g(t)=t+c. Derivation checked.")
row("SC1e-r7-L06-definition-2.2", "2.4-mathematics", "course/modules/SC/SC1/L06.html Definition 2.2; card SC1-c119", P,
    "Definition 2.2 now says A3 covers bounded stopping times only and tau_a is not shown bounded; A3 (L05) requires rho<=c (L05.html Assumption A3). Card c119 updated to match.")
row("SC1e-r7-delta-hunks-read", "2.9-prose", "delta_since_round6.diff (all 499 lines, all 11 hunk files)", P,
    f"{S}/out/delta_since_round6.diff: every hunk read in this round (L01 to L08 text and cards.json changes). No hunk left unread; changed-subject rows above are re-verified.")

ids = list(rows.keys())
missing = [i for i in prev_ids if i not in rows]
extra = [i for i in ids if i not in prev_ids and not i.startswith("SC1e-r7") and i != "SC1e-c048-hypothesis-mismatch"]
print("prev ids:", len(prev_ids), "missing from round 7:", missing, "extra non-r7 ids:", extra)
assert not missing, missing
rows_out = [rows[i] for i in prev_ids] + [rows[i] for i in ids if i not in prev_ids]
fails = [r["id"] for r in rows_out if r["status"] != P]
frag = {
    "unit": "SC1",
    "slice": "e",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e: all 194 cards of course/modules/SC/SC1/cards.json against lessons L01 to L08; round 7",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-SC1-e",
    "scratch": f"{S}/out",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows_out,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Round 7 at pin 06994db (delta since round 6 pin 4bd8cb94: cards.json c040, c054, c097, c119, c128, c162, plus L01 to L08 hunks). "
        "Delta saved as ledgers/SC1/scripts/SC1-e-r7/out/delta_since_round6.diff and read in full.",
        "Round-6 FAIL rows re-verified: SC1e-render-raw-lt PASS, SC1e-c116-c162-duplicate PASS, SC1e-L01-U-existence PASS, SC1e-L07-quiz-digits PASS, "
        "SC1e-L08-quiz-digits PASS. New FAIL: SC1e-c048-hypothesis-mismatch (card c048 lists Assumption 3.1 as a hypothesis; lesson adds it in the conclusion); "
        "SC1e-L03-statements is FAIL because of that card.",
        "Round-6 PASS rows are NOT carried; every row was re-verified with evidence at this pin, since the cited subjects changed or the row was re-derived.",
        "Mutants: not applicable to a cards and lesson slice (no grader); empty list, as in rounds 4 to 6.",
        "Not checked in this round: a line-by-line re-read of the unchanged prose of L01 to L08 (only the delta hunks, the cited statements of every card, "
        "and the lab outputs were read). Rendered-browser screenshots were not taken (page_smoke ran the headless checks). "
        "project.html and labs for other projects are outside this slice. mypy and ruff were not run because no Python source in this slice changed. "
        "Tooling pytest run: tests/test_page_checks.py and tests/test_docs_figures.py passed (55 tests shown, no failures).",
    ],
    "summary": (f"SC1-e round 7 at 06994db: {len(rows_out)} rows (pass={len(rows_out)-len(fails)} fail={len(fails)} unverifiable=0); "
                f"verdict {'FAIL' if fails else 'PASS'}. FAIL: {', '.join(fails) if fails else 'none'}. "
                "All 194 cards read and every changed hunk checked; the single defect is card SC1-c048."),
}
json.dump(frag, open("ledgers/SC1/SC1-e.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote ledgers/SC1/SC1-e.json rows", len(rows_out), "fails", fails)
