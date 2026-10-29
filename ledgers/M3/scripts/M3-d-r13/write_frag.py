import json, pathlib, sys
sys.path.insert(0, "tools")
import ledger
CAR = "Carried from round 12 (course/modules/M/M3/ files and grader byte-identical since ff38842; the round-13 delta changed only project.html lines 37, 53, 231, 469, cards.json lines 1280 and 1287, and L07/L08/L09 hunks): "
R = []
def row(i, check, loc, status, ev):
    R.append({"id": f"M3-d-R{i:02d}", "check": check, "location": loc, "status": status, "evidence": ev})
row(1, "Lab 1 twin output equals page expected block; page code equals twin", "course/modules/M/M3/project.html lines 131-137; tests/labs/M3/lab-M3-project-1.py", "PASS",
    "Re-run this round: python -I -W error tests/labs/M3/lab-M3-project-1.py exit 0; its stdout equals the page block (lines 131-137 after tag stripping); run_labs M3 PASS (12/12). Lab 1 block not in the delta.")
row(2, "Lab 2 completion: blanks at Step 3 and Step 5; completed code and output match", "course/modules/M/M3/project.html Lab 2 block (lines 214-220); tests/labs/M3/lab-M3-project-2.py lines 50 and 58", "PASS",
    "Twin lines 50 and 58 contain 'smallest >= -1e-10' and 'rebuilt[i][j] / math.sqrt(d[i] * d[j])', the expected blanks. Run this round: verdict False, deviation 0.000000, PSD at 1e-9 True, matching the page text (blanks filled 'verdict False, deviation below 5e-7, passes at 1e-9').")
row(3, "Lab 3 printed numbers recomputed independently", "project.html lines 460-468; ledgers/M3/scripts/M3-d-r13/numbers_check.py + numbers_check.out", "PASS",
    "numpy: min eig -0.14211264; clip distance 0.176573, projection 0.175003, gap 0.001570; max entry diff 0.011516; diagonal deviations 0; projection min eig -3.5e-13; det -0.261600; weights 1.778929 -1.096718 -0.255613 0.573402 sum 1. Twin lab-M3-project-3 output equals the page block line for line.")
row(4, "Lab 3 hypothesis sentence (smallest eigenvalue negative; projection nearer by a positive distance; unit diagonal to 5e-7; det nonzero; weights sum to 1)", "project.html Lab 3 paragraph (line 289)", "PASS",
    "Re-computed (numbers_check.out): smallest eigenvalue -0.142113; projection distance 0.175003 < clipping 0.176573; diagonals exact; det -0.2616 nonzero; weights sum 1.0.")
row(5, "Lab 1 and Lab 2 interpretation prose numbers", "project.html interpretation paragraphs after Lab 1 and Lab 2", "PASS", CAR + "Lab 1 numbers (0.636095, -0.382551, 0.469578, rebuilt diagonal 1.096064/1.104409/1.074824) re-checked against the twin output this round.")
row(6, "Lab 3 interpretation prose (distance gap, entry gap, determinant, A4 hypothesis, Sigma invertibility)", "project.html line 469 (changed this delta: 'Σ formed from it')", "PASS",
    "Re-verified: gap 0.001570, entry difference 0.011516, det -0.2616, weights and sums; X det -1.8e-16 (clipped matrix singular, A4); Y has eigenvalue 2.8e-17 when its diagonal is positive (Y diagonal positive: 1.0); Lab 3 prints no diagonal of the clipped matrix, as the sentence says. det Sigma = (v1 v2 v3 v4)^2 det C is the standard identity for Sigma = S C S.")
row(7, "Spec constants: test count 153; PSD tolerances (-1e-9 clipping, -1e-8 projection); ValueError conditions", "project.html grading mode (line 237) and spec (line 243)", "PASS",
    "Re-run: pytest --collect-only -q test_project.py in a scratch copy = '153 tests collected'; reference 153 passed (ledgers/M3/scripts/M3-d-r13/collect.out, ref_run.out). Tolerance sentence: test file byte-identical since ff38842; the ValueError conditions match reference.py _as_matrix and comparison_weights.")
