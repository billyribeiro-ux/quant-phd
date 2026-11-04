"""Writes the round-5 fragment ledgers/M3/M3-c.json for slice M3-c (L07-L09 and lab twins). Round 5 at pin 440ed3c.

The rows record what was run and read in this round; the evidence strings cite the logs under
ledgers/M3/scripts/M3-c-r5/ and the page or twin locators. Run: python3 -I <this file> from the checkout root.
"""
import json
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M3-c")
S = "ledgers/M3/scripts/M3-c-r5/"
ROWS = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    ROWS.append(r)


# ---- gates (run in this round on pin 440ed3c)
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3; --page L07, L08, L09",
    "PASS", f"'check_pages M3: PASS' EXIT=0 ({S}check_pages_M3.log); 'check_pages M3 L07|L08|L09: PASS' EXIT=0 ({S}check_pages_L07.log, _L08.log, _L09.log). Hub and other slices are not read here.")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3",
    "PASS", f"'check_dag M3: PASS' EXIT=0 ({S}check_dag_M3.log).")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3",
    "PASS", f"'check_projects M3: PASS' EXIT=0 ({S}check_projects_M3.log). Project content is another slice and is not read here.")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 and --page L07, L08, L09",
    "PASS", f"'run_labs M3: PASS (12/12)' EXIT=0 ({S}run_labs_M3.log); (1/1) PASS for L07, L08, L09 ({S}run_labs_L07.log, _L08.log, _L09.log).")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone",
    "PASS", f"{S}m3c_r5_twin_vs_page.py: each twin run alone as python -I -W error from an empty temporary directory: exit 0, stderr 0 bytes, stdout equals the page expected block (rstrip) for L07, L08, L09 ({S}m3c_r5_twin_vs_page.log).")
row("GATE-06", "2.5-labs", "ruff check and ruff format --check tests/labs/M3",
    "PASS", f"'All checks passed!' EXIT=0 ({S}ruff_check.log); '12 files already formatted' EXIT=0 ({S}ruff_format.log).")
row("GATE-07", "2.5-labs", "mypy --no-incremental (repository configuration)",
    "PASS", f"'Success: no issues found in 331 source files' EXIT=0 ({S}mypy.log).")
row("GATE-08", "2.9-smoke", "tools/page_smoke.py --unit M3 --pages L07, then L08, then L09 (each alone)",
    "PASS", f"'page_smoke M3: PASS' EXIT=0 for each page run alone ({S}page_smoke_pages_L07.log, _L08.log, _L09.log); lab timings 0.0 s.")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline",
    "PASS", f"'offline integrity: 560 entries, 0 problems' EXIT=0 ({S}verify_refs_offline.log). No live run: references/ is unchanged in the delta (git diff --numstat 4eb6788f 440ed3c8 is empty for references/).")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page'",
    "PASS", f"EXIT=0, 100% of selected tests passed ({S}pytest_slice.log). Full suite not run.")
row("GATE-11", "2.6-gate", "tools/run_graders.py --unit M3 --seeds 0-49",
    "PASS", f"'run_graders M3: PASS (reference 50/50 seeds, slowest 0.3 s)' EXIT=0 ({S}run_graders_M3.log). Grader content is another slice.")

# ---- labs: embed, statements, docstrings
row("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1 vs tests/labs/M3/lab-M3-L07-1.py",
    "PASS", f"{S}m3c_r5_twin_vs_page.py: unescaped <code data-run> text equals the twin byte for byte (after rstrip of trailing newline); expected block equals the twin's stdout ({S}m3c_r5_twin_vs_page.log).")
row("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1 vs tests/labs/M3/lab-M3-L08-1.py",
    "PASS", f"As LAB-L07-EMBED; both equal ({S}m3c_r5_twin_vs_page.log).")
row("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1 vs tests/labs/M3/lab-M3-L09-1.py",
    "PASS", f"As LAB-L07-EMBED; both equal, including the round-5 page docstring lines 210-212 and twin lines 16-18 ({S}m3c_r5_twin_vs_page.log).")
