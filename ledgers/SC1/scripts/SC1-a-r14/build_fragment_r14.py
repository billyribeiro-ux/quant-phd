"""Round-14 SC1-a: build ledgers/SC1/SC1-a.json from the round-13 row ids (every id kept) plus the round-14 rows.
Every evidence string names the command, script output or file:line read this round."""
import json
import sys
from datetime import UTC, datetime

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a"
OUT = "ledgers/SC1/scripts/SC1-a-r14/out"
PREV = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-a.round13.json", encoding="utf-8"))
prev_ids = [r["id"] for r in PREV["rows"]]

GATE = "ledgers/SC1/scripts/SC1-a-r14/gates_r14.sh"
R = {}  # id -> (check, location, status, evidence, fix)

def P(i, check, location, evidence):
    R[i] = (check, location, "PASS", evidence, "")

def F(i, check, location, evidence, fix):
    R[i] = (check, location, "FAIL", evidence, fix)

# ---- gates (run this round on the pin, outputs in out/) ----
P("SC1a-gate-check-pages", "2.9-structure-tool", "index.html, L01.html, L02.html, L03.html, cards.json",
  f"`tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS', rc=0 ({OUT}/check_pages_SC1.out; run by {GATE}).")
P("SC1a-gate-check-dag", "2.9-dag-tool", "index.html, L01.html, L02.html, L03.html",
  f"`tools/check_dag.py --all` -> 'check_dag SC1: PASS' among 28 units, rc=0 ({OUT}/check_dag_all.out).")
P("SC1a-gate-run-labs", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
  f"`tools/run_labs.py --unit SC1` -> 'run_labs SC1: PASS (11/11)', rc=0 ({OUT}/run_labs_SC1.out).")
P("SC1a-gate-page-smoke", "2.9-page-smoke", "index.html, L01.html, L02.html, L03.html",
  f"`tools/page_smoke.py --unit SC1 --pages <page>` run separately for index, L01, L02, L03: each 'PASS', rc=0 ({OUT}/page_smoke_*.out). Shared machine: other verifier pytest processes were running; timings are informational.")
P("SC1a-gate-lint-types-tests", "2.5-ruff-mypy-pytest", "tests/labs/SC1/*; pytest -k SC1",
  f"`ruff check .` 'All checks passed!'; `ruff format --check .` '559 files already formatted'; `mypy --no-incremental` 'Success: no issues found in 385 source files'; `pytest -k SC1 tests` 11 passed, collect-only 11 ({OUT}/ruff_*.out, mypy_full.out, pytest_SC1*.out).")
P("SC1a-gate-verify-refs", "2.1-citations", "course/modules/SC/SC1/index.html:182 (data-cite shreve2004stochastic)",
  f"`tools/verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems'; `--unit SC1` (live): '1 of 560 entries, 0 problems' ({OUT}/verify_refs_*.out).")

# ---- labs and twins ----
P("SC1a-lab-L01-twin", "2.5-lab-L01", "tests/labs/SC1/lab-SC1-L01-1.py; course/modules/SC/SC1/L01.html:137-208",
  f"Twin run alone as `python -I -W error` from an empty directory: rc=0, empty stderr; page code equals twin after strip; expected block equals stdout ({OUT}/twins_r14.out).")
P("SC1a-lab-L02-twin", "2.5-lab-L02", "tests/labs/SC1/lab-SC1-L02-1.py; course/modules/SC/SC1/L02.html:168-279",
  f"Same procedure: rc=0; page code == twin; expected block (216 of 216 ... 1.309399) == stdout ({OUT}/twins_r14.out).")
P("SC1a-lab-L03-twin", "2.5-lab-L03", "tests/labs/SC1/lab-SC1-L03-1.py; course/modules/SC/SC1/L03.html:131-252",
  f"Same procedure: rc=0; page code == twin; expected block == stdout, 16 closed-form rows True ({OUT}/twins_r14.out).")
P("SC1a-lab-claims-L01", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L01-1.py:1-9; L01.html:136, :139-144, :208",
  "Docstring (twin lines 1-9) and page hypothesis/interpretation (L01.html:136, :208) checked line by line against the output: 15 of 15, the 1/4 vs 5/8 pair, 81 of 81; 'simulates no path' true (no random call in twin).")
P("SC1a-lab-claims-L03", "2.5-lab-claims", "course/modules/SC/SC1/L03.html:133, :253, :343; twin",
  f"L03.html:133 (400 paths, H=1,2, k=0..7, se = H*sqrt(2/N)/20, z within +-3, closed form) matches the twin code and output; :253 |z| max 2.39 at H=1,N=2 and next 1.84 recomputed from printed mean/se ({OUT}/numbers_r14.out); :343 consistent.")
P("SC1a-lab-L02-docstring", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L02-1.py:1-8; L02.html:171-178",
  f"Docstring says the dyadic count and the grid-sup line hold for every seed and the bound lines describe one sample; checked by a 300-seed sweep ({OUT}/seed_sweep_r14.out: 0 failures) and by the output (L02.html:266-277).")
P("SC1a-lab-L02-hypothesis-expected", "2.5-lab-claims", "course/modules/SC/SC1/L02.html:170 (hypothesis), :266-278 (expected block, interpretation)",
  "Hypothesis text (216 of 216, grid-sup True, bound line probability 2^-m) matches output lines 266-267 and 170; interpretation counts 36 pairs (2,3,5,9,17) and the 1.309399 / 0.348139 values (recomputed in numbers_r14.out).")
P("SC1a-simulated-labels", "2.5-labels", "course/modules/SC/SC1/L02.html:170, :173; L03.html:132, :136",
  "L02 lab and L03 lab carry SIMULATED (generated draws from random.Random(SEED)); L01 lab is exact Fraction arithmetic and is correctly unlabelled (plan section 2.2 rule).")
P("SC1a-r4-seed-sweep-L02", "2.5-lab-seed", "tests/labs/SC1/lab-SC1-L02-1.py; course/modules/SC/SC1/L02.html:170",
  f"Re-run this round: dyadic 216-of-216 and grid-sup identity hold for all 300 seeds tested ({OUT}/seed_sweep_r14.out).")
P("SC1a-r12-L02-identities-301-seeds", "2.5-lab-seed", "tests/labs/SC1/lab-SC1-L02-1.py (docstring: identities hold for every seed)",
  f"Re-run this round with 300 seeds (0 failures; {OUT}/seed_sweep_r14.out); the lab section and twin are byte-identical to the round-13 pin (delta: {OUT}/delta_and_cards_r14.out).")
P("SC1a-r14-lab-mutants-new3", "2.5-labs", "ledgers/SC1/lab-mutants/SC1a-r14-lab-n1..n3 (3 new student-error mutants)",
  f"Three new student-error mutants of the labs: n1 L01 dyadic piece length 2**(n+1) -> sums 1/2, 3/8, 5/4, '0 of 15' (killed); n2 L02 hat slope doubled -> grid-sup 0.252987 (killed); n3 L03 se omits sqrt(n) -> se column changes (killed). Runner: {GATE.replace('gates_r14.sh','lab_mutants_r14.py')} ({OUT}/lab_mutants_all_r14.out).")
