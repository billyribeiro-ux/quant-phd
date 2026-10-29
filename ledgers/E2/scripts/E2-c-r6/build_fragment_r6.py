import json
S='ledgers/E2/scripts/E2-c-r6/out/'
rows=[]
def R(id,check,loc,status,ev,fix=None):
    r={'id':id,'check':check,'location':loc,'status':status,'evidence':ev}
    if status!='PASS': r['fix']=fix
    rows.append(r)
# gates
R('E2c-gate-check-pages','2.9 structure (check_pages)','course/modules/E/E2/L07.html, L08.html, L09.html','PASS',
  'Ran tools/check_pages.py --unit E2 --page L07/L08/L09 on pin 9fd6aed: "check_pages E2 L07: PASS", same for L08 and L09, exit 0 (%scheck_pages_L07.out, _L08.out, _L09.out).'%S)
R('E2c-gate-check-dag','2.9 DAG (check_dag)','course/modules/E/E2/L07-L09.html','PASS',
  'tools/check_dag.py --unit E2 exit 0, "check_dag E2: PASS" (%scheck_dag.out). Forward-reference and link scan in E2c-dag-outside-closure.'%S)
R('E2c-gate-run-labs','2.5 labs (run_labs)','tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py','PASS',
  'tools/run_labs.py --unit E2 --page L07/L08/L09 each exit 0, "run_labs E2: PASS (1/1)" (%srun_labs_L07.out, _L08.out, _L09.out).'%S)
R('E2c-gate-page-smoke','2.9 page_smoke (run alone)','course/modules/E/E2/L07.html, L08.html, L09.html','PASS',
  'tools/page_smoke.py --unit E2 --pages L0x one page at a time, each exit 0, "page_smoke E2: PASS", lab timings 0.0 to 0.2 s (%spage_smoke_L07.out, _L08.out, _L09.out).'%S)
R('E2c-twins-isolated','2.5 twins under python -I -W error','tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py','PASS',
  '.venv/bin/python -I -W error on each twin: exit 0, stderr 0 bytes (%stwin_L07/L08/L09.stdout and .stderr). grep for __main__ guard: 0 matches in each twin. git diff --quiet 04626e9 9fd6aed on the three twins: unchanged.'%S)
R('E2c-page-code-equals-twin','2.5 page code equals twin','L07.html, L08.html, L09.html data-run / pre code','PASS',
  'ledgers/E2/scripts/E2-c-r6/compare_r6.py: after html.unescape and tag strip, the single code block of each page equals the twin file (strip-equal) for L07, L08, L09 (%scompare_r6.out).'%S)
R('E2c-expected-equals-output','2.5 expected block equals output','L07.html pre.expected, L08.html, L09.html','PASS',
  'compare_r6.py: unescaped pre.expected equals the twin stdout (strip-equal) for L07 (37 lines), L08 (14), L09 (20) (%scompare_r6.out).'%S)
R('E2c-ruff-mypy-pytest','gates (ruff, mypy, pytest)','tests/labs/E2/*.py; tests/test_labs.py','PASS',
  'ruff check tests/labs/E2 exit 0 ("All checks passed!"); ruff format --check 12 files already formatted; mypy --no-incremental on the three twins: "Success: no issues found in 3 source files"; pytest tests/test_labs.py -k E2 -q exit 0 (%sruff_check.out, ruff_format.out, mypy.out, pytest_labs_E2.out).'%S)
R('E2c-verify-refs-offline','2.1 registry integrity (verify_refs --offline and --unit E2)','references/references.json','PASS',
  'tools/verify_refs.py --offline: "offline integrity: 560 entries, 0 problems" exit 0 (%sverify_refs_offline.out). tools/verify_refs.py --unit E2 (live, plain HTTP): "live re-verification of E2: 8 of 560 entries, 0 problems", exit 0 (%sverify_refs_unit_E2_online.out).'%(S,S))