row("LABSTMT-L07", "2.5-labs", "L07.html Lab 1 hypothesis (line 125), code (126-192), output (193-203), interpretation (204), key-results row (350)",
    "PASS", "Hypothesis: P symmetric and idempotent, Py = A beta, residual orthogonal, Pythagorean identity, agreement with NumPy to 1e-9; 4-dp coefficients and residual norm; A^T y to 2 dp; duplicated column with rank 2 of 3. Code lines 164-189 print exactly these checks with TOL = 1e-9; output lines 193-203 agree. Interpretation (204) matches the output and the SIMULATED generator (intercept 1.5, slopes 0.8 and -0.4, sd 0.3).")
row("LABSTMT-L08", "2.5-labs", "L08.html Lab 1 hypothesis (line 146), code (147-269), output (270-283), interpretation (284); Definition 3.1 (line 141)",
    "PASS", f"Hypothesis claims (M PSD, MV=VLambda, scores, trace, all to 1e-9; shares from unrounded eigenvalues; matches by largest |cos|; three matches distinct; doubling leaves shares unchanged; column-ten changes first share; E1 bound with its inputs) match code lines 221-266 and output 271-283. The lab matches each planted shape by argmax (code line 243); the lab does not test uniqueness, but on this panel the runner-up |cos| is at most 0.04 against maxima 0.9994, 0.9985, 0.9990 ({S}m3c_r5_numbers.log), so the printed matches are the Definition 3.1 matches.")
row("LABSTMT-L09", "2.5-labs", "L09.html Lab 1 hypothesis (line 193), code (194-335), output (336-348), interpretation (349), key-results rows (499-500)",
    "PASS", "Hypothesis counts (40 seeded 5x5 matrices; W passes the check with symmetry and unit diagonal to 1e-12 and smallest eigenvalue at least -1e-8; strict closeness) match code lines 306-332 (NONPSD_TOL 1e-9, TOL 1e-12, FEASIBLE_TOL 1e-8, MAX_ITER 500). Output 345-348 is 23, 23 of 23, 23 of 23, index-0 distances; the page interpretation (349) and key rows (499-500) quote these values, and m3c_r5_numbers.log reproduces them.")
row("LABDOC-L09", "2.5-labs", "tests/labs/M3/lab-M3-L09-1.py lines 1-20 (docstring) against lines 194-214 and the code 216-335",
    "PASS", "Docstring claims 1-4 (C0 witness -2.4; clipped B PSD with ||C0-B||_F^2 = sum of squared negative eigenvalues; R correlation matrix; 40 seeded matrices, generator 20261028, entries 0.5 plus symmetrised noise with sd 0.35, size 5) match the code (SEED 20261028, N_MATRICES 40, SIZE 5, seeded_matrices lines 272-282).")
row("LABDOC-L09-TOL", "2.5-labs", "tests/labs/M3/lab-M3-L09-1.py lines 16-18 (docstring) against course/modules/M/M3/L09.html line 349 and twin lines 71-76 (is_correlation)",
    "PASS", "Round-4 FAIL is fixed: the docstring now says 'to the tolerance of is_correlation' (lines 16-18), and page line 349 says 'to that tolerance'. is_correlation (twin lines 71-76) tests symmetry and unit diagonal to TOL = 1e-12 and smallest eigenvalue at least -FEASIBLE_TOL = -1e-8, so the 'to the tolerance' scope is true.")
row("LABSTMT-L09-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, runtime)",
    "PASS", "Imports are numpy and __future__ only (no network, no data files); seeds 7, 8 and 20261028 (lines 150, 213, 229 of the twins/pages); page_smoke timings 0.0 s per lab (page_smoke_pages_L0*.log); twins end with bare main() calls.")

# ---- numbers (independent recomputation, m3c_r5_numbers.py)
row("NUM-L07", "2.2-numbers", "L07.html E2 solution (line 302) quoting A^T y; output line 201",
    "PASS", f"Recomputed A^T y = (18.379697, 3.095863, -17.603498) unrounded; 2-dp (18.38, 3.10, -17.60) matches E2 and output ({S}m3c_r5_numbers.log).")
