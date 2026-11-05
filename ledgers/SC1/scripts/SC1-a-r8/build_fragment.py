# Round 8 verifier (SC1-a) fragment builder. Written by the round-8 verifier from its own full re-read of the slice at
# 0dee921a (previous pin 06994db1, the round-7 pin). Usage: python3 -I build_fragment.py <repo_root> <prev_fragment_json> <out_json>
# Rows whose subject changed, whose subject is a whole file set, or whose previous status the round-8 re-read contradicts are
# re-verified (FRESH). Every other previous PASS row is carried only when its cited lines are byte-identical since 06994db1
# (checked mechanically below against `git diff -U0 06994db1 0dee921a` for the slice files).
import json
import re
import subprocess
import sys

root, prev_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
prev = json.load(open(prev_path, encoding="utf-8"))
PIN = "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3"
BASE = "06994db16d1ab449bcf29898a7f56cfa999dce57"
SLICE_FILES = [
    "course/modules/SC/SC1/index.html",
    "course/modules/SC/SC1/L01.html",
    "course/modules/SC/SC1/L02.html",
    "course/modules/SC/SC1/L03.html",
    "tests/labs/SC1/lab-SC1-L01-1.py",
    "tests/labs/SC1/lab-SC1-L02-1.py",
    "tests/labs/SC1/lab-SC1-L03-1.py",
]
diff = subprocess.run(["git", "-C", root, "diff", "-U0", BASE, PIN, "--"] + SLICE_FILES, capture_output=True, text=True).stdout
changed = {}
cur = None
for line in diff.splitlines():
    if line.startswith("+++ b/"):
        cur = line[6:]
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
    if m and cur:
        start, count = int(m.group(1)), int(m.group(2) or 1)
        for n in range(start, start + max(count, 1)):
            changed.setdefault(cur, set()).add(n)
CHANGED_SUMMARY = {k: sorted(v) for k, v in changed.items()}

CARRY = ("Carried from round 7 (cited lines byte-identical since the previous pin 06994db1; "
         "git diff -U0 06994db1 0dee921a does not touch them): ")

