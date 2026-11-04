"""Writes ledgers/PC3/PC3-b.json for PC3 slice b, round 6 (independent verifier). Evidence strings cite the commands,
scripts and output files under ledgers/PC3/scripts/PC3-b-r6/."""
import datetime
import json

S = "ledgers/PC3/scripts/PC3-b-r6"
O = f"{S}/out"
P = "PASS"
rows = []


def row(rid, check, location, status, evidence, fix=""):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != P:
        r["fix"] = fix
    rows.append(r)


GATE = "Command output in " + O + "/"
row("gate-run-labs-unit", "2.5-labs", "tools/run_labs.py --unit PC3", P,
    GATE + "run_labs.out: 'run_labs PC3: PASS (9/9)', rc 0 (command run on pin 4bd8cb94).")
row("gate-check-pages", "2.9-prose", "tools/check_pages.py --unit PC3", P, GATE + "check_pages.out: 'check_pages PC3: PASS', rc 0.")
row("gate-check-dag", "2.9-DAG", "tools/check_dag.py --unit PC3", P, GATE + "check_dag.out: 'check_dag PC3: PASS', rc 0.")
row("gate-check-projects", "2.6-structure", "tools/check_projects.py --unit PC3", P,
    GATE + "check_projects.out: 'check_projects PC3: PASS', rc 0 (unit project, not in slice b; gate run as the round command list requires).")
row("gate-page-smoke-slice", "2.9-prose", "tools/page_smoke.py --unit PC3 --pages L04 L05 L06", P,
    GATE + "page_smoke_L04_L06.out: L04, L05, L06 each PASS (Chromium, light and dark, 360 px sweep, lab run in Pyodide); 'page_smoke PC3: PASS', rc 0. Note: --pages takes stems (L04), not file names.")
row("gate-ruff-mypy-twins", "2.5-labs", "ruff check, ruff format --check on the three twins; .venv/bin/mypy --no-incremental", P,
    GATE + "ruff_check.out 'All checks passed!'; ruff_format.out '3 files already formatted'; mypy.out 'Success: no issues found in 385 source files'.")
row("gate-pytest-lab-tooling", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py", P,
    "414 passed in 50.73s (command output, also pytest_slice_relevant.out shows dots only; count taken from a second run with the summary line).")
row("gate-verify-refs-offline", "2.1-citations", "tools/verify_refs.py --offline (whole registry; --unit needs a live run)", P,
    GATE + "verify_refs.out: 'offline integrity: 560 entries, 0 problems', rc 0. Slice b cites no registry key (grep data-cite in L04-L06: 0 hits).")
row("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", P,
    "Run alone: .venv/bin/python -I -W error <twin>; rc 0 each, stderr 0 bytes (" + O + "/lab-L0N.stderr); stdout saved as lab-L0N.stdout.")
row("twin-page-code-equals-twin", "2.5-labs", "course/modules/PC/PC3/L04.html, L05.html, L06.html vs the three twins", P,
    "ledgers/PC3/scripts/PC3-b-r6/embed_compare.py (output embed_compare.out): page code == twin after trailing-newline strip, for all three pages.")
row("twin-expected-equals-stdout", "2.5-labs", "expected blocks L04 lines 409-458, L05 lines 298-320, L06 lines 283-303", P,
    "embed_compare.out: expected == twin stdout for all three (trailing-newline strip only).")
row("lab-L04-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L04.html line 180 (hypothesis), line 459 (interpretation)", P,
    "Hypothesis: cash flow -9950 and P&L 30 (lab output lab-L04.stdout: 'cash flow ... = -9950', 'P&L ... = 30'); Part 2 nine fair values (9980..10020); Part 3 variance 25 I^2. Interpretation: 9 fills, -9950, inventory 1, settlement 9980, P&L 30 all match lab-L04.stdout. True.")
row("lab-L05-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L05.html line 163 (hypothesis), line 321 (interpretation)", P,
    "Hypothesis: naive 1351 = (n-k+1)(k-1), deque <= 2n = 400, 200 pushes; five edge checks (Part 2 has five True lines); five Part 3 rows: lab-L05.stdout. Interpretation numbers 1351, 354 match.")
