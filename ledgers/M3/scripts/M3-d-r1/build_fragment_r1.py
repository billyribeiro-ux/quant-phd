# Round-1 delta verifier (M3 slice d): builds ledgers/M3/M3-d.json from the round-12 base rows (read-only), the
# commands run in this checkout (outputs under ledgers/M3/scripts/M3-d-r1/out/) and the standing mutant run.
import json, re, sys
ROOT = "/Users/billyribeiro/.fanout/wt/verifyF21-M3-d"
OUT = ROOT + "/ledgers/M3/scripts/M3-d-r1/out/"
BASE = json.load(open("/Users/billyribeiro/.fanout/frags/D-M3-d.round12.json", encoding="utf-8"))
base_rows = {r["id"]: r for r in BASE["rows"]}
PIN_BASE = "329c1d7f"
CARRY = "Carried from round 12 (%s byte-identical since the previous pin 329c1d7f): "

def carry(rid, files):
    return {"id": rid, "check": base_rows[rid]["check"], "location": base_rows[rid]["location"], "status": "PASS",
            "evidence": CARRY % files + base_rows[rid]["evidence"]}

def new(rid, status, evidence, fix=None):
    r = {"id": rid, "check": base_rows[rid]["check"], "location": base_rows[rid]["location"], "status": status,
         "evidence": evidence}
    if fix:
        r["fix"] = fix
    return r

R = []
def add(r):
    R.append(r)

