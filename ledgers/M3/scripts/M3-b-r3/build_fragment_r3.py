"""Round-3 slice b: writes the ledger fragment ledgers/M3/M3-b.json from the rows verified this round.

Every row was re-verified in round 3 (none carried). Evidence names the scripts and output files under
ledgers/M3/scripts/M3-b-r3/. Run from the checkout root: python ledgers/M3/scripts/M3-b-r3/build_fragment_r3.py
"""
import json

S = "ledgers/M3/scripts/M3-b-r3/"
GATES = S + "gates_fast.out"
TWIN = S + "twin_vs_page.out"
NUM = S + "recheck_numbers_r3.out"
PS = S + "page_smoke_slice_b.out"
INV = S + "inventory_r3.out"
BAN = S + "banned_scan_r3.out"
DUP = S + "dup_scan_r3.out"
DAG = S + "dag_name_scan.out"
FWD = S + "forward_ref_scan.out"
CARDS = S + "slice_cards.txt"

R = []


def row(i, check, location, status, evidence, fix=None):
    d = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


L4 = "course/modules/M/M3/L04.html"
L5 = "course/modules/M/M3/L05.html"
L6 = "course/modules/M/M3/L06.html"
CD = "course/modules/M/M3/cards.json"

row("M3b-r1-01", "2.5-lab L04: hypothesis, code, expected block, interpretation present",
    L4 + ":174-266; tests/labs/M3/lab-M3-L04-1.py", "PASS",
    f"{TWIN}: lab-M3-L04-1 page_code_equals_twin=True expected_equals_output=True exit=0 stderr_bytes=0 under python -I -W error (script ledgers/M3/scripts/M3-b-r3/twin_vs_page.py). Hypothesis (L04:176) lists the printed checks; each is printed at twin lines 233-252.")
row("M3b-r1-02", "2.5 lab interpretation L04 against what the lab prints",
    L4 + ":265 vs expected block 256-264", "PASS",
    f"{TWIN} expected==output for L04; interpretation says counts with tolerance 1e-10 and no raw residuals; {NUM} section L04 gives max orth 1.55e-15, recon 3.11e-15, residual 2.11e-15, imag 0.0, pair orthogonality 6.1e-16 (margins >1e4 under 1e-10).")
row("M3b-r1-03", "2.5-lab L05 structure and twin run",
    L5 + ":175-305; tests/labs/M3/lab-M3-L05-1.py", "PASS",
    f"{TWIN}: lab-M3-L05-1 page_code_equals_twin=True expected_equals_output=True exit=0 stderr_bytes=0; {GATES} run_labs --page L05 PASS (1/1).")
row("M3b-r1-04", "2.5 lab interpretation L05 states what the lab prints (round-1 FAIL, re-verified)",
    L5 + ":303 vs expected 291-301; twin part_d()", "PASS",
    f"Interpretation says eigenvalues are rounded and a singular-matrix value within 1e-10 of zero prints as 0.0000. Twin part_d() prints '0.0 if abs(values[0]) <= TOL else values[0]' with :.4f, so the printed 0.0000 is implemented. {TWIN} shows the printed line 'Gram matrix of the rank 2 factor, eigenvalues sorted: 0.0000 1.0000 3.0000' and 'eigenvalues with absolute value at most 1e-10: 1'.")
row("M3b-r1-05", "2.5-lab L06 structure and twin run",
    L6 + ":135-225; tests/labs/M3/lab-M3-L06-1.py", "PASS",
    f"{TWIN}: lab-M3-L06-1 page_code_equals_twin=True expected_equals_output=True exit=0 stderr_bytes=0; {GATES} run_labs --page L06 PASS (1/1). The docstring tolerance sentence is row M3b-r3-66 (FAIL), not this row.")
row("M3b-r1-06", "2.5 lab hypothesis and interpretation L06 against twin and output",
    L6 + ":137, 224 vs twin lines 52-75 and expected 216-223", "PASS",
    f"Hypothesis lists the four identity checks, the seed-0 singular values, the planted rank-2 count and the sign-flip check; twin prints each (lines 52-75). Interpretation's 'print True for these ten matrices' matches {TWIN} (four True lines); 'count of 2' and 'three singular values rounded from unrounded values' match the twin (lines 60, 65 use unrounded s0 and planted SVD).")
row("M3b-r1-07", "2.5 twin lint, format and types",
    "tests/labs/M3/lab-M3-L04-1.py, lab-M3-L05-1.py, lab-M3-L06-1.py", "PASS",
    f"{GATES}: 'ruff check tests/labs/M3' All checks passed; 'ruff format --check tests/labs/M3' 12 files already formatted; 'mypy --no-incremental' Success: no issues found in 385 source files.")
row("M3b-r1-08", "2.5 lab runtime, no network, seeded RNG only",
    "three twins; " + PS, "PASS",
    f"{PS}: lab-M3-L04-1 0.0 s, lab-M3-L05-1 0.1 s, lab-M3-L06-1 0.0 s (Pyodide, under 10 s). Twins: default_rng(seed) in each (inventory {INV}: seeded True, no urllib/requests/socket/http imports).")
row("M3b-r1-09", "2.5 lab scope sentences (tested seeds, grid and matrices)",
    L4 + ":265; " + L5 + ":303, 312; " + L6 + ":224, 237", "PASS",
    "Each scope sentence names its sample: 200 seeded 4x4 (L04:265), 360 grid angles and 500x200 seeded forms (L05:303, :312), ten seeded matrices and the planted rank-2 threshold (L06:224, :237). Sampling sentences say a sample refutes but cannot prove (L05:303, :312). Checked against the twin code and output in " + TWIN + ".")