row("lab-L06-1-hypothesis-interpretation", "2.9-prose", "course/modules/PC/PC3/L06.html line 159 (hypothesis), line 304 (interpretation)", P,
    "Previous round FAIL is fixed. Interpretation now says printed break-evens 1164.10, 1206.34, 1249.05 differ by 42.24 and 42.71 (printed-value differences: 1056/25 = 42.24, 4271/100 = 42.71) and that from unrounded values the differences are 42.24 and 42.70 (l06_check.out: 42.24386873714821 and 42.7025308023877). Matches lab-L06.stdout.")
row("L04-definitions-A1-A6-notation", "2.4-notation", "course/modules/PC/PC3/L04.html lines 56-89", P,
    "Read in full. Symbols N, t, p, L declared local; A1 arrivals 1/4,1/4,1/2 matches lab draw thresholds (twin draw_game); A5 test |I|<=L after trade matches play(); A6 a=m+h, b=m-h. notation/notation.json has 8 symbols (T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q); a scan of all 352 math segments of L04 (and 309 of L05, 243 of L06) finds none of them, so no registry collision.")
row("L04-prop-2.2-2.3-identity", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 100-118", P,
    "Re-derived: C_t = sum c_s, I_t = sum sigma_s, W_N identity; W_t - W_{t-1} = (c_t + sigma_t v_t) + I_{t-1}(v_t - v_{t-1}). Lab Part 1 prints identity True (lab-L04.stdout).")
row("L04-prop-3.1-closed-form", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 127-139", "FAIL",
    "The displayed conclusion conditions on v_t = v only: E[c_t+sigma_t v_t | v_t = v]. Hypotheses H1-H2 fix I_{t-1}=0 and the quote a_t, b_t, which are functions of the public history (A3). The proof's step 'the quote is fixed' is therefore an unstated conditioning. The gap is real under A3: ledgers/PC3/scripts/PC3-b-r6/l04_prop31_alt_quote.py (exact enumeration, T=5, rule B: mid = 10000 + 10 x fills, which is a function of the fill history, so admissible under A3) gives, for v=9985 and I_4=0, a mixture E = -815/74 (about -11.01) while each quote's own value matches the displayed formula (quotes 10010/9990 -> 5/2; 10030/10010 -> -15/2; 10050/10030 -> -35/2; output l04_prop31_alt_quote.out). The quoting rule of Example 1.3 happens to fix the quote at I=0 (mid = 10000 - 10 x inventory, by induction on fills; l04_prop31_conditioning_lab_rule.out shows one quote at I=0 for every v), so the lab numbers are right; the proposition as stated for general A3 quotes is not.",
    "Restate the conclusion as a conditional expectation given the public history F_{t-1} and v_t = v, on the event {I_{t-1}=0}: E[c_t+sigma_t v_t | F_{t-1}, v_t = v] = (1-p)h - p[(v-a_t)^+ + (b_t-v)^+], with a_t, b_t F_{t-1}-measurable (H2) and the arrival independent of (F_{t-1}, v_t) by A1 (H3). Then the proof's 'the quote is fixed' is valid. Or state it for a fixed quote (a,b) and condition on that quote.")
row("L04-example-3.2-values", "2.2-numbers", "course/modules/PC/PC3/L04.html line 143", P,
    "Quote 10010/9990, p=1/2 with the quote fixed: E(10000)=5, E(10020)=0, E(9985)=5/2 (l04_check.out 'Example 3.2 values [5, 0, 5/2]'). Lab Part 2 grid agrees (lab-L04.stdout).")
row("L04-corollary-3.3", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 146-154", "FAIL",
    "Inherits the conditioning gap of Proposition 3.1 (its hypotheses are 'those of Proposition 3.1'; its conclusion is an expectation of the same kind). The algebra itself is right: with p=1/2 and v>=a, E = h/2 - (v-a)/2, zero iff v = a+h (checked, l04_check.py).",
    "Fix Proposition 3.1 as stated in its row; then state Corollary 3.3 for the conditional expectation given F_{t-1} and v_t = v, or for a fixed quote.")
