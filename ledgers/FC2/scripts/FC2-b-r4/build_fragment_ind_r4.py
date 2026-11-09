"""Round-4 independent verifier: writes the FC2 slice-b fragment (ledgers/FC2/FC2-b.json) from the checks run this round.

Every row cites a script or command in ledgers/FC2/scripts/FC2-b-r4/ or a locator in the pinned tree.
Run from the checkout root: .venv/bin/python -I ledgers/FC2/scripts/FC2-b-r4/build_fragment_ind_r4.py
"""
import json
from pathlib import Path

S = "ledgers/FC2/scripts/FC2-b-r4/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates (run this round by gates_ind_r4.sh; exit codes in gate_exit_codes.txt)
row("FC2b-cmd-check_pages", "gate", "index, L01-L08, cards.json (unit gate)", "PASS",
    f"tools/check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 ({S}check_pages.txt).")
row("FC2b-cmd-check_dag", "gate", "L04-L06 links and dfn", "PASS",
    f"tools/check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 ({S}check_dag.txt).")
row("FC2b-cmd-check_projects", "gate", "project.html (unit gate, outside slice)", "PASS",
    f"tools/check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 ({S}check_projects.txt).")
row("FC2b-cmd-run_graders", "gate", "grader/ (unit gate, outside slice)", "PASS",
    f"tools/run_graders.py --unit FC2 --seeds 0-49 -> 'run_graders FC2: PASS (reference 50/50 seeds)', exit 0 ({S}run_graders.txt).")
row("FC2b-cmd-run_labs", "gate", "tests/labs/FC2 (all 11 twins; L04, L05, L06 alone)", "PASS",
    f"tools/run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)'; --page L04, L05, L06 each 'PASS (1/1)', exit 0 ({S}run_labs_unit.txt, run_labs_L04.txt, run_labs_L05.txt, run_labs_L06.txt).")
row("FC2b-cmd-page_smoke", "gate", "L04.html, L05.html, L06.html (run alone)", "PASS",
    f"tools/page_smoke.py --unit FC2 --pages L04 / L05 / L06 -> each 'page_smoke ...: PASS', lab timings 0.0 s, exit 0 ({S}page_smoke_L04.txt, page_smoke_L05.txt, page_smoke_L06.txt).")
row("FC2b-cmd-ruff", "gate", "tests/labs/FC2 twins", "PASS",
    f"ruff check tests/labs/FC2 -> 'All checks passed!' ({S}ruff_check.txt); ruff format --check -> '11 files already formatted' ({S}ruff_format.txt).")
row("FC2b-cmd-mypy", "gate", "repository mypy configuration", "PASS",
    f"mypy --no-incremental -> 'Success: no issues found in 385 source files', exit 0 ({S}mypy.txt).")
row("FC2b-cmd-pytest", "gate", "tests/test_labs.py -k FC2; tests/test_page_checks.py; tests/test_run_labs.py", "PASS",
    f"pytest tests/test_labs.py -k FC2 -q -> 11 passed, exit 0 ({S}pytest_fc2.txt); pytest tests/test_page_checks.py tests/test_run_labs.py -q -> 47 passed, exit 0 ({S}pytest_page_checks.txt).")
row("FC2b-cmd-verify_refs", "gate", "references/references.json; L04-L06 carry no data-cite", "PASS",
    f"tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.txt). grep for data-cite, data-locator, data-files in L04-L06 returns none. Live Crossref run not made (no key in slice; no network).")

# ---- labs and twins (twin_vs_page_ind_r4.py, twin_vs_page_ind_r4.out)
row("FC2b-lab-L04-twin", "2.5 lab", "L04.html:123-244; tests/labs/FC2/lab-FC2-L04-1.py", "PASS",
    f"{S}twin_vs_page_ind_r4.out: 'L04 page-code-equals-twin=True', 'twin-exit=0 stderr-empty=True' under python -I -W error; 'L04 expected==stdout ... True' (23 lines). Twin unchanged since the round-3 pin.")
row("FC2b-lab-L05-twin", "2.5 lab", "L05.html:131-287; tests/labs/FC2/lab-FC2-L05-1.py", "PASS",
    f"{S}twin_vs_page_ind_r4.out: 'L05 page-code-equals-twin=True', twin exit 0, stderr empty, 'L05 expected==stdout ... True' (21 lines). Twin unchanged since round-3 pin.")
row("FC2b-lab-L06-twin", "2.5 lab", "L06.html:165-315; tests/labs/FC2/lab-FC2-L06-1.py", "PASS",
    f"{S}twin_vs_page_ind_r4.out: 'L06 page-code-equals-twin=True', twin exit 0, stderr empty, 'L06 expected==stdout ... True' (23 lines), after the round-4 twin edit (lines 111-114 of the twin; L06.html:281-283 identical). Code equality holds; the docstring defect is row FC2b-lab-L06-docstring.")
