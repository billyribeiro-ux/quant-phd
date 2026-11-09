"""Writes the round-15 PC3-b verifier fragment from the rows below (verifier's own assembly; no row is carried)."""
import json
import sys

S = "ledgers/PC3/scripts/PC3-b-r15/"
O = S + "out/"
rows = []


def r(id_, check, location, status, evidence, fix=None):
    row = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)


# ---- gates (commands run by the verifier on the pin) ----
r("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3",
  "PASS", "run_labs PC3: PASS (9/9), exit 0 (" + O + "run_labs_unit.out); includes lab-PC3-L04-1, L05-1, L06-1.")
r("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3", "PASS",
  "check_pages PC3: PASS, exit 0 (" + O + "check_pages.out)")
r("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3", "PASS",
  "check_dag PC3: PASS, exit 0 (" + O + "check_dag.out)")
r("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3", "PASS",
  "check_projects PC3: PASS, exit 0 (" + O + "check_projects.out); the project grader and project labs belong to another slice.")
r("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)", "PASS",
  "page_smoke PC3: PASS, exit 0; L04, L05, L06 each PASS; lab runtime 0.0 s; no console errors reported (" + O + "page_smoke_L456.out)")
r("gate-ruff-mypy-twins", "2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental",
  "PASS", "ruff check 'All checks passed!' exit 0 (" + O + "ruff_check.out); ruff format '9 files already formatted' exit 0 (" + O +
  "ruff_format.out); mypy 'Success: no issues found in 385 source files' exit 0 (" + O + "mypy.out)")
r("gate-pytest-lab-tooling", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py",
  "PASS", "exit 0, output is dots only, no F or E (" + O + "pytest_lab_tooling.out)")
r("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
  "offline integrity: 560 entries, 0 problems, exit 0 (" + O + "verify_refs_offline.out). The L04-L06 pages cite no key (data-references empty at L04.html line 726, L05.html 568, L06.html 539) and every L04-L06 card has cite [].")
r("gate-run-graders-unit", "2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49", "PASS",
  "run_graders PC3: PASS, reference 50/50 seeds, exit 0 (" + O + "run_graders_unit.out); recorded only, the grader is another slice.")
r("gate-fetch-data-check", "2.8-data", "tools/fetch_data.py --check", "PASS",
  "fetch_data: 3 datasets, 0 problems, exit 0 (" + O + "fetch_data_check.out); no slice page reads a dataset.")
r("gate-build-site-check", "2.9-prose", "tools/build_site.py --check", "PASS",
  "site data current: 6 outputs, exit 0 (" + O + "build_site_check.out)")
r("gate-render-curriculum-diff", "2.9-prose", "tools/render_curriculum.py; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "PASS",
  "render_curriculum wrote the same files; git diff exit 0, no change (" + O + "render_curriculum.out, " + O + "curriculum_diff.out)")
r("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html math vs notation/notation.json", "PASS",
  "Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur in any slice math (" + S + "notation_scan.py, output " + O + "notation_scan.out). Registered macros used: \\E and \\Var in L04 (registered in notation.json macros). Local letters (N, t, p, L, I, C, W, v, a, b, h, m, q, sigma, c, f, epsilon in L04; x, n, k, i, j, m, p, q, r in L05; S, K, D, F, I, A, h, l, u, m, tau in L06) each have one meaning within their lesson (notation.json 'about': conventionally local letters are defined per lesson).")
r("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", "PASS",
  "python -I -W error <twin>: exit 0 and 0 stderr bytes for each (" + O + "twin_L04.stdout/.stderr, twin_L05, twin_L06); no network or time module imported (import lines of the page code block: L04 205-209, L05 180-185, L06 179-184)."
  )
r("twin-page-code-equals-twin", "2.5-labs", "L04.html data-run vs tests/labs/PC3/lab-PC3-L04-1.py; L05.html vs lab-PC3-L05-1.py; L06.html vs lab-PC3-L06-1.py", "PASS",
  "html-unescaped data-run block equals the twin after the trailing newline is stripped, for all three (ruling: trailing newlines aside); code_identical_ignoring_trailing_newlines=True for L04, L05, L06 (" + S + "twin_page_compare.py, output " + O + "twin_page_compare.out).")
r("twin-expected-equals-stdout", "2.5-labs", "L04.html pre.expected lines 424-475; L05.html 307-331; L06.html 284-304", "PASS",
  "pre.expected (unescaped) equals the twin's stdout after trailing-newline strip for all three (" + O + "twin_page_compare.out: expected_equals_stdout=True x3).")
r("lab-L04-1-hypothesis-interpretation", "2.5-labs", "L04.html line 180 (hypothesis), 476 (interpretation), code 181-423",
  "PASS", "Hypothesis (line numbers are HTML lines of the page, equal to the pre.expected block lines): cash flow -9950, P&L 30, identity True, informed count on seed 0, seed-1 summary: all equal stdout lines 447-458. Independent re-simulation (" + S + "verify_numbers.py, " + O + "verify_numbers.out; " + S + "l04_mid_identity.py): seed 0 {fills 9, cash_flow -9950, inventory 1, settlement 9980, pnl 30, informed 13}; seed 1 {fills 16, cash_flow 20100, inventory -2, settlement 10020, pnl 60}. Part 2 nine grid values and Part 3 five inventories equal the stated checks. Interpretation (line 476) numbers agree.")
r("lab-L05-1-hypothesis-interpretation", "2.5-labs", "L05.html line 163 (hypothesis), 332 (interpretation), code 164-306",
  "PASS", "Hypothesis: 200 integers in 0..999 from random.Random(5); naive count 1351 = (200-8+1)(8-1); deque at most 2n = 400; 200 pushes; seed-6 run; Part 2 for window sizes 1..20; five edge checks (code lines 278-283 print five lines, stdout 320-324). Interpretation counts 1351, 354 and 350 reproduced by an independent deque implementation (" + O + "verify_numbers.out, seed 5 and seed 6 lines).")
