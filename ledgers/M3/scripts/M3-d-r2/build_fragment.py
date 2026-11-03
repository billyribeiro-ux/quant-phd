"""Write the round-2 M3-d verifier fragment (ledgers/M3/M3-d.json) from the evidence gathered in this checkout."""
import json

NOTE_CARRY = "Carried from round 1 (grader/test_project.py, instance.py, reference.py, starter.py byte-identical since the previous pin d0f39c0; git diff empty):"
O = "ledgers/M3/scripts/M3-d-r2/out"
rows = []


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    rows.append(r)


# ---- gates re-run on pin c737272
row("gate-check-pages", "gate: tools/check_pages.py --all (M3 line)", "course/modules/M/M3/*", "PASS",
    f"{O}/check_pages.out: 'check_pages M3: PASS', exit 0.")
row("gate-check-dag", "gate: tools/check_dag.py --all (M3 line)", "course/modules/M/M3/*", "PASS",
    f"{O}/check_dag.out: 'check_dag M3: PASS', exit 0.")
row("gate-check-projects", "gate: tools/check_projects.py --all (M3 line)", "course/modules/M/M3/project.html", "PASS",
    f"{O}/check_projects.out: 'check_projects M3: PASS', exit 0.")
row("gate-run-graders", "gate: tools/run_graders.py --unit M3 --seeds 0-49", "course/modules/M/M3/grader/", "PASS",
    f"{O}/run_graders.out: 'run_graders M3: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0.")
row("gate-run-labs", "gate: tools/run_labs.py --unit M3 (twins, page code = twin, expected = output)",
    "course/modules/M/M3/L0*.html, project.html", "PASS", f"{O}/run_labs.out: 'run_labs M3: PASS (12/12)', exit 0.")
row("gate-page-smoke", "gate: tools/page_smoke.py --unit M3 --pages, one page at a time (project, L01..L09, index)",
    "course/modules/M/M3/*.html", "PASS",
    f"{O}/page_smoke_*.out: 11 files, each 'page_smoke M3: PASS' and exit 0 (KaTeX strict check uses notation macros, incl. \\R).")
row("gate-ruff", "gate: ruff check and ruff format --check on grader and tests/labs/M3",
    "course/modules/M/M3/grader/, tests/labs/M3/", "PASS", f"{O}/ruff.out: 'All checks passed!', '16 files already formatted', exit 0 each.")
row("gate-mypy", "gate: mypy --no-incremental on reference.py, instance.py, starter.py", "course/modules/M/M3/grader/", "PASS",
    f"{O}/mypy.out: 'Success: no issues found in 3 source files', exit 0.")