row("FC2b-lab-L04-hypothesis", "2.5 lab", "L04.html:125 vs expected block L04.html:220-242", "PASS",
    f"{S}numbers_ind_r4.out (63 OK): call break-even 108, put break-even 93, call intrinsic 0,20,0,0,10, put 0,0,10,20,0, hold PV 6.561 -> 6.56, exercise at 1 PV 18, put date 3 PV 14.58; the hypothesis values match the printed block.")
row("FC2b-lab-L05-hypothesis", "2.5 lab", "L05.html:133 vs expected block L05.html:265-285", "PASS",
    f"{S}numbers_ind_r4.out: calls (3000,2000,1000,100,0) and puts (200,100,0,0,800) cents recomputed; parity cost zero; planted put -300 at 100 USD; planted convexity error violates exactly the triples (80,90,100), (80,90,110), (80,90,120) (same file, 'L05 planted convexity violated triples').")
row("FC2b-lab-L05-D-claim", "2.5 lab docstring", "tests/labs/FC2/lab-FC2-L05-1.py lines 5-9 (docstring) and L05.html:138-142", "PASS",
    f"{S}numbers_ind_r4.out: at D = 1/100 the call at 80 USD is 101.2 > spot 100 and the put at 80 USD is 2.0 > DK = 0.8, so the model-free checks fail; at D = 9/10 every check holds. The docstring's convexity claim (sum of two convex functions of K) is sound for any D.")
row("FC2b-lab-L06-hypothesis", "2.5 lab", "L06.html:167 vs expected block L06.html:293-315", "PASS",
    f"{S}twin_vs_page_ind_r4.out: expected block equals stdout. Printed: one-period True, four path checks True, self-financing True; V0 = 30 and 45 (L06.html:298, 305). Recomputed in {S}numbers_ind_r4.out.")
row("FC2b-lab-L05-named-errors", "2.5 lab interpretation", "L05.html:286; L05.html:281-284 printed triples", "PASS",
    f"Printed triples (L05.html:282-284) are the three the interpretation names (L05.html:286) and misconception 3 (L05.html:333); each has middle strike 9000 cents. Parity payoff check finds 0 of 40 pairs (L05.html:269, 274, 279).")
row("FC2b-lab-L06-docstring", "2.5 lab docstring vs printed output", "tests/labs/FC2/lab-FC2-L06-1.py:3-6 (shown on L06.html:170-173); printed lines L06.html:296, 302-304", "FAIL",
    f"The twin docstring says 'Prices are printed in integer cents' (lines 3-6). The output prints stock prices, payoffs and values after one move in currency units, not cents: 'payoff after an up move = 50' (L06.html:296), 'stock at expiry: uu=225 ud=75 dd=25' (L06.html:302), 'payoff at expiry: uu=125 ud=0 dd=0' (L06.html:303), 'value after an up move = 75' (L06.html:304). Only V0 is also printed in cents (L06.html:298, 305, 306). Found by the sentence-vs-output check, {S}misc_ind_r4.out and the twin docstring at lines 3-6.",
    "Edit the twin docstring (tests/labs/FC2/lab-FC2-L06-1.py lines 3-6) so it says only the replicating cost V0 is also printed in integer cents (half up); stock prices, payoffs and values are printed in currency units, and shares and bond positions as exact fractions. Then re-embed with `.venv/bin/python tools/embed_labs.py course/modules/FC/FC2/L06.html --refresh lab-FC2-L06-1` and rerun run_labs --page L06 and the twin check. The printed output does not change.")

# ---- math (L04 Lemma 1.2 ... L06 Theorem 3.3); numbers re-derived in numbers_ind_r4.py
row("FC2b-math-L04-s1-s2", "2.4 math", "L04.html:57-112 (A1-A5, Def 1.1, Lemma 1.2, Def 2.1, Prop 2.2, Prop 2.3, Remark 2.4)", "PASS",
    "Lemma 1.2 by cases (L04.html:80). Prop 2.2 proof (L04.html:99): position with zero initial value and payoff h - V_A(t) > 0 at t, excluded by A3. Prop 2.3 (L04.html:107): initial value V_A(0)-V_E(0) < 0 with non-negative payoff, excluded by A3; the American holder never exercises before tau, so its payoff at tau is h(S_tau). Remark 2.4 claim 'does not use A1 or A4' checked against the proof text.")
row("FC2b-math-L04-example-2.5", "2.4 math / 2.2 numbers", "L04.html:115-121 (Example 2.5, Remark 2.6)", "PASS",
    f"{S}numbers_ind_r4.out: intrinsic 0,20,0,0,10 (call) and 0,0,10,20,0 (put); PV 6.561 (hold), 18 (call at 1), 14.58 (put at 3); r = ln(10/9) = 0.10536 (A4). Remark 2.6 'at least 20 USD' is Prop 2.2 at t = 1.")
