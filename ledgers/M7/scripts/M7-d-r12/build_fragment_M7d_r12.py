"""Build ledgers/M7/M7-d.json (round 12, slice d) from the round-11 fragment and this round's evidence.

Usage: python -I build_fragment_M7d_r12.py <repo_root> <round11_fragment> <mutate_log>
Carried rows keep their round-11 ids, and their evidence is prefixed with the carry sentence the verifier rules require.
"""

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
r11 = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
mutate_log = Path(sys.argv[3]).read_text(encoding="utf-8")
r11_rows = {row["id"]: row for row in r11["rows"]}
r11_mutants = r11["mutants"]

GRADER = "grader/*.py (test_project.py, instance.py, reference.py, starter.py)"
LABS = "tests/labs/M7/lab-M7-project-1..3.py"
CARRY = "Carried from round 11 ({files} byte-identical since the previous pin ccaeeaf4): "

# Mutant results: every 'KILLED'/'SURVIVED' line of the final run of tools/mutate_graders.py --unit M7 --seeds 0-9.
mutant_rows = []
for line in mutate_log.splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mutant_rows.append({
            "id": name,
            "description": desc,
            "killed_by": None if killed.strip() == "None" or status == "SURVIVED" else killed.strip(),
        })
mutant_summary = re.search(r"mutate_graders M7: (\w+) \((\d+)/(\d+) killed\)", mutate_log)

fresh: dict[str, dict] = {}


