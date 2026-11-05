# Builds ledgers/PC3/PC3-a.json (round 9). Row ids, checks and locations are those of round 8 (kept), with round-9 status and evidence.
import json, sys
ROOT = sys.argv[1]
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-a.round8.json"))
O = "ledgers/PC3/scripts/PC3-a-r9/outputs/"
S = "ledgers/PC3/scripts/PC3-a-r9/"
ev = {
"PC3a-check-pages": ("PASS", f"check_pages PC3: PASS, exit 0 ({O}check_pages.out), run on c93dd526."),
"PC3a-check-dag": ("PASS", f"check_dag PC3: PASS, exit 0 ({O}check_dag.out). Every linked concept on index/L01/L02/L03 is in the closure (recomputed: coursekit.prerequisite_closure('PC3') = AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1); fermi-estimation (L01.html:59) and expected-value-game (L03.html:87) are defined once on their pages."),
"PC3a-check-projects": ("PASS", f"check_projects PC3: PASS, exit 0 ({O}check_projects.out). Project content is outside this slice; its hub claims are checked in PC3a-r6-hub-project-file-names, PC3a-r7-hub-hours-line-items, PC3a-r7-hub-autograder-seeds."),
"PC3a-run-labs": ("PASS", f"run_labs PC3: PASS (9/9), exit 0 ({O}run_labs.out); the three slice twins are among the nine."),
"PC3a-twins-alone": ("PASS", f"python -I -W error on each twin, exit 0: {O}twin_lab-PC3-L01-1.out, twin_lab-PC3-L02-1.out, twin_lab-PC3-L03-1.out (printed output shown in each file)."),
"PC3a-pytest-labs": ("PASS", f"pytest tests/test_labs.py -k PC3 -q: 9 passed, exit 0 ({O}pytest_labs_PC3.out); collect-only count 9 (same run, `pytest --collect-only -q`)."),
"PC3a-page-smoke": ("PASS", f"page_smoke.py --unit PC3: PASS for index, L01, L02, L03 (and L04-L06, project) with lab timings 0.0 s ({O}page_smoke_PC3.out)."),
"PC3a-ruff-mypy": ("PASS", f"ruff check tests/labs/PC3: All checks passed; ruff format --check: 9 files already formatted; mypy --no-incremental tests/labs/PC3: Success, 9 source files (outputs/ruff_check.out, ruff_format.out, mypy_labs.out)."),
"PC3a-verify-refs": ("PASS", f"verify_refs.py --offline: offline integrity 560 entries, 0 problems ({O}verify_refs_offline.out). The live run was not repeated this round; the slice cites only the two keys named at index.html:177 and no registry file changed since the round-8 pin."),
"PC3a-hub-hours": ("PASS", "index.html:29 data-hours-lessons=36, data-hours-project=14; index.html:42 '36 h lessons · 14 h project (28%)'; index.html:167 line items sum to 14 (1+1+3+2+2+4+1); L01/L02/L03 line 2 data-hours=6 and line 34 '6 study hours'. 6 x 6 = 36, 36 + 14 = 50."),
"PC3a-hub-placement": ("PASS", "index.html:76-136: ten items; eight prerequisite items (Pq1-Pq8: M4, M4, M1, M2, CS2, FC2, CF1, AC1) and two data-skill items at lines 128 and 133; data-mastery=0.8 at line 72; 8 of 10 = 80 percent, 7 of 10 = 70 percent (line 74). Answers recomputed: 3.5, 0.25, 2, 3, log2 n, S e^{r tau}, 90.909091, assets = liabilities + equity, -10005, 10040."),
"PC3a-hub-titles-prereqs": ("PASS", "index.html:35 closure list recomputed by coursekit.prerequisite_closure('PC3') (set equals the hub list); index.html:61-67 each link's concept id is in the closure and defined by the named module (e.g. cost-of-carry-forward-price at course/modules/FC/FC2/L02.html:88)."),
"PC3a-hub-objectives": ("PASS", "index.html:48-56: objective 1 = L01 Thm 1.2 and Prop 1.3; 2 = L02 Prop 2.4 and 2.5; 3 = L03 Thm 3.8; 4-6 = L04-L06 (outside slice, consistent with hub); 7 = project (seeds 0-49 and workspace seed, project.html:397)."),
"PC3a-hub-lesson-map": ("PASS", "index.html:145-150: six cards link L01-L06 with titles matching L01.html:35, L02.html:35, L03.html:35 (Fermi Estimation and Mental Math; Probability Puzzles and Conditional Reasoning; Expected-Value Games)."),
"PC3a-hub-data": ("PASS", "index.html:37, 170-173: no data file. L01 twin reads no file (docstring line 150); L02 twin 'no file is read' (docstring line 140); L03 twin stdlib only, no randomness, no network. grep over the three twins and the three lesson pages: no open(), read_text, data-files attribute, timer or datetime call (round-9 grep)."),
"PC3a-hub-P0.1-claim": ("PASS", "index.html:35 and 74: 'not yet released' claim. course/concepts.html:34-47 lists the P0.1 entries, each ending 'not yet released'. grep of data-concept in index/L01/L02/L03: no P0.1 concept linked."),
"PC3a-L01-numbers": ("PASS", "Recomputed in ledgers/PC3/scripts/PC3-a-r9/numbers_L01_r9.py (outputs/numbers_L01_r9.out): 12000, 234000, 19.5, ln19.5 = 2.9704144656, sqrt midpoint 52990.5652, factor widths ln3, ln5, ln1.3, reductions 0.4055/0.9163/0.1754 and shares 30.8 and 5.9 percent, 2.5649, 2.0541, 2.7951, remainder/bound 0.0046221254/0.0048728552 = 0.9485, 5.4 and 7.9 percent, 1.6289, 0.1289, 0.1662, ln16.5 = 2.8034, 0.167054. All match. The E2 sentence (L01.html:405-410) is covered by PC3a-L01-E2-shares and is excluded here."),
"PC3a-L01-proofs": ("PASS", "L01.html:76-80: lemma identities ab - a'b' = a(b-b') + b'(a-a') and AB - ab = A(B-b) + b(A-a) checked; induction steps and the attainment argument hold (positivity from A1). L01.html:92-94 (Prop 1.3) and 128-135 (Thm 1.5, uses A2 for x>0 and the direct x=0 case). L01.html:374-391 (P1-P3) re-derived: 1/l - 1/x = (x-l)/(lx), Bernoulli step, binomial tail."),
"PC3a-L01-A2-false-at-x0": ("PASS", "L01.html:115 A2 stated for x != 0; 123 H3 applies A2 only for x > 0; 130 treats x = 0 directly (both sides 0). Consistent."),
"PC3a-L01-grades-lab-only": ("PASS", "L01.html:458-465: T rows (458, 459, 460, 461, 462) are proved on the page or by hand; C rows (463, 464, 465) are labelled lab results; each C value matches the printed output (outputs/numbers_L01_r9.out and twin_lab-PC3-L01-1.out)."),
"PC3a-L02-grade-drill-lab-only": ("PASS", "L02.html:508: C grade 'closed form equals enumeration on 12 of 12 items' matches the Part 1 output line 'closed form equals enumeration on 12 of 12 items' (lab expected block, L02.html:340)."),
"PC3a-L01-claims": ("PASS", "L01.html:67-90, 82, 105-107, 113-141, 317-319, 328 checked against the proofs and the lab output: Section 2 narrowings, Section 3 remainder claims (n=2 equality, n=5 and n=10 strict), Example 1.7 ratio and percentage, Section 4 limits. No mismatch."),
"PC3a-L01-lab-match": ("PASS", f"lab_twin_match_r9.py ({O}lab_twin_match_r9.out): L01 page code equals tests/labs/PC3/lab-PC3-L01-1.py and the expected block equals the twin's stdout (26 lines)."),
"PC3a-L01-problems-quiz": ("PASS", "L01.html:345-451: 13 problems (M1-3, P1-3, E1-4, R1-3), each with solution; L01.html:470-548: 10 quiz items, each explanation re-derived (Q1 10; Q2 1.386294; Q3; Q4 234000; Q5 quote updates; Q6 0.004622; Q7; Q8 Bernoulli P2; Q9 52990.5652; Q10)."),
"PC3a-L01-only-scope": ("PASS", "L01.html:55 ('only the ordinary order and arithmetic of R' lists the extra tools used: log, derivative, Taylor, binomial, square root), 82 (worst case, every combination of values in the ranges: Theorem 1.2 proof), 314 (section heading). No unsupported 'only'."),
"PC3a-L01-twin-docstring-decimals": ("PASS", "tests/labs/PC3/lab-PC3-L01-1.py:1-8 docstring (stdlib only, no randomness, assumed ranges, Fractions, ten-place decimals, 1e-12 check) matches the code; the one float check is at line 96 (abs(sum(parts) - width) < 1e-12), as the docstring says; no file is read (no open() in the twin); lab_twin_match_r9.out shows the page code equals the twin."),
"PC3a-L01-research-problems": ("PASS", "L01.html:430-449: R1 criterion (half of the total, 1.4852; ln5 = 1.6094 exceeds it), R2 (proof uses only H1, H2; no joint assumption), R3 (A [1,3] to [1,2] reduction 0.4055 vs B [1,2.5] to [1,1.01] reduction 0.9063, recomputed) all correct."),
"PC3a-L01-misconception-accuracy": ("PASS", "L01.html:327-328: 'more precise factor' correction: the drop is independent of other factors, the share is not; 30.8 percent (quote updates) and 5.9 percent (minutes) recomputed from full precision."),
"PC3a-L01-KR-ln19.5-grade": ("PASS", "L01.html:461-463: product bounds and ln19.5 are hand-derived (T) and the ten-place decimal 2.9704144656 is a printed floating-point value graded C (lab Part 1)."),
"PC3a-L01-E2-shares": ("FAIL", "L01.html:408 (E2 solution): 'Dividing those four-place values gives 0.3085, which is 30.85 percent and would display as 30.9 percent'. Recomputed (outputs/numbers_L01_r9.out): 0.9163 / 2.9704 = 0.3084770 (30.8477 percent). 0.3085 and 30.85 are correct roundings, but the quotient of the printed values displays as 30.8 percent at one decimal; 30.9 appears only by rounding the already-rounded 30.85 (double rounding). The full-precision results 0.308472 and 30.8 percent and 0.059033 and 5.9 percent are correct.",
  ),
"PC3a-L02-numbers": ("PASS", "Recomputed: L02.html:111 (1/3, 1/2), 116-117 (12/20 = 3/5, 6/20 = 3/10, 3/4), 124 (1/2, 1/2), 129 (3/4), 398-417 (57/64 by complement, E1), 449-466, 489-493, 503-507. Matches lab output lines 328-358 and the twin."),
"PC3a-L02-proofs": ("PASS", "L02.html:75-100 (Prop 2.4 and 2.5 proofs, hypotheses H1 and H2 used). L02.html:423-441 (P1 equivalence, P2 three-cell expansion, P3 conditional measure additivity) re-derived."),
"PC3a-L02-lab-match": ("PASS", f"lab_twin_match_r9.py ({O}lab_twin_match_r9.out): L02 page code equals tests/labs/PC3/lab-PC3-L02-1.py; expected block (32 lines) equals stdout."),
"PC3a-L02-interp-reverse-conditional": ("PASS", "L02.html:359 interpretation: reverse conditional 1 and forward 1/3 for two flips, matching Part 4 output lines 350 and 352."),
"PC3a-L02-misconceptions-quiz": ("PASS", "L02.html:376-388 (three misconceptions with corrections matching Examples 2.6 and 2.8 and Part 4 output); L02.html:517-587 (10 quiz items) explanations re-derived."),
"PC3a-L02-where-canon-breaks": ("PASS", "L02.html:362-371: Example 2.8 probabilities 2/3 and 1/2 match Part 2 output; Example 2.7 swap argument (bijection preserving equal weights) is correct; Example 2.6 conditioning-event point matches the 1/3 and 1/2 values."),
"PC3a-L02-twin-bag-ball-label": ("PASS", "tests/labs/PC3/lab-PC3-L02-1.py Part 3 labels 'bag 1' and 'bag 2' and Part 4 urn labels r1-r3, b1-b2 (three red, two blue) match L02.html:116 and 129."),
"PC3a-L02-finite-probability-space-redefined": ("PASS", "L02.html:57 (Definition 2.1 'as defined in M4 Lesson 1'): course/modules/M/M4/L01.html:55 defines a finite probability space with positive weights summing to 1. L02.html:62 (A1) restates finiteness."),
"PC3a-L02-spaced-repetition": ("PASS", f"Round-8 FAIL resolved. L02.html:134 now states: 'The drill set has no spacing of its own: the drill items are not scheduled and are not cards. The spacing for this lesson comes from this lesson's cards, which finishing the quiz adds to the review deck. The review deck schedules its cards with FSRS-4.5, a spaced-repetition scheduler.' Each clause checked: quiz.js:81 adds the lesson's cards when the quiz completes (comment at quiz.js:3-4); review.js:3-4 and review.html:7 state FSRS-4.5; cards.json holds 23 L02 cards (computed with python); the lab items are generated in make_items (twin lines 172-187) and are not cards. The page now states the gap, so the curriculum element is disclosed rather than silently dropped. Architect note: the element 'with spaced repetition' is delivered through the lesson's cards, not through the drill items."),
"PC3a-L03-numbers": ("PASS", f"Recomputed in ledgers/PC3/scripts/PC3-a-r9/numbers_L03_r9.py ({O}numbers_L03_r9.out): continuation 250, value 1150/3 = 383.33, gain 100/3 = 33.33, stop faces 3-6, fee c=1 gain 74.5, R1 mean 50, biased per-turn 25 and play-all 150, 1575/32, 575/8, 625/8 (biased) and 0 for the five fair-game rules, E2 difference -575/8 = -71.875. All match the lab output and the page."),
"PC3a-L03-proofs": ("PASS", "L03.html:66-76 (Prop 3.2 linearity, finite sums), 107-110 (Def 3.7), 296-311 (Thm 3.8 and its backward induction: base, step with sum of conditional probabilities = 1 and sum x P(x|h) = 0 by H2, and V(empty) = 0). The step is valid for histories of positive probability. Re-derived."),
"PC3a-L03-A3-zero-probability-histories": ("PASS", "L03.html:292-293 (A3 quantifies histories with P(h) > 0 and fewer than N turns), 300 (H2 same condition), 308 (proof restricts to positive-probability histories and says zero-probability histories add nothing)."),
"PC3a-L03-thm-number-3-10": ("PASS", "No 'Theorem 3.10' in the slice: grep over index/L01/L02/L03 and the cross-reference scan (ledgers/PC3/scripts/PC3-a-r9/outputs/xref_r9.out) shows the only 3.10 is 'Example 3.10', which is defined at L03.html:320."),
"PC3a-L03-adapted-undefined": ("PASS", "grep 'adapted' over the slice: 0 hits. Probabilistic terms used in L03 (expectation, history, fair game, stopping rule, conditional payoff) are each defined on the page (Defs 3.1, 3.5, 3.7) or are M4/Lesson 2 concepts linked."),
"PC3a-L03-each-rule-claim": ("PASS", "L03.html:321 names the five rules; each is a function of the history only and forced to stop at N = 6 (twin RULES lines 223-229; stopping_expectation line 200). L03.html:552 Q11 consistent. Each rule is a stopping rule of Def 3.7."),
"PC3a-L03-grades-lab-only": ("PASS", "L03.html:468-475: T rows 468, 469, 470, 473, 475 are proved or hand-derived; C rows 471, 472, 474 are labelled lab results (enumeration of 64 policies, Part 3 finite enumeration, Part 3b biased game) and match outputs."),
"PC3a-L03-any-game-fee": ("PASS", "L03.html:448-450 (R2): gain for fee c = (sum_f max(100 f, 350 - c))/6 - 350; c = 100 gives 100/3 and c = 1 gives 74.5 (recomputed, numbers_L03_r9.out). Not fair because stop-at-once mean 350 != 0."),
"PC3a-L03-lab-docstring-two-methods": ("PASS", "tests/labs/PC3/lab-PC3-L03-1.py docstring (lines 121-124): Part 2 two ways, Part 3 two methods that must agree, Part 3b recursion alone (part_three lines 232-246 do exactly that). L03.html:114 hypothesis matches."),
"PC3a-L03-why-rhetorical-questions": ("PASS", "L01.html:51, L02.html:51, L03.html:51: no question marks inside the why-it-matters paragraph; word counts 119, 117 and 120 (at most 120 words)."),
"PC3a-L03-numbers-prose-claims": ("PASS", "L03.html:104 (383.33, 33.33), 322 (25 per turn, 150, 1575/32, 575/8, 625/8), 336 (100/3), 349 (gain 100/3). All recomputed."),
"PC3a-L03-quiz": ("PASS", "L03.html:480-564: 12 items; answers 350, 0.333333, 383.333333, 250, faces 1-2, 50, 150, 7 re-derived; each item has an explanation consistent with the lesson."),
"PC3a-L03-lab-match": ("PASS", f"lab_twin_match_r9.py ({O}lab_twin_match_r9.out): L03 page code equals tests/labs/PC3/lab-PC3-L03-1.py; expected block (30 lines) equals stdout."),
"PC3a-L03-canon-breaks": ("PASS", "L03.html:330-337: unbounded stopping named as outside Theorem 3.8 (Remark 3.9 consistent); fairness as hypothesis (Example 3.10 values confirmed); choice worth 100/3 in a non-fair game."),
"PC3a-L03-fair-game-before-definition": ("PASS", "L03.html:51 uses 'Definition 3.7' and 'Definition 3.5' by number before they appear; the terms are defined at L03.html:91-92 (fair game, history) and 108-110 (stopping rule) before any lab use at line 112."),
"PC3a-why-terms-before-definition": ("PASS", "L01.html:51-58: 'Fermi estimate' defined at line 59 (dfn), used in the meta line 38 (link to the definition); L02.html:38, 51 and L03.html:51, 91-92: terms named in the introductions are defined later or referenced by number."),
"PC3a-L03-numbers-key-rows-lab": ("PASS", "L03.html:471, 474, 475: lab-printed rows match outputs (best of 64 policies 1150/3; biased values 1575/32, 575/8, 625/8; E[X+Y] = 7)."),
"PC3a-notation": ("PASS", "Macros used in the slice: \\E, \\Prob, \\R, \\indic (registered in notation/notation.json), plus standard TeX (\\binom, \\omega, \\Omega, \\cdot). No use of registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f or \\mathbb{Q}. Local letters (N, t, h, W, V, L, U, P, Q) are used lesson-locally and are not registered. Notation check PASS."),
"PC3a-dag-prose-only-terms": ("PASS", "index.html:148 'adverse selection in plain words' (plain prose, no link, no dfn, D3); L02.html:275, 277, 557 'posterior' in lab code and a quiz explanation only (plain word, not a linked concept; D1); L03 uses 'backward induction' in prose (Example 3.6). No concept outside the closure is linked or defined."),
"PC3a-canon-misconceptions-problems-counts": ("PASS", "Misconceptions: L01 3 (L01.html:326-336), L02 3 (376-386), L03 3 (343-353). Problems: L01 13, L02 12, L03 12 (each tier has at least three problems; L01 Empirical has four)."),
"PC3a-hours-declared": ("PASS", "L01.html:2 data-hours=6 and 34 '6 study hours'; L02.html:2 and 34; L03.html:2 and 34. Sum 36 with index.html:29."),
"PC3a-r4-delta-read": ("PASS", "Round-9 delta read in full for the slice: git diff 0dee921a c93dd52 -- course/modules/PC/PC3 tests/labs/PC3 shows L02.html (one paragraph line, line 134) as the only change in index/L01/L02/L03 and the labs L01-L03 (labs and index/L01/L03 byte-identical). The other delta files (L04, L05, L06, cards.json, project.html, grader, labs L04/L05) are outside this slice. Global delta read: course/concepts.html line 139 (M3 wording) and curriculum/01-foundations.yaml, curriculum.json (M3 wording) do not touch PC3 concepts."),
"PC3a-r4-cross-references": ("PASS", f"xref_r9.py ({O}xref_r9.out): every Definition, Assumption, Proposition, Theorem, Example and Remark mentioned in L01, L02 and L03 is defined in that lesson; the only other-lesson mention is 'Lesson 2, Definition 2.2' in L03 (explicitly labelled)."),
"PC3a-r4-recompute-all-numbers": ("FAIL", f"Recomputation ({S}numbers_L01_r9.py, numbers_L03_r9.py, outputs in {O}) matches every number in the slice except the display claim at L01.html:408 ('would display as 30.9 percent'), which is incorrect; see PC3a-L01-E2-shares. Fix: as stated in that row."),
"PC3a-r4-restated-M4-concepts": ("PASS", "L02.html:57 (M4 Lesson 1 link), 67 (conditional probability linked to conditional-expectation-elementary, defined at course/modules/M/M4/L04.html:139), L03.html:62 (expectation linked to concepts.html#expectation). None is redefined."),
"PC3a-r4-observations-no-row": ("PASS", "L01.html:433 (criterion arithmetic) and tests/labs/PC3/lab-PC3-L02-1.py (drill set has no per-row observations); no observation claim lacks a computation."),
"PC3a-L03-misconception-most-likely": ("PASS", "L03.html:352-353: 'a fair game with expected payoff zero never pays a gain' corrected by Example 3.11 (a +100 outcome with probability 1/2)."),
"PC3a-L03-def35-next-turn": ("PASS", "L03.html:92 (Def 3.5 fairness of the next turn given the history), 293 (A3 for histories of positive probability), 300 (H2)."),
"PC3a-banned-and-process-words": ("PASS", "grep (case-insensitive) over index/L01/L02/L03 for banned strings (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly) and process words (build, builder, verifier, round, REQUESTS, unit report): 0 hits in prose. Three-dot ellipses occur only in lab code (L01 lines 169, 185, 202; L02 284-286; L03 134-223), allowed outside prose."),
"PC3a-r6-hub-ladder-rung2-wording": ("PASS", "index.html:159 'each of the two lines replaced by ___ ... Graded instantly': project.html:45 and 253 ('blanked with ___'), 349-350 (cash_flow and mark lines = ___) and the rung-2 description agree."),
"PC3a-r6-hub-project-file-names": ("PASS", "index.html:160 and 167 name market_maker.py with quote(state) and replay(log); project.html:386-400 (Required outputs) names market_maker.py, quote and replay. Consistent."),
"PC3a-r6-hours-curriculum-attribution": ("PASS", "index.html:167 hours statement; curriculum/06-profession-capstone.yaml:160 'Hours 50' and the module total 36 + 14 = 50 (computed)."),
"PC3a-r6-def21-m4-weights-positivity": ("PASS", "L02.html:57 (Definition 2.1, weights > 0) and L03.html:57 (A1, weights > 0) match course/modules/M/M4/L01.html:55 (weights p(omega) > 0 summing to 1)."),
"PC3a-r7-hub-skill-check-bid-ask": ("PASS", "index.html:129 (bid 10 005 cents, buy, cash flow -10005) and 131 (explanation -10 005 cents). index.html:133-136 (inventory +1, settlement 10040, mark 10040). Consistent with the convention that a maker's buy pays the bid (project.html conventions)."),
"PC3a-r7-hub-hours-line-items": ("PASS", "index.html:167 (1, 1, 3, 2, 2, 4, 1 = 14). course/modules/PC/PC3/project.html:422-435 time budget table lists the same seven lines and total 14. The project diff since round 8 changed lines 34, 386-400, 620-630 and 683 only; the table is unchanged."),
"PC3a-r7-hub-autograder-seeds": ("PASS", "index.html:55 (objective 7: seeds 0 to 49 and workspace seed) and 160 (seeds 0-49, own seed, seed plus 7919) match project.html:397 ('Nine checks run on each distinct seed of the set, which holds the fixed seeds 0 to 49, your seed and your seed plus 7919')."),
"PC3a-r7-L02-timed-drill-budget": ("PASS", "L02.html:134 states a per-item budget of 60 seconds kept on the student's clock with no timer on the page, and that the lab does not measure time; the twin has no timer (tests/labs/PC3/lab-PC3-L02-1.py has no time import). L02.html:359 interpretation consistent. Architect default B2 (plan §0.3, §12 Q2) followed."),
}
rows = []
for r in prev["rows"]:
    status, evidence = ev[r["id"]][0], ev[r["id"]][1]
    row = {"id": r["id"], "check": r["check"], "location": r["location"], "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = "Replace the sentence at course/modules/PC/PC3/L01.html:408 with: 'Dividing those four-place values gives 0.308477, which is 30.85 percent to two places and 30.8 percent to one place, so the solution divides the full-precision values instead.' Delete the claim that the four-place route displays as 30.9 percent (it does not: the single-rounding display is 30.8)."
    rows.append(row)
extra_fix = rows
ids = [r["id"] for r in rows]
assert ids == [r["id"] for r in prev["rows"]], "row ids must be kept"
assert set(ev) == set(ids), set(ev) ^ set(ids)
npass = sum(r["status"] == "PASS" for r in rows)
nfail = sum(r["status"] == "FAIL" for r in rows)
frag = {
  "unit": "PC3", "slice": "PC3-a", "round": 9,
  "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 9 (did not build PC3; no shared context with the builders)",
  "pin": "c93dd526025c6dffd34c54cd2c89eb62a890f885 (detached)",
  "base": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3 (the round-8 pin)",
  "checkout": ROOT,
  "scratch": "none outside the checkout: every script and output is under ledgers/PC3/scripts/PC3-a-r9/ (outputs/ subfolder)",
  "verified_at": "2026-11-05T02:30:00+00:00",
  "verdict": "FAIL",
  "scope": prev["scope"],
  "rows": rows,
  "mutants": [],
  "registry_flags": prev["registry_flags"],
  "freshness_flags": prev["freshness_flags"],
  "notes": [
    "Delta since round 8 for the slice: course/modules/PC/PC3/L02.html line 134 (one paragraph, the spacing sentences). index.html, L01.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py are byte-identical to the round-8 pin. Because L01 was re-read in full this round, every L01 row is re-verified (not carried), and the round-8 row PC3a-L01-E2-shares was found to be wrong.",
    "Round-8 FAIL PC3a-L02-spaced-repetition is PASS now: the page states that the drill set has no spacing of its own and that the lesson's cards (added to the FSRS-4.5 review deck when the quiz is finished) carry the spacing. Architect note: the curriculum wording 'with spaced repetition' is met through the cards, not the drill items; the architect should confirm this reading.",
    "Mutation testing is not applicable: the slice has no grader; the ruling says lab twins are demonstrations. mutants is empty.",
    "Not checked in this slice: cards.json (its 24 L01, 23 L02 and 29 L03 cards were not scanned against the lesson text this round; the L01-L03 quiz items are checked, but not the cards), L04-L06, project.html, grader/, the project labs. verify_refs live run not repeated (offline gate only). The 2025-2026 freshness scan does not apply because PC3 cites only two books at book level.",
    "Registry (not a PC3 page defect, not edited by this verifier): crack2015heard publisher string '[Timothy Falcon Crack]' and zhou2008practical publisher 'Lulu,]' carry stray brackets (references/references.json; plan B4). Registry owners should correct them.",
    "Summary of this round: two FAIL rows for one defect (PC3a-L01-E2-shares and its recompute row PC3a-r4-recompute-all-numbers), 74 PASS rows. Round-8 PASS rows were re-verified where their subjects were read this round; none was carried on trust."
  ],
  "summary": {
    "rows": len(rows), "pass": npass, "fail": nfail, "unverifiable": 0, "mutants_killed": 0, "mutants_total": 0,
    "recompute": "numbers_L01_r9.py and numbers_L03_r9.py: every value recomputed by script matches the page except the 30.9 display claim at L01.html:408"
  }
}
out = "ledgers/PC3/PC3-a.json"
import os
os.makedirs("ledgers/PC3", exist_ok=True)
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, "rows", len(rows), "pass", npass, "fail", nfail)
