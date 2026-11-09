"""Round-15 fragment builder for M7 slice d (repository script). Reads the round-14 row ids, the mutation logs of this
round, and writes ledgers/M7/M7-d.json. Run from the checkout root with python -I."""
import datetime, json, re, sys
from pathlib import Path

ROOT = Path.cwd()
S = ROOT / "ledgers/M7/scripts/M7-d-r15"
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/D-M7-d.round14.json").read_text(encoding="utf-8"))
prev_ids = [r["id"] for r in prev["rows"]]
prev_check = {r["id"]: r["check"] for r in prev["rows"]}
prev_loc = {r["id"]: r["location"] for r in prev["rows"]}

RE_READ = ("Read in full this round: course/modules/M/M7/project.html 1-482, grader/test_project.py 1-1128, grader/instance.py, "
           "grader/starter.py, grader/reference.py 1-380. ")
GATES = ("tools/check_pages.py --unit M7 PASS, check_dag.py --unit M7 PASS, check_projects.py --unit M7 PASS "
         "(ledgers/M7/scripts/M7-d-r15/check_*_M7_r15.log; repo-wide --all runs also exit 0). ")
MUT = ("tools/mutate_graders.py --unit M7 --seeds 0-9: 205/205 existing mutants killed (mutate_graders_M7_0-9_r15.log). ")

