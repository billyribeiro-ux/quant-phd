"""Build the PC3-b round-3 ledger fragment (ledgers/PC3/PC3-b.json) from the verification evidence in this scripts dir.

Usage: python -I build_fragment_r3.py <checkout-root>. Writes ledgers/PC3/PC3-b.json only.
"""
import json
import sys
from datetime import datetime, timezone

root = sys.argv[1]
S = "ledgers/PC3/scripts/PC3-b-r3/"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


PASS = "PASS"
# ---- gates and tooling
row("gate-run-labs-unit", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", PASS,
    f"Re-run: .venv/bin/python tools/run_labs.py --unit PC3 -> 'run_labs PC3: PASS (9/9)', exit 0 ({S}run_labs_unit.out); per page --page L04/L05/L06 'PASS (1/1)' each ({S}run_labs_L04.out, run_labs_L05.out, run_labs_L06.out).")
row("gate-check-pages", "2.9-structure", "course/modules/PC/PC3/L04.html, L05.html, L06.html", PASS,
    f"Re-run: .venv/bin/python tools/check_pages.py --unit PC3 -> 'check_pages PC3: PASS', exit 0 ({S}check_pages.out). The gate does not parse tag balance: see row L05-markup-raw-less-than, checked by {S}tag_scan.py.")
row("gate-check-dag", "2.9-DAG", "course/modules/PC/PC3/L04.html, L05.html, L06.html", PASS,
    f"Re-run: .venv/bin/python tools/check_dag.py --unit PC3 -> 'check_dag PC3: PASS', exit 0 ({S}check_dag.out). It checks linked uses only; the plain dfn is row L04-DAG-D-terms.")
row("gate-check-projects", "gate", "PC3 unit (project slice is not mine)", PASS,
    f"Re-run: .venv/bin/python tools/check_projects.py --unit PC3 -> 'check_projects PC3: PASS', exit 0 ({S}check_projects.out). Recorded for the unit only.")
row("gate-page-smoke-slice", "2.5-labs / 2.9-structure", "L04.html, L05.html, L06.html (run alone)", PASS,
    f"Re-run alone: .venv/bin/python tools/page_smoke.py --unit PC3 --pages L04 L05 L06 -> PASS for each page and 'page_smoke PC3: PASS', exit 0 ({S}page_smoke.out). Lab runtimes 0.0 s each.")
row("gate-ruff-mypy-twins", "gate", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", PASS,
    f"Re-run with explicit paths: ruff check -> 'All checks passed!' ({S}ruff_check.out); ruff format --check -> '3 files already formatted' ({S}ruff_format.out); mypy --no-incremental -> 'Success: no issues found in 3 source files' ({S}mypy.out).")
row("gate-pytest-lab-tooling", "gate", "tests/test_labs.py, tests/test_run_labs.py", PASS,
    f"Re-run: .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py -> all passed, exit 0 ({S}pytest_labs.out).")
row("gate-verify-refs-offline", "2.1-citations", "registry (slice cites no key)", PASS,
    f"Re-run: .venv/bin/python tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs.out). grep -c 'data-cite\\|data-locator' on L04, L05, L06 returns 0 for each.")
row("twin-run-alone-L04-L06", "2.5-labs", "tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, lab-PC3-L06-1.py", PASS,
    f"Each twin run as python -I -W error from an empty temporary directory: exit 0 and stderr 0 bytes for L04, L05, L06 ({S}twin_vs_page.py, output {S}twin_vs_page.out). The twins are byte-identical to 67c47689 (git diff --quiet 67c47689 HEAD -- the three twins: no diff).")
row("twin-page-code-equals-twin", "2.5-labs", "course/modules/PC/PC3/L04.html, L05.html, L06.html (data-run block)", PASS,
    f"{S}twin_vs_page.py: 'page code == twin: True' for L04, L05, L06 after html.unescape and trailing-newline strip ({S}twin_vs_page.out).")
row("twin-expected-equals-stdout", "2.5-labs", "course/modules/PC/PC3/L04.html (pre.expected lines 409-458), L05.html (lines 292-314), L06.html (lines 286-306)", PASS,
    f"{S}twin_vs_page.py: 'expected == stdout: True' for L04, L05, L06; the captured stdouts are {S}stdout_L04.out, stdout_L05.out, stdout_L06.out.")
# ---- lab hypothesis / interpretation
row("lab-L04-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L04.html line 180 (hypothesis) and 459 (interpretation)", PASS,
    f"Hypothesis claims checked against {S}stdout_L04.out: identity True, cash flow -9950, P&L 30, nine exact enumeration points, five inventories (Part 3). Interpretation: 9 fills in 20 turns, cash flow -9950, inventory 1, settlement 9980, P&L 30 all match the output. 'does not estimate p' matches the code (no estimator).")