P("SC1a-r10-lab-mutants-4of4", "2.5-labs", "ledgers/SC1/lab-mutants/*.py (6 existing) and ledgers/SC1/mutants/SC1a-r13-lab-m1..m4 (not re-run this round)",
  f"Round-13 four lab mutants exist in ledgers/SC1/mutants/ (not re-run here, outside this slice's mutant directory); the six lab-mutants in ledgers/SC1/lab-mutants/ were re-run and all 9 lab mutants are killed by the expected block ({OUT}/lab_mutants_all_r14.out).")
P("SC1a-r11-lab-mutants-6of6", "2.5-labs", "ledgers/SC1/lab-mutants/*.py",
  f"All lab-mutant files (6 existing + 3 new) re-run against the current twins: 9 of 9 differ from the expected block ({OUT}/lab_mutants_all_r14.out).")
P("SC1a-r10-L02-E3-unrounded", "2.2-numbers", "course/modules/SC/SC1/L02.html:421",
  "E3 recomputed: |xi_{1,1}| = 0.23317868947886533, 2x = 0.2331787 rounds to 0.233179; 2 x 0.116589 = 0.233178 (not the rounded value); sqrt(4 log 2)/2 = 0.8325546 (numbers_r14.out).")
P("SC1a-r10-lab-L01-L02-L03-claims", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L01-1.py:1-9; lab-SC1-L02-1.py:1-8; lab-SC1-L03-1.py:1-14",
  "Each twin docstring read and compared with its printed output: L01 'simulates no path' and the two identities; L02 'identities hold for every seed' (300-seed sweep), 'bound lines describe one sample'; L03 'SIMULATED', standard error with divisor PATHS-1, exact s^2 sums checked against the closed form.")

# ---- numbers ----
P("SC1a-numbers-L01", "2.2-numbers", "course/modules/SC/SC1/L01.html:132, :230, :299, :306, :350-353, :391-394, :396-399, :410-413, :424-427",
  "Re-derived with fractions: 3/64 x 16 = 3/4 (E1); 2^-(n) pieces; Cov(B_{1/4},B_{5/8}) = 2 x 1/8 = 1/4 (E2); Var(3B_1-B_2)=9+2-6=5; sd sqrt(1/4)=1/2; 1/sqrt(1/100)=10; E[B_3^2]=3; Var(B_2)=2; Cov(B_2,B_5)=2. All match the page.")
P("SC1a-numbers-L02", "2.2-numbers", "course/modules/SC/SC1/L02.html:268-277 (printed block), :278, :405-407, :411-414, :419-421",
  f"Printed block lines 266-277 equal the twin output; recomputed level sups, bounds (0.832555, 0.721013 ...), tail sum 1.3093991 -> 1.309399 and grid sup 0.3481387 -> 0.348139 ({OUT}/numbers_r14.out).")
P("SC1a-numbers-L03", "2.2-numbers", "course/modules/SC/SC1/L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434",
  f"All numbers recomputed (numbers_r14.out, seed-free closed forms): 0.166664 at H=2,N=128; 2.65625 = 4080/1536; se 0.0125 = 2 sqrt(1/64)/20; sqrt(2/pi) and sqrt(2Nt/pi); z values from printed mean/se; 0.625 = 15/24.")
P("SC1a-numbers-L02-36-points", "2.2-numbers", "course/modules/SC/SC1/L02.html:278; :411-414",
  "36 dyadic (depth, point) pairs = 2+3+5+9+17 (numbers_r14.out 'points: 36'); 216 = 18+24+35+54+85 (E2 recomputed: 'E2 total: 216').")
P("SC1a-numbers-L03-SE-follow", "2.2-numbers", "course/modules/SC/SC1/L03.html:398 (key-results row, grade C)",
  f"Gap = printed se / (H sqrt(2/N)/20) - 1 for all 16 cells: largest |gap| 13.21% at H=2,N=1 (0.1601/0.1414214 - 1 = 0.1320780), all others below 13.21% (numbers_r14.out). The row's 'within 14 percent' and '13.2 percent' are correct.")
P("SC1a-grade-L01", "2.3-grades", "course/modules/SC/SC1/L01.html:83, :101, :119, :349-353",
  "Prop 1.2, Remark 1.3, Example 1.4 graded T and each proved on the page; key-results rows graded T with proof locators; no lab-only claim graded T.")
P("SC1a-grade-L02", "2.3-grades", "course/modules/SC/SC1/L02.html:74, :103, :121, :145, :288, :302",
  "Lemma 2.2, Lemma 2.1, Lemma 2.3, Prop 2.4, Theorem 2.5, Remark 2.6 all graded T and proved on the page or under named Assumptions; A2 is labelled 'not proved' (L02.html:281-286).")
P("SC1a-grade-L03", "2.3-grades", "course/modules/SC/SC1/L03.html:77, :90, :99, :118, :394-398",
  "Lemmas 2.1, 2.2, Theorem 2.3, Prop 2.4 graded T with proofs; the lab-based row (L03.html:398) graded C with basis 'Lab 1 (SIMULATED), one seed'.")
P("SC1a-hub-grade-definition", "2.3-grades", "course/modules/SC/SC1/index.html:79; BLUEPRINT.md:158",
  "Index Pq1 answer 'A theorem, proved on the page or with a precisely cited proof' equals BLUEPRINT.md:158 wording. (Lesson legends say 'proved on the page', an abbreviation used in every module; not a conflict.)")

# ---- math ----
P("SC1a-math-L01-prop1.2", "2.4-math", "course/modules/SC/SC1/L01.html:84-98",
  "Re-derived: E[XY]=E X E Y by A1(a) for independent integrable X=B_s, Y=B_t-B_s; Cov = E X^2 = s = min(s,t); the s=0 and s=t cases correct; integrability via |XY|<=(X^2+Y^2)/2.")
P("SC1a-math-L01-remark1.3", "2.4-math", "course/modules/SC/SC1/L01.html:75 (A1(b)), :102-113",
  "Remark 1.3 proof re-derived: increments independent by (D3), normal by (D2), linear combinations of one independent family, A1(b) gives joint normality, covariance from Prop 1.2. Stated for 0<t_1<...<t_r (L01.html:107). The key-results summary of the same remark is a separate row (SC1a-r14-L01-keyresult-remark13-scope).")
P("SC1a-math-L01-canon-construction", "2.4-math", "course/modules/SC/SC1/L01.html:215 (canon item 1)",
  "Re-verified after the delta: the hypothesis list now reads 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1(a)-(c)', which matches Remark 2.6's H2 (L02.html:306). The product-space argument re-derived: U uniform and independent of B, B~ has the same fdd (P(U in G)=0), and B~ is discontinuous at U on every outcome.")
P("SC1a-math-L02-lemmas-2.1-2.2", "2.4-math", "course/modules/SC/SC1/L02.html:73-117",
  "Lemma 2.2 (a)-(e) re-derived (hat breakpoints, disjoint supports, dyadic vanishing, linearity); Lemma 2.1 Chernoff bound re-derived with theta = lambda (E e^{theta eta} = e^{theta^2/2}); 2 e^{-lambda_m^2/2} = 2 * 2^{-2m} checked numerically (numbers_r14.out).")
P("SC1a-math-L02-lemma2.3-arithmetic", "2.4-math", "course/modules/SC/SC1/L02.html:121-141 (Lemma 2.3, proof :132-140)",
  "Re-derived: Var(U_j) = 2^{-(n+2)} + 2^{-(n+2)} = 2^{-(n+1)}; Cov(U_j,V_j) = 2^{-(n+2)} - 2^{-(n+2)} = 0; the Consequence (L02.html:139) justifies the variance of the sum with A1(a) and the summands' independence (A1(e)). Round-12 gap closed.")
