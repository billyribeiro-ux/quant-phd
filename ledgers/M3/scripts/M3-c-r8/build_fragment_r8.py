"""Builds ledgers/M3/M3-c.json (round 8) from the row table below. Evidence lives in the cited outputs."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
S = "ledgers/M3/scripts/M3-c-r8"
O = f"{S}/out"

rows: list[dict[str, str]] = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    item = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        item["fix"] = fix
    rows.append(item)


# Gates (commands run on the pin 2d755599; outputs kept under out/).
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3, then --page L07, --page L08, --page L09", "PASS",
    f"{O}/check_pages_M3.out: 'check_pages M3: PASS' (exit 0); {O}/check_pages_L07.out, _L08.out, _L09.out: each 'PASS' exit 0.")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS",
    f"{O}/check_dag_M3.out: 'check_dag M3: PASS' exit 0. Independent DAG reading in DAG-LINKS and DAG-M4.")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
    f"{O}/check_projects_M3.out: 'check_projects M3: PASS' exit 0 (project not in slice c; run because it is a unit gate).")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3", "PASS",
    f"{O}/run_labs_M3.out: 'run_labs M3: PASS (12/12)' exit 0.")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone, python -I -W error, cwd a fresh /tmp directory",
    "PASS", f"{S}/twin_vs_page.py -> {O}/twin_vs_page.out: each twin exit 0, stderr 0 bytes, 'expected == output: True' for L07, L08, L09.")
row("GATE-06", "2.5-labs", "ruff check and ruff format --check tests/labs/M3", "PASS",
    f"{O}/ruff_check_labs.out: 'All checks passed!' exit 0; {O}/ruff_format_labs.out: '12 files already formatted' exit 0.")
row("GATE-07", "2.4-gate", "mypy --no-incremental (repository configuration)", "PASS",
    f"{O}/mypy.out: 'Success: no issues found in 385 source files' exit 0.")
row("GATE-08", "2.9-gate", "tools/page_smoke.py --unit M3 --page L07, then L08, then L09 (each alone)", "PASS",
    f"{O}/page_smoke_L07.out, page_smoke_L08.out, page_smoke_L09.out: each 'page_smoke ... PASS', exit 0, lab timing 0.0 s, boot 1.1-1.2 s.")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
    f"{O}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems' exit 0. Not run: the --unit form is a live network run; slice c cites no registry key (CITE-L07-L09).")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page'", "PASS",
    f"{O}/pytest_relevant.out: 395 tests, all dots, exit 0.")

# Lab twins and page code.
row("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1 vs tests/labs/M3/lab-M3-L07-1.py", "PASS",
    f"{S}/twin_vs_page.py -> {O}/twin_vs_page.out 'L07 code == twin: True' (page code unescaped, compared with the twin byte-for-byte after rstrip).")
row("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1 vs tests/labs/M3/lab-M3-L08-1.py", "PASS",
    f"{O}/twin_vs_page.out 'L08 code == twin: True'.")
row("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1 vs tests/labs/M3/lab-M3-L09-1.py", "PASS",
    f"{O}/twin_vs_page.out 'L09 code == twin: True'.")
row("LABSTMT-L07", "2.5-labs", "L07.html line 125 (hypothesis), code 126-192, expected 193-203, interpretation 204", "PASS",
    f"Hypothesis matches code: P symmetric, idempotent, Py = A beta, residual orthogonal, Pythagorean identity, direct-solver agreement, 4-dp coefficients and residual norm, 2-dp A^T y, duplicated column rank 2 of 3, null-direction equal fits (twin main()). Expected block equals the twin's output (twin_vs_page.out). Independent values in {S}/out/m3c_r8_numbers.out (QR coefficients 1.3325 0.8488 -0.4120; residual norm 0.8951; A^T y 18.38 3.10 -17.60; rank 2).")
row("LABSTMT-L08", "2.5-labs", "L08.html line 146 (hypothesis), code 147-269, expected 270-283, interpretation 284", "PASS",
    f"Hypothesis matches code: T = 750, six tenors, scales 8, 4, 2 bp and noise 0.5 bp, M PSD, MV = V Lambda, Z^T Z/(T-1) = Lambda, trace identity, shares from unrounded eigenvalues, three distinct matches, doubling and 0.25-year rescaling, Problem E1 bound with inputs. Expected equals output (twin_vs_page.out). Independent route {O}/jacobi_alt.out (Jacobi on M) reproduces every printed share and cosine.")
row("LABSTMT-L09", "2.5-labs", "L09.html line 190 (hypothesis: 'For 40 SIMULATED seeded 5 x 5 matrices, the lab counts how many alternating-projection outputs W pass its correlation check')", "FAIL",
    f"Code (twin main(), the loop over seeded_matrices with 'if eigvalsh(a)[0] >= -NONPSD_TOL: continue') computes W only for the non-PSD matrices; the printed denominator is the non-PSD count: page expected block (L09.html lines 343-344) reads '23 of 23' (not 'of 40'). The hypothesis's first count is therefore over a population the lab does not compute. The second clause and the interpretation (line 346) are correct.",
    "Rewrite the first count of the hypothesis to the population the code uses, e.g. 'For the non-PSD matrices among 40 SIMULATED seeded 5 x 5 matrices, the lab counts how many alternating-projection outputs W pass its correlation check ... and how many have W passing that check and ||A - W||_F strictly below ||A - R||_F.' Then re-embed with tools/embed_labs.py --refresh if the twin changes; the twin does not need to change.")
row("LABSTMT-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, network, runtime)", "PASS",
    "Imports: numpy and numpy.typing only (static read of each twin). Seeds explicit: default_rng(7), default_rng(8), default_rng(20261028). No network calls. page_smoke lab timing 0.0 s each (GATE-08).")
row("LABDOC-L09", "2.2-lab-prose", "tests/labs/M3/lab-M3-L09-1.py docstring claims 1-4 (lines 191-211 of the page code) vs code", "PASS",
    "Claim 1 (C0 entries, witness -2.4), claim 2 (clip gives B; ||C0-B||_F^2 = sum of squared negative eigenvalues), claim 3 (R correlation matrix), claim 4 (40 matrices, seed 20261028, non-PSD repaired two ways, counts) each match the code and printed lines 287-345. 'each raw entry with standard deviation 0.35' is the pre-symmetrisation noise; after (N+N^T)/2 the off-diagonal sd is 0.35/sqrt(2). The phrase names the raw entry, so it is accurate.")
row("LABDOC-L09-TOL", "2.2-lab-prose", "L09.html lines 190 and 346 vs twin constants TOL=1e-12, FEASIBLE_TOL=1e-8, NONPSD_TOL=1e-9", "PASS",
    "Hypothesis and interpretation quote 1e-12 (symmetry, unit diagonal), -1e-8 (smallest eigenvalue) and -1e-9 (non-PSD cut) exactly as the twin's constants and is_correlation().")

# Numbers (re-derived by {S}/m3c_r8_numbers.py and {S}/jacobi_alt.py).
row("NUM-L07", "2.2-numbers", "L07.html line 222 (residual 0.8951), 302 (A^T y), 307-309 (intercept 1.3325), 199-203 expected block", "PASS",
    f"{O}/m3c_r8_numbers.out: QR beta 1.3325 0.8488 -0.4120; residual norm 0.8951; A^T y 18.38 3.10 -17.60; M2 exact b0 = 7/6 and quiz tolerance check True; M1 Py = (1, 1); M3 25 = 9 + 16.")
row("NUM-L07-M", "2.2-numbers", "L07.html line 350 (rank 2 of 3) and the lab's duplicated-column check", "PASS",
    f"{O}/m3c_r8_numbers.out: rank of A^T A with a duplicated column = 2.")
row("NUM-L08", "2.2-numbers", "L08.html lines 284 (75.9, 18.1, 5.2; cosines 0.9994, 0.9985, 0.9990), 290-291 (0.7587 to 0.9791), 377 (0.9483; 13.6818; 88.2028), 391 (99.2, 0.15), 307-308 (4 x)",
    "PASS",
    f"Unrounded shares 75.872815, 18.088840, 5.161927 (percent) round to 75.9, 18.1, 5.2 (m3c_r8_numbers.out, jacobi_alt.out). Unrounded |cos| 0.999381, 0.998544, 0.999019 round to 0.9994, 0.9985, 0.9990; the minimum 0.998544 supports 'at least 0.9985' (misconception 1). First share 0.7587 to 0.9791 (4 dp, both routes). Bound 100 M11/(trace+99 M11) = 0.948346 from unrounded M11 13.6818..., trace 88.2028...; the printed inputs reproduce 0.9483. Printed-sum bound: unrounded sum 99.1235 differs from 99.2 by 0.0765, within 0.15 (E3).")
row("NUM-L09", "2.2-numbers", "L09.html lines 52, 336 (0.6400), 346-347, 444 (0.9798), 452 (0.25, 0.5), 497 (0.175527, 0.163280), 495 (0.04, 0.08)",
    "PASS",
    f"{O}/m3c_r8_numbers.out and {O}/jacobi_alt.out: C0 eigenvalues -0.8, 1.9, 1.9; ||C0-B||_F^2 = 0.6400000000 = sum of squared negative eigenvalues; R = [[1, .5, .5], [.5, 1, -.5], [.5, -.5, 1]]; ||C0-R||_F = sqrt(0.96) = 0.979796; Example 3.6 A_0 = 1.1 J, ||A-A_0||^2 = 0.04, ||A-R||^2 = 0.08; 40 seeded matrices, 23 non-PSD, 23 of 23 feasible, 23 of 23 closer; index-0 distances 0.17552673 and 0.16328044; E3 spectrum gives 0.5; M2 ||A||_F^2 = 4.88 = 2.2^2 + 0.2^2.")
row("ALT-L09", "2.5-labs (robustness)", "tests/labs/M3/lab-M3-L09-1.py repair procedure vs alternative correct procedures", "PASS",
    f"{S}/jacobi_alt.py (pure-Python cyclic Jacobi eigensolver, no LAPACK; same inputs and generator) -> {O}/jacobi_alt.out: eigenvalues -0.8, 1.9, 1.9; R identical; 23 non-PSD; 23 feasible; 23 closer; index 0 distances 0.175527 and 0.16328. Lab's stop rule (change < 1e-12 or 500 steps) reproduced.")
row("ALT-L08", "2.5-labs (robustness)", "L08.html Lab 1 PCA route vs a Jacobi eigensolver", "PASS",
    f"{S}/jacobi_alt.py -> {O}/jacobi_alt.out: Jacobi eigenvalues of M 66.921912, 15.954855, 4.552961, ...; shares 75.872815/18.088840/5.161927; residual |Mv - lambda v| 1.1e-14; best-match cosines 0.999381 (PC1), 0.998544 (PC2), 0.999019 (PC3); rescaled first share 0.9791; bound 0.9483.")

# Math (every displayed result re-derived by hand; numeric spot checks in scripts).
row("MATH-L07", "2.4-math", "L07.html Definition 1.1 (line 60), Theorem 1.2 (64-71) and proof (75-81), Theorem 1.3 (84-85) and proof (90), Remark 1.4 (95), Definition 2.1 (104), Theorem 2.2 (108-113) and proof (119-120)",
    "PASS",
    "Re-derived step by step: G symmetric positive definite (x^T G x = ||Ax||^2 > 0), inverse via V Lambda^{-1} V^T with VV^T = I (Lesson 6 Fact 1.2, assumed under F1); A^T(y-p) = 0; uniqueness via p'-p orthogonal to itself; P symmetric and idempotent; Theorem 1.3 cross term vanishes; Remark 1.4 with w = 0; Theorem 2.2 (a)-(c) from Theorem 1.3 and the normal equations. Numeric check: {O}/m3c_r8_numbers.out (P_svd vs inverse formula 1.9e-16; A^T residual 5e-15).")
row("MATH-L08", "2.4-math", "L08.html Proposition 1.1 (61-62), Proposition 1.2 (71-72), Definition 1.3 (82), Theorem 1.4 (86-93), Theorem 2.1 and proof (100-113), Corollary 2.2 (116-117), Proposition 2.3 and proof (121-127), Remark 2.4 (131-133), Section 3 (137) and Definition 3.1 (141), Problems P1-P3, R1-R3",
    "PASS",
    "Re-derived: M symmetric and PSD (Prop 1.1); trace identity (Prop 1.2); Z^T Z = (T-1) V^T M V = (T-1) Lambda (Thm 1.4); Theorem 2.1(a) by alpha-expansion and equality case; (b) for u orthogonal to v_1..v_{k-1}, alpha_1..alpha_{k-1} = 0 and lambda_i <= lambda_k for i >= k; Corollary 2.2; Prop 2.3 (c^2 M, order preserved since c^2 > 0); Remark 2.4 (M_jj > 0 from the 2tM_jl + t^2 M_ll argument, then M_jj(c^2 - c) = 0 contradiction); Section 3 identity tau^2 = -ab iota + (a+b) tau for two values (checked, residual 5e-16 for (1,2)); Definition 3.1 needs at least three values (curvature residual 0.8165 for (1,2,3), 21.07 for six lab tenors; {O}/jacobi_alt.out). Problems: M1 (M = [[4,7],[7,13]], trace 17, det 3, eigenvalues (17 +/- sqrt 277)/2), M2, M3 (shares 2/3, 1/3), P1-P3, R1-R3 re-derived.")
row("MATH-L09", "2.4-math", "L09.html Definition 1.1 (59-60), Definition 1.2 (64-65), Lemma 1.3 and proof (74-82), Definition 2.1 (89-90), Remark 2.2 (95), Example 2.3 (99-105), Definition 3.1 (112-115), Propositions 3.2-3.5 and proofs (119-171), Example 3.6 (174-177), Method 1 and 2 (182-184), Problems M1-M3, P1-P3, E1-E3, R1-R3",
    "PASS",
    "Re-derived: Lemma 1.3 needs only Q^T Q = I (tr(XY) = tr(YX)); Prop 3.2 (a) PSD and eigenvalues max(lambda, eps), (b) x^T A_eps x >= eps ||x||^2 with Q orthogonal (QQ^T = I by Lesson 6 Fact 1.2 under F1), so PD and invertible; Prop 3.3 (a) distance formula, (b) equality iff all lambda >= eps; Prop 3.4 congruence with D^{-1/2}; Prop 3.5 with t = -delta sign(b_ij), delta = |b_ij|/(1+b_jj) (bracket < -|b_ij|); Example 3.6 eigenvalues 2.2, -0.2, A_0 = 1.1 J, R = J, distances 0.04 and 0.08; M1 (eigenvalues 1.6, 0.4), M3 (lambda^2 - 13 lambda + 32, C = [[1, 1/3], [1/3, 1]]), P1 (|C_ij| <= 1 via t = +/-1), P2, P3, R1-R3 re-derived. Numbers: {O}/m3c_r8_numbers.out.")
row("PROP23-HYP", "2.4-math", "L08.html Proposition 2.3 statement (122), proof (127), E2 (384), key row 432", "PASS",
    "Hypotheses listed: real X, c nonzero, sum of eigenvalues > 0 for the shares. E2 and the key row restate them. Proof uses the centred data of cX = c X~ and M -> c^2 M.")
row("KEY-L08-430", "2.9-key-results", "course/modules/M/M3/L08.html key-results row line 430 against Theorem 1.4 (line 87)", "PASS",
    "Row states the scores identity and the shares summing to 1 under the positive sum; Theorem 1.4 states the same with the same hypotheses (F1-F4 and sum positive).")
row("PROB-L07", "2.4-math", "L07.html problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 241-336)", "PASS",
    "Every solution re-derived; E1-E3 numbers match the lab output (0.8951, 18.38/3.10/-17.60, 1.3325); R1 existence/uniqueness argument checked (basis via Lesson 1 Theorem 3.7; W = {0} case); R2 and R3 identities checked.")
row("PROB-L08", "2.4-math", "L08.html problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 323-419)", "PASS",
    "Every solution re-derived; E1 bound (100 M11/(S0+99 M11)) and E3 0.15 bound recomputed (m3c_r8_numbers.out, jacobi_alt.out); R3 (B^T B = I, W = BQ, complement eigenvalues 0) checked.")
row("PROB-L09", "2.4-math", "L09.html problems M1-M3, P1-P3, E1-E3, R1-R3 (lines 379-479)", "PASS",
    "Every solution re-derived; E2 sqrt(0.96) = 0.979796; E3 gives 0.5; R1 split identity checked; R2 gives identity matrix; R3 norm identity checked; P1 bound via t = +/-1.")
row("GRADE-L07", "2.3-grades", "L07.html block titles (lines 64, 84, 108) and key-results table (346-350)", "PASS",
    "Theorems 1.2, 1.3 and 2.2 are T with complete proofs; Remark 1.4 is T in the table; the lab row is C and labelled 'finite numerical check on a SIMULATED design'. No claim outside the proofs is graded.")
row("GRADE-L08", "2.3-grades", "L08.html block titles (61, 71, 86, 100, 116, 121) and key-results table (428-434)", "PASS",
    "Proposition 1.1, Proposition 1.2, Theorem 1.4, Theorem 2.1, Corollary 2.2, Proposition 2.3 are T with proofs; the two lab rows are C and state the panel is SIMULATED and that no yield-curve claim is made.")
row("GRADE-L09", "2.3-grades", "L09.html block titles (74, 122, 151, 163) and key-results table (491-500)", "PASS",
    "Lemma 1.3, Propositions 3.2-3.5 are T with proofs; Example 2.3 and Example 3.6 are T as exact arithmetic on the page; the two seeded-run rows are C with 'one run' or 'finite seeded check' basis.")
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (no data-cite, data-locator; empty data-references lists at 431, 519, 591)", "PASS",
    f"{S}/static_checks.py -> {O}/static_checks.out: data-cite/data-locator count 0 on all three pages; external URLs 0; '<ol data-references></ol>' present on all three. The pages' references sections state that no result is attributed to an outside source.")
row("XREF-EARLIER", "2.9-xref", "earlier-lesson cross-references: L01 Thm 3.7 (161-162); L04 F1-F4 (56-62), Def 1.1 (68-69), Def 1.2 (73-74), Thm 2.3 (130-131); L05 Def 1.4 (71-72), Thm 2.1 (108-109); L06 inner product and norm (56), Def 1.1 (59-60), Fact 1.2 (64-65), Prop 2.4 (126-127), Remark 2.5 (228-229); L03 Def 1.1 (61); L07 Thm 1.2 (cited from L08 line 137)",
    "PASS",
    "Each cited locator was read in the earlier lesson page. L06 Prop 2.4 states the Frobenius norm and the trace; L06 Remark 2.5 gives the singular-vector sign freedom that L08 line 293 cites; L05 Def 1.4 defines positive definite (used in L09 Prop 3.2(b)); L04 F4 defines the null space (used in L09 P2); L01 Thm 3.7 gives the bound on independent lists (R1). All read in the checkout.")
row("DAG-PSD-REDEF", "2.9-dag", "course/modules/M/M3/L09.html line 56 versus L05.html lines 71-72 (Definition 1.4)", "PASS",
    "L09 line 56 links the PSD concept to L05 (href L05.html#def-positive-semidefinite-matrix) and does not define it again; L09 has no <dfn> for PSD (dfn ids list in static_checks.out).")
row("NOTATION-R", "2.9-notation", "L07, L08, L09 math using \\R", "PASS",
    f"{O}/static_checks.out: \\R is the registered macro (tex \\mathbb{{R}}); used only as the real numbers.")
row("NOTATION-OPNAME", "2.9-notation", "L08.html \\operatorname{span} (line 402); L09 \\mathrm{sign} (Prop 3.5 proof); \\tr and \\diag on the pages", "PASS",
    f"Registered macros \\tr (matrix trace) and \\diag (diagonal matrix) are used with those meanings (notation.json macros); \\operatorname and \\mathrm are standard KaTeX.")
row("NOTATION-T", "2.9-notation", "L08.html Section 1 (line 56: T x n matrix, T >= 2) and Lab 1 (T = 750)", "PASS",
    "Registered symbol T means 'number of return observations (periods) in a sample' (notation.json symbols). L08 uses T for the number of observations (rows of the data), the same sample-size meaning. No conflicting use.")
row("NOTATION-AST", "2.9-notation", "L09.html line 93 (C^{\\ast}: nearest correlation matrix)", "PASS",
    "Registered R^{\\ast} is the SDF return in AP1; C^{\\ast} is a different symbol, local to the lesson.")
row("NOTATION-Q", "2.9-notation", "L07 and L09 orthogonal Q; \\mathbb{Q} registered for a probability measure", "PASS",
    "Plain Q is local (notation.json 'about': conventionally local letters are defined in the lesson); \\mathbb{Q} does not appear on the three pages.")
row("NOTATION-OTHER", "2.9-notation", "all control sequences in math on the three pages", "PASS",
    f"{O}/static_checks.out: registered macros used are \\R, \\diag, \\tr only; every other sequence is standard KaTeX or a lesson-local symbol (top, ast, iota, tau, bar, tilde, hat, Lambda, Gamma, lambda, varepsilon, kappa, delta, alpha, gamma, beta). No non-standard macro is introduced.")
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Definition 3.1 (141), quiz item L08q9 (507-511)", "PASS",
    "Quiz item states the level-like rule with the unique-largest |cos| condition; the explanation matches Definition 3.1, including the tie case.")
row("DEF-L08-MATCH", "2.2-lab-prose", "L08.html Definition 3.1 (141), canon-break (292), quiz explanation (511), lab main() match loop", "PASS",
    "Lab computes the match as argmax |cos| per planted shape and prints 'the three planted shapes match three different components'; the text and the lab agree.")
row("DAG-LINKS", "2.9-dag", "L07.html, L08.html, L09.html meta rows (lines 38-39)", "PASS",
    "check_dag M3 PASS (GATE-02). L07 uses L01 vector space; L08 uses L03, L04, L05; L09 uses L03, L04, L05; each Introduces link points to the lesson's own <dfn> (ids def-orthogonal-projection, def-least-squares-projection, def-principal-component-analysis, def-level-slope-curvature, def-nearest-correlation-matrix, def-eigenvalue-clipping).")
row("DAG-M4", "2.9-dag", "L07-L09 covariance, variance, correlation wording (static_checks.out, DAG section)", "PASS",
    "No M4 concept is linked. L09's 'correlation matrix' is the M3 definition 1.1, a plain descriptor (architect ruling B1/Q2, no link, no M4 prerequisite). The one covariance-family hit is the link text 'M3 project: Covariance-matrix doctor' (L09 line 597), a project title, not a concept use.")
row("DAG-PROSE-UNLINKED", "2.9-dag", "L09.html line 60 and other unlinked uses of positive semidefinite", "PASS",
    "Each PSD mention after the lesson's first link (L09 line 56) refers to the same concept defined in L05; no concept is used before its lesson.")
row("CONCEPT-L08-LSC", "2.9-dag/2.3-grades", "course/modules/M/M3/L08.html line 39 (Introduces row) and line 141 (dfn id=def-level-slope-curvature); curriculum/curriculum.json concepts['level-slope-curvature'].name; curriculum/01-foundations.yaml line 175",
    "FAIL",
    f"{S}/static_checks.py -> {O}/static_checks.out: registered name 'Level, slope and curvature factors of the yield curve' (module M3). L08 Introduces row: 'level-like, slope-like and curvature-like principal directions'. Definition 3.1 defines shape labels on principal directions and says 'they define no yield-curve factor' (line 141). So the id the curriculum assigns to M3 is defined by L08 under a different meaning, and the registered concept is not defined as named. The round-7 defect is therefore still open; the page edit changed the label, not the registered concept.",
    "Architect decision, because builders may not edit curriculum files. Either (a) change the registered concept name in curriculum/01-foundations.yaml M3 introduces (line 175) to 'Level-like, slope-like and curvature-like principal directions' and regenerate with tools/render_curriculum.py, keeping L08 as written; or (b) keep the registered name and have L08 define level, slope and curvature as an interpretation of the loadings, graded C, stated as a property of the SIMULATED Lab 1 output (plan section 2.3 and Q9), removing 'they define no yield-curve factor'. Until one is chosen, this row stays FAIL.")
row("DEFINE-BEFORE-USE", "2.9-prose", "first uses of tenor, trace, cosine, PSD, eigenvalue clipping, orthogonal, Frobenius, correlation matrix, nearest correlation matrix, column space, null space, positive definite, congruence", "PASS",
    "tenor and yield change defined in L08 Section 1 (line 56) before Section 3; trace and Frobenius norm from L06 Prop 2.4; orthogonal matrix from L06 Def 1.1; PSD from L05 Def 1.4; positive definite from L05 Def 1.4; null space from L04 F4; column space defined in L07 line 56 before use; congruence defined inline in L09 misconception 2. Forward pointers in why-it-matters ('Definition 1.3 of this lesson', 'Definitions 1.2 and 2.1') name later definitions and do not use the term undefined.")
row("PLAIN-REDEF", "2.9-dag", "course/modules/M/M3/L09.html Definition 1.2a removed (round-7 defect); line 68 cross-refers to L06 Definition 1.1", "PASS",
    "L09 has no <dfn> or definition block for orthogonal matrix (static dfn list). The round-7 Definition 1.2a is gone and its restatement is a cross-reference ('Orthogonal matrices are as in Lesson 6, Definition 1.1'). The transpose and trace sentences at line 56 are now cross-references too.")
row("PROSE-PROCESS", "2.9-prose", "L07, L08, L09 learner text (banned and process-word sweep)", "PASS",
    f"{O}/static_checks.out: no hits for TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, it can be shown, verifier, builder, ledger, previous version, reviewer, placeholder. 'unrounded' and 'fixed seed' are scientific wording, not process words.")
row("PROSE-ELLIPSIS", "2.9-prose", "quiz stems ending in an ellipsis: L07 (two), L08 (three), L09 (two)", "PASS",
    f"{O}/static_checks.out lists seven stems ending '...' (for example 'the projection matrix P is' followed by its options). Each is completed by the option list, so the ellipsis stands for the answer, not omitted content.")
row("PROSE-SCOPE", "2.9-prose", "scope words on the three pages (every, always, only, any, all, exactly, typically, not always)", "PASS",
    "Each occurrence checked: 'every' in proofs (Theorem 1.2(c), Prop 3.2(a), R1, P2, R3) or in the lab's tested scope ('doubling every entry' over one panel, labelled finite); 'always' appears only in quiz distractors and misconceptions (e.g. 'always invertible', 'always the level factor'); 'not always the nearest one' (L09 meta description) is supported by the 23 counted cases; 'only' in L07 line 204 is the 'for this duplicated design only' scope, correct; L09 canon-break 2 states the 40-matrix scope.")
row("PROSE-REMARK-2.4", "2.9-prose", "L08.html Remark 2.4 (131-133) and its last sentences", "PASS",
    "The remark proves M is not a multiple of M after a single-column rescaling (M_jj > 0 argument) and states that 'the lab does not establish a general rule for the direction of such a change'. The claim is scoped to one case.")
row("STRUCT-WHY", "2.9-structure", "L07 line 52, L08 line 52, L09 line 52 why-it-matters", "PASS",
    "Word counts (static_checks.out): L07 111, L08 114, L09 116, each at most 120 (BUILDER_RULES 4.2.1).")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts (BUILDER_RULES 4.2)", "PASS",
    "Order: why it matters, numbered core sections, inline lab, canon-breaks, misconceptions, problem set, key results, retrieval quiz, references. Misconceptions: 3 each. Problem tiers: 3 each in Mechanics, Proof, Empirical, Research. Quiz items: 9, 9, 11 (8-15). No debate key on M3, so no debate brief. Key-results table present on all three.")
row("HOURS", "2.9-hours", "L07.html data-hours 11, L08.html 12, L09.html 12; index.html data-hours-lessons 105; lesson hours L01-L09 sum", "PASS",
    f"{O}/static_checks.out: lesson hours 12+11+12+12+12+11+11+12+12 = 105 = hub data-hours-lessons; project 45; total 150.")
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) 'The program does not yet embed a multi-tenor series ...' and Lab 1 heading (145)", "PASS",
    "course/assets/data/market/MANIFEST.json: fx_daily (6 columns), fx_monthly (10), ust_daily (['tbill_3m', 'cmt_10y'], two series). tools/data_sources.yaml ust_daily transform series tbill_3m and cmt_10y. No embedded multi-tenor yield series, so the claim holds.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291) and Section 1 note (line 52)", "PASS",
    "Canon-break states the curriculum Treasury-curve lab is not run and that the three-component claim is not made for any real curve; line 52 says 'It makes no claim about any real curve'. The gap is stated, not hidden.")
row("SIMULATED-LABELS", "2.8-data", "L07 lab (124-128), L08 lines 145-151 and twin docstring, L09 lines 190, 199 and twin docstring", "PASS",
    "Each lab title or hypothesis carries SIMULATED; the twin docstrings say SIMULATED and name the seeds; key-results rows for the labs say 'SIMULATED'.")
row("DELTA-READ", "2.0-delta", "delta 9373ef39..2d755599 for slice c: course/modules/M/M3/L07.html (1 line), L08.html (lines 36-39, 56-58, 137, 141), L09.html (56-68), cards.json (c142, c147, c163, c207, c208)",
    "PASS",
    f"{S}/static_checks.py delta section -> {O}/static_checks.out: L07 2 +-, L08 8, L09 11, cards.json 14 lines; lab twins changed since the round-7 pin: none. project.html changed but is slice d's. Every L07-L09 row above was re-verified from the current files; no round-7 PASS row was carried.")
row("HYP-L08-DEF31", "2.4-math/2.9-structure", "L08.html Section 3 (line 137) and Definition 3.1 (line 141)", "PASS",
    "Fixed since round 7. Section 3 now assumes at least three distinct tenor values (forces n >= 3) and gives the two-value identity tau^2 = -ab iota + (a+b) tau; Definition 3.1 assumes the same before saying 'orthonormal by construction'. Checked: curvature residual 0 for one or two distinct values, nonzero for three (0.8165 for (1,2,3)), in {O}/jacobi_alt.out and {O}/m3c_r8_numbers.out.")

# Cards (new row).
row("CARDS-L07-L09", "2.7-cards", "course/modules/M/M3/cards.json entries with lesson L07, L08, L09 (71 cards)", "PASS",
    f"{S}/static_checks.py -> {O}/static_checks.out: full 202-card scan, no duplicate ids and no duplicate fronts. Sample 1 in 10 of the 71 (M3-c115, c125, c135, c145, c156, c166, c186, c207) read against the lesson text and correct. The round-7 edits are consistent: c142 and c207 state the three-distinct-values hypothesis; c147 cites Lesson 6 Prop 2.4; c163 counts the 23 non-PSD matrices; c208 (the card for the removed L09 Definition 1.2a) was removed.")

rows_sorted = rows
counts = Counter(r["status"] for r in rows_sorted)
verdict = "PASS" if counts["PASS"] == len(rows_sorted) else "FAIL"
fragment = {
    "unit": "M3",
    "slice": "c",
    "round": 8,
    "verifier": "independent Haiku verifier (round 8), checkout verifyD8-M3-c",
    "pin": "2d755599d8d74df292e3e43025f0458c4053802e",
    "base": "9373ef398589097500ea849e30ff9da423b98943",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD8-M3-c",
    "scratch": "twin runs in TemporaryDirectory under /tmp (removed after each run); no other scratch directory",
    "verified_at": "2026-11-04",
    "verdict": verdict,
    "rows": rows_sorted,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "FULL verification, from scratch, of L07, L08, L09 and their three lab twins, plus the L07-L09 cards. "
        "Delta 9373ef39..2d755599 read in full for slice c (L07, L08, L09, cards.json); lab twins unchanged. "
        "No round-7 PASS row was carried. Mutants: none, because the slice is lessons and lab twins (VERIFIER rulings: "
        "lab twins are demonstrations; mutation testing applies to project graders). Registry: no citation in the slice "
        "(CITE-L07-L09); no freshness flags because M3 has no debate brief and no cited source. "
        f"Scripts: {S}/static_checks.py, twin_vs_page.py, m3c_r8_numbers.py, jacobi_alt.py, build_fragment_r8.py; outputs in {O}/. "
        "Gate commands run on the pin: tools/check_pages.py (unit and each page), check_dag.py, check_projects.py, run_labs.py, "
        "ruff check and format on tests/labs/M3, mypy --no-incremental, page_smoke.py per page, verify_refs.py --offline, "
        "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page'. "
        "Not checked: a live verify_refs run (slice c cites no key); run_graders (no grader in slice c); a 360 px light and "
        "dark screenshot (page_smoke only); the rest of the cards (sampled); the full pytest suite; project.html, index.html "
        "and the grader (other slices)."
    ),
    "summary": (
        f"M3 slice c round 8 at pin 2d755599: {len(rows_sorted)} rows (pass={counts['PASS']} fail={counts['FAIL']} "
        f"unverifiable={counts['UNVERIFIABLE']}). Non-PASS: CONCEPT-L08-LSC (L08 defines under the registered id "
        "'level-slope-curvature' labels that disclaim the registered yield-curve concept; architect or curriculum change "
        "needed) and LABSTMT-L09 (Lab 1 hypothesis gives the first count over 40 matrices, the code and output over the 23 "
        "non-PSD matrices). All gates pass, all three twins match their pages and run clean under -I -W error, every number "
        "re-derived with a second algorithm (SVD/QR and a pure-Python Jacobi eigensolver), and the round-7 defects "
        "HYP-L08-DEF31 and PLAIN-REDEF are fixed."
    ),
}
out = ROOT / "ledgers/M3/M3-c.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, dict(counts), "verdict", verdict)