row("lab-L05-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L05.html line 157 (hypothesis) and 315 (interpretation)", PASS,
    f"Against {S}stdout_L05.out: 193 windows, naive 1351 = (n-k+1)(k-1), deque comparisons 354 <= 2n = 400, 200 pushes, five edge-case checks True, Part 2 agreement for k=1..20. Interpretation's 1351 and 354 match; 'not run times' matches the code (no timer).")
row("lab-L06-1-hypothesis-interpretation", "2.5-labs", "course/modules/PC/PC3/L06.html line 161-162 (hypothesis) and 307 (interpretation)", PASS,
    f"Against {S}stdout_L06.out: 10000 cents forward, zero payoff at 10000 and 100 at 10100 in all five spot states, annuity 3310/1331, break-even 399300/331, exact zero NPV, increasing NPV on the grid, rate sensitivity values. Interpretation's 'about 42 units' matches 1206.34-1164.10 and 1249.05-1206.34 (recomputed in {S}recompute_L06.py).")
# ---- L04
row("L04-definitions-A1-A6-notation", "2.4-notation / 2.9-prose", "course/modules/PC/PC3/L04.html lines 56-89 (symbols, Definition 1.1, A1 to A6, Example 1.3)", PASS,
    f"Symbols N, t, p, L declared at line 56. Notation scan of the three pages (macros used: \\sigma, \\varepsilon, \\E, \\Var, standard KaTeX; no registered symbol T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}} appears in math). A1 gives 1/4, 1/4, 1/2 matching draw_game in the twin (lines 235-254); A5 L=10 and q-bar=5 match constants at twin lines 208-212. Remark 1.2's constants N=20, v0=10000, move 5, q-bar 5, L 10, p 1/2 match the twin.")
row("L04-prop-2.2-2.3-identity", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 100-118", PASS,
    "Re-derived by hand: C_t = sum c_s, I_t = sum sigma_s under H1-H2; W_N = sum c_t + (sum sigma_t) v_N (Prop 2.2). W_t - W_{t-1} = c_t + sigma_t v_t + I_{t-1}(v_t - v_{t-1}) (Prop 2.3) matches the proof at line 117. Identity holds on seed 0 (stdout_L04.out: 'identity ... True').")
row("L04-prop-3.1-closed-form", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 127-139", PASS,
    f"Re-derived: three arrival contributions (a-v), (v-b), and -(v-a)^+-(b-v)^+ weighted by (1-p)/2, (1-p)/2, p; bracket = 2h gives (1-p)h - p[(v-a)^+ + (b-v)^+]. Exact enumeration at 9 fair values agrees with the closed form ({S}stdout_L04.out Part 2). Hypothesis list (H1-H3) checked against the proof steps (i)-(iii); A5 use is via 'q_t>=1 and |+-1|<=L' (line 135).")
row("L04-corollary-3.3", "2.4-mathematics", "course/modules/PC/PC3/L04.html lines 146-154", PASS,
    "With p=1/2 and v>=a, (b-v)^+ = 0 so E = h/2 - (v-a)/2; zero iff v = a+h (line 153). Hypothesis 'v>=a' is stated (line 148).")
row("L04-example-3.2-values", "2.2-numbers", "course/modules/PC/PC3/L04.html line 143", PASS,
    f"a=10010, b=9990, h=10, p=1/2: E(10000)=5, E(10020)=0, E(9985)=5/2; stdout_L04.out Part 2 prints 5, 0 and 5/2 at 10000, 10020 and 9985.")
row("L04-proposition-4.1-remark-4.2-sd", "2.2-numbers / 2.4-mathematics", "course/modules/PC/PC3/L04.html lines 163-176", PASS,
    f"Var(I eps) = 25 I^2 re-derived (line 170). SD = 5|I|: 15 at 3 units, 50 at 10 units (line 175) recomputed. Part 3 of stdout_L04.out prints variance 225 at |I|=3 and 2500 at I=10.")
row("L04-remark-4.2-inventory-independence", "2.4-mathematics / 2.2-numbers", "course/modules/PC/PC3/L04.html line 175 (Remark 4.2) and line 52 (why it matters)", PASS,
    f"Round-2 FAIL fixed at HEAD: line 175 now reads 'For a given quote and fair value v_t, the trade term then has the same distribution as at inventory 0, so its expected value does not depend on the position.' Line 52 now reads 'for a given quote, no expected gain'. Recomputed with {S}remark42_enum.py (output {S}remark42_enum.out): trade term at v=10000, quote 9990/10010, is 5 at I=0,1,3,9 and 5/2 at I=10 and I=-10; for |I|<=9 it equals the I=0 value at every grid point 9900..10100 (True).")