# numbers
R('E2c-l07-numbers','2.2 numbers L07','L07.html Example 3.3, Part B grid, M2, M3, R3, key results, quiz','PASS',
  'Re-derived by hand and in %srecompute_r6_l09_l07.py (exact Fractions, independent grid and menu checks): c = 0.3*6000-0.7*4000 = -1000; optimum 7000 (q_L=0,q_H=1); pooling 6000; exclusion 7000; induced low-price tie-break 6000; decline tie-break 4200; grid 15 of 15 pass, 15 pairs with q_L<=q_H; M2 c=1000, revenue 6000; M3 6500; R3 c=6000-10000p_H, c=0 at p_H=3/5. Twin stdout %stwin_L07.stdout matches the prose (all Part A/B/C figures).'%(S,S))
R('E2c-l08-numbers','2.2 numbers L08','L08.html Example 2.4, Remarks 2.3 and 3.2, Part B/C interpretation, E1-E3, R1, R3, key results','PASS',
  '%srecompute_r6.py (exact Fractions): E[M](5,2000)=85418692002000/64048012001 = 1333.6665625260 (equal to the page fraction, True); E[M](2,1)=4/9 by formula and by enumeration; E[M](3,1)=2/3; cont. 4000/3; difference 0.3332292; 1334-E[M]=0.3334375 per auction; 1333-E[M]=-0.6665625 (-0.67); -20000*E[M] = -26673331.25 -> -26673331; 20000*(1334-E[M]) = 6668.749 -> 6669; 52613/79810 = 0.66 SE; 79810/20000 = 3.99; 228/256 = 0.890625.'%S)
R('E2c-l09-numbers','2.2 numbers L09','L09.html Part A/B/C, E1-E3, R1, M1-M3, Remark 3.3','PASS',
  '%srecompute_r6_l09_l07.py (independent code, not the lab): order [1,0,3,2]; winners 0,1; clearing 7000; uniform 14000; discriminatory 17500; gap 3500 = 25%% of 14000; efficiency 14000/16000 = 7/8; k=2 over 256 profiles: 228 above, 28 equal, 0 below; equal set == profiles with top three bids equal (28); k=1 identity 256 of 256; M2 12000 vs 15000; Remark 3.3 efficiency 7/8.'%S)
R('E2c-l08-simulation-reproduction','2.5 lab / SIMULATED','tests/labs/E2/lab-E2-L08-1.py (seed 20261028)','PASS',
  'Independent re-implementation %ssim_l08_r6.py (random.Random(20261028), same draw order): naive total -26620718, shaded total 59282, SE 79809.92 (prints 79810), difference from exact 52613.25 = 0.659 SE, shaded-naive 26680000 = 1334*20000; matches the lab and the page.'%S)
# prose / math
R('E2c-l07-prop2.2','2.4 mathematics','L07.html Assumption 3, Definition 2.1, Proposition 2.2 and proof (lines 36-44 of the text dump)','PASS',
  'Read in full (%sout/L07.txt). Proof: type theta under x-hat gets x(s(theta)); equilibrium inequality for message s(theta\') gives the truthful-report inequality; outcome distribution unchanged. Complete for the stated one-agent finite setting.'%'ledgers/E2/scripts/E2-c-r6/')
R('E2c-l07-lemma3.1','2.4 mathematics','L07.html Assumption 4, Lemma 3.1 and proof','PASS',
  'Re-derived: U_H >= v_H q_L - tau_L = U_L + Delta q_L; U_L >= v_L q_H - tau_H = U_H - Delta q_H; U_H >= 0 follows from U_L>=0; both bounds give q_L<=q_H since Delta>0; converse holds.')
R('E2c-l07-prop3.2','2.4 mathematics','L07.html Proposition 3.2 statement (line 140), proof (line 153), key-results row 3','PASS',
  'Re-derived: R = p_H v_H q_H + c q_L - U_L with c = p_L v_L - p_H Delta; maximize over U_L=0 and q_H=1; f linear in q_L with endpoints p_H v_H and v_L; c<0, c>0, c=0 cases checked. Statement hypotheses v_H>0 and Delta>0 are both used (v_H>0 for monotonicity in q_H).')
