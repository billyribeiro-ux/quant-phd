"""Writes the round-10 verifier fragment for PC3 slice d (all cards.json against the six lessons).

Run from the checkout root: .venv/bin/python -I ledgers/PC3/scripts/PC3-d-r10/write_fragment_r10.py
"""

import json
from datetime import UTC, datetime

CK = "/Users/billyribeiro/.fanout/wt/verifyE10-PC3-d"
SCR = "ledgers/PC3/scripts/PC3-d-r10"
OUT = "/tmp/pc3d_r10"

P = "PASS"
F = "FAIL"


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    return r


rows = [
    row(
        "cards-schema",
        "2.7 schema and ids",
        "course/modules/PC/PC3/cards.json (174 cards)",
        P,
        "python -I json load: 174 cards, 174 unique ids, ids PC3-c001..c179 with gaps 118, 134, 152, 155, 172 (no id reused; "
        "gaps are the round-8/9 removals, unchanged this round). Every card has id, lesson (L01..L06), front, back, cite, grade, basis. "
        "Lesson counts from the same load: L01 24, L02 23, L03 29, L04 37, L05 26, L06 35.",
    ),
    row(
        "cards-coverage",
        "2.7 coverage (BUILDER_RULES 7)",
        "cards.json; L01-L06.html",
        P,
        "Every lesson has cards for its definitions, assumptions, propositions, theorems, corollaries, remarks, worked examples, problems "
        "and misconception entries (see the block rows below, each naming the lesson items it covers). No lesson has zero cards.",
    ),
    row(
        "cards-dup-scan",
        "2.7 full duplicate scan",
        "cards.json (all 174 front+back pairs)",
        P,
        "python: Counter over fronts and over backs gives no value above 1; no duplicate id; no duplicate (front, back) pair.",
    ),
    row(
        "cards-block-001-010",
        "2.7 content vs lesson, cards PC3-c001..c010",
        "L01.html Def 1.1 (l.59), A1 (l.64), Thm 1.2 (l.70-73), Prop 1.3 (l.87-89), Ex 1.4 (l.99), Sec 2 (l.105), Sec 5 (l.327-332)",
        P,
        "Re-read against the current L01.html (l.37-38 meta changed only in wording 'module M1'; card text unaffected). c001 ends = bounds of Thm 1.2 (l.59); "
        "c002 range is estimator's choice (l.64); c003 ln(u/l) (l.89); c004 both bounds attained (l.73); c005 no joint assumption, Sec 4 and R2 (l.82, l.318, l.438); "
        "c006 sum of log-widths (l.89); c007 12000 and 234000 (l.99, 20*2*300, 60*10*390); c008 drop equals factor's own width (l.105); "
        "c009 0.1754 = 5.9 percent of 2.9704 and 0.9163 = 30.8 percent (L01.html l.107, l.328; printed Part 2 at l.298-300); "
        "c010 Thm 1.2 assigns no probability (l.82, l.332). Numbers re-derived in ledgers/PC3/scripts/PC3-d-r10/rederive_r10.py.",
    ),
    row(
        "cards-block-011-020",
        "2.7 content vs lesson, cards PC3-c011..c020",
        "L01.html Thm 1.5 (l.121-125), Rem 1.6 (l.135), Ex 1.7 (l.140-141), Sec 4 (l.318-319), R3 (l.445-447); L02.html Rem 2.3 (l.72)",
        P,
        "c011 bound n(n-1)/2 (1+x)^(n-2) x^2 with A2 for x>0 (l.123, l.125, l.130); c012 n=2 equality (l.135); c013 (1.01)^10 = 1.1046221254, exact 1.10462212541 (l.140); "
        "c014 estimate 1.5, exact 1.6289, miss 0.1289 (l.141, l.336); c015 x>=0 only, bound grows (l.319); c016 R3 ln(3/2)=0.4055, ln(2.5/1.01)=0.9063, "
        "widths 1.0986 and 0.9163 (l.447; recomputed in rederive_r10.txt); c017 event and P(A) as M4 Lesson 1 (l.57); c018 equally likely (l.57); c019 Def 2.2 (l.67); "
        "c020 Remark 2.3 (l.72). All numbers re-derived.",
    ),
    row(
        "cards-block-021-030",
        "2.7 content vs lesson, cards PC3-c021..c030",
        "cards.json line 186 (PC3-c022 basis); L02.html Prop 2.4 (l.76-80), Prop 2.5 (l.89-94), Proof of Prop 2.5 (l.99), Ex 2.6 (l.111), Ex 2.7 (l.116-117), Sec 4 (l.377-386)",
        F,
        "PC3-c022 front and back now use C_1..C_m and P(C_i) (cards.json l.182-183, matching L02.html l.91-94 and l.99), and they agree with the lesson. "
        "But its basis field (cards.json line 186) still reads 'proof on the page (B is the disjoint union of the sets B ∩ A_i)'. The proof on the current page "
        "reads B ∩ C_i (L02.html l.99), and grep finds no A_i in any PC3 lesson or card. The round-10 rename to C_i left this locator behind. "
        "Other card checks in this block PASS: c021 hypotheses match Prop 2.4 (l.78); c023 1/3, 1/2 (l.111); c024-c025 match Sec 4 (l.382-386); "
        "c026-c029 3/5, 3/5, 3/10, 3/4 (L02.html l.116-117; printed l.355-358); c030-c031 1/3, 2/3, 1/2 (l.50-52).",
        "In cards.json line 186, change the basis text 'B ∩ A_i' to 'B ∩ C_i'. Front, back and id stay as they are. Re-run the card-number and notation checks.",
    ),
    row(
        "cards-block-031-040",
        "2.7 content vs lesson, cards PC3-c031..c040",
        "L02.html Ex 2.8 (l.122-124), Sec 4 (l.377-379), Lab 1 Part 1 (l.134, l.218-231); L03.html Def 3.1 (l.62), Prop 3.2 (l.68-70)",
        P,
        "c031 rule B conditional 1/2 with goat-event 2/3 (l.124); recomputed by enumeration; c032 misconception (l.378); c033 Ex 2.9 values 3/4 and P(red)=1/2 (l.129); "
        "c034 hypotheses A1, P(A)>0, P(B)>0 (l.78); c035 P(B)=29/100 and 15/29 (l.408); c036 12 of 12 from the printed L02.html block (l.340); c037 rule dependence (l.122-124, Sec 3 l.366); "
        "c038 E[X]=sum X p (l.62); c039 Prop 3.2 (l.68-70).",
    ),
    row(
        "cards-block-041-050",
        "2.7 content vs lesson, cards PC3-c041..c050",
        "L03.html Ex 3.3 (l.80), Def 3.4-3.7 (l.87-109), A2 (l.97), Ex 3.6 (l.102-104), Thm 3.8 (l.299-303), Rem 3.9 (l.316)",
        P,
        "c040 350 (l.80); c041 7 (l.80); c042 Def 3.4 (l.87); c043 Def 3.5 (l.92); c044 A2 (l.97); c045 250 = 350-100 (l.102); c046 1150/3 = 2300/6 and 383.33 (l.103-104); "
        "c047 best of 64 policies = 1150/3 (L03.html printed l.269); c048 Def 3.7 stops at length N (l.109); c049 Thm 3.8 hypotheses A1 and A3 (l.299), fairness (l.300), history (l.301), conclusion E[W]=0 (l.303); "
        "c050 Rem 3.9 (l.316).",
    ),
    row(
        "cards-block-051-060",
        "2.7 content vs lesson, cards PC3-c051..c060 (round-9 FAIL on c057 re-verified)",
        "cards.json lines 485-492 (PC3-c057); L03.html Thm 3.8 (l.299-301); L03.html Ex 3.10 (l.321-322), Ex 3.6 (l.102-104), Ex 3.11 (l.327), misconception 1 (l.345)",
        P,
        "The round-9 FAIL was c057 omitting the fairness hypothesis. c057 back now reads 'in a fair game over a finite horizon: the horizon is finite (H1), the game is fair at every history "
        "of fewer than N turns with positive probability (H2), and the rule depends only on the history (H3)'. This matches Thm 3.8 hypotheses at L03.html l.299 (H1), l.300 (H2), l.301 (H3). "
        "c051 150 cents, 25 per turn, 6*25 (l.322); c052 1575/32 and c053 zero for each of five rules (L03.html printed l.273-285, recomputed by independent enumeration: "
        "fair 0, biased 150, 1575/32, 1575/32, 575/8, 625/8). c054 Thm 3.8 applies to the fair game over N=6 (l.321). c055 R1 mean 50 from paths 200, 100, 0, -100 (l.267). "
        "c056 faces 1 and 2 reroll, threshold 3 (l.407). c058 100/3 (l.104). c059 stop payoff mean 350 (l.336). c060 (H2) fails at the first turn (R2 solution l.450).",
    ),
    row(
        "cards-block-061-070",
        "2.7 content vs lesson, cards PC3-c061..c070",
        "L03.html Ex 3.11 (l.327); L04.html Def 1.1 (l.59-65), A1 (l.72), A2 (l.73), A5 (l.76), Def 2.1 (l.97), Prop 2.2 (l.102), Prop 2.3 (l.112), Prop 3.1 (l.129-137), Ex 3.2 (l.143)",
        P,
        "c061 Ex 3.11 two outcomes (l.327, text re-read after round-10 wording change); c062 Def 1.1 quoted sizes {0..5} with q-bar=5 (L04.html l.63), same set as the round-9 text, now written out; "
        "c063 A1 probabilities 1/4, 1/4, 1/2 (l.72); c064 A5 fill test q_t>=1 and |I|<=L with L=10 (l.76); c065 W_t = C_t + I_t v_t, settlement v_N (l.97); "
        "c066 Prop 2.2 hypotheses and conclusion (l.102); c067 Remark 2.4 and Problem E3: 9990 mid, 9980 settlement, 40 vs 30 cents (l.122; E3 l.580-582); "
        "c068 Prop 2.3 decomposition (l.112); c069 Prop 3.1 formula, hypotheses H1-H3 (l.129-137; proof l.138 re-derived term by term); c070 Ex 3.2 values 5, 0, 5/2 (l.143).",
    ),
    row(
        "cards-block-071-080",
        "2.7 content vs lesson, cards PC3-c071..c080",
        "L04.html Cor 3.3 (l.148-153), Ex 3.2 (l.143), Rem 3.4 (l.158), Prop 4.1 (l.165-170), Rem 4.2 (l.175), Sec 5-6 (l.339-349); L04.html printed Part 1 block (l.445-457)",
        P,
        "c071 v = a+h, h/2-(v-a)/2 (l.153); c072 (1-p)h, a quarter of 2h (l.158); c073 mean 0 and variance 25 I^2 (l.170); c074 sd 15 and 50 cents (l.175); "
        "c075 nine fair values 9980..10020 step 5, lab output 'enumeration equals closed form on every grid point: True' (L04.html printed l.468); "
        "c076 closed form for every v, lab checks nine values (l.200); c077 9 fills (L04.html printed l.445); c078 expected trade term zero at v=a+h (l.233-234 of card; l.153); "
        "c079 M1 P&L 10 cents (L04.html l.516-518); c080 variance 2500 at I=10 (L04.html printed l.474).",
    ),
    row(
        "cards-block-081-090",
        "2.7 content vs lesson, cards PC3-c081..c090",
        "L04.html A3 (l.74), Misc 4 (l.349), R1 (l.593), R3 (l.605-607); L05.html Def 1.1 (l.58-65), Def 1.3 (l.78), Prop 2.1 (l.87), Rem 2.2 (l.97)",
        P,
        "c081 A3 public history (l.74); c082 d=(1-p)h/p=20/3 at p=3/5, h=10 (l.593, l.605-607 numbers re-derived); c083 variance < 100 gives |I|<2, largest 1, variance 25 (l.607); "
        "c084 six steps in order (l.60-65); c085 Rem 1.2 no time fixed (l.71); c086 Def 1.3 entries n-k+1 (l.78); c087 Prop 2.1 (n-k+1)(k-1) (l.87-92); "
        "c088 Rem 2.2 k=n/2+1, count n^2/4 (l.97).",
    ),
    row(
        "cards-block-091-100",
        "2.7 content vs lesson, cards PC3-c091..c100",
        "L05.html Def 3.1 (l.106), Prop 3.2 (l.125-127), Prop 3.3 (l.137-141), Rem 3.4 (l.147), Ex 3.5 (l.152), M2 (l.376-378), P3 (l.407-410), Sec 5 misconceptions (l.347-356)",
        P,
        "c089 surviving index (l.106); c090 Prop 3.2 output and deque order (l.125-130); c091 Prop 3.3 counts n, n, 2n (l.137); c092 Rem 3.4 all k-1 removed (l.147); "
        "c093 Ex 3.5 output (4,4,5) (l.152); recomputed; c094 M2 output (5,5,1,3) (l.378); c095 P3 n-1 (l.410); c096 1351 = 193*7 (L05.html printed l.312); "
        "c097 5239 = 169*31 (L05.html printed l.330); c098 total at most 2n (l.339, l.348); c099 counts are not run times (l.352); c100 Prop 3.2 is the proof for every sequence (l.356).",
    ),
    row(
        "cards-block-101-110",
        "2.7 content vs lesson, cards PC3-c101..c110",
        "L05.html Lab 1 Part 2 (l.176-177, l.319); L06.html Prop 1.1 (l.59-65), Rem 1.2 (l.70), Sec 1 (l.73), Prop 2.1 (l.91-102), Rem 2.2 (l.103), Prop 3.1 (l.112-117)",
        P,
        "c101 True for window sizes 1 to 20 on seed 5 (L05.html printed l.319); c102 (s-K)+ - (K-s)+ = s-K (l.60, proof l.65); c103 Rem 1.2 payoff form (l.70); "
        "c104 NPV formula (l.73); c105 A1 (l.82); c106 A2 (l.83); c107 Prop 2.1(i) portfolio pays F'-S/D (l.92, proof l.97); c108 Prop 2.1(ii) hypotheses A4, A5 (l.92, l.98); "
        "c109 Rem 2.2 S e^(r tau) (l.103); c110 Prop 3.1 NPV(u) = -I + mAu, u* = I/(mA) (l.112, proof l.117).",
    ),
    row(
        "cards-block-111-117",
        "2.7 content vs lesson, cards PC3-c111..c117",
        "L06.html Prop 3.2 (l.122-127), Cor 3.3 (l.132-137), Ex 4.2 (l.149), Rem 4.3 (l.154), Lab 1 Part 2 (L06.html printed l.297); annuity A (l.149)",
        P,
        "c111 Prop 3.2 bounds and attained ends (l.122, l.127); c112 Cor 3.3 straddle (l.132, l.137); c113 Def 4.1 five steps (l.144); c114 [200,1600] (l.149); "
        "c115 A = 3310/1331 at 10 percent (recomputed, 1/1.1+1/1.21+1/1.331); c116 about 1164.10 at 8 percent (rederive_r10.txt: 1164.1005); "
        "c117 -12513148 cents, exact -16655000000/1331 (L06.html printed l.297; recomputed -12513148.009).",
    ),
    row(
        "cards-block-119-123",
        "2.7 content vs lesson, cards PC3-c119..c123",
        "L06.html Lab 1 Part 1 (l.159, printed l.286-289), Prop 2.1 (l.92-98), Rem 4.3 (l.154), Lab 1 Part 2 (printed l.301-303), Ex 4.2 (l.149), Cor 3.3 (l.132-137)",
        P,
        "c119 payoffs 0 at 10000 and 100 at 10100 across five spot states, check True (L06.html printed l.286-288); c120 S/D uses no expectation (l.319 misconception); "
        "c121 break-evens 1164.10, 1206.34, 1249.05 (printed l.301-303); c122 buy only if units above 1206.34 (l.149 and l.63); "
        "c123 NPV sign negative at 200 and positive at 1600 at 8, 10, 12 percent (printed l.301-303 and l.297-298).",
    ),
    row(
        "cards-block-124-130",
        "2.7 content vs lesson, cards PC3-c124..c130",
        "L06.html Rem 4.3 (l.154), Prop 3.1 (l.112-117), M2 (l.351-353), M3 (l.358-360), R3 (l.435-436); L01.html Ex 1.4 (l.99), Ex 1.7 (l.140)",
        P,
        "c124 NPV at 1200 units and 8 percent is positive (recomputed +462582 cents, and 1200 > 1164.10); c125 M2 500/121 (l.353); c126 M3 33275/331 = 100.53 (l.360); "
        "c127 R3 margin 0.7540, fall 24.6 percent (l.435-436; recomputed 0.75397, 24.60 percent); c128 ln 19.5 = 234000/12000 (l.99); c129 ln 3, ln 5, ln 1.3 sum to ln 19.5 (l.99).",
    ),
    row(
        "cards-block-131-135",
        "2.7 content vs lesson, cards PC3-c131..c135 (c134 absent)",
        "L01.html Ex 1.7 (l.140-141), Thm 1.5 (l.125), Lab 1 Part 3 (L01.html printed l.306-307); L03.html Lab 1 Part 3b (L03.html printed l.282-285), Ex 3.10 (l.322)",
        P,
        "c130 remainder 0.0046221254 (L01.html printed l.306); c131 bound 0.0048728552 = 45*(1.01)^8*0.0001 (recomputed 0.00487285518); c132 remainder below bound (L01.html printed l.308); "
        "c133 bound 0.1662 above exact miss 0.1289 (L01.html printed l.307); c135 575/8 (L03.html printed l.285); the gap at c134 is intentional and not referenced by any row.",
    ),
    row(
        "cards-block-136-142",
        "2.7 content vs lesson, cards PC3-c136..c142",
        "L03.html printed Part 3b (l.281-285), Ex 3.10 (l.322); L04.html Lab 1 Part 1 printed block (l.445-457), Sec 6 E1 (l.568), E3 (l.580-582)",
        P,
        "c136 625/8 (L03.html printed l.285); c137 cash flow -9950 (L04.html printed l.446); c138 final inventory 1 (printed l.447); c139 settlement 9980 at v_20 (printed l.448); c140 P&L 30 (printed l.450); "
        "c141 identity True (printed l.451); c142 deque comparisons 354 at window 8 (L05.html printed l.313). Seed-0 path re-simulated independently in this checkout: 9 fills, -9950, 1, 9980, 30, 13 informed.",
    ),
    row(
        "cards-block-143-150",
        "2.7 content vs lesson, cards PC3-c143..c150",
        "L05.html Lab 1 Part 1 (L05.html printed l.313), Part 3 (printed l.327-331), Prop 3.3 (l.137-141); L06.html Problem E3 (l.410), Rem 4.3 (l.154), Lab 1 Part 2 (printed l.301-303)",
        P,
        "c143 200 pushes, 199 pops (L05.html printed l.313); c144 387 (largest of Part 3 rows) within 2n=400, pops 194 (L05.html printed l.331, recomputed); c145 382 (L05.html printed l.330); "
        "c146 five edge checks True (L05.html printed l.320-324); c147 399300/331 = 1206.34 (l.149 derivation); c148 1249.05 at 12 percent (l.154, rederive 1249.0469); "
        "c149 negative at 200, positive at 1600 at all three rates (L06.html printed l.297-303); c150 4894816 cents (L06.html printed l.298, recomputed 4894815.93).",
    ),
    row(
        "cards-block-151-168",
        "2.7 content vs lesson, cards PC3-c151..c168",
        "L06.html Problem E3 (l.410), Problem E2 (l.403), Rem 1.2 (L04 l.37), A2/A4/A6 (L04 l.31, l.33, l.35), Ex 1.3 (L04 l.39); L01.html A1 and A2 (l.64, l.115); L02.html A1, A2 (l.62, l.106); L03.html A1, A3 (l.23, l.193); L06.html Problem E3 solution",
        P,
        "c151 21.24 per point from unrounded 1249.0469 and 1164.1005, (1249.0469-1164.1005)/4 = 21.2366 (L06 l.410, recomputed 21.2366); c152 absent; c153 Rem 1.2 constants are model choices (L04 l.37); "
        "c154 Rem 1.2 a fill is always one unit (L04 l.37, l.76); c155 absent; c156 2.9704144656 (L01.html printed l.288); c157 A2 Lagrange form (L01 l.115); c158 A1 finite space (L02 l.62); "
        "c159 A2 1/4 each (L02 l.106); c160 A1 finite and integer cents (L03 l.23); c161 A3 finite horizon and fairness (L03 l.292-293); c162 A2 fair path (L04 l.31); "
        "c163 A4 informed trader (L04 l.33); c164 A6 quote form (L04 l.35); c165 A3 no costs (L06 l.84); c166 A4 no arbitrage (L06 l.85); c167 A5 short sale (L06 l.86); "
        "c168 Ex 1.3 mid 10000 before fill, h=10, q=1 (L04 l.39).",
    ),
    row(
        "cards-block-169-171",
        "2.7 content vs lesson, cards PC3-c169..c171",
        "L05.html Rem 3.6 (l.157-158); L04.html A3 (l.74) and Sec 2 inventory (l.56, l.41)",
        P,
        "c169 hash map keeps no order (l.157); c170 heap bound 3n floor(log2 n) = 4200 at n=200 (l.158, 3*200*7); c171 A3 public history, not v_t (L04 l.74).",
    ),
    row(
        "cards-block-172-179",
        "2.7 content vs lesson, cards PC3-c172..c179 (c172 removed; c173-c179 present)",
        "L03.html Def 3.7 (l.109), Def 3.5 (l.92), A3 (l.292-293), Rem 3.4 (l.316), Ex 3.6 (l.102-104); L04.html Sec 2 (l.41, l.56); L05.html Def 3.1 (l.106); L06.html Sec 6 misconception (l.327-330), Cor 3.3 (l.132-137), Problem E2 (l.403)",
        P,
        "c173 W(h) and stop pays W(h) (l.109); c174 sigma sign and c_t = -sigma f (L04 l.41); c175 I_0=0 and inventory sign convention (L04 l.56, l.41); c176 adverse selection as used (L04 l.70); "
        "c177 deque after step i (L05 l.106); c178 bounds do not fix sign (L06 l.132-137, l.327-330 with L06.html printed l.297-298); c179 -105000000/1331 = -78888.05, below 1206.34 (L06 l.403; recomputed -78888.054).",
    ),
    row(
        "cards-block-round3-id-carry",
        "2.7 id stability across rounds",
        "cards.json; L01.html Prop 1.3 (l.87); L04.html Rem 2.4 (l.122) and Sec 3 (l.125-128); L06.html Rem 4.3 (l.154)",
        P,
        "Ids c001..c179 are unchanged from round 9; no id renumbered; gaps match the round-9 removals. The card whose id changed content this round (c022, c057, c062) kept its id.",
    ),
    row(
        "cards-atomicity",
        "2.7 one fact per card",
        "cards.json (all 174 fronts and backs)",
        P,
        "Each card tests one fact. Multi-part answers (c057 hypotheses H1-H3, c084 six steps, c113 five steps, c069 formula with hypotheses) are one result with its listed parts, not separate facts.",
    ),
    row(
        "cards-c119-basis",
        "2.7 basis for a lab result",
        "cards.json PC3-c119; L06.html Lab 1 Part 1 (l.159)",
        P,
        "c119 basis 'Lab 1, Part 1 (five spot states, 8000 to 12000 cents)' names the lab part that prints the values (L06.html printed l.286-288).",
    ),
    row(
        "cards-c122-referent",
        "2.7 referent of the recommendation",
        "cards.json PC3-c122; L06.html Ex 4.2 (l.149)",
        P,
        "c122 recommendation refers to Example 4.2 (l.149: buy only if units above 1206.34 at this rate and measure units first). Basis names Example 4.2 recommendation on the page.",
    ),
    row(
        "cards-c146-grade",
        "2.7 grade of a lab check",
        "cards.json PC3-c146 (grade C); L05.html Lab 1 Part 2 (l.176-177)",
        P,
        "c146 grade C matches the lab output (L05.html printed l.320-324, five True checks on one generated sequence); the card says so.",
    ),
    row(
        "cards-misconception-coverage",
        "2.7 misconceptions covered",
        "cards.json; L01.html Sec 5 (3 entries, l.327-336); L02.html Sec 4 (3 entries, l.377-386); L03.html Sec 5 (3, l.344-353); L04.html Sec 6 (4, l.490-503); L05.html Sec 5 (3, l.347-356); L06.html Sec 6 (4, l.318-331)",
        P,
        "Each misconception entry has at least one card: L01 c009, c010, c014; L02 c024, c025, c032; L03 c057, c058, c061; L04 c078, c079, c080, c081; L05 c098, c099, c100; L06 c120, c121, c123, c178.",
    ),
    row(
        "cards-number-presence",
        "2.7 every card number appears in its lesson",
        "cards.json; L01-L06.html text dumps (/tmp/pc3d_r10)",
        P,
        "Script of numerals on each card against its own lesson text (also all lessons): every numeral appears in its lesson. The only misses were rendering artefacts of TeX (29/100, 15/29, 2300/6, n^2/4), which appear in the lesson as \\tfrac and \\frac.",
    ),
    row(
        "cards-lab-printed-values",
        "2.7 lab-printed values on cards",
        "tests/labs/PC3/lab-PC3-L01..L06-1.py run in isolation; course/modules/PC/PC3/L01..L06.html",
        P,
        "Each twin ran under python -I -W error (exit 0 for all six). Every output line appears verbatim in its lesson text (compare_outputs.txt, 0 missing across 166 lines), and each lesson's pre block equals its lab output.",
    ),
    row(
        "cards-rederive",
        "2.2 numbers on cards re-derived",
        "ledgers/PC3/scripts/PC3-d-r10/rederive_r10.py and out/rederive_r10.txt; independent enumeration in this round",
        P,
        "Own script: ln 19.5 and factor widths; narrowing reductions 0.4055, 0.9163, 0.1754 (share 30.85, 5.9); 1.01^10 and 1.05^10 with remainders and bounds; "
        "break-evens 1164.1005, 1206.3444, 1249.0469 and 21.2366 per point; NPV values at 200, 1200, 1300, 1600 and rates 8, 10, 12; stopping-rule values on fair (0) and biased games "
        "(150, 1575/32, 1575/32, 575/8, 625/8) by a separate recursion; reroll 250 and 1150/3; deque and naive counts for seed 5 and seed 6 (independent implementation); seed 0 and seed 1 game (9, -9950, 1, 9980, 30; 16, 20100, -2, 10020, 60).",
    ),
    row(
        "gates-structural",
        "2.9 structure gates for PC3 (checkout 00a84795)",
        "tools/check_pages.py --all; check_dag.py --all; check_projects.py --all; tools/run_labs.py --unit PC3; page_smoke.py --unit PC3 --skip-labs --skip-sweep; verify_refs.py --offline; run_graders.py --unit PC3 --seeds 0-49; ruff check and format --check tests/labs/PC3; pytest -q -k PC3; mypy --no-incremental",
        P,
        "check_pages: PC3 PASS (27 pages PASS, exit 0); check_dag: PC3 PASS; check_projects: PC3 PASS; PC3 gate PASS (9/9); page_smoke PC3 PASS (all eight PC3 pages, light and dark, desktop and 360 px; exit 0); "
        "verify_refs --offline 560 entries, 0 problems; run_graders PC3 PASS (50/50 seeds); ruff check and format: 9 files already formatted; pytest -k PC3 9 passed (dots, exit 0); mypy --no-incremental: no issues in 385 files. Outputs are in ledgers/PC3/scripts/PC3-d-r10/out/.",
    ),
    row(
        "cards-grade-agreement",
        "2.3 grades on cards vs lesson key-results tables",
        "cards.json; L01-L06 key results (L01 l.458-465; L02 l.501-508; L03 l.468-475; L04 l.619-624; L05 l.472-477; L06 l.447-452)",
        P,
        "Lab-only values graded C (c009, c013, c014, c036, c047, c051-c053, c067, c075, c077, c080, c096, c097, c101, c116, c117, c119, c121, c123, c124, c130-c133, c135-c137, c137-c145, c146, c148-c150) match the key-results C rows. Hand-derived T results (c004, c007, c016, c021, c022, c039, c049, c054, c057, c066, c068-c071, c073, c078, c079, c110-c112, c125-c129, c147, c151, c178, c179) match T rows or derivations on the page.",
    ),
    row(
        "cards-c013-exact-value",
        "2.2 exact value on card c013",
        "cards.json PC3-c013 (grade C); L01.html Ex 1.7 (l.140) and L01.html printed l.306",
        P,
        "Card value 1.1046221254 (ten places) and exact begins 1.10462212541 match l.140 and the lab output; recomputed (1.01)^10 = 1.1046221254112.",
    ),
    row(
        "adjacent-lesson-numbers",
        "2.7 cross-references to adjacent lesson numbers",
        "cards.json PC3-c017, c020, c043; L02.html Def 2.1 (l.57) and Rem 2.3 (l.72); L03.html Def 3.5 (l.92)",
        P,
        "c017 M4 Lesson 1 for events and P(A) (L02 l.57 says 'as in M4 Lesson 1'); c020 M4 conditional distribution (L02 l.72); c043 Def 3.5 fair game as in Lesson 2 Def 2.2 (L03 l.92 says 'Lesson 2, Definition 2.2').",
    ),
    row(
        "lesson-L02-introduces-metadata",
        "2.9 'Introduces' metadata of L02",
        "course/modules/PC/PC3/L02.html l.38",
        P,
        "L02.html l.38 'Introduces: conditional probability (Definition 2.2), Bayes' rule (Proposition 2.4) and the law of total probability (Proposition 2.5)'. The three items are defined on the page at l.67, l.76 and l.89.",
    ),
    row(
        "cards-process-words",
        "2.9 no process words in learner text",
        "cards.json; L01-L06.html visible text (python regex: round, verif, revis, previous, fixed, builder, agent, todo, draft, placeholder, pending, reviewer, corrected, no longer, was changed)",
        P,
        "Only ordinary mathematical or instructional uses ('fixed pair', 'earlier payoffs', 'fixed quote', 'verify it by counting', 'Mark this lesson complete'). No process word in a card or in lesson prose.",
    ),
    row(
        "cards-simulated-label",
        "2.8 SIMULATED label on simulated results",
        "cards.json PC3-c067, c077, c137-c141; L04.html Lab 1 header (l.180) and Lab 1 docstring (l.183)",
        P,
        "c067, c077 and c137-c141 cite the seed-0 path and say SIMULATED; L04 Lab 1 header and docstring say SIMULATED (l.183). The seeded L05 sequences and L02 drill items are labelled generated, not data.",
    ),
    row(
        "cards-notation",
        "2.4 notation vs notation/notation.json",
        "notation/notation.json (macros \\E, \\Prob, \\Var, \\R, \\indic; symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}); cards.json; L01-L06.html",
        P,
        "Macros used on PC3 pages: \\Prob (143), \\E (44), \\R (2), \\indic (2), \\Var (3); all registered. No PC3 page or card uses T, \\Phi, \\gamma, R^\\ast, R_f or \\mathbb{Q} with a meaning. Plain Q (L01 l.59) is the quantity, not the registered \\mathbb{Q}. C_i in L02 and C_t in L04 are lesson-local letters, not registered. The stale A_i of PC3-c022 is covered by cards-block-021-030.",
    ),
    row(
        "cards-block-titles",
        "2.7 block titles named on cards",
        "cards.json PC3-c018, c089, c177; L02.html l.57 (Definition 2.1); L05.html l.106 and l.157 (Definition 3.1, Remark 3.6)",
        P,
        "Block titles on the pages: Definition 2.1 (events on a finite probability space, l.57), Definition 3.1 (the deque and its invariant, L05 l.106), Remark 3.6 (L05 l.157). Each card names the title.",
    ),
    row(
        "lesson-numbers-prose",
        "2.2 prose numbers in lessons read by the cards (defect classes 1, 4, 7, 8)",
        "L01.html Ex 1.4 (l.99-100), Ex 1.7 (l.140-141), Sec 2 (l.107-109), Sec 5 (l.328), E1-E3 (l.400-415), R1 (l.433), R3 (l.447); L02.html Ex 2.6-2.9, E1, M2, R3 (l.412-490); L03.html Ex 3.6, 3.10, E2, R1, R2 (l.103, l.322, l.425, l.441-450); L04.html Ex 3.2, Rem 4.2, R1, R3, E2, E3 (l.143, l.175-177, l.593, l.605-607, l.573-575, l.580-582); L05.html Rem 2.2, Rem 3.6, E1-E3 (l.97, l.158, l.419-435); L06.html Ex 4.2, Rem 4.3, Sec 6, E1-E3, R1, R3 (l.149-154, l.396, l.403-410, l.435-436)",
        P,
        "Every prose number on these pages was recomputed: 12000, 234000, 19.5, 2.9704, 30.8 and 5.9 percent, 0.9485, 5.4 and 7.9 percent, 52990.57, 16.5 and 0.1671; 0.1289/1.6289, 0.1662; 1/6, 29/100, 15/29, 2/5; 383.33, 33.33, 1575/32, 625/8 minus 150 = -575/8 = -71.875, 74.5 at c=1; "
        "1351, 5239, 354, 387, 382, 13.7, 10000 at k=101; 1164.10, 1206.34, 1249.05, 42.24, 42.70 (unrounded), 42.71 (rounded difference), 21.24 per point; 0.7540 and 24.6 percent; -78888.05; 1 - 0.0000 checks all pass. Lab-printed numbers match the lab outputs.",
    ),
    row(
        "lesson-scope-words",
        "2.2 scope words (only, all, every, exactly, always) on cards and lesson claims (defect class 4)",
        "cards.json; L01-L06.html (scope words in cards and in the claims those cards state)",
        P,
        "'every' and 'all' on cards: c004 (both bounds attained), c012 (every x >= 0 equality), c076 (every fair value, by the proof with an arbitrary v), c100 (every sequence, Prop 3.2), c101 (window sizes 1 to 20 on one sequence, stated as one sequence), c149 (all three rates, computed). "
        "'only' on c031/c037/c085 are scoped to a rule or event; 'exactly' on c023/c091/c095 are computed counts. No scope word is left without a computation or a stated hypothesis.",
    ),
    row(
        "lesson-dag-and-attribution",
        "2.5 cross-module attributions and DAG (defect classes 3, 14)",
        "L01.html (M1, M2 references, l.37, l.39, l.49); L02.html (M4 Lesson 1 l.23, l.57; M4 conditional distribution l.72); L03.html (M4 expectation l.25); course check_dag output (ledgers/PC3/scripts/PC3-d-r10/out/check_dag.txt, PC3 PASS)",
        P,
        "Cross-module concepts used: exponential-and-logarithm and taylor-theorem (M1, M2) in L01; M4 events, conditional distribution and expectation in L02-L03, linked. L04-L06 concepts (market maker, forward, NPV) are in closure or prose-only per the Architect decisions; check_dag passes. No new attribution is made in the round-10 edits.",
    ),
]

