"""Builds the round-7 fragment for BK4 slice a from the verifier's evidence (rows are written by hand above).

Every row id from round 6 (/Users/billyribeiro/.fanout/frags/E-BK4-a.round6.json) is kept. Each row's status is the
verifier's round-7 result, re-derived this round from the cited lines and the scripts under ledgers/BK4/scripts/BK4-a-r7/.
"""
import json
import subprocess
from datetime import datetime, timezone

R = "ledgers/BK4/scripts/BK4-a-r7/"
rows = []


def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- hub (index.html) ----
row("BK4a-hub-hours-arithmetic", "2.9-structure hours", "index.html:29,40,42,138,140-144,162-174", "PASS",
    "data-hours-lessons=35 and data-hours-project=15 (index.html:29); bar 70%/30% (index.html:40); lessons 7 h each "
    "(L01-L05 eyebrow 'Lesson n of 5 · 7 study hours'); project table 2+2+3+3+2+2+1 = 15 (index.html:167-174, "
    "matches project.html:376-383); 35+15=50.")
row("BK4a-hub-placement-arithmetic", "2.9-structure placement bar", "index.html:71", "PASS",
    "Eight items (index.html:74-131: six prerequisite items, two data-skill items at lines 119 and 124). 0.8 x 8 = 6.4, so "
    "seven correct are needed; 6/8 = 75 percent and 7/8 = 87.5 percent (recomputed). quiz.js:72-75 reads the bar as "
    "correct/total >= mastery.")
row("BK4a-hub-placement-keys", "2.9-prose answer keys", "index.html:74-131", "PASS",
    "Q1 110/1.1 = 100; Q2 (1-(1/2)^3)/(1/2) = 1.75; Q3 lim 2x at 3 = 6; Q4 Bertrand price = c; Q5 grade C matches "
    "BLUEPRINT.md:161; Q6 FC1 lifecycle order matches course/modules/FC/FC1/L05.html:63 (clearing precedes settlement); "
    "Q7 min(120-100, 50) = 20; Q8 remainder to the first surviving member with DF>0 matches project.html:90,220 and "
    "L03.html:73. Each MC item has exactly one data-correct (grep count).")
row("BK4a-hub-prereq-chain", "2.11-dag prerequisites", "index.html:35,61; curriculum/02-economics-finance-core.yaml:367,1075; "
    "yaml:22 (E1 prereqs [M2]); curriculum/01-foundations.yaml:126 (M2 prereqs [M1])", "PASS",
    "FC1 prereqs [P0.1, E1]; E1 prereqs [M2]; M2 prereqs [M1]. 'through them M1' is correct.")
row("BK4a-hub-P0.1-link", "2.9-prose status", "index.html:35", "PASS",
    "The FC1 href resolves (links_check.out, 69 links, 0 problems). No course/modules/P0 directory exists, so the "
    "'not yet released' sentence is the program's convention (also in M1 and FC1 pages).")
row("BK4a-hub-financial-intermediary", "2.11-dag prerequisite list", "index.html:61-66", "PASS",
    "Three FC1 concepts linked to course/concepts.html#clearing-and-settlement, #trade-lifecycle, #bank-money-creation, "
    "which exist (concepts.html:477,483,485). clearing-and-settlement and trade-lifecycle are used in L01.html:37; "
    "bank-money-creation is used in L04.html:38,368 (not this slice).")
row("BK4a-hub-bertrand-trade-fee", "2.11-dag prerequisite use", "index.html:65", "PASS",
    "Sentence 'No lesson or project in BK4 uses present value, the geometric series, the limit or Bertrand competition'. "
    "Grep of index.html, L01-L03 and project.html for present value, discount, geometric, series, limit, Bertrand, "
    "competition: hits only in the placement items (index.html:74-99) and in unrelated words (limits of the simulator, "
    "project.html:416; 'sale at a discount', L04). Claim holds.")
row("BK4a-hub-concept-anchors", "2.11-dag links", "index.html:63-66; L01.html:37,59,64; L02.html:37,64,81,275; L03.html:37,67,134", "PASS",
    "Every concept link and def anchor in the slice resolves (links_check.py / links_check.out: 69 hrefs, 0 problems). "
    "check_dag --unit BK4 PASS.")
row("BK4a-hub-ladder-vs-project", "2.6-project ladder (hub description)", "index.html:150-156 vs project.html:45-48,107,201", "PASS",
    "Rung descriptions agree: four-member house (project.html:45,59); 40 seeded SIMULATED scenario losses "
    "(project.html:107); completion problem with two blanks (project.html:46); clearing_house.py to the interface "
    "(project.html:47,201); stretch not graded (project.html:48). The skip rule is a separate row (BK4a7-hub-skip-rule-vs-project).")
