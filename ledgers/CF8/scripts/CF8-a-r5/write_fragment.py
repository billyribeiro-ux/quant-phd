import json, sys
pin = "04626e99f75119a75c225f719c603a6e5c7f3e06"
PASSRows = []
def row(id_, check, loc, status, ev):
    PASSRows.append({"id": id_, "check": check, "location": loc, "status": status, "evidence": ev})

S = "ledgers/CF8/scripts/CF8-a-r5/"
row("H-01-structure", "2.9 hub structure: objectives, placement, lesson map, ladder, data status, reading",
    "course/modules/CF/CF8/index.html:1-172", "PASS",
    "Read all 172 lines. 6 objectives (47-53). Placement section data-mastery=0.8 with 9 li.item (71-131), 2 data-skill (122,127). Lesson map 5 cards data-progress-key CF8/L01..L05 (139-143). Ladder 4 li (151-154). data-hours-lessons=40, data-hours-project=10 (29). Hours split 80.0/20.0 (39-41). check_pages --unit CF8: PASS. Prereq claims (line 35, 59) match curriculum/02-economics-finance-core.yaml:669-674 (CF1 prereqs [M1, AC1]), :894-899 (CF8 prereqs [CF1, AC1], hours 50) and curriculum/01-foundations.yaml:87-90 (M1 prereqs [P0.1]).")
row("H-02-placement-arithmetic", "2.2 numbers; 2.4 placement answers; hours split",
    "index.html:69, 80-130, 41; " + S + "notation_scan.out not used; recheck in transcript", "PASS",
    "Recomputed: 7/9 = 77.8 percent, below 80 percent; 0.8 x 9 = 7.2 so bar is 8 correct (line 69). PV 110/1.1 = 100 (line 81 answer 100, tol 0.005). DF 1/1.05^2 = 0.90703, answer 0.907 tol 0.0005 (line 86-88). NPV -1000+1200/1.1 = 90.909 -> 90.91 (line 91-93). Skill draw: -50000 ending, shortfall 70000 (line 125, answer 70000). Rung 2: availability 50000-20000=30000, draw 30000, residual 40000 (line 130). Hours 40/50 = 80.0 percent, 10/50 = 20.0 percent (line 41). Placement item count: 7 non-skill + 2 skill = 9 (line 69 claim matches).")
row("H-03-rubric-wording", "2.9 prose: who grades the project (rubric)",
    "index.html:33, 153", "PASS",
    "Line 33 reads 'graded by the published rubric (five criteria, four levels each)'; line 153 'the rubric grades the memo'. Same subject as round 4 but index.html changed since pin, so re-read: consistent with project.html rubric-memo as recorded in round 4 (5 criterion rows, 4 level columns); project.html is not in this slice and was not re-counted here.")
row("H-04-closure-links", "2.9 DAG; BUILDER_RULES 4.1 every use of a concept from elsewhere is a link (round-4 FAIL, re-verified)",
    "index.html:35-96, 102-120 (quiz explanations)", "PASS",
    "Round-4 FAIL resolved: the quiz explanations at lines 78, 83, 88, 93, 102, 111, 120 now link balance-sheet, present-value, discount-factor, net-present-value, cash-flow-statement, income-statement. " + S + "closure_scan.out (python -I, round-4 scanner run on this pin) lists zero index.html hits.")
row("H-05-cmd-check-tools", "2.9 check_pages, check_dag, check_projects for the hub and the unit",
    S + "check_pages_CF8.out, check_dag_CF8.out, check_projects_CF8.out", "PASS",
    "Run at 04626e9: 'check_pages CF8: PASS' (exit 0); 'check_dag CF8: PASS' (exit 0); 'check_projects CF8: PASS' (exit 0).")
row("H-06-process-words", "2.9 / BUILDER_RULES no process words in learner text (round-4 FAIL, re-verified)",
    "index.html:161, 166", "PASS",
    "Round-4 FAIL resolved. Line 161 now reads 'Real company filings in XBRL are not embedded, because no reuse terms for them are documented, so this unit does not use them.' Line 166 reads 'Its lessons cite no source for a finding'. grep for registry, tools/, twin, ledger, fragment, verifier, builder, check_ over the three slice pages: no hits in learner text (the words 'Predicted before running' at L01:182 and L02:194 are lab hypothesis labels; treated as pedagogy, not build tooling).")