E = {}
E["PRJ-D1-01"] = "instances50_collect50_r15.py: for seeds 0-49 the label contains SIMULATED, make_instance is deterministic, and every start is feasible in exact Fractions (50 of 50). Output in the scripts folder."
E["PRJ-D1-02"] = RE_READ + "project.html:298-300 (three keys; seven multiplier keys; four certificate keys; list lengths n, Z) matched line by line against test_project.py output_shape (174-201)."
E["PRJ-D1-03"] = RE_READ + "project.html:309 re-derived: sum|d_i| <= tau iff some t has t_i >= d_i, t_i >= -d_i, sum t_i <= tau (witness t_i = |d_i|; sum|d_i| <= sum t_i <= tau)."
E["PRJ-D1-04"] = RE_READ + "project.html:310-313 re-derived from L = f + sum lam_j g_j + nu(sum w - 1) with g as listed in project.html:310: dL/dw_i gives gamma(Sigma w)_i - mu_i + nu - lam^l_i + lam^u_i + eta_k(i) + alpha_i - beta_i, dL/dt_i gives kappa - alpha_i - beta_i. Matches."
E["PRJ-D1-05"] = RE_READ + "project.html:310,314-319 six inequality groups and their g_j versus test_project.py inequality_pairs (116-130): identical."
E["PRJ-D1-06"] = RE_READ + "project.html:320 floor versus test_project.py recomputed_certificate (154-165): dual = max(0, -min m) and the agreement check applies the floor."
E["PRJ-D1-07"] = RE_READ + "project.html:317-321 versus recomputed_certificate (154-165) and assert_kkt (226-255): the four fields and their tolerances (1e-8 bound, 1e-9 agreement) agree."
E["PRJ-D1-08"] = RE_READ + "project.html:323-325 proposition and proof re-read step by step: convexity of L in (w,t), f(y) >= L(y,s) >= L(w,t) = f(w), midpoint argument for uniqueness; hypotheses complete. Grade T supported."
E["PRJ-D1-09"] = "project.html:325 hypotheses versus instance.py:3-4 and 39-43: Sigma = (A'A + I)/1000 gives x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0; SIMULATED label present (50 of 50 seeds)."
E["PRJ-D1-10"] = RE_READ + "project.html:326 refusal list versus reference.py _parse (54-109): each named condition raises ValueError (mapping, missing field, NaN/inf via _scalar, no assets, list lengths, symmetry, PD via LDL pivots, gamma, tau, lower>upper, start checks with TOL 1e-9, sector label range, empty sector)."
E["PRJ-D1-11"] = RE_READ + "test_project.py NAMED_CONDITIONS (637-651) and OTHER_SIDE_REFUSED (754-777) demand ValueError; other invalid inputs (864-906, 892-906) accept any Exception with a message, as project.html:326 and plan 7.4.1 require."
E["PRJ-D1-12"] = RE_READ + "project.html:326,332 boundary list versus EXACT_BOUNDARIES (674-680) and the named valid forms (637-651, 698-704): lower/upper/cap equal to the start, start sum inside 1e-9 on both sides, gamma 1e-9 accepted."
E["PRJ-D1-13"] = "run_labs.py --unit M7 PASS (11/11). twin_vs_page_r15.py: page code of lab-M7-project-1 equals tests/labs/M7/lab-M7-project-1.py; the twin exits 0 under python -I -W error with empty stderr; its stdout equals the expected block (project.html:156-166)."
E["PRJ-D1-14"] = "twin_vs_page_r15.py: page code of Lab 2 differs from tests/labs/M7/lab-M7-project-2.py only in the three blanked lines (residual, signs, dual_feasible); the completed twin's stdout equals the expected block (project.html:273-283), which equals Lab 1's block."
E["PRJ-D1-15"] = "twin_vs_page_r15.py: Lab 3 page code equals its twin; output equals the expected block (project.html:441-443). Printed 9/550, 9/1100 and 1/6250 re-derived by hand: 2*9/1100 = 9/550; gradient change of asset 2 is 2*(1/100*1/1000 - 9/100*1/1000) = -1/6250."
E["PRJ-D1-16"] = "project.html:33 data-hours-project=33 and table rows 344-350 sum to 2+3+10+6+7+5 = 33; course/modules/M/M7/index.html:29 data-hours-lessons=77 (lessons 3x9 + 5x10 = 77, index.html:141); curriculum/01-foundations.yaml M7 hours 110 = 77 + 33."
E["PRJ-D1-17"] = RE_READ + "project.html:40-49 ladder: rung 1 worked and annotated (Lab 1), rung 2 completion (Lab 2), rung 3 specification and autograder, rung 4 stretch. Matches the spec."
E["PRJ-D1-18"] = RE_READ + "project.html:288-336 spec read against instance.py and reference.py: inputs, outputs, conventions, constraints and grading are complete; no clarifying question arises from re-reading."
E["PRJ-D1-19"] = "git ls-files: course/modules/M/M7/grader/ holds instance.py, reference.py, starter.py, test_project.py; project.html:359 data-suite/data-support/data-solution/data-starter name the same files."
E["PRJ-D1-20"] = "page_smoke.py --unit M7 --pages project: PASS (page_smoke_project_r15.log: runtime boot, labs 1-3, in-browser grader 364 tests pass on a seed)."
E["PRJ-D1-21"] = "project.html symbols versus notation/notation.json (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q): none used with another meaning; gamma is the local risk aversion, which the registry allows; alpha, beta, eta, kappa, nu, tau are defined on the page."
E["PRJ-D1-22"] = "project.html:456 concept link to concepts.html#envelope-theorem; check_dag.py --unit M7 PASS (check_dag_M7_r15.log)."
E["PRJ-D1-23"] = "check_pages.py --unit M7 PASS (BANNED list applied, check_pages_M7_r15.log); project.html read for banned phrases, none found."
E["PRJ-D1-24"] = "Documented command run in a scratch copy: QF_SEED=7 pytest -q -p no:cacheprovider --assert=plain -W error test_project.py with reference.py as constrained_allocator.py: 364 passed (doc_command_reference_seed7_r15.log). The decode command prints the payload mapping (verified)."
E["PRJ-D1-25"] = "grader/starter.py:18-20 raises NotImplementedError. The same documented command on the starter: 361 failed, 3 passed (doc_command_starter_seed7_r15.log); project.html:301 consistent."
E["PRJ-D1-26"] = "instance.py make_instance read; 50 seeds deterministic, labelled and feasible (instances50_collect50_r15.py)."
E["PRJ-D1-27"] = "test_project.py:37 TOL = 1e-8 for feasibility and stationarity, agreement 1e-9; reference.py:21 TOL = 1e-9 for start checks; project.html:300,321 state the same values."
E["PRJ-D1-28"] = RE_READ + "Every assert and pytest.fail message read (test_project.py 60-77, 174-201, 231-255, 434-443, 1108-1121): each names a property or an index and prints no expected value. Default-mode and --assert=plain runs both pass (default_mode_reference_seed3_r15.log)."
E["PRJ-D1-29"] = "CPython: run_graders.py --unit M7 --seeds 0-49 PASS (reference 50/50). Pyodide: page_smoke.py --unit M7 --pages project PASS (in-browser grader 364 tests pass)."
E["PRJ-D1-30"] = "run_labs.py --unit M7 PASS (11/11); pytest tests/test_labs.py -k M7: exit 0, 11 passed (pytest_labs_M7_r15.log)."
E["PRJ-D1-31"] = RE_READ + "test_project.py HAND_CASES (274-312): each worked answer re-derived by hand (budget-only (0.6,0.4); zero turnover (0.5,0.5); single asset (1); upper bound (0.7,0.3); turnover (0.6,0.4); degenerate box (0.5,0.5)). The hand-case tests pass on reference (364 of 364 on seed 7)."
E["PRJ-D1-32"] = "check_projects.py --unit M7 PASS (check_projects_M7_r15.log); course/modules/M/M7 matches the curriculum/01-foundations.yaml M7 entry (grading autograder, hours 110)."
E["PRJ-D1-33"] = "project.html:465-466 cite boyd2004convex and stokey1989recursive; both keys present in references/references.json; verify_refs.py --offline: 560 entries, 0 problems; verify_refs.py --unit M7 (live Crossref run): 2 of 560 entries, 0 problems. The page attaches no claim to either source (reading list only), so no attribution is checked."
E["PRJ-D1-34"] = RE_READ + "project.html:338-354 time-budget table and the lesson structure; check_pages.py --unit M7 PASS."
E["PRJ-D1-35"] = MUT + "The three round-15 mutants (r15_01..03) are also killed (new_mutants_r15_seeds0-9.log)."
E["PRJ-D1-36"] = MUT + "All 208 mutants in the folder are killed (mutate log plus the new-mutant log)."
E["PRJ-D1-37"] = ("ledgers/M7/equivalent/ now exists with README.md and the eight removed mutants; each file is byte-identical to git 5e18d08d:ledgers/M7/mutants/<name> "
    "(equiv_sources_r15.sh, equiv_sources_r15.log: SAME for all eight). Re-run of equiv_recheck_r15.py (400 random page-valid cases): q04, r02, r04, s12_03, v10_01, v11_01 and v12_01 never differ from the reference by more than 1e-9. "
    "r05_turnover_total_slackness_term_zeroed and v10_02_complementary_slackness_signed_not_absolute DO differ: 9 and 23 of 400 cases beyond 1e-9 (max 6e-7 and 8e-7), and tiny_tau_probe_r15.log case A (tau=1e-9, mu=[1000,0]) gives reported complementary 0 against recomputed 5e-7 for both, case B (tau=1e-10, mu=[100,0]) gives 0 against 5e-9. "
    "The README proofs 7 and 8 (\"at most kappa times a slack of size at most 1e-9\", measured max 7.969e-11) are therefore false: kappa is not bounded by 1. See PRJ-R15-02.")
