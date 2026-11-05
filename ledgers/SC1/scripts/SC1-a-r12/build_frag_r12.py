"""Builds ledgers/SC1/SC1-a.json (round 12, slice a) from the verifier's checks. Every row's evidence cites a script
or file under ledgers/SC1/scripts/SC1-a-r12/ or a file and line of the slice. Usage: python -I build_frag_r12.py <checkout>"""
import datetime
import json
import sys

root = sys.argv[1]
S = "ledgers/SC1/scripts/SC1-a-r12/"
G = "course/modules/SC/SC1/"
PIN = "5db69a9bee460736c318ebfacc7200ee5a6eb0f0"
BASE = "11d7077a290f7960b183d3a5a6631af4773888f9"

def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

R = []
R.append(row("SC1a-gate-check-pages", "2.9-structure-tool", "index.html, L01.html, L02.html, L03.html, cards.json", "PASS",
    f"Round 12 at 5db69a9: `.venv/bin/python tools/check_pages.py --unit SC1` -> 'check_pages SC1: PASS', exit 0 ({S}check_pages_SC1.out)."))
R.append(row("SC1a-gate-check-dag", "2.9-dag-tool", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"`tools/check_dag.py --unit SC1` -> 'check_dag SC1: PASS' ({S}check_dag_SC1.out); `tools/check_dag.py --all` exit 0, every unit PASS ({S}check_dag_all.out)."))
R.append(row("SC1a-gate-run-labs", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    f"`tools/run_labs.py --unit SC1` -> 'run_labs SC1: PASS (11/11)', exit 0 ({S}run_labs_SC1.out)."))
R.append(row("SC1a-gate-page-smoke", "2.9-page-smoke", "index.html, L01.html, L02.html, L03.html", "PASS",
    f"`tools/page_smoke.py --unit SC1 --pages <page>` run alone for index, L01, L02, L03: each 'page_smoke SC1: PASS', exit 0 ({S}page_smoke_index.out, page_smoke_L01.out, page_smoke_L02.out, page_smoke_L03.out). Lab timings 0.0 s, 0.2 s, 0.1 s."))
R.append(row("SC1a-gate-lint-types-tests", "2.5-ruff-mypy-pytest", "tests/labs/SC1/*; pytest -k SC1", "PASS",
    f"`ruff check tests/labs/SC1 tests/test_labs.py` 'All checks passed!'; `ruff format --check` '12 files already formatted'; project-wide `ruff check .` and `ruff format --check .` pass ({S}ruff.out, ruff_full.out). `mypy --no-incremental` on the three twins: 'Success' ({S}mypy_twins.out); full project: 'Success: no issues found in 385 source files' ({S}mypy_full.out). `pytest -q -k SC1`: 11 passed, exit 0 ({S}pytest_SC1.out; collect-only 11 in {S}pytest_SC1_collect.out)."))
R.append(row("SC1a-gate-verify-refs", "2.1-citations", G + "index.html:182 (data-cite shreve2004stochastic)", "PASS",
    f"`tools/verify_refs.py --offline`: 'offline integrity: 560 entries, 0 problems', exit 0 ({S}verify_refs_offline.out). `tools/verify_refs.py --unit SC1` (live Crossref): 'live re-verification of SC1: 1 of 560 entries, 0 problems', exit 0 ({S}verify_refs_live_SC1.out)."))
R.append(row("SC1a-lab-L01-twin", "2.5-lab-L01", "tests/labs/SC1/lab-SC1-L01-1.py; " + G + "L01.html:137-208", "PASS",
    f"{S}lab_page_vs_twin_r12.py: page code equals twin (True), expected block equals twin stdout (True), exit 0, stderr empty, run as `python -I -W error` from an empty scratch directory ({S}lab_page_vs_twin_r12.out). Venv CPython 3.14.8 ({S}twin_venv_L01.out)."))
R.append(row("SC1a-lab-L02-twin", "2.5-lab-L02", "tests/labs/SC1/lab-SC1-L02-1.py; " + G + "L02.html:168-279", "PASS",
    f"Same script: page code = twin, expected = stdout, exit 0, stderr empty ({S}lab_page_vs_twin_r12.out); venv run ({S}twin_venv_L02.out)."))
R.append(row("SC1a-lab-L03-twin", "2.5-lab-L03", "tests/labs/SC1/lab-SC1-L03-1.py; " + G + "L03.html:131-252", "PASS",
    f"Same script: page code = twin, expected = stdout, exit 0, stderr empty ({S}lab_page_vs_twin_r12.out); venv run ({S}twin_venv_L03.out)."))
R.append(row("SC1a-lab-claims-L01", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L01-1.py:1-9 (docstring, shown at L01.html:137-145); L01.html:136 and :208", "PASS",
    f"Output (twin_venv_L01.out): 'dyadic variance sums equal t: 15 of 15 cases', 'Cov(B at 1/4, B at 5/8) = 1/4', '81 of 81 pairs'. Hypothesis (L01.html:136) gives the same counts (15 of 15, 81 of 81, exact Fractions); the docstring says nothing is random and no path is simulated, and the code uses only Fraction arithmetic (docstring L01.html:141-144; functions L01.html:156-172, identical to the twin)."))
R.append(row("SC1a-lab-claims-L03", "2.5-lab-claims", G + "L03.html:133 (hypothesis), :253 (interpretation), :343 (E1)", "PASS",
    f"Hypothesis: SE = H sqrt(2/N)/20 and Var(Q)=2H^2/N, 400 paths, z within +-3; output max |z| = 2.39 (H=1,N=2), all |z| <= 3 ({S}l03_numbers_r12.out). Interpretation claims 'no other |z| exceeds 1.84': second largest |z| = 1.8439 (H=1,N=128), confirmed. Interpretation says theoretical SE at H=1,N=1 is sqrt(2)/20 = 0.0707 (computed 0.070711), printed 0.0718 (correct); H=2,N=128 theory 0.0125 vs printed 0.0125 (correct)."))
R.append(row("SC1a-lab-L02-docstring", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L02-1.py:1-8 (docstring, shown at L02.html:171-178)", "PASS",
    f"Docstring: 'The dyadic count and the grid-supremum line are identities that hold for every seed'. Tested for seeds 0-299 and the production seed: no failures ({S}l02_identities_seeds_r12.out). 'Numbers are printed to six decimal places from unrounded values': code prints with .6f format calls on unrounded floats in main() (twin, identical to L02.html:170-278 code)."))
R.append(row("SC1a-r4-seed-sweep-L02", "2.5-lab-seed", "tests/labs/SC1/lab-SC1-L02-1.py; " + G + "L02.html:170 (SIMULATED claim)", "PASS",
    f"Same seed sweep ({S}l02_identities_seeds_r12.out): the 216-case count and the grid-supremum identity hold for all 301 seeds, so the 'for every seed' wording of the docstring is supported. The bound lines are sample quantities and the page says so (L02.html:170, :278)."))
R.append(row("SC1a-numbers-L01", "2.2-numbers", G + "L01.html:132, :230, :298, :305, :348-352, :393, :398, :412, :426", "PASS",
    "Recomputed by hand and checked: (3/4)/16=3/64 and 16*3/64=3/4 (E1, L01.html:299); Cov(B_{1/4},B_{5/8}) = 2*(1/8) = 1/4 (E2, :306); sd of B_{1/4}-B_0 = 1/2 (quiz, :394); ratio 1/sqrt(1/100)=10 (:399); Var(3B_1-B_2)=9+2-6=5 (:413); E[B_3^2]=3 (:427); 1/100 -> sd 1/10 is ten times h (:230)."))
R.append(row("SC1a-numbers-L02", "2.2-numbers", G + "L02.html:268-277 (printed block), :278 (interpretation), :405-407 (E1), :411-414 (E2), :419-421 (E3)", "PASS",
    f"Independent recomputation ({S}l02_bounds_r12.out): observed sups 0.116589, 0.731080, 0.229982, 0.327612, 0.252987, 0.198455, 0.156208, 0.128716 and bounds 0.832555, 0.832555, 0.721013, 0.588705, 0.465412, 0.360507, 0.275342, 0.208139 match the printed block exactly; sum of bounds for levels 5-8 = 1.309399 matches. The 216 count recomputed (E2: 2*9+3*8+5*7+9*6+17*5=216). The grid-supremum |Sigma_8-Sigma_4| = 0.348139 is the twin's own printed output (matched by run_labs/lab_page_vs_twin), not re-derived here."))