R('E2c-l07-prop3.2-hypothesis','2.4 mathematics','L07.html Proposition 3.2 (line 140) and key-results row (line 488)','PASS',
  'Statement and key-results row both state v_H > 0; the proof uses p_H v_H > 0 (monotone in q_H). Consistent.')
R('E2c-l07-prop-3.1-example','2.2 numbers / examples','L07.html Example 3.3','PASS',
  'c = 1800-2800 = -1000; optimum tau_H = 10000, revenue 7000; pooling 6000; exclusion described correctly; Part A/B printout as stated.')
R('E2c-l07-remark2.4-signaling','2.4 prose claims about L04, L05','L07.html Remark 2.4; L04.html; L05.html','PASS',
  'L05 text: "In this lesson the menu has two items, one for each type" (screening, consistent with Remark 2.4). L04 text: firm "sees the signal ... and sets a wage that depends on the signal" (consistent with "the firm sets the wage after it sees that action"). Text dumps in %sout/L04.txt, L05.txt.'%S)
R('E2c-l07-quiz-items','2.9 quiz','L07.html quiz L07q1-L07q9 (section 8)','PASS',
  'Each answer checked against Definition 1.2, Example 3.3, Lab 1 Part A/B/C, Proposition 3.2, Problems M2, R1, R3, P3. All keyed answers correct; distractors wrong (e.g., "Sell to both types at 10000" fails IR).')
R('E2c-l07-problem-set','2.9 problem set','L07.html Problems M1-M3, P1-P3, E1-E3, R1-R3','PASS',
  'Each worked solution re-derived: M1 4000; M2 c=1000, q=(1,1), tau=(6000,6000), revenue 6000 vs exclusion 5000; M3 6500; P1 (sum of IC gives (v_H-v_L)(q_H-q_L)>=0); P2; P3 U_H=0; E1 nine... 15 pass; E2 menus; E3 gap 1000; R1 induced menu IC/IR revenue 4200; R2 Delta>0 step; R3 threshold 3/5.')
R('E2c-l07-key-results','2.4 mathematics and grades','L07.html key-results rows (lines 484-490)','PASS',
  'Each row grade T matches its derivation (Prop 2.2 T, Lemma 3.1 T, Prop 3.2 T, R3 T, Lab 1 grid T for the menu values); no row claims an empirical result.')
R('E2c-l07-misconceptions','2.9 prose, claims','L07.html section 5 items 1-3','PASS',
  'Each misconception checked against Example 3.3, Lab 1 Parts A-C and Lemma 3.1; the 1333/1334 style claims are absent from L07. No overreach found.')
R('E2c-l07-notation-xstar','2.4 notation','L07.html all symbols','PASS',
  'Symbols used: theta, Theta, p_theta, v, tau, q, U, Delta, c, R, M (message set), X, x, s, x-hat. None is a registered symbol with another meaning (notation.json registers T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q only; no \\N for counts; \\E and \\Prob used via macros). Checked by grep of the math source.')
R('E2c-dag-outside-closure','2.9 DAG (use outside closure)','course/modules/E/E2/L07.html:92','PASS',
  'grep of L07-L09 for lagrange, kkt, convex, principle of optimality, expected utility, risk-averse, arrow, bayes, welfare, risk-neutral, principal: only the prose phrase "Bayesian-Nash condition of L02" (in closure via L02) and "risk neutral" (plain prose, as the plan requires). No link to an out-of-closure concept.')
R('E2c-banned-and-process-words','2.9 banned phrases and process words','L07.html, L08.html, L09.html; cards.json; tests/labs/E2/lab-E2-L07/08/09-1.py','PASS',
  'grep (case-insensitive) for builder, verifier, round, requests, unit report, TODO, TBD, clearly, obviously, well known, studies show, experts agree, important to note, beyond the scope, left as an exercise and the three-dot ellipsis: no hit in the pages or cards (the only "round" hits are "Lab 1 ... rounded" in the twins, which is the word for rounding).')
