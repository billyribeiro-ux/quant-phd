"""Build the round-11 SC1-e fragment from the row evidence written by the verifier (no network).

Usage: python -I build_fragment_r11.py  (run from the checkout root)
"""
import json
import sys

sys.path.insert(0, "tools")
import ledger  # noqa: E402

PIN = "11d7077a290f7960b183d3a5a6631af4773888f9"
BASE = "00a84795f276456fce19d4181373cc4efba11a36"
CW = "ledgers/SC1/scripts/SC1-e-r11/out"

CARRY10 = "Carried from round 10 (course/modules/SC/SC1/{f} byte-identical since the previous pin 00a84795): "

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    rows.append(r)


row("SC1e-structure-ids", "2.7-cards", "course/modules/SC/SC1/cards.json", "PASS",
    f"{CW}/dump_counts.txt and {CW}/scan_r11.out: 208 cards, 208 distinct ids, all match SC1-cNNN; keys are "
    "back, basis, cite, front, grade, id, lesson (or without basis/grade for definitional cards); per lesson "
    "L01 24, L02 30, L03 20, L04 25, L05 33, L06 28, L07 25, L08 23 (sum 208). New since round 10: SC1-c220, SC1-c221 "
    "(both L02). check_pages SC1 PASS (out/check_pages.txt). Ids need not be contiguous; none is missing a rule.")
row("SC1e-full-read-cards", "2.7-cards", "course/modules/SC/SC1/cards.json (all 208 cards)", "PASS",
    f"All 208 fronts and backs printed and read this round in {CW}/cards_L01.txt to cards_L08.txt (dump_cards.py). "
    "Cards whose text changed since 00a84795 (c011, c012, c013, c029, c030, c115, c116, c140, c162, c165, c171, c201, "
    "c206 to c210, new c220 and c221) were re-checked against the lesson text in the rows below; the rest are carried.")
row("SC1e-full-read-lessons", "2.9-prose", "course/modules/SC/SC1/L01.html to L08.html", "UNVERIFIABLE",
    f"This round read in full: L01 (rendered {CW}/L01.txt, all 431 lines, 27,029 bytes) and every changed hunk of "
    f"L01, L04 and L05 ({CW}/delta_r10_to_pin_r11.diff, 330 lines). For L02, L07 and L08 only the passages cited by "
    f"changed cards were read (L02.txt lines 76 to 84, 131 to 154, 271 to 293; L07.txt lines 50 to 78; L08.txt lines 46 "
    f"to 84, 100, 114). L03 and L06 were not re-read. The unchanged remainder of L02 to L08 (about 230 KB rendered "
    "text) was NOT read line by line in this round, so it is not claimed as read.",
    "Next round, read {L02..L08}.txt in full, line by line, recording each section's status; split the reading across "
    "agents if the context budget is short. This round cannot claim it.")
row("SC1e-near-duplicate-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (all pairs)", "PASS",
    f"{CW}/scan_r11.out: no identical front and no identical back. SequenceMatcher ratio >= 0.6 on front+back: "
    "c064/c202 0.792 (Assumption 4.2(a) and 4.2(b)), c170/c218 0.718, c116/c117 0.692 (Lemma 2.1(i) and (ii)), "
    "c161/c167 0.672, c030/c221 0.669 (closed form of M_m and finiteness of the sum), c137/c139 0.655, c011/c012 0.640, "
    "c196/c198 0.626, c067/c068 0.601, c081/c082 0.600. Each pair asks a different fact. c029 (P(E_m^c)) and c220 "
    "(P(Omega*)) do not duplicate each other.")
row("SC1e-learner-text-scan", "2.9-prose", "cards front and back; L01 to L08 text", "PASS",
    f"{CW}/scan_r11.out: no process word (builder, verifier, round, fixer, ledger, reviewer, sub-agent) in any card; "
    "no data-concept markup in any card.")
row("SC1e-card-numbers-in-lesson", "2.7-cards", "cards with a numeric token", "PASS",
    f"{CW}/scan_r11.out: 316 numeric tokens in the cards, 0 absent from the card's own lesson text (substring test, "
    "therefore weak; values recomputed in SC1e-numbers-recomputed). 261 cross-reference tokens, 0 absent.")