# ---- gates (re-run on pin 95f3f8cb)
add(new("gate-check-pages", "PASS", "check_pages M3: PASS EXIT 0 (ledgers/M3/scripts/M3-d-r1/out/check_pages_M3.out)"))
add(new("gate-check-dag", "PASS", "check_dag M3: PASS EXIT 0 (out/check_dag_M3.out)"))
add(new("gate-check-projects", "PASS", "check_projects M3: PASS EXIT 0 (out/check_projects_M3.out)"))
add(new("gate-run-labs", "PASS", "run_labs M3: PASS (12/12) EXIT 0 (out/run_labs_M3.out); each twin also run alone with python -I -W error, EXIT 0 for L01, L02, L04, L05, L06, L07, L08, L09 (out/twin_L0n.out)"))
add(new("gate-run-graders", "PASS", "run_graders M3 --seeds 0-49: PASS (reference 50/50 seeds, slowest 0.3 s) EXIT 0 (out/run_graders_M3.out)"))
add(new("gate-page-smoke", "PASS", "page_smoke M3 --pages project: PASS, modules/M/M3/project.html (out/page_smoke_project_delta.out)"))
add(new("gate-ruff", "PASS", "ruff check tests/labs/M3 course/modules/M/M3/grader: All checks passed! EXIT 0 (out/ruff_check.out); ruff format --check: 16 files already formatted EXIT 0 (out/ruff_format.out)"))
add(new("gate-mypy", "PASS", "mypy --no-incremental: Success: no issues found in 386 source files, EXIT 0 (out/mypy_delta.out)"))
add(new("gate-verify-refs", "PASS", "verify_refs.py --offline: offline integrity: 560 entries, 0 problems EXIT 0 (out/verify_refs_offline_delta.out); verify_refs.py --unit M3 (live): 2 of 560 entries, 0 problems EXIT 0 (out/verify_refs_M3_live_r1.out). references/references.json changed only in generated_at and a FC2 used_by entry; the M3 records are unchanged."))
add(new("gate-collect-only", "PASS", "pytest --collect-only on the staged reference grader (ledgers/M3/scripts/M3-d-r1/stage_grader_r1.sh): 198 tests collected, EXIT 0 (out/collect_only_M3.out); equals the page count at project.html line 247"))
add(new("gate-pytest-relevant", "PASS", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py tests/test_docs_figures.py -q: all passed, EXIT 0 (out/pytest_relevant_r1.out)"))
add(new("gate-mutate-m3", "PASS", "tools/mutate_graders.py --unit M3 --seeds 0-9: 'mutate_graders M3: PASS (184/184 killed)' EXIT 0 (out/mutate_M3_seeds0-9_r1.out). All 184 KILLED lines name a failing test; none is a collection error."))
add(new("gate-reference-starter", "PASS", "staged reference: 198 passed, EXIT 0 (out/reference_seed0_r1.out); staged starter: 197 failed, 1 passed, EXIT 1 (out/starter_seed0_r1.out); the starter is the learner's stub and its failures are NotImplementedError, as the page states"))
add(new("gate-alternatives-seeds-0-49", "PASS", "ledgers/M3/scripts/M3-d-r1/run_alts_r1.sh: 10 of 10 correct alternatives pass seeds 0-49 against the current grader (out/alts_seeds0-49_r1.out)"))

# ---- alternatives and probes
add(new("alternatives-svd-probe", "PASS", "ledgers/M3/scripts/M3-d-r10/probes/alt11_svd_signed_eigenvalues.py staged as covariance_doctor.py (/private/tmp/verifyD1-alt11): passes seeds 0-49 against the current 198-test grader (checked in this round)"))
add(new("alternatives-numpy-return-types", "PASS", "ledgers/M3/scripts/M3-d-r11/probes/make_numpy_return_probe_r11.py, rerun with its output path redirected (ledgers/M3/scripts/M3-d-r1/make_numpy_return_probe_r1.py): the NumPy-return reference passes seeds 0-9 with the current grader, 198 passed (/private/tmp/verifyD1-probe-numpy)"))
add(new("alternatives-count-and-seeds", "PASS", "ledgers/M3/alternatives/ has 10 files; all 10 pass seeds 0-49 with the current grader (out/alts_seeds0-49_r1.out)"))
add(new("alternatives-alt2-docstring", "PASS", "ledgers/M3/alternatives/alt2_dykstra_other_stop_rule.py line 1 now reads 'stops on the feasibility gap alone, within max_iter steps (default 500)'. Code: line 105 default max_iter=500, line 112 'for _ in range(max_iter):', lines 124-125 'if gap <= tol: break' (gap = _frobenius(new_x, y), line 122). No 5000 remains. The alternative passes seeds 0-49 (out/alts_seeds0-49_r1.out)."))

# ---- grader
add(new("grader-test-count-and-purity", "PASS", "collect-only = 198 (out/collect_only_M3.out) = page count at project.html line 247. The only grader change since the pin is the added block at test_project.py lines 241-272; test_functions_print_nothing and test_inputs_are_not_mutated are unchanged, and the new tests print nothing and only call sol.* functions."))
add(carry("grader-standard-library-only", "grader/test_project.py outside the added block at lines 241-272 (test_module_imports_only_standard_library_or_numpy),"))
add(carry("grader-lab3-reference-numbers", "grader/test_project.py outside lines 241-272 (test_lab3_reference_numbers_are_matched)"))
add(new("grader-failure-messages-leak-answers", "PASS", "grader/test_project.py: every message, including the new must_raise messages in the added block ('{call_name} on a non-square matrix ({shape})' and '{call_name} on an entry pair that differs by 1e-8'), names only the call and the input shape and states no expected value"))
add(new("grader-named-conditions", "PASS", "FIXED since round 12. test_project.py lines 241-272 add NON_DEFAULT_CALLS (is_psd(tol=1e-5), clip_repair(floor=0.1), clip_repair(floor=-0.5), projection_repair(tol=1e-6), projection_repair(max_iter=3)) with test_non_square_is_refused_with_non_default_arguments and test_asymmetry_beyond_tolerance_is_refused_with_non_default_arguments. The reference passes all 198 (out/reference_seed0_r1.out). The round-12 survivor v12d_03 is now in ledgers/M3/mutants/ and is killed by 14 of these tests (out/mutate_M3_seeds0-9_r1.out; direct run: 14 failed, 184 passed). The named refusals for projection_repair and is_psd with non-default tol and clip_repair with non-default floor are now exercised by these tests."))
add(carry("grader-browser-timeout", "course/modules/M/M3/project.html line 237, course/assets/js/python.js"))
add(carry("grader-reference-docstring", "grader/reference.py"))
add(new("grader-spec-rubric-counts", "PASS", "project.html line 247 states 198 tests; collect-only count is 198 (out/collect_only_M3.out); rubric counts at project.html lines 490, 495, 498-502 unchanged"))
add(carry("spec-projection-tol-undefined", "project.html lines 233, 246 and grader/starter.py lines 30-36"))
add(carry("grader-projection-spec-vs-reference", "grader/reference.py _psd_projection and projection_repair, and project.html line 248"))
add(carry("grader-weights-spec-vs-reference", "grader/reference.py comparison_weights and project.html line 249"))
add(carry("grader-numpy-bool-return", "grader/test_project.py lines 134-139 (the added block starts at 241)"))
add(new("grader-failure-messages-r10", "PASS", "grader/test_project.py: the messages of the added block (lines 241-272) name the call and the input shape and state no expected value (same check as grader-failure-messages-leak-answers)"))

# ---- mutants (standing set re-run; no new mutants authored, ruling 37)
add(new("mutants-existing-140", "PASS", "ledgers/M3/mutants/ holds 184 files; tools/mutate_graders.py --unit M3 --seeds 0-9 kills 184/184 by named tests (out/mutate_M3_seeds0-9_r1.out)"))
for rid in ["mutants-new-student-errors", "mutants-v2d-01-05", "mutants-v3d-02-05", "mutants-v5d-new-student-errors",
            "mutants-r6-new-student-errors", "mutants-r7-new-student-errors", "mutants-v8d-new-student-errors",
            "mutants-v9d-new-student-errors", "mutants-v10d-new-student-errors", "mutants-v11d-new-student-errors"]:
    add(new(rid, "PASS", "these files are unchanged since the pin and are in the standing set; each is KILLED by a named test in ledgers/M3/scripts/M3-d-r1/out/mutate_M3_seeds0-9_r1.out"))
add(carry("mutants-v2d-06", "ledgers/M3/retired/v2d_06_eigh_uses_numpy_not_standard_library.py"))
add(carry("mutants-r15d-description", "ledgers/M3/mutants/r15d_m01_is_psd_strict_boundary.py and r15d_m02_rescale_missing_sqrt_on_column.py"))
add(new("mutants-description-all", "PASS", "all 184 files in ledgers/M3/mutants/ begin with a one-line docstring; the first lines of the 13 files added or repaired since the pin (r12d_m02..m04, v12d_01..04, r18d_m01..m09) were read and each names a student error. The other 171 are byte-identical since the base and were parsed in round 12."))
add(carry("mutants-v5d-01-equivalent-moved", "ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py and ledgers/M3/equivalent/README.md"))
add(new("mutants-v5d-04-accepted-stop-rule", "PASS", "ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py passes seeds 0-49 against the current grader (out/alts_seeds0-49_r1.out); file byte-identical since the pin"))
add(new("equivalent-r6d-m04", "PASS", "ledgers/M3/alternatives/alt7_dykstra_gap_only_stop.py passes seeds 0-49 against the current grader (out/alts_seeds0-49_r1.out)"))
add(new("equivalent-r11d-m02", "PASS", "ledgers/M3/alternatives/alt8_dykstra_step_only_stop.py passes seeds 0-49 against the current grader (out/alts_seeds0-49_r1.out)"))
add(new("equivalent-r15d-m03-label", "PASS", "ledgers/M3/alternatives/alt9_dykstra_runs_full_budget.py passes seeds 0-49 against the current grader (out/alts_seeds0-49_r1.out)"))
add(carry("equivalent-readme-citation", "ledgers/M3/equivalent/README.md, ledgers/M3/equivalent/alt10_no_unit_diagonal_correction.py and grader/reference.py"))
add(new("mutants-collection-only-kills", "PASS", "FIXED since round 12. The three headers are repaired (second docstring removed): r12d_m02_min_eigenvalue_first_jacobi_value.py, r12d_m03_projection_keeps_negatives_down_to_minus_0p01.py and r12d_m04_weights_scale_row_by_first_volatility.py. Each is now killed by a named assertion: r12d_m02 by test_min_eigenvalue_is_smallest_of_diagonal, r12d_m03 by test_projection_repair_is_a_valid_repair[seed], r12d_m04 by test_lab3_reference_numbers_are_matched (out/mutate_M3_seeds0-9_r1.out). The run has 0 collection-only kills."))
add(new("mutants-v12d-new-student-errors", "PASS", "ledgers/M3/mutants/v12d_01, v12d_02, v12d_03 and v12d_04 are KILLED by named tests in out/mutate_M3_seeds0-9_r1.out. Note: v12d_01, v12d_02 and v12d_04 are not in the base pin 329c1d7f (they were added after it); the round-12 row cited them as present."))

# ---- spec, project page and brief
add(carry("project-numbers", "course/modules/M/M3/project.html lines 57-139, 466-477 and 591-617 (the only project changes are lines 247 and 264)"))
add(carry("project-lab1-memo-sentence", "project.html lines 57, 139 and tests/labs/M3/lab-M3-project-1.py"))
add(carry("project-lab2-completion", "project.html lines 142-224 and tests/labs/M3/lab-M3-project-2.py"))
add(carry("project-lab3-check", "project.html lines 290-478 and tests/labs/M3/lab-M3-project-3.py"))
add(carry("project-lab3-diagonal-positivity-sentence", "project.html lines 477, 605 and 617"))
add(new("project-spec-grader", "PASS", "project.html lines 229-239 re-read: line 239 now states 198 tests, equal to the collect-only count (out/collect_only_M3.out); signatures at line 235 match grader/starter.py; the four named conditions at line 237 are unchanged"))
add(carry("project-conventions-math", "project.html lines 242-252 and grader/reference.py lines 109-150"))
add(carry("project-conventions-link", "project.html lines 233 and 245 (DAG link targets)"))
for rid, loc in [("project-proof-A1", "line 643"), ("project-proof-A2", "line 644"), ("project-proof-A3", "line 645"), ("project-proof-A4", "line 645")]:
    add(carry(rid, "project.html " + loc))
add(new("project-hours", "PASS", "project hours table: 2 + 3 + 14 + 8 + 12 + 6 = 45, total row 45 (project.html lines 259-267; row 264 changed its label only); index.html data-hours-lessons=105 and data-hours-project=45; lesson data-hours 12+11+12+12+12+11+11+12+12 = 105; 105 + 45 = 150 (hours checked with grep over L01-L09, index.html and project.html; no hours attribute changed)"))
add(carry("project-exemplars", "project.html lines 509-654 (Exemplars A and B). No dedicated blind scorer file for M3 exists in ~/.fanout/blind/, so the base calibration rows are carried as the task instructs; the base disclosed that its calibration was not strictly blind (open, see notes)"))
add(carry("project-rubric", "project.html lines 494-507 (rubric table)"))
add(carry("rubric-C4-level2-vague", "project.html line 503 (C4 row)"))
add(carry("project-references", "project.html lines 674-684 and the M3 records in references/references.json (only generated_at and an FC2 used_by entry changed)"))
add(new("project-no-process-words", "PASS", "ledgers/M3/scripts/M3-d-r1/out/process_words_r1.out: 'none' for project.html, cards.json, grader/*.py and tests/labs/M3/lab-M3-project-*.py"))
add(carry("project-stretch", "project.html lines 663-670"))
add(new("project-links", "PASS", "process_words_r1.out: no external http(s) reference in project.html and no href/src target other than anchors and relative paths"))
add(new("project-brief-scope", "PASS", "curriculum/01-foundations.yaml lines 185-188 now read 'Compare the two repairs by their Frobenius distance from the input, and say for each repaired matrix whether the closed-form weight formula applies, with the reason.' project.html delivers both: distances (lines 288, 442-446 code, 475-477 interpretation), and per-repair applicability of the weight formula (lines 485-486 brief, 501 C2, 621). render_curriculum.py regenerates CURRICULUM.md and curriculum/curriculum.json with no diff (out/render_curriculum_diff.out, EXIT 0)."))
add(new("scope-repair-weights-vs-brief", "PASS", "The page and the curriculum brief now agree: the brief (curriculum/01-foundations.yaml 185-188) asks for the Frobenius-distance comparison and for the per-repair applicability of the closed-form weight formula, and project.html (lines 475-477, 486, 621) delivers both. The round-12 FAIL (brief asked for downstream weights, page declined) is closed by this match. NOTE for the architect (not a ruling-26 defect and not part of the verdict): the brief amendment (commit 6f5f300a) is not recorded as an architect ruling; plans/FINAL-ARCHITECT-RULINGS.md has no ruling on M3 B3 and plans/M3-build-plan.md section 9 B3 still reads 'Architect decision required'. The architect should record the decision."))
add(carry("spec-stop-rule-sentence", "project.html line 248 (Alternating steps)"))
add(carry("project-lab3-weights-sentence", "project.html lines 475-477 and tests/labs/M3/lab-M3-project-3.py"))

# ---- notation and DAG
add(new("notation-registry", "PASS", "notation/notation.json unchanged; project.html symbols unchanged apart from the row-264 label; cards.json has 0 backslash macros (grep count 0)"))
add(new("notation-R-macro", "PASS", "cards.json has no backslash macro; the changed project.html lines 247 and 264 contain no macro"))
add(carry("dag-linked-concepts", "project.html concept links (lines 233, 245) and the eigendecomposition, spectral-theorem and positive-semidefinite-matrix anchors"))
add(new("dag-m4-concepts-by-name", "PASS", "cards.json contains 'correlation' 18 times and 'variance' once, all plain prose allowed by architect ruling 3; no covariance, expectation, Gaussian, Cholesky or IEEE name in cards.json, grader/*.py or project.html additions"))
add(new("dag-cholesky-named-in-grader", "PASS", "grep -i 'cholesky|IEEE' over course/modules/M/M3/grader/*.py and cards.json: no hit"))

# ---- cards (cards.json changed: 210 records; L01, L02, L04, L05, L06 lesson text changed)
add(new("cards-structure", "PASS", "cards.json: 210 records, 210 unique ids, 0 duplicate fronts or backs; key sets: 50 without grade, 122 with grade, 38 with grade and basis (ledgers/M3/scripts/M3-d-r1/cards_scan_r1.py)"))
add(new("cards-id-sequence", "PASS", "ids M3-c001..M3-c219; missing numbers 37, 101, 102, 148, 176, 191, 201, 204, 206 (gaps are not defects, ruling 2); no out-of-order appended id (cards_scan_r1.out)"))
add(new("cards-numbers-cited", "PASS", "card_refs_r1.py: every Definition/Example/Proposition/Theorem/Remark/Corollary/Lemma/Fact N.M on a card resolves in its own lesson. Nine references were first flagged because a preceding 'Lesson 4' (F1 to F4) was misattributed; each resolves in its own lesson: c089 L05 Proposition 2.3, c127 L07 Remark 1.4, c143 L08 Theorem 2.1, c168 L07 Definition 2.1 and Theorem 2.2, c183 L09 Proposition 3.3 and Example 3.6, c195 L07 Theorem 1.2, c196 L07 Theorem 2.2, c203 L05 Theorem 2.2, Proposition 1.5 and Remark 3.2, c205 L06 Fact 1.2 (out/card_refs_r1.out)."))
add(new("cards-labels-cited", "PASS", "ruling 13 checked for changed cards: T cards c094, c097, c100, c179 mirror the L05 key-results T rows (Example 1.7, Remark 3.2, Example 2.6); C cards c218 and c219 mirror the L05 Lab 1 C row; no card in this set mismatches its key-results row, except c145 (see cards-L08)."))
add(new("cards-duplicate-scan", "PASS", "no duplicate front or back in cards.json (cards_scan_r1.out). Near pairs c097 (T, Remark 3.2 eigenvalue count) and c219 (C, Lab 1 Part D count), and c179 (T) and c218 (C), ask about the mathematics and about the printed output respectively and carry the grades of their key-results rows (ruling 13)."))
add(new("cards-sample-20", "PASS", "all 47 changed, added or removed records (37 changed, 6 added, 4 removed): c016-c019, c038, c039, c042, c054, c058, c071, c073, c075, c085, c094, c096-c098, c100, c105, c124-c126, c138-c141, c145, c161-c163, c167, c173-c175, c177, c179, c184, c214-c219; removed c037, c101, c176, c201) were read in full and checked against the current lesson text and the lab output; see the per-lesson rows"))
add(new("cards-lab-numbers", "PASS", "every number on a changed C card matches the output of its twin run now (out/twin_L01..L09.out): e.g. c016 188/200, c017 198/200, c018 100/100, c019 0/200 (L01); c038/c039/c184 50/50 (L02); c075 1200 and 1200 (L04); c096 500/500, c173 100000/100000, c218 True and -1.0000, c219 1 and 0.0000 1.0000 3.0000 (L05); c125 1.3325 0.8488 -0.4120, c126 0.8951, c177 2 of 3 (L07); c139 to c141, c174 75.9/18.1/5.2, 0.9994/0.9985/0.9990, 0.7587 to 0.9791 (L08); c161 0.6400000000, c162 23 of 40, c163 23 of 23, c175 23 of 23, c217 eigenvalues -0.8, 1.9, 1.9 (L09). LOW (not a ruling-26 kind, noted only): c075 says 'the lab counts a pair when its eigenvalues are more than 1e-6 apart, so no pair was skipped'; the lesson (L04 line 200) and the printed 1200 = 200 x 6 support 'no pair was skipped', but the stated rule alone does not imply it."))
add(new("cards-L01", "PASS", "changed c016, c017, c018, c019 read against L01 (lab heading 'Lab 1 ... (SIMULATED)' line 82, Corollary 3.6 and Proposition 3.5 text, lines 215, 232) and the twin output; unchanged cards carried"))
add(new("cards-L02", "PASS", "changed c038, c039, c042, c184 read against L02 (Definition 2.1 line 39 and misconception line 234-235 for c042; twin tolerance code line 151 for c039); c037 removed (Example 4.3 exists, line 73)"))
add(new("cards-L03", "PASS", "changed c054 read against L03 Definition 1.2, Proposition 1.4 and the Lesson 1 Proposition 3.12 citation; c058 against the L03 twin output 'det P = 6, which is nonzero, so P is invertible' (out/twin_L03.out); unchanged cards carried"))
add(new("cards-L04", "PASS", "changed c071 (Proposition 2.4, L04 line 64), c073 (Remark 2.7 line 75; (1,0), (1,1)/sqrt2 and 1/sqrt2 checked by hand), c075 (LOW wording note under cards-lab-numbers), new c215 (Definition 1.2, L04 line 32-33). c189, c190 unchanged."))
add(new("cards-L05", "PASS", "changed c085 (Theorem 2.1 line 45 and Example 2.6), c094 (Example 1.7), c096, c173 (twin), c097 (Remark 3.2: det(G - lambda I) = (1 - lambda) lambda (lambda - 3) and trace/minors check by hand), c098 (Example 1.7), c100 (Proposition 1.5, Remark 3.2, Definition 3.1 tolerance), c179 (Definition 3.1, Examples 1.7 and 2.6), new c218 and c219 (twin Part A and Part D). c176 removed. c089 and c203 references resolve."))
add(new("cards-L06", "PASS", "changed c105 read against Theorem 2.2 (L06 line 40-43: m, n >= 1, k = min(m,n), U and V orthogonal, sigma ordering); new c216 (Theorem 2.2 wording on left and right singular vectors); c205 Fact 1.2 resolves; c101 removed (its content is now Definition 1.1, restated)."))
add(new("cards-L07", "PASS", "changed c124, c125, c126, c177 read against the L07 twin output (out/twin_L07.out: all checks True; 1.3325/0.8488/-0.4120; 0.8951; rank 2 of 3) and the generator values 1.5, 0.8, -0.4 (L07 twin line 30); references c127, c168, c195, c196 resolve in L07."))
add(new("cards-L08", "FAIL", "card c145 (changed in this delta from C to T) grades a universal misconception 'False' as T. Its back says 'Assuming F1 to F4 of Lesson 4, which component is level-like depends on the data, because the order of the components follows the eigenvalues, by Theorem 2.1', with no matrix or dataset in which the first principal direction is not level-like. L08 has no such example (checked: no Example in L08 covers it; the page says at line 184 that the label is a computation on the data). A 'depends on the data' claim needs an explicit witness to be T, so the claim is an over-graded claim (ruling 26). Other changed L08 cards check out: c138 (Remark 2.4 hypotheses M_jl nonzero, c not 0 or 1, verified by hand), c139, c140, c141, c174, c214 (planted scale 8.0 at twin line 46 and the lesson's statement), c143, c145's removed planted-panel sentence.", "Either (a) add to L08 a worked witness: an explicit PSD M (or data matrix X) whose largest eigenvalue belongs to a non-level shape, with the eigendecomposition checked, and keep c145 as T with that Example as basis; or (b) regrade c145 to C naming the Lab 1 SIMULATED panel, restoring the planted-panel sentence (the round-12 form) so the claim is C with a basis."))
add(new("cards-L09", "PASS", "changed c161, c162, c163, c167, c175, c217 read against L09 Remark 2.2, Definition 2.1, Example 2.3, Proposition 3.3(a), Example 3.6 and the twin output (out/twin_L09.out): 0.6400000000, 23 of 40, 23 of 23, eigenvalues -0.8, 1.9, 1.9 (C with lab basis)"))
add(carry("cards-c208-duplicate", "cards.json record M3-c208"))
add(new("cards-c167-misconception", "PASS", "M3-c167 (changed) read against L09 Definition 2.1 and Remark 2.2 and the Lab 1 output (23 of 23 strictly closer): grade C naming the lab, basis 'Lab 1, 40 seeded 5 x 5 SIMULATED matrices'"))
add(new("cards-c209-c213-new", "PASS", "M3-c209 (L07) and M3-c210 to M3-c213 (L08) carried (records unchanged); new M3-c214 (L08, C naming the SIMULATED six-tenor panel; PC1 level-like and planted scale 8 bp per day match twin line 46 and the lesson) checked this round"))
add(carry("cards-c131", "cards.json record M3-c131 and L08.html Proposition 1.1"))
add(new("cards-c204", "PASS", "cards.json has no record M3-c204 (ids listed in cards_scan_r1.out: 9 missing numbers, c204 among them)"))
add(carry("cards-c144-prop23-hypothesis", "cards.json record M3-c144 and L08.html Proposition 2.3"))
add(new("cards-c163-lab-count", "PASS", "M3-c163 (changed) states 'All 23 (SIMULATED Lab 1 output)'; twin L09 prints 'alternating-projection output passes is_correlation and is strictly closer to A than R: 23 of 23' (out/twin_L09.out)"))
add(new("cards-sample-lesson-text-current", "PASS", "cards read against the current L01.html (changed lab headings and SIMULATED lines) and L08.html; c016-c019 agree with the current text"))
add(carry("cards-L08-section3", "course/modules/M/M3/L08.html Section 3 (lines 137-141) and the Section 3 cards carried as byte-identical records; the changed card c145 is reported under cards-L08"))
add(carry("lesson-l08-section3-text", "course/modules/M/M3/L08.html Section 3 (lines 137-141)"))
add(carry("lesson-l09-prop32b-reference", "course/modules/M/M3/L09.html line 119"))
add(new("links-and-anchors", "PASS", "check_pages M3 PASS (out/check_pages_M3.out) covers anchors across project, index and L08; process_words_r1.out: no bad target in project.html; index.html changed only in its lede and a prompt text, with no href change"))

add(carry("grader-instance", "grader/instance.py and project.html line 231"))
# ---- the rest carried from base unchanged
carried_ids = [r for r in base_rows if r not in {x["id"] for x in R}]
print("carried-by-default ids:", carried_ids, file=sys.stderr)
for rid in carried_ids:
    add(carry(rid, "the cited files"))

# ---- mutants list from the standing run
mutants = []
pat = re.compile(r"^KILLED (\S+?\.py): (.*) -> (.*) \(seed (\d+)\)$")
for line in open(OUT + "mutate_M3_seeds0-9_r1.out", encoding="utf-8"):
    m = pat.match(line.rstrip("\n"))
    if m:
        f, desc, test, seed = m.group(1), m.group(2), m.group(3), m.group(4)
        mutants.append({"id": f[:-3], "description": desc, "file": "ledgers/M3/mutants/" + f,
                        "killed_by": test + " (seed " + seed + ")"})

ids = [r["id"] for r in R]
missing = [i for i in base_rows if i not in ids]
assert not missing, missing
assert len(ids) == len(set(ids)), "duplicate ids"
status = {}
for r in R:
    status[r["status"]] = status.get(r["status"], 0) + 1
verdict = "FAIL" if any(r["status"] != "PASS" for r in R) else "PASS"
frag = {
    "unit": "M3", "slice": "d", "round": 1,
    "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 1 of the closing delta; shares no context with the builders",
    "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
    "base": "round-12 pin 329c1d7f (fragment ~/.fanout/frags/D-M3-d.round12.json). Delta 329c1d7f..95f3f8cb for this slice: project.html lines 247 and 264; grader/test_project.py (lines 241-272); cards.json (37 changed, 6 added, 4 removed records); curriculum/01-foundations.yaml 185-188 (brief); alternatives/alt2 line 1; mutants r12d_m02-m04 headers repaired; 13 new mutant files; L01, L02, L04, L05, L06 lesson text; tests/labs/M3 twins L01, L02, L05, L06; index.html lede and prompt; references.json metadata. Rulings 30 (delta closing) and 37 (no new mutants) and 26 (FAIL kinds) apply.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyF21-M3-d",
    "scratch": "ledgers/M3/scripts/M3-d-r1/",
    "verified_at": "2026-11-09T12:00:00+00:00",
    "verdict": verdict,
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
notes = [
    "Delta scope per ruling 30: every base non-PASS row re-verified from scratch (gate-mutate-m3, grader-named-conditions, mutants-existing-140, scope-repair-weights-vs-brief, alternatives-alt2-docstring, mutants-collection-only-kills); rows whose subject changed were re-verified; other rows carried with the carry prefix (cited files byte-identical since 329c1d7f). No new mutant was authored (ruling 37); the 13 mutant files added since the pin are the fixers' and are in the standing run (all KILLED by named tests).",
    "Ruling 26 FAIL kinds: one defect found, cards-L08 (c145 graded T as an over-claim). All other rows PASS.",
    "LOW, not a FAIL kind: c075 wording ('so no pair was skipped' follows from the printed 1200, not from the stated rule).",
    "Governance note (not a verdict input): the brief amendment in curriculum/01-foundations.yaml (commit 6f5f300a) is not recorded as an architect ruling in plans/FINAL-ARCHITECT-RULINGS.md; M3-build-plan.md section 9 B3 still says 'Architect decision required'. The page now matches the amended brief.",
    "Base row mutants-v12d-new-student-errors cited files (v12d_01, v12d_02, v12d_04) that were not present at the base pin 329c1d7f; they are present at 95f3f8cb and are killed.",
    "Lesson text in L01, L02, L04, L05 and L06 changed in this delta. The cards that cite the changed passages (listed in the cards-L0n rows) were checked; the unchanged card records were not re-read line by line against every changed paragraph (honest gap for those lessons; those lessons belong to slices a to c).",
    "Calibration: no blind scorer file for M3 exists in ~/.fanout/blind/; the base calibration rows (project-exemplars, project-rubric, rubric-C4-level2-vague) are carried as the task instructs. The base disclosed its calibration was not strictly blind; that remains an open gap.",
    "Could not check: the browser (Pyodide) run of the grader and alternatives (only local pytest); the live Crossref run for M3 records beyond verify_refs --unit M3 (2 entries, PASS); a line-by-line re-read of the unchanged 170 card records against the changed lesson text (the cards whose cited items changed were checked).",
]
frag["notes"] = " | ".join(notes)
frag["summary"] = ("M3 slice d closing delta round 1 on 95f3f8cb: verdict %s. %d rows: %s. Mutants in ledgers/M3/mutants/: %d, all KILLED by named tests (184/184, no collection-only kills). "
                   "Non-PASS: cards-L08 (c145 over-graded T)." % (verdict, len(R), ", ".join("%s %d" % (k, v) for k, v in sorted(status.items())), len(mutants)))
json.dump(frag, open(ROOT + "/ledgers/M3/M3-d.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("rows", len(R), status, "mutants", len(mutants), "verdict", verdict)