row("L04-canon-breaks-tick", "2.9-prose", "course/modules/PC/PC3/L04.html lines 462-468", PASS,
    "Canon-breaks section names model limits (A1-A6 conditional, no queue, quote rule of Example 1.3 depends only on fills). Each claim checked against the rules: 'by A5 a fill is one unit whatever the size' (line 467) matches line 76 and the twin (size only gates fills).")
row("L04-canon-breaks-quote-rule", "2.4-mathematics / 2.9-prose", "course/modules/PC/PC3/L04.html line 466", PASS,
    "'at a fair value inside the quote the expected change (1-p)h rises with the half-spread h' matches Prop 3.1 with b<=v<=a (both brackets zero). 'Arrival probabilities do not depend on the quote, by A1' matches line 72.")
row("L04-R2-spread-criterion", "2.4-mathematics", "course/modules/PC/PC3/L04.html line 584 (Research R2 solution)", PASS,
    "At v=m both brackets vanish so E=(1-p)h (re-derived). p<1 gives E>0 for all h>=1; p=1 gives E=0 for all h. The statement 'no finite spread selected' follows as written.")
row("L04-E1-seed1-numbers", "2.2-numbers", "course/modules/PC/PC3/L04.html line 552 (Problem E1)", PASS,
    f"Recomputed with the twin's own play(1) ({S}recompute_E_problems.py, output {S}recompute_E_problems.out): 16 fills of 20, cash flow 20100, final inventory -2, settlement 10020, mark -20040, P&L 60. All match line 552.")
row("L04-E2-binomial-z", "2.2-numbers / 2.4-mathematics", "course/modules/PC/PC3/L04.html line 559 (Problem E2)", PASS,
    f"Seed 0 has 13 informed arrivals of 20 (recomputed in {S}recompute_E_problems.out and from the stdout table). sqrt(0.25/20)=0.1118; 0.15/0.1118=1.34; 1.96 is the standard two-sided 5% normal quantile, a textbook constant not an attribution (not graded as a source claim).")
row("L04-E3-mid-vs-settlement", "2.2-numbers", "course/modules/PC/PC3/L04.html lines 564-566 (Problem E3); Remark 2.4 line 122", PASS,
    "Last quote of seed 0 is 9980/10000 (stdout_L04.out turn 20), mid 9990, settlement 9980. P&L at settlement -9950+9980=30; at mid -9950+9990=40; difference 10 = I x (mid - settlement) with I=1. Matches.")
row("L04-problems-R1-R3-M-P", "2.4-mathematics / 2.9-structure", "course/modules/PC/PC3/L04.html lines 498-595", PASS,
    "M1: S/D-type cash +10010, inventory -1, mark 10 (re-derived). M2: sell refused at I=10 (|11|>10), buy allowed (|9|<=10). M3: no trade at v=a, buy at v=a+1 (a loss of 1 cent). P1-P3 proofs re-derived (P3: Var = 25 I^2 = 400 at I=-4). R1: d=(1-p)h/p=20/3 at p=3/5, h=10. R3: 25I^2<100 gives |I|<2, largest integer 1 (variance 25).")
row("L04-quiz-answers", "2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L04.html lines 618-703", PASS,
    "All 12 keys re-derived: +10010; 10 (M1); no trade at v=a; 0 (v=10020); 5 (v=10000); refused fill at +10; 400; zero mean; 20/3 with tolerance 0.001 (6.6667 within 0.001); settlement; 9 fills; rises as (1-p)h. Each item has an explanation block.")
row("L04-quiz-q11-citation", "2.9-prose", "course/modules/PC/PC3/L04.html line 692", PASS,
    f"Quiz item 11 key 9 equals the fills count printed in Part 1 ('fills 9 of 20 turns', {S}stdout_L04.out). Explanation cites Lab 1, Part 1 correctly.")
row("L04-misconceptions", "2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L04.html lines 473-489", PASS,
    f"Four misconceptions. Their numbers check: 0 cents at v=10020 (stdout Part 2), 10010-10000=10 cents for the uninformed-buy P&L, variance 2500 cents^2 at I=10 (stdout Part 3), 50 cents SD at 10 units (Remark 4.2).")
