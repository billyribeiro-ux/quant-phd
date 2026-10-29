import json
R = "/Users/billyribeiro/.fanout/wt/verifyC4-FC1-a"
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

CMD = "Run in this checkout at b276325: "
row("cmd-check-pages", "2.9-structure", "course/modules/FC/FC1/ (hub, L01-L03)", "PASS",
    CMD + "tools/check_pages.py --unit FC1 -> 'check_pages FC1: PASS', exit 0 (/tmp/fc1-v/a-r4/check_pages.txt).")
row("cmd-check-dag", "2.9-dag", "course/modules/FC/FC1/", "PASS",
    CMD + "tools/check_dag.py --unit FC1 -> 'check_dag FC1: PASS', exit 0.")
row("cmd-page-smoke", "2.9-smoke", "FC/FC1/index.html, L01.html, L02.html, L03.html", "PASS",
    CMD + "tools/page_smoke.py --unit FC1 --pages FC/FC1/index.html FC/FC1/L01.html FC/FC1/L02.html FC/FC1/L03.html -> 'page_smoke FC1: PASS', exit 0. Unit summary only; per-page detail not printed by the tool.")
row("cmd-run-labs-L01", "2.5-labs", "course/modules/FC/FC1/L01.html lab-FC1-L01-1", "PASS",
    CMD + "tools/run_labs.py --unit FC1 --page L01 -> 'run_labs FC1: PASS (1/1)', exit 0.")
row("cmd-run-labs-L02", "2.5-labs", "course/modules/FC/FC1/L02.html lab-FC1-L02-1", "PASS",
    CMD + "tools/run_labs.py --unit FC1 --page L02 -> 'run_labs FC1: PASS (1/1)', exit 0.")
row("cmd-run-labs-L03", "2.5-labs", "course/modules/FC/FC1/L03.html lab-FC1-L03-1", "PASS",
    CMD + "tools/run_labs.py --unit FC1 --page L03 -> 'run_labs FC1: PASS (1/1)', exit 0.")
row("cmd-twin-alone", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py, lab-FC1-L02-1.py, lab-FC1-L03-1.py", "PASS",
    "ledgers/FC1/scripts/FC1-a-r4/lab_check.py: each twin run alone with python -I -W error: exit 0, empty stderr, identical stdout on two runs; page code block equals twin source (code_eq_twin True) and expected block equals twin output (expected_eq_output True) for L01, L02 and L03.")
row("cmd-ruff", "2.9-gate", "repository", "PASS",
    CMD + "ruff check . -> 'All checks passed!'; ruff format --check . -> '335 files already formatted'.")
row("cmd-mypy", "2.9-gate", "repository", "PASS",
    CMD + "mypy --no-incremental -> 'Success: no issues found in 229 source files'.")
row("cmd-pytest-slice", "2.9-gate", "tests/test_labs.py, test_run_labs.py, test_page_smoke.py, test_page_checks.py, test_curriculum.py, test_build_site.py", "PASS",
    CMD + "pytest -q on the six modules -> all passed (no failures, exit 0).")
row("cmd-verify-refs-live", "2.1-citations", "references/references.json keys harris2002trading, mishkin2021economics", "PASS",
    CMD + "tools/verify_refs.py --unit FC1 -> 'live re-verification of FC1: 2 of 560 entries, 0 problems'; --offline -> '560 entries, 0 problems'.")
row("cmd-numbers-recompute", "2.2-numbers", "all prose numbers in index, L01, L02, L03", "PASS",
    "ledgers/FC1/scripts/FC1-a-r4/numbers_r4.py (Fraction arithmetic): S1=1900, S2=2710, S10=6861.8940391 (686189 cents), 6,861.90 under 4-dp rounding first; Ex 3.6 1818.18 (20000/11 dollars, 18.18 percent of 10000, E2 ratio 2/11); half-redeposit stage-10 total 1817.90 (181790 cents); M2 S2=1850; M3 equity -20; Ex 2.5 cash -600, mid-move -1000; R2 cash 1400, mid-move +1000; M2 cash -160; hub 7/9=77.8 percent and 80 percent of 9 = 7.2; hours 50/70=71.4 and 20/70=28.6; coupon 500 and period-3 flow 10500; L02 counts (exposure 3,3,2,2,2; form 6,6; venue 4,8; exchange cash 1, derivative 3; malformed 14 for 13); L03 Part C grid 121 pairs. Every prose figure matches.")