row(8, "Convention and appendix math: A1 (clipping PSD), A2 (rescaling gives unit diagonal and PSD), A3 (two assets), A4 (singularity)", "project.html conventions (lines 243-247) and Appendix A (line 481)", "PASS",
    "Re-derived: A1 eigenvalues of clipped matrix are max(lambda, f) >= 0; A2 x^T Y x = z^T X z with z = D^-1/2 x, Y_ii = 1; A3 Sigma = [[a^2, rho a b],[rho a b, b^2]] has inverse proportional to [[b^2, -rho a b],[-rho a b, a^2]], so iota^T Sigma^-1 ∝ (b(b-rho a), a(a-rho b)) with denominator a^2+b^2-2 rho a b; det Sigma = a^2 b^2 (1-rho^2) != 0 needs |rho|<1 (raw HTML shows '|\\rho| < 1' and 'a, b > 0'); scaling by c cancels. A4 det X = 0 when a floor-0 eigenvalue is clipped, and det Y = det X / prod d_i = 0.")
row(9, "Rubric row C1 and exemplar scores", "project.html rubric table (C1 row, line 492) and exemplar A/B score lines", "PASS", CAR + "Rubric and exemplar text read in full this round; C1 wording consistent with A1/A2 as proved.")
row(10, "Exemplar A and exemplar B passages and annotations", "project.html exemplar passages", "PASS", CAR + "Exemplar A weights 1.78, -1.10, -0.26, 0.57 sum to 0.99 when rounded (checked); exemplar B figures -0.142113, 0.176573, 0.175003, 0.001570 equal the printed Lab 3 values.")
row(11, "Hours: hub split and lesson hours arithmetic", "project.html time-budget table; course/modules/M/M3/index.html line 42 ('105 h lessons · 45 h project (30%)')", "PASS",
    "Re-summed this round: 2+3+14+8+12+6 = 45 (the project total row); 105 + 45 = 150 matches the hub's '150 hours'. Rungs 1-2 (2 h + 3 h) match the page's rung text.")
row(12, "Reference solution passes the suite on 50 seeds; collect count", "course/modules/M/M3/grader/reference.py; tools/run_graders.py --unit M3", "PASS",
    "Re-run this round: run_graders M3 PASS (reference 50/50 seeds); copy-in-scratch pytest 153 passed with -W error (ref_run.out).")
row(13, "Stopping-rule survivor r6d_m04: is it a violation of a stated behaviour?", "ledgers/M3/mutants/r6d_m04_projection_stops_on_gap_only.py", "PASS",
    CAR + "Re-run this round: SURVIVED 50/50 (mutate_graders output mutate_m3_r13.out). Ruled not a violation: the spec says 'an approximation of the nearest' and states no stop rule; the output is still a PSD unit-diagonal matrix (the grader's valid-repair and no-farther tests pass).")
row(14, "Six alternative correct implementations pass 50 seeds", "ledgers/M3/alternatives/ and this round's /tmp alternatives (ledgers/M3/scripts/M3-d-r13/make_alts.py, alts_run.out)", "PASS",
    "Re-run this round on the current grader: alt1 (200 sweeps, tight cutoff), alt2 (is_psd negated comparison), alt3 (separate square roots in rescaling), alt4 (projection max_iter 2000), alt5 (no pivoting in weights), alt6 (floor via max over -inf): each pass=50 fail=0. The reference copy also passes 50/50 under the same runner (run_alts.sh control).")
row(15, "Mutants: every existing mutant is killed or ruled; kill records are accurate", "ledgers/M3/mutants (112 files); tools/mutate_graders.py --unit M3 --seeds 0-49 (mutate_m3_r13.out)", "PASS",
    "Round-12 defect cleared: the three projection stale copies (r6d_m04, r9d_m02, r11d_m02) are now reported SURVIVED, not KILLED, so the kill records are no longer spurious. All 108 kills are real kills. The gate's exit status is covered by row M3-d-R40.")
