"""Build the BK4-a round-8 fragment from the round-7 row ids. Every row states what was re-checked this round."""
import json
import subprocess

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-BK4-a"
S = "ledgers/BK4/scripts/BK4-a-r8"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-BK4-a.round7.json"))
prev_ids = [r["id"] for r in prev["rows"]]

G = {  # gate and script evidence
    "gates": f"{S}/gate_*.txt",
}
R = {}  # id -> (check, location, status, evidence, fix)

def P(i, check, loc, ev):
    R[i] = (check, loc, "PASS", ev, None)

def F(i, check, loc, ev, fix):
    R[i] = (check, loc, "FAIL", ev, fix)

HUB = "course/modules/BK/BK4/index.html"
L1 = "course/modules/BK/BK4/L01.html"
L2 = "course/modules/BK/BK4/L02.html"
L3 = "course/modules/BK/BK4/L03.html"
TW = ["tests/labs/BK4/lab-BK4-L01-1.py", "tests/labs/BK4/lab-BK4-L02-1.py", "tests/labs/BK4/lab-BK4-L03-1.py"]

# --- hub (index.html is byte-identical to the round-7 pin; every subject below was re-read this round)
P("BK4a-hub-hours-arithmetic", "2.9-structure hours", f"{HUB}:29,40,42,138,140-144,162-174",
  f"Re-read this round. data-hours-lessons=35, data-hours-project=15 (index.html:29); bar 70%/30% (:40); 5 x 7 = 35 and 2+2+3+3+2+2+1 = 15 (:162-174); L01/L02/L03 eyebrows 7 study hours and data-hours=7. gate_check_pages.txt PASS.")
P("BK4a-hub-placement-arithmetic", "2.9-structure quiz", f"{HUB}:71; course/assets/js/quiz.js:70",
  "Eight items (index.html:74-131). 0.8 x 8 = 6.4, so 7 correct are needed; 6/8 = 75 percent, 7/8 = 87.5 percent. quiz.js:70 computes correct/items.length >= mastery, so 6 of 8 fails and 7 of 8 passes.")
P("BK4a-hub-placement-keys", "2.4-mathematics keys", f"{HUB}:80,85,90,95,99,108,117,122,131",
  "Re-derived: 110/1.1 = 100; (1-(1/2)^3)/(1/2) = 1.75; lim_{x->3} 2x = 6; Bertrand price = c; grade C matches BLUEPRINT.md:161; FC1 lifecycle order matches course/modules/FC/FC1/L05.html:63 (order entry, matching, trade capture, clearing, settlement, position update); skill answers 20 (min(120-100,50)) and first surviving member (remainder rule, L01 not involved) match the project and Lesson 3 Definition 1.1.")
P("BK4a-hub-prereq-chain", "2.9-structure DAG", f"{HUB}:35,61; curriculum/02-economics-finance-core.yaml:22,367,1075; curriculum/01-foundations.yaml:126",
  "Re-read this round. curriculum/02-economics-finance-core.yaml:367 FC1 prereqs [P0.1, E1]; :1075 BK4 prereqs [FC1]; :22 E1 prereqs [M2]; curriculum/01-foundations.yaml:126 M2 prereqs [M1]. Curriculum unchanged since the round-7 pin (git diff 06994db1..HEAD -- curriculum empty). index.html:35 and :61 read this round: 'through them M1' is correct.")
P("BK4a-hub-P0.1-link", "2.9-structure links", f"{HUB}:35",
  "Re-checked this round: ledgers/BK4/scripts/BK4-a-r8/links_check.out, 57 hrefs in index and L01-L03, 0 problems (the FC1 href resolves). ls course/modules/P0 -> No such file or directory, so 'not yet released' is correct.")
P("BK4a-hub-financial-intermediary", "2.9-structure DAG", f"{HUB}:61-66; course/concepts.html:477,483,485",
  "Re-read this round. concepts.html:477 clearing-and-settlement, :483 bank-money-creation, :485 trade-lifecycle exist with anchors; links_check.out has 0 problems.")
P("BK4a-hub-bertrand-trade-fee", "2.9-structure scope", f"{HUB}:65; course/modules/BK/BK4/L01-L05.html, project.html",
  "Re-run this round with ctx.py over index, L01-L05 and project.html for 'present value', 'geometric', '\\blim', 'Bertrand' and 'limit': the only hits are index.html:65, index.html:74-99 (the placement items) and 'limit' in its ordinary sense (L03 canon, L04:7,52, project:214,416). No lesson or project uses the mathematical concepts.")
P("BK4a-hub-concept-anchors", "2.9-structure links", f"{HUB}:63-66; {L1}:37,59,64; {L2}:37,64,81,275; {L3}:37,67,134",
  "links_check.py (r8, links_check.out): 57 hrefs in index.html, L01, L02, L03; 0 missing files, 0 missing ids. check_dag --unit BK4 PASS (gate_check_dag.txt).")
P("BK4a-hub-ladder-vs-project", "2.9-structure prose", f"{HUB}:150-156 vs course/modules/BK/BK4/project.html:45-47,54,59,107,178",
  "Re-read this round. Four-member house (project:45,59); 40 seeded SIMULATED scenario losses (project:54,107); completion problem with two blanks, survivor share and sizing index (project:46,178); clearing_house.py (project:47). Hub rung texts agree.")