row("NUM-L07-M", "2.2-numbers", "L07.html line 222 (residual norm 0.8951) and E3 (line 307-309, intercept 1.3325)",
    "PASS", f"Recomputed residual norm 0.8951275538 -> 0.8951; beta_0 = 1.3325188472 -> 1.3325 ({S}m3c_r5_numbers.log). Both match the page and the output lines 199-200.")
row("NUM-L08", "2.2-numbers", "L08.html line 284 (shares 75.9, 18.1, 5.2; cosines 0.9994, 0.9985, 0.9990), line 290-291 (0.7587 to 0.9791), E1 (line 377: bound 0.9483, inputs 13.6818 and 88.2028), E3 (line 391: sum 99.2, bound 0.15), key rows 433-434",
    "PASS", f"Recomputed unrounded shares 75.872815%, 18.088840%, 5.161927%; cosines 0.999381, 0.998544, 0.999019; first share 0.7587281517 -> 0.9791448785; bound 100*M11/(trace+99*M11) = 0.9483461173 -> 0.9483, and the bound from the PRINTED inputs 13.6818 and 88.2028 is 0.9483461923 -> 0.9483 (so the printed inputs reproduce the value to four decimals). Sum of printed shares 99.2 vs unrounded sum 99.1236: difference 0.076 <= 0.15 ({S}m3c_r5_numbers.log).")
row("NUM-L09", "2.2-numbers", "L09.html why-it-matters (line 52: 40 inputs, 23 non-PSD); Lab 1 interpretation (349: index-0 distances 0.175527 and 0.163280, the 17 PSD matrices); Example 2.3 (line 106); Example 3.6 (line 179-180: 0.04, 0.08); E2 (line 447: 0.9798); key rows 498-500; R entries (output 342-344)",
    "PASS", f"Recomputed: x^T C0 x = -2.4; eig(C0) = -0.8, 1.9, 1.9; ||C0-B||_F^2 = 0.64 = sum of squared negative eigenvalues; R entries 0.5, 0.5, -0.5 (unit diagonal); ||C0-R||_F = 0.9797958971 -> 0.9798; non-PSD count 23 of 40 (smallest eigenvalues below -1e-9 include -7.81e-4, nearest PSD min eig 0.0309, so the threshold is not borderline); W passes is_correlation 23 of 23 and closer than R 23 of 23; first non-PSD index 0 distances 0.175527 (R) and 0.163280 (W). Example 3.6: A0 = 1.1 off/diag, ||A-A0||^2 = 0.04, ||A-R||^2 = 0.08 ({S}m3c_r5_numbers.log).")

# ---- maths
row("MATH-L07", "2.4-mathematics", "L07.html Definition 1.1 (60), Theorems 1.2 (64-71), 1.3 (84-85), Remark 1.4 (95), Theorem 2.2 (108-113), proofs (75-81, 88-90, 117-121); problems M1-M3 (243-259), P1-P3 (268-284), E1-E3 (293-309), R1-R3 (318-334)",
    "PASS", "Re-derived each proof: G invertibility (eigenvalues ||Av||^2 > 0), P symmetric and idempotent, closest-point expansion, uniqueness, normal equations equivalence. M2 by hand: normal equations give beta1 = 1/2 and beta0 = 7/6, fitted 7/6, 5/3, 13/6, residuals -1/6, 1/3, -1/6, all as printed. R1 existence argument (lines 318-320) re-checked: Theorem 3.7 of Lesson 1 exists (L01.html line 161) and gives the length bound; the W = {0} case is handled. R2, R3 re-derived. Hypotheses (F1-F4 of Lesson 4, L04.html lines 56-62) stated on each theorem.")
