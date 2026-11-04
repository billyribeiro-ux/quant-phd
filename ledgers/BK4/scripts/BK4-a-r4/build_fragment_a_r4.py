import json, subprocess
SC = "ledgers/BK4/scripts/BK4-a-r4/"
R = {}
def row(i, check, loc, status, ev):
    R[i] = dict(id=i, check=check, location=loc, status=status, evidence=ev)

# ---- hub index.html (byte-identical since 67a2d13; re-read in full this round) ----
row("BK4a-hub-hours-arithmetic","2.9-hours","index.html:29,42,164-176; L01/L02/L03 data-hours",
    "PASS","index.html:29 data-hours-lessons=\"35\" data-hours-project=\"15\"; :42 '35 h lessons · 15 h project (30% of the 50 module hours)'; hours table rows 2,2,3,3,2,2,1 sum to 15 (index.html:169-176, Total 15); L01/L02/L03 carry data-hours=\"7\" (L0x.html:2) and eyebrow '7 study hours'; 5 x 7 = 35; 15/50 = 30%.")
row("BK4a-hub-placement-arithmetic","2.9-structure","index.html:71-73,76-131",
    "PASS","data-mastery=\"0.8\" (index.html:71); 8 items (Pq1-Pq8); 0.8 x 8 = 6.4 so 7 correct needed; 6/8 = 75%, 7/8 = 87.5% (index.html:73). Six prerequisite items Pq1-Pq6 (M1,M2,E1,P0.1,FC1); skill items Pq7 (index.html:121) and Pq8 (index.html:126) with data-skill.")
row("BK4a-hub-placement-keys","2.9-prose-numbers","index.html:79,84,89,97,107,116,121,129",
    "PASS","Re-derived: 110/1.1 = 100 (data-correct option 100.00, index.html:79); 1+1/2+1/4 = 1.75 (data-answer=\"1.75\", index.html:84); lim 2x at 3 = 6 (data-answer=\"6\", :89); Bertrand price = c (:97); grade C for single sample (:107-108); clearing precedes settlement in FC1 lifecycle (:116; FC1 L05 line 63 gives order entry, matching, trade capture, clearing, settlement, position update); rung 1 min(120-100,50)=20 (data-answer=\"20\", :121); rung 2 remainder 1 cent to first surviving member (:129).")
row("BK4a-hub-prereq-chain","2.9-structure","index.html:35,61; curriculum/02-economics-finance-core.yaml:367,1075; yaml:22; closure",
    "PASS","yaml:1075 BK4 prereqs [FC1]; yaml:367 FC1 prereqs [P0.1, E1]; yaml:22 E1 prereqs [M2]; M1 prereqs [P0.1] (curriculum/01-foundations.yaml:91); tools/coursekit prerequisite_closure('BK4') = ['E1','FC1','M1','M2','P0.1'] (run this round). index.html:61 chain statement matches.")
row("BK4a-hub-P0.1-link","2.9-structure","index.html:35",
    "PASS","index.html:35 states 'P0.1 is not yet released in this program'; course/modules/P/ does not exist (checked this round), so P0.1 is not built; the disclosure is accurate and no link to P0.1 is made.")
row("BK4a-hub-financial-intermediary","2.9-prose","index.html:63-64",
    "PASS","index.html:63 'From FC1: clearing and settlement, the trade lifecycle, bank money creation' with concept links to ../../../concepts.html#...; FC1 concepts are in the closure (yaml:381-382 clearing-and-settlement, trade-lifecycle; bank-money-creation yaml:373).")
row("BK4a-hub-bertrand-trade-fee","2.9-prose","index.html:64 against index.html:95-101",
    "PASS","index.html:64 'Bertrand competition, which placement item 4 uses' matches item Pq4 (index.html:94-101: correct option marginal cost, explanation 'Bertrand outcome sets price equal to marginal cost').")
row("BK4a-hub-concept-anchors","2.9-concepts","index.html:63-66; L01.html:37,59,64; L02.html:51,64,81; L03.html:37,67,134",
    "PASS","Each dfn with data-concept appears once: L01 payment-system (L01.html:59), settlement-cycle (:64); L02 central-counterparty, multilateral-netting (L02.html:64,81); L03 ccp-default-waterfall, margin-cover (L03.html:67,134 per grep). Hub links to FC1/E1/M1/M2 concepts use concepts.html anchors. Links L02->L01#def-payment-system and L03->L02#def-* exist. check_dag BK4 PASS (ledgers/BK4/scripts/BK4-a-r4/check_dag.out).")
row("BK4a-hub-ladder-vs-project","2.9-structure","index.html:154,156; course/modules/BK/BK4/project.html:45,54",
    "PASS","index.html:154 worked example 'four-member clearing house, seeded SIMULATED set of 40 scenario losses' vs project.html:45 (rung 1, four-member, 40 scenario losses in project text); index.html:156 'clearing_house.py ... autograder checks ... seeded SIMULATED instances' vs project.html:47,201 (clearing_house.py). index.html:173 'seeds 0 to 9' matches project.html ('seeds 0 to 9') -- project-grader seed range is slice E's concern.")
row("BK4a-hub-data-status","2.9-data","index.html:37,184; course/modules/BK/BK4/*.html; tools/data_sources.yaml:19,53,9",
    "PASS","index.html:37 'Data: none' and :184 'No data is used in BK4'; grep for open(/urllib/requests/fetch( in the four pages and three twins: 0 hits (run this round). course/assets/data/market/MANIFEST.json datasets are fx_daily, fx_monthly, ust_daily only (run this round) -- no payment, settlement, clearing or stablecoin series, so index.html:184 is true.")