row("L04-proposition-4.1-remark-4.2-sd", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 163-176", P,
    "Prop 4.1 proof re-derived: E[I eps]=0, E[(I eps)^2]=25 I^2. Remark 4.2: sd 5|I| gives 15 at I=3 and 50 at I=10 (l04_check.out). The trade-term example at I=10: buy-only contributes 10 x 1/4 = 5/2 (l04_check.out).")
row("L04-remark-4.2-inventory-independence", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 175 and line 52", P,
    "Fair-move term is I_{t-1}(v_t - v_{t-1}); mean zero (Prop 2.3 link is correct). |I|<=L-1 gives |I+-1|<=L, so no refusal. Conditioning is 'for a given quote and fair value', which is explicit, so the statement is not affected by the Prop 3.1 gap.")
row("L04-canon-breaks-tick", "2.9-prose", "course/modules/PC/PC3/L04.html lines 462-468", P,
    "Model-limit paragraph: integer-cent quotes, 5 cent moves, A1 to A6 conditioning, queue not modelled, learning not modelled. No claim about real market makers. Checked against Definition 1.1 and A1 to A6.")
row("L04-canon-breaks-quote-rule", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 466", "FAIL",
    "The sentence 'Proposition 3.1 shows that, at a fair value inside the quote, the expected change (1-p)h rises with the half-spread h' cites Proposition 3.1 as an unconditional-in-quote statement. It inherits the conditioning gap; the conclusion holds for a given quote (the lab's quote at I=0 is fixed, so the example is right).",
    "Once Proposition 3.1 is restated conditional on F_{t-1}, change the sentence to 'for a given quote, at a fair value inside the quote, the expected change ... rises with h'.")
row("L04-R2-spread-criterion", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 584", P,
    "At v=m both brackets vanish, E=(1-p)h; p<1 gives E>0 for every h, p=1 gives E=0. Re-derived; the answer 'no finite spread' follows from A1 (arrivals do not depend on h).")
row("L04-E1-seed1-numbers", "2.2-numbers", "course/modules/PC/PC3/L04.html line 552 (Problem E1)", P,
    "ledgers/PC3/scripts/PC3-b-r6/l04_check.py (own implementation of Definition 1.1 and A1 to A6 from the page text, with the lab's draw order): seed 1 gives fills 16, cash flow 20100, inventory -2, settlement 10020, mark -20040, P&L 60. All match.")
row("L04-E2-binomial-z", "2.2-numbers", "course/modules/PC/PC3/L04.html line 559 (Problem E2)", P,
    "Seed 0 has 13 informed arrivals (l04_check.py arrivals_informed = 13; also counted from lab-L04.stdout turn column). se = sqrt(0.25/20) = 0.1118, z = 0.15/0.1118 = 1.3416, below 1.96. Numbers match.")
row("L04-E3-mid-vs-settlement", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 564-566 (Problem E3); Remark 2.4 line 122", P,
    "Last quote 9980/10000 (turn 20 of lab-L04.stdout), mid 9990, settlement 9980, cash flow -9950, inventory 1: P&L 30 at settlement, 40 at mid, difference 10. Verified in l04_check.out ('pnl 30').")
row("L04-problems-R1-R3-M-P", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 498-595", P,
    "Re-derived: M1 cash 10010, mark 10; M2 refusal at 11; M3 no trade at 10010, buy at 10011; P1 identity; P2 E(a)=h/2, E(a+h)=0; P3 variance 400 at I=-4; R1 d=(1-p)h/p=20/3 at p=3/5, h=10 (l04_check.out 6.666...); R2; R3 |I|<2 so largest |I|=1 with variance 25.")
row("L04-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L04.html lines 614-704", P,
    "Data-correct options checked (6 correct flags; each option text matches the math above). Numeric answers 10, 0, 5, 400, 6.6667 (tol 0.001: 20/3 = 6.66667), 9 (lab prints 'fills 9 of 20 turns'). The quiz numeric 'answer 0' item uses the fixed quote 9990/10010 (quote given in the item).")
