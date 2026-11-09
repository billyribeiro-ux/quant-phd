"""Round-15 fragment builder for SC1 slice a (pin d1e65a0). Keeps every round-14 row id.

Each row's evidence names what was re-checked this round; outputs live under ledgers/SC1/scripts/SC1-a-r15/out/.
Usage: python3 -I build_fragment_r15.py <checkout-root>
"""
import json
import sys

root = sys.argv[1]
prev = json.load(open("/Users/billyribeiro/.fanout/frags/E-SC1-a.round14.json", encoding="utf-8"))
O = "ledgers/SC1/scripts/SC1-a-r15/out/"
G = "gates_r15.sh"

GATE = {
    "SC1a-gate-check-pages": (PASS := "PASS"), }

E = {}  # id -> (status, evidence[, fix])
def P(i, ev):
    E[i] = ("PASS", ev)
def F(i, ev, fix):
    E[i] = ("FAIL", ev, fix)
def U(i, ev, fix):
    E[i] = ("UNVERIFIABLE", ev, fix)

RUFF_FIX = ("Pin at aeb512b6 or later (adds ledgers/*/lab-mutants to extend-exclude), or rewrap line 1 of "
            "ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py to 120 columns.")
RUFF_EV = (f"`.venv/bin/python -m ruff check .` at d1e65a0 -> 'Found 1 error': E501 Line too long (133 > 120) at "
           f"ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py:1:121 ({O}ruff_check.out). With "
           f"`--extend-exclude 'ledgers/*/lab-mutants'` it prints 'All checks passed!' ({O}ruff_check_excl_lab_mutants.out). "
           "No SC1 course, twin or grader file is involved.")

# gates
P("SC1a-gate-check-pages", f"`tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS' rc=0; `--all` rc=0 ({O}check_pages_SC1.out, {O}check_pages_all.out; {G}).")
P("SC1a-gate-check-dag", f"`tools/check_dag.py --all` rc=0, 'check_dag SC1: PASS' ({O}check_dag_all.out).")
P("SC1a-gate-run-labs", f"`tools/run_labs.py --unit SC1` -> 'run_labs SC1: PASS (11/11)', rc=0 ({O}run_labs_SC1.out).")
P("SC1a-gate-page-smoke", f"`tools/page_smoke.py --unit SC1 --pages p` for index, L01, L02, L03 run alone: each PASS, rc=0 ({O}page_smoke_*.out).")
F("SC1a-gate-lint-types-tests", f"ruff check FAILS at pin (E501 in ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py:1; {O}ruff_check.out). ruff format --check '563 files already formatted'; mypy --no-incremental 'Success: no issues found in 385 source files'; pytest -k SC1 '11 passed', collect 11 ({O}pytest_SC1*.out, {O}mypy_full.out).", RUFF_FIX)
P("SC1a-gate-verify-refs", f"`tools/verify_refs.py --unit SC1`: 'live re-verification of SC1: 1 of 560 entries, 0 problems'; `--offline`: '560 entries, 0 problems' ({O}verify_refs_*.out). index.html:182 data-cite shreve2004stochastic resolves.")
P("SC1a-lab-L01-twin", f"Twin tests/labs/SC1/lab-SC1-L01-1.py vs page L01.html data-run block: code identical after unescape+strip; run alone as `python -I -W error` from an empty dir: rc=0, stderr empty, stdout == expected block (6 lines) ({O}twins_r15.out).")
P("SC1a-lab-L02-twin", f"Twin lab-SC1-L02-1.py vs L02.html: code identical; `-I -W error` rc=0, empty stderr, 12 stdout lines == expected block ({O}twins_r15.out).")
P("SC1a-lab-L03-twin", f"Twin lab-SC1-L03-1.py vs L03.html: code identical; rc=0, empty stderr, 35 stdout lines == expected block ({O}twins_r15.out).")
P("SC1a-lab-claims-L01", "Twin docstring (lines 1-9: 'simulates no path', exact Fraction) and L01.html:136, :208 read against output: 15 of 15 dyadic cases, 81 of 81 pairs, Cov(B_1/4,B_5/8)=1/4 (recomputed, numbers_r15.out); no random call in twin.")
P("SC1a-lab-claims-L03", f"L03.html:133 (400 paths, H=1,2, k=0..7, se = H*sqrt(2/N)/20, |z|<=3 claim) vs twin and output; :253 |z| max 2.39 at H=1,N=2, next 1.84 at H=1,N=128 recomputed from printed mean/se (numbers_r15.out); :343 consistent.")
P("SC1a-lab-L02-docstring", f"Twin docstring lines 1-8 ('identities hold for every seed') checked by a 300-seed sweep: 0 failures ({O}seed_sweep_r15.out).")
P("SC1a-r4-seed-sweep-L02", f"Seeds 0..299 re-swept this round: identity-line failures = 0 ({O}seed_sweep_r15.out).")
P("SC1a-lab-L02-hypothesis-expected", "L02.html:170 hypothesis (SIMULATED, 216 of 216, grid-sup True, bound lines) matches expected block at :266-277 and twin output (twins_r15.out).")
P("SC1a-simulated-labels", "L02.html:170, :173 and L03.html:132, :136 carry the SIMULATED label; L03 interpretation says 'one seed'.")
P("SC1a-r4-twin-timing-and-purity", f"Twins: no network, seeded RNG only (L02, L03) or none (L01), stdlib only; page_smoke lab times 0.0-0.2 s ({O}page_smoke_*.out).")
P("SC1a-r8-lab-mutants", f"Lab mutants (ledgers/SC1/lab-mutants/): 13 of 13 killed (output differs from expected block) this round ({O}lab_mutants_r15.out).")
P("SC1a-r10-lab-mutants-4of4", f"Re-run this round: the four SC1a-r13 lab mutants in ledgers/SC1/lab-mutants/ are killed ({O}lab_mutants_r15.out).")
P("SC1a-r11-lab-mutants-6of6", f"Re-run this round: all 10 pre-existing lab mutants in ledgers/SC1/lab-mutants/ are killed ({O}lab_mutants_r15.out).")
U("SC1a-r14-lab-mutants-new3", "The round-14 row cites ledgers/SC1/lab-mutants/SC1a-r14-lab-n1..n3. Those files are absent at d1e65a0 (ls ledgers/SC1/lab-mutants lists 10 files; `git log --all -- 'ledgers/SC1/lab-mutants/SC1a-r14*'` returns nothing).", "Commit the three round-14 mutant files, or retire this row. Round-15 replacements are SC1a-r15-lab-p1..p3 (killed, see SC1a-r15-lab-mutants-p1-p3).")
P("SC1a-r10-L03-why-sample-means", "L03.html:51 and the twin's main(): sample means printed with se; 'one seed' wording matches output (twins_r15.out).")
P("SC1a-r10-lab-L01-L02-L03-claims", "Twin docstrings (L01 1-9, L02 1-8, L03 1-14) read this round against the outputs: all count and identity claims match (twins_r15.out).")
P("SC1a-r12-L02-identities-301-seeds", f"Re-run this round over seeds 0..299: 0 failures ({O}seed_sweep_r15.out).")
P("SC1a-r13-L02-R2-scope-only", "L02.html:439 R2 solution: uses the Lemma 2.1 bound, the union bound and continuity from below (Assumption 2.1(a),(c)), which is what the R2 question asks; no claim beyond it.")