row("M3b-r1-10", "2.2 printed and prose numbers L04 re-derived",
    L4 + ":51, 97-106, 164-172, 176, 256-265, 268-278, 297-420", "PASS",
    f"{NUM}: 1200 pairs (200 x C(4,2)); |<(1,0),(1,1)/sqrt2>| = 0.7071067812; eig(N) = 1, 3; Example 2.6 corollary value 3*(1/2)+1*(1/2) = 2; Remark 1.6 char poly lambda^2+1 (imag part 1). Fraction checks in the same output confirm Example 1.7 (-2) and L04 mech-3 (6).")
row("M3b-r1-11", "2.2 printed and prose numbers L05 re-derived",
    L5 + ":177, 291-303, 391-409, 453", "PASS",
    f"{NUM} L05 Part B: 118 negative grid angles, zero at 105, 165, 285, 345 (4 grid points), min -1.000000000000; grid fraction 118/360 = 0.327778 (rounds to 0.3278, E2 at L05:402); arc fraction 1/3. Part C: 500 of 500 Gram matrices, 100000 of 100000 forms. Part D: det(G-lambda I) at 0, 1, 3 is 0 and at 2 is 2 = (1-2)*2*(2-3).")
row("M3b-r1-12", "2.2 printed and prose numbers L06 re-derived",
    L6 + ":216-223, 261-300, 316-335, 384-455", "PASS",
    f"{NUM} L06: seed-0 4x3 singular values 2.2334970848, 0.9249716026, 0.3348254752 (SVD and sqrt eig agree), rounded 2.2335, 0.9250, 0.3348; planted rank-2 singular values 5.28, 0.578, 4.3e-16 gives count 2 at 1e-10 relative. Problems: M1 sigma 4 and 3 (L06:266-272), M2 sqrt2 and Frobenius 2 (L06:273-279), E3 sigma 5 (L06:330-334); quiz 30 (Frobenius of [[1,2],[3,4]]) and 8 (2I_2) at L06:411-455.")
row("M3b-r1-13", "2.2 scope words (every, all, only, exactly, never, same, any, in general, always)",
    L4 + ", " + L5 + ", " + L6 + " prose and changed lines L04:51, L05:51, L06:52, L06:348-358", "PASS",
    f"Scope scan {BAN} and the contextual list of every/for every/all/any/only/exactly lines. Each universal claim is either proved on the page (Lemma 1.4, Theorem 2.3 and its induction, Prop 2.1, Proposition 1.5, Theorem 2.1 both directions, Prop 2.3, Prop 2.4, R2, R3 of L06) or is a tested statement scoped in the sentence (L04:265, L05:303, L05:312, L06:224). No 'always', 'in practice', 'generic', 'robust' or 'stable' in the slice (BAN).")
row("M3b-r1-14", "2.2 rounding: displayed digits come from unrounded values",
    "printed decimals in L04-L06 pages and twins", "PASS",
    f"{NUM}: 1/sqrt2 = 0.70710678 (8 dp) rounds to 0.7071; 118/360 = 0.327778 rounds to 0.3278; seed-0 SVD values rounded from unrounded floats (twin uses s0 unrounded, line 60). Twin Part D rounds the near-zero eigenvalue to 0.0000 explicitly (L05 twin part_d).")
row("M3b-r1-15", "2.3 grades L04", L4 + ":77-171, 402-420", "PASS",
    "T for Lemma 1.3, 1.4, 2.1, 2.2, Theorem 2.3, Proposition 2.4, Corollary 2.5, Remark 2.7 (computed), Example 2.6 (computed); C for the lab row (L04:415) with basis 'Lab 1, seed 2604; a sample, not a proof'. Grades re-derived against BLUEPRINT section 3 by reading each proof.")
row("M3b-r1-16", "2.3 grades L05", L5 + ":107-173, 440-457", "PASS",
    "T for Prop 1.5, 1.6, Theorems 2.1, 2.2, Prop 2.3, 2.4, Remark 2.7, Remark 3.2; C for the Lab 1 key row (L05:453) as a sample result with basis named. Example 1.7 and 2.6 are computations (T).")
row("M3b-r1-17", "2.3 grades L06", L6 + ":63-133, 366-382", "PASS",
    "T for Fact 1.2, Lemma 1.3, Prop 2.1, Theorem 2.2, Theorem 2.3, Prop 2.4, Remark 2.5 (second part, I_2); C for the Lab 1 key row (L06:378) with basis 'finite numerical check on seeded inputs'.")
row("M3b-r1-18", "2.4 math L04 core: Lemmas 1.3, 1.4, 2.1, 2.2, Theorem 2.3 proof steps",
    L4 + ":77-142", "PASS",
    "Re-derived each step: Lemma 1.3 coefficient argument; Lemma 1.4 F1 one-sided inverse and norm; Lemma 2.1 conjugation identity s = conj(s) using A_ij = A_ji (so s real, lambda = s/(z*z) real); Lemma 2.2 real/imaginary parts of Az = lambda z; Theorem 2.3 induction: W invariant (L04:137-139), S symmetric, u_j eigenvectors, Lemma 1.3 + F4 basis, AQ = Q Lambda. No gap.")
