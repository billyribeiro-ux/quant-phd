"""Write the FC2 slice-b round-4 fragment (run with python -I from the checkout root)."""
import json

CARRY3 = "Carried from round 3 (course/modules/FC/FC2/L05.html lab block and L05 twin byte-identical since the previous pin; only L05.html lines 305 and 310 changed): "
CARRY3_L06 = "Carried from round 3 (tests/labs/FC2/lab-FC2-L06-1.py and the L06.html lab block byte-identical since the previous pin; L06.html changed only at lines 79, 114, 327): "
CARRY3_L04 = "Carried from round 3 (L04 lemma and proposition text byte-identical since the previous pin; only L04.html lines 111, 116-125, 247, 256, 320-323 and the Example 2.5 numbers changed): "
NO_CHANGE_R4 = "Re-run on the pin in round 4: "

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("FC2-b-gate-check-pages", "2.9-structure", "course/modules/FC/FC2/L04.html, L05.html, L06.html", "PASS",
     NO_CHANGE_R4 + "`.venv/bin/python tools/check_pages.py --unit FC2` -> 'check_pages FC2: PASS'."),
 row("FC2-b-gate-check-dag", "2.9-DAG", "course/modules/FC/FC2/L04.html, L05.html, L06.html", "PASS",
     NO_CHANGE_R4 + "`.venv/bin/python tools/check_dag.py --unit FC2` -> 'check_dag FC2: PASS'. grep: L04 has no 'convex'; L06 has no 'AP1'; links unchanged."),
 row("FC2-b-banned-and-process-words", "2.9-banned", "L04.html, L05.html, L06.html", "PASS",
     NO_CHANGE_R4 + "grep -i for builder|verifier|round |audit|TODO|placeholder|pending|honest over the three pages: only 'planted' (L05.html:286,325,333,407,425), the teaching term for a planted error in Lab 1. New text adds no process word."),
 row("FC2-b-page-smoke", "2.5/2.9-smoke", "L04.html, L05.html, L06.html", "PASS",
     NO_CHANGE_R4 + "`.venv/bin/python tools/page_smoke.py --unit FC2 --pages L04 L05 L06 --skip-sweep` -> 'page_smoke FC2: PASS' (each page lab ran)."),
 row("FC2-b-hours", "2.9-hours", "L04.html:2 (7 h), L05.html:2 (8 h), L06.html:2 (8 h); index.html:29, 138-140", "PASS",
     "data-hours 7/8/8 match hub cards 138-140 (L04 7 h, L05 8 h, L06 8 h). Hub split 60 + 30 = 90 (index.html:29). Unchanged this round."),
 row("FC2-b-lab-run-L04", "2.5-labs", "course/modules/FC/FC2/L04.html lab-FC2-L04-1; tests/labs/FC2/lab-FC2-L04-1.py", "PASS",
     NO_CHANGE_R4 + "run_labs FC2 -> 'run_labs FC2: PASS (11/11)'. Twin alone: `.venv/bin/python -I -W error tests/labs/FC2/lab-FC2-L04-1.py` exit 0, stderr empty (output /tmp/fc2b_r4_lab-FC2-L04-1.py.out, not kept). cmp_expected_r4.py: L04 EXPECTED==OUTPUT True, 23 lines (ledgers/FC2/scripts/FC2-b-r4/cmp_expected_r4.py). Twin imports fractions only; no RNG."),
 row("FC2-b-lab-L04-hypothesis", "2.5-labs", "L04.html lab hypothesis paragraph (line 125)", "PASS",
     NO_CHANGE_R4 + "hypothesis now says call best date 1, put best date 3, holding call 6.56 USD at date 0, and the discount factor 9/10. Output prints 'hindsight best exercise date for the call ... t = 1', '... put ... t = 3', 'call held to expiry, PV at 0: 6.56'. All match."),
 row("FC2-b-lab-L04-exact", "2.5-labs (exactness, plan 5.7)", "tests/labs/FC2/lab-FC2-L04-1.py:17-21, 66, 191-209", "PASS",
     "Round-3 FAIL resolved. Part 2 now uses DISCOUNT = Fraction(9, 10) and DISCOUNT**(expiry - t) (twin lines 21, 66-67 and 76-84); no math.exp remains (grep). Part 1 is integer cents. Values re-derived exactly in ledgers/FC2/scripts/FC2-b-r4/numbers_r4.py: 6.561, 7.29, 8.10, 9.00, 10.00, 18, 14.58, 6.561 match the printed table."),
 row("FC2-b-lab-L04-header", "2.5-labs (claim vs print)", "tests/labs/FC2/lab-FC2-L04-1.py:~187-190; L04.html:233 (expected block) and :242 (interpretation)", "PASS",
     "Round-3 FAIL resolved. Header now reads 'call hold (value at t)' and 'put hold (value at t)' in the twin and in the expected block (cmp_expected_r4.py: True). Interpretation (L04.html:242) says only the t=0 row is a present value at date 0 and equals the foot-of-table value 6.56; 1000(9/10)^4 = 656.1 cents, prints 6.56 (numbers_r4.py)."),
 row("FC2-b-lab-L05-run", "2.5-labs", "course/modules/FC/FC2/L05.html lab-FC2-L05-1; tests/labs/FC2/lab-FC2-L05-1.py", "PASS",
     NO_CHANGE_R4 + "run_labs FC2 PASS (11/11 includes L05). Twin alone under -I -W error exit 0, stderr empty. cmp_expected_r4.py: L05 EXPECTED==OUTPUT True, 21 lines."),
 row("FC2-b-lab-L05-claims", "2.5-labs (claims)", "L05.html lab hypothesis and interpretation; lab-FC2-L05-1", "PASS",
     CARRY3 + "round-3 evidence (cmp_expected_vs_output_r3.py; output in ledgers/FC2/scripts/FC2-b-r3/twin-output-L05-1.txt): zero parity cost at five strikes, 0 of 40 nonzero payoff checks, -300 at 100 USD for the put raised 300 cents, and the three convexity triples with 90 USD in the middle. Re-run this round: output matches the expected block."),
 row("FC2-b-lab-L05-D-claim", "2.5-labs (docstring claim)", "tests/labs/FC2/lab-FC2-L05-1.py docstring; ledgers/FC2/scripts/FC2-b-r3/l05_D_sweep_r3.py", "PASS",
     CARRY3 + "round-3 sweep (l05_D_sweep_r3.py, python -I): at D = 1/100 C(80) = 101.2 > 100 (bounds fail); no failure at D = 1/40; smallest D on the 1/1000 grid with no failure is 1/40. The lab docstring 'hold only for D >= 1/40 on this grid' is consistent. Re-derivation not repeated this round; the lab twin and docstring are unchanged."),
 row("FC2-b-lab-L06-run", "2.5-labs", "course/modules/FC/FC2/L06.html lab-FC2-L06-1; tests/labs/FC2/lab-FC2-L06-1.py", "PASS",
     NO_CHANGE_R4 + "run_labs FC2 PASS includes L06. Twin alone under -I -W error exit 0, stderr empty. cmp_expected_r4.py: L06 EXPECTED==OUTPUT True, 23 lines. pytest tests/test_labs.py tests/test_run_labs.py -k 'FC2 or L04 or L05 or L06': 69 passed."),
 row("FC2-b-lab-L06-claims", "2.5-labs (claims)", "L06.html lab hypothesis, interpretation and printed True lines", "PASS",
     CARRY3_L06 + "round-3 evidence: 30 (3000 cents) by replication and by risk-neutral expectation; 45 (4500 cents) by induction and closed form; each path check True. Re-run this round: output matches the expected block."),
 row("FC2-b-num-L04", "2.2-numbers", "L04.html Example 2.5 (line 116), Lab 1 interpretation (242), Remarks 2.6, R1 (359), R3 (373), E1-E3 (334-348), M1-M3, quiz (441-453), key results (388-389)", "PASS",
     NO_CHANGE_R4 + "ledgers/FC2/scripts/FC2-b-r4/numbers_r4.py (Fraction): 10(9/10)^4 = 6.561 -> 6.56; 20(9/10) = 18; 20(9/10)^3 = 14.58 (729/50); 10(9/10)^3 = 7.29; 10(9/10)^2 = 8.10; 1000(9/10)^4 = 656.1 cents; R1 S_tau = 100 + 20000/729 = 127.43484 (92900/729); R3 50(9/10)^4 = 32.805. ln(10/9) = 0.10536. All match the page."),
 row("FC2-b-num-L05", "2.2-numbers", "L05.html Problems M1-M3, E1-E3, R2, canon-breaks (line 406-ish), quiz, lab interpretation", "PASS",
     CARRY3 + "round-3 recomputation (numbers_L04_L06_r3.py): M1 P = 9.85; M2 bound 12; R2 9.48; canon 40.48. L05.html changed only at lines 305 and 310, which carry no number."),
 row("FC2-b-num-L06", "2.2-numbers", "L06.html Examples 1.5, 1.6, 3.4 (line 327), M1-M3, E2, R2; misconception 3; quiz 417-460", "PASS",
     NO_CHANGE_R4 + "numbers_r4.py: q = 3/4; Delta = 1/2; B = -20; V0 = 30; V(1,1) = 75; V(0,0) = 45; E_Q[S_2] = 625/4 = R_f^2 S_0; discounted 100; payoff at expected price 225/4 discounted 36; E_Q[payoff] = 1125/16 = 70.3125 (line 327 now states this). All match."),
 row("FC2-b-grades", "2.3-grades", "L04/L05/L06 key-results tables and claim spans", "PASS",
     NO_CHANGE_R4 + "re-graded the changed spans against BLUEPRINT section 3. L04 Example 2.5 values (6.56, 18.00, 14.58) are T as arithmetic of a stated path and A4. L05 key-results row 'no bound violated on the SIMULATED set' stays C. L06 P3-style claim at line 327 graded as arithmetic on the page (T). The new card FC2-c132 is graded T but its claim is not established by the lesson; see FC2-b-math-L05-misconception-deep-itm and FC2-b-cards-L05."),
 row("FC2-b-math-L04-lemma-prop", "2.4-math", "L04.html Lemma 1.2, Propositions 2.2 and 2.3, Remark 2.4, P1, P2, R2", "PASS",
     CARRY3_L04 + "round-3 re-derivation; Proposition 2.2 (A3 excludes X>0 with V0=0), Proposition 2.3 (A3 contradiction) and P1-P2 unchanged. Changed P3 is row FC2-b-dag-convex."),
 row("FC2-b-math-L04-thm41-hyp", "2.4-math (hypotheses)", "L04.html:111, :247, :256 and card FC2-c059", "PASS",
     "Round-3 FAIL resolved. Every L04 citation of Theorem 4.1 now carries 'a non-negative rate': L04.html:111 (Remark 2.4), :247, :256 (misconception 1), and why-it-matters at :51. Card FC2-c059 back now says 'and a non-negative rate'. Theorem 4.1 itself is at L05.html:301 with r >= 0."),
 row("FC2-b-math-L05-T1.2-T2.2", "2.4-math", "L05.html Theorem 1.2, Theorem 2.2 (a)-(d), Remark 1.3, Remark 2.3", "PASS",
     CARRY3 + "round-3 re-derivation; parity and bound portfolios unchanged (L05 hunks only at 305, 310)."),
 row("FC2-b-math-L05-T3.2-C3.4-P3", "2.4-math", "L05.html Theorem 3.2, Corollary 3.4, Remark 3.3, P1, P3", "PASS",
     CARRY3 + "round-3 four-case proof of Theorem 3.2 and Corollary 3.4 re-derived; unchanged this round."),
 row("FC2-b-math-L05-T4.1", "2.4-math (proof)", "L05.html:305 (proof), :310 (Remark 4.2)", "PASS",
     "Round-3 FAIL resolved. The proof no longer applies Theorem 2.2(b) at date t. It writes the date-t portfolio explicitly (buy European call V_E(t), sell one share, lend e^{-r(tau-t)}K), payoff (S_tau-K)^+ - S_tau + K = (K-S_tau)^+ >= 0 by checking the two cases, then A3 (V0 <= 0 and X >= 0 forces V0 = 0, so V0 >= 0 by contradiction), then e^{-r(tau-t)}K <= K from r >= 0 and K > 0. Second inference V_E(t) >= 0 by the same A3 step. Remark 4.2 now says the date-t equality is a remark. Re-derived by hand; no step uses the date-0 result."),
 row("FC2-b-math-L06-T1.4ab", "2.4-math", "L06.html Theorem 1.4 (a), (b), Proof (a), (b), Remark 1.7, Theorem 2.2", "PASS",
     NO_CHANGE_R4 + "re-derived: Delta = (V1u - V1d)/((u-d)S0); R_f B = (u V1d - d V1u)/(u-d); V0 = [(R_f-d)V1u + (u-R_f)V1d]/((u-d)R_f) = q-expectation / R_f with q = (R_f-d)/(u-d), 0 < q < 1 under A6. numbers_r4.py confirms with the example inputs."),
 row("FC2-b-math-L06-T1.4c", "2.4-math (statement)", "course/modules/FC/FC2/L06.html:79 (Theorem 1.4(c) parenthetical)", "FAIL",
     "The round-3 defect (A3 listed as hypothesis and then 'A3 fails') is fixed: line 79 now reads 'given A2, if the claim trades at a price pi != V0 ..., then a zero-cost portfolio with a strictly positive payoff exists ... A3 excludes such a portfolio, so under A3 the price is V0'. The proof at L06.html:81-84 (c) is correct: sell claim, buy replicating portfolio, lend surplus pi-V0, payoff (pi-V0)R_f > 0. But the statement's parenthetical reads '(sell the claim and hold the replicating portfolio, or buy the claim and sell it, and invest the surplus at the riskless rate)'. 'Buy the claim and sell it' is self-contradictory; the second case is buy the claim and SELL THE REPLICATING PORTFOLIO (short it), as the proof's 'reverse every position' says.",
     "In L06.html line 79 replace 'or buy the claim and sell it' with 'or buy the claim and sell the replicating portfolio'. Re-embed is not needed (no lab). Same wording fix in the statement only."),
 row("FC2-b-math-L06-T2.2-T3.3", "2.4-math", "L06.html Theorem 2.2, Definitions 3.1-3.2, Theorem 3.3, Example 3.4", "PASS",
     CARRY3 + "round-3 closed-form induction re-derived (Pascal step, index shift); Example 3.4 numbers re-derived this round (V(0,0)=45, V(1,1)=75). Unchanged except line 327, which is row FC2-b-num-L06."),
 row("FC2-b-math-L06-examples", "2.4-math (examples)", "L06.html Examples 1.5, 1.6, Remark 1.7, Section 4 canon-breaks, E3, R1", "PASS",
     CARRY3_L06 + "round-3 recomputation of Example 1.6 (cash 5 lent to 25/4), E3 (cash 2, payoff 5/2), R1 (B=-80), Section 4 three-price example (Delta*50=0 forces Delta=0, then 0=1). Lines 79, 114 and 327 changed, none of these examples."),
 row("FC2-b-notation", "2.4-notation", "L04.html, L05.html, L06.html; notation/notation.json", "PASS",
     NO_CHANGE_R4 + "grep: no \\Phi, \\gamma, R^\\ast, T-as-symbol in L04 or L05 pages; L06 uses \\mathbb{Q} (registered as probability measure) and R_f (gross return) with registered meanings. The L06 change at line 114 adds no symbol."),
 row("FC2-b-dag-AP1", "2.9-DAG", "course/modules/FC/FC2/L06.html:114", "PASS",
     "Round-3 FAIL resolved. grep -n AP1 over L04-L06 returns nothing. Line 114 now says 'A different measure, for a general model, is outside this unit, and this lesson does not use it.' No AP1 link, name or concept use."),
 row("FC2-b-dag-convex", "2.9-DAG (plan 6.2)", "course/modules/FC/FC2/L04.html P3 (lines 320-323)", "PASS",
     "Round-3 FAIL resolved. grep -i convex over L04.html returns nothing. P3 is now 'A chord inequality for the put payoff' and states the inequality without the word 'convex'. The first use of 'convexity in strike' in L05 is at L05.html:7 (meta) and the body definition at :111. L05 line 7 and body usage name strike convexity only."),
 row("FC2-b-cards-L04", "2.7-cards", "course/modules/FC/FC2/cards.json FC2-c051..c062 and new FC2-c135", "PASS",
     "Read every L04 card against L04.html. c059 fixed (non-negative rate). Updated c-cards for Example 2.5 (values 6.56, 18.00, 14.58 correct). New c135: '20 * 9/10 = 18.00 USD' matches Example 2.5 and Lab 1 Part 2. Grade T for each arithmetic card. All cited items exist in L04 (card_refs_r4.py)."),
 row("FC2-b-card-c059", "2.7-cards", "cards.json id FC2-c059", "PASS",
     "Back: 'Lesson 5 (Theorem 4.1) proves equality for a call on an underlying with no income and a non-negative rate, so the early-exercise premium is zero there.' Carries the hypothesis of Theorem 4.1 (L05.html:301)."),
 row("FC2-b-cards-L05", "2.7-cards", "course/modules/FC/FC2/cards.json FC2-c063..c080, FC2-c132", "FAIL",
     "New card FC2-c132 (L05, grade T): 'Should a deep in-the-money call ... be exercised early when r >= 0? No. ... selling the European call at V_E(t) >= S_t - K does at least as well as exercising ... (Section 6; Remark 4.2).' Remark 4.2 (L05.html:310) says the opposite of a decision rule: 'It does not say how the buyer of an American call should behave on each path', and 'the theorem says nothing about the price of the American call at t'. The card's 'selling the European call' is also not the holder's position; the holder owns the American call. Other L05 cards (c063-c080, c074 Problem E2 and c076 Section 5 exist in the page) read correctly against the lesson.",
     "Delete FC2-c132, or rewrite it to a true, proved statement: 'Under A1 to A5, (N) and r >= 0, Theorem 4.1 gives equal American and European call prices at date 0 only; at a later date the lesson proves no decision rule (Remark 4.2).' Keep its id unused or renumber with the same grading rule."),
 row("FC2-b-cards-L06", "2.7-cards", "cards.json FC2-c081..c098, FC2-c136, FC2-c137", "PASS",
     "Read every L06 card. c085 fixed (A3 is no longer said to fail). c087 (Delta 1/2, B -20) and c088 (V(0,0)=45, Lab 1 prints 45) match Example 1.5 and Example 3.4. New c136 (V0 = 50 - 20 = 30 = (3/4*50)/(5/4)) and c137 (V(1,1) = (3/4*125)/(5/4) = 75) recomputed in numbers_r4.py and match Lab 1 and Example 3.4."),
 row("FC2-b-card-c085", "2.7-cards", "cards.json FC2-c085", "PASS",
     "Back now: 'The price is not the replicating cost, so a zero-cost portfolio with a strictly positive payoff in every state exists, which A3 excludes; under A3 the price is V_0.' Matches the corrected statement at L06.html:79 (the parenthetical wording remains a FAIL in row FC2-b-math-L06-T1.4c, and the card's own text does not repeat that error)."),
 row("FC2-b-cards-duplicates", "2.7-cards", "cards.json (137 cards, FC2-c001..c137)", "PASS",
     NO_CHANGE_R4 + "full scan: 137 cards; no duplicate fronts or backs (script output: 'dup fronts [] dup backs []'). Numbered references in L04-L06 cards: every Theorem/Remark/Example/Lemma/Proposition/Definition/Corollary/Problem/Section cited is present in its page, except the naming 'Problem E2' and 'Section 5/6', which the page carries as 'E2 ·' and as section headings 5 and 6 (card_refs_r4.py: 3 textual misses, all of that form). No card repeats another."),
 row("FC2-b-quiz", "2.9-quiz", "L04.html quiz (lines 408-453; answers 17, 20, 77, 6.56), L05.html quiz (477-528), L06.html quiz (417-460)", "PASS",
     NO_CHANGE_R4 + "L04 numeric answer changed to 6.56 (tolerance 0.005), explanation 6.561 -> 6.56, and 18.00. Other answer keys re-checked against the lesson text: 17, 20, 77 (L04); 9.85, 12, 1, 40.48 (L05); 0.5, 30, 0.75, 45, 75 (L06). All consistent."),
 row("FC2-b-refs", "2.1-citations", "L04/L05/L06 References sections; references/references.json", "PASS",
     NO_CHANGE_R4 + "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems'. The three lessons cite no registry key (their References sections say so)."),
 row("FC2-b-data-figures", "2.8-data", "L04.html, L05.html, L06.html", "PASS",
     NO_CHANGE_R4 + "grep -c '<svg|<img|data-files' = 0 for all three pages. No dataset or figure. Simulated paths labelled SIMULATED (L04 Example 2.5 and Lab 1; L05 Lab 1)."),
 row("FC2-b-math-L05-misconception-deep-itm", "2.9-prose / 2.4 (decision claims)", "course/modules/FC/FC2/L05.html:336-337 (misconception 'A deep in-the-money call should be exercised early')", "FAIL",
     "New in round 4. The misconception says 'Remark 4.2 explains that selling the call at V_E(t) >= S_t - K does at least as well as exercising'. Remark 4.2 (L05.html:310) says nothing of the kind; it says the theorem 'does not say how the buyer of an American call should behave on each path' and that the date-t equality is 'a remark, not a proved result'. The cited bound concerns the European call, which the American holder does not own. The lesson's own L04 misconception (L04.html:261) says 'Whether holding beats selling is a question for Lesson 5', and Lesson 5 does not answer it for t > 0. So the misconception asserts a decision rule the page does not prove and mis-cites Remark 4.2.",
     "Replace L05.html:337 with: 'For an underlying with no income, r >= 0 and (N), Theorem 4.1 gives equal American and European call prices at date 0 only. Proposition 2.2 gives the exercise value as a lower bound on the market value, but the lesson proves no rule for holding against exercising at a later date (Remark 4.2).' Remove the 'selling the call at V_E(t)' clause. Also fix card FC2-c132 as in FC2-b-cards-L05."),
 row("FC2-b-cards-new-L04-L06", "2.7-cards", "cards.json FC2-c135 (L04), FC2-c136, FC2-c137 (L06)", "PASS",
     "Each new card checked against its page and recomputed in numbers_r4.py: 18.00 (20*9/10), 30 (50-20; (3/4*50)/(5/4)), 75 ((3/4*125)/(5/4)). Each grade T with a basis that names the example or lab."),
]