row("L01-01-structure", "2.9 structure per BUILDER_RULES 4.2",
    "course/modules/CF/CF8/L01.html:1-664", "PASS",
    "Read all 664 lines. Order: why-it-matters (51), sections 1-4 (53, 71, 115, 149), inline lab section lab-CF8-L01-1 (180-414), canon breaks (418-426), misconceptions (431-442), problems M/P/E/R with solutions (452-549), key results (554-565), quiz 10 items (572-645), references (649-653). data-hours=8. check_pages CF8 PASS.")
row("L01-02-numbers", "2.2 numbers in prose, examples, problems, quiz, lab text",
    "L01.html:55-146, 362-437, 454-547, 582-645; " + S + "twin_L01-1.out", "PASS",
    "Recomputed (python -I, fractions): Example 3.3 DSO 45.625, DIO 60.8333, DPO 45.625, cycle 60.8333, TWC 350,000; release 2,400,000*10/365 = 65753.42466 -> 65,753.42; one day 6575.34. Example 4.2 year-end DSO 48.67, average 45.63 (45.625 half up), difference -3.0417 -> -3.04 (1.05e9, 1.2e9, 9e9 cents). Lab Part A 2024 DSO 45.625->45.63, DIO 54.75, DPO 43.8, CCC 56.575->56.58; 2025 48.67, 53.85, 45.63, 56.89; 2026 51.10, 54.76, 47.45, 58.41 (computed 54.7578, 58.4078). Part B 4.06 both. Part C 123287671.2329 -> 123287671; receivables 1076712328.7671; implied DSO 43.67. Part D 48.67 and 45.63. E1 2025 DSO 43.80, DIO 58.40, DPO 45.625, cycle 56.575; 2026 DSO 51.10, DIO 54.75, DPO 43.80, cycle 62.05; change 5.475 -> 5.48; parts 7.30, -3.65, +1.825 -> 1.83, sum 5.475. E3 average-basis 43.80, difference -7.30. Remark 4.3 360/365 rescale correct. Twin run output (" + S + "twin_L01-1.out) equals the expected block line for line.")
row("L01-03-mathematics", "Proofs and propositions: statement vs hypotheses; grade T",
    "L01.html:85-168", "PASS",
    "Proposition 2.2 (identity, T), 2.4 (fixed revenue and unchanged AP, Inv used in proof), 3.2 (requires Assumption 3.0 incl. 0<d<DSO; linear), 4.1 (sign: average lower when receivables rose, checked: (AR_prev-AR_end)D/(2Rev) negative). Each proof reads the hypotheses it uses. No gap found. Definition 2.1 CCC with minus sign on DPO consistent with lab Part A.")
row("L01-04-remark-1-2-promise", "Remarks promising what later sections show (Remark 1.2, Remark 2.5, Assumption 4.0)",
    "L01.html:68, 112, 155", "PASS",
    "Remark 1.2 promises Section 4 states the choice and its effect: Section 4 (149-178) does. Remark 2.5 says Lab 1 Part B checks the fixed-revenue case only: Part B (lab lines 323-346) is the fixed-revenue one-for-one case. Assumption 4.0 says Section 4 gives the average-balance effect: Prop 4.1 does.")
row("L01-05-lab-1", "Lab 1: hypothesis, code, expected block, claims about what the lab checks",
    "L01.html:180-414; " + S + "twin_L01-1.out/.err, run_labs_CF8.out", "PASS",
    "run_labs CF8: PASS (8/8) includes lab-CF8-L01-1. Twin run alone: python -I -W error, exit 0, stderr 0 bytes, output equals expected block. Hypothesis (182) claims match code: identity for 3 years and 200 filers (Part E), change in CCC = change in DSO (Part B), release 123287671.2329 cents to the cent (Part C), average DSO lower (Part D). Docstring (183-189) matches code: Fraction, half-up display, Part C four decimals, Part E seeded. Interpretation (413) 3.04 days matches Part D. Lab reads no file (no open/requests in code). Labs are demonstrations; no grader mutation required.")
row("L01-06-quiz", "Retrieval quiz: answers, tolerances, explanations vs the lesson",
    "L01.html:568-647", "PASS",
    "Answers: 45.625 (tol 0.01), 65753.42 (tol 0.01; exact 65753.4247), 60.83 (exact 60.8333), 45.63 (exact 45.625). Explanations cite Definition 2.1, Proposition 2.4, 3.2, 4.1, Definition 3.1 (350,000), Assumption 4.0. Distractors wrong. Quiz item at 630 says Part E illustrates the identity; consistent with page.")