r("lab-L06-1-hypothesis-interpretation", "2.5-labs", "L06.html line 159 (hypothesis), 305 (interpretation), code 160-283",
  "PASS", "Hypothesis: payoff 0 at 10000 and 100 at 10100 for five spot values (stdout 287-290); annuity 3310/1331, break-even 399300/331, zero NPV at break-even, increasing NPV on grid, NPV at bounds and at 8, 10, 12 percent (stdout 292-304). All reproduced by " + S + "verify_numbers.py (" + O + "verify_numbers.out) and " + S + "extra_checks.py.")
r("L04-definitions-A1-A6-notation", "2.4-mathematics", "L04.html lines 56 (symbols), 62-65 (Def 1.1), 69-79 (A1-A6)", "PASS",
  "A1 probabilities 1/4, 1/4, 1/2 (line 72) equal (1-p)/2, (1-p)/2, p at p=1/2; A6 a=m+h, b=m-h with a-b=2h matches Prop 3.1 H2 (line 129); the arrival independence in A1 is an assumption stated as such.")
r("L04-lab-section-locator", "2.9-prose", "L04.html lines 72, 83 vs lab section at line 178 under h2 s4 (line 161)", "PASS",
  "'Lab 1 (Section 4)' (line 72) and 'the unit project (Project · Market-making game)' (line 83): the lab sits in Section 4 (lines 161-177 precede line 178 lab; Section 5 begins at line 479); project.html line 36 is 'Market-making game'.")
r("L04-prop-2.2-2.3-identity", "2.4-mathematics", "L04.html lines 100-118 (Prop 2.2, 2.3 with proofs)", "PASS",
  "Proof of Prop 2.2 by induction and Prop 2.3 algebra re-derived; exact random check of the Prop 2.3 identity on 2000 paths: True (" + O + "verify_numbers.out 'Prop 2.3 turn decomposition identity holds on random paths: True').")
r("L04-example-3.2-values", "2.4-mathematics", "L04.html lines 142-143 (Example 3.2)", "PASS",
  "E = 5, 0, 5/2 cents at v = 10000, 10020, 9985 (verify_numbers.out 'Example 3.2 E at v=...'); the lab grid (stdout 460-468) contains 9985, 10000 and 10020.")
r("L04-proposition-4.1-remark-4.2-sd", "2.4-mathematics", "L04.html lines 163-175 (Prop 4.1, Remark 4.2)", "PASS",
  "Mean 0 and variance 25 I^2 re-derived; sd 15 cents at |I|=3 and 50 at |I|=10 (5|I|); Lab Part 3 values 0, 25, 225, 225, 2500 (stdout 471-475) equal 25 I^2 (verify_numbers.out 'Part3').")
r("L04-remark-4.2-inventory-independence", "2.4-mathematics", "L04.html line 175 (Remark 4.2, I=10 case)", "PASS",
  "At I=10, quote 9990/10010, v=10000, p=1/2: informed does not trade, uninformed sell refused (|11|>10), uninformed buy contributes 10 with probability 1/4, so E = 5/2 (" + S + "l04_mid_identity.py output " + O + "l04_mid_identity.out); the I=0 value 5 matches Example 3.2.")
r("L04-remark-3.4-inventory-zero", "2.4-mathematics", "L04.html lines 157-158 (Remark 3.4)", "PASS",
  "(1-p)h = h/2 at p=1/2, which is 1/4 of the spread 2h (" + O + "l04_mid_identity.out: ratio 1/4).")
r("L04-canon-breaks-tick", "2.2-numbers", "L04.html line 484 ('the mid at turn t is 10000 - 10 I_{t-1}')", "PASS",
  "Claim checked on 2000 seeds x 20 turns = 40000 turn-states, 0 failures (" + S + "l04_mid_identity.py, " + O + "l04_mid_identity.out). Induction re-derived: each fill sets the last price to 10000 - 10 I_new.")
r("L04-canon-breaks-quote-rule", "2.4-mathematics", "L04.html lines 481-483 (canon breaks)", "PASS",
  "Statements follow from A1 (arrival probabilities independent of the quote, line 72) and Prop 3.1 at a fixed quote (per-quote term (1-p)h, rising with h); no unproved claim about wider quotes and flow.")
r("L04-R2-spread-criterion", "2.4-mathematics", "L04.html lines 597-601 (R2)", "PASS",
  "At v=m both brackets of Prop 3.1 vanish, E=(1-p)h; p<1 gives E>0 for all h>=1; p=1 gives E=0 for all h. Argument complete under A1.")
r("L04-E1-seed1-numbers", "2.2-numbers", "L04.html lines 567-570 (E1)", "PASS",
  "16 fills, cash flow 20100, inventory -2, settlement 10020, mark -20040, P&L 60 reproduced by " + S + "verify_numbers.py (" + O + "verify_numbers.out) and stdout line 458.")
r("L04-E2-binomial-z", "2.2-numbers", "L04.html lines 573-577 (E2)", "PASS",
  "SE sqrt(0.25/20) = 0.111803; z = 0.15/0.111803 = 1.3416 (1.34); 1.959964 = NormalDist().inv_cdf(0.975) to 6 places (" + O + "extra_checks.out). Decision 'does not reject' correct.")
r("L04-E3-mid-vs-settlement", "2.2-numbers", "L04.html lines 580-583 (E3)", "PASS",
  "-9950 + 9980 = 30; -9950 + 9990 = 40; difference 10 = I_N (mid - v_N) with I_N = 1 (verify_numbers.out 'E3 P&L').")