row("MATH-L08", "2.4-mathematics", "L08.html Proposition 1.1 (61-62), Proposition 1.2 (71-72), Definition 1.3 (82), Theorem 1.4 (86-87), Theorem 2.1 (100-104), proof (110-112), Corollary 2.2 (116-117), Proposition 2.3 (121-122), Remark 2.4 (131-132); problems M1-M3 (324-342), P1-P3 (349-366), E1-E3 (374-391), R1-R3 (399-416)",
    "PASS", "Re-derived: M symmetric PSD; trace identity; Z^TZ/(T-1) = Lambda; Rayleigh bound and equality case; scaling by c^2 with order preserved; Remark 2.4 (M_jj > 0 from the e_j + t e_l argument; kappa = c forced by M_jl != 0; c^2 != c). Worked numbers: M1 trace 17, det 3, eigenvalues (17 +/- sqrt 277)/2; M2 shares 2/3, 1/6, 1/6; M3 eigenvalues 18, 9; R3 BGB^T factorisation and eigenbasis BQ re-derived. E1 bound direction correct (Proposition P3 gives lambda_1' >= 100 M11). Remark 2.4 last sentence ('For c = 1 nothing changes. The shares can then change.') is ambiguous in wording but the excluded case is clear from the preceding sentences, and the existence claim rests on the one lab case; see PROSE-REMARK-2.4.")
row("MATH-L09", "2.4-mathematics", "L09.html Definition 1.1 (60), Lemma 1.3 (74-75; proof 78-84), Definition 2.1 (93), Definition 3.1 (116-118), Propositions 3.2 (122-126; proof 130-134), 3.3 (138-141; proof 146-147), 3.4 (151-152; proof 157-159), 3.5 (163-164; proof 169-173), Examples 2.3 (104-107) and 3.6 (178-180); problems M1-M3 (388-406), P1-P3 (413-429), E1-E3 (438-456), R1-R3 (463-479)",
    "PASS", "Re-derived each proof, including the trace-cyclic Frobenius identity in Lemma 1.3, the eigen-decomposition argument in Proposition 3.2, the squared-distance formula of Proposition 3.3(a), the congruence in Proposition 3.4 (S = D^{-1/2} symmetric), and the off-diagonal argument of Proposition 3.5 (delta(-2|b_ij| + delta b_jj) < 0). Example 3.6 values re-derived: eigenvalues 2.2 and -0.2, A0 = 1.1 J, R = J (all ones). Problem M3 (characteristic roots (13 +/- sqrt 41)/2 from trace 13 and determinant 32; C entries 1, 1, 1/3). Problem E3 gives 0.5. No hypothesis missing: Proposition 3.5 uses symmetry as well as PSD.")

# ---- curriculum-facing prose and structure
row("PROB-L07", "2.2-problems", "L07.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 241-336)",
    "PASS", "Three problems per tier (mechanics, proof, empirical, research), each with a worked solution in details.solution; solutions re-checked above (M1 P = (1/2)[[1,1],[1,1]]; M2 fit; M3 P = diag(1,0)).")
row("PROB-L08", "2.2-problems", "L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 324-416)",
    "PASS", "Three problems per tier with worked solutions; M1 numbers (M = [[4,7],[7,13]], trace 17, det 3) and E1 bound re-derived.")
row("PROB-L09", "2.2-problems", "L09.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (lines 386-479)",
    "PASS", "Three problems per tier with worked solutions; M2 Frobenius 4.88, M3 rescaling C entries 1, 1/3, E2 0.9798 re-derived.")
row("GRADE-L07", "2.3-grades", "L07.html grade spans (block titles 64, 84, 108) and key-results table (346-350)",
    "PASS", "T for Theorems 1.2, 1.3, 2.2 (proved on the page, so T is correct); the lab-output row (350) is C with the lab named (BLUEPRINT 3: a finite numerical check is C naming the lab).")
row("GRADE-L08", "2.3-grades", "L08.html grade spans (61, 71, 86, 100, 116, 121) and key-results table (428-434)",
    "PASS", "All proved results T; lab-derived rows 433-434 are C and name Lab 1 with the single-panel caveat. Definition 3.1 has no grade and claims no outside source.")
