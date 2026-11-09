import json, sys
root = sys.argv[1]
S = "ledgers/M3/scripts/M3-c-r1/out/"
CARRY = "Carried from round 11 (course/modules/M/M3/L07.html, L08.html, L09.html and tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py byte-identical since the previous pin ccaeeaf4, git diff empty): "
rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)

# ---- gates (re-run at pin 95f3f8cb; ledgers/M3/scripts/M3-c-r1/gates.sh, rc per command in out/gates.out)
row("GATE-01", "2.9-gate", "tools/check_pages.py --unit M3; --unit M3 --page L07, L08, L09", "PASS",
    S + "gates.out rc=0 for check_pages_M3, _L07, _L08, _L09; out/check_pages_M3.log: 'check_pages M3: PASS'.")
row("GATE-02", "2.9-gate", "tools/check_dag.py --unit M3", "PASS", S + "check_dag_M3.log: 'check_dag M3: PASS', rc=0.")
row("GATE-03", "2.6-gate", "tools/check_projects.py --unit M3", "PASS",
    S + "check_projects_M3.log: 'check_projects M3: PASS', rc=0 (project slice outside c; re-run because project.html and grader changed in the delta).")
row("GATE-04", "2.5-labs", "tools/run_labs.py --unit M3 (and --page L07, L08, L09)", "PASS",
    S + "run_labs_M3.log 'run_labs M3: PASS (12/12)'; run_labs_L07/L08/L09.log each 'PASS (1/1)'; all rc=0.")
row("GATE-05", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py run alone", "PASS",
    S + "twin_page_check.out: each run as `.venv/bin/python -I -W error <twin>` gives rc=0, stderr_bytes=0 (L07 11 lines, L08 14, L09 13); 'page code == twin: True; expected == twin stdout: True' for all three.")
row("GATE-06", "2.5-labs", "ruff check tests/labs/M3 course/modules/M/M3/grader; ruff format --check tests/labs/M3", "PASS",
    S + "ruff_check.log 'All checks passed!' rc=0; ruff_format.log '12 files already formatted' rc=0.")
row("GATE-07", "2.4-gate", ".venv/bin/mypy --no-incremental", "PASS", S + "mypy.log 'Success: no issues found in 386 source files', rc=0.")
row("GATE-08", "2.9-gate", "tools/page_smoke.py --unit M3 --pages L07, then L08, then L09 (each alone)", "PASS",
    S + "page_smoke_L07/L08/L09.log each 'page_smoke M3: PASS', rc=0.")
row("GATE-09", "2.1-citations", "tools/verify_refs.py --offline", "PASS",
    S + "verify_refs_offline.log 'offline integrity: 560 entries, 0 problems', rc=0 (references.json changed in the delta for an unrelated entry; no M3 citation changed).")
row("GATE-10", "2.5-labs", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k M3", "PASS",
    S + "pytest_M3.log: 12 dots, rc=0; out/collect_M3.out 'tests/test_labs.py: 12' (collect-only, the other two files select no M3 test).")
row("GATE-11", "2.9-gate", "tools/build_site.py --check", "PASS", S + "build_site_check.log 'site data current: 6 outputs', rc=0.")
row("GATE-12", "2.9-gate", "tools/render_curriculum.py then git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json", "PASS",
    S + "render_curriculum.log rc=0; render_diff rc=0 (regenerated files equal the committed ones).")
row("GATE-13", "2.8-data", "tools/fetch_data.py --check", "PASS", S + "fetch_data_check.log 'fetch_data: 3 datasets, 0 problems', rc=0.")

# ---- lab twins and page code (re-run; pages and twins byte-identical, but re-run because the lab gate is part of the slice)
for L in ("07", "08", "09"):
    row(f"LAB-L{L}-EMBED", "2.5-labs", f"course/modules/M/M3/L{L}.html section#lab-M3-L{L}-1 vs tests/labs/M3/lab-M3-L{L}-1.py", "PASS",
        S + "twin_page_check.out: 'L" + L + " page code == twin: True; expected == twin stdout: True' (page and twin byte-identical since ccaeeaf4).")

# ---- carried rows (subject byte-identical since ccaeeaf4)
row("LABSTMT-L07", "2.5-labs", "L07.html line 125 (hypothesis); code 126-192; expected 193-203; interpretation 204; twin docstring 131-139", "PASS",
    CARRY + "the same locators; the re-run output (out/twin_page_check.out, L07 11 lines) matches the expected block; interpretation 'Every check prints True' matches the twin's six True lines.")