row("BK4a-hub-data-status", "2.8-data", "index.html:37,182; tools/data_sources.yaml:19,53,91", "PASS",
    "Embedded ids are fx_daily, fx_monthly and ust_daily only (data_sources.yaml). No data-files attribute in index, L01-L03.")
row("BK4a-hub-reading-list", "2.1 citations", "index.html:186-194; references/references.json (duffie2011central, bisndcpmi)", "PASS",
    "Curriculum lists three sources (yaml:1089-1092); two are registry keys, the third (SEC T+1) is not admitted "
    "(no sec.gov record in references.json; review_queue.json:830). Live tools/verify_refs.py --unit BK4: 2 of 560 "
    "entries, 0 problems.")
row("BK4a-hub-process-words", "2.9-banned / process words", "index.html (visible text)", "PASS",
    "ledgers/BK4/scripts/BK4-a-r7/banned_scan.py -> banned_scan.out: hits 0 (banned phrases, process words, ellipses).")

# ---- L01 ----
row("BK4a-L01-numbers", "2.2-numbers", "L01.html:51,254-286,409,55", "PASS",
    "rederive_L01.py -> rederive_L01.out reproduces every printed value: gross 2841600; nets +379800, -1533900, +1154100 "
    "(sum 0); RTGS needs 112500, 1533900, 0; DNS debits 0, 1533900, 0; moved 1533900; 1 funded bank; 1 need>debit bank. "
    "Ratio 1533900/2841600 = 0.53980152...; 4 places 0.5398; percent 53.98. Interpretation text at L01.html:286 matches.")
row("BK4a-L01-prop-2.2-2.4", "2.4-mathematics", "L01.html:84-111", "PASS",
    "Prop 2.2 proof: feasible set o_i >= max(0,-mu), least element = need. Prop 2.3 proof: each payment adds +a and -a. "
    "Prop 2.4 proof uses k=m in the minimum and monotonicity of max(0,.); strictness by Example 2.6 (100 vs 50). "
    "Re-read in full this round.")
row("BK4a-L01-P2-iff", "2.4-mathematics", "L01.html:375-377", "PASS",
    "P2 solution covers the three cases mu>=0; mu<0 with S_m=mu; mu<0 with S_m>mu (debit 0 or -S_m < -mu, so they differ). "
    "Hypotheses listed (mu <= S_m, Prop 2.2, Section 2 definitions).")
row("BK4a-L01-examples-remarks", "2.4-mathematics", "L01.html:119-126", "PASS",
    "Example 2.6 running sums recomputed: A 0,-100,-100,-50; B 0,100,20,20; C 0,0,80,30; minima -100,0,0; nets -50,20,30; "
    "debit A 50; gross 230 (rederive_L01.out). Remark 2.7: A 0,50,-50,-50, need 50, debit 50.")
row("BK4a-L01-problems-M-P-E-R", "2.4/2.5 problem solutions", "L01.html:343-434", "PASS",
    "M1 need 200, debit 200 (rederive_L01.out 'M1'); M2 need 200, debit 100; M3 running 0,40,-30,-20, need 30, debit 20. "
    "P1-P3 proofs read and correct (P3 uses scaling by c>0). E1 1533900 both; E2 one bank (A); E3 base 2841600, 53.98 percent. "
    "R1-R3 checked (R3 running 0,-100,-100,0, need 100).")
row("BK4a-L01-remark-3.1-order", "2.4-mathematics", "L01.html:300; 432-434", "PASS",
    "Remark 3.1: inflows-first gives running minimum min(0,Net), so Need = Debit; R1 proof uses it. Correct.")
row("BK4a-L01-R3", "2.4-mathematics", "L01.html:432-434", "PASS",
    "Three-payment cycle of 100 dollars: nets 0; running A 0,-100,-100,0; need 100 (rederive_L01.out 'R3').")
row("BK4a-L01-remark-2.8", "2.5-lab statements", "L01.html:291 vs lab Part B/C (twin output)", "PASS",
    "Part B prints the Prop 2.4 check per bank and Part C the zero sum (tests/labs twin output, run_labs PASS).")
row("BK4a-L01-interp-three-inequalities", "2.5-lab interpretation", "L01.html:286 vs lab output", "PASS",
    "Each figure in the interpretation (379800 net, 0 debit, 112500 need; 1533900; 2841600; 1533900 moved) equals the printed output.")