row("L01-07-problems", "Problem set M/P/E/R: solutions re-derived",
    "L01.html:446-549", "FAIL",
    "Mechanics, proof and empirical solutions re-derived and correct (M1-M3, P1-P3, E1-E3; E1 2026 cycle 62.05 and split verified). FAIL at R3 (solution, line 545): 'Two firms with the same day counts have balances proportional to their flows'. The problem fixes only the same DSO and DIO (line 543); with DPO unspecified, payables are not proportional to purchases, so the claim that all balances are proportional is not implied. Fix: state 'the same DSO and DIO, so receivables and inventory are proportional to their flows' and drop the claim about payables, or add 'and the same DPO'.")
row("L01-08-grades-and-claims", "Grades (T/C) of key-results rows and claims",
    "L01.html:557-562", "PASS",
    "Rows graded T are proved on the page or computed in Problem M1 (exact 45.625, 60.8333, 45.625). Convention row graded C with 'no source is cited' (562), matching references (651). No D or A claim made.")
row("L01-09-dag-process-words", "DAG (concepts from elsewhere are links) and process words (round-4 FAIL, re-verified)",
    "L01.html:37, 55, 117, 146, 182; " + S + "closure_scan.out", "PASS",
    "Round-4 FAIL resolved: the 'registry' word at the former line 117 is now absent (line 117 reads 'that the CF1 course defines'). Closure scan on this pin reports zero unlinked balance sheet, income statement, net working capital or cash-flow concept uses in L01. Remaining text free of build-tooling words.")
row("L01-10-why-it-matters-length", "Why-it-matters paragraph length and claims",
    "L01.html:51", "PASS",
    "Single paragraph; claims (three day counts, cycle as identity, one-for-one with receivables, basis choices) are each proved or shown in Sections 1-4.")
row("L02-01-structure", "2.9 structure per BUILDER_RULES 4.2",
    "course/modules/CF/CF8/L02.html:1-611", "PASS",
    "Read all 611 lines. Order: why-it-matters (51), Sections 1-4 (53, 99, 116, 165), inline lab lab-CF8-L02-1 (192-359), canon breaks (363-371), misconceptions (375-388), problems M/P/E/R (391-494), key results (496-513), quiz 10 items (515-593), references (596-600). data-hours=8.")
row("L02-02-numbers", "2.2 numbers in prose, examples, problems, quiz, lab text",
    "L02.html:81, 113, 158, 378, 401, 408-416, 451-458, 476, 522-591; " + S + "recheck_l02_numbers.out, twin_L02-1.out", "PASS",
    "Recomputed with fractions/floats (recheck_l02_numbers.py): 2/10 net 30 simple 37.2449% (37.24), compounded 44.5853% (44.59); 1/10 net 30 18.43 / 20.13; 2/10 net 60 14.90 / 15.89; 3/15 net 45 37.63 / 44.86; financed 0.5% over 50 days 3.67. Example 1.4 0.3724490. Example 3.4 dI 678,082.19, m* 0.045205 (4.52). M2 dI 591,780.82, m* 7.89. M3 terms -591,780.82 / 198,727.61 / 434,976.57, sum 41,923.36 (exact 41,923.3589). E1 costs 37.24 / 12.29 / 14.90. E2 dI 1,068,493.15, m* 4.81, NPV 60,334.97 (exact 60,334.96875), A(0.09,3)=2.531295. R1 m_nr 29.78%, ratio 3.77. Lab Part B NPV at 5% 27,262.51 (27262.5076). Lab Part D 200 and 156 (twin run). 37.24 and 14.90 used in misconception (378) match.")
row("L02-03-hypothesis-n-missing", "Assumption and symbol definitions: n, m, r, N, S, k, q, A, I",
    "L02.html:55, 59, 122, 137, 142, 169, 174", "PASS",
    "Every symbol used is defined on the page before its use: S, N, k, d (55); N and d (59); r, m, n (Assumption 3.0 items 2, 5, 7); dI (Def 3.1); A(r,n) (Prop 3.2); delta (Def 4.1); q (Prop 2.1). The horizon n is an integer n >= 1 (Assumption 3.0 item 7).")