E["PRJ-D1-38"] = ("ledgers/M7/scripts/M7-d-r11/alts (alt1..alt9) re-run on seeds 0-49 (alts_r11_seeds0-49_r15.log): alt1, alt2, alt6, alt8, alt9 pass 50/50; alt3 48/50, alt4 41/50, alt5 46/50, alt7 49/50, all failing only "
    "on the named valid forms gamma = 1e-6 or 1e-9 (project.html:326). Classified as student errors under ruling 10 (float cutoffs at gamma scale), per the round-14 record; not over-constraint. Ruling 10 text not available to this verifier.")
E["PRJ-D1-39"] = ("BLUEPRINT.md:400-401 requires that deployment exclude every grader/reference.py. No exclusion exists in this repository: .gitignore, .vercelignore (absent), vercel.json (absent), "
    ".github/workflows/ci.yml (no publish step; only an artifact upload of screenshots), tools/build_site.py and tools/coursekit.py contain no exclusion. git ls-files shows 24 tracked reference.py files under course/ "
    "(including course/modules/M/M7/grader/reference.py). The deploy configuration, if any, is outside this repository and could not be read, so the requirement is unverifiable (fail closed). See the fix.")
E["PRJ-R4-01"] = RE_READ + "test_project.py module and function docstrings (1-12, 60-104, 447-453, 807-889) read; each states a property that the assertion checks."
E["PRJ-R5-01"] = RE_READ + "project.html:456 frontier bullet: the envelope relation, the sign convention left to the student, and the check on two grid points are stated; no claim is made that the suite checks them."
E["PRJ-R5-02"] = RE_READ + "test_project.py comments and messages at 275, 277, 295-296, 301, 303-305 checked against the hand cases they describe (each worked value re-derived)."
E["PRJ-R5-03"] = RE_READ + "project.html:450 'does not test' paragraph read: the suite runs on the generated problem and the hand cases only; the claims made there are true of test_project.py."
E["PRJ-R5-04"] = RE_READ + "project.html:349-350 rationale text for the self-check and certificate rows versus the grader's failure messages."
E["PRJ-R5-05"] = MUT + "r5_01..r5_05 are among the killed set (mutate_graders_M7_0-9_r15.log)."
E["PRJ-R6-01"] = GATES + "check_projects.py --all exits 0 (check_projects_all_r15.log)."
E["PRJ-R6-02"] = GATES + "check_pages.py --all exits 0 (check_pages_all_r15.log)."
E["PRJ-R6-03"] = GATES + "check_dag.py --all exits 0 (check_dag_all_r15.log)."
E["PRJ-R7-01"] = RE_READ + "test_project.py degenerate-box hand case (306-311) read; its worked answer (0.5, 0.5) re-derived; mutants r7_06 killed."
E["PRJ-R7-02"] = RE_READ + "test_project.py:295-296 comment (the upper-bound hand case) re-derived: without the 0.3 bound the answer is (0.55, 0.45)."
E["PRJ-R7-03"] = RE_READ + "test_project.py:916-921 comment on the every-position design read; the positions tuple (0, 1, 2, -1) and the N >= 3 guarantee match instance.py ASSET_COUNTS."
E["PRJ-R7-04"] = MUT + "r7_01..r7_05 killed."
E["PRJ-R7-05"] = "page_smoke.py --unit M7 --pages project PASS: the grader runs in Pyodide (in-browser 364 pass)."
E["PRJ-R7-06"] = RE_READ + "project.html and instance.py: no data file is read by the page, the labs or the suite; every case carries the SIMULATED label (50 of 50 seeds)."
E["PRJ-R7-07"] = RE_READ + "project.html:344-350 hours estimate re-estimated: rungs about 5 h, core solver about 10-14 h, linear constraints about 5-6 h, certificate about 4-6 h, self-check about 4-6 h; total about 28-37 h, within 30% of 33 h."
E["PRJ-R8-01"] = RE_READ + "test_project.py 60-77 (_observed_call), 80-104 (purity fixture), 1114-1121: every allocate call is checked for argument change, printing, warnings and determinism."
E["PRJ-R8-02"] = RE_READ + "test_project.py 1108-1112 and the purity fixture (80-104) read."
E["PRJ-R8-03"] = MUT + "v8_03_budget_multiplier_zero_when_start_is_optimal.py killed."
E["PRJ-R8-04"] = RE_READ + "test_project.py 302-311 (degenerate box hand case) read; the expected value (0.5, 0.5) is the worked answer."
E["PRJ-R9-01"] = RE_READ + "test_project.py 60-77 (_observed_call returns refusals) against the pytest.raises(ValueError) and pytest.raises(Exception) forms used at 686-692, 783, 887-889."
E["PRJ-R9-02"] = RE_READ + "test_project.py 82-89 docstring read; matches the fixture's behaviour."
E["PRJ-R9-03"] = RE_READ + "test_project.py:92 (@wraps(real)) and 319-326 (the wrapper's interaction with the tests) read."
E["PRJ-R9-04"] = RE_READ + "project.html:167 (Lab 1 interpretation) read against the printed output (expected block 156-166)."
E["PRJ-R9-05"] = RE_READ + "project.html:324 proof read line by line (see PRJ-D1-08)."
E["PRJ-R9-06"] = ("alts_r11_seeds0-49_r15.log and alts_repaired_r12fix_seeds0-49_r15.log and alts_original_r10_seeds0-49_r15.log re-run this round; "
    "exact alternatives pass 50/50; float alternatives fail only on the named gamma 1e-6 / 1e-9 forms (ruling 10 classification, see PRJ-D1-38 and PRJ-R10-02).")
