"""Write ledgers/PC3/PC3-d.json for the PC3 slice d closing delta, round 1 (carry rows from the round-12 fragment)."""
import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF31-PC3-d")
base = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-PC3-d.round12.json").read_text(encoding="utf-8"))
base_rows = {r["id"]: r for r in base["rows"]}
OUT_DIR = "ledgers/PC3/scripts/PC3-d-r1/out/"
CARRY = "Carried from round 12 (course/modules/PC/PC3/L01.html, L02.html, L03.html and the cited card objects byte-identical since the previous pin 5db69a9b, per card_delta.py and git diff --quiet): "

def carry(rid, check_extra=None, files_note=None):
    b = base_rows[rid]
    ev = CARRY + (files_note + "; " if files_note else "") + b["evidence"]
    return {"id": rid, "check": b["check"], "location": b["location"], "status": "PASS", "evidence": ev}

def row(rid, check, location, evidence):
    return {"id": rid, "check": check, "location": location, "status": "PASS", "evidence": evidence}

rows = []
rows.append(row("cards-schema",
    "cards.json is valid JSON; objects with keys id, lesson, front, back, cite; grade and basis on graded cards; ids unique",
    "course/modules/PC/PC3/cards.json (187 objects; was 174 at 5db69a9b)",
    "Re-run this round: ledgers/PC3/scripts/PC3-d-r1/cards_scan_r1.py -> out/cards_scan_r1.txt: 187 cards; ids unique and strictly increasing; keysets 140 x {back,basis,cite,front,grade,id,lesson} and 47 x {back,cite,front,id,lesson}; grades T 105, C 35, none 47; graded cards without basis: none; cite non-empty: none. card_delta.py output: 0 base ids removed, 13 new ids PC3-c180..c192, 20 base objects changed."))
rows.append(row("cards-coverage",
    "every card names an existing lesson; every lesson has cards; per-lesson counts",
    "course/modules/PC/PC3/cards.json; L01.html..L06.html",
    "cards_scan_r1.txt: L01 24, L02 23, L03 29, L04 40, L05 30, L06 41 (total 187); all six lesson files exist; every lesson has cards. tools/check_pages.py --unit PC3 -> out/check_pages_PC3.txt 'check_pages PC3: PASS' (exit 0)."))
rows.append(row("cards-dup-scan",
    "no duplicate front or back text across the 187 cards",
    "course/modules/PC/PC3/cards.json",
    "cards_scan_r1.txt: duplicate fronts [] and duplicate backs []."))
rows.append(row("cards-block-001-010",
    "cards PC3-c001..c010 against L01 text",
    "course/modules/PC/PC3/cards.json c001..c010; course/modules/PC/PC3/L01.html l.59-64, l.68-73, l.82, l.440",
    "Changed object c005 re-read against L01 (front now lists H1 k>=1 and the A1 bounds): Theorem 1.2 (H1) l.70, (H2) l.71 under A1 (l.64); worst-case and no-probability statement l.82; R2 solution l.440 (proof uses only ranges, no joint distribution). Basis 'Theorem 1.2 and its proof, which uses only (H1) and (H2)' matches l.440. PASS. The other nine objects are byte-identical to 5db69a9b and L01.html is byte-identical, so their round-12 evidence stands."))
rows.append(carry("cards-block-011-020", files_note="course/modules/PC/PC3/cards.json objects c011..c020"))
rows.append(carry("cards-block-021-030", files_note="cards c021..c030"))
rows.append(carry("cards-block-031-040", files_note="cards c031..c040"))
rows.append(row("cards-block-041-050",
    "cards PC3-c041..c050 against L03 text",
    "course/modules/PC/PC3/cards.json c050; course/modules/PC/PC3/L03.html l.294-303 (Theorem 3.8, (H1) finite N), l.315-316 (Remark 3.9), l.334 (Section 4)",
    "c050 re-verified: Theorem 3.8 (H1) 'the horizon N is finite' (L03 l.299) so the front's 'finite horizon N as a hypothesis' is right; the proof uses N in its induction (l.309); Section 4 l.334 names the unbounded case. Other objects byte-identical to base; L03.html byte-identical. PASS."))
rows.append(row("cards-block-051-060",
    "cards PC3-c051..c060 against L03 text and Lab 1 Part 3 output",
    "course/modules/PC/PC3/cards.json c053, c055; L03.html printed Part 3 block l.273-285 (equal to the twin output; run_labs PASS); L03.html l.440-443 (R1 solution), l.205 and l.519 (H3)",
    "c053 (grade C): lab code L03 l.207-210 enumerates product(outcomes, repeat=6) = 64 sequences next to the recursion; the printed Part 3 block l.273-278 prints expectation 0 for the five rules and 'the two methods agree for every rule: True'. PASS. c055 (grade T): R1 solution l.443 gives totals 200, 100, 0, -100 for the four paths, mean (200+100+0-100)/4 = 50 (rederive_r1 and mental check); the rule reads later payoffs so (H3) fails (l.205, l.519). PASS. Other objects in the block byte-identical to base."))