row("BK4a-hub-reading-list","2.9-references","index.html:186-194,193; references/references.json:2853 (bisndcpmi), :7411 (duffie2011central), :2815 (bisndbasel)",
    "PASS","index.html:190-191 data-cite duffie2011central and bisndcpmi, both keys present (references.json:7411, :2853). Registry record duffie2011central: authors Duffie, Zhu; title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?'; Review of Asset Pricing Studies 2011 (matches the index's 'Duffie and Zhu (2011)'). bisndcpmi is issuer-level (verified_by issuer), so index.html:193 'index-level only' is correct. SEC T+1 rule: no sec.gov key in references.json (grep count 0, this round). verify_refs --offline: 560 entries, 0 problems (ledgers/BK4/scripts/BK4-a-r4/verify_refs_offline.out).")
row("BK4a-hub-process-words","2.12-process-words","index.html (visible text)",
    "PASS","Stripped visible text of index.html (ledgers/BK4/scripts/BK4-a-r4/index.txt) and of L01-L03 scanned for build, builder, round, verifier, REQUESTS, unit report: zero hits. check_pages BK4 PASS.")
row("BK4a-hub-settlement-framing","2.9-prose / B1 settlement facts","index.html:33",
    "FAIL",
    "index.html:33 (visible text): 'A trade is settled when the money for it has moved, and the money moves through payment systems and clearing houses.' This is a real-world settlement statement about how money moves, presented as fact in the hub. Plan 2.2 and Architect default: settlement and market facts are stated only from an admitted source (B1); the registry has no settlement-mechanics record (references.json: no sec.gov key; no CCP-waterfall or settlement-process source). Only the model's own rules may be stated. LOW severity: it is a framing sentence, not a number. FIX: qualify as the model's rule, e.g. 'In this unit's model, a trade settles when its payment has moved between accounts, and the payment systems and clearing houses are defined in Lessons 1 and 2.' (index.html:33).")

# ---- L01 (changed since 67a2d13 at lines 115,313,330,370,377; re-verified in full) ----
row("BK4a-L01-numbers","2.1-numbers","L01.html:269-286; L01.html:409; L01.html:55",
    "PASS","Re-derived by ledgers/BK4/scripts/BK4-a-r4/rederive_a_r4.py (independent: seeded RNG re-drawn; RTGS peak need by binary search on the feasibility of o_i + S_{i,k} >= 0; no reuse of lab functions): Bank A need 112500, net +379800, debit 0; Bank B need 1533900, net -1533900, debit 1533900; Bank C need 0, net +1154100, debit 0; gross 2841600; DNS moved 1533900; ratio 5113/9472 = 0.53980152 -> 0.5398 (4 dp) and 53.98 % (L01.html:286, :409). All match the printed Lab 1 output (ledgers/BK4/scripts/BK4-a-r4/pure_L01.txt).")
row("BK4a-L01-prop-2.2-2.4","2.4-mathematics","L01.html:84-111 (Prop 2.2, 2.3, 2.4 with proofs); L01.html:115-126",
    "PASS","Prop 2.2 proof (L01.html:90): feasible o_i >= max(0,-mu) exactly; least element max(0,-mu) = Need. Prop 2.3 proof (:100): each payment contributes a - a; s != r cited but not needed (see BK4a-L01-A2-forward-ref / P1). Prop 2.4 proof (:110): k=m is in the minimum, so mu <= Net and Need >= Debit; strictness via Example 2.6 (Need 100, Debit 50, re-derived). Remark 2.5 now reads 'can' (L01.html:115), which the counterexample-free order statement supports: changing the sending order can change the running minimum (Example 2.6 vs Remark 2.7 re-derived: A need 100 -> 50).")
row("BK4a-L01-P2-iff","2.4-mathematics","L01.html:375-377",
    "PASS","Problem P2 (L01.html:375-377): Need = Debit iff min S >= 0 or S_m = min S. Re-derived by cases on mu >= 0; mu < 0 with S_m = mu; mu < 0 with S_m > mu (Need = -mu > 0, Debit < -mu so unequal). Hypotheses listed (mu <= S_m, Prop 2.2 under A1-A2, Section 2 definitions) match the argument. Raw HTML at L01.html:377 read (the '<' is text, not a tag).")
row("BK4a-L01-examples-remarks","2.4-mathematics","L01.html:119-126; L01.html:115-118",
    "PASS","Round-3 FAIL cleared: L01.html:115 now reads 'The peak need can, ... The order of payments can change the peak need, and so it can change the gap'. Example 2.6 (L01.html:120) re-derived: S_A = 0,-100,-100,-50; S_B = 0,100,20,20; S_C = 0,0,80,30; minima -100,0,0; Net -50,20,30 (sum 0); debit A 50; gross 230 dollars. Remark 2.7 (:125): S_A = 0,50,-50,-50, Need_A 50 (re-derived).")
row("BK4a-L01-problems-M-P-E-R","2.4-mathematics","L01.html:343-352, 357-359, 367-370, 381-384, 393-402, 407-409, 417-428, 420",
    "PASS","Round-3 FAIL cleared. P1 (L01.html:368-370) now states the part used: 'The proof uses only A1 in the form that the day's payments form a fixed finite list'. Re-derived: M1 need 200 debit 200 (:345); M2 need 200 debit 100 (:352); M3 need 30 debit 20 (:359); P3 scaling (:384) correct; E1 bank B 1533900 (:395); E2 1 of 3 banks, bank A 112500 vs 0 (:402); E3 ratio 53.98 % of gross (:409); R1 (:420) inflows-first order attains equality; R2 (:427) sum Debit = sum max(0,Net) <= gross; R3 (:434) cycle: Need_A 100, all debits 0 (re-derived).")
