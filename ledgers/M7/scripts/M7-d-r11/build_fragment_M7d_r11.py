"""Assemble the round-11 M7 slice-d fragment (ledgers/M7/M7-d.json) from the logs in ledgers/M7/scripts/M7-d-r11/."""
import ast, json, re, sys
from datetime import UTC, datetime
from pathlib import Path

NOTES = (
    "Round 11 on ccaeeaf. Delta from the round-10 pin 47a36d8c for the M7 slice: project.html:321-324 (Proposition hypothesis wording and proof, re-derived in full), cards.json (out of slice, not read beyond the diff), references.json (BK4/LX1 used_by only). grader/*.py, tests/labs/M7/project-*, ledgers/M7/mutants (191 existing) are byte-identical to 47a36d8c, but every round-10 PASS row was re-verified with fresh evidence this round, so no row is carried forward. "
    "Whole slice read line by line: project.html 1-482, grader/instance.py, starter.py, reference.py (1-334), test_project.py (1-1127). "
    "Verdict FAIL rests on PRJ-D1-39 only (cross-unit deployment exclusion of grader/reference.py, not implemented in the repository). "
    "Not checked: a visual/browser sweep beyond page_smoke; the cards (out of slice); the full repository pytest (only tests/test_labs.py -k M7); verify_refs live run (offline only); default pytest assertion mode (documented invocation uses --assert=plain); alternative solvers beyond the nine written here. "
    "Pre-existing ledgers/M7/M7-d.json (round 15, pin 448548f, ancestor of HEAD) was overwritten in this checkout by this round-11 fragment; it is not committed. "
    "The round-10 fragment /Users/billyribeiro/.fanout/frags/D-M7-d.round10.json was used as context only; its PASS rows were not trusted and were re-derived."
)

ROOT = Path(sys.argv[1]).resolve()
S = "ledgers/M7/scripts/M7-d-r11/"
MUT = ROOT / "ledgers/M7/mutants"

def read(name):
    return (ROOT / S / name).read_text(encoding="utf-8")

def mutant_rows(text):
    out = []
    for line in text.splitlines():
        m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
        if m:
            out.append((m.group(2), m.group(3), m.group(4), m.group(1)))
    return out

mutate = mutant_rows(read("mutate_M7_0-9_r11.log"))
new_kill = {}
for logname in ("kill_r11_new_mutants_final_0-49.log",):
    for line in read(logname).splitlines():
        m = re.match(r"^(KILLED|SURVIVED) (\S+) -> (.*)$", line)
        if m:
            new_kill[m.group(2)] = (m.group(3), m.group(1))
# the superseded first version of r11_03 is replaced by the final mutant: the final log wins
new_kill.update({k: v for k, v in new_kill.items()})
mutants = []
for name, desc, killed_by, status in mutate:
    assert status == "KILLED", name
    mutants.append({"id": name, "description": desc, "killed_by": killed_by + " (seeds 0-9)"})
for path in sorted(MUT.glob("r11_*.py")):
    doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    desc = doc.splitlines()[0].removeprefix("Student error: ")
    killed_by, status = new_kill[path.name]
    assert status == "KILLED", path.name
    mutants.append({"id": path.name, "description": desc, "killed_by": killed_by + " (seeds 0-49)"})
assert len(mutants) == 195, len(mutants)
assert len({m["id"] for m in mutants}) == 195

def row(id_, check, location, status, evidence, fix=""):
    return {"id": id_, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix}

