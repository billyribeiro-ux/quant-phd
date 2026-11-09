import json, datetime
C = "Carried from round 6 (byte-identical since the previous pin e896b7a4; no delta hunk in the cited range): "
R = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    R.append(r)

# ---- gates (all re-run this round in the checkout)
row("FC2b-cmd-check_pages", "gate", "index, L01-L08, cards.json (unit gate)", "PASS",
    "Run this round: .venv/bin/python tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 (ledgers/FC2/scripts/FC2-b-r7/gates1.txt).")
row("FC2b-cmd-check_dag", "gate", "L04-L06 links and dfn", "PASS",
    "Run this round: tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 (gates1.txt).")
row("FC2b-cmd-check_projects", "gate", "project.html (unit gate, outside slice)", "PASS",
    "Run this round: tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 (gates1.txt). project.html changed in this delta but is outside slice b.")
row("FC2b-cmd-run_graders", "gate", "grader/ (unit gate, outside slice; grader/test_project.py changed in this delta)", "PASS",
    "Run this round: tools/run_graders.py --unit FC2 --seeds 0-49 -> 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.2 s)' and 0.3 s on a second run, exit 0 (graders_labs.txt, gates2 re-run).")
row("FC2b-cmd-run_labs", "gate", "tests/labs/FC2 (unit, and L04, L05, L06 separately)", "PASS",
    "Run this round: tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; --page L04, L05, L06 each 'PASS (1/1)', exit 0 (graders_labs.txt).")
row("FC2b-cmd-page_smoke", "gate", "L04.html, L05.html, L06.html (each run alone)", "PASS",
    "Run this round, one page per invocation: tools/page_smoke.py --unit FC2 --pages L04 (then L05, then L06) -> 'page_smoke modules/FC/FC2/L0n.html: PASS' and 'page_smoke FC2: PASS', exit 0 each (gates2.txt).")
row("FC2b-cmd-twins-isolated", "gate", "tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py", "PASS",
    "Run this round: .venv/bin/python -I -W error on each twin: exit 0, stderr 0 bytes each; stdout equals the page's expected block line for line (ledgers/FC2/scripts/FC2-b-r7/twin_match_r7.py prints 'ALL True'; outputs L04.out, L05.out, L06.out).")
row("FC2b-cmd-ruff", "gate", "tests/labs/FC2 twins", "PASS",
    "Run this round: .venv/bin/ruff check tests/labs/FC2/ -> 'All checks passed!'; .venv/bin/ruff format --check tests/labs/FC2/ -> '11 files already formatted' (gates2.txt).")
row("FC2b-cmd-mypy", "gate", "repository mypy configuration", "PASS",
    "Run this round: .venv/bin/mypy --no-incremental -> 'Success: no issues found in 385 source files', exit 0 (gates2.txt).")
row("FC2b-cmd-pytest", "gate", "tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_run_labs.py", "PASS",
    "Run this round: pytest -k FC2 tests/test_labs.py -> 11 passed (11 dots), exit 0; pytest tests/test_page_checks.py tests/test_run_labs.py -> 47 passed (47 dots), exit 0 (pytest_r7.txt).")
row("FC2b-cmd-verify_refs", "gate", "references/references.json; L04-L06 carry no data-cite", "PASS",
    "Run this round: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (gates2.txt). Live run not performed (network; no L04-L06 page cites a key).")

# ---- labs
row("FC2b-lab-L04-twin", "lab", "L04.html:123-244; tests/labs/FC2/lab-FC2-L04-1.py", "PASS",
    "Re-run this round (twin_match_r7.py): page code block equals twin text (equal after stripping the surrounding newlines); expected block L04.html:220-242 equals twin stdout (23 lines). Outputs re-derived by hand: call payoff 25 and profit 17 at spot 125 (premium 800 cents); break-evens 108 (call) and 93 (put, premium 700 cents); call hold values 10(9/10)^(4-t) = 6.56, 7.29, 8.10, 9.00, 10.00; hindsight best dates t=1 (18.00) and t=3 (14.58). Changed line 243 re-verified (see FC2b-delta-L04-interpretation-243).")
row("FC2b-lab-L06-twin", "lab", "L06.html:165-318; tests/labs/FC2/lab-FC2-L06-1.py", "PASS",
    "Re-run this round (twin_match_r7.py): page code equals twin; expected block L06.html:294-316 equals twin stdout (23 lines). Hand re-derivation of L06.out: one-period q=3/4, shares 1/2, bond -20, V0=30=3000 cents; two-period uu=225, ud=75, dd=25, V0=45=4500 cents; holdings 3/4 and -30; after up 5/6 and -50; four path checks True. L06.html:55 is the only changed line in L06 and is outside this range.")
row("FC2b-lab-L04-hypothesis", "lab", "L04.html:125 vs expected block L04.html:220-242", "PASS",
    C + "L04.html line 125 and lines 220-242 (not in the delta hunk list 84, 99, 120, 243, 248, 250, 317, 421). Re-checked: the hypothesis sentence matches the printed values in L04.out.")