row("M3b-r1-19", "2.4 hypotheses L04 Proposition 2.4 (field of the vectors) (round-1 FAIL, re-verified)",
    L4 + ":144-152; Definition 1.2 at " + L4 + ":73-76", "PASS",
    "Proposition 2.4 states A real symmetric, v,w in R^n, lambda != mu, all real; proof uses only symmetry (Av.w = v.Aw) and lambda != mu. No complex hypothesis is needed and none is used.")
row("M3b-r1-20", "2.4 math L04 Corollary 2.5, Example 2.6, Remarks 1.5, 1.6, 2.7",
    L4 + ":97-106, 154-172", "PASS",
    f"{NUM}: Example 2.6 A(1,1)=(3,3), A(1,-1)=(1,-1), QLQ^T = A (hand computation re-done); corollary at (1,0) gives 2 = A_11. Remark 2.7 eigenspaces = lines through (1,0), (1,1); N - I rows (0,2), N - 3I rows (-2,2),(0,0); inner product 1/sqrt2. Remark 1.6 char poly lambda^2+1.")
row("M3b-r1-21", "2.4 math L05 core: Remark 1.2, Props 1.5, 1.6, Example 1.7, Remark 1.8, Theorems 2.1, 2.2",
    L5 + ":55-127, 107-125", "PASS",
    f"Remark 1.2 symmetric-part identity; Prop 1.5 ||Bx||^2; Prop 1.6 diagonal e_i and sums; Example 1.7 form -2 (recomputed in {NUM}); Remark 1.8 x1^2+x2^2 and char poly lambda^2-2lambda+2 (hand re-derived); Theorem 2.1 (=>) via w = real or imaginary part and 0 <= w^T A w = lambda||w||^2; (<=) via Corollary 2.5; Theorem 2.2 both directions. No gap.")
row("M3b-r1-22", "2.4 math L05 Propositions 2.3, 2.4, Example 2.5, Remark 2.7",
    L5 + ":128-161", "PASS",
    f"Prop 2.3 forces lambda_j y_j = 0 and so Ax = 0; Prop 2.4 B = Lambda^{{1/2}}Q^T gives B^TB = A; Example 2.5 entries 2, 1, 2 (Fraction check in {NUM}); Remark 2.7 O = -I gives -B, nonzero B distinct. No gap.")
row("M3b-r1-23", "2.4 math L05 Definition 3.1 and Remark 3.2",
    L5 + ":165-173", "PASS",
    f"{NUM} Part D: G = [[1,0,1],[0,1,1],[1,1,2]]; det(G - tI) = 0 at t=0, 1, 3 and 2 at t=2 matching (1-l)l(l-3) at 2; B(1,1,-1) = (0,0) so (1,1,-1) is in the null space. Smallest eigenvalue exactly 0 so Theorem 2.2 gives not PD.")
row("M3b-r1-24", "2.4 math L06 core: Fact 1.2, Lemma 1.3, Proposition 2.1",
    L6 + ":58-95", "PASS",
    "Fact 1.2: F1 applied to M = Q^T, N = Q gives Q^T invertible with inverse Q, so QQ^T = I; norm preservation. Lemma 1.3: Gram-Schmidt on u_1..u_r, e_1..e_m; discarded vectors are combinations of accepted ones; independence from L04 Lemma 1.3; count m. Prop 2.1: x^TA^TAx = ||Ax||^2 and the conjugate-transpose quotient gives real nonnegative eigenvalues. No gap.")
row("M3b-r1-25", "2.4 math L06 Theorem 2.2 (SVD) proof, Steps 1-5",
    L6 + ":97-113", "PASS",
    "Step 1 spectral decomposition of G with descending lambda; Step 2 u_i^T u_j = sigma_j^2 delta_ij/(sigma_i sigma_j) = delta_ij; Step 3 Lemma 1.3 completes U; Step 4 AV = U Sigma column by column (Av_j for j > r has ||Av_j||^2 = lambda_j = 0); Step 5 A = U Sigma V^T via VV^T = I (Fact 1.2) and rank = r. Eigenvalues are listed in descending order by reordering the orthonormal basis (implicit, not stated; acceptable).")
row("M3b-r1-26", "2.4 math L06 Theorem 2.3 and Proposition 2.4",
    L6 + ":115-133", "PASS",
    "Theorem 2.3: A^TA = V(Sigma^T Sigma)V^T; similarity with V^{-1} = V^T (Fact 1.2) gives equal characteristic polynomials. Prop 2.4: tr(A^TA) = sum a_ij^2 and tr(XY) = tr(YX) with X = V gives tr(Sigma^T Sigma) = sum sigma_i^2. No gap.")
row("M3b-r1-27", "2.4 math L06 Remark 2.5", L6 + ":227-230", "PASS",
    "(i) (u_i sigma_i)(v_i)^T unchanged under a joint sign flip; (ii) for I_2, U = V = [[0,1],[1,0]] gives U I U^T = I, a second decomposition with singular values 1, 1. Reworded sentence (L06:227-230, changed since round 2) still holds: singular vectors are not unique, singular values are.")
row("M3b-r1-28", "2.4 math L06 problem R1 (A and A^T share nonzero singular values)",
    L6 + ":341-347", "PASS",
    "Argument re-derived: L: E -> E' is injective for lambda > 0 (||Av||^2 = lambda||v||^2) and maps into the AA^T eigenspace (AA^T Av = lambda Av); the symmetric argument gives the reverse inequality; multiplicity equals dimension for symmetric matrices via Lemma 1.3-type eigenbasis (L04 Theorem 2.3); Theorem 2.3 applied to A and A^T gives the nonzero singular values. No gap.")