row("SC1e-numbers-recomputed", "2.2-numbers",
    "cards c010, c011, c029, c030, c051, c111 to c115, c141, c148 to c150, c159, c170 to c174, c187, c201, c220, c221",
    "PASS",
    f"{CW}/recompute_r11.out (independent script, no lab code imported): c111 1014 triples and c112 78 pairs "
    "(sum over N<=12 of N(N+1)/2 + N^2 = 1014; 78 pairs); c170 sum n*2^n over n=1..12 = 90114; c113 P(M10>=2)=281/512, "
    "2P(S10>2)=11/32, P(S10=2)=105/512; c114 495 = C(12,8) for both counts; c148 14893+6885=21778, 21778/65536=0.332306; "
    "c159 SE sqrt(121*279/(400^2*399))=0.022996; c150 gap (sqrt(2/pi)-0.7586)/0.0317=1.239 SE; c172 exact truncated "
    "means 5.480560, 11.815731, 24.557203; c174 densities 0.241971 and 0.109848, P(tau_1<=1)=0.317311, "
    "P(tau_1<=2)=0.4795; c115 erfc(1/sqrt2)=0.3173105079; c201 1-Phi(1)=0.1586552539; c141 integral = 1/sqrt(2pi)=0.3989423; "
    "c220/c221 sum m r^m with r=2^(-1/2) = r/(1-r)^2 = 8.242641; c030 closed form of M_m agrees with lambda_m 2^(-(m+1)/2) "
    "at m=3 (0.721013); c187 relative gaps of the printed SE against H sqrt(2/N)/20: max +13.21 percent (H=2,N=1), min "
    "-6.6 percent; c051 max |z| 2.39 at H=1,N=2, next largest 1.84. c111 and c113 values were also re-derived by hand.")
row("SC1e-L03-gap", "2.5-labs", "course/modules/SC/SC1/L03.html Lab 1 expected block; cards c051, c052, c187", "PASS",
    f"{CW}/lab_L03.stdout (twin run python -I -W error, exit 0): H=2,N=1 se 0.1601 against 2*sqrt2/20=0.141421, relative "
    "+13.2%; H=2,N=2 se 0.0934 against 0.1, -6.6%; largest |z| other than H=1,N=2 is 1.84 (H=1,N=128). Card c187 (within 14 "
    "percent, largest +13.2 percent at H=2,N=1) and card c051 (|z|=2.39 at H=1,N=2, no other above 1.84) agree.")
row("SC1e-labs-run", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py to lab-SC1-L08-1.py", "PASS",
    "tools/run_labs.py --unit SC1 -> out/run_labs.txt: 'run_labs SC1: PASS (11/11)', exit 0. Each of the eight twins run "
    f"alone with python -I -W error: exit 0 ({CW}/lab_L01.stdout to lab_L08.stdout).")
row("SC1e-labs-page-equals-twin", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html (data-run and expected blocks)",
    "PASS", f"ledgers/SC1/scripts/SC1-e-r10/embed_check_r10.py run at 11d7077 -> {CW}/embed_check_r11.out: for L01 to L08 "
    "code_in_page=True, expected_in_page=True, exit 0.")
row("SC1e-page-smoke", "2.5-labs", "course/modules/SC/SC1/L01.html to L08.html", "PASS",
    f"tools/page_smoke.py --unit SC1 --pages L01 ... L08 -> {CW}/page_smoke.txt: 'page_smoke SC1: PASS', exit 0.")
row("SC1e-check-pages-dag", "2.4-structure", "course/modules/SC/SC1/", "PASS",
    f"tools/check_pages.py --unit SC1 -> {CW}/check_pages.txt 'check_pages SC1: PASS' exit 0; tools/check_dag.py --unit SC1 "
    f"-> {CW}/check_dag.txt 'check_dag SC1: PASS' exit 0.")