R.append(row("SC1a-numbers-L03", "2.2-numbers", G + "L03.html:253, :270, :275, :343, :350, :357, :368, :375, :398, :434", "PASS",
    f"All 16 (mean, se, z) cells recomputed from the twin's own seeded functions ({S}l03_numbers_r12.out); exact sums H^4(4N^2-1)/(3N^3): H=2,N=8 -> 16*255/1536 = 2.65625 (E2 :350); H=2,N=128 -> 0.166664 (:270); H=1,N=2 -> 15/24 = 0.625 (quiz :434); H=2,N=128 SE 2*sqrt(2/128)/20 = 0.0125 (E3 :357)."))
R.append(row("SC1a-numbers-L02-36-points", "2.2-numbers", G + "L02.html:278 (interpretation); :411-414 (E2)", "PASS",
    "Points per depth 2, 3, 5, 9, 17 for depths 0-4 (2^n+1): 36 (depth, point) pairs (sum 36); 17 distinct points (2^4+1) (script output in " + S + "l02_identities_seeds_r12.out is the case count 216 for each seed). Interpretation statement correct."))
R.append(row("SC1a-numbers-L03-SE-follow", "2.2-numbers", G + "L03.html:398 (key-results row, grade C)", "PASS",
    f"Gap = printed-or-unrounded se / (H sqrt(2/N)/20) - 1 over all 16 cells ({S}l03_numbers_r12.out): max |gap| 13.218% at (H=2,N=1); printed 4dp values give 13.208% at the same cell. Both round to 13.2 percent. 'Within 14 percent in absolute value': all 16 |gap| < 14% (True). Grade C with 'Lab 1 (SIMULATED)' basis is consistent with FINAL-ARCHITECT-RULINGS item 13."))
R.append(row("SC1a-grade-L01", "2.3-grades", G + "L01.html:83, :101, :119, :349-353", "PASS",
    "Re-graded by BLUEPRINT §3: Proposition 1.2 (proof at :92-99), Remark 1.3 (proof at :110-113) and Example 1.4 (proof at :127-129) are T with the proof on the page; the Lab 1 result is not graded in prose (:208 says it adds no evidence beyond the proof); key-results rows T with 'Proved in' sources. No grade over-claim found."))
R.append(row("SC1a-grade-L02", "2.3-grades", G + "L02.html:74 (Lemma 2.2), :103 (Lemma 2.1), :121 (Lemma 2.3), :145 (Proposition 2.4), :288 (Theorem 2.5), :302 (Remark 2.6)", "PASS",
    "Each T has a complete proof on the page or is conditional on a named assumption (Lemma 2.1 on Assumption 2.1(a); Lemma 2.3 on A1(a),(b),(c),(e); Proposition 2.4 on Assumption 2.1; Theorem 2.5 on A2 and Assumption 2.1; Remark 2.6 on A1(a),(b),(e), A2, Assumption 2.1). A2 is labelled 'Sketch, not a proof' (:285). Grades correct; the Lemma 2.3 proof gap is a separate FAIL row."))
R.append(row("SC1a-grade-L03", "2.3-grades", G + "L03.html:77, :90, :99, :118, :394-398", "PASS",
    "Lemma 2.1 and 2.2 T (proofs :83-95); Theorem 2.3 T under Assumptions 3.1 and 3.2 (proof :107-113); Proposition 2.4 T (proof :125-129); the lab-based key-results row is C with basis 'Lab 1 (SIMULATED)' (:398). Matches BLUEPRINT §3 and FINAL-ARCHITECT-RULINGS item 13."))
R.append(row("SC1a-hub-grade-definition", "2.3-grades", G + "index.html:79; BLUEPRINT.md §3 (table)", "PASS",
    "index.html:79 quiz item 1 defines T as 'A theorem, proved on the page or with a precisely cited proof', which matches the BLUEPRINT §3 T row."))
R.append(row("SC1a-math-L01-prop1.2", "2.4-math", G + "L01.html:84-98 (Proposition 1.2 and proof)", "PASS",
    "Re-derived each step: s=t via (D1),(D2); X=B_s, Y=B_t-B_s independent by (D3) with t_0=0,t_1=s,t_2=t; E X^2=s, E Y^2=t-s, |XY|<=(X^2+Y^2)/2 integrable; E[XY]=EX EY=0 by A1(a); Cov(B_s,B_t)=E X^2 + E[XY] = s. Hypotheses (H1),(H2) match use."))
R.append(row("SC1a-math-L01-remark1.3", "2.4-math", G + "L01.html:75 (A1(b)), :102-113", "PASS",
    "Fixed from round 11 (row SC1a-r11-A1b-literal-false). The proof (:112) now applies A1(b) to coordinates that are combinations of the one family Delta_1..Delta_r, which are independent normals (D3 and D2). The A1(b) sentence, as now stated, is true: a vector X = AZ + b with Z a vector of independent normals is multivariate normal (Z is jointly Gaussian; linear images of Gaussian vectors are Gaussian). Mean 0 and covariance min(t_i,t_j) by Proposition 1.2. PASS."))
R.append(row("SC1a-math-L01-canon-construction", "2.4-math", G + "L01.html:215 (canon item 1)", "PASS",
    "Re-derived: U(omega,u)=u uniform and independent of B on the product space (the sigma(B)-events are A x (0,1); P((A x (0,1)) cap (Omega x C)) = P(A)Leb(C)); tilde B_t = B_t + 1{t=U}; tilde B_0 = 0 since U in (0,1); P(U in G)=0 for finite G so the finite-dimensional laws agree; tilde B_U = B_U + 1, so discontinuous at U on every outcome. Assumptions named (A1(a),(b),(e), A2, Assumption 2.1, Remark 2.6)."))
R.append(row("SC1a-math-L02-lemmas-2.1-2.2", "2.4-math", G + "L02.html:73-117", "PASS",
    "Lemma 2.2 (a)-(e) re-derived (breakpoints at multiples of 2^-m; disjoint supports; Lambda_{m,j}(k2^-n)=0 for n<m by the odd-integer distance argument; Sigma_M = Sigma_n at level-n points; linearity). Lemma 2.1: E e^{theta eta}=e^{theta^2/2} by completing the square; Markov/Chernoff bound with theta=lambda; symmetry gives factor 2. Assumption 2.1(a) used for monotone expectation. PASS."))
R.append(row("SC1a-math-L02-lemma2.3-arithmetic", "2.4-math", G + "L02.html:121-141 (Lemma 2.3, proof :132-139)", "FAIL",
    "Re-derived. Fixed since round 11: H2 now lists A1(a) (:124); the variance of U_j (:137) uses Cov(D_j,eta_j)=0 by A1(a) and the Cov(U_j,V_j)=0 step (:138) is correct (cross terms cancel: 1/2*(-c)+c*1/2=0). OPEN GAP: the Consequence paragraph (:139) says 'By A1(b), each sum is normal with variance 2^{-N} times the number of its level-N increments, which is t_i-t_{i-1}'. A1(b) (:75) gives normality only; it says nothing about variance. The variance of a sum of independent summands is the sum of their variances (Var(X+Y)=VarX+VarY+2Cov, Cov=0 by A1(a)), and that step is not stated. The same step is written out in Remark 2.6 (:315: 'By A1(a) the variance of the sum is the sum of the variances'), so the omission is local. Lemma 2.3's second claim (the law N(0,t_i-t_{i-1})) therefore rests on an unstated step. Round 11 row (i) 'variance additivity ... Var of each dyadic sum (L02.html:139)' is still open.",
    "At L02.html:139, after 'By A1(b), each sum is normal', add: 'By A1(a), the summands are integrable and pairwise independent, so their covariances vanish and the variance of the sum is the sum of the level-N variances, 2^{-N} times the number of its level-N increments, which is t_i - t_{i-1}.' Keep the grade T and the H2 list (which already includes A1(a))."))
R.append(row("SC1a-math-L02-prop2.4", "2.4-math", G + "L02.html:145-165", "PASS",
    "Re-derived: P(E_m^c) <= 2^{m-1}*2e^{-lambda_m^2/2} = 2^{m-1}*2*4^{-m} = 2^{-m} (since lambda_m^2/2 = 2m log 2); P(A_{m0}^c) <= 2^{1-m0}; continuity from below; M_m = lambda_m 2^{-(m+1)/2} = sqrt(2 log 2) sqrt(m) 2^{-m/2} (max abs difference 1e-16, " + S + "l02_bounds_r12.out); sum m r^m = r/(1-r)^2 with r=2^{-1/2}; Weierstrass-type Cauchy step; continuity by eps/3. All steps valid."))