row("GRADE-L09", "2.3-grades", "L09.html grade spans (74, 122, 151, 163) and key-results table (491-500)",
    "PASS", "Proved results and examples T; the two lab-derived rows (499-500) are C naming Lab 1 and the seeded finite check.")
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (data-cite, data-locator; references sections)",
    "PASS", "No data-cite or data-locator attribute appears in L07-L09 (grep); each references section is empty or states that no outside source is used (L07 line 430, L08 line 518). Nothing is attributed, so no registry key is checked.")
row("XREF-EARLIER", "2.4-mathematics", "L07, L08, L09 cross-references to earlier lessons",
    "PASS", "L07 line 75 'Fact 1.2 of Lesson 6' (L06.html line 64, Fact 1.2: orthonormal columns of a square matrix, giving VV^T = I); line 320 'Theorem 3.7 of Lesson 1' (L01.html line 161); L08 line 82 'Theorem 2.3 of that lesson' (L04.html line 130); L08 line 137 'Lesson 7, Theorem 1.2' (L07.html line 65); L08 line 293 'Lesson 6 notes the same sign freedom' (L06.html lines 229 sign flip); L09 line 112 'Lesson 4, Theorem 2.3' (L04.html line 130); L09 line 38, 56 'Lesson 5' (L05.html line 72 dfn; Theorem 2.1 at line 108 gives PSD iff eigenvalues nonnegative, as cited in L09 M1 solution line 390); L09 line 112 'Lesson 3' eigenvalues (L03 dfn at line 109).")
row("NOTATION-R", "2.4-notation", "L07, L08, L09 math using \\R (real numbers)",
    "PASS", "\\R is registered (notation/notation.json macros: 'real numbers'); used only for real vector and matrix spaces.")
row("NOTATION-OPNAME", "2.4-notation", "L08.html line 402 (\\operatorname{span}); L09.html line 171 (\\mathrm{sign}); \\tr and \\diag throughout",
    "PASS", "\\tr registered as matrix trace; \\diag registered as diagonal matrix; \\operatorname and \\mathrm are standard KaTeX (not program-wide symbols).")
row("NOTATION-T", "2.4-notation", "L08.html Section 1 (T x n matrix, T >= 2, T = 750)",
    "PASS", "Registry symbol T: 'number of return observations (periods) in a sample'; in L08 it is the number of observations (rows) of the panel, consistent with that meaning.")
row("NOTATION-AST", "2.4-notation", "L09.html line 93 (C^{\\ast}, nearest correlation matrix)",
    "PASS", "Registry registers R^\\ast (SDF payoff return, AP1), not a general superscript; C^{\\ast} is a distinct symbol with its own meaning in L09 and is not used for the registered object. No collision.")
row("NOTATION-Q", "2.4-notation", "L07.html and L09.html (orthogonal Q)",
    "PASS", "Q is used for an orthogonal matrix (Q^TQ = I); no registered symbol Q exists (only \\mathbb{Q}, the probability measure, which the slice does not use).")
row("NOTATION-OTHER", "2.4-notation", "all control sequences in L07-L09 math and twins (macro counts in m3c_r5_numbers and the scan logs)",
    "PASS", f"Control sequences used: \\top, \\lambda, \\varepsilon, \\beta, \\sum, \\lVert, \\tilde, \\hat, \\gamma, \\ldots, \\diag, \\tr, \\R and others. Program-wide macros in notation.json (\\R, \\tr, \\diag, \\ast via R^\\ast only) keep their meanings; the Greek letters are local and allowed by the registry note; \\iota and \\tau are local shape/tenor letters. Scan: {S}m3c_r5_prose_scan.log.")

# ---- defined terms, DAG, prose
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Definition 3.1 (line 141), quiz item L08q9 (line 505) and explanation (line 511)",
    "PASS", "The three places now agree: Definition 3.1 states the unique-maximum rule; the quiz asks for 'the one principal direction with the largest absolute cosine'; the explanation states the tie case gives no label.")