P("SC1a-math-L02-prop2.4", "2.4-math", "course/modules/SC/SC1/L02.html:145-165",
  "Re-derived: P(E_m^c) <= 2^{m-1} * 2 e^{-lambda_m^2/2} = 2^{-m}; P(A^c_{m0}) <= 2^{1-m0}; M_m = sqrt(2 log 2) sqrt(m) 2^{-m/2} <= sqrt(2 log 2) m r^m; sum m r^m = r/(1-r)^2 finite; Cauchy and uniform convergence; continuity by epsilon/3. H3 names Assumption 2.1(a)-(c), which the proof uses.")
P("SC1a-math-L02-A2-sketch", "2.4-math", "course/modules/SC/SC1/L02.html:281-286",
  "A2 is stated as an assumption and the sketch is labelled 'Sketch, not a proof'; the skipped step (passage of characteristic functions to the limit) is named.")
P("SC1a-math-L02-thm2.5", "2.4-math", "course/modules/SC/SC1/L02.html:288-300",
  "Theorem 2.5 H2 'Assuming A2 and Assumption 2.1(a)-(c)' (changed this delta, matches the proof's use of Prop 2.4(a)); (D1) via P2 (Sigma_M(0)=0), (D2)/(D3) via A2 and P(Omega*)=1, continuity off Omega* (path zero). Re-derived.")
P("SC1a-math-L03-thm2.3", "2.4-math", "course/modules/SC/SC1/L03.html:99-115",
  "Re-derived: E Q = t (telescoping), Var Q = sum 2 Delta_k^2 via A-3.2(a),(b) and Lemma 2.2, E(Q-t)^2 <= 2 t |P|; mean-square only (L03.html:115 disclaims pathwise).")
P("SC1a-math-L03-prop2.4", "2.4-math", "course/modules/SC/SC1/L03.html:117-129",
  "Re-derived: (a) (b^2-a^2)^2 <= 4H^2(b-a)^2 and sum Delta^2 <= |P| H give 4H^3|P|; (b) sum of (2j+1)^2 = N(4N^2-1)/3 by induction (checked N=1..4 numerically); result H^4(4N^2-1)/(3N^3).")
P("SC1a-math-L03-misc-claims", "2.4-math", "course/modules/SC/SC1/L03.html:259-261, :270, :274-279, :366-382",
  "Canon break 2: Var(Q)=2t^2 for the dependent family (direct); misconception 2: E|Z|=sqrt(2/pi) and E sum|dB| = sqrt(2Nt/pi) (re-derived); R1, R2 (c=2 least), R3 re-derived.")
P("SC1a-math-L03-density", "2.4-math", "course/modules/SC/SC1/L03.html:78, :332",
  "Lemma 2.1 (E Z^4 = 3 by integration by parts, boundary term 2R^3 phi(R) -> 0) and P3 (E|Z| = 2 phi(0)) re-derived.")
P("SC1a-grade-L02-remark2.6", "2.4-math", "course/modules/SC/SC1/L02.html:302-318",
  "Remark 2.6 H2 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1(a)-(c)' (changed this delta) matches its proof (uses A1(a) for variances, A1(b) normality, A1(e) grouping, A2 through Theorem 2.5). Gluing and (D1)-(D3) re-derived.")
P("SC1a-math-L02-thm2.5-extension", "2.4-math", "course/modules/SC/SC1/L02.html:314 (refinement paragraph)",
  "Refinement argument re-derived: each unit interval contributes at most one piece to W_t - W_s when refined with {s,t} and the integers; pieces come from distinct copies.")
P("SC1a-exercises-L01-L03", "2.4-problems", "course/modules/SC/SC1/L01.html:246-427; L02.html:351-520; L03.html:289-385",
  "Round-13 FAIL was the R2 solution at L02.html:439. Now fixed: it reads 'The bounds Prob(E_m^c)<=2^{-m} come from Lemma 2.1, which uses Assumption 2.1(a), and the union bound and continuity from below use Assumption 2.1(c)'. All 36 problems re-derived this round (L01 M1-3, P1-3, E1-3, R1-3; L02 M1-3, P1-3, E1-3, R1-3; L03 M1-3, P1-3, E1-3, R1-3): every numeric answer and proof step checks.")
P("SC1a-misconceptions-canon", "2.4-canon", "course/modules/SC/SC1/L01.html:219-237; L02.html:329-345; L03.html:265-281",
  "Each misconception re-derived: L01 independence of B_s,B_t (Cov 1/2), short-increment sd 1/10 at h=1/100, Definition 1.1 does not fix paths; L02 harmonic partial sums >= 1+k/2, variance bookkeeping fixes c, t^n example; L03 f=s^2 bound and 0.166664, absolute variation sqrt(2Nt/pi), random-number misconception.")
P("SC1a-canon-breaks-ungraded", "2.3-grades", "course/modules/SC/SC1/L02.html:319-327; L01.html:215-217; L03.html:259-261",
  "Canon-break statements are not graded T (they are stated as limits of the argument or as counterexamples checked by computation); the L02 non-normal item says the bounds 'do not follow from this page's arguments', which is hedged.")

# ---- notation ----
P("SC1a-notation-macros", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  "Registered macros used: \\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic only (scan of all \\( \\) math). Raw TeX commands (\\mathcal, \\mathrm{Leb}, \\operatorname{Bor}, \\varphi) are not registered macros and do not collide with a registered symbol.")
P("SC1a-notation-no-registered-collision", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  "Scan: no use of T, \\Phi, \\gamma_3, \\gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q} (notation/notation.json symbols). Plain Q (quadratic variation, L03) and plain R (bound in L03 Lemma 2.1 proof) are not the registered \\mathbb{Q} or \\R.")
P("SC1a-notation-T-subscript", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  "T appears in SC1 slice-a math only in L03.html:120 where the page states that T is reserved (notation/notation.json:112 meaning 'number of return observations'). No T used as a horizon.")
P("SC1a-notation-H-horizon", "2.4-notation", "course/modules/SC/SC1/L03.html:120, :122, :128, :133; tests/labs/SC1/lab-SC1-L03-1.py:160",
  "H is the horizon throughout L03 and in the twin (HORIZONS = (1.0, 2.0)); H is not a registered symbol.")
P("SC1a-r4-notation-S-symbol-L02", "2.4-notation", "course/modules/SC/SC1/L02.html (no plain S in math); L03.html:128 (local S(N))",
  "Scan of L01/L02 math segments: no plain S. L03 uses S(N) for the sum of odd squares, defined in place at L03.html:128; S is not a registered symbol (notation.json: S is local).")
P("SC1a-r4-thm23-counterexample-L03", "2.4-math", "course/modules/SC/SC1/L03.html:382 (R3 solution)",
  "R3 solution: Var(Q)=2t^2 for every N and the family is not standard BM; hypothesis (H1) named as failing (D3). Re-derived.")
P("SC1a-process-words", "2.9-prose", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html; lab twins L01-L03",
  "Scan (python regex, this round) for builder, build, round, verifier, REQUEST, architect, planner, fixer, ledger, unit report, Round, Verif, Build: hits are only 'verified' in the curriculum project title (index.html:36), the learner verb 'verify' (index.html:52) and 'unrounded'/'rounded' in maths prose. No process words.")