row("M3b-r1-29", "2.4 misconception counterexamples (L04, L05, L06)",
    L4 + ":279-296; " + L5 + ":317-334; " + L6 + ":242-259", "PASS",
    "L04: N has no orthonormal eigenbasis (Remark 2.7); [[4,1],[1,3]] not diagonal; (1,0),(1,1) for I_2 inner product 1. L05: [[1,2],[2,1]] form -2 at (1,-1) (recomputed); G has eigenvalue 0 with form 0 at (1,1,-1); the tolerance example. L06: [[0,1],[0,0]] singular values 1, 0 (A^TA = diag(0,1), recomputed); zero matrix SVD; sign-change and I_2 decompositions.")
row("M3b-r1-30", "2.4 canon-breaks claims (L04, L05, L06)",
    L4 + ":268-278; " + L5 + ":306-316; " + L6 + ":232-241", "PASS",
    "Each bullet matches a proved result or a lab: L04 symmetry hypothesis (Remark 2.7, Remark 1.6), eigenbasis non-uniqueness (I_2), F1-F4 assumed (stated in L04 section 1), floating-point tolerance (Lab 1). L05 exact vs numerical (Def 3.1), sample refutes but does not prove (Part C), factor not unique (Remark 2.7). L06 vectors not unique (Remark 2.5), wide-matrix zero eigenvalues (R2), rank threshold (Lab 1), low-rank approximation not proved and not claimed.")
row("M3b-r1-31", "2.4 problem set L04 (12 problems, all with solutions)",
    L4 + ":297-400", "PASS",
    "Mechanics M1-M3, Proof P1-P3, Empirical E1-E3, Research R1-R3 (L04:303-400). Recomputed: M1 orthogonality of (1, (-1+sqrt5)/2) and (1, (-1-sqrt5)/2) with <v,w> = 1 + (1-5)/4 = 0; M2 Q Lambda Q^T = [[2,3],[3,2]]; M3 x^TAx = 6 both ways (Fraction check); P3 uses only A^2 = A and v != 0 (correctly stated 'symmetry was not needed'); R2 and R3 checked.")
row("M3b-r1-32", "2.4 problem set L05 (12 problems, all with solutions)",
    L5 + ":335-439", "PASS",
    "M1 (2,1;1,2) eigenvalues 3, 1 from L04 Example 2.6 and L05 Example 2.5; M2 [[1,2],[2,4]] eigenvalues 0, 5 match L03 Problem M2 (L03 mech-2 at L03.html:297-300 uses the same matrix and eigenvectors (2,-1), (1,2)); x=(2,-1) gives 0; M3 eigenvalues 2, 4 and form 4 at (1,1). E1-E3 checked against the printed lab output; R1 O_t construction and R2 sampling argument re-derived.")
row("M3b-r1-33", "2.4 problem set L06 (12 problems, all with solutions) (round-2 FAIL: R2 gap, re-verified)",
    L6 + ":266-362 (R2 at 348-358)", "PASS",
    "Round-2 gap closed: R2 now proves E_0 = {x: A^TAx = 0} = N (||Ax||^2 = x^TA^TAx), so dim E_0 >= n-m by rank-nullity, then counts multiplicity through the orthonormal eigenbasis of A^TA (Theorem 2.3 of L04) and c_j lambda_j = 0. Complete. E2 rank bound and E1 sign flip re-derived; R1 and R3 also checked.")
row("M3b-r1-34", "2.9 cross-references L04 (Example 1.6 of L03; L03 eigendecomposition; L08 uses spectral theorem)",
    L4 + ":37, 51, 97-106, 166, 174; L03.html:96-97, 109, 271, 397; L08.html (Lesson 8 Section 1)", "PASS",
    "L03.html:96 'Example 1.6' is the matrix [[4,1],[1,3]] (eigenvalues (7 +- sqrt5)/2) used in L04 Remark 1.5; L03.html:109 defines eigendecomposition (dfn). L08.html Section 1 defines M = X~^T X~/(T-1) and uses the spectral theorem (L08 meta-row 'Uses: eigendecomposition, spectral theorem').")
row("M3b-r1-35", "2.9 cross-references L05 (L05 Example 2.6 vs L04 Example 2.6; Problem M2 of L03; Lesson 1 standard basis)",
    L5 + ":37, 51, 97, 109, 115, 140, 149-156, 224-225", "PASS",
    "L05 Example 2.6 (L05.html:154-157, eigen test on Example 1.7) is the L05 example the L05 text cites; L05 Example 2.5 (L05.html:149-152) and mech-1 (L05.html:341-347) cite 'Example 2.6 of Lesson 4' with the L04 meaning. L05 Prop 1.6 proof uses e_i 'Lesson 1' = L01 Example 3.9 (L01.html:183). L03 Problem M2 matrix [[1,2],[2,4]] matches L05 M2 (L03.html:297-300).")
row("M3b-r1-36", "2.9 cross-references L06 (span Lesson 1, Lesson 4 Lemma 1.3, Lesson 8)",
    L6 + ":38, 52, 80, 85, 112, 137, 238, 255, 345, 355", "PASS",
    "'span as defined in Lesson 1' = L01 Definition 2.1 (L01.html:92-95); 'Lesson 4, Lemma 1.3' = orthonormal vectors independent (L04.html:78-86); Lesson 8 statements at L06:52 and L06:238 match L08 Section 1 (M matrix) and L08 not using the SVD (L08 has no SVD use; its only 'singular' mention refers to Lesson 6 sign freedom).")
