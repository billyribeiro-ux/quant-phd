"""Writes ledgers/PC3/PC3-d.json (round 7) from the rows verified in this round. Usage: python -I build_fragment_r7.py"""
import datetime
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
S = "ledgers/PC3/scripts/PC3-d-r7"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


row("cards-schema", "2.7 schema and ids", "course/modules/PC/PC3/cards.json (177 cards)", "PASS",
    f"{S}/cards_struct_r7.out: 177 cards, 177 unique ids, all PC3-cNNN in ascending order, gaps at 134 and 155 only; "
    "keys id/lesson/front/back/cite on every card; grade and basis on 132 graded cards, none without the other; cite empty on "
    "all 177; empty front or back none. check_pages.py --all: 'check_pages PC3: PASS' (ledgers/PC3/scripts/PC3-d-r7/check_pages_all_r7.out).")
row("cards-coverage", "2.7 coverage (BUILDER_RULES 7)", "cards.json; L01-L06.html", "PASS",
    f"{S}/coverage_r7.out: every Definition, Theorem, Proposition, Corollary, Assumption, Remark and Example block title of L01-L06 "
    "is named by at least one card of its lesson. The 'Standing assumptions' blocks of L04 and L06 are covered by their A1-A6 and A1-A5 cards. "
    "L05 Remark 1.2 is named by c085 (script regex missed the trailing period; confirmed with label_refs_r7.out). Cards per lesson: L01 25, L02 23, L03 29, L04 37, L05 26, L06 37. "
    "Every lesson has at least one card (BUILDER_RULES 7).")
row("cards-dup-scan", "2.7 full duplicate scan", "cards.json (all 177 front+back pairs)", "PASS",
    f"{S}/cards_struct_r7.out: exact duplicate fronts none, exact duplicate backs none; near-duplicate pairs (ratio > 0.55) reviewed: "
    "c116/c148 (8 vs 12 percent break-even), c117/c150 (NPV at 200 vs 1600 units), c052/c135/c136 (three stopping rules), c027/c028 (urn events), "
    "c142/c145 (window 8 vs 32), c137-c140 (four quantities of one path), c013/c130 (value vs remainder), c127/c152 (percent vs cents of one margin), "
    "c093/c094 (two traces). Misconception cards restating a result (c032, c057, c112, c123, c178) are distinct by design.")

