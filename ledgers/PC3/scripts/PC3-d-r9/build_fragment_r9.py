"""Builds the round-9 verifier fragment ledgers/PC3/PC3-d.json (slice d: all cards.json against the lessons).

Every row below was produced in round 9 by reading the card and lesson text and by the scripts and outputs under
ledgers/PC3/scripts/PC3-d-r9/. No row is carried from round 8.
"""

import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE9-PC3-d")
S = "ledgers/PC3/scripts/PC3-d-r9/"

rows = [
    {
        "id": "cards-schema",
        "check": "2.7 schema and ids",
        "location": "course/modules/PC/PC3/cards.json (174 cards)",
        "status": "PASS",
        "evidence": f"{S}cards_presence_r9.out: 'cards: 174 unique ids: 174', structure PASS (keys id/lesson/front/back/cite on all; grade and basis paired; cite empty on all; known lesson on all). Ids c001-c179 with gaps at c118, c134, c152, c155 and c172 (c172 removed this round; the others were absent before).",
    },
    {
        "id": "cards-coverage",
        "check": "2.7 coverage (BUILDER_RULES 7)",
        "location": "cards.json; L01-L06.html",
        "status": "PASS",
        "evidence": "Round-9 script: every labelled block (Definition, Theorem, Proposition, Corollary, Example, Remark, Assumption) of L01-L06 is named by at least one card (13, 13, 19, 15, 13, 11 labels; no label missing). Standing assumptions A1-A6 of L04, A1-A2 of L01, A1-A2 of L02, A1-A3 of L03, A1-A5 of L06 each have a card (c002, c157, c158, c159, c160, c044, c161, c063, c162, c163, c064, c164, c171, c105, c106, c165, c166, c167).",
    },
    {
        "id": "cards-dup-scan",
        "check": "2.7 full duplicate scan",
        "location": "cards.json (all 174 front+back pairs)",
        "status": "PASS",
        "evidence": f"{S}cards_presence_r9.out: no duplicate ids; difflib front ratio > 0.8 pairs (c013/c130, c027/c028, c052/c135, c052/c136, c096/c142, c097/c145, c116/c148, c117/c150, c137-c141 family, c143/c145) each state a different fact on re-reading (different urn events, different rule, different windows, different rate or NPV point, different lab count).",
    },
    {
        "id": "cards-block-001-010",
        "check": "2.7 content vs lesson, cards PC3-c001..c010",
        "location": "L01.html Def 1.1, A1, Thm 1.2, Prop 1.3, Ex 1.4, Sec 2, Sec 5",
        "status": "PASS",
        "evidence": "c004 (Thm 1.2 back, now with product-interval sentence) matches L01 text 'The interval [prod l_i, prod u_i] is the product interval of the ranges'; c006 and c008 hypotheses match Prop 1.3 and Thm 1.2 (H1, H2, A1); c007 = 12 000 and 234 000 (20*2*300, 60*10*390); c009 grade C, figures 0.1754 / 5.9 percent and 0.9163 / 30.8 percent match Sec 5 and Lab 1 Part 2 (0.1753528875/2.9704144656 = 5.9033 %, 0.9162907319/2.9704144656 = 30.8472 %); c010 cites Sec 5 second entry.",
    },
    {
        "id": "cards-block-011-020",
        "check": "2.7 content vs lesson, cards PC3-c011..c020",
        "location": "L01.html Thm 1.5, Rem 1.6, Ex 1.7, Sec 4, R3; L02.html Rem 2.3",
        "status": "PASS",
        "evidence": f"c011 hypotheses (n>=2, x>=0, A2 for x>0) and bound match Thm 1.5 and {S}numbers_r9.out; c012 (equality at n=2) matches Rem 1.6; c015 matches Thm 1.5 (H2) and Sec 4; c016 (R3) back now writes ln(3/2) = 0.4055, equal to L01 R3 solution; c013 (1.1046221254) and c014 (1.6289, miss 0.1289, 1.5 estimate) match Lab 1 Part 3 output (lab_L01 isolated run); c017 'as in M4 Lesson 1' (M4/L01 defines finite probability space); c018 title 'Definition 2.1 (events on a finite probability space)' matches L02 Def 2.1; c019 and c020 match Def 2.2 and Rem 2.3.",
    },
    {
        "id": "cards-block-021-030",
        "check": "2.7 content vs lesson, cards PC3-c021..c030",
        "location": "L02.html Prop 2.4, Prop 2.5, Ex 2.6, Ex 2.7, Sec 4 misconceptions",
        "status": "PASS",
        "evidence": f"c021 hypotheses (A1, P(A)>0, P(B)>0) match Prop 2.4; c022 hypotheses match Prop 2.5 (A1, partition, P(A_i)>0); c023 (1/3 and 1/2; probabilities 3/4, 1/2, 1/4) hand-checked; c024 and c025 match L02 Sec 4 misconceptions and Lab 1 Part 4 output (1/3, 1/2, 1); c026-c028 (3/5, 3/5, 3/10 from 12/20 and 6/20) match Ex 2.7 and {S}lab_L02_twin_isolated_r9.out Part 4; c029 (3/4) matches Ex 2.7 and Part 4.",
    },
    {
        "id": "cards-block-031-040",
        "check": "2.7 content vs lesson, cards PC3-c031..c040",
        "location": "L02.html Ex 2.8, Sec 4, Lab 1 Part 1; L03.html Def 3.1, Prop 3.2",
        "status": "PASS",
        "evidence": f"c030 (rule A 1/3, 2/3) and c031 (rule B 1/2, 1/2; (1/3)/(2/3)=1/2) match Ex 2.8 and {S}lab_L02_twin_isolated_r9.out Part 2; c032 matches Sec 4; c033 (3/4; P(red)=1/2) matches Ex 2.9 and Part 3; c034 hypotheses match Prop 2.4 (H1); c035 (P(B)=29/100, 15/29) re-derived: (3/10)(1/2)+(7/10)(1/5)=29/100, (3/20)/(29/100)=15/29; c036 '12 of 12', lab prints 'closed form equals enumeration on 12 of 12 items'; c037 matches Ex 2.8 and Sec 3; c038 and c039 match Def 3.1 and Prop 3.2.",
    },
    {
        "id": "cards-block-041-050",
        "check": "2.7 content vs lesson, cards PC3-c041..c050",
        "location": "L03.html Ex 3.3, Def 3.4-3.7, Ass A2, Ex 3.6, Thm 3.8, Rem 3.9",
        "status": "PASS",
        "evidence": f"c040 (350) and c041 (7) match Ex 3.3 and Lab 1 Part 1 (E[X+Y]=7); c042-c044 match Def 3.4, Def 3.5, Assumption A2; c045 (250), c046 (1150/3 = 2300/6), lab_L03 Part 2 (continuation 250, value 1150/3) re-derived by numbers_r9.out; c048 matches Def 3.7; c049 hypotheses match Thm 3.8 (A1, A3, fairness at every history, rule depends on history); c050 matches Rem 3.9.",
    },
    {
        "id": "cards-block-051-060",
        "check": "2.7 content vs lesson, cards PC3-c051..c060 (card PC3-c057 omits the fairness hypothesis of Theorem 3.8)",
        "location": "cards.json line 485-492 (PC3-c057 back); course/modules/PC/PC3/L03.html line 345 (misconception 1 states 'in a fair game')",
        "status": "FAIL",
        "evidence": f"PC3-c057 back reads 'Theorem 3.8 gives expected total zero for every rule that depends only on the past.' Theorem 3.8 (L03.html Thm 3.8, H2) concludes E[W]=0 only for a FAIR game (fairness at every history). Without that hypothesis the card asserts a false general claim: {S}lab_L03_twin_isolated_r9.out Part 3b shows nonzero values for the biased game (1575/32, 575/8, 625/8, play-all 150), so a learner reading the card would conclude zero for biased games too. The lesson's own misconception 1 (L03.html line 345) carries 'in a fair game'. The other rows c051-c056, c058-c060 match their lesson text and lab output (c051 150 = 6*25; c052 1575/32; c053 zero by two methods; c054 uses A2 and N=6; c055 mean 50 from R1; c056 threshold face 3 from P3; c058 100/3; c059 mean 350 not zero; c060 (H2) fails at first turn).",
        "fix": "Edit course/modules/PC/PC3/cards.json PC3-c057 back to: 'Theorem 3.8 gives expected total zero for every stopping rule that depends only on the past, provided the game is fair at every history (H2) and the horizon is finite. A rule that looks ahead is not a stopping rule.' Then regenerate nothing (cards.json is a source file for the card deck; check_pages must still pass).",
    },
    {
        "id": "cards-block-061-070",
        "check": "2.7 content vs lesson, cards PC3-c061..c070",
        "location": "L03.html Ex 3.11, Sec 4-5; L04.html Def 1.1, A1, A2, A5, Def 2.1, Prop 2.2, Prop 2.3, Prop 3.1",
        "status": "PASS",
        "evidence": "c061 matches Ex 3.11; c062 matches Def 1.1 (q-bar = 5, bid < ask, A1, A4, A5); c063 matches A1 with p=1/2 (1/4, 1/4, 1/2); c064 matches A5 (q_t>=1 and |I|<=L, L=10); c065 matches Def 2.1; c066 hypotheses and conclusion match Prop 2.2 (H1, H2, W_N identity) and Problem E3 numbers; c068 hypotheses (Prop 2.2 and W_0=0) match Prop 2.3; c069 hypotheses (H1 to H3, A1, A2, A4, A5) match the page's Prop 3.1 (H3 now lists A5); the conclusion matches the page's formula; 'not claimed' sentence matches Prop 3.1 text.",
    },
    {
        "id": "cards-block-071-080",
        "check": "2.7 content vs lesson, cards PC3-c071..c080",
        "location": "L04.html Cor 3.3, Ex 3.2, Rem 3.4, Prop 4.1, Rem 4.2, Sec 5-6; lab_L04",
        "status": "PASS",
        "evidence": f"c070 values 5, 0, 5/2 re-derived ({S}numbers_r9.out: 5, 0, 5/2) and match Ex 3.2; c071 matches Cor 3.3 (v = a + h); c072 matches Rem 3.4; c073 matches Prop 4.1 (mean 0, variance 25 I^2); c074 (15 and 50 cents) matches Rem 4.2; c075 nine values 9980..10020 step 5 matches lab_L04 Part 2 (nine lines, 'enumeration equals the closed form on every grid point: True'); c076 matches Prop 3.1 proof (arbitrary v); c077 matches lab_L04 'fills 9 of 20 turns'; c078 matches Misconception 1 and Cor 3.3 (uninformed h/2, informed (v-a)/2 = h/2); lab_L04 Part 2 prints 0 at v=10020.",
    },
    {
        "id": "cards-block-081-090",
        "check": "2.7 content vs lesson, cards PC3-c081..c090",
        "location": "L04.html A3, Misc 4, R1, R3; L05.html Def 1.1, Def 1.3, Prop 2.1, Rem 2.2",
        "status": "PASS",
        "evidence": f"c081 matches Sec 6 misconception 4 and A3; c082 (d = (1-p)h/p = 20/3) matches R1 and {S}numbers_r9.out; c083 (|I| < 2, largest magnitude 1, variance 25; strict bound) matches R3; c084 matches Def 1.1 (six steps); c085 matches Rem 1.2; c086 matches Def 1.3; c087 (exactly (n-k+1)(k-1)) matches Prop 2.1; c088 (k = n/2+1, n^2/4) matches Rem 2.2 and numbers_r9.out (10000 at n=200, k=101).",
    },
    {
        "id": "cards-block-091-100",
        "check": "2.7 content vs lesson, cards PC3-c091..c100",
        "location": "L05.html Prop 3.2, Prop 3.3, Rem 3.4, Ex 3.5, M2, P3, Sec 5 misconceptions",
        "status": "PASS",
        "evidence": "c090 (output = window maximum; deque holds surviving indices) matches Prop 3.2; c091 (n appends, at most n removals, at most 2n tests) matches Prop 3.3; c092 (k-1 entries removed at step k) matches Rem 3.4 (trace re-run by hand); c093 (4,4,5) re-traced by hand from Ex 3.5; c094 (5,5,1,3) re-traced by hand from M2; c095 (n-1 comparisons for increasing input) matches P3; c098 and c099 match Sec 5 and Sec 4; c100 matches Sec 5 third misconception and Prop 3.2.",
    },
    {
        "id": "cards-block-101-110",
        "check": "2.7 content vs lesson, cards PC3-c101..c110",
        "location": "L05.html Lab 1 Part 2; L06.html Prop 1.1, Rem 1.2, Sec 1, Prop 2.1, Rem 2.2, Prop 3.1",
        "status": "PASS",
        "evidence": f"c101 matches lab_L05 'outputs equal for window sizes 1 to 20: True' ({S}lab_L05 run); c102 matches Prop 1.1 (both cases re-proved by hand); c103 matches Rem 1.2 (payoff form proved, price form linked); c104 defines NPV with r > -1 as in L06 Sec 1; c105 to c107 match A1, A2 (D in (0,1]) and Prop 2.1(i); c108 matches Prop 2.1(ii) and its reverse portfolio; c109 matches Rem 2.2 (S e^(r tau)); c110 (NPV(u) = -I + mAu, strictly increasing, u* = I/(mA)) matches Prop 3.1 (i) to (iii).",
    },
    {
        "id": "cards-block-111-117",
        "check": "2.7 content vs lesson, cards PC3-c111..c117",
        "location": "L06.html Prop 3.2, Cor 3.3, Ex 4.2, Rem 4.3, Lab 1 Part 2",
        "status": "PASS",
        "evidence": f"c111 matches Prop 3.2 (both ends attained); c112 matches Cor 3.3 (straddling range fixes nothing; wholly one side fixes sign); c113 five steps match Def 4.1; c114 [200, 1600] re-derived (2000*1*(1/10), 4000*2*(1/5)); c115 A = 3310/1331 re-derived; c116 break-even 8 percent 1164.10 (1164.1005) matches lab_L06 Part 2 and numbers_r9.out; c117 NPV at 200 = -16655000000/1331 = -12513148.009 displayed -12513148 (lab_L06 prints -12513148).",
    },
    {
        "id": "cards-block-119-123",
        "check": "2.7 content vs lesson, cards PC3-c119..c123",
        "location": "L06.html Lab 1 Part 1, Sec 6 misconceptions, Ex 4.2 recommendation, Rem 4.3",
        "status": "PASS",
        "evidence": f"c119 matches lab_L06 Part 1 (payoffs 0 and 100 across spot 8000 to 12000, 'payoff the same at the five spot values: True'); c120 matches Prop 2.1 and the misconception; c121 break-evens 1164.10, 1206.34, 1249.05 match lab_L06 and numbers_r9.out; c122 recommendation matches Ex 4.2; c123 sign pattern (negative at 200, positive at 1600 at 8, 10, 12 percent) matches lab_L06 sensitivity rows (-12422903 / 5616776; -12513148 / 4894816; -12598169 / 4214650).",
    },
    {
        "id": "cards-block-124-130",
        "check": "2.7 content vs lesson, cards PC3-c124..c130",
        "location": "L06.html Rem 4.3, Problem M2, M3; L01.html Ex 1.4, Ex 1.7",
        "status": "PASS",
        "evidence": f"c124 (1200 units above the 8 percent break-even 1164.10, NPV positive; numbers_r9.out) matches Rem 4.3 and Prop 3.1; c125 (500/121 = 4.13) and c126 (33275/331 = 100.53) re-derived in numbers_r9.out; c127 (margin falls to 0.7540 of 5000, fall 24.6 percent) re-derived; c128 (ln 19.5) and c129 (ln 3, ln 5, ln 1.3 sum to ln 19.5) match Ex 1.4; c130 remainder 0.0046221254 re-derived with exact fractions.",
    },
    {
        "id": "cards-block-131-135",
        "check": "2.7 content vs lesson, cards PC3-c131..c135 (c134 absent)",
        "location": "L01.html Ex 1.7, Lab 1 Part 3; L03.html Lab 1 Part 3b, Ex 3.10",
        "status": "PASS",
        "evidence": f"c131 bound 0.0048728552 re-derived (45 * 1.01^8 * 1e-4); c132 (remainder below bound) matches Thm 1.5 and lab_L01 'remainder 0.0046221254 bound 0.0048728552'; c133 bound 0.1662 re-derived (45*1.05^8*0.0025 = 0.16621) and matches lab_L01 'bound = 0.1662137374'; c135 (575/8) re-derived by recursion in numbers_r9.out and printed by lab_L03 Part 3b. c134 absent by numbering (no card removed in this round).",
    },
    {
        "id": "cards-block-136-142",
        "check": "2.7 content vs lesson, cards PC3-c136..c142",
        "location": "L03.html Lab 1 Part 3b; L04.html Lab 1 Part 1 and Sec 6 E1, E3; L05.html Lab 1 Part 1",
        "status": "PASS",
        "evidence": f"c136 (625/8) re-derived in numbers_r9.out; c137 to c140 (fills, cash -9950, inventory 1, settlement 9980, P&L 30) match lab_L04 Part 1 output (fills 9 of 20 turns; cash flow -9950; inventory 1; settlement 9980; P&L 30); c141 identity True matches lab_L04; c142 (354) matches lab_L05 Part 1 (deque comparisons = 354).",
    },
    {
        "id": "cards-block-143-150",
        "check": "2.7 content vs lesson, cards PC3-c143..c150",
        "location": "L05.html Lab 1 Parts 1-3; L06.html Lab 1 Part 2, Rem 4.3",
        "status": "PASS",
        "evidence": f"c143 (200 pushes, 199 pops) matches lab_L05 Part 1; c144 (387 within 2n = 400, largest in Part 3) matches lab_L05 Part 3 table; c145 (382) matches the window-32 row; c146 five edge-case checks all True (lab_L05 Part 2); c147 (399300/331 = 1206.34) re-derived; c148 (1249.05) re-derived (1249.0469); c149 signs at 8, 10, 12 percent match lab_L06; c150 (4894816) re-derived (4894815.93).",
    },
    {
        "id": "cards-block-151-168",
        "check": "2.7 content vs lesson, cards PC3-c151..c168",
        "location": "L06.html Problem E3; L03.html Sec 5 and Ex 3.11; L04.html Rem 1.2, A2, A4, A6, Ex 1.3; L01.html A1 and A2 (c157); L02.html A1 and A2 (c158, c159); L03.html A1 and A3 (c160, c161)",
        "status": "PASS",
        "evidence": f"c151 (21.24 per point; 84.9464/4 = 21.2366; 42.70 and 42.24) re-derived; c152 absent (removed, no gap issue); c153 and c154 match Rem 1.2 and A5; c156 (2.9704144656) matches lab_L01 Part 1; c157 matches A2 (Lagrange form, M2 Taylor theorem; M2/L08 'Taylor's Theorem with Remainder' exists); c158 to c161 match the page's A1 and A3; c162 to c164 match A2, A4, A6; c165 to c167 match A3, A4, A5 of L06; c168 (h = 10, q = 1, mid 10000 before any fill) matches Ex 1.3.",
    },
    {
        "id": "cards-block-169-171",
        "check": "2.7 content vs lesson, cards PC3-c169..c171",
        "location": "L05.html Rem 3.6; L04.html A3 (c171)",
        "status": "PASS",
        "evidence": "c169 matches Rem 3.6 (hash map has no order on values); c170 bound 3n floor(log2 n) = 4200 at n = 200 (floor(log2 200) = 7, numbers_r9.out) matches Rem 3.6; c171 matches A3 public-history wording.",
    },
    {
        "id": "cards-block-172-179",
        "check": "2.7 content vs lesson, cards PC3-c172..c179 (c172 removed this round)",
        "location": "L03.html Def 3.7, Ex 3.6, Ass A3, Rem 3.4; L04.html Sec 2, Sec 2 inventory; L05.html Def 3.1; L06.html Sec 6, Cor 3.3, Prob E2",
        "status": "PASS",
        "evidence": f"c173 (W(h) and payoff of a rule stopping at h) matches Def 3.7; c174 and c175 (fill sign, cash change c_t = -sigma_t f_t, inventory) match Sec 2 of L04; c176 matches Rem 3.4 (adverse selection); c177 title 'Definition 3.1 (the deque and its invariant)' matches L05 Def 3.1 and its content (surviving indices, increasing index front to back); c178 matches Cor 3.3 misconception; c179 (-105000000/1331 = -78888.05, negative since 1200 < 1206.34) re-derived in numbers_r9.out.",
    },
    {
        "id": "cards-block-round3-id-carry",
        "check": "2.7 id stability across rounds",
        "location": "cards.json; L01.html Prop 1.3; L04.html Rem 2.4 and Sec 3; L06.html Rem 4.3",
        "status": "PASS",
        "evidence": "Every id present in round 8 is still present with the same lesson, except c172, the only removal in this round (its content duplicates c004). No id is reassigned; c118 and c152 remain absent as in round 8. Checked by the round-9 presence script (ids unique, 174 cards).",
    },
    {
        "id": "cards-atomicity",
        "check": "2.7 one fact per card",
        "location": "cards.json (all 174 fronts and backs)",
        "status": "PASS",
        "evidence": "Re-read every front and back in round 9 (dump at ledgers/PC3/scripts/PC3-d-r9/cards_dump_r9.txt). Compound backs (for example c004, c047, c053) contain one result each with its direct consequence; no back asks the learner to combine two unrelated facts.",
    },
    {
        "id": "cards-c119-basis",
        "check": "2.7 basis for a lab result",
        "location": "cards.json PC3-c119",
        "status": "PASS",
        "evidence": "basis 'Lab 1, Part 1 (five spot states, 8000 to 12000 cents)' matches lab_L06 Part 1 output ('payoff at expiry for S_T = 8000..12000 is [0,0,0,0,0]' and [100,...]).",
    },
    {
        "id": "cards-c122-referent",
        "check": "2.7 referent of the recommendation",
        "location": "cards.json PC3-c122; L06.html Ex 4.2",
        "status": "PASS",
        "evidence": "The recommendation 'buy only if evidence puts units above 1206.34 per year at this rate, and measure units before committing' matches L06 Ex 4.2 Recommend paragraph word for word in substance.",
    },
    {
        "id": "cards-c146-grade",
        "check": "2.7 grade of a lab check",
        "location": "cards.json PC3-c146",
        "status": "PASS",
        "evidence": "grade C with basis 'Lab 1, Part 2 (finite check on one generated sequence)' is consistent with L05 Key results row ('CLab 1, Part 2 ... Proposition 3.2 is the proof for every sequence').",
    },
    {
        "id": "cards-misconception-coverage",
        "check": "2.7 misconceptions covered",
        "location": "cards.json; L01.html Sec 5 (3 entries); L02.html Sec 4 (3); L03.html Sec 5 (3); L04.html Sec 6 (4); L05.html Sec 5 (3); L06.html Sec 6 (4)",
        "status": "PASS",
        "evidence": "Each misconception entry has a card: L01 c009, c010, c014; L02 c024, c025, c032; L03 c057, c058, c061; L04 c078, c079, c080, c081; L05 c098, c099, c100; L06 c120, c121, c123, c178 (plus c125-c127 as problems). c057 is cited in the FAIL row above.",
    },
    {
        "id": "cards-number-presence",
        "check": "2.7 every card number appears in its lesson",
        "location": "cards.json; L01-L06 text dumps",
        "status": "PASS",
        "evidence": f"{S}cards_presence_r9.out: 4 tokens not matched by the automated plain-text search; each is present in the lesson in TeX form: 29/100 and 15/29 (L02 M2: \\tfrac{{29}}{{100}}, \\tfrac{{15}}{{29}}), 2300/6 (L03 Ex 3.6: \\frac{{2300}}{{6}}), 2/4 (L05 Rem 2.2: \\tfrac{{n^{{2}}}}{{4}}).",
    },
    {
        "id": "cards-lab-printed-values",
        "check": "2.7 lab-printed values on cards",
        "location": "tests/labs/PC3/lab-PC3-L01..L06-1.py run in isolation; course/modules/PC/PC3/L01..L06.html",
        "status": "PASS",
        "evidence": f"Each twin run with python -I -W error exits 0 ({S}lab_L0*_twin_isolated_r9.out). Printed values on cards match: L01 (1.1046221254, 0.0046221254, 0.0048728552, 0.1662, 2.9704144656, 12 000 and 234 000 product bounds); L02 (12 of 12, 1/3, 1/2, 1, 3/5, 3/10, 3/4, 2/3, 1/2); L03 (7, 1150/3, 1575/32, 575/8, 625/8, 150); L04 (9 fills, -9950, 1, 9980, 30, 2500, nine grid values); L05 (1351, 354, 200 pushes, 199 pops, 5239, 382, 387, 350, 197); L06 (3310/1331, 399300/331, -12513148, 4894816, 1164.10, 1206.34, 1249.05, 0 and 100 payoffs).",
    },
    {
        "id": "cards-rederive",
        "check": "2.2 numbers on cards re-derived",
        "location": f"{S}numbers_r9.py and numbers_r9.out",
        "status": "PASS",
        "evidence": f"Round-9 script {S}numbers_r9.py re-derived every numeric card value independently (exact fractions and float), including ln 19.5, the factor widths, the three narrowing reductions and their shares 30.8472 and 5.9033 percent, the Taylor remainder and bound at n=10 for x=0.01 and 0.05, the Monty Hall probabilities, the bias-game stopping values, the reroll value 1150/3, the L04 trade terms, the L05 naive counts, and the L06 annuity factor 3310/1331, break-evens and NPVs at 8, 10, 12 percent. Every value matched its card or lesson sentence. (The one mismatch in the script, an M2 NPV line, was a bug in the script itself; the lesson value 500/121 was re-derived by hand.)",
    },
    {
        "id": "gates-structural",
        "check": "2.9 structure gates for PC3 (checkout c93dd52)",
        "location": "tools/check_pages.py, check_dag.py, check_projects.py, page_smoke.py, run_labs.py, verify_refs.py --offline, pytest -k PC3, ruff on tests/labs/PC3",
        "status": "PASS",
        "evidence": f"check_pages --unit PC3: 'check_pages PC3: PASS'; check_dag --unit PC3: PASS; check_projects --unit PC3: PASS; page_smoke PC3 on the six lesson pages: PASS; run_labs --unit PC3: PASS (9/9); pytest -k PC3: all passed; verify_refs --offline: 560 entries, 0 problems; ruff check and ruff format --check on tests/labs/PC3: clean. Outputs under {S}.",
    },
    {
        "id": "cards-grade-agreement",
        "check": "2.3 grades on cards vs lesson key-results tables",
        "location": "cards.json; L01-L06 key-results tables",
        "status": "PASS",
        "evidence": "Every key-results row graded T in the lesson has a T card (for example L03 Thm 3.8 -> c049 T; L04 Prop 3.1 -> c069 T; L06 Prop 3.2 -> c111 T). Every row graded C (lab results) has a C card (c047, c053, c075, c101, c146 are C; L02 drill set c036 C). c124 and c148, c149 are C where the lab prints the value, which is conservative and acceptable; c151 is T because it is a hand computation from the closed form.",
    },
    {
        "id": "cards-c013-exact-value",
        "check": "2.2 exact value on card c013",
        "location": "cards.json PC3-c013; L01.html Ex 1.7 and Lab 1 Part 3",
        "status": "PASS",
        "evidence": "(1.01)^10 = 1.104622125411... ; 1.1046221254 to ten places (numbers_r9.out: 1.104622125411). Lesson text and lab_L01 Part 3 print 1.1046221254.",
    },
    {
        "id": "adjacent-lesson-numbers",
        "check": "2.7 cross-references to adjacent lesson numbers",
        "location": "cards.json PC3-c017, c020, c043; L02.html Def 2.1 and Rem 2.3",
        "status": "PASS",
        "evidence": "c017 'as in M4 Lesson 1' and c020 (M4 conditional distribution) point at course/modules/M/M4/L01.html (finite probability space) and M4/L04.html (conditional distribution, 4 occurrences); c043 cites Lesson 2 Definition 2.2 which exists in L02.html.",
    },
    {
        "id": "lesson-L02-introduces-metadata",
        "check": "2.9 'Introduces' metadata of L02",
        "location": "course/modules/PC/PC3/L02.html l.38",
        "status": "PASS",
        "evidence": "L02 'Introduces: conditional probability (Definition 2.2), Bayes' rule (Proposition 2.4) and the law of total probability (Proposition 2.5)' matches the labelled blocks of L02 and check_dag PASS.",
    },
    {
        "id": "cards-process-words",
        "check": "2.9 no process words in learner text",
        "location": "cards.json; L01-L06.html visible text",
        "status": "PASS",
        "evidence": "Round-9 regex scan of cards and visible lesson text for verif, builder, agent, round N, ledger, audit, reviewer, draft, TODO, corrected, fragment, ruling, renamed: only hit is L02 E1 'Verify it by counting the complement' (an exercise instruction) and L06 'no longer determines' (a modelling statement).",
    },
    {
        "id": "cards-simulated-label",
        "check": "2.8 SIMULATED label on simulated results",
        "location": "cards.json PC3-c067, c077, c137-c141; L04.html Lab 1 header",
        "status": "PASS",
        "evidence": "Every seed-0 and seed-1 card of L04 carries grade C and basis 'Lab 1, Part 1 (... SIMULATED ...)'; the lab header says SIMULATED; c067 says SIMULATED in its basis.",
    },
    {
        "id": "cards-notation",
        "check": "2.4 notation vs notation/notation.json",
        "location": "notation/notation.json (8 registered symbols and the registered macro table); cards.json; L01-L06.html",
        "status": "PASS",
        "evidence": "Registered macros used in PC3 pages: \\Prob, \\E, \\R, \\indic, \\Var (all registered with their meanings). No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) appears in PC3 cards or pages. Note (not a FAIL): L01 Definition 1.1 uses plain italic Q for a quantity, which is a different glyph from the registered \\mathbb{Q} (risk-neutral measure); no reuse of the registered macro.",
    },
    {
        "id": "cards-block-titles",
        "check": "2.7 block titles named on cards",
        "location": "cards.json PC3-c018, c089, c177; L02.html l.57; L05.html l.106, l.157",
        "status": "PASS",
        "evidence": "c018 'Definition 2.1 (events on a finite probability space), equally likely case' extends the title with the lesson's own Def 2.1 title; c089 and c177 'Definition 3.1 (the deque and its invariant)' match the L05 Def 3.1 title; c066, c068, c069, c071, c102, c110 titles match the lesson block titles (round-9 check). No title is invented.",
    },
    {
        "id": "lesson-numbers-prose",
        "check": "2.2 prose numbers in lessons read by the cards (defect classes 1, 4, 7, 8)",
        "location": "L01.html Ex 1.4, Ex 1.7, Sec 2, Sec 5, E1-E3, R1; L02.html Ex 2.6-2.9, E1, M2, R3; L03.html Ex 3.6, 3.10, E2, R1, R2; L04.html Ex 3.2, Rem 4.2, R1, R3, E2, E3; L05.html Rem 2.2, Rem 3.6, E1-E3; L06.html Ex 4.2, Rem 4.3, Sec 6, E1-E3, R1, R3",
        "status": "PASS",
        "evidence": f"Every prose number in these sections was re-derived in {S}numbers_r9.out with exact fractions (or 10-digit floats where the lesson prints a log or root): 0.4055, 0.9163, 30.8 and 5.9 percent (E2 full precision 30.8472 and 0.0590); 0.9485 (0.948546); 0.054 (5.425 percent over remainder); 7.9 percent (7.913); 2.8034 and 0.167054; 1.4852 and 1.6094; 149/2 and 100/3; 625/8 minus 150 = -575/8 = -71.875; 0.1118 and 1.34 standard errors; 20/3 cents; 42.24 and 42.70 unrounded differences; 21.24 per point; 24.6 percent margin fall at 0.7540; -78888.05 and 1550000000/1331 = 1164537.94. The lesson's rounding claim that 0.9163/2.9704 = 0.3085 'would display as 30.9 percent' is arithmetic on the four-place values and is consistent (30.85 at two places, 30.9 with half-up); the full-precision share is 30.8 (30.847). No mismatch found.",
    },
    {
        "id": "lesson-scope-words",
        "check": "2.2 scope words (only, all, every, exactly, always) on cards and lesson claims (defect class 4)",
        "location": "cards.json; L01-L06.html",
        "status": "PASS",
        "evidence": "Scope words in cards were listed and each is backed by a proof or a stated hypothesis on the page (for example 'every fair value v' c076 by the arbitrary-v proof; 'exactly n appends' c091 by Prop 3.3; 'Switching wins exactly when the first pick is a goat' c030 by Ex 2.8). The one exception, c057, is the FAIL row above.",
    },
    {
        "id": "lesson-dag-and-attribution",
        "check": "2.5 cross-module attributions and DAG (defect classes 3, 14)",
        "location": "L01.html (M1, M2 references); L02.html (M4 Lesson 1, M4 conditional distribution); L03.html (M4 expectation); check_dag output",
        "status": "PASS",
        "evidence": "M1/L03 'Exponential and Logarithm Functions' exists (cited for ln); M2/L08 'Taylor's Theorem with Remainder' exists (cited for A2); M4/L01 defines finite probability spaces; M4/L02 'Expectation and Variance'; M4/L04 'Independence and Conditional Expectation (Elementary)' contains 'conditional distribution'. check_dag --unit PC3: PASS, so no concept is used outside the prerequisite closure in the pages.",
    },
]