R.append(row("SC1a-math-L02-A2-sketch", "2.4-math", G + "L02.html:281-286", "PASS",
    "Labelled 'Sketch, not a proof'; names the skipped step (passage of characteristic functions to the limit on Omega*, and the joint version). Characteristic function of N(0,v) is e^{-u^2 v/2} (correct). The claim that the dyadic increments have these laws is Lemma 2.3 (PASS as a sketch)."))
R.append(row("SC1a-math-L02-thm2.5", "2.4-math", G + "L02.html:288-300", "PASS",
    "Proof re-derived: finite-dimensional laws of B equal those of Sigma (Prop 2.4(a)); B_0 = 0 via Lambda_{m,j}(0)=0 (P2, L02.html:389); (D2),(D3) from A2 on Omega*; continuity from Prop 2.4(b) on Omega* and identically zero off it. Conditional T with the assumptions named (A2, Assumption 2.1)."))
R.append(row("SC1a-math-L03-thm2.3", "2.4-math", G + "L03.html:99-115", "PASS",
    "Re-derived: E Q = sum Delta_k = t; U_k = X_k^2 independent (3.2(a)); Var(U_k)=2 Delta_k^2 (Lemma 2.2); Var(Q)=sum Var(U_k) (3.2(b)); E(Q-t)^2 = 2 sum Delta_k^2 <= 2 t |P| using sum Delta^2 <= max Delta * sum Delta = |P| t; mesh to zero under 3.1. Statement 'Assuming also Assumption 3.1' (:104) matches. PASS."))
R.append(row("SC1a-math-L03-prop2.4", "2.4-math", G + "L03.html:117-129", "PASS",
    "(a): (b^2-a^2)^2 = (b-a)^2 (b+a)^2 <= 4H^2 (b-a)^2, summed with sum Delta^2 <= |P| H gives 4H^3|P|. (b): t_{j+1}^2 - t_j^2 = H^2(2j+1)/N^2; S(N)=sum (2j+1)^2 = N(4N^2-1)/3 by induction (checked: (2N+1)(N+1)(2N+3)/3 both ways); sum = H^4 S(N)/N^4 = H^4(4N^2-1)/(3N^3). Numeric: H=2,N=8 -> 2.65625; H=1,N=2 -> 0.625 (lab output, " + S + "lab_page_vs_twin_r12.out)."))
R.append(row("SC1a-math-L03-misc-claims", "2.4-math", G + "L03.html:259-261, :270, :274-279, :366-382", "PASS",
    "Canon item 1 (fourth-moment bound: Var(X^2) <= E X^4 <= c Delta^2, so E(Q-t)^2 <= c t|P|) re-derived; canon item 2 (single variable X_N: Var Q = N^2 * 2 (t/N)^2 = 2t^2) re-derived; misconception: E|Z| = 2 phi(0) = sqrt(2/pi), expected sum sqrt(2Nt/pi); R1 = 2t^2/N, R2 (c=2 is least: equal partition gives exactly 2t|P|), R3 (Var Q = 2t^2) re-derived. All PASS."))
R.append(row("SC1a-math-L03-density", "2.4-math", G + "L03.html:78 (Lemma 2.1 density), :332 (P3)", "PASS",
    "Numeric: 2*phi(0) = 2/sqrt(2 pi) = 0.7978845608 = sqrt(2/pi) (checked). Integration by parts boundary term 2R^3 phi(R) -> 0. P3 solution: integral of z phi from 0 to R = phi(0) - phi(R). PASS."))
R.append(row("SC1a-grade-L02-remark2.6", "2.4-math", G + "L02.html:302-318", "PASS",
    "Re-derived: W_t = sum_{j<k} B^(j)_1 + B^(k)_{t-k} on [k,k+1]; continuous at integers since B^(k+1)_0 = 0; (D2) from one-piece-per-unit-interval and A1(b) (normal) with A1(a) for the variance; (D3) from refinement, H1 (independent copies), and A1(e) grouping. Remark conditional on the named assumptions (A1(a),(b),(e), A2, Assumption 2.1)."))
R.append(row("SC1a-math-L02-thm2.5-extension", "2.4-math", G + "L02.html:314 (refinement paragraph)", "PASS",
    "Each unit interval (k,k+1] meets the refined set in exactly one piece, so the pieces of W_t - W_s come from distinct copies (the claim at :314). Adding every integer in [s0,sq] makes this hold for the refined set. PASS."))
R.append(row("SC1a-exercises-L01-L03", "2.4-problems", G + "L01.html:246-427; L02.html:351-520; L03.html:289-385", "PASS",
    "Every problem solution re-derived: L01 M1-M3 (1/3,1/3; Cov 0, t-s; 5), P1-P3, E1-E3 (3/64, 1/4, 81 pairs), R1-R3; L02 M1 (hat values 0,1,0), M2 (xi_0/2 + xi_11/2), M3 (Var U_1 = 1/4), P1-P3, E1-E3 (216; level-1 values checked in " + S + "e3_l02_numbers_r12.out), R1-R3; L03 M1 (E Q = 1, Var Q = 1), M2 (48, 32), M3 (1/N -> 0), P1-P3, E1-E3, R1-R3. Each solution cites a named result. No arithmetic error found."))
R.append(row("SC1a-misconceptions-canon", "2.4-canon", G + "L01.html:219-237; L02.html:329-345; L03.html:265-281", "PASS",
    "L01: independence misconception (Cov = 1/2 for s=1/2,t=1; correct under A1(a)); sd misconception (1/10 vs 1/100); fixed-path misconception. L02: harmonic series partial sums >= 1 + k/2 (blocks of size 2^{i-1} each >= 1/2); coefficient-scale misconception (variance of U_j correct only at c^2=2^{-(n+2)}); pointwise limit t^n. L03: smooth-function sums <= 4H^3|P|; absolute-variation expectation sqrt(2Nt/pi); random-number misconception. All refutations correct."))
R.append(row("SC1a-canon-breaks-ungraded", "2.3-grades", G + "L02.html:319-327; L01.html:215-217; L03.html:259-261", "PASS",
    "Items name hypotheses whose failure changes the conclusion, and each comes with a counterexample or a derivation on the page (L01 §4 items 1-3; L02 f_n(t)=t^n; L03 single-variable example). No ungraded numeric claim is left without a basis."))
R.append(row("SC1a-notation-macros", "2.4-notation", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    "Macros in slice math (grep of \\(...\\) and \\[...\\]): \\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic, all registered in notation/notation.json. Other commands are standard LaTeX (Greek letters, \\mathcal{F}, \\mathrm{Leb}, \\operatorname{Bor}, \\mathbb{Z}, \\max, \\min, \\lfloor), used on the same convention as the other PASS pages (not registry symbols). Flagged here for the architect; not a FAIL under the convention in use."))
R.append(row("SC1a-notation-no-registered-collision", "2.4-notation", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    "No use of registered symbols with a different meaning: no \\Phi, \\gamma_3, \\gamma_4, \\mathbb{Q}, R^{e\\ast}, R_f; R^\\ast does not occur (the slice writes Omega^\\ast, a different symbol). grep of the four slice pages: 'ast' occurrences are Omega^\\ast only (L02.html:148, 151, 158, 283-299, 437, 461)."))
R.append(row("SC1a-notation-T-subscript", "2.4-notation", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    "The registered symbol T (number of return observations) is not used as a horizon or time in the slice: the only occurrence of the letter T in math is in prose at L03.html:120 ('the program's notation reserves T ...'). Horizon is H (L03). PASS."))
R.append(row("SC1a-notation-H-horizon", "2.4-notation", G + "L03.html:120, :122, :128, :133; tests/labs/SC1/lab-SC1-L03-1.py", "PASS",
    "H is the horizon in L03 Proposition 2.4 and the lab (HORIZONS=(1.0, 2.0), EXACT_HORIZONS). H is not a registered symbol, so no collision. The statement at L03.html:120 about T is accurate per notation/notation.json symbols array (T = number of return observations)."))
R.append(row("SC1a-r4-notation-S-symbol-L02", "2.4-notation", G + "L02.html:67-68, 126, 132-134, 139, 151, 163-165, 282, 296", "PASS",
    "The sum process is written Sigma_M / Sigma (local symbol, defined at :67-68); no S_n symbol in L02; no collision with a registered symbol (registry has no Sigma or Sigma_n)."))
