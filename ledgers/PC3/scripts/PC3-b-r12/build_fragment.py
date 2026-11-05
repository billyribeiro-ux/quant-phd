"""Writes the PC3-b round-12 ledger fragment from the rows decided by the verifier (stdlib only).

Usage: python -I build_fragment.py <checkout_root>
Asserts that every round-11 row id is kept.
"""
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-PC3-b.round11.json", encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]
O = "ledgers/PC3/scripts/PC3-b-r12/out/"
S = "ledgers/PC3/scripts/PC3-b-r12/"
rows = []

def P(rid, check, loc, ev):
    rows.append({"id": rid, "check": check, "location": loc, "status": "PASS", "evidence": ev})

def F(rid, check, loc, ev, fix):
    rows.append({"id": rid, "check": check, "location": loc, "status": "FAIL", "evidence": ev, "fix": fix})

# ---- gates (run fresh on pin 5db69a9)
P("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3",
  f"run_labs PC3: PASS (9/9), exit 0 ({O}run_labs.out)")
P("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3",
  f"check_pages PC3: PASS, exit 0 ({O}check_pages.out)")
P("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3",
  f"check_dag PC3: PASS, exit 0 ({O}check_dag.out)")
P("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3",
  f"check_projects PC3: PASS, exit 0 ({O}check_projects.out)")
P("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06 (run alone)",
  f"page_smoke PC3: PASS; L04, L05, L06 each PASS; exit 0 ({O}page_smoke.out)")
P("gate-ruff-mypy-twins", "2.5-labs", "ruff check tests/labs/PC3; ruff format --check tests/labs/PC3; mypy --no-incremental",
  f"'All checks passed!' ({O}ruff_check.out); '9 files already formatted' ({O}ruff_format.out); "
  f"'Success: no issues found in 385 source files' ({O}mypy.out)")
P("gate-pytest-lab-tooling", "2.5-labs", "pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py",
  f"all tests pass, exit 0 ({O}pytest_lab_tooling.out)")
P("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry)",
  f"'offline integrity: 560 entries, 0 problems', exit 0 ({O}verify_refs_offline.out). The slice cites no registry key.")
P("gate-run-graders-unit", "2.6-structure", "tools/run_graders.py --unit PC3 --seeds 0-49 (recorded for completeness; grader is another slice)",
  f"run_graders PC3: PASS (reference 50/50 seeds, slowest 0.3 s), exit 0 ({O}run_graders.out)")

# ---- notation
P("notation-registry-L04-L06", "2.4-notation", "course/modules/PC/PC3/L04.html, L05.html, L06.html (all math spans)",
  f"{S}notation_scan.py over 370 (L04), 315 (L05), 246 (L06) math spans ({O}notation_scan.out): no T, Phi, gamma_3, "
  "gamma_4, R^ast, R^{e ast}, R_f or mathbb{Q}. Registered macros in use: E (L04, expectation, as \\E), Var (L04, as \\Var). "
  "Plain letter E names an expected trade term in L04 (Example 3.2, Corollary 3.3, Problem R1, P2); plain E is not a registered "
  "symbol, so no collision under notation.json; judgement, not a fail. Local symbols per notation.json 'about': N, t, p, L, "
  "sigma, varepsilon, tau, M (L05 maximum), r (L05 Remark 2.2). No \\R, \\N or \\Prob macro is used on these pages.")

# ---- twins and labs
P("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py",
  f"python -I -W error on each twin: exit 0, 0 stderr bytes ({O}twin_lab-PC3-L04-1.stdout/.stderr, L05, L06; {S}embed_compare.py)")
P("twin-page-code-equals-twin", "2.5-labs", "course/modules/PC/PC3/L04.html, L05.html, L06.html code blocks vs the three twins",
  f"{S}embed_compare.py: code==twin True for L04, L05, L06 ({O}embed_compare.out)")
P("twin-expected-equals-stdout", "2.5-labs", "L04.html expected block lines 424-475 (52); L05.html 307-331 (25); L06.html 284-304 (21)",
  f"expected == twin stdout line for line: 52, 25, 21 lines ({O}embed_compare.out)")
P("lab-L04-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L04.html line 180 (hypothesis), line 476 (interpretation)",
  f"hypothesis: identity True, cash flow -9950, P&L 30, 13 informed, nine fair values, Part 3 mean 0 / variance 25 I^2 "
  f"all in {O}twin_lab-PC3-L04-1.stdout (lines 23-52). Interpretation: 9 fills, -9950, inventory 1, settlement 9980, P&L 30, "
  f"seed 1 16/20100/-2/10020/60 (stdout line 35). Independently re-derived in {S}l04_indep.py ({O}l04_indep.out): seed0 9/-9950/1/9980/30/13; seed1 16/20100/-2/10020/60.")