row("BK4a-L01-misconception-1", "2.9-misconceptions", "L01.html:322 vs lab Part B (L01.html:269-271)", "PASS",
    "Re-verified after the round-6 fix (sentence now cites Prop 2.4): Bank A need 112500 with debit 0; Bank B net -1533900 "
    "and debit = need = 1533900 (printed Part B).")
row("BK4a-L01-misconceptions-2-3", "2.9-misconceptions", "L01.html:326,330", "PASS",
    "Bank A net +379800, debit 0, need 112500 (Part B); Remark 2.7 need 100 -> 50, debit 50 unchanged.")
row("BK4a-L01-quiz", "2.9-quiz", "L01.html:463-534", "PASS",
    "10 items; each MC has one data-correct; answers recomputed: 200 (net -200), 200 (M1), 200 (doubled), 50 (Remark 2.7), "
    "net zero, 50 for net +50 gives debit 0, lag 'a lab parameter', 28416 dollars for 2841600 cents, T+1 'named'.")
row("BK4a-L01-lab-twin", "2.5-labs", "L01.html:128-287; tests/labs/BK4/lab-BK4-L01-1.py", "PASS",
    "run_labs --unit BK4 PASS (block equality and expected output). Twin alone: venv CPython 3.14.8 python -I -W error exit 0, "
    "stderr 0 bytes (gate_run_labs.txt; twin_L01_out.txt). Docstring claims (seed, twelve payments, whole dollars, integer cents, "
    "no rounding) match code lines 3-12 and 39-46.")
row("BK4a-L01-notation", "2.4 notation (notation.json)", "index.html; L01.html; L02.html; L03.html math spans", "PASS",
    "Scan of 12+178+176+381 math spans (inline): no T, Q, R, Phi, gamma, mathbb. Macros used: \\mathrm, \\max, \\min, \\sum, "
    "\\le, \\ge, floors, \\ell, \\delta, \\mathcal, \\infty; none conflicts with notation/notation.json (symbols T, Phi, gamma_3, "
    "gamma_4, R^ast, R^{e ast}, R_f, Q). \\R not used.")
row("BK4a-L01-dag-defs", "2.11-dag / define before use", "L01.html:37,59,64; index.html:66", "PASS",
    "def-payment-system (L01.html:59) and def-settlement-cycle (L01.html:64) are the only data-concept defs; hub links them "
    "(index.html:66). check_dag PASS.")
row("BK4a-L01-why-words", "2.9-prose length", "L01.html:51", "PASS", "Why-it-matters paragraph counted: 107 words (limit 120).")
row("BK4a-L01-structure", "2.9-structure", "L01.html:34-552", "PASS",
    "Sections 1-9 in template order: definitions (Section 1), liquidity (2), conditions on proofs (3), settlement cycle (4), "
    "misconceptions (5, three), problem set (6: M1-M3, P1-P3, E1-E3, R1-R3), key results (7), quiz (8, 10 items), references (9). Hours 7.")
row("BK4a-L01-grades", "2.3-grades", "L01.html:43-48, 84, 94, 104, 446-452", "PASS",
    "Grade legend and grades match BLUEPRINT.md:159-163 (B legend is the template shorthand; see notes). Proved items are T, "
    "lab-based claims are C (lab named, SIMULATED).")
row("BK4a-L01-FC1-claim", "2.9-prose cross-reference", "L01.html:55", "PASS",
    "FC1 Lesson 5 is the trade-lifecycle lesson (course/modules/FC/FC1/L05.html:63 defines the six states in this order).")
row("BK4a-L01-canon-breaks-wording", "2.9-prose", "L01.html:308-313", "PASS",
    "Four limits (queues, given day, settlement lag, which real system). None states a fact about a real system.")

# ---- L02 ----
row("BK4a-L02-prop-2.2", "2.4-mathematics", "L02.html:85-99", "PASS",
    "(a) each trade enters one receivable and one payable (A2); (b) sum n_i = G - G = 0; (c) max(0,x) - max(0,-x) = x; "
    "(d) A <= G from Pay_i >= 0 and Rec_i >= 0. Assumptions A1-A3 listed before the statement.")
row("BK4a-L02-prop-2.3-title", "2.4-mathematics", "L02.html:102-103", "PASS",
    "Title 'no netting reduction is achieved exactly when no member both receives and pays' matches the statement A = G iff "
    "each member has Rec = 0 or Pay = 0.")
