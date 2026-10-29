"""Round 6 (M7-d): build ledgers/M7/M7-d.json from the logs of this round (rows and mutants)."""
from __future__ import annotations

import json
import pathlib
import re
from datetime import UTC, datetime

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB6-M7-d")
LOG = ROOT / "ledgers/M7/scripts/M7-d-r6/logs/mutate_0_9.txt"

mutants = []
for line in LOG.read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, desc, killed = m.groups()
    mutants.append({
        "name": name,
        "description": desc,
        "killed_by": None if killed.strip() == "None" else killed.strip(),
    })

P = "PASS"
rows = [
    {"id": "PRJ-R6-01", "check": "check_projects M7 (project panel, grader paths)", "location": "tools/check_projects.py --unit M7", "status": P,
     "evidence": "Run: 'check_projects M7: PASS' (logs/check_projects.py output)."},
    {"id": "PRJ-R6-02", "check": "check_pages M7 (hours, ladder, data-hours arithmetic)", "location": "tools/check_pages.py --unit M7", "status": P,
     "evidence": "Run: 'check_pages M7: PASS'."},
    {"id": "PRJ-R6-03", "check": "check_dag M7 (concept links in project.html)", "location": "tools/check_dag.py --unit M7", "status": P,
     "evidence": "Run: 'check_dag M7: PASS'. Stretch link envelope-theorem (project.html line 450) is an M2 concept, usable by M7 (plan section 2)."},
    {"id": "PRJ-R6-04", "check": "run_graders reference on seeds 0-49 (363 tests per seed)", "location": "course/modules/M/M7/grader/reference.py", "status": P,
     "evidence": "Run: 'run_graders M7: PASS (reference 50/50 seeds, slowest 3.4 s)'. Own run: QF_SEED=0 pytest on reference copy: 363 passed."},
    {"id": "PRJ-R6-05", "check": "starter fails the suite", "location": "course/modules/M/M7/grader/starter.py", "status": P,
     "evidence": "Scratch copy /tmp/m7d_r6/ws with starter as constrained_allocator.py, QF_SEED=0: 360 failed, 3 passed (structure and determinism checks)."},
    {"id": "PRJ-R6-06", "check": "collected test count equals the page's 363 for every seed", "location": "course/modules/M/M7/project.html line 329; grader/test_project.py", "status": P,
     "evidence": "pytest --collect-only -q for seeds 0-49 (scratch ws): 50 of 50 seeds report '363 tests collected'."},
    {"id": "PRJ-R6-07", "check": "run_labs M7 (all lab twins, incl. project-1..3)", "location": "tests/labs/M7/lab-M7-project-{1,2,3}.py", "status": P,
     "evidence": "Run: 'run_labs M7: PASS (11/11)'."},
    {"id": "PRJ-R6-08", "check": "project twins alone under python -I -W error; stdout equals the page's expected block", "location": "project.html lines 155, 271/281 expected blocks; 435-437", "status": P,
     "evidence": "ledgers/M7/scripts/M7-d-r6/labcheck.py: lab-M7-project-1 exit 0, stdout==expected True; lab-M7-project-3 exit 0, stdout==expected True; lab-M7-project-2 twin (completed) exit 0, stdout==expected True."},
    {"id": "PRJ-R6-09", "check": "page code equals twin (lab 1 and lab 3) and lab 2 differs only in its blanks", "location": "project.html lines 56-154, 172-270, 372-434", "status": P,
     "evidence": "labcheck.py: lab-1 and lab-3 page_code==twin True. lab-2 diff: page line 'residual = ___' vs twin 'residual = [GAMMA * ...]' and 'signs = ___' / 'dual_feasible = ___' vs the twin's expressions; no other line differs."},
    {"id": "PRJ-R6-10", "check": "Lab 1 numbers re-derived in an independent Fraction script", "location": "project.html lines 155-166", "status": P,
     "evidence": "Independent script: w=(9/11,2/11,0), nu=-21/1100, lambda=9/1100 gives stationarity residuals (0,0,0) and budget gap 0; objective -3/220 (about -0.013636); budget-only w=(54/65,5/26,-3/130), sum 1. All match the printed expected block."},
    {"id": "PRJ-R6-11", "check": "Lab 3 residual claims re-derived by hand and by the lab", "location": "project.html lines 435-438", "status": P,
     "evidence": "Check A all zero; Check B dual residual 9/1100 and stationarity 9/550 (2 x 9/1100 flip in the third weight); Check C stationarity change gamma*Sigma*(1/1000,-1/1000,0) = (6,-16,-4)/100000, max 1/6250. Lab output matches (lab-M7-project-3 run)."},
    {"id": "PRJ-R6-12", "check": "certificate definitions (spec lines 309-317) match the grader's recomputation and the Lagrangian signs", "location": "project.html lines 309-317; grader/test_project.py lines 84-116", "status": P,
     "evidence": "Lagrangian L=f+sum lambda_j g_j with g_lower=l-w, g_upper=w-u, g_sector, g_plus=d-t, g_minus=-d-t, g_total=sum t - tau gives r^w = grad + nu - lam_l + lam_u + eta + alpha - beta and r^t = kappa - alpha - beta, exactly as lines 310-311 and test lines 91-101. Primal, dual, complementary definitions agree with lines 313-316 and test lines 105-116."},
    {"id": "PRJ-R6-13", "check": "sufficiency proposition and uniqueness proof (project.html lines 320-322)", "location": "project.html lines 320-322", "status": P,
     "evidence": "Read line by line: L convex in (w,t) given lambda>=0 and affine g; f(y) >= L(y,s) >= L(w,t) = f(w); strict-convexity midpoint argument gives uniqueness in w. Sigma=(A'A+I)/1000 PD argument x'Sigma x=(|Ax|^2+|x|^2)/1000 verified. Existence of multipliers is stated as unproved (honest)."},
    {"id": "PRJ-R6-14", "check": "linearization of the turnover constraint (lines 307)", "location": "project.html line 307", "status": P,
     "evidence": "Both directions checked: if sum|d|<=tau take t=|d|; conversely sum|d| <= sum t <= tau. Affineness in (w,t) holds."},
    {"id": "PRJ-R6-15", "check": "five hand-worked answers are correct", "location": "grader/test_project.py lines 218-246", "status": P,
     "evidence": "Hand-derived: budget only (0.6,0.4) from w=mu+0.3; zero turnover (0.5,0.5); single asset (1.0); upper bound binding (0.7,0.3) from unconstrained (0.35,0.65); turnover binding (0.6,0.4) from d=+-0.1. Reference passes all five (363 passed)."},
    {"id": "PRJ-R6-16", "check": "named ValueError conditions in spec (line 323) each have refused and accepted tests", "location": "grader/test_project.py lines 553-567, 590-596, 670-693, 697-708", "status": P,
     "evidence": "Read: symmetry, PD (singular, negative, indefinite), gamma positive, turnover >= 0, lower<=upper, start sum (1e-9), start in bounds, start sector caps, sector labels, empty sector, list lengths, non-finite, missing field, non-mapping, no assets. Each has a refused form and a valid boundary form."},
    {"id": "PRJ-R6-17", "check": "instances: SIMULATED, feasible by construction, <=3 decimals, both sectors non-empty (seeds 0-49)", "location": "course/modules/M/M7/grader/instance.py lines 34-68", "status": P,
     "evidence": "Script over 50 seeds: w0 sums to 1, lower<=w0<=upper, sector caps >= start sector sums, turnover_limit>=0, payload numbers with more than 3 decimals: 0. Label contains 'SIMULATED'."},
    {"id": "PRJ-R6-18", "check": "solution file may use the standard library only; no grader import", "location": "grader/test_project.py lines 268-282", "status": P,
     "evidence": "Test code read: AST import check against sys.stdlib_module_names and grader names. Reference imports only math, collections.abc, dataclasses, fractions, itertools, typing."},
    {"id": "PRJ-R6-19", "check": "ruff check and ruff format on labs and grader; mypy --strict on twins and grader files", "location": "tests/labs/M7, course/modules/M/M7/grader", "status": P,
     "evidence": "ruff check: 'All checks passed!'; ruff format --check: '15 files already formatted'; mypy --no-incremental --strict: 'Success: no issues found in 14 source files'."},
    {"id": "PRJ-R6-20", "check": "references cited by the reading list exist in the registry", "location": "project.html lines 459-460; references/references.json", "status": P,
     "evidence": "boyd2004convex and stokey1989recursive both present with status verified and used_by ['M7']. verify_refs --offline: '560 entries, 0 problems'."},
    {"id": "PRJ-R6-21", "check": "page_smoke M7 (page render, in-browser grader run)", "location": "course/modules/M/M7/project.html", "status": P,
     "evidence": "page_smoke: 'page_smoke modules/M/M7/project.html: PASS'; in-browser grader 'All 363 tests pass on seed 1381087627. (2.9 s)'; 'page_smoke M7: PASS'."},
    {"id": "PRJ-R6-22", "check": "hours arithmetic: project components sum to 33; lessons 77 + project 33 = 110", "location": "project.html lines 337-351; course/modules/M/M7/index.html data-hours-*", "status": P,
     "evidence": "2+3+10+6+7+5 = 33 (table lines 341-346). Hub: data-hours-lessons=77, data-hours-project=33 (grep index.html)."},
    {"id": "PRJ-R6-23", "check": "no process words in learner text", "location": "project.html (full text)", "status": P,
     "evidence": "grep -i for fixer, verifier, round, builder, slice on project.html: no match."},
    {"id": "PRJ-R6-24", "check": "notation: symbols on the project page against notation/notation.json", "location": "project.html lines 303-308; notation/notation.json", "status": P,
     "evidence": "gamma, mu, Sigma, w0, l, u, c_k, tau, k(i), S_k, d, t, nu, lambda, eta, alpha, beta, kappa, n, K, A are defined on the page (lines 287-308, 293). gamma and mu are local per the registry's own note (about field). No registered symbol is reused with another meaning, except the glyph in PRJ-R6-27."},
    {"id": "PRJ-R6-25", "check": "cards: numbers on each card's back appear in the card's own lesson (rule 10), with no duplicate ids or fronts", "location": "course/modules/M/M7/cards.json (144 cards)", "status": P,
     "evidence": "ledgers/M7/scripts/M7-d-r6/cards_numbers_r6.py: 15 tokens not found as plain text; each checked: they appear in the lesson as LaTeX \\tfrac (e.g. c048 17/30 and 11/30, c043 1/8 as \\tfrac18, c064 49/300, c084 1/8, c080 4/11, 11/4, 18/11). No duplicate ids or fronts. grades T and C only; every C card has a basis."},
    {"id": "PRJ-R6-26", "check": "cards: numeric claims re-derived from lab twin outputs", "location": "cards.json c009-c016, c027-c030, c049-c050, c060, c062-c064, c067, c069, c080, c086-c090, c102, c108-c116, c118, c130-c137, c150-c157", "status": P,
     "evidence": "Lab outputs in logs/lab-M7-L0N-1.out. Confirmed: c010 (midpoint 3/2, chord 1, gap -1/2), c012 (184 pairs, 552 = 3x184), c016 (2573/3125), c027 (Sigma rows), c028 (177/55, 47/55, 17/55, -9/55, 177/110), c060 (7/300 recomputed: best nu on grid -157/300), c062 (g=-1/2), c064 (-199/300), c080 (identity verified by Fraction), c088 (551/722 = 29/38 = 43/38 - 7/19), c089 (33x33 = 1089), c108-c109 (mu, diag), c110-c116 (lab rows), c130-c137 (table), c153 (378 = 3x126), c154 (ratios 0.9)."},
    {"id": "PRJ-R6-27", "check": "notation glyph 1 (all-ones vector) collides with the registry macro \\mathbf{1} (indicator)", "location": "project.html lines 306 and 313 use \\mathbf{1}; notation/notation.json macro \\indic = \\mathbf{1} ('indicator function')", "status": "FAIL",
     "evidence": "project.html line 306 writes \\(\\mathbf{1}^{\\top} w = 1\\) and line 313 writes \\(|\\mathbf{1}^{\\top} w - 1|\\). The page never defines 1 as the all-ones vector in Conventions (lines 303-308 define every other symbol). notation/notation.json defines \\mathbf{1} as the indicator function via macro \\indic.",
     "fix": "Add to Conventions (project.html line 303): 'Write 1 for the vector in R^n whose entries are all one.' Architect to decide whether the registry macro collision needs a registry entry."},
    {"id": "PRJ-R6-28", "check": "grader: dual residual floor at zero is exercised by the suite (spec line 315)", "location": "grader/test_project.py lines 105-116 and 365-369; grader/reference.py line 287; project.html line 315", "status": "FAIL",
     "evidence": "Mutant q04 (dual = -min(mult) with no max(0, .)) SURVIVES seeds 0-9 (logs/mutate_0_9.txt). The spec defines the dual residual as the larger of 0 and the negative of the smallest inequality multiplier (project.html line 315). Measured: over the reference's outputs for seeds 0-49 the smallest inequality multiplier is 0.0 on all 50 seeds, so the floor clause is never exercised. No test asserts that the reported dual residual is non-negative.",
     "fix": "Add to test_certificate_residuals_are_within_tolerance (grader/test_project.py line 365): assert float(seed_output()['certificate']['dual_residual']) >= -TOL and check the sign-clamped definition on hand cases. Note that no seed's output has all-positive inequality multipliers, so q04 is observable only on a solver output with all-positive multipliers; the non-negativity assertion is the cheapest kill."},
    {"id": "PRJ-R6-29", "check": "hand-worked cases: the certificate fields are checked against the recomputation", "location": "grader/test_project.py lines 388-397 (test_hand_case_matches_its_worked_answer) and project.html line 329 ('each with its own certificate check')", "status": "FAIL",
     "evidence": "The hand-case test calls output_shape, compares weights to 1e-8 and calls assert_kkt, which recomputes residuals from the student's multipliers. It never compares out['certificate'] with recomputed_certificate(); the certificate-agreement test (lines 356-362) runs on the seed case only. A certificate with a wrong field on a hand case passes.", "fix": "Add an assertion in test_hand_case_matches_its_worked_answer that float(out['certificate'][key]) equals recomputed_certificate(case, weights, multipliers)[key] within 1e-9 for each key."},
    {"id": "PRJ-R6-30", "check": "objective against three feasible comparators (page line 329)", "location": "grader/test_project.py lines 372-379; project.html line 329", "status": "FAIL",
     "evidence": "Comparator y = (1 - y_weight) w + y_weight w0. The parameter 0.0 (id 'start') gives y = w, the answer itself, so that comparison is trivially true; the starting portfolio (y_weight 1.0) is never compared. The page says three feasible comparators that are mixes of the answer and the starting portfolio, so only two are real comparisons.",
     "fix": "Parametrize y_weight over (0.25, 0.5, 0.75) or (0.25, 0.75, 1.0) and fix the ids so 'start' means the starting portfolio, or change the page to say two comparators."},
    {"id": "PRJ-R6-31", "check": "mutant suite: all grader mutants killed (ledgers/M7/mutants, seeds 0-9)", "location": "ledgers/M7/mutants/ (91 files); tools/mutate_graders.py --unit M7 --seeds 0-9", "status": "FAIL",
     "evidence": "Run: 'mutate_graders M7: FAIL (90/91 killed)'. The one survivor is q04 (PRJ-R6-28). The 87 earlier mutants are all killed; the new q01, q02, q03 are killed (test_certificate_agrees_with_the_recomputed_residuals seed 3 and seed 0; test_missing_field_is_refused_with_value_error[gamma] seed 0).", "fix": 'Kill q04 (see PRJ-R6-28); re-run tools/mutate_graders.py --unit M7 --seeds 0-9 until 91/91 are killed.'},
    {"id": "PRJ-R6-32", "check": "five alternative correct implementations pass the suite (rule 11, T2)", "location": "ledgers/M7/scripts/M7-d-r6/alt_float/constrained_allocator.py", "status": "FAIL",
     "evidence": "Only one alternative was built and run: the reference algorithm in float with different cutoffs (1e-9 tolerance, 1e-11 and 1e-12 zero tests). It passes all 363 tests on 35 of 50 seeds; on the other 15 seeds 1-3 tests fail, all of them the valid gamma boundary cases (1e-6 and 1e-9) because the alternative raises RuntimeError('the working set lost independence') at gamma=1e-6. The suite demands an answer, not a method, so this is a fragility of that alternative, not an over-constraint of the grader. Four further alternatives (exact enumeration, projected gradient, ADMM, log-barrier) were not built.",
     "fix": "Write the four other alternatives and a robust float variant; run each on seeds 0-49 through a harness (plan T2) and record the results."},
    {"id": "PRJ-R6-33", "check": "cards: every card agrees with the current lesson text (rule 10, full read)", "location": "course/modules/M/M7/cards.json vs L01.html-L08.html", "status": "UNVERIFIABLE",
     "evidence": "144 cards read in full. Numeric claims were checked (PRJ-R6-25, PRJ-R6-26) and lesson text was searched for numbers, but the 350 KB of lesson text was not read against each card's theorem and misconception wording in this round.", "fix": 'Read each card against the lesson section it cites (cards.json lesson field) and record a row per lesson (L01-L08) with the card ids checked.'},
    {"id": "PRJ-R6-34", "check": "browser-only claims: autosave and 'nothing you write leaves it'", "location": "project.html line 355 and footer line 474", "status": "UNVERIFIABLE",
     "evidence": "Not tested: no browser session was driven, and the storage and network behaviour of the grader panel was not inspected. page_smoke ran the in-browser grader (363 pass, 2.9 s), which covers the runtime claim only.", "fix": 'Drive the project page in a browser: type code, reload, confirm the saved draft; inspect network requests to confirm no code leaves the page; record the observations as a row.'},
    {"id": "PRJ-R6-35", "check": "Lab 1 prose: 'the code prints the four KKT quantities in steps 4 to 6'", "location": "project.html line 55", "status": P,
     "evidence": "Steps 4 (stationarity), 5 (primal: budget gap, smallest and largest weight), 6 (dual sign and complementary products) print the four conditions. Wording is loose but accurate."},
    {"id": "PRJ-R6-36", "check": "Lab 3 prose claims about which residuals respond", "location": "project.html line 438", "status": P,
     "evidence": "Output: B moves dual and stationarity; C moves stationarity only; primal and complementary stay zero. The paragraph says so (honest scope)."},
    {"id": "PRJ-R6-37", "check": "card ids unique; gaps in the id sequence", "location": "cards.json", "status": P,
     "evidence": "No duplicate ids; ids M7-c034, 035, 045, 054, 055, 066, 072, 094-096, 119-120, 138-141, 158-159 are absent and c160-c162 sit after c157 in file order. Gaps are not a defect by themselves; noted for the builder."},
    {"id": "PRJ-R6-38", "check": "pyflakes-level and type checks of the grader passed; the tests use the page's ValueError set", "location": "grader/test_project.py", "status": P,
     "evidence": "mypy --strict and ruff pass on the grader (PRJ-R6-19). Starter raises NotImplementedError and the suite fails on it (PRJ-R6-05)."},
]

fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 6,
    "verifier": "Haiku 5.5 (independent verifier, round 6; did not build M7)",
    "pin": "44f1eb6",
    "base": "not recorded: the round-5 fragment /Users/billyribeiro/.fanout/frags/B-M7-d.round5.json is absent from the frags folder; every row was re-derived, none carried",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyB6-M7-d",
    "scratch": "/tmp/m7d_r6 (ws/ holds grader copies outside the repo; labcheck and logs are copied under ledgers/M7/scripts/M7-d-r6/)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "notation/notation.json: macro \\indic is \\mathbf{1} (indicator function); M7 project.html uses \\mathbf{1} for the all-ones vector (PRJ-R6-27). Architect decision needed."
    ],
    "freshness_flags": [],
    "notes": (
        "Slice d: project.html, grader/ (reference, instance, starter, test_project), project labs 1-3, cards.json. "
        "Delta: the round-5 pin is not recorded, so the whole slice was re-verified. Four new mutants q01-q04 were written. "
        "Four FAIL rows are grader or page defects (PRJ-R6-28, -29, -30, -27) and two are verification gaps (PRJ-R6-32, -33). "
        "Could not check: the full card-to-lesson text read (PRJ-R6-33), browser storage and privacy claims (PRJ-R6-34), "
        "per-test timing under Pyodide below the page's 5 s bound (only the 2.9 s suite time was observed), and four of the five alternative implementations (PRJ-R6-32). "
        "Full gate for the M7 unit not run: check_pages/check_dag/check_projects/run_graders/run_labs/mutate/page_smoke/ruff/mypy/verify_refs were run for M7 only."
    ),
}

counts = {"pass": sum(r["status"] == "PASS" for r in rows), "fail": sum(r["status"] == "FAIL" for r in rows),
          "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
fragment["summary"] = {"rows": len(rows), **counts, "mutants": len(mutants), "mutants_killed": sum(bool(m["killed_by"]) for m in mutants)}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", out, fragment["summary"])