row("LABSTMT-L08", "2.5-labs", "L08.html line 146 (hypothesis); code 147-269; expected 270-283; interpretation 284; twin docstring 147-160", "PASS",
    CARRY + "the same locators; out/twin_page_check.out L08 matches the expected block.")
row("LABSTMT-L09", "2.5-labs", "L09.html line 190 (hypothesis); code 191-332; expected 333-345; interpretation 346; twin docstring 191-211", "PASS",
    CARRY + "the same locators; out/twin_page_check.out L09 matches the expected block.")
row("LABSTMT-RUNTIME", "2.5-labs", "tests/labs/M3/lab-M3-L07-1.py, lab-M3-L08-1.py, lab-M3-L09-1.py (imports, seeds, network)", "PASS",
    CARRY + "twins re-run with -I -W error: rc=0, empty stderr (out/twin_page_check.out).")
row("LABDOC-L09", "2.2-lab-prose", "tests/labs/M3/lab-M3-L09-1.py docstring lines 191-211 vs code 213-332 (page lines 191-211)", "PASS", CARRY + "twin unchanged; docstring unchanged.")
row("LABDOC-L09-TOL", "2.2-lab-prose", "L09.html lines 190 and 346 vs twin constants TOL, FEASIBLE_TOL, NONPSD_TOL (twin lines 30-32)", "PASS",
    CARRY + "twin constants TOL=1e-12, FEASIBLE_TOL=1e-8, NONPSD_TOL=1e-9 (lab-M3-L09-1.py lines 30-32) re-read in this round.")
row("NUM-L07", "2.2-numbers", "L07.html lines 199-203 (expected), 222 (residual 0.8951), 302 (A^T y), 307-309 (intercept 1.3325)", "PASS",
    CARRY + "re-run output: intercept 1.3325, slopes 0.8488 and -0.4120, residual 0.8951, A^T y 18.38 3.10 -17.60 (out/twin_page_check.out).")
row("NUM-L07-M", "2.2-numbers", "L07.html line 350 (rank 2 of 3) and the duplicated-column check (lab lines 183-189)", "PASS", CARRY + "re-run prints 'rank of A^T A with a duplicated column: 2 (of 3)'.")
row("NUM-L08", "2.2-numbers", "L08.html lines 275, 282-284 (shares 75.9/18.1/5.2; rescaling 0.7587 -> 0.9791; bound 0.9483; inputs 13.6818, 88.2028), 304 (cos 0.9985), 433", "PASS",
    CARRY + "re-run prints shares 75.9 18.1 5.2, 0.7587 -> 0.9791, bound 0.9483, M11 13.6818, trace 88.2028, cosines 0.9994/0.9985/0.9990.")
row("NUM-L09", "2.2-numbers", "L09.html lines 52, 336, 345-347, 444 (sqrt 0.96), 452, 494-497", "PASS",
    CARRY + "re-run prints ||C0-B||_F^2 = 0.6400000000, 23 of 40 non-PSD, 23 of 23 passing and closer.")