E["PRJ-R9-07"] = MUT + "The final folder holds 205 pre-existing and 3 round-15 mutants; 208 of 208 killed."
E["PRJ-R9-08"] = "pytest --collect-only: 364 tests collected for every seed 0-49 (instances50_collect50_r15.py output; the count line differs only in the timing text)."
E["PRJ-R9-09"] = "run_labs.py --unit M7 PASS; project.html lab blocks 53-285 and 372-445 equal the twins (twin_vs_page_r15.py)."
E["PRJ-R9-10"] = "page_smoke.py --unit M7 --pages project PASS (Pyodide: 364 tests pass in the browser)."
E["PRJ-R9-11"] = RE_READ + "test_project.py 274-311 hand-case comments read; each comment matches the worked answer."
E["PRJ-R10-01"] = ("Exact-Fraction alternatives in ledgers/M7/scripts/M7-d-r10/alts (alt_B, alt_G, alt_H, alt_I, alt_J) re-run on seeds 0-49: 50/50 each (alts_r12_r10_exact_seeds0-49_r15.log). "
    "The r12 exact alternatives alt_r12_1 and alt_r12_2 also pass 50/50.")
E["PRJ-R10-02"] = ("Float alternatives: the original r10 set (alt_A, C, D, E, F) passes 0 of 50 seeds, failing on the named valid forms gamma = 1e-6 and 1e-9 (alts_r12_r10_exact_seeds0-49_r15.log; project.html:326). "
    "The repaired variants (r12fix A, C, D, E, F) pass 50/50 (alts_repaired_r12fix_seeds0-49_r15.log). Classified as student errors under ruling 10 (the round-14 record); the five r10 originals are not over-constraint. Ruling 10 text not available to this verifier; the originals should be filed under ledgers/M7/mutants.")