row("SC1e-delta-read", "2.9-prose", "cards.json and L01, L04, L05 html since 00a84795", "PASS",
    f"git diff 00a84795 11d7077a restricted to the SC1 slice files, saved as {CW}/delta_r10_to_pin_r11.diff (330 lines). "
    "Changed: cards.json (hunks at c011 to c013, c029, c030, c115, c116, c140, c162, c165, c171, c201, c206 to c210; new "
    "c220, c221); L01.html (why-it-matters, the Section 4 bullet, the A1 block title and parts, the Section 4 proof bullet); "
    "L04.html (Uses line, Assumption 4.1 explain line); L05.html (why-it-matters, items (c) and (h), Remark 1.5, the "
    "Theorem 2.1 interpretation and misconception, Problem Q6 options). Every hunk read in full. L02, L03, L06, L07, L08 html "
    "and tests/labs/SC1 are unchanged. Outside this slice and not verified here: course/modules/SC/SC1/index.html, "
    "project.html and grader/test_project.py changed in the same range.")
row("SC1e-c048-round7", "2.2-numbers", "course/modules/SC/SC1/cards.json card SC1-c048; L03.html Theorem 2.3", "PASS",
    CARRY10.format(f="L03.html") + "card c048 is byte-identical, and its front and back were re-read this round "
    f"({CW}/cards_L03.txt): Q(P_n) to t in mean square, error at most 2t|P_n|, matches the Theorem 2.3 section.")
row("SC1e-L01-statements", "2.9-prose", "course/modules/SC/SC1/L01.html; cards SC1-c001 to c017, c186, c206 to c210, c219",
    "PASS", "L01 changed this range, so the statement rows were re-verified this round against the full L01 text "
    f"({CW}/L01.txt). c007 hypotheses (H2 A1(a)) match Proposition 1.2 (L01 lines 72 to 76); c008 (H2 A1(b), A1(a)) matches "
    "Remark 1.3; c011 to c013 match Section 4 (L01 line 199 to 201) with Remark 2.6 of Lesson 2; c014 to c016 match the "
    "misconception and Example 1.4 text (lines 203, 211, 215); c010 matches the Lab 1 block (lines 120, 188 to 189); c206 to "
    "c210 match Assumption A1(a) to (e) (lines 58 to 66); c219 matches line 100 (Gaussian process remark). No defect.")
row("SC1e-L02-statements", "2.9-prose", "course/modules/SC/SC1/L02.html; cards SC1-c018 to c041, c184, c185, c211 to c213, c220, c221",
    "PASS", "L02.html is byte-identical since 00a84795. Cards that changed were re-verified against L02.txt: c029 "
    "(line 143, P(E_m^c)<=2^-m by Lemma 2.1 and a union bound), c030 (line 148, M_m closed form), c220 (lines 143 to 145: "
    "P(A_m0^c)<=2^(1-m0), continuity from below, Assumption 2.1(c) at line 82, P(Omega*)=1), c221 (line 150, r^m sum). "
    "Unchanged cards c018 to c028, c031 to c041, c184, c185, c211 to c213 are carried from round 10 (byte-identical); c033, "
    "c034 and c035 were also re-read against lines 271, 283 and 289 to 293. c211 to c213 match Assumption 2.1(a) to (c) "
    "(lines 78 to 82).")
row("SC1e-L03-statements", "2.9-prose", "course/modules/SC/SC1/L03.html; cards SC1-c042 to c060, c187, c188", "PASS",
    CARRY10.format(f="L03.html") + "L03 cards c042 to c060, c187 and c188 are byte-identical. Re-checked this round: c044 to "
    "c050 (E Z^4=3, Var X^2=2 Delta^2, sum of (2j+1)^2 = N(4N^2-1)/3), c052 (H sqrt(2/N)/20), c053 (Var of squares <= E of "
    "fourth power), c054 (Var = 2t^2 for every N), c057 (sqrt(2Nt/pi)), c059 (c=2 for equal partitions), c187 and c051 against "
    f"{CW}/lab_L03.stdout.")
row("SC1e-L04-statements", "2.9-prose", "course/modules/SC/SC1/L04.html; cards SC1-c061 to c082, c202 to c204", "PASS",
    "L04.html changed (Uses line; Assumption 4.1 explain line at L04 line 385). Re-verified this round against L04.txt: Assumption "
    "4.1 (line 48) against c063 and the explain line; Assumption 4.2(a) to (d) (line 54) against c064 and c202 to c204; "
    "Propositions 2.2 to 2.4 proofs (lines 84 to 128) against c067 to c071; c069 (remark at line 110); c076 (E[(B_s+Y)^3|F_s] "
    "= B_s^3+3(t-s)B_s, line 227); R1 to R3 and P1 to P3 (lines 281 to 345) against c073 to c082. c072 matches "
    f"{CW}/lab_L04.stdout. Definition 1.2 (c065) block unchanged in the delta and carried.")
