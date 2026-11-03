"""Write ledgers/M3/M3-c.json (round 2, slice c, unit M3). Run from the checkout root with the repo venv."""

import json
import pathlib

S = "ledgers/M3/scripts/M3-c-r2"
G = f"{S}/"
ROWS = [
    ("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3", "PASS",
     f"'check_pages M3: PASS', exit 0 ({G}check_pages.log)"),
    ("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS",
     f"'check_dag M3: PASS', exit 0 ({G}check_dag.log)"),
    ("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
     f"'check_projects M3: PASS', exit 0 ({G}check_projects.log). Project content is slice d, not checked here"),
    ("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 (all 12 labs) and --unit M3 --page L07 / L08 / L09", "PASS",
     f"'run_labs M3: PASS (12/12)' ({G}run_labs_M3_all.log); 'PASS (1/1)' for each page ({G}run_labs_L07.log, "
     f"run_labs_L08.log, run_labs_L09.log); exit 0 each"),
    ("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py", "PASS",
     f"each run alone as python -I -W error from an empty directory (/private/tmp/verifyD2-twin-07, -08, -09): exit 0, "
     f"stderr 0 bytes; stdout kept ({G}twin_L07.stdout, twin_L08.stdout, twin_L09.stdout; summary {G}twin_alone.log)"),
    ("LAB-L07-EMBED", "2.5-labs", "course/modules/M/M3/L07.html section#lab-M3-L07-1", "PASS",
     f"{S}/check_embed_r2.py: page <code> equals twin text (True), expected block equals twin stdout (True), no @@ "
     f"markers ({G}check_embed_r2.log)"),
    ("LAB-L08-EMBED", "2.5-labs", "course/modules/M/M3/L08.html section#lab-M3-L08-1", "PASS",
     f"same comparison as LAB-L07-EMBED: code True, expected True, no markers ({G}check_embed_r2.log)"),
    ("LAB-L09-EMBED", "2.5-labs", "course/modules/M/M3/L09.html section#lab-M3-L09-1", "PASS",
     f"same comparison as LAB-L07-EMBED: code True, expected True, no markers ({G}check_embed_r2.log)"),
    ("GATE-06", "2.5-labs", "ruff check tests/labs/M3; ruff format --check tests/labs/M3", "PASS",
     f"'All checks passed!' and '12 files already formatted' ({G}ruff_check_twins.log)"),
    ("GATE-07", "2.5-labs", "mypy --no-incremental (repository configuration)", "PASS",
     f"'Success: no issues found in 331 source files', exit 0 ({G}mypy.log)"),
    ("GATE-08", "2.9-smoke", "tools/page_smoke.py --unit M3 --pages L07 L08 L09, and each page alone", "PASS",
     f"'page_smoke M3: PASS' for the three pages together ({G}page_smoke_L07-L09.log) and for each page alone "
     f"({G}page_smoke_L07.log, page_smoke_L08.log, page_smoke_L09.log). The three pages contain no svg and no chart "
     f"element (grep count 0), so the figure sweep is vacuous here"),
    ("GATE-09", "2.1-citations", "tools/verify_refs.py --offline (whole registry)", "PASS",
     f"'offline integrity: 560 entries, 0 problems', exit 0 ({G}verify_refs_offline.log). The live "
     f"'verify_refs.py --unit M3' needs the network and was not run; L07-L09 cite no registry key (grep for "
     f"data-cite, data-locator and the two Lesson 4 registry keys: 0 matches)"),
    ("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", "PASS",
     f"exit 0; no failure or error lines ({G}pytest_relevant.log, {G}pytest_relevant_summary.log)"),
    ("NUM-L07", "2.2-numbers",
     "course/modules/M/M3/L07.html: M2 coefficients 7/6, 1/2, fitted 7/6, 5/3, 13/6, residuals -1/6, 1/3, -1/6; "
     "M3 25 = 9 + 16; E2 vector (18.38, 3.10, -17.60); Misc 1 residual 0.8951; E3 intercept 1.3325; Lab 1 printed lines",
     "PASS",
     f"{G}check_numbers_r2.py ({G}check_numbers_r2.log): exact Fraction solve gives beta0 = 7/6, beta1 = 1/2, fitted and "
     f"residuals as printed, sums zero and orthogonal to x. Lab 1 recomputed by QR: beta = (1.332519, 0.848811, "
     f"-0.411964), residual norm 0.895128, A^T y = (18.37970, 3.09586, -17.60350); all printed values match"),
    ("NUM-L08", "2.2-numbers",
     "course/modules/M/M3/L08.html: shares 75.9 / 18.1 / 5.2 %, cosines 0.9994 / 0.9985 / 0.9990, first share 0.7587 "
     "-> 0.9791, E1 bound 0.9483 with M11 13.6818 and trace 88.2028, E3 printed sum 99.2 and 0.15 bound, M1 trace 17, "
     "det 3, eigenvalues (17 +- sqrt277)/2",
     "PASS",
     f"{G}check_numbers_r2.log: SVD of the centred panel gives shares 75.8728, 18.0888, 5.1619 %, unrounded top-3 sum "
     f"99.1236 (|99.2 - 99.1236| = 0.0764 <= 0.15); cosines 0.9994, 0.9985, 0.9990 on PC1, PC2, PC3; first share after "
     f"rescaling 0.979145; M11 13.681775, trace 88.202753; E1 bound 0.948346 > old share 0.758728; M1 trace 17, det 3, "
     f"eigenvalues 0.178342 and 16.821658 = (17 -+ sqrt277)/2"),
    ("NUM-L09", "2.2-numbers",
     "course/modules/M/M3/L09.html: x^T C0 x = -2.4; ||C0 - B||_F^2 = 0.64; R entries; E2 sqrt(0.96) = 0.9798; "
     "Example 3.6 squared distances 0.04 and 0.08, ||A||_F^2 = 4.88; M3 eigenvalues; Lab 1 23 of 40 non-PSD, 23 of 23 "
     "feasible and closer, first matrix 0.175527 / 0.163280",
     "PASS",
     f"{G}check_numbers_r2.log: closed form B = (19/30)[[2,1,1],[1,2,-1],[1,-1,2]] from C0 + 0.8 v v^T with "
     f"v = (1,-1,-1)/sqrt3 (deviation 2e-16), R = [[1,.5,.5],[.5,1,-.5],[.5,-.5,1]] (deviation 1e-16); ||C0-R||_F = "
     f"0.979796; the seeded repetition gives 23 non-PSD (index 0 first), 23/23 feasible, 23/23 closer, first matrix "
     f"0.175527 and 0.163280"),
    ("MATH-L07", "2.4-mathematics",
     "course/modules/M/M3/L07.html Theorem 1.2 (a)-(c), Theorem 1.3, Remark 1.4, Definition 2.1, Theorem 2.2 (a)-(c), "
     "R1-R3, P1-P3", "PASS",
     f"Every proof read in full ({S}/L07.txt, text of the page) and re-derived: G = A^T A invertible via v^T G v = "
     f"||Av||^2 and the spectral theorem (Lesson 4, Theorem 2.3); the expansion in Theorem 1.3 and Remark 1.4; normal "
     f"equations; uniqueness of the projection; R1 existence via a maximal independent list and L01 Theorem 3.7 (line "
     f"68 of L01 text); R3 Q^2 = Q. No gap found. The page differs from the previous pin only by \\mathbb{{R}} -> \\R "
     f"(diff against the sed-substituted old file: empty)"),
    ("MATH-L08", "2.4-mathematics",
     "course/modules/M/M3/L08.html Proposition 1.1, Proposition 1.2, Theorem 1.4, Theorem 2.1 (a)-(b), Corollary 2.2, "
     "Proposition 2.3, Remark 2.4, Definition 3.1, R1-R3, P1-P3", "PASS",
     f"Every proof re-derived ({S}/L08.txt): Theorem 2.1 by the coefficient identity u^T M u = sum lambda_i alpha_i^2; "
     f"Remark 2.4 argument (M_jj > 0 from the perturbation e_j + t e_l; kappa = c forced; M_jj(c^2 - c) = 0 false); "
     f"R3 block factorisation M = B G B^T and W = BQ; E1 bound logic. Checks in {G}check_numbers_r2.log. "
     f"Only change since the previous pin: \\mathbb{{R}} -> \\R (diff check empty)"),
    ("MATH-L09", "2.4-mathematics",
     "course/modules/M/M3/L09.html Lemma 1.3, Proposition 3.2 (a)-(b), Proposition 3.3 (a)-(b), Proposition 3.4, "
     "Proposition 3.5, Example 2.3, Example 3.6, Section 4 Method 1 and Method 2 statements, R1-R3, P1-P3", "PASS",
     f"Every proof re-derived ({S}/L09.txt): Lemma 1.3 trace identity; Prop 3.2 quadratic form in y = Q^T x; Prop 3.3(a) "
     f"diagonal difference; Prop 3.5 delta-bound (b_jj/(1+b_jj) < 1); Prop 3.4 congruence; Example 3.6 values by hand; "
     f"R1 split; P1 bound |C_ij| <= 1. Byte-identical since the previous pin (git diff --stat empty for L09.html)"),
    ("PROB-L07", "2.2-problems",
     "course/modules/M/M3/L07.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (12 solutions)", "PASS",
     f"each worked solution re-derived; M2 coefficients and residuals exact; E2 vector recomputed; quiz answers "
     f"checked (9 items, {S}/L07.txt); numbers in {G}check_numbers_r2.log"),
    ("PROB-L08", "2.2-problems",
     "course/modules/M/M3/L08.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (12 solutions)", "PASS",
     f"M1 matrix, trace 17, determinant 3, eigenvalues recomputed by SVD and exact arithmetic; M3 tripling 2/3, 1/3; "
     f"P3 Theorem 2.1(a) with e_1; E3 sum bound 0.15 (0.0764 observed); R1 maximiser set; R3 steps; quiz 9 items "
     f"({S}/L08.txt; {G}check_numbers_r2.log)"),
    ("PROB-L09", "2.2-problems",
     "course/modules/M/M3/L09.html problem set M1-M3, P1-P3, E1-E3, R1-R3 (12 solutions)", "PASS",
     f"M2 4.88 and M3 eigenvalues (13 +- sqrt41)/2 recomputed; E2 0.9798 recomputed; E1 witness term by term (3 - 5.4 "
     f"= -2.4); E3 0.5 and eigenvalues (2, 0.5, 0); R2 diag(1,1); quiz 11 items ({S}/L09.txt)"),
    ("LABSTMT-L07", "2.5-labs",
     "course/modules/M/M3/L07.html Lab 1 hypothesis, interpretation, key-results row and twin docstring", "PASS",
     f"hypothesis lists six checks at 1e-9 and the duplicated-column rank; the twin's printed lines 39-62 (stdout lines 1-10) "
     f"match each sentence; SIMULATED label present; generator parameters (seed 7 at line 25, intercept 1.5, slopes 0.8 and "
     f"-0.4, noise sd 0.3 at lines 27-30) match the twin; 'the lab does not check its "
     f"rank' matches code (only the duplicated design's rank is printed)"),
    ("LABSTMT-L08", "2.5-labs",
     "course/modules/M/M3/L08.html Lab 1 hypothesis, interpretation, key-results rows and twin docstring", "PASS",
     f"seeds 8 (twin line 67); T = 750 (line 22); tenors 0.25 to 10 (line 21); scales 8, 4, 2 bp and noise 0.5 bp (lines "
     f"46-52); each printed claim has a print line (lines 74-122); 'the three matches are distinct' is line 100; the E1 bound "
     f"inputs are printed at lines 114-122 and reproduce 0.9483; no Treasury data read (docstring line 4)"),
    ("LABSTMT-L09", "2.5-labs",
     "course/modules/M/M3/L09.html Lab 1 hypothesis, interpretation and key-results rows", "PASS",
     f"seeds 20261028 (line 35), 40 matrices (line 33), 5x5 (line 34), tolerances 1e-12 / 1e-8 / 1e-9 (lines 29-31), 500 steps (line 32); 'to that "
     f"tolerance' qualifier present; the alternating projections run only on the 23 non-PSD matrices, and the page "
     f"reports every count as 'of 23' (twin_L09.stdout lines 10-13), so no PSD-matrix claim is made. The twin docstring "
     f"sentence is graded separately in LABDOC-L09"),
    ("LABDOC-L09", "2.5-labs / 2.9-structure",
     "tests/labs/M3/lab-M3-L09-1.py line 17 (docstring; shown in the page's section#lab-M3-L09-1 code block)", "FAIL",
     f"The docstring says the lab 'shows only that R is not nearest for each instance where W is strictly closer, and "
     f"that W is feasible for the instances counted'. The code's closer counter (lines 126-127) increments when "
     f"d_alt < d_rescale without requiring is_correlation(alt); feasibility is counted separately (lines 122-123). A "
     f"W that fails the correlation check but is closer would be counted as closer, and nearest is taken over "
     f"correlation matrices, so the sentence overreaches. The printed output (23 of 23 for both counts, "
     f"twin_L09.stdout lines 11-12) makes the page's statements true for this run; only the docstring's general implication is unsupported "
     f"by the code",
     "Reword the docstring to 'R is not nearest for each instance where W passes the correlation check and is strictly "
     "closer', or make the closer count require is_correlation(alt). Then run `.venv/bin/python tools/embed_labs.py "
     "course/modules/M/M3/L09.html --refresh lab-M3-L09-1` (the expected output does not change) and rerun the "
     "embed comparison and run_labs for L09"),
    ("GRADE-L07", "2.3-grades",
     "course/modules/M/M3/L07.html grade spans", "PASS",
     "Theorem 1.2, Theorem 1.3 and Theorem 2.2 graded T and each proved on the page; the lab-only key-result row graded "
     "C with 'Lab 1 output' (single sample, BLUEPRINT 3 'One study finds' class). Remark 1.4 key-results row graded T "
     "(one-line expansion of Theorem 1.3). No A, B, D or X claim"),
    ("GRADE-L08", "2.3-grades",
     "course/modules/M/M3/L08.html grade spans", "PASS",
     "Propositions 1.1, 1.2, 2.3, Theorems 1.4, 2.1, Corollary 2.2 graded T with proofs; the simulation key-results rows "
     "graded C and name Lab 1; the level, slope and curvature labels are definitions (Definition 3.1, no grade needed)"),
    ("GRADE-L09", "2.3-grades",
     "course/modules/M/M3/L09.html grade spans", "PASS",
     "Lemma 1.3, Propositions 3.2 to 3.5, Example 2.3 and Example 3.6 graded T; the seeded 23-of-40 and distance rows "
     "graded C with 'Lab 1 output' (one seeded run, floating point)"),
    ("CITE-L07-L09", "2.1-citations",
     "course/modules/M/M3/L07.html, L08.html, L09.html (data-cite, data-locator)", "PASS",
     f"no data-cite or data-locator attribute (grep count 0 on each page); pages state 'No result is attributed to an "
     f"outside source'. Matches the sibling M-series pages (M1 L03 and M2 L05 carry no data-cite). Theorems are proved "
     f"on the page, which BLUEPRINT 3 allows for T"),
    ("XREF-EARLIER", "2.4-mathematics",
     "cross-lesson references in L07-L09: F1-F4 (L04 lines 25-28); L04 Theorem 2.3 (line 55); L05 Definition 1.4 "
     "(line 30) and Theorem 2.1 (line 45); L06 Fact 1.2 (lines 26-28) and Remark 2.5 (lines 138-139); L01 Theorem 3.7 "
     "(line 68) and subspace test Proposition 1.4 (line 35); L06 dot product and norm (line 23); L03 Definition 1.1 "
     "(line 25-26); L07 Theorem 1.2 used in L08", "PASS",
     f"each target read in the earlier lesson's text ({S}/L01.txt ... L06.txt in the scratch copy "
     f"/private/tmp/verifyD2-M3-c-scratch, textify.py in {S}). L06 differs from the previous pin only by \\mathbb{{R}} -> "
     f"\\R (diff check empty), and L01, L03, L04, L05 are byte-identical. Fact 1.2 gives Q Q^T = I from Q^T Q = I, as "
     f"L07 line 32 uses it"),
    ("NOTATION-R", "2.4-notation",
     "course/modules/M/M3/L07.html and L08.html (formerly 13 and 6 occurrences of \\mathbb{R})", "PASS",
     f"grep 'mathbb' in L07, L08, L09: 0 matches ({S}/check_notation_r2.log); the registry macro \\R is notation/notation.json "
     f"line 25 (tex \\mathbb{{R}}); L07 and L08 now use \\R. The round-1 FAIL is fixed at c737272"),
    ("NOTATION-OPNAME", "2.4-notation",
     "course/modules/M/M3/L07.html lines 75, 227; L08.html lines 72, 82, 325, 332, 429, 454; L09.html line 552 "
     "(\\operatorname{diag} and \\operatorname{tr} written raw, not via the registered macros)", "FAIL",
     f"notation/notation.json registers \\tr (tex \\operatorname{{tr}}, matrix trace) and \\diag (tex "
     f"\\operatorname{{diag}}, diagonal matrix). L09 uses the registered \\tr (11 uses) and \\diag (13 uses), but L07, L08 "
     f"and one place in L09 write the raw expansion (counts from grep -o on the three pages, saved in {S}/operatorname_grep.log). The meaning is unchanged, so this is a conformance defect, not a collision. "
     f"Architect ruling 1 replaced \\mathbb{{R}} with the registered \\R for the same reason",
     "Replace each raw \\operatorname{tr} with \\tr and each raw \\operatorname{diag} with \\diag at the nine listed "
     "locations (L08 span stays: no registered macro exists). Then rerun check_pages, check_dag and page_smoke for L07-L09"),
    ("NOTATION-T", "2.4-notation",
     "course/modules/M/M3/L08.html section 1 (T x n matrix, T - 1, T = 750)", "PASS",
     "notation.json symbol T: 'number of return observations (periods) in a sample' (module S1). L08 uses T for the number "
     "of yield-change observations, a count of observations in a sample, the same meaning with the observation type "
     "named differently (judgement, recorded). The verifier rules name this symbol's meaning as the number of observations"),
    ("NOTATION-Q", "2.4-notation",
     "course/modules/M/M3/L07.html, L09.html (orthogonal Q; \\mathbb{Q} in the registry)", "PASS",
     "registry \\mathbb{Q} is the AP1 probability measure; M3 writes plain Q for an orthogonal matrix. Different glyph, no "
     "collision (judgement, recorded). \\tr and \\diag used with their registered meanings"),
    ("NOTATION-OTHER", "2.4-notation",
     "all LaTeX in L07-L09", "PASS",
     f"{S}/check_notation_r2.log: the control sequences used are standard TeX or the registered macros \\R, \\tr, \\diag; "
     f"no registered symbol (\\E, \\Var, \\Cov, \\Corr, \\Phi, gamma_3, gamma_4, R^\\ast, R^{{e\\ast}}, R_f, \\mathbb{{Q}}) is "
     f"written with another meaning; alpha, beta, gamma, Lambda, Gamma, tau, kappa, delta, varepsilon are local"),
    ("DAG-LINKS", "2.9-structure",
     "dfn and concept links in L07-L09", "PASS",
     f"dfn ids def-orthogonal-projection and def-least-squares-projection (L07); def-principal-component-analysis and "
     f"def-level-slope-curvature (L08); def-nearest-correlation-matrix and def-eigenvalue-clipping (L09) match the "
     f"Introduces lines; concept links point to earlier lessons only (check_dag PASS, {G}check_dag.log)"),
    ("DAG-M4", "2.9-structure",
     "course/modules/M/M3/L08.html, L09.html, L07.html (covariance and correlation wording)", "PASS",
     "no concept link to an M4 concept and no M4 name linked (architect ruling 3). 'covariance', 'variance', 'Gaussian' "
     "do not occur in L07-L09 (grep); 'correlation' appears as plain prose in L09 (Definition 1.1 is a descriptor), "
     "allowed by ruling 3"),
    ("DEFINE-BEFORE-USE", "2.9-structure",
     "L07-L09 first uses of trace, subspace, kernel, positive definite, eigenvalue clipping, orthogonal, fitted vector, "
     "residual, tenor, cosine, Frobenius norm", "PASS",
     "trace defined in L08 line 25 before Proposition 1.2 and in L09 line 23; tenor defined L08 line 23; cosine defined "
     "L08 section 3 before Definition 3.1 and the lab; fitted vector and residual defined L07 section 2; Frobenius norm "
     "L09 Definition 1.2; eigenvalue clipping named in the why-it-matters paragraph with a pointer to Section 3, defined "
     "in Definition 3.1; positive definite from L05 Definition 1.4"),
    ("PROSE-PROCESS", "2.9-structure",
     "learner text of L07-L09", "PASS",
     f"grep for builder, verifier, ledger, round, pin, agent, TODO, TBD, lorem, 'for brevity', 'beyond the scope', "
     f"'left as an exercise', 'it is important to note', 'studies show', 'experts agree', 'it is well known', obviously, "
     f"clearly, 'it can be shown', historically, roughly, typically, 'in practice': none in the learner text "
     f"(scratch texts L07.txt, L08.txt, L09.txt, copies in {S})"),
    ("PROSE-ELLIPSIS", "2.9-structure",
     "course/modules/M/M3/L07.html quiz stems (2), L08.html (3), L09.html (2) ending in an ellipsis", "PASS",
     "each ellipsis ends a quiz stem whose options follow ('the matrix ... is' with options); it stands for the answer, not "
     "for omitted content, so BUILDER 1.3 is not triggered (judgement, recorded)"),
    ("PROSE-SCOPE", "2.2-scope",
     "scope words in L07-L09 (every, all, always, any, same, only, exactly, stable)", "PASS",
     f"each use checked against a proof or a stated finite check: 'every full-column-rank design' (Theorem 1.2); 'every "
     f"nonzero c and every data matrix' (Proposition 2.3); seeded claims scoped to one design, one panel, or 40 and 23 "
     f"matrices; 'always' and 'stable' appear only inside quoted misconceptions"),
    ("STRUCT-WHY", "2.9-structure",
     "why-it-matters paragraph (line 21) of L07, L08, L09", "PASS",
     "word counts 106, 109, 118 (limit 120; BUILDER 4.2.1), counted on the page text"),
    ("STRUCT-ORDER", "2.9-structure",
     "section order of L07-L09", "PASS",
     "why it matters, core content, inline lab, canon-breaks, misconceptions (3 each), problem set (Mechanics, Proof, "
     "Empirical, Research: 3 problems each, 12 details.solution per page), key-results table, retrieval quiz (9, 9, 11 "
     "items with explanations). No debate brief required (no debate key on M3)"),
    ("HOURS", "2.9-structure",
     "data-hours on L07 (11), L08 (12), L09 (12)", "PASS",
     "equal to plans/M3-build-plan.md section 2.2 (11, 12, 12); the plan's lesson total 105 h and project 45 h sum to "
     "150 h. The hub's split is slice a, not checked here"),
    ("DATA-CLAIM", "2.8-data",
     "course/modules/M/M3/L08.html section 4 'The program does not yet embed a multi-tenor series'", "PASS",
     "course/assets/data/market/MANIFEST.json: fx_daily (6 currencies), fx_monthly (10 currencies), ust_daily "
     "(tbill_3m, cmt_10y). No embedded series has three or more tenors. The claim holds"),
    ("HONEST-GAP", "2.8-data",
     "course/modules/M/M3/L08.html section 4 (Treasury lab not run; SIMULATED panel used)", "PASS",
     "the page states the curriculum's Treasury lab is not run and uses a SIMULATED six-tenor panel; consistent with the "
     "architect decision B2/Q1 in plans/M3-build-plan.md (Architect decisions block)"),
    ("SIMULATED-LABELS", "2.8-data",
     "labs and key-results of L07-L09", "PASS",
     "each lab hypothesis, docstring and key-results row using generated data says SIMULATED; no lab reads a data file "
     "(no data-files attribute on the three lab sections)"),
    ("LAB-RUNTIME-SEEDS", "2.5-labs",
     "labs L07, L08, L09", "PASS",
     f"seeds 7, 8 and 20261028 fixed in the twins; no network; page_smoke lab timings 0.0 to 0.1 s ({G}page_smoke_L07-L09.log)"),
]

