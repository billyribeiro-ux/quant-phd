"""Builds the round-2 fragment ledgers/M3/M3-b.json for slice b (M3 L04-L06, twins and cards)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyS2-M3-b")
OUT = ROOT / "ledgers/M3/M3-b.json"

P = "PASS"
F = "FAIL"

rows = [
    {"id": "M3b-r1-01", "check": "2.5-lab L04: hypothesis, code, expected block, interpretation present",
     "location": "course/modules/M/M3/L04.html:174-266; tests/labs/M3/lab-M3-L04-1.py", "status": P,
     "evidence": "Re-run this round: run_labs.py --unit M3 --page L04 -> 'run_labs M3: PASS (1/1)', exit 0 (scripts/M3-b-r2/gates_r2.out); page code is byte-identical to the twin and the expected block equals the twin's output (scripts/M3-b-r2/twin_L04.out)."},
    {"id": "M3b-r1-02", "check": "2.5 lab interpretation L04 against what the lab prints",
     "location": "course/modules/M/M3/L04.html:265 vs expected block lines 256-264", "status": P,
     "evidence": "Re-read: the interpretation names the 200 seed-2604 matrices and 1200 pairs, tolerance 1e-10, counts not residuals, the fixed rotation (Remark 1.6) and N (Remark 2.7). Every count it names is in the expected block (recheck L04-lab-counts: 200, 200, 200, 1200, 1200 in scripts/M3-b-r2/recheck_numbers_r2.out)."},
    {"id": "M3b-r1-03", "check": "2.5-lab L05 structure and twin run",
     "location": "course/modules/M/M3/L05.html:175-304; tests/labs/M3/lab-M3-L05-1.py", "status": P,
     "evidence": "run_labs.py --unit M3 --page L05 -> 'run_labs M3: PASS (1/1)' (gates_r2.out); twin under python -I -W error exit 0, stderr 0 bytes (scripts/M3-b-r2/twin_L05.out)."},
    {"id": "M3b-r1-04", "check": "2.5 lab interpretation L05 states what the lab prints (round-1 FAIL, re-verified)",
     "location": "course/modules/M/M3/L05.html:303 vs twin lines 228, 277 and expected lines 293, 300", "status": P,
     "evidence": "Round-1 defect fixed: L05.html:303 now says the lab prints verdicts, counts and eigenvalues rounded to four decimals, and that a value within 1e-10 of zero is printed as 0.0000. Twin prints eigenvalues with :.4f (lines 228, 277) and clamps |v|<=TOL to 0.0 (line 277). Expected lines 293 and 300 match the output. recheck L05-partD PASS."},
    {"id": "M3b-r1-05", "check": "2.5-lab L06 structure and twin run",
     "location": "course/modules/M/M3/L06.html:135-225; tests/labs/M3/lab-M3-L06-1.py", "status": P,
     "evidence": "run_labs.py --unit M3 --page L06 -> PASS (1/1); twin under python -I -W error exit 0, stderr 0 bytes (scripts/M3-b-r2/twin_L06.out)."},
    {"id": "M3b-r1-06", "check": "2.5 lab hypothesis and interpretation L06 against the twin and output",
     "location": "course/modules/M/M3/L06.html:137, 224 vs twin lines 143-150, 190-212 and expected lines 216-223", "status": P,
     "evidence": "Hypothesis: 10 matrices (5 of 4x3, 5 of 3x4), four identity checks, printed singular values, count at 1e-10 relative, sign flip; all match the twin. Interpretation: 'rounded to four decimals from the unrounded values' matches :.4f applied to svd output (twin line 197); recheck L06-seed0-sv re-derives 2.2335 0.9250 0.3348 from unrounded values by two algorithms."},
    {"id": "M3b-r1-07", "check": "2.5 twin lint, format and types",
     "location": "tests/labs/M3/lab-M3-L04-1.py, lab-M3-L05-1.py, lab-M3-L06-1.py", "status": P,
     "evidence": "gates_r2.out: ruff check 'All checks passed!' exit 0; ruff format --check '3 files already formatted' exit 0; mypy --no-incremental 'Success: no issues found in 3 source files' exit 0; pytest tests/test_labs.py -k 'M3 and (L04 or L05 or L06)' exit 0."},
    {"id": "M3b-r1-08", "check": "2.5 lab runtime, no network, seeded RNG only",
     "location": "three twins; scripts/M3-b-r2/page_smoke.out", "status": P,
     "evidence": "page_smoke.out: runtime boot 1.1 s, numpy preload 0.2 s, lab runs 0.0-0.1 s for each page; twins use numpy.random default_rng(seed) only (L04 seed 2604; L05 seed 2604; L06 seeds 0-4 and 100-104, 7, 8, 0). No network calls in the twins."},
    {"id": "M3b-r1-09", "check": "2.5 lab scope sentences (for the tested seeds, grid and matrices)",
     "location": "L04.html:265; L05.html:303, 312; L06.html:224, 237", "status": P,
     "evidence": "Each sentence re-read against the twin and output: L04 counts describe the 200 seed-2604 matrices only; L05 Part C counts describe 500 matrices x 200 vectors; L05:312 'For a Gram matrix, Proposition 1.5 proves it for every vector' (L05.html:76-83); L06:237 threshold is a convention of the lab. No sentence claims a property beyond the tested sample."},
    {"id": "M3b-r1-10", "check": "2.2 printed and prose numbers L04 re-derived",
     "location": "L04.html:51, 166, 171-176, 252, 265, 272, 323, 371, 415", "status": P,
     "evidence": "recheck_numbers_r2.out: L04-ex26-factor, L04-ex26-corollary (3/2+1/2=2), L04-rem27-ip (|<(1,0),(1,1)/sqrt2>|=0.7071067812), L04-E3-digits (1/sqrt2=0.70710678), L04-rem16 (eig +-i), L04-M1..M3, L04-R1 (z*Rz=2i), L04-E2-pairs (6 and 1200), L04-quiz-x (2): all PASS (44 of 44 checks PASS)."},
    {"id": "M3b-r1-11", "check": "2.2 printed and prose numbers L05 re-derived",
     "location": "L05.html:177, 295-303, 402, 409, 453", "status": P,
     "evidence": "recheck_numbers_r2.out: L05-ex17 (form -2, eig {-1,3}), L05-partB (118 negative, 4 zero, min -1.000), L05-E2 (118/360=0.327778; 59+59=118; 106..164 and 286..344), L05-partC (500/500; 100000/100000), L05-partD (eig 0, 1, 3; count 1), L05-rem32-det (det(G-lam I)=(1-lam)lam(lam-3) at 7 points): all PASS."},
    {"id": "M3b-r1-12", "check": "2.2 printed and prose numbers L06 re-derived",
     "location": "L06.html:221, 270, 277, 284, 334, 399, 413, 450", "status": P,
     "evidence": "recheck_numbers_r2.out: L06-seed0-sv (svd and sqrt eig(A^T A) agree to 1e-12; 2.2335, 0.9250, 0.3348), L06-planted-rank (count 2), L06-M1 (sv 4,3), L06-M2 (sqrt2, 0; ||A||_F^2=2), L06-M3 (1,1), L06-E3 (5; 25), L06-quiz-frob (30), L06-quiz-2I (8): all PASS."},
    {"id": "M3b-r1-13", "check": "2.2 scope words (every, all, only, exactly, never, same, any, in general, always)",
     "location": "L04.html, L05.html, L06.html prose and the changed lines L04:146, L05:130 and 303, L06:52 and 56",
     "status": P,
     "evidence": "grep -o -w counts this round: L04 every 18, all 7, only 4, exactly 2, never 1, same 4, any 7; L05 every 29, all 7, only 9, exactly 8, never 3, same 5, any 9, in general 2; L06 every 24, all 2, only 5, exactly 5, never 1, same 10, any 9, in general 1; always, generic, typically, stable, robust 0. Every hit in the changed lines was checked against its proof or lab; L06:52 'every real matrix' is Theorem 2.2 (any m x n); L05:303 'never shown' is true of the printed output."},
    {"id": "M3b-r1-14", "check": "2.2 rounding: displayed digits come from unrounded values",
     "location": "printed decimals in L04-L06 pages and twins", "status": P,
     "evidence": "Twins print :.4f from unrounded floats (L04 line 252; L05 lines 228, 277; L06 line 197). recheck: 2.2335/0.9250/0.3348 come from unrounded svd values, tie margin 0.216e-4 (L06-seed0-rounding-margin); 0.7071 from 0.7071067812."},
    {"id": "M3b-r1-15", "check": "2.3 grades L04", "location": "L04.html:77-171, 408-415", "status": P,
     "evidence": "Re-read: Lemmas 1.3, 1.4, 2.1, 2.2, Theorem 2.3, Proposition 2.4, Corollary 2.5 and Remarks 1.5, 1.6, 2.7 are T and carry proofs on the page; C only for the lab rows (L04.html:265, 415). Key-results table grades match."},
    {"id": "M3b-r1-16", "check": "2.3 grades L05", "location": "L05.html:107-173, 446-453", "status": P,
     "evidence": "Theorems 2.1, 2.2, Propositions 1.5, 1.6, 2.3, 2.4, Remarks 1.2, 2.7, 3.2 are T with proofs on the page; lab-derived statements are C (L05.html:303, 453). Remark 3.2's eigenvalues recomputed (L05-rem32-det)."},
    {"id": "M3b-r1-17", "check": "2.3 grades L06", "location": "L06.html:63-133, 371-377", "status": P,
     "evidence": "Fact 1.2, Lemma 1.3, Propositions 2.1, 2.4, Theorems 2.2, 2.3 are T with proofs; the lab row is C (L06.html:377). Remark 2.5 has no grade badge; its I_2 claim is derived on the page (L06-rem25)."},
    {"id": "M3b-r1-18", "check": "2.4 math L04 core: Lemmas 1.3, 1.4, 2.1, 2.2, Theorem 2.3 proof steps",
     "location": "L04.html:77-142", "status": P,
     "evidence": "Re-derived this round: Lemma 1.4 (F1 gives Q^{-1}=Q^T); Lemma 2.1 (conjugation argument uses A_ij=A_ji, checked); Lemma 2.2 (real and imaginary parts; F1 gives a nonzero null vector when det=0); Theorem 2.3 induction: W invariant under A, S symmetric, u_j eigenvectors (Au_j=mu_j u_j), F4 gives dim W = n-1, Lemma 1.3 completes the basis. No gap found."},
    {"id": "M3b-r1-19", "check": "2.4 hypotheses L04 Proposition 2.4 (field of the vectors) (round-1 FAIL, re-verified)",
     "location": "course/modules/M/M3/L04.html:145-151; Definition 1.2 at L04.html:74", "status": P,
     "evidence": "Round-1 defect fixed: L04.html:146 now states v, w in R^n and lists 'v, w in R^n' among the hypotheses; the proof at L04.html:151 uses only symmetry, the eigen-equations and lambda != mu. Card M3-c071 was updated to match (cards.json diff). The same fix is in L05.html:130 (x in R^n for Proposition 2.3)."},
    {"id": "M3b-r1-20", "check": "2.4 math L04 Corollary 2.5, Example 2.6, Remarks 1.5, 1.6, 2.7",
     "location": "L04.html:154-172, 98-105", "status": P,
     "evidence": "Example 2.6: Q Lambda Q^T = [[2,1],[1,2]] (recheck L04-ex26-factor); y = Q^T(1,0) gives y^2 = (1/2, 1/2), 3/2 + 1/2 = 2 (L04-ex26-corollary). Remark 2.7: N(1,1) = (3,3); N-I rows (0,2); N-3I rows (-2,2),(0,0); |inner product| = 1/sqrt2 (L04-rem27-*). Remark 1.6: eigenvalues +-i (L04-rem16)."},
    {"id": "M3b-r1-21", "check": "2.4 math L05 core: Remark 1.2, Propositions 1.5, 1.6, Example 1.7, Remark 1.8, Theorems 2.1, 2.2",
     "location": "L05.html:55-127", "status": P,
     "evidence": "Example 1.7 form -2 (L05-ex17); Remark 1.8 x^T M x = x1^2 + x2^2 on 1000 random x and eigenvalues 1 +- i (L05-rem18-*); Theorem 2.1 both directions (nonzero real eigenvector w, w^T A w = lambda ||w||^2; the converse via A = Q Lambda Q^T); Theorem 2.2 strict version. No gap found."},
    {"id": "M3b-r1-22", "check": "2.4 math L05 Propositions 2.3, 2.4, Example 2.5, Remark 2.7",
     "location": "L05.html:128-161", "status": P,
     "evidence": "Proposition 2.3 (hypothesis now x in R^n, L05.html:130): sum of nonnegative terms forces lambda_j y_j = 0, so Ax = 0. Proposition 2.4: B = Lambda^{1/2} Q^T gives B^T B = [[2,1],[1,2]] (L05-ex25). Remark 2.7: (OB)^T(OB) = A and -B is a second factor (L05-R1)."},
    {"id": "M3b-r1-23", "check": "2.4 math L05 Definition 3.1 and Remark 3.2", "location": "L05.html:165-173", "status": P,
     "evidence": "Remark 3.2: B = [[1,0,1],[0,1,1]], G = B^T B = [[1,0,1],[0,1,1],[1,1,2]]; det(G - lam I) = (1-lam) lam (lam-3) at 7 sample points; eigenvalues 0, 1, 3; (1,1,-1) in the null space (L05-rem32-*). Theorem 2.2 then gives 'not positive definite'."},
    {"id": "M3b-r1-24", "check": "2.4 math L06 core: Fact 1.2, Lemma 1.3, Proposition 2.1", "location": "L06.html:56-95", "status": P,
     "evidence": "Fact 1.2: F1 applied to M = Q^T, N = Q gives Q Q^T = I. Lemma 1.3: Gram-Schmidt on u_1..u_r followed by e_1..e_m; independence by Lesson 4 Lemma 1.3. Proposition 2.1: conjugate-transpose argument for an eigenvalue of A^T A, using (Az)^* = z^* A^T for real A."},
    {"id": "M3b-r1-25", "check": "2.4 math L06 Theorem 2.2 (SVD) proof, Steps 1-5", "location": "L06.html:97-113", "status": P,
     "evidence": "Re-derived: u_i^T u_j = delta_ij (Step 2 chain); Step 4 columns (for j > r, ||A v_j||^2 = v_j^T G v_j = lambda_j = 0); Step 5 A = U Sigma V^T and rank = dim span(u_1..u_r). Numeric checks L06-M1..M3 and L06-seed0-sv agree. Macro-only edits in Step 1 (L06.html:106) do not change the math."},
    {"id": "M3b-r1-26", "check": "2.4 math L06 Theorem 2.3 and Proposition 2.4", "location": "L06.html:115-133", "status": P,
     "evidence": "Theorem 2.3: A^T A = V (Sigma^T Sigma) V^T, similarity via V^{-1} = V^T (Fact 1.2), characteristic polynomial invariant. Proposition 2.4: trace identity tr(A^T A) = ||A||_F^2 = sum sigma_i^2 (L06-seed0-sv with the lab's matrix)."},
    {"id": "M3b-r1-27", "check": "2.4 math L06 Remark 2.5", "location": "L06.html:227-230", "status": P,
     "evidence": "u_i sigma_i v_i^T unchanged by a common sign flip; P I_2 P^T = I_2 for the swap P, so the decomposition with U = V = P is valid with singular values 1, 1 (L06-rem25)."},
    {"id": "M3b-r1-28", "check": "2.4 math L06 problem R1 (A and A^T share nonzero singular values)", "location": "L06.html:341-347", "status": P,
     "evidence": "Re-derived: L(v) = Av maps the lambda-eigenspace E of A^T A into that of A A^T and is injective on E (||Av||^2 = lambda ||v||^2); exchanging A and A^T gives equal dimensions; multiplicity equals dim E by the eigenbasis argument with Theorem 2.3 of Lesson 4. L06-R1-spot: singular values of A and A^T agree on 3 random 4x3 matrices."},
    {"id": "M3b-r1-29", "check": "2.4 misconception counterexamples (L04, L05, L06)",
     "location": "L04.html:283-292; L05.html:320-330; L06.html:245-256", "status": P,
     "evidence": "L04: [[4,1],[1,3]] symmetric with nonzero off-diagonal; (1,0),(1,1) for I_2 have inner product 1 (both eigenvectors for 1). L05: [[1,2],[2,1]] quadratic form -2 (L05-ex17); G has eigenvalue 0 with (1,1,-1) (L05-rem32-null). L06: [[0,1],[0,0]] has eigenvalues 0,0 and A^T A = diag(0,1), singular values 1,0 (L06-misc-sv); zero-matrix SVD by Theorem 2.2."},
    {"id": "M3b-r1-30", "check": "2.4 canon-breaks claims (L04, L05, L06)",
     "location": "L04.html:268-277; L05.html:306-315; L06.html:232-240", "status": P,
     "evidence": "L04: Theorem 2.3 needs symmetry; Remark 1.6 and Remark 2.7 as stated; F1-F4 assumed, not proved. L05: Remark 1.8 (non-symmetric positive form, eigenvalues 1 +- i); tolerance dependence; Lab Part C is a sample. L06: at most m nonzero eigenvalues of A^T A when m < n (rank argument); Lesson 8 forms M = X~^T X~/(T-1) (L08.html:54-57) and does not use the SVD (only a cross-reference at L08.html:293)."},
    {"id": "M3b-r1-31", "check": "2.4 problem set L04 (12 problems, all solutions)", "location": "L04.html:297-400", "status": P,
     "evidence": "All twelve re-derived this round: M1 (L04-M1), M2 (L04-M2), M3 (L04-M3), P1, P2 (F1 inverse argument), P3 (idempotent eigenvalues), E1, E2 (L04-E2-pairs), E3 (L04-E3-digits), R1 (L04-R1), R2 (max equals lambda_1 via Corollary 2.5), R3 (shift by mu)."},
    {"id": "M3b-r1-32", "check": "2.4 problem set L05 (12 problems, all solutions)", "location": "L05.html:339-438", "status": P,
     "evidence": "All twelve re-derived: M1 (eigenvalues 3, 1; L05 Example 2.5), M2 (eigenvalues 0, 5 as L03 M2 computes; x=(2,-1) gives 0, L05-M2), M3 (eigenvalues 2, 4; form 4 at (1,1), L05-M3), P1, P2, P3, E1 (form -2 at the eigenvector (1,-1)), E2 (118/360 = 0.3278; the arc is 120 degrees; L05-E2), E3 (eigenvalues 0, 1, 3), R1 (O_pi B = -B, L05-R1), R2 (-2 at (1,-1)), R3 (closure under sums; Proposition 1.6)."},
    {"id": "M3b-r1-33", "check": "2.4 problem set L06 (12 problems, all solutions)", "location": "L06.html:264-362", "status": F,
     "evidence": "Problem R2 (L06.html:350-352) asks for 'at least n - m zero eigenvalues' of A^T A. The solution (L06.html:352) proves only that the eigenspace of 0 has dimension at least n - m. It does not state that the count is with multiplicity, and does not derive that the multiplicity equals that dimension. All other eleven problems re-derived: M1 (L06-M1), M2 (L06-M2), M3 (L06-M3), P1, P2, P3, E1 (sign pair), E2 (rank at most 2), E3 (L06-E3), R1 (see row 28), R3 (I_n has infinitely many SVDs)."},
    {"id": "M3b-r1-34", "check": "2.9 cross-references L04",
     "location": "L04.html:37, 51, 99, 166, 174; L03.html:96-97, 109, 271, 397; L08.html:54-57, 82", "status": P,
     "evidence": "L03.html:96 Example 1.6 is the matrix [[4,1],[1,3]] (its eigenvalues (7 +- sqrt5)/2 at L03.html:271 and 397); L03.html:109 defines def-eigendecomposition (link target of L04.html:37); L04 Remark 1.5 and Example 2.6 reference resolve. L04.html:51 'Lesson 8 applies it to a symmetric matrix of centred data' matches L08.html:54-57 (M = X~^T X~/(T-1)) and L08.html:82 (spectral decomposition)."},
    {"id": "M3b-r1-35", "check": "2.9 cross-references L05",
     "location": "L05.html:37, 51, 97, 109, 115, 140, 149-156, 224-225", "status": P,
     "evidence": "L04.html:110 Lemma 2.1, L04.html:130 Theorem 2.3, L04.html:155 Corollary 2.5, L04.html:165 Example 2.6 all exist as cited; L03.html:297-303 Problem M2 is [[1,2],[2,4]] with solution eigenvalues 0 and 5 (L03 solution text); L01.html:183 Example 3.9 gives the standard basis cited as 'Lesson 1' for e_i; L01.html:93 defines span."},
    {"id": "M3b-r1-36", "check": "2.9 cross-references L06",
     "location": "L06.html:38, 52, 80, 85, 112, 137, 238, 255, 345, 355", "status": P,
     "evidence": "L03.html:109 def-eigendecomposition; L04.html:130 def-spectral-theorem; L04.html:78 Lemma 1.3; L01.html:93 span (L06:85 'span as defined in Lesson 1'); L08.html:54-57 M formula (L06:238); grep 'ingular' in L08.html returns only L08.html:293, a cross-reference, so the SVD is not used in Lesson 8."},
    {"id": "M3b-r1-37", "check": "2.9 DAG and concept definitions (check_dag and unit-wide grep)",
     "location": "L04.html:130; L05.html:72; L06.html:101; tools/check_dag.py --unit M3", "status": P,
     "evidence": "check_dag.py --unit M3 -> 'check_dag M3: PASS' (gates_r2.out). Definitions: spectral-theorem at L04.html:130, positive-semidefinite-matrix at L05.html:72, singular-value-decomposition at L06.html:101; links to L03 and L04 precede use."},
    {"id": "M3b-r1-38", "check": "2.9 DAG B4 (no Cholesky, no IEEE 754 theory)",
     "location": "L04-L06 pages and twins; plans/M3-build-plan.md section 9 B4", "status": P,
     "evidence": "grep -n -i 'cholesky|ieee|<svg|<img' over the three pages and twins returns no match (this round)."},
    {"id": "M3b-r1-39", "check": "2.9 undefined plain terms before first use", "location": "L04-L06 prose", "status": P,
     "evidence": "Checked: Gram matrix (L05.html:67 before L06.html:85); span (L01.html:93); characteristic polynomial (L03.html:91, Definition 1.5); eigenspace (L03.html:66); column space (defined L06.html:85, first used in Theorem 2.2 at L06.html:101); similar matrices (defined inside the proof at L06.html:122 before use); trace and Frobenius norm (L06.html:127); F1 to F4 (L04.html:55-63). Gram-Schmidt is named at L04.html:61 and used as the standard procedure at L06.html:80."},
    {"id": "M3b-r1-40", "check": "13 notation symbols vs notation/notation.json (symbol meanings)",
     "location": "L04-L06 math; notation/notation.json", "status": P,
     "evidence": "Tally of math segments this round: registered macros used are \\R (L04 11, L05 7, L06 14), \\tr (L06 7), \\diag (L04 4, L05 5, L06 6); \\N and \\se unused. Registered symbols T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q} do not occur in the slice (T appears only in the L06.html:238 cross-reference to Lesson 8). Local letters sigma, lambda, mu, E, m, n are defined in each lesson where used; none takes a registered meaning."},
    {"id": "M3b-r1-41", "check": "13 notation macros: registered macros used, not expanded (round-1 FAIL, re-verified)",
     "location": "course/modules/M/M3/L04.html:176 (open); L06.html:106, 132, 270, 293, 422 (fixed); notation/notation.json", "status": F,
     "evidence": "The round-1 defect in L06 is fixed: L06 now uses \\diag and \\tr at lines 106, 132, 270, 293, 422, and no \\operatorname{diag} or \\operatorname{tr} remains in the slice. But the lab hypothesis at L04.html:176 writes '\\mathrm{diag}(w)', an expanded form of the registered \\diag (notation.json: '\\diag' has tex '\\operatorname{diag}'). The same rule applies. \\operatorname{rank} (L04.html:62, L06.html:352) and \\operatorname{span} (L06.html:112) have no registered macro and are not defects. Fix: replace '\\mathrm{diag}(w)' with '\\diag(w)' at L04.html:176."},
    {"id": "M3b-r1-42", "check": "2.9 structure and word count L04", "location": "L04.html:33-420", "status": P,
     "evidence": "check_pages --unit M3 -> PASS (this round): section order, 6-12 study hours, why-it-matters at most 120 words, misconceptions, problem tiers, key results, quiz 10 items, references. data-hours=12 matches the header 'Lesson 4 of 9 · 12 study hours'."},
    {"id": "M3b-r1-43", "check": "2.9 structure and word count L05", "location": "L05.html:33-530", "status": P,
     "evidence": "check_pages --unit M3 -> PASS; data-hours=12 matches the header; quiz 10 items; key results table; references present."},
    {"id": "M3b-r1-44", "check": "2.9 structure and word count L06", "location": "L06.html:33-465", "status": P,
     "evidence": "check_pages --unit M3 -> PASS; data-hours=11 matches the header 'Lesson 6 of 9 · 11 study hours'; quiz 9 items; key results table; references present."},
    {"id": "M3b-r1-45", "check": "2.9 hours arithmetic (hub split vs lessons)",
     "location": "course/modules/M/M3/index.html data-hours-lessons=105, data-hours-project=45; L01-L09 data-hours", "status": P,
     "evidence": "grep: index.html data-hours-lessons=\"105\", data-hours-project=\"45\"; L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12; sum 105 = hub lessons figure; 45 is 30% of 150 (inside 10-40%)."},
    {"id": "M3b-r1-46", "check": "2.9 banned phrases (BUILDER_RULES 1.3-1.4)", "location": "L04-L06 pages", "status": P,
     "evidence": "check_pages --unit M3 -> PASS this round (its banned-string scan covers the three pages)."},
    {"id": "M3b-r1-47", "check": "2.9 banned ellipsis in learner prose (round-1 FAIL, re-verified)",
     "location": "course/modules/M/M3/L06.html:402", "status": P,
     "evidence": "Round-1 defect fixed: L06.html:402 now reads 'What are the singular values of the 3 x 3 identity matrix?'. grep for the ellipsis character and for '...' over the three pages finds no prose ellipsis; the math list ellipses are standard notation (cards only). check_pages PASS."},
    {"id": "M3b-r1-48", "check": "2.9 page_smoke L04-L06",
     "location": "tools/page_smoke.py --unit M3 --pages L04 L05 L06", "status": P,
     "evidence": "scripts/M3-b-r2/page_smoke.out: 'page_smoke modules/M/M3/L04.html: PASS', L05 PASS, L06 PASS, 'page_smoke M3: PASS', exit 0 (Chromium; zero console errors and no horizontal scroll at 360 px per tool contract)."},
    {"id": "M3b-r1-49", "check": "2.9 check_pages M3", "location": "tools/check_pages.py --unit M3", "status": P,
     "evidence": "'check_pages M3: PASS' exit 0 (gates_r2.out)."},
    {"id": "M3b-r1-50", "check": "2.9 external requests, figures, data", "location": "L04.html, L05.html, L06.html", "status": P,
     "evidence": "grep for <img>, <svg>, data-files in the three pages: none. page_smoke reports zero requests to any host other than the local server."},
    {"id": "M3b-r1-51", "check": "2.1 citations on the slice pages",
     "location": "L04.html:506-510; L05.html:540-544; L06.html:455-459", "status": P,
     "evidence": "Each references section states that no passage locator is cited and that no claim is attributed to axler2024linear or strang2023introduction. grep for data-cite and data-locator in the slice pages: none."},
    {"id": "M3b-r1-52", "check": "2.9 process words in learner text", "location": "L04-L06 pages, twins and slice cards", "status": P,
     "evidence": "grep -w -i for round, builder, verifier, verification, audit, fragment, rung, reviewer, open item over pages and twins: no hits. Slice cards read in full (scripts/M3-b-r2/cards_slice.txt): no process words."},
    {"id": "M3b-r1-53", "check": "2.9 quiz structure (items, explanations, answers)",
     "location": "L04.html:421-504; L05.html:459-538; L06.html:383-453", "status": P,
     "evidence": "Items: L04 10, L05 10, L06 9 (8-15 required). Each item has an explain block; mc items have one data-correct option. Numeric answers re-checked: L04 6 (C(4,2)), 0.7071, 2 (x^T A x); L05 1 (smallest eigenvalue), -2, 3, 1 (Part D count); L06 5, 30, 2 (k = min(4,2)), 8 (2I_2)."},
    {"id": "M3b-r1-54", "check": "2.7 cards L04 (20 cards read in full; round 1 read 19)",
     "location": "course/modules/M/M3/cards.json: M3-c063..c078, c189, c190, c192, c215", "status": P,
     "evidence": "All 20 read (scripts/M3-b-r2/cards_slice.txt) and checked against the L04 text: c070 matches Theorem 2.3; c071 matches Proposition 2.4 as amended; c073 matches Remark 2.7; c074 and c075 match the Lab 1 expected block. The duplicate pairing of the new card c215 is a separate row (M3b-r2-64)."},
    {"id": "M3b-r1-55", "check": "2.7 cards L05 (28 cards read in full)",
     "location": "cards.json: M3-c079..c100, c173, c176, c179, c180, c193, c203", "status": P,
     "evidence": "All 28 read and checked: c085 (new text) matches Example 2.6 and Theorem 2.1; c098 matches Example 1.7; c094-c097, c173, c176, c179 match the lab output. The duplicate of c085 with c176 is a separate row (M3b-r2-65)."},
    {"id": "M3b-r1-56", "check": "2.7 cards: the round-1 duplicate pair M3-c085 vs M3-c098 (round-1 FAIL, re-verified)",
     "location": "course/modules/M/M3/cards.json:582 (M3-c085), :676 (M3-c098)", "status": P,
     "evidence": "Round-1 pair resolved: c085 now asks for the eigenvalues of [[1,2],[2,1]] and Theorem 2.1's conclusion; c098 asks only the positive-entries misconception and gives the form value -2. The two no longer test the same fact. New duplicates introduced by the fix are rows M3b-r2-64 and M3b-r2-65."},
    {"id": "M3b-r1-57", "check": "2.7 cards L06 (16 cards read in full; round 1 read 15)",
     "location": "cards.json: M3-c101, c103..c114, c178, c205, c216", "status": P,
     "evidence": "All 16 read and checked: c105 (front now 'for m, n at least 1') matches Theorem 2.2; c106, c107, c108, c112, c113, c114 match Theorems 2.3, Proposition 2.4 and Remark 2.5; c216 matches Theorem 2.2's wording. The duplicate of c101 with c215 is row M3b-r2-64."},
    {"id": "M3b-r1-58", "check": "2.7 grades and basis on slice cards",
     "location": "cards.json: C cards c074, c075, c094-c097, c109-c111, c173, c176, c179", "status": P,
     "evidence": "Each C card has a basis naming the lab and its part. T cards cite a theorem, lemma, proposition or remark on the page. Cards with no grade field are definitions or recall items (c063-c065, c079, c081, c082, c092, c100, c101, c189, c190, c193, c215, c216), not claims."},
    {"id": "M3b-r1-59", "check": "2.7 numbers on cards appear in the lesson",
     "location": "cards.json slice entries vs L04-L06 text and expected blocks", "status": P,
     "evidence": "200 of 200 (L04.html:257-260), 1200 and 1200 of 1200 (L04.html:261-262), 118 of 360 and 4 (L05 expected line 295-296), 500 of 500 and 100000 (L05 lines 298-299), 2.2335/0.9250/0.3348 (L06 line 221), 0.7071 (L04 line 264), 0.0000/1.0000/3.0000 (L05 line 300) all appear in the lesson or its expected block."},
    {"id": "M3b-r1-60", "check": "2.7 card coverage and ids",
     "location": "course/modules/M/M3/cards.json (209 cards in the file; 64 in slice)", "status": P,
     "evidence": "python: 209 cards, 0 duplicate ids; slice 64 cards (L04 20, L05 28, L06 16) all read; every lesson value is an existing lesson; ids match the M3- prefix."},
    {"id": "M3b-r1-61", "check": "2.7 cross-lesson near duplicates (SequenceMatcher on fronts and token overlap)",
     "location": "course/modules/M/M3/cards.json whole file; scripts/M3-b-r2/dup_scan_r2.out", "status": F,
     "evidence": "dup_scan_r2.out finds two same-fact pairs that the round-2 card edits introduced: M3-c101 (L06) with M3-c215 (L04), both the orthogonal-matrix definition; and M3-c085 with M3-c176 (both L05), both the eigenvalues -1 and 3 of [[1,2],[2,1]]. Other high-similarity pairs (c082 with c193; c087 with c088) test different facts (PSD against PD). Fix: rows M3b-r2-64 and M3b-r2-65."},
    {"id": "M3b-r1-62", "check": "gate verify_refs (offline)", "location": "tools/verify_refs.py --offline", "status": P,
     "evidence": "'offline integrity: 560 entries, 0 problems', exit 0 (gates_r2.out)."},
    {"id": "M3b-r1-63", "check": "2.8 figures", "location": "L04-L06 pages", "status": P,
     "evidence": "No figure, svg, canvas or chart element in the three pages (grep). Labs print text only."},
    {"id": "M3b-r2-64", "check": "2.7 cards: duplicate definition of an orthogonal matrix (new in round 2)",
     "location": "course/modules/M/M3/cards.json: M3-c215 (L04) and M3-c101 (L06)", "status": F,
     "evidence": "c215 (new): 'When is a real square matrix Q orthogonal?' answered 'When its columns are orthonormal. Equivalently, Q^T Q = I ... (Definition 1.2)'. c101 (existing): 'What is an orthogonal matrix?' answered 'A square real matrix Q whose columns are orthonormal, that is, Q^T Q = I (Definition 1.1)'. Both test the same definition in the same words. Fix: delete one card. Keep c215 if the definition is taught in L04 (Definition 1.2) and remove c101, or change c101 to Fact 1.2 (Q Q^T = I)."},
    {"id": "M3b-r2-65", "check": "2.7 cards: duplicate eigenvalues of [[1,2],[2,1]] (new in round 2)",
     "location": "course/modules/M/M3/cards.json: M3-c085 (L05, line 582 region) and M3-c176 (L05)", "status": F,
     "evidence": "c085 (round-1 edit): asks 'What are the eigenvalues of [[1, 2], [2, 1]], and what does Theorem 2.1 conclude?' answered 'The eigenvalues are -1 and 3 (Example 2.6) ...'. c176: 'In Lab 1 Part A, what eigenvalues does the lab print for [[1, 2], [2, 1]], sorted?' answered '-1.0000 and 3.0000 (Lab 1 output)'. Same fact. Fix: make c085 ask only Theorem 2.1's conclusion for this matrix (not PSD, because -1 is an eigenvalue), or delete c176."},
]

FIXES = {
    "M3b-r1-33": "L06.html:350 add 'counted with multiplicity'; L06.html:352 add the step: by Theorem 2.3 of Lesson 4 the orthonormal eigenbasis contains the eigenvectors for 0 spanning the 0-eigenspace, so the number of zero eigenvalues counted with multiplicity equals its dimension, which is at least n - m.",
    "M3b-r1-41": "Replace '\\mathrm{diag}(w)' with '\\diag(w)' at course/modules/M/M3/L04.html:176 (the registered macro).",
    "M3b-r1-61": "Resolve the two duplicate pairs listed in M3b-r2-64 and M3b-r2-65, then re-run the cross-lesson scan.",
    "M3b-r2-64": "Delete M3-c101 (L06) or M3-c215 (L04), or change M3-c101 to Fact 1.2 (QQ^T = I).",
    "M3b-r2-65": "Change M3-c085 to ask only Theorem 2.1's conclusion for this matrix, or delete M3-c176.",
}
for _r in rows:
    if _r["status"] != P:
        _r["fix"] = FIXES[_r["id"]]

mutants: list[dict[str, str]] = []

summary = (
    "Slice b (M3 L04-L06 pages, lab twins and their 64 cards), round 2, pin 9294b914: FAIL. "
    "Rows: 65 total, 60 PASS, 5 FAIL (M3b-r1-33 problem R2 gap in L06; M3b-r1-41 L04 line 176 expanded \\mathrm{diag}; "
    "M3b-r1-61 near-duplicate scan; M3b-r2-64 duplicate orthogonal-matrix card; M3b-r2-65 duplicate eigenvalue card). "
    "The four round-1 FAILs 04, 19, 47, 56 are fixed and re-verified (41 is partly fixed: L06 yes, L04 no). "
    "All three labs run, all numbers and proofs were re-derived by independent scripts (44 of 44 checks), "
    "and the page, twin and card gates pass."
)

notes = [
    "Method: full read of course/modules/M/M3/L04.html (521 lines), L05.html (555 lines) and L06.html (470 lines) line by line; "
    "the lab twins tests/labs/M3/lab-M3-L04-1.py, lab-M3-L05-1.py, lab-M3-L06-1.py; all 64 slice cards read in full "
    "(scripts/M3-b-r2/cards_slice.txt). Cross-reference targets in L01, L03 and L08 were read at the cited lines.",
    "Delta from the round-1 pin aeb512b to 9294b914 inside the slice: L04.html:146 (Proposition 2.4 hypothesis); L05.html:130 "
    "(Proposition 2.3 hypothesis) and :303 (interpretation); L06.html:52, 56, 107, 132, 270, 293, 402, 422 (macros, why-it-matters, "
    "convention sentence, quiz prompt); cards M3-c071, c085, c098, c105, c215 (new), c216 (new). Outside the slice: L01, L02, L03 "
    "and index.html edits, cards c037, c042, c054, c201 and the references.json registry; they were not verified beyond the cited "
    "cross-references and hours.",
    "No row is carried from round 1. Every row was re-verified in this round against the pin, so no 'Carried from round 1' prefix is needed.",
    "Gates and commands run on the pinned checkout (outputs in scripts/M3-b-r2/): check_pages --unit M3 PASS; check_dag --unit M3 PASS; "
    "check_projects --unit M3 PASS; verify_refs --offline 560 entries 0 problems; run_labs --unit M3 --page L04, L05, L06 each PASS (1/1); "
    "each twin under python -I -W error exit 0 with empty stderr; ruff check and ruff format --check on the three twins PASS; "
    "mypy --no-incremental on the three twins PASS; pytest tests/test_labs.py -k 'M3 and (L04 or L05 or L06)' exit 0; "
    "page_smoke --unit M3 --pages L04 L05 L06 PASS (Chromium).",
    "Independent numeric re-derivation: scripts/M3-b-r2/recheck_numbers_r2.py run with python -I; output recheck_numbers_r2.out: 44 of 44 checks PASS. "
    "Duplicate scan: scripts/M3-b-r2/dup_scan_r2.out.",
    "Mutants: none written. This slice has no grader; VERIFIER_RULES 2.6 and the ruling apply mutation testing to project graders only, "
    "and lab twins are demonstrations.",
    "Borderline, not failed: cards M3-c108 (I_2 has more than one SVD) and M3-c114 (sign change and I_2 second decomposition, Remark 2.5) "
    "both use the I_2 example. Both are unchanged since round 1 and test different questions, so no fail is recorded. The builder may "
    "still want to differentiate them.",
    "Hours: L04 12, L05 12, L06 11 match the page headers and sum with the other lessons to the hub's 105; no conflict.",
    "Not checked: registry bibliographic data (no source is cited in the slice); live reference verification (offline only by ruling); "
    "the full M3 lab set outside L04-L06; the L01, L02, L03, L07, L08 and L09 pages beyond the cited cross-reference lines; "
    "a human-visible browser screenshot beyond the page_smoke run; a learner walkthrough of the Pyodide runtime.",
]

fragment = {
    "unit": "M3",
    "slice": "b",
    "round": 2,
    "verifier": "independent Haiku verifier, slice b (did not build M3)",
    "pin": "9294b914a51647c66d2dee62c4a112c76ba04900",
    "base": "aeb512b65b7774b59b84f836a13984fcfe9d0d1f (round-1 pin; round-1 fragment at /Users/billyribeiro/.fanout/frags/S-M3-b.round1.json)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyS2-M3-b",
    "scratch": "/Users/billyribeiro/.fanout/wt/verifyS2-M3-b/ledgers/M3/scripts/M3-b-r2",
    "verified_at": "2026-11-08",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": notes,
    "summary": summary,
}

OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, "rows", len(rows), "FAIL", sum(1 for r in rows if r["status"] == F))