# numbers
P("SC1a-numbers-L01", "L01.html:132 (1/2, 1/10, 1/4 pieces), :230 (sd 1/10, ratio 10), :299 (3/64, 16*3/64=3/4), :306 (2*1/8=1/4), :350-353, :391-399, :410-413 (Var(3B1-B2)=5, E[B3^2]=3, Var(B2)=2, Cov(B2,B5)=2) re-derived (numbers_r15.out, hand arithmetic in this round's notes).")
P("SC1a-numbers-L02", f"L02.html:268-277 printed block == twin output; bounds 0.832555 ... 0.208139 and their sum over levels 5-8 = 1.309399 recomputed (numbers_r15.out); the grid sup 0.348139 is the twin's printed value and equals the expected block (twins_r15.out).")
P("SC1a-numbers-L03", "L03.html:253 (|z| 2.39, 1.84), :270 (0.166664 at H=2,N=128), :275, :343, :350 (2.65625 = 4080/1536), :357 (0.0125), :368, :375, :398, :434 (0.625) recomputed (numbers_r15.out).")
P("SC1a-numbers-L02-36-points", "36 point-depth pairs = 2+3+5+9+17; 216 = 18+24+35+54+85 (numbers_r15.out: 'dyadic cases 216, points 36').")
P("SC1a-numbers-L03-SE-follow", "Largest |gap| 13.2078% at H=2,N=1 (0.1601/(2*sqrt2/20)-1 = 0.1320780); next 9.18% at H=2,N=4 (numbers_r15.out).")
P("SC1a-r8-hub-numbers", "index.html:29, :39-42 (72/28 h, 28%), :74 (nine questions, 7/9 = 77.8, 8/9 = 88.9 %), :143 (rung-2 answer 2, recomputed), :150 (8 x 9 h = 72) recomputed (numbers_r15.out).")
P("SC1a-r8-L02-unrounded-E3", f"L02.html:421: unrounded level-1 sup = 0.11658934473943267; |xi_11| = 0.23317868947886533 -> 2*sup = 0.2331787, rounds to 0.233179; 2*printed 0.116589 = 0.233178; sqrt(4 log 2)=1.665109, half 0.832555 (numbers_r15.out).")
P("SC1a-r10-L02-E3-unrounded", "Same check as SC1a-r8-L02-unrounded-E3 (numbers_r15.out).")
P("SC1a-r10-L02-quiz-q3-math", "L02.html:483-489: sqrt(m) 2^(-m/2) <= m r^m and sum m r^m = r/(1-r)^2 = 8.242641 (numbers_r15.out) match the quiz explanation.")
P("SC1a-r10-L03-key-results-14pct", "L03.html:398 row: 'within 14 percent' and '13.2 percent at H=2, N=1' match numbers_r15.out.")
P("SC1a-r11-numbers-recomputed", f"Recomputed this round in {O}numbers_r15.out (round-14 file superseded; numbers unchanged).")
P("SC1a-r10-hub-hours-sum", "index.html:29, :39-42, :150 and data-hours=9 on L01-L08 (grep: one data-hours per page, value 9) sum to 72; project.html data-hours-project=28; 72+28=100 = curriculum hours (curriculum.json / 03-markets.yaml:508).")
P("SC1a-hub-hours", "index.html:29 data-hours-lessons=72, data-hours-project=28; :39-42 bar 72%/28%; :150 eight x 9 h; project.html data-hours-project=28.")
P("SC1a-r11-hours-and-projects", "data-hours 9 on L01-L08 read this round; project.html:272-281 rung hours; index.html:143, :165 consistent.")
P("SC1a-r8-curriculum-facts", "index.html:31 (Tier M, 100 h), :35 (closure M1, M2, M4, M5, M6, P0.1), :60 (eight concepts), :184 (two sources): curriculum/03-markets.yaml:505-508 (SC1 tier M, 100 h) and curriculum.json SC1 introduces (8 keys) and sources (2 entries) read this round.")
P("SC1a-hub-grade-definition", "index.html:79 'A theorem, proved on the page or with a precisely cited proof' equals BLUEPRINT.md:158 'Theorem: proved on the page, or with a precisely cited proof'.")