row(16, "Docstrings and spec for comparison_weights and projection; weight formula consistent with the page", "course/modules/M/M3/grader/reference.py comparison_weights docstring", "PASS", CAR + "reference.py unchanged; matches the page's weight formula and the closed form re-derived in row R08.")
row(17, "Grader tests on the page's 'what the suite checks' claims", "course/modules/M/M3/grader/test_project.py lines 241-245, 319-326, 508", "PASS", CAR + "test_project.py byte-identical; 153 tests collected and passing (row R07).")
row(18, "Notation: symbols on the changed page vs notation/notation.json", "project.html changed lines 37, 53, 231, 469; notation/notation.json (8 symbols)", "PASS",
    "Re-checked this round. Symbols used on the M3 project: rho, Sigma, Lambda, iota, S, C, D, V, X, Y, f, A, v. The registry lists T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}; none is used with another meaning on these pages.")
row(19, "DAG and concept links from the page", "project.html line 53 (eigendecomposition and spectral-theorem links) and line 243", "PASS", "Re-run this round: check_dag.py --all reports M3 PASS. Lessons 3-5 and 7-9 named on the page are inside the module's prerequisite closure.")
row(20, "Structure gates: check_pages, check_dag, check_projects, page_smoke", "tools/check_pages.py, check_dag.py, check_projects.py, page_smoke.py --unit M3", "PASS",
    "Re-run this round: check_pages M3 PASS; check_dag M3 PASS; check_projects M3 PASS; page_smoke M3 PASS (index, concepts, review and M3 pages).")
row(21, "cards.json structure: unique ids, lesson names, cites, every lesson has cards", "course/modules/M/M3/cards.json (184 cards)", "PASS",
    "Re-run this round: 184 cards; no duplicate ids; no duplicate fronts.")
row(22, "Changed and carried cards: content matches the current lesson", "course/modules/M/M3/cards.json lines 1280 (M3-c183) and 1287 (M3-c184); carried cards c038, c040, c093, c138, c160", "PASS",
    "M3-c183 (L09): front 'squared Frobenius distance' = 0.04 matches L09 line 180 and Example 3.6; 'Assuming F1 to F4 of Lesson 4' matches the new L09 wording (L04 lines 56-62 define F1 to F4 as numbered assumptions). M3-c184 (L02): '50 of 50' matches L02 line 183 and lab output line 4. c038, c040, c093, c138, c160 are unchanged since ff38842 (diff shows only lines 1280 and 1287); c138 still matches the Remark 2.4 claim.")
row(23, "Grade C cards carry a basis or cite; grade rules", "course/modules/M/M3/cards.json (C cards incl. M3-c038, M3-c184)", "PASS", CAR + "C-graded cards c038 and c184 state their basis ('Lab 1 output', 'Proposition 3.1 predicts').")
row(24, "Lesson hunks cited by changed cards agree with the card text", "L09 lines 180, 342; L02 line 183; L08 Proposition 2.3 proof (remark 2.4 claim)", "PASS",
    "Re-read this round: the changed L08 proof of Proposition 2.3 now shows M_jj >= 0 from x = e_j and M_jj != 0 by the sign argument; the claim on the card M3-c138 (no single kappa; shares can change; Remark 2.4) is unchanged. L09 and L02 hunks re-read against cards c183 and c184.")
row(25, "Reading list and references: registry keys exist and verify offline", "course/modules/M/M3/project.html reading section; references/references.json", "PASS", CAR + "verify_refs.py --offline re-run this round: 560 entries, 0 problems.")
row(26, "Lede and conventions prose numbers and claims", "project.html line 37 (lede, changed this delta); Conventions section", "PASS",
    "Re-read this round: 'the weight formula (defined in the conventions)' resolves to the 'Weights.' bullet of the Conventions section; the unit diagonal and PSD links resolve to the same section. No numbers in the changed sentence.")