rows.append(row("cards-block-061-070",
    "cards PC3-c061..c070 against L03 and L04 text",
    "course/modules/PC/PC3/cards.json c062, c067; L04.html l.59-65 (Definition 1.1), l.122 (Remark 2.4), l.582-585 (Problem E3); L04.html Part 1 printed block (seed 0 log; equal to the twin output)",
    "c062 vs Definition 1.1 steps 1-4 (l.62-65): +/-5 move; integer bid < ask; size in {0..5}, q-bar = 5 largest; one arrival resolved by A1, A4, A5; fill changes cash and inventory as Section 2. PASS. c067 vs Remark 2.4 (final mid 9990, settlement 9980) and Problem E3 (l.583-585: P&L at settlement -9950+9980 = 30, at mid -9950+9990 = 40, difference 10 = 1 unit x 10). Seed 0 log: last fill at turn 19 price 9990 (so the turn-20 quote mid is 9990), settlement 9980, cash flow -9950, inventory 1 (L04.html printed Part 1 block). PASS. Other objects byte-identical."))
rows.append(row("cards-block-071-080",
    "cards PC3-c071..c080 against L04 text and Lab 1 printed output",
    "course/modules/PC/PC3/cards.json c072, c078; L04.html l.160 (Remark 3.4, changed), l.494 (misconception, changed), l.150-155 (Corollary 3.3), l.177 (Remark 4.2)",
    "c072 vs changed Remark 3.4 (l.160): (1-p)h cents per turn; at p=1/2 this is h/2, one quarter of the quoted spread 2h. Consistent. PASS. c078 vs changed misconception (l.494): from inventory zero, uninformed flow earns h/2 and the informed cost is (v-a)/2 = h/2 at v = a+h (Corollary 3.3 l.155 gives E = h/2 - (v-a)/2), so E = 0. PASS. c074 vs Remark 4.2 l.177 (3 units: 15 cents; 10 units: 50 cents). PASS. Other objects byte-identical."))
rows.append(row("cards-block-081-090",
    "cards PC3-c081..c090 against L04, L05 text",
    "course/modules/PC/PC3/cards.json c081, c090; L04.html l.74 (A3), l.131-134 (Proposition 3.1 H2), l.505-506 (misconception); L05.html l.124-132 (Proposition 3.2, Steps A-C)",
    "c081 vs A3 (l.74: quote is a function of the public history, not of v_t), misconception l.506 ('A3 excludes it ... Proposition 3.1 does not apply'), and H2 of Proposition 3.1 (l.131: quote is a fixed pair). PASS. c090 (changed to 'the value of the front index after step i') vs Proposition 3.2 conclusion (l.125) and Step B (l.131): the front is the window maximum. PASS. c087..c089 byte-identical, L05 Proposition 2.1 and Definition 3.1 unchanged (l.86-106)."))
rows.append(row("cards-block-091-100",
    "cards PC3-c091..c100 against L05 text and Lab 1 output",
    "course/modules/PC/PC3/cards.json c091, c096, c097 (changed), c092..c095, c098..c100; L05.html l.136-145 (Proposition 3.3 proof), l.146-149 (Remark 3.4), l.152-157 (Example 3.5), l.378-380 (M2), l.408-414 (P3), l.347-356 (misconceptions), l.419-435 (E1, E2 and E3 solutions), L05.html printed Part 1 and Part 3 blocks l.307-331",
    "c091 vs Proposition 3.3 proof (l.142: step i appends i once; no index appended twice): 'exactly n'. PASS. c096: L05.html printed Part 1 line l.312 'naive comparisons = 1351'; 193 x 7 = 1351 with n=200, k=8 (Proposition 2.1; E2 solution l.428 says the same formula for seed 6). PASS. c097: L05.html printed Part 3 line l.330 '32  169  5239'; 169 x 31 = 5239 (E1 solution l.421). PASS. c092 (Remark 3.4 example, k entries in one step, l.147), c093 (Example 3.5 outputs (4,4,5), l.152), c094 (M2 outputs (5,5,1,3), l.378), c095 (P3 n-1, l.410), c098 (l.348), c099 (l.169-170, l.352), c100 (l.355-356): each re-read against the cited text. PASS."))