R.append(row("SC1a-r4-thm23-counterexample-L03", "2.4-math", G + "L03.html:382 (R3 solution)", "PASS",
    "R3 names (H1) as the failing hypothesis (increments not independent, so not standard BM) and says (H2) does not apply because Assumption 3.2 is stated for independent variables. Consistent with Theorem 2.3 at L03.html:99-103."))
R.append(row("SC1a-process-words", "2.9-prose", G + "index.html, L01.html, L02.html, L03.html; lab twins L01-L03", "PASS",
    "grep of learner-visible text (tags stripped) for builder, verifier, round, fixer, planner, architect, ruling, REQUESTS, unit report, Q<n>, DAG_DEFECT: no hits ({S}slice_mech_r12.out). Twin docstrings checked by reading (lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py)."))
R.append(row("SC1a-banned-phrases", "2.9-prose", G + "index.html, L01.html, L02.html, L03.html; lab twins", "PASS",
    "grep for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, and ellipses: 0 hits in all four pages ({S}slice_mech_r12.out); no hits in the three twins (grep)."))
R.append(row("SC1a-structure-L01-L03", "2.9-structure", G + "L01.html, L02.html, L03.html", "PASS",
    f"check_pages PASS ({S}check_pages_SC1.out). Section order re-read in each lesson (why-it-matters, core, inline lab, canon-breaks, misconceptions, problem set, key results, quiz, references). why-it-matters word counts (script, {S}slice_mech_r12.out): L01 115, L02 101, L03 120 (all at most 120). Problems: at least three in each tier, each with a solution in details.solution; quiz items: 10, 10, 10 (each with explain). data-hours 9, 9, 9."))
R.append(row("SC1a-scope-words-L02-L03", "2.4-scope", G + "L02.html:122, :139, :158, :263, :316, :385, :417; L03.html:85, :104, :133, :253, :270", "PASS",
    "Scope words read in context. L02 'every outcome' statements are backed by Prop 2.4 (Omega*, :151) and Theorem 2.5 (:294); 'every finite set of times' (A2, :283) is the stated assumption, and Lemma 2.3 proves the dyadic case only; 'for every n' (Lemma 2.3 :126) is proved by induction (:131-139). L03 'for every N' (:104, :133) is backed by the closed form (Prop 2.4(b)) for the exact sums, and the 400-path run is only a sample (the page says so at :253). No unsupported scope word found."))
R.append(row("SC1a-scope-L01-prop1.2-only", "2.4-scope", G + "L01.html:216 (canon-break 2)", "PASS",
    "Canon item 2 claims only that the path-continuity event is not a function of the finite-dimensional laws; it is derived from the item-1 construction (B continuous on every outcome; tilde B on no outcome). Scope limited to that example. PASS."))
R.append(row("SC1a-ref-L01-every-result", "2.1-citations", G + "L01.html:434", "PASS",
    "L01 references section: 'This lesson cites no registry source. Each result is proved on this page from Definition 1.1 and, where it says so, from Assumption A1' and names Remark 2.6 of Lesson 2 as the one result from another lesson. Every L01 result is proved or named as an assumption (grade table and proofs read)."))
R.append(row("SC1a-r4-cauchy-schwarz-L01", "2.4-assumptions", G + "L01.html:95; index.html:69 (promise)", "PASS",
    "Integrability in the proof of Proposition 1.2 is shown by |XY| <= (X^2+Y^2)/2 (elementary), not by Cauchy-Schwarz; the step is complete. The hub promise at index.html:69 is evaluated under the separate row SC1a-hub-assumption-promise."))
R.append(row("SC1a-hub-assumption-promise", "2.4-assumptions", "index.html:69 (promise), :184; L01.html:72-80 (A1); L02.html:92-99 (Assumption 2.1); L03.html:70-71 (Assumption 3.2)", "FAIL",
    "The hub promise (index.html:69): a standard fact of a prerequisite that the page does not prove is stated as a numbered Assumption 'with the prerequisite it comes from, or, for a standard fact that the lesson cites to no source, labelled as such (Lesson 1, A1)'. Lesson 1 A1 now complies (:72 standard facts, stated without proof; :80 cites no source); Assumption 2.1 names M5 and M6 (:93). Assumption 3.2 (L03.html:70-71: 'independence and additivity of variance') states standard facts about independent variables and the variance of sums, which L03 'Uses' attributes to M4 (L03.html:37), but it names no prerequisite and does not say that it cites no source. The promise is not met for Assumption 3.2.",
    "At L03.html:71 add the source of the facts, as Assumption 2.1 does: 'The page does not prove these facts. They are facts of M4 (independence and variance).' (or the label 'standard facts, cites no source' used by Lesson 1 A1). Then keep index.html:69 as written."))
R.append(row("SC1a-attrib-L01-A1-parts", "2.4-assumptions", G + "L01.html:37, :72-80", "PASS",
    "Each part of A1 is a standard fact and is stated without attribution: (a) product rule for independent integrable variables; (b) corrected this round, now true (see SC1a-r11-A1b-literal-false); (c) uncorrelated jointly normal coordinates are independent (true); (d) pointwise limits on a measurable event are measurable (true); (e) grouping of independent families (true). No registry key, locator or theorem number is attached."))
R.append(row("SC1a-assump-L01-P3", "2.4-assumptions", G + "L01.html:285-287", "PASS",
    "P3 (covariance for s>t) uses A1(a) through Proposition 1.2 and symmetry of Cov; the solution names the property used. Consistent."))
R.append(row("SC1a-assump-L02-grouping", "2.4-assumptions", G + "L02.html:106, :116, :138", "PASS",
    "Lemma 2.1 (H2) 'Assuming Assumption 2.1(a)' (:106) and its use (:116); the grouping facts used in the Lemma 2.3 step are A1(e) (:138), named. The variance step in the Consequence (:139) is the separate FAIL row SC1a-math-L02-lemma2.3-arithmetic."))
R.append(row("SC1a-attrib-L02-lemma2.1-union", "2.4-attribution", G + "L02.html:97 (Assumption 2.1(c)), :158 (union bound in Proposition 2.4(a))", "PASS",
    "Assumption 2.1(c) states the countable union bound and continuity from below; Proposition 2.4(a) uses both (:158). Attribution is to the Assumption, not to a source. PASS."))
R.append(row("SC1a-attrib-L02-eponym", "2.1-citations", G + "L02.html:7 (meta description); tests/labs/SC1/lab-SC1-L02-1.py:1-8", "PASS",
    "grep of index.html, L01-L03 and the L02 twin for eponyms and attribution words (Levy, Ciesielski, Schauder, Wiener, Donsker, Bachelier, Einstein, Karatzas, Shreve): none in the slice text (L02 uses 'hat function' and no eponym). Shreve appears only as the curriculum source with its key (L03.html:491). PASS."))
R.append(row("SC1a-reference-section-L02-L03", "2.1-citations", G + "L02.html:547; L03.html:491; L01.html:434", "PASS",
    "L02: 'This lesson cites no registry source'; L03: 'cites no passage from a registry source' and states the curriculum source with key shreve2004stochastic at book level, no locator. The only registry key in the slice is shreve2004stochastic (index.html:182; references.json key verified live this round)."))
R.append(row("SC1a-hub-hours", "2.9-hours", G + "index.html:29, :39-42, :150; project.html:272-280", "PASS",
    "index.html data-hours-lessons=72, data-hours-project=28; 72 + 28 = 100 (curriculum 100 h, curriculum/03-markets.yaml:508); project 28 percent of 100 (10-40 percent rule). Project table rows 2+3+10+8+3+2 = 28 (project.html:272-280). Eight lessons at 9 h each = 72 (L01-L03 data-hours 9; L04-L08 data-hours 9 per grep)."))
R.append(row("SC1a-hub-placement", "2.9-structure", G + "index.html:72-145", "PASS",
    "Nine items: seven prerequisite (P0.1, M1, M2, M4 x2, M5, M6) and two data-skill items (Pq8 rung 1; numeric rung 2). data-mastery 0.8; 7/9 = 77.8 percent, 8/9 = 88.9 percent, both as the text says. Correct options re-checked: T (theorem), contradiction, 1 (int 2x), 2 (E X), product rule, completeness, X_n, 2P(B_t>=a), 2 (paths reaching 1). PASS."))
