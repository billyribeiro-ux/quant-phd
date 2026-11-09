"""Write the CS2 slice c round 1 ledger fragment (verifier-authored rows; CS2 slice c round 1)."""
import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyS1-CS2-c")
PIN = "aeb512b65b7774b59b84f836a13984fcfe9d0d1f"
S = "ledgers/CS2/scripts/CS2-c-r1/"

rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates and tools -------------------------------------------------------
row("C-01", "2.9 structure: check_pages (unit and per page)",
    "course/modules/CS/CS2/L09.html, L10.html, L11.html, cards.json", "PASS",
    "tools/check_pages.py --unit CS2 -> 'check_pages CS2: PASS' (exit 0); --page L09, --page L10, --page L11 each PASS. "
    "The tool enforces the banned-phrase list, the why-it-matters word limit (<=120), 6-12 declared hours, the minimum "
    "counts and the card rules; none fired.")
row("C-02", "2.9 DAG: check_dag and concept links",
    "course/modules/CS/CS2/L09.html:38,65; L10.html:38,67; L11.html:38,76", "PASS",
    "tools/check_dag.py --unit CS2 -> 'check_dag CS2: PASS' (exit 0). dfn ids def-welford-algorithm (L09:65), "
    "def-monotonic-deque (L10:67), def-quantile-sketch (L11:76) each occur once. Links to L01#def-big-o-complexity "
    "(L09:38, L10:38) and L04#def-comparison-sorting, L04#def-binary-search (L11:38) point to earlier lessons.")
row("C-03", "2.5 labs: run_labs, page code equals twin, expected equals output",
    "course/modules/CS/CS2/L09.html:119-216; L10.html:118-210; L11.html:142-258", "PASS",
    "tools/run_labs.py --unit CS2 --page L09 / L10 / L11 -> 'run_labs CS2: PASS (1/1)' each (exit 0). The tool checks the "
    "page code byte-for-byte against tests/labs/CS2/lab-CS2-L09-1.py, L10-1.py, L11-1.py and the expected block against "
    "the twin's stdout.")
row("C-04", "2.5 labs: twins alone under python -I -W error",
    "tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py", "PASS",
    "python -I -W error <twin>: exit 0 and 0 bytes on stderr for all three. Stdout saved at " + S + "twin_L09.out (12 lines), "
    "twin_L10.out (5 lines), twin_L11.out (2 lines); each equals the page's expected block (L09:205-216, L10:206-210, "
    "L11:257-258).")
row("C-05", "2.5/2.9 page_smoke (Chromium, run alone on the three pages)",
    "course/modules/CS/CS2/L09.html, L10.html, L11.html", "PASS",
    "tools/page_smoke.py --unit CS2 --pages L09 L10 L11 -> 'page_smoke CS2: PASS' (exit 0); each page PASS: zero console "
    "errors, math renders, no external request, no horizontal scroll at 360 px, every lab runs (L09 0.1 s, L10 0.0 s, "
    "L11 0.0 s). Log: " + S + "page_smoke_L09-L11.txt. These pages carry no figures.")
row("C-06", "gate: ruff check and ruff format --check on the three twins",
    "tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py", "PASS",
    "ruff check -> 'All checks passed!'; ruff format --check -> '3 files already formatted'.")
row("C-07", "gate: mypy --no-incremental on the three twins",
    "tests/labs/CS2/lab-CS2-L09-1.py, lab-CS2-L10-1.py, lab-CS2-L11-1.py", "PASS",
    "mypy --no-incremental <three twins> -> 'Success: no issues found in 3 source files'.")
row("C-08", "gate: relevant pytest",
    "tests/test_labs.py -k CS2", "PASS",
    "pytest tests/test_labs.py -k CS2 -q -> 14 tests, 100% passed, exit 0.")
row("C-09", "2.1 citations: registry integrity and keys cited on the slice",
    "course/modules/CS/CS2/L09.html, L10.html, L11.html; references/references.json", "PASS",
    "tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems' (exit 0). The three pages carry zero "
    "data-cite and zero data-locator attributes (grep count 0), so no registry key is attributed on this slice. The live "
    "run (--unit) needs network access and was not run; no claim on the slice needs it.")