rows.append(row("cards-block-101-110",
    "cards PC3-c101..c110 against L05 and L06 text and output",
    "course/modules/PC/PC3/cards.json c110 (changed), c101; L05.html l.319 (Part 2 output); L06.html l.111-117 (Proposition 3.1)",
    "c110 vs Proposition 3.1 (i) (L06 l.117: NPV(u) = -I + sum u m (1+r)^-t = -I + mAu): back 'NPV(u) = -I + m A u' matches; the hypotheses in the front match H1-H3 (l.112). PASS. c101: L05.html printed Part 2 line l.319 'outputs equal for window sizes 1 to 20: True'. PASS. c102..c109 byte-identical with their L06 cited lines (l.59-64, l.69-73, l.82-86, l.92-103) unchanged; their round-12 evidence stands."))
rows.append(row("cards-block-111-117",
    "cards PC3-c111..c117 against L06 text and lab output",
    "course/modules/PC/PC3/cards.json c112, c116 (changed), c117; L06.html l.122-127 (Prop 3.2), l.132-137 (Cor 3.3 and proof), l.149 (Ex 4.2), l.154 (Rem 4.3), out/L06.html printed line l.299",
    "c112 vs Corollary 3.3 (l.132): if l < u* < h the bounds alone do not fix the sign; the unit count l gives a loss, h a gain (l.137, NPV(u) = mA(u-u*) by Prop 3.1). Hypotheses in the front match l.122 and l.112. PASS. c116 (break-even at 8% = 1164.10; A = 2.5770970; 3000/A = 1164.1005): rederive_r1.txt 'break-even at 8%: display2 1164.10 display4 1164.1005'. PASS. c117: L06.html printed line l.299 'NPV at the lower bound = -12513148 cents (exact -16655000000/1331)'; rederive_r1.txt: 5000*200*3310/1331 - 15000000 = -16655000000/1331, display -12513148. PASS. c111, c113, c114, c115 re-read against l.122, l.144, l.149; PASS."))
rows.append(row("cards-block-119-123",
    "cards PC3-c119..c123 against L06 text and lab output",
    "course/modules/PC/PC3/cards.json c119, c120, c121, c122, c123 (changed); L06.html l.149 (Ex 4.2), l.154 (Rem 4.3), l.172-173 (Lab Part 1 docstring, changed), l.288-291 (output), l.320-333 (misconceptions)",
    "c119 (grade C): L06.html printed lines l.288 and l.290: payoff ['0',...] at F=10000 and ['100',...] at F=10100 over S_T = 8000..12000, both 'payoff the same ... True' (l.289, l.291). The lesson's changed l.172-173 says the lab checks five spot values, consistent. PASS. c121 and c123 (grade C): printed break-evens 1164.10, 1206.34, 1249.05 (L06.html printed lines l.303-305) and the misconception text l.325/333. PASS. c122 vs Example 4.2 recommendation (l.149: buy only if evidence puts units above 399300/331, about 1206.34; measure units first). PASS. c120 vs l.321 (unchanged). PASS."))
rows.append(row("cards-block-124-130",
    "cards PC3-c124..c130 against L06 and L01 text",
    "course/modules/PC/PC3/cards.json c124 (changed), c125, c126, c127; L06.html l.117 (Prop 3.1), l.154 (Rem 4.3), l.353-355 (M2), l.359-362 (M3), l.437 (R3)",
    "c124 (grade T): at 8% the break-even is 1164.1005 (l.154), 1200 > 1164.10, and NPV is strictly increasing (Prop 3.1 (ii)), so NPV(1200) > 0. rederive_r1.txt 'NPV(1200) at 8% positive: True'. PASS. c125 (M2 500/121 = 4.1322; rederive True). PASS. c126 (M3 33275/331 = 100.53; rederive True). PASS. c127 (R3: m* = 15000000/(1600*A) = 3769.8 cents, ratio 0.7540, fall 24.60%; rederive). PASS. c128..c130 (L01) byte-identical with L01.html byte-identical."))