row("M3b-r1-37", "2.9 DAG and concept definitions (check_dag and unit-wide grep)",
    L4 + ":130; " + L5 + ":72; " + L6 + ":101; tools/check_dag.py --unit M3", "PASS",
    f"{GATES}: check_dag M3 PASS (exit 0). {DAG}: concept names and ids outside the closure {{M1, P0.1}} (1101 concepts scanned) occur in L04-L06 pages: none; the only card hits are 'correlation' in L09 cards (c146-c208 range) and 'independence' in L01 card M3-c022; none in the L04-L06 pages or in the 62 slice cards. Each dfn is defined once (L04 def-spectral-theorem, L05 def-positive-semidefinite-matrix, L06 def-singular-value-decomposition; {INV}).")
row("M3b-r1-38", "2.9 DAG B4 (no Cholesky, no IEEE 754 theory) and B1-B3 (M4 terms)",
    "L04-L06 pages and twins; plans/M3-build-plan.md section 9 B4", "PASS",
    f"{S}word_scan.out (scan of covariance, correlat, variance, expectation, cholesky, IEEE, principal, portfolio, shrinkage, regression, etc. in L04-L06 pages): 'floating-point' appears only as a tolerance remark (L05:51, :185, :330; L06:237); no 'Cholesky', no 'IEEE', no covariance/correlation/variance/expectation/portfolio in the pages. Cards hits for 'correlation' are in L09 cards.")
row("M3b-r1-39", "2.9 undefined plain terms before first use (define-before-use)",
    L4 + ":51; " + L5 + ":51; " + L6 + ":52", "PASS",
    f"Plain terms are defined in the pages or in the lesson's earlier sections (vector space, span, basis, dimension, orthonormal, Gram matrix, quadratic form, column space, rank). The why-it-matters paragraphs name later definitions with explicit pointers ('Definition 1.1 below', 'defined in Section 2'). {FWD}: this pointer pattern appears in 49 of 203 lesson pages across the course, so it is the repo convention and is not failed here.")
row("M3b-r1-40", "2.4/2.9 notation: symbol meanings vs notation/notation.json (program-wide symbols)",
    "L04-L06 math; notation/notation.json", "PASS",
    f"{INV}: registered macros used: \\R, \\diag, \\tr (all registered). Plain letters: T appears only as the observation count of the registered symbol (L06 canon-breaks, M = X~^TX~/(T-1)); N, M, E, R, Q, Sigma, Lambda, tau, sigma are local and defined where used (L04 Remark 2.7 N; L05 Def 3.1 tau; L06 sigma and Sigma in Theorem 2.2). No registered symbol (R_f, R^*, R^{{e*}}, \\mathbb{{Q}}, Phi, gamma_3, gamma_4, \\E, \\Var, \\Cov) takes another meaning: \\mathbb{{Q}} is not used in the slice, and plain R (rotation matrix, L04 Remark 1.6) is not a registered symbol.")
row("M3b-r1-41", "2.9 registered macros: \\diag at L04:176 (round-1 FAIL, re-verified)",
    L4 + ":176 (open); " + L6 + " (round-1 lines 106, 132, 270, 293, 422)", "PASS",
    f"Round-2 open item: L04:176 used \\mathrm{{diag}}. Now \\diag(w) (grep count of 'mathrm{{diag}}' = 0 in L04, L05, L06; {INV}). notation.json macro '\\\\diag' -> \\operatorname{{diag}} (registered). L06 uses \\diag 6 times, \\tr 7 times, both registered.")
row("M3b-r1-42", "2.9 structure and word count L04", L4 + ":33-521", "PASS",
    f"Order per BUILDER_RULES 4.2 (inventory in {INV}): why it matters (51), core sections 1-2 (53-172), inline Lab 1 (174-266), canon breaks (268), misconceptions 3 (279), problem set 4 tiers x 3 with details.solution (297-400), key results (402-420), quiz 10 items (421-504), references (506). No debate block (no debate key). No word-count gate in this slice.")
row("M3b-r1-43", "2.9 structure and word count L05", L5 + ":33-545", "PASS",
    f"why it matters (51), core sections 1-3 (53-173), inline Lab 1 (175-305), canon breaks (306), misconceptions 3 (317), problem set 4 tiers x 3 (335-439), key results (440-457), quiz 10 items (459-538), references (540). No debate key. Order per BUILDER_RULES 4.2.")
row("M3b-r1-44", "2.9 structure and word count L06", L6 + ":33-465", "PASS",
    f"why it matters (52), core sections 1-2 (54-133), inline Lab 1 (135-225), remark 2.5 (227), canon breaks (232), misconceptions 3 (242), problem set 4 tiers x 3 (260-362), key results (366-382), quiz 9 items (384-454), references (456). Order per BUILDER_RULES 4.2 ({INV}).")
row("M3b-r1-45", "2.9 hours arithmetic (hub split vs lessons)",
    "course/modules/M/M3/index.html data-hours-lessons=105, data-hours-project=45; L01-L09 data-hours", "PASS",
    f"{INV}: L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12 = 105 = data-hours-lessons; data-hours-project = 45; total 150 = curriculum. Hours are design targets; no arithmetic conflict.")