row("L04-scope-and-banned-phrases", "2.9-prose", "course/modules/PC/PC3/L04.html, L05.html, L06.html", PASS,
    "grep (case-insensitive) for BUILDER_RULES 1.3-1.4 banned phrases (TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, important to note, studies show, experts agree, well known, obvious, clearly, it can be shown, historically, roughly) and process words (builder, verifier, round, architect, agent, REQUEST): zero hits in prose. Scope words checked one by one (every, all, always, only, same, exactly, any); each has a computation or an explicit hypothesis.")
row("L04-structure-hours", "2.9-structure", "course/modules/PC/PC3/L04.html lines 2, 35, 52, 54-161, 178-460, 462-468, 470-490, 492-595, 597-612, 614-704", PASS,
    "Order: why it matters (115 words, <=120), numbered sections, inline lab, canon breaks, misconceptions (4, >=3), problem set (3 per tier, 12 total with <details class=solution>), key results table, quiz (12 items, 8-15, each with explain). data-hours=6; PC3 index hours split 36 lesson + 14 project = 50 = curriculum hours (curriculum.json PC3 hours 50).")
row("L04-DAG-D-terms", "2.9-DAG", "course/modules/PC/PC3/L04.html line 52 (inventory dfn) and line 158 (adverse selection, now plain)", "FAIL",
    f"Adverse selection (line 158) is now plain prose with no dfn: the round-2 FAIL is fixed. A new defect remains: line 52 contains '<dfn>inventory</dfn>'. The term is the D4 concept family (plan section 4 row D4: inventory-model, MS1, outside the closure, 'Plain prose, no link'), and the Architect default says concepts outside the closure are 'plain prose with no link and no dfn'. check_dag.py passes because it ignores dfn without data-concept ({S}check_dag.out). The mark-to-market value dfn at line 97 is not a registered concept and is not a redefinition of FC2's marking to market (FC2 L03 line 62 defines variation margin) and is not counted.",
    "Line 52: replace '<dfn>inventory</dfn>' with plain text 'inventory' (keep '(the units the maker holds)'). No other change is needed for this row.")
row("L04-A1-project-consistency", "2.4-notation / 2.9-prose", "course/modules/PC/PC3/L04.html line 72 (A1); course/modules/PC/PC3/project.html line 404; tests/labs/PC3/lab-PC3-project-1.py lines 37-44", PASS,
    "project.html line 404 states 1/4 uninformed buy, 1/4 uninformed sell, 1/2 informed, matching A1 at line 72 and project-1 twin draw thresholds 0.25 and 0.5.")
row("L04-key-results-prop-3.1-assumptions", "2.4-mathematics / 2.9-prose", "course/modules/PC/PC3/L04.html line 605 (key-results row for Proposition 3.1)", "FAIL",
    "The key-results row cites 'Proposition 3.1, proved in section 3 under A1, A3, A4 and A6', but the proof of Prop 3.1 cites A5 explicitly at line 135 ('the fill occurs (A5)'), and the hypothesis (H2) relies on q_t>=1 and L>=1, which are A5's conditions. The summary omits A5, so the list of assumptions is incomplete.",
    "Line 605: change 'under A1, A3, A4 and A6' to 'under A1, A3, A4, A5 and A6'.")
# ---- L05
row("L05-def-3.1-markup", "2.4-mathematics / 2.9-prose", "course/modules/PC/PC3/L05.html line 106 (Definition 3.1)", PASS,
    "Definition 3.1 (surviving index, deque invariant) matches the pseudocode (lines 113-120) and Prop 3.2 Step A. 'monotonic-deque' link resolves to the CS2 concept (concepts.html#monotonic-deque exists once). The local dfn 'surviving at step i' is not a registered concept.")
row("L05-prop-2.1-2.2-remark", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 85-98", PASS,
    f"Prop 2.1 count (n-k+1)(k-1): the twin's naive_maxima makes k-1 comparisons per window ({S}stdout_L05.out: naive 1351). Remark 2.2: (n-r)r = n^2/4 - (r-n/2)^2 re-derived; maximum at k = n/2+1 for even n.")
row("L05-prop-3.2-correctness", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 123-133 (Proposition 3.2, proof Steps A-C)", PASS,
    "Round-2 FAIL fixed at HEAD: line 131 now reads 'f&lt;p\\le i' (escaped). tag_scan.py reports zero parse errors for L05 at HEAD (ledgers/PC3/scripts/PC3-b-r3/tag_scan.out) and reports 4 errors at 67c47689, so the fix is verified. Re-derived Steps A, B, C: invariant, last-occurrence maximum survives, front is window maximum. Outputs equal for k=1..20 (stdout_L05.out).")