# grades
P("SC1a-grade-L01", "L01.html:83 (Prop 1.2 T), :101 (Remark 1.3 T), :119 (Example 1.4 T), :349-353 (key results T with proof locators); the lab-based row is not graded T.")
P("SC1a-grade-L02", "L02.html:74 (Lemma 2.2 T), :103 (Lemma 2.1 T), :121 (Lemma 2.3 T), :145 (Prop 2.4 T), :288 (Thm 2.5 T), :302 (Remark 2.6 T); A2 labelled 'not proved' at :281-286.")
P("SC1a-grade-L03", "L03.html:77 (Lemma 2.1 T), :90 (Lemma 2.2 T), :99 (Thm 2.3 T), :118 (Prop 2.4 T), :394-398 (C row with basis 'Lab 1 (SIMULATED), one seed').")
P("SC1a-canon-breaks-ungraded", "Canon-break items (L01.html:215-217, L02.html:319-327, L03.html:259-261) make counter-claims and carry no T grade; they point to proofs or stated assumptions.")
P("SC1a-grade-L02-remark2.6", "L02.html:302-318 Remark 2.6: T; proof under the named assumptions (H2 lists A1(a), A1(b), A1(e), A2, Assumption 2.1(a)-(c)).")
P("SC1a-r10-L03-R3-hypothesis", "L03.html:382 R3 solution and :99-103 Theorem 2.3 hypotheses: H1 failure named correctly (increments not independent).")
P("SC1a-r4-thm23-counterexample-L03", "L03.html:382: the R3 counterexample (dependent increments) is correct: Var(Q)=2t^2 for all N.")