row("ALT-L09", "2.5-labs (robustness)", "tests/labs/M3/lab-M3-L09-1.py repair procedures vs alternative correct procedures", "PASS", CARRY + "twin unchanged; no new alternative run (no grader in slice c).")
row("ALT-L08", "2.5-labs (robustness)", "L08.html Lab 1 eigh-based PCA vs an SVD route", "PASS", CARRY + "twin unchanged.")
row("MATH-L07", "2.4-math", "L07.html Definition 1.1 (60), Theorem 1.2 (64-71) and proof (75-81), Theorem 1.3 (84-86) and proof (90), Remark 1.4 (94-95), Theorem 2.2 (108-115) and proof (119-120)", "PASS", CARRY + "page statements unchanged.")
row("MATH-L08", "2.4-math", "L08.html Proposition 1.1 (61-62), Proposition 1.2 (71-72), Definition 1.3 (82), Theorem 1.4 (86-87) and proof (92), Theorem 2.1 (100-105) and proof (110-112), Corollary 2.2 (117), Proposition 2.3 (121-122) and proof (127), Remark 2.4 (131-132), Section 3 (137), Definition 3.1 (141)", "PASS", CARRY + "page statements unchanged; Remark 2.4 (line 131) re-read for card c138 and still proves the claim with M positive semidefinite (Prop 1.1).")
row("MATH-L09", "2.4-math", "L09.html Definition 1.1 (59-60), Definition 1.2 (64-65), Lemma 1.3 (71) and proof (77-81), Definition 2.1 (89), Example 2.3 (99-104), Definition 3.1 (114), Proposition 3.2 (119-121) and proof (127-131), Proposition 3.3 (136-137) and proof (143-144), Proposition 3.4 (148-149) and proof (154-156), Proposition 3.5 (161) and proof (166-170), Example 3.6 (175-177), Method 2 (184), Remark 2.2 (94-96)", "PASS", CARRY + "page statements unchanged; Proposition 3.3(a) re-read for card c161.")
row("PROP23-HYP", "2.4-math", "L08.html Proposition 2.3 statement (122), proof (127), E2 solution (384), key-results row (432)", "PASS", CARRY + "page unchanged.")
row("KEY-L08-430", "2.9-key-results", "L08.html key-results row 430 vs Theorem 1.4 (line 87)", "PASS", CARRY + "page unchanged.")
row("PROB-L07", "2.4-math", "L07.html problems M1-M3 (241-261), P1-P3 (266-286), E1-E3 (291-311), R1-R3 (316-336), each with <details class=solution>", "PASS", CARRY + "page unchanged.")
row("PROB-L08", "2.4-math", "L08.html problems M1-M3 (323-343), P1-P3 (348-368), E1-E3 (373-393), R1-R3 (398-418)", "PASS", CARRY + "page unchanged.")
row("PROB-L09", "2.4-math", "L09.html problems M1-M3 (384-402), P1-P3 (409-428), E1-E3 (433-453), R1-R3 (458-478)", "PASS", CARRY + "page unchanged.")
row("GRADE-L07", "2.3-grades", "L07.html block titles (64 T, 84 T, 108 T); Remark 1.4 (94-95) via key-results rows 346-348 (T); row 350 (C)", "PASS", CARRY + "page unchanged.")
row("GRADE-L08", "2.3-grades", "L08.html block titles (61 T, 71 T, 86 T, 100 T, 116 T, 121 T) and key-results table (428-434)", "PASS", CARRY + "page unchanged.")
row("GRADE-L09", "2.3-grades", "L09.html block titles (59, 63, 70, 89, 111, 118, 135, 147, 159, 174) and key-results rows 488-497", "PASS", CARRY + "page unchanged.")
row("CITE-L07-L09", "2.1-citations", "L07.html, L08.html, L09.html (grep: no data-cite, no data-locator; <ol data-references> empty at lines 431, 519, 592)", "PASS",
    CARRY + "pages unchanged; references/references.json changed only in an unrelated entry (used_by FC2, line 2922 area), which none of these pages cite.")

row("XREF-EARLIER", "2.9-xref", "L07.html line 56 (notation paragraph: 'with the inner product and norm of Lesson 6'); L08.html line 58 and L09.html lines 56, 65 (Lesson 6, Proposition 2.4); L09.html line 68 (Lesson 6, Definition 1.1); L08 Lesson 6 sign-freedom note; L09 Lesson 4 Definition 1.1 and Theorem 2.3; L09 Lesson 5 Theorem 2.1 and Definition 1.4; L07 Lesson 1 Theorem 3.7 and Fact 1.2 of Lesson 6", "FAIL",
    "Lesson 6 changed in the delta: course/modules/M/M3/L06.html line 56 now reads 'The inner product, the norm, orthogonality and orthonormality are the terms of Lesson 4, Definition 1.2, and are not restated here.' (the old line 56 defined the inner product and norm). L07.html line 56 still says 'with the inner product and norm of Lesson 6', which points the reader to a lesson that no longer defines them (checked: re-read 'Unless a proof says otherwise' paragraph, L06 lines 56-59). All other earlier-lesson targets re-checked and correct: L06 Definition 1.1 (line 59, title now 'restated from Lesson 4, Definition 1.2'; orthogonal matrix still defined there), L06 Proposition 2.4 (line 126, Frobenius identity and trace, statement unchanged; the line-132 change is a macro only), L05 Theorem 2.1 (line 108), L05 Definition 1.4 (line 71-72), L04 Theorem 2.3 (line 130), L04 Definition 1.1 and 1.2 (lines 68, 73), L06 Fact 1.2 (line 64), L01 Theorem 3.7 (line 161, title unchanged; L01 hunks are the lab title and a SIMULATED note).",
    "L07.html line 56: change 'with the inner product and norm of Lesson 6' to 'with the inner product and norm of Lesson 4, Definition 1.2' (the terms L06 now points to), then re-run check_pages --unit M3 --page L07 and page_smoke L07.")