row("L04-quiz-q11-citation", "2.9-prose", "course/modules/PC/PC3/L04.html lines 690-692", P,
    "Quiz item 'how many of the 20 turns on seed 0 have a fill' -> 9; lab-L04.stdout prints 'fills 9 of 20 turns'. Lesson states no registry citation; quiz refers to Lab 1 only.")
row("L04-misconceptions", "2.9-prose", "course/modules/PC/PC3/L04.html lines 471-487", P,
    "Misconception 1: uninformed flow (1-p)h = h/2 = a quarter of 2h at p=1/2; zero at v=10020 (lab-L04.stdout). Misconception 2: P&L 10 after uninformed buy at 10010 with settlement 10000. Misconception 3: 25 I^2 = 2500 at I=10 (lab-L04.stdout). Misconception 4: A3 excludes v_t-dependent quotes.")
row("L04-scope-and-banned-phrases", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file)", P,
    "BANNED list (tools/check_pages.py:58-72) scanned with word boundaries: 0 hits for TODO, TBD, lorem, obviously, clearly, studies show, experts agree, it is well known, important to note, '...'. Process words (build, builder, round, verifier, REQUESTS, unit report): 0 hits. Scope words 'every', 'always', 'never', 'all': each is backed by a proof or the lab (checked above).")
row("L04-structure-hours", "2.9-prose", "course/modules/PC/PC3/L04.html (whole file); index.html data-hours-lessons=36", P,
    "data-hours=6; sections in template order; 4 problem tiers x 3 problems with solutions (12 solution blocks); 4 misconceptions; quiz 12 items; Where the canon breaks present. check_pages PASS. Lessons 6 x 6 = 36 matches hub data-hours-lessons=36 (index.html line 29).")
row("L04-DAG-D-terms", "2.9-DAG", "course/modules/PC/PC3/L04.html lines 52, 158, 465 (adverse selection); links line 9-10", P,
    "Links used (expectation, market-maker, bid-ask-spread, limit-order-book: owners M4, FC1; expected-value-game linked to L03.html#def-expected-value-game, which exists). Out-of-closure term 'adverse selection' (owner E2, D3 in plan) is used in prose only, no link, no dfn, as the architect default allows. Note: the plan says the term is used once; it appears twice (lines 158 and 465). Not a FAIL: the architect default is plain prose.")
row("L04-A1-project-consistency", "2.4-notation", "course/modules/PC/PC3/L04.html line 72 (A1); project.html line 404; tests/labs/PC3/lab-PC3-project-1.py lines 37-44", P,
    "A1 says Lab 1 and the project use p=1/2 with probabilities 1/4, 1/4, 1/2. project.html line 404 states the same 1/4, 1/4, 1/2. lab-PC3-project-1.py lines 37-44 draws uninformed buy below 0.25, uninformed sell below 0.5, else informed: consistent.")
row("L04-key-results-prop-3.1-assumptions", "2.9-prose", "course/modules/PC/PC3/L04.html lines 597-612 (key results row 3), line 605", "FAIL",
    "Key-results row 'From inventory zero, the expected trade term is (1-p)h - p[(v-a)^+ + (b-v)^+]' grade T, source Proposition 3.1 under A1, A3, A4, A5, A6. Inherits the conditioning gap of Proposition 3.1 (the table repeats its unconditional-in-quote form).",
    "Fix Proposition 3.1 (conditioning on F_{t-1} and v_t) and write the row as 'given the public history, from inventory zero ...'.")
row("L04-key-results-table-other", "2.9-prose", "course/modules/PC/PC3/L04.html lines 597-612 (other rows)", P,
    "Rows: Proposition 2.2 identity (T); Proposition 2.3 split (T); Corollary 3.3 (T, see FAIL row above); Proposition 4.1 (T); enumerated-expectation row (C, Lab 1 Part 2, nine values 9980..10020). Grades match the proof status (C for the lab check).")
row("L05-def-3.1-markup", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 106 (Definition 3.1)", P,
    "Surviving index definition read: i-k<j<=i and x_j > x_m for j<m<=i; monotonic-deque link to CS2 concept (in closure). Markup change (article 'a' instead of 'the') does not alter the definition.")