row(27, "Lab 3 expected block equals twin output", "project.html lines 460-468; tests/labs/M3/lab-M3-project-3.py", "PASS", "Re-run this round: twin output equals the page block line for line (run in -I -W error).")
row(28, "Rubric row C1 and exemplar B annotations", "project.html rubric row C1 (line 492); Exemplar B passage", "PASS", CAR + "Rubric row C1 wording re-read this round.")
row(29, "Round-10 FAIL cards c143, c145, c161, c165 cleared", "course/modules/M/M3/cards.json: M3-c143, M3-c145, M3-c161, M3-c165", "PASS", CAR + "cards unchanged except lines 1280 and 1287.")
row(30, "Cards carried from earlier rounds still match their lessons", "course/modules/M/M3/cards.json (c094, c101, c104, c133, c142, c153 and others)", "PASS", CAR + "cards unchanged except lines 1280 and 1287; their lesson sources (L01 to L09) changed only in the hunks listed above, none of which these cards cite.")
row(31, "Hours arithmetic and Lab 3 interpretation cross-references", "project.html time budget (lines 258-264), line 469", "PASS", "Re-summed (row R11) and re-verified the line 469 numbers (row R06).")
row(32, "Card M3-c040 back vs L02 Misconception 1", "course/modules/M/M3/cards.json M3-c040; course/modules/M/M3/L02.html Misconception 1", "PASS", CAR + "c040 unchanged; its matrix [[1,1],[1,-1]] and [[0,2],[1,0]] for basis (1,0),(1,1) re-derived: P = [[1,1],[0,1]], P^-1 A P = [[0,2],[1,0]].")
row(33, "Card M3-c093 back lists the eigenvalues asked by its front", "course/modules/M/M3/cards.json M3-c093; course/modules/M/M3/L05.html", "PASS", CAR + "L05 lab output line 8 (Gram matrices, 500 of 500) unchanged.")
row(34, "Process words in learner-visible Lab 2 docstring", "project.html Lab 2 block docstring (line 144)", "PASS", "Re-read this round: 'Rung 2 completion problem: the clipping repair on a second matrix. Fill the ___ blanks.' contains no process word.")
row(35, "comparison_weights refuses a volatility that is not strictly greater than zero", "course/modules/M/M3/grader/reference.py comparison_weights; test_project.py test_weights_refuse_volatility_at_or_below_zero", "PASS", CAR + "reference.py refuses zero, negative and NaN volatilities (it checks 'not float(v) > 0.0'); the grader test passes on the reference (row R12).")
row(36, "New student-error grader mutants (at least three) are killed", "ledgers/M3/mutants/r12d_m01..m04", "PASS", CAR + "r12d mutants killed in round 12; re-run this round as part of the full mutate run (row R37).")
row(37, "Alternatives and mutants re-run on the current grader", "ledgers/M3/mutants (all files); tools/mutate_graders.py --unit M3 --seeds 0-49", "PASS",
    "Re-run this round: 112 mutant files; 108 KILLED, 4 SURVIVED (r6d_m04, r9d_m02, r11d_m02 ruled in rounds 11-13; r13d_m03 equivalent, row R43). Verified mutant r13d_m03 gives bit-identical output to the reference on all 50 seeds, so it is not a grader gap.")
row(38, "Lab 1 composition claim in card M3-c184 and lesson text", "course/modules/M/M3/cards.json M3-c184; course/modules/M/M3/L02.html line 183; tests/labs/M3/lab-M3-L02-1.py output line 4", "PASS",
    "Re-run this round: lab-M3-L02-1.py prints 'composition matrix equals the product of matrices in 50 of 50 pairs'; L02 line 183 says 'again 50 of 50'. The card's 'the count covers the listed pairs only' is consistent with a finite seeded count.")
row(39, "Card M3-c183 (new) vs L09 Proposition 3.3(a) and Example 3.6", "course/modules/M/M3/cards.json M3-c183; course/modules/M/M3/L09.html lines 180, 185, 342", "PASS",
    "Re-derived: A = [[1,1.2],[1.2,1]] has eigenvalues 2.2 and -0.2; clipping gives A_0 = [[1.1,1.1],[1.1,1.1]]; A - A_0 = [[-0.1,0.1],[0.1,-0.1]]; squared Frobenius norm 0.04 = (0-(-0.2))^2. L09 line 180 states the same numbers.")