r("L04-problems-R1-R3-M-P", "2.4-mathematics", "L04.html lines 515-612 (M1-M3, P1-P3, E1-E3, R1-R3 with solutions)", "PASS",
  "M1 cash +10010, W=10 (line 519); M2 refuses 11, fills 9 (line 526); M3 boundary v=a no trade, v=a+1 buy (line 533); P1 algebra; P2 difference h/2; P3 25*16=400; R1 d=(1-p)h/p=20/3 (verify_numbers.out 'R1 d'); R2 argument complete; R3 25I^2<100 gives |I|<2, largest integer 1 (line 608). Each tier has three problems with a details.solution (" + O + "structure_counts.out).")
r("L04-M3-inventory-hypothesis", "2.4-mathematics", "L04.html lines 522-526 (M2), 529-533 (M3)", "PASS",
  "Limit and boundary arithmetic reproduced (|11|>10 refused; |9|<=10 fills; v=10010 no trade; v=10011 buy).")
r("L04-quiz-q11-citation", "2.5-labs", "L04.html quiz item 11 (lines 707-709) vs lab output line 446", "PASS",
  "Answer 9 equals 'fills 9 of 20 turns' (stdout 446; verify_numbers.out seed 0 fills 9).")
r("L04-quiz-answers", "2.4-mathematics", "L04.html lines 634-720 (12 items)", "PASS",
  "12 items (" + O + "structure_counts.out). MC keys: +10010; 'No, strictly above'; refused at inventory 11; zero because moves are equally likely; settlement v_N; rises as (1-p)h. Numeric keys: 10 (P&L), 0 (v=10020), 5 (v=10000), 400 (25*16), 6.6667 with tolerance 0.001 (20/3 = 6.66667), 9 (fills). All correct.")
r("L04-key-results-prop-3.1-assumptions", "2.3-grades", "L04.html line 622 (key results row for Prop 3.1)", "PASS",
  "Assumption list A1, A2, A4, A5, A6 and H1-H3 matches Prop 3.1 hypotheses (lines 128-129); grade T with proof on the page.")
r("L04-prop-3.1-closed-form", "2.4-mathematics", "L04.html lines 127-139 (Prop 3.1 + proof)", "PASS",
  "Closed form (1-p)h - p[(v-a)^+ + (b-v)^+] equals the three-arrival enumeration on 20000 random (a, b, v, p) cases with 0 mismatches (" + S + "verify_numbers.py, " + O + "verify_numbers.out).")
r("L04-corollary-3.3", "2.3-grades", "L04.html lines 146-153 (Corollary 3.3 + proof)", "PASS",
  "E = h/2 - (v-a)/2 for v >= a and p = 1/2; zero iff v = a+h (verify_numbers.out 'Cor 3.3 zero at v=a+h: E: 0'). Grade T and its hypotheses (p=1/2, v>=a) are stated.")
r("L04-misconceptions", "2.9-prose", "L04.html lines 490-505 (four misconceptions)", "PASS",
  "Each is a wrong belief with a correct statement: 0 cents at v=10020 (stdout 468); 10 cents after the buy at 10010 with settlement 10000; variance 2500 at 10 units (stdout 475); A3 excludes a quote from v_t. Four >= three.")
r("L04-key-results-table-other", "2.3-grades", "L04.html lines 620-625 (key results, six rows)", "PASS",
  "Rows 620-624 are T and each cites a proof on the page; row 625 is C and names Lab 1 Part 2 (SIMULATED grid), as the round-14 ruling requires.")
r("L04-scope-and-banned-phrases", "2.9-prose", "L04.html visible prose (scope words: only 14, every 7, any 5, same 7, exactly 6)",
  "PASS", "Scope-word sentences listed by " + S + "prose_scan.py (" + O + "prose_scan.out); each was read and checked against a proof, an enumeration or a lab line (e.g. 'only when A5 allows it' L04 l.64; 'the proof covers every fair value' L04 l.201). No banned string (check_pages PASS; my scan found no TODO, TBD, lorem, ellipsis, obviously, clearly, studies show, experts agree, it is well known, it is important to note, for brevity, details omitted, beyond the scope, left as an exercise, you can add more). No process word (build, builder, round, verifier, REQUESTS, unit report) in visible prose. Judgement, not a row: the Section 5 descriptions of real limit-order-book queues and of real asset income and short-sale costs are model-limit prose with no grade or key; accepted as generic market-structure description under the plan (no reference admitted); the architect may wish a grade on them.")
r("L04-structure-hours", "2.9-prose", "L04.html header data-hours=6; section order lines 52-730", "PASS",
  "data-hours=6; order: why it matters (52), sections 1-4 with lab inline (54-177, lab 178), where the canon breaks (479), misconceptions (487), problem set (509), key results (614), quiz (631), references (723). 12 problems (3 per tier), 4 misconceptions, 12 quiz items, 6 key rows. why-it-matters is 119 words (<=120; " + O + "prose_scan.out).")
r("L04-DAG-D-terms", "2.9-DAG", "L04.html lines 38, 60, 64, 97, 158, 482", "PASS",
  "adverse selection (lines 158, 482) is plain prose with no link and no dfn, which the architect default permits (plan D3); 'fill' (line 64) and 'mark-to-market value' (line 97) are plain dfn without data-concept (skipped by check_dag, BUILDER_RULES §2.1 item 5); market-making-game dfn (line 60) is in its assigned lesson; link targets (expected-value-game L03, market-maker, bid-ask-spread, limit-order-book, expectation) are in the closure. check_dag PASS.")
r("L04-A1-project-consistency", "2.9-prose", "L04.html line 72 and line 83 vs project.html lines 53-57, 76-81", "PASS",
  "The project uses the same constants (HORIZON 20, START 10000, MOVE 5, LIMIT 10, HALF_SPREAD 10, MAX size 5) and the same arrival draw (below 0.25 uninformed buy, below 0.5 uninformed sell, else informed; project lines 91-98); its hypothesis (line 57) reports 9 fills, -9950, inventory 1, settlement 9980, P&L 30, the same as L04 stdout.")