row("DAG-PSD-REDEF", "2.9-dag", "course/modules/M/M3/L09.html line 122 (pointer to Lesson 5, Definition 1.4) and line 56 (link only) versus L05.html line 72 (the only dfn for positive semidefinite)", "PASS",
    "Re-verified: grep of L05.html '<dfn' finds the PSD dfn only at line 72 (out/delta_checks.out 'L05 PSD dfn lines: [72]'); L05 hunks of this delta (lines 51, 130, 186-188, 303, 330, 453-455) do not touch line 72; L09.html line 122 still points to Lesson 5 Definition 1.4.")
for ident, desc in [("NOTATION-R", "L07, L08, L09 math using \\R"), ("NOTATION-OPNAME", "registered \\tr and \\diag: L08 lines 56-72, 137; L07 lines 56, 332; L09 lines 56-65"),
                    ("NOTATION-T", "L08.html Section 1 (line 56) and Lab 1 (T_DAYS = 750)"), ("NOTATION-AST", "L09.html lines 90 and 93 (C^{\\ast})"),
                    ("NOTATION-Q", "L07, L09 orthogonal Q; \\mathbb{Q} registered"), ("NOTATION-OTHER", "all control sequences in math on L07, L08, L09")]:
    row(ident, "2.9-notation", desc, "PASS", CARRY + "pages unchanged and notation/notation.json byte-identical (git diff empty).")
row("DEF-L08-CLOSE", "2.9-structure", "L08.html Section 3 (137), Definition 3.1 (141), quiz item L08q9 (505-511)", "PASS", CARRY + "page unchanged (Definition 3.1 now at line 140 in the file read this round; text unchanged).")
row("DEF-L08-MATCH", "2.2-lab-prose", "L08.html Definition 3.1 (141), canon-break (292), quiz explanation (511), lab matches (238-246, 277-280)", "PASS", CARRY + "page unchanged.")
row("DAG-LINKS", "2.9-dag", "L07.html, L08.html, L09.html meta rows (lines 38-39)", "PASS", CARRY + "pages unchanged; check_dag M3 PASS (GATE-02).")
row("DAG-M4", "2.9-dag", "L07-L09 covariance, variance, correlation, expectation wording; curriculum.json concepts: correlation and covariance-matrix owned by M4", "PASS",
    "Re-verified: a leaf-level diff of curriculum/curriculum.json between ccaeeaf4 and HEAD changes exactly one leaf, /parts/1/modules/2/project/brief (the M3 project brief); the concept entries are unchanged; check_dag M3 PASS.")
row("DAG-PROSE-UNLINKED", "2.9-dag", "L09.html line 60 (positive semidefinite in Definition 1.1) and other plain PSD mentions", "PASS", CARRY + "pages unchanged; Lesson 5 Definition 1.4 unchanged (see DAG-PSD-REDEF).")
row("CONCEPT-L08-LSC", "2.9-dag/2.3-grades", "course/modules/M/M3/L08.html line 39 (Introduces link text), line 141 (dfn id=def-level-slope-curvature)", "PASS", CARRY + "page unchanged.")
row("DEFINE-BEFORE-USE", "2.9-prose", "first uses of tenor, trace, cosine, PSD, eigenvalue clipping, orthogonal, Frobenius, explained share (L08 52-58, 137, 141; L09 52-65, 109-116)", "PASS",
    "Re-verified for the delta-touched definitions: 'orthogonal' (L09 line 68) points to L06 Definition 1.1 (line 59), which still defines the orthogonal matrix; 'trace' and 'Frobenius' (L08 line 58; L09 lines 56, 65) point to L06 Proposition 2.4 (line 126), which still states both; 'PSD' points to L05 Definition 1.4 (line 71); the L08 and L09 pages are byte-identical.")