rows.append(carry("cards-block-131-135", files_note="cards c131..c135 and cited L01/L03/lab lines"))
rows.append(carry("cards-block-136-142", files_note="cards c136..c142; L03/L04/L05 lab outputs byte-identical (run_labs PASS 9/9 this round)"))
rows.append(row("cards-block-143-150",
    "cards PC3-c143..c150 against L04, L05 and L06 text and lab output",
    "course/modules/PC/PC3/cards.json c147, c148 (changed), c149, c150; L06.html l.149 (Ex 4.2), l.154 (Rem 4.3), l.398 (E1), l.300 output; out/L06.html printed Part 2 block l.299-305",
    "c148 (grade T, break-even at 12% = 1249.05): E1 solution (l.398): A = 2.4018313, 3000/A = 1249.0469 -> 1249.05; rederive_r1.txt '3000/A(12%) = 1249.0469416785206'. PASS. c149 (grade C, sign at 200 and 1600 at 8, 10, 12%): L06.html printed lines l.303-305 (-12422903/5616776; -12513148/4894816; -12598169/4214650) and rederive: all negative at 200, positive at 1600. PASS. c150 (grade C, 4894816 at 1600 units, 10%): L06.html printed line l.300; exact 6515000000/1331 = 4894815.93, display 4894816. PASS. c147 (Ex 4.2 break-even 399300/331, about 1206.34): rederive 'u* exact 10% == 399300/331: True'. PASS. c143..c146 (L05 lab outputs) byte-identical with the L05 lab, run_labs PASS."))
rows.append(carry("cards-block-151-168", files_note="cards c151..c168 that are not in the changed set are byte-identical; the changed c151 is re-checked below"))
rows[-1] = row("cards-block-151-168",
    "cards PC3-c151..c168 against L01 to L06 text",
    "course/modules/PC/PC3/cards.json c151 (changed), c153, c154, c162-c164, c165-c167 (L06 A3-A5 l.84-86); L06.html l.412 (E3 solution, changed); L04.html l.64-65, l.76, l.83, l.88",
    "c151 (grade T, about 21.24 units per point): E3 solution l.412: unrounded (1249.0469-1164.1005)/4 = 21.2366 -> 21.24 (rederive_r1: 21.236599..., displays 21.24); 84.9464 -> 84.95 and 42.2439 / 42.7025 also re-derived. PASS. c153 (constants are choices, l.83): PASS. c154 (fill is one unit whatever the quoted size, A5 l.76 and l.83): PASS. c162, c163, c164 and c168 (L04 A2, A4, A6, Example 1.3 at l.73-88) and c165-c167 (L06 A3-A5 at l.84-86) have byte-identical cited lines: re-read, PASS. Other objects in the block byte-identical to base and their round-12 evidence stands.")
rows.append(carry("cards-block-169-171", files_note="cards c169..c171; L04.html l.74, l.93 and L05.html l.156-158 byte-identical"))
rows.append(row("cards-block-172-179",
    "cards PC3-c173..c179 against L03, L04, L05 and L06 text and lab output",
    "course/modules/PC/PC3/cards.json c174, c175, c176, c178 (changed), c179 (E2 solution changed); L04.html l.93 and l.97, l.52, l.56; L04.html l.160 (Remark 3.4 changed); L06.html l.149, l.321-333, l.404-405 (E2 changed)",
    "c174 (sigma_t: +1 buy, -1 sell, 0 no fill) vs L04 l.93: PASS. c175 (I_t signed units, I_0 = 0) vs L04 l.56 (I_0 = 0) and Proposition 2.2 proof l.107 (I_t = sum sigma_s): PASS. c176 (adverse selection, the loss a maker takes when its counterparty knows the value better) vs changed Remark 3.4 l.160: matches. PASS. c178 (Fermi bounds do not fix the sign; [200,1600] brackets 1206.34; NPV negative at 200, positive at 1600) vs Example 4.2 l.149 and misconception l.329: PASS. c179 (E2): changed solution l.405: NPV(1200) at 10% = -105000000/1331 = -78888.05 (negative, 1200 < 1206.34). rederive_r1: 'NPV at 1200, 10%: exact -105000000/1331 ... == : True'. PASS. c173, c177 byte-identical; L03 l.109 and L05 l.106 unchanged."))