row("C-10", "2.9 hours arithmetic",
    "course/modules/CS/CS2/index.html; L01-L11 data-hours", "PASS",
    "Lesson data-hours CS2 L01..L11 = 8,9,10,10,9,9,10,10,10,8,7 (sum 100) = index.html data-hours-lessons=\"100\". "
    "L09 10 h, L10 8 h, L11 7 h match the build plan split. Project 30 = data-hours-project. 100 + 30 = 130 = the CS2 "
    "curriculum entry hours (curriculum/curriculum.json CS2 entry).")

# ---- labs ------------------------------------------------------------------
row("C-11", "2.5 lab L09: hypothesis, interpretation and expected block vs output",
    "course/modules/CS/CS2/L09.html:121,217; tests/labs/CS2/lab-CS2-L09-1.py", "PASS",
    "Hypothesis (L09:121): offset 0 errors all below 1e-14 (expected L09:206-208: 9.258e-16, 2.819e-17, 7.286e-15); "
    "two-pass most accurate at all three offsets (L09:206-216); naive error rises 7.286e-15 -> 1.418e-02 -> 1.000 and is "
    "0.000000e+00 at 1e9 (L09:208, 212, 216); Welford error stays below naive at each offset. Re-derived with exact "
    "Fractions in " + S + "l09_numbers.py (relative errors 9.25811790803366e-16, 8.851711977883603e-11, 7.449311491697682e-08 "
    "for Welford; naive 7.285854280028804e-15, 0.01418496900662534, 1.0). SIMULATED label present (L09:217, twin docstring).")
row("C-12", "2.5 lab L10: hypothesis and interpretation vs code and output",
    "course/modules/CS/CS2/L10.html:120,211; tests/labs/CS2/lab-CS2-L10-1.py:71-79", "PASS",
    "Hypothesis (L10:120): brute-force equality and the window-size bound are checked; the operation bound is not asserted. "
    "Code: lines 71-76 raise AssertionError only on brute-force mismatch or deque size > window; line 79 prints '2N = 400' "
    "beside the count. Interpretation (L10:211) totals 396-399 (output min 399,398,398,397,396; max 399,399,398,398,397), "
    "largest single-push removals 1,2,5 for w=1,2,5 and 6 for w=13,30, deque size 10 at w=30: all match the expected block "
    "L10:206-210 and the twin run (" + S + "twin_L10.out). The 2n-1 and n-w claims were re-run in " + S + "worked_examples.py.")
row("C-13", "2.5 lab L10: twin docstring states what the lab checks",
    "tests/labs/CS2/lab-CS2-L10-1.py:6; course/modules/CS/CS2/L10.html:120", "FAIL",
    "Twin docstring line 6 reads 'The total number of deque operations (appends plus removals) for each deque is counted and "
    "compared with 2N.' The code asserts no operation bound (lines 71-76 assert brute-force equality and size only), and the "
    "page at L10:120 says 'It does not assert the operation bound'. Under rule 2 the docstring is a statement about what the "
    "lab checks, and it contradicts the page.",
    "Change twin line 6 to '... is counted, and 2N is printed beside it.' (no 'compared'), then re-embed the page with "
    "tools/embed_labs.py course/modules/CS/CS2/L10.html --refresh lab-CS2-L10-1, and confirm with "
    "tools/run_labs.py --unit CS2 --page L10 that the page code still equals the twin.")
row("C-14", "2.5 lab L11: hypothesis, claims in code, interpretation, expected block",
    "course/modules/CS/CS2/L11.html:144,259; tests/labs/CS2/lab-CS2-L11-1.py:97-109", "PASS",
    "Hypothesis (L11:144): both inequalities of Definition 1.2 asserted for nine probes (twin lines 99-100 raise on failure); "
    "printed deficit read as zero and asserted only <= eps (line 99 is the same condition). Expected block (L11:257-258) "
    "matches the twin run (" + S + "twin_L11.out). Interpretation (L11:259): exact counts by sorting and bisect (twin lines "
    "86-98), sketch sorts only buffers and stored pairs (lines 58, 73), SIMULATED label present. Re-derived by " + S +
    "l11_numbers.py: pass True for both epsilons, excess 0.0212 and 0.0442, deficit 0.0, stored 500 and 220.")

# ---- mathematics -----------------------------------------------------------
row("C-15", "2.4 math: Lemma 1.3 (sum of squares identity)",
    "course/modules/CS/CS2/L09.html:72-80", "PASS",
    "Expansion sum (x_i-m)^2 = sum x_i^2 - 2m sum x_i + n m^2 at m = xbar_n gives sum x_i^2 - n xbar_n^2 (re-derived by hand). "
    "Identity checked with exact Fractions over 200 random rational streams (" + S + "l09_worked_examples.py: True).")