fragment = {
    "unit": "PC3",
    "slice": "PC3-d",
    "round": 9,
    "verifier": "Claude Haiku 5.5, independent verifier, slice d (ALL cards.json against the lessons), round 9; did not build PC3",
    "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885",
    "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (round-8 pin; round-8 fragment /Users/billyribeiro/.fanout/frags/E-PC3-d.round8.json, read as context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE9-PC3-d",
    "scratch": "/tmp/pc3d_r9 (lesson text dumps, cards dump, lab outputs); durable scripts and outputs under ledgers/PC3/scripts/PC3-d-r9/",
    "verified_at": "2026-11-04T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d is cards.json against the six lessons. No grader, lab code or reference is in the slice; no grader mutants "
        "were written (mutants belong to the project slices). The delta since the round-8 pin (0dee921a..c93dd526) touched "
        "cards.json (c004, c008, c016, c018, c066, c068, c069, c071, c073, c076, c089, c102, c110, c172 removed, c177), "
        "L02, L04, L05, L06 text, lab twins L04 and L05, and project files; every card was re-read against the current "
        "lesson text in this round, and no round-8 PASS row is carried. Cards in the delta match their current lesson text. "
        "One FAIL: PC3-c057 back states Theorem 3.8's zero conclusion without the fairness hypothesis (see cards-block-051-060). "
        "Not run in this slice: mypy --no-incremental (no Python tool or reference changed; the L04 and L05 twins were checked "
        "by run_labs, isolated execution, pytest -k PC3 and ruff), full pytest suite, page_smoke across the project and hub pages "
        "(only the six lessons were smoke-tested), and check_pages/check_dag/check_projects for other units. Verdict is FAIL because "
        "one row is FAIL."
    ),
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": 0,
        "mutants": 0,
        "mutants_killed": 0,
    },
}

out_path = ROOT / "ledgers/PC3/PC3-d.json"
out_path.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n")
print("wrote", out_path, fragment["summary"])