row("DEFINE-L08-OVERLINE", "2.9-prose (terms before definition)", "course/modules/M/M3/L08.html line 137 (the centred squared tenors \\tau^{2} - \\overline{\\tau^{2}}\\iota_n)", "PASS", CARRY + "page unchanged.")
row("PLAIN-REDEF", "2.9-dag", "L09.html line 68 (orthogonal matrices cross-reference) and line 56 (trace, symmetry)", "PASS",
    "Re-verified: L09.html line 68 'Orthogonal matrices are as in Lesson 6, Definition 1.1.' still resolves (L06 line 59 defines the orthogonal matrix); line 56 targets (Lesson 4 Definition 1.1 at L04 line 68; Lesson 6 Proposition 2.4) unchanged.")
row("PROSE-PROCESS", "2.9-prose", "L07, L08, L09 learner text (banned and process-word sweep)", "PASS", CARRY + "pages unchanged.")
row("PROSE-ELLIPSIS", "2.9-prose", "L07.html 398, 412; L08.html 445, 459, 505; L09.html 527, 536 (quiz stems ending in an ellipsis)", "PASS", CARRY + "pages unchanged.")
row("PROSE-SCOPE", "2.9-prose", "scope words on the three pages (always, only, exactly, every, all, any, same, whenever, guarantee, not always, stable, real data, real curve)", "PASS", CARRY + "pages unchanged.")
row("PROSE-REMARK-2.4", "2.9-prose", "L08.html Remark 2.4 (131-133) and its last sentences", "PASS", CARRY + "page unchanged; the card c138 wording matches the remark's hypothesis M_jl != 0 for some l != j.")
row("STRUCT-WHY", "2.9-structure", "L07 line 52, L08 line 52, L09 line 52 (why-it-matters)", "PASS", CARRY + "pages unchanged.")
row("STRUCT-ORDER", "2.9-structure", "L07, L08, L09 section order and counts (BUILDER_RULES 4.2)", "PASS", CARRY + "pages unchanged.")
row("HOURS", "2.9-hours", "L07.html data-hours 11 (line 2, eyebrow 35), L08.html 12, L09.html 12; index.html line 29 data-hours-lessons 105 and data-hours-project 45", "PASS",
    "Re-verified: index.html line 29 data-hours-lessons=105 equals the sum of the nine lesson data-hours (L01 12, L02 11, L03 12, L04 12, L05 12, L06 11, L07 11, L08 12, L09 12 = 105); index card kickers match each lesson; data-hours-project=45 and project.html '45 hours' unchanged by the delta hunks; eyebrow 150 hours = 105 + 45.")
row("DATA-CLAIM", "2.8-data", "L08.html canon-break (line 291) 'The program does not yet embed a multi-tenor series from which three or more tenors can be read'", "PASS", CARRY + "page unchanged; the page text is unchanged and fetch_data --check passed (GATE-13); the claim itself was not re-checked against the data beyond that.")
row("HONEST-GAP", "2.8-data", "L08.html canon-break (line 291) and the Section 1 note (line 52)", "PASS", CARRY + "page unchanged.")
row("SIMULATED-LABELS", "2.8-data", "L07 lab (docstring line 128, hypothesis line 125), L08 lines 145-151 and twin docstring line 149, L09 lines 190, 199 and 346", "PASS", CARRY + "pages and twins unchanged.")
row("DELTA-READ", "2.0-delta", "delta ccaeeaf4..95f3f8cb for slice c (git diff)", "PASS",
    "Re-run: git diff --stat ccaeeaf4..HEAD -- course/modules/M/M3 tests/labs/M3 gives L01, L02, L04, L05, L06, cards.json, grader/test_project.py, index.html, project.html and four M3 twins (L01, L02, L05, L06); L07/L08/L09 pages and their twins are unchanged. Slice-c subjects changed: cards.json (16 L07-L09 cards changed, c201 removed, c214 and c217 added; lesson counts L07 21, L08 28, L09 29) and index.html (lines 33, 133, 164). Repo-wide diff is 11111 files (other units and ledgers); only slice paths were read as the delta. Hunks of L01, L02, L04, L05, L06 read in full (see notes).")
row("HYP-L08-DEF31", "2.4-math/2.9-structure", "L08.html Section 3 (line 137) and Definition 3.1 (line 141)", "PASS", CARRY + "page unchanged; re-read for card c211 (three distinct tenor values; Lesson 7 Theorem 1.2 hypothesis: independent columns, L07 line 64-72).")