row("C-16", "2.4 math: Theorem 2.1 (one step) and its algebra",
    "course/modules/CS/CS2/L09.html:84-95", "PASS",
    "Each step re-derived: n M_n = (n-1)M_{n-1} + x_n; x_n - M_n = d(n-1)/n; the true difference of sums "
    "x_n^2 - n M_n^2 + (n-1) M_{n-1}^2 = d^2 (n-1)/n equals the update's increment. Welford exact identity over 200 streams: "
    "True (l09_worked_examples.py).")
row("C-17", "2.4 math: Theorem 2.2 (induction) and its cited induction principle",
    "course/modules/CS/CS2/L09.html:97-105; course/modules/M/M1/L06.html:64", "PASS",
    "Base case M_1 = x_1, S_1 = 0 correct; inductive step uses hypothesis (4) and Theorem 2.1. The citation 'Theorem 1.2 of "
    "M1 Lesson 6' matches course/modules/M/M1/L06.html:64, 'Theorem 1.2 (the induction principle)'. L10:79 cites the same.")
row("C-18", "2.4 math: Corollary 2.3 (six operations, O(1))",
    "course/modules/CS/CS2/L09.html:107-115", "PASS",
    "The six operations (subtraction, division, addition for M; subtraction, multiplication, addition for S) are counted "
    "correctly; the constant c = 6 witnesses O(1) in the Lesson 1 sense (L01 definition by witnesses).")
row("C-19", "2.2/2.4 problem sets L09 (M1-M3, P1-P3, E1-E3, R1-R3)",
    "course/modules/CS/CS2/L09.html:253-352", "PASS",
    "M1: sum 40, mean 5, S_8 = 32, 32/7, 4 (exact). M2: M_2=1.5, S_2=0.5, M_3=2, S_3=2. M3: S_4=1, pop var 1/4 = p(1-p). "
    "P1 S_2 = d^2/2; P2 constant stream; P3 merge identity (exact over 200 random cases: True). R1 weighted recursion exact "
    "over 200 streams (True); example M_2=7/4, S_2=3/4 (script output). R3: 0.24 = 6/25, S_10 = 2.4. E1 (zero naive "
    "estimate) and E2 (absolute error) are recomputed in " + S + "l09_numbers.py; E3 is a stated hypothesis, not a claim. "
    "All other items re-derived in " + S + "l09_worked_examples.py.")
row("C-20", "2.4 math: Theorem 2.2 and Theorem 2.3 (L10), front invariant",
    "course/modules/CS/CS2/L10.html:72-92", "PASS",
    "Invariant D_i = S_i proved by induction: cases (a) block removal at the back, (c) expiry block at the front, and both "
    "inclusions re-derived (L10:80-81). Theorem 2.3 'latest position attaining the minimum' argument re-derived (L10:91). "
    "Front equals window minimum for the lab series (lab Expected block; twin).")
row("C-21", "2.4 math: Theorem 2.4 (2n bound) and Corollary 2.5 (a), (b), (c)",
    "course/modules/CS/CS2/L10.html:96-114", "PASS",
    "n appends plus at most n removals gives <= 2n (L10:103). Comparison count: each step-(1) comparison either removes or "
    "stops the loop, <= 2n. Corollary 2.5(c) example re-run in " + S + "worked_examples.py: one insertion removes w entries for "
    "w=1,2,5 (outputs 1,2,5). (b) D_i subset of W_i gives |D_i| <= w.")
row("C-22", "2.2/2.4 problem sets L10 (M1-M3, P1-P3, E1-E3, R1-R3)",
    "course/modules/CS/CS2/L10.html:247-341", "PASS",
    "Re-run with the deque code in " + S + "worked_examples.py: M2 deques equal L10:258 at every step; M3 removals per position "
    "[0,1,0,2,0], total ops 8 <= 10; E1 2n-1 at n=1,2,5,200 (399 at 200); E2 removes 5 at i=5; E3 19 for n=10 at w=1,3,10; "
    "R1 looser rule front = window minimum and values non-decreasing over 300 random series (True); R2 deque [(1,1),(2,4)] "
    "at i=2; R3 removals n-w (7 and 8 for (10,3) and (12,4)). P1-P3 proofs read and correct.")