R('E2c-notation-registry','2.4 notation','L07.html, L08.html, L09.html','PASS',
  'Math sources contain only \\\\theta, \\\\Delta, \\\\tau, \\\\E, \\\\Prob, \\\\indic, \\\\varepsilon, \\\\max, \\\\sum, \\\\prod, \\\\dots (no \\\\N, \\\\Normal, \\\\Phi, \\\\gamma, \\\\R, hand-written E or P). The only "P(" is inside a lab docstring (code, not prose). L09 R1 renamed the bid level to w (the value symbol v_i is reserved for values).')
R('E2c-attributions','2.1 attribution','L08.html section 9 (the two registry titles); L07.html section 9; L09.html section 10','PASS',
  'L08 §9 names "COUNTERSPECULATION, AUCTIONS, AND COMPETITIVE SEALED TENDERS" (1961) and "A Theory of Auctions and Competitive Bidding" (1982): both match references/references.json title and print_year for vickrey1961counterspeculati and milgrom1982theory, and the page attributes no result to either. L07 and L09 cite no source. No locator, page or number is attributed to any paper. Live check: verify_refs --unit E2, 0 problems.')
R('E2c-hours','2.9 hours arithmetic','L07.html, L08.html, L09.html data-hours and header','PASS',
  'Each lesson header and data-hours = 10 (grep); within the 6-12 rule of check_pages; the hub split is not in this slice (slice d).')
R('E2c-lab-claims-match-output','2.5 lab claims vs output','L07 interpretation (Lab 1 Part A/B/C paragraph, section 3 end); L08 SIMULATED output paragraph; L09 Part A/B/C paragraph','PASS',
  'Each printed figure in the interpretation paragraphs equals the twin stdout (compare_r6.py and twin_L0x.stdout): L07 Part A four menus, grid 15, best 7000, induced 6000 and 4200; L08 -26620718, -26673331, 59282, 6669, 79810, 4/9; L09 14000/17500/7/8/228/28/0/256 of 256. Each claim the page makes that the lab does not print (e.g., L07 "not a proof of the optimum") is hedged.')
R('E2c-lab-docstring-claims','2.5 docstrings','tests/labs/E2/lab-E2-L07-1.py, L08-1.py, L09-1.py docstrings','PASS',
  'L07 docstring: Parts A/B/C described match code (four menus; grid steps 1/4; tie-break order low-price first). L08 docstring: SIMULATED labelled; half-width 2000; value 5000-15000; ties to lower index; standard error printed. L09 docstring: 4 bidders, 2 units, 256 profiles, efficiency undefined when sum not positive, not evaluated. All consistent with the code.')
R('E2c-html-structure','2.9 structure','L07.html, L08.html, L09.html','PASS',
  'check_pages PASS for each page (E2c-gate-check-pages); section order: header, Definitions, Propositions with Assumptions, Lab, Misconceptions, Problem set (M/P/E/R), Key results, Quiz, References, complete button, prev/next. Verified in text dumps.')
R('E2c-delta-r5-hunks','2.9 delta (round-5 hunks, re-read)','L07.html lines 49, 89, 92, 137, 367, 485; L08.html lines 52, 75; L09.html line 52','PASS',
  'Round 6 re-read every hunk of 04626e9..9fd6aed in the slice (L08.html two hunks, L09.html two hunks, cards.json five hunks). The round-5 hunk lines are byte-identical at 04626e9 and 9fd6aed (L07.html has no hunk in the delta), and each was re-verified as text in %sout/L07.txt, L08.txt, L09.txt.'%S)
R('E2c-delta-r6-hunks','2.9 delta (round-6 hunks)','L08.html lines 57, 289; L09.html lines 243, 397; cards.json E2-c083, c098, c100, c104, c105','PASS',
  'L08 line 57 (Assumption 1 "in cents ... The number a is called the half-width"): consistent with Assumption 1 and the code HALF_WIDTH. L08 line 289 ("The loss in one auction is M cents, and the expected loss is E[M] > 0 cents"): signed reading, consistent with Proposition 2.1 (profit -M); not a finding. L09 line 243 (Part A interpretation "bidder 3 ... is the first loser, so its bid is the clearing bid"): consistent with ranking 1,0,3,2. L09 line 397 (R1 renamed to w): consistent with its solution (4w+1). Card hunks: see the card rows.')