row("BK4a-L02-prop-2.3-proof", "2.4-mathematics", "L02.html:106-109; 348-349 (P2)", "PASS",
    "Three cases (Rec=0; Rec>0,Pay=0; Rec>0,Pay>0) cover the terms; the strict case gives A < G. Re-read in full.")
row("BK4a-L02-example-2.4", "2.2-numbers", "L02.html:112-113; 270; 294", "PASS",
    "n = -50, 20, 30; A = 50; G = 230; floor(10000 x 180/230) = 7826 (Fraction 7826.0869...), rederive_L02.out.")
row("BK4a-L02-lab-claims", "2.5-lab statements", "L02.html:123,127; tests/labs/BK4/lab-BK4-L02-1.py main()", "PASS",
    "Twin checks: receivables equal gross (line 220), nets sum to zero (227), payers equal payees after netting (234), A <= G (235). "
    "Page statements match.")
row("BK4a-L02-lab-numbers", "2.2/2.5 lab numbers", "L02.html:241-269 (expected); 270 (interpretation); 365-381 (E1-E3)", "PASS",
    "rederive_L02.py reproduces the six trades (generator from Random(2026)), receivables, payables, nets -3627000/+1753300/"
    "+3340300/-1466600, A 5093600, reduction 2502700, floor 3294 bps. All printed values match.")
row("BK4a-L02-lab-numbering", "2.9-structure", "L02.html:121,123,125-127,270", "PASS", "Lab 1 is the only lab in the lesson; labels consistent.")
row("BK4a-L02-attribution", "2.1 attribution", "L02.html:277,285,425; references/references.json:7411-7432", "PASS",
    "Registry title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', authors Duffie and Zhu, Review of Asset "
    "Pricing Studies 2011, verified by Crossref (live verify_refs). The lesson attributes only the question, and states no finding.")
row("BK4a-L02-canon-misconceptions", "2.9-misconceptions", "L02.html:280-285, 293-302", "PASS",
    "Four limits; misconceptions checked against Prop 2.2(b),(c) and Lab Part C/D (zero-sum and positive netted amount).")
row("BK4a-L02-problems", "2.4/2.2 problem solutions", "L02.html:315-406", "PASS",
    "M1 nets -10,-20,50,-20, A 50, G 180, 7222 bps; M2 G 460, A 100, 7826 bps; M3 nets -200,100,100, A = G = 200; P1-P3 "
    "correct; E1-E3 match Parts B-D; R1-R3 correct (R2 X/Y nets, rederive_L02.out).")
row("BK4a-L02-key-results", "2.3-grades", "L02.html:416-425", "PASS", "T rows are proved on the page; C rows name Lab 1 or are question-only.")
row("BK4a-L02-quiz", "2.9-quiz", "L02.html:432-510", "PASS",
    "10 items, each MC has one data-correct; answers recomputed: 20; 50; zero sum; 7826; equality case; 100; no money move; "
    "zero sum not a guarantee; 50936 dollars; zero netted amount for a cycle.")
row("BK4a-L02-lab-twin", "2.5-labs", "L02.html:121-271; tests/labs/BK4/lab-BK4-L02-1.py", "PASS",
    "run_labs PASS; twin alone under venv CPython 3.14.8, python -I -W error, exit 0, stderr 0 bytes (twin_L02_out.txt). "
    "Docstring (four members, six trades, seed, integer cents, floor only in bps) matches the code.")
row("BK4a-L02-why-structure", "2.9-structure", "L02.html:34-518", "PASS",
    "Sections 1-9; why-it-matters 96 words; 4 canon limits; 3 misconceptions; problem set 3+3+3+3; quiz 10 items; hours 7.")
row("BK4a-L02-meta-description", "2.9-prose", "L02.html:7", "PASS",
    "Meta description states the Lab 1 scope (four members, six trades, integer cents, seeded SIMULATED) that the lab implements.")

# ---- L03 ----
row("BK4a-L03-legend", "2.3-grades", "L03.html:43-48", "PASS", "Same legend as L01 (see BK4a7-L01-legend-B-template).")
row("BK4a-L03-four-resources", "2.9-prose", "L03.html:55; 418", "PASS",
    "The intro names three resources (margin, default fund, CCP capital) and then the survivors' default funds; Definition 1.1 has exactly those layers.")