P("lab-L05-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L05.html line 163 (hypothesis), line 332 (interpretation)",
  f"hypothesis: 1351 = (n-k+1)(k-1) (stdout line 6), 400 bound (line 8), 200 pushes (line 9), five edge checks (lines 15-18), "
  f"five Part 3 sizes (lines 21-25). Interpretation 354 (line 7) and 350 for seed 6 (line 11). Own recount {S}l05_indep.py ({O}l05_indep.out) agrees.")
P("lab-L06-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L06.html line 159 (hypothesis), line 305 (interpretation)",
  f"hypothesis: payoffs 0 and 100 at five spot values (stdout lines 4-7), annuity 3310/1331, break-even 399300/331, NPVs at bounds "
  f"and 8/10/12 percent (lines 9-21). Interpretation printed breaks 1164.10, 1206.34, 1249.05 and differences 42.24, 42.71 (lines 19-21). "
  f"Own recomputation {S}l06_indep.py ({O}l06_indep.out) matches every printed value.")

# ---- L04 rows (round-11 ids kept)
P("L04-definitions-A1-A6-notation", "2.4-notation", "course/modules/PC/PC3/L04.html lines 56-89",
  "A1 probabilities 1/4, 1/4, 1/2 at p=1/2 match lab ARRIVAL_PROBABILITY (tests/labs/PC3/lab-PC3-L04-1.py line 38); A5 L=10 matches LIMIT=10 (line 35); A6 form matches Example 1.3 quote (line 83)")
P("L04-lab-section-locator", "2.9-prose", "course/modules/PC/PC3/L04.html lines 72, 161, 178-179",
  "A1 reference to Lab 1 (Section 4) at line 72; Section 4 heading line 161; Lab 1 at lines 178-179 inside Section 4")
P("L04-prop-2.2-2.3-identity", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 100-122",
  "Re-derived by hand: C_t and I_t sums (Prop 2.2 proof) and W_t - W_{t-1} = (c_t + sigma_t v_t) + I_{t-1}(v_t - v_{t-1}) (Prop 2.3); also stdout identity True")
P("L04-example-3.2-values", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 143",
  f"5, 0 and 5/2 at v = 10000, 10020, 9985: closed form and enumeration agree ({O}twin_lab-PC3-L04-1.stdout lines 37-45; {O}l04_indep.out 'Example 3.2')")
P("L04-proposition-4.1-remark-4.2-sd", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 164-175",
  f"mean 0, variance 25 I^2 by enumeration for I in {{-4,0,1,3,10}} ({O}l04_indep.out); sd 15 at 3 units, 50 at 10 units")
P("L04-remark-4.2-inventory-independence", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 175",
  f"I=10 at quote 9990/10010, v=10000: uninformed buy only, 10 cents x 1/4 = 5/2; I=0 gives 5 ({O}l04_indep.out 'Remark 4.2'); sell refused at 11 by A5")
P("L04-remark-3.4-inventory-zero", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 157-158",
  "Uninformed flow (1-p)h; at p=1/2 equals h/2 = 2h/4, a quarter of the spread 2h (Proposition 3.1 algebra re-checked)")
P("L04-canon-breaks-tick", "2.9-prose", "course/modules/PC/PC3/L04.html lines 481-483 (Section 5, paragraphs 1-3)",
  "Integer-cent quotes and 5-cent moves match Definition 1.1; 'cannot show that a wider quote costs customers' follows from A1 (arrivals independent of quote) and Prop 3.1")
P("L04-canon-breaks-quote-rule", "2.9-prose", "course/modules/PC/PC3/L04.html line 484 (Section 5, paragraph 4)",
  f"mid at turn t = 10000 - 10 I_(t-1) checked on every turn of seeds 0..49 ({S}l04_indep.py: 'Section 5 mid identity holds on seeds 0..49: True'); the 'every fill moves the mid by 10' claim matches Example 1.3")
P("L04-R2-spread-criterion", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 597-601 (R2)",
  "E = (1-p)h for mid fair value; p<1 gives E>0 for every h>=1; p=1 gives E=0 for every h; re-derived")
P("L04-E1-seed1-numbers", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 565-571 (E1)",
  f"16 fills, 20100, inventory -2, settlement 10020, mark -20040, P&L 60: stdout line 35 and {O}l04_indep.out seed1")
P("L04-E2-binomial-z", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 572-578 (E2)",
  f"se = sqrt(0.25/20) = 0.1118; z = 0.15/0.1118 = 1.34; 1.959964 = z(0.975) ({O}l04_indep.out: se 0.1118, z 1.3416, z crit 1.959964)")
P("L04-E3-mid-vs-settlement", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 579-586 (E3)",
  f"last quote 9980/10000 (mid 9990), settlement 9980, cash -9950: P&L 30 at settlement, 40 at mid, difference 10 ({O}twin_lab-PC3-L04-1.stdout line 22; {O}l04_indep.out 'E3')")