row("SC1e-L05-statements", "2.9-prose", "course/modules/SC/SC1/L05.html; cards SC1-c083 to c105, c189, c193 to c200, c214, c216",
    "PASS", "L05.html changed. Re-verified this round against L05.txt: Assumption A4 items (a) to (i) (lines 44 to 60) against "
    "c193 to c200 and c214; Lemma 1.3 (line 86) and Theorem 1.4 (line 102) against c086, c087, c100, c104; Remark 1.5 (line 120) "
    "against c088: the card names A4(a), A4(b), A4(f), the narrower and correct set, and the lesson says 'assuming A4', so they "
    "agree (no defect); Theorem 2.1 (line 138, A4(e)) against c090 and c102; c097 (R1, lines 390 to 394: path 1 has eta*=1/4, path "
    "2 has eta*=3/4, they agree on [0,1/2], A4(d)) against c097; c099 and c133 against the A3 statement (lines 262 to 282); c105 "
    "(M3, line 328); c091, c092, c216 against "
    f"{CW}/lab_L05.stdout (225 cases, largest gap 5.55e-16, mass 3.81e-29, integral 1.0000000000); c103 (line 445, B_1=1 gives 3).")
row("SC1e-L06-statements", "2.9-prose", "course/modules/SC/SC1/L06.html; cards SC1-c106 to c133, c217", "PASS",
    CARRY10.format(f="L06.html") + "the cards c106 to c114, c117 to c133 and c217 are byte-identical and carried. Changed card "
    "c115 and c116 were re-verified: Lemma 2.1 (L06.txt line 88: B continuous, a>0, t>0, B_0=0) against c116; Theorem 2.5 and "
    "Corollary 2.6 (lines 138, 162) against c115; c111 to c114 and c113 re-derived (rows SC1e-numbers-recomputed); "
    f"{CW}/lab_L06.stdout matches.")
row("SC1e-L07-statements", "2.9-prose", "course/modules/SC/SC1/L07.html; cards SC1-c134 to c159, c191, c215", "PASS",
    CARRY10.format(f="L07.html") + "the cards c134 to c136, c141 to c146, c148, c149, c150, c152 to c157, c159, c191 and c215 "
    "are byte-identical and carried. The changed card c140 (the round-10 FAIL) is now correct against L07.txt lines 70 to 74: "
    "Corollary 1.5(b) needs H1, H2 (A3, A4 of Lesson 5), H3 and A5. c137, c138 and c139 re-read against lines 52 to 66 "
    f"(Theorem 1.3, Remark 1.4, Corollary 1.5(a)). c148 (21778), c149, c150 against {CW}/lab_L07.stdout. c141 proof "
    "(P2, line 420) re-read: integration by parts and R(1-Phi(R)) <= phi(R) are correct.")
row("SC1e-L08-statements", "2.9-prose", "course/modules/SC/SC1/L08.html; cards SC1-c161 to c183, c201, c205, c218", "PASS",
    CARRY10.format(f="L08.html") + "the unchanged cards are carried. Changed cards re-verified this round: c162 against "
    "Proposition 1.2 hypotheses (L08.txt lines 48 to 50); c165 against Corollary 1.5 (line 76) and its derivative (line 80); "
    f"c171 (512, 0, 384, 0, 288, 0, 224, 0, 180, 0; 1588; 794) against {CW}/lab_L08.stdout and the reflection count; c201 "
    f"against Lab 1 Part D of this lesson (0.317311, {CW}/lab_L08.stdout) and Lab 1 Part D of Lesson 7 (0.1586552539, "
    f"{CW}/lab_L07.stdout). c172 and c174 re-derived.")