row("BK4a-L03-notation-d", "2.4 notation", "L03.html:61,69-71,100,139,480-482", "PASS",
    "Notation scan of the 381 math spans: no registry symbol used; local symbols (IM_delta, DF_i, K, L, a_1..a_3, Z, D, ell, x_i, p_i, c(M), S, L_(k), t, k) are defined at first use.")
row("BK4a-L03-def-props-1.2-1.3", "2.4-mathematics", "L03.html:66-96", "PASS",
    "Definition 1.1 layer order and survivor rule; Prop 1.2 conservation (proof cases Z>=D and Z<D); Prop 1.3 (0 <= ell <= n+ - 1; x_i+1 <= DF_i). Re-read in full.")
row("BK4a-L03-remark-1.4", "2.4-mathematics", "L03.html:100-101", "PASS",
    "a2>0 implies a1 = IM; a3>0 implies a2 = DF; Z>0 implies a3 = K; each follows from min(.,.) < argument.")
row("BK4a-L03-example-1.5", "2.2-numbers", "L03.html:104-121; table 108-117; lab Part A1 output", "PASS",
    "All eight table rows (80,120,170,180,181,200,205,300) equal the recomputed layers (rederive_L03.out 'A1'): e.g. 200 -> 8, 12; 300 -> 40, 60, uncovered 20.")
row("BK4a-L03-example-1.6", "2.2-numbers", "L03.html:124-126; lab Part A2 output", "PASS",
    "Loss 1: member 1 pays 1; loss 2: members 1 and 2 pay 1 each (rederive_L03.out 'A2').")
row("BK4a-L03-def-2.1-prop-2.3", "2.4-mathematics", "L03.html:133-165", "PASS",
    "Definition 2.1 cover floor and basis stated; Prop 2.3 with k = ceil(tS/10000), Parts 1-3 re-read; A3, A4 listed.")
row("BK4a-L03-cor-2.4-ex-2.5", "2.4-mathematics; 2.2-numbers", "L03.html:168-181; lab Part B output", "PASS",
    "Corollary 2.4 proof uses ceiling monotonicity and sorted losses. Example 2.5: 9900*200/10000 = 198 (k=198); 9975*200/10000 = 199.5 (k=200); "
    "printed sized margins 2961 and 2992 match rederive_L03.out.")
row("BK4a-L03-R1-note", "2.4-mathematics", "L03.html:530-533", "PASS",
    "Real-valued margins: {M : cover >= t} = [L_(k), inf), smallest element L_(k). Correct.")
row("BK4a-L03-canon-bullet-6", "2.9-prose / 2.4 scope", "L03.html:422 (round 6 cited 421)", "PASS",
    "Re-verified after the round-6 fix. At 9900 bps, S=200: the sized margin is L_(198); the printed cover 9900 gives c=198 and "
    "two scenarios above. The general statement is conditioned: two lie above only when L_(198) < L_(199); ties leave fewer "
    "(printed draw: L(198)=2961 < L(199)=2981, rederive_L03.out). The 'each scenario above the margin' sentence is correct.")
row("BK4a-L03-misconceptions", "2.9-misconceptions", "L03.html:430-443", "PASS",
    "Four misconceptions; each corrected by a cited definition, remark or lab part (Remark 2.2, Example 2.5, Remark 1.4, Part A3 output).")
row("BK4a-L03-problems", "2.4/2.2 problem solutions", "L03.html:455-546", "PASS",
    "M1 8, 12, total 200; M2 7500 cover, k=3, margin 3000; M3 40, 50, 50; P1-P3 proofs correct; E1 3058+102; E2 residual 857, "
    "312+381+164 = 857, DF/2 exact; E3 198 of 200; R1 correct; R2 S=100 k=99/100; R3 k=S iff S<=399 (S=400 gives k=399).")
row("BK4a-L03-key-results", "2.3-grades", "L03.html:556-566", "PASS",
    "All T rows proved in-section; C rows (lab fixtures and seeded losses) name Lab 1 Parts A1, A2, B.")
row("BK4a-L03-quiz", "2.9-quiz", "L03.html:571-646", "PASS",
    "10 items; one data-correct per MC; answers recomputed: default fund; 8; 20; yes (L_s <= M); 7500; k=3; 50; 1 cent; 198 of 200; k=399.")
row("BK4a-L03-lab-twin", "2.5-labs", "L03.html:187-411; tests/labs/BK4/lab-BK4-L03-1.py", "PASS",
    "run_labs PASS; twin alone under venv CPython 3.14.8, -I -W error, exit 0, stderr 0 bytes (twin_L03_out.txt). "
    "Inputs of A3/B regenerated from Random(2026) and match the printed header (rederive_L03.out); B k, sized margin and brute-force minimum agree.")