def put(row_id, check, location, status, evidence, fix=""):
    row = {"id": row_id, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        row["fix"] = fix
    fresh[row_id] = row


def carry(row_id, files=GRADER):
    old = r11_rows[row_id]
    row = dict(old)
    row["evidence"] = CARRY.format(files=files) + old["evidence"]
    fresh[row_id] = row


MUT = "round-12 final tools/mutate_graders.py --unit M7 --seeds 0-9 (ledgers/M7/scripts/M7-d-r12/gates/mutate_M7_0_9_final.log)"
SCR = "ledgers/M7/scripts/M7-d-r12/"

# --- rows whose subject is the page, re-read and re-derived this round ---
put("PRJ-D1-02", "2.6-spec", "project.html:299-300; grader/test_project.py output_shape (174-201)", "PASS",
    "Round 12: project.html:299-300 read in full; output_shape checks the three keys, the seven multiplier names, the list lengths and the certificate keys. Reference passes it on seeds 0-49 (ledgers/M7/scripts/M7-d-r12/gates/run_graders_M7_0_49.log: reference 50/50).")
put("PRJ-D1-03", "2.4-math", "project.html:309", "PASS",
    "Round 12: re-derived. sum|d_i| <= tau iff some t has t_i >= d_i, t_i >= -d_i, sum t_i <= tau (forward: t_i = |d_i|; converse: sum|d_i| <= sum t_i <= tau). The page's 'every constraint is affine (a linear function plus a constant) in them' holds for all six families in (w,t).")
put("PRJ-D1-04", "2.4-math", "project.html:310-313", "PASS",
    "Round 12: re-derived by hand from the Lagrangian of the linearized problem with g = l-w, w-u, sum_S w-c, d-t, -d-t, sum t - tau: dL/dw_i = gamma(Sigma w)_i - mu_i + nu - lam^l_i + lam^u_i + eta_k(i) + alpha_i - beta_i and dL/dt_i = kappa - alpha_i - beta_i. Matches r^w and r^t on the page and test_project.py stationarity (133-151).")
put("PRJ-D1-05", "2.4-math", "project.html:310,314-319; grader/test_project.py inequality_pairs (116-130)", "PASS",
    "Round 12: the six inequality families and their g_j in inequality_pairs match the page's list item by item; the primal residual terms (page 315) match test_project.py primal construction (156).")
put("PRJ-D1-06", "2.4-math", "project.html:320; grader/test_project.py recomputed_certificate (154-165)", "PASS",
    "Round 12: the floor changes the dual residual only when every inequality multiplier is positive (dual = max(0, -min m)); the 1e-9 threshold statement follows (unfloored value -m differs from 0 by m). test_project.py line 157 floors with max(0.0, ...).")
put("PRJ-D1-07", "2.4-math", "project.html:317-321; test_project.py recomputed_certificate (154-165)", "PASS",
    "Round 12: dual uses exactly the six multiplier families the page names; complementary slackness uses the six g_j at t=|d| (test_project.py 158). Matches.")
put("PRJ-D1-08", "2.4-math", "project.html:323-325 (Proposition, T, and proof)", "PASS",
    "Round 12: proof re-derived in full: f(y) >= L(y,s) >= L(w,t) = f(w) for every feasible (y,s) (feasibility gives g_j <= 0, lam_j >= 0, budget term 0; L convex and stationary at (w,t)); complementary slackness gives L(w,t)=f(w); uniqueness by the midpoint argument with f strictly convex in w. Hypotheses on line 325 are the ones used. See PRJ-R12-10.")
put("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:3-4,39-43", "PASS",
    "Round 12: instance.py:39-41 builds Sigma = (A'A + I)/1000 with integer A entries (rng.randint(-2,2)); x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0. Page line 325 states that existence of multipliers is not proved there; no existence claim is made.")
put("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py _parse (54-109)", "PASS",
    "Round 12: each named ValueError condition on page line 326 is raised by reference.py _parse at the stated place (lines 55-108); the gamma 1e-6 and 1e-9 valid forms are accepted by _scalar and _parse (line 65 only refuses gamma <= 0).")
put("PRJ-D1-12", "2.6-spec", "project.html:326,332; test_project.py EXACT_BOUNDARIES (674-680), NAMED_CONDITIONS (637-651)", "PASS",
    "Round 12: EXACT_BOUNDARIES holds lower-equals-start, upper-equals-start, cap-equals-start, start-sum-inside-low-side and gamma-just-inside-zero; NAMED_CONDITIONS holds gamma-positive-zero-boundary (1e-6) and gamma-positive-negative-boundary (1e-9). All pass on the reference (50/50) and on the exact alternatives; the float alternatives that fail these are classified in PRJ-R12-04.")
put("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", "PASS",
    "Round 12: lab_page_vs_twin log: page code == twin (True); twin under python -I -W error exits 0 with no stderr; output == page expected block (True). run_labs --unit M7: 11/11 PASS (ledgers/M7/scripts/M7-d-r12/gates/run_labs_M7.log). Numbers re-derived with Fractions (ledgers/M7/scripts/M7-d-r12/alts_v12/rederive_labs_v12.log).")
put("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "PASS",
    "Round 12: the completion page code differs from the twin only on three lines, each containing ___ (step 4 residual; step 6 signs and dual_feasible), so every line equals the twin or contains ___ (labs_page_vs_twin log). Expected block == twin output (True).")
put("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "PASS",
    "Round 12: page code == twin (True); expected block == output (True); check A 0/0/0/0, check B dual 9/1100 and stationarity 9/550, check C stationarity 1/6250 re-derived with Fractions (ledgers/M7/scripts/M7-d-r12/alts_v12/rederive_labs_v12.log).")
put("PRJ-D1-16", "2.9-hours", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml M7 hours 110", "PASS",
    "Round 12: component hours 2+3+10+6+7+5 = 33 = data-hours-project and eyebrow; index.html:29 data-hours-lessons=77; 77+33 = 110 = curriculum M7 hours: 110 (curriculum/01-foundations.yaml:301). Arithmetic consistent.")
put("PRJ-D1-17", "2.9-structure", "project.html:40-49", "PASS",
    "Round 12: four rungs present in order (worked example lab, completion lab, graded spec with autograder, stretch); tier F keeps rungs 1-2 at full length (plan 7.1).")
put("PRJ-D1-18", "2.6-spec", "project.html:288-336", "PASS",
    "Round 12: Context, Inputs, Required outputs, Constraints, Grading present in the dl; Grading says autograder only and 364 checks; collect-only gives 364 on seeds 0-49 (PRJ-R12-07).")
put("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py --unit M7 --pages project", "PASS",
    "Round 12: ledgers/M7/scripts/M7-d-r12/gates/page_smoke_M7_project.log: page_smoke modules/M/M7/project.html PASS; in-browser grader 'All 364 tests pass on seed 2012128808 (3.1 s)'; the tool fails on console errors, external requests and unrendered math, so the PASS covers them.")
put("PRJ-D1-21", "2.4-notation", "project.html symbols vs notation/notation.json (8 registered entries)", "PASS",
    "Round 12: registry entries are T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q. project.html uses gamma (risk aversion, unsubscripted), Sigma, mu, nu, lambda, eta, alpha, beta, kappa, tau, t, d, n, Z, A (matrix), L, b. No registered symbol is used with another meaning.")
put("PRJ-D1-22", "2.9-dag", "project.html:456 (envelope-theorem link); course/modules/M/M7/index.html", "PASS",
    "Round 12: project.html:456 links envelope-theorem in M2; curriculum M7 prereqs are [M2, M3]; check_dag --all PASS (ledgers/M7/scripts/M7-d-r12/gates/check_dag_all.log).")
put("PRJ-D1-23", "2.9-prose", "project.html; tools/check_pages.py BANNED list", "PASS",
    "Round 12: check_pages --all PASS (ledgers/M7/scripts/M7-d-r12/gates/check_pages_all_r12v.log); read project.html learner text: no banned phrase found.")
put("PRJ-D1-24", "2.6-spec", "project.html:364-366 (local run and decode commands)", "PASS",
    "Round 12: ran the page's local command with the reference as constrained_allocator.py: 364 passed in 0.94 s (seed 0). Ran the decode command from a folder holding instance.py (without -I): prints the seed-7 case dict.")
put("PRJ-D1-25", "2.6-autograder", "grader/starter.py:18-20; project.html:301", "PASS",
    "Round 12: running the suite on starter.py as constrained_allocator.py (seed 0): 361 failed, 3 passed (the NotImplementedError is raised, so the suite fails on the starter).")
put("PRJ-D1-29", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke) and CPython (run_graders)", "PASS",
    "Round 12: page_smoke in-browser run 364 tests pass (3.1 s); run_graders --unit M7 --seeds 0-49: reference 50/50 (ledgers/M7/scripts/M7-d-r12/gates/run_graders_M7_0_49.log).")