# ---- cards (cards.json changed: re-verify from scratch every subject that changed)
row("CARDS-DUP-SCAN", "2.7-cards", "course/modules/M/M3/cards.json (all 210 cards)", "PASS",
    "ledgers/M3/scripts/M3-c-r1/out/cards_scan.out: 'cards 210 dup ids [] dup fronts [] dup backs []'; key sets uniform; L07 21, L08 28, L09 29 (78 L07-L09 cards); no T card carries a basis; every C card carries a basis.")
row("CARDS-READ-L07-L09", "2.7-cards", "course/modules/M/M3/cards.json, the 78 cards with lesson L07 (21), L08 (28) or L09 (29)", "FAIL",
    "All 16 changed L07-L09 cards and the 2 added (c214, c217) and the 1 changed ungraded card (c211) were read against the current lesson text (see CARD-* rows). Unchanged cards are byte-identical to ccaeeaf4 (checked in cards_scan/delta_checks). Result: card M3-c145 is over-graded (row CARD-C145).",
    "Fix CARD-C145 as specified in that row, then re-verify the card set.")
row("CARD-C127", "2.7-cards / 2.4-math", "cards.json entry M3-c127 (now line 860 of cards.json; was 873 at ccaeeaf4), L07, T; vs L07.html misconception 1 (lines 220-223) and Remark 1.4 (94-95)", "PASS",
    CARRY + "the entry M3-c127 is byte-identical (delta_checks.out 'M3-c127 byte-identical'); the line number moved because cards above it changed.")
row("CARD-C167", "2.7-cards / 2.2-claims", "cards.json entry M3-c167 (line 1132, L09, grade C, basis 'Lab 1, 40 seeded 5 x 5 SIMULATED matrices') vs L09.html misconception 3 (lines 368-374), Definition 2.1 (89), Remark 2.2 (94-96), printed output (out/twin_page_check.out; lab lines 117-137)", "PASS",
    "Re-verified: only the basis string changed (dropped '(seed 20261028)'). Claims: lab prints '23 of 23' for is_correlation pass and strictly-closer counts; tolerances TOL 1e-12, FEASIBLE_TOL 1e-8 (lab lines 30-31) match the card; Remark 2.2 last sentence supports 'not nearest' up to tolerance. Grade C with a SIMULATED basis is consistent.")
row("CARDS-NEW-c208-c213", "2.7-cards / 2.4-math", "cards.json M3-c208 (line 1380, L09, T), M3-c209 (1387, L07), M3-c210 (1393, L08), M3-c211 (1399, L08), M3-c212 (1405), M3-c213 (1411)", "PASS",
    "Re-verified all six (c211 changed): c208 = L09 Method 1 (line 182) with Propositions 3.2(a) and 3.4 (line 148) and the positive-diagonal hypothesis; c209 = L07 Section 1 column space definition; c210 = L08 Section 3 cosine (line 137); c211 = L08 Section 3 (line 137) 'at least three distinct tenor values', with the earlier shapes independent and Lesson 7 Theorem 1.2 (hypothesis: independent columns) at L07 lines 64-72; c212 and c213 = L08 Section 1 tenor and bp definitions.")
row("HUB-L08-TITLE", "2.9-structure (cross-page title agreement)", "course/modules/M/M3/index.html line 155 (hub card for L08) vs L08.html h1", "PASS",
    "Re-verified: index.html line 155 card-title is 'Principal Component Analysis and Level-like, Slope-like and Curvature-like Directions', equal to the L08.html h1 text; line 155 is not in any delta hunk (hunks at lines 33, 133, 164).")

# ---- new rows for the delta-changed subjects
row("CARD-C138", "2.7-cards / 2.4-math", "cards.json M3-c138 (line 935, L08, T) vs L08.html Remark 2.4 (lines 131-133)", "PASS",
    "Re-verified (front and back changed in the delta to add 'M_jl nonzero for some l other than j'). Remark 2.4 proves the claim under the same hypothesis, using Proposition 1.1 (M positive semidefinite, so M_jj > 0). The card text does not repeat 'M positive semidefinite'; without it the answer fails (M = [[0,1],[1,0]], c = 2 gives M' = 2M). The lesson's M is the PSD matrix of Section 2 throughout, so the card is correct in its lesson context; recorded as a note, not a defect.")