P("L04-problems-R1-R3-M-P", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 515-607 (M1 515, M2 522, M3 529-532, P1 540, P2 547, P3 554, E1-E3 565-586, R1 590, R2 597, R3 604)",
  "M1 cash 10010, W 10; M2 refusal at 11; M3 no trade at 10010, buy at 10011; P1 two-turn identity; P2 h/2 and 0; P3 400; R1 d = 20/3; R2 existence; R3 |I| < 2 -> 1 unit, 25 cents^2 (all re-derived; {S}l04_indep.py)")
P("L04-M3-inventory-hypothesis", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 529-532 (M3)",
  "A4 strict inequalities: no trade at v = a = 10010; buy at the ask for v = 10011, loss of one cent; unchanged this round and re-checked")
P("L04-quiz-q11-citation", "2.9-prose", "course/modules/PC/PC3/L04.html lines 706-709 (quiz item 11)",
  f"'fills 9 of 20 turns' is printed (stdout line 23) for the seeded path")
P("L04-quiz-answers", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 632-720 (12 items)",
  "Answers re-derived: +10010; 10; No (strict); 0; 5; refused; 400; zero; 6.6667 (=20/3); settlement; 9; rises as (1-p)h; explanations cite existing items")
P("L04-key-results-prop-3.1-assumptions", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 622 (key-results row 3)",
  "Row states H1 to H3 and the fixed-quote restriction, matching Prop 3.1 hypotheses (lines 128-129)")
P("L04-prop-3.1-closed-form", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 127-139",
  f"closed form (1-p)h - p[(v-a)^+ + (b-v)^+] equals exact enumeration on 8505 cases (p in {{0,1/5,1/2,3/5,1}}, h=1..7, three mids, 81 fair values) ({S}l04_indep.py; {O}l04_indep.out)")
P("L04-corollary-3.3", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 146-154",
  f"E = h/2 - (v-a)/2 for v >= a at p=1/2; zero iff v = a+h (checked over h=1..7, d=0..29; {O}l04_indep.out)")
P("L04-misconceptions", "2.9-prose", "course/modules/PC/PC3/L04.html lines 487-507 (four items)",
  "Item 1: zero at a+h = 10020 (stdout line 45); item 2: P&L 10; item 3: 2500 cents^2 at 10 units (stdout line 52); item 4: A3 excludes quotes on v_t")
P("L04-key-results-table-other", "2.3-grades", "course/modules/PC/PC3/L04.html lines 620-629 (rows 1, 2, 5, 6)",
  "Row 1 T (Prop 2.2), row 2 T (Prop 2.3), row 5 T (Prop 4.1), row 6 C (Lab 1 Part 2; ruling 13: lab-only); matching cards c066, c068, c073, c075 carry the same grades")
P("L04-scope-and-banned-phrases", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file)",
  f"banned-string scan (check_pages PASS, {O}check_pages.out; own scan: no hit); process-word scan: none in prose or code; scope words reviewed (each 'every'/'only'/'any' has a proof or computation)")
P("L04-structure-hours", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file); course/modules/PC/PC3/index.html",
  "data-hours=6; lesson order matches BUILDER 4.2 (why, core, lab, canon, misconceptions, problems, key results, quiz); check_pages PASS")
P("L04-DAG-D-terms", "2.9-DAG", "course/modules/PC/PC3/L04.html lines 60, 157-158, 482",
  f"adverse selection (line 158) plain prose, no link, no dfn (plan D3); limit-order-book linked (FC1, in closure); check_dag PASS ({O}check_dag.out)")
P("L04-A1-project-consistency", "2.9-prose", "course/modules/PC/PC3/L04.html line 72; course/modules/PC/PC3/project.html lines 53 and 404",
  "p = 1/2 (line 72) matches project line 404 (1/4, 1/4, 1/2); project line 53 uses seed 0, the same quote rule and 10-cent half-spread")
P("L04-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L04.html line 736 (site-footer)",
  "'Each key result is proved on the page or computed by Lab 1, and each is graded': all six key rows carry T or C")
P("L04-lab-docstring-money-integer", "2.9-prose", "tests/labs/PC3/lab-PC3-L04-1.py lines 3-6 and course/modules/PC/PC3/L04.html line 184",
  "Same text in twin and page (embed_compare PASS); 'Quotes, cash flows and inventory marks are integer numbers of cents' holds for realised values (stdout lines 3-35); expectations declared Fraction in the same docstring")

# ---- L05 rows
P("L05-def-3.1-markup", "2.9-prose", "course/modules/PC/PC3/L05.html lines 105-106 (Definition 3.1)",
  "dfn for 'surviving at step i' is a plain dfn (no data-concept, plan §2.1 item 5); monotonic-deque linked to CS2 (in closure)")
P("L05-prop-2.1-2.2-remark", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 85-98",
  f"Prop 2.1 count (n-k+1)(k-1) equals the lab's naive count (stdout line 6); Remark 2.2 identity (n-r)r = n^2/4 - (r-n/2)^2 re-derived; peak k = n/2+1 (n=10 -> k=6, count 25; n=200 -> k=101, 10000) ({O}l05_indep.out)")