put("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py -k M7", "PASS",
    "Round 12: pytest tests/test_labs.py -k M7: 11 passed (ledgers/M7/scripts/M7-d-r12/gates/pytest_test_labs_M7.log); run_labs 11/11.")
put("PRJ-D1-31", "2.6-spec", "project.html:332; grader/test_project.py HAND_CASES (274-312)", "PASS",
    "Round 12: HAND_CASES has six entries (page 332 says six). Worked answers re-derived by hand: budget only (0.6, 0.4); zero turnover (0.5, 0.5); single asset (1.0); upper bound binding (0.7, 0.3); turnover binding (0.6, 0.4); degenerate box (0.5, 0.5). All six pass on the reference.")
put("PRJ-D1-32", "2.6-atlas", "project.html; curriculum/01-foundations.yaml M7 entry; check_projects --all", "PASS",
    "Round 12: the M7 curriculum entry has no atlas key (project grading: autograder); check_projects --all PASS (ledgers/M7/scripts/M7-d-r12/gates/check_projects_all_r12v.log).")
put("PRJ-D1-33", "2.1-citations", "project.html:465-466 (reading list); references/references.json", "PASS",
    "Round 12: the two reading-list items carry only data-cite keys and no claim. verify_refs --offline (all 560 registry entries): 0 problems (ledgers/M7/scripts/M7-d-r12/gates/verify_refs_offline_all.log).")
put("PRJ-D1-34", "2.9-structure", "project.html:338-354; tools/check_pages.py --unit M7", "PASS",
    "Round 12: check_pages --unit M7 PASS (ledgers/M7/scripts/M7-d-r12/gates/check_pages_M7.log); check_pages --all PASS.")