row("CARD-C145", "2.7-cards / 2.4-math", "cards.json M3-c145 (line 986, L08, grade T, basis None) vs L08.html misconception 2 (lines 311-312) and Theorem 2.1 (100-105)", "FAIL",
    "The card is graded T with no basis and says 'False ... which component is level-like depends on the data, because the order of the components follows the eigenvalues (Theorem 2.1)'. A T 'False' for 'always' needs a counterexample proved on the page. L08 contains none: Theorem 2.1 gives only the order of eigenvalues; Lab 1 shows level first on one panel (the page itself says the lab does not vary the scales, line 312); line 292 says no computation on real data is made. The delta changed the grade from C to T without adding the counterexample. The same unproved sentence is in L08.html line 312.",
    "Either (a) grade M3-c145 as C with basis 'Theorem 2.1 and the Lab 1 panel (one SIMULATED case)' and reword the back to say the page shows one panel only, or (b) add to L08 Section 3 a short constructed case: with f1, f3 from Definition 3.1, M = f3 f3^T + (1/2) f1 f1^T is PSD with eigenvalues 1, 1/2, 0, so by Theorem 2.1 its top direction v1 = f3 is curvature-like and PC1 is not level-like; cite it in the card's basis (T) and in L08.html line 312. Then re-run check_pages --unit M3 --page L08, run_labs (unchanged), and re-verify this row.")
row("CARD-C211", "2.7-cards / 2.4-math", "cards.json M3-c211 (line 1399, L08, ungraded) vs L08.html Section 3 (line 137) and Lesson 7 Theorem 1.2 (lines 64-72)", "PASS",
    "Re-verified (changed in the delta): 'at least three distinct tenor values' matches Definition 3.1 (line 141) and line 137; the earlier shapes are then nonzero, mutually orthogonal and independent, which is the hypothesis of L07 Theorem 1.2 (columns linearly independent). Ungraded card, so no grade claim.")
row("CARD-C214", "2.7-cards / 2.2-claims", "cards.json M3-c214 (line 1417, L08, grade C, basis 'Lab 1, one SIMULATED six-tenor panel') vs L08.html lines 146, 239-241, 277-279, 311-312 and twin lines 192-194", "PASS",
    "New card. 'PC1 is level-like' matches the printed 'planted level: best-matching component PC1, |cosine| 0.9994' (Definition 3.1 match); 8 bp per day on the level factor matches twin line 192 (scale=8.0) and L08 line 146; 'the lab does not vary the planted scales' matches L08 line 146 and 312. Grade C with a SIMULATED basis is consistent.")
row("CARD-C217", "2.7-cards / 2.2-claims", "cards.json M3-c217 (line 1437, L09, grade C, basis 'Lab 1, one fixed matrix C0 (Example 2.3)') vs L09.html Example 2.3 (lines 99-104) and the printed output", "PASS",
    "New card. C0 = [[1, 0.9, 0.9], [0.9, 1, -0.9], [0.9, -0.9, 1]] matches Example 2.3 (line 101). Eigenvalues -0.8, 1.9, 1.9 match the printed 'C0 eigenvalues, ascending: -0.800000 1.900000 1.900000' (out/twin_page_check.out L09) and trace 3 and det -2.888 (hand check).")
row("CARD-C201-REMOVED", "2.7-cards", "cards.json: M3-c201 (L08, grade T, Corollary 2.2) removed in the delta", "PASS",
    "Removal is not a defect: the content is still on the page (L08 Corollary 2.2 line 116-118). grep -r 'M3-c201' course/ tools/ returns no lines (re-run this round). Recorded for the record.")
row("CARD-LAB-L07", "2.7-cards / 2.2-numbers", "cards.json M3-c124, c125, c126, c177 (lines 836, 844, 852, 1201) vs L07 expected block and twin output", "PASS",
    "Basis strings changed only (seed removed) and c177 back dropped the seed. Re-verified against out/twin_page_check.out: c124 'Every check prints True' (six identity lines True); c125 intercept 1.3325, slopes 0.8488 and -0.4120, generator 1.5, 0.8, -0.4 (twin line 30); c126 residual 0.8951; c177 rank 2 (of 3).")
row("CARD-LAB-L08", "2.7-cards / 2.2-numbers", "cards.json M3-c139, c140, c141, c174 (lines 942, 950, 958, 1185) vs L08 expected block and twin output", "PASS",
    "Basis strings changed only. Re-verified: c139 all identities True; c140 cosines 0.9994 (PC1), 0.9985 (PC2), 0.9990 (PC3); c141 first share 0.7587 -> 0.9791; c174 shares 75.9, 18.1, 5.2 from unrounded eigenvalues.")
