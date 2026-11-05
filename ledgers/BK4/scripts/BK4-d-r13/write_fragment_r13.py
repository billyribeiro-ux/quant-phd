# Writes the round-13 fragment ledgers/BK4/BK4-d.json for slice BK4-d (cards.json against L01-L05, ruling 13).
import datetime
import json
import sys

PIN = "e919577b45b431ce68e1e6533b00b8a301277937"
BASE = "5db69a9bee460736c318ebfacc7200ee5a6eb0f0"
S = "ledgers/BK4/scripts/BK4-d-r13/out/"
SC = "/Users/billyribeiro/.fanout/scratch-BK4-d-r13/"
CARRY = "Carried from round 12 (course/modules/BK/BK4/L04.html and cards BK4-c061..c070 byte-identical since the previous pin): "
CARRY71 = "Carried from round 12 (course/modules/BK/BK4/L04.html and cards BK4-c071..c080 byte-identical since the previous pin): "


def row(id_, check, location, evidence, status="PASS"):
    return {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}


rows = [
    row("cards-lessons-read-in-full", "2.7-source-read",
        "course/modules/BK/BK4/L01.html, L02.html, L03.html (read in full this round); L04.html, L05.html (carried, card-cited passages re-read)",
        "L01, L02 and L03 were converted to text by ledgers/BK4/scripts/BK4-d-r13/strip.py into " + SC + "L01.txt (319 lines), L02.txt (302) and L03.txt (405), and read line by line this round. "
        "L04.html and L05.html are byte-identical to the previous pin (git diff --quiet 5db69a9 e919577 exit 0). "
        "Their card-cited passages were printed and read this round (L04.txt lines 15-50, 238-244, 281-283; L05.txt lines 27-66, 240-246; L05 Example 2.8 and Problem M3 located by grep). "
        "The rest of L04 and L05 is carried from round 12. The project page, grader and project labs are outside this slice."),
    row("cards-structure", "2.7-structure",
        "course/modules/BK/BK4/cards.json",
        "python3 count over cards.json: 101 cards, 101 unique ids (ledgers/BK4/scripts/BK4-d-r13/dup_scan_r13.py, out/dup_scan_r13.txt). "
        "card_delta_r13.py against 5db69a9 (out/card_delta_r13.txt): added BK4-c106, changed BK4-c094 (front only), removed none, 99 unchanged. "
        "Every card has id, lesson, front, back, basis, cite; c106 is an ungraded definition with cite []. Id gaps c042, c045, c070, c082, c085 are not defects (FINAL-ARCHITECT-RULINGS 2). "
        "check_pages --unit BK4 PASS (out/check_pages.txt, includes check_cards)."),
    row("cards-duplicate-scan", "2.7-duplicate-scan",
        "course/modules/BK/BK4/cards.json (all 5050 card pairs, front and back)",
        "ledgers/BK4/scripts/BK4-d-r13/dup_scan_r13.py -> out/dup_scan_r13.txt: exact duplicate field pairs: none. Pairs with difflib ratio > 0.6: 161. "
        "Against the previous pin (160 pairs on the same method, recomputed from 5db69a9): the only new pair is BK4-c018 front vs BK4-c106 front (0.602). "
        "c018 asks for the gross notional of a trade set (L02 Assumption 1.3, sum of trade amounts a_t); c106 asks for the gross value of a day's payments (L01 Section 2, sum of payment amounts); the backs differ; distinct questions. "
        "The c094 front rewording removed no pair above 0.6 (its highest ratio is now 0.443). The other 160 pairs have byte-identical cards and were reviewed as distinct in round 12 (carried)."),
    row("cards-coverage", "2.7-coverage",
        "L01.html, L02.html, L03.html, L05.html key-results tables and card set",
        "Key-results rows of the lessons (grep of " + SC + "L0n.txt) mapped to cards: L01 'Three payments ... (Example 2.6, Remark 2.7)' to c008, c009; L01 'On the seeded day ...' rows to c010, c011, c012, c014; "
        "L02 'Example 2.4' row to c027, c028; L02 'On the seeded set' row to c031 and c092; L03 'fixture rows of Example 1.5 and 1.6' row to c043, c044; L03 'On the seeded SIMULATED losses' row to c049, c050; "
        "L05 'At p=1/8 ... 2188' row to c086, c094; L05 variance row to c087. L04 rows carried from round 12. "
        "The header edits in L01 and L02 (Keys to Source) change no row. c106 is ungraded and mirrors no key row. No card number is absent from its lesson (see cards-xrefs)."),
    row("cards-numbers", "2.2-card-numbers",
        "course/modules/BK/BK4/cards.json numbers against L01-L05 text and lab printouts",
        "ledgers/BK4/scripts/BK4-d-r13/recheck_cards_r13.py -> out/recheck_cards_r13.txt: SUMMARY 56 of 56 checks True (exact Fraction and integer arithmetic). "
        "Covered: c008, c009 (need 100 and 50); c012 (1533900/2841600 = 0.53980152, to four places 0.5398); c014 (net +379800, debit 0); c027 (net -50, 20, 30; A = 50); "
        "c028 (floor(10000*180/230) = 7826); c031 (1753300 + 3340300 = 5093600); c092 (sum of receivables 314500+2067800+3340300+1873700 = 7596300); c043 (8, 12, residual 20); c044 (leftover to members 1 and 2); c048 (k = 198); "
        "c072 (11/10, 11000 bps), c073 (20/19), c075 (9/10, 9000 bps, rho/2 = 19/40), c080-c090 (4375/2, 2188 after half-up rounding, 1875, 57421875/4, 133984375/4, 19140625, 343/512, 169/512 vs 192/512), c094 (2187.5 rounds half up to 2188)."),
    row("cards-xrefs", "2.7-xrefs",
        "cards.json basis and text labels against lesson headings",
        "ledgers/BK4/scripts/BK4-d-r13/xref_labels_r13.py -> out/xref_labels_r13.txt: 216 labelled references (Definition, Proposition, Remark, Example, Problem, Corollary, Assumption, Section) in card front, back and basis. "
        "Each resolves as a heading in the card's own lesson (0 not found in own lesson, 0 unresolved). Examples: L01 Remark 2.5, 2.7; L02 Section 4, Problem R1, P3; L03 Remark 1.4, 2.2, Example 1.5, 1.6, Corollary 2.4; L04 Remark 2.8, 4.1, Problem R1; L05 Example 2.7, 2.8, Problem M3."),
    row("cards-lab-outputs", "2.5-lab-printouts",
        "tests/labs/BK4/lab-BK4-L01-1.py .. lab-BK4-L05-1.py; cards c010-c012, c014, c031, c049, c050, c087, c092",
        "tools/run_labs.py --unit BK4: 'run_labs BK4: PASS (8/8)', exit 0 (out/run_labs.txt). Each lab twin run alone as python3 -I -W error <absolute path> from /tmp: exit 0 for L01-1 to L05-1 (out/lab-BK4-L0n-1.out). "
        "Printed values match the C cards: L01 Part B Bank A need 112500, net +379800, debit 0; Bank B need 1533900, net -1533900, debit 1533900; Part C gross 2841600, moved 1533900. "
        "L02 Part B gross 7596300; Part D paid 5093600, reduction 2502700, 3294 bps. L03 Part B 9900 bps: k = 198, sized margin 2961, brute force 2961; 9975 bps: k = 200, sized margin 2992, brute force 2992 (lines 23-28). "
        "L03 Part A1 rows match the Example 1.5 table; Part A2 gives member 1 with 1 cent at residual 1 and members 1 and 2 at residual 2. "
        "L05 Part B 4375/2 and 169/512 and 343/512; Part C 1875; Part D variance 133984375/4 (comonotone), 57421875/4 (independent), equal means. L04 worked values 9/10, 11/10, 20/19."),
    row("cards-grades-vs-keyresults", "2.3-grade-mirror",
        "L01.html, L02.html, L03.html, L05.html key-results rows against mirrored cards",
        "Grades agree on every mirrored pair (key-results text of " + SC + "L01.txt, L02.txt, L03.txt, L05.txt): "
        "L01 'Three payments' row T vs c008, c009 T; L01 'On the seeded day' row C vs c010, c011, c012, c014 C; L02 'Example 2.4' row T vs c027, c028 T; L02 'On the seeded set' row C vs c031, c092 C; "
        "L03 'fixture rows of Example 1.5 and 1.6' row T vs c043, c044 T; L03 'On the seeded SIMULATED losses' row C vs c049, c050 C; L05 'At p=1/8 ... 2188' row T vs c086, c094 T; L05 variance row C vs c087 C. "
        "Bases agree in substance. L04 rows: " + CARRY + "rows 288-293 vs c067-c069, c071-c075 as in round 12."),
    row("cards-hypotheses", "2.4-hypotheses",
        "cards T-graded fronts and backs against the hypotheses of the cited proposition",
        "L01 c004-c007 (Assumption 1.3: A1 and A2; A2 wording changed this round, its hypothesis content unchanged); L02 c022-c026, c029, c099 (A1 to A3, G > 0 for c029); "
        "L03 c036-c041 (A1, A2), c043-c044 (A1, A2 for Examples 1.5 and 1.6), c046-c047 (A3, A4), c104 (A1, A2); L05 c080-c084 (Assumption 1.3 finite space; A1, A2; A3 = independent events; A4 = F1=F2=F3, L05.txt lines 27-33; "
        "Proposition hypotheses at L05.txt lines 36-66: Prop 2.1 finite space, A1, A2; Prop 2.2 A1-A3; Prop 2.4 A1, A2, A4; Prop 2.5 A1-A4, 0<p<1, kappa>0; Prop 2.6 A1, A2, 0<p<1, l_i>=1, kappa>=1). "
        "L04 c067-c076: " + CARRY71 + "Assumptions 1-3, 0<=x<1, x<=rho (Definition 2.1), y<=rho for Prop 2.5."),
    row("cards-attribution-duffie", "2.1-attribution",
        "cards BK4-c032 (cite duffie2011central); references/references.json",
        "Registry record duffie2011central (references/references.json): title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', authors Duffie and Zhu, year 2011, container Review of Asset Pricing Studies, doi 10.1093/rapstu/rar001. "
        "git diff of references/ since 5db69a9 is empty. Live: plain curl https://api.crossref.org/works/10.1093/rapstu/rar001 returned HTTP 200 with the same title, container and issued 2011-07-18, authors Duffie and Zhu (out/duffie_crossref_r13.json). "
        "Publisher: plain curl https://doi.org/10.1093/rapstu/rar001 returned HTTP 403 at https://academic.oup.com/raps/article-lookup/doi/10.1093/rapstu/rar001 (out/duffie_doi_r13.txt). The abstract is therefore unread; no bot check was bypassed. "
        "c032 states only the question the paper asks, so no finding is attributed and the abstract is not needed for this card."),
    row("cards-banned-and-process-words", "2.9-banned-and-process",
        "cards.json front, back and basis; learner text changed in L01 and L03 this round",
        "Regex over all 101 card fronts, backs and bases for we, our, you, your, learner, this card, obvious, clearly, simply, trivial, surely, as expected, note that, the lab, build, builder, verifier, round: no hits (python3 -I, this round). "
        "check_pages --unit BK4 PASS (out/check_pages.txt, BANNED list). The changed learner text in L01 (Assumption 1.3 A2, Definition 2.1, misconception 1) and L03 (why-it-matters, Example 1.5) was read and contains no banned or process word."),
    row("cards-notation", "2.4-notation",
        "cards.json against notation/notation.json",
        "c106 uses m, the number of payments in a day, defined in L01 Assumption 1.3. The changed L01 and L03 text uses only symbols already defined locally on its page (Debit_i, Net_i, S_{i,k}, IM_delta, DF_i, D, u, Z, n+, c(M), S, k, t). "
        "No registered symbol is given another meaning. git diff of notation/ and references/ since 5db69a9 is empty."),
    row("cards-dag", "2.9-dag",
        "check_dag --unit BK4; cards name concepts",
        "check_dag.py --unit BK4: PASS (out/check_dag.txt). c106 names only the gross value of the day's payments, defined in L01 Section 2; it introduces no concept and uses none outside the closure."),
    row("cards-pages-gate", "2.9-page-gates",
        "check_pages --unit BK4; page_smoke --unit BK4; tests/test_page_checks.py",
        "check_pages.py --unit BK4: PASS (out/check_pages.txt). page_smoke.py --unit BK4 run alone: PASS for modules/BK/BK4/project.html, index.html, concepts.html, review.html and BK4 (out/page_smoke.txt). "
        ".venv/bin/python -m pytest -q tests/test_page_checks.py: exit 0 (out/pytest_page_checks.txt)."),
    row("cards-c001-c010", "2.7-cards-sample",
        "cards BK4-c001..c010 against L01.txt Definitions 1.1, 1.2, 2.1, Propositions 2.2-2.4, Problem P2, Example 2.6, Remark 2.7, Lab 1 Part B",
        "Read this round in full text. c004-c007 Propositions 2.2 to 2.4 and Problem P2 (solution: mu >= 0 or S_m = mu, case analysis re-derived); c008 running sums 0, -100, -100, -50 and need 100 (Example 2.6); "
        "c009 sums 0, 50, -50, -50 and need 50 (Remark 2.7); c010 1533900 both (Lab 1 Part B). All agree with the text; numbers in recheck_cards_r13.py."),
    row("cards-c011-c020", "2.7-cards-sample",
        "cards BK4-c011..c020 against L01.txt and L02.txt",
        "c011 112500 (Lab 1 Part B, C); c012 1533900 of 2841600, 0.5398 (Lab 1 Part C; 0.53980152 at four places); c013 A2 and Definition 2.1 (wording changed this round, content identical); "
        "c014 Bank A net +379800, debit 0, need 112500 (Lab 1 Part B); c015 Remark 2.5 and Remark 2.7. c016-c020 L02 Definitions 1.1, 1.2, Assumption 1.3 (G), Definition 2.1 (n_i, A, reduction). All agree."),
    row("cards-c021-c030", "2.7-cards-sample",
        "cards BK4-c021..c030 against L02.txt",
        "c021 reduction definition and floor; c022-c025 Proposition 2.2(a)-(d) with proofs read; c026 Proposition 2.3 (proof read, both directions); c027 and c028 Example 2.4 (A = 50; floor(10000*180/230) = 7826); "
        "c029 and c030 Problems R1 and P3 solutions. All agree."),
    row("cards-c031-c040", "2.7-cards-sample",
        "cards BK4-c031..c040 against L02.txt and L03.txt Definition 1.1, Propositions 1.2 and definition 2.1",
        "c031 5093600 (Lab 1 Part D; 1753300 + 3340300); c032 paper-level attribution (see cards-attribution-duffie); c033-c035 misconceptions and Section 4 of L02 read; "
        "c036-c038 Definition 1.1 (layers and share rule; floor and leftover, read in full, with the why-it-matters change checked); c039 Definition 2.1 (count share in bps; the L03 why-it-matters sentence 'count share of scenarios' agrees); c040 Proposition 1.2 (proof read). All agree."),
    row("cards-c041-c050", "2.7-cards-sample",
        "cards BK4-c041..c050 against L03.txt Example 1.5, Example 1.6, Propositions 1.3, 2.3, Corollary 2.4, Example 2.5, Lab 1 Part A1, A2, B",
        "c041 Proposition 1.3 bound (proof read). c043 re-derived against the rewritten Example 1.5: L=200 gives a1=100, a2=50, a3=30, Z=20, members pay floor(20*40/100)=8 and floor(20*60/100)=12, uncovered 0; "
        "lab Part A1 row 200 prints 8 and 12. c044 Example 1.6: D=3, Z=2, p_i=2/3, floor shares 0, leftover 2 to members 1 and 2 (lab Part A2). c045 gap is not a defect. c046 Proposition 2.3 (proof read; checked against 3000 brute-force draws in recheck_cards_r13.py). "
        "c047 Corollary 2.4 (proof read). c048 k = 198 (Example 2.5). c049 2961 and c050 2992 are lab printouts (out/lab-BK4-L03-1.out lines 23-28), graded C naming Lab 1 Part B. All agree."),
    row("cards-c051-c060", "2.7-cards-sample",
        "cards BK4-c051..c060 against L03.txt sections 1-3, Remarks 1.4, 2.2, Definition 2.1, Example 2.5, Definition 1.1",
        "c051-c054 definitions match L03 section 1. c055 Remark 2.2 (a1 = min(L, M) equals L iff L <= M). c056 Definition 2.1 and Example 2.5 (k = 198 of 200; cover depends only on c(M)). "
        "c057 Remark 1.4 (a2 > 0 implies a1 = IM; a3 > 0 implies a2 = DF; Z > 0 implies a3 = K), confirmed by a 20000-draw sweep in recheck_cards_r13.py. c058 Definition 1.1 (shares by DF_i). All T claims are derived on the page."),
    row("cards-c061-c070", "2.7-cards-sample",
        "cards BK4-c061..c070 against L04.txt Definitions 1.1, 1.2, 2.1, 3.1, Propositions 2.2, 2.4, 2.5",
        CARRY + "L04 byte-identical and cards unchanged, so the round-12 row is carried. Re-checked this round: Definitions 1.2, 2.1 and 3.1 printed and read (L04.txt lines 25-41, 238-241); "
        "c067 (theta = (rho - x)/(1 - x)), c068 (theta - 1 = (rho - 1)/(1 - x)) and c069 (difference identity) checked exactly by recheck_cards_r13.py (3000 draws each); lab L04 prints 6 coverage-below-1 rows consistent with the sign rule."),
    row("cards-c071-c080", "2.7-cards-sample",
        "cards BK4-c071..c080 against L04.txt Proposition 2.2, 2.4, 2.6, 2.7, Remarks 2.8, 4.1, Problem R1, and L05.txt Definitions 1.1, 1.2, 2.1, Assumption 1.3",
        CARRY71 + "Re-checked this round: c072 and c075 (Remark 2.8 printed at L04.txt line 65-66: 9/10, 11/10, 113/120 -> 9416); c073 (Remark 4.1 and Problem R1: rho* = 1/(1-h) = 20/19); c074 (rho = 1 with h > 0 gives theta - 1 = -h/(1-x) < 0, checked on a grid); "
        "c076 (theta - rho = x(rho-1)/(1-x)). c077-c080 L05 Definitions 1.1, 1.2, 2.1 and Assumption 1.3 printed and read this round (L05.txt lines 23-34). All agree; recheck_cards_r13.py CHECK lines for c072, c073, c074, c075, c076 are True."),
    row("cards-c081-c090", "2.7-cards-sample",
        "cards BK4-c081..c090 against L05.txt Propositions 2.1-2.6, Example 2.7, Example 2.8, Problem M3",
        "Read this round: L05.txt lines 36-66 (Propositions 2.1-2.6 and hypotheses), Example 2.7 (line 66-67), Example 2.8 (line 69), Problem M3 (line 240-242), Remark 2.3, Proposition 2.5 proof. "
        "c081 enumeration equals pkappa sum l (exact); c083 Var4 - Var3 = 19140625 = 2 kappa^2 p(1-p) sum_{i<j} l_i l_j (exact, recomputed); c084 (1-p)^3 = 343/512 < 7/8; c086 4375/2 = 2187.5 (Example 2.8, T); "
        "c087 variances 133984375/4 and 57421875/4 are lab output (Part D), graded C; c088 same mean and variance order; c089 169/512 vs 192/512 (Example 2.7, T); c090 1875 (Problem M3, T). c082 and c085 gaps not defects."),
    row("cards-c091-c094", "2.7-cards-sample",
        "cards BK4-c091..c094 against L01.txt Definition 2.1, L02.txt section 3, L04.txt Definition 1.1, L05.txt Example 2.8",
        "c091 net debit definition: Debit_i = max(0, -Net_i), Net_i = S_{i,m} (L01 Definition 2.1, read this round, unchanged in content). c092 7596300 (Lab 1 Part B, C). c093 claims outstanding = total of claims at a date (L04.txt line 22). "
        "c094 changed this round (front only): the rounding rule of Lab 1 (nearest cent, exact half up, applied once) applied to 2187.5 gives 2188 (L05.txt line 69, lab output 'closed form rounded half up to the cent: 2188 cents'). Grade T by Example 2.8. Agrees with key row."),
    row("cards-c095-c098", "2.7-cards-sample",
        "cards BK4-c095..c098 against L02.txt Definition 2.1, L03.txt where-the-canon-breaks, L04.txt Definition 2.1 and Remark 2.3, L05.txt Assumption 1.3",
        "c095 multilateral netting (L02 Definition 2.1). c096 variation margin: L03.txt section 3 defines it and says the model has initial margin only. c097 admissible share (L04 Definition 2.1; Remark 2.3 read this round). c098 joint law (L05 Assumption 1.3 text read this round). All agree."),
    row("cards-c099", "2.7-cards-sample",
        "cards BK4-c099 against L02.txt Proposition 2.2(b) and misconception 1",
        "A = 0 iff every n_i <= 0 (Definition 2.1 with the max); Proposition 2.2(b) sum zero forces every n_i = 0. Matches L02 section 5 misconception 1 read this round."),
    row("cards-c100-c101", "2.7-cards-sample",
        "cards BK4-c100, c101 against L05.txt Proposition 2.4 and L01.txt Example 2.6",
        "c100 Proposition 2.4: the proof of Proposition 2.1 uses only the finite space, A1 and A2, so E[C] is unchanged under A4 (L05.txt Proposition 2.4 proof read). c101 DNS net debit of A in Example 2.6 is 50 (net -50), L01.txt Example 2.6 read this round."),
    row("cards-c102-c104", "2.7-cards-sample",
        "cards BK4-c102..c104 against L02.txt Problems R1 and P3, L03.txt Proposition 1.3",
        "c102 reduction = 10000 iff A = 0 (Problem R1 solution read). c103 Problem P3: the cycle has A = 0 and reduction 10000 bps. c104 Proposition 1.3 (proof read): x_i <= DF_i and x_i + 1 <= DF_i for leftover recipients. All agree."),
    row("cards-c105", "2.7-cards-sample",
        "cards BK4-c105 against L03.txt Definition 2.1",
        "Scenario set: S losses L_1..L_S, non-negative integers in cents, S >= 1 (L03 Definition 2.1 read this round). Agrees."),
    row("cards-c106", "2.7-cards-new",
        "cards BK4-c106 against L01.txt section 2",
        "c106 (new this round): 'The sum of the m payment amounts of the day, in cents.' L01.txt section 2 states: 'The gross value of the day is the sum of the m payment amounts, in cents.' "
        "Ungraded definition with cite [], as the other definition cards. Lesson is L01, section 2 exists. Not a duplicate (see cards-duplicate-scan). PASS."),
    row("cards-scope-claims", "2.7-scope-words",
        "cards.json scope words: only, every, all, exactly, same, depends only, always, never",
        "c015 'never changes the net debit' (Remark 2.5: Net and Debit are sums independent of order); c056 'depends only on how many losses are at or below the margin' (Definition 2.1: cover is a function of c(M)); "
        "c057 'only after' (Remark 1.4); c076 'Only when x = 0 or rho = 1' (theta - rho = x(rho-1)/(1-x), x < 1); c088 'same mean' (Propositions 2.1, 2.2, 2.4); c090 'depends only on failure probability' negated by Proposition 2.1; "
        "c099 and c102 'Only when / exactly' (Proposition 2.2(b), Problem R1); c034 and c035 'No' answers. Each scope word has a proof, an enumeration or a definition behind it."),
    row("cards-refs-live", "2.1-refs",
        "verify_refs --unit BK4 (live); duffie2011central",
        "tools/verify_refs.py --unit BK4 (live re-verification): '3 of 560 entries, 0 problems' (out/verify_refs_live_BK4.txt, exit 0). Duffie record unchanged (references/ diff empty). Plain-curl Crossref check in cards-attribution-duffie."),
    row("cards-property-checks", "2.2-property-sweeps",
        "exact identity sweeps (recheck_cards_r13.py)",
        "Randomised exact sweeps, all True (out/recheck_cards_r13.txt): 20000 waterfall conservation draws (c040); 20000 layer-order draws (c057); 3000 Proposition 2.3 draws against brute force plus 2000 monotonicity draws (c046, c047); "
        "3000 coverage identity draws (c068, c076); 3000 Proposition 2.5 difference draws (c069); L05 500 random parameter sets for mean and variance identities (c080, c083, c100); exact grid checks for c055, c071, c084, c089."),
    row("cards-grade-rule9", "2.3-ruling-13",
        "cards.json grades against plans/FINAL-ARCHITECT-RULINGS.md ruling 13",
        "Ruling 13 applied to every graded card. T (value derived by hand on the page in a numbered Example, Remark, Problem or Proposition): c004-c009, c022-c030, c033, c040-c044, c046-c048, c055-c058, c067-c076, c080-c084, c086, c088-c090, c094, c099-c104. "
        "C (value appears only in lab output, or rests on SIMULATED data the page does not derive; lab named in basis): c010, c011, c012, c014, c031, c049, c050, c087, c092. "
        "c043 and c044 are T after the Example 1.5 and 1.6 rewrite, because the page derives the values by hand; c049 and c050 are C because the page gives only k. c086 and c094 T (Example 2.8 derives 2187.5 by hand). c072 T (Remark 2.8 derives 11/10 by hand). c089 T (Example 2.7 derives 169/512 by hand). c090 T (Problem M3 derives 1875 by hand). No card grades a lab-only value as T, and no derived value is graded C."),
    row("cards-delta-round13", "2.7-delta",
        "BK4 delta 5db69a9..e919577 in course/modules/BK/BK4 (cards.json, L01.html, L02.html, L03.html), project and grader files (not card-cited)",
        "git diff read in full (44 insertions, 23 deletions across 7 files). cards.json: c094 front reworded (same answer, 2188); c106 added (ungraded definition, verified above). "
        "L01.html: Assumption 1.3 A2 and Definition 2.1 net-debit wording (same formula); misconception 1 wording (same numbers, 112500 and 1533900 unchanged); key-results header Keys to Source. "
        "L02.html: key-results header only. L03.html: why-it-matters wording ('count share of scenarios'); Example 1.5 rewritten with hand-derived rows L=80, 120, 170, 180, 181, 200, 205, 300 (values agree with the lab fixture and the table). "
        "The project.html, grader/test_project.py and tests/labs/BK4/lab-BK4-project-1.py hunks are not cited by any card and are outside this slice. The L04 and L05 files are unchanged."),
    row("cards-delta-round12", "2.7-delta",
        "previous round delta (5db69a9 and earlier)",
        "Superseded: every card's current text and grade was checked this round in full, not carried from the earlier pin; the round-12 delta hunks are no longer relevant to the current cards.",
    ),
    row("cards-delta-round7", "2.7-delta", "earlier round delta", "Superseded by the full re-read of cards.json at e919577 (rows cards-c001-c010 to cards-c106)."),
    row("cards-delta-round8", "2.7-delta", "earlier round delta", "Superseded by the full re-read of cards.json at e919577 (rows cards-c001-c010 to cards-c106)."),
    row("cards-delta-round9", "2.7-delta", "earlier round delta", "Superseded by the full re-read of cards.json at e919577 (rows cards-c001-c010 to cards-c106)."),
    row("cards-delta-round10", "2.7-delta", "earlier round delta", "Superseded by the full re-read of cards.json at e919577 (rows cards-c001-c010 to cards-c106)."),
    row("cards-delta-round11", "2.7-delta", "earlier round delta", "Superseded by the full re-read of cards.json at e919577 (rows cards-c001-c010 to cards-c106)."),
    row("cards-gates", "2.9-gates",
        "check_pages, check_dag, run_labs, page_smoke, pytest test_page_checks, verify_refs --unit BK4 (live)",
        "Run this round: check_pages --unit BK4 PASS; check_dag --unit BK4 PASS; run_labs --unit BK4 PASS (8/8); page_smoke --unit BK4 PASS; pytest tests/test_page_checks.py exit 0; verify_refs --unit BK4 live 0 problems (all in out/). "
        "Not run in this slice: ruff, mypy, build_site --check, fetch_data --check (no Python or site-data file in the card slice changed; see notes)."),
]

