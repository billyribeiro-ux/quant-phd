"""Write ledgers/M7/M7-d.json (round 1) from the round-1 checks. Usage: python3 -I write_fragment_r1.py <checkout-root>"""
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
S = "ledgers/M7/scripts/M7-d-r1"
PIN = "d0f39c09" + "f" * 0  # placeholder replaced below
import subprocess

PIN = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()

log = (root / S / "mutate_all_r1_with_new.log").read_text(encoding="utf-8")
mutants = []
for line in log.splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?):? (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    killed_by = None if killed.startswith("None") or status == "SURVIVED" else killed.split(" (seed")[0]
    mutants.append({"id": name.removesuffix(".py"), "description": desc.strip(), "killed_by": killed_by})

P = "course/modules/M/M7"
rows = [
    ("PRJ-D1-01", "2.9 spec: Context and Inputs", "project.html:292-295", "PASS",
     "Context is four sentences (project.html:292). Inputs fields gamma, mu, sigma, w0, lower, upper, sector, sector_caps, turnover_limit and label match grader/instance.py:56-67 key for key; the decode command was run (misc_checks_r1.log)."),
    ("PRJ-D1-02", "2.6 spec: Required outputs (three keys, seven multiplier keys, four certificate keys)", "project.html:299-300", "PASS",
     "Page names the keys; test_project.py:125-150 (output_shape) checks them; reference.py:330-334 returns exactly them; seed 0 full suite 363 passed (run_graders_0-49.log)."),
    ("PRJ-D1-03", "2.4 maths: linearized turnover (t_i >= +-d_i, sum t <= tau)", "project.html:309", "PASS",
     "Re-derived: if sum|d| <= tau then t=|d| satisfies all three; converse sum|d| <= sum t <= tau. Constraints are affine in (w,t). Matches reference.py:116-119 sign forms (2^n sum s_i d_i <= tau)."),
    ("PRJ-D1-04", "2.4 maths: stationarity residuals r^w_i, r^t_i", "project.html:310-312", "PASS",
     "Derived signs from the gradients of g_j: l-w gives -lambda^l, w-u gives +lambda^u, sector gives +eta, d-t gives +alpha, -d-t gives -beta, sum t - tau gives +kappa in t, so r^t = kappa - alpha - beta. Equal to test_project.py:84-102 and reference.py:305-309."),
    ("PRJ-D1-05", "2.4 maths: four certificate definitions", "project.html:314-319", "PASS",
     "Each field (primal max over 0, budget, bounds, sector, turnover gap; stationarity max over r^w and r^t; dual max(0, -min); complementary max |lambda g|) equals test_project.py:105-116 and reference.py:262-315 (read in full)."),
    ("PRJ-D1-06", "2.4/2.2: dual-residual floor 'structural' claim and 'zero on seeds 0-299'", "project.html:320", "PASS",
     "scripts/M7-d-r1/claims_seeds.py over seeds 0-299 (claims_seeds.log): minimum inequality multiplier exactly 0 on 300/300; at least n+1 zero bound multipliers on 300/300. The 'structural' argument is the reference's own working-set bound (reference.py:204, 229, independence in n unknowns), so it describes the reference's construction and is accurately labelled as such."),
    ("PRJ-D1-07", "2.4: tolerances 1e-8 (fields) and 1e-9 (agreement and starting portfolio)", "project.html:321", "PASS",
     "test_project.py:36 (TOL=1e-8), :360 and :405 (agreement 1e-9); reference.py:21 (TOL=1e-9) used at :102-108. Matches the page."),
    ("PRJ-D1-08", "2.4 maths: Proposition (sufficiency of KKT), graded T", "project.html:323-324", "PASS",
     "Re-derived the proof: L convex in (w,t) since f is convex in w and constraints affine; stationarity gives minimiser of L; f(y) >= L(y,s) >= L(w,t) = f(w) by complementary slackness; uniqueness by midpoint argument with strict convexity. Every step uses a stated hypothesis. Hypotheses are listed at project.html:325."),
    ("PRJ-D1-09", "2.4: hypotheses paragraph (Sigma = (A'A+I)/1000, 50 of 50 seeds)", "project.html:325", "PASS",
     "instance.py:39-43 builds Sigma = (A'A + I)/1000; x'Sigma x = (|Ax|^2+|x|^2)/1000 > 0 for x != 0 (re-derived). run_graders_0-49.log: reference 50/50 seeds."),
    ("PRJ-D1-10", "2.6 spec: named ValueError conditions and boundary values", "project.html:326", "PASS",
     "Each listed condition is in reference.py:54-109 (ValueError messages) and tested in both the invalid and valid form (test_project.py:563-577, 633-703, 760-840, 849-1025). Seed 0 collection and run: 363 passed. Non-ValueError invalid inputs (TypeError, reference.py:40, 50, 96) carry messages, as the page allows."),
    ("PRJ-D1-11", "2.6 spec: purity and silence", "project.html:327", "PASS",
     "reference.py contains no print or warnings call (read in full). test_project.py:1032-1051 checks no mutation, no output, no warnings, determinism. Mutants z03 and z04 killed."),
    ("PRJ-D1-12", "2.6 spec: grading paragraph counts (363 checks; 3 comparators; 5 hand cases)", "project.html:332", "PASS",
     "misc_checks_r1.log: 363 tests collected for each seed 0-49 (50 of 50). test_project.py:372 has three comparators (0.25, 0.5, 0.75); HAND_CASES at :218-246 has five entries; hand answers re-derived by hand (budget only (0.6,0.4); upper bound (0.7,0.3); turnover (0.6,0.4))."),
    ("PRJ-D1-13", "2.5 labs: Lab 1 (lab-M7-project-1) output and prose", "project.html:53-168", "PASS",
     "run_labs --unit M7 --page project: 3/3 pass (run_labs_M7_project.log). Twin run under python -I -W error exits 0 with empty stderr and output identical to the page block. lab_recheck_r1.py recomputes stationarity 0, budget gap 0, objective -3/220 (about -0.013636), matching the prose (line 167)."),
    ("PRJ-D1-14", "2.5 labs: Lab 2 completion problem", "project.html:170-285", "PASS",
     "run_labs completion rule passes (3 blanks, twin is the completed solution). Twin output equals Lab 1 output line for line. Prose at line 284 is accurate about the three blanks (residual, signs, dual_feasible)."),
    ("PRJ-D1-15", "2.5 labs: Lab 3 certificate numbers and prose", "project.html:372-445", "PASS",
     "Twin output (check A zeros; B stationarity 9/550 and dual 9/1100; C stationarity 1/6250) reproduced by lab_recheck_r1.py (lab_recheck_r1.log). 9/550 = 2 x 9/1100 is the prose's 'twice' claim. Pytest run of tests/test_labs.py -k 'M7 and project' passed."),
    ("PRJ-D1-16", "2.9 hours: 33-hour split, 77 + 33 = 110", "project.html:33, 338-354; index.html:29,39-42; L01-L08 data-hours", "PASS",
     "Components 2+3+10+6+7+5 = 33 (project.html:344-350). Lesson data-hours 9,9,10,10,10,10,9,10 sum to 77 (index.html:29 data-hours-lessons=77). 77 + 33 = 110 (index.html:31)."),
    ("PRJ-D1-17", "2.9 / BUILDER 5.1: four-rung ladder", "project.html:40-49", "PASS",
     "Rung 1 worked example (Lab 1), rung 2 completion (Lab 2), rung 3 graded (spec and grader), rung 4 stretch (not graded). Tier F keeps rungs 1-2 at full length (plan 7.1). check_projects --unit M7 PASS (check_projects.log)."),
    ("PRJ-D1-18", "2.6: spec completeness (no clarifying question needed)", "project.html:288-336", "PASS",
     "Checked every question a competent student would ask: multiplier representation is non-unique (grader checks the student's own multipliers, test_project.py:170-199, so any valid set passes); the seed comes from the autograder panel (project.html:364); the infeasible-start case is covered by the start checks. No open question found."),
    ("PRJ-D1-19", "BUILDER 1.3-1.4 banned phrases; 1.3 placeholders", "project.html (whole)", "PASS",
     "misc_checks_r1.log: no TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important, studies show, experts agree, well known, obviously or clearly. The only 'just' is 'just inside it' (line 326), which is prose."),
    ("PRJ-D1-20", "BUILDER 1.8 and page_smoke: no external requests, zero console errors", "project.html; page_smoke_project_r1.log", "PASS",
     "No http(s) link in project.html (misc_checks_r1.log). page_smoke --unit M7 --pages project: PASS, with the in-browser grader reporting All 363 tests pass."),
    ("PRJ-D1-21", "Notation: symbols vs notation/notation.json", "project.html:305-318, 390-392", "PASS",
     "The eight registered symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) do not occur on the page. Bare gamma, mu, Sigma, nu, lambda, eta, alpha, beta, kappa, tau, Z, n and w are local letters (notation.json 'about' says gamma, mu, sigma are local). No registered symbol takes another meaning."),
    ("PRJ-D1-22", "2.9 / BUILDER 1.10: DAG and concept use", "project.html:292, 309, 456; L03.html:62; M2/L22.html", "PASS",
     "check_dag --unit M7 PASS. Lagrangian is defined at L03.html:62, which the page links. envelope-theorem is defined in M2 (course/modules/M/M2/L22.html), in the prerequisite closure, and linked. 'Covariance matrix' appears only in the no-link disclaimer at project.html:292, as architect decision B1/Q1 requires."),
    ("PRJ-D1-23", "2.9: process words in learner text", "project.html (whole)", "PASS",
     "grep -w -i for round, fixer, builder, verifier, ledger, plan and agent on project.html returns 0 matches (run in this round; no learner-facing process words)."),
    ("PRJ-D1-24", "2.6 spec: local-run instructions and decode command", "project.html:364-366", "PASS",
     "misc_checks_r1.log: the decode command prints the case keys (run from the grader folder, without -I). The suite is run in the checkout's Python 3.14.8 venv (plain pytest flags as on the page). Note: the host python3 is 3.15.0; the page's 'Python 3.14' statement refers to the course tools' version and matches the venv."),
    ("PRJ-D1-25", "2.6 autograder 1: run_graders on reference, starter fails", "grader/reference.py, grader/starter.py", "PASS",
     "run_graders_0-49.log: 'run_graders M7: PASS (reference 50/50 seeds, slowest 3.3 s)'. No FAIL line, so the starter fails the suite and mypy --strict is clean."),
    ("PRJ-D1-26", "2.6 autograder 2: instances valid and materially different (sample of 50 seeds)", "grader/instance.py:34-68", "PASS",
     "instances_0_49.log: 0 validity problems on seeds 0-49 (determinism, bounds, start sum, caps); 50 distinct answers; 12 distinct active-set patterns; asset counts 3:18, 4:14, 5:18 (all three sizes occur)."),
    ("PRJ-D1-27", "2.6 autograder: standard library only, reference and tests", "grader/reference.py:11-18; grader/test_project.py:268-282", "PASS",
     "reference.py imports only math, collections.abc, dataclasses, fractions, itertools, typing; test_only_standard_library_imports enforces it on the student file."),
    ("PRJ-D1-28", "2.6 autograder 4: failure messages name the property, never the answer", "grader/test_project.py (all assert messages)", "PASS",
     "Read every assertion message: each names a property or a field and a hint, and none prints the expected value. Parametrised ids carry only case names. Local runs use --assert=plain, so no value is shown."),
    ("PRJ-D1-29", "2.6 autograder: mypy --strict and ruff", "grader/*.py, tests/labs/M7", "PASS",
     "mypy_r1.log: strict mypy on reference.py, instance.py, starter.py and tests/labs/M7/*.py: no issues. ruff_r1.log: ruff check and ruff format --check pass."),
    ("PRJ-D1-30", "2.5 labs: pytest on lab twins (tests/test_labs.py)", "tests/labs/M7/lab-M7-project-1..3.py", "PASS",
     "pytest_labs_M7_project_r1.log: passes. Twins run alone under python -I -W error (exit 0, no stderr)."),
    ("PRJ-D1-31", "2.6 autograder 5: same suite in Pyodide and local pytest", "project.html:359; grader/test_project.py:3-5", "PASS",
     "page_smoke project: in-browser grader 'All 363 tests pass' (page_smoke_project_r1.log). Local pytest: 363 pass on seed 0 and on the reference for all seeds 0-49."),
    ("PRJ-D1-32", "2.6 atlas milestone: none; check_projects", "project.html; curriculum 'no Atlas milestone'", "PASS",
     "No atlas key and no milestone reference on the page; check_projects --unit M7 PASS (check_projects.log)."),
    ("PRJ-D1-33", "2.6 reading list: registry keys", "project.html:465-466", "PASS",
     "references/references.json entries boyd2004convex (status verified, used_by M7) and stokey1989recursive (status verified, used_by M7) exist. The page cites them only as reading, no attributed claim. verify_refs --offline: 560 entries, 0 problems."),
    ("PRJ-D1-34", "2.6 hours: estimate each component", "project.html:344-350", "PASS",
     "My own estimate: rung 1 about 2 h, rung 2 about 2-3 h, core solver 12-20 h, linear constraints 4-8 h, certificate 3-6 h, self-check 3-5 h. Total 26-44 h; the 33 h declared is within 30% of the midpoint."),
    ("PRJ-D1-35", "2.6 autograder 3: all existing mutants killed", "ledgers/M7/mutants/*.py (122)", "PASS",
     "mutate_all_r1_with_new.log: 126/126 killed on seeds 0-9 (including the 122 existing and my 4 new). Descriptions and killing tests are in mutants[]."),
    ("PRJ-D1-36", "2.6 autograder 3: at least three new student-error mutants written by this verifier", "ledgers/M7/mutants/d1_01..d1_04_*.py", "PASS",
     "make_mutants_r1.py generates four mutants from reference.py: d1_01 weights 1e-7 off optimum; d1_02 turnover multipliers by displacement sign; d1_03 primal residual reported as zero with a 5e-9 budget gap; d1_04 turnover stationarity reports kappa alone. All four are killed (see mutants[])."),
    ("PRJ-D1-37", "2.6 autograder: dual-residual floor is not tested by the mutation suite", "project.html:320; grader/test_project.py:108, 360", "PASS",
     "The page states this openly. The agreement test does recompute the floored dual residual for the student's own multipliers (test_project.py:108, 360), so an answer with all multipliers positive is checked against the floor. The reference never produces such an answer (claims_seeds.log), so no reference-derived mutant can show the floor. Documented, not a mismatch."),
    ("PRJ-D1-38", "2.6 autograder: five alternative correct implementations must pass seeds 0-49", "ledgers/M7/scripts/M7-d-r1/alts/ (alt1 only); alt1_seeds_0-49.log", "UNVERIFIABLE",
     "Only one alternative was built (alt1, working-set enumeration, make_alt1.py). Its first version failed 19 of 50 seeds with RuntimeError('no KKT working set was found') from its own solver (alt1_seeds_0-49.log; error type confirmed on seeds 3, 8, 9, 10, 13, 14, 25, 33, 34, 35, 36). Its second version (allowing budget-free working sets) passed seed 0 but was too slow for n=5 seeds and the run did not finish. Alternatives 2 to 5 (ADMM with polish, log-barrier, dual ascent, a second exact active-set) were not built. No suite verdict on a correct answer was produced, so no grader defect is shown by this row."),
    ("PRJ-D1-39", "BUILDER 1.10 / BLUEPRINT 7: reference.py excluded from deployment", "course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml; no .vercelignore or vercel.json", "FAIL",
     "The reference lives under the deployable course/ tree. misc_checks_r1.log: no exclusion in .gitignore, no .vercelignore, no vercel.json, and the CI workflow has no deploy step. BLUEPRINT.md:400-401 requires the deployment to exclude every grader/reference.py. The repository does not implement or evidence this. Fix: add the exclusion to the deployment configuration (for example a .vercelignore line course/**/grader/reference.py), or move the reference files outside course/ and have run_graders and page_smoke read them from there. This is a repo-wide issue, not specific to M7."),
]
rows_json = []
for rid, check, loc, status, ev in rows:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = ("Build alternatives 2 to 5 under ledgers/M7/scripts/M7-d-r1/alts/ and fix alt1 so it completes the search (its solver, not the suite, raises). Re-run each alternative on seeds 0-49 with run_alt_seeds.sh." if rid == "PRJ-D1-38" else
                      "Add the deployment exclusion for every grader/reference.py (course/**/grader/reference.py) in the deployment configuration, or move the reference solutions out of course/.")
    rows_json.append(row)

n_pass = sum(1 for r in rows_json if r["status"] == "PASS")
n_fail = sum(1 for r in rows_json if r["status"] == "FAIL")
n_unv = sum(1 for r in rows_json if r["status"] == "UNVERIFIABLE")
killed = sum(1 for m in mutants if m["killed_by"])
verdict = "PASS" if n_pass == len(rows_json) else "FAIL"
frag = {
    "unit": "M7",
    "slice": "d",
    "round": 1,
    "verifier": "Haiku 5.5 independent verifier (M7-d round 1)",
    "pin": PIN,
    "base": "none: first independent verification of slice d in this round (per the workflow task). Earlier fragments in ledgers/M7/M7-d.json history were not read as inputs.",
    "checkout": str(root),
    "scratch": "/tmp/m7d-* (collect, alt1 and run copies); no output depends on them",
    "verified_at": datetime.now(UTC).isoformat(timespec="seconds"),
    "verdict": verdict,
    "rows": rows_json,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Ran: run_graders --unit M7 --seeds 0-49 (PASS 50/50); mutate_graders --unit M7 --seeds 0-9 (126/126 killed); "
        "run_labs --unit M7 --page project (3/3); twin runs under python -I -W error; check_projects, check_pages, check_dag (M7 PASS); "
        "ruff; mypy --strict per the page command; pytest labs; page_smoke --pages project (PASS); verify_refs --offline (0 problems); "
        "claims_seeds.py over seeds 0-299; instances_0_49.py; lab_recheck_r1.py; misc_checks_r1.sh; collect-only over seeds 0-49 (363 each). "
        "Not checked: the five alternative implementations (only one built, incomplete); a visual figure sweep (the project has no figures); "
        "the full repository pytest, ruff and mypy (no code outside this slice changed in this round); card-level text (slice e)."
    ),
    "summary": {"rows": len(rows_json), "pass": n_pass, "fail": n_fail, "unverifiable": n_unv,
                "mutants": len(mutants), "mutants_killed": killed},
}
out = root / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, "verdict", verdict, frag["summary"])