P("BK4a-hub-data-status", "2.8-data", f"{HUB}:37,182; tools/data_sources.yaml:19,53,91",
  "Embedded ids are fx_daily (:19), fx_monthly (:53), ust_daily (:91) only. grep for data-files in index, L01-L03, L04, L05, project: 0 hits. No payment, settlement, clearing or stablecoin series in data_sources.yaml.")
P("BK4a-hub-reading-list", "2.1-citations", f"{HUB}:186-194; references/references.json (duffie2011central, bisndcpmi); curriculum/02-economics-finance-core.yaml:1089-1092",
  "verify_refs --unit BK4 (live, gate_verify_refs_unit_BK4.txt): 2 of 560 entries, 0 problems. bisndcpmi record: url https://www.bis.org/committees/cpmi/publications, verified_by issuer, type primary (index-level only, as the page says). No sec.gov record (grep count 0); the SEC source is pending in references/review_queue.json:830. Curriculum lists three sources (yaml:1089-1092).")
P("BK4a-hub-process-words", "2.9-structure prose", f"{HUB} (visible text)",
  f"{S}/banned_scan.py -> banned_scan.out: hits 0 (word-bounded scan of banned strings, filler, process words and ellipses over index, L01, L02, L03 visible text).")

# --- L01 (changed since round 7: lines 100 and 296 re-read)
P("BK4a-L01-numbers", "2.2-numbers", f"{L1}:51,254-286,409,55",
  f"{S}/rederive_L01.py -> rederive_L01.out: day regenerated from Random(20260); gross 2841600; nets +379800, -1533900, +1154100 (sum 0); need 112500, 1533900, 0; debits 0, 1533900, 0; moved 1533900; ratio 5113/9472 = 0.5398015... (rounded 0.5398); 2841600 cents = 28416 dollars. ALL matches the printed Part B and C values (ALL_PART_B_MATCH True).")
P("BK4a-L01-prop-2.2-2.4", "2.4-mathematics", f"{L1}:84-111; 296",
  "Re-read this round. Prop 2.2 proof: feasible o_i >= max(0,-mu), least element = need. Prop 2.3 proof (L01:100, changed this round): each payment adds +a to r and -a to s, so the sum is zero; dropping 's != r' does not invalidate it, because a self-payment adds and subtracts the same amount (stated at L01:296). Prop 2.4 proof uses k=m in the minimum and monotonicity of max(0,.); strictness by Example 2.6 (Need_A 100 > Debit_A 50).")
P("BK4a-L01-P2-iff", "2.4-mathematics", f"{L1}:375-377",
  "P2 cases mu>=0 (both zero), mu<0 and S_m=mu (both -mu), mu<0 and S_m>mu (Need=-mu, Debit is 0 or -S_m < -mu; differ). Re-derived. Hypotheses listed (mu <= S_m, Prop 2.2, Section 2 definitions) are the ones used.")
P("BK4a-L01-examples-remarks", "2.4-mathematics", f"{L1}:119-126; rederive_L01.out",
  "Example 2.6 running sums A 0,-100,-100,-50; B 0,100,20,20; C 0,0,80,30; minima -100,0,0; nets -50,20,30; debit A 50; gross 230 (rederive_L01.out 'Example 2.6'). Remark 2.7 running A 0,50,-50,-50; need 50; debit 50 (rederive_L01.out 'Remark 2.7').")
P("BK4a-L01-problems-M-P-E-R", "2.4-mathematics problems", f"{L1}:343-434",
  "rederive_L01.out: M1 running 0,300,-200, need 200, debit 200; M2 doubled, need 200, debit 100 (by scaling); M3 running 0,40,-30,-20, need 30, debit 20. P1 proof text (L01:370) correct, uses A1 finite list and the sender/receiver clause. P2, P3 correct. E1 1533900 and 1533900; E2 1 of 3 (Bank A); E3 2841600 base, 1533900, 0.5398. R1 proof uses Remark 3.1 and Prop 2.4, correct. R2 identity and gross bound correct. R3 nets 0, running A 0,-100,-100,0, need 100 (rederive_L01.out 'R3').")
P("BK4a-L01-remark-3.1-order", "2.4-mathematics", f"{L1}:300; 420",
  "Remark 3.1: inflows first gives running minimum min(0,Net), so Need = Debit (re-derived). The claim that the running minimum depends only on the order of payments to or from i is correct because S_{i,k} changes only at those payments.")
P("BK4a-L01-R3", "2.4-mathematics problems", f"{L1}:432-434",
  "rederive_L01.out 'R3 nets [0, 0, 0] debits [0, 0, 0] A running [0, -100, -100, 0] need A 100'. Matches the page.")
P("BK4a-L01-remark-2.8", "2.5-labs", f"{L1}:289-292 vs twin output",
  "Remark 2.8 says Part B prints the Prop 2.4 inequality per bank and Part C prints the zero sum. Checked against the printed output (twin output: 'net positions sum to zero: True', Part B 'RTGS need at least DNS net debit: True' per bank) and the code (lab lines 225, 233-235).")
P("BK4a-L01-interp-three-inequalities", "2.2-numbers", f"{L1}:286 vs lab output",
  "Each figure in the interpretation (379800 net; 0 debit; 112500 need; 1533900; 2841600; 1533900 moved) equals the printed output (lab_L01 output block lines 269-279). The ratio 0.5398 is stated with the lab not printing it, correctly.")