r("L04-footer-registry-claim", "2.1-citations", "L04.html lines 725-727 (references), 736 (footer)", "PASS",
  "No registry key cited; <ol data-references></ol> empty; footer claim (each key result proved or computed by Lab 1, and graded) is accurate for this page.")
r("L04-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py docstring 1-203, code 209-263, 365-414", "PASS",
  "Quotes, cash flows and marks are int cents (Turn dataclass, play()); expectations and variances are Fraction (one_turn_change, fair_move_mark_change); the docstring's 'a printed fraction such as 5/2 is 2.5 cents' matches stdout line 461.")

# ---- Lesson 05 ----
r("L05-def-3.1-markup", "2.9-prose", "L05.html lines 104-107 (Def 3.1), 106 link to concepts.html#monotonic-deque", "PASS",
  "Definition of surviving index matches Prop 3.2 Step A and the code's pop condition (strict > in the survival test, pops on <=); the concept is linked, not redefined (check_dag PASS).")
r("L05-prop-2.1-2.2-remark", "2.4-mathematics", "L05.html lines 85-98 (Prop 2.1, proof, Remark 2.2)", "PASS",
  "Count (n-k+1)(k-1) equals the naive counter on seeds 5 and 6 for k in {1,2,8,32,200} (verify_numbers.out 'formula=' values); Remark 2.2 identity (n-r)r = n^2/4 - (r-n/2)^2 checked by expansion; k=101 maximises at n=200 with count 10000 (verify_numbers.out 'R2').")
r("L05-prop-3.2-correctness", "2.4-mathematics", "L05.html lines 123-133 (Prop 3.2, Steps A, B, C) and pseudocode 113-120", "PASS",
  "Steps A, B, C read; the pseudocode and the lab's deque_maxima agree; the deque output equals brute-force window maxima for every k in 1..20 on seed 5 and for k in {1,2,8,32,200} on seeds 5 and 6, and for k=1,201 and empty input (" + O + "verify_numbers.out 'equal_brute=True', 'windows 1..20 agree').")
r("L05-prop-3.3-bound", "2.4-mathematics", "L05.html lines 135-143 (Prop 3.3 + proof)", "PASS",
  "Comparisons <= 2n for seeds 5 and 6 at every k tested; pushes = n; pops <= n; increasing sequences give exactly n-1 comparisons for all n < 30 and k <= n (" + O + "verify_numbers.out).")
r("L05-remark-3.4-k-range", "2.4-mathematics", "L05.html lines 145-148 (Remark 3.4)", "PASS",
  "For x = (k, k-1, ..., 1, k+1), n = k+1, step k+1 pops exactly k entries for k = 1..7 (" + O + "verify_numbers.out 'Remark3.4 k=...').")
r("L05-example-3.5-trace", "2.4-mathematics", "L05.html lines 150-153 (Example 3.5)", "PASS",
  "Outputs (4,4,5) reproduced (" + O + "verify_numbers.out 'Example 3.5 outputs').")
r("L05-problems-M-P", "2.4-mathematics", "L05.html lines 367-413 (M1-M3, P1-P3)", "PASS",
  "M1 = 21; M2 trace gives (5,5,1,3) (verify_numbers.out 'M2 outputs'); M3 k=1 outputs the input, k=n one output; P1 algebra and n=200 gives k=101 and 10000; P2 argument valid; P3 n-1 (checked for n<30).")
r("L05-E1-E3-numbers", "2.2-numbers", "L05.html lines 417-437 (E1, E3)", "PASS",
  "E1: 169*31 = 5239 and 5239/382 = 13.71 (verify_numbers.out 'E1 ratio'); E3: 2n = 400, 387 <= 400, 194 pops, split bound 194 + 200 = 394 (stdout 331).")
r("L05-E2-seed6-numbers", "2.2-numbers", "L05.html lines 424-429 (E2)", "PASS",
  "Seed 6, window 8: outputs equal, naive 1351, deque 350 comparisons, 200 pushes, 197 pops (verify_numbers.out 'seed 6 k=8'; stdout 316-317).")
r("L05-R1-scope-sentence", "2.9-prose", "L05.html lines 442-448 (R1)", "PASS",
  "R1 states a protocol and claims no timing result; the twin imports no time module and prints counts only (page code block import lines 180-185).")
r("L05-R2-R3", "2.4-mathematics", "L05.html lines 449-462 (R2, R3)", "PASS",
  "R2: k = 101, count 10000 (verify_numbers.out). R3: a strictly increasing input removes one back index per step i>=2 and total comparisons n-1 (verified by P3 check).")
r("L05-key-results-grades", "2.3-grades", "L05.html lines 472-477 (six rows)", "PASS",
  "T rows: Prop 2.1, Remark 2.2, Prop 3.2, Prop 3.3, Problem P3 (proved on the page). Row 477 is C naming Lab 1 Part 2 on one seeded sequence, as BLUEPRINT §3 requires for single-sample evidence.")
r("L05-quiz-answers", "2.4-mathematics", "L05.html lines 487-562 (10 items)", "PASS",
  "MC keys: 21; 'Yes, total bound'; n-1; 'last occurrence of ties' (strict survival in Def 3.1); counts not run times; 'No outputs'. Numeric keys: 400, 10000, 5, 1351 (structure_counts.out). All correct.")
r("L05-misconceptions-canon-breaks", "2.9-prose", "L05.html lines 336-358 (canon breaks, misconceptions)", "PASS",
  "Three misconceptions (346-358) and canon breaks (337-340): per-step cost k vs total 2n (Remark 3.4 and Prop 3.3, verified); counts not run times; one sequence is not proof. Statements true.")
