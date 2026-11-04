"""Build the round-5 M7-d fragment (ledgers/M7/M7-d.json) from this round's logs. Hand-written rows; mutants parsed from the log."""

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD5-M7-d")
S = "ledgers/M7/scripts/M7-d-r5"

mutants = []
pat = re.compile(r"^KILLED (\S+?): (.*) -> (.*) \(seed (\d+)\)$")
for line in (ROOT / S / "mutate_all_r5_full_0-9.log").read_text(encoding="utf-8").splitlines():
    if not line.startswith("KILLED "):
        continue
    m = pat.match(line)
    assert m, line[:120]
    name, desc, test, seed = m.group(1), m.group(2), m.group(3), m.group(4)
    mutants.append({"name": name, "description": desc, "killed_by": f"{test} (seed {seed})"})
assert len(mutants) == 157, len(mutants)
assert not any(x["name"].startswith("x3_04") for x in mutants)

def row(i, check, location, status, evidence, fix=None):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
 row("PRJ-D1-01", "2.6-spec", "project.html:292-295; grader/instance.py:20-21,56-66", "PASS",
     "Field list at project.html:295 (gamma, mu, sigma, w0, lower, upper, sector, sector_caps, turnover_limit, label) equals the keys make_instance writes (instance.py:57-66). instance_facts_r5.log: asset counts {3: 18, 4: 14, 5: 18} over seeds 0-49; SECTOR_COUNT = 2 (instance.py:20)."),
 row("PRJ-D1-02", "2.6-spec", "project.html:299-300; grader/test_project.py:126-149; grader/reference.py:330-334", "PASS",
     "Three output keys, seven multiplier names, list sizes and four certificate keys as stated on the page are checked by output_shape (test_project.py:126-149) and returned by reference.py:330-334. run_graders_0-49.log PASS 50/50."),
 row("PRJ-D1-03", "2.4-math", "project.html:309", "PASS",
     "Re-derived: t_i >= |d_i|, t_i >= -d_i, sum t_i <= tau implies sum|d_i| <= tau (sum|d_i| <= sum t_i); t_i = |d_i| satisfies all three when sum|d_i| <= tau. Matches reference.py:189-191 and test_project.py:63-65,68-82."),
 row("PRJ-D1-04", "2.4-math", "project.html:310-313; grader/test_project.py:85-103; grader/reference.py:303-309", "PASS",
     "Re-derived from L = f + sum lambda_j g_j + nu(sum w - 1), g_j <= 0: r^w_i = gamma(Sigma w)_i - mu_i + nu - lambda^l_i + lambda^u_i + eta_k(i) + alpha_i - beta_i; r^t_i = kappa - alpha_i - beta_i. Page :312-313 and test_project.py:92-102 match term by term."),
 row("PRJ-D1-05", "2.4-math", "project.html:314-319; grader/test_project.py:106-117; grader/reference.py:262-315", "PASS",
     "Each certificate bullet (primal :315, stationarity :316, dual :317, CS :318) matches recomputed_certificate (test_project.py:106-117) and reference._certificate (reference.py:262-315). The primal gaps d_i - t_i and -d_i - t_i are <= 0 at t = |d| and do not change the maximum with 0."),
 row("PRJ-D1-06", "2.4-math", "project.html:320 (floor sentence)", "PASS",
     "Math re-derived: the floored and unfloored dual residuals differ only when min m > 0, i.e. when every inequality multiplier is positive, and then the unfloored value is -min m < 0. The sentence is true. The clause after it is the subject of PRJ-D1-23."),
 row("PRJ-D1-07", "2.4-math", "project.html:321; grader/test_project.py:37,364; grader/reference.py:21", "PASS",
     "TOL = 1e-8 for feasibility, stationarity, CS (test_project.py:37, 179-203); agreement at 1e-9 (test_project.py:364, 409); starting-portfolio checks at 1e-9 (reference.py:21, 102-108). Matches project.html:321."),
 row("PRJ-D1-08", "2.4-math", "project.html:322-325 (Proposition and proof)", "PASS",
     "Proof re-derived line by line: L convex in (w,t) (f convex in w, each g_j affine, lambda_j >= 0); stationarity makes (w,t) a minimiser of L; for feasible (y,s), f(y) >= L(y,s) >= L(w,t) = f(w) by g_j <= 0, lambda_j >= 0, budget term 0 on the feasible set and CS; uniqueness by the midpoint, feasible because the feasible set is convex, and strict convexity of f in w. All hypotheses used are stated at :323 and :325."),
 row("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:38-41", "PASS",
     "instance.py:38 integer factor matrix A; instance.py:41 Sigma = (A'A + I)/1000; x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0. The disclaimer that existence of multipliers is not proved (project.html:325) is honest."),
 row("PRJ-D1-10", "2.4-math", "project.html:326; grader/reference.py:42-108; grader/test_project.py:567-707,684-707", "PASS",
     "Each named ValueError condition has a check in reference.py (mapping :55, missing field :57-59, non-finite :42-43, no assets :62-63, one entry per asset :71-72,83-84,91-92, symmetric :76-77, positive definite :78-79, gamma :65-66, turnover :67-69, lower above upper :85-86, start sum and box :102-105, start sector cap :106-108, sector label :97-98, cap without assets :100-101). NAMED_CONDITIONS, OTHER_SIDE_REFUSED and EXACT_BOUNDARIES pass on the reference (run_graders_0-49.log)."),
 row("PRJ-D1-11", "2.6-spec", "project.html:327,330; grader/test_project.py:272-286,1043-1055; grader/reference.py:13-18", "PASS",
     "reference.py imports only stdlib (:13-18) and contains no print or warning. test_project.py:272-286 rejects non-stdlib and grader imports; :1036-1055 checks unchanged argument, silence and determinism."),
 row("PRJ-D1-12", "2.6-spec", "project.html:332; grader/test_project.py", "PASS",
     "collect_all_seeds_0-49.log: 363 tests collected for each of seeds 0-49 (50 of 50). Page count at project.html:332 is 363."),
 row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", "PASS",
     "run_labs_M7.log: PASS 11/11. labs_check_r5.log: page code equals the twin; twin run as python -I -W error exits 0, 0 bytes stderr; output equals the expected block. recompute_r5.log: budget-only 54/65, 5/26, -3/130; constrained 9/11, 2/11, 0; nu = -21/1100; lambda = 9/1100; stationarity residuals 0; objective -3/220 = -0.013636 (float -0.013636363636)."),
 row("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", "PASS",
     "labs_check_r5.log: the page code differs from the twin only on the three blanked lines (:250 residual, :261 signs, :262 dual_feasible); the twin output equals the expected block. Hypothesis and interpretation (:172, :284) describe the blanks correctly."),
 row("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", "PASS",
     "labs_check_r5.log: twin output equals the expected block. recompute_r5.log (independent Fraction recomputation): A all 0; B stationarity 9/550 (twice the multiplier 9/1100), dual 9/1100; C stationarity 1/6250, primal 0, CS 0. Every prose claim at :374 and :444 matches."),
 row("PRJ-D1-16", "2.9-structure", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml:298-301", "PASS",
     "Components 2+3+10+6+7+5 = 33 (:344-349); total 33 (:350). Hub index.html:29 data-hours-lessons=77, data-hours-project=33; 77 + 33 = 110, equal to the curriculum M7 hours 110 (curriculum/curriculum.json, 01-foundations.yaml:301). check_pages_unit.log PASS."),
 row("PRJ-D1-17", "2.9-structure", "project.html:40-49", "PASS",
     "Four rung-title spans in order (Rung 1 to 4) at :44-47; check_projects.log PASS."),
 row("PRJ-D1-18", "2.9-structure", "project.html:288-336", "PASS",
     "Read in full this round (all 482 lines). Tolerance pointer at :292 ('tolerance given under Conventions below') points at :321, where 10^-8 is stated."),
 row("PRJ-D1-19", "2.9-structure", "project.html; grader/*.py; tests/labs/M7/*", "PASS",
     "Process-word scan (round, fixer, builder, verifier, ledger, architect, TODO, draft, planner, audit, mutant, shim, census, of 50, the reference, course's own) over project.html, test_project.py, instance.py, starter.py returns only code identifiers ('solution') and no process wording; check_pages_unit.log PASS."),
 row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py:297", "PASS",
     "page_smoke_project.log: 'in-browser grader: All 363 tests pass on seed 1573569196'; 'page_smoke modules/M/M7/project.html: PASS'; 'page_smoke M7: PASS'."),
 row("PRJ-D1-21", "2.4-notation", "project.html:292-336,456; notation/notation.json", "PASS",
     "Registered symbols (notation.json symbols: T, Phi, gamma_3, gamma_4, R^*, R^{e*}, R_f, Q) do not occur on the page. The new symbol b (:456, 'budget level b') is a local letter, defined in its own sentence; it is not a registered symbol and has no other meaning on the page. gamma, mu, sigma, nu and eta are local per notation.json 'about'."),
 row("PRJ-D1-22", "2.9-structure", "project.html:292,310,456; course/concepts.html (envelope-theorem)", "PASS",
     "check_dag.log PASS. Link envelope-theorem (:456) resolves to course/concepts.html#envelope-theorem (concept defined in M2/L22). Lagrangian is taught in L03 (:310), inside the M7 prerequisite closure (plans/M7-build-plan.md:3, prerequisites M2, M3)."),
 row("PRJ-D1-23", "2.9-prose", "project.html:320", "FAIL",
     "The page says: 'The suite does not test the case in which the floor changes the value ... the suite does not separate it from its absence.' Experiment (scripts/M7-d-r5/floor_experiment.py): a learner answer built from reference.py that adds 2e-9 to every inequality multiplier (all positive, min m = 2e-9) and passes the primal, stationarity and CS checks within 1e-8. With dual_residual = max(0, -min m) it passes 363/363 on seeds 0-9 (floor_experiment_floored_0-9.log). With dual_residual = -min m (unfloored) it fails test_certificate_agrees_with_the_recomputed_residuals on 10 of 10 seeds (floor_experiment_unfloored_0-9.log). So the agreement check (test_project.py:109) does test the floor, and separates it, for any answer whose multipliers are all positive. The statement that the floor never changes the value is true of the suite's own reference outputs (floor_check.log), but the sentence as written overstates what the suite tests.",
     "Replace the two sentences 'The suite does not test the case in which the floor changes the value.' and 'The floor is part of the definition, and the suite does not separate it from its absence.' with: 'The floor is part of the definition. An answer whose inequality multipliers are all positive is the case in which it changes the value, and the agreement check then compares your reported residual with the floored value, so an unfloored report fails it.'"),
 row("PRJ-D1-24", "2.6-spec", "project.html:359,364-366; grader/test_project.py:3-7", "PASS",
     "Flags -q -p no:cacheprovider --assert=plain -W error with QF_SEED match the run_graders and the alternative runs. The decode command on the page (project.html:366) runs: python3 -c 'import json; from instance import make_instance; print(json.loads(make_instance(7)['payload']))' prints a case (decode_seed7.log); the sector-label line of the same case is [1, 0, 0, 1]. The page's 'Python 3.14' matches the venv (Python 3.14.8) and pyproject requires-python >=3.14."),
 row("PRJ-D1-25", "2.6-autograder", "grader/reference.py; grader/starter.py; grader/test_project.py", "PASS",
     "run_graders_0-49.log: PASS (reference 50/50 seeds). starter_seed0.log: starter (raises NotImplementedError, starter.py:20) gives '360 failed, 3 passed'; the page's 'the suite fails on the starter' (project.html:301) holds."),
 row("PRJ-D1-26", "2.6-autograder", "grader/instance.py:34-68", "PASS",
     "instance_facts_r5.log: asset counts {3: 18, 4: 14, 5: 18} over seeds 0-49; every case feasible as exact decimals (50 of 50); sector labels cover both sectors; gamma positive; turnover limit non-negative."),
 row("PRJ-D1-27", "2.6-autograder", "grader/reference.py:13-18; grader/test_project.py:272-286", "PASS",
     "Stdlib-only imports (PRJ-D1-11); AST walk at test_project.py:272-286; mypy_project.log and ruff_check_grader.log pass."),
 row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py (every assert message)", "PASS",
     "Every assert message read (lines 129-1005). Each names a property (budget, box, sector cap, turnover, dual feasibility, stationarity in weights or auxiliaries, CS, certificate field, named condition, refusal must carry a message). None prints an expected value; --assert=plain echoes no operands."),
 row("PRJ-D1-29", "2.6-autograder", "grader/*.py; tests/labs/M7/lab-M7-project-1..3.py", "PASS",
     "mypy_project.log: 'Success: no issues found in 6 source files' (mypy --no-incremental --strict on reference, instance, starter and the three twins). ruff_check_grader.log: All checks passed. ruff_format_grader.log: 7 files already formatted (grader 4 plus 3 twins)."),
 row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py -k M7", "PASS",
     "pytest_labs_M7.log: 11 passed, exit 0."),
 row("PRJ-D1-31", "2.6-autograder", "project.html:359; grader/test_project.py:3-7", "PASS",
     "Local flags run on seeds 0-49 (run_graders_0-49.log) and in the browser (page_smoke_project.log); same flags in both."),
 row("PRJ-D1-32", "2.6-atlas", "project.html; plans/M7-build-plan.md:3,28,349-352", "PASS",
     "No atlas key on the grader panel (project.html:359). plans/M7-build-plan.md:3 ('no Atlas milestone') and :28 and :349-352 agree; the M7 curriculum entry has no atlas key (curriculum/01-foundations.yaml:298-301)."),
 row("PRJ-D1-33", "2.1-citations", "project.html:465-466; references/references.json:3648,21295", "PASS",
     "verify_refs_offline.log: 'offline integrity: 560 entries, 0 problems', exit 0. boyd2004convex (references.json:3648) and stokey1989recursive (:21295) are registry keys. The page only lists them as reading."),
 row("PRJ-D1-34", "2.9-structure", "project.html:344-350", "PASS",
     "2+3+10+6+7+5 = 33 (see PRJ-D1-16). Per-component hours are design targets (ruling); the arithmetic is consistent."),
 row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (x3_04 file absent at this pin)", "PASS",
     "The round-4 survivor x3_04 is deleted at 440ed3c (ls ledgers/M7/mutants | grep x3_04 prints nothing; the file list at this pin has 157 entries). mutate_all_r5_full_0-9.log: 'mutate_graders M7: PASS (157/157 killed)' over the 152 existing and 5 new mutants."),
 row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/x3_01..x3_03; ledgers/M7/mutants/r4_01..r4_06", "PASS",
     "mutate_all_r5_full_0-9.log: all of x3_01..x3_03 and r4_01..r4_06 KILLED (r4_06 by test_named_condition_boundary_is_accepted[start-within-sector-cap-boundary], seed 1)."),
 row("PRJ-D1-37", "2.6-mutation", "project.html:317,320; grader/test_project.py:108-109; grader/reference.py:202-205,229-230,239-241,287", "PASS",
     "Equivalence of the deleted x3_04 (unfloored dual) with the reference on every output the reference solver produces: at most n-1 inequality rows are working (rank test, reference.py:202-205, 229-230), and the lower/upper/sector entries of the others are exact 0 (reference.py:239-241); there are 2n+Z such entries, so one is 0, so min m = 0 and the floored and unfloored values coincide (floor_check.log). A learner answer whose multipliers are all positive is a different case, which PRJ-D1-23 covers. The deletion stands."),
 row("PRJ-D1-38", "2.6-autograder", "ledgers/M7/scripts/M7-d-r5/alts/*.py; alts_run/*_0-49.log", "PASS",
     "Seven correct alternatives pass 50 of 50 seeds 0-49 under the page's flags: alt_r4_exact_bland_active, alt_r4_exact_empty_start_min, alt_r4_reused_r3v_relative_float, alt_r5_exact_reversed_order_max_drop, r3_alt_empty_start, r3_alt_lu_solver, r3_alt_nullspace. The float alternatives with absolute cutoffs fail only on the gamma boundaries (gamma-positive-zero/negative-boundary at 1e-6, gamma-just-inside-zero at 1e-9), which the page states are valid (project.html:326): they raise 'no convergence' or 'working set dependent' there. These are alternative defects with absolute cutoffs, not an over-constrained grader."),
 row("PRJ-D1-39", "2.9-structure", "course/modules/M/M7/grader/reference.py; BLUEPRINT.md:400-401; .github/workflows/ci.yml", "FAIL",
     "BLUEPRINT.md:400-401 requires deployment to exclude every grader/reference.py. Searched this round: no vercel.json, .vercelignore, netlify, wrangler, Dockerfile, railway or deploy file exists (find); no 'vercel' or 'railway' text in the repo; ci.yml has checks and a screenshot upload only, no deploy step; no tool excludes reference.py (grep over tools/ finds only run_graders, page_smoke and check_projects). The file sits under course/, the static site BLUEPRINT names as deployed, and is served at its own path. grader.js:25-33 fetches only the starter, suite and support files; that does not stop direct access to reference.py. The publication rule is therefore unimplemented at this pin, and a deploy configuration outside the repo cannot be read (UNVERIFIABLE, counted as FAIL).",
     "Add the publication exclusion for course/modules/*/*/grader/reference.py to the deploy configuration (or a build step that copies course/ without it) and show the published artifact listing without reference.py."),
 row("PRJ-R4-01", "2.9-prose", "grader/test_project.py:381-382 (docstring)", "PASS",
     "The round-4 docstring cited seeds 162, 163, 182 and 267. The current docstring (test_project.py:380-382) states the condition only: 'When the answer equals the starting portfolio, every mix equals the answer, and the check holds with equality.' That is true (y = w = w0 for every mix). No seed census remains in test_project.py (grep for seeds and reference)."),
 row("PRJ-R5-01", "2.4-math", "project.html:456 (frontier bullet)", "PASS",
     "'the derivative of the optimal objective with respect to the budget level b, the right-hand side of the budget constraint sum_i w_i = b (the page sets b = 1)': the budget is sum_i w_i = 1 at project.html:306-308, so the parenthetical is true. The bullet asks the learner to state a sign convention, so it claims no sign."),
 row("PRJ-R5-02", "2.6-spec", "grader/test_project.py:223 (comment); :348-349 (message)", "PASS",
     "Comment at :223: stationarity w - mu + nu = 0 with the budget fixing nu = -0.3 gives w = mu + 0.3 = (0.6, 0.4): sum(mu) = 0.4, so 0.4 - 2nu = 1 and nu = -0.3, and w = (0.3+0.3, 0.1+0.3) = (0.6, 0.4). Message at :348-349: the total multiplier must equal the sum of the plus and minus multipliers, which is r^t = kappa - alpha - beta = 0 (test_project.py:102)."),
 row("PRJ-R5-03", "2.9-prose", "project.html:450 ('No case reads a data file')", "PASS",
     "The only file read in the grader is Path(sol.__file__).read_text at test_project.py:275 (the learner's own source for the import check). instance.py opens no file (instance.py:1-68). No case reads a data file."),
 row("PRJ-R5-04", "2.9-structure", "project.html:349 (rationale), :350 (total)", "PASS",
     "Prose only; the hours figures 5 and 33 are unchanged and sum as in PRJ-D1-16. The new rationale names no number."),
 row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", "PASS",
     "Five new student-error mutants, one change each from reference.py (make_r5.py): r5_01 Hessian without gamma; r5_02 sector multiplier sign flipped in the certificate; r5_03 starting budget by exact equality; r5_04 gamma = 0 accepted; r5_05 weights rounded to six decimals. All five KILLED in mutate_all_r5_full_0-9.log (killed-by lines in the fragment's mutants list)."),
]