row("BK4a-L01-remark-3.1-order","2.4-mathematics","L01.html:300",
    "PASS","Remark 3.1 (L01.html:300): inflows first gives running sums rising to total inflow then falling monotonically to Net_i; running min over k (k=0 included) = min(0,Net_i); Need = max(0,-Net_i) = Debit. Re-derived.")
row("BK4a-L01-R3","2.4-mathematics","L01.html:432-434",
    "PASS","R3 (cycle A->B->C->A, 100 dollars each): nets all 0, debits all 0; A's running sums 0,-100,-100,0 so Need_A 100 dollars (re-derived by rederive_a_r4.py-equivalent check in this round's review).")
row("BK4a-L01-remark-2.8","2.9-prose-numbers","L01.html:291 against lab output L01.html:274",
    "PASS","Remark 2.8 (L01.html:291) describes Lab 1 Part B (inequality per bank) and Part C (zero sum); matches printed output lines 274-275 of the page and twin_L01 output (ledgers/BK4/scripts/BK4-a-r4/pure_L01.txt).")
row("BK4a-L01-interp-three-inequalities","2.9-prose-numbers","L01.html:286",
    "PASS","Interpretation paragraph (L01.html:286): Bank B 1533900 = its debit (re-derived); Bank A net credit 379800, debit 0, need 112500; Bank C nothing; 1533900 and 2841600 printed; ratio 0.5398 from 0.53980152 (re-derived); 'The lab does not print that ratio' correct (lab prints only the two cents amounts).")
row("BK4a-L01-misconception-1","2.9-prose-numbers","L01.html:322 against lab Part B L01.html:269-271",
    "PASS","Misconception 'Net settlement removes the need for liquidity' (L01.html:322): Bank A need 112500 vs debit 0 (net receiver, need falls); Bank B need = debit = 1533900 (not removed). Printed day matches (pure_L01.txt, Part B).")
row("BK4a-L01-misconceptions-2-3","2.9-prose-numbers","L01.html:321-330",
    "PASS","L01.html:326: net receiver A has net +379800, debit 0, RTGS need 112500, strict Prop 2.4 (verified). L01.html:330: Remark 2.7 A need 100 -> 50, debit 50 unchanged (verified). 'only the peak need can depend on order' matches Remark 2.5 wording.")
row("BK4a-L01-quiz","2.3-grades/quiz","L01.html:458-537",
    "PASS","Quiz answers checked against data-correct/data-answer: 200 dollars (:465; net -200 -> debit 200); need 200 (data-answer 200, :471); 'at least' (:479); need 200 after doubling (:485); 50 after payment 3 first (:490); Zero (:499); 0 dollars (:508); 'one business day, a lab parameter' (:517); 28416 dollars (:522; 2841600 cents = 28416 dollars); 'named, statement not made' (:531). Each explanation agrees with the lesson.")
row("BK4a-L01-lab-twin","2.5-labs","L01.html:128-287; tests/labs/BK4/lab-BK4-L01-1.py",
    "PASS","Page code block equals the twin byte-for-byte after rstrip (ledgers/BK4/scripts/BK4-a-r4/lab_block_compare.py: 'CODE block equals twin'); expected block (class=expected, :254-285) equals the pure run output of python3 -I -W error on the twin (exit 0, empty stderr: twin_L01.err 0 bytes). Twin docstring and output consistent with lesson wording (SIMULATED, integer cents, Part D lag as a parameter).")
row("BK4a-L01-notation","2.3-notation","L01.html, L02.html, L03.html; notation/notation.json",
    "PASS","Math extracted from all pages (ledgers/BK4/scripts/BK4-a-r4/math_symbols.py). Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur (forbidden-hits 0, bare-T-hits 0). No \\mathbb{R} (macro \\R used per FINAL 1). T+1 appears only in prose (L01 x3), not as a symbol.")
row("BK4a-L01-dag-defs","2.5-dfn","L01.html:37,59,64; index.html:68",
    "PASS","dfn ids: L01 def-payment-system (L01.html:59), def-settlement-cycle (:64); Uses/Introduces lines at :37-38; index.html:68 'defined in Lesson 1' matches. Plain dfn for net debit, RTGS, DNS, peak need, etc. (no data-concept); check_dag PASS.")
row("BK4a-L01-why-words","2.12-process-words","L01.html:51",
    "PASS","Why-it-matters paragraph (L01.html:51) is learner text: no process words (scan zero hits); it states the lab checks 'on a seeded SIMULATED day'.")
row("BK4a-L01-structure","2.7-structure","L01.html:34-545",
    "PASS","check_pages BK4 L01 PASS (ledgers/BK4/scripts/BK4-a-r4/check_pages_L01.out); 3 misconceptions (:321,325,329); problem sets Mechanics M1-M3, Proof P1-P3, Empirical E1-E3, Research R1-R3 with solutions; key-results table; quiz 10 items; hours data-hours 7.")
row("BK4a-L01-grades","2.3-grades","L01.html:43-48, 84, 94, 104, 446-452",
    "PASS","Legend (:43-48) T/replicated/published/working paper/lore/refuted; Props 2.2-2.4 graded T with proofs; Key results rows 446-452: T rows proved in-page, C rows name Lab 1 Parts B/C with SIMULATED and one seed (:451-452). No B or D claims.")