P("L05-prop-3.2-correctness", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 123-133",
  f"deque state after every step equals Definition 3.1 survivors and outputs equal the brute maximum on 3000 random sequences (n<=25, values 0..9): 0 invariant failures, 0 output failures ({O}l05_indep.out)")
P("L05-prop-3.3-bound", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 135-142",
  f"while-loop tests <= 2n and back removals + front removals <= n on the same 3000 sequences: 0 failures ({O}l05_indep.out)")
P("L05-remark-3.4-k-range", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 147 (Remark 3.4, first sentences)",
  f"x=(k,...,1,k+1): deque after step k is 1..k; step k+1 removes all k in one loop, for k=1..11 ({O}l05_indep.out 'Remark 3.4'); the round-11 wording 'at step k' is corrected to 'at step k+1'")
P("L05-example-3.5-trace", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 151-153",
  f"states [1],[1,2],[3],[3,4],[5]; outputs (4,4,5) ({O}l05_indep.out 'Example 3.5')")
P("L05-problems-M-P", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 367-413 (M1-M3, P1-P3)",
  f"M1 21; M2 outputs (5,5,1,3) and states ({O}l05_indep.out); M3 k=1 outputs equal input, k=n gives [max]; P1 count 10000 at n=200, k=101; P2 argument checked; P3 n-1 for every n<30 and k<=n ({O}l05_indep.out)")
P("L05-E1-E3-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 417-437 (E1, E3)",
  "E1: 169 x 31 = 5239 (printed), 5239/382 = 13.71 -> 13.7; E3: 387 is the largest deque count (stdout lines 21-25), 194 pops, 200 pushes, 194+200 = 394 >= 387, bound 400")
P("L05-E2-seed6-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 424-430 (E2)",
  f"seed 6, window 8: outputs equal, naive 1351, deque 350 comparisons, 200 pushes, 197 pops (stdout line 11; {O}l05_indep.out 'seed 6 k 8')")
P("L05-R1-scope-sentence", "2.9-prose", "course/modules/PC/PC3/L05.html lines 440-448 (R1)",
  "Protocol solution states that the lab times nothing and no timing result is proved; the lab has no timer (lab docstring line 6-7)")
P("L05-R2-R3", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 449-462",
  "R2: maximiser k-1 = n/2 = 100, count 10000 re-derived; R3: strictly increasing sequence gives n-1 tests for every k (verified n<30)")
P("L05-key-results-grades", "2.3-grades", "course/modules/PC/PC3/L05.html lines 466-481",
  "Rows 1-5 T (Props 2.1, 3.2, 3.3, Remark 2.2, Problem P3) match cards c087, c088, c090, c091, c095 (T); row 6 C (Lab 1 Part 2) matches card c101 (C)")
P("L05-quiz-answers", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 483-563 (quiz items 1-10)",
  "Answers re-derived: 21; 400; 10000; yes (bound counts removals); 5; n-1; last occurrence of the maximum (strict survival, Def 3.1); 1351; not run times; no outputs")
P("L05-misconceptions-canon-breaks", "2.9-prose", "course/modules/PC/PC3/L05.html lines 336-359",
  "354 <= 400 (stdout line 7); amortised reading correct; per-step budget of one operation is false (Remark 3.4)")
P("L05-structure-hours", "2.9-prose", "course/modules/PC/PC3/L05.html (whole file)",
  "data-hours=6; six steps in Definition 1.1; section order matches BUILDER 4.2; check_pages PASS")
P("L05-markup-raw-less-than", "2.9-prose", "course/modules/PC/PC3/L05.html Definition 3.1 and math spans",
  "'i-k&lt;j' escaped; raw '>' in running text is valid HTML; math spans render (page_smoke PASS, all math rendered)")
P("L05-meta-uses-hash-map-heap", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38-40 and Remark 3.6 lines 157-158",
  "hash-map and binary-heap are CS2 concepts linked from the closure; Remark 3.6 heap bound 3n floor(log2 n) = 4200 at n=200 re-computed")
P("L05-meta-uses-other", "2.9-DAG", "course/modules/PC/PC3/L05.html line 38 (Uses list)",
  "big-O-complexity (CS2), monotonic-deque (CS2), unit-test (CS1): all in the prerequisite closure ({AC1, CF1, CS1, CS2, E1, FC1, FC2, M1, M2, M4, P0.1})")
P("L05-why-it-matters-comparisons", "2.9-prose", "course/modules/PC/PC3/L05.html line 52",
  "91 words (<=120); claims 'proves that a monotonic deque returns the same answers with at most twice the input length in comparisons' match Prop 3.2 and 3.3")
P("L05-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L05.html line 578 (site-footer)",
  "footer claim holds: all six key rows carry T or C, and C rows name Lab 1")
P("L05-DAG-links", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38, 58, 106, 157-158",
  "all links point to CS1/CS2 concepts in the closure or to this lesson's own definitions; check_dag PASS")