blocks = [
    ("cards-block-001-010", "PC3-c001..c010", "L01.html l.59-107, 327-335",
     "c001 Def 1.1 (l.59-60); c002 A1 (l.64); c003 log width (l.89, l.199); c004 Thm 1.2 hypotheses and conclusion (l.70-73); c005 (l.82, R2 l.437-440); "
     "c006 Prop 1.3 (l.85-89); c007 Example 1.4 products 12 000 and 234 000 (l.99); c008 (l.105); c009 misconception, 0.1754 = 5.9 percent and 0.9163 = 30.8 percent (l.107, l.328; lab output l.300 and l.299; recomputed in card_arithmetic_r7.out); c010 second misconception (l.331-332)."),
    ("cards-block-011-020", "PC3-c011..c020", "L01.html l.114-141, 202, 260, 267; L02.html l.22-29, 56-80",
     "c011 Thm 1.5 hypotheses H1-H3 and bound (l.119-125); c012 Remark 1.6 (l.135); c013 1.1046221254 (lab output l.306; card_arithmetic_r7.out 1.104622125411); c014 1.5 and 1.6289 and miss 0.1289 (l.141, l.336); "
     "c015 (l.319); c016 R3 ln 1.5 = 0.4055, ln(2.5/1.01) = 0.9063 (l.447, card_arithmetic_r7.out); c017 Def 2.1 with p(w) > 0 (L02 l.57, changed text matches); c018 (l.57); c019 Def 2.2 (l.67); c020 Remark 2.3 (l.72)."),
    ("cards-block-021-030", "PC3-c021..c030", "L02.html l.76-101, 110-129",
     "c021 Prop 2.4 hypotheses A1, P(A)>0, P(B)>0 (l.78-80); c022 Prop 2.5 (l.91-94); c023 Example 2.6 values 1/3 and 1/2 with probabilities 3/4, 1/2, 1/4 (l.111; lab Part 4 output); c024 misconception (l.381-382); c025 counterexample 1/3 vs 1 (l.386; lab Part 4); "
     "c026-c028 urn 3/5, 3/5, 3/10 (l.116; lab Part 4; card_arithmetic_r7.out); c029 3/4 with one blue and three red left (l.117, l.358)."),
    ("cards-block-031-040", "PC3-c031..c040", "L02.html l.122-124, 366-382; L03.html l.62-80",
     "c030 rule A 1/3 and 2/3 (L02 l.123); c031 rule B both 1/2, goat event 2/3 (l.124); c032 misconception (l.377-378); c033 bag 3/4, P(red) 1/2 (l.129); c035 M2 P(B)=29/100, P(A|B)=15/29 (l.408; card_arithmetic_r7.out); "
     "c036 12 of 12 (lab Part 1 output l.340); c037 where the canon breaks (l.366); c038 Def 3.1 (l.62); c039 Prop 3.2 hypotheses and conclusion, changed text re-read against l.66-75; c040 E[face]=7/2, 350 cents (l.80)."),
    ("cards-block-041-050", "PC3-c041..c050", "L03.html l.62-111, 189-204, 297-316",
     "c041 E[X+Y]=7 (l.80, lab Part 1 output l.257); c042 Def 3.4 (l.87); c043 Def 3.5 wording (l.92); c044 A2 (l.97); c045 250 cents (l.102); c046 1150/3 = 2300/6 (l.103); c047 lab Part 2 1150/3 (output l.269); c048 Def 3.7 (l.109); c049 Thm 3.8 hypotheses H1-H3 and conclusion (l.299-303); c050 Remark 3.9 (l.316)."),
    ("cards-block-051-060", "PC3-c051..c060", "L03.html l.102-104, 207-224, 249-267, 279-285, 321-322, 345-349",
     "c051 150 = 6 x 25 (l.322; output l.281); c052 1575/32 (l.282 and output l.282); c053 changed text, zero for the five rules by two methods (output l.273-279); c054 Thm 3.8 with A2 over N=6 (l.321); c055 R1 mean 50 from totals 200, 100, 0, -100 (l.443; card_arithmetic_r7.out); "
     "c056 P3 threshold face 3 (l.407); c057 misconception (l.344-345); c058 100/3 (l.104, l.349); c059 reroll game not fair, mean 350 (l.349); c060 (H2) fails at the first turn (l.300, l.450)."),
    ("cards-block-061-070", "PC3-c061..c070", "L03.html l.326-327, 352-353; L04.html l.25-70, 128-143",
     "c061 Example 3.11 (l.327, l.353); c062 Def 1.1 steps (l.59-65); c063 A1 probabilities 1/4, 1/4, 1/2 (l.72); c064 A5 (l.76); c065 Def 2.1 (l.97); c066 Prop 2.2 hypotheses H1-H2 and conclusion (l.102); c067 seed-0 mid 9990 and settlement 9980: 40 vs 30 (l.122, l.566; lab output l.434-436); "
     "c068 Prop 2.3 (l.112); c069 changed text re-read against l.129-138: fixed quote, A6, A4, arrival independent of v_t, formula (1-p)h - p[(v-a)^+ + (b-v)^+] re-derived; c070 Example 3.2 values 5, 0, 5/2 (l.143; lab Part 2 output l.445-449)."),
    ("cards-block-071-080", "PC3-c071..c080", "L04.html l.147-175, 329-349, 475-476",
     "c071 Cor 3.3 with changed hypotheses (l.148, l.152-153), E = h/2 - (v-a)/2, zero iff v = a+h; c072 Remark 3.4 changed text (l.158), (1-p)h = h/2 = a quarter of 2h; c073 Prop 4.1 hypotheses and mean 0, variance 25 I^2 (l.165-170); c074 Remark 4.2 15 and 50 cents (l.175); "
     "c075 nine fair values 9980..10020 (lab Part 2 output lines 443-451); c076 changed text, Prop 3.1 for every fair value under (H3) (l.129-134) and the lab checks the nine grid values (l.198-199); c077 9 fills (output l.431); c078 misconception (l.475-476); c079 M1 10 cents (l.502)."),
    ("cards-block-081-090", "PC3-c081..c090", "L04.html l.487, 577-591; L05.html l.22-64, 86-97",
     "c080 variance 2500 at 10 units (output l.458; l.483); c081 A3 misconception (l.487, l.74); c082 R1 d = (1-p)h/p = 20/3 (l.577-578); c083 R3 |I|=1 variance 25, 2 gives 100 (l.591); c084 six steps in order (L05 l.60-65); c085 Remark 1.2 (l.71); c086 Def 1.3 n-k+1 entries (l.78); "
     "c087 Prop 2.1 (n-k+1)(k-1) (l.86-92); c088 Remark 2.2, k = n/2+1, n^2/4 (l.97; card_arithmetic_r7 algebra); c089 Def 3.1 surviving index (l.106); c090 Prop 3.2 (l.124-125)."),
    ("cards-block-091-100", "PC3-c091..c100", "L05.html l.136-151, 203-215, 328-345, 399",
     "c091 Prop 3.3 appends n, removals at most n, tests at most 2n (l.137, l.142); c092 Remark 3.4 changed basis, all k-1 removed in one pass (l.147); c093 (4,4,5) trace (l.152; output of the lab logic re-traced); c094 (5,5,1,3) (M2 l.367); c095 P3 n-1 comparisons (l.399); "
     "c096 1351 = 193 x 7 (output l.303); c097 5239 = 169 x 31 (output l.319); c098 misconception (l.337); c099 operation counts not run times (l.341); c100 Prop 3.2 proof versus one sequence (l.345)."),
    ("cards-block-101-110", "PC3-c101..c110", "L05.html l.163-176, 308; L06.html l.59-117; L06.html l.69-73",
     "c101 True for windows 1 to 20 (output l.308); c102 Prop 1.1 (l.60-65); c103 Remark 1.2 is put-call parity (l.69-70); "
     "c104 FAILS: the card cites 'Remark 1.2 (net present value, defined in the linked module)'. L06.html Remark 1.2 (l.69, text l.69-70) is the put-call parity remark; no Definition 1.3 exists anywhere in L06.html (grep 'Definition' gives only Definition 4.1). The NPV formula is the unnumbered paragraph at L06.html l.73. The formula sum C_t(1+r)^(-t) itself is correct. "
     "c105 A1 (l.82); c106 A2 (l.83); c107 Prop 2.1(i) portfolio (l.92, l.97); c108 Prop 2.1(ii) hypotheses A1-A5 (l.92, l.98); c109 Remark 2.2 (l.103); c110 Prop 3.1 hypotheses and u* = I/(mA) (l.112, l.117)."),
    ("cards-block-111-117", "PC3-c111..c117", "L06.html l.121-127, 131-137, 149-154",
     "c111 Prop 3.2 bounds and attainment (l.122-127); c112 Cor 3.3 (l.132-137); c113 Def 4.1 five steps (l.144); c114 [200,1600] (l.149); c115 A = 3310/1331 = 2.48685 (l.149; card_arithmetic_r7.out); c116 break-even 8 percent 1164.10 (l.154; output l.301); c117 NPV at 200 units -12513148, exact -16655000000/1331 (output l.297; card_arithmetic_r7.out)."),
    ("cards-block-118-123", "PC3-c118..c123", "L06.html l.91-98, 103, 144-154, 304-331",
     "c118 changed text (A1 to A3), spot cancels (l.97); c119 five spot states 8000-12000, 0 and 100 cents, lab True (output l.286-289); c120 misconception (l.319); c121 break-even moves with the rate (l.154); c122 recommendation above 1206.34 (l.149); c123 sign at 8, 10, 12 percent (output l.301-303; l.331)."),
    ("cards-block-124-130", "PC3-c124..c130", "L06.html l.149-154, 403-405, 421; L01.html l.99, 107, 146",
     "c124 1200 units at 8 percent: 1200 > 1164.10 and NPV increasing gives positive; card_arithmetic_r7.out NPV(1200, 8%) = +462581.92 (basis is labelled lab but the claim is derived from the printed break-even; accepted as C); c125 M2 500/121 (l.353, card_arithmetic_r7.out); c126 M3 33275/331 (l.358-360); c127 R3 margin fall 0.7540 and 24.6 percent (l.435; card_arithmetic_r7.out 0.75397, 24.60); c128 ln 19.5 (l.99); c129 ln 3, ln 5, ln 1.3 sum (l.99); c130 remainder 0.0046221254 (output l.306)."),
    ("cards-block-131-135", "PC3-c131..c136 (c134 absent)", "L01.html l.135-141, 146; L03.html l.322, 283-285; lab outputs",
     "c131 bound 0.0048728552 (output l.306; card_arithmetic_r7.out); c132 remainder below bound, lab checks 0 <= remainder <= bound (l.146; output l.308); c133 bound 0.1662 and miss 0.1289 (output l.307); c135 575/8 and c136 625/8 (output l.284-285; card_arithmetic_r7.out with corrected path weighting)."),
    ("cards-block-136-142", "PC3-c137..c142", "L04.html l.79-80, 293-299, 321; lab Part 1 output",
     "c137 cash flow -9950 (output l.432); c138 final inventory 1 (output l.433); c139 settlement 9980 (output l.434); c140 P&L 30 = -9950 + 9980 (output l.436; l.566); c141 identity True (output l.437); c142 deque comparisons 354 (L05 output l.304); "
     "seed-0 game re-simulated independently in card_arithmetic_r7.out: fills 9, cash -9950, inventory 1, settlement 9980, P&L 30."),
    ("cards-block-143-150", "PC3-c143..c150", "L05.html l.186-203, 252-256, 309-321; L06.html l.182-188, 297-303",
     "c143 200 pushes, 199 pops (output l.304 and the Part 3 row k=8 at l.318); c144 window 200: 387 <= 400 and largest in Part 3 (output l.320); c145 window 32: 382 (output l.319); c146 five edge checks True (output l.309-313); c147 u* = 399300/331 (l.149; card_arithmetic_r7.out 1206.3444); c148 break-even 12 percent 1249.05 (output l.303; 1249.0469); c149 signs at 8, 10, 12 percent (output l.301-303); c150 NPV at 1600 = 4894816 (output l.298)."),
    ("cards-block-151-168", "PC3-c151..c168", "L06.html l.306-307 (E3), l.435 (R3); L03.html l.109, 297-303; L04.html l.76, 83, 88; L01.html l.67-80, 446-447",
     "c151 E3 21.2366 displays 21.24, computed from unrounded break-evens (l.410-412; card_arithmetic_r7.out 21.2366); c152 margin 3769.8 cents = 15000000 x 1331/(1600 x 3310) (l.435; card_arithmetic_r7.out 3769.8263); c153 Remark 1.2 (L04 l.82); c154 A5 and fill of one unit (l.76, l.82); "
     "c155 absent; c156 2.9704144656 printed to ten places (output l.288); c157 A2 Lagrange form, not reproved (L01 l.115); c158 A1 finite, P(B)>0 (L02 l.62); c159 A2 1/4 each (L02 l.106); c160 changed text, p(w) > 0 matches L03 l.57; c161 A3 (L03 l.293); c162 A2 fair path (L04 l.73); c163 A4 (L04 l.75); c164 A6 (L04 l.77); c165 A3 no costs (L06 l.84); c166 A4 (L06 l.85); c167 A5 (L06 l.86); c168 Example 1.3 (L04 l.88)."),
    ("cards-block-169-171", "PC3-c169..c171", "L05.html l.156-161; L04.html l.74",
     "c169 hash map does not report the maximum (l.157); c170 heap bound 3n floor(log2 n) = 4200 for n = 200 against 400 (l.158); c171 A3 public history, not v_t (L04 l.74)."),
    ("cards-block-172-179", "PC3-c172..c179", "L01.html l.68-73; L03.html l.109, 297; L04.html l.93, 97; L06.html l.149-154, 403-405, 435",
     "c172 product interval of the ranges (Theorem 1.2 conclusion l.73; the parenthetical reads '(product interval)' where the block title is '(product bounds)', accepted as a gloss); c173 Def 3.7 W(h) (l.109); c174 fill sign sigma_t and cash change c_t = -sigma_t f_t (L04 l.93); c175 inventory change (l.93); "
     "c176 Remark 3.4 (l.157-158); c177 Def 3.1 of the deque (L05 l.106); c178 Cor 3.3 with output signs (l.132, output l.297-298); c179 E2 -105000000/1331 = -78888.05 (l.403; card_arithmetic_r7.out)."),
    ("cards-block-round3-id-carry", "PC3-c003, PC3-c069, PC3-c151", "cards.json; L01.html l.85-89; L04.html l.128-138; L06.html l.410-412",
     "Round-3 ids re-verified this round: c003 log-error width ln(u/l) (L01 l.89, l.199); c069 changed text, re-derived (L04 l.128-138); c151 re-derived (card_arithmetic_r7.out)."),
    ("cards-atomicity", "2.7 one fact per card", "cards.json (all 177 fronts and backs)", "PASS",
     "Each card was read in full (ledgers/PC3/scripts/PC3-d-r7 dumps, /tmp/pc3d_r7/cards.txt). Composite misconception cards (c009, c014, c025, c123) each state one misconception and its counter-fact; no card asks two unrelated facts."),
    ("cards-c119-basis", "2.7 basis", "cards.json PC3-c119", "PASS",
     "basis 'Lab 1, Part 1 (five spot states, 8000 to 12000 cents)' names the lab part that prints the values (output l.286-289)."),
    ("cards-c122-referent", "2.7 referent", "cards.json PC3-c122", "PASS",
     "The Fermi range and the recommendation are on L06.html l.149 (Example 4.2); the 1206.34 threshold matches Problem E2 and Prop 3.1."),
    ("cards-c146-grade", "2.7 grade", "cards.json PC3-c146", "PASS",
     "Grade C for the five edge-case checks, which are lab prints (L05 output l.309-313); the lesson key-results table grades the Part 2 result C (L05 l.466)."),
    ("cards-misconception-coverage", "2.7 misconceptions", "cards.json; L01 l.327-336; L02 l.377-386; L03 l.344-353; L04 l.474-487; L05 l.336-345; L06 l.318-331", "PASS",
     "Each misconception paragraph has at least one card: L01 c009, c010, c014; L02 c024, c025, c032; L03 c057, c058, c061; L04 c078, c079, c080, c081; L05 c098, c099, c100; L06 c120, c121, c123, c178."),
    ("cards-number-presence", "2.7 numbers in own lesson", "cards.json; L01-L06 text dumps", "PASS",
     f"{S}/cards_struct_r7.out: 'tokens absent from own lesson: 0' (every numeric token of every card, after comma removal, occurs in its own lesson text dump /tmp/pc3d_r7/L0n.txt)."),
    ("cards-lab-printed-values", "2.2 printed values behind cards", "tests/labs/PC3/lab-PC3-L01..L06-1.py; course/modules/PC/PC3/L01..L06.html", "PASS",
     f"Every lab run again (python -I -W error, exit 0 for all six); outputs in {S}/outputs/. Every output line occurs verbatim in its lesson page (checked by script, 0 missing lines of 26+32+30+50+23+21). run_labs.py --unit PC3: PASS (9/9) ({S}/run_labs_PC3_r7.out)."),
    ("cards-rederive", "2.2 / 2.4 numbers re-derived by verifier", f"{S}/card_arithmetic_r7.py", "PASS",
     f"{S}/card_arithmetic_r7.out, written from the lesson statements, not the lab code: biased-game rules (1575/32, 575/8, 625/8, 150), fair-game zero, reroll 250, 1150/3, 100/3, R1 mean 50, urn 3/5, 3/5, 3/10, 3/4, M2 15/29, bag 3/4, ln 19.5 and factor widths, shares 5.9 and 30.8 percent, R3 widths, Taylor remainder and bound at n=10 (0.0046221254, 0.0048728552, 0.1288946268, 0.1662137374), A(10%)=3310/1331, break-evens 1164.1005, 1206.3444, 1249.0469, NPV(200), NPV(1600), NPV(1200)=-105000000/1331, NPV(1300), M2 500/121, M3 33275/331, R3 margin 3769.83 and 0.7540, E3 21.2366, seed-0 game 9 fills, -9950, 1, 9980, 30, mid-marked 40. One script bug (weighting of unplayed turns) was found and fixed in this round; the corrected output matches the lab."),
    ("gates-structural", "2.9 gates for the slice", "check_pages, check_dag, check_projects, run_labs, pytest for PC3", "PASS",
     f"{S}/check_pages_all_r7.out: check_pages PC3: PASS. {S}/check_dag_all_r7.out: check_dag PC3: PASS. {S}/check_projects_all_r7.out: check_projects PC3: PASS. {S}/run_labs_PC3_r7.out: run_labs PC3: PASS (9/9). {S}/pytest_pc3_r7.out: pytest -k 'PC3 or pc3' exit 0."),
    ("cards-grade-agreement", "2.3 grades vs key-results tables", "cards.json; L01-L06 key-results tables", "PASS",
     "Card grades agree with the grade of the same result in each lesson's key-results table: T for proofs (Thm 1.2, Prop 1.3, Thm 1.5, Prop 2.4, 2.5, Prop 3.2, Thm 3.8, Prop 2.2, Prop 3.1, Cor 3.3, Prop 4.1, Prop 1.1, Prop 2.1, Prop 3.3); C for lab results (L01 c009, c130-c133, c156; L02 c036; L03 c047, c051-c053, c135-c136; L04 c067, c075, c077, c137-c141; L05 c101, c142-c146; L06 c116-c117, c119, c121, c123, c124, c148-c150)."),
    ("cards-c013-exact-value", "2.2 exact digits", "cards.json PC3-c013; L01.html l.140", "PASS",
     "1.1046221254 to ten places and 1.10462212541 as the exact leading digits: (1.01)^10 = 1.1046221254112045... (card_arithmetic_r7 check)."),
    ("adjacent-lesson-numbers", "2.9 cross-references in cards", "cards.json PC3-c017, c020, c043; label_refs_r7.out", "PASS",
     f"{S}/label_refs_r7.out: 'cards naming a label absent from their own lesson: 0'. Cross references resolve: 'Lesson 2, Definition 2.2' (c043) and 'Definition 2.2' exist in L02; 'M4 Lesson 1' (c017) is the prerequisite named in L02 l.57."),
    ("lesson-L02-introduces-metadata", "2.9 structure (round-6 FAIL re-verified)", "course/modules/PC/PC3/L02.html line 38", "PASS",
     "Round-6 FAIL is resolved at pin 06994db: L02.html l.38 now reads 'Introduces: conditional probability (Definition 2.2), Bayes' rule (Proposition 2.4) and the law of total probability (Proposition 2.5)'. All three blocks exist in L02.html (block titles Definition 2.2, Proposition 2.4, Proposition 2.5); the 'defined here in prose' wording is removed."),
    ("cards-process-words", "2.9 process words (round-6 FAIL re-verified)", "cards.json PC3-c092 basis; all cards", "PASS",
     "Round-6 FAIL is resolved: c092 basis is now 'Remark 3.4 (a direct trace of the while loop at step k)'. Re-scan of every front, back and basis for verified, verifier, builder, round, checked by, reviewed, this card: no hit. c076 back 'The lab checks only the nine grid values' describes what the lab does (L04 l.198-199), not a process."),
    ("cards-simulated-label", "2.8 SIMULATED labels", "cards.json PC3-c067, c077, c137-c141", "PASS",
     "Each card drawn from the seed-0 game names SIMULATED in its front or basis (c067 basis, c077, c137-c141 fronts). The seeded sequences of L05 are generated test inputs that the lab calls 'not data'; no market data is used."),
    ("cards-notation", "3 notation vs notation.json", "notation/notation.json (8 symbols); cards.json", "PASS",
     "notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f and Q. No card uses a standalone T (script scan: none) or any other registered symbol. Cards write E[.], Prob and Var in plain text and use no macro that the registry defines with a different meaning."),
]
for entry in blocks:
    if len(entry) == 5:
        rid, check, loc, status, ev = entry
        fix = None
        row(rid, check, loc, status, ev, fix)
        continue
    rid, cards_in, loc, ev = entry
    check = f"2.7 content vs lesson, cards {cards_in}"
    status = "FAIL" if rid == "cards-block-101-110" else "PASS"
    fix = None
    if status != "PASS":
        fix = ("Change the front of PC3-c104 so it does not cite Remark 1.2. Remark 1.2 in L06.html (line 69, put-call parity) is "
               "a different result. Either cite the unnumbered NPV paragraph of Section 1 (L06.html line 73, the sentence beginning "
               "'For cash flows') or give that paragraph a numbered Definition block in L06.html and cite that number. Example front: "
               "'Net present value, as Section 1 of this lesson states it. For cash flows C_0 to C_n and a rate r > -1, what is NPV(r)?'. "
               "Then rerun check_pages, coverage_r7.py and label_refs_r7.py.")
    row(rid, check, loc, status, ev, fix)