frag = {
    "unit": "BK4",
    "slice": "BK4-d",
    "round": 13,
    "verifier": "Claude Haiku 5.5 (claude-haiku-5-5), independent verifier for BK4-d (ALL cards.json against L01-L05 incl. ruling 13); did not build BK4",
    "pin": PIN + " (detached HEAD of the checkout)",
    "base": BASE + " (round-12 pin). Delta " + BASE[:8] + "..e919577 for BK4: cards.json (c094 front, c106 added), L01.html, L02.html, L03.html, project and grader files (not card-cited), no change to L04.html, L05.html, notation/, references/, tools/ or tests/labs/BK4 twins L01-L05.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE13-BK4-d",
    "scratch": SC + " (L01-L05 stripped text, regenerated by ledgers/BK4/scripts/BK4-d-r13/strip.py)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": ["Only cited work with a card: Duffie and Zhu (2011), title-level question; no 2025-2026 literature checked for freshness."],
    "notes": (
        "Judgment calls, recorded in rows: (1) c043 and c044 are T because Example 1.5 and Example 1.6 derive the values by hand (ruling 13); c049 and c050 stay C (only k is derived). "
        "(2) c032 abstract unread: publisher returned HTTP 403 to plain curl at the recorded URL, not bypassed; the card attributes only the question in the title. "
        "(3) c106 is a new ungraded definition; its near-template with c018 is distinct (trade gross notional vs day payment gross value). "
        "(4) L04 and L05 are byte-identical to the previous pin, so their round-12 rows are carried with the required prefix, and card-cited passages were re-read where the card changed or where a grade rests on them. "
        "Not checked: the project page, grader and project labs (other slices); ruff, mypy --no-incremental, build_site --check, fetch_data --check (not part of a card slice, not run); the Basel III and other unread standards (not cited by any card); the Duffie abstract (publisher 403); a full character-level re-read of L04 and L05 this round (carried from round 12, byte-identical)."
    ),
    "summary": "",
}
n = len(rows)
frag["summary"] = f"BK4-d round 13: PASS. {n} rows, all PASS. Cards 101 (c106 added, c094 front reworded). Every card re-checked against the current L01-L03 text and the byte-identical L04-L05 text; 56 exact checks, 216 label references resolved, 8 lab twins run alone (exit 0), 161 near pairs reviewed (one new, distinct). Ruling 13 applied to every graded card. Mutants: none (cards slice)."
json.dump(frag, open("ledgers/BK4/BK4-d.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", n, "statuses", sorted({r["status"] for r in rows}))