P("SC1a-banned-phrases", "2.9-prose", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  "Scan for TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', ellipsis outside code: no hits.")
P("SC1a-structure-L01-L03", "2.9-structure", "course/modules/SC/SC1/L01.html, L02.html, L03.html",
  "Section order in each lesson: why-it-matters (<=120 words), core, lab, canon-breaks, misconceptions (3 each), problem set (3 per tier x 4 tiers, each with details.solution), key-results table, quiz (10 items each, with explanations), references, next/prev nav. check_pages PASS.")
P("SC1a-scope-words-L02-L03", "2.4-scope", "course/modules/SC/SC1/L02.html:139, :158, :316, :389; L03.html:85, :104, :133, :253, :270",
  "'every', 'all', 'any', 'almost surely', 'converges' used with computations: L02:139 (Consequence, finite sums), :158 (union bound over m>=m0), :316 (refinement), :389 (E2); L03:85, :104, :133, :253, :270 (lab-based statements limited to the sample; 'for every' statements computed).")
P("SC1a-scope-L01-prop1.2-only", "2.4-scope", "course/modules/SC/SC1/L01.html:216-217",
  "Canon items 2 and 3 state scope precisely: whole-path property not fixed by fdd, non-normal increments break Remark 1.3 only (Prop 1.2 still holds, re-derived).")
P("SC1a-ref-L01-every-result", "2.1-citations", "course/modules/SC/SC1/L01.html:434",
  "Reference paragraph: no registry source; the only result from another lesson is Remark 2.6 of Lesson 2 (used in L01:215, named with its assumptions). Checked against L01.html:215 and L02.html:302-318.")
P("SC1a-r4-cauchy-schwarz-L01", "2.4-assumptions", "course/modules/SC/SC1/L01.html:95; index.html:69 (promise)",
  "L01:95 bounds |XY| by (X^2+Y^2)/2 (elementary, not Cauchy-Schwarz); integrability derived from E X^2 = s and E Y^2 = t-s. index.html:69 promise (numbered Assumption or labelled) is met by A1 (L01.html:72-80, labelled as citing no source).")
P("SC1a-hub-assumption-promise", "2.4-assumptions", "course/modules/SC/SC1/index.html:69 (promise), :184; L01.html:72-80 (A1); L02.html:92-99 (Assumption 2.1); L03.html:71 (Assumption 3.2)",
  "Round-12 FAIL is closed: L03.html:71 names M4 as the source of Assumption 3.2 and says it is assumed; index.html:184 names A1 (L1), A2 and Assumption 2.1(a)-(c) (L2), Assumptions 3.1 and 3.2 (L3) and matches the lesson headings. Re-verified after the delta.")
P("SC1a-attrib-L01-A1-parts", "2.4-assumptions", "course/modules/SC/SC1/L01.html:37, :72-80",
  "A1 has five parts (a)-(e), each stated without proof, with the note 'cites no source for them' (L01.html:80); L01.html:37 names the prerequisites (M4, M6) that the facts come from.")
P("SC1a-assump-L01-P3", "2.4-assumptions", "course/modules/SC/SC1/L01.html:285-288",
  "Problem P3 invokes Proposition 1.2 for the pair (t,s) and names symmetry; no undeclared assumption (A1(a) is named in the statement).")
P("SC1a-assump-L02-grouping", "2.4-assumptions", "course/modules/SC/SC1/L02.html:106, :116, :138",
  "Lemma 2.1 uses 2.1(a) (named), Lemma 2.3 uses A1(e) grouping (named at L02.html:124 and :138); no unnamed assumption.")
P("SC1a-attrib-L02-lemma2.1-union", "2.4-attribution", "course/modules/SC/SC1/L02.html:97 (Assumption 2.1(c)), :158",
  "Assumption 2.1(c) states countable subadditivity and continuity from below (L02.html:97); the union bound and the limit at :158 use exactly those parts.")
P("SC1a-attrib-L02-eponym", "2.1-citations", "course/modules/SC/SC1/L02.html:7; tests/labs/SC1/lab-SC1-L02-1.py:1-8",
  "grep (this round) for Levy/Ciesielski/Schauder in L01-L03 pages and twins: no eponymous attribution appears; the construction is described by its hats and not attributed to a named source.")
P("SC1a-reference-section-L02-L03", "2.1-citations", "course/modules/SC/SC1/L02.html:547; L03.html:491; L01.html:434",
  "Reference sections: L02 cites no registry source and states A2 is 'not attributed to a source'; L03 says the curriculum lists Shreve and that no passage locator is confirmed (book-level only).")

# ---- hub ----
P("SC1a-hub-hours", "2.9-hours", "course/modules/SC/SC1/index.html:29, :39-42, :150; project.html:33, :272-281",
  "data-hours-lessons=72 (8 x data-hours 9 on L01-L08, read this round), data-hours-project=28 (project.html:33), time-budget table recomputed 2+3+10+8+3+2 = 28 (project.html:272-281).")
P("SC1a-hub-placement", "2.9-structure", "course/modules/SC/SC1/index.html:72-145",
  "Nine placement items: seven prerequisite items (P0.1, M1, M2, M4, M5, M6) and two skill checks (data-skill). 7/9 = 77.8%, 8/9 = 88.9% (index.html:74); mastery bar 80% needs 8 of 9.")
P("SC1a-r4-hub-quiz-keys", "2.9-structure", "course/modules/SC/SC1/index.html:72-145",
  "Answer keys re-derived: Pq1 option 1 (theorem grade); Pq2 proof by contradiction; numeric 1 (integral of 2x on [0,1]) and 2 (E[X] for values 1, 3 with probability 1/2); Pq4 E[XY]=E[X]E[Y]; Pq5 completeness; Pq6 X_n; Pq8 2P(B_t>=a); rung 2 numeric 2 (two paths reach 1 of four).")
P("SC1a-hub-prereq-chain", "2.9-structure", "course/modules/SC/SC1/index.html:35, :58-68; curriculum/01-foundations.yaml",
  "Chain recomputed from curriculum/curriculum.json: SC1 prereqs [M6]; M6 [M4, M5]; M4 [M2]; M5 [M2]; M2 [M1]; M1 [P0.1]; P0.1 []. Closure M1, M2, M4, M5, M6, P0.1 as stated.")
P("SC1a-hub-concept-list", "2.9-structure", "course/modules/SC/SC1/index.html:62-67",
  "Each listed concept is linked with data-concept and a concept-index href; check_dag --all PASS (SC1 entry).")
P("SC1a-hub-cards-L01-L03", "2.7-cards-copy", "course/modules/SC/SC1/index.html:152-154",
  "Card copy for L01-L03 agrees with the current lesson text (min(s,t) covariance; the A2 identification; quadratic variation, mean-square limit, s^2 sums) and with the card set re-read this round.")
P("SC1a-hub-ladder-objectives", "2.9-structure", "course/modules/SC/SC1/index.html:163-171; :168",
  "Ladder rung texts (index.html:167-170) describe the project rungs; project.html:207 prints 29 for n=6, a=2, which equals 22+7 recomputed (walks ending >= 2 plus walks ending > 2).")
P("SC1a-hub-data-status", "2.8-data", "course/modules/SC/SC1/index.html:37, :174-177; L01.html-L03.html",
  "No real data; labs use closed forms, exact walks, generated paths; generated paths labelled SIMULATED (L02, L03). tools/fetch_data.py --check: 3 datasets, 0 problems.")