row("gate-verify-refs", "gate: tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"{O}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', exit 0. Live run not performed (no reference changed in M3).")
row("gate-collect-only", "grader test count equals the page's stated count", "course/modules/M/M3/project.html line 237 vs grader/test_project.py", "PASS",
    "Re-run this round: copied test_project.py, instance.py, reference.py (as covariance_doctor.py) to /tmp/m3d_r2_coll; "
    "'QF_SEED=0 .venv/bin/python -I -m pytest --collect-only -q -p no:cacheprovider test_project.py' -> '155 tests collected'. project.html line 237 says '155 tests'.")
row("gate-pytest-relevant", "relevant pytest: lab, page and run-labs suites filtered to M3/page/lab",
    "tests/test_page_checks.py, tests/test_labs.py, tests/test_run_labs.py", "PASS",
    f"{O}/pytest_relevant.out: all dots, '100%', exit 0.")
row("gate-mutate-m3", "tools/mutate_graders.py --unit M3 --seeds 0-9 over every file in ledgers/M3/mutants/ (134 files)",
    "ledgers/M3/mutants/*.py", "FAIL",
    f"{O}/mutate_M3_all_seeds0-9_after_v2d.out: 'mutate_graders M3: FAIL (133/134 killed)'. The one survivor is v2d_06_eigh_uses_numpy_not_standard_library.py, "
    "'SURVIVED ... -> None'. All 128 pre-existing mutants and the five new v2d_01..05 are killed.",
    "Add a grader test that refuses any non-standard-library import in covariance_doctor.py (for example an ast scan for imports outside sys.stdlib_module_names, "
    "so that v2d_06 fails on seed 0). Then v2d_06 is killed; keep the file in mutants/.")
row("gate-reference-starter", "reference passes and starter fails on seeds 0-49", "course/modules/M/M3/grader/reference.py, starter.py", "PASS",
    f"{O}/sources_seeds0-49.out: reference.py 'P' x50, starter.py 'F' x50.")
row("gate-alternatives-seeds-0-49", "six alternatives pass the grader on seeds 0-49 (rule: seeds 0-49 for project graders)",
    "ledgers/M3/alternatives/alt1..alt6", "PASS",
    f"{O}/sources_seeds0-49.out: alt1..alt6 each 'P' x50. Count of spec-conforming alternatives is a separate row.")

# ---- grader
row("gate-named-conditions", "tests demand ValueError only for the four named conditions",
    "course/modules/M/M3/grader/test_project.py (must_raise sites)", "PASS",
    "Re-read this round: must_raise sites at lines 175 (non-square), 185 and 225 (asymmetry beyond 1e-9), 649, 661, 697 (asymmetry), 708 and 732 (volatility conditions). "
    "No other exception assertion. Matches project.html line 235 and the reference's four conditions.")
row("grader-instance", "instance.py matches its docstring and the page's contract", "course/modules/M/M3/grader/instance.py", "PASS",
    NOTE_CARRY + " round 1 read in full: k in {3,4,5}; redrawn until min eigenvalue < -_MARGIN (0.02); unit diagonal; seeded Random.")
row("grader-test-count-and-purity", "grader purity, mutation and repeat-call tests", "grader/test_project.py", "PASS",
    NOTE_CARRY + " test_functions_print_nothing, test_inputs_are_not_mutated, test_repeated_calls_agree present; 155 collected this round.")
row("grader-lab3-reference-numbers", "grader's Lab 3 constants equal the numbers the page prints",
    "grader/test_project.py LAB3_CORR, LAB3_VOLS, test_lab3_reference_numbers_are_matched", "PASS",
    f"{O}/numpy_check.out (independent numpy eigh, clip, Higham nearest correlation to 1e-14): smallest eigenvalue -0.142113; clip distance 0.176573; "
    "nearest distance 0.175003; gap 0.001570; max entry difference 0.011516; det -0.261600; weights 1.778929, -1.096718, -0.255613, 0.573402. All equal the test constants.")
row("grader-browser-timeout", "page states a run in the browser stops after 120 seconds (project.html line 235)",
    "course/assets/js/python.js:4, :36-37", "PASS",
    "python.js line 4: const TIMEOUT_MS = 120000; line 36 message 'Stopped after ${TIMEOUT_MS / 1000} s'.")
row("grader-standard-library-only", "page constraint 'Standard library only' (project.html line 235) is enforced by the grader",
    "course/modules/M/M3/grader/test_project.py (no import test); course/modules/M/M3/project.html line 235", "FAIL",
    "No test inspects imports. v2d_06 (numpy.linalg.eigh inside _eigh) passes seeds 0-9 ('PPPPPPPPPP'). Alternatives alt1, alt3 and alt6 also import numpy and pass seeds 0-49 "
    "(alt1 line 30, alt3 lines 88 and 144, alt6 line 7).",
    "Add an import-scan test (ast over covariance_doctor.py, every imported top-level name must be in sys.stdlib_module_names) that asserts on seed 0. "
    "Resolve the NumPy conflict in row alternatives-five-standard-library first.")
row("grader-reference-docstring", "reference.py docstring prose (not learner text)", "course/modules/M/M3/grader/reference.py lines 1-5", "PASS",
    "Observation only, not a row defect: line 4 reads 'the Frobenius-nearest repair is Alternating projections, with correction terms, ...' (ungrammatical; the reference is not shipped to learners).")

# ---- alternatives
row("alternatives-five-standard-library", "five correct alternatives in different styles that obey the page's constraints (rule: five, seeds 0-49)",
    "ledgers/M3/alternatives/alt1..alt6", "FAIL",
    "Pass seeds 0-49, but only alt2 (Dykstra, other stop rule), alt4 (Jacobi, other cutoffs) and alt5 (Cholesky bisection) are standard-library only. "
    "alt1 (numpy.linalg.eigh, lazy import line 30), alt3 (numpy.linalg.solve and eigvalsh, lines 88 and 144) and alt6 (numpy, line 7) break project.html line 235 'Standard library only'. "
    "Plan M3 section 10 Q3 (binding) says 'NumPy yes' for labs and the project, while project.html line 235 forbids it; section 5.2 lists stdlib options (4) Fraction clipping and (5) shifted power iteration that are not built.",
    "Architect decides Q3 first. If the standard-library constraint stands: build two more stdlib alternatives (plan 5.2 items 4 and 5, Fraction-based clipping and shifted power iteration) that pass seeds 0-49. "
    "If NumPy is allowed for the project: change project.html line 235 and the grader-panel data-packages, and keep alt1, alt3, alt6 as valid alternatives.")
row("alternatives-seeds-0-49", "alternatives run under the grader on seeds 0-49", "ledgers/M3/alternatives/", "PASS",
    f"{O}/sources_seeds0-49.out: all six alternatives 'P' x50. (Spec-conformance is the separate row alternatives-five-standard-library.)")

# ---- mutants
row("mutants-existing-128", "re-run of every pre-existing mutant (128 files) on seeds 0-9",
    "ledgers/M3/mutants/ (pre-existing files)", "PASS",
    f"{O}/mutate_M3_all_seeds0-9_after_v2d.out: every KILLED line for the 128 pre-existing files, including d5/d6/f2/fx/m/r*/b2d/v01-v03 families.")
row("mutants-new-student-errors", "round-1 new student-error mutants vd1_01..vd1_05", "ledgers/M3/mutants/vd1_0[1-5]*.py", "PASS",
    f"{O}/mutate_M3_all_seeds0-9_after_v2d.out: vd1_01 killed by test_lab3_reference_numbers_are_matched (seed 0); vd1_02 by test_clip_repair_negative_floor_keeps_eigenvalue_above_it; "
    "vd1_03 by test_non_square_is_refused[three_rows_two_columns-is_psd]; vd1_04 by test_asymmetry_beyond_tolerance_is_refused; vd1_05 by test_is_psd_one_by_one. All seed 0.")
row("mutants-v2d-01-05", "round-2 new student-error mutants v2d_01..v2d_05 (at least three required)", "ledgers/M3/mutants/v2d_0[1-5]*.py", "PASS",
    f"{O}/mutate_M3_all_seeds0-9_after_v2d.out: each KILLED on seed 0 (clip floor on first eigenvalue only; weights solving for vols; clip refusing non-PSD input; weights refusing a negative weight; Gershgorin min_eigenvalue). "
    f"{O}/run_my_mutants: 'FFFFFFFFFF' per file on seeds 0-9.")
row("mutants-v2d-06", "round-2 student-error mutant v2d_06 (NumPy eigh in _eigh)", "ledgers/M3/mutants/v2d_06_eigh_uses_numpy_not_standard_library.py", "FAIL",
    "Survives seeds 0-9 (PPPPPPPPPP): the grader does not kill a stated-constraint violation (see grader-standard-library-only).",
    "Kill with the standard-library import test; see grader-standard-library-only.")

# ---- equivalents
row("equivalent-r6d-m04", "equivalent: projection stops on gap alone (README proof)", "ledgers/M3/equivalent/r6d_m04_projection_stops_on_gap_only.py", "PASS",
    f"Diff vs grader/reference.py: stop test only (plus docstring). {O}/equiv_proof.log: 290 inputs (60 random per size 2-5 and grader seeds 0-49): "
    "unit-diagonal deviation 0, asymmetry 2.2e-16, min eigenvalue -6.7e-11 (>= -1e-8), never farther from the input than the reference. Survives seeds 0-49 (sources_seeds0-49.out).")
row("equivalent-r11d-m02", "equivalent: projection stops on step alone (README proof)", "ledgers/M3/equivalent/r11d_m02_projection_stops_on_step_only.py", "PASS",
    f"Same measurement as equivalent-r6d-m04 ({O}/equiv_proof.out): identical extremes; survives seeds 0-49.")
row("equivalent-r15d-m03-label", "equivalent: never stops early; label and README agree",
    "ledgers/M3/equivalent/r15d_m03_projection_repair_never_stops_early.py and README.md", "PASS",
    "Round-1 FAIL (label) is fixed: the file is renamed to r15d_m03_projection_repair_never_stops_early.py and README line 'r15d_m03...' matches. Diff vs reference: module docstring lines, the stop test ending in 'and False'. "
    f"Measured over the 290 inputs: min eigenvalue -1.4e-15, unit diagonal exact, farther than reference by at most 7.9e-11 (within any stated tolerance). Survives seeds 0-49. "
    "Nuance: the README says its only change is the stop test and the first docstring line; the diff also adds a docstring sentence. Not a defect.")
row("equivalent-readme-citation", "README cites project.html line 660 as stating no stop criterion",
    "ledgers/M3/equivalent/README.md line 4-5; course/modules/M/M3/project.html lines 233 and 660", "PASS",
    "Line 660 is the stretch prompt on tol and max_iter; it states no criterion. Line 233 states the bound 'stops after at most max_iter alternating steps'. Both support 'no stop criterion stated'. Optional: cite line 233 too.")

# ---- project
row("project-numbers", "every number printed by Lab 1, Lab 2 and Lab 3 and quoted in the rubric, appendix and Lab 3 prose",
    "course/modules/M/M3/project.html lines 57-60, 130-137, 213-220, 460-468, 469, 575, 609, 622", "PASS",
    f"Twins under python -I -W error: lab-M3-project-1/2/3 exit 0 with outputs equal to the page expected blocks. Independent numpy ({O}/numpy_check.out) reproduces "
    "every printed value, including Lab 1 eigenvalues -0.275297 1.463830 1.811467 and Lab 2 -0.203711 1.486490 1.717222, the rebuilt diagonals, the Lab 3 distances and the weights. "
    "Gap 0.001570 = 0.176573 - 0.175003 (unrounded).")
row("project-lab1-memo-sentence", "changed sentence: 'A2's hypothesis of a positive diagonal is met here ... a zero or negative diagonal entry would have printed no value or a deviation of 2'",
    "course/modules/M/M3/project.html Repairs and their checks paragraph (line ~597)", "PASS",
    "Checked against the Lab 3 code path (project.html Lab 3, repaired = x / math.sqrt(d_i d_j)): d_i = 0 gives ZeroDivisionError (no value); mixed sign gives math.sqrt of a negative, ValueError (no value); "
    "both negative gives repaired_ii = -1 and deviation 2. Since Lab 3 printed 0.000000, all rebuilt diagonal entries are positive. Claim holds.")
row("project-conventions-link", "changed link '<a href=\"#conventions\">conventions</a> of Rung 3'", "course/modules/M/M3/project.html Rungs 1 and 2 paragraph", "PASS",
    "id=\"conventions\" exists in project.html; the conventions section defines clipping and the PSD test.")
row("project-hours", "hours arithmetic: project 45 h; components 2+3+14+8+12+6; hub split 105 + 45 = 150",
    "course/modules/M/M3/project.html time budget, index.html line 29 and 39, L01..L09 data-hours", "PASS",
    "Components 2+3+14+8+12+6 = 45 (project.html table); data-hours-project=45 and data-hours-lessons=105 in index.html; L01..L09 data-hours 12+11+12+12+12+11+11+12+12 = 105; 105+45 = 150 = index.html 'Tier F · 150 hours'.")
row("project-proof-A1", "Appendix A1 (clipping gives a PSD matrix)", "course/modules/M/M3/project.html Appendix A1", "PASS",
    "Re-read: X = V Lambda_f V^T; z^T X z = sum max(Lambda_ii, f) (V^T z)_i^2 >= 0 since max >= f >= 0. Hypotheses named (real symmetric, f >= 0, F1 to F4 for the spectral theorem). Correct.")
row("project-proof-A2", "Appendix A2 (rescaling keeps PSD and gives unit diagonal)", "course/modules/M/M3/project.html Appendix A2", "PASS",
    "Re-read: Y_ii = X_ii / (sqrt(d_i))^2 = 1; z^T Y z = q^T X q with q = D^(-1/2) z >= 0. Positivity of d_i named. Correct.")
row("project-proof-A3", "Appendix A3 (two-asset weights and scaling)", "course/modules/M/M3/project.html Appendix A3", "PASS",
    f"Re-read: |rho| < 1 and a, b > 0 named; det = a^2 b^2 (1 - rho^2) > 0; Sigma^-1 iota = (b(b - rho a), a(a - rho b))/det; sum a^2 + b^2 - 2 rho a b = (a-b)^2 + 2ab(1-rho) > 0; scaling by c gives c^2 on each term. "
    f"{O}/numpy_check.out 'A3 check' row agrees with the closed form.")
row("project-proof-A4", "Appendix A4 (clipped matrix singular; rescaled and Sigma singular under positive-diagonal hypothesis)", "course/modules/M/M3/project.html Appendix A4", "PASS",
    "Re-read: Lambda_ii = lambda_i < 0 gives X u_i = V Lambda_0 e_i = 0 (singular); with positive diagonal, z = D^(1/2) u_i gives Y z = D^(-1/2) X u_i = 0; S_v^(-1) z gives Sigma S_v^(-1) z = S_v Y z = 0. Hypotheses named (F1 to F4, negative eigenvalue, positive diagonal, v > 0). Correct.")
row("project-rung-labs", "Labs 1 and 2 (rung 1 worked example; rung 2 completion) and Lab 3", "course/modules/M/M3/project.html; tests/labs/M3/lab-M3-project-1..3.py", "PASS",
    "Twins run alone (python -I -W error) exit 0; run_labs 12/12; Lab 2 blanks (smallest >= -1e-10; math.sqrt(d[i] * d[j])) produce the printed expected output.")
row("project-spec-grader", "specification: function list, signatures, four ValueError conditions, 155 tests, browser 120 s, placement link",
    "course/modules/M/M3/project.html lines 233-237; grader/starter.py lines 15-35; index.html line 68", "PASS",
    "starter.py signatures: min_eigenvalue(matrix), is_psd(matrix, tol=1e-10), clip_repair(matrix, floor=0.0), projection_repair(matrix, tol=1e-10, max_iter=500), comparison_weights(corr, vols) match page line 233. "
    "Named conditions match reference.py. 155 tests collected. Standard-library constraint is the separate FAIL row grader-standard-library-only.")
row("project-exemplars", "exemplars A and B, annotations and official scoring are internally consistent with the rubric",
    "course/modules/M/M3/project.html lines 501-575 (exemplars) and rubric 486-497", "PASS",
    "Each annotation names a rubric descriptor and its level; official scores agree with the annotations (A: C1 2, C2 2, C3 2, C4 1, C5 2; B: 4, 4, 4, 3, 3). Consistency check only: the verifier did not independently re-score the exemplars.")
row("project-rubric", "rubric: five criteria, four levels each, descriptors present", "course/modules/M/M3/project.html lines 486-497", "PASS",
    "Five criteria (C1 to C5), each with four level cells. Level-3 bar stated.")
row("project-references", "Reading: two named sources; no passage locator claimed", "course/modules/M/M3/project.html lines 665-669; references/references.json", "PASS",
    "axler2024linear and strang2023introduction are both keys in references/references.json (count 2). The page says no locator is confirmed and attributes no statement to them.")
row("project-no-process-words", "no process words in learner text (project.html, cards.json, L06-L08 edits)", "course/modules/M/M3/", "PASS",
    "grep -i for verifier, builder, architect, planner, ruling, round, fixer, TODO, placeholder, mutant, ledger: no matches.")
row("project-stretch", "stretch items make no claim", "course/modules/M/M3/project.html lines 656-661", "PASS", "Three open-ended tasks; they state no result.")

# ---- lessons (prose)
for lid in ["L01", "L02", "L03", "L04", "L05", "L09"]:
    row(f"prose-{lid}", f"lesson prose {lid} (statements, proofs, claims)", f"course/modules/M/M3/{lid}.html", "PASS",
        "Carried from round 1 (" + lid + ".html byte-identical since the previous pin d0f39c0; git diff empty this round).")
for lid in ["L06", "L07", "L08"]:
    row(f"prose-{lid}", f"lesson prose {lid}: change since d0f39c0 is the registered-macro substitution only",
        f"course/modules/M/M3/{lid}.html", "PASS",
        "Only change: \\mathbb{R} replaced by \\R (notation/notation.json macro \\R = \\mathbb{R}). Normalising \\R back to \\mathbb{R} reproduces the previous file exactly "
        f"(counts 14/13/6 identical). KaTeX strict check of the page passes (gate-page-smoke).")
row("notation-registry", "every symbol and macro vs notation/notation.json; a registered symbol never reused",
    "course/modules/M/M3/*.html, cards.json; notation/notation.json", "PASS",
    f"{O}/notation_m3.txt lists every control word: registered in use are \\R, \\diag, \\tr only; no \\mathbb{{R}} remains. T is used as the number of observations (L08), matching the registry meaning. "
    "\\mathbb{C} (L04 x3, L06 x1) and \\Sigma, \\Lambda etc. are not registry program-wide symbols. \\ast appears only in C^{\\ast} (L09, nearest correlation matrix); R^\\ast, x^\\ast and R^{e\\ast} are registered with other meanings and are not used.",
    None)
row("notation-R-macro", "module pages use the registered \\R, not \\mathbb{R}", "course/modules/M/M3/*.html", "PASS",
    f"grep counts: 0 occurrences of mathbb{{R}} in M3; \\R occurs in L01-L08 (40/20/12/10/9/4/10/4 counts in those files); page_smoke KaTeX strict check passes.")
row("dag-linked-concepts", "concept links in M3 are within the unit's prerequisite closure", "course/modules/M/M3/*.html data-concept links", "PASS",
    f"check_dag M3: PASS. Linked concepts used in M3: eigendecomposition, spectral-theorem, vector-space, positive-semidefinite-matrix, singular-value-decomposition, quantifiers, principal-component-analysis, orthogonal-projection, nearest-correlation-matrix, mathematical-induction, linear-map, level-slope-curvature, least-squares-projection, eigenvalue-clipping, direct-proof.")
row("dag-m4-concepts-by-name", "M4 concepts (covariance-matrix, correlation, variance, expectation, standard deviation, Gaussian) used by name in M3 without a link",
    "course/modules/M/M3/*.html, project.html, grader/starter.py", "PASS",
    "Architect ruling 3 (plans/FINAL-ARCHITECT-RULINGS.md) and plan M3 B1 option (a) allow these words as plain prose. Verified: no data-concept link to covariance-matrix, correlation, variance or expectation exists in M3; the word 'expectation' is not used.")
row("hours-arithmetic", "hub split and lesson hours", "course/modules/M/M3/index.html, L01..L09 data-hours, project.html data-hours-*", "PASS",
    "105 lesson hours (sum of the nine data-hours), 45 project hours, 150 total; project components sum to 45. Hours are design targets (ruling) so only arithmetic is checked.")

# ---- cards
card_carry = "Carried from round 1 (cards.json entries for these ids are identical to d0f39c0, checked per entry by JSON comparison; only M3-c131 changed and M3-c204 was added):"
row("cards-structure", "cards.json: unique ids, each lesson exists and has cards, grade values valid, citations resolve",
    "course/modules/M/M3/cards.json (201 cards)", "PASS",
    "Python JSON check: 201 cards, no duplicate ids, grades T (114), C (39) or absent (48, check_pages allows absent grade), every lesson L01..L09 has cards; check_pages M3 PASS.")
row("cards-id-sequence", "card ids sequential (round-1 FAIL)", "course/modules/M/M3/cards.json", "PASS",
    "Architect ruling 2 (plans/FINAL-ARCHITECT-RULINGS.md item 2): ids need not be sequential; gaps and out-of-order appended ids are not defects. check_pages does not require it.")
row("cards-numbers-cited", "every numbered label a card cites (Definition, Proposition, Theorem, Lemma, Remark, Fact...) appears in its lesson",
    "course/modules/M/M3/cards.json vs L01..L09.html", "PASS",
    f"{O}/cards_numbers.out: 191 citations checked, 0 missing (including 'Definition 1.2a' in L09 for M3-c204 and 'Proposition 1.1' in L08 for M3-c131).")
row("cards-c131", "M3-c131 (reworded): agrees with L08 Proposition 1.1 and its proof", "course/modules/M/M3/cards.json M3-c131", "PASS",
    "Front: symmetric and PSD of M = X~^T X~/(T-1) for T x n X with T >= 2. Back: x^T M x = ||X~ x||^2/(T-1) >= 0 (L08 Proposition 1.1 proof). Grade T. Correct.")
row("cards-c204", "M3-c204 (new, L09): not a duplicate of an existing card and agrees with the lesson", "course/modules/M/M3/cards.json M3-c204 vs M3-c101", "FAIL",
    "Content agrees with L09 Definition 1.2a. But M3-c101 (L06): 'What is an orthogonal matrix? ... Q^T Q = I (Definition 1.1)' asks the same definition; the new card restates it with Q^T Q = Q Q^T = I. Also the definition appears twice in M3 (L06 Definition 1.1 and L09 Definition 1.2a). Rule 10: no duplicate cards.",
    "Remove M3-c204, or replace it with a non-duplicate question, e.g. 'For a square Q, does Q^T Q = I alone imply Q Q^T = I?' answered from L06 Fact 1.2. Consider one definition of orthogonal matrix in M3.")
for lid, rng in [("L01", "M3-c001..c022, c169, c170"), ("L02", "M3-c023..c042, c184, c187"), ("L03", "M3-c043..c062, c171, c172, c188"),
                 ("L04", "M3-c063..c078, c189, c190, c192"), ("L05", "M3-c079..c100, c173, c176, c179, c180, c193, c203"),
                 ("L06", "M3-c101..c114, c178"), ("L07", "M3-c115..c129, c168, c177, c194..c196")]:
    row(f"cards-{lid}", f"cards of {lid} agree with the lesson, carry hypotheses, no duplicates ({rng})", f"course/modules/M/M3/cards.json ({lid} entries)", "PASS",
        card_carry + " lesson " + lid + ".html byte-identical since d0f39c0; cited labels resolved (cards-numbers-cited).")
row("cards-L08", "cards of L08 agree with the lesson (M3-c130..c145, c174, c186, c197..c201)", "course/modules/M/M3/cards.json (L08 entries)", "PASS",
    "M3-c131 re-verified against Proposition 1.1 (cards-c131). Others: identical to d0f39c0 (JSON comparison); lesson text changed by the macro substitution only (prose-L08).")
row("cards-L09", "cards of L09 agree with the lesson, no duplicates (M3-c146..c167, c175, c181..c183, c185, c202, c204)", "course/modules/M/M3/cards.json (L09 entries)", "FAIL",
    "M3-c204 (added this round) duplicates M3-c101; see cards-c204. The other L09 cards are identical to d0f39c0 and agree with the unchanged L09 text.",
    "Fix cards-c204; the other 28 L09 cards need no change.")

# ---- registry/freshness flags & notes
registry_flags = [
    "L09 uses C^{\\ast} twice for the nearest correlation matrix (course/modules/M/M3/L09.html). The starred registry symbols R^\\ast, x^\\ast and R^{e\\ast} carry other meanings; C^\\ast is not registered. PASS with a recommendation to write \\hat C.",
    "\\mathbb{C} is used in L04 (3 times) and L06 (once) and is not a registered macro; not a registry symbol, so not a conflict. Consider a NOTATION_REQUESTS entry for \\C for consistency with \\R."
]
freshness_flags = []

summary = ("M3-d round 2 on pin c737272: verdict FAIL. Rows: %d total, %d PASS, %d FAIL. FAILs: (1) grader does not enforce the page's 'Standard library only' (v2d_06 survives, mutant kept in mutants/); "
           "(2) only three of the six alternatives obey the stated constraint (alt1, alt3, alt6 use NumPy), so the five-correct-alternatives requirement is not met, and the NumPy question conflicts with binding plan Q3; "
           "(3) M3-c204 is a duplicate of M3-c101 (and makes L09's card row FAIL). Round-1 FAILs resolved: dag-m4-concepts-by-name (ruling 3), cards-id-sequence (ruling 2), equivalent-r15d-m03-label (renamed, label and README consistent).")

notes = (
    "Round 2 on pin c737272. Delta since round-1 pin d0f39c0 (git diff, read in full in ledgers/M3/scripts/M3-d-r2/out/m3_course_diff.txt and equiv.txt): "
    "course/modules/M/M3/L06.html, L07.html, L08.html (\\mathbb{R} to \\R only, verified by normalisation); cards.json (M3-c131 reworded, M3-c204 added); project.html (two hunks: the 'conventions' link and the Lab 1 memo sentence about A2); "
    "ledgers/M3/equivalent/README.md and the r15d file (renamed and rewritten); ledgers/M3/mutants (vd1_01..05 present in this pin). Grader, alternatives, twins (tests/labs/M3), notation.json, references and tools for M3 are byte-identical to d0f39c0 (git diff empty). "
    "Other-unit changes in the range (FC1 curriculum brief, program.json, CS2, E3, E5, M2, M4 pages, tools) do not touch M3 and were not re-verified. "
    "Previous non-PASS rows: dag-m4-concepts-by-name re-verified against ruling 3 (PASS); cards-id-sequence against ruling 2 (PASS); equivalent-r15d-m03-label re-verified (PASS). "
    "Round-1 PASS rows carried only where the subject is byte-identical (grader, prose L01-L05, L09, cards per entry). Re-verified: changed subjects (project.html hunks, L06-L08 deltas, cards c131/c204, README, r15d, mutants list, alternatives count). "
    "Commands run by this verifier: check_pages, check_dag, check_projects, run_graders 0-49, run_labs, page_smoke for project, L01..L09 and index, ruff check and format, mypy --no-incremental, verify_refs --offline, collect-only, mutate_graders --unit M3 --seeds 0-9 (134 files), alternatives/reference/starter/equivalents on seeds 0-49, the three project twins under python -I -W error, pytest for test_page_checks, test_labs and test_run_labs filtered. "
    "NOT CHECKED: the full line-by-line re-read of the 9 lesson pages this round (carried or macro-verified as above); the 204-card text read in full this round (carried per entry with JSON comparison plus the citation scan); the exemplar scores were not independently re-scored (consistency only); render_curriculum, build_site --check, fetch_data --check and the whole pytest suite were not run (no input of M3 changed); verify_refs live was not run. "
    "The 'Standard library only' and NumPy question needs an architect decision (plan M3 section 10 Q3 says 'NumPy yes'). The reference.py docstring line 4 is ungrammatical (not learner text). "
    "The reference-deployment rule (ruling 4) is not applied. Mutant survivor v2d_06 is left in mutants/ on purpose as the finding."
)

fragment = {
    "unit": "M3",
    "slice": "M3-d",
    "round": 2,
    "verifier": "Claude Haiku 5.5, independent verifier for M3-d, round 2 (did not build M3; share no context with the builders; round-1 fragment used as context only)",
    "pin": "c737272f5bdef4a027417989cd52254555e8a0bb",
    "base": "d0f39c0 (round-1 pin); delta read in full: L06/L07/L08 macro-only, cards.json c131 reworded and c204 added, project.html two hunks, equivalent/ README and r15d renamed/rewritten, mutants vd1_01..05 present",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD2-M3-d",
    "scratch": "ledgers/M3/scripts/M3-d-r2/",
    "verified_at": "2026-11-02T00:00:00+00:00",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": registry_flags,
    "freshness_flags": freshness_flags,
    "notes": notes,
    "summary": summary % (len(rows), sum(1 for r in rows if r["status"] == "PASS"), sum(1 for r in rows if r["status"] != "PASS")),
}

import glob, os
mut_dir = "ledgers/M3/mutants"
killed_lines = {}
for line in open("ledgers/M3/scripts/M3-d-r2/out/mutate_M3_all_seeds0-9_after_v2d.out", encoding="utf-8"):
    if line.startswith(("KILLED ", "SURVIVED ")):
        name = line.split(":", 1)[0].split(" ", 1)[1].strip()
        killer = line.split("-> ", 1)[1].strip() if "-> " in line else None
        killed_lines[name] = (line.startswith("KILLED"), killer, line.split(":", 1)[1].split(" -> ")[0].strip())
mutants = []
for path in sorted(glob.glob(f"{mut_dir}/*.py")):
    name = os.path.basename(path)
    if name.startswith("v2d_"):
        ok, killer, desc = killed_lines[name]
        mutants.append({"id": name[:-3], "description": desc, "file": path, "killed_by": killer if ok else "",
                        "note": "round-2 new student-error mutant" if name.startswith("v2d_0") and name != "v2d_06_eigh_uses_numpy_not_standard_library.py" else "round-2 mutant: survivor (see row mutants-v2d-06)"})
    else:
        if name in killed_lines:
            ok, killer, desc = killed_lines[name]
            mutants.append({"id": name[:-3], "description": desc, "file": path, "killed_by": killer if ok else ""})
        else:
            raise SystemExit("missing killer line for " + name)
fragment["mutants"] = mutants
fragment["summary"] += " Mutants: %d files in ledgers/M3/mutants/ (128 pre-existing and vd1, plus six round-2 files); 133 killed on seed 0; v2d_06 survives (no killed_by)." % len(mutants)

with open("ledgers/M3/M3-d.json", "w", encoding="utf-8") as fh:
    json.dump(fragment, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), "mutants", len(mutants))