R('E2c-define-before-use-forward-ref','2.9 define-before-use','L09.html why-it-matters (line 52), lab hypothesis (line 94)','PASS',
  'Forward pointers to Definition 3.1 (allocative efficiency) in the L09 why-it-matters and lab text are labelled as forward references ("as Definition 3.1 states"); allocative efficiency is not one of the 12 registered concepts, so no dfn is required. Concepts used earlier: bid-shading (L08), nash-equilibrium (L01) linked.')
R('E2c-l08-prop2.1','2.4 mathematics','L08.html Proposition 2.1 (lines 88-95 of the HTML; text lines 36-40)','PASS',
  'Re-derived: profit = -M in every realization (ties included); E[M] >= E[eps_1] = 0; strict via P(eps_2=a, eps_1=-a)=(2a+1)^-2 and a>=1; checked numerically for n=2, a=1 (4/9>0).')
R('E2c-l08-prop2.2','2.4 mathematics','L08.html Proposition 2.2 and proof (text lines 41-47)','PASS',
  'Re-derived: M+a = sum_{x=-a}^{a-1} 1{M>x}; formula checked against enumeration for n=2,a=1 (4/9), n=2,a=2 (4/5), n=3,a=2 (6/5) via %srecompute_r6.py.'%S)
R('E2c-l08-remark2.3-grade','2.3 grades','L08.html Remark 2.3 (text line 49), key results','PASS',
  'Remark 2.3 states 4000/3 (T, derivation) and the discrete value (T, basis Prop 2.2) consistent with key-results rows 234 and 235 (both T). Card E2-c098 disagrees: see E2c-cards-l08-c091-c100.')
R('E2c-l08-continuous-analogue','2.2 numbers','L08.html Remark 2.3','PASS',
  'a(n-1)/(n+1) = 4000/3 = 1333.33 for n=5, a=2000; difference from discrete 0.3332292 (0.3332); rounded figures differ by 0.34: all recomputed in %srecompute_r6.out.'%S)
R('E2c-l08-remark3.2','2.2 numbers and derivation','L08.html Remark 3.2 (text line 58)','PASS',
  'Smallest whole-cent shading with c >= E[M] = 1333.6666 is 1334; 1333-E[M] = -0.66656 -> -0.67; lab Part C uses shade = half-up(E[M]) = 1334. Remark carries no grade; its numbers follow from Proposition 3.1 (T) and the T value.')
R('E2c-l08-quiz-items','2.9 quiz','L08.html quiz L08q1-L08q9 (section 8)','PASS',
  'Answers checked: largest signal wins; -4/9; strictly positive; 1334; 4000/3 = 1333.33 (differs by 0.3332); 2/3; 1333 gives -0.67; winner profit -250 with V=9000, M=250. Distractor "Yes, any positive shading does" is wrong per Remark 3.2.')
R('E2c-l08-problem-set','2.9 problem set','L08.html Problems M1-M3, P1-P3, E1-E3, R1-R3','PASS',
  'Solutions re-derived: M1 -4/9; M2 2/3 (27ths); M3 5/9 and 1 cent suffices; P1 ties; P2; P3 E[M]>0 needs a>=1; E1 52613/79810 = 0.66; E2 26680000; E3 0.33343747 and 6668.749 -> 6669; R1 1/3 vs 4/9, diff 1/9; R2; R3 {1334,...}. All numbers match the exact recomputation.')
R('E2c-l09-prop2.1','2.4 mathematics','L09.html Definition 1.1-1.2, Proposition 2.1 and proof (text lines 26-35)','PASS',
  'Re-derived: sum of k inequalities b_(j) >= b_(k+1); equality iff every term 0, i.e., top k+1 bids equal; ranking complete by index tie-break; exactly k winners since k<n. Checked by exhaustive enumeration of 256 profiles in %srecompute_r6_l09_l07.py.'%S)
R('E2c-l09-prop3.2-prop4.1','2.4 mathematics','L09.html Definition 3.1 (line 251 of HTML), Proposition 3.2 (line 256), Proposition 4.1 (line 273)','PASS',
  'Definition 3.1 undefined for nonpositive second entry stated; Proposition 3.2 proof uses ranking by value and P3; Proposition 4.1 follows from Definition 1.1 with k=1; checked on 256 profiles (k=1 identity 256 of 256).')