P = "PASS"
rows = [
 row("PRJ-D1-01", "2.6-spec", "course/modules/M/M7/grader/instance.py (make_instance)", P,
     "Read in full (instance.py:34-68). Returns label containing SIMULATED; same seed gives same payload (test_instance_is_simulated_and_deterministic, run in run_graders_M7 seeds 0-49, ledgers/M7/scripts/M7-d-r11/run_graders_M7_seeds0-49_r11.log)."),
 row("PRJ-D1-02", "2.6-spec", "project.html:299-300; grader/test_project.py output_shape (181-201)", P,
     "allocate returns exactly weights/multipliers/certificate; multipliers exactly the seven keys; certificate the four keys (output_shape). Reference passes 50/50 seeds (run_graders_M7 r11 log)."),
 row("PRJ-D1-03", "2.4-math", "project.html:309", P,
     "Re-derived: sum|d_i| <= tau iff exists t with t_i >= d_i, t_i >= -d_i, sum t_i <= tau. Forward direction t_i = |d_i|; converse sum|d_i| <= sum t_i <= tau. Both directions on the page are correct."),
 row("PRJ-D1-04", "2.4-math", "project.html:310-313", P,
     "Re-derived the Lagrangian of the linearized problem: dL/dw_i = gamma(Sigma w)_i - mu_i + nu - lambda^l_i + lambda^u_i + eta_k(i) + alpha_i - beta_i; dL/dt_i = kappa - alpha_i - beta_i. Matches test_project.py stationarity() (lines 133-151) and reference _certificate (lines 303-309)."),
 row("PRJ-D1-05", "2.4-math", "project.html:310,314-319; grader/test_project.py inequality_pairs (116-130)", P,
     "The six constraint forms g_j <= 0 on the page (l-w, w-u, sector-c, d-t, -d-t, sum t - tau) and their multipliers match inequality_pairs one-to-one."),
 row("PRJ-D1-06", "2.4-math", "project.html:320; grader/test_project.py recomputed_certificate (154-165)", P,
     "Dual residual = max(0, -min inequality multiplier); the floor changes the value only when every inequality multiplier is positive, and the 1e-9 agreement threshold matches the sentence on p.320 (test_certificate_agrees_with_the_recomputed_residuals, 1e-9)."),
 row("PRJ-D1-07", "2.4-math", "project.html:317-321; test_project.py recomputed_certificate (154-165)", P,
     "Primal, stationarity, dual and complementary-slackness definitions on the page are reproduced exactly by recomputed_certificate and by reference._certificate (exact Fraction arithmetic)."),
 row("PRJ-D1-08", "2.4-math", "project.html:323-325 (Proposition T and proof, changed hunk at line 324)", P,
     "Re-derived in full on the current text: L(w,t) = f(w) + sum lambda_j g_j + nu(sum w - 1) is convex and differentiable (f convex, lambda_j >= 0 stated as hypothesis, g_j affine); stationarity gives the global minimum; every feasible y lifts to s_i = |y_i - w0_i| (linearization equivalence); f(y) >= L(y,s) >= L(w,t) = f(w) by complementary slackness; uniqueness by the midpoint of two minimizers (feasible set convex, f strictly convex in w, f(w)=f(w')). Hypotheses on line 325 cover every hypothesis used. Existence of multipliers is explicitly not claimed."),
 row("PRJ-D1-09", "2.4-math", "project.html:325; grader/instance.py:3-4,39-43", P,
     "Sigma = (A'A + I)/1000 (instance.py:41): x'Sigma x = (|Ax|^2 + |x|^2)/1000 > 0 for x != 0, so the positive-definiteness sentence on p.325 holds for every generated instance."),
 row("PRJ-D1-10", "2.6-spec", "project.html:326; grader/reference.py _parse (54-109)", P,
     "Each named refusal is raised as ValueError in _parse: not a mapping (55-56), field missing (58-59), NaN/inf (43), no assets (63), list length (71-72, 83-84), asymmetric (77), not PD (79, pivots), gamma (66), turnover (69), lower>upper (86), start sum (103), start bound (105), sector cap (108), label range (98), sector without asset (100-101)."),
 row("PRJ-D1-11", "2.6-spec", "grader/test_project.py NAMED_CONDITIONS (637-651), OTHER_SIDE_REFUSED (754-777)", P,
     "Each named condition has an invalid test (pytest.raises ValueError) and a valid test; the suite passes 50/50 on the reference (run_graders_M7 r11 log)."),
 row("PRJ-D1-12", "2.6-spec", "project.html:326,332; test_project.py EXACT_BOUNDARIES (674-680), NAMED_CONDITIONS", P,
     "Boundary values (bound and cap equal to start, start sum inside 1e-9 on the low side, gamma 1e-6 and 1e-9, turnover 0) accepted by reference on all 50 seeds. Acceptance of gamma 1e-9 is stricter than the page's own example (1e-6); see PRJ-R11-03."),
 row("PRJ-D1-13", "2.5-lab", "project.html:53-168; tests/labs/M7/lab-M7-project-1.py", P,
     "tools/run_labs.py --unit M7 --page project -> 'run_labs M7: PASS (3/3)' (ledgers/M7/scripts/M7-d-r11/run_labs_M7_project_r11.log). Twin under python -I -W error rc 0, empty stderr; page code == twin; expected block == twin output (labs_twin_vs_page_expected_r11.log)."),
 row("PRJ-D1-14", "2.5-lab", "project.html:170-285; tests/labs/M7/lab-M7-project-2.py", P,
     "Page code differs from the twin only at the three blanks (residual, signs, dual_feasible; diff in labs_twin_vs_page_expected_r11.log). Completed twin output equals the Lab 1 expected block line for line."),
 row("PRJ-D1-15", "2.5-lab", "project.html:372-445; tests/labs/M7/lab-M7-project-3.py", P,
     "Output: check A all zero; B stationarity 9/550, dual 9/1100, others 0; C stationarity 1/6250, primal 0, dual 0. Recomputed by hand: flipped multiplier gives dual 9/1100 and stationarity 2*9/1100 = 9/550; moving 1/1000 gives asset-1 gradient change -1/6250. All match page text lines 444."),
 row("PRJ-D1-16", "2.9-hours", "project.html:33,338-354; course/modules/M/M7/index.html:29; curriculum/01-foundations.yaml:298-299", P,
     "Table 2+3+10+6+7+5 = 33 (= data-hours-project 33). Hub data-hours-lessons 77 + project 33 = 110 = curriculum M7 hours 110."),
 row("PRJ-D1-17", "2.9-structure", "project.html:40-49", P,
     "Ladder: rung 1 solved and annotated (Lab 1), rung 2 completion (Lab 2), rung 3 spec + autograder + Lab 3 check, rung 4 stretch. check_pages M7 PASS (check_pages_all_r11.log)."),
 row("PRJ-D1-18", "2.6-spec", "project.html:288-336", P,
     "Spec completeness: a competent student's clarifying questions were checked against the page: multiplier non-uniqueness is covered by 'satisfy the definitions above' (line 330); sign conventions by Conventions (303-310); tolerances by 320-321; refusal list by 326. Honest gap kept: existence of multipliers is not proved on the page (stated on line 325)."),
 row("PRJ-D1-19", "2.9-structure", "course/modules/M/M7/grader/ (instance.py, reference.py, starter.py, test_project.py)", P,
     "All four files present (git ls-files); check_projects M7 PASS (check_projects_all_r11.log)."),
 row("PRJ-D1-20", "2.9-structure", "project.html; tools/page_smoke.py --unit M7 --pages project", P,
     "ledgers/M7/scripts/M7-d-r11/page_smoke_project_r11.log: 'page_smoke modules/M/M7/project.html: PASS', 'in-browser grader: All 364 tests pass.'"),
 row("PRJ-D1-21", "2.4-notation", "project.html symbols vs notation/notation.json (8 registered entries)", P,
     "Registry entries are T, Phi, gamma_3, gamma_4, R*, R^{e*}, R_f, Q. The project page uses none of them (grep of math on page: no T, Phi, R_*, Q as symbols; T at line 323 is the data-grade attribute). Macros used are only standard TeX (\\top, \\tfrac, \\sum, \\square). Local letters (gamma, mu, nu, lambda, eta, alpha, beta, kappa, Z, n, k, S_k, l, u, s, A, b) are defined on the page where first used (lines 295, 305-310, 325, 456)."),
 row("PRJ-D1-22", "2.9-dag", "project.html:456 (envelope-theorem link); course/modules/M/M7/index.html:64", P,
     "envelope-theorem is introduced in M2 (curriculum/curriculum.json M2 introduces) and M2 is in M7's prerequisite closure (plan section 2, closure {P0.1, M1, M2, M3}). check_dag M7 PASS (check_dag_all_r11.log)."),
 row("PRJ-D1-23", "2.9-prose", "project.html; grader/test_project.py; grader/reference.py (banned-phrase scan)", P,
     "Scan of prose for TODO, TBD, lorem, ellipsis prose, for brevity, details omitted, beyond the scope, obviously, clearly, roughly, about N, studies show, experts agree: no hits in learner text (only Python type annotations tuple[..., ...] match the ellipsis pattern)."),
 row("PRJ-D1-24", "2.6-spec", "project.html:364-366 (local run and decode commands)", P,
     "Decode command run verbatim from a scratch folder with Python 3.14.8: printed the case for seed 7. Local pytest command run with the reference as constrained_allocator.py: 364 passed in 3.55 s; with the starter: 361 failed, 3 passed. (Run without -I, because -I removes the working directory from sys.path.)"),
 row("PRJ-D1-25", "2.6-autograder", "grader/starter.py:18-20", P,
     "Starter raises NotImplementedError; the suite fails 361 of 364 on seed 7 (scratch run, output above). run_graders M7 PASS includes the starter check."),
 row("PRJ-D1-26", "2.6-autograder", "grader/instance.py (make_instance); instances_sample_seeds0-49_r11.log", P,
     "Seeds 0-49 (all 50, not a sample): every instance accepted by reference (50/50 valid); 50 distinct reference answers; n = 3:18, 4:14, 5:18; turnover multiplier nonzero (turnover binds) in 47 of 50; sector cap binds in 19 of 50; lower bound binds in 4; upper in 6."),
 row("PRJ-D1-27", "2.6-autograder", "grader/test_project.py:37; grader/reference.py:21", P,
     "TOL = 1e-8 for feasibility, stationarity and complementary slackness (test line 37); agreement 1e-9 (line 434, 479); start checks 1e-9 (reference line 21, and test _start_sum_* at 544-551). Matches page lines 320-321."),
 row("PRJ-D1-28", "2.6-autograder", "grader/test_project.py assert and pytest.fail messages", P,
     "Every message is a fixed sentence; formatted parts are key names, indices, field names or the hand-case name (lines 192-193, 238, 391, 435, 474, 480, 889, 897, 1077). No message prints a computed or expected value under the documented --assert=plain invocation (see PRJ-R11-04 for the default-mode note)."),
 row("PRJ-D1-29", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke) and CPython (run_graders)", P,
     "page_smoke in-browser grader: All 364 tests pass; CPython: 364 collected on every seed 0-49 (collect_r11.log) and reference passes 50/50 under -W error."),
 row("PRJ-D1-30", "2.5-lab", "tests/labs/M7/lab-M7-project-1..3.py; tests/test_labs.py", P,
     "pytest tests/test_labs.py -k M7 -> 11 passed (pytest_labs_M7_r11.log)."),
 row("PRJ-D1-31", "2.6-spec", "project.html:332; grader/test_project.py HAND_CASES (274-312)", P,
     "Worked answers re-derived by hand: budget only (0.6,0.4) from w = mu + 0.3; zero turnover (0.5,0.5); single asset 1.0; upper bound binding (0.7,0.3) (without the 0.3 bound the turnover limit gives (0.55,0.45): objective slope 2x-0.9 along the line); turnover binding (0.6,0.4) (objective slope 2x-0.4, turnover limit x<=0.1); degenerate box (0.5,0.5). The six cases are the six entries in HAND_CASES. Their comments (275-305) match."),
 row("PRJ-D1-32", "2.6-atlas", "project.html; curriculum/01-foundations.yaml:298-327", P,
     "M7 has no atlas key; the Atlas branch does not apply."),
 row("PRJ-D1-33", "2.1-citations", "project.html:465-466 (reading list); references/references.json", P,
     "verify_refs --offline: 560 entries, 0 problems (verify_refs_offline_r11.log). boyd2004convex and stokey1989recursive: status verified, used_by includes M7. The page states no attributed claim (reading list only; 'no reading is needed')."),
 row("PRJ-D1-34", "2.9-structure", "project.html:338-354; tools/check_pages.py --unit M7", P,
     "check_pages M7 PASS; hours table has six rows with rationale and a total row."),
 row("PRJ-D1-35", "2.6-mutation", "ledgers/M7/mutants/ (195 files: 191 existing + 4 round-11)", P,
     "tools/mutate_graders.py --unit M7 --seeds 0-9: 'mutate_graders M7: PASS (191/191 killed)' (mutate_M7_0-9_r11.log). Round-11 mutants killed on seeds 0-49 (kill logs)."),
 row("PRJ-D1-36", "2.6-mutation", "ledgers/M7/mutants/ families f6, g2, m, p, q, r, s, v, w, x, y, z, d1-d3, r13-r15", P,
     "All families present; every one reported KILLED in mutate_M7_0-9_r11.log (no SURVIVED line)."),
 row("PRJ-D1-37", "2.6-mutation", "ledgers/M7/mutant_equivalence_r14.json; ledgers/M7/mutants/", P,
     "No equivalent mutant is listed in the 195. The first version of r11_03 was equivalent (budget plus n-1 inequality rows already limit the working set to n-1, so len(working) >= n never fires); it was rewritten to fire at n-1 (vertex) and is killed (kill_r11_mutant03_0-49.log)."),
 row("PRJ-D1-38", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/alt1..alt9 (alts_suite_r11*.log, r10alt_rerun_*.log)", P,
     "Five correct solvers pass all 364 checks on seeds 0-49: alt1 (exact, last-index drop), alt2 (exact, empty start, LIFO), alt6 (scale-aware float 1e-9 + exact polish), alt8 (exact, reversed row order), alt9 (scale-aware float 1e-10 + exact polish). Four float solvers with absolute cutoffs or without polish fail (PRJ-R11-01). The suite does not reject any correct method."),
 row("PRJ-D1-39", "2.9-structure", "BLUEPRINT.md:400-401 (section 7); course/modules/M/M7/grader/reference.py; .github/workflows/ci.yml; no deployment config in repo", "FAIL",
     "Re-checked at ccaeeaf: BLUEPRINT section 7 says deployment excludes every grader/reference.py. No vercel.json, no .vercelignore, no publish or copy step in .github/workflows/ci.yml, tools/build_site.py has no exclusion, .gitignore does not exclude reference.py, and reference.py is tracked (git ls-files). The exclusion is therefore not implemented anywhere in the repository. This is cross-unit, not M7-specific.",
     "Add the exclusion to whatever publishes course/ (for example a .vercelignore entry or a build copy step in tools/build_site.py) for course/modules/*/*/grader/reference.py, and check it in CI; or amend BLUEPRINT section 7 to name the mechanism that exists."),
]