row("M3b-r1-46", "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "L04-L06 pages, cards, twins", "PASS",
    f"{BAN}: no TODO, TBD, lorem, 'for brevity', 'details omitted', 'beyond the scope', 'left as an exercise', 'you can add more', 'it is important to note', 'studies show', 'experts agree', 'it is well known', 'obviously', 'clearly', 'it can be shown' in the slice. Only hits: scope 'for every' (verified above) and mathematical list ellipses in cards (c070 line 475, c103 693, c105 707, c106 714, c107 721) that are sequence notation, not omitted content.")
row("M3b-r1-47", "2.9 banned ellipsis in learner prose (round-1 FAIL, re-verified)",
    L6 + ":402 (round-1)", "PASS",
    f"{INV}: '…' count 0 and '...' count 0 in L04, L05, L06 HTML. The round-1 instance is gone.")
row("M3b-r1-48", "2.9 page_smoke L04-L06 (alone)", "tools/page_smoke.py --unit M3 --pages L04 L05 L06", "PASS",
    f"{PS}: 'page_smoke modules/M/M3/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke M3: PASS', exit=0 (Chromium headless, light and dark, 360 px, Pyodide labs).")
row("M3b-r1-49", "2.9 check_pages M3", "tools/check_pages.py --unit M3", "PASS",
    f"{GATES}: 'check_pages M3: PASS' exit=0.")
row("M3b-r1-50", "2.9 external requests, figures, data", L4 + ", " + L5 + ", " + L6, "PASS",
    f"{INV}: svg 0, chart 0 on all three pages (no figures); data-cite 0. page_smoke {PS} checks zero requests to any host other than the local server, PASS.")
row("M3b-r1-51", "2.1 citations on the slice pages", L4 + ":506-510; " + L5 + ":540-544; " + L6 + ":456-460", "PASS",
    f"data-cite count 0 and no claim span with a citation in L04-L06 ({INV}). Each reference section says no passage locator was read and no claim is attributed to axler2024linear or strang2023introduction. {S}verify_refs_offline.out: 560 entries, 0 problems.")
row("M3b-r1-52", "2.9 process words in learner text", "L04-L06 pages, twins and slice cards", "PASS",
    f"{BAN} (process-word patterns: round, verifier, builder, architect, ledger, agent, planner, B1-B4, DATA_REQUEST, REFERENCE_REQUEST, previous round, fixed in): no hits in L04-L06, labs or slice cards.")
row("M3b-r1-53", "2.9 quiz structure (items, explanations, answers)",
    L4 + ":421-504 (10 items); " + L5 + ":459-538 (10 items); " + L6 + ":384-454 (9 items)", "PASS",
    "Every item has an explanation (hidden div.explain) and a correct option or numeric answer: L04 answers 6, 0.7071 (tol 5e-5), 2, mc options; L05 answers 1, -2, 3, 1; L06 answers 5, 8, 30, 2 with mc options. Each numeric answer recomputed (recheck_numbers_r3.out; L06 Frobenius 1+4+9+16 = 30).")
row("M3b-r1-54", "2.7 cards L04 (20 cards read in full)",
    CD + ": M3-c063..c078, c189, c190, c192, c215", "PASS",
    f"All 20 read in {CARDS}. Each back checked against the L04 text: definitions (c063-c065, c189, c190, c215), Lemma 1.3, 1.4, 2.1, 2.2, Theorem 2.3, Prop 2.4, Cor 2.5 (hypotheses listed), Remark 2.7 and Remark 1.6 (c073, c076), lab cards c074/c075 (200 of 200, 1200 of 1200 with basis), misconceptions c076-c078. Grades: T for every theorem card; C with basis for lab cards; no cite. Near-duplicate pairs from {DUP} (c063/c081, c064/c190, c067/c192, c077/c112, c072/c089) test different facts.")
row("M3b-r1-55", "2.7 cards L05 (27 cards read in full)",
    CD + ": M3-c079..c100, c173, c179, c180, c193, c203", "PASS",
    f"All 27 read in {CARDS} (c176 is no longer in the file; round-2 count of 28 included it). Back checked against L05 text: Remark 1.2, Def 1.1, 1.3, 1.4, Props 1.5, 1.6, Theorems 2.1 and 2.2 (hypotheses), Prop 2.3, 2.4, Remark 2.7, Def 3.1, Remark 3.2 (c093), lab cards c094-c097 and c173, c179 (basis named), misconceptions c098-c100. Card c100 has no grade field (its sibling misconceptions c098, c099 carry T); noted, not failed. Numbers 118, 500, 100000, 1 and 0.0000 match the expected block.")
row("M3b-r1-56", "2.7 cards: round-1 duplicate pair M3-c085 vs M3-c098 (round-1 FAIL, re-verified)",
    CD + ": M3-c085 (L05), M3-c098 (L05)", "PASS",
    f"c085 asks what Theorem 2.1 concludes for [[1,2],[2,1]]; c098 is the misconception 'positive entries imply PSD' with the same matrix. They test different questions (theorem conclusion vs misconception). {DUP}: no pair with same front; the Jaccard flag between them is below 0.45. Not a duplicate.")