row("C-23", "2.4 math: Lemma 2.3 (telescoping partial sums)",
    "course/modules/CS/CS2/L11.html:95-104", "PASS",
    "1/((h+1)(h+2)) = 1/(h+1) - 1/(h+2) telescopes to 1 - 1/(H+2) < 1 for every integer H >= 0 (H=0 gives 1/2). "
    "Statement and proof re-derived; no limit used.")
row("C-24", "2.4 math: Theorem 2.2 (weight conservation, compaction bound) and Theorem 2.4 (rank error)",
    "course/modules/CS/CS2/L11.html:84-115", "PASS",
    "Weight: a compaction removes k_h 2^h and adds (k_h/2) 2^{h+1} (L11:91). Compaction bound via P_{h+1} <= P_h <= n "
    "(L11:92). Theorem 2.4: per-compaction change in Rhat(v)-R(v) is 2^h(2 floor(c/2) - c) in {0, -2^h} (L11:113), so "
    "-E <= diff <= 0; E <= eps n via C_h 2^h <= n/k_h, k_h >= (h+1)(h+2)/eps and Lemma 2.3 (L11:114). Checked on the lab "
    "stream: per-level compactions {0:125, 1:20, 2:5, 3:1} equal floor(5000/(k_h 2^h)) (" + S + "l11_numbers.py).")
row("C-25", "2.4 math: Theorem 2.5 (quantile answer satisfies Definition 1.2) and Corollary 2.6 (memory)",
    "course/modules/CS/CS2/L11.html:117-138", "PASS",
    "Upper count: R(v) >= Rhat(v) >= W_{j*} >= qn (L11:125). Lower count: Rhat^-(v) <= W_{j*-1} < qn or j*=1 gives 0 "
    "(L11:126). Corollary 2.6: 2^h <= P_h <= n bounds the level count; k_h - 1 <= (h+1)(h+2)/eps + 1; the telescoped "
    "sum (L+1)(L+2)(L+3)/3 re-derived (sum m(m+1) to M = 13 is 910). Exact checks in " + S + "l11_numbers.py: all nine probes "
    "pass on the lab stream, a sorted stream, a reversed stream and a second seed.")
row("C-26", "2.2/2.4 problem sets L11 (M1-M3, P1-P3, E1-E3, R1-R3)",
    "course/modules/CS/CS2/L11.html:289-392", "PASS",
    "M1 k_0..k_2 at eps=1/10 = 20, 60, 120 (script). M2 running totals 1,3,7 and value 5 (by hand). M3 and E1 by simulation "
    "(" + S + "worked_examples.py): 40 values -> level 1 holds 20 items, total weight 40; 39 values -> 10 at level 1 and 19 at "
    "level 0, stored 29, weight 39, E = 1. E2 per-level bounds 125, 20, 5, 1 sum 151 (the printed compaction count); "
    "eps=1/10 gives 250+41+10+3+1 = 305. R2 sign reversal (odd positions give +1 when c odd) re-derived. R3 = 18187 exact.")

# ---- numbers in prose -------------------------------------------------------
row("C-27", "2.2 numbers: L09 prose and key results",
    "course/modules/CS/CS2/L09.html:117,217,223,224,234,238,314,365", "PASS",
    "Recomputed from unrounded values in " + S + "l09_numbers.py: exact sample variance 0.08728110122738864 (offset 0), "
    "0.08728110122651767 (1e6), 0.0872811009301336 (1e9); running sum of squares at 1e9 = 2.0000000020427427e21 (page: "
    "2.0000000020e21); math.ulp(2e21) = 262144.0; (n-1) s^2 at 1e9 = 174.4749207593 (page 174.4749 via 1999 x 0.08728110093); "
    "E2 absolute error = 0.0872811 x 9.25811790803366e-16 = 8.0806e-17 -> 8.1e-17 (page); E1 '0.0872811' is the 7-digit "
    "value; sys.float_info.mant_dig = 53 in the venv's CPython 3.14.8. Line 217 is the offset 1e9 context (the 0.08728110093 "
    "value is the 1e9 exact variance).")