row("SC1e-assumption-labels", "2.9-prose", "cards naming A1 to A5 and Assumptions 2.1, 3.1, 3.2, 4.1, 4.2", "PASS",
    "Each named assumption exists with that content: A1(a) to (e) (L01.txt lines 58 to 66); Assumption 2.1(a) to (c) (L02.txt "
    "lines 78 to 82); A2 (c033 against L02.txt line 271); Assumption 3.1 and 3.2 (c188, c060; carried); Assumption 4.1 (line 48); "
    "Assumption 4.2(a) to (d) (line 54); A3 (L05.txt line 262 to 270); A4(a) to (i) (lines 44 to 60); A5 (L07.txt lines 76 to 78).")
row("SC1e-cross-references", "2.9-prose", "cards naming Problems, Sections, Lab parts and numbered results", "PASS",
    f"{CW}/scan_r11.out: 261 cross-reference tokens checked against the card's own lesson text, 0 absent; 44 'of Lesson K' "
    "references. Checked by hand: c220 (Assumption 2.1(c), L02.txt line 82), c221 (step 2 of Proposition 2.4(b)), c140 (Lesson 5 "
    "and Theorem 1.3 of Lesson 7), c201 (Lab 1 Part D of Lesson 7).")
row("SC1e-hypotheses-carried", "2.9-prose", "cards for Lemma, Proposition, Theorem, Corollary, Remark statements", "PASS",
    "The round-10 FAIL is cleared: the front of SC1-c140 now carries H1 (standard Brownian motion with continuous paths and "
    "B_0=0), H3 (H>0), A3, A4 and A5. Hypotheses of every card changed in this range were re-checked: c011 to c013 (Remark 2.6 of "
    "Lesson 2, A1(a), A1(b), A1(e), A2, Assumption 2.1), c029 (H1, Assumption 2.1), c220 (H1, H2, Assumption 2.1), c030 and c221 "
    "(H1 of Proposition 2.4(b)), c115 (continuous paths, A3, A4), c116 (L06 Lemma 2.1), c162 (Proposition 1.2 H1, H2), c165 "
    "(H1, H2 of Proposition 1.2, A3, A4), c201 and c205. The other statement cards were carried from round 10.")
row("SC1e-grades-audit", "2.4-grades", "cards with grade C and grade T", "PASS",
    f"{CW}/scan_r11.out: 122 cards graded T and 23 graded C; 'T/C cards without basis []'. New c220 and c221 are T with bases "
    "(Proof of Proposition 2.4(a) and (b), step 2). C cards cite a SIMULATED or numerical lab (c010, c037, c038, c051, c072, c091, "
    "c092, c111 to c114, c148 to c150, c170 to c174, c187, c216, c218).")
row("SC1e-cites-and-registry", "2.3-registry", "cards.json cite fields", "PASS",
    f"{CW}/scan_r11.out: 'cite nonempty []': no card cites a registry key. The lessons cite no registry source (L01.txt line "
    "425; L02.txt line 544). references/references.json changed in the range but has no SC1 key in use.")
row("SC1e-notation", "2.6-notation", "cards and L01 to L08 text; notation/notation.json", "PASS",
    "git diff 00a84795 11d7077a -- notation is empty. New L01 macros: \\Cov, \\Var, \\Prob, \\indic, \\Normal are registered; "
    "\\operatorname{Bor}, \\mathrm{Leb}, \\mathcal F, \\Omega are not registry macros but reuse no registered meaning (the same "
    "class as the existing \\mathcal F in L04 and L05). No T, gamma, R^*, or Phi reuse in the changed text.")
row("SC1e-dag", "2.8-dag", "cards; L01 to L08 text", "PASS",
    f"check_dag SC1 PASS ({CW}/check_dag.txt). Cross-references in the changed text point inside SC1 (Remark 2.6 of Lesson 2 "
    "from L01 Section 4; Theorem 2.3 of Lesson 3 from L04 Uses) or to M6 Lesson 9 Definition 9.1 (course/modules/M/M6/L09.html, "
    "the stopping-time definition, which L05 uses). No new concept link in any card.")
row("SC1e-scope-words", "2.4-scope", "cards and the changed lesson text", "PASS",
    "Scope words in the changed text are each backed: L01 Section 4 'for every finite set of times' (P(U in G)=0) and 'for every "
    "outcome' (B~_U=B_U+1); L05 Remark 1.5 'any standard Brownian motion' (explicitly under assumed A4); L05 Theorem 2.1 'for all "
    "u,v>0' (Lemma 2.2 and A4(e)); c220 'for every' (sum of the bounds for m>=m_0). No unsupported universal claim found.")