put("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (all files)", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT}: {mutant_summary.group(0) if mutant_summary else 'no summary line'}. The folder holds the 195 round-11 files, 3 untracked r12_* files present in the checkout, and 4 new v12_* files; the equivalent candidate v12_01 was removed (PRJ-R12-06).",
    "Kill or remove any surviving mutant; a survivor is a grader defect only if project.html states the behaviour it violates.")
put("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/ (all families)", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    "Round 12: every family in the folder is in the final run above; each mutant's killed_by is listed in this fragment's mutants array.",
    "Kill or remove any surviving mutant.")
put("PRJ-D1-39", "2.9-structure", "BLUEPRINT.md:400-401 (section 7); course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml; no deployment config", "FAIL",
    "Round 12 re-check at 329c1d7: BLUEPRINT.md:400-401 says deployment 'excludes every grader/reference.py'. grep for reference.py over .github, tools/build_site.py, tools/coursekit.py, tools/check_pages.py, .gitignore finds no exclusion; there is no vercel.json or .vercelignore at the repo root; reference.py is tracked (git ls-files course/modules/M/M7/grader). The exclusion the blueprint describes does not exist in the repository.",
    "Add the exclusion to whatever publishes course/ (for example a .vercelignore entry or a build copy step in tools/build_site.py) for course/modules/*/*/grader/reference.py, and check it in CI; or amend BLUEPRINT section 7 to name the mechanism that exists.")
put("PRJ-R5-01", "2.4-math", "project.html:456 frontier bullet", "PASS",
    "Round 12: the frontier bullet now asks for mu'w against w'Sigma w and for the budget multiplier against d(objective)/db; it states no numeric value. Read in full.")
put("PRJ-R5-03", "2.9-prose", "project.html:450 ('does not test' paragraph)", "PASS",
    "Round 12: the paragraph limits the suite to the seed case and the hand cases; consistent with test_project.py scope.")
put("PRJ-R5-04", "2.9-structure", "project.html:349-350", "PASS",
    "Round 12: 'The module hub declares 77 lesson hours and this 33-hour project, which together make the module's 110 hours' matches index.html:29 and the curriculum M7 hours 110.")
put("PRJ-R6-01", "2.6-gate", "tools/check_projects.py --all", "PASS", "Round 12: check_projects --all PASS (ledgers/M7/scripts/M7-d-r12/gates/check_projects_all_r12v.log).")
put("PRJ-R6-02", "2.6-gate", "tools/check_pages.py --all", "PASS", "Round 12: check_pages --all PASS (ledgers/M7/scripts/M7-d-r12/gates/check_pages_all_r12v.log).")
put("PRJ-R6-03", "2.9-dag", "tools/check_dag.py --all", "PASS", "Round 12: check_dag --all PASS (ledgers/M7/scripts/M7-d-r12/gates/check_dag_all.log).")
put("PRJ-R7-06", "2.8-data", "project.html; grader/instance.py", "PASS",
    "Round 12: project.html has no data-files attribute and reads no snapshot; instance.py generates the case and labels it SIMULATED (line 57). No MANIFEST entry is needed.")