rows.append(row("cards-block-180-192",
    "new cards PC3-c180..c192 (added since 5db69a9b) against the current lesson text",
    "course/modules/PC/PC3/cards.json c180..c192; L04.html l.59-65, l.93-97, l.486 (changed), l.76; L05.html l.124-132, l.136-142, l.147-152, l.339; L06.html l.75, l.111-117, l.132-137, l.149, l.311-313",
    "c180 (Prop 3.2: deque decreasing front to back, Step A l.130) PASS. c181 (at most n removals; index leaves once, Prop 3.3 proof l.142) PASS. c182 (at most 2n while-loop tests; tests <= back removals + n, back removals <= n, l.142) PASS. c183 (strictly increasing, slope mA > 0, Prop 3.1 (ii) l.117) PASS. c184 (u* = I/(mA), NPV negative below, positive above; the sign part is proved in the Corollary 3.3 proof l.137 and P2 l.380, not in part (iii)) PASS with note N2. c185 (c_t = -sigma_t f_t; A) l.93) PASS. c186 (m_t = 10000 - 10 I_(t-1), L04 l.486 'By induction on the fills'): mid_identity_r1.py checks 40000 quote turns over 2000 seeds under the Example 1.3 rule: 0 violations. PASS. c187 (cash-flow statement ends at balance-sheet cash, L06 l.75) PASS. c188 (total over the run, at most 2n; single step may cost order k, Remark 3.4 l.147; Section 4 l.339) PASS. c189 (factor of 8: each of three factors x2; 2000x1x0.1 = 200, 4000x2x0.2 = 1600) PASS. c190 (model result under A1-A5, L06 l.311) PASS. c191 (sufficient condition: whole [l,h] strictly one side of u*; zero-width at u* fixes sign at zero; positive width with end at u* does not, l.132 and l.137) PASS with note N1. c192 (fill definition: one unit at quoted price; A5 l.76; dfn in Definition 1.1 step 3 l.64) PASS with note N3."))
rows.append(row("cards-block-round3-id-carry",
    "ids are stable and the round-3 cards keep their prop references; no id removed or renumbered",
    "course/modules/PC/PC3/cards.json",
    "card_delta.py: old ids only [] (no base id removed); 20 base objects changed and 13 ids appended (PC3-c180..c192); ids strictly increasing; gaps are not defects (plans/FINAL-ARCHITECT-RULINGS.md ruling 2). PASS."))
rows.append(row("cards-atomicity",
    "each card tests one fact (BUILDER_RULES 7)",
    "course/modules/PC/PC3/cards.json (187 objects, read in full this round)",
    "Changed and new cards each ask for one quantity or one property. c184 back gives the break-even and the sign (two statements of one proposition, the sign from its (ii)/(iii) and Corollary proof); c191 back adds two clarifying sentences around one sufficient condition. Not a ruling-26 kind. PASS, with note N1/N2."))
rows.append(row("cards-c119-basis",
    "c119 basis and lab reference",
    "cards.json PC3-c119; course/modules/PC/PC3/L06.html Lab Part 1 docstring l.172-173 (changed), output l.288-291",
    "Basis 'Lab 1, Part 1 (five spot states, 8000 to 12000 cents)' matches the printed values (L06.html printed lines l.288-291). The changed docstring l.172-173 names the five spot values and Proposition 2.1; tests/labs/PC3/lab-PC3-L06-1.py l.13-15 agrees (run_labs PASS 9/9). PASS."))
rows.append(row("cards-c122-referent",
    "c122 refers to the lesson's recommendation",
    "cards.json PC3-c122; course/modules/PC/PC3/L06.html Example 4.2 (l.149), unchanged",
    "The recommendation in Example 4.2 (l.149): buy only if the firm's evidence puts units above 399300/331 (about 1206.34) at this rate, and measure units before committing. Card matches. PASS."))
rows.append(carry("cards-c146-grade", files_note="cards.json PC3-c146 and L05 lab lines 176-177, 319-324 byte-identical"))
rows.append(row("cards-misconception-coverage",
    "every misconception in each lesson has a card",
    "course/modules/PC/PC3/L04.html l.493, l.497, l.501, l.505; L05.html l.347, l.351, l.355; L06.html l.320, l.324, l.328, l.332; L01..L03 misconceptions unchanged",
    "L04 (4 misconceptions): c078, c079, c080, c081. L05 (3): c098, c099, c100. L06 (4): c120, c121, c178, c123. Each has a card with the misconception's topic. PASS."))
rows.append(row("cards-number-presence",
    "every number on a card appears in its own lesson text",
    "course/modules/PC/PC3/cards.json; L01..L06.html (stripped text)",
    "cards_scan_r1.py: every numeric token of length >= 2 in card front/back is found verbatim in its own lesson's text (miss list empty), including 1164.10, 1249.05, 1206.34, 21.24, 4894816, -12513148, 1351, 5239, 4200, 6.67. PASS."))
rows.append(row("cards-lab-printed-values",
    "card values for lab output equal the printed lesson values and the twin output",
    "tests/labs/PC3/lab-PC3-L0{1..6}-1.py; course/modules/PC/PC3/L0{1..6}.html printed blocks; ledgers/PC3/scripts/PC3-d-r1/out/twin_L0*.stdout",
    "Changed lab-printed values: L05 1351, 5239, 354, 382, 387, 200/199, 194 (L05.html printed Part 1 line l.312-331); L06 -12513148, 4894816, 1164.10, 1206.34, 1249.05, 12422903, 5616776 (L06.html printed Part 2 block l.299-305); L04 9 fills, -9950, 1, 9980, 30, 16/20100/-2/10020/60 (L04.html printed Part 1 block). All equal to the card values. run_labs PASS 9/9 (page code equals twin; expected block equals output). PASS."))