row("grep-scope-words-L03", "2.9-prose", "course/modules/FC/FC1/L03.html", "PASS",
    "Scope words (every, all, only, always, same, exactly) re-read in L03 lines 57-341 and 423-467. Each occurrence is covered by a proof, a finite labelled grid, or a definition, except that the Proposition 2.3 scope inherits the constant-half-spread gap recorded in L03-A1-single-half-spread, which is a separate row.")
row("hub-placement-numbers", "2.2-numbers", "index.html lines 69, 80-131", "PASS",
    "Nine items (seven prerequisite, two skill checks). Answers recomputed: 110/1.1 = 100; 1+1/2+1/4 = 1.75; 100-P = P-20 gives 60; Q = 40 at P = 60; 1000 x 1.05^2 = 1102.50; coupon 500; period-3 flow 10500. 80 percent of nine = 7.2, so eight correct; 7/9 = 77.8 percent.")
row("hub-hours-arithmetic", "2.9-hours", "index.html lines 29, 39-41", "PASS",
    "data-hours-lessons=50 and data-hours-project=20 sum to 70; L01, L02, L03 each data-hours=10 (5 x 10 = 50); 50/70 = 71.4 percent, 20/70 = 28.6 percent; bar widths 71.4 percent and 28.6 percent.")
row("hub-rung2-lab2-description", "2.6-projects-hub-claim", "index.html line 152", "PASS",
    "Line 152 now reads 'the discount exponent and the trade's cash flow, with its two blanks'. project.html line 46 ('fill in the two blanks, the discount exponent and the trade's cash flow') and line 105 (Lab 2 heading 'the discount exponent and the trade's cash flow') agree. Fixed since round 3.")
row("hub-rung1-rung2-skill-items", "2.2-numbers", "index.html lines 122-131", "PASS",
    "Coupon 10000 x 500/10000 = 500 cents; period-3 flow 500 + 10000 = 10500 cents; both match the coupon rule of project.html.")
row("hub-structure-objectives-prereqs", "2.9-structure", "index.html lines 35, 44-65, 135-171", "PASS",
    "Six objectives (4 to 8 required); prerequisite list now names only Bertrand competition from E1 and the geometric series from M1; both prerequisite titles match curriculum/01-foundations.yaml ('How to Study This Program') and curriculum/02-economics-finance-core.yaml ('Microeconomics'); lesson map links L01 to L05; data status matches the pages (no data-files attribute in index, L01, L02, L03).")
row("hub-core-reading-registry", "2.1-citations", "index.html lines 164-171; references/references.json", "PASS",
    "data-cite entries are rendered from the registry; harris2002trading year 2002 and mishkin2021economics year 2021 in references.json. No page or figure is cited from either book (L03 lines 341 and 564 say book level only).")
row("hub-lesson-card-claims", "2.9-prose", "index.html lines 139-143", "PASS",
    "Each card blurb matches its lesson headings: L01 (intermediary, multiplier, leakage, loss buffer), L02 (venue, taxonomy, register check), L03 (quote, spread, capture, closed-sequence condition).")
row("hub-placement-grade-C-text", "2.3-grades", "index.html lines 114-120", "PASS",
    "'working paper, practitioner research or single-sample evidence' matches BLUEPRINT.md line 161 (grade C row).")

row("L01-prop2.2-proof", "2.4-mathematics", "L01.html lines 88-96", "PASS",
    "X_t + l_t = rho D_t + (1-rho) D_t = D_t under A1 and the loan definition; summing over t gives the cumulative identity. Stock reading checked: cumulative reserves rho S_n and cumulative loans (1-rho) S_n sum to S_n.")
row("L01-prop3.1-closed-form-proof", "2.4-mathematics", "L01.html lines 102-113", "PASS",
    "Finite geometric sum with q = 1-rho, q != 1 since rho > 0; 0 <= q < 1 from A1; rho = 1 gives S_n = d; numerically S10 = 6861.8940391.")