F("BK4a-L01-misconception-1", "2.9-structure prose / 2.1 defined term", f"{L1}:322 (first sentence)",
  "Definition 2.1 (L01:80) defines the peak intraday need of bank i under RTGS only. The first sentence of Misconception 1 says 'Netting can lower the need, as it does for Bank A in Lab 1, which has an RTGS peak need of 112500 cents and a DNS net debit of 0'. Netting does not change the RTGS peak need (Remark 2.5 and Definition 2.1 say the need depends on the running minimum, not on settlement design), so the sentence uses 'need' for the DNS funding requirement, a second meaning of a defined term in the same paragraph. The second sentence ('It does not remove the need for a bank that is a net payer') has the same ambiguity. The corrected figures in the rest of the paragraph are right: Bank A need 112500 with debit 0, Bank B debit = need = 1533900.",
  f"At L01.html:322 replace 'Netting can lower the need, as it does for Bank A in Lab 1, which has' with 'Net settlement can lower the funds a bank must find at settlement, as it does for Bank A in Lab 1, whose RTGS peak need is 112500 cents and whose DNS net debit is' and keep the figures. Replace 'It does not remove the need for a bank that is a net payer' with 'It does not remove the settlement funding of a bank that is a net payer'. Then re-run run_labs --unit BK4 is not needed (prose only); re-run check_pages --unit BK4.")
P("BK4a-L01-misconceptions-2-3", "2.9-structure prose", f"{L1}:326,330",
  "Misconception 2: Bank A net +379800, debit 0, RTGS need 112500 (Part B output); Prop 2.4 strict. Misconception 3: Remark 2.7 need 100 -> 50 dollars, debit 50 unchanged (rederive_L01.out). Both correct.")
P("BK4a-L01-quiz", "2.9-structure quiz", f"{L1}:463-534",
  "10 items; each MC has one data-correct; answers recomputed: 200 (net -200), 200 (M1), 200 (doubled, Remark 2.7 and P3), 50 (Remark 2.7), zero (Prop 2.3), 0 for net +50, lab parameter (Part D), 28416 dollars (2841600 cents), T+1 named not stated. All explanations match the page.")
P("BK4a-L01-lab-twin", "2.5-labs", f"{L1}:128-287; tests/labs/BK4/lab-BK4-L01-1.py",
  "gate_run_labs.txt: run_labs BK4 PASS (8/8). Twin alone: .venv/bin/python -I -W error tests/labs/BK4/lab-BK4-L01-1.py -> exit 0, stderr 0 bytes (twin_L01_err.txt, twin_L01_out.txt). Page code vs twin (page_code.py / diff): identical except the final newline after main(). Expected block equals the output (run_labs).")
P("BK4a-L01-notation", "2.4-mathematics notation", f"{HUB}; {L1}; {L2}; {L3} math spans",
  f"{S}/notation_scan.py -> notation_scan.out: 746 math spans; no registered symbol (T, Phi, gamma_3, gamma_4, R^*, R^{{e*}}, R_f, Q) appears; mathbb count 0 (ruling 1 satisfied). Commands used are standard TeX or defined locally (mu and ell in L01/L03 are local; delta, IM, DF, K, V, Z, D, u, x_i in L03 are defined at L03:61-73).")
P("BK4a-L01-dag-defs", "2.9-structure DAG", f"{L1}:37,59,64; {HUB}:66",
  "def-payment-system (L01:59) and def-settlement-cycle (L01:64) are the only data-concept defs in L01; index:66 links them. check_dag --unit BK4 PASS (gate_check_dag.txt).")
P("BK4a-L01-why-words", "2.9-structure prose", f"{L1}:51",
  "Why-it-matters paragraph: 107 words by a count of the rendered text (limit 120).")
P("BK4a-L01-structure", "2.9-structure", f"{L1}:34-552",
  "Sections 1-9 in template order (definitions, liquidity, conditions on proofs, settlement cycle, misconceptions, problem set, key results, quiz, references). Four canon limits (L01:310-313); three misconceptions; problem set M1-M3, P1-P3, E1-E3, R1-R3; ten quiz items.")
P("BK4a-L01-grades", "2.3-grades", f"{L1}:43-48, 84, 94, 104, 446-452",
  "Claim spans are T (Props 2.2-2.4, Example 2.6 and Problem P2 rows) or C (lab rows naming Lab 1 Parts B and C, SIMULATED). Grade B appears only in the legend (L01:45), see BK4a7-L01-legend-B-template.")
P("BK4a-L01-FC1-claim", "2.9-structure DAG", f"{L1}:55; course/modules/FC/FC1/L05.html:63",
  "FC1 Lesson 5 (L05.html:63) is the trade-lifecycle lesson and states the six states in order.")
P("BK4a-L01-canon-breaks-wording", "2.9-structure prose", f"{L1}:308-313",
  "Four limits (no queues or credit lines; the day is given; settlement cycle is a parameter; no statement which real system uses which design). None states a fact about a real system.")