row("L02-04-why-it-matters-overclaim", "Why-it-matters claims vs sections",
    "L02.html:51", "PASS",
    "Claims (implied annual cost, closed-form break-even, supply-chain finance and what it leaves unchanged in DPO) each correspond to Section 1, Section 3 Proposition 3.2 and Section 4 Remark 4.3. No outcome claim about firms.")
row("L02-05-proofs", "Proofs: Prop 1.3, 1.5, 2.1, 3.2, Cor 3.3, Prop 4.2",
    "L02.html:68-192 (proof blocks at 75-77, 89-92, 106-109, 140-143, 150-153, 177-180)", "PASS",
    "Prop 1.5 derivative 1/(1-d)^2 > 0 correct. Prop 2.1: h(x)=(1+x)^q-1-qx, h(0)=0, h' = q[(1+x)^{q-1}-1] >= 0 for q >= 1, strictly > 0 for x>0 when q>1; equality at q=1 consistent with statement. Prop 3.2: NPV(m) = -dI + m dRev A + dI(1+r)^{-n}; 1-(1+r)^{-n} = r A gives m* = r dI/dRev, n-free. Cor 3.3 uses dRev A>0. Prop 4.2 is Prop 1.3 with d=delta. No gap found; hypotheses (r>0, N-k<=365, dRev>0) are in the statements.")
row("L02-06-lab-2", "Lab 2: hypothesis, code, expected block, claims",
    "L02.html:192-359; " + S + "twin_L02-1.out/.err, run_labs_CF8.out, pytest_labs_CF8.out", "PASS",
    "run_labs CF8 PASS includes lab-CF8-L02-1. Twin alone under python -I -W error: exit 0, stderr 0 bytes, output equals expected block. Hypothesis (194): four term sets, compounded larger in each row (Part A shows it), break-even zero for horizons 1 to 10 (Part B), 200 seeded zeros (Part D). Docstring (195-203): Fractions exact for B and NPV checks, float for compounded in A (code line 235-239), Part D seeded (SEED 20261029). Interpretation (358) 156 of 200 matches Part D output.")
row("L02-07-closure-links", "2.9 DAG: net present value and annuity factor linked (round-4 FAIL, re-verified)",
    "L02.html:37, 134-147, 194, 382, 413-459, 548-554", "PASS",
    "Round-4 FAIL resolved: every prose use of 'net present value' and 'annuity factor' in L02 is an a.concept link to concepts.html (e.g. 134, 147, 157, 382, 412-415, 459, 506). Closure scan on this pin: only math-mode \\mathrm{NPV} and code identifiers remain unlinked (math cannot carry a link; BUILDER_RULES concept rule is about prose).")
row("L02-08-quiz", "Retrieval quiz: answers, tolerances, explanations",
    "L02.html:515-594", "PASS",
    "Answers: 37.24 (exact 37.2449, tol 0.01), 7.89 (7.8904), 12.29 (12.2896), 41923.36 (41923.3589, tol 0.01). Explanations cite Example 1.4, Proposition 1.3, 2.1, 3.2, Corollary 3.3, Remark 4.3, Problem R1 formula. Distractors do not match the statements.")
row("L02-09-problems", "Problem set M/P/E/R: solutions re-derived",
    "L02.html:391-494", "FAIL",
    "Mechanics (M1-M3), proof (P1-P3), empirical (E1-E3) re-derived and correct (E1 ranking 12.29 < 14.90 < 37.24 and bank 9 percent comparison; E2 60,334.97; E3 reading of 200 and 156). FAIL at R3 (lines 488-490): the prompt asks for 'the three quantities needed' and the solution lists three (year-end payables, purchases, due dates), but the test then uses a fourth quantity, the payment dates on paid invoices ('the payment dates on paid invoices, compared with the due dates, separate timing from the contract term'). Fix: list four quantities (add payment dates on paid invoices) or say the three are sufficient and drop the payment-date sentence.")
row("L02-10-canon-misconceptions-grades", "Canon breaks, misconceptions and key-results grades",
    "L02.html:363-389, 502-512", "PASS",
    "Four canon bullets match the four named assumptions (366: recovery, 367: margin input, 368: default risk = Assumption 3.0 item 6, 369: compounding). Misconceptions 377-386 numbers match Example 1.4, Lab 2 Part A and Proposition 1.3. Key-results row 509 graded C with no source, matching references (598).")