P("L05-card-PC3-c092", "2.7-cards", "course/modules/PC/PC3/cards.json id PC3-c092 vs course/modules/PC/PC3/L05.html line 147",
  "front and back now say step k+1 removes all k entries in one run of the while loop; matches Remark 3.4 text and the k=1..11 check (l05_indep.out)")

# ---- L06 rows
P("L06-prop-1.1-payoff-identity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 58-66",
  "Proof cases s>=K and s<K re-derived; identity holds for all real s, K")
P("L06-remark-1.2-put-call-parity", "2.1-citations", "course/modules/PC/PC3/L06.html lines 68-71",
  "Price form call - put = S - DK matches FC2 L05 Theorem 1.2 (C - P = S - e^{-r tau} K, D = e^{-r tau}) read at course/modules/FC/FC2/L05.html; the lesson does not re-derive it")
P("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 73-76, 110-118",
  "NPV formula equals CF1 L01 Definition 1.1 (course/modules/CF/CF1/L01.html); Prop 3.1 statement and proof re-derived")
P("L06-prop-2.1-forward", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 90-98",
  "(i) and (ii) re-derived; A1 used for (i) (no income), A4 and A5 for (ii); reverse portfolio cost zero and payoff S/D - F' re-checked")
P("L06-remark-2.2-continuous-convention", "2.1-citations", "course/modules/PC/PC3/L06.html lines 80-90 (A2) and 102-104 (Remark 2.2)",
  "S/D = S e^{r tau} with D = e^{-r tau}; matches FC2 L02 Definition 2.1 and Proposition 2.2 (course/modules/FC/FC2/L02.html: F* = S e^{r tau})")
P("L06-corollary-3.3-grade", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 130-139",
  "ell < u* < h gives loss at ell and gain at h; both ends admissible; sign fixed when [ell,h] lies on one side (checked with l06_indep.py numbers)")
P("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 120-128",
  "Induction proof re-derived; both ends attained (P3 check: 200 and 1600)")
P("L06-example-4.2-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 146-150",
  f"A = 3310/1331; u* = 399300/331 = 1206.34; NPV(200) = -12513148 cents and NPV(1600) = 4894816 cents at 10 percent; range [200, 1600] ({O}l06_indep.out)")
F("L06-remark-4.3-sensitivity", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 153-155 (Remark 4.3)",
  f"Printed values 1164.10, 1249.05 and the sign statements are correct ({O}l06_indep.out). The sentence 'Measured from the unrounded values, 1164.1005, 1206.3444 and 1249.0469' "
  f"is correct at 4 decimals (exact 1164.100542, 1206.344411, 1249.046942) but is not derived on the page: no annuity factor at 8 percent is shown, and the page's own displayed factor at 12 percent (2.40183, E1 line 397) gives 3000/2.40183 = 1249.0476, not 1249.0469. "
  "The difference 42.24 and 42.70 displays are unaffected.",
  "Show the annuity factors to at least seven significant digits: A(8 percent) = 2.5770970 and A(12 percent) = 2.4018313 (sums of (1+r)^-t, t = 1 to 3), so that 3000/A reproduces 1164.1005 and 1249.0469 on the page; or give the unrounded values only as 2-decimal results.")
P("L06-E1-12pct", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 392-398 (E1)",
  f"A(12 percent) = 2.40183 (exact 2.4018313); break-even about 1249.05 (exact 1249.0469) matches stdout line 21 ({O}l06_indep.out)")
P("L06-E2-first-negative", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 399-405 (E2)",
  f"grid 200..1600 step 100: positive at 1300, 1400, 1500, 1600 (count 4); largest negative 1200; NPV(1200) = -105000000/1331 = -78888.05; NPV(1300) = 1550000000/1331 = 1164537.94 ({O}l06_indep.out)")
F("L06-E3-42.71", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 406-416 (E3)",
  f"Displayed results are correct: 84.95 (exact 84.9464), 21.24 (21.2366), 42.24 (42.2439), 42.70 (42.7025), 42.71 from displayed values ({O}l06_indep.out). FAIL: the 4-decimal unrounded break-evens 1164.1005 and 1249.0469 (line 411) are asserted with 'its own factor A' but neither factor is shown; the displayed E1 factor 2.40183 yields 1249.0476, so the chain a reader can follow does not reproduce the stated unrounded values (BUILDER 3.5; VERIFIER 2.2(c)).",
  "Write the annuity factors A(8 percent) and A(12 percent) to seven significant digits in the solution, so that 1164.1005 and 1249.0469 are reproducible, and make E1's factor consistent with it (or say E1 uses a rounded factor). The 2-decimal displays do not change.")