row("FC2b-lab-L06-hypothesis", "lab", "L06.html:167 vs expected block L06.html:294-316", "PASS",
    C + "L06.html line 167 and 294-316 are outside the only L06 delta hunk (line 55). Output re-run this round (L06.out) shows V0=30=3000 cents, V0=45=4500 cents and the True checks at the printed lines.")
row("FC2b-lab-L06-docstring", "lab", "tests/labs/FC2/lab-FC2-L06-1.py:1-12 (shown on L06.html:170-178); printed lines L06.html:297-309", "PASS",
    "Twin docstring read in full (lines 1-12, unchanged since e896b7a4). Claims checked against L06.out: stock prices, payoffs and values after one move in currency units; time-0 values in integer cents (3000, 3000, 4500, 4500); parameters spot 100, strike 100, up 3/2, down 1/2, gross return 5/4; payoff max(S-K,0); no random input. All match.")

# ---- math
row("FC2b-math-L04-s1-s2", "math", "L04.html:57-112 (A1-A5, Def 1.1, Lemma 1.2, Def 2.1, Prop 2.2, Prop 2.3, Remark 2.4)", "PASS",
    "Subject changed (lines 84 and 99), so re-verified from scratch this round: lines 57-112 read in full. Def 1.1 payoffs and profit convention; Lemma 1.2 proof (both cases) correct; Remark 1.3 (line 84) claims only what Lemma 1.2 gives; Def 2.1 h(s) correct; Prop 2.2 statement V_A(t) >= h(S_t) and the new proof at line 99: initial value V_A(t)-h(S_t) < 0 with payoff zero in every state, which is excluded by A3 at L04.html:62 (cost <= 0 and payoff >= 0 implies cost 0). Prop 2.3 proof and Remark 2.4 (line 111) unchanged and consistent with it.")
row("FC2b-math-L04-example-2.5", "math", "L04.html:115-121 (Example 2.5, Remark 2.6)", "PASS",
    "Subject changed (line 120). Re-verified: path 100,120,90,80,110; call intrinsic 0,20,0,0,10; 10(9/10)^4 = 6.561 -> 6.56; 20*9/10 = 18; put intrinsic 0,0,10,20,0; 20(9/10)^3 = 14.58; r = ln(10/9) = 0.10536. Remark 2.6 new wording (line 120) is consistent: best dates known after the path; sale value at date 1 at least 20 by Prop 2.2.")