fragment = {
    "unit": "PC3",
    "slice": "PC3-d",
    "round": 10,
    "verifier": "Claude Haiku 5.5, independent verifier, slice d (ALL cards.json against the lessons), round 10; did not build PC3",
    "pin": "00a84795f276456fce19d4181373cc4efba11a36",
    "base": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (round-9 pin; round-9 fragment /Users/billyribeiro/.fanout/frags/E-PC3-d.round9.json, read as context only)",
    "checkout": CK,
    "scratch": f"{OUT} (lesson and card text dumps, lab outputs); durable scripts and outputs under {SCR}/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d is cards.json against the six lessons. cards.json (c022 basis, c057, c062 and the rest of cards.json), L01, L02 and L03 "
        "changed since the round-9 pin, so no row is carried: every row was re-verified from scratch this round. Round-9 FAIL (cards-block-051-060, c057) is fixed "
        "and now PASS. One new FAIL: cards-block-021-030, because the basis of PC3-c022 still names the disjoint pieces B ∩ A_i after the proof was renamed to C_i. "
        "No grader, lab code or reference is in this slice, so no grader mutants were written; the lab twins were run in isolation only as lab-printed-value evidence. "
        "Not run in this round: the full pytest suite (only -k PC3), page_smoke with --skip-labs and --skip-sweep, check_pages/check_dag/check_projects beyond PC3 "
        "(run with --all, which covers every unit), render_curriculum, build_site, fetch_data, and the live verify_refs run. "
        "No published fact is cited in PC3 (its lessons cite no registry source), so no UNVERIFIABLE row arises. "
        "Card ids have gaps (118, 134, 152, 155, 172); they are stable identifiers left by removals, not defects."
    ),
    "summary": {},
}

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
fragment["summary"] = {
    "rows": len(rows),
    "pass": counts["PASS"],
    "fail": counts["FAIL"],
    "unverifiable": counts["UNVERIFIABLE"],
    "mutants_killed": 0,
    "mutants": 0,
}
fragment["verdict"] = "PASS" if counts["FAIL"] == 0 and counts["UNVERIFIABLE"] == 0 else "FAIL"

with open(f"{CK}/ledgers/PC3/PC3-d.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("wrote", len(rows), "rows; pass", counts["PASS"], "fail", counts["FAIL"])