row("L05-prop-2.1-2.2-remark", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 85-98", P,
    "Prop 2.1 count (n-k+1)(k-1): 1351 for n=200, k=8 (l05_check.out). Remark 2.2 completing the square verified; (n-r)r = n^2/4 - (r-n/2)^2.")
row("L05-prop-3.2-correctness", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 123-133", P,
    "Steps A, B, C re-derived line by line: invariant decreasing values from front to back; front expiry removes at most one index (i-k) and only if it is the front; front is the last occurrence of the window maximum (l05_check.py: brute-force equal for all k in 1..20, seeds 5 and 6).")
row("L05-prop-3.3-bound", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 142 (proof), 113-120 (pseudocode), statement line 137", P,
    "Previous round FAIL is fixed. The proof now counts only while-loop tests: each test is followed by a back removal or is the single failed test of its step, so tests <= back removals + n <= 2n; the front-expiry test is an if outside the loop and is excluded, matching the statement's 'while-loop tests'. Removals <= n since each index leaves once. Checked: l05_check.out: for every k in 1..200 on seed 5, comparisons <= 400, pops <= 200, pushes = 200 (also seed 6). Re-derived independently.")
row("L05-remark-3.4-k-range", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 147 (Remark 3.4)", P,
    "Example x = (k, k-1, ..., 2, k+1) with n = k: at step k the deque holds indices 1..k-1 and the value k+1 removes all k-1 (l05_check.py: k=5 example, step-k removals 4). Re-derived.")
row("L05-example-3.5-trace", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 151-153", P,
    "Trace of x=(3,1,4,1,5), k=3: deques (1), (1,2), (3), (3,4), (5); outputs (4,4,5). l05_check.out 'Example 3.5 outputs [4, 4, 5]'.")
row("L05-problems-M-P", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 344-396", P,
    "M1 21 (7 windows of 3). M2 trace on (2,5,1,0,3), k=2: outputs (5,5,1,3) matches l05_check.out 'M2 trace outputs [5, 5, 1, 3]'. M3 k=1 identity, k=n single max. P1 peak n^2/4 at k=n/2+1 (n=200: k=101, 10000). P2 survival of q re-derived. P3 strictly increasing gives n-1 for all k (l05_check.out 'increasing n-1 for all k: True').")
row("L05-E1-E3-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 400-420 (E1-E3); expected block lines 298-320", P,
    "E1: 169*31 = 5239; 5239/382 = 13.7147 -> 13.7 (l05_check.out). E2 seed 6: outputs equal, naive 1351, deque 350 comparisons, 200 pushes, 197 pops (l05_check.out 'seed6 k8 ... deque {comps 350, pops 197, pushes 200}'); not printed by the lab, and the page says so. E3: largest deque count at k=200 (387), bound 400, split 194+200=394 >= 387; row shows 200 pushes, 194 pops (lab-L05.stdout).")
row("L05-R1-scope-sentence", "2.9-prose", "course/modules/PC/PC3/L05.html lines 423-431 (R1)", P,
    "Timing protocol research item: states that the lab does not time anything and proves no timing result; consistent with lab docstring 'no timing'. No timing claim is made.")
row("L05-R2-R3", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 432-446", P,
    "R2: k=101 maximises (n-k+1)(k-1) = 10000 for n=200 (l05_check.out 'R2 k maximizing naive: 101 10000'). R3: strictly increasing sequence removes one back element per step i>=2 and total n-1; per-step removal does not force order nk.")
row("L05-key-results-grades", "2.9-prose", "course/modules/PC/PC3/L05.html lines 449-464", P,
    "Rows match Propositions 2.1, Remark 2.2, 3.2, 3.3 (wording 'at most 2n comparisons in its while-loop tests' matches the fixed statement), P3, and the C-graded Lab 1 Part 2 row.")
row("L05-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L05.html lines 472-552", P,
    "Data-correct flags checked (6 correct options): 21; 'yes, total bound counts all removals' (Prop 3.3); n-1; largest value with last occurrence of ties (proof: an earlier equal index fails strict survival); 1351; 'counts, not run times'; 'No outputs' for window > length. Numeric 400, 10000, 5, 1351 verified.")