P("BK4a-L02-prop-2.2", "2.4-mathematics", f"{L2}:85-99",
  "Re-read. (a) each trade enters one receivable and one payable (A2); (b) sum n_i = G - G = 0; (c) max(0,x) - max(0,-x) = x; (d) 0 <= A <= G from Pay_i >= 0 and Rec_i >= 0. Assumption 1.3 (A1-A3) listed before the statement.")
P("BK4a-L02-prop-2.3-title", "2.4-mathematics", f"{L2}:102-103",
  "Title matches the statement (A = G iff each member has Rec = 0 or Pay = 0).")
P("BK4a-L02-prop-2.3-proof", "2.4-mathematics", f"{L2}:106-109; 348-349",
  "Re-derived. Three cases cover each term (Rec=0; Rec>0, Pay=0; Rec>0, Pay>0 gives strict inequality). Hypotheses named in P2 (L02:349).")
P("BK4a-L02-example-2.4", "2.2-numbers", f"{L2}:112-113; 270; 294",
  "rederive_L02.out: n = -50, 20, 30; A = 50; G = 230; floor(10000 x 180/230) = 7826 (exact 7826.0869...).")
P("BK4a-L02-lab-claims", "2.5-labs", f"{L2}:123,127; {L2}:219-237 (page code = tests/labs/BK4/lab-BK4-L02-1.py)",
  "Twin checks (page code lines 219-237): receivables equal gross notional; net obligations sum to zero; amount paid equals amount paid by net payers; netted amount at most gross. Page statements at L02:123,127 and 270 match.")
P("BK4a-L02-lab-numbers", "2.2-numbers", f"{L2}:241-269 (expected); 270; 365-381",
  f"{S}/rederive_L02.py -> rederive_L02.out: six trades regenerated from Random(2026); receivables 314500, 2067800, 3340300, 1873700; payables 3941500, 314500, 0, 3340300; nets -3627000, +1753300, +3340300, -1466600; A 5093600; reduction 2502700; floor 3294 (exact 3294.63); MATCHES_L02_PART_B_TO_D True.")
P("BK4a-L02-lab-numbering", "2.9-structure", f"{L2}:121,123,125-127,270",
  "Lab 1 is the only lab in the lesson; the lab label, the section heading and the interpretation agree.")
P("BK4a-L02-attribution", "2.1-citations", f"{L2}:277,285,425; references/references.json (duffie2011central, record lines); course/modules/BK/BK4/index.html:191",
  "Registry title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', authors Duffie and Zhu, Review of Asset Pricing Studies (verify_refs live: 0 problems). The lesson attributes only the question of the title and states no finding. Access check: plain curl to https://doi.org/10.1093/rapstu/rar001 returned HTTP 403 (duffie_crossref.out records the URL and code), and the Crossref API record (same DOI) has title, authors and container but no abstract. No claim on the page depends on the abstract, so the attribution passes on the registry record.")
P("BK4a-L02-canon-misconceptions", "2.9-structure prose", f"{L2}:280-285, 293-302",
  "Four limits. Misconceptions checked against Prop 2.2(b),(c) and Lab Part C/D (zero sum; positive netted amount 5093600). Re-read this round.")
P("BK4a-L02-problems", "2.4-mathematics problems", f"{L2}:315-406",
  "rederive_L02.out: M1 nets -10,-20,50,-20, A 50, G 180, floor 7222 bps; M2 G 460, A 100, floor 7826 bps; M3 nets -200, 100, 100, A = G = 200, 0 bps; R2 A 100 in both sets (rederive_L02.out 'R2 Y'); P1-P3 correct (P3 cycle nets zero, 10000 bps); E1 5093600 and 2502700, base 7596300; E2 +3340300 and -3627000; E3 members 1, 2, 4. E2 and E1 scope: see BK4a8-L02-E2-only-scope.")
P("BK4a-L02-key-results", "2.3-grades", f"{L2}:416-425",
  "T rows are proved on the page (Props 2.2, 2.3, R1, P3, Example 2.4). C rows name Lab 1 or are question-only.")
P("BK4a-L02-quiz", "2.9-structure quiz", f"{L2}:432-510",
  "10 items; answers recomputed: n_2 = +20; A = 50; zero sum (Prop 2.2(b)); 7826; equality case; 100; no money moves in the identities; zero sum is not a guarantee of no default; 5093600 cents = 50936 dollars; zero for a cycle (P3).")
P("BK4a-L02-lab-twin", "2.5-labs", f"{L2}:121-271; tests/labs/BK4/lab-BK4-L02-1.py",
  "run_labs BK4 PASS (gate_run_labs.txt). Twin alone under .venv/bin/python -I -W error: exit 0, stderr 0 bytes (twin_L02_err.txt). Page code equals the twin except the final newline.")
P("BK4a-L02-why-structure", "2.9-structure", f"{L2}:34-518",
  "why-it-matters 96 words (limit 120); four canon limits; three misconceptions; problem set 3+3+3+3; quiz 10 items; hours 7 (data-hours attribute and eyebrow).")
P("BK4a-L02-meta-description", "2.9-structure prose", f"{L2}:7",
  "Meta description states novation, CCP, multilateral netting, the net obligation identity, the bound netted <= gross, Lab 1 on a seeded SIMULATED set of four members and six trades in integer cents. Matches the lab (MEMBERS=4, TRADES=6, SEED=2026).")