row("L05-prop-3.3-bound", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 135-143", PASS,
    "n appends, at most n removals, at most 2n while-loop tests re-derived. Lab 1: 354 comparisons, 199 pops, 200 pushes at k=8 (stdout_L05.out), within 2n=400.")
row("L05-remark-3.4-k-range", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 147 (Remark 3.4)", PASS,
    "x=(k,k-1,...,2,k+1), n=k: at step k the deque holds 1..k-1 in decreasing value and x_k=k+1 removes all k-1 in one loop (re-derived).")
row("L05-example-3.5-trace", "2.4-mathematics", "course/modules/PC/PC3/L05.html line 152 (Example 3.5)", PASS,
    "Traced by hand for x=(3,1,4,1,5), k=3: deques (1), (1,2), (3), (3,4), (5); outputs (4,4,5). Matches the page.")
row("L05-problems-M-P", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 350-396 (M1-M3, P1-P3)", PASS,
    "Round-2 FAIL fixed: lines 391 and 393 now use &lt;. M1 = 21 re-derived. M2 trace of (2,5,1,0,3), k=2 re-derived: outputs (5,5,1,3). M3 k=1 and k=n re-derived. P1: (n-r)r<=n^2/4 and k=101 for n=200 (count 10000). P2 survival argument re-derived. P3: n-1 comparisons for every k (re-derived by hand; the twin's deque on n=50 is consistent).")
row("L05-E1-E3-numbers", "2.2-numbers", "course/modules/PC/PC3/L05.html lines 400-420 (E1-E3); expected block lines 292-314", PASS,
    f"E1: 169*31=5239 and 5239/382=13.7 (stdout_L05.out k=32 row). E2 (seed 6): recomputed with the twin's functions: outputs equal, naive 1351, deque comparisons 350, pushes 200, pops 197, matching the page's '350 ... 200 pushes and 197 pops' ({S}recompute_E_problems.out). E3: window 200 gives 387 comparisons, 200 pushes, 194 pops; 194+200=394 >= 387.")
row("L05-R1-scope-sentence", "2.9-prose", "course/modules/PC/PC3/L05.html line 429 (Research R1 solution)", PASS,
    "Protocol criterion; the sentence that the lesson proves operation counts and bounds but no timing result matches the page (no timing in lab, stated at line 157).")
row("L05-R2-R3", "2.4-mathematics", "course/modules/PC/PC3/L05.html lines 433-445", PASS,
    "R2: k=101, count 10000 (Remark 2.2) re-derived. R3: a strictly increasing sequence removes one from the back at each step i>=2 (re-derived) and P3 gives n-1 comparisons for every k.")
row("L05-key-results-grades", "2.3-grades", "course/modules/PC/PC3/L05.html line 460 (key-results row for seed 5)", PASS,
    "Round-2 FAIL fixed: the row is now grade C with source 'Lab 1, Part 2 (seeded sequence, seed 5, window sizes 1 to 20; Proposition 3.2 is the proof for every sequence)'. A lab check on one generated sequence is C under BLUEPRINT section 3 (a result read off a lab), and the general statement is named as Prop 3.2 (T).")
row("L05-quiz-answers", "2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L05.html lines 466-546", PASS,
    "Round-2 FAIL fixed: item 9's explanation (line 534) now reads '(Section 5, Misconception 2)', and Misconception 2 is in Section 5 (line 334). All ten keys re-derived: 21; 400; 10000; the removal bound; 5 windows; n-1; the front is the last occurrence of the maximum (Prop 3.2 Step B); 1351; the counts are not run times; no outputs for a window longer than the sequence (lab Part 2 line 305 check).")
row("L05-misconceptions-canon-breaks", "2.9-prose", "course/modules/PC/PC3/L05.html lines 318-342", PASS,
    "Canon-breaks names the model limit (operation count is not run time, amortised bound, comparability). Misconception 1's '354 comparisons within 400' matches stdout_L05.out. Misconception 3 matches the lab's single-sequence check.")
row("L05-structure-hours", "2.9-structure", "course/modules/PC/PC3/L05.html", PASS,
    "Why it matters 89 words (<=120). Sections 1-3, lab, canon breaks, 3 misconceptions, problem set 12 (3 per tier), key results, quiz 10 items each with explain. data-hours=6.")