row("SC1e-r8-twin-docstring-only", "2.5-labs", "tests/labs/SC1/ twins", "PASS",
    "tests/labs/SC1 is byte-identical since 00a84795 (not in the delta). The L01 twin docstring (lines 124 to 130) was re-read "
    "against the output and the page text (page lines 118 to 120 and 191): 'simulates no path' and 'exact on grids' agree. The "
    "other twin docstrings are carried from round 10.")
row("SC1e-c052-term", "2.9-prose", "course/modules/SC/SC1/cards.json card SC1-c052 front and back", "PASS",
    CARRY10.format(f="L03.html") + "card c052 is byte-identical. Re-checked this round: H sqrt(2/N)/20 with t=H matches "
    "Var(Q)=2H^2/N (equal steps) and sqrt(400)=20.")
row("SC1e-c150-assumption-reference", "2.9-prose", "course/modules/SC/SC1/cards.json card SC1-c150 back", "PASS",
    "c150 is unchanged. 'Assumption A5 of Lesson 7' exists (L07.txt line 76). sqrt(2/pi)=0.797885; gap 1.239 SE = "
    f"(0.797885-0.7586)/0.0317 ({CW}/lab_L07.stdout).")
row("SC1e-c140-hypotheses", "2.9-prose", "course/modules/SC/SC1/cards.json card SC1-c140 front", "PASS",
    "The round-10 fix is applied at 11d7077: front now reads 'Corollary 1.5(b). Hypotheses: B is a standard Brownian motion with "
    "continuous paths and B_0=0; H>0 is fixed; Assumptions A3 and A4 of Lesson 5 hold; Assumption A5 (the tail formula for a "
    "nonnegative variable) holds. What is E[M_H]?' This matches L07.txt lines 72 to 74. Back: 2 sqrt(H) times the integral of "
    "(1-Phi(u)) equals 2 sqrt(H)/sqrt(2 pi) = sqrt(2H/pi).")
row("SC1e-c219-new", "2.9-prose", "course/modules/SC/SC1/cards.json card SC1-c219", "PASS",
    "c219 unchanged. Matches L01 Remark 1.3 (H2 'assuming A1(a) and A1(b)') and L01.txt line 100: Gaussian process, mean 0, "
    "covariance min(s,t) for s,t>0.")
row("SC1e-c220-c221-new", "2.2-numbers", "course/modules/SC/SC1/cards.json SC1-c220, SC1-c221", "PASS",
    "New in this range. c220: P(Omega*)=1; P(A_m0^c)<=2^(1-m0) (sum of 2^-m for m>=m0); continuity from below (Assumption 2.1(c)) "
    "against L02.txt lines 143 to 145, which state the same chain. c221: M_m<=sqrt(2 log 2) m r^m since sqrt(m)<=m; sum m r^m = "
    "r/(1-r)^2 finite for r=2^(-1/2) against L02.txt line 150. Both graded T with a proof basis, consistent with the L02 key-results "
    "row (line 455).")
row("SC1e-c029-c030-changed", "2.2-numbers", "course/modules/SC/SC1/cards.json SC1-c029, SC1-c030", "PASS",
    "Changed fronts and backs re-checked. c029 P(E_m^c)<=2^-m: 2e^(-lambda_m^2/2)=2*2^(-2m), union bound over 2^(m-1) coefficients "
    "gives 2^(m-1)*2^(1-2m)=2^(-m) (L02.txt line 143). c030 M_m=lambda_m 2^(-(m+1)/2)=sqrt(2 log 2) sqrt(m) 2^(-m/2) (L02.txt "
    f"line 148; {CW}/recompute_r11.out at m=3).")
row("SC1e-c011-c013-changed", "2.9-prose", "course/modules/SC/SC1/cards.json SC1-c011, c012, c013", "PASS",
    "Changed fronts (now name A1(a), A1(b), A1(e), A2, Assumption 2.1 of Lesson 2 and Remark 2.6 of Lesson 2) match L01.txt "
    "Section 4 (lines 199 to 201) and L02.txt Remark 2.6 hypotheses (line 293). Answers match the section: same finite-dimensional "
    "laws because P(U in F)=0; B~_U=B_U+1 and B~_t -> B_U as t -> U, so discontinuous at U; the continuity event holds for B on every "
    "outcome and for B~ on none.")