R.append(row("SC1a-r4-hub-quiz-keys", "2.9-structure", G + "index.html:72-145 (data-correct / data-answer)", "PASS",
    "data-answer and data-correct flags match each item's explanation: numeric 1 (x^2 at 1), 2 (E X=2), skill numeric 2 (paths ++ and +-), mc keys (theorem; proof by contradiction; product rule; completeness; X_n; 2P(B_t>=a)). Explanations read."))
R.append(row("SC1a-hub-prereq-chain", "2.9-structure", G + "index.html:35, :58-68; curriculum/01-foundations.yaml (prereqs)", "PASS",
    "Curriculum prereqs (read with grep): M1 <- P0.1; M2 <- M1; M4 <- M2; M5 <- M2; M6 <- M4, M5; SC1 <- M6 (curriculum/03-markets.yaml:509). Hub chain 'SC1 requires M6, which requires M4 and M5. Those require M2, which requires M1, and M1 requires P0.1' matches. Closure M1, M2, M4, M5, M6, P0.1 matches the planner's closure."))
R.append(row("SC1a-hub-concept-list", "2.9-structure", G + "index.html:66 (From M6 list); hub list at :62-67", "PASS",
    f"Every hub-listed concept id is in the closure (owners M1, M2, M4, M5, M6, P0.1; {S}concept_owners_r12.out). Each is named in the module (grep: e.g. cauchy-sequence in L02 Prop 2.4 step 3; dominated convergence in L05; geometric series in L02 Step 2) or in the hub quiz (proof by contradiction, Pq2). Lessons link the concepts they use at first use ({S}hub_concept_use_r12.out). No concept outside the closure is listed."))
R.append(row("SC1a-hub-cards-L01-L03", "2.7-cards-copy", G + "index.html:152-154", "PASS",
    "Hub cards agree with the L01-L03 text: L01 (covariance min(s,t) from increments, scale of an increment, what the definition does not decide); L02 (hat functions, uniform convergence, continuous paths, A2 as the all-times identification); L03 (squared-increment sums, L2 limit with mesh to zero, t->t^2 sums vanish). Consistent with Lemma 2.3's dyadic scope and A2."))
R.append(row("SC1a-hub-ladder-objectives", "2.9-structure", G + "index.html:163-171 (ladder); :168 (rung 2)", "PASS",
    "Rung 2 text: 'discrete reflection count for the simple random walk, with the identity line and the final comparison line removed', and the twin of project-2 computes the n=6, a=2 count (29, verified by running lab-SC1-project-2.py: 'walks with maximum >= a: 29', reflection identity holds). Rung counts consistent with the project (project.html hours table, :272-280)."))
R.append(row("SC1a-simulated-labels", "2.5-labels", G + "L02.html:170 and :173 (lab-SC1-L02-1.py:3); L03.html:132 and :136", "PASS",
    "L02 hypothesis begins 'SIMULATED.' (:170), twin docstring 'SIMULATED.' (:3); L03 heading '(SIMULATED)' (:132) and docstring 'SIMULATED.' (:136). L01 labs are exact (no SIMULATED label needed; the lab docstring says no path is simulated). Matches BLUEPRINT §5.3."))
R.append(row("SC1a-hub-data-status", "2.8-data", G + "index.html:37, :174-177; L01-L03", "PASS",
    "'No real data is used in SC1' (index.html:176). grep for data-files and for MANIFEST references in index.html and L01-L03: none. Labs use generated values and closed forms only."))
R.append(row("SC1a-dag-hub-prose", "2.9-dag", G + "index.html:33, :53, :150", "PASS",
    f"check_dag SC1 PASS and --all PASS ({S}check_dag_all.out). Hub prose names no concept before its lesson (index.html:33 names Assumptions A3 and A4 of Lesson 5, which L05.html defines as Assumption A3 (L05.html:271) and A4(a)-(h) (grep); index.html:54 names Lesson 6 Theorem 2.5, which L06.html defines (reflection identity))."))
R.append(row("SC1a-prose-L01-three-conditions", "2.9-prose", G + "index.html:49; L01.html:51", "PASS",
    "'Three conditions' refers to Definition 1.1 (D1)-(D3) at L01.html:61-63, consistent in both places."))
R.append(row("SC1a-define-dyadic", "2.9-define-before-use", G + "L01.html:132 (dfn def-dyadic-partition), L02.html:71, L03.html:55", "PASS",
    "'Dyadic partition' is defined at L01.html:132 (plain dfn with id) and used later at L02.html:71 and L03.html:55 with a link to L01.html#def-dyadic-partition (check_dag confirms the anchor). The dyadic time of depth n is defined at L02.html:71 before its use in Lemma 2.2/2.3 and L02.html:132."))
R.append(row("SC1a-scope-L03-converge", "2.4-scope", G + "L03.html:270 (misconception 1)", "PASS",
    "The misconception's refutation (sums vanish for s^2 and converge in mean square to t for Brownian motion) uses Prop 2.4(a) and Theorem 2.3 with their assumptions named. No unsupported 'converges' claim. PASS."))
R.append(row("SC1a-hub-quiz-cross", "2.9-hub-quiz", G + "index.html:143 (skill check 2 explanation)", "PASS",
    "The explanation's count (paths ++ and +- reach 1: 2) and its rung-2 cross-reference (n=6, a=2 prints 29) are verified: twin run prints 'walks with maximum >= a: 29' (lab-SC1-project-2.py, this round)."))
R.append(row("SC1a-prose-two-sources", "2.1-citations", G + "index.html:184; references/references.json", "PASS",
    f"index.html:184: the curriculum lists two sources; only shreve2004stochastic is cited, no passage locator; the second (Karatzas & Shreve) has no admitted record. grep of references/references.json for 'Karatzas': 0 hits. Consistent with the planner's B2 (plans/SC1-build-plan.md) and the registry flag below."))
R.append(row("SC1a-lab-L02-hypothesis-expected", "2.5-lab-claims", G + "L02.html:170 (hypothesis), :275-278 (interpretation)", "PASS",
    "Hypothesis predicts 216 of 216, the grid-supremum True, each level within its bound with probability at most 2^{-m} and the sample count not guaranteed. Output: 216 of 216, True, eight of eight within bound. Interpretation (:278) says 'Neither number proves a bound on the supremum over [0,1]' for the tail grid sup 0.348139 vs sum of bounds 1.309399 (honest)."))
R.append(row("SC1a-r4-twin-timing-and-purity", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    "Each twin runs under `python -I -W error` with rc 0 and empty stderr (" + S + "lab_page_vs_twin_r12.out); page_smoke lab timings 0.0 s (L01), 0.2 s (L02), 0.1 s (L03) (page_smoke_L0x.out). Standard library only (fractions, math, random, itertools)."))
R.append(row("SC1a-r5-gaussian-process-scope-L01", "2.4-scope", G + "L01.html:107 (Remark 1.3 scope) and :115 (Gaussian process definition)", "PASS",
    "Remark 1.3 is for 0 < t_1 < ... < t_r; the Gaussian-process definition (:115) uses the same range; the sentence 'a standard Brownian motion is one, with mean zero and covariance min(s,t) for s,t>0' is within that range. PASS."))
R.append(row("SC1a-r6-variance-t0-L01", "2.4-math", G + "L01.html:67 ('Standard' paragraph)", "PASS",
    "'(D1) and (D2) give Var(B_t)=t for every t>=0: (D1) gives t=0, (D2) with s=0 gives t>0' is correct: Var(B_0)=0 since B_0=0, and Var(B_t)=t from N(0,t)."))
R.append(row("SC1a-r6-quiz-mesh-hypothesis-L03", "2.4-quiz", G + "L03.html:437-443 (quiz item 5)", "PASS",
    "Quiz item 5 answer 'Assumption 3.1' is the mesh condition, which the conclusion of Theorem 2.3 adds ('Assuming also Assumption 3.1', L03.html:104). Explanation correct."))
R.append(row("SC1a-r7-notation-F-clarity-L01", "2.4-notation", G + "L01.html:215", "PASS",
    "The probability space is written (Omega, F, P) with F defined by the product construction in the same paragraph; \\mathcal F is the sigma-algebra, not a registered symbol collision. PASS."))