row("BK4a-L01-FC1-claim","2.9-attribution","L01.html:55",
    "PASS","'FC1 Lesson 5 followed one trade through that sequence': course/modules/FC/FC1/L05.html is 'Clearing, Settlement and the Trade Lifecycle' and its Lab 1 traces one seeded trade through the states (FC1 L05 Definition 1.2 and Lab 1 Part 1). Verified this round.")
row("BK4a-L01-canon-breaks-wording","2.9-prose","L01.html:308-313",
    "PASS","Canon-break list (:310-313): 'simplified outside it'; 'The lesson states no finding about any such design'; 'The lesson does not say which real system uses which design ... the lesson states no fact about which design any real system uses; the two designs are defined in Definitions 1.1 and 2.1'. No 'only' claim without a computation (round-3 defect cleared).")

# ---- L02 (changed at lines 390, 392, 421) ----
row("BK4a-L02-prop-2.2","2.4-mathematics","L02.html:85-99",
    "PASS","Prop 2.2 (a)-(d) re-proved (L02.html:95-98): (a) each trade enters one Rec and one Pay (A2); (b) sum n_i = G - G = 0; (c) max(0,x)-max(0,-x)=x summed; (d) A <= G via max(0,n_i) <= Rec_i. Random check of 3000 trade sets (rederive_a_r4.py): A in [0,G], sum max(0,-n)=A, zero mismatches.")
row("BK4a-L02-prop-2.3-title","2.9-prose","L02.html:102-103",
    "PASS","Title 'no netting reduction is achieved exactly when no member both receives and pays' matches the statement A = G iff each member has Rec=0 or Pay=0; random check of 3000 cases: zero mismatches.")
row("BK4a-L02-prop-2.3-proof","2.4-mathematics","L02.html:106-109; L02.html:348-349 (P2)",
    "PASS","Proof (L02.html:108): three cases (Rec=0; Rec>0,Pay=0; Rec>0,Pay>0) re-derived and correct; 'strictly smaller' in the last case because Rec-Pay < Rec and 0 < Rec. P2 (:349) hypotheses Pay>=0, Rec>=0, G=sum Rec stated.")
row("BK4a-L02-example-2.4","2.4-numbers","L02.html:113; L02.html:270; L02.html:294",
    "PASS","Example 2.4 re-derived: Rec (50,100,80), Pay (100,80,50), n (-50,20,30), A 50, G 230, reduction 180, floor(10000*180/230)=7826 (7826.08...). L02.html:294 'amount paid after netting is 50 dollars against 230' correct.")
row("BK4a-L02-lab-claims","2.5-labs","L02.html:123, 127; tests/labs/BK4/lab-BK4-L02-1.py main()",
    "PASS","Lab 1 prints checks: receivables sum to gross (True), net obligations sum to zero (True), payments in = payments out (True), after netting <= gross (True). Expected text (L02.html:127) lists exactly these four checks; main() called at top level (twin line 113).")
row("BK4a-L02-lab-numbers","2.5-numbers","L02.html:241-269 (expected); L02.html:270 (interpretation); L02.html:365-381 (E1-E3)",
    "PASS","Independent re-derivation of the seed-2026 trade set (rederive_a_r4.py): G=7596300; Rec (314500,2067800,3340300,1873700); Pay (3941500,314500,0,3340300); n (-3627000,+1753300,+3340300,-1466600); A=5093600; reduction 2502700; floor(10000*2502700/7596300)=3294 (3294.63). All equal the printed output (pure_L02.txt). L02.html:270 sentences verified; E1 sum 2502700+5093600=7596300 verified.")
row("BK4a-L02-lab-numbering","2.9-prose","L02.html:121,123,125-127,270 and section id",
    "PASS","Lab numbering 'Lab 1' consistent with twin lab-BK4-L02-1 and Parts A-D printed; section 3 heading and section ids match.")
row("BK4a-L02-attribution","2.3-attribution","L02.html:277,285,425,514; references/references.json:7411-7416",
    "PASS","Duffie and Zhu (2011) cited at paper level only (data-cite duffie2011central, L02.html:277). Registry title is exactly the question stated (references.json:7411-7416, title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?'); the page states no finding of the paper (L02.html:277, 285, 425 C 'question only'). No page, table or equation of the paper is typed.")
row("BK4a-L02-canon-misconceptions","2.9-prose-numbers","L02.html:280-285, 293-302",
    "PASS","Netted-amount zero iff all n_i = 0 (re-derived: A=0 iff all n_i<=0 and sum 0). 'CCP cannot fail' misconception answer (:302) correct: sum zero is bookkeeping and holds whether or not a member defaults.")
row("BK4a-L02-problems","2.4-mathematics","L02.html:315-331 (M1-M3), 340-356 (P1-P3), 365-381 (E1-E3), 390-406 (R1-R3)",
    "PASS","Round-3 FAIL cleared. R1 (L02.html:390) now states 'under Assumption 1.3 with G > 0'; solution (:392) divides by G. M1 re-derived: n (-10,-20,50,-20), A 50, G 180, floor 7222 (7222.2...). M2: 7826, equal ratio. M3: n (-200,100,100), A 200 = G, 0 bps. P1 (:342) A2 and A1 used. P2 (:349). P3 (:356) cycle: zero nets, A=0, 10000 bps (k=2..6 verified). E1-E3 verified (E3 members 1,2,4 both receive and pay; member 3 only receives). R2 (:399) X and Y: A 100 both, G 100 and 200 dollars (re-derived). R3 (:406) changes by at most a (argument checked).")