row("C-28", "2.2 numbers: L09 ratios of errors",
    "course/modules/CS/CS2/L09.html:238 (misconception 2), 223", "PASS",
    "From unrounded relative errors (l09_numbers.py): naive/Welford = 7.86969 (page: 7.87, 'about 8'), 1.60251e8 (page 1.60e8), "
    "1.34241e7 (page 1.34e7). Ratios from the printed three-digit values (7.286e-15/9.258e-16 = 7.87, 1.418e-2/8.852e-11 = "
    "1.60e8, 1/7.449e-8 = 1.34e7) agree to two digits, as the page states.")
row("C-29", "2.2 numbers: L10 prose and key results",
    "course/modules/CS/CS2/L10.html:52,61,211,232,356,397; quiz L10:394-397", "PASS",
    "Totals 396-399 (min over 5 windows 396, max 399), bound 400, deque size 10 at window 30, removals 5 at window 5 and 6 at "
    "windows 13/30 re-derived by running the twin (" + S + "twin_L10.out). 2n = 400 at n = 200. The '2n-1' and 'n-w' "
    "statements are verified in worked_examples.py.")
row("C-30", "2.2 numbers: L11 prose, key results and quiz",
    "course/modules/CS/CS2/L11.html:52,259,266,276,356,406; quiz L11:425-489", "PASS",
    "l11_numbers.py: largest excess/N 0.0212 (eps 1/20) and 0.0442 (eps 1/10), each below eps; deficit 0.0 both; stored 500 "
    "and 220; compactions 151 and 305; capacities 40/120/240 and 20/60/120; closed form 198430 at n=1e9 (L=29), 18213 at "
    "n=5000 (L=12), exact Corollary 2.6 sum 18187; all match the page. (9087 and 9113 are eps=1/10 values not quoted on the page.)")

# ---- grades ------------------------------------------------------------------
row("C-31", "2.3 grades: L09 claim spans and key results",
    "course/modules/CS/CS2/L09.html:85,98,108,361-365", "PASS",
    "Theorems 2.1, 2.2 and Corollary 2.3 carry claim spans graded T; key rows 361-364 are T and point to proofs on the page; "
    "row 365 is C and names Lab 1 (SIMULATED stream, one seed). Cards c123, c124, c193-c195 are C naming Lab 1. "
    "Lemma 1.3 is T in the table and card c119 but its block has no claim span (see C-36).")
row("C-32", "2.3 grades: L10 claim spans and key results",
    "course/modules/CS/CS2/L10.html:73,85,97,107,352-356", "PASS",
    "Theorems 2.2, 2.3, 2.4 and Corollary 2.5 graded T; key rows 352-355 T with proofs on the page; row 356 C naming Lab 1. "
    "Cards c136, c154, c231, c234 are C naming Lab 1; cards for proven results are T.")
row("C-33", "2.3 grades: L11 claim spans and key results",
    "course/modules/CS/CS2/L11.html:85,107,118,130,402-406", "PASS",
    "Theorems 2.2, 2.4, 2.5 and Corollary 2.6 graded T; key rows 402-405 T; row 406 C naming Lab 1. Cards c150, c198-c202 C naming "
    "Lab 1; the key-results row and its cards carry the same grade and basis (architect ruling 13).")
row("C-34", "2.3 grades: Lemma 1.3 claim markup",
    "course/modules/CS/CS2/L09.html:73", "FAIL",
    "The block title is '<span class=\"block-title\">Lemma 1.3 ...' with no claim span or data-grade. Lemma 1.3 is a substantive "
    "claim: the key-results table grades it T (L09:361) and card CS2-c119 is T. BUILDER_RULES §2.1 requires every substantive "
    "claim to carry the markup; M1 lessons mark their lemmas 'block-title claim' with data-grade (course/modules/M/M1/L02.html:97, 107).",
    "Change L09.html:73 to '<span class=\"block-title claim\" data-grade=\"T\">Lemma 1.3 <span class=\"name\">(sum of squares "
    "identity)</span></span>', then re-run check_pages --unit CS2.")
row("C-35", "2.3 grades: Lemma 2.3 claim markup",
    "course/modules/CS/CS2/L11.html:96", "FAIL",
    "The block title is '<span class=\"block-title\">Lemma 2.3 ...' with no claim span or data-grade. Lemma 2.3 is used in "
    "Theorem 2.4 (L11:114) and card CS2-c144 grades it T, so the grade is asserted but not marked on the claim. Same convention "
    "as M1 lemmas (course/modules/M/M1/L02.html:97, 107).",
    "Change L11.html:96 to '<span class=\"block-title claim\" data-grade=\"T\">Lemma 2.3 <span class=\"name\">(the capacity series "
    "sums to one)</span></span>', then re-run check_pages --unit CS2.")