row("BK4a-L03-why-structure", "2.9-structure", "L03.html:34-657", "PASS",
    "Sections 1-7; why-it-matters 118 words (limit 120); 6 canon limits; 4 misconceptions; problem set 3+3+3+3; quiz 10; hours 7.")
row("BK4a-L03-uses-meta", "2.9-DAG", "L03.html:37", "PASS",
    "Uses central-counterparty and multilateral-netting, linked to L02.html#def-central-counterparty and #def-multilateral-netting (both exist, L02.html:64,81).")

# ---- round-6 FAIL rows, re-verified ----
row("BK4a6-L03-lab-docstring-seed", "2.5 labs (docstring claim vs code)", "tests/labs/BK4/lab-BK4-L03-1.py:3-7; course/modules/BK/BK4/L03.html:192-198", "PASS",
    "Re-verified after the round-6 fix. The docstring now says the Part A3 and B inputs are seeded and the Part A1 and A2 inputs are "
    "the stated fixtures. Code: fixtures hard-coded (lines 342-343, 353-356); seeded draws at lines 334-336 (A3 inputs) and 369 (B). "
    "The page copy equals the twin (run_labs PASS).")
row("BK4a6-L03-corollary-heading", "2.9-prose (heading vs statement)", "course/modules/BK/BK4/L03.html:168", "PASS",
    "Re-verified after the round-6 fix. Heading 'the sized margin does not fall as the target rises' matches Corollary 2.4 "
    "(M(t) <= M(t'), non-strict).")

# ---- gates and cross-checks ----
row("BK4a-gate-check-pages", "gate", "tools/check_pages.py --unit BK4", "PASS", R + "gate_check_pages.txt: check_pages BK4: PASS (exit 0).")
row("BK4a-gate-check-dag", "gate", "tools/check_dag.py --unit BK4", "PASS", R + "gate_check_dag.txt: check_dag BK4: PASS (exit 0).")
row("BK4a-gate-run-labs", "gate", "tools/run_labs.py --unit BK4", "PASS", R + "gate_run_labs.txt: run_labs BK4: PASS (8/8).")
row("BK4a-gate-page-smoke", "gate", "tools/page_smoke.py --unit BK4 --pages index L01 L02 L03 (run alone)", "PASS",
    R + "gate_page_smoke.txt: all four pages PASS; zero console errors, no horizontal scroll, lab runtimes 0.0 s.")
row("BK4a-gate-ruff-mypy", "gate", "ruff check/format --check, mypy --no-incremental on tests/labs/BK4 (three twins)", "PASS",
    R + "gate_ruff_mypy.txt: All checks passed; 8 files formatted; mypy no issues in 3 source files.")
row("BK4a-gate-pytest-labs", "gate", "pytest tests/test_labs.py -k BK4; tests/test_page_checks.py", "PASS",
    R + "gate_pytest_labs_bk4.txt: 8 tests, exit 0; ledgers/BK4/scripts/BK4-a-r7/gate_pytest_page_checks.txt: 41 tests, exit 0.")
row("BK4a-gate-verify-refs", "2.1 citations", "tools/verify_refs.py --offline; --unit BK4", "PASS",
    R + "gate_verify_refs_offline.txt: 560 entries, 0 problems. " + R + "gate_verify_refs_unit_BK4.txt: live, 2 of 560 entries, 0 problems.")
row("BK4a-banned-and-process", "2.9-banned", "index.html; L01-L03 visible text", "PASS", R + "banned_scan.out: hits 0.")
row("BK4a-scope-words", "2.4 scope words", "index.html; L01-L03 (301 hits)", "PASS",
    R + "scope_words.txt lists all 301 hits (every/all/any/never/exactly/same/only/none, each). Each universal is backed by a "
    "proof, a finite enumeration in Lab 1 or a definition; quoted misconceptions and quiz distractors are labelled as such.")
row("BK4a-hub-settlement-framing", "2.9-prose / B1 settlement facts", "index.html:33", "PASS",
    "The lede states a model convention ('In this unit's model, a trade settles when its payment has moved'). No T+1 fact is stated.")
row("BK4a-hub-P0.1-grade-source", "2.3-grades / prose", "index.html:108", "PASS",
    "Grade C wording matches BLUEPRINT.md:161 (working paper, practitioner research, single-sample evidence).")