row("L01-prop3.5-hypothesis-A3", "2.4-mathematics", "L01.html lines 76 (A3), 131-133 (Proposition 3.5), 135-138 (proof)", "PASS",
    "Fixed since round 3. The statement now keeps A1, keeps the no-withdrawal and no-repayment parts of A3, and says that the no-cash-leaves clause is replaced by the leakage of A2'. The proof uses only A1 and D_{t+1} = phi(1-rho) D_t, and the limit d/(1-kappa) with (1-kappa) - rho = (1-rho)(1-phi) >= 0 re-derived; equality iff phi = 1 or rho = 1.")
row("L01-Dt-definition-vs-recursion", "2.4-mathematics", "L01.html line 73 (Assumption 2.0), lines 84-86, 94-95, 131-133", "PASS",
    "Fixed since round 3. Assumption 2.0 now defines D_t as the deposits received at stage t (new deposits, not the balance) and S_n as the balance after stages 0 to n. Recursion D_1 = (1-rho)d, S_n = sum D_t and Lab 1 Part B wording ('deposits received at that stage') now agree.")
row("L01-prop2.2-cumulative-claim", "2.4-mathematics", "L01.html lines 88-96", "PASS",
    "Cumulative identity follows from the stage identity; under the flow reading of D_t the sum is S_n.")
row("L01-prop4.1", "2.4-mathematics", "L01.html lines 149-167", "PASS",
    "Assets A - lambda = D + E - lambda; equity E - lambda (Remark 1.2); nonnegative iff lambda <= E. Lab 1 Part D values 50, 0, -50 re-derived.")
row("L01-remark3.2-R1-R3-P-problems", "2.4-mathematics", "L01.html lines 115-118, 343-446", "PASS",
    "Remark 3.2 (rho = 0 gives S_n = (n+1)d); P1 difference (1-rho)^{n+1} d; P2 relaxed to rho = 0 keeping A2 and A3 (D_t = d, S_n = (n+1)d unbounded), re-read this round; P3; R1 bound d/c; R2 least equity lambda; R3 no phi gives 2d/rho. All re-derived.")
row("L01-example3.3-3.6", "2.2-numbers", "L01.html lines 120-143", "PASS",
    "S1 = 1900, S2 = 2710, S10 = 6861.8940391 -> 6,861.89 (686189 cents); 4-dp rounding first gives 6861.90; Example 3.6 1000/0.55 = 1818.18 (181818 cents), 18.18 percent of 10000.")
row("L01-lab1-expected-vs-output", "2.5-labs", "tests/labs/FC1/lab-FC1-L01-1.py; L01.html lines 172-309", "PASS",
    "Page code equals the twin; expected block equals the twin's output under python -I -W error (exit 0, empty stderr, deterministic). Changed Part B label re-checked: the printed line is identical in twin and page. Values: 6.8619, 686189, 1000000, B True, C 181790 and 181818, D 50/0/-50.")
row("L01-lab1-hypothesis-and-interpretation", "2.5-labs", "L01.html lines 171, 310", "PASS",
    "Hypothesis predicts Parts A to D and the printed values agree; interpretation says the parameters are typed in and describe no real bank.")
row("L01-key-results-lab-row-grade", "2.3-grades", "L01.html line 460", "FAIL",
    "The row reads 'Lab 1, Parts A to D, exact comparisons printed as True'. The printed output does not support this: Part D prints 'equity nonnegative: False' for the 150 loss (L01.html line 309); Part C prints one comparison, 'the full-redeposit limit exceeds the half-redeposit limit: True' (line 303), and no other True; Parts A and B print True (lines 291, 296-297). The row grades a typed-in exact check as T; this is accepted as an exact instance check, not a theorem.",
    "Change the source cell to: 'Lab 1 Parts A and B print True for each exact comparison; Part C prints True for the limit comparison; Part D prints the sign test (True, True, False), which agrees with Proposition 4.1.' Keep grade T only as an exact instance check of Propositions 2.2, 3.1, 3.5 and 4.1 for the typed-in parameters.")