# ---- DAG, notation, attribution, prose --------------------------------------
row("C-36", "2.9/notation: DAG usage outside closure, definitions in place",
    "course/modules/CS/CS2/L09.html:60; L10.html:67; L11.html:38,62-63,76", "PASS",
    "'variance' appears only as plain formulas (L09:60, Definition 1.1; L09 Corollary 2.3, P3, quiz) and "
    "'quantile' only as plain words (L11:62-63, Definition 1.2 'approximate quantile'); both are the architect's issue-2/Q2 decision (no dfn, no "
    "link). The induction link (L09:38, L10:38, L11:38) points to M1 (prereq now in CS2's closure). L11 links L04 (earlier "
    "lesson). Each concept owned by these lessons is defined once.")
row("C-37", "2.6/notation: registry symbols and macros",
    "course/modules/CS/CS2/L09.html, L10.html, L11.html; notation/notation.json", "PASS",
    "No registered symbol (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) and no registered macro "
    "(\\R, \\E, \\Var, ...) appears in the slice's math (grep: 0 hits). Local letters (S_n, M_n, d, W_n, D_i, S_i, R(v), "
    "R^-(v), E, C_h, k_h, P_h, sigma_n^2) are defined in place, as notation.json's 'about' field allows.")
row("C-38", "2.9 attributions: cross-unit and textbook citations",
    "course/modules/CS/CS2/L09.html:104; L10.html:79; course/modules/M/M1/L06.html:64", "PASS",
    "The only cross-unit theorem number, 'Theorem 1.2 of M1 Lesson 6', matches M1 L06 line 64 (the induction principle). No "
    "statement, locator or theorem number is attributed to cormen2022introduction on these pages.")
row("C-39", "2.9 prose: process words, unfinished text, terms before definition",
    "course/modules/CS/CS2/L09.html, L10.html, L11.html", "PASS",
    "grep for builder, verifier, round, TODO, TBD, lorem, 'can be shown', clearly, obviously, trivial, honest: 0 hits. "
    "'stream' appears in the L09 why-it-matters (L09:52) before its definition (L09:56) as plain English, not a concept key; "
    "no defect. Learner text uses no process language.")
row("C-40", "2.9 prose: scope words (every, all, always, never, exact, stable, only)",
    "course/modules/CS/CS2/L09.html:52-238; L10.html:61-231; L11.html:52-275", "PASS",
    "Every scope claim traced: 'every stream' rests on Theorems 2.2 (L09), 2.4 and 2.5 (L11) and the lab says 'one stream' "
    "(L11:259); 'exact' is tied to hypothesis 3 with the floating-point caveat (L09:117, 223); 'stable' is disclaimed "
    "(L09:223); 'constant time' is corrected (L10:227, 217); 'every value' is corrected (L10:231); 'bounded set' (L11:52) "
    "is supported by Corollary 2.6; 'no comparison with other sketch designs' (L11:266) is an explicit non-claim.")
row("C-41", "2.9 structure: section order and minimum counts L09",
    "course/modules/CS/CS2/L09.html", "PASS",
    "Order matches BUILDER_RULES §4.2: why (L09:52); core sections 1-2 (L09:54, 82); inline lab (L09:119); canon-breaks "
    "(L09:220); misconceptions (L09:229, 3 items); problems (L09:247, four tiers of three); key results (L09:355, five rows); "
    "quiz (L09:371, 9 items with explanations); references (L09:443). No debate key on CS2 (none required).")
row("C-42", "2.9 structure: section order and minimum counts L10",
    "course/modules/CS/CS2/L10.html", "PASS",
    "Order: why (L10:52); sections 1-2 (L10:54, 63); lab (L10:118); canon-breaks (L10:214); misconceptions (L10:223, 3 items); "
    "problems (L10:241, four tiers of three); key results (L10:346, five rows); quiz (L10:362, 10 items with explanations); "
    "references (L10:443).")
row("C-43", "2.9 structure: section order and minimum counts L11",
    "course/modules/CS/CS2/L11.html", "PASS",
    "Order: why (L11:52); sections 1-2 (L11:54, 70); lab (L11:142); canon-breaks (L11:262); misconceptions (L11:271, 3 items); "
    "problems (L11:289, four tiers of three); key results (L11:396, five rows); quiz (L11:412, 10 items with explanations); "
    "references (L11:493).")