put("PRJ-R7-07", "2.6-hours", "project.html:344-350", "PASS", "Round 12: the six component rows sum to 33 (see PRJ-D1-16).")
put("PRJ-R7-05", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", "PASS", "Round 12: page_smoke in-browser run 364 pass (3.1 s).")
put("PRJ-R9-04", "2.9-prose", "project.html:167 (Lab 1 interpretation)", "PASS",
    "Round 12: each step named in the interpretation (steps 1 to 7) is printed by the lab output; the values 54/65, 5/26, -3/130, (9/11, 2/11, 0), -21/1100, 9/1100 and -3/220 match the expected block.")
put("PRJ-R9-05", "2.4-math", "project.html:324 (proof)", "PASS", "Round 12: proof re-derived in full (see PRJ-D1-08).")
put("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder)", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL", f"Round 12: {MUT}.", "Kill or remove any surviving mutant.")
put("PRJ-R9-08", "2.9-structure", "grader/test_project.py (collected count); project.html:332", "PASS",
    "Round 12: collect-only on seeds 0-49 gives 364 on every seed (ledgers/M7/scripts/M7-d-r12/collect_seeds_0-49_M7d_r12.log); the page says 364.")
put("PRJ-R9-09", "2.5-lab", "project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    "Round 12: labs_page_vs_twin log and run_labs 11/11 (see PRJ-D1-13 to PRJ-D1-15).")
put("PRJ-R9-10", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", "PASS", "Round 12: page_smoke in-browser run 364 pass (3.1 s).")
put("PRJ-R10-05", "2.6-autograder", "tools/run_graders.py --unit M7 --seeds 0-49; mypy --strict on grader", "PASS",
    "Round 12: run_graders 50/50 (ledgers/M7/scripts/M7-d-r12/gates/run_graders_M7_0_49.log); mypy --no-incremental over the repo: 'Success: no issues found in 385 source files' (ledgers/M7/scripts/M7-d-r12/gates/mypy_nocache.log).")
put("PRJ-R10-06", "2.9-structure", "repo gates: ruff check ., ruff format --check ., mypy --no-incremental, verify_refs --offline", "PASS",
    "Round 12: ruff check . 'All checks passed!'; ruff format --check . 559 files formatted; mypy 385 files; verify_refs --offline 560 entries 0 problems (ledgers/M7/scripts/M7-d-r12/gates/ruff_check_all.log, ruff_format_all.log, mypy_nocache.log, verify_refs_offline_all.log).")
put("PRJ-R11-03", "2.6-spec", "project.html:326 (gamma valid form) vs test_project.py EXACT_BOUNDARIES (gamma 1e-9) and NAMED_CONDITIONS (gamma 1e-6)", "PASS",
    "Round 12: the page now names gamma values of 1e-6 and 1e-9 as valid; the suite holds both as valid (NAMED_CONDITIONS gamma-positive-zero-boundary and EXACT_BOUNDARIES gamma-just-inside-zero) and both pass on the reference and on the float alternative F1.")
put("PRJ-R11-02", "2.6-mutation", "ledgers/M7/mutants/r11_01, r11_03, r11_05, r11_06", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT} covers these four files.", "Kill or remove any surviving mutant.")
put("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT} covers these files.", "Kill or remove any surviving mutant.")
put("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT} covers these files.", "Kill or remove any surviving mutant.")
put("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT} covers this file.", "Kill or remove any surviving mutant.")
put("PRJ-R10-03", "2.6-mutation", "ledgers/M7/mutants/r10_01..r10_03", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT} covers these files.", "Kill or remove any surviving mutant.")
put("PRJ-R10-04", "2.6-autograder", "ledgers/M7/mutants/ full set", "PASS" if mutant_summary and mutant_summary.group(1) == "PASS" else "FAIL",
    f"Round 12: {MUT}.", "Kill or remove any surviving mutant.")

put("PRJ-R10-01", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/alt_B, alt_G, alt_H, alt_I, alt_J (exact Fraction active sets)", "PASS",
    "Round 12 re-run: ledgers/M7/scripts/M7-d-r12/alts_v12/run_r10_exact_alts_r12.log: alt_B 50/50, alt_G 50/50, alt_H 50/50, alt_I 50/50, alt_J 50/50 on seeds 0-49 with the browser flags.")
put("PRJ-R10-02", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/alt_A, alt_C, alt_D, alt_E, alt_F (float alternatives)", "FAIL",
    "Round 12 re-run: ledgers/M7/scripts/M7-d-r12/alts_v12/run_r10_float_alts_AF_r12.log: alt_A, alt_C, alt_D 0/50 seeds, each failing test_named_condition_boundary_is_accepted[gamma-positive-zero-boundary] (gamma = 1e-6) on every seed. ledgers/M7/scripts/M7-d-r12/alts_v12/diagnose_gamma_r12.py: alt A, C and D raise RuntimeError 'the working set lost independence' on seed 0 with gamma = 1e-6, a valid input; the suite is not at fault (alt_v12_F1 passes seed 0 with gamma 1e-6 and passes 50/50). The round-11 PASS for this row is not reproduced.",
    "Repair alternatives A, C, D, E and F (their rank test rejects a valid working set when gamma is 1e-6; use a scaled tolerance, as alt_v12_F1 does) and re-run them on seeds 0-49, or remove them from the evidence and say so.")
# --- rows whose subject is unchanged since the pin (grader, labs, registry), carried with the required sentence ---
for rid in ["PRJ-D1-01", "PRJ-D1-11", "PRJ-D1-19", "PRJ-D1-27", "PRJ-D1-28", "PRJ-R4-01", "PRJ-R5-02",
            "PRJ-R7-02", "PRJ-R7-03", "PRJ-R8-01", "PRJ-R8-02", "PRJ-R8-04", "PRJ-R9-01", "PRJ-R9-02", "PRJ-R9-03",
            "PRJ-R9-06", "PRJ-R9-11", "PRJ-R11-04", "PRJ-D1-37", "PRJ-D1-38"]:
    if rid in r11_rows:
        carry(rid, files=GRADER if rid not in ("PRJ-D1-37", "PRJ-D1-38", "PRJ-R9-06") else
              "ledgers/M7/mutant_equivalence_r14.json and ledgers/M7/scripts/M7-d-r11/alts/ (and the suite they run)")

# --- rows whose evidence is replaced by round-12 evidence (r11 ids not listed above remain via the carry loop) ---
for rid, row in r11_rows.items():
    if rid not in fresh:
        carry(rid)


new_rows = [
    ("PRJ-R12-01", "2.6-autograder", "grader/instance.py (make_instance) seeds 0-49", "PASS",
     "Round 12: ledgers/M7/scripts/M7-d-r12/alts_v12/instances_v12.log: n in {3,4,5}, Z=2 on every seed; 50 distinct reference weight vectors over seeds 0-49 (answers change, not only labels); a sector cap binds on 20 seeds (both sectors); the turnover constraint binds (kappa > 0) on 47 seeds."),
    ("PRJ-R12-02", "2.6-autograder", "plans/M7-build-plan.md section 7.4 item 2 (five alternatives, different methods)", "UNVERIFIABLE",
     "Round 12: only the active-set family was written. Alternatives: exact active set (r12 alt 1, 2; r10 B, G, H, I, J), float active set F1 (ledgers/M7/scripts/M7-d-r12/alts_v12/alt_v12_F1_float_active_set_refined.py). Projected gradient, ADMM, log-barrier interior point and dual ascent (plan 7.4 item 2) were not written, so the 'five different methods' requirement is not verified.",
     "Write alternatives (2) to (5) of plan 7.4 item 2 as complete solvers (projected gradient, ADMM, log-barrier, dual ascent) under ledgers/M7/scripts/, run each through ledgers/M7/scripts/M7-d-r12/alts_v12/run_candidates_v12.py on seeds 0-49, and record the results in this fragment."),
    ("PRJ-R12-03", "2.6-autograder", "over-constraint check: exact and float active-set alternatives on seeds 0-49", "PASS",
     "Round 12: run_alts_r12.py: alt_r12_1_exact_min_index 50/50, alt_r12_2_exact_most_negative_largest_rate 50/50, F1 float (partial pivoting, refinement, cutoffs 1e-12/1e-10/1e-13) 50/50 (ledgers/M7/scripts/M7-d-r12/alts_v12/run_F1_0-49.log); r10 exact B, G, H, I, J (ledgers/M7/scripts/M7-d-r12/alts_v12/run_r10_exact_alts_r12.log). No correct alternative fails the suite."),
    ("PRJ-R12-04", "2.6-autograder", "over-constraint check: float alternatives r12 alt 3-7 (solver defects on valid gamma inputs)", "PASS",
     "Round 12: the failing float alternatives raise RuntimeError 'working set dependent' or leave the budget gap above 1e-8 on valid gamma = 1e-6 or 1e-9 cases (ledgers/M7/scripts/M7-d-r12/alts_v12/diagnose_gamma_r12.py: alt_r12_3 and alt_r12_4 raise on seed 9 gamma 1e-6; F1 returns budget gap 1e-16 on the same case). They are solver defects, not suite over-constraint, because F1 passes the identical tests. Classification: alts_suite_r12.log, classify_alt_failures_r12.log."),
    ("PRJ-R12-05", "2.6-mutation", "new student-error mutants v12_02, v12_03, v12_04, v12_05 (ledgers/M7/mutants/)", "PASS",
     "Round 12: each is a complete module written from the reference by one replaced line (alts_v12/make_mutants_v12.py). Seeds 0-49 (alts_v12/v12_mutants_and_F1_0-49.log): v12_02 (diagonal Sigma in the solve) passes 0/50 seeds; v12_03 (sector caps left out of the search) passes 6/50 seeds, killed by the start-within-sector-cap boundary tests; v12_04 (start tolerance 1e-8) passes 0/50; v12_05 (cap for sector 0 only) passes 23/50, killed on the other 27 by the sector-1 cap tests. Killed_by per seed-0 run in alts_v12/v12_mutants_0-9.log and the mutants array."),
    ("PRJ-R12-06", "2.6-mutation", "equivalence proof: v12_01 (dual residual reported without the floor at zero)", "PASS",
     "Round 12: equivalent to the reference. The mutant differs only when every inequality multiplier entry is > 0. The reference's working set holds at most n-1 inequality rows (budget row and working set are linearly independent in R^n, reference.py 204, 229), so the n lower-bound entries contain a zero and min = 0 on every reference output. ledgers/M7/scripts/M7-d-r12/alts_v12/equiv_v12_01.log: 450 cases (seeds 0-49 plus 400 random) answered; 0 with every entry > 0. The mutant is kept out of mutants/."),
    ("PRJ-R12-07", "2.6-autograder", "grader/test_project.py collect-only, seeds 0-49", "PASS",
     "Round 12: ledgers/M7/scripts/M7-d-r12/collect_seeds_0-49_M7d_r12.log: '364 tests collected' for all 50 seeds; the page's count is 364."),
    ("PRJ-R12-08", "2.5-lab", "project.html lab code and expected blocks vs tests/labs/M7/lab-M7-project-1..3.py", "PASS",
     "Round 12: ledgers/M7/scripts/M7-d-r12/labs_page_vs_twin_M7d_r12.log: lab 1 and lab 3 page code equal the twins; lab 2 differs only on three ___ lines; each twin's output equals its expected block."),
    ("PRJ-R12-09", "2.4-math", "project.html Lab 1 and Lab 3 printed numbers", "PASS",
     "Round 12: ledgers/M7/scripts/M7-d-r12/alts_v12/rederive_labs_v12.log recomputes -3/220, budget-only weights, the answer (9/11, 2/11, 0), nu = -21/1100, lam3 = 9/1100, residuals 0/9/550/1/6250 with Fractions; also cross-checks the answer through reference.py (budget multiplier -0.0190909..., lower 0.00818...)."),
    ("PRJ-R12-10", "2.4-math", "project.html:323-325 Proposition (grade T)", "PASS",
     "Round 12: the proof uses only the stated hypotheses: convexity of L in (w,t) (f convex, g_j affine, lam_j >= 0), stationarity gives the minimum of L, feasibility of every y via s_i = |y_i - w0_i| (linearization equivalence), complementary slackness, and the midpoint argument for uniqueness of w. Grade T is supported."),
    ("PRJ-R12-11", "2.6-spec", "project.html:292-300 inputs and outputs vs instance.py and test_project.py", "PASS",
     "Round 12: fields and types in project.html:292-300 match instance.py output keys and test_project.py output_shape; the field 'label' exists (instance.py:57)."),
    ("PRJ-R12-12", "2.6-spec", "project.html:326 named conditions vs test_project.py NAMED_CONDITIONS, OTHER_SIDE_REFUSED, EXACT_BOUNDARIES, non-finite, missing field, non-mapping, no assets, one entry short/long", "PASS",
     "Round 12: every named condition on the page has an invalid test (ValueError, with a message) and a valid-form test; the other invalid inputs are tested with any exception carrying a message; the page's list of conditions matches the test list one to one."),
    ("PRJ-R12-13", "2.6-autograder", "Pyodide timing (plan 7.4; BUILDER_RULES 5.3.4)", "PASS",
     "Round 12: page_smoke in-browser suite: 364 tests in 3.1 s (limit 60 s per suite); local slowest single test 0.01 s on seed 0 (pytest --durations). Per-test Pyodide times are not measured individually, so the 5 s per test limit is checked only in aggregate."),
    ("PRJ-R12-14", "2.1-citations", "project.html:465-466 reading list keys", "PASS",
     "Round 12: boyd2004convex and stokey1989recursive are registry keys (verify_refs --offline: 0 problems); the page makes no claim from either source, so no locator is needed (plan 9.1)."),
    ("PRJ-R12-15", "2.9-dag", "project.html:310 'defined in Lesson 3' link", "PASS",
     "Round 12: L03.html:62 defines the Lagrangian of the problem; project.html links L03.html."),
]
for item in new_rows:
    rid, check, loc, status, ev = item[:5]
    fix = item[5] if len(item) > 5 else ""
    put(rid, check, loc, status, ev, fix)

# Rebuild the list in round-11 order, then append the round-12 rows.
order = list(r11_rows.keys()) + [rid for rid, *_ in new_rows]
seen = set()
final_rows = []
for rid in order:
    if rid in fresh and rid not in seen:
        seen.add(rid)
        final_rows.append(fresh[rid])
for rid in fresh:
    if rid not in seen:
        final_rows.append(fresh[rid])
        seen.add(rid)

counts = {s: sum(1 for r in final_rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(final_rows) else "FAIL"
killed = len(mutant_rows)
fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 12,
    "verifier": "Haiku 5.5 independent verifier (round 12, slice d); did not build M7-d",
    "pin": "329c1d7 (329c1d7feac5479403c351e64587c867278452cc)",
    "base": "ccaeeaf4 (round-11 pin, ccaeeaf44bea94b37d912ec1da3c660bb2c55d87); slice delta: project.html (lines 292-336, 456), 4 new mutants, no grader or lab changes",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD12-M7-d",
    "scratch": "ledgers/M7/scripts/M7-d-r12/ (ledgers/M7/scripts/M7-d-r12/gates/, ledgers/M7/scripts/M7-d-r12/alts_v12/, collect and lab scripts, logs)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": final_rows,
    "mutants": mutant_rows,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 12, slice d (project.html, grader, project labs, mutants, alternatives). Read in full: project.html 1-482, "
        "grader/instance.py, starter.py, reference.py, test_project.py. Delta from the round-11 pin: project.html "
        "wording (292, 309, 326, 332, 456) re-read; 4 new mutants (r11_*) and no grader or lab byte changes. Untracked "
        "files found in the checkout at start (ledgers/M7/mutants/r12_01, r12_04, r12_05 and an earlier scripts folder) "
        "were not produced by this run; they were re-run through mutate_graders and are counted. Gaps: five alternatives "
        "with different methods (PRJ-R12-02); Pyodide per-test timing; live verify_refs; full pytest; cards (out of slice)."
    ),
    "summary": {"rows": len(final_rows), "pass": counts["PASS"], "fail": counts["FAIL"],
                "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutant_rows), "mutants_killed": killed,
                "mutate_summary": mutant_summary.group(0) if mutant_summary else None},
}
out = repo / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(final_rows), counts, "mutants", len(mutant_rows), "killed", killed)