row("BK4a-L02-key-results","2.3-grades","L02.html:416-425",
    "PASS","Round-3 FAIL cleared: row 421 now reads 'Proved in Problem R1 under Assumption 1.3 with G > 0' (L02.html:421). Row 425 graded C, 'Question only' for Duffie and Zhu. Other T rows proved on page.")
row("BK4a-L02-quiz","2.3-grades/quiz","L02.html:432-510",
    "PASS","Quiz answers vs data-correct/data-answer: plus 20 (:439); 50 (:444); They sum to zero (:453); 7826 (:458); When no member both receives and pays (:467); 100 (:472); 'No, the identities set the amounts and a payment system moves them' (:481); 'No, bookkeeping identity holds whether or not a member fails' (:490); 50936 dollars (:495; 5093600 cents = 50936 dollars); Zero (:504). Explanations agree.")
row("BK4a-L02-lab-twin","2.5-labs","L02.html:121-271; tests/labs/BK4/lab-BK4-L02-1.py",
    "PASS","Page code block equals twin after rstrip ('CODE block equals twin'); expected block equals pure run output (lab_block_compare.py); twin exit 0 under python3 -I -W error with empty stderr (twin_L02.err 0 bytes).")
row("BK4a-L02-why-structure","2.7-structure","L02.html:34-518",
    "PASS","check_pages BK4 L02 PASS; 3 misconceptions; problem sets with M/P/E/R; key results; quiz 10 items; references section (:514) states the one paper-level registry cite. page_smoke L02 PASS (Pyodide runtime, page_smoke.out).")

# ---- L03 (changed at lines 55, 421) ----
row("BK4a-L03-legend","2.9-grades","L03.html:43-48",
    "PASS","Grade legend identical to the other pages (T/replicated/published/working paper/lore/refuted).")
row("BK4a-L03-four-resources","2.9-prose","L03.html:55",
    "PASS","Round-3 FAIL cleared by the permitted option: L03.html:55 now reads 'Section 3 names the close-out part of that limit'. Section 3 (L03.html:418) names the close-out limit. The netting part of the limit is stated only in the L03.html:55 sentence itself, not elaborated as a canon break; no false pointer remains. Count 'Three resources' matches Definition 1.1 (margin, default fund, CCP capital; survivors pay the residual, :66-73) -- verified against lab output.")
row("BK4a-L03-notation-d","2.3-notation","L03.html:61,69-70,100,139,480-482",
    "PASS","Symbols L, IM, DF, K, D, Z, u, x_i, ell, S, L_s, M, c(M), t, k, n^+ are local and defined on first use (L03.html:55-61, 67-73, 130-146). No registered symbol reused (math extraction: forbidden 0). d not used in L03.")
row("BK4a-L03-def-props-1.2-1.3","2.4-mathematics","L03.html:66-96",
    "PASS","Definition 1.1 layers and survivor rule re-implemented independently (rederive_a_r4.py): 20000 random cases of Prop 1.2 conservation, 0 mismatches; Prop 1.3 (x_i <= DF_i, 0 <= ell <= n+ - 1) 0 mismatches; Remark 1.4 0 mismatches. Proof of Prop 1.3 (:95) checked: fractional parts in [0,1), ell < n+, integer => ell <= n+-1; x_i+1 <= DF_i for DF_i>0.")
row("BK4a-L03-remark-1.4","2.4-mathematics","L03.html:100-101",
    "PASS","Remark 1.4 (a2>0 => a1=IM; a3>0 => a2=DF; Z>0 => a3=K) proved and random-checked (0 mismatches).")
row("BK4a-L03-example-1.5","2.5-numbers","L03.html:104-121; L03.html:108-117 table; lab Part A1 output",
    "PASS","Example 1.5 table (eight rows: 80,120,170,180,181,200,205,300) re-derived with an independent waterfall: margin/DF/capital/M1/M2/uncovered rows match exactly (e.g. 181 -> M1 1; 205 -> 10,15; 300 -> 40,60,uncovered 20). Table header matches. Lab Part A1 output identical (pure_L03.txt).")
row("BK4a-L03-example-1.6","2.5-numbers","L03.html:124-126",
    "PASS","Example 1.6: residual 1 -> member 1 pays 1; residual 2 -> members 1 and 2 pay 1 each; matches lab Part A2 (pure_L03.txt) and independent re-derivation.")
row("BK4a-L03-def-2.1-prop-2.3","2.4-mathematics","L03.html:132-165",
    "PASS","Definition 2.1 (cover floor(10000 c/S), basis = count, not dollar-weighted) and Prop 2.3 parts 1-3 proved (L03.html:162-164) and checked: 400 random (S, losses, t) cases brute-force vs order statistic, 0 mismatches; k in [1,S]; cover(L_(k)) >= t and cover(L_(k)-1) < t.")
row("BK4a-L03-cor-2.4-ex-2.5","2.4-numbers","L03.html:167-180; L03.html:404-409 (lab Part B)",
    "PASS","Cor 2.4 monotone (proof :173) correct. Example 2.5: S=200, 9900*200/10000 = 198 exactly -> k=198; 9975 -> 199.5 -> k=200 (re-derived). Lab Part B: sized 2961 (k=198) and 2992 (k=200); brute-force 2961 and 2992, both True (pure_L03.txt; re-derived with the seed).")