row("BK4a-hub-card-L02", "2.9-hub lesson map", "index.html:141", "PASS",
    "Card text (novation, CCP, net obligations summing to zero, netted amount vs gross notional, Lab 1 seeded SIMULATED) matches L02.")
row("BK4a-L01-canon-bullet-only-designs", "2.9-prose", "L01.html:313", "PASS",
    "States that no admitted source covers which real system uses which design; consistent with the registry (no payment-system record).")
row("BK4a-L01-A2-forward-ref", "2.9-prose", "L01.html:71; 79-80", "PASS",
    "Assumption A2 says the net debit is 'defined in Definition 2.1' (explicit forward pointer, not an undefined use). Acceptable.")
row("BK4a-L01-R1-order-claim", "2.4-mathematics", "L01.html:420", "PASS",
    "Proof of R1 uses Remark 3.1 and Prop 2.4; the hypothesis that net positions do not depend on order is named.")
row("BK4a-rederive-r4", "2.2 independent re-derivation", "ledgers/BK4/scripts/BK4-a-r7/rederive_L01.py/.out, rederive_L02.py/.out, rederive_L03.py/.out", "PASS",
    "Three scripts re-derive every printed lab value and every worked number from the seeds and from Fraction; all comparisons True.")
row("BK4a-lab-block-equality-r4", "2.5 lab blocks", "run_labs --unit BK4 (page code = twin; expected = output)", "PASS",
    R + "gate_run_labs.txt: 8/8 PASS (code byte-identical to twin; expected block matches output under the page rule).")
row("BK4a-gate-repo-ruff-mypy-r4", "gate", "tests/labs/BK4 (slice-scope ruff/mypy)", "PASS", R + "gate_ruff_mypy.txt.")
row("BK4a5-L01-lede-settlement-framing", "2.1 / B1 settlement facts", "L01.html:51", "PASS",
    "States 'The lesson describes no real payment system.' and no settlement rule as fact.")
row("BK4a5-L01-designs-pointer", "2.9-prose cross-reference", "L01.html:59", "PASS", "Definition 1.1 names the two designs; no real-system claim.")
row("BK4a5-L01-canon-heading", "2.9-prose", "L01.html:308", "PASS", "Heading 'The model stops' matches the four limits below it.")
row("BK4a5-L02-canon-heading", "2.9-prose", "L02.html:280", "PASS", "Heading matches the four limits (L02.html:282-285).")
row("BK4a5-hub-prereq-uses", "2.9-prose / 2.11-dag", "index.html:61-66", "PASS",
    "Hub prerequisite list uses only FC1 concepts that FC1 defines (concepts.html:477,483,485).")
row("BK4a5-links-anchors", "2.9-links", "index.html; L01-L03 (all hrefs)", "PASS", R + "links_check.out: 69 links, 0 problems.")
row("BK4a5-twins-alone", "2.5-labs", "tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, lab-BK4-L03-1.py", "PASS",
    "Each run alone under venv CPython 3.14.8 with python -I -W error: exit 0, stderr empty (twin_L0x_out.txt).")

# ---- round-7 new rows ----
row("BK4a7-hub-skip-rule-vs-project", "2.9-prose / 2.6 ladder (cross-page)",
    "course/modules/BK/BK4/project.html:43 (contradicts index.html:71,150)", "FAIL",
    "The hub (index.html:71 and :150) and the placement quiz (course/assets/js/quiz.js:72-75: 'you may skip rungs 1-2' only when "
    "the overall bar AND every data-skill item are correct) say a student must reach the bar and answer both skill checks. "
    "project.html:43 says 'If you met the placement bar on the module page, skip rungs 1 and 2'. Verified with sed on project.html:43 "
    "and quiz.js:56-77. The round-6 hub-ladder row did not cite this line.",
    "Owner: the project slice. Replace project.html:43 with: 'If you met the placement bar on the module page and answered both "
    "skill checks, skip rungs 1 and 2 and start at rung 3.' (the same rule as index.html:71,150 and quiz.js:72-75).")
row("BK4a7-L03-scenario-intro-before-def", "2.9 define before use (term-level)",
    "course/modules/BK/BK4/L03.html:51 (scenario losses, defaulter's margin); :55 (defaulter); :134 (scenario set)", "PASS",
    "The introduction paragraph (L03:51) uses 'scenario losses' and 'the defaulter's margin' as preview wording before "
    "Definition 1.1 (L03:55) and Definition 2.1 (L03:134). No statement in Sections 1-2 uses either before its definition, and "
    "the intro's wording is descriptive, so this is not a define-before-use defect.")
