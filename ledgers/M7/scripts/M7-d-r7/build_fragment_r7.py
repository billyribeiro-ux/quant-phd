import json, re, pathlib, datetime
W = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB7-M7-d")
L = W / "ledgers/M7/scripts/M7-d-r7"
CK = "course/modules/M/M7/checks"  # unused placeholder
mut = []
for line in (L / "mutate_all96.log").read_text().splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killer = m.groups()
    mut.append({
        "name": name,
        "description": desc,
        "killed_by": killer if status == "KILLED" else "SURVIVED: none of the 10 seeds (0-9) fails any test",
        "status": status,
    })
assert len(mut) == 96, len(mut)
P = "PASS"; F = "FAIL"; U = "UNVERIFIABLE"
def carry(n, what):
    return f"Carried from round 6 ({what} byte-identical since pin 44f1eb6; git diff 44f1eb6 7aa909e hunks in project.html are at lines 39, 303-322, 329, 441 only):"
rows = [
 ("PRJ-R6-01", "tools/check_projects.py --unit M7", "tools/check_projects.py", P, "check_projects M7: PASS (ledgers/M7/scripts/M7-d-r7/checks.log)"),
 ("PRJ-R6-02", "tools/check_pages.py --unit M7 (hours, ladder, data-hours)", "tools/check_pages.py", P, "check_pages M7: PASS (checks.log)"),
 ("PRJ-R6-03", "tools/check_dag.py --unit M7 (concept links in project.html)", "course/modules/M/M7/project.html", P, "check_dag M7: PASS (checks.log)"),
 ("PRJ-R6-04", "run_graders reference, seeds 0-49", "course/modules/M/M7/grader/reference.py", P, "run_graders M7: PASS (reference 50/50 seeds, slowest 3.4 s) (run_graders.log)"),
 ("PRJ-R6-05", "starter fails the suite (run_graders check)", "course/modules/M/M7/grader/starter.py", P, "run_graders M7: PASS; tools/run_graders.py docstring lists the starter-fails check (run_graders.log)"),
 ("PRJ-R6-06", "collected test count equals page's 363 for every seed", "course/modules/M/M7/project.html line 329; grader/test_project.py", P, "pytest --collect-only: '363 tests collected' for QF_SEED 0, 17 and 49 (collect.log)"),
 ("PRJ-R6-07", "all M7 lab twins incl. project-1..3 via run_labs", "tests/labs/M7/lab-M7-project-{1,2,3}.py", P, "run_labs M7: PASS (11/11) (run_labs.log)"),
 ("PRJ-R6-08", "project twins run under python -I -W error; stdout equals page expected block", "project.html lines 155, 271/281, 435-437", P, "run_labs runs each twin as sys.executable -I -W error (tools/run_labs.py line 55) and PASS 11/11 (run_labs.log)"),
 ("PRJ-R6-09", "page code equals twin (lab 1, lab 3); lab 2 differs only in its blanks", "project.html lines 56-154, 172-270, 372-434", P, "run_labs M7 PASS keeps page and twin in agreement (run_labs.log); project twins byte-identical since 44f1eb6 (git diff --quiet)"),
 ("PRJ-R6-10", "Lab 1 numbers re-derived independently", "project.html lines 155-166", P, carry(10, "project.html lines 155-166")),
 ("PRJ-R6-11", "Lab 3 residual claims re-derived", "project.html lines 435-438", P, carry(11, "project.html lines 435-438")),
 ("PRJ-R6-12", "certificate definitions (page 309-317) match the grader recomputation", "project.html lines 306, 313, 315; grader/test_project.py lines 105-116", P, "Re-derived this round: page now writes |sum_i w_i - 1| (line 313) and the grader computes abs(sum(w) - 1.0) in recomputed_certificate (test_project.py line 109); dual floor (line 315) matches max(0, -min) in the grader; see PRJ-R6-28 for the one mutant that breaks the floor"),
 ("PRJ-R6-13", "sufficiency proposition (page 320-322) and uniqueness proof", "project.html lines 320-322", P, "Re-read this round: Lagrangian L(w,t) with budget term nu(sum_i w_i - 1); chain f(y) >= L(y,s) >= L(w,t) = f(w) uses feasibility, lambda >= 0 and complementary slackness; midpoint argument gives uniqueness under strict convexity in w; hypotheses list matches (line 322); the instance covariance (A'A+I)/1000 matches grader/instance.py lines 39-41"),
 ("PRJ-R6-14", "linearization of turnover constraint", "project.html line 307", P, carry(14, "project.html line 307 (context line in the diff, not a changed line)")),
 ("PRJ-R6-15", "five hand-worked answers are correct", "grader/test_project.py lines 218-246", P, carry(15, "grader/test_project.py lines 218-246; the suite passes 363/363 on the reference")),
 ("PRJ-R6-16", "named ValueError conditions have refused and accepted tests", "grader/test_project.py lines 553-567, 590-596, 670-693, 697-708", P, carry(16, "the cited test lines")),
 ("PRJ-R6-17", "instances SIMULATED, feasible by construction, <=3 decimals, both sectors non-empty", "course/modules/M/M7/grader/instance.py lines 34-68", P, carry(17, "grader/instance.py")),
 ("PRJ-R6-18", "solution may use standard library only; no grader import", "grader/test_project.py lines 268-282", P, "test_only_standard_library_imports is in the 363 passing on reference seeds 0, 17, 49 (pytest run in /tmp/m7d_r7_ws)"),
 ("PRJ-R6-19", "ruff check and ruff format on labs and grader; mypy --strict", "tests/labs/M7; course/modules/M/M7/grader", P, "ruff check tests/labs/M7 course/modules/M/M7/grader: All checks passed (ruff.log); mypy --no-incremental on reference, instance, starter and the three project twins: no issues (mypy.log). ruff format --check not re-run this round"),
 ("PRJ-R6-20", "references cited by the reading list exist in the registry", "project.html lines 459-460; references/references.json", U, "Not re-run this round (verify_refs not run for this slice); the cited lines are not in the delta hunks, so the prior PASS is carried in spirit, but it is not re-proved. Honest gap"),
 ("PRJ-R6-21", "page_smoke M7 (render, in-browser grader run)", "course/modules/M/M7/project.html", P, "page_smoke M7: PASS (page_smoke.log)"),
 ("PRJ-R6-22", "hours: project components sum to 33; lessons 77 + project 33 = 110", "project.html lines 337-351; index.html data-hours", P, "check_pages M7 PASS (checks.log); the hub hunk changes lede prose only"),
 ("PRJ-R6-23", "no process words in learner text", "project.html (delta lines 39, 303-322, 329, 441)", P, "Delta prose read: 'Rungs 1 and 2 are both in this module' (line 42); 'Lagrangian (defined in Lesson 3)' (line 308); the not-tested paragraph (line 444). No process words"),
 ("PRJ-R6-24", "notation: symbols vs notation/notation.json", "project.html lines 303-308", P, "Changed symbols only: the all-ones vector is written as sum_i w_i (line 306, 313). Other symbols carried from round 6 (their lines are unchanged)"),
 ("PRJ-R6-25", "cards: numbers on each back appear in the card's own lesson; no duplicate fronts or ids", "course/modules/M/M7/cards.json (146 cards)", U, "ledgers/M7/scripts/M7-d-r7/cards_numbers_r7.log: duplicate ids [], duplicate fronts [], non-T grades have a basis. The script flags M7-c080 (18/11, 4/11, 11/4) and M7-c084 (1/8) as absent from L05.html, but L05 writes these as TeX fractions (\\tfrac{18}{11}, \\tfrac{11}{4}, \\tfrac{1}{8}), so those flags are script limitations. The script does not parse TeX fractions, so its number check is not a reliable PASS for the 146 cards; the row is UNVERIFIABLE until the number check reads TeX fractions and is re-run"),
 ("PRJ-R6-26", "cards: numeric claims re-derived from lab outputs", "cards.json c009-c016, c027-c030, c049-c050, c060, c062-c064, c067, c069, c080, c086-c090, c102, c108-c116, c118, c130-c137, c150-c157", U, "Only changed/new cards re-derived this round: M7-c080 (Remark 2.4 identity, v'Qv shown in lesson as the sum; PASS), M7-c163 (Proposition 3.4 statement, PASS), M7-c164 (Proposition 2.1 hypothesis 0<g2<g1 and conclusion R(g1)<=R(g2), PASS). The other numeric cards were not re-derived this round; gap"),
 ("PRJ-R6-27", "notation glyph 1 (all-ones vector) vs registry macro \\mathbf{1} = \\indic", "course/modules/M/M7/project.html lines 306, 313", P, "grep -n 'mathbf{1}' project.html returns nothing (round-6 hits at 306 and 313 are gone; the page now writes sum_i w_i). The registry macro question remains for notation/notation.json and is not this slice"),
 ("PRJ-R6-28", "dual residual floor at zero is exercised by the suite (spec line 315)", "grader/test_project.py lines 105-116, 365-369; grader/reference.py line 287; project.html line 315", F, "ledgers/M7/mutants/q04_dual_residual_without_zero_floor.py SURVIVES seeds 0-9 (mutate_all96.log). A reference-output scan over seeds 0-49 (ledgers/M7/scripts/M7-d-r7/minmult.py) finds min inequality multiplier = 0.0 on every seed, so the floor max(0, -min) never differs from -min on any seed the suite generates. Fix: add a hand-worked or constructed case in which every inequality multiplier of a correct answer is strictly positive, so that a floor-less residual is refused"),
 ("PRJ-R6-29", "hand-worked cases: certificate fields checked against the recomputation", "grader/test_project.py lines 388-410", P, "The round-6 gap is closed: test_hand_case_matches_its_worked_answer now asserts each certificate field against recomputed_certificate (test_project.py lines 401-405); reference passes all 5 hand cases (363/363). Mutant coverage of this added check is not separately shown"),
 ("PRJ-R6-30", "objective against three feasible comparators (page line 329)", "grader/test_project.py lines 372-379; project.html line 329", P, "Page line 329 names the comparators as the mixes at 0.25, 0.5 and 0.75 of the way from the answer to the start; test_project.py line 372 parametrizes exactly 0.25, 0.5, 0.75 (the 0.0 case is the answer itself and is gone). Consistent"),
 ("PRJ-R6-31", "mutant suite: every grader mutant killed (ledgers/M7/mutants, seeds 0-9)", "ledgers/M7/mutants/ (96 files); tools/mutate_graders.py --unit M7 --seeds 0-9", F, "mutate_graders M7: FAIL (92/96 killed) (mutate_all96.log). Survivors: q04 (PRJ-R6-28); r02_turnover_total_residual_dropped_from_primal, r04_budget_left_out_of_primal_residual, r05_turnover_total_slackness_term_zeroed. r02 and r04 change only the primal residual, and r05 only the turnover complementary term, so each equals the correct field on any output that the weight and KKT checks accept; they are equivalent-on-feasible-output survivors. Page line 315 defines these terms, so under the rulings they count as FAIL. Fix: an agreement check on a deliberately infeasible or non-complementary output, or the page states that the certificate is checked only on the four fields for feasible answers"),
 ("PRJ-R6-32", "five alternative correct implementations pass the suite (rule 11)", "ledgers/M7/scripts/M7-d-r7/alt/alt_float.py", F, "Only one alternative was run (the round-6 float working-set solver, alt_float.py). Against the current suite on seeds 0-9 it fails 4 tests: gamma-just-inside-zero (gamma=1e-9, seeds 1, 8, 9) and gamma-positive-zero-boundary and gamma-positive-negative-boundary (gamma=1e-6, seeds 7, 9) with RuntimeError 'the working set lost independence' (constrained_allocator.py line 232). gamma=1e-6 is a page-valid input (project.html spec, line 323: 'a gamma of 10^-6 ... are valid'), so this solver is not shown to be correct; it is not established whether it is a solver defect or the suite over-constrains. Four more alternatives are required"),
 ("PRJ-R6-33", "cards: every card agrees with the CURRENT lesson text (rule 10, full read)", "course/modules/M/M7/cards.json vs L01.html-L08.html", U, "Not performed in full this round: 146 cards against eight lessons. Read this round: M7-c080, c163, c164 (changed/new) against L05 Remark 2.4 and L06 Proposition 2.1, Remark 2.2 and Proposition 3.4: all agree. The other 143 cards are not re-read; gap"),
 ("PRJ-R6-34", "browser-only claims: autosave, nothing you write leaves the browser", "project.html line 355 and footer line 474", U, "Not checkable with plain curl or in this checkout: requires the browser (Pyodide/storage). Honest gap, not run"),
 ("PRJ-R6-35", "Lab 1 prose: code prints the four KKT quantities in steps 4 to 6", "project.html line 55", P, carry(35, "project.html line 55")),
 ("PRJ-R6-36", "Lab 3 prose claims about which residuals respond", "project.html line 438", P, carry(36, "project.html line 438")),
 ("PRJ-R6-37", "card ids unique; gaps in the id sequence", "course/modules/M/M7/cards.json", P, "cards_numbers_r7.log: duplicate ids []; 146 ids unique (python json check); 18 gaps listed (informational)"),
 ("PRJ-R6-38", "pyflakes/type checks of the grader pass", "grader/test_project.py, reference.py, instance.py, starter.py", P, "mypy --no-incremental on the grader files: no issues (mypy.log); ruff check on grader: all checks passed (ruff.log)"),
 ("PRJ-R7-01", "delta since pin 44f1eb6 read in full (slice d files)", "project.html; grader/test_project.py; cards.json; index.html; tests/labs/M7/lab-M7-L02-1.py (not in slice d)", P, "git diff 44f1eb6 7aa909e read hunk by hunk for slice-d files: project.html (39, 303-322, 329, 441), test_project.py (369-410), cards.json (c080 changed; c163, c164 added). Each hunk is covered by a row above"),
]
rows_out = [{"id": i, "check": c, "location": loc, "status": s, "evidence": e} for i, c, loc, s, e in rows]
assert len({r["id"] for r in rows_out}) == len(rows_out)
verdict = "PASS" if all(r["status"] == "PASS" for r in rows_out) else "FAIL"
summ = {"rows": len(rows_out), "pass": sum(r["status"] == P for r in rows_out), "fail": sum(r["status"] == F for r in rows_out), "unverifiable": sum(r["status"] == U for r in rows_out), "mutants": len(mut), "mutants_killed": sum(m["status"] == "KILLED" for m in mut)}
frag = {
 "unit": "M7", "slice": "d", "round": 7,
 "verifier": "Haiku 5.5 (independent verifier, round 7; did not build M7)",
 "pin": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4",
 "base": "44f1eb6 (round-6 pin per B-M7-d.round6.json)",
 "checkout": str(W),
 "scratch": str(L) + " (logs, scripts, alt/); /tmp/m7d_r7_ws and /tmp/m7d_r7_alt are scratch copies",
 "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
 "verdict": verdict,
 "rows": rows_out,
 "mutants": [{"name": m["name"], "description": m["description"], "killed_by": m["killed_by"]} for m in mut],
 "registry_flags": [],
 "freshness_flags": [],
 "notes": "Round 7 re-ran checks_projects, check_pages, check_dag, run_graders seeds 0-49, collect counts, run_labs, page_smoke, ruff, mypy, mutate_graders over 96 mutants (5 new: r01-r05), the alt_float solver, and the card-number script. Five FAIL-class findings: q04 floor survivor (PRJ-R6-28); mutant survivors r02, r04, r05 (PRJ-R6-31); one alternative implementation only (PRJ-R6-32); card-number script needs TeX-fraction fix (PRJ-R6-25). Gaps: full card read (PRJ-R6-33), browser claims (PRJ-R6-34), refs (PRJ-R6-20), most numeric cards (PRJ-R6-26). Interpreter for verifying the twins: run_labs uses sys.executable -I -W error. The checkout's .venv is a symlink tracked as modified (git status shows 'M .venv')",
 "summary": summ,
}
(W / "ledgers/M7/M7-d.json").write_text(json.dumps(frag, ensure_ascii=False, indent=1) + "\n")
print(summ, verdict)