row("DEF-L08-MATCH", "2.9-structure", "L08.html Definition 3.1 (line 141): match defined as the principal direction with the largest |cos|, provided exactly one attains it; canon-break (292); quiz explanation (511)",
    "PASS", f"Round-4 FAIL is fixed: Definition 3.1 gives no match on a tie, so the 'largest cosine' match is well defined. The round-4 tie case (diag(3,2,1)) is now covered by the rule: no match when two principal directions tie. The lab uses argmax on the planted panel with no tie (runner-up |cos| 0.032, 0.040, 0.040 against maxima 0.9994, 0.9985, 0.9990; {S}m3c_r5_numbers.log). Canon-break line 292 states the no-match rule. Lab 1 does not test uniqueness and no sentence claims that it does.")
row("DAG-LINKS", "2.9-structure", "L07.html, L08.html, L09.html meta rows (lines 38-39 in L07; 38-39 in L08 and L09)",
    "PASS", "check_dag M3: PASS (GATE-02). Each link target exists and is earlier: vector-space (L01), eigendecomposition (L03), spectral-theorem (L04), positive-semidefinite-matrix (L05). Self links for orthogonal-projection, least-squares-projection, principal-component-analysis, level-slope-curvature, nearest-correlation-matrix and eigenvalue-clipping are the lesson's own dfn ids, each defined once in this slice.")
row("DAG-M4", "2.9-structure", "L07, L08, L09 (covariance, variance, correlation, Gaussian, standard deviation wording)",
    "PASS", "No covariance-matrix, variance or expectation word on L07 or L08 (scan {S}m3c_r5_prose_scan.log, concept-words group). L09 uses 'correlation matrix' as the lesson's own defined term (Definition 1.1), with no link to the M4 concept 'correlation' and no M4 prerequisite; this is the plain-descriptor use permitted by architect decision B1/Q2 (plans/M3-build-plan.md, Architect decisions).")
row("DAG-PSD-REDEF", "2.9-structure", "course/modules/M/M3/L09.html line 56 (Section 1 restates the defining condition of positive semidefinite) versus course/modules/M/M3/L05.html line 72 (dfn def-positive-semidefinite-matrix)",
    "FAIL", "L09.html line 56 reads 'a symmetric C is <a class=\"concept\" data-concept=\"positive-semidefinite-matrix\" ...>positive semidefinite</a> when x^{\\top} C x \\ge 0 for every vector x, as defined in Lesson 5.' The defining condition is restated on the page. L05.html line 72 defines the registered concept with the same condition. The round-4 defect (a restatement) is still present: 440ed3c adds the link and the 'as defined in Lesson 5' pointer but keeps the defining clause. BUILDER_RULES 1.10 requires linking to the earlier definition instead of restating it.",
    "L09.html line 56: delete the clause 'when \\(x^{\\top} C x \\ge 0\\) for every vector \\(x\\)', so the sentence reads 'a symmetric \\(C\\) is positive semidefinite (Lesson 5)', keeping the link element. No other change is needed. Re-run check_dag and check_pages for M3.")
row("DAG-PROSE-UNLINKED", "2.9-structure", "unlinked prose mentions of registered prior concepts: L08.html line 137 (orthogonal projection, from L07), line 52, 62 (positive semidefinite), L08 line 52 and L09 line 112 (spectral theorem)",
    "PASS", "The VERIFIER 2.9 criterion is order and no double definition, and both hold (check_dag M3 PASS; no concept used before its lesson). BUILDER_RULES 4.1 asks for a link on every use of an earlier concept; these prose mentions are not linked. Noted for the builder, not a verifier failure under 2.9.")
row("PLAIN-REDEF", "2.9-structure", "plain terms restated across lessons: L09.html line 56 and L08 line 58 (trace); L09.html Definition 1.2a (orthogonal matrix, also L06.html Definition 1.1 line 59); L07.html line 56 (subspace, also L01)",
    "PASS", "These are plain terms, not registered concepts (curriculum.json has no entry for orthogonal-matrix, subspace or trace). Each restatement is equivalent to the earlier definition (Q^TQ = I and QQ^T = I are equivalent for square Q by L06 Fact 1.2). No contradiction. Noted as redundancy only.")