# math
P("SC1a-math-L01-prop1.2", "L01.html:84-98 re-derived: E[XY]=EXEY via A1(a) for X=B_s, Y=B_t-B_s; Cov = E X^2 = s; s=0, s=t cases; integrability via |XY|<=(X^2+Y^2)/2.")
P("SC1a-math-L01-remark1.3", "L01.html:101-113 re-derived: (D3) independence, (D2) normality, A1(b) joint normality, covariance by Prop 1.2; hypothesis 0<t_1<...<t_r at :107 matches the key-results row (:351).")
P("SC1a-math-L01-canon-construction", "L01.html:215 canon item 1: hypotheses list 'A1(a), A1(b), A1(e), A2 and Assumption 2.1(a)-(c)' matches Remark 2.6 (L02.html:306); product-space argument re-derived (U uniform, independent; B~ same fdd; discontinuous at U).")
P("SC1a-math-L02-lemmas-2.1-2.2", "L02.html:73-117 re-derived: Lemma 2.2(a)-(e) (hats, disjoint supports, dyadic vanishing, linearity); Lemma 2.1 Chernoff bound with theta=lambda >= 0 (lambda >= 0 required).")
P("SC1a-math-L02-lemma2.3-arithmetic", "L02.html:132-140 re-derived: Var(U_j) = 2^-(n+2)+2^-(n+2) = 2^-(n+1); Cov(U_j,V_j)=0; numbers_r15.out 'Var(U) n=0..3 True'.")
P("SC1a-math-L02-prop2.4", "L02.html:145-165 re-derived: P(E_m^c) <= 2^(m-1)*2*2^(-2m) = 2^-m; P(A^c_m0) <= 2^(1-m0); M_m identity max error 1.1e-16 (numbers_r15.out); summability via r/(1-r)^2.")
P("SC1a-math-L02-A2-sketch", "L02.html:281-286: A2 labelled as assumed; sketch names the skipped passage of characteristic functions to the limit.")
P("SC1a-math-L02-thm2.5", "L02.html:288-300 re-derived: (D1) via Sigma_M(0)=0 (P2 at :387-389), (D2)/(D3) from A2, continuity from Prop 2.4(b).")
P("SC1a-math-L03-thm2.3", "L03.html:99-115 re-derived: E Q = t (telescoping), Var Q = sum 2 Delta^2 (Lemma 2.2, A3.2(a),(b)), error bound sum Delta^2 <= |P| t.")
P("SC1a-math-L03-prop2.4", "L03.html:117-129 re-derived: (b^2-a^2)^2 <= 4H^2(b-a)^2; S(N)=N(4N^2-1)/3 by induction; exact sum H^4(4N^2-1)/(3N^3); closed form matches all 16 cells (numbers_r15.out: 0 mismatches).")
P("SC1a-math-L03-misc-claims", "L03.html:259-261, :270, :274-279, :366-382 re-derived: fourth-moment remark, dependence counterexample (Var 2t^2), expected absolute-increment sum sqrt(2Nt/pi) (E|Z| quadrature check 0.7978845611 vs sqrt(2/pi)=0.7978845608).")
P("SC1a-math-L03-density", "L03.html:78, :332: E Z^2 = 1, E|Z| = 2 phi(0) = sqrt(2/pi) (P3) re-derived.")
P("SC1a-grade-L02-remark2.6-math", "Remark 2.6 proof re-read: refinement, (D2) via A1(a),(b) and copies, (D3) via A1(e); no gap found.")
P("SC1a-math-L02-thm2.5-extension", "L02.html:314 refinement paragraph re-read: pieces from distinct copies for s<t; each unit interval contributes at most one piece.")
P("SC1a-r4-cauchy-schwarz-L01", "L01.html:95: |XY| <= (X^2+Y^2)/2 used for integrability (not Cauchy-Schwarz); index.html:69 promise matches the assumptions stated.")
P("SC1a-r6-variance-t0-L01", "L01.html:67: Var(B_t)=t for all t>=0, from (D1) at t=0 and (D2) with s=0 for t>0.")
P("SC1a-r11-A1b-literal-false", "L01.html:75 A1(b) second sentence (vector of combinations of one common independent-normal family is multivariate normal) is a true standard fact; :112 uses it correctly.")
P("SC1a-r5-gaussian-process-scope-L01", "L01.html:107 and :115: Gaussian process claim restricted to 0<t_1<...<t_r and to s,t>0.")
P("SC1a-r6-quiz-mesh-hypothesis-L03", "L03.html:437-443: Assumption 3.1 named as the mesh condition; quiz explanation matches Theorem 2.3's conclusion.")
P("SC1a-r8-A3-in-L05", "L05.html:59 'Assumption A4' block and :271 'Assumption A3 (strong Markov property; not proved here)' exist; index.html:33 cites them as Lesson 5 assumptions.")
P("SC1a-attrib-L01-A1-parts", "L01.html:37 (parts (a) to (e), stated in §2) and :72-80 (five parts) read: consistent with the uses in §2 and §4.")
P("SC1a-r10-A1-attribution-M4", "L01.html:37, :71-80: A1 is labelled as a prerequisite fact with no source; no bibliographic claim attached.")
P("SC1a-hub-assumption-promise", "index.html:69 promise ('stated as numbered Assumption ... labelled as such (Lesson 1, A1)') matches L01.html:71-81 and L02.html:92-99, :281; index.html:184 consistent.")
P("SC1a-assump-L01-P3", "L01.html:285-288 (P3: Assuming A1(a)): symmetry of covariance only; solution correct.")
P("SC1a-assump-L02-grouping", "L02.html:106, :116, :138: grouping and independence uses (A1(a), A1(e)) named where used.")
P("SC1a-attrib-L02-lemma2.1-union", "L02.html:97 (Assumption 2.1(c) union bound) and :158 (Prop 2.4(a)) consistent.")
P("SC1a-r13-L02-assumption21-part-naming", "L02.html:99 convention; :149 (Prop 2.4 H3 = Assumption 2.1(a)-(c)); :292 (Thm 2.5 H2); :306 (Remark 2.6 H2); names match the parts stated at :93-99.")
P("SC1a-r9-quiz-L02-q3-explanation", "L02.html:489 explanation and :161 Step 2 reference: correct (sqrt m 2^(-m/2) <= m r^m).")

# notation
P("SC1a-notation-macros", "All macros used on index, L01-L03 are registry macros (\\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic) or standard LaTeX; no unregistered macro (checked against notation/notation.json, 26 macros).")
P("SC1a-notation-no-registered-collision", "Registered symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, \\mathbb{Q}. None used on these pages (no T, Phi, gamma, R_f); plain Q(P) is the quadratic variation, not \\mathbb{Q}.")
P("SC1a-notation-T-subscript", "No plain T in math on these pages; the horizon is H (L03.html:120 note on T reserved for return observations, which matches notation.json 'T').")
P("SC1a-notation-H-horizon", "L03.html:120, :122, :128, :133 use H as horizon; the twin uses H only as a horizon; notation.json has no H entry.")
P("SC1a-r4-notation-S-symbol-L02", "L02.html has no plain S in math; L03.html:128 uses S(N) locally (a local sum, not registered).")
P("SC1a-r10-notation-collisions", "notation/notation.json symbols vs the pages: no collision (see SC1a-notation-no-registered-collision).")
P("SC1a-r7-notation-F-clarity-L01", "L01.html:55, :215 use F-sigma-algebra; no registry conflict.")