row("BK4a-L03-R1-note","2.4-mathematics","L03.html:529-533",
    "PASS","R1 (real margins): Prop 2.3 part 2 argument uses only that M is real; set of margins with cover >= t is [L_(k), infinity); smallest attained at L_(k). Correct.")
row("BK4a-L03-canon-bullet-6","2.9-prose","L03.html:421",
    "PASS","Round-3 FAIL cleared. L03.html:421 now: 'While each of these two losses stays at or above the sized margin, changing it does not change the sized margin, because the 198 smallest losses stay the same.' Re-tested: 2000 random edits of the two largest losses to values in [margin,3000] left the 198th order statistic (2961) unchanged; lowering one to margin-1 changed it. The 'two largest scenarios are above the sized margin' part holds: cover 9900 = exactly 198 at or below 2961 (strict).")
row("BK4a-L03-uses-meta","2.9-prose","L03.html:37",
    "PASS","'Uses' line (L03.html:37) lists L02 and integer sums/floors; matches the lesson's own content.")
row("BK4a-L03-misconceptions","2.9-prose-numbers","L03.html:426-445",
    "PASS","Misconception 1 (loss equal to margin counted; Remark 2.2) correct. Misconception 2 (9900 = 198 of 200; Example 2.5) correct. Misconception 3 (default fund pays only after IM is used in full; Remark 1.4) correct; lab Part A3 'within the margin' has DF 0, capital 0 (pure_L03.txt). Misconception 4 (survivors' IM do not enter the waterfall) correct: Def 1.1 uses only DF_i for survivors.")
row("BK4a-L03-problems","2.4-mathematics","L03.html:454-546 (M1-M3, P1-P3, E1-E3, R1-R3)",
    "PASS","M1: a1 100, a2 50, a3 30, Z 20, 8 and 12, total 200 (re-derived). M2: cover(4000)=7500 (c=3); k=3; margin 3000; cover(2999)=5000 (re-derived). M3: 8000 -> k=4 -> 40; 8001 -> 4.0005 -> k=5 -> 50; 10000 -> 50. P1 (:482) a3>0 => a2=DF and a1=IM (proof checked). P2 (:489) ceiling in [1,S]. P3 (:496) c(M) monotone; cover=10000 for M >= max; search ends at max loss. E1 (:506-507) 3058/102/0 matches Part A3 output. E2 (:514) residual 857; 312+381+164 = 857; DF 624,762,328 total 1714; shares exactly DF/2 (re-derived). E3 (:521) 198 at or below, 2 above (50c=9900 only at c=198). R1-R3 (:532-546) verified: R2 boundary S=100 k=99 (9900), k=100 (10000) (re-derived); R3 k=S iff S<=399, first S with k<S is 400 (re-derived over S=1..1999).")
row("BK4a-L03-key-results","2.3-grades","L03.html:556-565",
    "PASS","Each key-results claim maps to a numbered result on the page (Prop 1.2, 1.3; Remark 1.4, 2.2; Prop 2.3; Cor 2.4) graded T with 'Proved in' pointers; rows 564-565 graded C naming Lab 1 Parts A1, A2, B; numbers 2961 and 2992 match the output.")
row("BK4a-L03-quiz","2.3-grades/quiz","L03.html:571-646",
    "PASS","Quiz data-correct/data-answer: DF (:578); 8 (:585; Example 1.5 M1 at 200); 20 (:590); Yes, L_s <= M (:598); 7500 (:605); k=3 (:610); 50 cents (:619; k=5 for 8001); 1 cent (:625); 'margin covers 198 of 200' (:633); 399 (:640; 9975*400/10000=399). Explanations agree with the page.")
row("BK4a-L03-lab-twin","2.5-labs","L03.html:187-411; tests/labs/BK4/lab-BK4-L03-1.py",
    "PASS","Page code equals twin after rstrip; expected block (tolerance 1e-9) equals the pure run output (ledgers/BK4/scripts/BK4-a-r4/pure_L03.txt); twin exit 0 under python3 -I -W error, empty stderr. Output lines and the interpretation (L03.html:410-411) agree.")
row("BK4a-L03-why-structure","2.7-structure","L03.html:34-657",
    "PASS","check_pages BK4 L03 PASS; 4 misconceptions; problem set M/P/E/R; key results; quiz 10; section 3 canon breaks (:416-421) with bullets; page_smoke L03 PASS.")

# ---- gates (re-run this round) ----
row("BK4a-gate-check-pages","2.10-gate","tools/check_pages.py --unit BK4; --page L01/L02/L03",
    "PASS","'check_pages BK4: PASS' (check_pages_unit.out); --page L01, L02, L03 PASS. Note: '--page index' is not a valid target (the hub is not a lesson page) and FAILs for that reason; the unit-level run already covers index.html.")
row("BK4a-gate-check-dag","2.10-gate","tools/check_dag.py --unit BK4",
    "PASS","'check_dag BK4: PASS' (check_dag.out).")
row("BK4a-gate-run-labs","2.10-gate","tools/run_labs.py --unit BK4",
    "PASS","'run_labs BK4: PASS (8/8)' (run_labs.out). Twins under python3 -I -W error: exit 0 for L01, L02, L03 with empty stderr.")
row("BK4a-gate-page-smoke","2.10-gate","tools/page_smoke.py --unit BK4 --pages index L01 L02 L03",
    "PASS","'page_smoke BK4: PASS'; modules/BK/BK4/L01,L02,L03 PASS; lab runtime lines 0.0 s (page_smoke.out).")