row("DEFINE-BEFORE-USE", "2.9-structure", "first uses of tenor, trace, cosine, subspace, column space, orthogonal, null space, PSD, eigenvalue clipping, and roadmap terms in why-it-matters (L07 line 52, L08 line 52, L09 line 52)",
    "PASS", "Plain terms are defined before first use in the body (tenor and trace L08 56-58; cosine L08 137; subspace and column space L07 56; PSD in L09 56 via Lesson 5). The why-it-matters paragraphs name later definitions explicitly ('Definition 1.3 of this lesson', 'Definitions 1.2 and 2.1', 'Method 1, Section 4'), which is a roadmap, not a use before definition.")
row("PROSE-PROCESS", "2.9-structure", "L07.html, L08.html, L09.html learner text (process-word scan)",
    "PASS", f"No 'builder', 'verifier', 'architect', 'ledger', 'open item', 'DAG' or planner word in learner text; matches were substrings ('unrounded', 'data-correct'). Scan {S}m3c_r5_prose_scan.log.")
row("PROSE-ELLIPSIS", "2.9-structure", "quiz stems ending in an ellipsis: L07 lines 398 and 412; L08 lines 445, 459, 505; L09 lines 530 and 539",
    "PASS", "Each is a completion stem ('... is…') whose options supply the missing words, not an ellipsis standing for omitted lesson content. Accepted as the quiz format; no content is omitted.")
row("PROSE-SCOPE", "2.2-scope", "scope words in L07-L09 (every, all, always, any, only, exactly, same, never, generic, stable, typically, robust, in practice): scan {S}m3c_r5_prose_scan.log",
    "PASS", "Each universal or scope claim is backed by a proof (for example L07 lines 68-80, 85-90; L08 lines 110-112, 117, 122-127; L09 lines 141-147, 159, 164-173) or by the tested scope named in the sentence (L08 line 146, 'Doubling every entry'; L09 line 52 and 349, 'in all 23' of 23; L09 line 356, 'not always' is supported by the 23 instances of Lab 1). 'Any choice' (L09 line 118) is backed by Propositions 3.2-3.5, whose proofs use only Q orthogonal and Lambda diagonal.")
row("PROSE-REMARK-2.4", "2.9-structure", "L08.html Remark 2.4, final sentences (line 132: 'For c = 1 nothing changes. The shares can then change.')",
    "PASS", "The existence claim 'the shares can change' is supported by the one Lab 1 case (0.7587 to 0.9791, output line 282) and graded C in key row 434 as a single case. The phrase 'then' refers to the excluded case c not in {0, 1} of the same paragraph. Wording could be clearer; not a failure.")
row("STRUCT-WHY", "2.9-structure", "L07 line 52, L08 line 52, L09 line 52 why-it-matters",
    "PASS", "Word counts (tags stripped, math text kept): L07 110, L08 109, L09 115, all within BUILDER_RULES 4.2's 120-word limit ({S}m3c_r5_prose_scan.log).")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts (BUILDER_RULES 4.2)",
    "PASS", "Order: why-it-matters, core sections with Definition/Theorem/Proof/Remark blocks, inline lab, canon-breaks, misconceptions (3 each), problem set (3 per tier: mechanics, proof, empirical, research, each with a worked solution), key-results table, retrieval quiz (L07 9 items, L08 9, L09 11), references. No debate brief is required (M3 has no debate key, curriculum.json).")
row("HOURS", "2.9-structure", "L07.html data-hours 11 (line 2), L08.html 12 (line 2), L09.html 12 (line 2)",
    "PASS", "Hours 11, 12, 12 match plans/M3-build-plan.md section 2.2 (Lessons L07 11, L08 12, L09 12). Hub split and total are checked by check_pages M3: PASS (GATE-01); hub is another slice.")
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) and Lab 1 heading (line 145)",
    "PASS", "Claim: the program does not embed a multi-tenor series from which three or more tenors can be read. course/assets/data/market/MANIFEST.json: ust_daily columns are tbill_3m and cmt_10y only; fx_daily and fx_monthly are currency series. tools/data_sources.yaml lines 91-116 agree. The claim is true; the lesson does not claim a real-curve result.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291) and Lab 1 heading (line 145)",
    "PASS", "The curriculum's Treasury lab is stated as not run, and L08 uses a SIMULATED panel, consistent with architect decision B2/Q1 (plans/M3-build-plan.md, Architect decisions).")