row("L01-canon-breaks-misconceptions", "2.9-prose", "L01.html lines 315-341", "PASS",
    "Canon-break bullets and misconceptions 1 to 3 re-read. Misconception 1 now says the output prints multiplier 1.9000 (190000 cents), which matches Lab 1 Part A line n = 1. Figures 6.8619, 1900, 10 and 1/2 twice re-checked.")
row("L01-quiz-explanations", "2.7-cards-quiz", "L01.html lines 466-541", "PASS",
    "Each quiz answer and explanation recomputed: reserve 100; D_1 800; S_2/d 1.75; limit 10000; leakage limit smaller; equity 40; S_2 700 for 400 at rho = 1/2; zero-reserve multiplier n+1.")
row("L01-grade-legend", "2.3-grades", "L01.html line 46", "PASS",
    "Legend C entry now reads 'working paper, practitioner research or single sample', matching BLUEPRINT.md line 161.")
row("L01-uses-and-dfn", "2.5-DAG-definitions", "L01.html lines 37, 38, 59, 81; check_dag FC1 PASS", "PASS",
    "Uses: geometric series (used in Section 3). Introduces: bank money creation and financial intermediary, dfn ids def-financial-intermediary and def-bank-money-creation, as the hub assigns.")

row("L02-prop1.4-hypothesis-scope", "2.4-mathematics", "L02.html lines 68-69 (Assumption 1.3), 73 (Proposition 1.4), 78 (proof), 83 (Remark 1.5)", "PASS",
    "Fixed since round 3. Proposition 1.4 now states 'for any finite set of n trades each of which is classified by Assumption 1.3'; the proof uses that each trade of the set is classified; Remark 1.5 and card FC1-c021/c022 agree. 'Classified' is used for a single trade with the sense of Assumption 1.3's scope sentence (executed on a Definition 1.1 venue or bilaterally); this is read as the intended definition and accepted.")
row("L02-prop2.5-proof", "2.4-mathematics", "L02.html lines 117-125", "PASS",
    "Each entry has exactly one value on each axis, the statement carries that hypothesis, and the counts over the listed values partition the n entries.")
row("L02-remark2.6-P3", "2.4-mathematics", "L02.html lines 127-130, 340-343", "PASS",
    "Entry with k exposure values exceeds n by k-1; Problem P3 gives |S|-1; Lab 2 Part D prints 14 for 13 entries.")
row("L02-example3.1-four-combinations", "2.3-grades", "L02.html line 255 (Example 3.1), line 407 (key-results row 4)", "PASS",
    "Fixed since round 3. Example 3.1 now names the basis: entries 1, 3, 4 and 6 of the register in the lab code, read by hand, not printed by Lab 2. The key-results row is graded C with that basis (line 407). The card still needs the same basis; recorded in cards-L02-scan.")
row("L02-lab2-expected-vs-output", "2.5-labs", "tests/labs/FC1/lab-FC1-L02-1.py; L02.html lines 135-247", "PASS",
    "Page code equals twin; expected equals output under python -I -W error. Counts recomputed from REGISTER: exposure 3,3,2,2,2; form 6,6; venue 4,8; exchange entries 1,3,5,11 with cash 1 and derivative 3; three exposure classes; malformed total 14 for 13.")
row("L02-lab2-hypothesis-and-interpretation", "2.5-labs", "L02.html lines 133, 246", "PASS",
    "Hypothesis lists the Part B counts and the Part C result printed; the interpretation says the register is typed in and makes no market claim.")
row("L02-misconceptions-and-register-claims", "2.9-prose", "L02.html lines 279-289", "PASS",
    "Misconception 2 lists entries 3, 5, 6, 8, 10, 11 (six derivatives) with exposures equities, rates, rates, credit, fx, commodities; Part B prints the count 6. Misconception 3 matches Part C.")
row("L02-uses-line-intermediary", "2.5-DAG", "L02.html lines 34-38 (meta row)", "PASS",
    "Fixed since round 3. The Uses entry for financial intermediary has been removed. The term appears in L02 only in the lesson-nav link text 'L01 · Money, Banks and Financial Intermediaries' (line 503), not as a concept used in the body.")