# prose / banned / process / scope
P("SC1a-banned-phrases", "grep (case-insensitive) for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, well known, obviously, clearly on index, L01-L03, cards.json: 0 hits; '...' occurs only as \\dots/ellipsis in math ranges.")
P("SC1a-process-words", "grep for round, verifier, delta, pin, fragment, builder, checker, revision, previous version, corrected, reviewer on index, L01-L03, cards.json: 0 process-word hits in learner text ('rounded' is arithmetic).")
P("SC1a-r10-process-words", "Same grep as SC1a-process-words: 0 hits.")
P("SC1a-prose-L01-three-conditions", "index.html:49 and L01.html:51, :61-63 state the three conditions of Definition 1.1 consistently.")
P("SC1a-scope-words-L02-L03", "L02.html:139, :158, :316, :389; L03.html:85, :104, :133, :253, :270 scope words ('every', 'all', 'only') checked against the computation or hypothesis they qualify; no unsupported scope found.")
P("SC1a-scope-L01-prop1.2-only", "L01.html:216-217: 'Proposition 1.2 uses A1(a) only' is consistent with the proof (:94-98).")
P("SC1a-scope-L03-converge", "L03.html:270 misconception 1: sums vanish in the limit for s^2; for Brownian motion mean is t for every partition (Thm 2.3) - no overreach.")
P("SC1a-prose-two-sources", "index.html:184 and references/references.json: shreve2004stochastic is in the registry (title 'Stochastic Calculus for Finance II', 2004); 'Karatzas' has 0 registry hits (grep -c -i karatzas = 0), consistent with index.html:184.")
P("SC1a-ref-L01-every-result", "L01.html:434 references paragraph: no registry source cited; every result proved or assumed on the page (or Remark 2.6 named).")
P("SC1a-reference-section-L02-L03", "L02.html:547 and L03.html:491 reference sections: no passage attributed; L03 names shreve2004stochastic at book level only.")
P("SC1a-r9-hub-ost-card-L04", "index.html:155 L04 card ('filtration, martingales B_t, B_t^2-t and the exponential martingale') matches L04 headings (Def 1.1, Prop 2.2, 2.3, 2.4).")
P("SC1a-r10-card-L05-ck-wording", "index.html:156 card ('Chapman-Kolmogorov identity proved by completing the square', 'strong Markov property stated as Assumption A3') matches L05.html Lemma 2.2 (completing the square), Theorem 2.1 and Assumption A3 (:271).")
P("SC1a-r8-project-rung-hours-and-check", "index.html:143 (rung-2 answer 2; n=6, a=2 count 29 recomputed by enumeration: numbers_r15.out) and project.html:207 'n = 6, a = 2: walks with maximum >= a: 29' agree; hours on project.html:272-281.")
P("SC1a-r10-hub-rung2-count", "index.html:143 and project.html:207 (29 for n=6, a=2) recomputed.")
P("SC1a-r7-forward-refs-L01-s4", "L01.html:215, :217 (section 4) refer only to Lesson 2 items and Remark 2.6, defined earlier in the course.")
P("SC1a-define-dyadic", "L01.html:132 defines dyadic partition (dfn); L02.html:71 and L03.html:55 link it (a href L01.html#def-dyadic-partition); anchor resolves.")
P("SC1a-r7-katex-render", f"page_smoke PASS for index, L01, L02, L03 (math rendered per the tool; {O}page_smoke_*.out).")
P("SC1a-r7-gate-check-projects", "`tools/check_projects.py --unit SC1`: 'check_projects SC1: PASS' rc=0 (r15 gates).")
P("SC1a-r10-cmd-check_projects", "Same command: check_projects SC1: PASS.")
P("SC1a-r8-links-anchors", "Internal href targets on index, L01-L03 resolve (scripted check this round: no missing #anchors or files); concept hash targets exist in course/concepts.html (1273 ids).")
P("SC1a-hub-cards-L01-L03", "index.html:152-154 cards match L01-L03 titles and content (Brownian motion, construction, quadratic variation).")
P("SC1a-hub-ladder-objectives", "index.html:163-171 ladder four rungs; :168 rung-2 text matches project.html:45 (completion problem, graded instantly).")
P("SC1a-hub-data-status", "index.html:37, :174-177: no real data; SIMULATED labels present in L02 and L03 labs.")
P("SC1a-dag-hub-prose", "index.html:33, :53, :150 prose consistent with check_dag PASS (all units).")
P("SC1a-hub-quiz-cross", "index.html:143 (rung 2 answer 2) and the explanation (paths ++ and +-) correct (numbers_r15.out: reach count 2).")
P("SC1a-r4-hub-quiz-keys", "index.html:72-145 quiz keys: Pq1..Pq8 and rung-2 numeric answered: correct options (grade T meaning, contradiction, int 1, E[X]=2, independence, completeness, martingale X_n, reflection tail 2P(B_t>=a), count 2).")
P("SC1a-hub-placement", "index.html:72-145: nine items (seven prerequisite, two skill checks), 80% bar = eight of nine: 7/9=77.8, 8/9=88.9 (numbers_r15.out).")
P("SC1a-hub-concept-list", "index.html:58-68 lists concepts from M1, M2, M4, M5, M6, P0.1; each link target exists in course/concepts.html (scripted check, 0 missing).")
P("SC1a-hub-prereq-chain", "index.html:35, :58-68 closure M1, M2, M4, M5, M6, P0.1; curriculum/01-foundations.yaml M6 prereqs [M4, M5] (:261-265) and chain read.")
P("SC1a-r10-hub-prereq-curriculum", "index.html:35, :58-68 vs curriculum/01-foundations.yaml:261-265 (M6 prereqs) and curriculum.json SC1 prereqs ['M6'] (read this round).")
P("SC1a-r10-hub-concept-count", "index.html:60 'eight concepts' = curriculum SC1 introduces (8 keys) = 8 dfn data-concept definitions in L01-L08 (grep this round).")
P("SC1a-r11-concept-list-exact", "index.html:58-68 vs curriculum.json SC1 introduces: brownian-motion, brownian-motion-construction, quadratic-variation, continuous-time-martingale, markov-property, reflection-principle, running-maximum-distribution, first-passage-time (exact match, read this round).")
P("SC1a-r8-lab-mutants-placeholder", "Mutant placement note: lab mutants live in ledgers/SC1/lab-mutants/ (mutate_graders reads ledgers/SC1/mutants/).")
P("SC1a-structure-L01-L03", "BUILDER_RULES 4.2 order checked on L01-L03 (read this round): why-it-matters 118/101/114 words (<=120); core sections; inline lab; canon breaks; misconceptions (3 each); problem set (3 per tier, worked solutions in details.solution); key-results table; quiz 10 items each (8-15); debate not required (curriculum SC1 has no debate key); check_pages PASS.")
P("SC1a-r9-hub-objective-reflection-proof", "index.html:54 objective 6 (Lesson 6, Theorem 2.5, A3 and A4) matches L06.html Theorem 2.5 (fixed-time identity) and Prop 2.3/2.7 assumptions.")
P("SC1a-r10-hub-ost-no-op", "placeholder")  # replaced below if present
del E["SC1a-r10-hub-ost-no-op"]
P("SC1a-r9-hub-reflection-assumptions", "index.html:33 lede now reads: fixed-time form (Theorem 2.5 of Lesson 6), path-level form (Proposition 2.7 of Lesson 6) under A3 and A4 of Lesson 5, finiteness proved in Lesson 8. L06.html:52, :119, :149 (Prop 2.7 path-level; Prop 2.3 fixed-time; Remark 2.4) and L06.html:332 ('Lesson 8 does') and L08.html:88 (Cor 1.4 under A3, A4) agree. Former FAIL cleared.")
P("SC1a-r10-hub-lede-path-level", "Same as SC1a-r9-hub-reflection-assumptions: index.html:33 now says path-level reflection is proved in Proposition 2.7 of Lesson 6 (L06.html:185-200 statement and proof), which matches L06.html:52, :119, :332. Former FAIL cleared.")
P("SC1a-r14-L01-keyresult-remark13-scope", "L01.html:351 now reads 'For 0<t_1<...<t_r' with the same hypotheses as Remark 1.3 (A1(a), A1(b)) at :102-107. Former FAIL cleared.")
P("SC1a-r14-L02-keyresult-lemma21-lambda", "L02.html:459 now reads 'for lambda >= 0 and a standard normal eta' with H1/H2 of Lemma 2.1 (:105-106). Former FAIL cleared.")
P("SC1a-r14-L03-keyresult-lemma22-mean", "L03.html:395 now reads 'normal with mean 0 and variance Delta>0' matching Lemma 2.2 (:90). Former FAIL cleared.")
P("SC1a-r14-cards-L01-L03-changed", "cards.json changes this delta: c044/c045 split into E[Z^4] only (c044, c045) plus new c236 (E[Z^2]) and c237 (Var(X^2)); each matches Lemma 2.1/2.2 (L03.html:77-96). No duplicate fronts (0).")
P("SC1a-r10-cards-dup-hypotheses", "cards.json L01-L03 (81 cards this pin): no duplicate ids or fronts; c044/c045 vs c236/c237 are distinct questions.")
P("SC1a-r11-cards-scan", "cards.json: all 81 L01-L03 cards read in full this round (223 cards in file; ids and fronts unique). Every card statement matches its lesson text.")
P("SC1a-r13-cards-L01-L03-read", "Same full read of the 81 L01-L03 cards this round (cards_r15.txt).")
P("SC1a-r10-cmd-check_pages", "tools/check_pages.py --unit SC1 PASS; --all rc=0 (r15 gates).")
P("SC1a-r10-cmd-check_dag", "tools/check_dag.py --all rc=0 (r15 gates).")
P("SC1a-r10-cmd-run_labs", "tools/run_labs.py --unit SC1: 11/11 PASS (r15 gates).")
P("SC1a-r10-cmd-page_smoke", "page_smoke PASS index, L01, L02, L03 individually (r15 gates).")
P("SC1a-r10-cmd-twins-python-I-W-error", "Twins run with python -I -W error: rc=0, empty stderr for L01, L02, L03 (twins_r15.out).")
P("SC1a-r10-cmd-verify_refs", "verify_refs offline 560 entries 0 problems; --unit SC1 1 of 560, 0 problems (r15 gates).")
F("SC1a-r10-cmd-ruff-mypy", f"ruff check . FAILS at pin; ruff format PASS (563 files); mypy --no-incremental PASS (385 files) ({O}ruff_check.out, {O}mypy_full.out).", RUFF_FIX)
P("SC1a-r10-cmd-pytest-SC1", "pytest -q -k SC1 tests: 11 passed; collect-only 11 (pytest_SC1*.out).")
P("SC1a-r11-twins-venv-314", "`.venv/bin/python -V` = Python 3.14.8 (CPython). Pyodide version not checked (see notes).")
P("SC1a-r7-gate-check-projects-unused", "placeholder")
del E["SC1a-r7-gate-check-projects-unused"]
P("SC1a-gate-check-projects-note", "placeholder")
del E["SC1a-gate-check-projects-note"]
P("SC1a-hub-hours-check", "placeholder")
del E["SC1a-hub-hours-check"]