row("L05-markup-raw-less-than", "2.9-markup", "course/modules/PC/PC3/L05.html lines 130-131, 391, 393", PASS,
    f"Round-2 FAIL fixed at HEAD: all raw '<' before a letter or backslash inside math is now '&lt;'. {S}tag_scan.py at HEAD: L04 0 errors, L05 0 errors, L06 0 errors, TOTAL 0 (tag_scan.out). The scanner was validated against the 67c47689 pages, where it reports L05 line 131 '</p> closes open <p\\le>', line 391-395 errors, and L06 line 519 (tag_scan on the old pin: 5 issues).")
row("L05-meta-uses-hash-map-heap", "2.9-prose / plan section 3 (L05 content)", "course/modules/PC/PC3/L05.html line 38 (Uses row) and body Sections 1-3", "FAIL",
    f"The Uses row lists 'hash map' and 'binary heap' as concepts the lesson uses, but neither term appears in the body (grep -c -i 'hash\\|heap' on L05.html returns 1, the Uses row only, line 38). Plan section 3 (L05 entry) requires the lesson to cover 'choosing a structure (hash-map, binary-heap, monotonic-deque)'. Only the deque is discussed; Definition 1.1 step 4 is left general.",
    "Either (a) add a Remark in Section 3 comparing the window's needs with a hash map (no order, so no window maximum) and a binary heap (push and pop each O(log n), so n pushes and n pops cost O(n log n) against Proposition 3.3's O(n) total), with the cost statements labelled as model costs, or (b) remove 'hash map' and 'binary heap' from the Uses row (line 38) and from the plan's L05 coverage claim.")
# ---- L06
row("L06-prop-1.1-payoff-identity", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 58-66", PASS,
    "(s-K)^+ - (K-s)^+ = s-K re-derived in both cases s>=K and s<K (lines 65).")
row("L06-remark-1.2-put-call-parity", "2.2-numbers / 2.9-prose", "course/modules/PC/PC3/L06.html line 70 (Remark 1.2)", PASS,
    "Price form cited as the linked FC2 concept (not re-derived), D defined as the discount factor of A2 in Section 2 (line 86). Payoff identity is Prop 1.1.")
row("L06-prop-2.1-forward", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 93-107", PASS,
    f"(i) zero cost, payoff F'-S/D in every state, re-derived. (ii) F'>S/D and F'<S/D cases each contradict A4 with the stated portfolio; A5 used for the short sale. Lab Part 1 prints payoff 0 at F=10000 and 100 at F=10100 in every spot state ({S}stdout_L06.out).")
row("L06-remark-2.2-continuous-convention", "2.9-prose / 2.2-numbers", "course/modules/PC/PC3/L06.html lines 86, 105-106 (A2 and Remark 2.2); canon-breaks line 312", PASS,
    "D=e^{-r tau} and S/D=S e^{r tau} match the linked FC2 concept (FC2 L02 defines cost-of-carry F*=S e^{r tau}; continuous compounding). The linked NPV (CF1 L01 line 61) uses (1+r)^{-t}, i.e. discrete, matching 'the linked net present value is discrete' (line 312).")
row("L06-definition-1.3-NPV-and-prop-3.1", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 74-76, 113-121", PASS,
    "Def 1.3 matches CF1 L01 lines 59-61 exactly. Prop 3.1: NPV(u) = -I + mAu, A>0 for r>-1 and n>=1, unique root u*=I/(mA) (re-derived).")
row("L06-prop-3.2-fermi-bounds", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 124-131", PASS,
    "Induction re-derived: products of positive interval factors attain min product of lower ends and max product of upper ends; both ends attained by choosing each factor at an end.")
row("L06-corollary-3.3-grade", "2.4-mathematics / 2.3-grades", "course/modules/PC/PC3/L06.html lines 133-141", PASS,
    "Corollary re-derived: NPV(u)=mA(u-u*); if l<u*<h the bounds straddle the break-even. Grade T (proof on page) consistent with BLUEPRINT section 3.")
row("L06-example-4.2-numbers", "2.2-numbers", "course/modules/PC/PC3/L06.html line 152 (Example 4.2)", PASS,
    f"Units bounds [200,1600] (2000*1*0.1, 4000*2*0.2). A=3310/1331 (re-derived exactly, {S}recompute_L06.out: A10 exact check True). Break-even 399300/331 = 1206.344 (recomputed exact {S}recompute_L06.out). NPV at 200 negative, at 1600 positive at 10% (exact NPV(lo) = -16655000000/1331, NPV(hi) = 6515000000/1331).")