row("L02-grade-legend", "2.3-grades", "L02.html line 45", "PASS",
    "Legend C entry matches BLUEPRINT.md line 161.")
row("L02-key-results-other-rows", "2.3-grades", "L02.html lines 404-408", "PASS",
    "Rows 1 to 3 are T with proofs or the lab counts; row 5 counts recomputed and graded T from Lab 2 Part B; row 4 is C with basis (see L02-example3.1-four-combinations).")
row("L02-quiz", "2.7-cards-quiz", "L02.html lines 414-493", "PASS",
    "Answers recomputed: OTC by terms (Def 1.1); exactly one (Def 2.1); derivative count 6 (Part B); exchange derivatives 3 (Part C); rates for the government bond futures; 1 for the 13-entry register; no market size (Remark 3.2); 5 exposure values; form axis (Remark 2.2); venue values exchange and OTC.")

row("L03-A1-single-half-spread", "2.4-mathematics", "L03.html line 80 (A1), line 88 (Definition 2.1, p_t = m_t + sigma_t h), lines 98-100 (Proposition 2.3)", "FAIL",
    "Counterexample inside A1 to A3: at one mid 10000, a customer buys one share at the ask 10001 (half-spread 1) and a customer sells one share at the bid 9997 (half-spread 3). The sequence is closed, the mids are equal, and P = C = 10001 - 9997 = 4 cents. V = 2 and the mid-move term is 0, so Proposition 2.3 needs h = 2, which is the half-spread of neither quote. A1 lets the quote in force change between trades, but nothing in A1 to A3 or Definition 1.2 fixes h across the sequence. A script with 2000 random constant-h sequences (ledgers/FC1/scripts/FC1-a-r4/numbers_r4.py) confirms the identity holds once h is constant.",
    "Add to A1: 'the half-spread h is the same at every trade of the sequence (the quote is not revised within it)'. Alternatively restate Proposition 2.3 with h_t per trade: P = sum_t h_t q_t + sum_t sigma_t q_t (m_t - m_n), and carry h_t through Definition 2.1, Corollary 2.4, card FC1-c041 and c042.")
row("L03-prop2.3-proof-algebra", "2.4-mathematics", "L03.html lines 96-106", "FAIL",
    "The algebra is correct for one h: sigma q p - sigma q m_n = sigma q (m_t - m_n) + h q uses sigma^2 = 1 and a single h for every trade (line 105). The statement 'Under A1 to A3, for any finite sequence' does not carry that single-h hypothesis, and the variable-quote counterexample in L03-A1-single-half-spread violates it. Proposition 2.3 is therefore graded T on a hypothesis it does not state.",
    "Fix as in L03-A1-single-half-spread: state the constant half-spread in A1 (or use h_t in the statement and the proof).")
row("L03-cor2.4-prop2.3-P1-P2", "2.4-mathematics", "L03.html lines 108-116 (Corollary 2.4), 396-413 (P1, P2)", "FAIL",
    "Corollary 2.4 states P = C = sQ, with s the quoted spread, for a closed sequence at one mid, and its proof uses P = hV from Proposition 2.3. Counterexample: one share bought at the ask 10001 and one share sold at the bid 9997 at mid 10000 (closed, one mid). C = P = 4 cents, while sQ = 2 with h = 1 and sQ = 6 with h = 3. P1 and P2 use Proposition 2.3 and Definition 2.1 and inherit the same gap.",
    "Make the half-spread constant in A1 (see L03-A1-single-half-spread); the corollary, P1 and P2 then hold as written.")
row("L03-example2.5-numbers", "2.2-numbers", "L03.html lines 118-121, 351, 477", "PASS",
    "Cash -9998 x 100 + 9992 x 100 = -600; hV = 2 x 200 = 400; mid-move (-1)(100)(10000-9990) = -1000; 400 - 1000 = -600. Misconception 1 figures match.")