row("L05-misconceptions-canon-breaks", "2.9-prose", "course/modules/PC/PC3/L05.html lines 324-348", P,
    "Misconception 1: 354 comparisons for n=200, k=8 within 400 (l05_check.out). Misconception 2 and 3 consistent with the lab (no timing; Part 2 is a finite check). Canon-breaks: amortised bound and single-step cost k-1 consistent with Remark 3.4.")
row("L05-structure-hours", "2.9-prose", "course/modules/PC/PC3/L05.html (whole file)", P,
    "data-hours=6; 4 tiers x 3 problems with solutions; 3 misconceptions; quiz 10 items; key results table; Where the canon breaks present; check_pages PASS.")
row("L05-markup-raw-less-than", "2.9-prose", "course/modules/PC/PC3/L05.html (Definition 3.1 and math)", P,
    "Raw '<' is escaped as &lt; in the HTML (Definition 3.1 line 106); the '>' in x_j>x_m is raw HTML text, valid; page_smoke PASS (KaTeX renders, zero console errors).")
row("L05-meta-uses-hash-map-heap", "2.9-DAG", "course/modules/PC/PC3/L05.html lines 38-40 (Uses), Remark 3.6 lines 157-158", P,
    "hash-map, binary-heap, big-o-complexity, monotonic-deque, unit-test are linked to CS2/CS1 concepts (owners in closure). Remark 3.6 heap bound 3*200*7 = 4200 (l05_check.out 'Remark 3.6 heap bound 4200' and the text).")
row("L06-prop-1.1-payoff-identity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 58-66", P,
    "Proof by cases re-derived: (s-K)^+ - (K-s)^+ = s-K. Key-results row 'for all real s and K' is backed by this proof.")
row("L06-remark-1.2-put-call-parity", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 69-71 (Remark 1.2), linked put-call-parity concept", P,
    "Price form C - P = S - DK with D = e^{-r tau} is the statement of FC2 L05 (course/modules/FC/FC2/L05.html line 59), under FC2's standing assumptions. The remark says the lesson does not re-derive it and uses the link only: accurate.")
row("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 74-76, 113-121", P,
    "NPV formula sum C_t (1+r)^{-t} matches CF1 L01 line 60 (linked). Proposition 3.1 hypotheses (H1)-(H3) complete; proof: NPV(u) = -I + mAu, A>0, unique break-even I/(mA). Re-derived (l06_check.py).")
row("L06-prop-2.1-forward", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 93-107", P,
    "Hypotheses A1-A3 for (i), plus A4 and A5 for (ii). (i) cost zero, payoff F'-S/D (l06_check.out: 100 = 10100 - 9700/0.97 check). (ii) both directions use A4 and A5 correctly (short sale and reverse portfolio).")
row("L06-remark-2.2-continuous-convention", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 86, 105-106; FC2 L02 Definition 2.1", P,
    "D = e^{-r tau} gives S/D = S e^{r tau}, equal to the cost-of-carry price of FC2 L02 Definition 2.1 (F* = S e^{r tau}, linked). Rational D = 97/100 is an input; statement that e^{-r tau} is irrational in general is a true remark, not used in a number.")
row("L06-corollary-3.3-grade", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 131-139 (statement and proof)", P,
    "Rewritten with l = prod l_j and h = prod h_j: if l < u* < h then NPV(l) < 0 < NPV(h); if the interval lies on one side the sign is fixed. Re-derived from Proposition 3.1 (NPV = mA(u-u*)). Hypotheses (Prop 3.1 and 3.2) stated.")
row("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 123-131", P,
    "Induction re-derived: product of positive intervals; both ends attained by choosing each factor at an end. Consistent with P3 solution and Example 4.2.")
row("L06-example-4.2-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 146-150 (Example 4.2), line 152", P,
    "Bounds 200 and 1600 (l06_check.py: 2000*1*0.1 and 4000*2*0.2). A = 3310/1331 (exact). u* = 399300/331 = 1206.3444 -> 1206.34. NPV at 200 = -12513148 (exact -16655000000/1331) and at 1600 = 4894816 (l06_check.out). Range straddles u*.")