NEW_ROWS_NOTE = "Rows NUM, MATH, PROB, LABSTMT, GRADE, NOTATION, STRUCT and DAG are re-derived in round 2 (fresh evidence), not carried."


def main() -> None:
    rows = []
    for item in ROWS:
        rid, check, location, status, evidence = item[:5]
        fix = item[5] if len(item) > 5 else ""
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = fix
        rows.append(row)
    fragment = {
        "unit": "M3",
        "slice": "c",
        "round": 2,
        "verifier": "independent Haiku verifier, checkout verifyD2-M3-c",
        "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
        "base": "d0f39c09598ffefaf0ec18d5d1077cfacd42998b",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-M3-c",
        "scratch": "/private/tmp/verifyD2-M3-c-scratch",
        "verified_at": "2026-11-02",
        "verdict": "FAIL" if any(r["status"] != "PASS" for r in rows) else "PASS",
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": (
            "Lesson slice L07-L09 and lab twins only. Delta since the round-1 pin d0f39c09: L06, L07 and L08 pages changed "
            "only by \\mathbb{R} -> \\R (verified by sed-substituted diff against the old files); L09.html and all lab twins "
            "are byte-identical. Round 2 re-derived every row rather than carrying round-1 PASS rows. Cards for L07-L09 and the "
            "project are slice d and were not checked. Lab twins are demonstrations; project mutation testing does not apply to "
            "them, so no mutants are listed. The lab-twin docstring defect (LABDOC-L09) and the raw operator names "
            "(NOTATION-OPNAME) are the two non-PASS rows. The earlier round-1 NOTATION-R FAIL is fixed."
        ),
        "summary": "",
    }
    passes = sum(1 for r in rows if r["status"] == "PASS")
    fails = sum(1 for r in rows if r["status"] == "FAIL")
    fragment["summary"] = (
        f"Slice c (L07-L09 and lab twins), round 2: {len(rows)} rows, {passes} PASS, {fails} FAIL, 0 UNVERIFIABLE. "
        "Gates (check_pages, check_dag, check_projects, run_labs, twins alone under -I -W error, ruff, mypy, page_smoke, "
        "pytest subset, verify_refs offline) all pass. Non-PASS: LABDOC-L09 (lab docstring overreaches: closer count does "
        "not require a correlation matrix) and NOTATION-OPNAME (raw \\operatorname{tr} and \\operatorname{diag} where "
        "registered macros exist)."
    )
    out = pathlib.Path("ledgers/M3/M3-c.json")
    out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} rows={len(rows)} pass={passes} fail={fails}")


if __name__ == "__main__":
    main()
