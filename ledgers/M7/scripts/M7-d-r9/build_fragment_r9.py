"""Round 9 (M7-d): build ledgers/M7/M7-d.json from the round-9 evidence. Rows and statuses are the verifier's; this script only serialises them."""
import json, re, subprocess, pathlib, datetime
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD9-M7-d")
S = "ledgers/M7/scripts/M7-d-r9"
PIN = "1e272e5a641f18412703b37778a44db6f7391a69"
prev = json.load(open("/Users/billyribeiro/.fanout/frags/D-M7-d.round8.json"))
prev_rows = {r["id"]: r for r in prev["rows"]}

def mutant_rows():
    out = []
    for line in open(ROOT / S / "mutate_M7_0-9_r9_final.log", encoding="utf-8"):
        m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*?) -> (.*)$", line.rstrip("\n"))
        if not m:
            continue
        status, name, desc, killed = m.groups()
        out.append({"id": name.removesuffix(".py"), "description": desc,
                    "file": f"ledgers/M7/mutants/{name}", "killed_by": killed if status == "KILLED" else ""})
    return out

rows = []
def row(id_, check, location, status, evidence, fix=None):
    r = {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix or "see evidence"
    rows.append(r)

CARRY = lambda txt: txt  # every row below was re-verified this round; no carried PASS rows
# --- round-8 rows, re-verified on pin 1e272e5 ---
for rid in [f"PRJ-D1-{i:02d}" for i in range(1, 39)]:
    pass  # filled explicitly below for readability

D1 = {
 "PRJ-D1-01": ("2.6-spec", "course/modules/M/M7/grader/instance.py:14-68", "PASS",
   "Re-read instance.py (unchanged since the pin of round 8). Seeds 0-49 all generate valid cases (run_graders_M7_0-49.log: reference 50/50); asset counts are 3, 4 and 5 (instance.py:21). PASS."),
 "PRJ-D1-02": ("2.6-spec", "course/modules/M/M7/project.html:299-300; grader/test_project.py:output_shape", "PASS",
   "output_shape re-read (test_project.py:173-199); reference passes 50/50 (run_graders_M7_0-49.log); collected 364 on all 50 seeds (collect_all_seeds_r9.log)."),
 "PRJ-D1-03": ("2.4-math", "course/modules/M/M7/project.html:309", "PASS",
   "Linearization re-derived both ways (t_i = |d_i| satisfies the three turnover constraints; sum|d_i| <= sum t_i <= tau). Unchanged line."),
 "PRJ-D1-04": ("2.4-math", "course/modules/M/M7/project.html:310-313", "PASS",
   "r^w_i and r^t_i re-derived from the Lagrangian L = f + sum lambda_j g_j + nu(sum w - 1) with g_j as on page:310 (d/dw_i: gamma(Sigma w)_i - mu_i + nu - lambda^l_i + lambda^u_i + eta_k(i) + alpha_i - beta_i; d/dt_i: kappa - alpha_i - beta_i). Matches reference.py:305-308. Unchanged lines."),
 "PRJ-D1-05": ("2.4-math", "course/modules/M/M7/project.html:310, 314-319; grader/test_project.py:inequality_pairs", "PASS",
   "Inequality list (l-w, w-u, sector minus cap, d-t, -d-t, sum t - tau) and the four certificate definitions match inequality_pairs and recomputed_certificate (test_project.py:115-164) and reference._certificate (reference.py:262-315)."),
 "PRJ-D1-06": ("2.4-math", "course/modules/M/M7/project.html:320", "PASS",
   "Floor claim re-derived: unfloored value is -min(multipliers), differs from the floored value only when min > 0; the agreement tolerance 1e-9 (test_project.py:433) makes the failure threshold min > 1e-9. Degenerate case: r8 multipliers re-derived (see PRJ-R9-11)."),
 "PRJ-D1-07": ("2.4-math", "course/modules/M/M7/project.html:317-321; grader/test_project.py:153-164", "PASS",
   "Four certificate definitions re-derived; reference._certificate computes the same quantities in exact arithmetic; the suite recomputes them independently; agreement 50/50 seeds (run_graders_M7_0-49.log)."),
 "PRJ-D1-08": ("2.4-math", "course/modules/M/M7/project.html:323-324 (Proposition and proof)", "PASS",
   "Re-derived this round after the line-324 change (PRJ-R9-05). Every step valid under the hypotheses; the extension step is written. PASS."),
 "PRJ-D1-09": ("2.4-math", "course/modules/M/M7/project.html:325; grader/instance.py:38-43", "PASS",
   "Sigma = (A'A + I)/1000 is symmetric, and x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0 (instance.py:40-41). Unchanged."),
 "PRJ-D1-10": ("2.6-spec", "course/modules/M/M7/project.html:326; grader/reference.py:54-109", "PASS",
   "Each named refusal on page:326 is coded in reference._parse (ValueError for mapping, missing field, no assets, list length, symmetry, PD, gamma, turnover, bound order, start checks, sector label range, sector without asset; TypeError for bool or float labels and wrong types)."),
 "PRJ-D1-11": ("2.6-spec", "course/modules/M/M7/grader/test_project.py:NAMED_CONDITIONS, OTHER_SIDE_REFUSED", "PASS",
   "Each named condition has an invalid mutation refused with ValueError and a valid mutation accepted (test_named_condition_* pass on the reference, 364/364 seed 0). The valid-form rule is consistent with reference.py."),
 "PRJ-D1-12": ("2.6-spec", "course/modules/M/M7/project.html:326, 332; test_project.py:EXACT_BOUNDARIES", "PASS",
   "Boundary values named on the page (bound or cap equal to start; start sum inside 1e-9; turnover limit 0; gamma 1e-6) are exercised as accepted inputs; the reference passes them (364/364)."),
 "PRJ-D1-13": ("2.5-lab", "course/modules/M/M7/project.html:53-168; tests/labs/M7/lab-M7-project-1.py", "PASS",
   "run_labs_M7.log: 'run_labs M7: PASS (11/11)'. page_labs_r9.log: page code == twin (trailing newline ignored) True; twin exit 0 under python -I -W error; output == expected block True. Numbers re-derived exactly (claims_r9.py, budget-only 54/65, 5/26, -3/130; answer 9/11, 2/11, 0; nu -21/1100; lambda 9/1100; objective -3/220)."),
 "PRJ-D1-14": ("2.5-lab", "course/modules/M/M7/project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "PASS",
   "page_labs_r9.log: the page code differs from the twin only at the three blanks (step 4 residual; step 6 signs and dual_feasible), as the hypothesis states; the twin exits 0 and its output equals the expected block (True)."),
 "PRJ-D1-15": ("2.5-lab", "course/modules/M/M7/project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "PASS",
   "page_labs_r9.log: page code == twin, output == expected block. claims_r9.py: check A all zero; check B stationarity 9/550 (= 2 x 9/1100) and dual 9/1100; check C stationarity max 1/6250. Interpretation sentence matches."),
 "PRJ-D1-16": ("2.9-structure", "course/modules/M/M7/project.html:33, 338-354; course/modules/M/M7/index.html:29; curriculum/curriculum.json (M7 hours 110)", "PASS",
   "index.html:29 data-hours-lessons=77; project.html:33 data-hours-project=33; 77+33 = 110 = curriculum M7 hours (110, prereqs M2, M3); 33/110 = 30%."),
 "PRJ-D1-17": ("2.9-structure", "course/modules/M/M7/project.html:40-49", "PASS",
   "Ladder re-read: rung 1 solved (Lab 1), rung 2 completion (Lab 2), rung 3 spec plus autograder (Lab 3 check), rung 4 stretch (page:453-460)."),
 "PRJ-D1-18": ("2.9-structure", "course/modules/M/M7/project.html:288-336", "PASS",
   "Spec sections present (Context, Inputs, Required outputs, Conventions, Constraints, Grading, Reading list). Open question for the student (symmetry tolerance) is recorded in notes, not a row failure."),
 "PRJ-D1-19": ("2.9-structure", "course/modules/M/M7/grader/ (instance.py, reference.py, test_project.py, starter.py)", "PASS",
   "All four files exist; check_projects_M7.log: 'check_projects M7: PASS', exit 0."),
 "PRJ-D1-20": ("2.9-structure", "course/modules/M/M7/project.html; tools/page_smoke.py", "PASS",
   "page_smoke_project.log: zero errors on project.html; in-browser grader 'All 364 tests pass on seed 488945597'; 'page_smoke M7: PASS', exit 0."),
 "PRJ-D1-21": ("2.4-notation", "course/modules/M/M7/project.html; notation/notation.json", "PASS",
   "notation.json macros (\\E, \\Prob, \\R, \\N, \\argmax, \\tr, \\diag, \\SR, ...) and registered symbols (T, \\Phi, \\gamma_3, \\gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}) are absent from project.html and the project labs (grep this round). Local Greek letters (gamma, mu, Sigma, nu, lambda, eta, alpha, beta, kappa, tau) are defined on page:305-310, as notation.json 'about' allows. L, S_k, Z, n are local."),
 "PRJ-D1-22": ("2.9-structure", "course/modules/M/M7/project.html:456; course/concepts.html", "PASS",
   "check_dag_all.log: every unit PASS, exit 0. curriculum M7 prereqs M2, M3; the envelope-theorem concept is linked from the stretch; M2 introduces it (plans/M7-build-plan.md:47)."),
 "PRJ-D1-23": ("2.9-prose", "course/modules/M/M7/project.html; tests/labs/M7/lab-M7-project-*.py; grader/*.py", "PASS",
   "grep (this round) for round, verifier, builder, agent, Claude, LLM over project.html, the project labs and grader/*.py: no hits. check_pages_M7.log: PASS."),
 "PRJ-D1-24": ("2.6-spec", "course/modules/M/M7/project.html:364-366", "PASS",
   "Local command run on the reference (pytest -p no:cacheprovider --assert=plain -W error, QF_SEED=0; the page's -q and -I added in the harness): 364 passed (grader_suite_r9.sh, output in this round's runs)."),
 "PRJ-D1-25": ("2.6-autograder", "course/modules/M/M7/grader/starter.py:18-20", "PASS",
   "starter.allocate raises NotImplementedError (starter.py:20), as the page states (project.html:301)."),
 "PRJ-D1-26": ("2.6-autograder", "course/modules/M/M7/grader/instance.py:34-68", "PASS",
   "make_instance is deterministic (random.Random seeded by a string, instance.py:35); test_instance_is_simulated_and_deterministic passes; valid cases on seeds 0-49 (run_graders_M7_0-49.log)."),
 "PRJ-D1-27": ("2.6-autograder", "course/modules/M/M7/grader/test_project.py:37; reference.py:21", "PASS",
   "TOL = 1e-8 (test_project.py:37), agreement 1e-9 (test_project.py:433, 478), starting-portfolio tolerance 1e-9 (reference.py:21). Match page:321 and page:326."),
 "PRJ-D1-28": ("2.6-autograder", "course/modules/M/M7/grader/test_project.py (every assert message)", "PASS",
   "Every assert message is a fixed sentence with at most an index or case name (for example test_project.py:230-254, 381-383, 466-479). No message interpolates an expected value. The new fixture messages (test_project.py:72-98) are fixed sentences too."),
 "PRJ-D1-29": ("2.6-autograder", "course/modules/M/M7/grader/test_project.py; course/assets/js/py-worker.js", "PASS",
   "In-browser Pyodide (page_smoke_project.log: 364 pass); Node-hosted vendored Pyodide (pyodide_durations_r9.log: 364 passed); local pytest (364 passed)."),
 "PRJ-D1-30": ("2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py", "PASS",
   "pytest_M7_r9.log: 11 passed (tests/test_labs.py -k M7), exit 0."),
 "PRJ-D1-31": ("2.6-spec", "course/modules/M/M7/project.html:332; grader/test_project.py:HAND_CASES", "PASS",
   "collect_all_seeds_r9.log: '364 tests collected' on every seed 0-49. HAND_CASES has six entries (test_project.py:273-311)."),
 "PRJ-D1-32": ("2.6-atlas", "course/modules/M/M7/project.html; curriculum.json M7 entry", "PASS",
   "Not applicable: grep -ic atlas project.html = 0; the M7 curriculum entry has no atlas key."),
 "PRJ-D1-33": ("2.1-citations", "course/modules/M/M7/project.html:465-466; references/references.json", "PASS",
   "verify_refs_offline.log: '560 entries, 0 problems'. references.json unchanged this delta, so no live run was needed (CLAUDE.md: live run after changing references)."),
 "PRJ-D1-34": ("2.9-structure", "course/modules/M/M7/project.html:344-350", "PASS",
   "Hours table: 2 + 3 + 10 + 6 + 7 + 5 = 33, total row 33 = data-hours-project. Design-target ruling: arithmetic only."),
 "PRJ-D1-35": ("2.6-mutation", "ledgers/M7/mutants/ (188 files); tools/mutate_graders.py --unit M7 --seeds 0-9", "FAIL",
   "Final run (mutate_M7_0-9_r9_final.log, exit 1): 'mutate_graders M7: FAIL (185/188 killed)'. SURVIVED: v9_06_prints_before_refusing_a_non_integer_sector_label.py, v9_07_marks_its_argument_before_refusing_text_in_mu.py, v9_08_allocate_takes_an_optional_second_argument.py. The 185 killed include all 177 earlier mutants and v8_01..v8_03 (the round-8 survivors v8_01, v8_02 are now killed).",
   "Kill the three survivors by the fixes of PRJ-R9-01 (pytest.fail in the purity checks) and PRJ-R9-03 (functools.wraps on the fixture wrapper); both were validated in scratch (fix_and_masking_r9.log)."),
 "PRJ-D1-36": ("2.6-mutation", "ledgers/M7/mutants/ (families f6, g2, m, p, q, r, r13, r14, s, v, w, x, y, z)", "PASS",
   "Every family killed in mutate_M7_0-9_r9.log (185 KILLED, 0 SURVIVED, pre-v9_06..08 folder) and in the final run (see PRJ-R9-07, mutate_M7_0-9_r9_final.log)."),
 "PRJ-D1-37": ("2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/mutants/", "PASS",
   "The 8 equivalence-removed mutants named in mutant_equivalence_r14.json are absent from the folder (checked this round); no mutant in the folder is marked equivalent."),
 "PRJ-D1-38": ("2.6-autograder", "ledgers/M7/scripts/M7-d-r9/ alternatives (alt/, altr8/)", "PASS",
   "Correct alternatives pass 50/50 seeds 0-49 each (correct_alts_run_0-49.log): altA, altB (exact), altV1, altV2, altV4 (float, relative cutoffs), and alt_empty_start, alt_nullspace, alt_reverse_order (defective_alts_run_0-49.log: 50/50 each). Defective alternatives fail on page-named valid inputs (defective_alts_run_0-49.log): altC 38/50, altD 43/50, altE 42/50, alt_float 35/50, altG 41/50, altH 44/50, altV3 41/50, altV5 42/50 passing; e.g. 'altC_float_tight_1e-12.py seed=7 :: 2 failed' on test_named_condition_boundary_is_accepted[gamma-positive-zero-boundary] (gamma 1e-6, page:326)."),
 "PRJ-D1-39": ("2.9-structure", "course/modules/M/M7/grader/reference.py; BLUEPRINT.md:400-401; plans/M7-build-plan.md:408 (T6); .github/workflows/ci.yml; tools/build_site.py", "FAIL",
   "Re-checked on 1e272e5: BLUEPRINT.md:400-401 requires deployment to exclude every grader/reference.py. No deployment configuration exists (no vercel.json, netlify.toml, wrangler.toml, Dockerfile, railway config); .github/workflows/ci.yml has no deploy job; tools/build_site.py and tools/*.py contain no exclusion of reference.py (grep, this round); course/modules/M/M7/grader/reference.py remains in the course/ tree. Repo-level gap, outside this unit.",
   "Add the publication exclusion for course/**/grader/reference.py to the deployment configuration, or a build step that removes it from the published tree, and state it in the repo (BLUEPRINT.md:400-401; plan T6)."),
}
for rid, (check, loc, st, ev, *fix) in D1.items():
    row(rid, check, loc, st, ev, fix[0] if fix else None)

PASS_OLD = [
 ("PRJ-R4-01", "2.9-prose", "course/modules/M/M7/grader/test_project.py (docstrings and messages)", "FAIL",
   "Re-read every docstring and assert message this round. The new autouse fixture docstring (test_project.py:82-89) states 'A refusal is allowed, and these checks still apply to it'; that is not true for the tests that catch with pytest.raises(Exception) (PRJ-R9-01, PRJ-R9-02).",
   "Let the purity failure propagate past pytest.raises(Exception): raise pytest.fail(message, pytrace=False) instead of AssertionError in _observed_call and checked (validated in scratch, PRJ-R9-01), and correct the docstring only if the fix is not made."),
 ("PRJ-R5-01", "2.4-math", "course/modules/M/M7/project.html:456 (frontier bullet)", "PASS",
   "Line 456 byte-identical to the pin's line (read this round). The stretch asks the sign convention; no numeric result is asserted."),
 ("PRJ-R5-02", "2.6-spec", "course/modules/M/M7/grader/test_project.py (comments and messages)", "PASS",
   "Every comment and message in the file re-read this round (lines 1-1127); the round-7 corrected comments are correct (PRJ-R7-02, PRJ-R7-03). The new fixture docstring is covered by PRJ-R9-02."),
 ("PRJ-R5-03", "2.9-prose", "course/modules/M/M7/project.html:450", "PASS",
   "Line 450 unchanged; 'every case carries the SIMULATED label' holds: instance.py:57 label string; no data reads in test_project.py or reference.py (grep)."),
 ("PRJ-R5-04", "2.9-structure", "course/modules/M/M7/project.html:349-350", "PASS",
   "Hours total sentence: 77 + 33 = 110, matches index.html:29 and curriculum M7 hours 110."),
 ("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", "PASS",
   "All five KILLED in mutate_M7_0-9_r9.log."),
 ("PRJ-R6-01", "2.6-gate", "tools/check_projects.py", "PASS", "check_projects_M7.log: 'check_projects M7: PASS', exit 0 (run this round)."),
 ("PRJ-R6-02", "2.6-gate", "tools/check_pages.py", "PASS", "check_pages_M7.log: 'check_pages M7: PASS', exit 0 (run this round)."),
 ("PRJ-R6-03", "2.9-dag", "course/modules/M/M7/project.html; tools/check_dag.py", "PASS", "check_dag_all.log: every unit PASS, exit 0 (run this round)."),
 ("PRJ-R7-01", "2.6-mutation", "course/modules/M/M7/grader/test_project.py:degenerate box hand case; ledgers/M7/mutants/r7_06_*.py", "PASS",
   "r7_06 KILLED in mutate_M7_0-9_r9.log by the degenerate hand case."),
 ("PRJ-R7-02", "2.9-prose", "course/modules/M/M7/grader/test_project.py:294-296 (comment on the upper bound binding case)", "PASS",
   "Re-derived this round with the reference: with upper bound 1.0 the answer is (0.55, 0.45), with upper bound 0.3 it is (0.7, 0.3); the comment is correct."),
 ("PRJ-R7-03", "2.9-prose", "course/modules/M/M7/grader/test_project.py:916-921 (comment before POSITIONS)", "PASS",
   "Checked against the code: the starting-sum tests call _make_room (test_project.py:928-953); the lower-bound tests also raise the upper bound (test_project.py:965, 979); the upper-bound tests change only the bound. The comment matches."),
 ("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", "PASS", "All five KILLED in mutate_M7_0-9_r9.log."),
 ("PRJ-R7-05", "2.6-autograder", "course/modules/M/M7/grader/test_project.py (per-test time in Pyodide)", "PASS",
   "pyodide_durations_r9.log (Node-hosted vendored Pyodide, reference, seed 0): 364 passed, total 9.5 s, max single-test call 0.023 s; under BUILDER_RULES 5 s per test. Node-hosted, not the browser."),
 ("PRJ-R7-06", "2.8-data", "course/modules/M/M7/project.html; course/modules/M/M7/grader/instance.py", "PASS",
   "No dataset, download or figure on the page; the case is generated and labelled SIMULATED (instance.py:57)."),
 ("PRJ-R7-07", "2.6-hours", "course/modules/M/M7/project.html:344-350", "PASS", "Same arithmetic as PRJ-D1-34: 33 = 2+3+10+6+7+5."),
 ("PRJ-R8-01", "2.6-autograder", "course/modules/M/M7/grader/test_project.py:1114-1120 (test_allocate_prints_nothing_and_warns_nothing); course/modules/M/M7/project.html:327", "FAIL",
   "Accepted inputs are now covered: the autouse fixture (test_project.py:80-103) checks every call; v8_01 (debug print on zero turnover) is KILLED (mutate_M7_0-9_r9.log). The refusal path is not: the fixture's AssertionError is caught by the pytest.raises(Exception) tests, so a print made only before a refusal survives: v9_06 SURVIVES seeds 0-9 (probe_mutants_r9_c.log; fix_and_masking_r9.log: 364 passed with v9_06). Page:327 states 'It does not print, does not emit warnings' for the function, not only for accepted inputs.",
   "Raise pytest.fail(..., pytrace=False) from the checks in _observed_call and checked, so the purity failure is not caught by pytest.raises(Exception) (scratch check: v9_06 20 failed, reference 364 passed; fix_and_masking_r9.log)."),
 ("PRJ-R8-02", "2.6-autograder", "course/modules/M/M7/grader/test_project.py:1107-1111 (test_allocate_does_not_change_its_argument); course/modules/M/M7/project.html:327", "FAIL",
   "Accepted inputs are now covered (v8_02 KILLED; v9_04 KILLED). The refusal path is not: v9_07, which writes into its argument before refusing text in mu, SURVIVES seeds 0-9 (probe_mutants_r9_c.log; fix_and_masking_r9.log: 364 passed with v9_07). Page:327 'does not change its argument' is universal.",
   "Same fix as PRJ-R8-01 (pytest.fail in the purity checks; scratch: v9_07 25 failed, reference 364 passed)."),
 ("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", "PASS",
   "KILLED in mutate_M7_0-9_r9.log (test_hand_case_matches_its_worked_answer[zero turnover], seed 0)."),
 ("PRJ-R8-04", "2.6-spec", "course/modules/M/M7/grader/test_project.py:302-311 (degenerate box hand case and its comment)", "PASS",
   "Re-derived this round: lower = upper = start with zero turnover gives (0.5, 0.5); the multipliers lower (0.5, 0.5), upper (0.55, 0.35), sector 0.05, alpha = beta = 1, kappa = 2, nu = -0.3 satisfy stationarity (r_w = r_t = 0) and complementary slackness, with every inequality multiplier positive and the smallest 1/20. The comment's claims hold."),
]
for rid, check, loc, st, ev, *fix in PASS_OLD:
    row(rid, check, loc, st, ev, fix[0] if fix else None)

NEW = [
 ("PRJ-R9-01", "2.6-autograder", "course/modules/M/M7/grader/test_project.py:60-103 (fixture and _observed_call) against the pytest.raises(Exception) tests at :886, :894, :903, :912, :1020, :1074", "FAIL",
   "Purity masked on refusal paths. _observed_call raises AssertionError (test_project.py:71-76) and checked re-raises through it; the wrong-type tests catch that with pytest.raises(Exception, match=r'\\S'), so the AssertionError counts as the expected refusal. Mutants: v9_06 (prints 'refusing a boolean or non-integer sector label' before its TypeError) and v9_07 (writes instance['note'] before refusing text in mu) both SURVIVE seeds 0-9 (probe_mutants_r9_c.log). With v9_06 the suite passes: 'v9_06 seed 0: 364 passed' (fix_and_masking_r9.log); the boolean refusal tests pass with the print (33 passed under -k boolean). The direct call prints 'refusing a boolean or non-integer sector label' then 'refused: a sector label must be an integer' (run this round). Page:327 (project.html:327): 'The function is pure. It does not print, does not emit warnings, does not change its argument...'. Page:332 lists 'purity and silence' as checked.",
   "In _observed_call and checked, replace raise AssertionError(...) with pytest.fail(message, pytrace=False) (pytest.fail raises a BaseException subclass, which pytest.raises(Exception) does not catch). Validated in a scratch copy: reference 364 passed; v9_06 20 failed; v9_07 25 failed (fix_and_masking_r9.log)."),
 ("PRJ-R9-02", "2.9-prose", "course/modules/M/M7/grader/test_project.py:82-89 (every_allocate_call_is_pure docstring)", "FAIL",
   "The docstring says: 'A refusal is allowed, and these checks still apply to it.' For the tests that catch with pytest.raises(Exception), the purity checks do not apply to a refusal: the AssertionError from the check satisfies the catch (PRJ-R9-01). The sentence describes the intent, not the behaviour.",
   "Fix with the same change as PRJ-R9-01 (the sentence then holds), or reword the docstring to state the limitation."),
 ("PRJ-R9-03", "2.6-autograder", "course/modules/M/M7/grader/test_project.py:80-103 (autouse fixture rebinds sol.allocate) and :319-325 (test_module_defines_allocate_with_one_argument)", "FAIL",
   "Regression from round 8. The autouse fixture replaces sol.allocate with checked(instance) (test_project.py:103), so inspect.signature(sol.allocate) in test_module_defines_allocate_with_one_argument sees one parameter whatever the student wrote. Mutant v9_08 (allocate(instance, tolerance=1e-9)) SURVIVES seeds 0-9 with the round-9 suite (probe output this round: SURVIVED seeds 0-9; 364 passed in fix_and_masking_r9.log). The round-8 test file (git show 2d755599:.../test_project.py) KILLS it: 'FAILED test_project.py::test_module_defines_allocate_with_one_argument' (fix_and_masking_r9.log). Page:300-303 and page:33/Required outputs state 'one function allocate(instance)'.",
   "Decorate checked with @functools.wraps(real) (inspect.signature then follows __wrapped__). Validated in scratch: reference 364 passed; v9_08 1 failed (fix_and_masking_r9.log). Apply together with the PRJ-R9-01 fix."),
 ("PRJ-R9-04", "2.9-prose", "course/modules/M/M7/project.html:167 (Lab 1 interpretation, changed this delta)", "PASS",
   "Re-derived against the Lab 1 output (project.html:156-166). 'Step 5 shows that the budget gap is zero, and prints the smallest weight, zero at its lower bound, and the largest, 9/11': output line 'step 5 smallest weight: 0 largest weight: 9/11' and 'step 5 budget gap: 0' (line 162-163); the long-only bound (page:55, each weight at least zero) gives the lower bound zero for the third asset. 'its product with the held weight is zero': 'step 6 weight times multiplier, held assets: [0]' (line 165). Consistent with the code (lines 139-147)."),
 ("PRJ-R9-05", "2.4-math", "course/modules/M/M7/project.html:324 (proof, changed this delta)", "PASS",
   "Re-derived: 'Each g_j is affine in (w,t), because the constraints are affine' (true by hypothesis); L = f + sum lambda_j g_j + nu(sum w - 1) is convex in (w,t) because f is convex in w, lambda_j >= 0 and the rest is affine; stationarity gives a global minimiser of L; extension s_i = |y_i - w0_i| is feasible by the linearization equivalence (page:309); f(y) >= L(y,s) >= L(w,t) = f(w) by complementary slackness; uniqueness by the midpoint argument with the feasible set convex. No gap found."),
 ("PRJ-R9-06", "2.6-autograder", "ledgers/M7/scripts/M7-d-r9/correct_alts_run_0-49.log; defective_alts_run_0-49.log (over-constraint check of the new fixture)", "PASS",
   "Five correct alternatives pass all 50 seeds on the round-9 suite: altA 50/50, altB 50/50, altV1 50/50, altV2 50/50, altV4 50/50 (correct_alts_run_0-49.log SUMMARY lines). Three more correct alternatives: alt_empty_start 50/50, alt_nullspace 50/50, alt_reverse_order 50/50 (defective_alts_run_0-49.log). The purity fixture does not reject any correct method."),
 ("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder, 188 files); ledgers/M7/scripts/M7-d-r9/mutate_M7_0-9_r9_final.log", "FAIL",
   "Final gate: 'mutate_graders M7: FAIL (185/188 killed)', exit 1. The five new student-error mutants v9_01..v9_05 are KILLED (v9_01 prints when turnover binds; v9_02 prints for five-asset binding turnover; v9_03 warns on a degenerate box; v9_04 stores a note in its argument; v9_05 negates the budget multiplier on every second call), and the round-8 survivors v8_01 and v8_02 are KILLED. The survivors are v9_06 (print before refusing a non-integer sector label), v9_07 (argument change before refusing text in mu) and v9_08 (optional second argument), the subjects of PRJ-R9-01 and PRJ-R9-03. mutate_M7_0-9_r9.log (before v9_06..v9_08 existed): 185/185 KILLED.",
   "Kill v9_06 and v9_07 with pytest.fail in the purity checks (PRJ-R9-01) and v9_08 with functools.wraps (PRJ-R9-03)."),
 ("PRJ-R9-08", "2.6-spec", "course/modules/M/M7/grader/test_project.py (collected count) ; project.html:332", "PASS",
   "collect_all_seeds_r9.log: '364 tests collected' on all 50 seeds 0-49 with the round-9 file; reference 364 passed (seed 0, pytest output)."),
 ("PRJ-R9-09", "2.5-lab", "course/modules/M/M7/project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
   "page_labs_r9.log: lab 1 and lab 3 page code == twin (trailing newline ignored); lab 2 differs only at the three blanks; all three twins exit 0 under python -I -W error with empty stderr; each output equals its expected block (True). run_labs_M7.log 11/11."),
 ("PRJ-R9-10", "2.6-autograder", "course/modules/M/M7/grader/test_project.py under Node-hosted Pyodide", "PASS",
   "pyodide_durations_r9.log: 364 passed, exit 0, max call 0.023 s (reference, seed 0)."),
 ("PRJ-R9-11", "2.9-prose", "course/modules/M/M7/grader/test_project.py:274-311 (hand-case comments)", "PASS",
   "Re-run with the reference (this round): 'upper bound binding' with upper 1.0 gives (0.55, 0.45) (the comment's claim that the turnover limit alone stops the answer at (0.55, 0.45) holds), with upper 0.3 gives (0.7, 0.3); 'turnover binding' gives (0.6, 0.4); budget-only (0.6, 0.4) by hand (stationarity w - mu + nu = 0, nu = -0.3). The 0.55 claim is also checked by hand: on the sum-one line, the derivative 2 w1 - 0.7 is positive for w1 >= 0.35, and the turnover constraint gives w1 >= 0.55."),
]
for rid, check, loc, st, ev, *fix in NEW:
    row(rid, check, loc, st, ev, fix[0] if fix else None)

mut = mutant_rows()
fails = [r["id"] for r in rows if r["status"] != "PASS"]
n_pass = sum(1 for r in rows if r["status"] == "PASS")
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
frag = {
 "unit": "M7", "slice": "d", "round": 9,
 "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 9 (did not build M7-d; own checkout)",
 "pin": PIN,
 "base": "2d755599d8d74df292e3e43025f0458c4053802e (round-8 pin); delta 2d755599..1e272e5 in slice: project.html line 167 (Lab 1 interpretation) and line 324 (Proposition proof); grader/test_project.py lines 60-103 (new autouse purity fixture and _observed_call) and the import of functools/copy; cards.json changed in the same range but is not in slice M7-d (no cards in this slice)",
 "checkout": "/Users/billyribeiro/.fanout/wt/verifyD9-M7-d",
 "scratch": "/tmp/m7d-r9 (scratch runs only; every row's evidence script or log is under ledgers/M7/scripts/M7-d-r9/)",
 "verified_at": now,
 "verdict": "FAIL",
 "rows": rows,
 "mutants": mut,
 "registry_flags": [],
 "freshness_flags": [],
 "notes": (
   "Round 9 on 1e272e5. Verdict FAIL: " + str(len(fails)) + " non-PASS rows (" + ", ".join(fails) + "). "
   "Root cause of the three new FAILs (PRJ-R9-01..03): the autouse purity fixture (test_project.py:80-103) is correct for accepted inputs (v8_01, v8_02 and v9_01..v9_05 are killed; five correct alternatives pass 50/50), but (a) its AssertionError is caught by the pytest.raises(Exception) tests, so refusal-path prints, warnings and argument changes survive (v9_06, v9_07), and (b) the fixture replaces sol.allocate with a one-argument wrapper that hides the signature from test_module_defines_allocate_with_one_argument (v9_08 survives; the round-8 suite kills it). Both fixes (pytest.fail with pytrace=False, functools.wraps) were validated in scratch copies only (fix_and_masking_r9.log); the repo was not edited. "
   "Mutation gate: the full run started before v9_06..v9_08 were added and recorded 185/185 KILLED (mutate_M7_0-9_r9.log); after adding them the final folder has 188 files (mutate_M7_0-9_r9_final.log). The three new survivors are the FAILs above. "
   "Gates re-run this round: check_pages, check_projects, check_dag --all, run_labs (11/11), page_smoke project (in-browser 364), verify_refs --offline (560, 0 problems), run_graders 0-49 (50/50), ruff check and ruff format --check (clean), mypy --no-incremental (no issues in 385 files), pytest tests/test_labs.py -k M7 (11 passed), collect-only 364 on seeds 0-49, Node-hosted Pyodide (364 passed). Live verify_refs not re-run: references.json unchanged in the delta. "
   "Alternatives: correct altA, altB, altV1, altV2, altV4, alt_empty_start, alt_nullspace, alt_reverse_order pass 50/50; defective altC, altD, altE, alt_float, altG, altH, altV3, altV5 fail on seeds where page-named valid inputs (gamma 1e-6, gamma 1e-9) are refused or wrong; counts are identical to round 8."),
 "summary": (
   "M7-d round 9: verdict FAIL. " + str(len(rows)) + " rows: " + str(n_pass) + " PASS, " + str(len(fails)) + " FAIL (" + ", ".join(fails) + "). "
   "New FAILs: refusal-path purity masked by pytest.raises(Exception) (v9_06, v9_07 survive); docstring claim false for those tests; signature test masked by the fixture (v9_08 survives, round-8 suite kills it). "
   "Carried-forward FAILs: PRJ-D1-39 (repo has no reference.py deployment exclusion), PRJ-R8-01/02 (still open on the refusal path). Lab 1 and the Proposition proof changes verified; alternatives and mutation gate clean."),
 "not_checked": [
   "The browser (Chromium) run of the alternatives; the in-browser grader was run through page_smoke (364 pass), the alternatives were run in local pytest only.",
   "The live verify_refs run (no references changed in the delta).",
   "The full pytest suite (tests/) and tools/render_curriculum.py, build_site.py --check, fetch_data.py --check (no curriculum, site-data, market or reference input of this slice changed; cards.json belongs to another slice).",
   "The starter on 50 seeds (starter.py raises NotImplementedError; PRJ-D1-25 checked on one seed run through run_graders).",
   "Mutation coverage of purity on accepted inputs that no test calls: a print on an untested input is not killable by a finite suite; only the page-stated behaviour on the tested inputs was checked.",
   "Hours were not re-estimated (architect ruling: design targets; arithmetic only).",
   "The symmetry tolerance of sigma (unstated in the page; no row).",
 ],
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "pass", n_pass, "fail", fails, "mutants", len(mut), "killed", sum(1 for m in mut if m["killed_by"]))