rows.append(row("cards-rederive",
    "every number in the changed cards re-derived by independent code",
    "ledgers/PC3/scripts/PC3-d-r1/rederive_r1.py -> out/rederive_r1.txt; mid_identity_r1.py -> out/mid_identity_r1.txt",
    "Fraction-exact A(8,10,12%) = 50725/19683, 3310/1331, 52725/21952; break-evens 1164.1005, 1206.3444, 1249.0469 (display 1164.10, 1206.34, 1249.05); diffs 42.24, 42.70, 42.71 (printed-difference), 84.95, 21.24; NPVs at 200/1200/1300/1600 and at 8/12%; M2 500/121; M3 33275/331; R3 0.7540, 24.6%; E2 -105000000/1331 and 1550000000/1331; mid identity 0 violations in 40000 turns. All match the cards and the lesson text. PASS."))
rows.append(row("gates-structural",
    "structural gates on the pin, run by this verifier",
    "tools/check_pages.py --unit PC3; tools/check_dag.py --all; tools/check_projects.py --all; tools/run_labs.py --unit PC3; tools/page_smoke.py --unit PC3; tools/verify_refs.py --offline; ruff; mypy; pytest -k PC3",
    "check_pages PC3: PASS (out/check_pages_PC3.txt). check_dag --all: PC3 PASS (out/check_dag.txt, exit 0). check_projects --all: 27 PASS lines, exit 0 (out/check_projects.txt). run_labs --unit PC3: PASS (9/9) (out/run_labs_PC3.txt). page_smoke --unit PC3: PASS (out/page_smoke_PC3.txt). verify_refs --offline: 560 entries, 0 problems (out/verify_refs_offline.txt). ruff check and ruff format --check tests/labs/PC3: pass (out/ruff_labs_PC3.txt). mypy --no-incremental tests/labs/PC3: Success, 9 files (out/mypy_labs_PC3.txt). pytest -q -k PC3: 9 passed, exit 0 (out/pytest_k_PC3.txt). Each twin run alone under python -I -W error: exit 0 (out/twin_L0*.exit). Not run: full pytest, render_curriculum, build_site --check, fetch_data --check, live verify_refs, run_graders and mutate_graders (no grader change in slice d)."))
rows.append(row("cards-grade-agreement",
    "every graded card agrees with its lesson's key-results table",
    "course/modules/PC/PC3/cards.json; L04.html key results l.620-627; L05.html l.472-477; L06.html l.449-454",
    "L04 table: c069 T, c071 T, c073 T, c075 C (lab-based) agree with the card grades. L05 table: c087 T, c088 T, c090 T, c091 T, c095 T, c101 C agree. L06 table: c102 T, c107 T, c108 T, c110 T, c111 T, c147 T agree, and the changed table row (l.453 'positive factor ranges') agrees with c111 T. No card's grade is higher than its table row. PASS."))
rows.append(carry("cards-plan-grade-c043", files_note="cards.json PC3-c043 byte-identical; plans/PC3-build-plan.md §9 (l.519-531) is outside the diff hunks (l.319, l.406-428)"))
rows.append(row("cards-process-words",
    "no process words in learner text",
    "course/modules/PC/PC3/cards.json (187 objects); L04..L06.html changed hunks",
    "Word scan over all card front/back/basis for round, ruling, verifier, fixer, builder, architect, delta, pin, closing, audit, blocker, FAIL, PASS, sweep, mutant: no process word; the only regex hit is the English verb 'fail' in c123 ('a recommendation that holds at one rate can fail at another'). Changed lesson hunks read in full: no process words. PASS."))
rows.append(row("cards-simulated-label",
    "SIMULATED results carry the label; generated inputs are not called data",
    "course/modules/PC/PC3/cards.json c067, c077, c137..c141; L04.html l.182-186 (SIMULATED header), L05.html l.163-166 (generated input, not data), L06.html l.158-168",
    "c067 (seed 0, SIMULATED) and the seed-0 cards c137..c141 keep the SIMULATED label, and L04 l.182 and l.185 say so. The L05 counts are on a generated input, labelled 'generated input and not data' (l.163). The L06 values use assumed inputs (l.162). PASS."))