row("CARD-LAB-L09", "2.7-cards / 2.2-numbers", "cards.json M3-c161, c162, c163, c175 (lines 1086, 1094, 1102, 1193) vs L09 expected block and twin output", "PASS",
    "c161 back drops the printed-eigenvalues sentence; re-verified 0.6400000000 = sum of squared negative eigenvalues of C0 and Proposition 3.3(a) (line 136-137, eps=0). c162 23 of 40 (smallest eigenvalue below -1e-9). c163 and c175: 23 of 23 pass is_correlation and 23 of 23 strictly closer (out/twin_page_check.out L09 lines). Basis strings changed only (seed removed).")
row("INDEX-HUB-EDITS", "2.9-structure", "course/modules/M/M3/index.html lines 33 (lede), 133 (skill check 2), 164 (worked example rung)", "PASS",
    "Re-verified: line 133 explanation ('rescaling step ... taught in Lesson 9') matches L09 Method 1 (line 182); C = D^{-1} S D^{-1} is correct for S = D C D with D diagonal positive; line 164 and line 33 contain no claim about L07-L09 beyond the Lesson 9 pointer.")

verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "M3",
    "slice": "c",
    "round": 1,
    "verifier": "independent Haiku verifier (closing delta, round 1), checkout verifyF21-M3-c",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "ccaeeaf44bea94b37d912ec1da3c660bb2c55d87",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M3-c",
    "scratch": "ledgers/M3/scripts/M3-c-r1/ (gates.sh, twin_page_check.py, cards_scan.py, delta_checks.py, build_fragment.py; logs in out/)",
    "verified_at": "2026-11-09",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "CLOSING DELTA per ruling 30 (plans/FINAL-ARCHITECT-RULINGS.md) and ruling 37 (no new mutants). Delta = git diff ccaeeaf4..95f3f8cb over the slice paths. "
        "Base fragment ~/.fanout/frags/D-M3-c.round11.json (round 11, pin ccaeeaf4, all 75 rows PASS). Round field is 1 per the assignment; the base round was 11. "
        "Subjects that changed: cards.json (16 L07-L09 cards changed, M3-c201 removed, M3-c214 and M3-c217 added); index.html (lines 33, 133, 164). "
        "Subjects that changed through an earlier lesson: L06.html (line 56 now says the inner product and norm are Lesson 4 Definition 1.2; line 59 title restated), L05.html (hunks at 51, 130, 186-188, 303, 330, 453-455; the PSD dfn at line 72 unchanged), L04 (hunks at 51, 104, 146, 176, 337-394; theorem and definition lines unchanged), L01 and L02 (lab title and SIMULATED notes). "
        "L07, L08, L09 pages and their four lab-twin files are byte-identical to ccaeeaf4; every row that cites only them is carried with the prefix. "
        "Hunks read in full: cards.json (all 210 entries compared by id), index.html (3 hunks), L06 (all hunks, for cross-reference targets), L05 and L04 (hunks checked against cited targets). "
        "Not in slice c: project.html, project grader test_project.py (project slice; 163 to 198 tests), curriculum project brief, tests/test_lx1_project_lab3.py, and the other units. Not re-run: run_graders and mutate_graders for the M3 project (project slice). "
        "No mutants: slice c is lab and lesson pages; VERIFIER_RULES 2.6 mutation applies to project graders only. "
        "Calibration: slice c is not a rubric slice; no M3 blind scorer file exists in ~/.fanout/blind (files there are BK4-c, CS2-d, FC2-d, LX1-c, PC3-c); no calibration rows in the base. "
        "Not checked: visual screenshots (page_smoke PASS relied on, as in the base); live verify_refs (offline ruling); the proofs of L07-L09 theorems were not re-derived in this round because their pages are byte-identical (carried)."
    ),
    "summary": (
        f"M3 slice c closing delta at pin 95f3f8cb: {len(rows)} rows; "
        f"PASS={sum(1 for r in rows if r['status']=='PASS')} FAIL={sum(1 for r in rows if r['status']=='FAIL')}. "
        "Non-PASS: XREF-EARLIER (L07.html line 56 cites Lesson 6 for the inner product and norm, which Lesson 6 no longer defines); "
        "CARD-C145 (T grade with no counterexample on the page); CARDS-READ-L07-L09 (carries CARD-C145)."
    ),
}
json.dump(frag, open(root + "/ledgers/M3/M3-c.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows", len(rows), "verdict", verdict)