P("BK4a-L03-legend", "2.3-grades", f"{L3}:43-48",
  "Same legend as L01 (see BK4a7-L01-legend-B-template). No claim on L03 is graded B.")
P("BK4a-L03-four-resources", "2.9-structure prose", f"{L3}:55; 66-73",
  "Intro names margin, default fund and CCP capital, then the survivors' default funds; Definition 1.1 has exactly those layers in that order.")
P("BK4a-L03-notation-d", "2.4-mathematics notation", f"{L3}:61,67-73,100,139,152,480-482; notation_scan.py",
  "Registered symbols absent (notation_scan.out). Local symbols are defined where used: delta (L03:61), V (L03:67), D, DF_i, IM_i, K (L03:61-67), a_1..a_3, Z, u, x_i, y_i, l (L03:69-80), p_i (L03:95), L_(k), t, k (L03:152).")
P("BK4a-L03-def-props-1.2-1.3", "2.4-mathematics", f"{L3}:66-96",
  "Re-read. Definition 1.1 layer order and survivor rule; Prop 1.2 conservation (Z >= D and Z < D cases); Prop 1.3: 0 <= l <= n+ - 1 (fractional parts < 1), x_i + 1 <= DF_i for DF_i > 0. Hypotheses A1, A2 stated.")
P("BK4a-L03-remark-1.4", "2.4-mathematics", f"{L3}:100-101",
  "a2 > 0 implies a1 = IM; a3 > 0 implies a2 = DF; Z > 0 implies a3 = K. Each follows from the min argument, re-derived.")
P("BK4a-L03-example-1.5", "2.2-numbers", f"{L3}:104-121; rederive_L03.out 'A1'",
  "All eight table rows (80, 120, 170, 180, 181, 200, 205, 300) match rederive_L03.out line by line (e.g. 181 -> member 1 pays 1; 205 -> 10 and 15; 300 -> 40, 60, uncovered 20). Table column order matches the lab output.")
P("BK4a-L03-example-1.6", "2.5-labs", f"{L3}:124-126; rederive_L03.out 'A2'",
  "Loss 1: member 1 pays 1; loss 2: members 1 and 2 pay 1 each, member 3 pays 0 (rederive_L03.out 'A2'; twin output 'Part A2').")
P("BK4a-L03-def-2.1-prop-2.3", "2.4-mathematics", f"{L3}:133-165",
  "Definition 2.1 cover floor and basis (count of scenarios, not dollar-weighted). Prop 2.3 with k = ceil(tS/10000), Parts 1-3 re-read: Part 2 uses floor(y) >= t iff y >= t for integer t and c(M) integer. A3, A4 listed before the statement.")
P("BK4a-L03-cor-2.4-ex-2.5", "2.4-mathematics", f"{L3}:168-181; rederive_L03.out 'Ex2.5'",
  "Corollary 2.4 proof (ceiling non-decreasing; sorted losses). Example 2.5: 9900 x 200/10000 = 198 (k=198); 9975 x 200/10000 = 199.5 (k=200). Printed sized margins 2961 and 2992 match rederive_L03.out ('target 9900 ... margin 2961', 'target 9975 ... margin 2992').")
P("BK4a-L03-R1-note", "2.4-mathematics", f"{L3}:530-533",
  "Real-valued margins: {M : cover >= t} = [L_(k), inf), smallest element L_(k). Correct; the proof of Prop 2.3 Part 2 uses only that M is real.")
P("BK4a-L03-canon-bullet-6", "2.2-numbers", f"{L3}:422 (round 6 cited 421)",
  "At 9900 bps and S=200: sized margin is L_(198) = 2961; L_(199) = 2981 so exactly two scenarios lie above (rederive_L03.out 'max loss 2992 L(198) 2961 L(199) 2981'); cover at 2961 is 9900 and one cent below is 9850 (rederive_L03.out). The general statement is correct, including the tie case.")
P("BK4a-L03-misconceptions", "2.9-structure prose", f"{L3}:430-443",
  "Four misconceptions, each corrected by a cited definition, remark or lab part (Def 2.1, Remark 2.2, Example 2.5, Remark 1.4, Part A3 output with DF 0 and capital 0 for loss 1529).")
P("BK4a-L03-problems", "2.4-mathematics problems", f"{L3}:455-546",
  "rederive_L03.out and hand checks: M1 8, 12, total 200; M2 cover 7500, k=3, margin 3000; M3 40, 50, 50; P1-P3 proofs correct; E1 3160 -> margin 3058, DF 102; E2 residual 857 = 312+381+164, DF/2 exact (624, 762, 328 even); E3 198 of 200 at 9900 (floor(50c)=9900 only for c=198); R1 real margins; R2 k = 99 and 100, at most one above; R3 k = 399 at S = 399, 400 and 400 at S = 401 (rederive_L03.out).")
P("BK4a-L03-key-results", "2.3-grades", f"{L3}:556-566",
  "T rows are proved in section 1 or 2; C rows name Lab 1 Parts A1, A2, B (fixed fixture and seeded losses).")
P("BK4a-L03-quiz", "2.9-structure quiz", f"{L3}:571-646",
  "10 items; one data-correct per MC; answers recomputed: default fund; 8; 20; yes (L_s <= M); 7500; k=3; 50; 1 cent; 198 of 200; k=399 (9975 x 400/10000 = 399 exactly).")