row("SC1e-L08-changed-cards", "2.2-numbers", "course/modules/SC/SC1/cards.json SC1-c162, c165, c171, c201", "PASS",
    "All four changed backs/fronts are re-derived in the L08 row above and in SC1e-numbers-recomputed; the lab values match "
    f"{CW}/lab_L08.stdout and {CW}/lab_L07.stdout.")
row("SC1e-lab-outputs-cards", "2.5-labs", "cards backed by a lab (c037, c038, c051, c072, c091, c092, c111 to c114, c127, c149, c150, c170 to c174, c187, c216, c218)",
    "PASS",
    f"Each card's lab number compared with its twin's stdout ({CW}/lab_L02.stdout to lab_L08.stdout): c037 216 of 216 "
    "(L02 line 1); c038 8 of 8 levels within bound; c051 and c187 (L03); c072 54.598150033 and e^4 (L04); c091 225 cases, "
    "c092 1.0000000000, c216 5.55e-16 (L05); c111 1014, c112 78, c113, c114 495, c127 105/512 (L06); c148 0.332306, c149 "
    "0.2275 and 0.3025 with SE 0.0210 and 0.0230, c150 0.7586 and SE 0.0317, c201 0.1586552539 (L07); c170 90114, c171 "
    "counts, c172 means, c173 sample means and z, c174 density and P(tau<=1) (L08); c218 78 of 78 (L08).")

mutants = []

fragment = {
    "unit": "SC1",
    "slice": "e",
    "round": 11,
    "verifier": "Claude Haiku 5.5, independent verifier for SC1-e: all cards of course/modules/SC/SC1/cards.json (208) against lessons L01 to L08; round 11",
    "pin": PIN,
    "base": BASE,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-e",
    "scratch": CW,
    "verified_at": "2026-11-05T12:10:00Z",
    "verdict": None,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [
        "Gates run this round at 11d7077: run_labs, page_smoke, check_pages, check_dag, twins under python -I -W error, embed_check, recompute_r11.py, scan_r11.py.",
        "Not run: ruff, mypy, pytest, verify_refs. No Python module outside the lab twins and no tool or registry file in this slice changed in the range; the slice cites no registry key.",
        "Out of slice and not verified here: course/modules/SC/SC1/index.html, project.html, grader/test_project.py (changed in the same range).",
    ],
    "notes": (
        "Round 11 at pin 11d7077 (delta base 00a84795). The round-10 FAIL rows SC1e-L07-statements, SC1e-hypotheses-carried and "
        "SC1e-c140-hypotheses are cleared (c140 now carries H1, H3). The UNVERIFIABLE row SC1e-full-read-lessons remains: a "
        "full line-by-line read of L02 to L08 was not completed this round. Rows that carry round-10 evidence say so with the "
        "'Carried from round 10' prefix, and cite the byte-identical files. Minor observations, not findings: c088 names A4(a), "
        "A4(b), A4(f) where the L05 remark says 'assuming A4'; c220 writes P(Omega*)=lim P(A_m0) >= 1 where =1 is the claim (the "
        "upper bound is trivial, so this is a wording point only). No mutants: this slice has no grader."
    ),
    "summary": None,
}

n_pass = sum(1 for r in rows if r["status"] == "PASS")
n_unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
n_fail = sum(1 for r in rows if r["status"] == "FAIL")
fragment["verdict"] = "PASS" if n_pass == len(rows) else "FAIL"
fragment["summary"] = (
    f"SC1 slice e round 11 at 11d7077a: {len(rows)} rows; PASS {n_pass}, FAIL {n_fail}, UNVERIFIABLE {n_unv}. "
    "Non-PASS: SC1e-full-read-lessons (full line-by-line read of L02 to L08 not completed). Verdict FAIL."
)
path = "ledgers/SC1/SC1-e.json"
with open(path, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "PASS", n_pass, "FAIL", n_fail, "UNVERIFIABLE", n_unv, "verdict", fragment["verdict"])
print("validate:", ledger.validate(json.load(open(path, encoding="utf-8")), "SC1-e"))
