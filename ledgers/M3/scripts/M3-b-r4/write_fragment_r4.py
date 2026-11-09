"""Writes the round-4 fragment ledgers/M3/M3-b.json (slice b, unit M3). Rows are the round-4 verdicts; evidence cites
scripts and outputs under ledgers/M3/scripts/M3-b-r4/."""
import json
import sys

ROOT = sys.argv[1]
S = "ledgers/M3/scripts/M3-b-r4/out/"
R = []


def row(i, check, loc, status, evidence, fix=None):
    d = {"id": i, "check": check, "location": loc, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix
    R.append(d)


P = "PASS"
F = "FAIL"

row("M3b-r1-01", "2.5-lab L04: structure, hypothesis, code, expected block, interpretation",
    "course/modules/M/M3/L04.html:174-265; tests/labs/M3/lab-M3-L04-1.py",
    P, "Page and twin read in full this round. " + S + "twin_vs_page_r4.out: L04 expected_equals_output=True, exit=0, "
    "stderr_bytes=0 under python -I -W error. " + S + "diff_twin_page_r4.out: page code equals twin after the trailing "
    "newline that embed_labs strips. " + S + "run_labs_L04.out: run_labs M3 PASS (1/1). Hypothesis (L04:176) matches the "
    "printed lines: 200 of 200 four times, 1200 pairs, rotation True, 0.7071.")

row("M3b-r1-02", "2.5 lab interpretation L04 against what the lab prints",
    "course/modules/M/M3/L04.html:265 vs expected block 256-264",
    P, "L04:265 says the lab prints counts at tolerance 1e-10, not raw residuals; the twin prints counts only "
    "(tests/labs/M3/lab-M3-L04-1.py:58-76). Expected block equals run output (" + S + "twin_vs_page_r4.out).")

row("M3b-r1-03", "2.5-lab L05 structure and twin run",
    "course/modules/M/M3/L05.html:175-304; tests/labs/M3/lab-M3-L05-1.py",
    P, S + "twin_vs_page_r4.out: L05 expected_equals_output=True, exit=0, stderr 0. " + S + "run_labs_L05.out: PASS (1/1). "
    "Twin read in full (113 lines). Hypothesis L05:177 matches the prints (Parts A-D).")

row("M3b-r1-04", "2.5 lab interpretation L05 states what the lab prints (0.0000 rule)",
    "course/modules/M/M3/L05.html:303 vs expected block 291-301; twin part_d lines 93-103",
    P, "L05:303 says a singular-matrix value within 1e-10 of zero prints as 0.0000. Twin part_d prints "
    "'0.0 if abs(values[0]) <= TOL else values[0]' at :.4f (lab-M3-L05-1.py:98-100). " + S + "twin_vs_page_r4.out shows "
    "'0.0000 1.0000 3.0000' and 'eigenvalues with absolute value at most 1e-10: 1'. The sign masking this produces is what "
    "makes M3b-r4-67 (card c100) unsupported; the row's own statement is accurate.")

row("M3b-r1-05", "2.5-lab L06 structure and twin run",
    "course/modules/M/M3/L06.html:135-225; tests/labs/M3/lab-M3-L06-1.py",
    P, S + "twin_vs_page_r4.out: L06 expected_equals_output=True, exit=0, stderr 0. " + S + "run_labs_L06.out: PASS (1/1). "
    "Twin read in full (81 lines).")

row("M3b-r1-06", "2.5 lab hypothesis and interpretation L06 against twin and output",
    "course/modules/M/M3/L06.html:137, 227 vs twin lines 55-78",
    P, "L06:137 lists the four identity checks at 1e-12 and 1e-10, ten seeded matrices, the seed-0 singular values, the "
    "planted rank-2 count and the sign flip; twin lines 55-78 print exactly these, and the sign-flip line now states "
    "'to 1e-12' (twin line 78). L06:227 'print True for these ten matrices' matches " + S + "twin_vs_page_r4.out.")

row("M3b-r1-07", "2.5 twin lint, format and types",
    "tests/labs/M3/lab-M3-L04-1.py, lab-M3-L05-1.py, lab-M3-L06-1.py",
    P, S + "ruff_check_labs.out: 'All checks passed!' EXIT=0. " + S + "ruff_format_labs.out: '12 files already formatted' "
    "EXIT=0. " + S + "mypy.out: 'Success: no issues found in 385 source files' EXIT=0.")

row("M3b-r1-08", "2.5 lab runtime, no network, seeded RNG only",
    "three twins; " + S + "page_smoke_L04_L06.out",
    P, S + "page_smoke_L04_L06.out: lab timings under 0.1 s each. Twin imports read in full: L04 numpy only; L05 math and "
    "numpy; L06 numpy only. Seeds: L04 default_rng(2604) (line 40); L05 default_rng(SEED=2604) (line 74); L06 "
    "default_rng(seed), default_rng(100+seed), default_rng(0), default_rng(7), default_rng(8) (lines 49-70).")

row("M3b-r1-09", "2.5 lab scope sentences name their tested sample",
    "course/modules/M/M3/L04.html:265; L05.html:303; L06.html:227, 327",
    P, "L04:265 scopes the claims to the 200 seeded 4x4 matrices and 1200 pairs (twin SEED, N_MATRICES). L05:303 says a "
    "sample refutes but cannot prove and that Theorem 2.1 covers all vectors (twin Part C, 500 x 200). L06:227 calls the "
    "ten-matrix check finite and seeded, not a proof of Theorem 2.2.")

row("M3b-r1-10", "2.2 printed and prose numbers L04 re-derived",
    "course/modules/M/M3/L04.html:51, 97-106, 164-172, 176, 256-265, 268-278, 297-420",
    P, S + "recheck_numbers_r4.out (script ledgers/M3/scripts/M3-b-r4/recheck_numbers_r4.py): Example 2.6 gives "
    "QLambdaQ^T = [[2,1],[1,2]], y = (1/sqrt2, 1/sqrt2), sum lambda_j y_j^2 = 2; Remark 2.7 |<.,.>| = 1/sqrt2 = 0.7071067812; "
    "Remark 1.6 characteristic polynomial lambda^2+1; M1 inner product 0 and eigenvalues (7 +/- sqrt5)/2; M2 gives "
    "[[2,3],[3,2]]; M3 gives 6 both ways; R1 z*Rz = 2i. C(4,2) = 6, 200 x 6 = 1200.")

row("M3b-r1-11", "2.2 printed and prose numbers L05 re-derived",
    "course/modules/M/M3/L05.html:177, 291-303, 391-409, 453",
    P, S + "recheck_numbers_r4.out: 1 + 2 sin 2t matches the form to 8.9e-16; negative grid count 118, zero count 4 at "
    "105, 165, 285, 345 degrees; 118/360 = 0.3278 against one third; grid minimum -1.0; Example 2.5 B^T B = [[2,1],[1,2]]; "
    "Example 2.6 eigenvalues -1, 3; Remark 3.2 eigenvalues 0, 1, 3; M2 eigenvalues 0, 5; M3 eigenvalues 2, 4 and form 4 at "
    "(1,1). Part C counts (500 of 500; 100000 of 100000) are twin outputs (" + S + "twin_vs_page_r4.out).")

row("M3b-r1-12", "2.2 printed and prose numbers L06 re-derived",
    "course/modules/M/M3/L06.html:216-224, 261-300, 316-335, 384-455",
    P, S + "recheck_numbers_r4.out: seed-0 singular values unrounded 2.2334970848, 0.9249716026, 0.3348254752, which round "
    "to 2.2335, 0.9250, 0.3348 (no value within 0.2 units of a rounding boundary at the fourth decimal); planted singular "
    "values 5.28, 0.578, 4.3e-16, count above 1e-10 relative = 2; M1 A^TA = diag(9,16), sigma = 4, 3; M2 A^TA eigenvalues "
    "0, 2; E3 A^TA eigenvalues 0, 25, sigma = 5; Frobenius of [[1,2],[3,4]] = 30; ||2I_2||_F^2 = 8; [[0,1],[0,0]] gives "
    "A^TA = diag(0,1).")

row("M3b-r1-13", "2.2 scope words (every, all, only, exactly, never, same, any, always)",
    "course/modules/M/M3/L04.html, L05.html, L06.html prose",
    P, S + "prose_scan_r4.out (script ledgers/M3/scripts/M3-b-r4/prose_scan_r4.py) counts each scope word; every "
    "occurrence was read in context. Examples: L05:303 'Theorem 2.1 covers all vectors' (Theorem 2.1 is proved for all "
    "vectors); L06 R3 'infinitely many' (proved with rotations); L05 Remark 2.7 'at least two factors' (proved). No "
    "unsupported scope word found.")

row("M3b-r1-14", "2.2 rounding: displayed digits come from unrounded values",
    "printed decimals in L04-L06 pages and twins",
    P, S + "recheck_numbers_r4.out: 1/sqrt2 = 0.70710678 shown as 0.7071; 118/360 = 0.32777... shown as 0.3278; seed-0 "
    "singular values rounded from unrounded values (see M3b-r1-12); the 0.0000 rule is the twin's explicit "
    "'0.0 if abs(values[0]) <= TOL' branch.")

row("M3b-r1-15", "2.3 grades L04",
    "course/modules/M/M3/L04.html:78-155, 402-416",
    P, "Lemmas 1.3, 1.4, 2.1, 2.2, Theorem 2.3, Proposition 2.4, Corollary 2.5 are graded T and proved on the page "
    "(L04:78-155). Remark 2.7's 1/sqrt2 is T in the key-results row (L04:415 area). The lab row (C) names Lab 1, seed 2604.")

row("M3b-r1-16", "2.3 grades L05 (key-results and lab rows)",
    "course/modules/M/M3/L05.html:107-173, 440-457 (row at L05.html:453)",
    F, "Theorem, Proposition and Remark grades T in L05 are correct (Props 1.5, 1.6; Thms 2.1, 2.2; Props 2.3, 2.4; Remarks "
    "2.7, 3.2). The key-results row at L05:453 is graded C and includes 'the tolerance test rejects [[1,2],[2,1]]' and "
    "'the rank 2 Gram matrix has one near-zero eigenvalue'. Both are derived by hand on the page (Example 2.6 at L05:154-156, "
    "Remark 3.2 at L05:171-173), so ruling 13 requires T for them. Severity LOW (not in ruling 26's blocking list).",
    "Split the row at L05:453: T row for the Example 1.7/2.6 facts and the Remark 3.2 count (basis: those numbered blocks); "
    "C row only for the printed lines (True, 118 of 360, 500 of 500, 100000 of 100000). Mirror in cards per M3b-r4-68.")

row("M3b-r1-17", "2.3 grades L06",
    "course/modules/M/M3/L06.html:63-133, 366-382",
    P, "Fact 1.2 (L06:64), Lemma 1.3 (L06:74), Proposition 2.1 (L06:88), Theorems 2.2 (L06:97) and 2.3 (L06:116), "
    "Proposition 2.4 (L06:125) are T with proofs on the page. Key-results rows (L06:372-380) are T for theorems and C "
    "for the lab row, which names Lab 1.")

row("M3b-r1-18", "2.4 math L04 core: Lemmas 1.3, 1.4, 2.1, 2.2, Theorem 2.3 proof",
    "course/modules/M/M3/L04.html:77-142",
    P, "Read line by line. Lemma 2.1 index-swap conjugate argument (L04:116) uses symmetry and realness; Lemma 2.2 uses F2 "
    "for a complex root, F1 for a null vector and real/imaginary parts (L04:126); Theorem 2.3 induction: W = null space of "
    "q^T has dimension n-1 by F4 (L04:137), W invariant (L04:138), S symmetric (L04:138), u_j eigenvectors (L04:139), "
    "n orthonormal vectors form a basis (L04:140), A = Q Lambda Q^T (L04:141). No gap.")

row("M3b-r1-19", "2.4 hypotheses L04 Proposition 2.4 (field of the vectors)",
    "course/modules/M/M3/L04.html:144-152; Definition 1.2 at L04.html:73-76",
    P, "Statement (L04:146) gives A real symmetric, v, w in R^n, real lambda != mu; proof (L04:151) uses only symmetry and "
    "the two eigen-equations, so every hypothesis used is stated.")

row("M3b-r1-20", "2.4 math L04 Corollary 2.5, Example 2.6, Remarks 1.5, 1.6, 2.7",
    "course/modules/M/M3/L04.html:97-106, 154-172",
    P, "Recomputed in " + S + "recheck_numbers_r4.out: Example 2.6 QLambdaQ^T and y = Q^T x; Remark 1.5 entries; Remark 1.6 "
    "characteristic polynomial; Remark 2.7 eigenspaces (1,0) and (1,1), inner product 1/sqrt2 (not zero).")

row("M3b-r1-21", "2.4 math L05 core: Remark 1.2, Propositions 1.5, 1.6, Example 1.7, Remark 1.8, Theorems 2.1, 2.2",
    "course/modules/M/M3/L05.html:55-127",
    P, "Read in full. Remark 1.2 (L05:62) transposes a 1x1 matrix; Prop 1.5 (L05:82); Prop 1.6 (L05:92); Example 1.7 "
    "value -2 (L05:97, recheck: 1 - 4 + 1); Remark 1.8 M gives x1^2 + x2^2 and characteristic polynomial lambda^2 - 2 lambda + 2 "
    "(L05:102); Theorem 2.1 (=>) uses a nonzero real eigenvector (L05:114) and (<=) uses Corollary 2.5 (L05:115); Theorem 2.2 "
    "(<=) uses Q invertible so y != 0 (L05:125). Hypotheses stated.")

row("M3b-r1-22", "2.4 math L05 Propositions 2.3, 2.4, Example 2.5, Remark 2.7",
    "course/modules/M/M3/L05.html:128-161",
    P, "Proposition 2.3 proof (L05:135): lambda_j y_j^2 = 0 gives lambda_j y_j = 0, so Lambda y = 0 and Ax = 0. Proposition "
    "2.4 (L05:145) gives B = Lambda^{1/2} Q^T with B^T B = A. Example 2.5 entries 2, 1, 2 (recheck). Example 2.6 eigenvalues "
    "3, -1 (L05:155). Remark 2.7 (L05:160) (OB)^T(OB) = A.")

row("M3b-r1-23", "2.4 math L05 Definition 3.1 and Remark 3.2",
    "course/modules/M/M3/L05.html:165-173",
    P, "Remark 3.2 expansion (1-lambda) lambda (lambda-3) confirmed (recheck eigenvalues 0, 1, 3); B(1,1,-1) = (0,0) so "
    "(1,1,-1) is an eigenvector for 0; Prop 1.5 gives PSD; Theorem 2.2 gives not PD (L05:172). Definition 3.1 is a decision "
    "rule and the twin implements it (lab-M3-L05-1.py:98-103).")

row("M3b-r1-24", "2.4 math L06 core: Fact 1.2, Lemma 1.3, Proposition 2.1",
    "course/modules/M/M3/L06.html:58-95",
    P, "Fact 1.2 proof (L06:70): F1 applied to M = Q^T and N = Q. Lemma 1.3 proof (L06:80): Gram-Schmidt accept/discard "
    "argument, span and independence, and the count m via Lesson 1 Example 3.9 and Theorem 3.8 (L01.html:173-185 read: "
    "Theorem 3.8 invariance of dimension; Example 3.9 standard basis of dimension n). Proposition 2.1 proof (L06:94) uses "
    "(Az)^* = z^* A^T for real A.")

row("M3b-r1-25", "2.4 math L06 Theorem 2.2 (SVD) proof, Steps 1-5",
    "course/modules/M/M3/L06.html:97-113",
    P, "Read step by step. Step 2 (L06:109): orthonormality chain of u_j verified; r <= m from Lemma 1.3 and dimension. "
    "Step 4 (L06:111): lambda_j = 0 gives Av_j = 0, columns agree. Step 5 (L06:112): VV^T = I by Fact 1.2; column space "
    "equals span(u_1..u_r); rank r. No missing hypothesis.")

row("M3b-r1-26", "2.4 math L06 Theorem 2.3 and Proposition 2.4",
    "course/modules/M/M3/L06.html:115-133",
    P, "Theorem 2.3 proof (L06:122): A^T A = V(Sigma^T Sigma)V^T with U^T U = I; similarity by P^{-1} M P preserves the "
    "characteristic polynomial; V^T V = I. Proposition 2.4 proof (L06:132): trace of A^T A equals the sum of squared entries "
    "(via tr(XY) = tr(YX)). Checked numerically (" + S + "recheck_numbers_r4.out: E3 and M2 checks).")

row("M3b-r1-27", "2.4 math L06 Remark 2.5",
    "course/modules/M/M3/L06.html:227-230 (Remark 2.5 block after the lab)",
    P, "Sign-pair invariance of u_i sigma_i v_i^T is correct; I_2 = U I_2 U^T for orthogonal U by Fact 1.2; U = V = "
    "[[0,1],[1,0]] with Sigma = I_2 gives I_2 with singular values 1, 1 (" + S + "recheck_numbers_r4.out: "
    "'Remark 2.5 I2 SVD check' gives the identity).")

row("M3b-r1-28", "2.4 math L06 problem R1 (A and A^T share nonzero singular values)",
    "course/modules/M/M3/L06.html:345-355",
    P, "Read in full. Map v -> Av is injective on the eigenspace for lambda > 0 and sends it into the eigenspace of AA^T; the "
    "dimension argument runs both ways; multiplicities equal dimensions by the spectral theorem (Lesson 4 Theorem 2.3, "
    "cited explicitly). No gap.")

row("M3b-r1-29", "2.4 misconception counterexamples (L04, L05, L06)",
    "course/modules/M/M3/L04.html:279-296; L05.html:317-334 (misconception 3 at L05.html:329-330); L06.html misconceptions",
    F, "L04 and L06 counterexamples verified (N and I_2 eigenspaces; [[4,1],[1,3]] symmetric; A = [[0,1],[0,0]] has "
    "singular values 1, 0 while both eigenvalues are 0; the zero matrix). L05 misconception 3 (L05:329-330) rests on "
    "'a floating-point solver may return a value near zero with either sign'. The page does not show that (Part D prints "
    "0.0000 by design; L05:303). See M3b-r4-67 (blocking).",
    "Fix M3b-r4-67: grade or evidence the sign claim, and cite that evidence in the misconception paragraph.")

row("M3b-r1-30", "2.4 canon-breaks claims (L04, L05, L06)",
    "course/modules/M/M3/L04.html:268-278; L05.html:306-316; L06.html:232-241",
    P, "Each bullet re-checked. L04: symmetry hypothesis (Remarks 1.6, 2.7), eigenbasis non-unique (I_2 example), F1-F4 assumed, "
    "tolerance 1e-10. L05: Remark 1.8, tolerance decision, sample refutes not proves, factor not unique (Remark 2.7). L06: "
    "vectors not unique (Remark 2.5), m < n padding zeros, rank threshold, Lesson 8 eigendecomposes M = X~^T X~/(T-1) "
    "(L08.html:56-57, Section 1) and does not use the SVD (only a sign-freedom mention at L08.html:293). The symbol "
    "definition issue in L06 bullet 4 is recorded as M3b-r4-69 (LOW).")

row("M3b-r1-31", "2.4 problem set L04 (12 problems, all with solutions)",
    "course/modules/M/M3/L04.html:297-400 (P2 solution at L04.html:339)",
    F, "All twelve problems re-derived (M1-M3 numbers, P1, P3, E1-E3, R1-R3). P2's middle equality (QΛ^{-1}Q^T)(QΛQ^T) = "
    "QΛ^{-1}ΛQ^T uses Q^T Q = I (Definition 1.2), which the solution does not name. Severity LOW.",
    "Add 'using Q^T Q = I (Definition 1.2)' to the L04.html:339 solution (M3b-r4-70).")

row("M3b-r1-32", "2.4 problem set L05 (12 problems, all with solutions)",
    "course/modules/M/M3/L05.html:335-439",
    P, "All twelve re-derived: M1 (eigenvalues 3, 1); M2 (0, 5, form zero at (2,-1)); M3 (2, 4, form 4 at (1,1)); P1; P2; "
    "P3 (Prop 2.3); E1 (-2 = 2 * -1 as a check); E2 (59 + 59 = 118; 120/360); E3 (eigenvalues 0, 1, 3); R1 (Remark 2.7 factors); "
    "R2 (sampling); R3 (Definition 1.4 only). Solutions consistent with the page's statements.")

row("M3b-r1-33", "2.4 problem set L06 (12 problems, all with solutions), R2 gap closed",
    "course/modules/M/M3/L06.html:266-362 (R2 at 384-390)",
    P, "M1 (SVD of diag(3,4) checked by product U diag(4,3) V^T = diag(3,4)); M2 (A^T A eigenvalues 2, 0); M3 (Sigma 3x2); P2; "
    "P3; E1 (sign pair); E2 (seeds 7 and 8, as in twin line 65); E3; R1; R2 now cites Theorem 2.3's orthonormal eigenbasis and "
    "rank-nullity; R3 (I_n infinitely many SVDs). Round-2 R2 gap closed.")

row("M3b-r1-34", "2.9 cross-references L04",
    "course/modules/M/M3/L04.html:37, 51, 97-106, 166, 174; L03.html:96-97, 109, 271; L08.html:38",
    P, "L03.html:96 Example 1.6 is the symmetric matrix [[4,1],[1,3]] with eigenvalues (7 +/- sqrt5)/2 (L03.html:271); "
    "L03.html:109 defines eigendecomposition (anchor def-eigendecomposition); L08.html:38 lists the spectral theorem as used.")

row("M3b-r1-35", "2.9 cross-references L05",
    "course/modules/M/M3/L05.html:37, 51, 97, 109, 115, 140, 149-156, 224-225",
    P, "L05:150 'Example 2.6 of Lesson 4' gives the same Q and Lambda as L04.html:165-166. L05 M1 'Problem M2 of Lesson 3': "
    "the L03 M2 matrix is [[1,2],[2,4]] with eigenvalues 0 and 5 (L03.html:298-308). 'Lesson 1 standard basis' (L05:92) "
    "matches L01 Example 3.9 (L01.html:183-186).")

row("M3b-r1-36", "2.9 cross-references L06",
    "course/modules/M/M3/L06.html:38, 52, 80, 85, 112, 137, 238, 241, 345, 355",
    P, "L06:80 Lesson 1 Example 3.9 and Theorem 3.8 (L01.html:173-185); L06:85 span as in Lesson 1 Definition 2.1 "
    "(L01.html:92); L06:112 Lesson 4 Lemma 1.3 (L04.html:78); L06:52 Lesson 8 uses the spectral theorem on data "
    "(L08.html:56-57); L06:241 Lesson 8 Section 1 (L08.html:56-57). All targets exist with the cited content.")

row("M3b-r1-37", "2.9 DAG and concept definitions",
    "course/modules/M/M3/L04.html:130; L05.html:72; L06.html:101; check_dag",
    P, S + "check_dag_M3.out: 'check_dag M3: PASS'. One dfn per concept: L04.html:130 (spectral-theorem), L05.html:72 "
    "(positive-semidefinite-matrix), L06.html:101 (singular-value-decomposition). Links L03 eigendecomposition and "
    "M1 induction only point backward.")

row("M3b-r1-38", "2.9 DAG B4 (no Cholesky, no IEEE 754 theory)",
    "L04-L06 pages and twins; plans/M3-build-plan.md section 9 B4",
    P, S + "prose_scan_r4.out: 'Cholesky' 0, 'IEEE' 0, '754' 0 in visible text of L04, L05, L06; twins read in full, none name them.")

row("M3b-r1-39", "2.9 undefined plain terms before first use (define-before-use)",
    "course/modules/M/M3/L04.html:51; L05.html:51; L06.html:52",
    P, "Why-it-matters terms are defined later with an explicit pointer ('Definition 1.1 below', 'Theorem 2.3, stated below', "
    "'Definition 3.1 below'); the convention is the one accepted in round 3. The symbols without a definition on L06 "
    "(X~, centred data) are at L06:241, not in these paragraphs, and are recorded as M3b-r4-69.")

row("M3b-r1-40", "2.4/2.9 notation: symbol meanings vs notation/notation.json",
    "L04-L06 math; notation/notation.json",
    P, S + "prose_scan_r4.out macro inventory: \\R, \\diag, \\tr are registered and used with their registry meaning; T occurs "
    "only at L06:241 as the number of observations (registry meaning). No \\Phi, \\gamma, \\E, \\mathbb{Q} or R^\\ast. Local letters "
    "(sigma, Sigma, Lambda, E, E_0, N, S, L, delta, tau) are defined in each lesson. Unregistered standard KaTeX commands "
    "(\\mathbb{C}, ^{\\top}, \\operatorname, \\binom, \\dim, \\mathcal{L}, \\tilde) are not registry collisions; they are "
    "requested under L03's NOTATION_REQUESTS (plans/M3-open-items.md).")

row("M3b-r1-41", "2.9 registered macros: \\diag at L04:176 and in L06",
    "course/modules/M/M3/L04.html:176; L06.html:106",
    P, S + "prose_scan_r4.out: no \\mathrm{diag} in L04-L06; L04.html:176 uses \\diag(w); L06.html:106 uses \\diag.")

row("M3b-r1-42", "2.9 structure and word count L04",
    "course/modules/M/M3/L04.html:33-521",
    P, "Order matches BUILDER 4.2: why-it-matters (L04:51, 113 words, at most 120), core sections 1-2 (L04:53-142), inline "
    "lab (L04:174-265), canon-breaks (L04:267-273), misconceptions (3, L04:279-296), problem set (4 tiers of 3, L04:297-400), "
    "key-results table (L04:402-416), quiz (10 items, all with explain blocks), references, navigation. data-hours 12 matches "
    "the eyebrow. " + S + "prose_scan_r4.out confirms counts.")

row("M3b-r1-43", "2.9 structure and word count L05",
    "course/modules/M/M3/L05.html:33-555",
    P, "Order matches BUILDER 4.2; why-it-matters 120 words (at the 120-word limit); 3 misconceptions; problem set 4 tiers of 3; "
    "key-results table; quiz 10 items with explain blocks; data-hours 12. " + S + "prose_scan_r4.out.")

row("M3b-r1-44", "2.9 structure and word count L06",
    "course/modules/M/M3/L06.html:33-471",
    P, "Order matches BUILDER 4.2; why-it-matters 99 words; Remark 2.5 after the lab; canon-breaks (4 bullets); 3 misconceptions; "
    "problem set 4 tiers of 3; key-results table; quiz 9 items with explain blocks; data-hours 11. " + S + "prose_scan_r4.out.")

row("M3b-r1-45", "2.9 hours arithmetic (hub split vs lessons)",
    "course/modules/M/M3/index.html data-hours-lessons=105, data-hours-project=45; L01-L09 data-hours",
    P, "data-hours of L01..L09 are 12, 11, 12, 12, 12, 11, 11, 12, 12 = 105 = data-hours-lessons; 105 + 45 = 150 = curriculum. "
    + S + "check_pages_M3.out PASS (checks the hub split).")

row("M3b-r1-46", "2.9 banned phrases (BUILDER 1.3-1.4)",
    "L04-L06 pages, cards, twins",
    P, S + "prose_scan_r4.out: zero hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an "
    "exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, "
    "it can be shown. One case-insensitive match of 'in this lesson' (L06 why-it-matters) is a neutral sentence, not an "
    "opener. " + S + "prose_scan_r4.out cards: no hits.")

row("M3b-r1-47", "2.9 banned ellipsis in learner prose",
    "course/modules/M/M3/L04.html, L05.html, L06.html; cards",
    P, S + "prose_scan_r4.out: zero ellipsis characters outside math on the three pages. Card text uses the math "
    "sequence ellipsis (q_1, ..., q_n) in M3-c070, c103, c105, c106, c107 (standard notation, accepted convention).")

row("M3b-r1-48", "2.9 page_smoke L04-L06 (alone)",
    "tools/page_smoke.py --unit M3 --pages L04 L05 L06",
    P, S + "page_smoke_L04_L06.out: 'page_smoke M3: PASS', EXIT=0 (run last in the gate script, no other gate concurrent).")

row("M3b-r1-49", "2.9 check_pages M3",
    "tools/check_pages.py --unit M3 (and --page L04, L05, L06)",
    P, S + "check_pages_M3.out PASS; check_pages_L04.out, check_pages_L05.out, check_pages_L06.out PASS; check_projects_M3.out PASS.")

row("M3b-r1-50", "2.9 external requests, figures, data",
    "course/modules/M/M3/L04.html, L05.html, L06.html",
    P, S + "prose_scan_r4.out: http 0, data-files 0, svg 0, data-chart 0 on each page; no figures to sweep.")

row("M3b-r1-51", "2.1 citations on the slice pages",
    "course/modules/M/M3/L04.html:506-510; L05.html:540-544; L06.html:456-460",
    P, S + "prose_scan_r4.out: data-cite 0 on each page; the References sections state that no passage locator is cited and "
    "that no claim is attributed to a source. No registry key is cited, so no key was read.")

row("M3b-r1-52", "2.9 process words in learner text",
    "L04-L06 pages, twins and slice cards",
    P, S + "prose_scan_r4.out: word-boundary search for round, verif*, builder*, ledger*, slice, architect*, fixer*, pending "
    "finds no process word on any page or in the cards ('rounded' is a display word).")

row("M3b-r1-53", "2.9 quiz structure (items, explanations, answers)",
    "course/modules/M/M3/L04.html:417-502 (10 items); L05.html:459-538 (10); L06.html:395-455 (9)",
    P, S + "prose_scan_r4.out: items 10, 10, 9; explain blocks 10, 10, 9; multiple-choice items have one data-correct option "
    "(7, 6, 5); numeric items carry data-answer (3, 4, 4).")

row("M3b-r1-54", "2.7 cards L04 (20 cards read in full)",
    "course/modules/M/M3/cards.json: M3-c063..c078, c189, c190, c192, c215",
    F, "All 20 cards read. Grades and bases agree with the lesson (T cards match Lemmas, Propositions, Theorem and "
    "Corollary; C cards c074, c075 name Lab 1). Defect: M3-c075 front says '1200 eigenvector pairs with distinct eigenvalues' "
    "(cards.json:508-511), but the lab and the page count only pairs whose eigenvalues are more than 1e-6 apart (L04:176; "
    "L04 E2). Severity LOW.",
    "Change the front of M3-c075 to 'pairs whose eigenvalues are more than 1e-6 apart' (M3b-r4-71).")

row("M3b-r1-55", "2.7 cards L05 (27 cards read in full)",
    "course/modules/M/M3/cards.json: M3-c079..c100, c173, c179, c180, c193, c203",
    F, "All 27 read. M3-c100 (cards.json:684-688) is graded T, but its back asserts 'a floating-point solver may return a "
    "value near zero with either sign', which the page does not prove or show (blocking; see M3b-r4-67). The other 26 agree "
    "with their lesson text; the grade issues on c094, c097, c179 are recorded in M3b-r4-68 (LOW).",
    "Fix M3b-r4-67.")

row("M3b-r1-56", "2.7 duplicate pair c085 vs c098 (round-1 FAIL, re-verified)",
    "course/modules/M/M3/cards.json: M3-c085, M3-c098",
    P, S + "cards_scan_r4.out: the pair is not among the 25 pairs with token Jaccard >= 0.5; c085 asks about Theorem 2.1 for "
    "[[1,2],[2,1]] and c098 asks whether positive entries suffice.")

row("M3b-r1-57", "2.7 cards L06 (15 cards read in full)",
    "course/modules/M/M3/cards.json: M3-c103..c114, c178, c205, c216",
    P, "All 15 read. T cards tie to Lemma 1.3, Proposition 2.1, Theorems 2.2 and 2.3, Proposition 2.4, Remark 2.5, Fact 1.2; "
    "misconception cards c112-c114 match the lesson's misconceptions; C cards c109-c111 name Lab 1 and carry basis. No "
    "card for M3-c101 (removed in round 2).")

row("M3b-r1-58", "2.7 grades and basis on slice cards",
    "course/modules/M/M3/cards.json: C cards c074, c075, c094-c097, c109-c111, c173, c179",
    F, "Eleven C cards (c074, c075, c094, c095, c096, c097, c109, c110, c111, c173, c179) all name their Lab 1 basis. Ruling 13 "
    "is breached for c094 (cards.json:638), c097 (:662) and c179 (:1218), whose values are derived by hand in Example 1.7, "
    "Remark 3.2 and Example 2.6. Severity LOW.",
    "Regrade per M3b-r4-68.")

row("M3b-r1-59", "2.7 numbers on cards appear in the lesson",
    "course/modules/M/M3/cards.json slice entries vs L04-L06 text and expected blocks",
    P, "Card numbers 200, 1200, 6, 118, 360, 500, 100000, 1e-10, 1e-6, 1e-12, 2.2335, 0.9250, 0.3348, 0.7071, 'two' and "
    "'one' each appear in the lesson text or expected block (checked against L04:176, L04:415; L05:303, L05:291-301, L05:453; "
    "L06:137, L06:216-224).")

row("M3b-r1-60", "2.7 card coverage and ids",
    "course/modules/M/M3/cards.json (208 cards; 62 in slice)",
    P, S + "cards_scan_r4.out: 208 cards, 208 unique ids; slice 62 = 20 + 27 + 15; 39 T, 11 C, 12 ungraded definition cards. "
    "Definitions, theorems, key results and misconceptions of L04-L06 each have a card. The L06 page re-states Definition 1.1 "
    "(orthogonal matrix) and Gram matrix; recorded as M3b-r4-72 (LOW).")

row("M3b-r1-61", "2.7 cross-lesson near duplicates (full scan of all 208 cards)",
    "course/modules/M/M3/cards.json whole file",
    P, S + "cards_scan_r4.out: 25 pairs with token Jaccard >= 0.5; each is a different fact (for example kernel vs image; "
    "PSD vs PD; Lab 1 count variants). Closest slice pairs c082/c193 and c087/c088 ask PSD vs PD. The cross-lesson pair "
    "M3-c083 (L05, B^T B) and M3-c131 (L08, X~^T X~/(T-1)) is the same Gram fact for different matrices; noted for the L08 "
    "verifier, not a duplicate in this slice.")

row("M3b-r1-62", "gate verify_refs (offline)",
    "tools/verify_refs.py --offline",
    P, S + "verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' EXIT=0. The slice cites no key.")

row("M3b-r1-63", "2.8 figures (slice pages)",
    "course/modules/M/M3/L04.html, L05.html, L06.html",
    P, S + "prose_scan_r4.out: svg 0 and data-chart 0 on each page; no figures on the slice.")

row("M3b-r2-64", "2.7 duplicate definition of an orthogonal matrix (cards c215 and c101)",
    "course/modules/M/M3/cards.json: M3-c215 (L04); M3-c101 (absent)",
    P, "cards_scan_r4.out: ids 100, 103 adjacent, M3-c101 absent; M3-c215 is the only card on the definition. The page-level "
    "restatement in L06 Definition 1.1 is recorded as M3b-r4-72 (LOW).")

row("M3b-r2-65", "2.7 duplicate eigenvalues of [[1,2],[2,1]] (cards c085 and c176)",
    "course/modules/M/M3/cards.json: M3-c085 (L05); M3-c176 (absent)",
    P, "M3-c176 absent; M3-c085 is the only card on Theorem 2.1 for this matrix. The lab card c179 is graded in M3b-r4-68.")

row("M3b-r3-66", "2.5 lab docstring claim vs printed output (L06 tolerances)",
    "tests/labs/M3/lab-M3-L06-1.py:4-5, 78; course/modules/M/M3/L06.html:138-142, 225 expected block",
    P, "Twin docstring now says each printed tolerance is stated on its line (lines 4-5). The sign-flip line now prints "
    "'to 1e-12' (twin line 78). The page code equals the twin (diff_twin_page_r4.out) and the expected block equals the "
    "output (twin_vs_page_r4.out). Round-3 FAIL resolved.")

row("M3b-r4-67", "2.3/2.5 card M3-c100 and misconception 3: unsupported sign claim graded T (blocking)",
    "course/modules/M/M3/cards.json:684-688 (M3-c100 grade T); course/modules/M/M3/L05.html:329-330 (misconception 3); "
    "L05.html:303 (sign never shown); tests/labs/M3/lab-M3-L05-1.py:8-11, 93-103",
    F, "Back of M3-c100: 'a floating-point solver may return a value near zero with either sign', graded T. T requires a "
    "proof on the page (BLUEPRINT section 3); the page cites no source; Lab 1 prints no sign (Part D prints 0.0 for "
    "abs <= 1e-10, twin lines 98-100; L05:303 says the sign is never shown). The claim is true for numpy.linalg.eigvalsh: "
    + S.replace("out/", "") + "sign_probe_r4.out (script ledgers/M3/scripts/M3-b-r4/sign_probe_r4.py) finds 1031 of 2000 "
    "seeded rank-2 Gram matrices with a negative computed smallest eigenvalue (minimum -1.57e-14). Misconception 3 gives "
    "this claim as its evidence, so the misconception lacks its evidence (BUILDER 4.2.6). Over-graded claim: blocking under "
    "ruling 26.",
    "Choose one: (a) regrade M3-c100 to D with the flag 'It is widely claimed' and say on L05 that Lab 1 does not show the "
    "sign; or (b) add a printed count to Lab 1 (e.g. the number of seeded rank-2 Gram matrices whose computed smallest "
    "eigenvalue is negative), regenerate the expected block with tools/embed_labs.py --refresh, update the L05:303 "
    "interpretation, grade M3-c100 C naming that line, and cite it from misconception 3.")

row("M3b-r4-68", "2.3/2.7 ruling 13 T-versus-C mismatches on cards c094, c097, c179 and key-results row L05:453 (LOW)",
    "course/modules/M/M3/cards.json:638-643 (c094), :662-667 (c097), :1218-1223 (c179); L05.html:453 (C row); "
    "L05.html:97 (Example 1.7), :155 (Example 2.6), :171-173 (Remark 3.2)",
    F, "Ruling 13: a value derived by hand in a numbered Example is T with that Example as basis, even when a lab also prints "
    "it. c094 'both diagonal entries positive' is stated in Example 1.7 (L05:97) but graded C with basis 'Lab 1 Part A'. "
    "c179 'smallest eigenvalue -1, rejected' follows from Example 2.6 (L05:155) and Definition 3.1 but is graded C. c097 "
    "'one eigenvalue within 1e-10 of zero' follows from Remark 3.2's exact spectrum 0, 1, 3 (L05:172) but is graded C. The "
    "printed lines (True, 118 of 360, 500 of 500, 100000 of 100000, 'eigenvalues ... at most 1e-10: 1') remain C. Severity LOW.",
    "Regrade c094, c179, c097 to T with basis Example 1.7, Example 2.6, Remark 3.2 respectively, and keep a separate C card "
    "for each printed line; split key-results row L05.html:453 into a T row and a C row; keep card and row grades equal.")

row("M3b-r4-69", "2.9 define-before-use: X~, T and 'centred data' used on L06 before any definition (LOW)",
    "course/modules/M/M3/L06.html:241 (canon-breaks bullet 4); defined at course/modules/M/M3/L08.html:56-57",
    F, "L06:241 writes M = X~^T X~/(T-1) and 'a scaled Gram matrix of centred data'. X~, T and centred data are not defined "
    "on L06 (grep: 'tilde' and 'centred' occur only on line 241). They are defined in L08 Section 1 (L08.html:56-57), a later "
    "lesson. Plain symbol use before definition (BUILDER 8; VERIFIER 2.9). Severity LOW.",
    "Add one clause at L06:241: 'X~ is the centred data matrix with T rows (Lesson 8, Section 1)', or drop the formula and keep "
    "the cross-reference by name.")

row("M3b-r4-70", "2.4 proof step not named: L04 P2 middle equality uses Q^T Q = I (LOW)",
    "course/modules/M/M3/L04.html:339 (P2 solution)",
    F, "(Q Lambda^{-1} Q^T)(Q Lambda Q^T) = Q Lambda^{-1} Lambda Q^T uses Q^T Q = I (Definition 1.2, L04.html:74). The solution "
    "names only QQ^T = I (Lemma 1.4). The step is correct but unnamed. Severity LOW.",
    "Insert 'using Q^T Q = I (Definition 1.2)' after the first equality of the L04.html:339 display.")

row("M3b-r4-71", "2.7 card M3-c075 front wording differs from the lab and lesson (LOW)",
    "course/modules/M/M3/cards.json:508-511",
    F, "Front: '1200 eigenvector pairs with distinct eigenvalues'. Lab 1 (L04:176, twin line 54) and the page (L04 E2; key-results "
    "row L04:415) count pairs whose eigenvalues are more than 1e-6 apart. Severity LOW.",
    "Change the front to 'pairs whose eigenvalues are more than 1e-6 apart'.")

row("M3b-r4-72", "2.9 plain terms defined again in L06 instead of linked (LOW)",
    "course/modules/M/M3/L06.html:58-61 (Definition 1.1, orthogonal matrix; L04.html:73-76 is Definition 1.2); "
    "L06.html:85 ('It is the Gram matrix of the columns of A'; L05.html:66-68 is Definition 1.3)",
    F, "BUILDER 1.10 and 8: a term already defined in an earlier lesson of the unit is defined again rather than referred to. "
    "Neither term is a registered concept (no dfn), so check_dag does not fail. Severity LOW.",
    "Refer to 'orthogonal matrix (Lesson 4, Definition 1.2)' and 'Gram matrix (Lesson 5, Definition 1.3)' in L06, or keep one "
    "restatement clause labelled as such.")

frag = {
    "unit": "M3",
    "slice": "b",
    "round": 4,
    "verifier": "independent Haiku verifier, slice b (did not build M3)",
    "pin": "edbb7aa8de20e6d2f3035c463a79a318c22623c4",
    "base": "8196077d5f56c3919d33e69888176d197d378ad4 (round-3 pin; round-3 fragment /Users/billyribeiro/.fanout/frags/S-M3-b.round3.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS4-M3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS4-M3-b/ledgers/M3/scripts/M3-b-r4",
    "verified_at": "2026-11-09",
    "verdict": "FAIL",
    "rows": R,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Method: L04.html (521 lines), L05.html (555), L06.html (471) read in full this round; the three twins read in full; all 62 slice cards re-read (cards.json). Delta 8196077d..edbb7aa8 for the slice read in full (ledgers/M3/scripts/M3-b-r4/delta.diff, 261 lines): L04 (why-it-matters, Remark 1.6, P2, R2, R3), L05 (why-it-matters), L06 (Lemma 1.3 proof, Prop 2.1, Theorem 2.2 Step 2, lab docstring, sign-flip print, E2), L06 twin, cards.json (M3-c100 grade; L01/L02 card wording outside the slice), plans/FINAL-ARCHITECT-RULINGS.md (rulings 1-26 applied).",
        "Carry: none. Every round-3 row was re-verified this round because all three pages and the L06 twin changed; no 'Carried from round 3' prefix is used.",
        "Gates on the pinned checkout (ledgers/M3/scripts/M3-b-r4/out/): check_pages M3 and --page L04/L05/L06 PASS; check_dag M3 PASS; check_projects M3 PASS; run_labs --page L04, L05, L06 each PASS (1/1); ruff check and ruff format --check tests/labs/M3 PASS; mypy --no-incremental PASS (385 files); verify_refs --offline 560 entries, 0 problems; pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_docs_figures.py exit 0; page_smoke --unit M3 --pages L04 L05 L06 PASS. Each twin run alone with python -I -W error exits 0 with empty stderr (twin_vs_page_r4.out).",
        "Mutants: none, by design. The slice has no project grader (VERIFIER 2.6 and the ruling apply mutation testing to project graders only); the lab twins are demonstrations.",
        "Ruling 26 classification: blocking = M3b-r4-67 (over-graded claim) and the two rows that depend on it, M3b-r1-29 and M3b-r1-55. LOW rows, deferrable to plans/KNOWN-ISSUES.md with these ids: M3b-r1-16, M3b-r1-31, M3b-r1-54, M3b-r1-58, M3b-r4-68, M3b-r4-69, M3b-r4-70, M3b-r4-71, M3b-r4-72. The slice is not accepted until M3b-r4-67 is fixed and the lab (if option b is chosen) is re-run.",
        "Observations, not rows: the math ellipsis in cards c070, c103, c105, c106, c107 is accepted notation; the Remark 3.2 determinant expansion is stated without its intermediate steps (routine, not flagged); the L05 why-it-matters forward pointer to Definition 3.1 follows the accepted convention; cross-lesson pair M3-c083 (L05) and M3-c131 (L08) is noted for the L08 verifier.",
        "Not checked: the full gate (render_curriculum, build_site --check, fetch_data --check, full pytest suite, page_smoke --all, live verify_refs) is outside slice b and was not run; no screenshot or visual diff; L08 and L01/L03 beyond the cited lines; no source was consulted because the slice cites no registry key; no mutation or alternative-implementation run (no grader); the trailing-newline difference between page code and twin is treated as the embed convention, not as a defect.",
    ],
    "summary": "Slice b (M3 L04-L06 pages, lab twins, 62 slice cards), round 4 at pin edbb7aa8: FAIL. 72 rows: 60 PASS, 12 FAIL (1 blocking root cause M3b-r4-67 with dependents M3b-r1-29 and M3b-r1-55; 9 LOW). Round-3 FAIL M3b-r3-66 is resolved. Every lab twin runs clean, each page code equals its twin (modulo trailing newline), each expected block equals the output, all printed and prose numbers re-derived, all gates PASS.",
}

with open(ROOT + "/ledgers/M3/M3-b.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("rows", len(R), "PASS", sum(r["status"] == "PASS" for r in R), "FAIL", sum(r["status"] == "FAIL" for r in R))