row("FC2b-math-L04-problems", "2.4 math / 2.2 numbers", "L04.html:281-377 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    f"{S}numbers_ind_r4.out: M1 payoff 12, profit 8, break-even 54; M2 break-even 77, profit 17; E1 exercise 20 vs hold 7.29 at 1; E2 put 6.561, 14.58, call 18; E3 8.10 vs 0; R1 threshold 100+20000/729 = 127.43484; R3 hold 32.805 > exercise 7.29. P3 chord proof re-derived (affine pieces of max(K-s,0)).")
row("FC2b-math-L05-thm1.2", "2.4 math", "L05.html:62-68 (Theorem 1.2, proof)", "PASS",
    "Portfolio X (long call, short put, short share, lend e^{-r tau}K): V0 = C - P - S + e^{-r tau}K; payoff (S-K)^+ - (K-S)^+ - S + K = 0 by Lemma 1.2 of L04 (L05.html:67). Both signs of V0 excluded by A3 (L05.html:67). A4 used for the return K of the loan, A1/A2 for the share return.")
row("FC2b-math-L05-remark1.3-hypotheses", "2.4 math", "L05.html:70-72", "PASS",
    "Remark 1.3 lists A1, A2, A3, A5 for the proof and A4 for the rate (L05.html:71); the proof (L05.html:67) uses exactly these. Consistent with card FC2-c064.")
row("FC2b-math-L05-thm2.2", "2.4 math", "L05.html:83-103 (Theorem 2.2 (a)-(d), proof, Remark 2.3)", "PASS",
    "Each part re-derived: (a) min(S,K) >= 0 under (N) gives C <= S, C >= 0 by A3; (b) (K-S)^+ >= 0 gives C >= S - DK; (c) min(S,K) >= 0 under (N) gives P <= DK; (d) (S-K)^+ >= 0 gives P >= DK - S (L05.html:95-98). Remark 2.3 lists (N) for (a), (c) only; checked.")
row("FC2b-math-L05-thm3.2-cor3.4", "2.4 math", "L05.html:109-129 (Def 3.1, Theorem 3.2 cases (i)-(iv), Remark 3.3); L05.html:289-295 (Corollary 3.4)", "PASS",
    f"Cases (i)-(iv) re-derived (L05.html:120-123); butterfly payoff >= 0 on a grid for four strike triples (numbers_ind_r4.out, 'Theorem 3.2 butterfly payoff'). Remark 3.3 lambda = 1/2 at equal spacing. Corollary 3.4 proof (L05.html:294) is valid; (N) is listed though not used (over-listing, not a gap).")
row("FC2b-math-L05-thm4.1-remark4.2", "2.4 math", "L05.html:299-311 (Theorem 4.1 and proof, Remark 4.2)", "PASS",
    "Re-derived: Prop 2.3 gives V_A(0) >= V_E(0); date-t portfolio (L05.html:305) gives V_E(t) >= S_t - e^{-r(tau-t)}K >= S_t - K when r >= 0; the American and European cash flows net to >= 0 (L05.html:305); A3 excludes V_E(0) - V_A(0) < 0 (L05.html:306). Remark 4.2 says the date-t equality is not proved; r < 0 breaks the step (L05.html:310, Problem R2).")
row("FC2b-math-L05-problems", "2.4 math / 2.2 numbers", "L05.html:348-436 (M1-M3, P1-P3, E1-E3, R1-R3)", "PASS",
    f"{S}numbers_ind_r4.out: M1 P = 9.85; M2 lower bound 12 > 3, position value -9 (receive 9); M3 chord 9.5 >= 9, second difference 1; E1 second differences 0, 100, 800 cents; E3 put 8 = DK - S, call 0 = max(S-DK,0); R2 bound 9.48 vs intrinsic 20; Section 5 bound 40.48. P1 algebra re-derived; P3 parity-to-puts identity re-derived.")
row("FC2b-math-L05-why-it-matters-rate", "2.9 prose / 2.4 math", "L05.html:51 (why-it-matters); round-2 FAIL re-verified", "PASS",
    "The round-2 FAIL (non-negative rate qualifier) is still resolved: L05.html:51 states the American-call equality 'at a non-negative rate' and 'under Theorem 4.1 of Lesson 5' (also L05.html:301). Word count 119 (text_checks_ind_r4.out).")
row("FC2b-math-L06-thm1.4", "2.4 math", "L06.html:76-90 (Def 1.3, Theorem 1.4 (a)-(c), proof)", "PASS",
    "(a) subtraction gives Delta S0 (u-d) = V1(u)-V1(d) (L06.html:82): unique. (b) V0 = ((R_f-d)V1(u)+(u-R_f)V1(d))/((u-d)R_f) re-derived (L06.html:85-86); q > 0 needs R_f > d and 1-q > 0 needs u > R_f (L06.html:88). (c) replicated arbitrage at pi > V0 gives (pi-V0) R_f > 0 in both states (L06.html:89); reversal for pi < V0.")
row("FC2b-math-L06-thm2.2-thm3.3", "2.4 math", "L06.html:116-153 (Theorem 2.2; Definitions 3.1-3.2; Theorem 3.3 and closed-form induction)", "PASS",
    f"Closed-form induction re-derived at L06.html:152 (Pascal rule, factor R_f^{{-(m+1)}}). {S}numbers_ind_r4.out: Theorem 3.3 closed form equals backward induction for N = 4 on 20 random payoffs; Theorem 1.4(b) identity on 200 random exact parameter sets.")
row("FC2b-math-L06-examples", "2.2 numbers / 2.4 math", "L06.html:93-99 (Ex 1.5, 1.6), 155-158 (Ex 3.4)", "PASS",
    f"{S}numbers_ind_r4.out: Ex1.5 Delta 1/2, B -20, V0 30, q 3/4; replication 75-20*5/4 = 50 and 25-25 = 0 (L06.html:94). Ex1.6 cash 5, lent to 25/4, both states 25/4 (L06.html:99). Ex3.4: V(1,1)=75, V(0,0)=45, closed form 45, 4500 cents (L06.html:157).")
row("FC2b-math-L06-remarks-misconceptions", "2.2 numbers / 2.4 math", "L06.html:101-105, 114, 327-336", "PASS",
    f"Remark 1.7 and the Section 2 remark: E^Q[S1] = R_f S0 exactly at q = (R_f-d)/(u-d) (algebra). Misconception 3 (L06.html:334): 156.25, 56.25, 36, 70.3125 = 1125/16 all recomputed in {S}numbers_ind_r4.out.")

# ---- numbers in prose (2.2)
row("FC2b-num-L04", "2.2 numbers", "L04.html prose numbers (lines 51, 73, 116, 120, 125, 243, 258-266, 335-377, 389-390)", "PASS",
    f"Every L04 prose number recomputed exactly ({S}numbers_ind_r4.py / .out): 6.561 -> 6.56, 14.58, 18, 108, 93, 127.43484, 32.805, 0.10536, 25, 17, 77, 54, 8.10. Display rounding stated at L04.html:243.")
row("FC2b-num-L05", "2.2 numbers", "L05.html prose numbers (lines 51, 286, 315, 352, 359, 366, 402-416, 434, 480-531)", "PASS",
    f"{S}numbers_ind_r4.out: 30/20/10/1/0 USD calls, 2/1/0/0/8 USD puts, 40.48, 9.48, 9.85, 12, 9, 15, 100, 0.9*120 - 100 = 8, second differences 0/100/800 cents, -300 cents planted cost. Line 286 'printed calls are in cents' matches the printed 'synthetic calls, cents'.")
row("FC2b-num-L06", "2.2 numbers", "L06.html prose numbers (lines 94, 99, 157, 319, 332, 342-388, 441-476)", "PASS",
    f"{S}numbers_ind_r4.out: 3/4, 1/2, 30, 3000 cents, 25/4, 45, 4500 cents, 75, 156.25, 56.25, 36, 70.3125, M1 V0 40 (4000 cents), M2 Delta 2/3 and B -80/3, M3 V(0,0) 48 (4800 cents), E2 60 (6000 cents), E3 arbitrage cash 0 and 5/2 both states, R1 replication, R2 q 1/2, V0 25, B -25.")
row("FC2b-num-L04-why-locator", "2.2 numbers (locators)", "L04.html:51, 116, 360, 374 (locators for the derived numbers)", "PASS",
    "Each derived number carries a page locator (Example 2.5 at L04.html:116; table L04.html:235-242; R1 L04.html:360; R3 L04.html:374). Quiz numbers resolve to Example 2.5 or Lab 1 Part 2 (L04.html:443-445, 454).")

# ---- structure and prose (2.9)
row("FC2b-struct-L04", "2.9 structure", "L04.html (BUILDER_RULES 4.2 order and counts)", "PASS",
    "Order: why-it-matters (L04.html:51, 120 words), core sections 1-2 (Definition, Lemma, Proposition, Example, Remark blocks), inline Lab 1 (L04.html:123-244), canon (L04.html:246-251), misconceptions 4 (L04.html:253-273), problem set M1-M3, P1-P3, E1-E3, R1-R3 each with details.solution, key-results table (L04.html:380-394), quiz 9 items with explain blocks (L04.html:396-466). data-hours=7 and 'Lesson 4 of 8 · 7 study hours' agree with the hub card (index.html:138).")
row("FC2b-struct-L05", "2.9 structure", "L05.html (BUILDER_RULES 4.2 order and counts)", "PASS",
    "Order: why-it-matters (L05.html:51, 119 words), sections 1-4, inline Lab 1 (L05.html:131-287), canon (L05.html:313-318), misconceptions 4 (L05.html:320-340), problem set 3 per tier with solutions (L05.html:342-420), key-results table (L05.html:447-462), quiz 9 items (L05.html:464-534). data-hours=8 agrees with index.html:139.")
row("FC2b-struct-L06", "2.9 structure", "L06.html (BUILDER_RULES 4.2 order and counts)", "PASS",
    "Order: why-it-matters (L06.html:51, 113 words), sections 1-3 plus Definition 3.5, inline Lab 1 (L06.html:165-317), canon (L06.html:319-324), misconceptions 3 (L06.html:326-336), problem set 3 per tier (L06.html:338-396), key-results (L06.html:398-410), quiz 10 items (L06.html:412-481). data-hours=8 agrees with index.html:140.")
row("FC2b-hours", "2.9 hours", "L04-L06 data-hours; index.html:29 and cards 138-140", "PASS",
    "data-hours L04=7, L05=8, L06=8 (grep, misc_ind_r4.out); hub cards 'L04 · 7 h', 'L05 · 8 h', 'L06 · 8 h' (index.html:138-140); hub data-hours-lessons=60 and data-hours-project=30 sum to 90 (index.html:29). Lessons L01-L08 sum to 60 by the plan's split (6+8+9+7+8+8+8+6).")
row("FC2b-banned-process", "2.9 banned phrases / process words", "L04-L06 visible prose", "PASS",
    f"{S}text_checks_ind_r4.py / .out: no hit for TODO, TBD, lorem, brevity, beyond the scope, left as an exercise, important to note, studies show, experts agree, well known, obviously, clearly, 'it can be shown that', builder, verifier, agent, reviewer, planner, architect, orchestrat, mutant, round (visible text, labs excluded).")
row("FC2b-notation", "2.4 notation", "L04-L06 math vs notation/notation.json", "PASS",
    f"{S}scope_symbols_ind_r4.out: single-letter symbols used: L04 AEHKSVXacefhirstx; L05 ACDEKPSVXZegrstx; L06 BKNRSVabdfijkmnqru. No standalone T in math, no Phi, gamma, R^*, R^e*. R_f in L06 is the gross riskless return (notation.json symbols[6] meaning). \\mathbb{{Q}} matches symbols[7]. Raw \\mathbb{{E}} in L06 (20 uses) has the meaning of macro \\E (notation.json macros) and does not collide; noted, not failed.")
row("FC2b-dag-links", "2.9 DAG", "L04-L06 concept links and definitions", "PASS",
    "check_dag passes (gate). Links: L05 to L04#def-option-payoff and #def-american-option (earlier lesson); L06 to L01#def-arbitrage-opportunity, L04#def-option-payoff, L04#def-american-option; concepts.html for present-value, continuous-compounding, expectation, discount-factor (M1/M4 closure). No link to FI1 convexity; 'convexity in strike' is written in full (L05.html:107).")
row("FC2b-define-before-use-self-financing", "2.9 define before use", "L06.html:161-162 (Definition 3.5)", "PASS",
    "'self-financing' first appears in the dfn at L06.html:161-162; later uses L06.html:275, 283, 313 come after it. 'claim' is used at L06.html:55 before Definition 1.2 (L06.html:64) introduces it; it is a plain term, noted, not failed.")
row("FC2b-scope-words", "2.9 scope words", "L04-L06 'every', 'all', 'never', 'any', 'always', 'only', 'exactly', 'same' (all prose contexts)", "PASS",
    "All contexts listed this round (exact grep with 60-char context). Each is either a proved claim (e.g. 'never better than selling' L04.html:262 by Prop 2.2; 'exactly one replicating portfolio' L06.html:79 by Theorem 1.4(a); 'for every strike' L05.html:64 by Theorem 1.2), a finite check printed by a lab ('all 40 pairs' L05.html:133 and output L05.html:269), or a stated convention. No unsupported scope word found.")
row("FC2b-simulated-labels", "2.8 SIMULATED labels", "L04 Example 2.5 (L04.html:115), L04 lab (L04.html:124-128), L05 lab (L05.html:132-136)", "PASS",
    "SIMULATED appears in the Example 2.5 title, the L04 lab heading/hypothesis, L04.html:128 (twin docstring line 3), the L05 lab heading/hypothesis and L05.html:136 (twin docstring line 3). The L06 lab is labelled 'All inputs are model values' (L06.html:167) and the twin docstring says no data is read; no generated data is presented as market data.")
row("FC2b-figures", "2.8 figures", "L04-L06 (no figures, data-files or data-cite)", "PASS",
    "grep for data-files, data-cite, <svg, <img, figures- in L04-L06: none (2.8 nothing to check for this slice).")
row("FC2b-lab-rng-network", "2.5 labs (RNG, network)", "tests/labs/FC2 L04/L05/L06 twins (read in full)", "PASS",
    "misc_ind_r4.out: no random, socket, urllib or http in the three twins; the only 'random' tokens are the docstring sentences 'draws no random numbers'. Each runs under python -I -W error with empty stderr (twin_vs_page_ind_r4.out). Runtime 0.0 s in page_smoke.")

# ---- cards (BUILDER_RULES 7; cards_ind_r4.py / .out; cards_slice_ind_r4.txt)
row("FC2b-cards-coverage", "2.7 cards coverage", "cards.json: 68 cards with lesson L04 (18), L05 (24), L06 (26)", "PASS",
    f"{S}cards_ind_r4.out lists the 68 slice cards. Every definition, lemma, theorem, proposition, corollary, remark-result, example and misconception in L04-L06 has a card: L04 Def 1.1 c051, Lemma 1.2 c052, Def 2.1 c053, Prop 2.2 c054, Prop 2.3 c055, Remark 2.4 c059, Example 2.5 c056/c057/c135, Remark 2.6 c062, break-even c058, misconceptions c059-c062; L05 Def 1.1 c063, Thm 1.2 c064, Def 2.1 c065, Thm 2.2 c066/c160/c161/c162, Remark 2.3 c067, Def 3.1 c068, Thm 3.2 c069, Cor 3.4 c070, Remark 3.3 c153, Thm 4.1 c071/c132, r<0 c080, Problem-level c072-c079, misconceptions; L06 Def 1.1 c081, Def 1.2 c082, Def 1.3 c083, Thm 1.4 c084/c085/c163, Ex 1.5 c086/c136, Ex 1.6 c097, Remark 1.7 c087, Def 2.1 c088, Thm 2.2 c089, Def 3.1 c090, Def 3.2 c092, Thm 3.3 c093/c150, Ex 3.4 c094/c098/c137/c148, Def 3.5 c174, A6' c149, Section 4 c096, misconceptions c087/c091/c098.")
row("FC2b-cards-duplicates", "2.7 duplicates (full deck)", "cards.json (whole deck, full scan)", "PASS",
    f"{S}cards_ind_r4.out: 164 ids, 164 unique; no exact duplicate fronts. Near-duplicate scan (word Jaccard >= 0.45 on front+back, touching L04-L06) lists 9 pairs, judged in the next row.")
row("FC2b-cards-near-duplicate", "2.7 near duplicates", "L05 c160/c161/c162/c066; L06 c084/c089/c163/c150; L05 c071/c132; L04 c143 vs L02 c017", "PASS",
    "c160 (lower bound on C), c161 (upper bound on P), c162 (lower bound on P) and c066 (0 <= C <= S) test different bounds; c084 (formula), c150 (multi-period formula) and c163 (uniqueness) test different facts. c084 and c089 state the same identity in two notations (Theorem 1.4(b) and Theorem 2.2); judged as distinct cards because each is the lesson's own statement and the question differs (cost vs discounted expectation), not a duplicate. c071 (date-0 price) and c132 (no exercise rule) differ. c143 (discount t to tau) and c017 (discount tau to 0, L02) differ.")
row("FC2b-cards-delta-round1", "2.7 cards delta since round-3 pin", "cards.json delta 8196077d..edbb7aa8 for L04-L06", "PASS",
    "git diff 8196077d edbb7aa8 -- course/modules/FC/FC2/cards.json: changes to slice cards: FC2-c072 only (L05, back text now says the zero holds by construction; re-verified against L05.html:286 and tests/labs/FC2/lab-FC2-L05-1.py lines 34-39 (synthetic_put) and 109-116 (main)). Other changed cards (c021, c033, c037, c043, c047, c113, c115, c165) are L02, L03, L07 and not in this slice; c170 (L03) removed (not in slice). L04 cards unchanged since round 3.")
row("FC2b-cards-hypotheses", "2.7 cards hypotheses", "cards.json hypotheses for L04-L06 propositions", "PASS",
    "c054 (A2, A3), c055 (A2, A3, A5), c064 (A1-A5), c066 (A1-A5, N), c067 (N in (a), (c)), c069 (A2, A3, A5, N), c070 (A2, A3, A5, N), c071 (A1-A5, N, r >= 0), c084 (A1, A2, A3, A5, A6), c085 (A2, A3), c089 and c093 (A6, A6'), c160-c162 (A1-A5, N) all match the statements at L04.html:94-104, L05.html:63-65, 84-86, 114-116, 299-301, L06.html:77-79, 139-141.")
row("FC2b-cards-grade-ruling9", "2.7 cards grades (ruling 9)", "cards.json grades for L04-L06", "PASS",
    "Lab-only values graded C with the lab named in basis: c058, c061, c072, c073, c074, c079, c095, c148, c155, c171. Page-derived or proved values graded T: c056, c057, c075 (values computed on the page's Problem E1 from the page's formula; judgement, see notes), c076, c086, c094, c097, c098, c135-c137. Theorems T: c052, c054, c055, c064, c066-c070, c071, c080, c084, c085, c089, c093, c096, c132, c160-c163, c150, c153.")
row("FC2b-cards-L04-grades", "2.7 cards grades", "cards.json FC2-c051..c062, c135, c142, c143, c158, c159, c176 (18 cards)", "PASS",
    "Each card checked against L04 text: c051 (L04.html:70), c052 (L04.html:77, 84), c053 (L04.html:91), c054 (L04.html:96), c055 (L04.html:104), c056/c057 (L04.html:116, 235-242), c058 (L04.html:231-232), c059 (L04.html:111, 258), c060 (L04.html:262), c061 (L04.html:266), c062 (L04.html:270), c135 (L04.html:116, 240), c142 (A3 L04.html:62), c143 (A4 L04.html:63), c158 (L04.html:249), c159 (A2 L04.html:61), c176 (A1 L04.html:60).")
row("FC2b-cards-L04-rest", "2.7 cards without grade", "cards.json L04 cards without grade (c051, c053, c142, c143, c158, c159, c176)", "PASS",
    "Definitions and restatements of A1-A4 and Def 1.1/2.1 need no grade under BUILDER_RULES 7; c158 restates which propositions use A1 (L04.html:249) and is kept ungraded (judgement, see notes).")
row("FC2b-cards-L05-C-grades", "2.7 cards grades (C)", "cards.json L05 C-graded cards c072, c073, c074, c079, c155, c171", "PASS",
    f"Each names Lab 1 in basis or text and matches {S}numbers_ind_r4.out: c072 zero residuals at 80-120 USD and the by-construction note (L05.html:286; synthetic_put at L05.html:167-172, twin lines 34-39); c073 -300 cents at 100 USD, parity payoff zero (L05.html:273-274); c074 call and put at 90 USD raised by 500 cents, parity zero (L05.html:278-279); c079 three triples with middle 90 USD (L05.html:281-284); c155 no bound or triple violated (L05.html:270-271); c171 none of the 40 pairs (L05.html:269).")
row("FC2b-cards-L05-c064", "2.7 cards (c064)", "cards.json FC2-c064 (Theorem 1.2 card)", "PASS",
    "c064: 'Every strike, not only the at-the-money one ... (Theorem 1.2). The proof uses the four payoffs, A1, A2, A3 and A5 ... and the rate of A4. It uses no distribution for S_tau (Remark 1.3).' Matches L05.html:64, 67, 71.")
row("FC2b-cards-L05-rest", "2.7 cards (L05 others)", "cards.json L05 cards c063-c070, c075, c076, c078, c080, c132, c153, c160-c162", "PASS",
    "c063 (Def 1.1); c065 (Def 2.1 and (N), L05.html:76, 80); c066 (Theorem 2.2(a)); c067 (Remark 2.3); c068 (Def 3.1, 'refers to strikes only', L05.html:107); c069 (Theorem 3.2, four cases, L05.html:116-124); c070 (Cor 3.4); c071 (Theorem 4.1 and Remark 4.2); c075 (Problem E1, L05.html:400-402, values 0, 100, 800 cents); c076 (Section 5, L05.html:315); c078 (Theorem 2.2(a) and A3, L05.html:329); c080 (Remark 4.2, Problem R2, L05.html:310, 434); c132 (Remark 4.2); c153 (Remark 3.3); c160-c162 (Theorem 2.2(b)-(d)).")
row("FC2b-cards-L06-grades", "2.7 cards (L06)", "cards.json FC2-c081..c098, c136, c137, c148-c150, c163, c166, c174 (26 cards)", "PASS",
    f"Each card checked against L06 text: c081 (L06.html:59), c082 (L06.html:64), c083 (L06.html:69), c084 (L06.html:78, 89), c085 (L06.html:79, 89), c086 and c136 (L06.html:94; {S}numbers_ind_r4.out), c087 (L06.html:104), c088 and c091 (L06.html:111, 114), c089 (L06.html:118), c090 (L06.html:128), c092 (L06.html:133-135), c093 (L06.html:141-145), c094 and c137 (L06.html:157), c148 (lab output L06.html:307), c150 (L06.html:141-144), c097 (L06.html:99), c098 (L06.html:334), c149 (L06.html:128, 322), c163 (L06.html:82), c166 (L06.html:64), c174 (L06.html:162).")
row("FC2b-cards-L06-rest", "2.7 cards without grade (L06)", "cards.json L06 cards without grade (c081-c083, c088, c090, c092, c149, c166, c174)", "PASS",
    "Each is a definition or restatement of Definitions 1.1-1.3, 2.1, 3.1, 3.2, 3.5 and A6' and the lesson text carries it (L06.html:59-73, 111, 128, 133-137, 162).")
row("FC2b-quiz-L04-L06", "2.9 quiz", "L04.html:396-466 (9 items), L05.html:464-534 (9 items), L06.html:412-481 (10 items)", "PASS",
    "Every correct option and numeric answer re-derived: L04 25, 17, V_A(0) >= V_E(0), 20, only at expiry, 77, 6.56, date 1, Lemma 1.2 option; L05 S - DK, 9.85, sell call and buy share, 12, weight (K3-K2)/(K3-K1), 1 (20-2*10+1), Theorem 4.1 equality, (N), 40.48; L06 u/d/R_f/payoffs, 0.5, 30, d<R_f<u, 0.75, arbitrage with sell call/buy 1/2 share/borrow 20/lend 5, 45, replication no, 75, 100. The changed L05 explain line (L05.html:489) still states the A3 reason correctly.")
row("FC2b-cards-key-mirror", "2.9 key-results tables vs cards", "key-results tables L04.html:380-394, L05.html:447-462, L06.html:398-408 vs cards", "PASS",
    "L04 table rows (T) match c054, c055, c056, c057, c052 (Example 2.5 and Lemma 1.2). L05 table rows match c064, c066-c070, c071 and the C row matches c072/c155 (SIMULATED). L06 table rows match c084, c089, c085, c093, and the 45 row matches c094.")
row("FC2b-cards-c176-added", "2.7 card c176 (L04)", "cards.json FC2-c176", "PASS",
    "c176 (A1 of Lesson 4: nothing paid over the life) matches L04.html:60 and carries no grade (restatement).")
row("FC2b-misconception-L04-L06-other", "2.9 misconceptions (L04 2-4, L05 2-4, L06 1-3)", "L04.html:256-271, L05.html:327-337, L06.html:327-335", "PASS",
    "L04 misconceptions 2 (Prop 2.2), 3 (Lab 1 payoff 25 vs profit 17, break-even 108), 4 (Example 2.5 hindsight, Remark 2.6); L05 misconceptions 2 (Theorem 2.2(a) and A3), 3 (triples, L05.html:281-284), 4 (Theorem 4.1 date 0 only, Remark 4.2); L06 misconceptions 1 (Remark 1.7, price 30), 2 (Theorem 2.2, q not a probability), 3 (36 vs 45 vs 70.3125). Each evidence is non-circular.")
row("FC2b-misconception-L05-1", "2.9 misconception (L05 1)", "L05.html:323-326 (misconception 1, evidence sentence); lab zero residuals L05.html:286; twin lab-FC2-L05-1.py synthetic_put", "PASS",
    "Round-3 FAIL is fixed in the pinned tree: L05.html:325 now reads 'Lab 1 builds its puts from parity, so its zero residuals hold by construction and are not evidence; the planted put error at 100 USD is detected because it breaks the identity (a parity cost of -300 cents).' The evidence for 'for every strike' is Theorem 1.2 (L05.html:64, 67, 71). Consistent with the twin (synthetic_put, twin lines 34-39, builds P from parity) and the printed -300 (L05.html:273).")

fragment = {
    "unit": "FC2",
    "slice": "b",
    "round": 4,
    "verifier": "Haiku independent verifier, FC2 slice b round 4 (did not build FC2)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin; previous fragment /Users/billyribeiro/.fanout/frags/S-FC2-b.round3.json). Delta 8196077d..edbb7aa8 read in full for the slice (L05.html:325, 489; L06.html:281-283; tests/labs/FC2/lab-FC2-L06-1.py:111-114; cards.json c072 and removed L03 c170).",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-FC2-b",
    "scratch": "none outside the checkout; all scripts are under ledgers/FC2/scripts/FC2-b-r4/",
    "verified_at": "2026-11-09T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Scope: slice b = L04.html, L05.html, L06.html; lab twins tests/labs/FC2/lab-FC2-L04-1.py, lab-FC2-L05-1.py, lab-FC2-L06-1.py; the 68 slice cards (L04 18, L05 24, L06 26) in course/modules/FC/FC2/cards.json. Every row re-derived in this round; no row carried from round 3.",
        "Mutation testing: not applicable. Slice b has no project grader; mutants apply only to project graders (ruling in verifier-rules.md). mutants is empty.",
        "Ruling 26 (severity rule): the text of 'ruling 26' is not in verifier-rules.md or the files given to this verifier, so I could not apply its severity wording. The one FAIL is classed by the rule it violates (sentences about what a lab prints vs the output, including docstrings: verifier-rules.md hunt class 2). It is a low-severity wording defect with no numeric or mathematical error.",
        "Judgement accepted, not failed: (1) c075 is graded T with basis 'Problem E1 (exact)': its values are computed on the page from the page's own formula (L05 twin docstring), consistent with the plan section 10 convention; c072 is C because it is a lab output. (2) c158 and c142/c143/c159/c176 carry no grade (restatements of hypotheses, BUILDER_RULES 7). (3) c084 and c089 state the same identity in two notations. (4) Corollary 3.4 and Theorem 4.1 list (N) that their proofs do not use (over-listing). (5) L06 A2 (L06.html:55) omits 'no bid-ask spread', which L04 A2 (L04.html:61) and L05 (L05.html:317) state; the numbering is the same, so not failed. (6) L06.html:322 'Assumption A6' holds u, d and R_f fixed across nodes' reads awkwardly but is not wrong. (7) Raw \\mathbb{E} in L06 instead of the registered macro \\E: same meaning, not a collision.",
        "Not checked: the live verify_refs run (needs network; the slice cites no key); a browser screenshot of L04-L06 (page_smoke's geometry and console checks passed, no visual review); the hub, L01-L03, L07-L08 and project pages (other slices); the full text of the three curriculum sources (no key cited in this slice)."
    ],
    "summary": "FC2 slice b round 4 (pin edbb7aa8): 67 rows, 66 PASS, 1 FAIL. The one FAIL (FC2b-lab-L06-docstring, low severity) is a twin docstring sentence that says prices are printed in integer cents while the output prints stock prices and payoffs in currency units. All gates (check_pages, check_dag, check_projects, run_graders, run_labs, page_smoke for L04-L06, ruff, mypy, pytest, verify_refs --offline) pass. The round-3 FAIL (L05 misconception 1) is fixed. Every number in prose re-derived (63 exact checks). Twins match page code and expected blocks."
}

Path("ledgers/FC2/FC2-b.json").write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", sum(r["status"] == "PASS" for r in rows), "fail", sum(r["status"] == "FAIL" for r in rows))