# round-9 and round-10 rows, re-verified this round (ids kept)
rows += [
 row("PRJ-R4-01", "2.9-prose", "grader/test_project.py docstrings and messages", P,
     "Every docstring checked against its code: purity fixture (80-104) runs each call twice on a snapshot; _observed_call (60-77) checks argument, prints, warnings; messages carry no values."),
 row("PRJ-R5-01", "2.4-math", "project.html:456 frontier bullet", P,
     "Learner is asked to state the sign convention; the page claims no value for the multiplier sign."),
 row("PRJ-R5-02", "2.6-spec", "grader/test_project.py comments and messages (275, 277, 295-296, 301, 303-305)", P,
     "Each comment's arithmetic recomputed (see PRJ-D1-31)."),
 row("PRJ-R5-03", "2.9-prose", "project.html:450 ('does not test' paragraph)", P,
     "Matches the suite: seed problem, hand cases and named conditions are tested; no data file is read; the method is not tested."),
 row("PRJ-R5-04", "2.9-structure", "project.html:349-350", P,
     "Total row and rationale match the hub: 77 + 33 = 110."),
 row("PRJ-R5-05", "2.6-mutation", "ledgers/M7/mutants/r5_01..r5_05", P,
     "Each r5 mutant reported KILLED in mutate_M7_0-9_r11.log."),
 row("PRJ-R6-01", "2.6-gate", "tools/check_projects.py --all", P,
     "check_projects_all_r11.log: rc 0; 'check_projects M7: PASS'."),
 row("PRJ-R6-02", "2.6-gate", "tools/check_pages.py --all", P,
     "check_pages_all_r11.log: rc 0; 'check_pages M7: PASS'."),
 row("PRJ-R6-03", "2.9-dag", "tools/check_dag.py --all", P,
     "check_dag_all_r11.log: rc 0; 'check_dag M7: PASS'; 27 PASS lines, no failure line."),
 row("PRJ-R7-01", "2.6-mutation", "grader/test_project.py degenerate box hand case (306-311); mutants r7_06_*", P,
     "Degenerate-box hand case present; r7_06_unfloored_dual_residual_on_degenerate_positive_multipliers KILLED."),
 row("PRJ-R7-02", "2.9-prose", "grader/test_project.py:295-296 comment", P,
     "Recomputed: with upper 0.3 the answer is (0.7, 0.3); without it the turnover limit stops at (0.55, 0.45)."),
 row("PRJ-R7-03", "2.9-prose", "grader/test_project.py:916-921 comment", P,
     "Comment matches _make_room and the starting-sum tests; POSITIONS are four fixed ids; collected count is 364 on every seed (collect_r11.log)."),
 row("PRJ-R7-04", "2.6-mutation", "ledgers/M7/mutants/r7_01..r7_05", P,
     "All KILLED in mutate_M7_0-9_r11.log."),
 row("PRJ-R7-05", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", P,
     "page_smoke in-browser grader: 364 tests pass in 2.9 s, under the 60 s limit; run_graders slowest seed 6.3 s (run_graders log)."),
 row("PRJ-R7-06", "2.8-data", "project.html; grader/instance.py", P,
     "No dataset read; every instance label contains SIMULATED (test_instance_is_simulated_and_deterministic)."),
 row("PRJ-R7-07", "2.6-hours", "project.html:344-350", P,
     "Own estimate: worked example 2-3 h; completion 2-3 h; core solver (active set over box, sector, 2^n sign forms) 10-18 h; linear constraints and auxiliaries 5-7 h; certificate and own tests 5-7 h; self-check 3-5 h. Range 27-43 h, central 35 h, 6% above the declared 33 h: inside the 30% rule."),
 row("PRJ-R8-01", "2.6-autograder", "grader/test_project.py:60-77, 1114-1121 and purity fixture (80-104)", P,
     "v8_01_prints_a_debug_line_on_zero_turnover and v9_06_prints_before_refusing_a_non_integer_sector_label KILLED (mutate_M7_0-9_r11.log); the fixture uses pytest.fail, which is not caught by pytest.raises(Exception)."),
 row("PRJ-R8-02", "2.6-autograder", "grader/test_project.py:1108-1112 and purity fixture", P,
     "v9_07_marks_its_argument_before_refusing_text_in_mu and z04_allocate_marks_its_argument KILLED."),
 row("PRJ-R8-03", "2.6-mutation", "ledgers/M7/mutants/v8_03_budget_multiplier_zero_when_start_is_optimal.py", P,
     "KILLED in mutate_M7_0-9_r11.log."),
 row("PRJ-R8-04", "2.6-spec", "grader/test_project.py:302-311", P,
     "Degenerate-box hand case and its comment re-verified (PRJ-D1-31)."),
 row("PRJ-R9-01", "2.6-autograder", "grader/test_project.py:60-77 (_observed_call) vs pytest.raises(Exception) tests", P,
     "_observed_call uses pytest.fail(pytrace=False) (lines 72-76), so refusal-path defects are not masked; v9_06 and v9_07 KILLED."),
 row("PRJ-R9-02", "2.9-prose", "grader/test_project.py:82-89 docstring", P,
     "Docstring: run twice on a snapshot, refusal allowed, checks apply to refusals; the code (92-102) does exactly this."),
 row("PRJ-R9-03", "2.6-autograder", "grader/test_project.py:92 (@wraps) and 319-326", P,
     "@wraps(real) keeps the signature; v9_08_allocate_takes_an_optional_second_argument KILLED."),
 row("PRJ-R9-04", "2.9-prose", "project.html:167 (Lab 1 interpretation)", P,
     "Re-read: budget-only, held asset, KKT steps and 'the bound multiplier not held at zero is zero by construction' match the code (lab-M7-project-1 lines 117-152)."),
 row("PRJ-R9-05", "2.4-math", "project.html:324 (proof)", P,
     "Changed hunk re-derived in full (see PRJ-D1-08)."),
 row("PRJ-R9-06", "2.6-autograder", "ledgers/M7/scripts/M7-d-r11/alts/ and alts_suite_r11*.log", P,
     "Over-constraint check (see PRJ-D1-38 and PRJ-R11-01): no correct solver fails; the failing float solvers fail the spec's own tolerance or crash at gamma 1e-6 and 1e-9."),
 row("PRJ-R9-07", "2.6-mutation", "ledgers/M7/mutants/ (final folder)", P,
     "195 mutants: 191 existing killed on seeds 0-9 (mutate_M7_0-9_r11.log); 4 round-11 mutants killed on seeds 0-49 (PRJ-R11-02)."),
 row("PRJ-R9-08", "2.9-structure", "grader/test_project.py (collected count); project.html:332", P,
     "collect_r11.log / collect_r11.py: 364 collected on every seed 0-49, return code 0 on each."),
 row("PRJ-R9-09", "2.5-lab", "project.html:53-285, 372-445; tests/labs/M7/lab-M7-project-1..3.py", P,
     "run_labs project PASS (3/3); twins run under python -I -W error with empty stderr."),
 row("PRJ-R9-10", "2.6-autograder", "grader/test_project.py under Pyodide (page_smoke)", P,
     "page_smoke in-browser grader: 364 pass (page_smoke_project_r11.log)."),
 row("PRJ-R9-11", "2.9-prose", "grader/test_project.py:274-311 hand-case comments", P,
     "Each comment's arithmetic recomputed (PRJ-D1-31)."),
 row("PRJ-R10-01", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/alt_B, alt_G, alt_H, alt_I, alt_J (re-run round 11)", P,
     "Re-run this round on seeds 0-49: " + "see r10alt_rerun_alt_B..J logs; exact solvers pass (no KILLED line) as recorded there."),
 row("PRJ-R10-02", "2.6-autograder", "ledgers/M7/scripts/M7-d-r10/alts/alt_A, alt_C, alt_D, alt_E, alt_F (re-run round 11)", P,
     "Re-run this round: alt_A, alt_C, alt_D, alt_E fail on gamma-positive-zero-boundary (gamma 1e-6, seed 0) and alt_F on gamma-just-inside-zero (gamma 1e-9, seed 0) (r10alt_rerun_*.log); cause not diagnosed for these five. Round-11 diagnosis of the same boundary for my own absolute-cutoff float solvers (alt3, alt4, alt5): 'singular float system' at gamma 1e-6 and 1e-9 (diag_gamma_r11.py). Pure scale-aware float (alt7) returns primal residual 2.47e-8 > 1e-8 at gamma 1e-9, seed 8. A scale-aware float solver with exact polish passes (alt6, alt9). These are defective float methods; the suite is consistent with the spec, which requires every valid input to certify within 1e-8."),
 row("PRJ-R10-03", "2.6-mutation", "ledgers/M7/mutants/r10_01..r10_03", P,
     "All three KILLED in mutate_M7_0-9_r11.log."),
 row("PRJ-R10-04", "2.6-autograder", "ledgers/M7/mutants/ full set", P,
     "tools/mutate_graders.py --unit M7 --seeds 0-9: 191/191 killed (mutate_M7_0-9_r11.log); round-11 mutants 4/4 killed on seeds 0-49."),
 row("PRJ-R10-05", "2.6-autograder", "tools/run_graders.py --unit M7 --seeds 0-49; mypy --strict on grader", P,
     "'run_graders M7: PASS (reference 50/50 seeds, slowest 6.3 s)' (run_graders_M7_seeds0-49_r11.log); mypy --strict on instance.py, test_project.py, constrained_allocator.py (reference), starter.py: 'Success: no issues found in 4 source files' (mypy_strict_grader_r11.log)."),
 row("PRJ-R10-06", "2.9-structure", "repo gates: ruff check ., ruff format --check ., mypy --no-incremental, verify_refs --offline", P,
     "ruff_check_r11.log: All checks passed; ruff_format_r11.log: 553 files already formatted; mypy_r11.log: Success, 385 source files; verify_refs_offline_r11.log: 560 entries, 0 problems."),
 row("PRJ-R11-01", "2.6-autograder", "over-constraint: ledgers/M7/scripts/M7-d-r11/alts/ (nine solvers)", P,
     "Five correct solvers pass 364/364 on seeds 0-49: alt1, alt2, alt6, alt8, alt9 (alts_suite_r11*.log: no KILLED). Failing: alt3, alt4, alt5, alt7 (and round-10 alt_A, C, D, E, F). Every failure is a numerical defect at the gamma boundary (singular float system from absolute cutoffs, or certificate residual 2.47e-8 above 1e-8), not a spec violation by a correct method. No correct solver is over-constrained by the suite."),
 row("PRJ-R11-02", "2.6-mutation", "ledgers/M7/mutants/r11_01, r11_03, r11_05, r11_06", P,
     "Four new student-error mutants (reference.py with one edit): r11_01 turnover multipliers as positive/negative parts of net; r11_03 solver raises at a vertex working set (n-1 rows); r11_05 turnover sign forms for half the orthants only; r11_06 sector caps read in reverse. All KILLED on seed 0 (kill_r11_new_mutants_final_0-49.log). The first-failing test reported for r11_03 is a wrong-type test whose control call (the valid seed-0 case) raises under the mutant, so the kill is by the valid case. r11_03 as first written was equivalent and was rewritten (PRJ-D1-37)."),
 row("PRJ-R11-03", "2.6-spec", "project.html:326 (gamma valid form) vs test_project.py EXACT_BOUNDARIES (gamma 1e-9)", P,
     "The page names gamma 1e-6 as valid and lists 'gamma is not positive' as the only gamma refusal, so any positive gamma is a valid input; the suite accepts gamma 1e-9 and certifies it to 1e-8. This is consistent with the page, not beyond it. Observation for the builder: the page could say that any positive gamma is valid, so students do not infer a floor. Not a FAIL."),
 row("PRJ-R11-04", "2.6-autograder", "grader/test_project.py assertion style under default pytest mode", P,
     "Documented invocation uses --assert=plain (project.html:365; run_graders PYTEST_FLAGS). Under default assertion rewriting a failing assert_kkt message shows the learner's own residual (checked: 'where 0.00652 = max(...)'), not the expected answer. The hand-case assertion abs(got[i] - value) would expose the worked value under default rewriting; this was not run and is outside the documented invocation."),
]

