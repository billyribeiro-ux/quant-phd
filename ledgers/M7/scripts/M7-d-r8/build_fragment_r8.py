"""Assemble the round-8 M7-d fragment from the logs written in this checkout (rows restate evidence; no row is asserted)."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1])
S = "ledgers/M7/scripts/M7-d-r8"
mut = []
for line in (ROOT / S / "mutate_all102.log").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    desc = re.sub(r"^Student error \S+?:\s*", "", desc).strip()
    mut.append({
        "name": name,
        "description": desc,
        "killed_by": None if killed == "None" else killed,
        "status": status,
    })
assert len(mut) == 102, len(mut)

P = "Carried from round 7 (grader/, tests/labs/M7/lab-M7-project-*.py, tools/, references/ byte-identical since 7aa909e):"
C6 = "Carried from round 7 (project.html lines 155-166 byte-identical since 7aa909e):"
rows = [
 ("PRJ-R6-01", "tools/check_projects.py --unit M7", "tools/check_projects.py", "PASS", f"check_projects M7: PASS (log {S}/check_projects.log, exit 0)"),
 ("PRJ-R6-02", "tools/check_pages.py --unit M7 (hours, ladder, data-hours)", "tools/check_pages.py", "PASS", f"check_pages M7: PASS ({S}/check_pages.log, exit 0)"),
 ("PRJ-R6-03", "tools/check_dag.py --unit M7 (concept links)", "course/modules/M/M7/project.html", "PASS", f"check_dag M7: PASS ({S}/check_dag.log, exit 0)"),
 ("PRJ-R6-04", "run_graders reference, seeds 0-49", "course/modules/M/M7/grader/reference.py", "PASS", f"run_graders M7: PASS, reference 50/50 seeds ({S}/run_graders.log)"),
 ("PRJ-R6-05", "starter fails the suite", "course/modules/M/M7/grader/starter.py", "PASS", "Carried from round 7 (grader/starter.py and tools/run_graders.py byte-identical since 7aa909e): starter raises NotImplementedError (starter.py line 20), so the suite fails on it"),
 ("PRJ-R6-06", "collected test count equals the page's 363 for every seed", "course/modules/M/M7/project.html line 329; grader/test_project.py", "PASS", f"pytest --collect-only: '363 tests collected' for QF_SEED 0, 17, 49 ({S}/collect.log)"),
 ("PRJ-R6-07", "all M7 lab twins via run_labs", "tests/labs/M7/", "PASS", f"run_labs M7: PASS (11/11) ({S}/run_labs.log)"),
 ("PRJ-R6-08", "project twins under python -I -W error; stdout equals page expected block", "project.html lines 155, 271/281, 435-437", "PASS", f"run_labs runs each twin as sys.executable -I -W error and matches the expected block: PASS 11/11 ({S}/run_labs.log)"),
 ("PRJ-R6-09", "page code equals twin (lab 1, lab 3); lab 2 differs only in its blanks", "project.html lines 56-154, 172-270, 372-434", "PASS", f"run_labs M7 PASS keeps page code and twin in agreement ({S}/run_labs.log); project twins byte-identical since 7aa909e"),
 ("PRJ-R6-10", "Lab 1 numbers re-derived", "project.html lines 155-166", "PASS", C6 + " step values (9/11, 2/11, 0; nu=-21/1100; lower multiplier 9/1100; objective -3/220) re-read against the printed block"),
 ("PRJ-R6-11", "Lab 3 residual claims re-derived", "project.html lines 435-438", "PASS", "Carried from round 7 (project.html lines 435-438 byte-identical since 7aa909e): check B stationarity 9/550 = 2 x 9/1100 and check C primal and complementary zero, as printed"),
 ("PRJ-R6-12", "certificate definitions (page 306-316) match the grader recomputation", "project.html lines 306, 313, 315; grader/test_project.py lines 105-116", "PASS", "Carried from round 7 (project.html lines 306, 313, 315 and grader/test_project.py lines 105-116 byte-identical since 7aa909e): the grader's primal, dual, stationarity and complementary definitions match page lines 313-316; the dual floor is a separate defect, PRJ-R6-28"),
 ("PRJ-R6-13", "sufficiency proposition and uniqueness proof (page 320-322)", "project.html lines 320-322", "PASS", "Carried from round 7 (project.html lines 320-322 byte-identical since 7aa909e): Lagrangian chain f(y) >= L(y,s) >= L(w,t) = f(w) and the midpoint argument are valid under the stated hypotheses"),
 ("PRJ-R6-14", "linearization of turnover constraint", "project.html line 307", "PASS", "Carried from round 7 (project.html line 307 byte-identical since 7aa909e): both directions re-read, and t_i = |d_i| satisfies the three conditions"),
 ("PRJ-R6-15", "five hand-worked answers are correct", "grader/test_project.py lines 218-246", "PASS", "Carried from round 7 (grader/test_project.py byte-identical since 7aa909e): re-worked this round: budget-only (0.6,0.4), zero turnover (0.5,0.5), single asset (1.0), upper bound (0.7,0.3), turnover binding (0.6,0.4)"),
 ("PRJ-R6-16", "named ValueError conditions have refused and accepted tests", "grader/test_project.py lines 553-567, 590-596, 670-693, 697-708", "PASS", "Carried from round 7 (grader/test_project.py byte-identical since 7aa909e); the suite passes 363/363 on the reference for seeds 0-49 (run_graders)"),
 ("PRJ-R6-17", "instances SIMULATED, feasible by construction, <=3 decimals, both sectors non-empty", "course/modules/M/M7/grader/instance.py lines 34-68", "PASS", "Carried from round 7 (grader/instance.py byte-identical since 7aa909e); re-read this round: label contains SIMULATED (line 57), starting weights sum to 100 hundredths, caps and upper bounds never below w0, labels i mod 2 shuffled so both sectors are non-empty for n >= 3"),
 ("PRJ-R6-18", "solution may use standard library only; no grader import", "grader/test_project.py lines 268-282", "PASS", "Carried from round 7 (grader/test_project.py byte-identical since 7aa909e); the three alternatives and the reference import only the standard library"),
 ("PRJ-R6-19", "ruff check and format on the labs and grader; mypy", "tests/labs/M7; course/modules/M/M7/grader", "PASS", f"ruff check course/modules/M/M7 tests/labs/M7: 'All checks passed!' ({S}/ruff.log); mypy --no-incremental: 'Success: no issues found in 255 source files' ({S}/mypy.log)"),
 ("PRJ-R6-20", "reading-list keys resolve in the registry (offline integrity)", "course/modules/M/M7/project.html lines 459-460; references/references.json", "PASS", f"tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' ({S}/verify_refs.log); boyd2004convex at references.json line 3648 and stokey1989recursive at line 21295. The live run was not performed; the reading list is not graded"),
 ("PRJ-R6-21", "page_smoke M7 project (render and in-browser grader)", "course/modules/M/M7/project.html", "PASS", f"page_smoke M7: PASS; 'in-browser grader: All 363 tests pass on seed 1395987016' ({S}/page_smoke.log)"),
 ("PRJ-R6-22", "hours: project components sum to 33; lessons 77 + project 33 = 110", "project.html lines 337-351; index.html data-hours", "PASS", f"project.html table rows 2+3+10+6+7+5 = 33 (lines 341-346); check_pages M7 PASS ({S}/check_pages.log)"),
 ("PRJ-R6-23", "no process words in learner text", "project.html (delta lines 39, 290); course/modules/M/M7/cards.json", "PASS", "grep for round/verif/builder/draft/todo/placeholder/agent/audit over project.html, cards.json and L01-L06 finds only learner exercise wording (L03 line 429 'verify that', an instruction to the learner)"),
 ("PRJ-R6-24", "notation: symbols vs notation/notation.json", "project.html lines 303-308", "PASS", "notation/notation.json registers 8 program-wide symbols (T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q); none occurs on the project page or in M7 cards; the page's other letters are lesson-local per the registry's 'about' field"),
 ("PRJ-R6-25", "cards: numbers on each back appear in the card's own lesson; no duplicate ids or fronts; non-T grades have a basis", "course/modules/M/M7/cards.json (149 cards)", "PASS", f"{S}/cards_numbers_r8.log: 149 cards, 149 distinct ids and fronts, grades T 112 / C 37, no non-T card without basis; 15 flagged tokens resolve as TeX fractions (\\tfrac23, \\tfrac18, \\tfrac{14}{15}, \\tfrac{17}{30}, \\tfrac{11}{30}, \\tfrac{7}{300}, \\tfrac{49}{300}, \\tfrac{199}{150}, \\tfrac{18}{11}, \\tfrac{11}{4}, \\tfrac{4}{11}, \\tfrac{1}{8}) found by a TeX-aware grep in the lesson"),
 ("PRJ-R6-26", "cards: numeric claims re-derived or matched to lab output", "cards.json", "PASS", "Matched to the printed expected blocks: L01 (c012, c016), L02 (c027-c030), L03 (c049, c050), L04 (c063), L05 (c087-c089, c093), L06 (c108-c111, c112, c115, c116), L07 (c130-c137), L08 (c150-c154, c157). Re-derived with exact Fractions: c028 (177/55, 177/110), c060 (7/300), c062 (-1/2), c063 (1331 dual points, 27951 pairs, unique max), c064 (199/150, -199/300), c048 (14/15, -11/30, sum 17/30), c046/c047, c050, c082, c086, c113 (0.5722548 unrounded), c114 (0.5588607 unrounded; 0.558860 from printed weights)"),
 ("PRJ-R6-27", "notation glyph 1 (all-ones) vs registry macro", "course/modules/M/M7/project.html lines 306, 313", "PASS", "Carried from round 7 (project.html lines 306, 313 byte-identical since 7aa909e)"),
 ("PRJ-R6-28", "dual residual floor at zero is exercised by the suite (spec line 315)", "grader/test_project.py lines 105-116, 365-369; grader/reference.py line 287", "FAIL", f"Mutant q04 (dual residual = -min multiplier, no floor) SURVIVES seeds 0-9 ({S}/mutate_all102.log). {S}/minmult_r8.py over seeds 0-49 of the reference: min inequality multiplier is 0.0 on 50 of 50 seeds, so the floor max(0, -min) is never exercised. The suite never asserts that a certificate field is non-negative and no hand case has all inequality multipliers positive, so no test can tell the no-floor residual from the page's definition (page line 315)."),
 ("PRJ-R6-29", "hand-worked cases: certificate fields checked against the recomputation", "grader/test_project.py lines 388-410", "PASS", "Carried from round 7 (grader/test_project.py byte-identical since 7aa909e): assert_kkt and the recomputed certificate are applied to every hand case"),
 ("PRJ-R6-30", "objective against three feasible comparators (page line 329)", "grader/test_project.py lines 372-383; project.html line 329", "PASS", "Carried from round 7 (grader/test_project.py and project.html line 329 byte-identical since 7aa909e): mixes at 0.25, 0.5, 0.75 of the way from the answer to w0 are convex combinations of feasible points"),
 ("PRJ-R6-31", "mutant suite: every grader mutant killed (ledgers/M7/mutants, seeds 0-9)", "ledgers/M7/mutants/ (102 files); tools/mutate_graders.py --unit M7 --seeds 0-9", "FAIL", f"mutate_graders M7: FAIL, 98/102 killed ({S}/mutate_all102.log). Survivors: q04 (PRJ-R6-28); r02_turnover_total_residual_dropped_from_primal, r04_budget_left_out_of_primal_residual, r05_turnover_total_slackness_term_zeroed. Each is the reference solver with one certificate term removed or zeroed; the removed term is <= 0 (r02, r05 when the turnover constraint holds or its multiplier vanishes) or within 1e-9 (r04: |sum w - 1| ~ 1e-16 on the reference), so the value agrees with the page's definition on every output that passes the other checks. The page states each term (lines 313, 316). New mutants r8_m01 to r8_m06 are all killed (PRJ-R8-15)."),
 ("PRJ-R6-32", "five alternative correct implementations pass the suite (rule 11)", "ledgers/M7/scripts/M7-d-r8/alt/ (3 files); ledgers/M7/scripts/M7-d-r7/alt/alt_float.py", "FAIL", f"Three exact active-set alternatives pass 363/363 on seeds 0-49 (alts_0-9.log, alts_10-49.log: 150 of 150 runs). The round-7 float solver alt_float fails 4 of 10 seeds (seeds 1, 7, 8, 9) on valid gamma boundary cases (gamma = 1e-9, 1e-6, page line 323) with RuntimeError 'the working set lost independence'; it is not a correct implementation. Only three correct alternatives were run; a fourth and fifth were not written. The three alternative files were found committed in the checkout and were not authored by this verifier."),
 ("PRJ-R6-33", "cards: every card agrees with the CURRENT lesson text (rule 10, full read)", "course/modules/M/M7/cards.json vs L01.html-L08.html", "UNVERIFIABLE", "All 149 cards were read in full this round, every cited Remark/Theorem/Proposition/Example/Problem resolves in its lesson (cards_numbers_r8 citation check: 0 unresolved, Problem M3 and P2 are titled 'M3 ·' and 'P2 ·' in L04 and L06), and every changed card (c009, c042, c080, c084, c100, c107, c165, c166, c167) was checked against the current lesson text. The prose claims of the other ~135 cards were not each compared with the current lesson wording; this gap is honest"),
 ("PRJ-R6-34", "browser-only claims: autosave; nothing you write leaves the browser", "project.html line 355 and footer line 474", "UNVERIFIABLE", "Requires the browser's storage behaviour; not checked with plain curl or in this checkout. Honest gap, not run"),
 ("PRJ-R6-35", "Lab 1 prose: code prints the four KKT quantities in steps 4 to 6", "project.html line 55", "PASS", "Carried from round 7 (project.html line 55 byte-identical since 7aa909e): steps 4, 5 and 6 print stationarity residuals, budget gap and dual signs, as in the expected block"),
 ("PRJ-R6-36", "Lab 3 prose claims about which residuals respond", "project.html line 438", "PASS", "Carried from round 7 (project.html line 438 byte-identical since 7aa909e): candidate B moves dual and stationarity, candidate C moves stationarity; primal and complementary are zero in all three printed lines"),
 ("PRJ-R6-37", "card ids unique; gaps in the id sequence", "course/modules/M/M7/cards.json", "PASS", "149 distinct ids (cards_numbers_r8.log: duplicate ids []); gaps at c034, c035, c045, c054, c055, c066, c072, c094-c096, c119, c120, c138-c141, c158, c159 are informational, not a rule"),
 ("PRJ-R6-38", "pyflakes/type checks of the grader", "grader/test_project.py, reference.py, instance.py, starter.py", "PASS", f"ruff and mypy pass on the grader directory ({S}/ruff.log, {S}/mypy.log)"),
 ("PRJ-R7-01", "delta since pin 44f1eb6 read in full (round-7 row)", "project.html; grader/test_project.py; cards.json; tests/labs/M7", "PASS", "Round-7 row kept for its own scope; the delta since 7aa909e is read in full under PRJ-R8-01 to PRJ-R8-11"),
 ("PRJ-R8-01", "delta since 7aa909e: project.html lede (line 39) wording", "course/modules/M/M7/project.html line 39", "PASS", "'returns with each answer its Lagrange multipliers, defined in the specification below, and a certificate that checks its optimality conditions to the stated tolerance': multipliers are defined at project.html lines 308-316 and the tolerance at line 318 (1e-8)"),
 ("PRJ-R8-02", "delta since 7aa909e: spec context (line 290) 'checks the four KKT conditions ... to the stated tolerance'", "course/modules/M/M7/project.html line 290", "PASS", "Tolerance stated at project.html line 318 (1e-8, recomputed agreement 1e-9); grader TOL = 1e-8 at test_project.py line 36 and the 1e-9 agreement at line 360"),
 ("PRJ-R8-03", "cards c009 and c165 (Q1, Q2 eigenvalues) against L01", "cards.json c009, c165; L01.html lines 153-154, 332, 387", "PASS", "Q1 eigenvalues 3 and 1, Q2 eigenvalues 3 and -1 (recomputed by hand: det(Q - lI)); Example 3.3 (L01 line 153), Problem P3 'A negative eigenvalue refutes convexity' (L01 line 387), Proposition 3.2 (L01 line 134)"),
 ("PRJ-R8-04", "card c042 (sufficiency theorem) against L03 Theorem 2.1 and Remark 2.2", "cards.json c042; L03.html lines 104-118", "PASS", "Theorem 2.1 (L03 line 104) assumes f, g_i convex and differentiable and h_j affine; Remark 2.2 (line 117) 'what the proof uses' matches the card's hypothesis list"),
 ("PRJ-R8-05", "cards c080 and c166 (Remark 2.4) against L05", "cards.json c080, c166; L05.html lines 124-125", "PASS", "Completing-the-square identity expanded by hand: (2x1+x2/2)^2 + (11/4)(x2+4x3/11)^2 + (18/11)x3^2 = 4x1^2+3x2^2+2x3^2+2x1x2+2x2x3 = x'Qx; Av = 0 for v=(-2,1,1); Qxhat + c = -A'lambda* gives the vanishing linear term (L05 line 125)"),
 ("PRJ-R8-06", "card c084 (midpoint uniqueness) against L05 Proposition 3.4", "cards.json c084; L05.html lines 160-170", "PASS", "Proposition 3.4 (midpoint convex F, Q positive definite) at line 160; the midpoint identity f(z) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y) was re-derived for f = (1/2)x'Qx + c'x"),
 ("PRJ-R8-07", "cards c100 and c167 (budget closed form, 1'z > 0) against L06 Theorem 1.3 and P2", "cards.json c100, c167; L06.html lines 69-79, 475-480", "PASS", "Theorem 1.3 (L06 lines 69-79) states w = (y - lambda z)/gamma and lambda = (1'y - gamma)/(1'z) with 1'z > 0; the proof uses Theorem 2.3 of L05 (line 77); problem P2 (line 476) 'The budget multiplier denominator is positive'; 1'z = z'Sigma z since Sigma z = 1"),
 ("PRJ-R8-08", "card c107 (QP with turnover) against L06 Proposition 3.4 and Remark 3.5", "cards.json c107; L06.html lines 134-145", "PASS", "Proposition 3.4 (L06 line 134) and the linear form (L06 line 145) match the card's statement; the removed sentence about Lab 1 is not needed"),
 ("PRJ-R8-09", "L06 notation change a,b -> y,z: no stale meaning left", "course/modules/M/M7/L06.html lines 70-79, 120, 165-167, 267-270, 477-479, 548", "PASS", "grep: a^T w <= beta at L06 line 120 is the coefficient vector of Definition 3.1 (local, lesson-defined); y, z are not registered in notation/notation.json (8 entries) and are defined where introduced (line 70)"),
 ("PRJ-R8-10", "grader, twins, tools, references unchanged since the round-7 pin", "course/modules/M/M7/grader/; tests/labs/M7/lab-M7-project-*.py; tools/; references/", "PASS", "git diff --quiet 7aa909e ce7b382 over these paths: grader, project twins, tools and references all unchanged (exit 0)"),
 ("PRJ-R8-11", "L06 lab twin change (tests/labs/M7/lab-M7-L06-1.py) still runs and matches its expected block", f"tests/labs/M7/lab-M7-L06-1.py; L06.html", "PASS", f"run_labs M7: PASS (11/11) including L06 ({S}/run_labs.log)"),
 ("PRJ-R8-12", "delta: L06 numbers in cards c113 and c114 (unrounded values)", "cards.json c113, c114; L06.html Part D and Part B", "PASS", "Recomputed from the twin's own functions (exec without main): objective difference at gamma=16 is 0.5722548315 (card: 0.5722548); turnover at gamma=4 is 0.5588607333 (card: 0.5588607); from the printed six-place weights it is 0.5588600 (card: 0.558860)"),
 ("PRJ-R8-13", "new student-error mutants r8_m01..r8_m06 (verifier's own, >= 3 required)", "ledgers/M7/mutants/r8_m01..r8_m06", "PASS", f"All six killed on seed 0 or 2: start sum one-sided (r8_m01), equal bounds refused (r8_m02), weights rounded to 6 places (r8_m03), turnover from zero (r8_m04), sector cap per asset (r8_m05), gamma = 0 accepted (r8_m06); generated by {S}/make_mutants_r8.py"),
 ("PRJ-R8-14", "three exact alternatives pass the suite, seeds 0-49", f"{S}/alt/alt_reverse_order.py, alt_nullspace.py, alt_empty_start.py", "PASS", f"150 of 150 runs pass 363/363 ({S}/alts_0-9.log, {S}/alts_10-49.log); provenance: committed in the checkout, not authored here"),
 ("PRJ-R8-15", "reference multiplier scan (supports PRJ-R6-28)", f"{S}/minmult_r8.py", "PASS", "Scan of the reference over seeds 0-49 completed: min inequality multiplier 0.0 on 50/50 seeds (supports PRJ-R6-28)"),
]
rows_out = []
for rid, check, loc, status, ev in rows:
    r = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        r["fix"] = {
            "PRJ-R6-28": "Add a hand case with every inequality multiplier positive (or assert each certificate field >= 0 on seed outputs) so the dual floor of page line 315 is tested.",
            "PRJ-R6-31": "Decide whether a certificate term that is zero on every feasible correct output must be detectable; if yes, add a test that fails a certificate whose primal residual omits a violated constraint (r02, r04) or whose complementary term omits kappa*g (r05), with a hand-built infeasible probe. q04 is fixed by the PRJ-R6-28 fix.",
            "PRJ-R6-32": "Write two more correct, independent alternatives (for example a different working-set order or a null-space method) and fix or drop alt_float; it fails valid gamma boundary inputs the page names.",
            "PRJ-R6-33": "Compare each remaining card's prose with the current lesson text (about 135 cards) and record a row per lesson.",
            "PRJ-R6-34": "Verify the autosave and storage statements in a browser session and record the result.",
        }[rid]
    rows_out.append(r)

frag = {
    "unit": "M7",
    "slice": "d",
    "round": 8,
    "verifier": "Haiku 5.5 (independent verifier, round 8; did not build M7)",
    "pin": "ce7b3821c288da3dbba5dd4c90fb87dfd6d30089",
    "base": "7aa909e95b757b1abf7b75186d5fa1ed7d1945a4 (round-7 pin per B-M7-d.round7.json)",
    "checkout": str(ROOT),
    "scratch": str(ROOT / S),
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows_out,
    "mutants": [
        {"id": m["name"], "name": m["name"], "description": m["description"], "killed_by": m["killed_by"], "status": m["status"]}
        for m in mut
    ],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta since 7aa909e: project.html lede (line 39) and spec context (line 290); cards.json (c009, c042, c080, c084, c100, c107 changed; c165-c167 added); L01-L06 lessons; L06 lab twin. grader/, project twins, tools/, references/ unchanged. "
        "Gates: check_projects, check_pages, check_dag, run_labs 11/11, run_graders 50/50, collect 363 x3 seeds, page_smoke, ruff, mypy, verify_refs offline all PASS. "
        "Not performed: the live verify_refs run; browser-only claims; full prose comparison of all cards; a fourth and fifth correct alternative. "
        "Survivors r02, r04, r05 are observationally equal to the reference on every output that passes the other checks; they remain FAIL under the rule that a survivor is a FAIL when the page states the term (lines 313, 316)."
    ),
    "summary": {},
}
n = len(rows_out)
frag["summary"] = {
    "rows": n,
    "pass": sum(r["status"] == "PASS" for r in rows_out),
    "fail": sum(r["status"] == "FAIL" for r in rows_out),
    "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows_out),
    "mutants": len(mut),
    "mutants_killed": sum(m["status"] == "KILLED" for m in mut),
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, frag["summary"])