row("BK4a-gate-ruff-mypy","2.10-gate","twins; repo gates",
    "PASS","Twins: ruff check PASS, ruff format --check PASS, mypy --no-incremental PASS. Repo-wide (this round): 'All checks passed!' and '553 files already formatted' (ruff_repo.out); 'Success: no issues found in 385 source files' (mypy_repo.out).")
row("BK4a-gate-pytest-labs","2.10-gate","tests/test_labs.py, tests/test_run_labs.py, tests/test_page_checks.py",
    "PASS","pytest -q on the three modules: exit 0, no failures (pytest_relevant.out).")
row("BK4a-gate-verify-refs","2.10-gate","tools/verify_refs.py --offline (the --unit flag only applies to live runs; no live run was done)",
    "PASS","'offline integrity: 560 entries, 0 problems' (verify_refs_offline.out). Live check not run (no network in this round's scope); registry is unchanged between the pins.")
row("BK4a-banned-and-process","2.9-banned","index.html, L01.html, L02.html, L03.html",
    "PASS","check_pages BANNED list passes on all four pages (check_pages_index/unit outputs); process-word scan on visible text: zero hits.")
row("BK4a-scope-words","2.9-scope-words","L01.html, L02.html, L03.html (every, all, always, never, any, for every)",
    "PASS","Round-3 FAIL cleared: the three named sentences are fixed (L01.html:313; L01.html:115; L03.html:421). Remaining scope words checked against a proof or computation: 'every d' (L01.html:64 'holds for any value of d'; :305 'every d >= 0'; :312 'holds for every value of d') -- no d in Props 2.2-2.4; 'every order' (L01.html:115; the same claim is at L01.html:115) -- Prop 2.4 proof uses only k=m; 'any set of trades ... however many members' (L02.html:118) -- proofs are general over finite sets; 'every scenario' (L03.html:312, 496, 543-544) -- c(M)=S for M >= max loss; 'every statement ... initial margin' (L03.html:420) -- the model has no variation margin; 'every fixture row sums' (lab output: True).")
row("BK4a-hub-P0.1-grade-source","2.9-attribution","index.html:110",
    "PASS","Placement item Pq5 (index.html:104-110): grade C for a single sample; grade legend (L0x.html:46) and BLUEPRINT grade definition agree. P0.1 is named as the source and is unreleased in the program (index.html:35), disclosed honestly.")
row("BK4a-hub-card-L02","2.9-structure","index.html:143",
    "PASS","Card L02 (index.html:143): '7 h', title equals L02 h1 'Central Counterparties and Multilateral Netting'; description (novation, net obligations sum to zero, netted vs gross notional, checked in Lab 1 on seeded SIMULATED trades) matches L02 content.")
row("BK4a-L01-canon-bullet-only-designs","2.9-prose","L01.html:313",
    "PASS","Round-3 FAIL cleared: L01.html:313 now reads 'the lesson states no fact about which design any real system uses; the two designs are defined in Definitions 1.1 and 2.1'. The false 'only' is gone.")
row("BK4a-L01-A2-forward-ref","2.5-dfn","L01.html:71; L01.html:79-80",
    "PASS","A2 names Definition 2.1 before it appears (forward reference to net debit). Accepted in round 3 and re-checked: the reference is to a definition in the same lesson (L01.html:79-80), not to a concept outside the unit.")
row("BK4a-L01-R1-order-claim","2.4-mathematics","L01.html:420",
    "PASS","R1 solution (L01.html:420): 'Remark 3.1 shows that if all inflows of i come first ...' and 'Such an order exists' -- the Remark 3.1 claim is correct (verified) and the existence argument is correct.")
row("BK4a-L02-meta-description","2.9-prose","L02.html:7",
    "PASS","Meta description (L02.html:7) describes novation, CCP and netting identities; contains no claim beyond the page.")

# ---- new rows this round ----
row("BK4a-rederive-r4","2.1-numbers (independent)","ledgers/BK4/scripts/BK4-a-r4/rederive_a_r4.py; out rederive_a_r4.out",
    "PASS","Independent re-derivation (stdlib, python3 -I): L01 seed day and needs by binary search; L02 seed trade set and every netting number; Example 2.4/M1/M2/M3/R2 bps; L03 Example 1.5/1.6 table, 20000 random waterfall conservation/Prop 1.3/Remark 1.4 cases, 400 random Prop 2.3 brute-force cases, R2/R3 boundaries, Example 2.5, lab Part B seeded sizings and counts. 0 mismatches in every random check.")
row("BK4a-lab-block-equality-r4","2.5-labs","lab_block_compare.py on L01-L03 and tests/labs/BK4/lab-BK4-L0{1,2,3}-1.py",
    "PASS","Page code (first pre block) equals twin source (rstrip per line) for L01, L02, L03; page expected block (class=expected) equals the run output of python3 -I -W error on each twin (pure_L0n.txt). Lab output is deterministic for the seeds.")
row("BK4a-gate-repo-ruff-mypy-r4","2.10-gate","ruff check ., ruff format --check ., mypy --no-incremental (whole repo), build_site --check, check_pages --all",
    "PASS","ruff check: All checks passed; ruff format --check: 553 files already formatted; mypy --no-incremental: no issues in 385 files; build_site.py --check: 'site data current: 6 outputs'; check_pages.py --all: PASS for every built unit (check_pages_all.out).")