P("BK4a-L03-lab-twin", "2.5-labs", f"{L3}:187-411; tests/labs/BK4/lab-BK4-L03-1.py",
  "run_labs BK4 PASS (gate_run_labs.txt). Twin alone under .venv/bin/python -I -W error: exit 0, stderr 0 bytes (twin_L03_err.txt). Page code equals the twin except the final newline. Inputs of A3 and B regenerated from Random(2026) in the same order as the code (rederive_L03.py) and match the printed values.")
P("BK4a-L03-why-structure", "2.9-structure", f"{L3}:34-657",
  "why-it-matters 118 words (limit 120); six canon limits (L03:417-422); four misconceptions; problem set 3+3+3+3; quiz 10; hours 7.")
P("BK4a-L03-uses-meta", "2.9-structure DAG", f"{L3}:37; {L2}:64,81",
  "Uses central-counterparty and multilateral-netting, linked to L02.html#def-central-counterparty and #def-multilateral-netting; both anchors exist (links_check.out, 0 problems).")
P("BK4a6-L03-lab-docstring-seed", "2.5-labs", f"tests/labs/BK4/lab-BK4-L03-1.py:3-7 (page docstring {L3}:190-199)",
  "Docstring says Part A3 and B inputs are seeded and A1, A2 are stated fixtures. Code: rng drives im, df, capital (A3) and losses (B); A1 and A2 use literal fixtures. Consistent.")
P("BK4a6-L03-corollary-heading", "2.9-structure prose", f"{L3}:168",
  "Heading 'the sized margin does not fall as the target rises' matches Corollary 2.4 (M(t) <= M(t'), non-strict).")
P("BK4a-gate-check-pages", "2.9-structure gate", "tools/check_pages.py --unit BK4",
  f"Re-run this round: {S}/gate_check_pages.txt -> 'check_pages BK4: PASS', exit 0.")
P("BK4a-gate-check-dag", "2.9-structure gate", "tools/check_dag.py --unit BK4",
  f"Re-run this round: {S}/gate_check_dag.txt -> 'check_dag BK4: PASS', exit 0.")
P("BK4a-gate-run-labs", "2.5-labs gate", "tools/run_labs.py --unit BK4",
  f"Re-run this round: {S}/gate_run_labs.txt -> 'run_labs BK4: PASS (8/8)', exit 0.")
P("BK4a-gate-page-smoke", "2.9-structure gate", "tools/page_smoke.py --unit BK4 --pages index L01 L02 L03 (run alone)",
  f"Re-run this round alone: {S}/gate_page_smoke.txt -> index, L01, L02, L03 each PASS; 'page_smoke BK4: PASS'; exit 0. Zero console errors and no external requests are reported by the checker.")
P("BK4a-gate-ruff-mypy", "2.5-labs gate", "ruff check/format --check tests/labs/BK4; mypy --no-incremental on the three twins",
  f"Re-run this round: {S}/gate_ruff.txt ('All checks passed!', '8 files already formatted', exit 0); {S}/gate_mypy.txt ('Success: no issues found in 3 source files', exit 0).")
P("BK4a-gate-pytest-labs", "2.5-labs gate", "pytest tests/test_labs.py -k BK4; tests/test_page_checks.py",
  f"Re-run this round: {S}/gate_pytest_labs_bk4.txt (exit 0, 8 passed) and {S}/gate_pytest_page_checks.txt (exit 0).")
P("BK4a-gate-verify-refs", "2.1-citations gate", "tools/verify_refs.py --offline; tools/verify_refs.py --unit BK4",
  f"Re-run this round: {S}/gate_verify_refs_offline.txt ('offline integrity: 560 entries, 0 problems'); {S}/gate_verify_refs_unit_BK4.txt ('live re-verification of BK4: 2 of 560 entries, 0 problems').")
P("BK4a-banned-and-process", "2.9-structure prose", f"{HUB}; {L1}-{L3} visible text",
  f"{S}/banned_scan.py -> banned_scan.out: hits 0 (banned strings, filler, process words, ellipses).")
P("BK4a-scope-words", "2.9-structure scope", f"{HUB}; {L1}-{L3} (all scope words)",
  f"Re-enumerated this round: {S}/scope_words_r8.txt (457 lines containing every, all, any, always, never, only, exactly, same, none, each, no; markup and meta lines included). Every universal in the prose was read in context against its proof, finite check or lab (L01 Prop 2.2-2.4 and R1, L02 Prop 2.2-2.3 and R1-R3, L03 Prop 2.3, P3, R3). The 'Using only' problem prompts are a separate defect, see BK4a8-L01-E2-only-scope and BK4a8-L02-E2-only-scope.")
P("BK4a-hub-settlement-framing", "2.9-structure prose", f"{HUB}:33",
  "The lede states a model convention ('In this unit's model, a trade settles when its payment has moved between accounts'). No T+1 fact is stated.")
P("BK4a-hub-P0.1-grade-source", "2.3-grades", f"{HUB}:108; BLUEPRINT.md:161",
  "Grade C wording matches BLUEPRINT.md:161 (working paper, practitioner research, single-sample evidence).")
P("BK4a-hub-card-L02", "2.7-cards", f"{HUB}:141; {L2}",
  "Card text (novation, CCP, net obligations summing to zero, netted amount vs gross notional, Lab 1 seeded SIMULATED) matches L02. Card rows themselves belong to slice F.")