r("L05-structure-hours", "2.9-prose", "L05.html header data-hours=6; sections lines 52-569", "PASS",
  "data-hours=6; order: why it matters (52), sections 1-3 with lab inline (54-160, lab 161), canon (336), misconceptions (344), problem set (362), key results (466), quiz (483), references (565). 12 problems (3 per tier), 3 misconceptions, 10 quiz items, 6 key rows. why-it-matters is 94 words (" + O + "prose_scan.out).")
r("L05-markup-raw-less-than", "2.9-prose", "L05.html prose outside pre and script", "PASS",
  "Inequalities in prose are written &lt; (e.g. line 106 'i-k&lt;j'); check_pages and page_smoke PASS (" + O + "check_pages.out, page_smoke_L456.out).")
r("L05-meta-uses-hash-map-heap", "2.9-DAG", "L05.html line 38 (Uses row), lines 157-158 (Remark 3.6)", "PASS",
  "Hash map and binary heap are linked closure concepts (CS2); Remark 3.6 says a hash map keeps no order and states the heap's comparison bound only, and line 157 says it 'does not consider any other use of a hash map'.")
r("L05-meta-uses-other", "2.9-DAG", "L05.html lines 38-39 and in-text terms", "PASS",
  "big-O, monotonic deque and unit test are used in Def 1.1 step 3, Section 3 and Problem set; each is linked to CS2/CS1 in the closure.")
r("L05-why-it-matters-comparisons", "2.2-numbers", "L05.html line 52 (why it matters)", "PASS",
  "'at most twice the input length in comparisons' is Prop 3.3 (2n); the 'exactly' count is Prop 2.1; word count 94 (<=120).")
r("L05-footer-registry-claim", "2.1-citations", "L05.html lines 567-569 (references), 578 (footer)", "PASS",
  "No registry key cited; footer claim matches the page.")
r("L05-DAG-links", "2.9-DAG", "L05.html links at lines 38, 106, 157-158; lesson nav 573-574", "PASS",
  "All concept links are to closure concepts (concepts.html anchors) and the Previous/Next links are L04 and L06; no later-defined concept is used; check_dag PASS.")
r("L05-card-PC3-c092", "2.7-cards", "cards.json PC3-c092 (L05 Remark 3.4 card)", "PASS",
  "Front and back match Remark 3.4 (line 147): all k entries removed at step k+1 (verify_numbers.out 'Remark3.4').")
r("L05-card-PC3-c096-grade", "2.7-cards", "cards.json PC3-c096 (grade T)", "PASS",
  "1351 = (200-8+1)(8-1) by Prop 2.1; grade T correct because the count is derived on the page.")
r("L05-card-PC3-c097-grade", "2.7-cards", "cards.json PC3-c097 (grade T)", "PASS",
  "5239 = (200-32+1)(32-1) = 169*31 by Prop 2.1; grade T correct.")

# ---- Lesson 06 ----
r("L06-prop-1.1-payoff-identity", "2.4-mathematics", "L06.html lines 58-66 (Prop 1.1 + proof), key row 448", "PASS",
  "(s-K)^+ - (K-s)^+ = s-K checked on the integer grid -5..5 for both (" + O + "verify_numbers.out 'Prop 1.1 payoff identity ... True'); cases in the proof re-derived.")
r("L06-remark-1.2-put-call-parity", "2.1-citations", "L06.html lines 68-71 (Remark 1.2); linked FC2 put-call parity", "PASS",
  "The linked FC2 definition (course/modules/FC/FC2/L05.html, id def-put-call-parity) states C - P = S - e^{-r tau} K under A1-A5; with D = e^{-r tau} (A2, line 83) that is S - DK. The page says 'under that module's assumptions' and does not re-derive. Not an attribution to a registry key.")
r("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "L06.html line 73 (NPV formula); linked CF1 definition (course/modules/CF/CF1/L01.html, id def-net-present-value)", "PASS",
  "The linked CF1 definition is NPV(r) = sum_{t=0}^{n} C_t/(1+r)^t, identical to line 73; the page uses it without redefinition.")
r("L06-prop-2.1-forward", "2.4-mathematics", "L06.html lines 79-99 (A1-A5, Prop 2.1 + proof)", "PASS",
  "(i) zero cost (-S + S), payoff F' - S/D independent of S_tau; (ii) both reverse arguments valid under A4 and A5; check M1: 4900/0.98 = 5000, payoff 50 (verify_numbers.out 'M1 payoff').")
r("L06-remark-2.2-continuous-convention", "2.1-citations", "L06.html lines 101-104 (Remark 2.2); linked FC2 L02 def-cost-of-carry-forward-price", "PASS",
  "The linked FC2 definition states F* = S e^{r tau}, the same as S/D with D = e^{-r tau}; the statement that D is taken as a rational input is consistent with the lab (D = 97/100).")
r("L06-corollary-3.3-grade", "2.3-grades", "L06.html lines 130-137 (Corollary 3.3 statement at 132; proof at 137), card PC3-c112", "FAIL",
  "The round-14 defect is fixed: the statement now requires the whole interval [l,h] to lie strictly on one side of u* (h < u* or l > u*), and the proof's condition is the same. The new sentence 'A range with an end exactly at u* does not fix the sign, because that end has NPV=0' is false for the degenerate range l = h = u*: Prop 3.2 admits one factor with l_1 = h_1 = 399300/331 (0 < l <= h), so the only admissible value is u* with NPV(u*) = mA(u*-u*) = 0 everywhere on the range. That range has a fixed sign (zero). Verifier check: " + S + "extra_checks.py (" + O + "extra_checks.out) gives sign 0 at both ends of the point range. The claim is graded T and is therefore over-stated.",
  fix="At line 132 replace 'A range with an end exactly at u* does not fix the sign, because that end has NPV=0.' by 'A range of positive width with an end exactly at u* does not fix the sign, because the NPV is zero at that end and nonzero at the other end.' Make the same change in the back of card PC3-c112 (course/modules/PC/PC3/cards.json line 957).")