row("L06-remark-4.3-sensitivity", "2.2-numbers", "course/modules/PC/PC3/L06.html line 157 (Remark 4.3); expected block lines 286-306", PASS,
    f"Recomputed exactly ({S}recompute_L06.out): break-even 1164.1005 at 8%, 1206.3444 at 10%, 1249.0469 at 12%; displayed 1164.10, 1206.34, 1249.05. NPV at the lower bound: -12422903 (8%), -12513148 (10%), -12598169 (12%, half-up of -12598168.73). NPV at upper: 5616776, 4894816, 4214650. Signs negative at 200 and positive at 1600 at all three rates. Matches stdout_L06.out.")
row("L06-E1-12pct", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 390-395 (Problem E1)", PASS,
    f"Annuity at 12% = 52725/21952 = 2.4018313 (recomputed); 3000/2.40183 = 1249.047, displayed 1249.05 (recompute_L06.out).")
row("L06-E2-first-negative", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 397-403 (Problem E2)", PASS,
    f"Exact (recompute_L06_problems.out): NPV(1200) = -105000000/1331 = -78888.05 cents; NPV(1300) = 1550000000/1331 = 1164537.94 cents; positive grid points are 1300, 1400, 1500, 1600 (count 4); largest negative grid point 1200. Matches.")
row("L06-E3-42.71", "2.2-numbers", "course/modules/PC/PC3/L06.html lines 404-409 (Problem E3 solution)", PASS,
    "Unrounded break-evens 1164.1005, 1206.3444, 1249.0469 (exact values recomputed). 1249.0469-1164.1005=84.9464 displays 84.95; /4 = 21.2366 displays 21.24; 1206.3444-1164.1005=42.2439; 1249.0469-1206.3444=42.7025 displays 42.70; 1249.05-1206.34=42.71 (the displayed-difference value, correctly rejected). Matches lines 409-416.")
row("L06-E3-rest-and-quiz-q9", "2.2-numbers / 2.9-prose", "course/modules/PC/PC3/L06.html lines 409-416 (Problem E3) and quiz item 9 (line 521)", PASS,
    "Quiz item 9 (line 521) is the numeric 21.24 with tolerance 0.01; its explanation at line 524 (84.9464/4 = 21.2366) matches the recomputation. The round-2 row id 'quiz-q9' refers to this item.")
row("L06-M1-M3-numbers", "2.2-numbers / 2.4-mathematics", "course/modules/PC/PC3/L06.html lines 345-366", PASS,
    "M1: 49/0.98 = 50; payoff 0.50 (re-derived). M2: NPV = 500/121 = 4.13 (recomputed exact). M3: u* = 1000*1331/(4*3310) = 33275/331 = 100.53 (recomputed exact: 100.5287).")
row("L06-P1-P3-proofs", "2.4-mathematics", "course/modules/PC/PC3/L06.html lines 370-390", PASS,
    "P1 reverse portfolio payoff S/D-F' in every state with zero cost (re-derived; the sentence 'the forward delivers the asset to the long party, which covers the short sale' is awkward but the arithmetic is right). P2: one zero at u*=I/(mA), sign by slope (re-derived). P3: product bounds [200,1600], endpoints (2000,1,1/10) and (4000,2,1/5).")
row("L06-R1-R3", "2.4-mathematics / 2.2-numbers", "course/modules/PC/PC3/L06.html lines 420-440", PASS,
    f"R1: each factor has ratio 2 so each log-width is ln 2 (re-derived; tie). R2: break-even I/sum(m_t(1+r)^-t) re-derived. R3: m* = 15000000*1331/(1600*3310) = 2495625/662 = 3769.83 cents, ratio 0.7540 of 5000, fall 24.6% (recompute_L06_problems.out: 3769.826, 0.753965, 24.603%). The page's 3769.8 and 24.6 are right.")
row("L06-quiz-answers", "2.9-prose / 2.4-mathematics", "course/modules/PC/PC3/L06.html lines 461-536", PASS,
    "Round-2 FAIL (missing </p>) fixed at HEAD: the quiz item explanation at line 524 is closed; tag_scan.py reports zero errors for L06 at HEAD (tag_scan.out). Keys re-derived: 50; F'-S/D; no expectation; 4.13 (|4.13-500/121| = 0.0022 < 0.005); 1206.34 (|1206.34-1206.3444| = 0.0044 < 0.005); nothing decided; 4 grid points; rises strictly; 21.24 (|21.24-21.2366| = 0.0034 < 0.01); balance-sheet cash.")
row("L06-canon-breaks-and-misconceptions", "2.9-prose / 2.2-numbers", "course/modules/PC/PC3/L06.html lines 310-337", PASS,
    f"Canon-breaks: convention remark (discrete NPV, continuous forward) checked against CF1 L01 and FC2 L02. Fermi factor range 'by a factor of 8' = 1600/200 (re-derived). Misconceptions: 1164.10, 1206.34, 1249.05 (stdout_L06.out); 'about 21 units per point' = 84.9464/4 = 21.2366; the bounds-straddle statement; 'sign same at all three rates' (recompute_L06.out).")