row("L03-prop3.2-equilibria", "2.4-mathematics", "L03.html lines 148-159", "PASS",
    "Asymmetric profiles fail (dealer 2 or 1 gains by a tie at the lower ask or at the rival's ask; a1 = c case handled). Symmetric (c+k, c+k): k=0 and k=1 and k=2 are equilibria by the case analysis; k>=3 deviation to a-1 earns (k-1)Q > kQ/2 iff k > 2. Independent check: wide grid 100 to 159 with Q = 1000 gives exactly (100,100), (101,101), (102,102).")
row("L03-remark3.3-R1-R3", "2.4-mathematics", "L03.html lines 161-163, 446-465", "PASS",
    "R1 three-dealer symmetric profiles: (c,c,c) and (c+1,c+1,c+1) equilibria, (c+2,c+2,c+2) not (checked by script with Q = 300: k=0 True, k=1 True, k=2 False, k=3 False). R2 numbers: sale at 9988 pays 998800, purchase at 10002 receives 1000200, cash 1400, spread term 400, mid-move +1000 (re-derived). R3 consistent with the grid. Remark 3.3 scope matches R1.")
row("L03-lab1-expected-vs-output", "2.5-labs", "tests/labs/FC1/lab-FC1-L03-1.py; L03.html lines 166-334", "PASS",
    "Page code equals twin; expected equals output under python -I -W error. Part A: 14 trades, inventory 0, cash 4000 = 4 x 1000. Part B: terminal mid 10001, spread capture 4000, mid-move -545, P&L 3455 = 4000 - 545. Part C: 121 pairs, equilibria (100,100), (101,101), (102,102), all symmetric. Seed 2026 is labelled SIMULATED.")
row("L03-lab1-hypothesis-and-interpretation", "2.5-labs", "L03.html lines 168, 333", "PASS",
    "Hypothesis predicts Part A zero inventory and 4000, Part B the identity with V = 2000, Part C the three symmetric pairs and 121 pairs; printed values agree. Interpretation says the grid is finite and the proof covers all whole-cent asks.")
row("L03-grades-key-results", "2.3-grades", "L03.html lines 475-480", "PASS",
    "Rows 1 to 4 are T (proved in section 2 or 3, or computed by hand from Proposition 2.3). Rows 5 and 6 are C naming Lab 1 Parts A, B and C (seeded SIMULATED flow and finite grid).")
row("L03-uses-line-exchange-otc", "2.5-DAG", "L03.html lines 34-38 (meta row)", "PASS",
    "Fixed since round 3. The Uses line now names Bertrand competition (E1) and integer arithmetic only. The body of L03 has no use of exchange-traded or OTC markets; 'Exchanges' occurs only in the book title (line 564).")
row("L03-canon-breaks-misconceptions", "2.9-prose", "L03.html lines 336-362", "PASS",
    "Canon-break bullets: Example 2.5 (positive spread capture, negative profit) re-derived; Remark 2.2 V = 2Q only for closed; four excluded items match A2; Harris cited at book level. Misconception 2 'unless every trade is one share' is correct by Proposition 2.3's V.")
row("L03-problems-and-quiz", "2.7-cards-quiz", "L03.html lines 364-560", "PASS",
    "M1 cash 200 = sQ; M2 cash -160, P = -160, terms 320 and -480; M3 spread 30, relative 0.6 percent; P1, P2, P3 correct; E1 to E3 print-based answers re-derived (E2 -545 with terminal 10001, E3 0.03 percent); quiz answers 4, 200, -1000, 121, 103 (k = 3, deviation 102 earns 2000 vs 1500), 1000, tick one cent.")

row("grade-legend-C-text", "2.3-grades", "course/modules/FC/FC1/L01.html line 46; L02.html line 45; L03.html line 46", "PASS",
    "All three slice lessons now read 'working paper, practitioner research or single sample', matching BLUEPRINT.md line 161. Out of this slice: course/templates/lesson.html line 48 and L04.html line 46, L05.html line 47 still read 'single study'; recorded in notes, not a slice row.")

row("cards-L01-scan", "2.7-cards-quiz", "course/modules/FC/FC1/cards.json FC1-c001..c018, c091..c094, c103..c104", "PASS",
    "24 L01 cards re-read against the current L01 text. c005 flow reading of D_t; c009 states A1, 0 < rho <= 1 and the no-withdrawal and no-repayment parts of A3, matching the fixed Proposition 3.5; c014 says Lab 1 Part A prints True 'at every stage', which is one printed True for all stages 0 to 10 (accepted as the same content); values 6,861.89, 181818, -50, 1900 match the lesson and output.")