r("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "L06.html lines 120-128 (Prop 3.2 + induction proof)", "PASS",
  "Induction step: P_{k-1} in [L, H] with L, H > 0 and x_k in [l_k, h_k] gives P_{k-1} x_k in [L l_k, H h_k]; ends attained by choosing each factor at one end. Re-derived; the example bounds 200 and 1600 are reproduced (verify_numbers.out 'Fermi bounds').")
r("L06-example-4.2-numbers", "2.2-numbers", "L06.html lines 147-150 (Example 4.2)", "PASS",
  "Units range [200, 1600] (2000*1*0.1, 4000*2*0.2); A = 3310/1331 (exact sum (1210+1100+1000)/1331); u* = 399300/331 = 1206.3444 (about 1206.34); NPV(200) = -16655000000/1331 < 0, NPV(1600) = 6515000000/1331 > 0 (verify_numbers.out); the range straddles u*, so Corollary 3.3 applies as the page says.")
r("L06-remark-4.3-sensitivity", "2.2-numbers", "L06.html lines 152-155 (Remark 4.3)", "PASS",
  "Unrounded break-evens 1164.100542, 1206.344411, 1249.046942 (verify_numbers.out); four-decimal values 1164.1005, 1206.3444, 1249.0469 as stated; differences from the four-decimal values 42.2439 -> 42.24 and 42.7025 -> 42.70 (exact differences 42.2439, 42.7025 as well); A at 8/10/12 percent 2.5770970, 2.4868520, 2.4018313 (7 dp, verify_numbers.out); 3000 = 15000000/5000; NPV at 200 negative and at 1600 positive at all three rates (verify_numbers.out floats; stdout lines 302-304 also agree).")
r("L06-E2-first-negative", "2.2-numbers", "L06.html lines 401-405 (E2)", "PASS",
  "Grid points above 1206.34 are 1300, 1400, 1500, 1600 (four), and 1200 is the largest negative point (verify_numbers.out 'grid positive/negative points'); NPV(1200) = -105000000/1331 = -78888.05 and NPV(1300) = 1550000000/1331 = 1164537.94 (verify_numbers.out 'E2 NPV' lines).")
r("L06-E1-12pct", "2.2-numbers", "L06.html lines 393-398 (E1)", "PASS",
  "A(12%) = 2.4018313 (7 dp; unrounded 2.40183127); 3000/A = 1249.0469 (unrounded 1249.046942), displayed 1249.05, matching stdout line 304.")
r("L06-E3-42.71", "2.2-numbers", "L06.html lines 407-413 (E3)", "PASS",
  "Width 1249.0469 - 1164.1005 = 84.9464 -> 84.95; 84.9464/4 = 21.2366 -> 21.24; 1206.3444 - 1164.1005 = 42.2439 -> 42.24; 1249.0469 - 1206.3444 = 42.7025 -> 42.70; 1249.05 - 1206.34 = 42.71 (not the answer), as stated (verify_numbers.out).")
r("L06-E3-rest-and-quiz-q9", "2.2-numbers", "L06.html line 411 (E3), quiz item 9 (lines 519-523)", "PASS",
  "Quiz key 21.24 with tolerance 0.01 against 21.2366: difference 0.0034 is within tolerance; the explanation '84.9464/4 = 21.2366' is correct.")
r("L06-M1-M3-numbers", "2.2-numbers", "L06.html lines 345-361 (M1-M3)", "PASS",
  "M1: 4900/0.98 = 5000, payoff 50; M2: NPV = 500/121 = 4.13 (verify_numbers.out 'M2 NPV'); M3: u* = 33275/331 = 100.53 (verify_numbers.out 'M3').")
r("L06-P1-P3-proofs", "2.4-mathematics", "L06.html lines 370-388 (P1-P3)", "PASS",
  "P1 reverse portfolio: cost +S - S = 0 and payoff S/D - F' in every state; P2 affine argument valid (slope mA > 0); P3 bounds 200 and 1600, endpoints attained (line 386).")
r("L06-R1-R3", "2.4-mathematics", "L06.html lines 418-438 (R1-R3)", "PASS",
  "R1: each factor ratio 2 so log-width ln 2 each (verify_numbers.out 'R1'); R2 closed form u* = I / sum m_t(1+r)^-t with positivity noted; R3: m* = 15000000*1331/(1600*3310) = 2495625/662 = 3769.83 cents, ratio 3993/5296 = 0.7540, fall 24.60 percent (verify_numbers.out 'R3').")
r("L06-quiz-answers", "2.4-mathematics", "L06.html lines 463-533 (10 items)", "PASS",
  "Numeric keys: 5000; 4.13 (tolerance 0.005; 500/121 = 4.1322); 1206.34 (tolerance 0.005); 4 positive grid points; 21.24 (tolerance 0.01; 21.2366). MC keys: F' - S/D in every state; S/D with no expectation; 'nothing' decided by the range; rises strictly; balance-sheet cash (AC1 L03 line 57). All correct (" + O + "structure_counts.out).")
r("L06-canon-breaks-and-misconceptions", "2.9-prose", "L06.html lines 310-312 (canon breaks), 318-333 (misconceptions)", "PASS",
  "Payoff 0 and 100 at the two quotes (stdout 287-289); 21.24 average over four points (verify_numbers.out); bounds 200 and 1600 have opposite signs (stdout 293-298); the sign at the bounds is the same at 8, 10, 12 percent (stdout 302-304); 8 = 1600/200 = 2 x 2 x 2, one factor of each of three ranges doubled (Example 4.2, L06.html line 149). The canon-break claims are model limits, not numbers.")
