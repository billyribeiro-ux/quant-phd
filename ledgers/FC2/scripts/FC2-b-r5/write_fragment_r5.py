"""Build ledgers/FC2/FC2-b.json (round 5) and validate it with tools/ledger.py."""
import json
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyC5-FC2-b"
sys.path.insert(0, f"{ROOT}/tools")
import ledger  # noqa: E402

P = "PASS"
GATE = "Re-run at 04626e9 this round"
rows = [
    ("FC2-b-gate-check-pages", "tools/check_pages.py --unit FC2", "L04.html, L05.html, L06.html", P,
     f"{GATE}: 'check_pages FC2: PASS'."),
    ("FC2-b-gate-check-dag", "tools/check_dag.py --unit FC2", "L04-L06 links and definitions", P,
     f"{GATE}: 'check_dag FC2: PASS'. L04 has no 'convex' (grep -i convex); L06 has no 'AP1' (grep AP1 returns nothing)."),
    ("FC2-b-banned-and-process-words", "grep -i for builder/verifier/round/audit/TODO/placeholder/pending/honest", "L04-L06 pages", P,
     "grep -n -i -E 'builder|verifier|round |audit|TODO|placeholder|pending|honest' over the three pages: no hits; 'planted' appears only in lab code and printed output labels (L05.html:251-285), which is lab wording."),
    ("FC2-b-page-smoke", "tools/page_smoke.py --unit FC2 --pages L04 L05 L06 --skip-sweep", "L04-L06", P,
     f"{GATE}: 'page_smoke FC2: PASS' (L05 runtime boot 1.2 s, lab-FC2-L06-1 0.0 s)."),
    ("FC2-b-hours", "data-hours on L04/L05/L06 and hub cards index.html:138-140, :29-31", "L04.html:2, L05.html:2, L06.html:2; index.html:29,31,138-140", P,
     "data-hours 7/8/8 match hub card kickers L04 7 h, L05 8 h, L06 8 h. Sum of all eight lesson hours 6+8+9+7+8+8+8+6 = 60 = index data-hours-lessons=60; 60+30=90 (index.html:31); 30/90 = 33.3%. Unchanged this round."),
    ("FC2-b-lab-run-L04", "tools/run_labs.py --unit FC2; python -I -W error tests/labs/FC2/lab-FC2-L04-1.py", "L04.html lab-FC2-L04-1; tests/labs/FC2/lab-FC2-L04-1.py", P,
     "run_labs --unit FC2: 'run_labs FC2: PASS (11/11)'. Twin alone under -I -W error: exit 0, stderr 0 bytes."),
    ("FC2-b-lab-L04-hypothesis", "read hypothesis paragraph against twin output", "L04.html:125", P,
     "Hypothesis: call payoff 0 up to 100 and profit negative below 108 (output rows 100.00 to 125.00: call profit -8.00, 17.00); put break-even 93 (output 'put break-even spot ... 93.00'); best dates 1 and 3 (output 'best exercise date ... t = 1', 't = 3'); holding call 6.56 (output 'call held to expiry, PV at 0: 6.56'). Part 2 factor 9/10 matches DISCOUNT = Fraction(9, 10) (twin line 22)."),
    ("FC2-b-lab-L04-exact", "twin lines 17-21, 66-84, 191-209; ledgers/FC2/scripts/FC2-b-r5/twin_vs_page_r5.py", "tests/labs/FC2/lab-FC2-L04-1.py:22, :68", P,
     "DISCOUNT = Fraction(9, 10) (twin line 22) and DISCOUNT ** (expiry - t) (twin line 68). No float exponent in the code. Output equals the page expected block (twin_vs_page_r5.py: 'L04 EXPECTED==OUTPUT: True')."),
    ("FC2-b-lab-L04-header", "L04.html expected block and twin output header", "L04.html:233 and :242; twin part_two print", P,
     "twin_vs_page_r5.py: 'L04 EXPECTED==OUTPUT: True'. Header 'call hold (value at t)' and 'put hold (value at t)' appear in both."),
    ("FC2-b-lab-L05-run", "tools/run_labs.py --unit FC2; python -I -W error tests/labs/FC2/lab-FC2-L05-1.py", "L05.html lab-FC2-L05-1", P,
     "run_labs --unit FC2: PASS (11/11 includes L05). Twin alone: exit 0, stderr 0 bytes. twin_vs_page_r5.py: 'L05 PAGE_CODE==TWIN: True', 'L05 EXPECTED==OUTPUT: True'."),
    ("FC2-b-lab-L05-claims", "L05.html lab hypothesis (:133) and interpretation (:286) against twin output", "L05.html:133, :286; lab-FC2-L05-1", P,
     "Hypothesis: parity cost zero at five strikes and payoff zero at 40 pairs (output: 'nonzero at 0 of 40'); put +300 at 100 gives -300 (output '[0, 0, -300, 0, 0]'); call+put at 90 +500 gives three violated triples all with 90 middle (output 'violated 3' and three lines 'call at 9000 cents lies above the chord'). Interpretation: calls 30,20,10,1,0 and puts 2,1,0,0,8 USD match the printed cents (3000,2000,1000,100,0 and 200,100,0,0,800). Re-derived with ledgers/FC2/scripts/FC2-b-r5/numbers_r5.py."),
    ("FC2-b-lab-L05-D-claim", "L05 twin docstring lines 138-143 (D = 9/10; bounds hold for D >= 1/40; convexity for every D)", "tests/labs/FC2/lab-FC2-L05-1.py:1-7, :21", P,
     "numbers_r5.py: bounds_ok False at D = 1/41 (call at 80 = 100.05 > spot), True at 1/40 (call at 80 = 100.00) and at every D sampled in [1/40, 3] step 1/100. Convexity holds at D = 9/10 and at 200 random D in [0.01, 2]. Claim 'hold only for D >= 1/40 on this grid' matches. Call at D = 1/100 is 101.20 > 100 (docstring says 'exceeds the spot': TRUE)."),
    ("FC2-b-lab-L06-run", "tools/run_labs.py --unit FC2; python -I -W error tests/labs/FC2/lab-FC2-L06-1.py", "L06.html lab-FC2-L06-1", P,
     "run_labs PASS (11/11 includes L06). Twin alone exit 0, stderr 0 bytes. twin_vs_page_r5.py: 'L06 PAGE_CODE==TWIN: True', 'L06 EXPECTED==OUTPUT: True'."),
    ("FC2-b-lab-L06-claims", "L06.html lab hypothesis (:162), interpretation (:309), output lines 286-308", "L06.html:162, :309", P,
     "Hypothesis: one-period 30 (3000 cents) output line 291-292; two-period 45 (4500 cents) output line 298-299; all True lines 293, 304-308. Interpretation 'say nothing about any market' and 'u, d, R_f fixed' consistent with the code (twin constants SPOT, STRIKE, UP, DOWN, RETURN; no data read)."),
    ("FC2-b-num-L04", "ledgers/FC2/scripts/FC2-b-r5/numbers_r5.py (Fraction)", "L04.html:116, :120, :242, :335, :342, :349, :358, :360, :372-374, :445; Remark 2.6", P,
     "Example 2.5: call intrinsic 0,20,0,0,10; hold 10(9/10)^4 = 6.561 -> 6.56; exercise at 1 = 20*9/10 = 18; put best date 3 = 20(9/10)^3 = 14.58 (put intrinsic 0,0,10,20,0). R1: S_tau = 100 + 20000/729 = 92900/729 = 127.43484 to 5 d.p. (exact in script). R3: best early PV 7.29, hold PV 32.805. E2: put PV 6.561 -> 6.56, best date still 3, call best still 1 (18.00). E3: 10(9/10)^2 = 8.10. M1 payoff 12, profit 8, break-even 54; M2 break-even 77, payoff 20, profit 17. r = ln(10/9) = 10.54 per cent. All match page text."),
    ("FC2-b-num-L05", "numbers_r5.py", "L05.html:352, :359, :366, :402, :416, :434, :441, :480, :494, :508, :526, :531", P,
     "M1 P = 8 - 100 + 101.85 = 9.85; M2 bound 12, cash 9; M3 chord 9.5, second difference 1; E1 second differences 0, 100, 800 cents; E3 put bound 8, call bound 0; R2 bound 120 - 110.517 = 9.48 (script 9.4829) vs intrinsic 20; canon put example 100e^{-0.1} - 50 = 40.4837 -> 40.48. Quiz numeric answers 9.85, 12, 1, 40.48 consistent. Planted convexity triples re-derived: (80,90,100), (80,90,110), (80,90,120) = 3 triples."),
    ("FC2-b-num-L06", "numbers_r5.py (exact)", "L06.html:94, :99, :157, :327, :337, :345, :365, :369, :373, :383, :385", P,
     "Example 1.5: q = 3/4, Delta = 1/2, B = -20, V0 = 30 = (3/4 * 50)/(5/4). Example 1.6: surplus 35-50+20 = 5 lent to 25/4. Example 3.4: V(1,1) = 75, V(1,0) = 0, V(0,0) = 45; E^Q[S_2] = 625/4 = 156.25 = R_f^2 S_0; E^Q[payoff] = 1125/16 = 70.3125; payoff at expected price 56.25, discounted 36. M1 q = 1/2, V0 = 40; M2 Delta = 2/3, B = -80/3; M3 V(1,1)=120, V(0,0)=48; E2 V0 = 60; E3 surplus 2 with payoffs 5/2 both states; R2 q = 1/2, V0 = 25. Closed form 16/25 * 9/16 * 125 = 45."),
    ("FC2-b-grades", "key-results tables L04 (:386-390), L05 (:453-458), L06 (:396-400); claim spans", "L04.html:386-390; L05.html:453-458; L06.html:396-400", P,
     "Each key-results row matches a theorem, proposition or example on the page and carries the right grade: the SIMULATED lab row in L05 is C (:458). L04 Example 2.5 values are T as arithmetic from A4."),
    ("FC2-b-math-L04-lemma-prop", "L04 Lemma 1.2, Propositions 2.2 and 2.3, Remark 2.4, P1-P3, R2", "L04.html:77-125, :320-323", P,
     "Lemma 1.2 proof checks both sign cases. Prop 2.2 (A2, A3) and Prop 2.3 (A2, A3, A5) proofs re-read and correct; Prop 2.3 proof uses no date other than 0 and tau. P3 chord inequality proof valid (each affine piece of max(K-s,0) is below f). Remark 2.4 now qualifies the equality at date 0 (:111). Scope issue at :248 is a separate row."),
    ("FC2-b-math-L04-thm41-hyp", "L04 citations of Theorem 4.1 (:111, :258 and card FC2-c059)", "L04.html:111, :258", P,
     "Each citation carries 'a non-negative rate' and date-0 scope (:111, :258). The unqualified citation at :248 is recorded in FC2-b-math-L04-canon-date0."),
    ("FC2-b-math-L05-T1.2-T2.2", "L05 Definition 1.1, Theorem 1.2 and proof, Theorem 2.2 (a)-(d), Remark 2.3", "L05.html:59, :67, :76-103", P,
     "Def 1.1 adds 'parity cost' = C - P - S + DK, which is V0 in the proof of Theorem 1.2 (:67) and is the quantity Lab 1 prints as 'parity cost'. Parts (a)-(d) portfolios and payoffs re-derived: (a) S-C, payoff min(S,K); (b) C-S+DK, payoff (K-S)^+; (c) DK-P, payoff min(S,K); (d) P+S-DK, payoff (S-K)^+. Proof intro (:94) 'parts (a) and (c) use a second portfolio' is correct (buy one call :95, buy one put :97). Remark 2.3 uses (N) only in (a), (c). Term 'parity portfolio' is introduced by the forward reference to the proof, not defined separately (noted, not a defect)."),
    ("FC2-b-math-L05-T3.2-C3.4-P3", "L05 Definition 3.1, Theorem 3.2 proof cases (i)-(iv), Remark 3.3, Corollary 3.4, P1, P3, R3", "L05.html:111-128, :290-295, :375-391, :437-441", P,
     "Theorem 3.2 case algebra re-derived: (iii) g = (1-lambda)(K3 - s) >= 0; (iv) g = K2 - lambda K1 - (1-lambda) K3 = 0. Initial value lambda C1 + (1-lambda) C3 - C2 correct. Remark 3.3 second difference C1 - 2C2 + C3 correct. Corollary 3.4 portfolio correct. R3 now says 'do not rise with strike', matching the Corollary. P3 algebra: S-terms cancel and D-bracket is zero by P1."),
    ("FC2-b-math-L05-T4.1", "L05 Theorem 4.1 statement (:301) and proof (:304-306), Remark 4.2 (:309-310)", "L05.html:301, :304-306, :309-310", P,
     "Proof now applies Prop 2.3 under A2, A3, A5 (:304) and writes the date-t portfolio explicitly (:305). Date-t bound: V_E(t) - S_t + e^{-r(tau-t)}K >= 0 by A3 gives V_E(t) >= S_t - e^{-r(tau-t)}K >= S_t - K since r >= 0. Remark 4.2 states the date-0 scope; it says the theorem does not say how the buyer should behave on each path, which supports the page's 'no rule for later dates' sentences (L04 :120, :262; L05 :337). Round-4 FAIL resolved."),
    ("FC2-b-math-L06-T1.4ab", "L06 Definition 1.3, Theorem 1.4 (a), (b), proof, Remark 1.7, Theorem 2.2", "L06.html:69-88, :99, :111-118", P,
     "Re-derived: Delta = (V1u - V1d)/((u-d)S0), R_f B = (u V1d - d V1u)/(u-d), V0 = [(R_f-d)V1u + (u-R_f)V1d]/((u-d)R_f). q = (R_f-d)/(u-d), 1-q = (u-R_f)/(u-d); 0<q<1 from A6. Example 1.5 numbers match (Delta 1/2, B -20, V0 30)."),
    ("FC2-b-math-L06-T1.4c", "L06 Theorem 1.4(c) parenthetical (:79) and proof (c) (:89)", "L06.html:79, :89", P,
     "Round-4 FAIL resolved. Line 79 now reads 'sell the claim and hold the replicating portfolio, or buy the claim and sell the replicating portfolio, and invest the surplus'. Both cases re-derived: pi > V0 sell claim, buy replicating, lend pi - V0 gives (pi - V0) R_f > 0; pi < V0 reversed gives (V0 - pi) R_f > 0. Matches proof (:89) and Example 1.6 (:99)."),
    ("FC2-b-math-L06-T2.2-T3.3", "L06 Theorem 2.2, Definitions 3.1-3.2, Theorem 3.3 statement and closed-form proof (:146-152), Example 3.4", "L06.html:117-158", P,
     "Closed-form induction re-derived: coefficients binom(m, i-1) and binom(m, i) with Pascal's rule; R_f powers match. Example 3.4 values re-derived (V(1,1)=75, V(1,0)=0, V(0,0)=45, closed form 45). Definition 3.1 node count n+1 correct."),
    ("FC2-b-math-L06-examples", "L06 Examples 1.5, 1.6, Remark 1.7, Section 4 canon-breaks, Misconceptions 1-3, E1 (:365), R1, R3", "L06.html:94-106, :314-327, :365, :377-387", P,
     "E1 now reads 'the closed form printed on the next line' (:365); lab output has V0 line 298 and closed form line 299: TRUE. Section 4 three-price example: last two equations force Delta = 0 and R_f B = 0, then 0 = 1 (re-derived). Misconception 3 numbers (156.25, 56.25, 36, 45, 70.3125) re-derived. R1 replicating claim (50, 0, -50 with Delta 1 and B -80) re-derived."),
    ("FC2-b-notation", "notation/notation.json (R_f, \\mathbb{Q}, T) against L04-L06 symbols", "L04.html, L05.html, L06.html", P,
     "Registry: R_f = gross riskless return for the period (L06 :59, :64 use R_f = 1 + r_1 per period: same meaning). \\mathbb{Q} = risk-neutral measure (L06 :111, :114: same meaning). L04/L05 use r as the continuous rate of A4 and D = e^{-r tau} locally, and L06 :59 says the unsubscripted r is not used there. No registered symbol reused with another meaning in the slice. 'T' not used in the slice."),
    ("FC2-b-dag-AP1", "grep -n AP1 course/modules/FC/FC2/L0[456].html", "L06.html:114 (former AP1 link)", P,
     "grep returns nothing for AP1 in L04-L06. L06 :114 says 'A different measure, for a general model, is outside this unit' with no link. check_dag FC2 PASS."),
    ("FC2-b-dag-convex", "grep -i convex course/modules/FC/FC2/L04.html", "L04.html:320-323 (P3)", P,
     "grep -i convex on L04.html returns nothing. P3 states the chord inequality for max(K-s,0) without the FC-unit term. check_dag FC2 PASS."),
    ("FC2-b-cards-L04", "cards.json FC2-c051..c062, c135, c142, c143 against L04.html", "cards.json FC2-c051..c062, c135, c142, c143", P,
     "Each card read against L04 text. c059 'strict for any put or call' matches Remark 2.4 (:111) and misconception 1 (:258). c060 matches misconception 2 (:262). c142 matches A3 (:62) exactly. c143 matches A4 (:63): x e^{r(tau-t)}. c135 value 18.00 = 20*9/10 matches Example 2.5. All numbers (6.56, 18.00, 14.58, 108, 93, 25.00, 17.00) match output/text. Grades T with basis present."),
    ("FC2-b-card-c059", "cards.json FC2-c059 back (round-4 fix)", "cards.json:409 (FC2-c059)", P,
     "Back: 'No. Proposition 2.3 proves only the weak inequality V_A(0) >= V_E(0), and the lesson does not claim that it is strict for any put or call (Remark 2.4).' Matches Remark 2.4 and misconception 1. Round-4 PASS holds."),
    ("FC2-b-cards-L05", "cards.json FC2-c063..c080, c132 against L05.html; FC2-c069 wording", "cards.json:477-481 (FC2-c069), :514 (FC2-c074); FC2-c077 absent between c076 (line 530) and c078", "FAIL",
     "Card FC2-c069 back: 'The proof is a payoff argument on the butterfly position, checked in four cases.' The term 'butterfly' appears nowhere in L05.html (grep -i butterfly over FC2 returns only this card), so the card names a position the lesson never names. Other L05 cards match their text: c063-c067, c070-c076, c078-c080 re-checked; c074 corrected to parity holds (matches Lab 1 output); c132 corrected (see FC2-b-card-c132)."),
    ("FC2-b-cards-L06", "cards.json FC2-c081..c098, c136, c137 against L06.html", "cards.json FC2-c081..c098, c136, c137", P,
     "Each card re-read against L06 and re-derived in numbers_r5.py: c085 (A3 not said to fail; both cases of Theorem 1.4(c)), c091 (q = 3/4, u = 3/2), c094 (45 = 4500 cents), c095 (True lines 304-308; holdings 3/4 and -30 at cost 45), c096 (Section 4), c097 (25/4), c098 (56.25 -> 36; 45). c136 V0 = 30 = (3/4*50)/(5/4); c137 V(1,1) = 75."),
    ("FC2-b-card-c085", "cards.json FC2-c085 back", "cards.json FC2-c085", P,
     "Back states the zero-cost positive-payoff portfolio for pi != V0 and the two directions, matching Theorem 1.4(c) and Example 1.6. Round-4 PASS holds."),
    ("FC2-b-cards-duplicates", "duplicate scan of cards.json (142 cards)", "course/modules/FC/FC2/cards.json", P,
     "Re-run this round: 142 cards; duplicate ids [], duplicate fronts [], duplicate backs []. Gap at FC2-c077 (card removed this round, see FC2-b-cards-removed-c077); no repo reference to FC2-c077 (grep)."),
    ("FC2-b-quiz", "quiz items in L04 (:400-465), L05 (:464-533), L06 (:405-473)", "L04.html:401-464; L05.html:469-532; L06.html:409-472", P,
     "Numeric answers: L04 17, 20, 77, 6.56 (tol 0.005); L05 9.85 (tol 0.005), 12, 1, 40.48 (tol 0.005; 40.4837); L06 0.5, 30, 0.75, 45, 75 (tol 0). Explanations re-derived. L05 Q7 explanation now says 'at date 0' (:517). L05 Q8 'Beyond A1 to A5, (N)' is correct because (N) is stated separately (:76). Each of the 5 multiple-choice items in each quiz has one data-correct option (L04: 5 mc items, L05: 5, L06: 5 of 10 items)."),
    ("FC2-b-refs", "tools/verify_refs.py --offline; L04-L06 References sections", "L04.html:468-472; L05.html:536-540; L06.html:476-480", P,
     "verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'. The three pages cite no registry key (their References sections say so)."),
    ("FC2-b-data-figures", "grep -c '<svg|<img|data-files' on L04-L06", "L04.html, L05.html, L06.html", P,
     "Count 0 for all three pages. No dataset or figure; SIMULATED paths labelled SIMULATED (L04 :116, L05 :286, L06 Lab claim)."),
    ("FC2-b-math-L05-misconception-deep-itm", "L05 misconception 'A deep in-the-money call should be exercised early' (:336-337) and card FC2-c132", "L05.html:337", P,
     "Round-4 FAIL resolved. Line 337 now says Theorem 4.1 gives equal prices 'at date 0 only' and that the lesson 'proves no rule for holding against exercising at a later date (Remark 4.2)'. Consistent with Remark 4.2 (:310) and Proposition 2.2 bound (L04)."),
    ("FC2-b-cards-new-L04-L06", "new/changed cards FC2-c135 (L04), c136, c137 (L06), c142, c143 (L04)", "cards.json", P,
     "Each new card checked against its page and recomputed in numbers_r5.py: 18.00 (20*9/10), 30 (50-20), 75 ((3/4*125)/(5/4)). Grades T with basis. c142 and c143 match A3 and A4 text."),
    ("FC2-b-math-L04-canon-date0", "L04 Section 3 'Where the canon breaks', second paragraph (:248)", "course/modules/FC/FC2/L04.html:248", "FAIL",
     "Sentence: 'Lesson 5 proves bounds for European prices and an equality for an American call with no income and a non-negative rate (Theorem 4.1 there).' The equality holds at date 0 only (L05 Theorem 4.1 :301, Remark 4.2 :309-310). Round 5 fixed the same overstatement in L04 :111, :258, :262 and L05 :301, but this sentence still states the equality unqualified."),
    ("FC2-b-card-c132", "cards.json FC2-c132 (round-4 FAIL)", "cards.json:925 (FC2-c132)", P,
     "Front: 'Does Lesson 5 give a rule for exercising a deep in-the-money call early when r >= 0?' Back: 'No... Theorem 4.1 gives equal American and European call prices at date 0 only... proves no rule... (Remark 4.2).' The round-4 claim 'Depth in the money does not change this (Section 6; Remark 4.2)' is removed. Matches L05 :337 and Remark 4.2."),
    ("FC2-b-cards-refs", "tools/check card numbers against lesson text (ledgers/FC2/scripts/FC2-b-r4/card_refs_r4.py, run this round)", "cards.json FC2-c076 '(Section 5)'", P,
     "The round-5 run reports 'MISSING FC2-c076 L05 Section 5'. The literal string is absent, but L05.html:314 is the numbered heading '5 Where the canon breaks' and the card's Section 5 is that heading. The card's number appears in its lesson, so this is recorded as PASS (the regex, not the card, is the limit). All other card references (Theorem, Remark, Example, Problem, Lemma, Proposition, Corollary, Definition) appear in their lessons."),
    ("FC2-b-cards-removed-c077", "cards.json FC2-c077 removed this round (L05)", "cards.json (removed between FC2-c076 at line 530 and FC2-c078)", P,
     "Removed card 'Does put-call parity hold only for at-the-money options?' repeats L05 misconception 1 (:324-325), which is still present. No reference to FC2-c077 in the repo (grep). The id gap is harmless: check_pages requires only the id pattern and no duplicates."),
    ("FC2-b-terms-L05", "defined and used terms in L04-L06 (parity cost, break-even, parity portfolio, risk-neutral probability)", "L04.html:73; L05.html:59; L06.html:111", P,
     "'break-even' defined at L04:73 before its use in the lab hypothesis (:125). 'parity cost' defined at L05:59 before the lab uses it (twin docstring and output). 'parity portfolio' is named in L05:59 by forward reference to the proof at :67, which describes it; not a defect. 'risk-neutral probability' is defined at L06:111 and introduced in the header (L06:38)."),
]