R.append(row("SC1a-r7-gate-check-projects", "2.9-projects-tool", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    f"`tools/check_projects.py --unit SC1` -> 'check_projects SC1: PASS' ({S}check_projects_SC1.out)."))
R.append(row("SC1a-r7-katex-render", "2.9-math-rendered", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    "page_smoke on each page (alone): zero unrendered math (.katex-error) and each expression re-parses under KaTeX strict mode (page_smoke_index/L01/L02/L03.out)."))
R.append(row("SC1a-r7-forward-refs-L01-s4", "2.9-define-before-use", G + "L01.html:215 and :217 (canon-breaks section 4)", "PASS",
    "Forward references in L01 section 4 are to Lesson 2 by name (Remark 2.6, A2, Assumption 2.1, Hypothesis H1), each labelled 'of Lesson 2'; no L01 term is used before its definition in §1-§3."))
R.append(row("SC1a-r8-curriculum-facts", "2.9-structure", G + "index.html:33, :35, :60, :184", "PASS",
    "Curriculum facts (read from curriculum/03-markets.yaml and 01-foundations.yaml): Part SC, tier M, 100 h, prereq M6; M6 title 'Measure-Theoretic Probability' (hub :35); closure M1, M2, M4, M5, M6, P0.1; two sources (curriculum string). All match."))
R.append(row("SC1a-r8-links-anchors", "2.9-structure", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    "Concept links: every concepts.html#id anchor used by the four pages exists in course/concepts.html (script output, " + S + "slice_mech_r12.out). Intra-unit links (L01.html#def-brownian-motion, L01.html#def-dyadic-partition) resolve to ids in their targets. page_smoke reports zero failed requests on each page."))
R.append(row("SC1a-r8-A3-in-L05", "2.4-math", "course/modules/SC/SC1/L05.html:271, :279, :288; index.html:33, :53, :156", "PASS",
    "L05 defines Assumption A3 (strong Markov, 'not proved here', L05.html:271) and Assumption A4 (a-h, grep); the hub's claim (index.html:33) that A3 and A4 are stated in Lesson 5 is true. L05 is another slice; only the cross-reference was checked."))
R.append(row("SC1a-r8-project-rung-hours-and-check", "2.9-structure", G + "index.html:143, :165, :168; project.html:206, :272-280", "PASS",
    "Rung hours 2 + 3 (rungs 1, 2) and the 10 + 8 + 3 + 2 project rows total 28 (project.html:272-280). The rung-2 check prints 29 (twin run, this round). The hub's rung descriptions (:165-170) match the project ladder names."))
R.append(row("SC1a-r8-hub-numbers", "2.2-numbers", G + "index.html:29, :39-42, :74, :143, :150", "PASS",
    "72 and 28 (hours), 28 percent, 80 percent mastery bar, 7/9 = 77.8 percent and 8/9 = 88.9 percent (recomputed), 29 (rung-2 count, recomputed by twin), nine items, eight lessons of 9 h. All correct."))
R.append(row("SC1a-r8-lab-mutants", "2.5-labs", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    f"Lab-claim kill check (demonstrations, not graded): 9 of 9 single-change mutants of the three twins are killed by the expected block ({S}lab_mutants_r12.out; mutant files in ledgers/SC1/mutants/SC1-a-r12/)."))
R.append(row("SC1a-r8-L02-unrounded-E3", "2.2-numbers", G + "L02.html:419-421 (E3), :170", "PASS",
    f"Unrounded |xi_11| = 0.23317868947...; sup = 0.11658934... -> 0.116589; twice the unrounded sup = 0.2331787 -> 0.233179 (6 dp); doubling the printed 0.116589 gives 0.233178 (as E3 says); lambda_1/2 = 0.8325546 -> 0.832555 ({S}e3_l02_numbers_r12.out)."))
R.append(row("SC1a-r9-hub-ost-card-L04", "2.9-structure", G + "index.html:155 (L04 card); L04.html", "PASS",
    "Hub L04 card: 'The filtration of Brownian motion, the martingales B_t, B_t^2-t and the exponential martingale.' It makes no optional-stopping claim; L04 mentions optional stopping only where it states the theorem with its assumption (grep count 1 in L04.html). Agreement holds."))
R.append(row("SC1a-r9-hub-reflection-assumptions", "2.9-structure", G + "index.html:33 (lede), :157 (L06 card); L06.html:118-119, :52", "PASS",
    "Hub lede and L06 card state the reflection identity as fixed-time under A3 and A4; L06 'Theorem 2.5 (the reflection identity for Brownian motion)' is the fixed-time result, 'the results below need the path only on [0,t] for a fixed t>0' (L06 text). Consistent."))
R.append(row("SC1a-r9-hub-objective-reflection-proof", "2.9-structure", G + "index.html:54 (objective 6); L06.html (Theorem 2.5)", "PASS",
    "Objective 6 names 'the fixed-time reflection identity for Brownian motion (Lesson 6, Theorem 2.5)'. grep: L06.html contains 'Theorem 2.5 <span class=\"name\">(the reflection identity for Brownian motion)'. Locator correct."))
R.append(row("SC1a-r9-quiz-L02-q3-explanation", "2.9-structure", G + "L02.html:489; L02.html:161 (Step 2)", "PASS",
    "The explanation's bound M_m <= sqrt(2 log 2) m r^m with r = 2^{-1/2} matches Step 2 (:161); sqrt(m) 2^{-m/2} <= m r^m for m >= 1 is correct (sqrt m <= m). The correct option is the one that names m r^m with 0 <= r < 1."))
R.append(row("SC1a-r10-cmd-check_pages", "2.9-structure-tool", "tools/check_pages.py --unit SC1", "PASS",
    f"'check_pages SC1: PASS' exit 0 ({S}check_pages_SC1.out). Note: `--page index` is not a valid use of the flag (it checks lesson templates; `check_pages.py --page index` reports 13 lesson-template failures for the hub). The unit-level run covers the hub."))
R.append(row("SC1a-r10-cmd-check_dag", "2.9-dag-tool", "tools/check_dag.py --all", "PASS",
    f"`check_dag --all`: every unit PASS, including SC1 ({S}check_dag_all.out, {S}check_dag_SC1.out)."))
R.append(row("SC1a-r10-cmd-check_projects", "2.9-projects-tool", G + "project.html (unit gate)", "PASS",
    f"'check_projects SC1: PASS' ({S}check_projects_SC1.out)."))
R.append(row("SC1a-r10-cmd-run_labs", "2.5-labs-run", "tests/labs/SC1/*-1.py and project labs", "PASS",
    "run_labs --unit SC1: 11/11 (" + S + "run_labs_SC1.out)."))
R.append(row("SC1a-r10-cmd-page_smoke", "2.9-page-smoke", "index, L01, L02, L03", "PASS",
    "page_smoke run alone per page: PASS for index, L01, L02, L03 (page_smoke_*.out)."))
R.append(row("SC1a-r10-cmd-twins-python-I-W-error", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, L02-1, L03-1", "PASS",
    "Each twin: `.venv/bin/python -I -W error` (CPython 3.14.8) from an empty directory: rc 0, empty stderr (" + S + "lab_page_vs_twin_r12.out; twin_venv_L0x.out)."))
R.append(row("SC1a-r10-cmd-verify_refs", "2.1-citations", G + "index.html:182 (data-cite)", "PASS",
    "verify_refs --offline: 560 entries, 0 problems; verify_refs --unit SC1 (live): 1 of 560 entries, 0 problems (" + S + "verify_refs_offline.out, verify_refs_live_SC1.out)."))
R.append(row("SC1a-r10-cmd-ruff-mypy", "2.5-ruff-mypy", "tests/labs/SC1/*; tests/test_labs.py", "PASS",
    "ruff check and format check (pass); mypy --no-incremental on the three twins (Success) and on the whole project (385 files, Success) (" + S + "mypy_twins.out, mypy_full.out)."))
R.append(row("SC1a-r10-cmd-pytest-SC1", "2.5-pytest", "tests/test_labs.py (SC1 cases)", "PASS",
    "`pytest -q -k SC1`: 11 passed, exit 0 (" + S + "pytest_SC1.out); collect-only count 11 in tests/test_labs.py (" + S + "pytest_SC1_collect.out)."))
R.append(row("SC1a-r10-lab-mutants-4of4", "2.5-labs", "ledgers/SC1/mutants/SC1-a-r12/ (re-created)", "PASS",
    "The round-10 lab mutants are not in this pin, so the four student-error lab mutants (dyadic width t/2**(n+1); level scale on the grid; SE divisor n+1; exact-sum offset) were re-created from their descriptions and run this round as m6-m9 (" + S + "lab_mutants_r12.out): 4 of 4 killed."))