E["PRJ-R10-03"] = MUT + "r10_01..r10_03 killed."
E["PRJ-R10-04"] = MUT + "All 208 mutants are killed."
E["PRJ-R10-05"] = "run_graders.py --unit M7 --seeds 0-49 PASS (reference 50/50, run_graders_M7_seeds0-49_r15.log); mypy --strict on test_project.py and instance.py in a scratch workspace: no issues (mypy_strict_m7_grader_r15.log)."
E["PRJ-R10-06"] = ("ruff check . PASS (ruff_check_r15.log); ruff format --check . PASS (554 files, ruff_format_r15.log); mypy --no-incremental PASS on 385 files (mypy_r15.log); "
    "verify_refs.py --offline PASS, 560 entries, 0 problems (verify_refs_offline_r15.log).")
E["PRJ-R11-01"] = ("Round-11 nine solvers re-run on seeds 0-49 (alts_r11_seeds0-49_r15.log): alt1, alt2, alt6, alt8, alt9 pass 50/50; alt3, alt4, alt5, alt7 fail only on the named gamma 1e-6 / 1e-9 forms. "
    "Ruling 10 classification as in PRJ-D1-38; the five required alternatives of plan 7.4.2 pass (PRJ-R14-15).")
E["PRJ-R11-02"] = MUT + "r11_01, r11_03, r11_05, r11_06 killed."
E["PRJ-R11-03"] = RE_READ + "project.html:326 gamma valid form versus EXACT_BOUNDARIES (gamma 1e-9, test_project.py 654-656, 679) and NAMED_CONDITIONS gamma 1e-6 (640-641): consistent."
E["PRJ-R11-04"] = "Default pytest assertion mode (no --assert=plain) on the reference, seed 3: 364 passed (default_mode_reference_seed3_r15.log)."
E["PRJ-R12-01"] = "instances50_collect50_r15.py: make_instance valid, labelled and deterministic for seeds 0-49 (50 of 50); run_graders PASS on seeds 0-49."
E["PRJ-R12-02"] = "plans/M7-build-plan.md:223-232 (section 7.4) read: item 2 requires five alternative correct implementations, each a different method, passing seeds 0-49; the five plan alternatives (r14 alt1-alt5) pass 50/50 (alts_front_end_seeds0-49_r15.log)."
E["PRJ-R12-03"] = "Exact and float active-set alternatives on seeds 0-49: exact r14 alt1, r12 alt_r12_1 and alt_r12_2 and r10 alt_B, G, H, I, J pass 50/50; the repaired float alternatives pass 50/50 (alts logs in ledgers/M7/scripts/M7-d-r15)."
E["PRJ-R12-04"] = ("Float alternatives alt_r12_3..7 (ledgers/M7/scripts/M7-d-r12/alts) re-run: 37, 40, 38, 40, 41 of 50 seeds pass, failing only on the named gamma 1e-6 / 1e-9 forms (alts_r12_r10_exact_seeds0-49_r15.log). "
    "Classified as student errors under ruling 10, as in PRJ-R10-02.")
E["PRJ-R12-05"] = MUT + "v12_02, v12_03, v12_04, v12_05 killed."
E["PRJ-R12-06"] = ("ledgers/M7/equivalent/v12_01_dual_residual_reported_without_the_floor_at_zero.py now lives in the equivalent folder with a README section. "
    "The argument holds: F2 (README) is exact, the smallest inequality multiplier is 0 on every reference output (equiv_recheck_r15.py: 0 of 400 answers with a non-zero minimum), and v12_01 never differs from the reference beyond 1e-9 (0 of 400). Structural, not sampled.")