# ---- cards -------------------------------------------------------------------
row("C-44", "2.7 cards sample (1 in 10): CS2-c116 (L09)",
    "course/modules/CS/CS2/cards.json:823", "PASS",
    "Front 'What is an online statistic?' matches the definition at L09:56; grade T; no proposition cited.")
row("C-45", "2.7 cards sample (1 in 10): CS2-c126 (L09)",
    "course/modules/CS/CS2/cards.json:896", "PASS",
    "Matches L09:117 and 223 (floating-point caveat) and Theorem 2.2 hypothesis (3). T is right for the statement that the "
    "theorem does not by itself bound floating-point error.")
row("C-46", "2.7 cards sample (1 in 10): CS2-c135 (L10)",
    "course/modules/CS/CS2/cards.json:959", "PASS",
    "Matches Corollary 2.5(c) (L10:108) and its series (x_0 < ... < x_{w-1} then a smaller value); hypotheses present.")
row("C-47", "2.7 cards sample (1 in 10): CS2-c200 (L11)",
    "course/modules/CS/CS2/cards.json:1441", "PASS",
    "C grade, names Lab 1; 'all nine probes pass at both epsilons' matches the expected block (L11:257-258) and the rerun.")
row("C-48", "2.7 cards sample (1 in 10): CS2-c205 (L11)",
    "course/modules/CS/CS2/cards.json:1465", "PASS",
    "'20 items' at level 1 after 40 adds at eps=1/10 matches M3 (L11:313); re-simulated in worked_examples.py.")
row("C-49", "2.7 cards sample (1 in 10): CS2-c207 (L11)",
    "course/modules/CS/CS2/cards.json:1472", "PASS",
    "Deficit <= 0 argument: Theorem 2.5 upper count and Theorem 2.4 (R >= Rhat) (L11:119-125). The card states the hypotheses.")
row("C-50", "2.7 cards hypotheses: L11 cards citing Corollary 2.6 or Theorem 2.5 without hypotheses",
    "course/modules/CS/CS2/cards.json:1073 (CS2-c151), 1633 (CS2-c235), 1558 (CS2-c217)", "FAIL",
    "CS2-c151 (T) and CS2-c235 (T) cite Corollary 2.6 but omit its hypotheses ('those of Theorem 2.2, with n >= 1', L11:131). "
    "CS2-c217 (T) cites Theorem 2.5 with E = 0 without the values-in-order, exact-arithmetic and eps-in-(0,1) hypotheses "
    "(L11:86, 119). The other L11 T cards (c145-c149) carry them, so the set is inconsistent.",
    "Prefix the back of CS2-c151, c235 and c217 with the hypothesis sentence used in CS2-c147, e.g. 'Assume the values are "
    "added in order, eps is fixed in (0, 1), the capacities are as in Definition 2.1, arithmetic is exact and n >= 1.'")
row("C-51", "2.7 cards hypotheses: L10 card citing Theorem 2.2 without hypotheses",
    "course/modules/CS/CS2/cards.json:981 (CS2-c138)", "FAIL",
    "CS2-c138 (T) cites Theorem 2.2 for 'it holds only the candidates' without its hypotheses (w >= 1, real values with no NaN, "
    "exact comparisons; L10:74). Other L10 T cards (c130-c133, c135, c137, c139) carry them.",
    "Prefix the back of CS2-c138 with 'Assume w >= 1, real values with no NaN and exact comparisons.'")
row("C-52", "2.7 cards hypotheses: L09 card citing Corollary 2.3 without hypotheses",
    "course/modules/CS/CS2/cards.json:1551 (CS2-c225)", "FAIL",
    "CS2-c225 (T) states the Welford state and cites Corollary 2.3 without its hypotheses (the stream of Theorem 2.2 and exact "
    "arithmetic; L09:109). Other L09 T cards (c120-c122) carry them.",
    "Prefix the back of CS2-c225 with 'Assume the stream of Theorem 2.2 and exact arithmetic.'")