P("BK4a-L01-canon-bullet-only-designs", "2.9-structure prose", f"{L1}:313",
  "States that no admitted source covers which real system uses which design; consistent with the registry (no payment-system record; references.json has no such key).")
P("BK4a-L01-A2-forward-ref", "2.9-structure DAG", f"{L1}:71; 79-80",
  "A2 says the net debit is 'defined in Definition 2.1': an explicit forward pointer, not an undefined use.")
P("BK4a-L01-R1-order-claim", "2.4-mathematics", f"{L1}:420",
  "R1 proof uses Remark 3.1 and Prop 2.4; the hypothesis that net positions do not depend on order is named.")
P("BK4a-rederive-r4", "2.2-numbers", f"{S}/rederive_L01.py/.out, rederive_L02.py/.out, rederive_L03.py/.out",
  "All three re-run this round with Fraction or exact integers; every printed value and worked number matches (ALL_PART_B_MATCH True; MATCHES_L02_PART_B_TO_D True; rederive_L03 'matches printed True' for all eight A1 rows).")
P("BK4a-lab-block-equality-r4", "2.5-labs", "run_labs --unit BK4 (page code = twin; expected = output)",
  f"{S}/gate_run_labs.txt: 8/8 PASS. Page code vs twin: identical except the final newline (page_code_L0x.py diffs). Expected blocks match output.")
P("BK4a-gate-repo-ruff-mypy-r4", "2.5-labs gate", "tests/labs/BK4 (slice-scope ruff/mypy)",
  f"{S}/gate_ruff.txt and gate_mypy.txt (re-run this round).")
P("BK4a5-L01-lede-settlement-framing", "2.9-structure prose", f"{L1}:51",
  "States 'The lesson describes no real payment system.' and no settlement rule as fact.")
P("BK4a5-L01-designs-pointer", "2.9-structure prose", f"{L1}:59",
  "Definition 1.1 names the two designs; no real-system claim.")
P("BK4a5-L01-canon-heading", "2.9-structure prose", f"{L1}:308",
  "The canon-breaks lead-in 'Four places where the model stops:' matches the four bullets below it (L01:310-313).")
P("BK4a5-L02-canon-heading", "2.9-structure prose", f"{L2}:280",
  "Lead-in 'Four places where the model stops:' matches the four bullets (L02:282-285).")
P("BK4a5-hub-prereq-uses", "2.9-structure DAG", f"{HUB}:61-66",
  "Hub prerequisite list uses only FC1 concepts that FC1 defines (course/concepts.html:477,483,485).")
P("BK4a5-links-anchors", "2.9-structure links", "index.html; L01-L03 (all hrefs)",
  f"{S}/links_check.py -> links_check.out: 57 hrefs, 0 problems.")
P("BK4a5-twins-alone", "2.5-labs", "tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py",
  f"Re-run this round alone under .venv/bin/python -I -W error: exit 0; stderr empty (twin_L01/L02/L03_err.txt).")
F("BK4a7-hub-skip-rule-vs-project", "2.9-structure prose", f"course/modules/BK/BK4/project.html:43 vs {HUB}:71,150; course/assets/js/quiz.js:56-78",
  "Round 7 failed this row because project.html:43 said the rung skip needs only the placement bar. The round-8 pin changes project.html:43 to 'If you pass the placement diagnostic ..., which needs the mastery bar and both skill checks, skip rungs 1 and 2'. quiz.js:71-72 computes skilled = every data-skill item right and passed = overall AND skilled, which matches index.html:71 ('reach the bar and answer both skill checks') and index.html:150. Now consistent. (Not a row failure: PASS.)",
  None)
R["BK4a7-hub-skip-rule-vs-project"] = ("2.9-structure prose", f"course/modules/BK/BK4/project.html:43 vs {HUB}:71,150; course/assets/js/quiz.js:56-78", "PASS",
  "Round 7 failed this row because project.html:43 said the rung skip needed only the placement bar. The round-8 pin changes project.html:43 to 'If you pass the placement diagnostic ..., which needs the mastery bar and both skill checks, skip rungs 1 and 2'. quiz.js:71-72 computes skilled = every data-skill item right and passed = overall AND skilled, which matches index.html:71 ('reach the bar and answer both skill checks') and index.html:150. Consistent.", None)
F("BK4a7-L03-scenario-intro-before-def", "2.9-structure prose / define before use", f"{L3}:51 (first use of 'scenario losses'); {L3}:7 (meta); {L3}:134 (scenario set defined)",
  "The plan (BK4-build-plan.md:176-177) requires terms outside the nine concepts, including 'scenario', to be defined in prose at first use with a plain <dfn>. 'Scenario' is first used in the why-it-matters paragraph (L03:51, 'the k-th smallest scenario loss') and is never defined as a term: no <dfn> for it exists in L03 (grep), and Definition 2.1 (L03:134) defines a 'scenario set' of losses only after the first use. Round 7 passed this as preview wording; under the binding plan rule and verifier rule 5 (terms used before definition) it does not pass. Verifier disagreement with round 7 recorded here.",
  f"At {L3}:51 mark the first use with <dfn>scenario</dfn> and give its meaning in the same sentence (for example: 'the k-th smallest loss of the scenario set, a fixed set of simulated losses for one default defined in Section 2'), or move the first use after Definition 2.1. Re-run check_pages --unit BK4.")