row("cards-L02-scan", "2.7-cards-quiz", "course/modules/FC/FC1/cards.json FC1-c019..c034, c095..c096 (FC1-c030 in particular)", "FAIL",
    "18 L02 cards re-read. FC1-c030 (back: 'Yes. Example 3.1 gives a cash exchange entry, a derivative exchange entry, a cash OTC entry and a derivative OTC entry, so form and venue vary independently') states the four-combination result without the basis that the lesson now gives (a hand reading of register entries 1, 3, 4 and 6, not printed by Lab 2; key-results row graded C). The round-3 fix asked for this card to be changed to match, and it was not.",
    "Change FC1-c030 back to: 'Yes, on a hand reading of register entries 1 (cash, exchange), 3 (derivative, exchange), 4 (cash, OTC) and 6 (derivative, OTC) of Lab 2; the lab prints no cross-tabulation (Example 3.1, graded C).'")
row("cards-L03-scan", "2.7-cards-quiz", "course/modules/FC/FC1/cards.json FC1-c035..c055, c097..c098, c105..c108", "FAIL",
    "27 L03 cards re-read. FC1-c041 ('P = hV + sum sigma_t q_t (m_t - m_n) ... holds whether or not the sequence is closed') and FC1-c042 ('P = C = sQ ... every trade is at the same mid') state Propositions 2.3 and Corollary 2.4 without the constant half-spread they need (see L03-A1-single-half-spread: a closed sequence with quotes of half-spread 1 and 3 gives P = 4, not 2h = 4 for any single h). The other 25 cards agree with the lesson and lab output (c052 4000, c053 4000 and 10001, c097 -545, c098 3455).",
    "Fix at the source (A1 constant half-spread, or h_t in Proposition 2.3), then add the same hypothesis to FC1-c041 and FC1-c042.")
row("cards-duplicates-and-numbers", "2.7-cards-quiz", "course/modules/FC/FC1/cards.json (69 cards for L01 to L03)", "PASS",
    "No duplicate ids and no duplicate fronts across the file. Every number in the L01 to L03 card backs (6,861.89; 686189; 181818; 1,818.18; 1900; 2710; 14/13; 121; 4000; 10001; -545; 3455; -50; 6, 4 and 8 counts) appears in its lesson or printed lab output.")
row("cards-coverage", "2.7-cards-quiz", "course/modules/FC/FC1/cards.json; L01.html, L02.html, L03.html quiz sections", "PASS",
    "Each L01 to L03 card's lesson field matches the lesson whose result its back cites (read card by card).")
row("notation-symbols", "2.9-notation", "L01, L02, L03 math; notation/notation.json", "PASS",
    "Registered program-wide symbols in notation.json: T (sample size), Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, \\mathbb{Q}. None appears in L01 to L03 with another meaning: T is not used, R is used only as problem labels R1 to R3, and plain Q (volume and demand) is not \\mathbb{Q}. Local letters (sigma, S, m, mu) are defined where used (Definition 2.1 sigma_t; Section 3 S_n).")
row("DAG-concepts", "2.5-DAG", "index.html lines 61-62; L01 line 37; L02 line 34-38; L03 line 37; check_dag FC1 PASS", "PASS",
    "Hub prerequisites name Bertrand competition (E1) and the geometric series (M1), both in the closure; L03 uses Bertrand competition (E1) as linked; L02 no longer declares an unused intermediary use; L01 uses geometric series. check_dag passes.")
row("banned-phrases-and-process-words", "2.9-prose", "index.html, L01.html, L02.html, L03.html visible prose", "PASS",
    "Scanned for builder/verifier/round/fragment/TODO/placeholder/fixed-in-prose. None found. 'agent' appears only in the economics sense ('a dealer is an agent that posts a bid').")
row("data-and-figures", "2.9-data", "index.html lines 159-162; L01-L03 (no data-files)", "PASS",
    "No data-files attribute in the slice; labs use typed-in or seeded SIMULATED input, labelled on the page. Hub data status matches.")