row("C-53", "2.7 cards: full scan for duplicates",
    "course/modules/CS/CS2/cards.json (224 cards, all lessons)", "PASS",
    "ledgers/CS2/scripts/CS2-c-r1/cards_dup_scan.py: no duplicate ids, no duplicate fronts. 133 pairs with difflib ratio >= 0.55 "
    "across the unit; the pairs inside L09-L11 ask different quantities (c124/c195 naive vs Welford; c198/c199 sketch items vs "
    "compactions; c201/c202 excess vs deficit; c134/c137 indices vs time; c154/c234 windows 5 vs 30).")
row("C-54", "2.7 cards: numbers appear in the lesson",
    "course/modules/CS/CS2/cards.json (L09-L11 cards)", "PASS",
    "Each number on the slice's cards occurs in its lesson: 7.87 (L09:238); 8.852e-11, 7.449e-08, 8.728109e-02 (L09:206-214); "
    "198430 (L11:52); 18187 (L11:389, 276); 0.0212, 0.0442 (L11:259, 257-258); 151 and 305 (L11:257-258, 356); 20/60/120 and "
    "40/120/240 (L11:299, 257); 396-399 and 400 (L10:211, 397); 10 at window 30 (L10:211, 232).")
row("C-55", "2.7 cards: agree with current lesson text and key-results grades",
    "course/modules/CS/CS2/cards.json (all 57 L09-L11 cards)", "PASS",
    "All 57 L09-L11 cards read in full and compared with the lesson text. C-graded cards name Lab 1 and match the expected "
    "blocks; T-graded cards match a numbered result and key-results row. The card-level hypothesis gaps are rows C-50 to C-52.")

# ---- structure summary -------------------------------------------------------
row("C-56", "2.9 prose: why-it-matters, hub links and lesson navigation",
    "course/modules/CS/CS2/L09.html:52,451-452; L10.html:52,450-452; L11.html:52,501-503", "PASS",
    "Each why-it-matters is under 120 words (check_pages). Lesson navigation: L09 Previous L08 and Next L10; L10 Previous L09 and "
    "Next L11; L11 has only a Previous link to L10 (last lesson). Quiz input names (for example L09q1, L09q4) are unique "
    "within each page; the quiz counts are 9, 10 and 10.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}

fragment = {
    "unit": "CS2",
    "slice": "c",
    "round": 1,
    "verifier": "independent verifier (Haiku 5.5), CS2 slice c round 1",
    "pin": PIN,
    "base": "n/a (round 1). A prior ledgers/CS2/CS2-c.json at pin 7aa909e95b757b1abf7b75186d5fa1ed7d1945a4 (round 7) was replaced and not relied on.",
    "checkout": str(ROOT),
    "scratch": "/tmp/cs2c-r1",
    "verified_at": "2026-11-09T03:20:00Z",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Scope: lessons L09, L10, L11 with lab twins tests/labs/CS2/lab-CS2-L09-1.py, L10-1.py, L11-1.py and cards CS2-c116..c153, "
        "c167, c198-c202, c205, c207, c217, c225, c226, c235 (57 cards). All three lessons and twins read line by line; all 57 cards read. "
        "Every number, proof and worked example recomputed with scripts in " + S + " (l09_numbers.py, l09_worked_examples.py, "
        "l11_numbers.py, worked_examples.py, cards_dup_scan.py); run outputs kept as twin_L09/L10/L11.out and page_smoke_L09-L11.txt. "
        "No mutants: the slice has no project grader, and lab twins are demonstrations (verifier-rules ruling). "
        "Tracked files already present in " + S + " from commit 18171917 (card_scan.py, deque_invariant_check.py, expected_vs_run.py, "
        "recompute_L09_L11.py, recompute_L10_L11.py, sketch_random_check.py, weighted_welford_check.py) were not read or relied on. "
        "Not checked: project.html, grader and rubric (other slices); index.html hub (other slice); curriculum/CURRICULUM.md "
        "credential maps; live verify_refs (network); Pyodide beyond page_smoke (the labs ran in Chromium through page_smoke)."
    ),
    "summary": (
        f"CS2 slice c round 1: {len(rows)} rows (pass={counts['PASS']} fail={counts['FAIL']} unverifiable={counts['UNVERIFIABLE']}); "
        "no mathematical, numerical or lab-output error found. Six FAIL rows: a lab docstring that says the lab compares with 2N "
        "(C-13), two lemma claims without claim markup (C-34, C-35), and three card groups missing proposition hypotheses (C-50 to C-52)."
    ),
}

out = ROOT / "ledgers/CS2/CS2-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(rows), counts, verdict)