row("L06-remark-4.3-sensitivity", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 153-155 (Remark 4.3); expected block lines 298-303", P,
    "Unrounded break-evens 1164.1005, 1206.3444, 1249.0469 (l06_check.out). Differences 42.2439 -> 42.24 (8 to 10) and 42.7025 -> 42.70 (10 to 12). Printed 1164.10, 1206.34, 1249.05. NPVs at 200/1600 at 8, 10, 12 percent match lab-L06.stdout (-12422903/5616776; -12513148/4894816; -12598169/4214650).")
row("L06-E1-12pct", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 395-401 (Problem E1)", P,
    "Annuity at 12 percent = 2.4018313 (l06_check.out 2.40183...), break-even 3000/A = 1249.0469 -> 1249.05, matches lab-L06.stdout.")
row("L06-E2-first-negative", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 402-408 (Problem E2)", P,
    "Grid 200..1600 by 100 at 10 percent: positive points 1300, 1400, 1500, 1600 (count 4); largest negative 1200 (l06_check.out). NPV(1200) = -105000000/1331 = -78888.054 -> -78888.05; NPV(1300) = 1550000000/1331 = 1164537.94 (l06_check.out). Both match.")
row("L06-E3-42.71", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 410-416 (Problem E3)", P,
    "Width 1249.0469 - 1164.1005 = 84.9464 -> 84.95; per point 84.9464/4 = 21.2366 -> 21.24; 1206.3444 - 1164.1005 = 42.2439 -> 42.24; 1249.0469 - 1206.3444 = 42.7025 -> 42.70; printed-value difference 1249.05 - 1206.34 = 42.71 (l06_check.out). All correct.")
row("L06-E3-rest-and-quiz-q9", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 409-416 and quiz item 9 (about line 521)", P,
    "Quiz 'average change ... 21.24': 84.9464/4 = 21.2366 -> 21.24 (tolerance 0.01). Item text and explanation consistent with Problem E3.")
row("L06-M1-M3-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 345-366 (Problems M1-M3)", P,
    "M1: 4900/0.98 = 5000, payoff 50 (l06_check.out). M2: NPV = 500/121 = 4.1322 (l06_check.out, 'M2 NPV 500/121 ... True'). M3: u* = 33275/331 = 100.5287 -> 100.53 (l06_check.out).")
row("L06-P1-P3-proofs", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 370-390", P,
    "P1 reverse portfolio: cost 0 (A5 short sale at S, lend S, A3 no cost), payoff S/D - F' in every state. P2 affine with positive slope: one zero, sign on each side. P3 product bounds 200 and 1600, ends attained. Re-derived.")
row("L06-R1-R3", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 418-440", P,
    "R1: each factor ratio is 2, log-width ln 2 each (l06_check.out: four ln 2 values). R2: break-even I/sum m_t(1+r)^{-t}, re-derived. R3: m* = 15000000*1331/(1600*3310) = 3769.83 cents, 0.7540 of 5000, fall 24.6 percent (l06_check.out 'R3 m* 3769.826...', 'fall % 24.6').")
row("L06-quiz-answers", "2.9-prose", "course/modules/PC/PC3/L06.html lines 461-536", P,
    "Data-correct flags checked (5 correct options). Numeric answers 5000, 4.13 (tol 0.005; 500/121 = 4.1322), 1206.34 (tol 0.005; 1206.3444), 4, 21.24 (tol 0.01), and the others are consistent with the math above.")
row("L06-canon-breaks-and-misconceptions", "2.9-prose", "course/modules/PC/PC3/L06.html lines 310-337", P,
    "Canon-breaks: 'factor of 8' = 2 x 2 x 2 (l06_check.out, bounds 200 and 1600). Misconception 2 'about 21 units per point' = 84.9464/4 (l06_check.out). Misconception 1 and 3 values match lab-L06.stdout.")