P("SC1a-dag-hub-prose", "2.9-dag", "course/modules/SC/SC1/index.html:33, :53, :150",
  "Hub prose names only closure concepts and SC1's own concepts; check_dag --all PASS. (Line 33 contains the path-level statement that is FAILED separately in SC1a-r10-hub-lede-path-level.)")
P("SC1a-prose-L01-three-conditions", "2.9-prose", "course/modules/SC/SC1/index.html:49; L01.html:51, :61-63",
  "Three conditions (start at zero, normal increments of variance = length, independent increments over disjoint intervals) match Definition 1.1 (L01.html:61-63).")
P("SC1a-define-dyadic", "2.9-define-before-use", "course/modules/SC/SC1/L01.html:132 (dfn); L02.html:71 (link); L03.html:55 (link)",
  "Dyadic partition defined in L01 (L01.html:132) before its links in L02:71 and L03:55.")
P("SC1a-scope-L03-converge", "2.4-scope", "course/modules/SC/SC1/L03.html:270 (misconception 1)",
  "Misconception 1 says sums vanish for s^2 and that Brownian sums have mean elapsed time with mean-square error to zero, and makes no pathwise claim (L03.html:115, :278).")
P("SC1a-hub-quiz-cross", "2.9-hub-quiz", "course/modules/SC/SC1/index.html:143",
  "Rung-2 skill check answer 2 (paths ++ and +-) and its explanation 'its check prints 29' matches project.html:207 (n=6, a=2 prints 29).")
P("SC1a-prose-two-sources", "2.1-citations", "course/modules/SC/SC1/index.html:184; references/references.json",
  "index.html:184 says the curriculum's second source has no admitted record: grep -i karatzas references/references.json -> 0 hits; shreve2004stochastic present at references.json:20734. Statement correct.")
P("SC1a-r5-gaussian-process-scope-L01", "2.4-scope", "course/modules/SC/SC1/L01.html:107, :115",
  "Gaussian process definition uses vectors with 0<t_1<...; Remark 1.3 gives the BM statement for 0<t_1<...; consistent.")
P("SC1a-r6-variance-t0-L01", "2.4-math", "course/modules/SC/SC1/L01.html:67",
  "Var(B_t)=t for all t>=0: t=0 from (D1), t>0 from (D2) with s=0 (re-derived).")
P("SC1a-r6-quiz-mesh-hypothesis-L03", "2.4-quiz", "course/modules/SC/SC1/L03.html:437-443",
  "Quiz item: the mesh condition is Assumption 3.1, added in the conclusion of Theorem 2.3 ('Assuming also Assumption 3.1'); Assumption 3.2 is (H2). Correct.")
P("SC1a-r7-notation-F-clarity-L01", "2.4-notation", "course/modules/SC/SC1/L01.html:55, :215",
  "\\mathcal F in L01 is the sigma-algebra of the probability space (L01.html:215, with (Omega, F, P); probability space is an M6 concept, L01.html:37); no filtration macro is registered and no filtration symbol appears in L01-L03.")
P("SC1a-r7-gate-check-projects", "2.9-projects-tool", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  f"`tools/check_projects.py --unit SC1` -> 'check_projects SC1: PASS' rc=0 ({OUT}/check_projects_SC1.out).")
P("SC1a-r7-katex-render", "2.9-math-rendered", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  f"page_smoke (alone, per page) PASS with zero console errors reported by the tool; KaTeX asset links present (index.html:9, :12-13; L01 same). Math render confirmed by page_smoke, not by a screenshot.")
P("SC1a-r7-forward-refs-L01-s4", "2.9-define-before-use", "course/modules/SC/SC1/L01.html:215, :217 (section 4)",
  "Section 4 uses Lesson 2 items (Remark 2.6, A2, Assumption 2.1) that appear later; they are named as Lesson 2 items with their numbers and are not linked concepts.")
P("SC1a-r8-curriculum-facts", "2.9-structure", "course/modules/SC/SC1/index.html:33, :35, :60, :184",
  "Curriculum facts match curriculum/03-markets.yaml:505-532 (title, tier M, 100 h, prereq M6, 8 introduced concepts, sources) and the index's statements.")
P("SC1a-r8-links-anchors", "2.9-structure", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  "Internal anchors checked: L01.html#def-brownian-motion (target L01:59, used at L02:37 and L03:37); L01.html#def-dyadic-partition (target L01:132, used at L02:71 and L03:55); index links to L01-L08 and project.html exist; page_smoke reports no failures.")
P("SC1a-r8-A3-in-L05", "2.4-math", "course/modules/SC/SC1/L05.html:59 (Assumption A4) and :271 (Assumption A3); index.html:33, :53, :156",
  "L05 states Assumption A3 (strong Markov property, 'not proved here') as a numbered block at L05.html:271 and Assumption A4 (standard facts used without proof) at L05.html:59; the hub's 'stated in Lesson 5' claim is consistent. L05 statement-level checks belong to the L05 slice.")
P("SC1a-r8-project-rung-hours-and-check", "2.9-structure", "course/modules/SC/SC1/index.html:143, :165, :168; project.html:167, :206, :210, :272-281",
  "Rung 2 count 29 (project.html:207); project hours 28 (project.html:272-281); rung 3 names bm_checks.py (project.html).")
P("SC1a-r8-hub-numbers", "2.2-numbers", "course/modules/SC/SC1/index.html:29, :39-42, :74, :143, :150",
  "72 + 28 = 100; 28% of 100 = 28; 7/9 = 77.8%, 8/9 = 88.9%; 29 walks; 9 study hours per lesson.")
P("SC1a-r8-L02-unrounded-E3", "2.2-numbers", "course/modules/SC/SC1/L02.html:419-421, :170",
  "E3 derivation from the unrounded supremum (0.11658934...) re-derived; 0.233179 is the rounding of 2 x unrounded; the printed-digit doubling argument is correct.")
P("SC1a-r9-hub-ost-card-L04", "2.9-structure", "course/modules/SC/SC1/index.html:155 (L04 card); L04.html:7, :51, :103, :109",
  "L04 card 'filtration of Brownian motion, the martingales B_t and B_t^2 - t and the exponential martingale' matches L04 (B_t^2 - t martingale at L04.html:109; exponential martingale at L04.html:51). L04 statement checks belong to the L04 slice.")
F("SC1a-r9-hub-reflection-assumptions", "2.9-structure / 2.4-assumptions", "course/modules/SC/SC1/index.html:33 (lede)",
  "index.html:33 says: 'The reflection is proved in its fixed-time form only; the path-level reflection at the first passage time is not proved.' This is now contradicted by L06, which the delta changed: L06.html:52 ('the path-level reflection is proved in Proposition 2.7'), L06.html:119 (Proposition 2.7 states and proves the reflection principle under A3), L06.html:149 (Remark 2.4 'Proposition 2.7 extends it to the whole reflected path'), L06.html:332 and :531. Read this round; evidence in ledgers/SC1/scripts/SC1-a-r14/out/claims_r14.out. The sentence claims a non-proof that the lesson now proves.",
  "Replace the index.html:33 sentence with: 'The reflection is proved in its fixed-time form (Theorem 2.5 of Lesson 6) and in its path-level form (Proposition 2.7 of Lesson 6), under Assumptions A3 and A4 stated in Lesson 5; that the first-passage time is finite is proved in Lesson 8 under the same assumptions.' Confirm L08.html:88 first (Prob(tau_a<infinity)=1 under A3, A4) before the edit.")