row(40, "mutate_graders M3 gate exit status", "tools/mutate_graders.py --unit M3 --seeds 0-49 (ledgers/M3/scripts/M3-d-r13/mutate_m3_r13.out)", "FAIL",
    "Gate exits 1: 'mutate_graders M3: FAIL (108/112 killed)'. The four survivors are r6d_m04, r9d_m02, r11d_m02 (ruled not violations in rounds 11-13) and r13d_m03 (equivalent: identical output). No grader defect. Fix (builder/tool owner): record the ruled survivors in the tool's allowlist or delete the ruled equivalent mutant. Severity low.")
row(41, "New student-error grader mutants: at least three new, each killed", "ledgers/M3/mutants/r13d_m01..m05", "PASS",
    "Five new mutants written this round and killed on seed 0 by the suite: r13d_m01 (clip floor ignored at zero) by test_clip_repair_is_positive_semidefinite; r13d_m02 (no pivot division) by test_lab3_reference_numbers_are_matched; r13d_m04 (off-diagonal volatility dropped) by test_lab3_reference_numbers_are_matched; r13d_m05 (last Jacobi value) by test_min_eigenvalue_matches_planted_spectrum. r13d_m03 survived as an equivalent mutant (row R43).")
row(42, "Six alternative correct implementations pass 50 seeds on the current grader", "ledgers/M3/scripts/M3-d-r13/alts_run.out; /tmp/m3d13_alts (make_alts.py)", "PASS",
    "alt1-alt6 each pass=50 fail=0; control reference pass=50. Validates that the suite does not over-constrain tight cutoffs, pivoting choices, the is_psd comparison form, and the projection iteration cap.")
row(43, "Mutant r13d_m03 (sign-flipped unit-diagonal Dykstra correction) is equivalent", "ledgers/M3/mutants/r13d_m03_projection_unit_diagonal_correction_sign_flipped.py", "PASS",
    "Analysis: after projection the off-diagonal entries of new_x equal y + corr_u, so the off-diagonal part of corr_u is identically 0 in both versions; the diagonal of corr_u is overwritten by new_x[i][i] = 1 before it is used. Both versions give the same iterates; numerical probe over seeds 0-49 gives max |ref - mut| = 0.0. Equivalent, not a grader gap.")
row(44, "Lab 3 and project labs run under -I -W error", "tests/labs/M3/lab-M3-project-1..3.py; lab-M3-L01..L09", "PASS", "Each of the 12 M3 lab twins run alone with python -I -W error: exit 0 (this round). run_labs M3 PASS (12/12).")
row(45, "Gates: ruff, format, mypy strict, verify_refs, build_site, render_curriculum", "repo root", "PASS",
    "ruff check . 'All checks passed!'; ruff format --check . '362 files already formatted'; mypy (strict, repo config) 'Success: no issues found in 255 source files'; verify_refs --offline '560 entries, 0 problems'; build_site --check 'site data current'; render_curriculum.py left git status unchanged (only the .venv symlink).")