row("FC2b-math-L04-problems", "math", "L04.html:281-377 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    "Subject changed (line 317, P2 solution). Re-verified every problem: M1 (12, 8, 54); M2 (77; 20, 17); M3 (0,20,0,0,10; dates 1 and 4); P1 monotone; P2 new solution (initial value V(t)-(K-S_t)^+ < 0, payoff zero, A3 excludes); P3 affine-pieces argument correct; E1 values 0,20,0,0,10 vs 6.56,7.29,8.10,9.00,10.00 (exercise better only at t=1); E2 (hold 0.00; put 6.56; put best date 3 at 14.58; call best date 1 at 18.00); E3 (8.10 vs 0); R1 S_tau = 100 + 20000/729 = 127.43484; R2 monotone; R3 path 100,90,95,110,150: exercise best 7.29 vs hold 32.805.")
row("FC2b-math-L04-s1-s2-theorem-grades", "math", "L04.html claim grades (data-grade attributes, L04)", "PASS",
    "Subject changed only in prose at lines 84, 99, 120, 248, 250, 317, 421; claim blocks Lemma 1.2, Prop 2.2, Prop 2.3 keep data-grade=T and their proofs are on the page. Re-checked this round.")
row("FC2b-math-L05-thm1.2", "math", "L05.html:62-68 (Theorem 1.2, proof)", "PASS", C + "L05.html lines 62-68 (no delta hunk). Re-checked from the page text as carried.")
row("FC2b-math-L05-remark1.3-hypotheses", "math", "L05.html:70-72 (Remark 1.3)", "PASS", C + "L05.html lines 70-72 (no delta hunk).")
row("FC2b-math-L05-thm2.2", "math", "L05.html:83-103 (Theorem 2.2 (a)-(d), proof, Remark 2.3)", "PASS", C + "L05.html lines 83-103 (no delta hunk). The (N) uses at lines 95, 97, 102 read this round and consistent with the definition at L05.html:76.")
row("FC2b-math-L05-thm3.2-cor3.4", "math", "L05.html:109-129 (Def 3.1, Theorem 3.2 cases (i)-(iv), Remark 3.3); L05.html:289-295 (Corollary 3.4)", "PASS", C + "L05.html lines 109-129 and 289-295 (delta hunk at 107 is outside both ranges).")
row("FC2b-math-L05-thm4.1-remark4.2", "math", "L05.html:299-311 (Theorem 4.1 and proof, Remark 4.2)", "PASS", C + "L05.html lines 299-311 (no delta hunk). Re-read this round: the proof uses V_E(t) >= S_t - K (intrinsic bound) and the lab check of calls below intrinsic value at L05.html:286 targets that bound.")
row("FC2b-math-L05-problems", "math", "L05.html:348-436 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS", C + "L05.html lines 348-436 (no delta hunk). The R3 solution at line 441, which lies just after this range, was re-verified separately (FC2b-delta-L05-R3).")
row("FC2b-math-L05-why-it-matters-rate", "math", "L05.html:51 (why-it-matters)", "PASS",
    "Subject changed. Re-verified: the sentence now names 'a non-negative spot at expiry and a non-negative rate' in place of (N). That is the content of (N) (L05.html:76: spot at expiry non-negative) and of Theorem 4.1's hypothesis r >= 0. Four bounds (Theorem 2.2) and convexity (Def 3.1) references match. No (N) symbol before its definition.")
row("FC2b-math-L06-thm1.4", "math", "L06.html:76-95 (Def 1.3, Theorem 1.4 (a)-(c), proof; Ex 1.5, Ex 1.6)", "PASS", C + "L06.html lines 76-95 (the only L06 delta hunk is line 55).")
row("FC2b-math-L06-thm2.2-thm3.3", "math", "L06.html:116-158 (Theorem 2.2; Definitions 3.1-3.2; Theorem 3.3 and closed-form induction; Example 3.4)", "PASS", C + "L06.html lines 116-158 (no delta hunk).")
row("FC2b-math-L06-examples", "math", "L06.html:93-99 (Ex 1.5, 1.6), 155-158 (Ex 3.4)", "PASS", C + "L06.html lines 93-99 and 155-158 (no delta hunk).")
row("FC2b-math-L06-remarks-misconceptions", "math", "L06.html:101-105 (Remark 1.7), 114 (Remark on q), 327-336 (misconceptions)", "PASS", C + "L06.html lines 101-105, 114 and 327-336 (no delta hunk).")
row("FC2b-plan-L06-A2", "plan", "L06.html:55 (A2) vs plans/FC2-build-plan.md section 5.2 A2 (plan lines 287-288)", "PASS",
    "Subject changed (line 55: 'lending and borrowing at the riskless return R_f of Definition 1.1, without limit'). Plan A2 (lines 287-288): unlimited borrowing and lending at the riskless rate, except where a lesson adds a cost explicitly; L06 adds no cost. R_f is the plan's symbol. plans/FC2-build-plan.md unchanged in this delta (git diff stat empty).")
row("FC2b-plan-L04-no-L05-result", "plan", "L04.html:51, 111, 120, 243, 248, 258, 262 vs plan lines 105 and 431-432", "PASS",
    "Subject changed at 120, 243, 248, 250; re-verified this round. Plan line 105: L04 defines the concept and gives the payoff argument for no income; plan 431-432: the early-exercise-never-optimal result is proved in L05 and not stated in L04. L04 states only Prop 2.2 (exercise at once never better than selling, a consequence of the bound) and Prop 2.3, and explicitly leaves holding open (line 258/262). Judgement as in round 6; no L04 text states the L05 theorem. The plan is unchanged.")
row("FC2b-num-L04", "numbers", "L04.html prose numbers (lines 51, 73, 116, 120, 125, 243, 258-266, 335-377, 389-390)", "PASS",
    "Changed numbers re-derived: 120 (20 USD intrinsic, 18 at t=0), 243 (25.00, 17.00, 108.00, 93.00, 8.00 premium, 1000(9/10)^4 = 656.1 cents = 6.56, best dates 1 and 3), 317 and 421 (10(9/10)^4 = 6.561; 25 - 8 = 17). All other numbers unchanged since e896b7a4 and match the L04.out printed values.")
row("FC2b-num-L04-why-locator", "numbers", "L04.html:51, 116, 360, 374 (locators for derived numbers)", "PASS", C + "L04.html lines 51, 116, 360 and 374 (no delta hunk).")
row("FC2b-num-L05", "numbers", "L05.html prose numbers (lines 51, 286, 315, 352, 359, 366, 402-416, 434, 480-531)", "PASS",
    "Changed numbers re-derived: 286 (synthetic calls 30,20,10,1,0 USD and puts 2,1,0,0,8 USD match L05.out; -300 cents at 100 USD; 40 pairs; three violated triples), 511 quiz arithmetic (20-2*10+1 = 1; 8-100+0.97*105 = 9.85; 100e^-0.1-50 = 40.48). Other numbers unchanged since e896b7a4.")
row("FC2b-num-L06", "numbers", "L06.html prose numbers (lines 94, 99, 157, 319, 332, 335, 342-388, 441-476)", "PASS", C + "L06.html numbers at the listed lines (the only changed line, 55, has no number).")
row("FC2b-struct-L04", "structure", "L04.html (BUILDER_RULES 4.2 order and counts)", "PASS",
    "Re-checked this round (struct_r7.py): tag counts, id list and class counts of L04.html identical between e896b7a4 and aa659725; the only diff opcodes are single-line 'replace' at lines 84, 99, 120, 243, 248, 250, 317, 421 (text only). Quiz still 9 items (grep count).")
row("FC2b-struct-L05", "structure", "L05.html (BUILDER_RULES 4.2 order and counts)", "PASS",
    "struct_r7.py: tag, id and class counts identical; single-line text replacements at 51, 107, 286, 325, 441, 511. Quiz still 9 items.")
row("FC2b-struct-L06", "structure", "L06.html (BUILDER_RULES 4.2 order and counts)", "PASS",
    "struct_r7.py: tag, id and class counts identical; single-line text replacement at 55 only. Quiz still 10 items.")
row("FC2b-lab-L05-twin", "lab", "L05.html:131-287; tests/labs/FC2/lab-FC2-L05-1.py", "PASS",
    "Re-run this round: page code equals twin; expected block equals twin stdout (21 lines); run under -I -W error exit 0 with 0 bytes stderr. Changed line 286 re-verified (FC2b-lab-L05-named-errors).")
row("FC2b-lab-L05-hypothesis", "lab", "L05.html:133 vs expected block L05.html:265-285", "PASS", C + "L05.html lines 133 and 265-285 (no delta hunk).")
row("FC2b-lab-L05-D-claim", "lab", "tests/labs/FC2/lab-FC2-L05-1.py lines 5-9 (docstring) and L05.html:138-142", "PASS",
    C + "twin unchanged. Docstring claims re-checked by hand this round: D = 9/10 used only (DISCOUNT constant); at D = 1/100 the call at 80 USD is 10120 cents > S = 10000 (bound violated) and put 200 > DK = 80, as stated; convexity holds for each D because each call is a sum of convex functions of K. The lab tests no other D (grep shows only DISCOUNT = Fraction(9, 10)).")
row("FC2b-lab-L05-named-errors", "lab", "L05.html:286; L05.html:281-284 printed triples", "PASS",
    "Subject changed at line 286 (only the word 'only' removed from two sentences). Re-verified against L05.out: synthetic calls 30.00, 20.00, 10.00, 1.00, 0.00 USD; puts 2.00, 1.00, 0.00, 0.00, 8.00 USD; parity cost 0 on the synthetic set; planted parity error changes only the put at 100 USD (planted_puts, lab line 112) so cost is -300 at 100 USD and the payoff check is silent (0 of 40); planted convexity error moves call and put at 90 USD by 500 cents, parity holds, and three triples are violated (printed lines 281-284).")
row("FC2b-misconception-L05-1", "misconception", "L05.html:323-326 (misconception 1, evidence sentence); lab zero residuals L05.html:286; twin lab-FC2-L05-1", "PASS",
    "Subject changed at line 325 ('computes its puts from parity'). Re-verified: the twin sets P = C - S + DK (puts follow from parity); planted put error at 100 USD gives parity cost -300 cents (L05.out); Theorem 1.2 holds for every strike K > 0 (line 325's first sentence).")
row("FC2b-misconception-L04-L06-other", "misconception", "L04.html:256-271 (re-verified), L05.html:327-337, L06.html:327-335", "PASS",
    C + "L04.html 256-271, L05.html 327-337 and L06.html 327-335 (no delta hunk in these ranges). L04 misconception 1 ('Proposition 2.3 proves only V_A(0) >= V_E(0)') and misconception 2 ('exercising at once is never better than selling') re-read this round and consistent with lines 99 and 111.")
row("FC2b-quiz-L04-L06", "quiz", "L04.html:396-466 (9 items), L05.html:464-534 (9 items), L06.html:412-481 (10 items)", "PASS",
    "Counts re-checked by grep: 9, 9, 10. Subject changed at L04 line 421 (q3 explanation) and L05 line 511 (q7 prompt); both re-read in full this round with all their options and explanations: L04 q1-q9 answers (25, 17, V_A(0) >= V_E(0), 20, only at expiry, 77, 6.56, date 1, S - K) correct; L05 q1-q9 answers (C - P = S - DK, 9.85, sell call and buy share, 12, convexity weight (K3-K2)/(K3-K1), 1, the same price at date 0, (N), 40.48) correct. L06 items carried (L06 delta line 55 is outside the quiz).")
row("FC2b-misconception-L05-R3", "misconception", "L05.html:441 (R3 solution)", "PASS", "Subject changed (see FC2b-delta-L05-R3).")
row("FC2b-banned-process", "process", "L04-L06 visible prose and twin docstrings", "PASS",
    "Scan of all 32 added lines this round (ledgers/FC2/scripts/FC2-b-r7/added_lines.txt) for process words (verif, round, fixed, builder, delta, previous, earlier, reviewer, we, I, revised, corrected, changed): none in learner text; the one 'round' match is 'rounded to the nearest cent' (display rounding).")
row("FC2b-notation", "notation", "L04-L06 math vs notation/notation.json", "PASS",
    "R_f matches notation.json (gross riskless return for the period, reciprocal of a sure payoff of 1); L06.html:59 Def 1.1 uses R_f = 1 + r_1 and reserves r for A4 (consistent). (N) is a hypothesis label, not a notation.json symbol, and it is first introduced at L05.html:76. No symbol is reused with a new meaning in the changed hunks.")
row("FC2b-dag-links", "dag", "L04-L06 concept links and definitions", "PASS",
    "check_dag.py FC2 PASS (fresh). The changed hunks add no links; L06 line 55 uses R_f with a numbered pointer to Definition 1.1 (same lesson). No new concept used outside its prerequisite closure.")
row("FC2b-define-before-use-self-financing", "define-before-use", "L06.html:161-162 (Definition 3.5), first use L06.html:167", "PASS", C + "L06.html lines 161-162 and 167 (no delta hunk).")
row("FC2b-define-before-use-N", "define-before-use", "L05.html:51 (first use, why-it-matters) vs L05.html:76 (definition of (N))", "PASS",
    "Round 6 FAIL fixed. grep of '(N)' in L05.html now returns first occurrence at line 76 (the definition: 'The bounds below use one more hypothesis, (N): the spot price at expiry is non-negative.'). Line 51 now reads 'a non-negative spot at expiry and a non-negative rate' with no (N) symbol. No (N) use in L04 or L06.")
row("FC2b-define-before-use-R_f-L06-A2", "define-before-use", "L06.html:55 (A2 names R_f) vs L06.html:59 (Definition 1.1)", "PASS",
    "R_f is named in A2 before Definition 1.1 at L06.html:59, but with a numbered pointer ('the riskless return R_f of Definition 1.1'), the same forward-pointer pattern the paragraph already uses for A5 and A6. Accepted as a reference to a definition, not a use of an undefined term. Note only.")
row("FC2b-scope-words", "scope", "L04-L06 'every', 'all', 'never', 'any', 'always', 'only', 'exactly', 'same' in the changed hunks and in the added lines", "PASS",
    "Scan of added lines (added_lines.txt): 'only' in 4 places, each either a computed claim (only the t=0 row is a value at date 0; only the put price changes in the planted parity error; only the call and put at 90 USD change in the convexity error) or a stated assumption (A5, 'paid at the end of the period only'). 'every' and 'same' occur in the claims re-verified above. The round-6 scope 'only' removals (L04 84, 120, 248, 250; L05 107, 286, 441) are checked: the lesson still states the same claim without the scope word.")
row("FC2b-simulated-labels", "simulated", "L04 Example 2.5 (L04.html:115), L04 lab (L04.html:124-128), L05 lab (L05.html:132-136), L06 lab (L06 165-318)", "PASS",
    C + "L04.html:115 and 124-128, L05.html:132-136, L06.html:165-318 (no delta hunk). Changed line 243 keeps the SIMULATED label ('the single SIMULATED path') and does not claim market data.")
row("FC2b-figures", "figures", "L04-L06 (no figures, data-files or data-cite)", "PASS",
    "struct_r7.py: class and tag counts identical between pins (no figure element added); no data-files or data-cite attribute introduced by the delta.")
row("FC2b-lab-rng-network", "lab", "tests/labs/FC2 L04/L05/L06 twins (read in full)", "PASS",
    "Twins unchanged in this delta (git diff stat empty for tests/labs/FC2). grep this round: imports are __future__, fractions, math, itertools only; no random, urllib, requests, socket, http or open() call. Docstrings say 'draws no random numbers' / 'no data file is read' and that holds.")
row("FC2b-hours", "hours", "L04-L06 data-hours; index.html:29 and the hub hour cards", "PASS",
    "data-hours: L01 6, L02 8, L03 9, L04 7, L05 8, L06 8, L07 8, L08 6 = 60 lesson hours, matching the hub 'data-hours-lessons=60' and the 30 h project (90 total). L04 card 'L04 · 7 h', L05 '8 h', L06 '8 h' at index.html lines 138-140. Arithmetic consistent; hub unchanged in this delta.")

# ---- cards
row("FC2b-cards-hypotheses", "cards", "cards.json FC2-c059 (L04 hypotheses) and the other slice cards", "PASS",
    C + "card objects FC2-c059 byte-identical; its cited lines (Prop 2.3 at L04.html:104-105, Remark 2.4 at line 111) unchanged. Card says 'Under A2, A3 and A5' matching the proposition.")
row("FC2b-cards-delta-round1", "cards", "cards.json delta e896b7a4..aa659725 for L04-L06", "PASS",
    "Re-run this round (cards_delta_r7.py): card objects in the slice unchanged; the only added slice card is FC2-c187 (L04, A1 wording identical to L04.html:60); no card removed in the delta (c176 absent since round 6); changed objects c006, c144, c178 and added c186 are L01/L03, outside slice b (for their owners). Totals 172 -> 174 cards.")
row("FC2b-cards-coverage", "cards", "cards.json: slice cards with lesson L04, L05, L06", "PASS",
    "Re-counted: L04 19 (c051-c062, c135, c142, c143, c158, c159, c179, c187), L05 25, L06 29 = 73 slice cards. Every L04-L06 card id is a card of its lesson and no card references a missing lesson.")
row("FC2b-cards-duplicates", "cards", "cards.json whole deck (174 cards), pairwise scan", "PASS",
    "dup_r7.py scan: no duplicate ids; no pair with identical fronts (highest front ratio 0.98: FC2-c139 (L02) vs FC2-c187 (L04), 'What does Assumption A1 (no income) of Lesson N say?' with different lesson-specific wording: asset vs underlying). Same question form in two lessons is not a duplicate fact.")
row("FC2b-cards-near-duplicate", "cards", "near-duplicate pairs in the slice", "PASS",
    "Slice pairs with front ratio >= 0.6: c160/c162 (lower bounds on call vs put, different facts), c066/c161 (0 <= C <= S vs 0 <= P <= DK), c057/c135 (put vs call on the path), c161/c162, c069/c070 (convexity vs monotone), c187 vs L02 A1 (above). All distinct facts.")
row("FC2b-cards-grade-ruling9", "cards", "cards.json grades for L04-L06", "PASS",
    "Re-checked: proved-on-page claims are T (Lemma 1.2 c052, Prop 2.2 c054, Prop 2.3 c055, Thm 4.1 c071, Thm 2.2 c066 etc.); claims read off a SIMULATED lab are C with the lab named (c058, c061, c072-c074, c079, c095, c148, c155, c171); c187 is a definition with no empirical claim and needs no grade (BUILDER_RULES 7).")
row("FC2b-cards-L04-grades", "cards", "cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c179 (c176 removed)", "PASS",
    "Grades re-read: T on c052, c054, c055, c056, c057, c059, c060, c062, c135, c179; C on c058, c061 with basis 'Lab 1, Part 1 (exact)'; ungraded definitions c051, c053, c142, c143, c158, c159. Content of c179 fails on wording (see FC2b-cards-c179-scope); its grade is right.")
row("FC2b-cards-L04-rest", "cards", "L04 cards without grade (c051, c053, c142, c143, c158, c159, c187)", "PASS",
    "Ungraded cards are definitional or assumption-statement cards with no empirical claim; each back is checkable against the lesson text (A1 L04.html:60, A2 L04.html:61, A3 L04.html:62, A4 L04.html:63, A5 L04.html:64).")
row("FC2b-cards-L05-C-grades", "cards", "cards.json L05 C-graded cards c072, c073, c074, c079, c155, c171", "PASS",
    "All six are C with a basis naming Lab 1 (SIMULATED price set). Their backs match L05.out: parity cost 0 at all strikes; -300 cents at 100 USD; parity cost zero for the 90 USD raise; three violated triples; no bound or convexity violation on the synthetic set; none of the 40 pairs has nonzero payoff.")
row("FC2b-cards-L05-c064", "cards", "cards.json FC2-c064 (Theorem 1.2 card)", "PASS",
    "c064 back 'every strike, not only the at-the-money one' matches Theorem 1.2 (every K > 0) and Remark 1.3 (does not say put equals call). Consistent with the revised misconception at L05.html:325.")
row("FC2b-cards-L05-rest", "cards", "cards.json L05 cards c063, c065-c071, c075, c076, c078, c080, c132, c153, c160-c162, c180", "PASS",
    "Re-read this round against the changed L05 lines: c068 back 'The word refers to strikes only' restates the stipulation at L05.html:107 ('In this lesson the word convexity refers to convexity in strike'), which fixes the meaning for the lesson, so no extra scope is asserted (PASS). c070 'gives no size for the fall' matches the R3 solution at line 441. c071 matches Theorem 4.1 (and (N), r >= 0) and Remark 4.2. c071 consistent with quiz q7 (L05.html:511). c075 Problem E1 values checked (0, 100, 800 cents). c076 arithmetic: 100e^-0.1 - 50 = 40.48.")
row("FC2b-cards-L06-grades", "cards", "cards.json FC2-c081..c098, c136, c137, c148-c150, c163, c166, c174, c181", "PASS",
    "Re-read; c081 'R_f = 1 + r_1 (Definition 1.1), unsubscripted r not used' matches L06.html:59. c086, c091, c094, c097, c098, c136, c137 arithmetic re-derived: Example 1.5 shares 1/2, bond -20, cost 30; Example 3.4 V(1,1)=75, V0=45; c097 cash 35-50+20=5 lent to 25/4 with the -25 repayment netted in the position. c098 expected final 156.25 discounts to 100; payoff 56.25 discounts to 36 (vs correct 45).")
row("FC2b-cards-L06-rest", "cards", "L06 cards without grade (c082, c083, c088, c090, c092, c166, c174, c184, c185)", "PASS",
    "c082 (A6: 0 < d < R_f < u) matches L06.html Definition 1.2 (line 64); c184, c185 (carried since round 6) match Definitions 1.1 and 1.2; definitional cards with no empirical claim.")
row("FC2b-cards-key-mirror", "cards", "key-results tables L04.html:383-393, L05.html:450-460, L06.html:401-410 vs cards", "PASS",
    C + "key-results table lines in L04.html 383-393, L05.html 450-460 and L06.html 401-410 (no delta hunk). Each row restates a card's result (checked against the slice cards).")
row("FC2b-cards-c176-added", "cards", "cards.json FC2-c176 (removed in round 6); FC2-c184, c185 (added in round 6); FC2-c187 (added this delta)", "PASS",
    "c176 absent from cards.json and from any page or tool (grep). c184 and c185 unchanged this delta and consistent with Definitions 1.1 and 1.2. c187 added this delta: see FC2b-cards-c187.")
row("FC2b-cards-c187", "cards", "cards.json FC2-c187 (L04, added this delta)", "PASS",
    "Front 'What does Assumption A1 (no income) of Lesson 4 say?' back 'The underlying pays no dividend, coupon or storage cost over the life of the contract (A1 of Lesson 4).' matches L04.html:60 ('A1 (no income). The underlying pays no dividend, coupon or storage cost over the life of the contract.') verbatim; one fact; no grade needed (definitional). Lesson number and assumption number appear in the lesson.")
row("FC2b-cards-c179-scope", "cards", "cards.json FC2-c179 (L04) back vs L04.html:84 (Remark 1.3)", "FAIL",
    "Card FC2-c179 back reads 'The identity concerns payoffs only and says nothing about what the two options cost.' The current Remark 1.3 at L04.html:84 reads 'The identity concerns payoffs. It does not say what the two options cost.' This delta removed the word 'only' from Remark 1.3 (the earlier text was 'concerns payoffs only'); the card was not updated and now asserts a scope word the lesson no longer states (rule 10: cards must agree with the current lesson text).",
    "Change the FC2-c179 back text in cards.json to 'The identity concerns payoffs and says nothing about what the two options cost.' (drop 'only'); if the card is generated from a source file, change the source and regenerate.")

# ---- delta rows (every changed hunk, verified this round)
row("FC2b-delta-L04-interpretation-243", "delta", "L04.html:243 (Part 1/Part 2 interpretation)", "PASS",
    "Changed: 'subtracted only in the profit column' -> 'subtracted in the profit column'. Re-verified: profit = payoff - premium (25 - 8 = 17 at 125 USD, L04.out); payoff column has no premium term; all printed values (6.56, 7.29, 8.10, 9.00, 10.00; 18.00; 14.58; 108.00; 93.00) match the expected block.")
row("FC2b-delta-L04-remark-1.3", "delta", "L04.html:84 (Remark 1.3)", "PASS",
    "Changed: 'concerns payoffs only' -> 'concerns payoffs'. Statement is Lemma 1.2 plus the cost remark; the card back FC2-c179 retains 'only' and is the one FAIL row (FC2b-cards-c179-scope).")
row("FC2b-delta-L04-prop2.2-proof", "delta", "L04.html:99 (Proof of Proposition 2.2)", "PASS",
    "Changed proof: initial value V_A(t) - h(S_t) < 0 and payoff zero in every state, excluded by A3 (L04.html:62: cost at most zero and payoff non-negative imply cost zero). Correct under A2 (free buying and exercising, L04.html:61) and A3. The old text claimed zero initial value and a strictly positive payoff at t; the new text is consistent with A3 as written.")
row("FC2b-delta-L04-remark-2.6", "delta", "L04.html:120 (Remark 2.6)", "PASS",
    "Changed: 'are known only after the path is observed' -> 'are known after the path is observed'. Consistent with Example 2.5 (hindsight); 'at least 20 USD by Proposition 2.2' holds (intrinsic value at date 1 is 20).")
row("FC2b-delta-L04-canon-breaks", "delta", "L04.html:248, 250 (Section 3 Where the canon breaks)", "PASS",
    "Changed: 'gives only a lower bound' -> 'gives a lower bound' (Prop 2.2) and 'the lesson shows only that' -> 'the lesson shows that' (Remark 2.4). Consistent with Prop 2.3 (V_A(0) >= V_E(0)) and with the remark's limit (no equality, no strictness). No new claim.")
row("FC2b-delta-L04-P2-317", "delta", "L04.html:317 (P2 solution)", "PASS", "Changed proof text in P2 solution, same argument as line 99 with h(s)=(K-s)^+. Re-verified (see FC2b-math-L04-problems).")
row("FC2b-delta-L04-q3-421", "delta", "L04.html:421 (quiz q3 explanation)", "PASS",
    "Changed: 'gives only the inequality (Remark 2.4)' -> 'gives the inequality (Remark 2.4)'. The correct option V_A(0) >= V_E(0) and the explanation are consistent with Prop 2.3 and Remark 2.4.")
row("FC2b-delta-L05-why-it-matters-51", "delta", "L05.html:51 (why-it-matters)", "PASS", "Changed: '(N)' replaced by 'a non-negative spot at expiry'; fixes the define-before-use FAIL of round 6 (see FC2b-define-before-use-N). Content re-checked against Theorem 4.1 hypotheses (A1-A5, r >= 0, and (N) = non-negative spot).")
row("FC2b-delta-L05-convexity-107", "delta", "L05.html:107 (Section 3 intro)", "PASS", "Changed: 'refers to convexity in strike only' -> 'refers to convexity in strike'. The definitional sentence still fixes the lesson's meaning of 'convexity'. Card FC2-c068 consistent (see FC2b-cards-L05-rest).")
row("FC2b-delta-L05-interpretation-286", "delta", "L05.html:286 (Lab 1 interpretation)", "PASS", "Changed: 'it confirms only the payoff identity over 40 pairs' -> 'it confirms the payoff identity over 40 pairs'. The phrase 'the planted parity error changes only a put price' is unchanged and matches the twin (planted_puts changes only the strike-100 put). Re-verified against L05.out (see FC2b-lab-L05-named-errors).")
row("FC2b-delta-L05-misconception-325", "delta", "L05.html:325 (misconception 1)", "PASS", "Changed: 'builds its puts from parity' -> 'computes its puts from parity'. Lab 1 computes P = C - S + DK (twin); the planted error at 100 USD still breaks the identity (-300 cents). Consistent with card FC2-c072 ('sets each put from parity').")
row("FC2b-delta-L05-R3-441", "delta", "L05.html:441 (R3 solution)", "PASS", "Changed: 'It shows only that the prices do not rise with strike' -> 'It shows that the prices do not rise with strike'. The portfolio (buy K1 call, sell K2 call) gives C(K1) >= C(K2) by A3: correct (if C(K1) < C(K2) the cost is negative with non-negative payoff, excluded by A3). The corollary gives no size of the fall. Consistent with card FC2-c070.")
row("FC2b-delta-L05-quiz-q7-511", "delta", "L05.html:511 (quiz q7 prompt)", "PASS", "Changed prompt: 'With no income on the underlying and r >= 0' -> 'Under A1 to A5, (N) and r >= 0'. Now names the hypotheses of Theorem 4.1; the correct option (same price at date 0, no value at date 0 from early exercise) is unchanged and correct.")
row("FC2b-delta-L06-A2-55", "delta", "L06.html:55 (A2)", "PASS", "Changed: 'at the riskless return below' -> 'at the riskless return R_f of Definition 1.1'. Pointer to the defining item; R_f = gross riskless return (notation.json, Definition 1.1). See FC2b-define-before-use-R_f-L06-A2.")

# ---- gate on the whole slice
verdict = "PASS" if all(r["status"] == "PASS" for r in R) else "FAIL"
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
frag = {
    "unit": "FC2",
    "slice": "b",
    "round": 7,
    "verifier": "Haiku independent verifier, FC2 slice b round 7 (did not build FC2)",
    "pin": "aa6597255304919b9c4e5e5ca07763ae3e13d45c",
    "base": "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a (round-6 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-FC2-b.round6.json). Delta e896b7a4..aa659725 read in full for the slice: L04.html lines 84, 99, 120, 243, 248, 250, 317, 421; L05.html lines 51, 107, 286, 325, 441, 511; L06.html line 55; cards.json FC2-c187 added (c006, c144, c178, c186 outside slice); tests/labs/FC2 unchanged.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS7-FC2-b",
    "scratch": "ledgers/FC2/scripts/FC2-b-r7/ (gates1.txt, gates2.txt, graders_labs.txt, pytest_r7.txt, twin_match_r7.py, struct_r7.py, cards_r7.py, cards_delta_r7.py, dup_r7.py, delta_pages.diff, delta_cards.diff, added_lines.txt, L04.out, L05.out, L06.out). Mutants: ledgers/FC2/mutants/ (empty; slice b has no project grader).",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: slice b = L04.html, L05.html, L06.html; twins tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py (unchanged in this delta); the 73 slice cards in course/modules/FC/FC2/cards.json (L04 19, L05 25, L06 29).",
        "Round-6 FAIL FC2b-define-before-use-N is fixed: (N) first occurs at L05.html:76 and the line-51 use was replaced with the hypothesis content.",
        "The only FAIL is FC2b-cards-c179-scope (low): card FC2-c179 keeps 'only' after the lesson text lost it in this delta.",
        "Judgement accepted and not failed: L04 Prop 2.2 proof now argues via a negative initial value; A3 as written in L04.html:62 excludes it. R_f named in L06 A2 before Definition 1.1 with a numbered pointer, accepted as a reference (not a use of an undefined term).",
        "Observation, not a row: Theorem 4.1 lists (N) as a hypothesis, but its proof (L05.html:303-306) does not invoke (N); a superset of hypotheses is not a failure under the rules.",
        "Observation, not a row: card FC2-c187 (L04) and FC2-c139 (L02) have near-identical fronts ('What does Assumption A1 (no income) of Lesson N say?') about different lesson-specific assumptions; not duplicates.",
        "Mutation testing: not applicable. Slice b has no project grader; per the rulings, lab twins are demonstrations. mutants is empty.",
        "Committed state note: ledgers/FC2/FC2-b.json as committed at the checkout pin was an older fragment (pin 0d2d0f3); it is overwritten here as the task specifies. Nothing committed.",
        "Not checked: a browser screenshot or visual review of L04-L06 (page_smoke geometry and console checks passed; no visual review); the live verify_refs run (network); the hub, L01-L03, L07-L08 and project pages except where unit gates cover them; card FC2-c186 (L01) and c006, c144, c178 (other slices); the full curriculum source for lesson hours (only the hub split and the page data-hours were compared).",
    ],
    "summary": f"FC2 slice b round 7 (pin aa659725, delta from e896b7a4): {len(R)} rows; {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. The FAIL is FC2b-cards-c179-scope (low): card FC2-c179 back keeps 'payoffs only' after L04 Remark 1.3 dropped 'only'. The round-6 FAIL (define-before-use (N) at L05.html:51) is fixed. All gates pass in this checkout: check_pages, check_dag, check_projects, run_graders (50/50), run_labs (11/11 and each page), page_smoke (each page alone), twins under python -I -W error with exact output match, ruff, mypy --no-incremental, pytest subsets, verify_refs --offline.",
}
out = "ledgers/FC2/FC2-b.json"
json.dump(frag, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", out, len(R), "rows", counts, verdict)