FRESH = {
    "SC1a-gate-check-pages": ("PASS", "index.html, L01.html, L02.html, L03.html, cards.json", "Round 8 at 0dee921a: tools/check_pages.py --unit SC1 -> 'check_pages SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r8/check_pages.out)."),
    "SC1a-gate-check-dag": ("PASS", "index.html, L01.html, L02.html, L03.html", "Round 8 at 0dee921a: tools/check_dag.py --unit SC1 -> 'check_dag SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r8/check_dag.out)."),
    "SC1a-gate-run-labs": ("PASS", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "Round 8 at 0dee921a: tools/run_labs.py --unit SC1 -> 'run_labs SC1: PASS (11/11)', exit 0; per-page runs with --page L01, L02, L03 each 'PASS (1/1)' (ledgers/SC1/scripts/SC1-a-r8/run_labs_unit.txt, run_labs_L01.txt, run_labs_L02.txt, run_labs_L03.txt)."),
    "SC1a-gate-page-smoke": ("PASS", "index.html, L01.html, L02.html, L03.html", "Round 8 at 0dee921a: tools/page_smoke.py --unit SC1 --pages index.html L01.html L02.html L03.html --skip-sweep -> 'page_smoke SC1: PASS', exit 0 (ledgers/SC1/scripts/SC1-a-r8/page_smoke.out). The pages carry no data-chart or svg, so the sweep has no figure to sweep; this was not run."),
    "SC1a-gate-lint-types-tests": ("PASS", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py; pytest -k SC1", "Round 8 at 0dee921a: ruff check and ruff format --check on the three twins: 'All checks passed!' and '3 files already formatted' (ruff.out); mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (mypy.out); python -m pytest -q -k SC1: 11 tests passed, exit 0 (pytest_sc1.out)."),
    "SC1a-gate-verify-refs": ("PASS", "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic)", "Round 8 at 0dee921a: tools/verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (verify_refs.out). The live run was not made (references unchanged in the delta). The key is present in references/references.json (entries[] with key shreve2004stochastic, used_by SC1), and links_anchors_check.py reports 0 unknown keys (links_anchors_check.out)."),
    "SC1a-lab-L01-twin": ("PASS", "tests/labs/SC1/lab-SC1-L01-1.py; L01.html:137-206", "Round 8 at 0dee921a: twin run as python -I -W error from an empty scratch directory: exit 0, stderr 0 bytes. extract_check.py (ledgers/SC1/scripts/SC1-a-r8/extract_check.py) finds the page code equal to the twin and the expected block equal to the twin's stdout, exactly, not only within tolerance (page_twin_exact.out)."),
    "SC1a-lab-L02-twin": ("PASS", "tests/labs/SC1/lab-SC1-L02-1.py; L02.html:168-279", "Round 8 at 0dee921a: twin run as python -I -W error from an empty scratch directory: exit 0, stderr 0 bytes; page code equal to the twin; expected block equal to stdout exactly (page_twin_exact.out). CPython 3.14.8 (the venv)."),
    "SC1a-lab-L03-twin": ("PASS", "tests/labs/SC1/lab-SC1-L03-1.py; L03.html:131-252", "Round 8 at 0dee921a: twin run as python -I -W error from an empty scratch directory: exit 0, stderr 0 bytes; page code equal to the twin; expected block (35 lines) equal to stdout exactly (page_twin_exact.out)."),
    "SC1a-lab-claims-L01": ("PASS", "tests/labs/SC1/lab-SC1-L01-1.py:1-9 (docstring, shown at L01.html:137-145); L01.html:136 and :208", "Round 8 at 0dee921a: the twin's printed lines are 'dyadic variance sums equal t: 15 of 15 cases (depths 0 to 4)', 'covariance equals min(s, t) on the grid: 81 of 81 pairs' and 'Cov(B at 1/4, B at 5/8) = 1/4; min of the two times = 1/4'; the hypothesis and interpretation at L01.html:136 and :208 state the same counts and values, and the twin's docstring matches the code. Re-run in page_twin_exact.out."),
    "SC1a-lab-L02-docstring": ("PASS", "tests/labs/SC1/lab-SC1-L02-1.py:1-8 (docstring, shown at L02.html:171-178)", "Round 8 at 0dee921a: the docstring claims (exact dyadic equality from the zero-hat property; grid-sup identity; SIMULATED) match the code lines 190-246 and the printed lines 1-2 of the expected block (page_twin_exact.out). The docstring's claim that identical floating-point sums result was checked by the exact-equality output 216 of 216."),
    "SC1a-numbers-L03-SE-follow": ("PASS", "course/modules/SC/SC1/L03.html:398 (key-results row, grade C)", "Round 8 at 0dee921a, recomputed in ledgers/SC1/scripts/SC1-a-r8/numbers_r8.py from the printed 4-decimal standard errors: the largest gap |printed/(H*sqrt(2/N)/20) - 1| is +13.2078% at H=2, N=1 (printed 0.1601, population 0.141421); next +9.18% (H=2,N=4), +7.60% (H=1,N=2). So 'agree to within 14 percent' and 'the largest, 13.2 percent, is at H=2, N=1' hold (numbers_r8.out)."),
    "SC1a-numbers-L03": ("PASS", "course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434", "Round 8 at 0dee921a, re-read: :253 |z| largest 2.39 at H=1,N=2 and next 1.84 (the printed z values, twin output); H=1,N=1 population sqrt(2)/20 = 0.0707 vs printed 0.0718; H=2,N=128 population 0.0125 = printed. :270 sum 0.166664 (printed line 'H = 2, N = 128: sum = 0.166664'). :275 E|Z|=sqrt(2/pi) and sqrt(2Nt/pi). :350 16*255/1536 = 2.65625 (printed 2.656250). :357 changed at 0dee921a: '1/80 = 0.0125' and 'agrees ... at four decimal places for this seed' hold for the printed N=128 row, 0.0125 = 0.0125 (numbers_r8.out). :368 2t^2/N. :375 sum = t|P|, E = 2t|P|. :434 15/24 = 0.625, printed 0.625000."),
    "SC1a-numbers-L02-36-points": ("PASS", "course/modules/SC/SC1/L02.html:263 (interpretation); :411-414 (E2)", "Round 8 at 0dee921a, re-read: 36 (depth,point) pairs = 2+3+5+9+17; 216 = 18+24+35+54+85 (E2 at :414 and the 216 of 216 expected line). The lab code loops levels range(n, LEVELS+1), so the count is 9-n per point."),
    "SC1a-math-L01-canon-construction": ("PASS", "course/modules/SC/SC1/L01.html:215 (canon item 1)", "Round 8 at 0dee921a: L01.html:215 changed (letter G for the finite time set; the construction is unchanged). Re-derived: on Omega x (0,1) with P (x) Leb, B extended by B_t(omega,u)=B_t(omega) keeps continuous paths; U(omega,u)=u is uniform and independent of sigma(B) because P((A x (0,1)) cap (Omega x C)) = P(A) Leb(C); B~_t = B_t + 1{t=U} has B~_0 = 0 since U in (0,1); for finite G, P(U in G)=0 so B~ and B agree a.s. at each t in G and have the same finite-dimensional laws; B~_U = B_U + 1 with B continuous gives discontinuity at U on every outcome. Each step holds as written."),
    "SC1a-canon-breaks-ungraded": ("PASS", "course/modules/SC/SC1/L02.html:319-327; L01.html:215-217; L03.html:259-261", "Round 8 at 0dee921a: the three canon-break blocks carry no data-grade of their own (grep of L01.html:211-219, L02.html:319-327, L03.html:256-263); the claims at L01.html:215-217 were re-derived in this round (product extension, two-time counterexample, B_1 in {-1,+1})."),
    "SC1a-r7-forward-refs-L01-s4": ("PASS", "course/modules/SC/SC1/L01.html:215 and :217 (canon-breaks section 4)", "Round 8 at 0dee921a: section 4 of L01 names Assumption A2, Assumption 2.1 and Remark 2.6 of Lesson 2 before the reader reaches them. These are results, not concepts: no concept is linked or defined out of order (check_dag.out PASS). The plan (line 184) forbids links to later concepts only; section 4 is canon-breaks and carries no grade of its own. Forward references to results are recorded, not failed."),
    "SC1a-r7-notation-F-clarity-L01": ("PASS", "course/modules/SC/SC1/L01.html:215", "Round 8 at 0dee921a: the finite time set in L01.html:215 is now G ('For every finite set of times G, P(U in G)=0'), so the letter F no longer names a time set beside the sigma-algebra \\(\\mathcal F\\). The round-7 clarity note is resolved."),
    "SC1a-r6-variance-t0-L01": ("FAIL", "course/modules/SC/SC1/L01.html:67 ('Standard' paragraph)", "Round 8 at 0dee921a: L01.html:67 now reads '(D1) fixes the value at time 0' and then 'None of the three says anything directly about the paths.' Under the page's own wording, (D1) is B_0 = 0 as a random variable, which constrains every path at time 0; so the sentence 'None of the three says anything directly about the paths' is contradicted by the sentence before it. The variance statement (Var(B_t)=t for t>=0 from (D1) at t=0 and (D2) with s=0) is correct."),
    "SC1a-math-L02-thm2.5-extension": ("PASS", "course/modules/SC/SC1/L02.html:302-318 (Refinement paragraph at :314)", "Round 8 at 0dee921a: the round-7 FAIL is fixed. L02.html:314 now reads 'For s<t, each unit interval contains at most one such piece, so the pieces of W_t-W_s come from distinct copies.' Re-derived: for s<t the refinement adds only the integers in [s,t], so (s,t] meets each [k,k+1] in at most one piece, and the copies are distinct. The (D2) paragraph (:315) and (D3) paragraph (:316) are unchanged and use the same refinement correctly."),
    "SC1a-grade-L02-remark2.6": ("PASS", "course/modules/SC/SC1/L02.html:302-318", "Round 8 at 0dee921a: grade T for Remark 2.6 is correct under its hypotheses H1 (copies) and H2 (A1(a), A1(b), A1(e), A2, Assumption 2.1), which the statement lists; the proof is complete for (D1), (D2), (D3) and continuity given those hypotheses (L02.html:313-316 re-read)."),
    "SC1a-r4-thm23-counterexample-L03": ("PASS", "course/modules/SC/SC1/L03.html:382 (R3 solution)", "Round 8 at 0dee921a: the round-7 FAIL is fixed. L03.html:382 now reads 'One hypothesis fails. (H1) fails ... (H2) does not apply here, because Assumption 3.2 is stated for independent variables, and these squares are not independent.' E Q = t and Var Q = 2t^2 re-checked (Q = N X_N^2, Var(X_N^2) = 2(t/N)^2 by Lemma 2.2). No contradiction remains."),
    "SC1a-math-L03-misc-claims": ("PASS", "course/modules/SC/SC1/L03.html:259-261, :270, :274-279, :366-382", "Round 8 at 0dee921a: L03.html:382 re-derived (above); :259-261 canon (c * t|P| bound with Var((dB)^2) <= c Delta^2); :270 (exact 0.166664); :274-279 (E|Z| = sqrt(2/pi), absolute-sum growth sqrt(2Nt/pi)); :366-368 (R1, 2t^2/N)."),
    "SC1a-misconceptions-canon": ("PASS", "course/modules/SC/SC1/L01.html:219-237; L02.html:329-345; L03.html:265-281 (the round-7 location 'L02.html:307-330' was a stale range that contains no misconception)", "Round 8 at 0dee921a: each misconception re-derived from the page's own statements: L01 (Cov(B_{1/2},B_1)=1/2 so not independent; 1/100 gives sd 1/10 = ten times h; Definition 1.1 fixes laws and §4 process has the same laws with different paths); L02 (1 + k/2 lower bound on the harmonic partial sums, Step 2 needs summability; Var(U_j) = 2^{-(n+1)} only when c^2 = 2^{-(n+2)}; the pointwise-limit example f_n = t^n); L03 (the s^2 sum 0.166664 at H=2, N=128; E|Z| = sqrt(2/pi) so the absolute sum grows as sqrt(2Nt/pi); Theorem 2.3 mean-square limit is a constant with error at most 2t|P_n|)."),
    "SC1a-exercises-L01-L03": ("PASS", "course/modules/SC/SC1/L01.html:246-427; L02.html:351-520; L03.html:289-385", "Round 8 at 0dee921a: every worked solution in the three problem sets re-read and hand-checked: L01 M1-M3 (Cov 1/3, Var 1/3, Var(3B_1-B_2)=5), P1-P3, E1-E3 (3/64, 16*3/64=3/4, 2/8 + 1/8 counts, 81 = 9*9); L02 M1-M3 (Lambda(1/4)=1; Sigma_1(1/2)=xi_0/2+xi_{1,1}/2; Var(U_1)=1/4 at n=1), P1-P3, E1-E3 (216; the level-1 unrounded value 0.11658934 -> 0.116589 and twice it 0.2331787 -> 0.233179; sqrt(4 log 2)/2 = 0.832555), R1-R3; L03 M1-M3 (E Q = 1, Var = 1; Var(X^2)=32; 1/N), P1-P3, E1-E3 (z 2.39; 2.65625; 0.0125), R1-R3 (R3 corrected at :382)."),
    "SC1a-notation-T-subscript": ("PASS", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "Round 8 at 0dee921a: grep for T as a symbol in math (T_, T^, T(, T=, \\(T\\)) finds no use of T as a horizon or sample size in the four pages; the only math-mode T is grade T and the mention at L03.html:120 that the program reserves T for the number of observations."),
    "SC1a-notation-no-registered-collision": ("PASS", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "Round 8 at 0dee921a: notation/notation.json symbols are T, \\Phi/\\Phi^{-1}, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}. None appears in the four pages (grep: no \\Phi, \\mathbb{Q}, R^\\ast, \\gamma). Local symbols used (Sigma, Lambda, xi, eta, varphi, Omega^\\ast, W, U, V, D_j, S(N), H, N, G) are not registered."),
    "SC1a-notation-macros": ("PASS", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html", "Round 8 at 0dee921a: every backslash command used in the four pages is standard KaTeX or one of the registered macros used here (\\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic); \\Normal(0,\\,t-s) takes the variance as its second argument, matching notation.json ('\\Normal(\\mu, \\sigma^2)'). katex_render_check.js renders 1281 math spans with 0 parse errors under notation.json macros (katex_render.out)."),
    "SC1a-process-words": ("PASS", "index.html, L01.html, L02.html, L03.html; lab twins L01-L03", "Round 8 at 0dee921a: case-insensitive grep on the four pages and the three twins for builder, verifier, fixer, ledger, round, draft, agent, reviewer, audit, REQUESTS and unit report finds none (empty output)."),
    "SC1a-banned-phrases": ("PASS", "index.html, L01.html, L02.html, L03.html; lab twins", "Round 8 at 0dee921a: tools/check_pages.py --unit SC1 PASS (its banned-string list) and a grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly finds nothing; the four pages contain no ellipsis outside math."),
    "SC1a-structure-L01-L03": ("PASS", "course/modules/SC/SC1/L01.html, L02.html, L03.html", "Round 8 at 0dee921a: each lesson has, in order, why-it-matters (<=120 words), numbered core sections with Definition/Lemma/Proposition/Theorem/Remark/Example blocks, inline labs (L01 lab 1 at :134, L02 at :168, L03 at :131), canon-breaks, >=3 misconceptions, problem set with 3 problems in each of mechanics, proof, empirical, research, each with details.solution, key-results table, quiz of 10 items each with an explanation, references, lesson nav. check_pages.out PASS. data-hours=9 on each."),
    "SC1a-r4-twin-timing-and-purity": ("PASS", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "Round 8 at 0dee921a: each twin run as python -I -W error from an empty scratch directory: exit 0, stderr 0 bytes; CPython wall time under one second each (measured); no network and no file read (the twins import only math, random, fractions, itertools, __future__). Pyodide timing: page_smoke.out PASS with labs enabled (per-lab Pyodide seconds are not printed by page_smoke)."),
    "SC1a-hub-ladder-objectives": ("FAIL", "course/modules/SC/SC1/index.html:168 (rung 2 description, inside :163-171)", "Round 8 at 0dee921a: index.html:168 says the completion problem has 'the cap line and the final comparison line removed'. project.html:199 and :202 (lab twin tests/labs/SC1/lab-SC1-project-2.py) blank the identity line ('identity = ___') and the comparison line ('reflection identity holds: ... == ___'); no cap line exists in rung 2. The objectives (:45-56) and the rung 1, 3, 4 descriptions (:167, :169, :170) match the project page."),
    "SC1a-r8-curriculum-facts": ("PASS", "course/modules/SC/SC1/index.html:33, :35, :60, :184 (hub facts)", "Round 8 at 0dee921a: curriculum YAML read via ledgers/SC1/scripts/SC1-a-r8/hub_prereq_check.py -> hub_prereq_check.out: SC1 'Stochastic Processes', tier M (curriculum/03-markets.yaml:505-508), hours 100, prereqs [M6]; M6 'Measure-Theoretic Probability', prereqs [M4, M5]; M4 and M5 prereq [M2]; M2 prereq [M1]; M1 prereq [P0.1]; P0.1 prereqs []. The hub's chain M6 -> M4, M5 -> M2 -> M1 -> P0.1 and the closure {M1, M2, M4, M5, M6, P0.1} hold. curriculum/03-markets.yaml lists two sources (:523-524), so the hub's 'two sources' sentence holds."),
    "SC1a-r8-links-anchors": ("PASS", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html (107 local links)", "Round 8 at 0dee921a: links_anchors_check.py -> 'links checked: 107 problems: 0' (links_anchors_check.out): every local href and src resolves, every #fragment exists in its target page (including concepts.html anchors), no external hosts, every data-cite key is in references.json."),
    "SC1a-r8-A3-in-L05": ("PASS", "course/modules/SC/SC1/L05.html:270, :278; index.html:33, :53, :156", "Round 8 at 0dee921a: L05.html:270 states 'Assumption A3 (strong Markov property; not proved here)' and :278 says 'Assumption A3 is stated for bounded stopping times'. The hub's 'stated in Lesson 5' (index.html:33) and 'the strong Markov property with its assumption' (:53) hold."),
    "SC1a-r8-project-rung-hours-and-check": ("PASS", "course/modules/SC/SC1/index.html:143, :165, :168; project.html:206, :274-275", "Round 8 at 0dee921a: project.html:206 prints 'n = 6, a = 2: walks with maximum >= a: 29' (the hub's 'its check prints 29', index.html:143, is correct; by the reflection count, the walks with maximum >= 2 are those ending at >= 2 (22 = C(6,4)+C(6,5)+C(6,6)) plus those ending at >= 3 (7 = C(6,5)+C(6,6)), giving 29). project.html:274-275 give rung 1 = 2 h and rung 2 = 3 h, so 'the hours of each rung are on the project page' (index.html:165) holds."),
    "SC1a-r8-hub-numbers": ("PASS", "course/modules/SC/SC1/index.html:29, :39-42, :74, :143, :150", "Round 8 at 0dee921a: 72 + 28 = 100; 28/100 = 28%; 7/9 = 77.8% and 8/9 = 88.9%, so eight of nine is the first count at or above 80 percent; nine items, two marked data-skill (index.html:131, :140); eight lessons of data-hours=9 (grep of L01-L08 data-hours) = 72."),
    "SC1a-r8-lab-mutants": ("PASS", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "Round 8 at 0dee921a: four single-line mutants of the three twins (ledgers/SC1/scripts/SC1-a-r8/lab_mutants/) each change the printed output away from the page's expected block (see mutants list). Lab mutants are not graded (architect ruling); the expected blocks are shown to be sensitive to the claimed quantities."),
    "SC1a-r8-L02-unrounded-E3": ("PASS", "course/modules/SC/SC1/L02.html:421 (E3), :170", "Round 8 at 0dee921a: the seeded level-1 supremum is 0.11658934473943267 (printed 0.116589); twice it is 0.23317868947886533, which rounds to 0.233179; sqrt(4 log 2) = 1.6651092223153954 and half of it 0.8325546111576977 (printed 0.832555). The text at :421 is correct (numbers_r8.out)."),
}

FIXES = {
    "SC1a-hub-ladder-objectives": "Replace index.html:168 'with the cap line and the final comparison line removed' by 'with the identity line and the final comparison line removed'.",
    "SC1a-r6-variance-t0-L01": "Replace the sentence at L01.html:67 'Conditions (D2) and (D3) are statements about laws, and (D1) fixes the value at time 0. None of the three says anything directly about the paths.' by: '(D2) and (D3) are statements about laws. (D1) is pathwise only at time 0: it says that every path starts at 0. None of the three constrains a path between its times.'",
}

rows = []
carried_hits = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in FRESH:
        status, loc, ev = FRESH[rid]
        row = {"id": rid, "check": r["check"], "location": loc or r["location"], "status": status, "evidence": ev}
        if status != "PASS":
            row["fix"] = FIXES[rid]
        rows.append(row)
        continue
    # carried: check the mechanical byte-identity of the cited lines
    loc = r["location"]
    hit = []
    for fname, lines in CHANGED_SUMMARY.items():
        short = fname.split("/")[-1]
        if short in loc or fname in loc:
            for m in re.finditer(r"(\d+)(?:\s*-\s*(\d+))?", loc):
                a = int(m.group(1)); b = int(m.group(2) or a)
                if any(a <= n <= b for n in lines):
                    hit.append((fname, a, b))
    if hit:
        carried_hits.append((rid, hit))
        rows.append({"id": rid, "check": r["check"], "location": loc, "status": "FAIL", "evidence": "Carry blocked by mechanical check: " + str(hit),
                     "fix": "Re-verify this row from the changed lines."})
        continue
    ev = r["evidence"]
    if ev.startswith("Carried from round"):
        ev = ev.split("): ", 1)[1] if "): " in ev else ev
    rows.append({"id": rid, "check": r["check"], "location": loc, "status": "PASS",
                 "evidence": CARRY + ev})

# new rows added in round 8 (checked this round, not in the round-7 fragment)
NEW_CHECK = {
    "SC1a-r8-curriculum-facts": "2.9-structure",
    "SC1a-r8-links-anchors": "2.9-structure",
    "SC1a-r8-A3-in-L05": "2.4-math",
    "SC1a-r8-project-rung-hours-and-check": "2.9-structure",
    "SC1a-r8-hub-numbers": "2.2-numbers",
    "SC1a-r8-lab-mutants": "2.5-labs",
    "SC1a-r8-L02-unrounded-E3": "2.2-numbers",
}
known = {r["id"] for r in rows}
for rid, ch in NEW_CHECK.items():
    if rid in known:
        continue
    status, loc, ev = FRESH[rid]
    rows.append({"id": rid, "check": ch, "location": loc, "status": status, "evidence": ev})

out = {
    "unit": "SC1",
    "slice": "a",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier SC1-a round 8 (did not build SC1; full re-read of index.html, L01-L03 and the three twins at 0dee921a; delta from 06994db1 read hunk by hunk)",
    "pin": PIN,
    "base": BASE,
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-SC1-a",
    "scratch": "ledgers/SC1/scripts/SC1-a-r8/",
    "verified_at": "2026-11-05T01:57:39Z",
    "verdict": None,
    "rows": rows,
    "mutants": [
        {"id": "SC1a-r8-lab-mut1-L01-max-not-min", "description": "lab-SC1-L01-1: covariance_from_increments sums the first max(i, j) increments instead of min(i, j); the printed covariance line becomes 'Cov(B at 1/4, B at 5/8) = 5/8' and the grid count becomes 9 of 81.", "killed_by": "run of the mutated twin: printed lines differ from the L01.html expected block (ledgers/SC1/scripts/SC1-a-r8/lab_mutants/r8-lab-mut1-L01-max-not-min.py.out)"},
        {"id": "SC1a-r8-lab-mut2-L02-scale-half-m", "description": "lab-SC1-L02-1: level_term_sup uses 2**(-m/2) instead of 2**(-(m+1)/2); the grid-supremum line prints False instead of True and every observed sup changes.", "killed_by": "run of the mutated twin: 'grid supremum of each level term equals the formula ... : False' against the expected True (lab_mutants/r8-lab-mut2-L02-scale-half-m.py.out)"},
        {"id": "SC1a-r8-lab-mut3-L03-divisor-n", "description": "lab-SC1-L03-1: standard error divides by n instead of n - 1 (sqrt(variance*(n-1)/n/n)); z values change, e.g. z = 2.40 at H=1, N=2 against the printed 2.39.", "killed_by": "run of the mutated twin: 10 printed lines differ from the L03.html expected block (lab_mutants/r8-lab-mut3-L03-divisor-n.py.out)"},
        {"id": "SC1a-r8-lab-mut4-L03-closed-form-plus", "description": "lab-SC1-L03-1: closed form uses (4N^2 + 1) instead of (4N^2 - 1); 'closed form matches: False' at all 16 levels.", "killed_by": "run of the mutated twin: 16 printed lines differ from the L03.html expected block (lab_mutants/r8-lab-mut4-L03-closed-form-plus.py.out)"},
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
out_txt = json.dumps(out, ensure_ascii=False, indent=1)
open(out_path, "w", encoding="utf-8").write(out_txt + "\n")
print("changed lines (slice):", {k: v for k, v in CHANGED_SUMMARY.items()})
print("carry-blocked rows:", carried_hits)
print("rows:", len(rows), "by status:", {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")})