rows.append(row("cards-notation",
    "no registered symbol reused with another meaning (notation/notation.json)",
    "notation/notation.json (symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q); changed cards and changed lesson hunks",
    "Scan of the changed and new cards and changed hunks: none of the registered symbols appears. Program-unregistered letters are local (L04 I_t inventory and I_0; L06 I outlay, A annuity factor, u units, m margin, h product bound; L04 h half-spread): each is defined in its own lesson. Note N4: L06 uses A for the annuity factor while A1-A5 are assumption labels; A is not a registered symbol, so this is not a notation FAIL. PASS."))
rows.append(row("cards-block-titles",
    "block titles quoted on cards match the lesson headings",
    "cards.json c005, c092, c110, c112, c124, c173..c184, c191, c192; L04.html l.59, l.122, l.494; L05.html l.124, l.136, l.146; L06.html l.111, l.131, l.143, l.149",
    "Headings checked: Proposition 3.2 (correctness of the deque) l.124 and Proposition 3.3 (total work of the deque) l.136 match exactly. Quoted titles that are truncations of a heading: c110, c183, c184 'Proposition 3.1 (linear net present value)' against l.111 'Proposition 3.1 (linear net present value and its break-even)'; c112 'Corollary 3.3 (a range that straddles the break-even)' against l.131 'Corollary 3.3 (a range that straddles the break-even does not fix the sign)'. Not a heading: c191 'Corollary 3.3 (the sign is fixed on one side)' (no such heading exists), and c192 'Definition 1.1 (fill)' (the fill definition is step 3 of Definition 1.1, l.64). These are presentation locators, not one of the ruling-26 FAIL kinds; recorded as non-blocking note N1 and N3 for a LOW fixer pass. PASS under ruling 26."))
rows.append(row("lesson-numbers-prose",
    "prose numbers in the lessons that the cards quote agree with unrounded values",
    "L04.html l.160, l.494; L06.html l.149, l.154, l.306, l.312, l.324-325, l.398, l.405, l.412, l.437, l.453",
    "L04 l.160/494: (1-p)h = h/2 at p=1/2 = quarter of 2h. PASS. L06 l.154: break-evens 1164.1005, 1206.3444, 1249.0469 (exact 1164.100542, 1206.344411, 1249.046942); 42.24 lower at 8% and 42.70 higher at 12% (from unrounded differences 42.2439, 42.7025); A = 2.5770970, 2.4868520, 2.4018313; 3000 = 15000000/5000; NPV negative at 200 and positive at 1600 at all three rates (rederive). PASS. L06 l.306: printed differences 42.24 and 42.71 (1206.34-1164.10, 1249.05-1206.34) and unrounded 42.24, 42.70. PASS. L06 l.324-325: 21.24 per point = (1249.0469-1164.1005)/4 = 21.2366. PASS. L06 l.398 E1, l.405 E2 (-78888.05, 1164537.94), l.412 E3 (84.9464 -> 84.95, 21.2366 -> 21.24, 42.2439, 42.7025 -> 42.70, 42.71 is not the answer): all re-derived. PASS. L06 l.437 R3: m* = 3769.8 cents, 0.7540 of 5000, fall 24.6%. PASS."))
rows.append(row("lesson-scope-words",
    "scope words in cards claim no more than the proofs and labs show",
    "cards.json (changed and new objects); L04.html l.64-65, l.485-486; L05.html l.52, l.339; L06.html l.154, l.172-173, l.311-313",
    "'every' and 'all' and 'only' in changed cards and changed hunks: c053 'every rule' (five rules computed by two methods, lab l.278); c119 'each of five spot states' (lab prints five); L06 l.173 'The lab checks this at five spot values; Proposition 2.1 covers every spot state' (Prop 2.1 (i) l.92-97 argument does not depend on S_tau); L04 l.64 'only when A5 allows it' (A5 l.76); L05 l.339 'average over the run at most two per step' (Prop 3.3). No scope word exceeds its proof or lab. PASS."))
rows.append(row("lesson-dag-and-attribution",
    "uses lines and attributions, DAG (check_dag) and no unread citation",
    "course/modules/PC/PC3/L04.html l.38, l.64-65 (link to the unit project), L05.html l.52, L06.html l.52, l.56, l.75; check_dag --all",
    "check_dag PC3: PASS. Changed text references only this unit's own items (Definition 1.3, Definition 3.1, Definition 4.1, Proposition 3.1, Remark 4.3, the unit project link) and the prerequisite articulation concept already in L06 Uses. No new citation was added; each lesson keeps 'cites no registry source' (L04 l.727, L05 l.567, L06 l.538). PASS."))