row("M3b-r1-57", "2.7 cards L06 (15 cards read in full; round 2 counted 16 with c101)",
    CD + ": M3-c103..c114, c178, c205, c216", "PASS",
    f"All 15 read in {CARDS}. c101 is absent from the file (the round-2 L06 duplicate of M3-c215 is gone; {INV} lists the ids absent). Each back checked: Lemma 1.3 (c103), Prop 2.1 (c104), Theorem 2.2 (c105, hypotheses m, n >= 1 and F1-F4), Theorem 2.3 (c106), Prop 2.4 (c107), Remark 2.5 (c108, c114), lab cards c109-c111 (basis named, grade C), misconceptions c112-c114, c178 (rank), c205 (Fact 1.2), c216 (naming).")
row("M3b-r1-58", "2.7 grades and basis on slice cards",
    CD + ": C cards c074, c075, c094-c097, c109-c111, c173, c179", "PASS",
    f"{INV}: slice grades T 38, C 11, none 13 (definitions c063-c065, c079, c081, c082, c092, c189, c190, c193, c215, c216, and c100). Each C card has a 'basis' naming the lab and part (c074, c075, c094-c097, c109-c111, c173, c179). No card has a 'cite'.")
row("M3b-r1-59", "2.7 numbers on cards appear in the lesson",
    CD + " slice entries vs L04-L06 text and expected blocks", "PASS",
    "200 of 200 and 1200 (c074, c075: L04 hypothesis L04:176, key row L04:415, expected 256-264); 0.7071 (c073: L04 Remark 2.7 and E3); 118 of 360 and one third (c095: L05:303 and E2 L05:402); 500 of 500 and 100000 (c096, c173: L05 expected block and key row); 0.0000, 1.0000, 3.0000 and one near-zero eigenvalue (c097: L05 E3 L05:407-409 and expected block); 2.2335, 0.9250, 0.3348 and two singular values (c110, c111: L06 expected 216-223 and key row 378); ten matrices (c109: L06:137).")
row("M3b-r1-60", "2.7 card coverage and ids",
    CD + " (208 cards in file; 62 in slice)", "PASS",
    f"{INV}: total 208; L04 20, L05 27, L06 15 (slice 62). Round-2 record counted 64 slice cards including the two round-2 duplicates c101 and c176, both now absent. Every lesson result has a card (Definitions, Lemmas, Theorems, Props, Remarks, lab results, misconceptions) per BUILDER_RULES section 7. Ids: c101, c102, c176 absent; no duplicate ids (DUP).")
row("M3b-r1-61", "2.7 cross-lesson near duplicates (full scan of all 208 cards)",
    CD + " whole file; " + DUP, "PASS",
    f"{DUP}: 208 cards, distinct ids, no same-front pair. Jaccard >= 0.45 flags reviewed for slice cards: c082/c193 (PSD vs PD definitions), c087/c088 (PSD vs PD theorems), c067/c192 (Lemma 1.4 two claims), c063/c081, c064/c190, c077/c112, c072/c089, c085/c088, c096/c173, c085/c087, c079/c081, c083/c131 (L08 cross-lesson), c089/c154 (L09), c131/c193 (L08/L05). Each pair asks different facts. Round-2 duplicates c101 and c176 removed.")
row("M3b-r1-62", "gate verify_refs (offline)", "tools/verify_refs.py --offline", "PASS",
    f"{S}verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. (The --unit form is live-only; the earlier gates_fast.out line 'verify_refs --unit M3' exit=2 was a wrong invocation and is superseded by this run.)")
row("M3b-r1-63", "2.8 figures (slice pages)", L4 + ", " + L5 + ", " + L6, "PASS",
    f"No figures or charts in L04-L06 ({INV}: svg 0, chart 0). Nothing to sweep; page_smoke {PS} PASS.")
row("M3b-r2-64", "2.7 cards: duplicate definition of an orthogonal matrix (round-2 FAIL, re-verified)",
    CD + ": M3-c215 (L04); M3-c101 (L06, round 2)", "PASS",
    f"c101 is absent from cards.json ({INV}). c215 (L04, 'When is a real square matrix Q orthogonal?') is the only card for the orthogonal-matrix definition. L06 Definition 1.1 has no card. Not a duplicate now.")
row("M3b-r2-65", "2.7 cards: duplicate eigenvalues of [[1,2],[2,1]] (round-2 FAIL, re-verified)",
    CD + ": M3-c085 (L05); M3-c176 (L05, round 2)", "PASS",
    f"c176 is absent from cards.json ({INV}). c085 is the only card for the Theorem 2.1 conclusion on [[1,2],[2,1]]. Not a duplicate now.")
row("M3b-r3-66", "2.5 lab docstring claim vs printed output (new in round 3): L06 'Tolerances are absolute and stated in each printed line'",
    "tests/labs/M3/lab-M3-L06-1.py:4 and :74-75; " + L6 + ":141 (page copy of the docstring)", "FAIL",
    "The docstring says every printed line states its tolerance. The sign-flip line prints 'flipping the signs of the first singular pair still reconstructs A: True' (twin line 75) but its tolerance 1e-12 (line 74, np.max(...) < 1e-12) is not printed. The other tolerance-using lines print their tolerance (lines 53-56, 65). Verified by reading the twin and page (" + TWIN + " prints the same line without a tolerance).",
    "Either print the tolerance on the sign-flip line (for example f\"flipping the signs of the first singular pair still reconstructs A to 1e-12: {bool(still_a)}\") or change twin line 4 to 'Tolerances are absolute and stated in each printed line that uses one'. Then run .venv/bin/python tools/embed_labs.py course/modules/M/M3/L06.html --refresh lab-M3-L06-1, re-run run_labs --unit M3 --page L06, twin_vs_page, and page_smoke for L06.")