P("SC1a-r9-hub-objective-reflection-proof", "2.9-structure", "course/modules/SC/SC1/index.html:54 (objective 6); course/modules/SC/SC1/L06.html:153",
  "Objective 6 'Prove the fixed-time reflection identity (Lesson 6, Theorem 2.5), under Assumptions A3 and A4' matches L06.html:153 (Theorem 2.5, the reflection identity).")
P("SC1a-r9-quiz-L02-q3-explanation", "2.9-structure", "course/modules/SC/SC1/L02.html:489; L02.html:161",
  "L02 quiz Q3 explanation: Step 2 bounds M_m by sqrt(2 log 2) m r^m; sqrt(m) 2^{-m/2} <= m r^m; matches L02.html:161 (Step 2) and the numbers.")
for i, t in [("SC1a-r10-cmd-check_pages", "tools/check_pages.py --unit SC1"), ("SC1a-r10-cmd-check_dag", "tools/check_dag.py --all"),
             ("SC1a-r10-cmd-check_projects", "tools/check_projects.py --unit SC1"), ("SC1a-r10-cmd-run_labs", "tools/run_labs.py --unit SC1"),
             ("SC1a-r10-cmd-page_smoke", "tools/page_smoke.py --unit SC1 --pages index|L01|L02|L03"),
             ("SC1a-r10-cmd-twins-python-I-W-error", "python -I -W error on each twin from an empty directory"),
             ("SC1a-r10-cmd-verify_refs", "tools/verify_refs.py --offline and --unit SC1"),
             ("SC1a-r10-cmd-ruff-mypy", "ruff check, ruff format --check, mypy --no-incremental"),
             ("SC1a-r10-cmd-pytest-SC1", "pytest -k SC1 tests")]:
    P(i, "2.9-command", "see command", f"Run this round: `{t}`; outputs in {OUT}/ (see the matching SC1a-gate row for the exact line and rc).")
P("SC1a-r10-hub-prereq-curriculum", "2.9-structure", "course/modules/SC/SC1/index.html:35, :58-68; curriculum/01-foundations.yaml:261-265",
  "M6 'Measure-Theoretic Probability' prereqs [M4, M5] (01-foundations.yaml:262-265), recomputed from curriculum.json (prereq chain as in SC1a-hub-prereq-chain).")
P("SC1a-r10-hub-concept-count", "2.9-structure", "course/modules/SC/SC1/L01.html, L02.html, L03.html (dfn); index.html:60; curriculum/03-markets.yaml:513-521",
  "One dfn per lesson for the three in-slice concepts (def-brownian-motion, def-brownian-motion-construction, def-quadratic-variation); curriculum introduces lists 8 concepts; index.html:60 says eight; grep over L04-L08 confirms the other five dfn ids once each.")
P("SC1a-r10-hub-rung2-count", "2.9-structure", "course/modules/SC/SC1/index.html:143; project.html:167, :206, :210",
  "Rung-2 count 29 (project.html:207) re-derived (22 + 7 = 29 by the reflection identity for n=6, a=2).")
P("SC1a-r10-hub-hours-sum", "2.9-hours", "course/modules/SC/SC1/index.html:29, :39-42, :150; L01-L08 data-hours",
  "Eight lessons at data-hours 9 (L01-L08 html root attributes) = 72; project 28; total 100 (hub split 72/28).")
F("SC1a-r10-hub-lede-path-level", "2.9-prose", "course/modules/SC/SC1/index.html:33; L06.html:52, :119, :149, :332",
  "The lede's path-level statement is contradicted by L06 (Proposition 2.7 proves the path-level reflection; L06.html:52, :119, :149, :332, :531). Same sentence as SC1a-r9-hub-reflection-assumptions, checked here as a scope claim. The round-13 PASS on this row was made against the L06 text at e919577, which said 'not proved here' (git show e919577b:course/modules/SC/SC1/L06.html).",
  "Same edit as SC1a-r9-hub-reflection-assumptions (index.html:33).")
P("SC1a-r10-notation-collisions", "2.4-notation", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html; notation/notation.json",
  "Same scan as SC1a-notation-no-registered-collision; notation.json symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, mathbb Q) not used with another meaning.")
P("SC1a-r10-process-words", "2.9-prose", "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
  "Process-word scan repeated this round: no builder/round/verifier/REQUESTS/unit report in learner text; see SC1a-process-words.")
P("SC1a-r10-cards-dup-hypotheses", "2.7-cards", "course/modules/SC/SC1/cards.json (79 L01-L03 cards)",
  f"Full scan of 221 cards: no duplicate ids and no duplicate fronts. Two backs are identical ('They are independent.': SC1-c208 for A1(c), SC1-c210 for A1(e)) but their fronts are different questions, so they are not duplicate cards ({OUT}/delta_and_cards_r14.out).")
P("SC1a-r10-card-L05-ck-wording", "2.7-cards-copy", "course/modules/SC/SC1/index.html:156; L05.html:7, :52",
  "Index card 'Chapman-Kolmogorov identity proved by completing the square' matches L05.html:7 ('Chapman-Kolmogorov identity proved by completing the square') and L05.html:52.")
P("SC1a-r10-A1-attribution-M4", "2.4-assumptions", "course/modules/SC/SC1/L01.html:37, :71-80",
  "A1 is attributed to the prerequisite facts by the Uses row (M4 and M6 concepts) and labelled as citing no source (L01.html:80).")
P("SC1a-r11-A1b-literal-false", "2.4-math", "course/modules/SC/SC1/L01.html:75 (A1(b), second sentence); :112",
  "A1(b) second sentence (a vector whose coordinates are linear combinations of one common independent normal family is multivariate normal) is true (linear image of a Gaussian vector); Remark 1.3 proof uses it at L01.html:112. Re-derived.")
P("SC1a-r11-numbers-recomputed", "2.2-numbers", f"{OUT}/numbers_r14.out (this round's recomputation; the round-13 file numbers_r13.out is context only)",
  "Every number in the slice re-derived this round with an independent script (numbers_r14.py); see the per-page number rows.")
P("SC1a-r11-concept-list-exact", "2.9-structure", "course/modules/SC/SC1/index.html:58-68; curriculum/01-foundations.yaml; curriculum/03-markets.yaml:513-521",
  "Concept lists in the hub match the closure and the introduced concepts; check_dag PASS.")
P("SC1a-r11-hours-and-projects", "2.9-hours", "course/modules/SC/SC1/L01-L08 data-hours; index.html:29, :39-42, :150; project.html:33, :272-281",
  "Recomputed: 9 x 8 = 72, project 2+3+10+8+3+2 = 28, total 100.")
P("SC1a-r11-cards-scan", "2.7-cards", "course/modules/SC/SC1/cards.json (221 cards this pin)",
  f"Full scan this round: 221 cards, 0 duplicate ids, 0 duplicate fronts; 79 cards in L01-L03 (previous pin 76, 3 added, 12 changed; see SC1a-r14-cards-L01-L03-changed). Output in {OUT}/delta_and_cards_r14.out.")
P("SC1a-r11-delta-read", "2.9-delta", "git diff e919577b 8e5751c9 for index.html, L01.html, L02.html, L03.html, cards.json, tests/labs/SC1",
  f"Every hunk in the slice read (ledgers/SC1/scripts/SC1-a-r14/delta_slice_a_r14.diff): index.html:181-184 (wording); L01.html:51, :215, :353, :434 (wording); L02.html:149, :292, :306, :439, :458-461, :547 (wording and the R2 fix); L03.html unchanged; twins unchanged; 12 L01-L03 cards changed and 3 added. Defects found in the delta are rows SC1a-r9/r10-hub-* and the cross-slice check of L06.")