r("L06-articulation-claim-linked", "2.1-citations", "L06.html line 75 and quiz item 10 (lines 525-531) vs course/modules/AC/AC1/L03.html line 57 (def-statement-articulation)", "PASS",
  "The linked AC1 definition states 'the cash-flow statement ends at the balance-sheet cash'; the L06 use matches. Correction of round-14 evidence: the definition is in AC1/L03.html line 57, not AC1/L08.html.")
r("L06-footer-registry-claim", "2.1-citations", "L06.html lines 538-540 (references), 549 (footer)", "PASS",
  "No registry key cited; data-references empty (line 539); footer claim matches the page.")
r("L06-structure-hours", "2.9-prose", "L06.html header data-hours=6; sections lines 52-546", "PASS",
  "data-hours=6; order: why it matters (52), sections 1-4 with lab inline (54-156, lab 157), canon (308), misconceptions (315), problem set (337), key results (442), quiz (459), references (536). 12 problems (3 per tier), 4 misconceptions, 10 quiz items, 6 key rows; why-it-matters 86 words (" + O + "prose_scan.out).")
r("L06-DAG-and-cross-links", "2.9-DAG", "L06.html lines 38-39, 56, 75, 545; L01.html id def-fermi-estimation", "PASS",
  "Links: FC2 forward-contract and cost-of-carry (FC2 L02), put-call-parity (FC2 L05), CF1 net-present-value (CF1 L01), AC1 statement-articulation (AC1 L03), and L01.html#def-fermi-estimation (exists). Nothing from L04 or L05 is used. check_dag PASS.")
r("L06-why-it-matters-scope", "2.9-prose", "L06.html line 52 (why it matters)", "PASS",
  "The four claims (forward price proof, payoff identity, break-even derivation, Remark 4.3 sensitivity) each point to content on the page; 86 words (<=120).")
r("L06-lab-docstring-money-integer", "2.5-labs", "tests/labs/PC3/lab-PC3-L06-1.py docstring 1-177, code 186-283", "PASS",
  "Prices and outlay are int cents; values are Fraction; half_up applies once at display, toward +infinity (floor(x*scale + 1/2) with sign handled; for x = -12513148.009 it displays -12513148 as stdout line 298 shows). Docstring statements (97/100 input, 15000000 cents, 5000 margin, 3 years, rate 10%) match the code.")
r("L06-card-PC3-c148-grade", "2.7-cards", "cards.json PC3-c148 (grade T, basis Problem E1 and Remark 4.3)", "PASS",
  "1249.05 at 12 percent: 3000/A = 1249.0469 (verify_numbers.out); grade T is correct because the value is derived on the page from Prop 3.1.")
r("L06-card-PC3-c151", "2.7-cards", "cards.json PC3-c151 (grade T, basis Problem E3)", "PASS",
  "(1249.0469 - 1164.1005)/4 = 21.2366, displayed 21.24 (verify_numbers.out); grade T correct.")

# ---- cards ----
r("card-full-scan-L04", "2.7-cards", "cards.json, all 39 L04 cards (PC3-c062..c083, c137..c141, c153..c154, c162..c164, c168, c171, c174..c176, c185..c186)", "PASS",
  "Every front and back read in full (" + O + "cards_L456_dump.txt lines 4-84, 199-213, 244-248, 250-288, 313-318); each checked against the lesson text; numbers in cards appear in the lesson (" + O + "cards_check.out: 0 missing); grades T/C with basis agree with the lesson.")
r("card-full-scan-L05", "2.7-cards", "cards.json, all 29 L05 cards (PC3-c084..c101, c142..c146, c169..c170, c177, c180..c182)", "PASS",
  "All 29 read in full (" + O + "cards_L456_dump.txt lines 70-123, 214-228, 271-306, 289-291, 298-306); each checked against the L05 text and outputs.")
r("card-full-scan-L06", "2.7-cards", "cards.json, all 38 L06 cards (PC3-c102..c127 except c118, c147..c151, c165..c167, c178..c179, c183..c184, c187)", "FAIL",
  "All 38 read in full. 37 agree with the lesson text and carry the proposition hypotheses where they state a proposition. PC3-c112 (cards.json lines 954-957) repeats the degenerate-boundary error of row L06-corollary-3.3-grade ('A range that lies wholly on one side ... does fix it' is fixed, but the new back still says 'A range with an end exactly at u* does not fix the sign, because that end has NPV zero').",
  fix="Fix card PC3-c112 back as in row card-PC3-c112-corollary-boundary.")
r("card-PC3-c112-corollary-boundary", "2.7-cards", "course/modules/PC/PC3/cards.json line 957 (PC3-c112 back)", "FAIL",
  "Back: '... The sign is fixed when the whole interval [l, h] lies strictly on one side of the break-even, that is h < u* or l > u*, ... A range with an end exactly at u* does not fix the sign, because that end has NPV zero.' The last sentence is false for the point range l = h = u* (NPV zero everywhere on it; " + O + "extra_checks.out).",
  fix="Replace the last sentence by 'A range of positive width with an end exactly at u* does not fix the sign, because the NPV is zero at that end and nonzero at the other.' (same change as line 132 of L06.html).")
r("card-duplicate-scan", "2.7-cards", "cards.json, all 106 L04-L06 cards", "PASS",
  "cards_check.py (" + O + "cards_check.out): 182 unique ids across the unit; near-duplicate fronts (difflib ratio >= 0.85): c096/c142, c097/c145, c110/c183, c110/c184, c116/c148, c117/c150, c138/c140, c181/c182. Each pair asks a different fact (naive vs deque counts; different Prop 3.1 claims; 8% vs 12%; 200 vs 1600 units; final inventory vs P&L; removals vs comparisons). No card is a duplicate.")