R('E2c-l09-grades','2.3 grades','L09.html key-results rows (lines ~423-427 of HTML; section 8 table)','PASS',
  'Row 247 T (Prop 2.1), row 248 T (Prop 3.2), row 249 T (Prop 4.1), row 250 C with basis (Lab 1 Part B exhaustive enumeration), row 251 T with base stated: each grade matches its derivation or enumeration.')
R('E2c-l09-quiz-items','2.9 quiz','L09.html quiz L09q1-L09q9 (section 9)','PASS',
  'Answers checked: clearing bid second-highest; discriminatory revenue >= uniform; 14000; 17500; second-highest; 7/8; efficiency 1; 228; Remark 2.2 (no). Each keyed answer correct.')
R('E2c-l09-problem-set','2.9 problem set','L09.html Problems M1-M3, P1-P3, E1-E3, R1-R3','PASS',
  'M1 ranking 1,3,2,0, clearing 6000; M2 12000 vs 15000, diff 3000; M3 winner pays 7000 vs 8000; E1 14000/16000 = 7/8 = 0.875; E2 228/256 = 0.890625 = 89.06%; E3 3500/14000 = 25%; R1 4w+1 summed = 28 (w renamed from v); R2 multi-unit equilibrium needs strategies; R3 Prop 4.1 proof. All verified.')
R('E2c-l09-why-it-matters','2.9 prose','L09.html line 52 (why-it-matters)','PASS',
  'Paragraph states the fixed-bid comparison, the 256-profile enumeration and the one fixed profile for efficiency; each claim matches Lab 1 output. "Lab 1 checks the revenue ranking" is an exhaustive count printed by Part B (no assertion), which is the only check the lab performs; accepted as the same claim.')
R('E2c-l08-why-it-matters-def1.2','2.9 prose','L08.html line 52 and line 75 (why-it-matters, Definition 1.2 wording)','PASS',
  'Why-it-matters states the simulation is SIMULATED and makes no claim about real bidders; Definition 1.2 wording matches Proposition 2.1 and §2.')
# cards
R('E2c-cards-l07-c076-c085','2.7 cards (full scan of L07 cards c076-c085)','course/modules/E/E2/cards.json E2-c076 to E2-c085','PASS',
  'All ten cards read against L07 text: definitions (c076-c079) match Definitions 1.1-1.2; c080 matches Definition 2.1 and Proposition 2.2 (no grade field on a theorem card, noted); c081 matches Proposition 2.2; c082 matches Lemma 3.1 with its hypotheses; c083 now carries v_H > 0 (the round-5 defect is fixed) and matches Proposition 3.2 statement; c084 matches Example 3.3; c085 matches Problem R3 (threshold 3/5). Grades T agree with Key results rows.')
R('E2c-cards-l07-c086-c090','2.7 cards (L07 c086-c090)','cards.json E2-c086 to E2-c090','PASS',
  'c086 grade C with basis Lab 1 Part B (15 pairs); c087 grade C with basis Lab 1 Part C (6000 vs 4200); c088 matches Example 3.3 and Lemma 3.1; c089 matches Lab 1 Part A (-4000 IR failure); c090 grade C with basis Lab 1 Part C. Grades agree with the lesson (lab observations are C with basis).')
R('E2c-cards-l08-c091-c100','2.7 cards (L08 c091-c100)','cards.json E2-c098 (grade "C", basis "Lab 1, Part B ...") and E2-c100 (grade "C")','FAIL',
  'Grade mismatch. E2-c098 (1333.67 cents = 85418692002000/64048012001) is graded C, but L08.html Key results row 235 grades that value T ("Proposition 2.2 evaluated exactly with fractions") and Remark 2.3 says "grade T". E2-c100 (1334 is the smallest whole-cent shading; 1333 leaves -0.67) is graded C with basis "Lab 1, Part B", but it follows from Proposition 3.1 (T, Key results row 233) and the T value, and Lab 1 Part B prints only the total -26673331 cents, not the per-auction -0.67. Wording of c091-c097, c099 matches the lesson.',
  'Set cards.json E2-c098 and E2-c100 "grade" to "T" and drop their "basis" fields (the figures are derived on the page), or, if the lesson is to grade them C, change L08.html Key results row 235 and Remark 2.3 to C with a basis and then make the cards agree. Re-run tools/check_pages.py --unit E2 --page L08.')