P("SC1a-exercises-L01-L03", "Problem sets re-derived this round: L01 M1-M3, P1-P3, E1-E3, R1-R3 (L01.html:246-342 solutions checked: 1/3 and 1/3; 2 Var 5; 1/4 Cov; 3/64 pieces; symmetry); L02 M1-M3 (:354-372), P1-P3 (:379-398), E1-E3 (:404-422: 216 count, 0.2331787 and 0.832555), R1-R3 (:429-448); L03 M1-M3 (:289-309), P1-P3 (:315-334), E1-E3 (:340-359), R1-R3 (:365-384) all re-derived; no wrong solution found.")
P("SC1a-misconceptions-canon", "Misconception blocks read in full: L01.html:224-235 (three wrong statements corrected correctly), L02.html:332-343 (harmonic series block sums correct: partial sum >= 1+k/2; scale bookkeeping; f_n(t)=t^n), L03.html:268-279 (smooth vs BM, E|Z| sum sqrt(2Nt/pi), constant limit) all correct.")
P("SC1a-attrib-L02-eponym", "Grep for eponyms and bibliographic attributions in L01, L02, L03, index and twins (Wiener, Levy, Ciesielski, Schauder, Paley, Donsker, Kolmogorov, Karatzas, Shreve): only 'Chapman-Kolmogorov' (name of an identity, index.html:53, :156) and the registry-keyed Shreve reference (L03.html:491, index.html:182); no bibliographic claim attached. L02.html:7 meta description names no source.")
P("SC1a-r11-delta-read", "git diff 8e5751c d1e65a0 for index.html, L01.html, L02.html, L03.html, cards.json and tests/labs/SC1 read hunk by hunk this round (see SC1a-r15-delta-read); tests/labs/SC1 unchanged in the delta.")