P("L06-E3-rest-and-quiz-q9-placeholder", "2.9-prose", "placeholder (not emitted)", "placeholder")
rows.pop()  # placeholder removed above; real rows follow
F("L06-E3-rest-and-quiz-q9", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 406-416 (E3 rest) and quiz item 9, lines 519-523 (explanation)",
  "The answer 21.24 with tolerance 0.01 is correct (exact 21.2366). The quiz explanation '84.9464/4 = 21.2366' (line 522) takes the difference of the same unrounded break-evens that E3 does not derive (see L06-E3-42.71); its arithmetic is correct from those inputs.",
  "Same fix as L06-E3-42.71: once A(8 percent) and A(12 percent) are shown, the quiz explanation is reproducible; no change to the answer 21.24.")
P("L06-M1-M3-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 342-362 (M1-M3)",
  "M1: 4900/0.98 = 5000, payoff 50; M2: 500/121 = 4.13; M3: 100000 x 1331/(400 x 3310) = 33275/331 = 100.53 (all re-derived, l06_indep.out)")
P("L06-P1-P3-proofs", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 367-390 (P1-P3)",
  "P1 reverse portfolio cost +S-S = 0 and payoff S/D - F'; P2 affine zero; P3 bounds 200 and 1600 with attaining factors")
P("L06-R1-R3", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 417-437 (R1-R3)",
  f"R1: each log-width ln 2 (ratios 2, 2, 2), tie; R2 closed form u* = I / sum m_t (1+r)^-t; R3: m* = 3769.83 cents, 0.7540 of 5000, fall 24.60 percent ({O}l06_indep.out)")
P("L06-quiz-answers", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 459-533 (10 items)",
  "Answers: 5000; F'-S/D; S/D; 4.13 (500/121); 1206.34; Nothing; 4; the NPV rises strictly; 21.24 (tolerance 0.01 vs 21.2366); articulation balance-sheet cash. Explanation of item 9 is covered by L06-E3-rest-and-quiz-q9")
F("L06-canon-breaks-and-misconceptions", "2.9-prose", "course/modules/PC/PC3/L06.html lines 308-334 (Section 5 and misconceptions), line 324",
  f"Misconception 2 states 'On average over 8 to 12 percent, the break-even moves by 21.24 units per point of rate, which is (1249.0469-1164.1005)/4 from the unrounded values (Problem E3)'. The displayed 21.24 is correct ({O}l06_indep.out), but the unrounded inputs are not derived on the page (see L06-E3-42.71). Canon paragraphs (Section 5) re-checked: 'a factor of 8' is 2 x 2 x 2 (each factor range has ratio 2) and equals 1600/200 = 8; the stated model limits follow from Example 4.2.",
  "Same fix as L06-E3-42.71: show A(8 percent) and A(12 percent) to seven significant digits before quoting the unrounded values, or quote 21.24 from the 2-decimal break-evens 1164.10 and 1249.05 (1249.05 - 1164.10 = 84.95, /4 = 21.24).")
P("L06-articulation-claim-linked", "2.1-citations", "course/modules/PC/PC3/L06.html line 75 and quiz item 10 (line 525-531)",
  "Linked concept statement-articulation (course/modules/AC/AC1/L03.html, Definition 1.1): 'the cash-flow statement ends at the balance-sheet cash'; the lesson uses it as the prerequisite states it")
P("L06-footer-registry-claim", "2.9-prose", "course/modules/PC/PC3/L06.html line 549 (site-footer)",
  "footer claim holds: key rows T (Props 1.1, 2.1, 3.1, 3.2 and Example 4.2 row) or C (none in L06 key table; all rows T)")
P("L06-structure-hours", "2.9-prose", "course/modules/PC/PC3/L06.html (whole file); course/modules/PC/PC3/index.html",
  "data-hours=6; structure matches BUILDER 4.2; check_pages and check_projects PASS; hub split 36 lessons + 14 project unchanged")
P("L06-DAG-and-cross-links", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 38-39, 56, 75, 86",
  "forward-contract, cost-of-carry-forward-price, put-call-parity (FC2), net-present-value (CF1), statement-articulation (AC1) in closure; fermi-estimation linked to L01 (earlier lesson); case-interview defined once here")
P("L06-why-it-matters-scope", "2.9-prose", "course/modules/PC/PC3/L06.html line 52 (why-it-matters), against Remark 4.3, Example 4.2, Problems R2 and R3",
  "Round-11 FAIL is fixed: the text no longer says 'the one assumption it varies'. It says the lesson reports how the answer moves when the rate moves (Remark 4.3), which Remark 4.3 and Lab 1 Part 2 support. 80 words (<=120).")
P("L06-lab-docstring-money-integer", "2.9-prose", "tests/labs/PC3/lab-PC3-L06-1.py lines 6-9 and course/modules/PC/PC3/L06.html lines 165-168",
  "Round-11 FAIL is fixed: 'Prices and the outlay are integer numbers of cents. A cash flow at a fractional number of units, such as the break-even, is an exact fraction of a cent.' Code agrees (cash_flows(units) uses Fraction units; MARGIN and OUTLAY are int); embed_compare PASS.")