E["PRJ-R12-07"] = "pytest --collect-only for seeds 0-49: 364 tests on every seed (instances50_collect50_r15.py)."
E["PRJ-R12-08"] = "twin_vs_page_r15.py: page code and expected blocks of Labs 1-3 equal the twins (Lab 2 differs only by its blanks)."
E["PRJ-R12-09"] = "Printed numbers of Lab 1 and Lab 3 re-derived with exact Fractions in the lab runs (run_labs PASS); -3/220 = -0.0136363..., 9/550, 9/1100, 1/6250 checked by hand."
E["PRJ-R12-10"] = RE_READ + "project.html:323-325 proposition graded T; proof checked step by step; hypotheses complete (see PRJ-D1-08)."
E["PRJ-R12-11"] = RE_READ + "project.html:292-300 inputs and outputs versus instance.py fields (gamma, mu, sigma, w0, lower, upper, sector, sector_caps, turnover_limit, label, payload) and test_project.py output_shape: consistent."
E["PRJ-R12-12"] = RE_READ + "project.html:326 named conditions versus NAMED_CONDITIONS, OTHER_SIDE_REFUSED and EXACT_BOUNDARIES: consistent."
E["PRJ-R12-13"] = "page_smoke.py --unit M7 --pages project: in-browser grader 364 tests in 2.3 s (page_smoke_project_r15.log); plan 7.3 limits are met."
E["PRJ-R12-14"] = "project.html:465-466 data-cite keys boyd2004convex and stokey1989recursive: both present in references/references.json; verify_refs.py --offline and --unit M7 PASS."
E["PRJ-R12-15"] = "project.html:310 link to L03.html: course/modules/M/M7/L03.html line 62 defines the Lagrangian of (P) and the KKT point."
E["PRJ-R14-01"] = ("ledgers/M7/equivalent/ exists with README.md (10007 bytes) and the nine candidate files; the location requirement is met. The proofs are assessed in PRJ-D1-37 and PRJ-R15-02 (the two false proofs are not in this row).")
E["PRJ-R14-02"] = RE_READ + "project.html:167, 172, 310 multiplier references versus the Conventions at 310: consistent."
E["PRJ-R14-03"] = RE_READ + "project.html:444 Lab 3 interpretation versus the printed lines (441-443) and the residuals() definition at project.html:401-415 (stationarity is the largest absolute expression; complementary is the largest absolute product): consistent with the output."
E["PRJ-R14-04"] = RE_READ + "project.html:169-285 Lab 2 blanks versus tests/labs/M7/lab-M7-project-2.py (diff shows only the three blanks)."
E["PRJ-R14-05"] = MUT + "w14d_01, w14d_02, w14d_03 killed."
E["PRJ-R14-06"] = "pytest --collect-only for seeds 0-49: 364 checks on every seed (instances50_collect50_r15.py); project.html:332 states 364."
E["PRJ-R14-07"] = RE_READ + "project.html:450 'every case carries the SIMULATED label': instance.py label on 50 of 50 seeds and hand-case labels (test_project.py 261, 282) confirmed."
E["PRJ-R14-08"] = RE_READ + "project.html:326 'other invalid inputs... raise an exception that carries a message' versus test_project.py 864-906 and 879-906: consistent."
E["PRJ-R14-09"] = "check_projects.py --unit M7 PASS (rubric checks not applicable: grading autograder); curriculum/01-foundations.yaml:318-327 M7 entry read (grading: autograder)."
E["PRJ-R14-10"] = "curriculum/meta.yaml read for M7 (no atlas block for this project); check_projects.py --unit M7 PASS."
E["PRJ-R14-11"] = RE_READ + "project.html:344-350 verifier estimate re-derived (see PRJ-R7-07)."
E["PRJ-R14-12"] = GATES
E["PRJ-R14-13"] = "page_smoke.py --unit M7 --pages project: the in-browser suite runs in 2.3 s on a seed (page_smoke_project_r15.log), well under plan 7.3 limits."
E["PRJ-R14-14"] = "run_labs.py --unit M7 PASS (11/11); pytest tests/test_labs.py -k M7: exit 0, 11 passed."
E["PRJ-R14-15"] = "plan 7.4.2 five alternatives (r14 alt1-alt5): each passes all 364 checks on seeds 0-49 (alts_front_end_seeds0-49_r15.log: 50/50 each), ruling 19 applied."
E["PRJ-R14-16"] = "ledgers/M7/scripts/M7-d-r14/alts: five front-end solvers 50/50 (alts_front_end_seeds0-49_r15.log); five repaired float variants 50/50 (alts_repaired_r12fix_seeds0-49_r15.log)."
E["PRJ-R14-18"] = "references/references.json has boyd2004convex and stokey1989recursive; verify_refs.py --unit M7 (live): 2 of 560 entries, 0 problems (verify_refs_M7_live_r15.log)."

NEW = []
def new(id_, check, location, status, evidence, fix=""):
    NEW.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})

new("PRJ-R15-01", "2.6-autograder", "course/modules/M/M7/grader/reference.py:204 (initial working set, <= TOL) and :21, :1-8 docstring", "FAIL",
    "Page-valid inputs on which the reference returns a non-optimal, uncertified answer. (A) gamma=1, Sigma=I, mu=[1000,0], w0=(1/2,1/2), tau=1e-9: reference returns (1/2,1/2); reported and recomputed complementary slackness 5e-7 > 1e-8 (project.html:321). Exact Fractions: f(w0 + (tau/2)(1,-1)) - f(w0) = -5e-7 (tiny_tau_probe_r15.log; feasible point, so w0 is not optimal). "
    "(E) same mu, upper bound on asset 0 = 1/2 + 1e-9, tau=2: reference returns (1/2,1/2), complementary 1e-6, objective gap -1e-6. Cause: line 204 admits a row whose slack is positive (<= TOL) into the working set, so its multiplier can be positive while the constraint is slack. The docstring at the top of reference.py says every active-set decision is exact, which line 204 contradicts. "
    "No test in the suite uses such an input, so the suite accepts this solver (and would fail its own assert_kkt on these inputs). Generator cases (mu <= 0.04) are not affected.",
    "Admit to the initial working set only rows whose slack is exactly zero (b - a.x == 0), after snapping a start that violates a bound or sector cap by at most TOL onto that limit (so the start is exactly feasible); correct the module docstring. Add two hand cases to test_project.py: mu=[1000,0], tau=1e-9 (expected weights (1/2+5e-10, 1/2-5e-10)) and mu=[1000,0], upper=[1/2+1e-9, 2] (expected (1/2+1e-9, 1/2-1e-9)). Then re-run run_graders --seeds 0-49, mutate_graders and the five alternatives.")