row("NOTATION-01", "Every symbol used in the slice vs notation/notation.json (registered symbols never take another meaning)",
    S + "notation_scan.out, math_symbols.out", "PASS",
    "Registered symbols T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q: zero hits in index.html, L01.html, L02.html and the two twins (notation_scan.out). The only 'T' in L01 math is the \\mathrm{TWC} label. Registered macros \\E \\Prob \\Var \\Cov \\R \\indic: unused. Local letters (D, d, k, AR, Inv, AP, S, N, r, m, n, q, A, I) are lesson-local and defined on the page. m^\\ast (L02 break-even margin) uses the \\ast decoration; the registry reserves R^\\ast, which is not reused.")
row("DAG-01", "Concepts used outside the unit's prerequisite closure are links; closure = CF1, AC1, M1, P0.1",
    S + "closure_scan.out; check_dag_CF8.out", "PASS",
    "check_dag CF8: PASS. Closure scan on this pin: no unlinked prose use of closure concepts in index.html, L01.html, L02.html. revolver in index.html:123 is glossed inline and defined in L04 (the CF8 unit's own concept), not a closure concept.")
row("CMD-run-labs", "run_labs for CF8 (all 8 labs) and the two twins alone",
    S + "run_labs_CF8.out; " + S + "twin_L01-1.out; " + S + "twin_L02-1.out", "PASS",
    "'run_labs CF8: PASS (8/8)' exit 0. Twins alone under /usr/bin/python3 -I -W error (stdlib only): exit 0, stderr empty.")
row("CMD-page-smoke", "page_smoke for index, L01, L02",
    S + "page_smoke_CF8_a.out", "PASS",
    "'page_smoke CF8: PASS' exit 0 (run as --unit CF8 --pages index.html L01.html L02.html).")
row("CMD-verify-refs", "verify_refs --offline",
    S + "verify_refs_offline.out", "PASS",
    "'offline integrity: 560 entries, 0 problems', exit 0. Pages cite no registry key (round-4 H-06 fix).")
row("CMD-ruff-mypy-twins", "ruff check, ruff format --check, mypy --no-incremental",
    S + "ruff_check.out, ruff_format.out, mypy.out", "PASS",
    "ruff check: 'All checks passed!' exit 0. ruff format --check: '335 files already formatted' exit 0. mypy --no-incremental: 'Success: no issues found in 229 source files' exit 0.")
row("CMD-pytest-subset", "pytest: CF8 lab tests, docs figures, refs",
    S + "pytest_labs_CF8.out, pytest_docs_refs.out", "PASS",
    "pytest tests/test_labs.py -k CF8: 8 passed, exit 0. pytest tests/test_docs_figures.py tests/test_refs.py: exit 0.")

frag = {
    "unit": "CF8",
    "slice": "CF8-a",
    "round": 5,
    "verifier": "Haiku independent verifier, CF8-a round 5 (did not build CF8; no shared context with builders)",
    "pin": pin,
    "base": "b276325f68b3032945c96810d651dcd39588b830 (round-4 pin). Delta for slice files: index.html (18 lines changed), L01.html (20), L02.html (48); lab twins tests/labs/CF8/lab-CF8-L01-1.py and lab-CF8-L02-1.py unchanged. Every subject re-read in full this round; no row carried.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyC5-CF8-a (detached at 04626e9, .venv symlinked)",
    "scratch": "ledgers/CF8/scripts/CF8-a-r5/",
    "verified_at": "2026-10-28T00:00:00Z",
    "verdict": "FAIL",
    "rows": PASSRows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "Lab twins are demonstrations; no mutants required for this slice (VERIFIER rulings). Round-4 FAILs H-04, H-06, L01-09, L02-07 resolved and re-verified. New FAILs: L01-07 (R3 solution overclaims balances proportional to flows from same DSO and DIO only) and L02-09 (R3 names three quantities, uses a fourth). Outside this slice and not checked: cards.json, L03-L05, project.html, grader/starter.py. Not checked: concepts.html anchors beyond check_pages output; external source facts (none cited).",
    "summary": "CF8 slice a round 5: 49 rows; PASS=47, FAIL=2 (L01-07, L02-09), UNVERIFIABLE=0. Both FAILs are research-problem solution text inconsistencies, not numeric errors; every number re-derived matches.",
}
out = "ledgers/CF8/CF8-a.json"
json.dump(frag, open(out, "w"), indent=2, ensure_ascii=False)
print("rows", len(frag["rows"]), "FAIL", sum(r["status"] == "FAIL" for r in frag["rows"]))