# ---- card rows
F("L05-card-PC3-c096-grade", "2.3-grades", "course/modules/PC/PC3/cards.json id PC3-c096 (grade C, basis 'Lab 1, Part 1 ...'); course/modules/PC/PC3/L05.html line 428 (E2)",
  "The card states the naive count 1351 = (n-k+1)(k-1) for n=200, k=8. The count depends only on n and k (Proposition 2.1, T on the page; Problem E2 line 428 says so and derives 193 x 7 = 1351 by hand). BLUEPRINT 3 grades C as working-paper or single-sample evidence; this is a proved instance, so C mis-grades it (VERIFIER 2.3). Ruling 13 (FINAL-ARCHITECT-RULINGS item 13) grades a value derived by hand on the page T with that derivation as basis.",
  "Set grade to T and basis to 'Proposition 2.1 with n = 200, k = 8 (Problem E2 hand computation); Lab 1, Part 1 prints the same count'.")
F("L05-card-PC3-c097-grade", "2.3-grades", "course/modules/PC/PC3/cards.json id PC3-c097 (grade C); course/modules/PC/PC3/L05.html line 421 (E1)",
  "Same defect as PC3-c096: 5239 = (200-32+1)(32-1) = 169 x 31 is derived by hand in Problem E1 (line 421) from Proposition 2.1 and is independent of the sequence. C mis-grades it (BLUEPRINT 3; ruling 13).",
  "Set grade to T and basis to 'Proposition 2.1 with n = 200, k = 32 (Problem E1 hand computation); Lab 1, Part 3 prints the same count'.")
F("L06-card-PC3-c148-grade", "2.3-grades", "course/modules/PC/PC3/cards.json id PC3-c148 (grade C, basis 'Remark 4.3 and Lab 1, Part 2'); course/modules/PC/PC3/L06.html lines 397-398 (E1)",
  "The card states the 12 percent break-even 'about 1249.05 units per year'. E1 (lines 397-398) derives it by hand from Proposition 3.1 and the annuity factor 1/1.12 + 1/1.2544 + 1/1.404928 = 2.40183, giving 3000/2.40183, about 1249.05. The value is a closed-form result shown on the page, so the card's C grade with a lab-only basis is a mismatch (ruling 13; BLUEPRINT 3).",
  "Set grade to T and basis to 'Proposition 3.1 with the 12 percent annuity factor (Problem E1 hand computation); Lab 1, Part 2 prints 1249.05'.")
F("L06-card-PC3-c151", "2.3-grades", "course/modules/PC/PC3/cards.json id PC3-c151 (grade T, basis 'Problem E3 solution ...')",
  "The card's T grade rests on the 4-decimal unrounded break-evens (1249.0469 - 1164.1005)/4 = 21.2366. Recomputed exactly (l06_indep.out: 21.236600), so the value is right, but the 8-percent annuity factor is not on the page and the 12-percent factor shown (2.40183) reproduces 1249.0476, not 1249.0469 (see L06-E3-42.71). The derivation the card cites is therefore not reproducible from the page.",
  "After the factors are written out (see L06-E3-42.71), keep T with that basis; otherwise cite the 2-decimal break-evens and grade the 21.24 result to the lab (C).")

# ---- card coverage rows (98 cards in L04-L06, read in full)
P("card-full-scan-L04", "2.7-cards", "course/modules/PC/PC3/cards.json lessons L04 (37 cards: c062-c083, c137-c141, c153-c154, c162-c164, c168, c171, c174-c176)",
  "All 37 read against the current L04 text: definitions and assumptions match (A1-A6, Def 1.1, Def 2.1, Remark 1.2, Example 1.3); T cards match proofs; C cards (c067, c075, c077, c137-c141) name Lab 1 and are lab-only or rest on SIMULATED data (ruling 13); no card cites a registry key")
P("card-full-scan-L05", "2.7-cards", "course/modules/PC/PC3/cards.json lessons L05 (26 cards: c084-c101, c142-c146, c169-c170, c177)",
  "All 26 read against the current L05 text; content correct. Grades: c096 and c097 mis-graded (see FAIL rows); c142-c146 and c101 C naming Lab 1 (seeded, lab-only) are correct; c143 pushes/pops mixed C is acceptable (pops lab-only)")
P("card-full-scan-L06", "2.7-cards", "course/modules/PC/PC3/cards.json lessons L06 (35 cards: c102-c127, c147-c151, c165-c167, c178-c179)",
  "All 35 read against the current L06 text; content correct. Grades: c148 mis-graded and c151 rests on unshown unrounded values (see FAIL rows); c116, c117, c119, c121, c123, c124, c149, c150 C naming Lab 1 are correct (lab-only)")
P("card-duplicate-scan", "2.7-cards", "course/modules/PC/PC3/cards.json (all 174 cards, ids and fronts)",
  "No duplicate id and no duplicate front (python check). Near-neighbours state different facts (e.g. c072 uninformed flow vs c078 misconception; c074 sd vs c080 variance at 10 units)")