F("BK4a8-L01-E2-only-scope", "2.4-mathematics / problem scope words", f"{L1}:400-402",
  "E2 is worded 'Using only Lab 1, Part C, how many banks have an RTGS peak need above their DNS net debit? Name them using Part B.' The prompt restricts the source to Part C and then requires Part B; the solution uses Part B (Bank A need 112500, debit 0). The 'only' is contradicted inside the prompt (scope word without a computation, verifier rule 4).",
  "Change the prompt to 'Using Lab 1, Parts B and C, how many banks ...? Name them.' (or delete 'only' and 'using Part B'). Prose-only change; re-run check_pages --unit BK4.")
F("BK4a8-L02-E2-only-scope", "2.4-mathematics / problem scope words", f"{L2}:372-374",
  "E2 is worded 'Using only Lab 1, Part C, name the member with the largest net obligation owed to it, and the member with the largest net obligation it owes.' The solution then also uses the netted amount printed in Part D (L02:374, '5093600 cents, is the netted amount printed in Part D'). The 'only' restriction is contradicted by its own solution.",
  "Either delete 'only' from the prompt, or delete the Part D sentence from the solution (the Part C figures 3340300 and -3627000 answer the question alone). Prose-only change.")

P("BK4a7-L01-legend-B-template", "2.3-grades template", f"{L1}:45; {L2}:45; {L3}:45; course/templates/lesson.html:47; BLUEPRINT.md:160",
  "Shared legend 'B published, not settled' (template text, also in merged AC1/AC2/AC4). BLUEPRINT.md:160 defines B as published in a top peer-reviewed venue, not robustly replicated or actively contested. No claim in BK4 slice a is graded B (grep of data-grade in claim spans: T and C only). Recorded as a template matter for the owner, not a slice-a defect (see notes).")
P("BK4a7-L02-duffie-attribution-abstract", "2.1-citations", f"{L2}:277,285,425",
  "The lesson attributes only the question of the title to Duffie and Zhu (2011) and states no finding. The abstract could not be read: plain curl to https://doi.org/10.1093/rapstu/rar001 returned HTTP 403 (duffie_crossref.out); the Crossref record has no abstract. No sentence depends on it.")
P("BK4a7-gate-check-projects", "2.9-structure gate", "tools/check_projects.py --unit BK4",
  f"Re-run this round: {S}/gate_check_projects.txt -> 'check_projects BK4: PASS', exit 0. Project content itself is slice b.")

# --- ensure every prior id is accounted for
missing = [i for i in prev_ids if i not in R]
extra = [i for i in R if i not in prev_ids]
print("missing", missing)
print("extra (new rows)", extra)
rows = []
order = prev_ids + [i for i in R if i not in prev_ids]
for i in order:
    if i not in R:
        continue
    check, loc, status, ev, fix = R[i]
    row = {"id": i, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

fails = [r for r in rows if r["status"] != "PASS"]
passes = [r for r in rows if r["status"] == "PASS"]
frag = {
    "unit": "BK4",
    "slice": "BK4-a",
    "round": 8,
    "verifier": "Haiku independent verifier, BK4-a round 8 (did not build BK4)",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    
    "checkout": ROOT,
    "scratch": f"{ROOT}/{S}",
    "verified_at": "2026-11-04T23:30:00Z",
    "verdict": "FAIL" if fails else "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Byte-identical to the round-7 pin: index.html, L02.html, L03.html, tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py, quiz.js, lesson.html, hub.html. Changed: L01.html (2 hunks), project.html (3 hunks, one read for the hub cross-check; project itself is slice b). No round-7 PASS row was carried: every row id was re-checked this round against the subject as it stands at 0dee921, with the evidence named in the row.",
        "Full read this round: index.html (all 197 lines), L01.html (all 555 lines), L02.html (all 528 lines), L03.html (all 657 lines), the three twins (page code diffed against twin files).",
        "Mutants: none. Verifier rules 2.6 mutation applies to project graders; lab twins are demonstrations (FINAL-ARCHITECT-RULINGS ruling 9 context). No grader in this slice.",
        "Notes not failing a row: (a) index.html:71 says 'Below the bar, revisit the prerequisites first' while quiz.js:78 says 'work through the lessons and every rung of the ladder'. Both can hold; flagged for the builder's judgement. (b) BLUEPRINT.md:160-161 grade B reads 'published in a top peer-reviewed venue'; the shared legend (lesson.html:47, L01-L03 line 45) reads 'published, not settled'. No B claim exists in slice a, so the legend is a template matter for the owner, not a slice-a defect.",
        "Duffie and Zhu (2011): the abstract is not readable (doi.org HTTP 403 to plain curl; Crossref has no abstract). No slice-a sentence depends on it.",
        "Hub claims about L04 and L05 (objectives 4-5 and the lesson cards) were checked for existence and for matching wording only; their content belongs to slice b.",
    ],
    "summary": {"rows": len(rows), "pass": len(passes), "fail": len(fails), "unverifiable": 0},
}
out = f"{ROOT}/ledgers/BK4/BK4-a.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, "rows", len(rows), "pass", len(passes), "fail", len(fails))