fragment = {
    "unit": "PC3",
    "slice": "PC3-d",
    "round": 7,
    "verifier": "Claude Haiku 5.5, independent verifier, slice d (ALL cards.json against the lessons), round 7; did not build PC3",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin; round-6 fragment /Users/billyribeiro/.fanout/frags/E-PC3-d.round6.json). Delta since it, PC3 files: cards.json (17 lines: c017, c039, c053, c069, c071, c072, c076, c092, c104, c118, c160, c172, c173, c176 changed), L01.html (E2 solution), L02.html (metadata, Def 2.1, Section 3), L03.html (A1, Part 3b interpretation), L04.html (Def, Prop 3.1, Cor 3.3 text), L06.html (Cor 3.3 and its proof), index.html, project.html, grader/starter.py, grader/test_project.py, tests/labs/PC3/lab-PC3-L04-1.py. Every card row is re-verified this round against the current text; no row is carried.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-PC3-d",
    "scratch": "/tmp/pc3d_r7 (lesson text dumps and card dumps); durable scripts and outputs under ledgers/PC3/scripts/PC3-d-r7/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": None,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice d is cards.json only, so no grader mutants were written or run (the mutant requirement belongs to the project slices). "
        "The single non-PASS row (cards-block-101-110, card PC3-c104) is a regression that the round-6 fragment passed: its row cited 'Def 1.3 NPV (l.73)', but L06.html has no Definition 1.3 and l.73 is an unnumbered paragraph; "
        "round 6 was wrong to PASS it. Non-blocking observations, not rows: parenthetical glosses on c109 ('algebra of the discount factor' for Remark 2.2, whose block title is 'the same price in the linked convention'), "
        "c169 and c170 (Remark 3.6 glosses for the hash map and heap), c172 ('product interval' for Theorem 1.2, block title 'product bounds') and c178 (Corollary 3.3 gloss). The numbers and claims in these cards are correct; the glosses do not change any fact. "
        "Card c124 (basis: Lab 1, Part 2) states a claim derived from the printed 8 percent break-even; the grade C is kept."
    ),
    "summary": None,
}
non_pass = [r["id"] for r in rows if r["status"] != "PASS"]
fragment["verdict"] = "PASS" if not non_pass else "FAIL"
fragment["summary"] = {
    "rows": len(rows),
    "pass": sum(r["status"] == "PASS" for r in rows),
    "fail": sum(r["status"] == "FAIL" for r in rows),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows),
    "mutants": 0,
    "mutants_killed": 0,
}
out = ROOT / "ledgers/PC3/PC3-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"], fragment["verdict"])