# new rows
F("SC1a-r15-gate-ruff-check", RUFF_EV, RUFF_FIX)
P("SC1a-r15-lab-mutants-p1-p3", f"New student-error lab mutants written this round: p1 (L01 dyadic piece count doubled), p2 (L02 level scale 2^(-m/2)), p3 (L03 increment sd sqrt(H)/N). Each differs from its expected block: killed ({O}lab_mutants_r15.out).")
P("SC1a-r15-links-anchors-scripted", "Scripted check of every href and data-concept on index, L01-L03: 0 missing internal anchors/files, 0 external hrefs, 1273 concept ids present.")
P("SC1a-r15-delta-read", "git diff 8e5751c d1e65a0 for index.html (lede), L01.html (why-it-matters, canon item 4, Remark 1.3 misconception, key-results row, footer), L02.html (canon bullets, key-results row, footer), L03.html (key-results row), cards.json (c044, c045, c236, c237), curriculum/01-foundations.yaml and curriculum.json (M3 brief only; no SC1 effect): read hunk by hunk.")
P("SC1a-r15-counts", "Counts this round: 81 L01-L03 cards; 36 dyadic point-depth pairs; 216 dyadic cases; 16 z rows; 16 (H,N) exact cells; 9 hub quiz items; 13 lab mutants.")

rows = []
notes_extra = []
prev_ids = [r["id"] for r in prev["rows"]]
prev_map = {r["id"]: r for r in prev["rows"]}
for pr in prev["rows"]:
    i = pr["id"]
    if i not in E:
        raise SystemExit(f"no r15 decision for previous row {i}")
    e = E[i]
    row = {"id": i, "check": pr["check"], "location": pr["location"], "status": e[0], "evidence": e[1]}
    if e[0] != "PASS":
        row["fix"] = e[2]
    rows.append(row)
# new rows (not in previous fragment)
for i in ["SC1a-r15-gate-ruff-check", "SC1a-r15-lab-mutants-p1-p3", "SC1a-r15-links-anchors-scripted", "SC1a-r15-delta-read", "SC1a-r15-counts"]:
    e = E[i]
    loc = {"SC1a-r15-gate-ruff-check": "ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py:1",
           "SC1a-r15-lab-mutants-p1-p3": "ledgers/SC1/lab-mutants/SC1a-r15-lab-p1..p3",
           "SC1a-r15-links-anchors-scripted": "course/modules/SC/SC1/index.html, L01.html, L02.html, L03.html",
           "SC1a-r15-delta-read": "git diff 8e5751c d1e65a0 (slice-a files)",
           "SC1a-r15-counts": "course/modules/SC/SC1/index.html, L01-L03, cards.json"}[i]
    chk = {"SC1a-r15-gate-ruff-check": "2.5-ruff", "SC1a-r15-lab-mutants-p1-p3": "2.5-labs",
           "SC1a-r15-links-anchors-scripted": "2.9-structure", "SC1a-r15-delta-read": "2.9-delta",
           "SC1a-r15-counts": "2.2-numbers"}[i]
    row = {"id": i, "check": chk, "location": loc, "status": e[0], "evidence": e[1]}
    if e[0] != "PASS":
        row["fix"] = e[2]
    rows.append(row)