rows.append(carry("lesson-L02-introduces-metadata", files_note="course/modules/PC/PC3/L02.html byte-identical"))
rows.append(carry("adjacent-lesson-numbers", files_note="cards c017, c020, c043 byte-identical; L02.html l.57, l.72 and L03.html Definition 3.5 byte-identical"))

assert len({r["id"] for r in rows}) == len(rows), "duplicate row ids"
missing = set(base_rows) - {r["id"] for r in rows}
assert not missing, f"base ids dropped: {missing}"
notes = (
 "Slice d closing delta, round 1 (rulings 30 and 37). Base: round-12 fragment (pin 5db69a9b, 44 rows, all PASS). "
 "Delta 5db69a9b..95f3f8cb over the slice paths: course/modules/PC/PC3/cards.json (20 base objects changed: c005, c050, c053, c055, c062, c067, c081, c090, c091, c096, c097, c110, c112, c116, c123, c124, c148, c174, c175, c178; 13 new objects c180..c192); L04.html (l.64-65, l.72, l.83, l.127 new paragraph, l.160, l.485-486, l.494); L05.html (l.7, l.52, l.508, l.511 quiz); L06.html (l.52, l.132, l.154, l.172-173, l.305-306, l.311-313, l.324-325, l.397-412, l.430, l.453); tests/labs/PC3/lab-PC3-L06-1.py (docstring l.13-15, mirrored in the page). "
 "Byte-identical since the base pin: L01.html, L02.html, L03.html, lab-PC3-L01..L05 twins. Outside slice d (not verified here): course/modules/PC/PC3/project.html, grader/test_project.py, plans/PC3-build-plan.md (hunks at l.319, l.406-428 are project sections; §9 unchanged). "
 "Rows: every base row re-verified or carried; the base had no non-PASS row. Rows re-verified: all with a changed or new card or a changed cited hunk; carried (prefix 'Carried from round 12'): cards-block-011-020, 021-030, 031-040, 131-135, 136-142, 169-171, cards-c146-grade, cards-plan-grade-c043, lesson-L02-introduces-metadata, adjacent-lesson-numbers. "
 "Mutants: none authored (ruling 37); slice d holds no grader. The base's round-11 FAIL (c092 vs L05 l.147) and the round-12 note (L05 quiz 'removes k-1 entries') are both closed in this pin: L05 l.508 and l.511 now say k. "
 "Non-blocking notes (not ruling-26 kinds; no row set to FAIL): "
 "N1 titles: c191 quotes 'Corollary 3.3 (the sign is fixed on one side)', which is not a lesson heading; c110, c183, c184 and c112 quote truncated headings (L06 l.111, l.131); a LOW presentation fix would align them. "
 "N2 basis: c184 basis 'proof on the page (part iii)' — part (iii) (L06 l.117) gives only the zero; the sign (negative below, positive above u*) is proved in the Corollary 3.3 proof (l.137) and in P2 (l.380). The claim is supported; the pointer should name l.137. "
 "N3 locator: c192 'Definition 1.1 (fill)' — 'fill' is defined as a dfn in Definition 1.1 step 3 (l.64) and fixed by A5 (l.76); the locator names no heading. "
 "N4 notation (local, not a FAIL): L06 uses A for the annuity factor while A1..A5 are assumption labels; A is not registered in notation/notation.json. "
 "N5 wording: L04 l.134 'not claimed for a quote that depends on the public history' is a correct restriction (Proposition 3.1 needs a fixed quote, H2); c081 is consistent with it; no action. "
 "Not run: full pytest suite (ran pytest -k PC3 only), render_curriculum.py, build_site.py --check, fetch_data.py --check, live verify_refs, run_graders.py and mutate_graders.py (slice d has no grader; grader changed only in the project slice), check_pages --all (ran --unit PC3). "
 "Gate outputs: ledgers/PC3/scripts/PC3-d-r1/out/."
)
fragment = {
 "unit": "PC3",
 "slice": "PC3-d",
 "round": 1,
 "verifier": "Claude Haiku 5.5, independent verifier, unit PC3 slice d closing delta (rulings 30 and 37), round 1; did not build PC3",
 "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
 "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (round-12 pin; round-12 fragment /Users/billyribeiro/.fanout/frags/E-PC3-d.round12.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-PC3-d",
 "scratch": "/tmp/pc3d_r1 (stripped lesson dumps L01.txt..L06.txt)",
 "verified_at": "2026-11-09T16:40:00+00:00",
 "verdict": "PASS",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": notes,
 "summary": {"rows": len(rows), "pass": len(rows), "fail": 0, "unverifiable": 0, "mutants_killed": 0, "mutants": 0},
}
out = ROOT / "ledgers/PC3/PC3-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows))