R.append(row("SC1a-r10-L02-E3-unrounded", "2.2-numbers", G + "L02.html:421 (E3); tests/labs/SC1/lab-SC1-L02-1.py", "PASS",
    "Same as SC1a-r8-L02-unrounded-E3: unrounded |xi_11| = 0.2331787 (7 dp), printed 0.116589, doubling gives 0.233178 (printed digits) vs 0.233179 (unrounded). E3 is correct."))
R.append(row("SC1a-r10-L02-quiz-q3-math", "2.2-numbers", G + "L02.html:483-489", "PASS",
    "Quiz item 3: the correct option is the one with terms at most m r^m, with the sum finite; the explanation's inequality holds (SC1a-r9-quiz-L02-q3-explanation)."))
R.append(row("SC1a-r10-L03-key-results-14pct", "2.2-numbers", G + "L03.html:398; " + S + "l03_numbers_r12.out", "PASS",
    "Same as SC1a-numbers-L03-SE-follow: max |gap| 13.2 percent at H=2,N=1; all 16 gaps within 14 percent (recomputed)."))
R.append(row("SC1a-r10-L03-why-sample-means", "2.5-lab-claims", G + "L03.html:51; tests/labs/SC1/lab-SC1-L03-1.py", "PASS",
    "why-it-matters (L03.html:51): 'Lab 1 simulates Brownian increments on partitions into 2^k equal steps and prints the sample means with standard errors'. The twin prints mean and se for 2^k steps (k=0..7) and 2 horizons. Matches."))
R.append(row("SC1a-r10-L03-R3-hypothesis", "2.4-math", G + "L03.html:382 (R3 solution), :99-103 (Theorem 2.3 hypotheses)", "PASS",
    "R3 names H1 (not standard BM) as failing and says H2 does not apply; Theorem 2.3's H1 is 'B is a standard Brownian motion' (L03.html:101). Consistent."))
R.append(row("SC1a-r10-hub-prereq-curriculum", "2.9-structure", G + "index.html:35, :58-68; curriculum/01-foundations.yaml", "PASS",
    "Same as SC1a-hub-prereq-chain: curriculum prereq lists M1<-P0.1, M2<-M1, M4<-M2, M5<-M2, M6<-M4,M5 and SC1<-M6 match the hub."))
R.append(row("SC1a-r10-hub-concept-count", "2.9-structure", G + "L01.html:59, L02.html:68, L03.html:59; curriculum/03-markets.yaml:513-521", "PASS",
    f"SC1 owns 8 concepts in curriculum.json (brownian-motion, brownian-motion-construction, continuous-time-martingale, first-passage-time, markov-property, quadratic-variation, reflection-principle, running-maximum-distribution; {S}concept_owners_r12.out). Each of the three slice-owned ones is defined once: brownian-motion (L01.html:59), brownian-motion-construction (L02.html:68), quadratic-variation (L03.html:59)."))
R.append(row("SC1a-r10-hub-rung2-count", "2.9-structure", G + "index.html:143; " + "course/modules/SC/SC1/project.html:206", "PASS",
    "Twin lab-SC1-project-2 prints 'walks with maximum >= a: 29' for n=6, a=2 (run this round); project.html:206 expected block shows the same line."))
R.append(row("SC1a-r10-hub-hours-sum", "2.9-hours", G + "index.html:29, :39-42, :150; L01-L08 data-hours", "PASS",
    "72 = 8 x 9 (L01-L08 data-hours 9 each per grep); 28 = project table sum (project.html:272-280); total 100 = curriculum SC1 hours."))
R.append(row("SC1a-r10-hub-lede-path-level", "2.9-prose", G + "index.html:33; L06.html", "PASS",
    "Hub lede: 'The reflection is proved in its fixed-time form only; the path-level reflection at the first passage time is not proved.' L06 says the fixed-time results need the path only on [0,t] (L06 text) and does not reprove path-level results. Consistent."))
R.append(row("SC1a-r10-notation-collisions", "2.4-notation", G + "index.html, L01.html, L02.html, L03.html; notation/notation.json", "PASS",
    "Registered symbols T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q: none used with another meaning in the slice (see SC1a-notation-no-registered-collision, SC1a-notation-T-subscript). Registered macros used: \\E, \\Prob, \\Var, \\Cov, \\Normal, \\indic (notation/notation.json lines)."))
R.append(row("SC1a-r10-process-words", "2.9-prose", G + "index.html, L01.html, L02.html, L03.html", "PASS",
    "Same grep as SC1a-process-words: no process words in learner text."))
R.append(row("SC1a-r10-cards-dup-hypotheses", "2.7-cards", G + "cards.json (216 cards; L01-L03 cards read in full: " + S + "cards_L01_L03_r12.txt)", "PASS",
    f"Fixed since round 11. Full scan ({S}cards_scan_r12.out): 216 cards, no duplicate id, front or back; ids match SC1-cNNN. Card SC1-c026 (Lemma 2.3) now lists 'assuming A1(a), A1(b), A1(c) and A1(e)', matching L02.html:124. Card SC1-c207 restates A1(b) exactly as L01.html:75 now reads. Every number in an L01-L03 card appears in its lesson (script). Card SC1-c027 and c028 match the step text (:137-138)."))
R.append(row("SC1a-r10-lab-L01-L02-L03-claims", "2.5-lab-claims", "tests/labs/SC1/lab-SC1-L01-1.py:1-9; lab-SC1-L02-1.py:1-8; lab-SC1-L03-1.py:1-14; L01.html:136, :208; L02.html:170-278; L03.html:133, :253", "PASS",
    "Docstrings and lesson statements about each lab match code and output (checked per lab, see SC1a-lab-claims-L01, SC1a-lab-L02-docstring, SC1a-lab-claims-L03)."))
R.append(row("SC1a-r10-card-L05-ck-wording", "2.7-cards-copy", G + "index.html:156 (L05 card body); L05.html:7 (meta), :52", "PASS",
    "Hub L05 card: 'the Chapman-Kolmogorov identity proved by completing the square'. L05 (meta description and the Chapman-Kolmogorov block) states the same proof method. Consistent."))
R.append(row("SC1a-r10-A1-attribution-M4", "2.4-assumptions", G + "L01.html:37, :71-80", "PASS",
    "L01 'Uses' (:37) lists M4 concepts as prerequisite facts and says facts the page does not prove are stated as A1 (a-e); A1 itself (:72) carries no M4 attribution and no registry key; L01.html:80 says it cites no source. No attribution to M4 is made for A1's parts, so no misattribution."))
R.append(row("SC1a-r11-A1b-literal-false", "2.4-math", G + "L01.html:75 (A1(b), second sentence)", "PASS",
    "Fixed since round 11. Old sentence ('A vector whose coordinates are such combinations is multivariate normal') was false for (Z, eps*Z). New sentence: 'A vector each of whose coordinates is a finite linear combination of one common family of independent normal variables is multivariate normal.' True: such a vector is X = AZ + b for a vector Z of independent normals (jointly Gaussian), and linear images of Gaussian vectors are Gaussian. The counterexample does not satisfy the new hypothesis ((Z, eps*Z) is not a combination of one independent family). Counterexample script from round 11 is kept at " + S + "a1b_counterexample.py (the old text, for reference)."))
R.append(row("SC1a-r11-lab-mutants-6of6", "2.5-labs", "tests/labs/SC1/*-1.py against the expected blocks", "PASS",
    "Lab-claim kill check this round: 9 of 9 mutants killed (" + S + "lab_mutants_r12.out), including the round-11 classes (covariance index, hat support, grid depth, SE divisor, exact-sum offset, dyadic width)."))
R.append(row("SC1a-r11-numbers-recomputed", "2.2-numbers", S + "e3_l02_numbers_r12.out, l03_numbers_r12.out, l02_bounds_r12.out, l02_identities_seeds_r12.out", "PASS",
    "Every number in prose recomputed by scripts written this round (see rows SC1a-numbers-L01/L02/L03 and SC1a-r8-L02-unrounded-E3)."))
R.append(row("SC1a-r11-concept-list-exact", "2.9-structure", G + "index.html:58-68; " + S + "concept_owners_r12.out; " + S + "hub_concept_use_r12.out", "PASS",
    "Hub prerequisite list: every listed concept is in the closure (owners M1, M2, M4, M5, M6, P0.1) and is used in the module by name or link (hub_concept_use_r12.out shows the links; names found by grep). No extra concept outside the closure."))