row("L06-DAG-and-cross-links", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 38, 39, 56, 75, 86", P,
    "Uses list: forward-contract, cost-of-carry-forward-price, put-call-parity (FC2), net-present-value (CF1), statement-articulation (AC1), fermi-estimation (L01.html#def-fermi-estimation, exists: grep count 2 in L01). All owners in closure {AC1, CF1, FC2} (check_dag PASS).")
row("L06-structure-hours", "2.9-prose", "course/modules/PC/PC3/L06.html (whole file)", P,
    "data-hours=6; 4 tiers x 3 problems with solutions; 4 misconceptions; quiz 10 items; key results; Where the canon breaks; check_pages PASS.")
row("L06-articulation-claim-linked", "2.9-DAG", "course/modules/PC/PC3/L06.html line 75 and quiz item 10", P,
    "Linked statement-articulation (AC1 L03 line 57): 'the cash-flow statement ends at the balance-sheet cash'. The quiz answer 'Balance-sheet cash' matches it. Concept owner AC1 is in closure.")
row("L05-meta-uses-other", "2.9-prose", "course/modules/PC/PC3/L05.html (Uses list, lesson meta)", P,
    "Meta and Uses rows checked; all concepts owned by CS1/CS2 (in closure); check_dag PASS.")
row("L05-remark-3.6-hash-heap", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 157-158 (Remark 3.6)", P,
    "Heap comparisons: push <= floor(log2 m), pop <= 2 floor(log2 m); total <= 3 n floor(log2 n) = 4200 at n=200 vs deque 2n = 400. Re-derived. The remark says it does not prove the heap reports the maximum: honest scope.")
row("L04-remark-3.4-inventory-zero", "2.4-mathematics", "course/modules/PC/PC3/L04.html Remark 3.4 (lines 157-158)", P,
    "From inventory zero the uninformed flow earns (1-p)h, a quarter of the 2h spread at p=1/2 (Prop 3.1 with v inside the quote, given quote). Adverse selection described as the informed cost outside the quote; the remark says it does not develop the theory. Consistent with the proof.")

assert len(rows) == 77, len(rows)
frag = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 6,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 6 (did not build PC3)",
    "pin": "4bd8cb94a8e171e80c4c34da1b3f32be7cb93f07",
    "base": "7376a5e2 (round-5 pin). Delta 7376a5e2..4bd8cb94 touches L04.html (2 hunks), L05.html (4 hunks, incl. Proposition 3.3 proof and Remark 3.6 wording), L06.html (about 8 hunks, incl. Remark 4.3, Corollary 3.3, Problem E2/E3, interpretation), plus other slices. All three twins are byte-identical since 9a02b1af (not in the delta). Every slice row is re-verified from scratch in this round.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE6-PC3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyE6-PC3-b/ledgers/PC3/scripts/PC3-b-r6/out",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Slice PC3-b: course/modules/PC/PC3/L04.html, L05.html, L06.html and tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py. Cards (cards.json) are not in this slice's file list and are not checked here.",
        "Mutants: none. This is a lab-page slice, not a project grader slice (architect ruling: lab twins are demonstrations; mutation testing applies to project graders). No new grader mutants are claimed.",
        "Round-5 FAIL rows: L06 interpretation of Lab 1 (now PASS, re-verified) and L05 Proposition 3.3 proof (now PASS, re-verified). New FAIL: the conditioning of Proposition 3.1 (E given v_t alone, with quote and inventory as history functions); Corollary 3.3, key-results row and the canon-breaks sentence inherit it. Counterexample under an A3-admissible quote rule: ledgers/PC3/scripts/PC3-b-r6/l04_prop31_alt_quote.py (output l04_prop31_alt_quote.out). The lab's own quote rule fixes the quote at I=0 (mid = 10000 - 10 x inventory), so the printed lab numbers are correct.",
        "Not checked: the cards for L04-L06 (cards.json, outside this slice's files); the project page and grader (other slice); live verify_refs run (slice cites no registry key; offline integrity checked for the whole registry)."
    ],
    "summary": None,
}
counts = {"rows": len(rows), "pass": sum(r["status"] == P for r in rows),
          "fail": sum(r["status"] == "FAIL" for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag["summary"] = counts
with open("ledgers/PC3/PC3-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print(counts)