ids = [r["id"] for r in rows]
expected_ids = (["PRJ-D1-%02d" % i for i in range(1, 40)] + ["PRJ-R4-01"] + ["PRJ-R5-%02d" % i for i in range(1, 6)]
                + ["PRJ-R6-%02d" % i for i in range(1, 4)] + ["PRJ-R7-%02d" % i for i in range(1, 8)]
                + ["PRJ-R8-%02d" % i for i in range(1, 5)] + ["PRJ-R9-%02d" % i for i in range(1, 12)]
                + ["PRJ-R10-%02d" % i for i in range(1, 7)])
assert ids[:len(expected_ids)] == expected_ids, "row ids drifted"
assert len(set(ids)) == len(ids)

counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if counts["PASS"] == len(rows) else "FAIL"
fragment = {
    "unit": "M7",
    "slice": "d",
    "round": 11,
    "verifier": "Haiku 5.5 independent verifier (round 11); did not build M7-d",
    "pin": "ccaeeaf4 (ccaeeaf44bea94b37d912ec1da3c660bb2c55d87)",
    "base": "47a36d8c78633793ccc762ae19dcd5e19b780d19 (round-10 fragment pin); M7-slice delta since then: project.html:321-324 (proof hunk) and cards.json (out of slice); grader, labs and mutants unchanged in that range",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD11-M7-d",
    "scratch": "ledgers/M7/scripts/M7-d-r11/ (all scripts, logs, alts, instance sample, collect, labs comparison); helper copies in /tmp were used only to generate files that now live in the scripts folder",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": {
        "rows": len(rows),
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants": len(mutants),
        "mutants_killed": sum(1 for m in mutants if m["killed_by"]),
    },
}
out = ROOT / "ledgers/M7/M7-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), counts, "mutants", len(mutants), "killed", fragment["summary"]["mutants_killed"], "verdict", verdict)