row("registry-mishkin-harris", "2.1-citations", "index.html line 166; L03 lines 341, 564", "PASS",
    "Harris: registry year 2002, title 'Trading and Exchanges: Market Microstructure for Practitioners', L03 cites book level with year 2002. Mishkin: registry year 2021; curriculum string says 2022 (registry flag, unchanged since round 3).")

rows = rows
counts = {}
for r in rows:
    counts[r["status"]] = counts.get(r["status"], 0) + 1
verdict = "PASS" if counts.get("PASS", 0) == len(rows) else "FAIL"
frag = {
  "unit": "FC1",
  "slice": "FC1-a",
  "round": 4,
  "verifier": "Haiku independent verifier, FC1-a round 4 (did not build FC1)",
  "pin": "b276325",
  "base": "ccfdf4c (round-3 pin). Delta ccfdf4c..b276325 in the slice: index.html, L01.html, L02.html, L03.html, tests/labs/FC1/lab-FC1-L01-1.py changed; lab-FC1-L02-1.py and lab-FC1-L03-1.py unchanged; cards.json changed (FC1-c021/c022, c030 untouched, c041 etc.). Every changed hunk in the slice was read (/tmp/fc1-v/a-r4-delta.diff, 377 lines).",
  "checkout": R,
  "scratch": "/tmp/fc1-v/a-r4/",
  "verified_at": "2026-10-29T02:22:37+00:00",
  "verdict": verdict,
  "rows": rows,
  "mutants": [],
  "registry_flags": [
    "mishkin2021economics: curriculum string 'Mishkin, 13th ed. (2022)' vs registry year 2021. The hub renders registry fields only; owner to decide.",
    "harris2002trading: curriculum string '(2003)' vs registry and Crossref year 2002. L03 states registry year 2002 and cites at book level."
  ],
  "freshness_flags": [],
  "notes": [
    "Slice read in full this round: index.html (176 lines), L01.html (558), L02.html (510), L03.html (577), the three twins, and all L01 to L03 cards in cards.json (69 cards). Every hunk of the round delta was re-read.",
    "Mutants: none. The slice is hub and lessons, not a project grader; mutate_graders is not applicable (verifier rules: lab twins are demonstrations).",
    "Out of this slice and recorded only: course/templates/lesson.html line 48, L04.html line 46 and L05.html line 47 still read 'single study' for grade C; they are not in this slice and the L01 to L03 pages now match BLUEPRINT.",
    "Could not check: rendered layout and console behaviour in a browser (page_smoke prints only the unit summary; no screenshot taken); project.html and the grader were consulted only for the hub's Lab 2 description; L04 and L05 were checked only through the hub card blurbs.",
    "Previous round carry rule: no PASS row was carried from round 3 without re-verification. Rows whose cited subject changed or whose evidence I re-derived are listed as fresh; the L01-key-results-lab-row-grade and L03 hypothesis rows were FAIL on re-verification although their subject text was unchanged."
  ],
  "summary": "Slice FC1-a round 4 at b276325: %d rows, %d PASS, %d FAIL. FAILs: (1) L03 Proposition 2.3, Corollary 2.4, P1-P2 and cards c041/c042 need a constant half-spread across a sequence, which A1 to A3 do not state (counterexample: buy at ask 10001 and sell at bid 9997, P = 4, no single h fits); (2) L01 key-results row 460 claims 'exact comparisons printed as True' for Parts A to D, but Part D prints False for the 150 loss; (3) card FC1-c030 still gives the four-combination result without the basis the round-3 fix required. Round-3 FAILs on Proposition 1.4 scope, Assumption 2.0 D_t, Proposition 3.5 A3, Example 3.1 grade, the hub rung-2 text, and the Uses lines are fixed and re-verified PASS." % (len(rows), counts.get("PASS",0), counts.get("FAIL",0))
}
out = R + "/ledgers/FC1/FC1-a.json"
json.dump(frag, open(out, "w"), ensure_ascii=False, indent=1)
print(out, verdict, counts, len(rows))