row("BK4a7-L01-legend-B-template", "2.3 grades (legend)", "course/modules/BK/BK4/L01.html:45 (and L02:45, L03:45); BLUEPRINT.md:160",
    "PASS",
    "The legend reads 'B published, not settled' (course/templates/lesson.html:47, the program template, also in the merged AC1, AC2, AC4 "
    "pages). BLUEPRINT.md:160 defines B with a venue criterion. The legend is a shorthand; no claim in BK4 slice a is graded B, so no "
    "claim-level grade changes. Recorded as a note for the owner of the template.")
row("BK4a7-L02-duffie-attribution-abstract", "2.1 attribution (abstract)", "course/modules/BK/BK4/L02.html:277,285,425",
    "PASS",
    "The lesson attributes only the question of the title to Duffie and Zhu (2011) and states no finding, so no claim depends on the "
    "abstract. The abstract was not read by the verifier (see what could not be checked). Plan B2 is respected.")
row("BK4a7-gate-check-projects", "gate (cross-check)", "tools/check_projects.py --unit BK4", "PASS",
    R + "gate_check_projects.txt: check_projects BK4: PASS (exit 0). Project content itself is in another slice.")

notes = [
    "Round 7 of BK4-a (hub index.html, L01.html, L02.html, L03.html, labs tests/labs/BK4/lab-BK4-L01-1.py, lab-BK4-L02-1.py, "
    "lab-BK4-L03-1.py). Pin 06994db16d1ab449bcf29898a7f56cfa999dce57 (HEAD). Base 4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin). "
    "Delta for the slice: L01.html lines 76, 305, 322; L02.html lines 379, 381; L03.html lines 130, 168, 192-198 (docstring copy), 422; "
    "tests/labs/BK4/lab-BK4-L03-1.py lines 3-7. index.html and lab-BK4-L01-1.py and lab-BK4-L02-1.py are byte-identical to the base.",
    "Every page in the slice was read in full (stripped-text views with source line numbers, strip.py), and every number and "
    "claim was checked. Rows carried from round 6 were NOT carried on trust: every row was re-verified this round with the "
    "evidence named in it. Every round-6 row id is kept (92 ids).",
    "Round-6 FAIL rows BK4a-L03-canon-bullet-6, BK4a6-L03-corollary-heading and BK4a6-L03-lab-docstring-seed are re-verified as PASS "
    "after the 06994db fixes.",
    "Only non-PASS row: BK4a7-hub-skip-rule-vs-project. It is a cross-page defect whose defect site is project.html:43 (project slice, "
    "not this slice's file). The hub text is correct and matches quiz.js.",
    "Mutants: none. Slice a has no grader (grader/ is another slice). The lab twins are demonstrations; mutation testing does not apply "
    "to them (FINAL-ARCHITECT-RULINGS 9; the verifier rules ruling on labs).",
    "Hours: arithmetic only (hub 35 + 15 = 50; lessons 7 h; project components 15). Hours are design targets.",
    "Cards (cards.json), L04, L05, project.html, grader/ and the hub-described L04/L05 content are other slices and were not "
    "verified here, except for the hub titles and the grep-based scope checks that the hub's own sentences require.",
]

registry_flags = [
    "SEC T+1 rule (plan B1): not admitted. references/review_queue.json:830 holds the entry. No lesson in slice a states the T+1 rule as a fact (L01.html:64, 312).",
    "CPMI (bisndcpmi) is index-level only; no slice-a sentence attributes a report, principle or data item to it (index.html:191; L02/L03 do not cite it).",
    "duffie2011central: registry title and authors match the lesson; the paper's findings are not stated anywhere in the slice (plan B2).",
]

summary = {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"),
           "fail": sum(1 for r in rows if r["status"] == "FAIL"),
           "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE")}
verdict = "PASS" if summary["fail"] == 0 and summary["unverifiable"] == 0 else "FAIL"

frag = {
    "unit": "BK4",
    "slice": "BK4-a",
    "round": 7,
    "verifier": "Haiku independent verifier, BK4-a round 7 (did not build BK4)",
    "pin": "06994db16d1ab449bcf29898a7f56cfa999dce57",
    "base": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07 (round-6 pin; fixes 06994db1 are the delta)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE7-BK4-a",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE7-BK4-a/ledgers/BK4/scripts/BK4-a-r7",
    "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
with open("ledgers/BK4/BK4-a.json", "w", encoding="utf-8") as f:
    json.dump(frag, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("rows", summary, "verdict", verdict)