row(46, "Test-count and grader collection claim", "project.html line 237 ('153 tests'); grader/test_project.py", "PASS", "collect-only 153 tests (collect.out); reference 153 passed (ref_run.out).")
frag = {
 "unit": "M3", "slice": "d", "round": 13,
 "verifier": "independent verifier (Claude Haiku 5.5), unit M3 slice d, round 13",
 "pin": "fca6bb1",
 "base": "round-12 fragment /Users/billyribeiro/.fanout/frags/B-M3-d.round12.json (pin ff38842)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyB13-M3-d",
 "scratch": "ledgers/M3/scripts/M3-d-r13/",
 "verified_at": "2026-10-29T13:00:00+00:00",
 "verdict": "FAIL",
 "rows": R,
 "mutants": [
  {"id": "r13d_m01_clip_floor_applied_only_when_positive", "description": "clip_repair ignores the floor at zero, so negative eigenvalues survive. KILLED on seed 0.", "killed_by": "test_clip_repair_is_positive_semidefinite[seed] (seed 0)"},
  {"id": "r13d_m02_weights_skip_pivot_division", "description": "comparison_weights omits the division by the pivot. KILLED on seed 0.", "killed_by": "test_lab3_reference_numbers_are_matched (seed 0)"},
  {"id": "r13d_m03_projection_unit_diagonal_correction_sign_flipped", "description": "projection_repair's unit-diagonal Dykstra correction has the wrong sign. SURVIVED: equivalent mutant (identical iterates on seeds 0-49).", "killed_by": "SURVIVED (equivalent; row M3-d-R43)"},
  {"id": "r13d_m04_weights_off_diagonal_volatility_dropped", "description": "comparison_weights puts volatilities on the diagonal only. KILLED on seed 0.", "killed_by": "test_lab3_reference_numbers_are_matched (seed 0)"},
  {"id": "r13d_m05_min_eigenvalue_last_jacobi_value", "description": "min_eigenvalue returns the last Jacobi diagonal entry. KILLED on seed 0.", "killed_by": "test_min_eigenvalue_matches_planted_spectrum[seed] (seed 0)"},
  {"id": "alternatives_alt1_to_alt6", "description": "Six correct alternatives (tight Jacobi cutoff, negated is_psd comparison, separate square-root rescale, projection max_iter 2000, weights without pivoting, floor via max over -inf): each passes 50/50 seeds.", "killed_by": "not a mutant (over-constraint check): 50/50 each"},
  {"id": "all_existing_112", "description": "tools/mutate_graders.py --unit M3 --seeds 0-49: 108 KILLED, 4 SURVIVED (r6d_m04, r9d_m02, r11d_m02 ruled in rounds 11-13; r13d_m03 equivalent). Gate exit 1, see row M3-d-R40.", "killed_by": "mutate_graders M3 seeds 0-49"}
 ],
 "registry_flags": [],
 "freshness_flags": ["Round-13 delta from ff38842 to fca6bb1 for slice d: project.html lines 37, 53, 231, 469; cards.json lines 1280 (M3-c183) and 1287 (M3-c184); L07, L08, L09 hunks (read and checked against the cards)."],
 "notes": [
  "Not checked: the 120-second browser run limit (plain-text claim, no browser run).",
  "Not checked: Stretch prompts (stated as tasks).",
  "Not checked in full: prose of L01-L09 outside the cited hunks and card sources; these are other slices.",
  "Not checked: the vendor directory (course/assets/vendor) was not copied to the checkout, so the browser-based page_smoke M3 ran against the checkout's existing assets as the gate reports PASS; no vendor-dependent claim was re-derived.",
  "Not checked: the rubric exemplar annotations are judged as pedagogy, not re-scored by a human.",
  "Tool note: check_pages --all fails on E3 (missing tests/labs/E3/lab-E3-project-2.py) in this checkout when run unit-wide; check_pages M3 PASS when run for M3. Not M3 slice d.",
  "Tool note: mutate_graders M3 exits 1 for ruled survivors (see M3-d-R40)."
 ],
 "summary": "M3 slice d round 13: FAIL on one row (M3-d-R40: the mutate_graders M3 gate exits 1 with 108/112 killed; the four survivors are ruled non-violations or equivalent; no grader defect found). 46 rows: 45 PASS, 1 FAIL. Five new student-error mutants killed; six alternatives pass 50/50; reference 50/50; collect 153; project.html Lab 3 numbers recomputed with numpy and matched; cards c183 and c184 match their lessons; gates check_pages M3, check_dag, check_projects, page_smoke M3, run_labs M3, verify_refs, ruff, format, mypy strict pass."
}
out = pathlib.Path("ledgers/M3/M3-d.json")
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("errors:", ledger.validate(frag, "M3-d"))