new("PRJ-R15-02", "2.6-mutation", "ledgers/M7/equivalent/r05_turnover_total_slackness_term_zeroed.py; ledgers/M7/equivalent/v10_02_complementary_slackness_signed_not_absolute.py; ledgers/M7/equivalent/README.md proofs 7 and 8", "FAIL",
    "Both files are NOT equivalent to the reference on page-valid inputs, so they cannot be kept as equivalent mutants (VERIFIER_RULES 2.6(3)). tiny_tau_probe_r15.log: case A (tau=1e-9, mu=[1000,0]): r05 and v10_02 report complementary 0 against recomputed 5e-7 (agreement fails at 1e-9); case B (tau=1e-10, mu=[100,0]): both report 0 against 5e-9. "
    "equiv_recheck_r15.py (400 random page-valid cases): r05 distinguished in 9, v10_02 in 23. The README's bound 'multiplier times slack <= 1e-9' is false because the multiplier is not bounded by 1 (kappa = 500 in case A). Neither mutant is killed by the suite, so both survive on valid inputs that the page allows (project.html:318 states the complementary-slackness definition these mutants violate).",
    "Remove both from ledgers/M7/equivalent/ and list them in ledgers/M7/mutants/ with their docstring descriptions. Kill them with the PRJ-R15-01 hand cases (the page-valid tau=1e-9 input). After PRJ-R15-01 is fixed, re-prove them: with an exact active set, kappa > 0 forces sum|d_i| = tau and every product m*g is exactly zero, which may make them equivalent; if so, cite that argument in the README and keep them out of mutants. Correct README proofs 7 and 8 and the 'Corrections' section.")
new("PRJ-R15-03", "2.6-mutation", "ledgers/M7/mutants/r15_01_sector_cap_start_tolerance_1e-8.py, r15_02_start_budget_check_tolerance_1e-6.py, r15_03_only_first_sector_cap_checked_at_start.py", "PASS",
    "Three verifier-written student-error mutants (generated by ledgers/M7/scripts/M7-d-r15/make_r15_mutants.py from the reference): sector-cap start tolerance 1e-8 (killed on seed 0 by test_named_condition_is_refused_with_value_error[start-within-sector-cap-invalid]); start budget tolerance 1e-6 (killed by test_named_condition_is_refused_with_value_error[start-sums-to-one-invalid]); only the first sector cap checked at start (killed by test_named_condition_other_side_is_refused_with_value_error[start-within-sector-cap-last-sector]). 0 of 10 seeds pass each (new_mutants_r15_seeds0-9.log).")
new("PRJ-R15-04", "2.6-mutation", "ledgers/M7/equivalent/ (q04, r02, r04, s12_03, v10_01, v11_01, v12_01)", "PASS",
    "Equivalence proofs that hold: F2 (README) is exact on every reference output (smallest inequality multiplier exactly 0 on 400 of 400 random answers; equiv_recheck_r15.py), so q04, v11_01, v10_01, s12_03 and v12_01 are structurally equal to the reference on the dual and turnover-multiplier fields, and r02 is equal because the turnover gap is <= 0 (F4). r04 differs only by |sum(w0) - 1| <= 1e-9 (reference.py:102), inside the page's agreement tolerance (project.html:321); observed max difference 8e-14 on 400 cases. Source of each file is byte-identical to git 5e18d08d (equiv_sources_r15.log).")

ROWS = []
for i in prev_ids:
    if i in ("PRJ-D1-37", "PRJ-D1-39"):
        continue  # written below with FAIL status
    ROWS.append({"id": i, "check": prev_check[i], "location": prev_loc[i], "status": "PASS", "evidence": E[i], "fix": ""})
FAIL_D1_37 = {"id": "PRJ-D1-37", "check": "2.6-mutation", "location": "ledgers/M7/equivalent/README.md; ledgers/M7/equivalent/r05_turnover_total_slackness_term_zeroed.py; ledgers/M7/equivalent/v10_02_complementary_slackness_signed_not_absolute.py",
    "status": "FAIL", "evidence": E["PRJ-D1-37"],
    "fix": "The folder and sources now exist, but two of the eight removed mutants are not equivalent (r05, v10_02): move both to ledgers/M7/mutants/ and kill them (see PRJ-R15-02), and correct README proofs 7 and 8. Keep the other six proofs; r04 is equal only up to the 1e-9 agreement tolerance, which the README states."}