P("SC1a-r11-twins-venv-314", "2.5-labs-run", ".venv (CPython)",
  "`.venv/bin/python --version` -> Python 3.14.8, the version named by pyproject requires-python >=3.14 and by VERIFIER 2.5 for the lab interpreter. (Pyodide version is not inspected here.)")
P("SC1a-r13-L02-R2-scope-only", "2.4-scope", "course/modules/SC/SC1/L02.html:439 (R2 solution)",
  "Round-13 FAIL is closed. Now: 'The bounds Prob(E_m^c) <= 2^{-m} come from Lemma 2.1, which uses Assumption 2.1(a), and the union bound and continuity from below use Assumption 2.1(c). So the deduction uses Assumption 2.1(a) and Assumption 2.1(c).' Re-derived: Lemma 2.1 uses (a); the union bound and continuity from below use (c). Accurate.")
P("SC1a-r13-L02-assumption21-part-naming", "2.9-structure / 2.4-assumptions", "course/modules/SC/SC1/L02.html:99 (convention); :149 (Prop 2.4 H3); :292 (Thm 2.5 H2); :306 (Remark 2.6 H2)",
  "Round-13 FAIL is closed. L02.html:149 'Assuming Assumption 2.1(a)-(c)'; :292 'Assuming A2 and Assumption 2.1(a)-(c)'; :306 'Assuming A1(a), A1(b), A1(e), A2 and Assumption 2.1(a)-(c)'. Lemma 2.1 H2 names 2.1(a) (L02.html:106); Lemma 2.3 names A1 only. Every result that uses 2.1 now names its part.")
P("SC1a-r13-cards-L01-L03-read", "2.7-cards", "course/modules/SC/SC1/cards.json (79 L01-L03 cards)",
  "Round-13 row carried 76 identical cards; the pin changed, so every L01-L03 card was re-read this round (79 cards; the 21 changed and 3 added are checked against the current lesson text; c011-c013 now say 2.1(a)-(c); c054 and c060 reworded; c207/c232 and c210/c233/c234 split). Evidence: out/delta_and_cards_r14.out (card diff) and the full card dump read this round.")
P("SC1a-r14-cards-L01-L03-changed", "2.7-cards", "course/modules/SC/SC1/cards.json: c011-c013, c029, c032, c034, c035, c054, c060, c207, c210, c220 changed; c232-c234 added",
  f"Changed L01-L03 card objects checked against the current lesson text: c011-c013 (Remark 2.6 hypotheses, L02.html:306; B~ construction, L01.html:215); c029/c032/c034/c035/c220 (Prop 2.4 / Thm 2.5 / Remark 2.6 hypotheses now (a)-(c), L02.html:149, :292, :306); c054 (dependent family, L03.html:382); c060 (Assumption 3.2(a), L03.html:71); c207/c232, c210/c233 (A1(b), A1(e) split, L01.html:75, :78); c234 (Assumption 3.2(b), L03.html:71). All agree. ({OUT}/delta_and_cards_r14.out)")
P("SC1a-r10-lab-L01-L02-L03-claims-dup", "2.5-lab-claims", "see SC1a-r10-lab-L01-L02-L03-claims", "Duplicate-check of the same claim; evidence as in that row.")
R.pop("SC1a-r10-lab-L01-L02-L03-claims-dup", None)


P("SC1a-r4-twin-timing-and-purity", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
  f"Each twin run alone with python -I -W error from an empty directory: rc=0, no stderr, stdout equal to the page's expected block ({OUT}/twins_r14.out). Page_smoke lab times 0.0 s (L01), 0.2 s (L02), 0.1 s (L03) on this machine; informational, not a Pyodide claim.")
P("SC1a-r8-lab-mutants", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py",
  f"Lab mutants of the three twins re-run this round: 9 of 9 differ from the expected block ({OUT}/lab_mutants_all_r14.out); the round-8 set is among them (ledgers/SC1/lab-mutants/SC1a-r6-* and SC1a-lab-mut*).")
P("SC1a-r10-L02-quiz-q3-math", "2.2-numbers", "course/modules/SC/SC1/L02.html:483-489",
  "Quiz Q3: the terms sqrt(m) 2^{-m/2} are at most m r^m with r=2^{-1/2} (since sqrt(m) <= m), and sum m r^m = r/(1-r)^2 = 8.2426... (numbers_r14.out) is finite; option wording and explanation correct.")
P("SC1a-r10-L03-key-results-14pct", "2.2-numbers", "course/modules/SC/SC1/L03.html:398",
  f"'within 14 percent' and '13.2 percent at H=2, N=1' recomputed from the printed values: 13.21% ({OUT}/numbers_r14.out).")
P("SC1a-r10-L03-why-sample-means", "2.5-lab-claims", "course/modules/SC/SC1/L03.html:51; tests/labs/SC1/lab-SC1-L03-1.py main()",
  "L03.html:51 says the lab 'prints the sample means with standard errors'; the twin's main() prints mean, se and z for every horizon and level (output lines 218-235).")
P("SC1a-r10-L03-R3-hypothesis", "2.4-math", "course/modules/SC/SC1/L03.html:382; :99-103",
  "R3 hypothesis: all increments equal one variable, so the family is not independent and Theorem 2.3's (H1) and (H2) fail; (H2) names Assumption 3.2 for independent variables (L03.html:71(a)). Re-derived.")

# ---- round-14 FAIL rows (new) ----
F("SC1a-r14-L01-keyresult-remark13-scope", "2.4-math (key-results summary)", "course/modules/SC/SC1/L01.html:351",
  "Key-results row: 'Each finite vector (B_{t_1},...,B_{t_r}) is multivariate normal with covariance min(t_i,t_j) (Remark 1.3), assuming A1(a) and A1(b)'. Remark 1.3 (L01.html:107) is stated only for 0<t_1<...<t_r; the row drops that hypothesis and says 'each finite vector'. (Locator: ledgers/SC1/scripts/SC1-a-r14/out/claims_r14.out.) The statement is true with t_i>=0 but is not the cited result.",
  "Edit L01.html:351 to 'For 0<t_1<...<t_r, the vector (B_{t_1},...,B_{t_r}) is multivariate normal with covariance min(t_i,t_j) (Remark 1.3), assuming A1(a) and A1(b)'.")
F("SC1a-r14-L02-keyresult-lemma21-lambda", "2.4-math (key-results summary)", "course/modules/SC/SC1/L02.html:459",
  "Key-results row: 'P(|eta|>lambda) <= 2 e^{-lambda^2/2} for a standard normal eta (Lemma 2.1)' with no hypothesis on lambda. Lemma 2.1 H1 (L02.html:105) requires lambda >= 0. For lambda = -10 the left side is 1 and the right side is 2e^{-50}, about 3.9e-22 (the bound fails), so the row omits a stated hypothesis.",
  "Edit L02.html:459 to 'for \\(\\lambda\\ge 0\\) and a standard normal \\(\\eta\\) (Lemma 2.1)'.")