out_rows = []
for rid, check, loc, status, ev in rows:
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != P:
        r["fix"] = {
            "FC2-b-cards-L05": "In cards.json FC2-c069 back, replace 'on the butterfly position' with 'on the portfolio of the proof of Theorem 3.2' (or define butterfly on L05.html). Re-run card check.",
            "FC2-b-math-L04-canon-date0": "In L04.html:248, change 'and an equality for an American call' to 'and, at date 0, an equality for an American call'.",
        }[rid]
    out_rows.append(r)

frag = {
    "unit": "FC2",
    "slice": "b",
    "round": 5,
    "verifier": "Haiku independent verifier (FC2 slice b, round 5; did not build FC2)",
    "pin": "04626e9",
    "base": "b276325 (round-4 pin; delta b276325..04626e9 read for every L04-L06 hunk, card and lab twin)",
    "checkout": ROOT,
    "scratch": "/tmp",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "FAIL",
    "rows": out_rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta b276325..04626e9 for slice b: L04.html (meta, why-it-matters, Def 2.1, Remark 2.4, Remark 2.6, lab docstring/interpretation, misconceptions 1-2, R3, key quiz none), L05.html (meta, why-it-matters, Def 1.1, Theorem 2.2 proof intro, Theorem 4.1 proof, misconception 4, R3, quiz 7-8), L06.html (Theorem 1.4(c), Remark, E1), lab-FC2-L04-1.py (docstring only), cards.json (c004..c143 changes; c077 removed; c139-c141 L02 and c144 L03 new, out of slice). Every hunk in slice b was read.",
        "Round-4 FAIL rows resolved: FC2-b-math-L06-T1.4c, FC2-b-math-L05-misconception-deep-itm, FC2-b-card-c132 (c132 part of FC2-b-cards-L05). FC2-b-cards-L05 stays FAIL for the new c069 wording.",
        "Labs are demonstrations; mutation testing does not apply (verifier-rules ruling). mutants list empty by ruling.",
        "Out of slice, not a row: course/modules/FC/FC2/index.html:138 describes L04 as 'the exercise decision for one contract with and without early exercise'; L04 Remark 2.6 says the example is not a decision rule. Hub owner should align.",
        "Out of slice, not checked: L01-L03, L07-L08 pages and cards (other than the cross-check of hours), project page, grader, project labs 1-3.",
        "Commands run at 04626e9: check_pages FC2 (PASS), check_dag FC2 (PASS), run_labs --unit FC2 (11/11 PASS), twin alone under python -I -W error (L04, L05, L06 exit 0, stderr empty), page_smoke FC2 --pages L04 L05 L06 --skip-sweep (PASS), ruff check and ruff format --check on the three twins (clean), mypy --no-incremental tests/labs/FC2 (no issues), pytest -k FC2/FC/twin/lab in test_labs, test_run_labs, test_page_checks (all passed), verify_refs --offline (560 entries, 0 problems).",
        "Not run: full project gate (ruff/mypy over the whole repo, pytest full), check_projects, run_graders, mutate_graders, tools/fetch_data.py, render_curriculum.py: these belong to other slices or the full-gate run; not needed for slice b.",
    ],
    "summary": "FC2 slice b round 5: 46 rows, 44 PASS, 2 FAIL. FAIL rows: FC2-b-math-L04-canon-date0 (L04.html:248 states the Theorem 4.1 equality without 'at date 0'); FC2-b-cards-L05 (cards.json FC2-c069 names a 'butterfly position' the lesson never names). Round-4 FAIL rows FC2-b-math-L06-T1.4c, FC2-b-math-L05-misconception-deep-itm and FC2-b-card-c132 are now PASS.",
}

problems = ledger.validate(frag, "FC2-b")
print("validate:", problems)
with open(f"{ROOT}/ledgers/FC2/FC2-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(out_rows), "PASS", sum(r["status"] == "PASS" for r in out_rows), "FAIL", sum(r["status"] == "FAIL" for r in out_rows))