fragment = {
    "unit": "M7",
    "slice": "M7-d",
    "round": 5,
    "verifier": "Claude Haiku 5.5, independent verifier for M7-d, round 5 (did not build M7-d; works in its own checkout)",
    "pin": "440ed3c8216725d498d9c6d7c746907d4d418198",
    "base": "4eb6788fe3b408bb6d90ac73addc6fb17af47b8b (round-4 pin). Slice delta since that pin: course/modules/M/M7/project.html (lines 317, 320, 349, 450, 456), grader/test_project.py (lines 223, 348, 380-382), ledgers/M7/mutants (x3_04 deleted; r4_06 edited). cards.json (not this slice) also changed. grader/reference.py, instance.py, starter.py, the three project twins and plans/ are byte-identical to the round-4 pin. Every changed subject was re-verified from scratch this round.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD5-M7-d",
    "scratch": "/tmp/m7d-r5-floor/{floored,unfloored}/{0..9}, /tmp/m7d-r5-c0..c49 (collect), /tmp/m7d-r5-run (alternatives), /tmp/m7d-r5-starter",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Round 5 on 440ed3c. Rows: %d (PASS %d, FAIL %d, UNVERIFIABLE 0). Mutants: %d in ledgers/M7/mutants, all KILLED on seeds 0-9 (mutate_all_r5_full_0-9.log: 157/157); "
        "5 are new (r5_01..r5_05). Non-PASS: PRJ-D1-23 (project.html:320: the suite does test and separate the floor for learner answers whose multipliers are all positive; experiment floor_experiment_*_0-9.log) and "
        "PRJ-D1-39 (no publication exclusion for grader/reference.py; BLUEPRINT.md:400-401). Cards (cards.json M7-c192 edit, M7-c200 added) are outside slice d and were not checked. "
        "Not verified: the deploy configuration outside the repository (PRJ-D1-39). Lab 1 and Lab 3 numbers and the proposition were re-derived; the Lab 2 blanks were checked against the twin."
    ),
    "summary": "",
}
n = len(rows)
npass = sum(r["status"] == "PASS" for r in rows)
fragment["notes"] = fragment["notes"] % (n, npass, n - npass, len(mutants))
fragment["summary"] = (
    f"M7-d round 5: verdict FAIL. Rows {n}: PASS {npass}, FAIL {n - npass}, UNVERIFIABLE 0. "
    f"Mutants {len(mutants)}: all killed on seeds 0-9 (x3_04 deleted at this pin; r5_01..r5_05 added). "
    "Alternatives: 7 correct alternatives pass 50/50 seeds 0-49; float alternatives with absolute cutoffs fail on the gamma boundaries (alternative defects). "
    "Non-PASS: PRJ-D1-23 (floor sentence overstates the suite), PRJ-D1-39 (no reference.py publication exclusion)."
)
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, n, npass)
