"""Build the M7-d round-10 ledger fragment from the logs and rows written by the verifier (round 10).

Reads ledgers/M7/scripts/M7-d-r10/mutate_M7_0-9_r10.log for the mutant killers, adds the three r10 mutants, writes
ledgers/M7/M7-d.json and validates it with tools/ledger.py. Run from the checkout root.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

S = "ledgers/M7/scripts/M7-d-r10"
PIN = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()

R = []


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
    R.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


PRIOR = "Carried from round 9 with the subject re-read this round: "
row("PRJ-D1-01", "2.6-spec", "course/modules/M/M7/grader/instance.py (make_instance)", "PASS",
    "Read in full. Returns SIMULATED label; same seed gives same payload (test_instance_is_simulated_and_deterministic, "
    "suite pass 0-49, " + f"{S}/suite_run.py).")
row("PRJ-D1-02", "2.6-spec", "project.html:299-300; grader/test_project.py output_shape (351-353)", "PASS",
    "Reference returns exactly weights/multipliers/certificate with the seven multiplier keys (50/50 seeds, "
    "run_graders_M7_r10.log).")
row("PRJ-D1-03", "2.4-math", "project.html:309", "PASS",
    "Re-derived: t_i>=|d_i| with t_i>=d_i, t_i>=-d_i, sum t_i<=tau is equivalent to sum|d_i|<=tau (both directions "
    "written out on the page are correct).")
row("PRJ-D1-04", "2.4-math", "project.html:310-313", "PASS",
    "Re-derived dL/dw_i with g=l-w (-lambda_l), g=w-u (+lambda_u), sector (+eta_k), d-t and -d-t (+alpha_i, -beta_i) "
    "and dL/dt_i = kappa-alpha_i-beta_i; matches test_project.py stationarity() lines 133-151.")
row("PRJ-D1-05", "2.4-math", "project.html:310,314-319; grader/test_project.py inequality_pairs (116-130)", "PASS",
    "Each g_j of the page matches the pair list; turnover_total pair sum(t)-tau present.")
row("PRJ-D1-06", "2.4-math", "project.html:320", "PASS",
    "Unfloored dual value is -min(lambda); floor is 0; differs only when min>0. Test threshold 1e-9 (agreement) "
    "matches the sentence; degenerate-box hand case exercises it (test_project.py:306-311).")
row("PRJ-D1-07", "2.4-math", "project.html:317-321; test_project.py recomputed_certificate (154-165)", "PASS",
    "Primal, stationarity, dual, complementary-slackness definitions reproduced exactly.")
row("PRJ-D1-08", "2.4-math", "project.html:323-324 (Proposition T and proof)", "PASS",
    "Re-derived: L convex and differentiable in (w,t); f(y)>=L(y,s)>=L(w,t)=f(w) for feasible (y,s); midpoint "
    "argument for uniqueness. Hypotheses sentence (line 325) states every hypothesis the proof uses; existence of "
    "multipliers is explicitly not claimed.")
row("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py Sigma line", "PASS",
    "x'Sigma x = (|Ax|^2+|x|^2)/1000 > 0 for x != 0 with Sigma=(A'A+I)/1000 as the generator writes it.")
row("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py _parse (54-109)", "PASS",
    "Every named refusal in the page list is raised with ValueError in reference.py (lines 55-108).")
row("PRJ-D1-11", "2.6-spec", "grader/test_project.py NAMED_CONDITIONS, OTHER_SIDE_REFUSED", "PASS",
    "Each named condition has invalid and valid tests; ran 50/50 seeds.")
row("PRJ-D1-12", "2.6-spec", "project.html:326,332; test_project.py EXACT_BOUNDARIES (674-680)", "PASS",
    "Boundary values (bound/cap equal to start, sum inside 1e-9, gamma 1e-6) accepted by reference on 50 seeds.")
row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", "PASS",
    "run_labs --unit M7 --page project PASS (3/3); twin under python -I -W error rc 0, empty stderr; output equals "
    "page expected block line for line (diff in this round's log).")
row("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "PASS",
    "Completed twin output equals Lab 1 expected block; three blanks (residual, signs, dual_feasible) present.")
row("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "PASS",
    "Output: check A all zero; B stationarity 9/550, dual 9/1100; C stationarity 1/6250; all match page text.")
row("PRJ-D1-16", "2.9-hours", "project.html:33,338-354; course/modules/M/M7/index.html:29", "PASS",
    "Table sums 2+3+10+6+7+5=33; hub lessons 77 + project 33 = 110 = curriculum M7 hours 110.")
row("PRJ-D1-17", "2.9-structure", "project.html:40-49", "PASS",
    "Ladder: rung 1 solved, rung 2 instant completion check, rung 3 spec+autograder, rung 4 open stretch; scope "
    "matches the curriculum project brief (budget, box, sector, turnover, KKT).")
row("PRJ-D1-18", "2.6-spec", "project.html:288-336", "PASS",
    "Spec completeness: no blocking question found (see notes for the one honest gap: existence of multipliers is "
    "stated as not proved).")
row("PRJ-D1-19", "2.9-structure", "course/modules/M/M7/grader/ (instance, reference, starter, test_project)", "PASS",
    "All four files present; tools/check_projects.py --unit M7 PASS.")
row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py --unit M7 --pages project", "PASS",
    f"{S}/page_smoke_project_r10.log: project PASS, in-browser grader All 364 tests pass.")
row("PRJ-D1-21", "2.4-notation", "project.html symbol set vs notation/notation.json", "PASS",
    "Symbols used on the page: w,t,d,f,L,g,l,u,c,S,tau,mu,Sigma,gamma,nu,lambda,eta,alpha,beta,kappa,Z,n,A,s,y,k,b. "
    "Registry entries T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q are not used; gamma/mu/Sigma are local letters "
    "defined on the page (line 305).")
row("PRJ-D1-22", "2.9-dag", "project.html:456 envelope-theorem link; course/concepts.html", "PASS",
    "envelope-theorem is M2 (prerequisite of M7, plan line 178 usable); tools/check_dag.py --unit M7 PASS.")
row("PRJ-D1-23", "2.9-prose", "project.html (banned strings, process words)", "PASS",
    "Scan for TODO/TBD/lorem/ellipsis/for brevity/obviously/clearly/it can be shown/roughly/about N: 0 hits; no "
    "process words (verifier, round, ledger) in learner text.")
row("PRJ-D1-24", "2.6-spec", "project.html:364-366", "PASS",
    "Decode command run verbatim (make_instance(7) payload printed); pytest line uses the flags the suite was run "
    "with (suite_run.py FLAGS).")
row("PRJ-D1-25", "2.6-autograder", "grader/starter.py:18-20", "PASS",
    "Starter fails 3/3 seeds (361 failed on seed 2); run_graders M7 PASS includes the starter check.")
row("PRJ-D1-26", "2.6-autograder", "grader/instance.py (make_instance)", "PASS",
    f"{S}/instance_sample_r10.log: seeds 0-19 give n in {{3,4,5}}, 20 distinct reference answers, turnover, "
    "lower, upper and sector multipliers active on different seeds; reference accepts all 50 seeds.")
row("PRJ-D1-27", "2.6-autograder", "grader/test_project.py:37; reference.py:21", "PASS",
    "TOL 1e-8 for feasibility/stationarity/CS, 1e-9 for agreement and start checks; reference uses 1e-9 for start.")
row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py (assert and fail messages)", "PASS",
    "No message interpolates a value: only names/indices/keys are formatted (grep of f-string messages, lines 191-198, "
    "238, 390, 382, 1077, 889, 897).")
row("PRJ-D1-29", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke) and CPython (suite_run)", "PASS",
    "page_smoke in-browser 364 pass; CPython 364 collected and reference passes 50/50 under -W error.")
row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py", "PASS",
    f"pytest tests/test_labs.py -k M7 -> 11 passed ({S}/pytest_labs_M7_r10.log).")
row("PRJ-D1-31", "2.6-spec", "project.html:332; grader/test_project.py HAND_CASES (274-312)", "PASS",
    "Worked answers re-derived by hand: budget-only (0.6,0.4); zero turnover (0.5,0.5); single asset (1.0); upper "
    "bound binding (0.7,0.3) with turnover slack; turnover binding (0.6,0.4); degenerate box (0.5,0.5). Reference "
    "passes all six on 50 seeds.")
row("PRJ-D1-32", "2.6-atlas", "project.html; curriculum.json M7 entry", "PASS",
    "No atlas key on M7; the Atlas branch does not apply.")
row("PRJ-D1-33", "2.1-citations", "project.html:465-466; references/references.json (boyd2004convex, stokey1989recursive)", "PASS",
    "verify_refs --offline: 560 entries, 0 problems (r10 log). Both keys are verified with DOIs and used_by M7. The "
    "page makes no attributed claim (reading list only). Live verify_refs not re-run: references.json unchanged.")
row("PRJ-D1-34", "2.9-structure", "project.html:344-350; tools/check_pages.py --unit M7", "PASS",
    "check_pages --unit M7 PASS; hours table rows and rationales present.")
row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (191 files incl. r10_01..03)", "PASS",
    f"{S}/mutate_M7_0-9_r10.log: mutate_graders M7 188/188 killed on seeds 0-9; r10_01..03 killed on seed 0 "
    "(see mutants list).")
row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/ families f6,g2,m,p,q,r,s,v,w,x,y,z,d1-d3,r13-r15", "PASS",
    "All families present and all killed in the full gate run.")
row("PRJ-D1-37", "2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/mutants/", "PASS",
    "No equivalent mutant is listed (all 191 are killed on seeds 0-9), so no equivalence proof is needed in this "
    "folder.")
row("PRJ-D1-38", "2.6-autograder", f"{S}/alts/ (alt_B, alt_G, alt_H, alt_I, alt_J)", "PASS",
    "Five correct exact-arithmetic alternatives with different search orders and tie-breaks pass 364 checks on all "
    "50 seeds (alts_run_*.log). Three float alternatives are killed on gamma boundaries; see PRJ-R10-02.")
row("PRJ-D1-39", "2.9-structure", "BLUEPRINT.md:400-401 (§7); course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml; no deployment config in repo",
    "FAIL",
    "BLUEPRINT §7 says deployment excludes every grader/reference.py. The repository has no deployment configuration "
    "(no vercel.json, .vercelignore, Pages workflow or copy step) and ci.yml has no publish step, so the exclusion is "
    "not implemented anywhere: course/ is published as-is with reference.py inside. Cross-unit defect, not M7-specific.",
    "Add the exclusion to whatever publishes course/ (for example a .vercelignore entry or a build copy step in "
    "tools/build_site.py) for course/modules/*/*/grader/reference.py, and check it in CI, or amend BLUEPRINT §7 to "
    "name the mechanism that exists.")
row("PRJ-R4-01", "2.9-prose", "grader/test_project.py docstrings and messages", "PASS",
    "Re-read every docstring against its code: purity fixture (80-104) runs each call twice on a snapshot; "
    "_observed_call (60-77) checks argument, prints, warnings; messages carry no values.")
row("PRJ-R5-01", "2.4-math", "project.html:456 frontier bullet", "PASS",
    "Learner is asked to state the sign convention; the page claims no value.")
row("PRJ-R5-02", "2.6-spec", "grader/test_project.py comments and messages", "PASS",
    "Comments at 275, 277, 295-296, 301, 303-305 checked against the arithmetic (see PRJ-D1-31).")
row("PRJ-R5-03", "2.9-prose", "project.html:450", "PASS",
    "The 'does not test' paragraph matches the suite (seed problem plus hand cases only).")
row("PRJ-R5-04", "2.9-structure", "project.html:349-350", "PASS",
    "Total row and rationale match the hub (77 + 33 = 110).")
row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", "PASS",
    "Each r5 mutant killed on seeds 0-9 (mutate_M7_0-9_r10.log).")
row("PRJ-R6-01", "2.6-gate", "tools/check_projects.py --all", "PASS",
    f"{S}/check_projects_all_r10.log rc 0; check_projects M7 PASS.")
row("PRJ-R6-02", "2.6-gate", "tools/check_pages.py --all", "PASS",
    f"{S}/check_pages_all_r10.log rc 0; check_pages M7 PASS.")
row("PRJ-R6-03", "2.9-dag", "tools/check_dag.py --all", "PASS",
    f"{S}/check_dag_all_r10.log: rc 0, 27 PASS lines, 0 other lines; M7 PASS.")
row("PRJ-R7-01", "2.6-mutation", "grader/test_project.py degenerate box hand case; mutants r7_06_*", "PASS",
    "Degenerate box hand case present and its mutant killed on seed 0-9.")
row("PRJ-R7-02", "2.9-prose", "grader/test_project.py:295-296 comment", "PASS",
    "Recomputed: with upper 0.3 the answer is (0.7,0.3); without it the turnover limit stops at (0.55,0.45).")
row("PRJ-R7-03", "2.9-prose", "grader/test_project.py:916-921 comment", "PASS",
    "Comment matches _make_room and the starting-sum tests; POSITIONS are four fixed ids, collected count is seed-independent.")
row("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", "PASS",
    "All killed in the full gate run.")
row("PRJ-R7-05", "2.6-autograder", "grader/test_project.py (Pyodide timing)", "PASS",
    "page_smoke in-browser grader: 364 tests in 2.4 s, under the time limit.")
row("PRJ-R7-06", "2.8-data", "project.html; grader/instance.py", "PASS",
    "No dataset read; every case label contains SIMULATED (test_instance_is_simulated_and_deterministic).")
row("PRJ-R7-07", "2.6-hours", "project.html:344-350", "PASS",
    "Estimate: worked example 2h, completion 2-3h, core solver 12-18h, linear constraints 5-7h, certificate and tests "
    "5-7h, self-check 3-5h: total 29-42h vs declared 33 (inside +/-30%).")
row("PRJ-R8-01", "2.6-autograder", "grader/test_project.py:1114-1121 and purity fixture (80-104)", "PASS",
    "Refusal-path prints and warnings are killed: v8_01 (debug print) and v9_06 (print before refusal) killed; the "
    "fixture now uses pytest.fail, which is not caught by pytest.raises(Exception).")
row("PRJ-R8-02", "2.6-autograder", "grader/test_project.py:1108-1112 and fixture", "PASS",
    "Argument-change on refusal path: v9_07 killed; z04 killed.")
row("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", "PASS",
    "Killed by the full gate run.")
row("PRJ-R8-04", "2.6-spec", "grader/test_project.py:302-311", "PASS",
    "Degenerate-box hand case and its comment verified (see PRJ-D1-31).")
row("PRJ-R9-01", "2.6-autograder", "grader/test_project.py:60-103 (fixture) vs pytest.raises(Exception) tests", "PASS",
    "Round-9 root cause fixed in this checkout: _observed_call uses pytest.fail(pytrace=False) (lines 72-76), so "
    "refusal-path defects are not masked. v9_06 and v9_07 killed (mutate_M7_0-9_r10.log).")
row("PRJ-R9-02", "2.9-prose", "grader/test_project.py:82-89 docstring", "PASS",
    "Docstring states: run twice, snapshot, refusal allowed, checks apply to refusals; code does exactly this (92-102).")
row("PRJ-R9-03", "2.6-autograder", "grader/test_project.py:92 (@wraps) and :319-326", "PASS",
    "@wraps(real) keeps the signature visible; v9_08 (optional second argument) killed on seed 0.")
row("PRJ-R9-04", "2.9-prose", "project.html:167 (Lab 1 interpretation)", "PASS",
    "Re-read: budget-only, held asset, KKT steps and 'bound multiplier not held at zero is zero by construction' match "
    "the code (lines 117-152).")
row("PRJ-R9-05", "2.4-math", "project.html:324 (proof)", "PASS",
    "Proof re-derived in full (see PRJ-D1-08).")
row("PRJ-R9-06", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts_run_*.log", "PASS",
    "Over-constraint: five exact alternatives pass 50/50; float alternatives fail only the gamma-boundary tests (see "
    "PRJ-R10-02).")
row("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder)", "PASS",
    "Full gate run 188/188 killed; the three r10 additions killed (PRJ-R10-03).")
row("PRJ-R9-08", "2.6-spec", "grader/test_project.py (collected count); project.html:332", "PASS",
    f"{S}/collect_r10.log: 364 collected on every seed 0-49.")
row("PRJ-R9-09", "2.5-lab", "project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
    "run_labs project PASS; twins run under -I -W error.")
row("PRJ-R9-10", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", "PASS",
    "page_smoke in-browser grader 364 pass on seed 1541887665.")
row("PRJ-R9-11", "2.9-prose", "grader/test_project.py:274-311 hand-case comments", "PASS",
    "Each comment's arithmetic recomputed (see PRJ-D1-31).")
row("PRJ-R10-01", "2.6-autograder", f"{S}/alts/alt_B, alt_G, alt_H, alt_I, alt_J", "PASS",
    "Over-constraint check: exact-arithmetic solvers that differ in row order, empty start, ratio tie-break and "
    "negative-row drop all pass 364 checks on seeds 0-49 (collect 364, 0 failures each).")
row("PRJ-R10-02", "2.6-autograder", f"{S}/alts/alt_A, alt_C, alt_F; {S}/gamma_probe*_r10.py",
    "PASS",
    "Float alternatives with absolute cutoffs fail on every seed only on the gamma boundary tests (gamma 1e-6 raises "
    "RuntimeError; alt_F at gamma 1e-9 returns primal residual 2.2e-5 against 1e-8). These are defective methods, and "
    "the spec permits any method, including exact arithmetic which passes. Open: I did not build a conditioning-aware "
    "float solver, so whether one passes gamma 1e-9 is not shown here.")
row("PRJ-R10-03", "2.6-mutation", f"ledgers/M7/mutants/r10_01..r10_03 (written by {S}/make_new_mutants.py)", "PASS",
    "Three new student errors: sector multipliers divided by sector size; budget multiplier read off asset 0; lower "
    "multipliers reported as zero. Each killed on seed 0 (suite_run.py).")
row("PRJ-R10-04", "2.6-autograder", "ledgers/M7/mutants/ full gate", "PASS",
    "tools/mutate_graders.py --unit M7 --seeds 0-9 -> 188/188 killed (mutate_M7_0-9_r10.log).")
row("PRJ-R10-05", "2.6-autograder", "tools/run_graders.py --unit M7 --seeds 0-49; mypy --strict on grader",
    "PASS",
    "run_graders M7 PASS (reference 50/50, starter fails, mypy strict clean); collect 364 on 50 seeds.")
row("PRJ-R10-06", "2.9-structure", "repo gates: ruff check ., ruff format --check ., mypy --no-incremental",
    "PASS",
    f"ruff check: All checks passed; ruff format: 553 files formatted; mypy: Success, 385 files ({S}/mypy_r10.log).")

MUTANT_LOG = ROOT / S / "mutate_M7_0-9_r10.log"
mutants = []
pattern = re.compile(r"^KILLED (\S+): (.*) -> (.*)$")
for line in MUTANT_LOG.read_text(encoding="utf-8").splitlines():
    m = pattern.match(line)
    if m:
        name, desc, killed = m.group(1), m.group(2), m.group(3)
        mutants.append({"name": name, "description": desc, "killed_by": killed})
r10 = [
    ("r10_01_sector_multipliers_divided_by_sector_size.py", "test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary] (seed 0)"),
    ("r10_02_budget_multiplier_read_from_asset_zero.py", "test_stationarity_holds_in_the_weights (seed 0)"),
    ("r10_03_lower_multipliers_reported_as_zero.py", "test_named_condition_boundary_is_accepted[lower-not-above-upper-boundary] (seed 0)"),
]
for name, killer in r10:
    text = (ROOT / "ledgers/M7/mutants" / name).read_text(encoding="utf-8")
    first = text.split('"""', 1)[1].splitlines()[0]
    mutants.append({"name": name, "description": first, "killed_by": killer})

fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 10,
    "verifier": "Haiku 5.5 independent verifier (round 10); did not build M7-d",
    "pin": PIN,
    "base": "1e272e5a641f18412703b37778a44db6f7391a69 (round-9 pin); M7 slice changed since: test_project.py, project.html, lab-M7-project-3.py",
    "checkout": str(ROOT),
    "scratch": f"{S} (all scripts, alternatives, probes and logs); no scratch outside the checkout",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 10 on 47a36d8c. Delta since round-9 pin 1e272e5: test_project.py (pytest.fail + wraps), project.html "
        "(Lab 1 and Lab 3 interpretation, Proposition-adjacent wording), lab-M7-project-3.py docstring; all re-read in "
        "full this round, so no round-9 PASS row is carried on stale evidence. Not checked: a browser visual sweep "
        "beyond page_smoke; the card-level lesson trace (cards are not in this slice); the live verify_refs run; the "
        "full repository pytest (only tests/test_labs.py -k M7). Open honest gap: no conditioning-aware float solver "
        "was built, so float-method acceptance at gamma 1e-9 is not demonstrated (PRJ-R10-02). alt_F is alt_D with the p-zero "
        "cutoff and the negative-multiplier cutoff set to 1e-8 by sed (a one-line edit, recorded here). alt_D and alt_E are "
        "generated by make_alts.py and not cited by any row. Only one blocking "
        "FAIL: PRJ-D1-39, which is cross-unit (no deployment exclusion of grader/reference.py exists in the repo)."
    ),
    "summary": {},
}
fragment["summary"] = {
    "rows": len(R),
    "pass": sum(r["status"] == "PASS" for r in R),
    "fail": sum(r["status"] == "FAIL" for r in R),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in R),
    "mutants": len(mutants),
    "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
problems = ledger.validate(json.loads(out.read_text(encoding="utf-8")), "M7-d")
print("validate:", problems)
print(fragment["summary"])