R('E2c-cards-l08-c101-c103-c106','2.7 cards (L08 c101, c102, c103, c106)','cards.json E2-c101, c102, c103, c106','PASS',
  'c101 and c102: SIMULATED, grade C with basis Lab 1 Parts B/C; totals -26620718, 59282, exact -26673331 and 6669, difference 52613 = 0.66 SE of 79810; 26680000 = 1334*20000; match the printed output and Key results row 236 (C). c103 matches misconception 1 (Proposition 2.1). c106 matches Research problem R2 (T).')
R('E2c-cards-l08-c104','2.7 cards (L08 c104)','cards.json E2-c104','PASS',
  'Round-5 defect fixed: back now says the expected loss is E[M] cents (Proposition 2.1), which matches misconception 2 ("expected loss is E[M] > 0 cents") and Proposition 2.1 (profit -M). Grade T consistent. Not a misstatement of the sign of M per realization.')
R('E2c-cards-l08-c105','2.7 cards (L08 c105)','cards.json E2-c105 (grade "C", basis "Lab 1, Part B ...; Proposition 3.1")','FAIL',
  'Answer now correct ("Not every positive shading"; 1333 leaves -0.67, 1334 nonnegative), but the grade is wrong: it rests on Proposition 3.1 (T, Key results row 233) and the derived -0.67 of Remark 3.2; Lab 1 Part B prints only the total, not the per-auction -0.67. Lesson misconception 3 (L08.html section 5) states the same numbers ungraded from Remark 3.2. The card also duplicates the 1333/1334 fact of E2-c100 (not an identical card).',
  'Set cards.json E2-c105 "grade" to "T" and remove its "basis" field, so the card agrees with Proposition 3.1 and Remark 3.2 (T); or change the lesson and the card together to C with a stated basis.')
R('E2c-cards-l09-c107-c121','2.7 cards (L09 c107-c121)','cards.json E2-c107 to E2-c121; in particular E2-c120','FAIL',
  'E2-c120 back reads "For a common top value v, the count is 4v + 1". L09.html R1 (section 7 Research problem R1, solution text) has been renamed to w: "b(1)=b(2)=b(3)=w ... the count for w is 4w + 1". The symbol v is the bidder value v_i in L09 §1 and §3, so the card no longer agrees with the current lesson text and uses a symbol the lesson reserves for values. Other L09 cards (c107-c119, c121) match Definition 1.1-1.2, Proposition 2.1, 3.2, 4.1, Definition 3.1, Remark 2.2, Lab 1 Parts A/C and Problem P3.',
  'In cards.json E2-c120 "back", replace "a common top value v" with "a common top bid w" and "4v + 1" with "4w + 1" (keep "0 to 3" and "1 + 5 + 9 + 13 = 28").')
R('E2c-cards-duplicates','2.7 cards (duplicate scan)','course/modules/E/E2/cards.json (123 cards; L07-L09 = c076-c121)','PASS',
  'Python scan (%sout/cards_L07_09.txt): no duplicate ids; no duplicate fronts; no two backs identical. E2-c100 and E2-c105 test the same 1333/1334 fact with different questions: noted, not a duplicate.'%S)
R('E2c-cards-grades','2.3 grades (card vs lesson)','cards.json E2-c076 to E2-c121','FAIL',
  'Re-graded every card in L07-L09 against the lesson key-results and the derivation. Mismatches: E2-c098 (C vs T), E2-c100 (C vs T), E2-c105 (C vs T). All other graded cards agree: C cards are lab or simulation observations (c086, c087, c090, c101, c102, c118) with a basis, T cards are derivations. Cards without a grade field are definitions or the theorem card c080 (grade not required by BUILDER_RULES §7).',
  'Fix E2-c098, E2-c100 and E2-c105 as in the rows above (grade T, no basis), then re-run tools/check_pages.py --unit E2 --page L08.')