r("card-key-results-agreement", "2.7-cards", "cards.json L04-L06 cards vs key-results tables L04.html 620-625, L05.html 472-477, L06.html 448-453", "PASS",
  "Grades on cards agree with the key-results rows that mirror them (dump lines above): T for proved results, C for lab-read values (c075, c077, c101, c117, c119, c121, c123, c137-c146, c149, c150).")
r("card-number-in-lesson", "2.7-cards", "cards.json numbers vs own lesson text and lab output", "PASS",
  "cards_check.py: 0 card numbers missing from their own lesson page (small integers excluded; " + O + "cards_check.out). The exact -16655000000/1331 of card c117 appears in the L06 expected block at HTML line 298.")
r("card-cite-empty", "2.1-citations", "cards.json L04-L06 'cite' fields", "PASS",
  "All 106 cards have cite []; no registry key is cited, and none is claimed.")
r("card-PC3-c187-articulation", "2.7-cards", "cards.json PC3-c187 (new this round, L06)", "PASS",
  "Front and back match L06.html line 75 and AC1 L03 line 57; the card states no result of its own and makes no claim beyond the prerequisite's identity; no grade, which is acceptable for an identity taken from a prerequisite.")
r("card-PC3-c081-basis-H2", "2.7-cards", "cards.json PC3-c081 basis (changed to hypothesis H2)", "PASS",
  "Basis now cites H2 (the quote is fixed), which is the hypothesis the content depends on (L04.html line 129). The round-14 judgement is resolved.")
r("delta-r14-hunks-L04-L06-cards", "2.10-delta", "git diff 8e5751c9..d1e65a0 (round-14 pin to this pin): L04.html lines 65, 83, 483-484; L06.html lines 132, 154, 310-312, 324, 411, 429; cards.json c081, c112, c187", "PASS",
  "Every hunk in the slice was read and re-verified: L04 l.65 (fill definition), l.83 (Remark 1.2 'by A5'), l.483-484 (canon breaks) are correct; L06 l.154 (Remark 4.3), l.310-312 (canon), l.324 (misconception), l.411 (E3), l.429 (R2 positivity) are correct; L06 l.132 (Corollary 3.3) is the FAIL row above; cards c081 and c187 pass; c112 is the FAIL row above.")
r("delta-r14-twins-unchanged", "2.10-delta", "git diff 8e5751c9..d1e65a0 -- tests/labs/PC3", "PASS",
  "The diff stat for the three slice twins is empty (no change), so the twins are byte-identical to the round-14 pin; they were nonetheless re-run and compared (twin rows above).")
r("delta-r15-L05-unchanged", "2.10-delta", "git diff 8e5751c9..d1e65a0 -- course/modules/PC/PC3/L05.html", "PASS",
  "L05.html is byte-identical to the round-14 pin; it was nevertheless re-read in full and every L05 row above is re-derived by this verifier (not carried).")

fragment = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 15 (did not build PC3)",
    "pin": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa",
    "base": "8e5751c9 (round-14 pin). Delta 8e5751c9..d1e65a0 in this slice: L04.html (lines 65, 83, 483-484), L06.html (lines 132, 154, 308-321, 411, 429), cards.json (c081, c112, new c187). L05.html and the three slice twins are byte-identical to the round-14 pin. No PASS row is carried from the round-14 fragment: every row was re-derived by this verifier from the pin.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE15-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE15-PC3-b/ledgers/PC3/scripts/PC3-b-r15/out",
    "verified_at": "2026-11-09T01:33:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Checkout note: the worktree was at 9ca1d8cb when this round began; it was moved to the stated pin d1e65a0 with git checkout --detach (no other change).",
        "Mutation testing: not applicable to this slice (the slice is lab twins and cards; project graders belong to another slice). mutants is empty; no mutant was written or killed.",
        "Carried rows: none. The round-14 fragment was used only as context; its PASS rows were not trusted and each subject was re-verified (the L05 subject is byte-identical to the round-14 pin, and it was nevertheless re-read and re-derived).",
        "Defect class found this round: a T-graded corollary whose new wording is false at a degenerate point range (l = h = u*). It is a one-clause fix (rows L06-corollary-3.3-grade, card-PC3-c112-corollary-boundary).",
        "Judgement (not a row): Section 5 of L04 and L06 describes real-market features (limit-order-book queues; income, borrowing and short-sale costs in real assets) without a grade or registry key. They are model-limit prose under the plan (no reference admitted). The architect may want a grade on them; the verifier does not fail them on that ground.",
        "Judgement (not a row): 'adverse selection' appears twice in L04 (lines 158, 482) and in card PC3-c176, although plan D3 says 'used once'. The architect default permits prose use with no link or dfn, so accepted.",
        "Not checked: the Pyodide browser runtime beyond page_smoke's own run; the visual layout at 360 px (page_smoke's width check is the only evidence); the linked prerequisite modules beyond the definitions cited above; the registry (no key is cited in this slice); the project grader, project page and hub (other slices); tests/test_docs_figures.py (not in the slice's gates); a mutation run (not applicable)."
    ],
    "summary": "Slice b (L04-L06, twins, 106 cards). 3 FAIL rows, all on one defect: the Corollary 3.3 sentence 'a range with an end exactly at u* does not fix the sign' (L06.html line 132, card PC3-c112 back) is false for the degenerate point range l = h = u*. Every computed number, every lab output, every twin, and every other card checked out. Fix: add 'of positive width' to that sentence in both places.",
}

with open("ledgers/PC3/PC3-b.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows:", len(rows), "pass:", sum(1 for x in rows if x["status"] == "PASS"),
      "fail:", sum(1 for x in rows if x["status"] == "FAIL"))