# ---- assemble in round-3 order, then new rows ----
order = json.load(open('/Users/billyribeiro/.fanout/frags/E-BK4-a.round3.json'))['rows']
ids = [r['id'] for r in order]
extra = [i for i in R if i not in ids]
missing = [i for i in ids if i not in R]
assert not missing, missing
rows = [R[i] for i in ids] + [R[i] for i in extra]
for r in rows:
    if r['id'] in ids and r['status'] == 'PASS' and not r['evidence'].startswith('Carried'):
        pass
nonpass = [r['id'] for r in rows if r['status'] != 'PASS']
verdict = 'PASS' if not nonpass else 'FAIL'
for r in rows:
    if r['status'] != 'PASS':
        r['fix'] = "index.html:33: qualify the sentence as the model's rule, e.g. 'In this unit's model, a trade settles when its payment has moved between accounts; the payment systems and clearing houses are defined in Lessons 1 and 2.'"
frag = {
 "unit": "BK4", "slice": "BK4-a", "round": 4,
 "round_note": "Round 4 of BK4-a (hub index.html, L01, L02, L03, lab twins 1-3). Delta from the round-3 pin 67a2d13 to 9a02b1a: L01.html:115,313,330,370,377; L02.html:390,392,421; L03.html:55,421 (10 lines). index.html and tests/labs/BK4/lab-BK4-L0{1,2,3}-1.py are byte-identical since 67a2d13 (git diff --stat empty). Every round-3 row id is kept. All four pages were re-read in full as stripped text (ledgers/BK4/scripts/BK4-a-r4/L01.txt, L02.txt, L03.txt, index.txt) and every hunk re-verified; all numbers re-derived by rederive_a_r4.py; gates re-run.",
 "verifier": "Haiku independent verifier, BK4-a round 4 (did not build BK4)",
 "pin": "9a02b1af9f92a060f7fabf7e1b3afb5ea95f45ba",
 "base": "67a2d13e7575608e95b2e34a9c7c2a82c61b117b (round-3 pin; round-3 fragment /Users/billyribeiro/.fanout/frags/E-BK4-a.round3.json)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyE4-BK4-a (detached at 9a02b1a; .venv symlinked; vendor copied)",
 "scratch": "/Users/billyribeiro/.fanout/wt/verifyE4-BK4-a/ledgers/BK4/scripts/BK4-a-r4/",
 "verified_at": "2026-11-04T13:25:28Z",
 "verdict": verdict,
 "rows": rows,
 "mutants": [],
 "registry_flags": [
   "SEC T+1 settlement rule (curriculum yaml:1092): no sec.gov key in references/references.json (grep count 0, re-checked this round). Index and lessons correctly say the rule is not stated (index.html:193; L01.html:64, 312). Required before any settlement fact is stated (B1).",
   "duffie2011central: registry fields read this round (authors Duffie, Zhu; title; Review of Asset Pricing Studies 2011). Publisher abstract not read (not needed: the slice states no finding of the paper).",
   "bisndcpmi: issuer-level record (verified_by issuer, references.json:2853); used at index level only."
 ],
 "freshness_flags": [
   "Duffie and Zhu (2011) is the only CCP-risk source cited, at paper level; no post-2011 CCP-risk literature is in the registry. Not a defect for this slice, which states no finding."
 ],
 "notes": [
   "Round-4 defect found: index.html:33 states a real-world settlement fact ('the money moves through payment systems and clearing houses') without a B1 admitted source (row BK4a-hub-settlement-framing, FAIL, low severity). All round-3 FAIL rows are cleared by the edits at L01.html:115,313,370; L02.html:390,392,421; L03.html:55,421.",
   "Forward references and definitions: L01.html:59 says the designs are 'defined in Section 2' while L01.html:313 says 'defined in Definitions 1.1 and 2.1'. Both are accurate (Definition 1.1 names the designs, Section 2 defines their liquidity measures); not a defect.",
   "Proposition 2.3 (L01.html:100) cites 's != r by Assumption 1.3' inside its proof, while L01.html:296 says the proof does not need that rule. The proof is valid either way; not a defect.",
   "No mutants: this slice has no grader (grader and project belong to slice E). Alternatives: not applicable.",
   "Command invocation note: 'tools/check_pages.py --unit BK4 --page index' is not a valid lesson target; the unit-level run includes the hub and PASSES. Not a defect of the pages.",
   "Hub placement item Pq5 cites P0.1 (unreleased in this program, index.html:35). Accepted as disclosed in round 3."
 ],
 "summary": f"BK4 slice a round 4: {len(rows)} rows, {len(rows)-len(nonpass)} PASS, {len(nonpass)} non-PASS ({', '.join(nonpass) if nonpass else 'none'}). Round-3 FAIL rows (L01 remark 2.5 quantifier; L01 P1 assumption; L01 'only' at 313; L02 R1 missing G>0 at 390/421; L03 netting-limit sentence at 55; L03 false sensitivity sentence at 421; scope-word aggregate) are cleared with fresh evidence. All gates PASS (check_pages unit and all pages, check_dag, run_labs 8/8, page_smoke index/L01-L03, ruff and mypy twins and repo, pytest labs, verify_refs --offline, build_site --check). Numbers re-derived independently; twin code equals page code; expected blocks equal run output."
}
ledger = '/Users/billyribeiro/.fanout/wt/verifyE4-BK4-a/ledgers/BK4/BK4-a.json'
json.dump(frag, open(ledger, 'w'), indent=1, ensure_ascii=False)
print("rows", len(rows), "nonpass", nonpass, "verdict", verdict)