assert len(rows) == len({r["id"] for r in rows})
mutants = [
 {"id": "SC1a-lab-mut1-L01-cov-max", "description": "covariance sums increments up to max(i,j) instead of min(i,j)", "killed_by": "lab-SC1-L01-1 expected block"},
 {"id": "SC1a-lab-mut2-L02-scale", "description": "L02 level scale changed; bound and sup lines differ", "killed_by": "lab-SC1-L02-1 expected block"},
 {"id": "SC1a-lab-mut3-L03-closed-form", "description": "closed form for s^2 sums changed; closed-form column prints False", "killed_by": "lab-SC1-L03-1 expected block"},
 {"id": "SC1a-r13-lab-m1-L01-cov-max", "description": "covariance sums increments up to max(i,j); covariance line differs", "killed_by": "lab-SC1-L01-1 expected block"},
 {"id": "SC1a-r13-lab-m2-L02-hat-peak-half", "description": "hat peak 1/2 instead of 1; grid-sup line prints False", "killed_by": "lab-SC1-L02-1 expected block"},
 {"id": "SC1a-r13-lab-m3-L03-var-divisor-n", "description": "sample variance divides by n instead of n-1; z values change", "killed_by": "lab-SC1-L03-1 expected block"},
 {"id": "SC1a-r13-lab-m4-L03-closed-form-H3", "description": "closed form uses H cubed instead of H^4", "killed_by": "lab-SC1-L03-1 expected block"},
 {"id": "SC1a-r6-lab-mut1-L01-min-to-max", "description": "L01 covariance min replaced by max", "killed_by": "lab-SC1-L01-1 expected block"},
 {"id": "SC1a-r6-lab-mut2-L02-scale", "description": "L02 scale mutant (r6)", "killed_by": "lab-SC1-L02-1 expected block"},
 {"id": "SC1a-r6-lab-mut3-L03-closed-form", "description": "L03 closed-form mutant (r6)", "killed_by": "lab-SC1-L03-1 expected block"},
 {"id": "SC1a-r15-lab-p1-L01-dyadic-width-doubled", "description": "dyadic piece length t/2**(n+1): depth sums equal t/2, so the 15-of-15 line prints 0 of 15", "killed_by": "lab-SC1-L01-1 expected block"},
 {"id": "SC1a-r15-lab-p2-L02-level-scale-off-by-half-exponent", "description": "level scale 2**(-m/2) instead of 2**(-(m+1)/2) in the partial sum; bound and tail lines change", "killed_by": "lab-SC1-L02-1 expected block"},
 {"id": "SC1a-r15-lab-p3-L03-sd-taken-as-sqrt-horizon-over-steps", "description": "increment sd sqrt(H)/N instead of sqrt(H/N); means and z values change", "killed_by": "lab-SC1-L03-1 expected block"},
]

counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows:
    counts[r["status"]] += 1
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
frag = {
  "unit": "SC1", "slice": "a", "round": 15,
  "verifier": "Haiku independent verifier, SC1-a round 15 (did not build SC1)",
  "pin": "d1e65a0203e386e3246429ba1cf7e723eb6cfbfa",
  "base": "8e5751c903f0246115eba746afdf5d71f612bb37 (round-14 pin; round-14 fragment /Users/billyribeiro/.fanout/frags/E-SC1-a.round14.json used as context only)",
  "checkout": "/Users/billyribeiro/.fanout/wt/verifyE15-SC1-a (detached at d1e65a0; the checkout was found at 9ca1d8cb and moved to the pin; .venv symlinked)",
  "scratch": "none used for evidence; all scripts under ledgers/SC1/scripts/SC1-a-r15/",
  "verified_at": "2026-11-08T00:00:00+00:00",
  "verdict": verdict,
  "rows": rows,
  "mutants": mutants,
  "registry_flags": ["Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) is the second source the curriculum lists for SC1 (curriculum/03-markets.yaml); no registry record (grep -c -i karatzas references/references.json = 0). Not cited by the unit, so no request is needed unless the architect wants it cited."],
  "freshness_flags": [],
  "notes": "ROUND 15 at d1e65a0. Full read this round: index.html (190 lines), L01.html (446), L02.html (560), L03.html (504), twins, cards.json L01-L03 (81 cards), and the slice-a delta since 8e5751c. No row was carried: the subject files changed (index.html, L01-L03, cards.json) so every row was re-verified. The round-14 FAIL rows (SC1a-r9-hub-reflection-assumptions, SC1a-r10-hub-lede-path-level, SC1a-r14-L01/L02/L03-keyresult-*) are now PASS. FAIL rows this round are gate/bookkeeping only: ruff check fails at this pin on a verifier-written lab-mutant file (fixed in aeb512b6, which is after the pin), and the round-14 mutant files are absent. No unit-content defect was found in index.html, L01-L03, the twins or the cards. Lab twins are demonstrations, so grader mutation (tools/mutate_graders.py) does not apply to this slice; lab mutants are in ledgers/SC1/lab-mutants/ (mutate_graders reads ledgers/SC1/mutants/). Not checked: L04-L08 prose and the grader/project (other slices); the Pyodide interpreter version (page_smoke reports timings only); the Shreve book (no passage is cited); the curriculum renderer and build_site --check (not in this slice's gate list; program.json and curriculum.json changed only in the M3 brief).",
  "summary": {
    "text": f"SC1-a round 15 at d1e65a0: verdict {verdict}. {len(rows)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: SC1a-gate-lint-types-tests, SC1a-r10-cmd-ruff-mypy, SC1a-r15-gate-ruff-check (ruff E501 on ledgers/SC1/lab-mutants/SC1a-r13-lab-m1-L01-cov-max.py:1 at this pin); SC1a-r14-lab-mutants-new3 (UNVERIFIABLE: files absent at pin).",
    "counts": counts,
    "mutants": f"{len(mutants)} of {len(mutants)} lab mutants killed (3 new this round)",
  },
}
out = root + "/ledgers/SC1/SC1-a.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
open(out, "a", encoding="utf-8").write("\n")
print("wrote", out, "rows", len(rows), counts, verdict)