F("SC1a-r14-L03-keyresult-lemma22-mean", "2.4-math (key-results summary)", "course/modules/SC/SC1/L03.html:395",
  "Key-results row: 'For X normal with variance Delta: E[X^4] = 3 Delta^2 and Var(X^2) = 2 Delta^2 (Lemma 2.2)'. Lemma 2.2 (L03.html:90) requires mean zero and Delta>0. For a normal with mean 1 and variance 1, E[X^4] = 10, not 3 (computed: E[(1+Z)^4] = 1+6+3 = 10), so the row omits the mean-zero hypothesis.",
  "Edit L03.html:395 to 'For \\(X\\) normal with mean 0 and variance \\(\\Delta>0\\): ...' (keep the rest of the row).")

# ---- verifying the mean-1 computation used in the row ----
import random

missing = [i for i in prev_ids if i not in R]
if missing:
    print("MISSING round-13 ids:", missing)
    sys.exit(1)
new_ids = [i for i in R if i not in prev_ids]
print("round-13 ids kept:", sum(1 for i in prev_ids if i in R), "of", len(prev_ids), "| new ids:", new_ids)

rows = []
for rid in prev_ids + new_ids:
    check, loc, status, ev, fix = R[rid]
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = fix
    rows.append(row)

mutants = [
    {"id": "SC1a-r14-lab-n1-L01-dyadic-depth-off-by-one", "description": "lab-SC1-L01-1: dyadic piece length uses 2**(n+1) pieces (student depth off-by-one); the variance sums fail to equal t and the count line prints 0 of 15.",
     "killed_by": "exact diff vs expected block (ledgers/SC1/lab-mutants/SC1a-r14-lab-n1-L01-dyadic-depth-off-by-one.py; out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-r14-lab-n2-L02-hat-support-halved", "description": "lab-SC1-L02-1: hat slope doubled so the support is half the radius 2**(-m) of Definition 2.1; the grid-supremum value changes to 0.252987.",
     "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-r14-lab-n3-L03-se-missing-root-n", "description": "lab-SC1-L03-1: standard error omits the division by sqrt(n) (sd instead of sd/sqrt(n)); every se and z in the printed block changes.",
     "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-lab-mut1-L01-cov-max", "description": "lab-SC1-L01-1: covariance sums increments up to max(i,j) instead of min(i,j) (round-6 mutant re-run).", "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-lab-mut2-L02-scale", "description": "lab-SC1-L02-1: hat scale altered (round-6 mutant re-run).", "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-lab-mut3-L03-closed-form", "description": "lab-SC1-L03-1: closed form altered (round-6 mutant re-run).", "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-r6-lab-mut1-L01-min-to-max", "description": "lab-SC1-L01-1: min replaced by max in the covariance (round-6 mutant re-run).", "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-r6-lab-mut2-L02-scale", "description": "lab-SC1-L02-1: scale variant (round-6 mutant re-run).", "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
    {"id": "SC1a-r6-lab-mut3-L03-closed-form", "description": "lab-SC1-L03-1: closed-form variant (round-6 mutant re-run).", "killed_by": "exact diff vs expected block (out/lab_mutants_all_r14.out)"},
]

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"

fragment = {
    "unit": "SC1",
    "slice": "a",
    "round": 14,
    "verifier": "Haiku independent verifier, SC1-a round 14 (did not build SC1)",
    "pin": "8e5751c903f0246115eba746afdf5d71f612bb37",
    "base": "e919577b45b431ce68e1e6533b00b8a301277937 (round-13 pin; round-13 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round13.json used as context only)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a (detached at 8e5751c, .venv symlinked)",
    "scratch": "none used for evidence; all scripts are under ledgers/SC1/scripts/SC1-a-r14/",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) is the second source the curriculum lists for SC1 (curriculum/03-markets.yaml:524). references/references.json has no record (grep -i karatzas: 0 hits). index.html:184 says the module cites nothing from it, which is correct. A registry request is needed only if the architect wants the source cited."
    ],
    "freshness_flags": [],
    "notes": [
        f"Scope: index.html (190 lines), L01.html (446), L02.html (560), L03.html (504) and the three twins were read in full at 8e5751c. The 79 L01-L03 cards were read in full. Delta since e919577 read hunk by hunk ({OUT}/../delta_slice_a_r14.diff).",
        "Round-13 FAIL rows: SC1a-exercises-L01-L03, SC1a-r13-L02-R2-scope-only and SC1a-r13-L02-assumption21-part-naming are now PASS after re-derivation. All 36 problems re-derived.",
        "Round-13 PASS rows were not carried. Every row is re-verified this round: the subject files changed (index.html, L01, L02, cards.json) or the row was re-derived for independence. The L03.html, the three twins and the lab sections of L01 and L02 are byte-identical to the round-13 pin (out/delta_and_cards_r14.out), so their rows could be carried; they were re-run instead.",
        "Five FAIL rows this round, four distinct defects: the hub reflection sentence (index.html:33; two rows) contradicts L06 as changed in this delta; three key-results rows drop a stated hypothesis (L01.html:351 Remark 1.3 scope; L02.html:459 lambda >= 0; L03.html:395 mean zero).",
        "Gates re-run at 8e5751c: check_pages, check_dag --all, check_projects, run_labs (11/11), page_smoke per page (alone), ruff check and format, mypy --no-incremental (385 files), pytest -k SC1 (11) and collect, verify_refs --offline and --unit SC1 (live), fetch_data --check. All rc=0; script ledgers/SC1/scripts/SC1-a-r14/gates_r14.sh.",
        "Lab mutants: 3 new student-error mutants written and killed; 6 existing lab mutants re-run and killed. They live in ledgers/SC1/lab-mutants/ (not ledgers/SC1/mutants/, because tools/mutate_graders.py reads that directory as grader mutants). Lab twins are demonstrations, so grader mutation (tools/mutate_graders.py) is not applied to this slice; the grader is a project slice.",
        "Not checked in this slice: L04-L08 prose, project.html and the grader (other slices); L04-L08 cards (other slices); the Shreve book (no passage is cited, so nothing was read from it); run_graders.py and mutate_graders.py (not slice-a gates); the Pyodide interpreter version (page_smoke reports only timings); the L05/L06/L08 statements that the hub cites, which were checked only at the heading or line the hub names (L05.html:59, :271; L06.html:52, :119, :149, :332; L08.html:88).",
        "Timings: page_smoke reported lab times of 0.0-0.2 s and boot 1.1-1.2 s. The machine also ran other verifiers' pytest processes at the start of the run, so timings are informational.",
        "Row ids: every round-13 id is kept (132). New ids this round: SC1a-r14-L01-keyresult-remark13-scope, SC1a-r14-L02-keyresult-lemma21-lambda, SC1a-r14-L03-keyresult-lemma22-mean, SC1a-r14-cards-L01-L03-changed, SC1a-r14-lab-mutants-new3.",
    ],
    "summary": {
        "text": f"SC1-a round 14 at 8e5751c: verdict FAIL. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: SC1a-r9-hub-reflection-assumptions and SC1a-r10-hub-lede-path-level (index.html:33 vs L06 as changed), SC1a-r14-L01-keyresult-remark13-scope (L01.html:351), SC1a-r14-L02-keyresult-lemma21-lambda (L02.html:459), SC1a-r14-L03-keyresult-lemma22-mean (L03.html:395).",
        "counts": counts,
        "mutants": f"{len(mutants)} of {len(mutants)} killed (3 new round-14 lab mutants + 6 existing lab mutants)",
    },
}

json.dump(fragment, open(ROOT + "/ledgers/SC1/SC1-a.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", ROOT + "/ledgers/SC1/SC1-a.json", "rows", len(rows), counts, "verdict", verdict)