notes = [
    "Method: full read of course/modules/M/M3/L04.html (521 lines), L05.html (555 lines), L06.html (471 lines) and cards.json (all 62 slice cards read from " + CARDS + "). Twins tests/labs/M3/lab-M3-L04-1.py, lab-M3-L05-1.py, lab-M3-L06-1.py read in full. Delta since round-2 pin 9294b914 read in full: L04:176 (\\mathrm{diag} -> \\diag), fieldset style attributes (L04, L05, L06), L05:51 why-it-matters wording, L06:227-230 Remark 2.5 wording, L06:348-358 problem R2 rewritten, cards.json (c101 and c176 removed). No row is carried: every row was re-verified in round 3, so no 'Carried from round' prefix is needed.",
    "Gates on the pinned checkout (" + GATES + "): check_pages --unit M3 PASS; check_dag --unit M3 PASS; check_projects --unit M3 PASS; run_labs --unit M3 --page L04, L05, L06 each PASS (1/1); ruff check and ruff format --check tests/labs/M3 PASS; mypy --no-incremental PASS (385 files). verify_refs --offline (" + S + "verify_refs_offline.out) 560 entries, 0 problems. pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py with -k filter (" + S + "pytest_relevant.out) exit 0. page_smoke --unit M3 --pages L04 L05 L06 (" + PS + ") PASS.",
    "Lab checks (" + TWIN + "): each twin run alone with python -I -W error exits 0 with empty stderr; each page's code block equals its twin; each expected block equals the twin's output. Numbers re-derived independently in " + NUM + " (orthogonality, reconstruction, residual, imaginary-part and pair margins; Part B 118/4/-1; Part C 500/500 and 100000/100000; Part D eigenvalues 0, 1, 3; seed-0 SVD 2.2335/0.9250/0.3348; planted rank count 2; Fraction checks of the Example and problem numbers).",
    "Mutants: none. This slice has no project grader; VERIFIER_RULES 2.6 and the ruling apply mutation testing to project graders only, and lab twins are demonstrations. The 'mutants' list is empty by design, not by omission.",
    "Convention accepted, not failed: why-it-matters paragraphs in L04, L05, L06 name later definitions with explicit pointers ('Definition 1.1 below', 'defined in Section 2'). " + FWD + " shows this pattern in 49 of 203 lesson pages across the course.",
    "Math-ellipsis convention accepted: cards c070, c103, c105, c106, c107 use '...' style sequence notation (x_1, ..., x_n) that is standard mathematics, not omitted content (" + BAN + ").",
    "Hours: L04 12, L05 12, L06 11 match their data-hours; the lesson sum 105 equals the hub split (" + INV + ").",
    "Cards: card M3-c100 (misconception on floating-point eigenvalues) has no grade field while its siblings c098 and c099 carry T. Not a failure of any rule; a consistency fix for the builder.",
    "Round-2 FAIL rows M3b-r1-33, M3b-r1-41, M3b-r1-61, M3b-r2-64, M3b-r2-65 are re-verified PASS in this round (R2 completed; \\diag at L04:176; duplicate cards removed).",
    "Only new FAIL in round 3: M3b-r3-66 (L06 lab docstring says every printed line states its tolerance; the sign-flip line does not). Fix is in the twin and requires embed_labs --refresh; the page code must be re-embedded from the twin, not hand-edited.",
    "Not checked: (1) run_graders and mutate_graders (project-only; this slice has no grader); (2) the full gate (render_curriculum, build_site --check, fetch_data --check, the complete pytest suite, page_smoke --all, verify_refs live run) which is outside slice b and was not run; (3) L01-L03, L07-L09 pages beyond the cross-reference lines cited; (4) a visual screenshot diff in light and dark mode beyond page_smoke's own checks; (5) live Crossref or publisher checks (offline only, per the ruling); (6) no source is cited in the slice, so no registry locator was read; (7) the exact line of L08 Section 1 that defines M was located by text search, not by a numbered anchor.",
]

summary = ("Slice b (M3 L04-L06 pages, lab twins and their 62 slice cards), round 3, pin 8196077d: FAIL. "
           "Rows: 66 total, 65 PASS, 1 FAIL (M3b-r3-66: L06 lab docstring says every printed line states its tolerance; the sign-flip line does not). "
           "All round-2 FAIL rows (M3b-r1-33, M3b-r1-41, M3b-r1-61, M3b-r2-64, M3b-r2-65) are fixed and re-verified PASS. "
           "Every lab twin runs under python -I -W error, each page's code equals its twin and each expected block equals the output; all printed numbers and every proof re-derived; page_smoke PASS; check_pages, check_dag, check_projects, run_labs, ruff, mypy, verify_refs offline PASS.")

frag = {
    "unit": "M3",
    "slice": "b",
    "round": 3,
    "verifier": "independent Haiku verifier, slice b (did not build M3)",
    "pin": "8196077d5f56c3919d33e69888176d197d378ad4",
    "base": "9294b914a51647c66d2dee62c4a112c76ba04900 (round-2 pin; round-2 fragment /Users/billyribeiro/.fanout/frags/S-M3-b.round2.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS3-M3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS3-M3-b/ledgers/M3/scripts/M3-b-r3",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}
with open("ledgers/M3/M3-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows:", len(R), "PASS:", sum(r["status"] == "PASS" for r in R), "FAIL:", sum(r["status"] == "FAIL" for r in R))