row("L06-DAG-and-cross-links", "2.9-DAG", "course/modules/PC/PC3/L06.html lines 38, 39, 56, 78, 86", PASS,
    "Uses links resolve: forward-contract, cost-of-carry-forward-price, put-call-parity, net-present-value, statement-articulation (concepts.html ids exist once each), fermi-estimation (L01.html#def-fermi-estimation, earlier lesson). Introduces case-interview (dfn at line 147, defined once). All are in the PC3 prerequisite closure (plan section 0.2). AC1 L03 line 57 defines 'the cash-flow statement ends at the balance-sheet cash' and the page's statement at line 78 matches it.")
row("L06-structure-hours", "2.9-structure", "course/modules/PC/PC3/L06.html", PASS,
    "Why it matters 76 words (<=120). Sections 1-4, lab, canon breaks, 4 misconceptions, problem set 12 (3 per tier), key results, quiz 10 items with explain. data-hours=6. No excluded topics (CAPM, duration, DCF) appear (plan D6).")
# ---- two new rows for the round-3 pass
row("L04-key-results-table-other", "2.4-mathematics / 2.9-prose", "course/modules/PC/PC3/L04.html lines 603-608 (other key-results rows)", PASS,
    "Rows for Prop 2.2, Prop 2.3, Prop 3.1 (line 605 excepted), Cor 3.3, Prop 4.1 and the lab row re-checked: grades T for proved statements and C for the lab row; sources name the proof section and the lab part. Only the Prop 3.1 assumption list is defective (row L04-key-results-prop-3.1-assumptions).")
row("L05-meta-uses-other", "2.9-prose", "course/modules/PC/PC3/L05.html line 38 (Uses) other entries", PASS,
    "big-O complexity (body line 62), monotonic deque (body Section 3) and unit test (body step 6, line 65) are used in the body. The two defective entries are row L05-meta-uses-hash-map-heap.")

# ---- carry-over rows that are not re-run as separate checks are NOT used: every row above is re-verified in round 3.
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
fragment = {
    "unit": "PC3",
    "slice": "PC3-b",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for PC3-b round 3 (did not build PC3; re-verified L04-L06 and lab twins from scratch at 67a2d13e)",
    "pin": "67a2d13e",
    "base": "67c47689 (round-2 pin). Delta 67c47689..67a2d13e touches L04.html, L05.html, L06.html (round-2 fixes) and cards.json/project.html (other slices). The three lab twins are byte-identical across the delta and since 1c1645f3. No row carried: every subject page changed, so every row was re-verified.",
    "checkout": root,
    "scratch": "/Users/billyribeiro/.fanout/scratch/PC3-b-r3-old",
    "verified_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Slice PC3-b: course/modules/PC/PC3/L04.html, L05.html, L06.html and tests/labs/PC3/lab-PC3-L04-1.py, lab-PC3-L05-1.py, "
        "lab-PC3-L06-1.py, read in full (L04 721 lines, L05 563, L06 553; twins 228, 134, 123). "
        "Every round-2 row id is kept (70 ids) and two rows are added (L04-key-results-prop-3.1-assumptions, L05-meta-uses-hash-map-heap), "
        "plus two support rows (L04-key-results-table-other, L05-meta-uses-other). "
        "Mutants: none, because lab twins are demonstrations and mutation testing applies only to project graders (architect ruling). "
        "Not checked: (1) a visual Chromium render of the pages (the markup defects are verified by the tokenizer scan, not a screenshot); "
        "(2) cards.json, project.html grader, rubric and the index hub's other content (other slices); "
        "(3) live verify_refs --unit PC3 (the slice cites no registry key); "
        "(4) the 1.96 two-sided normal quantile in Problem E2 is a textbook constant, not computed on the page and not sourced; accepted as a standard constant, as in round 2; "
        "(5) the L04 Uses row's 'expected-value game' link is not used by name in the body (it is the basis of the expectation work); not counted as a failure; "
        "(6) the L06 P1 sentence 'the forward delivers the asset to the long party, which covers the short sale' is awkward in wording but the arithmetic is right; not counted."
    ),
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
        "fail_rows": [r["id"] for r in rows if r["status"] != "PASS"],
    },
}
out = f"{root}/ledgers/PC3/PC3-b.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, fragment["summary"])