R.append(row("SC1a-r11-hours-and-projects", "2.9-hours", G + "L01.html-L08.html data-hours; index.html:29, :39-42, :150; project.html:33, :272-280", "PASS",
    "Hub 72 + 28 = 100 = curriculum SC1 hours (curriculum/03-markets.yaml:508). Project hours table sums to 28 (project.html:272-280). Hub percentages 72 percent and 28 percent (28 of 100) correct."))
R.append(row("SC1a-r11-cards-scan", "2.7-cards", G + "cards.json (216 cards); " + S + "cards_scan_r12.out", "PASS",
    "Full scan (216 cards): no duplicate ids, fronts or backs; L01-L03 cards (76) read in full (" + S + "cards_L01_L03_r12.txt); card numbers appear in their lessons; grades: T 125, C 27, definitions None (definitions carry no grade by convention in BUILDER_RULES §7)."))
R.append(row("SC1a-r11-delta-read", "2.9-delta", "git diff 11d7077a..5db69a9 for index.html, L01.html, L02.html, L03.html, cards.json, tests/labs/SC1", "PASS",
    "Every hunk of the slice-a delta read: index.html:69 (promise, see SC1a-hub-assumption-promise); L01.html:75 (A1(b)), :112 (Remark 1.3 proof), :215 (canon item 1, 'A2 and Assumption 2.1 are stated in Lesson 2'); L02.html:68 (§3 cross-reference), :124 (H2 adds A1(a)), :137-138 (Cov and independence paragraphs), :460 (key results), :526 (quiz explanation); L03.html:55 (dyadic partition wording), :398 (C row, 13.2 percent); cards.json (130-line change, all L01-L03 cards read, all 216 scanned). Lab twins for SC1 unchanged (git diff empty). Not in slice a: L04.html, L05.html, project.html and curriculum/program hunks (other slices; the two non-SC1 curriculum hunks concern the arbitrage project only)."))
R.append(row("SC1a-r11-twins-venv-314", "2.5-labs-run", "tests/labs/SC1/lab-SC1-L01-1.py, lab-SC1-L02-1.py, lab-SC1-L03-1.py", "PASS",
    "Run under the repo venv (python3.14.8 via .venv/bin/python -> python3): rc 0, empty stderr, output equals the expected blocks (" + S + "twin_venv_L01.out, twin_venv_L02.out, twin_venv_L03.out; lab_page_vs_twin_r12.out)."))
R.append(row("SC1a-r12-L02-identities-301-seeds", "2.5-lab-seed", "tests/labs/SC1/lab-SC1-L02-1.py (docstring: identities hold for every seed)", "PASS",
    "New this round: 301 seeds (0-299 and 20260101) all satisfy the 216-case dyadic identity and the grid-supremum identity; the bound lines are not claimed to hold for every seed and the page says so (L02.html:278)."))

# Mutants: lab-claim kill checks (demonstrations; not graded)
MUT = [
    ("SC1a-r12-lab-m1", "lab-SC1-L01-1: covariance sums increments up to max(i,j) instead of min(i,j); line 'Cov(B at 1/4, B at 5/8)' prints 5/8.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m2", "lab-SC1-L02-1: hat peak 1/2 instead of 1; grid-supremum line prints False.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m3", "lab-SC1-L03-1: closed form uses H cubed instead of H^4; exact-match column prints False.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m4", "lab-SC1-L03-1: sample variance divides by n instead of n-1; z for N=2 prints 2.40.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m5", "lab-SC1-L02-1: bound uses sqrt(2 m log 2); bound lines change.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m6", "lab-SC1-L01-1: dyadic piece length t/2^(n+1) instead of t/2^n; sums print t/2.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m7", "lab-SC1-L02-1: grid check uses a level scale off by a factor sqrt(2); grid-supremum line prints False.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m8", "lab-SC1-L03-1: standard error divides the sample variance by n+1; first z changes.", "exact diff vs expected block (lab_mutants_r12.out)"),
    ("SC1a-r12-lab-m9", "lab-SC1-L03-1: exact s-squared sum drops the first interval; closed-form match prints False.", "exact diff vs expected block (lab_mutants_r12.out)"),
]
MUTANTS = [{"id": i, "description": d, "killed_by": k} for i, d, k in MUT]

frag = {
    "unit": "SC1",
    "slice": "a",
    "round": 12,
    "round_note": "Round 12, independent verifier (Haiku), did not build SC1. Previous pin 11d7077 (round 11); this pin 5db69a9 is the fix commit for round 11 (ccaeeaf4 and 5db69a9 in between).",
    "verifier": "verifier Haiku, round 12 (slice a)",
    "pin": PIN,
    "base": BASE,
    "checkout": root,
    "scratch": "/tmp (sc1a_r12 scratch; twins run from empty directories)",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": MUTANTS,
    "registry_flags": [
        "Curriculum SC1 lists Karatzas & Shreve, Brownian Motion and Stochastic Calculus, 2nd ed. (1991) as a second source (curriculum/03-markets.yaml:524). No registry record exists (grep of references/references.json: 0 hits). The hub says so (index.html:184); no action in slice a unless the module should cite it."
    ],
    "freshness_flags": [],
    "notes": [
        "Full read of the slice at 5db69a9: index.html (190 lines), L01.html (446), L02.html (560), L03.html (504), the three lab twins, and all 76 L01-L03 cards in full (all 216 cards scanned for duplicates and number agreement).",
        "Delta since round 11 (11d7077 -> 5db69a9): every hunk in slice a read (index.html:69; L01.html:75, :112, :215; L02.html:68, :124, :137-138, :460, :526; L03.html:55, :398; cards.json). Lab twins unchanged.",
        "Gates run at 5db69a9 (outputs in ledgers/SC1/scripts/SC1-a-r12/): check_pages --unit SC1; check_dag --unit SC1 and --all; check_projects --unit SC1; run_labs --unit SC1 (11/11); page_smoke --unit SC1 --pages index, L01, L02, L03 each alone; ruff check and format (project-wide); mypy --no-incremental (twins and full project, 385 files); pytest -k SC1 (11 passed); verify_refs --offline and --unit SC1 (live); twins under python -I -W error (venv CPython 3.14.8); fetch_data --check (exit 0).",
        "Round-11 FAIL rows: SC1a-math-L01-remark1.3 (fixed: Remark 1.3 now applies A1(b) to one common family), SC1a-r11-A1b-literal-false (fixed: A1(b) now true), SC1a-r10-cards-dup-hypotheses (fixed: c026 and c207 match the lesson), SC1a-math-L02-lemma2.3-arithmetic (PARTLY fixed: Var(U_j) and Cov now justified; the Consequence variance at L02.html:139 is still unjustified, FAIL again), SC1a-hub-assumption-promise (PARTLY fixed: A1 now complies; L03 Assumption 3.2 does not, FAIL again).",
        "Not run: run_graders and mutate_graders (project graders; outside slice a). Project graders' mutants (ledgers/SC1/mutants/m01-m21.py) are not this slice's.",
        "Tool note: `tools/check_pages.py --unit SC1 --page index` fails with 13 lesson-template problems because --page addresses lesson pages only; the unit-level run (PASS) covers index.html. Not a finding against the hub.",
        "Round-10 lab mutant files (ledgers/SC1/mutants/SC1-a-r10/) are not in this pin; the four round-10 mutant classes were re-created from their descriptions and run as SC1a-r12-lab-m6..m9 (all killed).",
        "Lab mutants are demonstrations (ruling: lab twins are not mutation-tested); they are recorded only as lab-claim kill checks.",
        "Statistics: rows 128 carried ids from round 11 plus 1 new id (SC1a-r12-L02-identities-301-seeds); PASS 127, FAIL 2 (SC1a-math-L02-lemma2.3-arithmetic, SC1a-hub-assumption-promise), UNVERIFIABLE 0. No row is marked PASS on a carried basis; every row was re-checked this round against the current subject.",
    ],
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in R:
    counts[r["status"]] += 1
frag["summary"] = {
    "text": f"SC1-a round 12 at {PIN[:7]}: verdict FAIL. {len(R)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, {counts['UNVERIFIABLE']} UNVERIFIABLE. Non-PASS: " + ", ".join(r["id"] for r in R if r["status"] != "PASS") + ".",
    "counts": counts,
    "non_pass_ids": [r["id"] for r in R if r["status"] != "PASS"],
    "mutants": f"{len(MUTANTS)} of {len(MUTANTS)} lab-claim mutants killed (demonstrations)",
}
out = root + "/ledgers/SC1/SC1-a.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, counts, len(R))