row("SIMULATED-LABELS", "2.8-data", "L07 lines 124-125, 128; L08 lines 145-146, 149; L09 lines 52, 193, twin docstring lines 1-10 and 202",
    "PASS", "Every generated input carries the SIMULATED label on the page and in the twin docstring, and no real data is read by L07-L09 (no data-files attribute).")

mutants = []
fragment = {
    "unit": "M3",
    "slice": "c",
    "round": 5,
    "verifier": "independent Haiku verifier (round 5), checkout verifyD5-M3-c",
    "pin": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-M3-c",
    "scratch": "system temp directories created per twin run (tempfile.TemporaryDirectory, removed after each run); no other scratch",
    "verified_at": "2026-11-03",
    "verdict": "FAIL",
    "rows": ROWS,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta read hunk by hunk from 4eb6788f to 440ed3c8 (git diff --numstat): L07.html 1 line (R1 statement, line 318); "
        "L08.html 4 lines (Definition 3.1 line 141, canon-break line 292, quiz item L08q9 lines 507 and 511); "
        "L09.html 6 lines (meta description line 7, why-it-matters line 52, Section 1 line 56, lab docstring lines 210-212); "
        "tests/labs/M3/lab-M3-L09-1.py 3 lines (docstring lines 16-18). No change in notation/, tools/, curriculum/, references/, atlas/, plans/ or course assets between the two pins. "
        "All three pages were read in full line by line (L07 443 lines, L08 531, L09 606) and both twins in full. Every round-4 row was re-derived; "
        "every row whose subject changed was re-verified. Mutants: none, because slice c has no grader and VERIFIER_RULES 2.6 mutation testing applies to project graders only (plan 11, rulings). "
        "Not checked: cards.json entries for L07-L09 (another slice); project.html, grader/ and the hub index (other slices); a full pytest run (only the selected slice tests); a live verify_refs run; a light/dark 360 px screenshot (page_smoke only). "
        "Pre-existing files: ledgers/M3/M3-c.json held a round-18 fragment from an earlier history (pin 8f80909), which this round overwrote as instructed; "
        "ledgers/M3/scripts/M3-c-r5/build_fragment_r5.py, embed_and_numbers_r5.py and recompute_numbers_r5.py are tracked files from commit 44f1eb6a that this verifier did not write and did not rely on. "
        "The verifier's own scripts are m3c_r5_twin_vs_page.py, m3c_r5_numbers.py, m3c_r5_prose_scan.py and m3c_r5_write_fragment.py, with their logs; gates.sh ran the standard gates."
    ),
    "summary": "",
}
n_fail = sum(1 for r in ROWS if r["status"] != "PASS")
n_pass = len(ROWS) - n_fail
fragment["summary"] = (
    f"M3 slice c round 5 at pin 440ed3c: {len(ROWS)} rows (pass={n_pass}, fail={n_fail}, unverifiable=0). "
    "The one FAIL is DAG-PSD-REDEF (L09.html line 56 still restates the Lesson 5 definition of positive semidefinite). "
    "The round-4 FAILs DEF-L08-MATCH and LABDOC-L09-TOL are fixed and now PASS. Every gate passes: check_pages, check_dag, check_projects, run_labs (12/12), "
    "twins alone under python -I -W error, page code and expected blocks equal the twins, ruff, mypy --no-incremental, pytest slice, page_smoke per page, verify_refs --offline, run_graders 50/50. "
    "Every quoted number was recomputed independently (m3c_r5_numbers.log)."
)
out = ROOT / "ledgers/M3/M3-c.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "rows", len(ROWS), "fail", n_fail)