frag = {
 "unit": "FC2",
 "slice": "b",
 "round": 4,
 "verifier": "Haiku independent verifier (FC2 slice b, round 4)",
 "pin": "b276325",
 "base": "ccfdf4c",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyC4-FC2-b",
 "scratch": "/tmp",
 "verified_at": "2026-10-29T02:30:00+00:00",
 "verdict": "FAIL",
 "rows": rows,
 "mutants": [],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": [
   "Delta ccfdf4c..b276325 for slice b: L04.html (hunks at 51-340 and the Example 2.5 block), L05.html (lines 305 and 310 only), L06.html (lines 79, 114, 327), lab-FC2-L04-1.py (rewritten to Fraction, DISCOUNT 9/10), cards.json (c059, c085, c132, c135, c136, c137 new or changed; other changed cards are L02, L03, L07, L08 and out of slice).",
   "Mutants: labs are demonstrations, not graders; mutation testing does not apply (verifier-rules ruling). No mutants listed.",
   "Previously FAILed round-3 rows re-verified from scratch and now PASS: FC2-b-lab-L04-exact, FC2-b-lab-L04-header, FC2-b-math-L04-thm41-hyp, FC2-b-math-L05-T4.1, FC2-b-dag-AP1, FC2-b-dag-convex, FC2-b-card-c059, FC2-b-card-c085. FC2-b-math-L06-T1.4c stays FAIL on a new wording defect in the same line.",
   "Out of slice, not a row: plans/FC2 hub index.html:138 describes L04 as 'the exercise decision for one contract with and without early exercise'; L04 Remark 2.6 says it is not a decision rule. Hub owner should align.",
   "Out of slice, not checked: L01-L03, L07-L08 pages and cards (including new card FC2-c133 at L03), project, grader."
 ],
 "summary": "FC2 slice b round 4: 45 rows, 43 PASS (of which 6 carried from round 3 with the prefix), 2 FAIL rows for L06 Theorem 1.4(c) parenthetical wording (L06.html:79) and the L05 deep-in-the-money misconception plus card FC2-c132 (L05.html:336-337; cards.json) that cite Remark 4.2 for a decision rule the remark denies; mutants 0/0 (not applicable to labs)."
}
rows_count = len(rows)
print("rows", rows_count, "PASS", sum(r["status"] == "PASS" for r in rows), "FAIL", sum(r["status"] == "FAIL" for r in rows))
json.dump(frag, open("ledgers/FC2/FC2-b.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