R('E2c-notes-no-row-cards-l07-c080','2.7 cards (theorem card without grade)','cards.json E2-c080','PASS',
  'Theorem-statement card without a grade field; BUILDER_RULES §7 requires a grade only for graded results other than theorems. Noted, not a failure.')
frag={
 'unit':'E2','slice':'E2-c','round':6,
 'verifier':'Claude Haiku 5.5, independent verifier for E2-c round 6 (did not build E2; no context shared with the builders)',
 'pin':'9fd6aedde63046c002ed77af5b5152daf84a3abf',
 'base':'04626e99f75119a75c225f719c603a6e5c7f3e06 (round-5 pin; round-5 fragment /Users/billyribeiro/.fanout/frags/C-E2-c.round5.json used as context only; its PASS rows were not carried)',
 'checkout':'/Users/billyribeiro/.fanout/wt/verifyC6-E2-c',
 'scratch':'/Users/billyribeiro/.fanout/wt/verifyC6-E2-c/ledgers/E2/scripts/E2-c-r6',
 'verified_at':'2026-10-29T05:06:07+00:00',
 'verdict':'FAIL',
 'rows':rows,
 'mutants':[],
 'registry_flags':[],
 'freshness_flags':[],
 'notes':[
  'Lab-only slice (L07-L09 and their twins). Mutation testing applies to project graders only (VERIFIER rulings), so mutants is empty by design; tools/mutate_graders.py was not run for this slice.',
  'Delta 04626e9..9fd6aed inside the slice: L08.html (lines 57, 289), L09.html (lines 243, 397), cards.json (E2-c083, c098, c100, c104, c105). L07.html and the three twins are byte-identical to the previous pin. Files outside the slice in the delta (E2 L01-L06, project, E5/FC1/CF8/M6 labs) were not read beyond confirming they are outside the slice.',
  'Lesson wording nit, not a finding: L08.html misconception 2 says "The loss in one auction is M cents", where M can be negative (for n=2, a=1, M=-1 with probability 1/9). The signed reading matches Proposition 2.1 (profit -M), so it passes.',
  'Card E2-c080 has no grade field (a theorem statement); BUILDER_RULES §7 does not require one. Not counted.',
  'Cards E2-c100 and E2-c105 overlap (both state that 1333 leaves -0.67 and 1334 is the threshold, with different questions). Not identical; the grade fix above resolves the consistency issue.',
  'Not checked by this verifier: the hub and project (slice d); the full pytest suite and repo-wide gates; the unit-wide grader gates; the Pyodide run beyond page_smoke; the rendered figures (the three lessons have no figures, so 2.8 does not apply); visual rendering at 360 px (page_smoke reports PASS, not inspected by eye).',
  'Papers: none of the registry papers was opened. No result is attributed to them (L08 §9 names titles and years only), so VERIFIER §2.1 abstract reading is not triggered for this slice. Live Crossref re-resolution of the 8 E2 keys returned 0 problems.',
  'Previous round fragment row E2c-cards-l07-c076-c085 FAIL (E2-c083) and E2c-cards-l08-c104 FAIL are re-verified: both now PASS. E2c-cards-l08-c105 is still FAIL: its answer is fixed, its grade is not.'
 ],
 'summary':'Slice E2-c (L07-L09, twins, cards) at 9fd6aed, round 6: verdict FAIL. Gates (check_pages, check_dag, check_projects, run_labs, twins under -I -W error, page_smoke, ruff, mypy, pytest test_labs E2, verify_refs offline and online) all PASS; all L07-L09 numbers, proofs and lab outputs re-derived PASS. Four card rows FAIL: E2-c098, E2-c100 and E2-c105 are graded C where the lesson grades the same derived results T (grade mismatch), and E2-c120 uses v where R1 now uses w.'
}
json.dump(frag,open('ledgers/E2/E2-c.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
from collections import Counter
print(Counter(r['status'] for r in rows), len(rows))