FAIL_D1_39 = {"id": "PRJ-D1-39", "check": "2.9-structure", "location": "BLUEPRINT.md:400-401; course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml",
    "status": "FAIL", "evidence": E["PRJ-D1-39"],
    "fix": "Make the publish step exclude every grader/reference.py (for example copy course/ to the published directory minus grader/reference.py, or move reference solutions out of course/ and have run_graders.py and page_smoke.py read them from there), and add a CI assertion that no grader/reference.py exists under the published tree. Until then, state where the deploy configuration lives so the requirement can be checked."}
# insert the FAIL rows back in the original order
out_rows = []
for i in prev_ids:
    if i == "PRJ-D1-37":
        out_rows.append(FAIL_D1_37)
    elif i == "PRJ-D1-39":
        out_rows.append(FAIL_D1_39)
    else:
        out_rows.append(next(r for r in ROWS if r["id"] == i))
# R14-01 (umbrella) location now exists: PASS with the proof problems referenced
for r in out_rows:
    if r["id"] == "PRJ-R14-01":
        r["status"] = "PASS"; r["fix"] = ""
out_rows += NEW

mutants = []
pat = re.compile(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$")
for line in (S / "mutate_graders_M7_0-9_r15.log").read_text(encoding="utf-8").splitlines():
    m = pat.match(line)
    if m:
        mutants.append({"id": m.group(2), "description": m.group(3), "killed_by": None if m.group(1) == "SURVIVED" else m.group(4)})
new_block = (S / "new_mutants_r15_seeds0-9.log").read_text(encoding="utf-8").splitlines()
for line in new_block:
    if line.startswith("r15_0") and "seeds passing 0/10" in line:
        name = line.split(":")[0]
        seed0 = next(x for x in new_block[new_block.index(line) + 1:] if x.strip().startswith("seed 0:"))
        killed = seed0.split(":", 1)[1].split(",")[0].strip()
        doc = (ROOT / "ledgers/M7/mutants" / name).read_text(encoding="utf-8").split("\n", 1)[0].strip('"')
        mutants.append({"id": name, "description": doc, "killed_by": f"{killed} (seed 0)"})
assert len(mutants) == 208, len(mutants)

counts = {"PASS": sum(r["status"] == "PASS" for r in out_rows), "FAIL": sum(r["status"] == "FAIL" for r in out_rows)}
fragment = {
    "unit": "M7", "slice": "d", "round": 15,
    "verifier": "Haiku 5.5 independent verifier (round 15, slice d); did not build M7-d",
    "pin": "dde0486b (dde0486beeb0312e4ac1cc03aaa02e56644adb24); delta from 1431aa1d (round-14 pin)",
    "base": "1431aa1d (1431aa1d842a5d2d05fd5953c098500bf78a4307); round-14 fragment D-M7-d.round14.json used as context only",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD15-M7-d",
    "scratch": "ledgers/M7/scripts/M7-d-r15/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": "FAIL" if counts["FAIL"] or any(r["status"] != "PASS" for r in out_rows) else "PASS",
    "rows": out_rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 1431aa1d..dde0486b for slice d: ledgers/M7/equivalent/ (new README and nine files), ledgers/M7/mutants/ (three w14d files were already there at the previous base; no change to project.html, grader/*, tests/labs/M7/*, tools/*, references, notation or curriculum M7 entries: git diff empty). "
        "Read in full this round: project.html, grader/test_project.py, instance.py, starter.py, reference.py (1-380). Round-14 PASS rows were not copied; each was re-checked against the subject or a command in this round. "
        "Rulings: 9 and 22 applied to the equivalence folder (README form); 19 applied to the front-end solvers (float feasibility and dual checks with tolerance); 10 applied to the float alternatives that fail only on the named gamma 1e-6 / 1e-9 forms (their text is not available to this verifier; the classification is taken from the round-14 record and PRJ-D1-38, PRJ-R10-02, PRJ-R12-04 depend on it); 25 is cited by the README but its text is not available to this verifier, so the r04 tolerance argument is checked only to the extent stated in PRJ-R15-04. "
        "Not checked: repository-wide pytest (only tests/test_labs.py -k M7); full Chromium page_smoke for L01-L08 (other slices); cards (out of slice); the deploy configuration (not in the repository, see PRJ-D1-39); the exact text of rulings 10, 19, 22 and 25; the four original r10 float alternatives were not filed under mutants (recommended). "
        "The ledgers/M7/M7-d.json in the checkout at the pin was another lineage and is replaced by this fragment. The five alternatives of plan 7.4.2 are the r14 alt1..alt5 solvers (all 50/50)."
    ),
    "summary": {
        "rows": len(out_rows), "pass": counts["PASS"], "fail": counts["FAIL"], "unverifiable": 0,
        "mutants": len(mutants), "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"], fragment["verdict"])