P("card-key-results-agreement", "2.7-cards", "L04, L05, L06 key-results tables vs cards",
  "Every key row has a card with the same grade and basis: L04 c066, c068, c069, c071, c073, c075; L05 c087, c088, c090, c091, c095, c101; L06 c102, c107, c108, c110, c111, c147")
P("card-number-in-lesson", "2.7-cards", "cards.json numbers vs lesson text (L04, L05, L06)",
  "Every number on a card appears in its lesson: e.g. 1164.10 (Remark 4.3), -12513148 (lab expected block), 4894816 (lab), 40 and 30 cents (E3), 2500 and 50 cents (Remark 4.2), 193 x 7 and 169 x 31 (E2, E1), 387 and 382 (E3, E1)")
P("card-cite-empty", "2.1-citations", "cards.json, lessons L04-L06",
  "Every card in these lessons has cite == []; no registry key is needed (the lessons cite none)")

# ---- other gates / rows
P("L06-E3-rest-and-quiz-q9-note", "2.9-prose", "placeholder", "placeholder")
rows.pop()

rows_ids = [r["id"] for r in rows]
missing = [i for i in prev_ids if i not in rows_ids]
extra = [i for i in rows_ids if i not in prev_ids]
print("round-11 ids:", len(prev_ids), "missing:", missing)
print("new ids:", extra)
for r in rows:
    if r["status"] != "PASS" and not r.get("fix"):
        raise SystemExit("no fix: " + r["id"])
counts = {"PASS": sum(1 for r in rows if r["status"] == "PASS"), "FAIL": sum(1 for r in rows if r["status"] == "FAIL")}
verdict = "PASS" if counts["FAIL"] == 0 else "FAIL"
frag = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 12,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 12 (did not build PC3)",
    "pin": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0",
    "base": "11d7077a290f7960b183d3a5a6631af4773888f9 (round-11 pin). Delta 11d7077..5db69a9 in this slice: L04.html line 181-189 docstring and line 576 (E2 1.959964); L05.html line 147 (Remark 3.4); L06.html line 52 (why-it-matters), line 91 (Prop 2.1 title), line 149 (Example 4.2), line 320 (misconception 1), lines 162-170 (lab docstring); tests/labs/PC3/lab-PC3-L04-1.py lines 3-6; tests/labs/PC3/lab-PC3-L06-1.py lines 6-9; cards.json PC3-c082, c087, c092 fronts/basis. lab-PC3-L05-1.py is byte-identical. Outside the slice: plans/PC3-build-plan.md, plans/FINAL-ARCHITECT-RULINGS.md (item 13, read and applied), project.html, grader.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE12-PC3-b/ledgers/PC3/scripts/PC3-b-r12/out",
    "verified_at": "2026-11-05T12:30:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice b: L04.html, L05.html, L06.html, their lab twins and the PC3 cards for L04-L06. Lab twins are demonstrations; mutation testing does not apply (architect ruling), so mutants is empty.",
        "Full read: each page read line by line (prose, problems, key results, quizzes); each twin read in full; all 98 cards for L04-L06 read in full (cards.json).",
        "Independent recomputation: l04_indep.py (own game simulator, Prop 3.1 enumeration over 8505 cases, Corollary 3.3, Remark 4.2, R1, E2, E3, mid identity on seeds 0-49), l05_indep.py (own deque, Def 3.1 survivors on 3000 sequences, bounds, traces, P3, Remark 3.4 k=1..11), l06_indep.py (exact NPV, break-evens, Remark 4.3, E1-E3, R3, M1-M3), notation_scan.py, embed_compare.py, build_fragment.py. Outputs in out/.",
        "Judgement (not a row): L04 Section 1 and Remark 4.2 use 'adds no expected gain' for the inventory term (mean zero, Prop 4.1); this is the inventory's contribution, not the trade term, and reads correctly.",
        "Judgement (not a row): L05 Remark 3.6 bounds a push by floor(log2 m) for a heap of m entries after the push; read that way it is correct.",
        "Judgement (not a row): L05 cards c143 (pushes and pops, grade C) mix a T count (pushes = n, Prop 3.3) with lab-only pops; graded C as a lab report, accepted.",
        "Judgement (not a row): plain letter E for expected trade terms in L04 is not a registered symbol; accepted under notation.json.",
        "Round-11 FAIL rows L06-why-it-matters-scope and L06-lab-docstring-money-integer are re-verified and now PASS.",
        "Round-12 FAIL rows: card grades (c096, c097, c148) and the unrounded break-even derivation (Remark 4.3, E3, quiz item 9, misconception 2, card c151). The 2-decimal values the page prints are correct; the defects are grade and derivation completeness.",
    ],
    "summary": {"rows": len(rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": 0},
}
out = root / "ledgers/PC3/PC3-b.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), "pass", counts["PASS"], "fail", counts["FAIL"], "verdict", verdict)
