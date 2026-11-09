"""Build the round-15 FC2-d fragment from the round-15 outputs in ledgers/FC2/scripts/FC2-d-r15/out/."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD15-FC2-d")
S = "ledgers/FC2/scripts/FC2-d-r15"
OUT = f"{S}/out"
CARRY = (
    "Carried from round 14 (course/modules/FC/FC2/grader/*, tests/labs/FC2/lab-FC2-project-{1,2,3}.py, "
    "notation/notation.json, references/references.json, curriculum/02-economics-finance-core.yaml, and "
    "project.html outside lines 37 and 518 are byte-identical since the previous pin 1431aa1d; "
    "git diff --name-only 1431aa1d HEAD confirms it):"
)

# Mutants: parse the full run (103 builder mutants plus the 4 round-15 mutants).
mutants = []
for line in (ROOT / OUT / "mutate_graders_with_r15.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    state, fname, desc, killed = m.groups()
    name = fname.removesuffix(".py")
    if state == "KILLED":
        killed_by = killed.strip()
    else:
        killed_by = ""
    ruled = {
        "r15_a_parity_explanation_reverses_the_positive_gap_trade": "SURVIVED (ruled non-finding: explanation direction is not in the grader spec, round-6 ruling, see fc2d-r5-mut-direction and fc2d-r15-mut-a-parity-explanation-direction)",
        "r15_c_parity_explanation_prints_gross_where_net_belongs": "SURVIVED (ruled non-finding: explanation numbers are not in the grader spec, same class as the round-6 ruling, see fc2d-r15-mut-c-explanation-net-as-gross)",
        "r15_d_convexity_explanation_reverses_the_chord_side": "SURVIVED (ruled non-finding: explanation direction is not in the grader spec, round-6 ruling, see fc2d-r15-mut-d-convexity-explanation-side)",
    }
    if name in ruled:
        killed_by = ruled[name]
    mutants.append({"id": name, "description": desc.strip(), "killed_by": killed_by})

assert len(mutants) == 107, len(mutants)


def fam(prefix: str) -> str:
    hits = [m for m in mutants if m["id"].startswith(prefix)]
    assert hits, prefix
    return "; ".join(f"{m['id']} KILLED ({m['killed_by'].split('->')[-1].strip()})" for m in hits)


def alt_line(name: str) -> str:
    text = (ROOT / OUT / f"alt_{name}.out").read_text(encoding="utf-8").strip().splitlines()
    passes = sum(1 for ln in text if ln.endswith("exit=0") or " exit=0 " in ln)
    return f"{name}: {passes}/50 seeds exit 0"


rows = []


def row(rid, check, location, status, evidence, fix=""):
    rows.append({"id": rid, "check": check, "location": location, "status": status, "evidence": evidence, "fix": fix})


row("fc2d-gate-check-projects", "tools/check_projects.py --unit FC2", "tools/check_projects.py", "PASS",
    f"Fresh at dde0486b: {OUT}/check_projects.out 'check_projects FC2: PASS', exit 0.")
row("fc2d-gate-check-pages", "tools/check_pages.py --unit FC2", "tools/check_pages.py", "PASS",
    f"Fresh: {OUT}/check_pages.out 'check_pages FC2: PASS', exit 0.")
row("fc2d-gate-check-dag", "tools/check_dag.py --unit FC2", "tools/check_dag.py", "PASS",
    f"Fresh: {OUT}/check_dag.out 'check_dag FC2: PASS', exit 0.")
row("fc2d-gate-run-labs", "tools/run_labs.py --unit FC2", "project labs lab-FC2-project-1..3", "PASS",
    f"Fresh: {OUT}/run_labs.out 'run_labs FC2: PASS (11/11)', exit 0.")
row("fc2d-gate-page-smoke", "tools/page_smoke.py --unit FC2 and --pages project alone", "course/modules/FC/FC2/project.html", "PASS",
    f"Fresh: {OUT}/page_smoke.out 'page_smoke FC2: PASS'; {OUT}/page_smoke_project_alone.out 'page_smoke modules/FC/FC2/project.html: PASS', exit 0.")
row("fc2d-gate-run-graders", "tools/run_graders.py --unit FC2 --seeds 0-49", "course/modules/FC/FC2/grader", "PASS",
    f"Fresh: {OUT}/run_graders.out 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)'; the tool also runs its mypy --strict pass on reference, instance and starter.")
row("fc2d-gate-ruff", "ruff check and ruff format --check on the grader and tests/labs/FC2", "course/modules/FC/FC2/grader; tests/labs/FC2", "PASS",
    f"Fresh: {OUT}/ruff_check.out 'All checks passed!'; {OUT}/ruff_format.out '15 files already formatted'.")
row("fc2d-gate-mypy", "mypy (repo config) and mypy --strict on the grader", "pyproject.toml [tool.mypy]; course/modules/FC/FC2/grader", "PASS",
    f"Fresh: {OUT}/mypy_root.out 'Success: no issues found in 385 source files', exit 0. The grader strict pass is inside run_graders (PASS, above). A bare mypy --strict on the grader folder without scanner.py fails with import-not-found (scratch artefact, {OUT}/mypy.out), as in round 14.")
row("fc2d-gate-pytest", "pytest -k 'FC2 or project' tests/", "tests/", "PASS",
    f"Fresh: {OUT}/pytest_fc2.out, exit 0, no failures.")
row("fc2d-gate-verify-refs", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"Fresh: {OUT}/verify_refs.out 'offline integrity: 560 entries, 0 problems', exit 0.")
row("fc2d-collect-count", "pytest --collect-only count equals the page count", "course/modules/FC/FC2/project.html:320", "PASS",
    f"Fresh: {OUT}/collect_per_seed.out: reference collects 98 tests on each of seeds 0-49 (exit 0 for all 50). project.html:320 states 98 (grep verified).")
row("fc2d-seeds-84", "reference passes the suite on the seed window", "course/modules/FC/FC2/grader/test_project.py", "PASS",
    f"Fresh: {OUT}/run_graders.out, reference 50/50 seeds 0-49 under --assert=plain -W error.")
row("fc2d-starter-fails", "the starter fails the suite", "course/modules/FC/FC2/grader/starter.py", "PASS",
    f"Fresh: {OUT}/starter_0_49.out: starter exit 1 on 50/50 seeds (88 to 90 failed on seeds 0 to 2, {OUT}/starter.out).")
row("fc2d-alternatives", "five plus one alternative correct implementations, and two new ones, pass the suite",
    "ledgers/FC2/scripts/FC2-d-r14/alts/*.py; ledgers/FC2/scripts/FC2-d-r15/alts/*.py", "PASS",
    "; ".join(alt_line(n) for n in ["alt1_fraction_class", "alt2_integer_only", "alt3_float_epsilon_cutoff",
                                    "alt4_adjacent_slopes", "alt5_forward_price_parity", "alt7_integer_scaled",
                                    "alt8_decimal_60"]) + " (alt1..alt5 are round-14 files run via harness.py; alt7 and alt8 are round-15 files).")
row("fc2d-alt-r14-float-no-cutoff", "plain float implementation without cutoff is rejected", "course/modules/FC/FC2/grader/test_project.py:286-291, 802-806", "PASS",
    f"Fresh: {OUT}/float_no_cutoff_r15.out: the float scanner fails 2 tests (non-dyadic discount-factor ties) on every seed (e.g. seed 0: '2 failed, 96 passed'). project.html:308 requires each money value to be computed from exact fractions, so rejecting plain float is the specified behaviour.")
row("fc2d-alt-r6-overconstraint", "round-6 alternative passes the suite", f"{S}/alt6_round6_alternative.py", "PASS",
    f"Fresh: {OUT}/alt_alt6_round6_alternative.out, {alt_line('alt6_round6_alternative')}.")
row("fc2d-mutate-builder", "all builder mutants are killed (pre-existing set, 103 files)", "ledgers/FC2/mutants/", "PASS",
    f"Fresh: {OUT}/mutate_all_r15.out 'mutate_graders FC2: PASS (103/103 killed)', run before the round-15 mutants were added. The later full run {OUT}/mutate_graders_with_r15.out reports 103/107 (the four round-15 mutants are discussed in their own rows).")
row("fc2d-mut-new-r14", "round-14 new mutants r14_a to r14_e are killed", "ledgers/FC2/mutants/r14_a..r14_e", "PASS",
    fam("r14_") + f" ({OUT}/mutate_graders_with_r15.out).")
row("fc2d-mut-v03", "mutant v03 killed", "ledgers/FC2/mutants/v03*", "PASS", fam("v03_") + ".")
row("fc2d-mut-v04", "mutant v04 killed", "ledgers/FC2/mutants/v04*", "PASS", fam("v04_") + ".")
row("fc2d-mut-v05", "mutant v05 killed", "ledgers/FC2/mutants/v05*", "PASS", fam("v05_") + ".")
row("fc2d-mut-v06", "mutant v06 killed", "ledgers/FC2/mutants/v06*", "PASS", fam("v06_") + ".")
row("fc2d-mut-v01-boundary", "mutant v01 (zero net boundary) killed", "ledgers/FC2/mutants/v01*", "PASS", fam("v01_") + ".")
row("fc2d-mut-v02-labels", "mutant v02 (explanation labels) killed", "ledgers/FC2/mutants/v02*", "PASS", fam("v02_") + ".")
row("fc2d-r5-mut-swap-weights", "mutant r5_b killed", "ledgers/FC2/mutants/r5_b*", "PASS", fam("r5_b_") + ".")
row("fc2d-r5-mut-skip-first", "mutant r5_c killed", "ledgers/FC2/mutants/r5_c*", "PASS", fam("r5_c_") + ".")
row("fc2d-r6-mut-new", "round-6 new mutants r6_a to r6_c killed", "ledgers/FC2/mutants/r6_*", "PASS", fam("r6_") + ".")
row("fc2d-r7-mut-new", "round-7 new mutants r7_a to r7_c killed", "ledgers/FC2/mutants/r7_*", "PASS", fam("r7_") + ".")
row("fc2d-r5-mut-direction", "round-5 mutant r5_d (explanation direction) is ruled a non-finding and is not in the suite",
    "ledgers/FC2/mutants/ (r5_d absent); course/modules/FC/FC2/grader/test_project.py", "PASS",
    "r5_d_explanation_direction_reversed.py is absent from ledgers/FC2/mutants. The round-6 ruling still holds: project.html:301 says the explanation 'names the rule and the assumptions the finding depends on, by the labels'; no sign or direction statement is required in the explanation string. Direction is an item of the note's settlement rubric (project.html:512), not of the grader spec. The same reasoning covers r15_a, r15_c and r15_d below.")
row("fc2d-r5-grader-exact-ties", "round-5 exact-tie tests", "course/modules/FC/FC2/grader/test_project.py:271-291, 795-822", "PASS",
    CARRY + " the tie values were re-derived in round 14 with Fraction (ledgers/FC2/scripts/FC2-d-r14/out/rederive.out).")
row("fc2d-r6-new-tie-tests", "round-6 new tie tests", "course/modules/FC/FC2/grader/test_project.py:809-850", "PASS",
    CARRY + " test_project.py:809-850 unchanged; the suite passes on the reference on seeds 0-49 this round (run_graders).")
row("fc2d-grader-stdlib", "grader is standard library only", "course/modules/FC/FC2/grader/instance.py, reference.py, starter.py; course/modules/FC/FC2/grader/test_project.py", "PASS",
    CARRY + " the solution-facing files import only the standard library; the suite runs on the reference on seeds 0-49 this round.")
row("fc2d-grader-messages", "named error messages", "course/modules/FC/FC2/grader/test_project.py:450-650; course/modules/FC/FC2/project.html:305-316", "PASS",
    CARRY + " the message tests are unchanged and the reference passes them on seeds 0-49 this round.")
row("fc2d-grader-instance-validity", "instance generator validity", "course/modules/FC/FC2/grader/instance.py:41-60, 102-111, 118-131", "PASS",
    CARRY + " instance.py is unchanged; run_graders' fingerprint and validity checks passed on seeds 0-49 this round.")
row("fc2d-grader-instance-diversity", "instance diversity across seeds", "course/modules/FC/FC2/grader/instance.py:6-9, 134-142", "PASS",
    CARRY + " instance.py is unchanged; run_graders' instance check passed on seeds 0-49 this round.")
row("fc2d-lab1", "project Lab 1 page code, expected block and twin", "course/modules/FC/FC2/project.html:53-165; tests/labs/FC2/lab-FC2-project-1.py", "PASS",
    f"Fresh: {S}/out/lab_compare_r15.out: 'lab 1: twin exit=0 page_code_equals_twin=True expected_equals_output=True'.")
row("fc2d-lab2", "project Lab 2 completion page code, expected block and twin", "course/modules/FC/FC2/project.html:166-277; tests/labs/FC2/lab-FC2-project-2.py", "PASS",
    f"Fresh: {S}/out/lab_compare_r15.out: expected block equals the twin's output. The page code differs from the twin only in the three blanks (page lines '___' for twin lines 58, 60 and 73), as the completion design states.")
row("fc2d-lab3", "project Lab 3 page code, expected block and twin", "course/modules/FC/FC2/project.html:375-488; tests/labs/FC2/lab-FC2-project-3.py", "PASS",
    f"Fresh: {S}/out/lab_compare_r15.out: 'lab 3: twin exit=0 page_code_equals_twin=True expected_equals_output=True'.")
row("fc2d-lab-twins-pure", "twins run alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS",
    f"Fresh: python -I -W error exit 0 for each twin ({OUT}/twin1.txt, twin2.txt, twin3.txt; {S}/out/lab_compare_r15.out).")
row("fc2d-rederive-numbers", "every number in the Lab 1, Lab 2 and Lab 3 prose re-derived", "course/modules/FC/FC2/project.html:53-488", "PASS",
    f"Fresh: {OUT}/rederive_r15.out 'ALL ASSERTIONS PASS': Lab 1 kept 9500 parity (120/75) and 10500 convexity (75/30); Lab 3 kept 6500 (226/166), 7000 (540/480), 6000 convexity (63/3, exact chord -188/3); cost 45 and 60.")
row("fc2d-rubric-observable", "rubric levels are observable", "course/modules/FC/FC2/project.html:504-516", "PASS",
    CARRY + " lines 504-516 unchanged.")
row("fc2d-rubric-calib-A", "calibration of Exemplar A against the official scoring", "course/modules/FC/FC2/project.html:584-641 (article#exemplar-a, data-scores 2,1,2,2,1)", "PASS",
    "Calibration instruction applied: ~/.fanout/blind/FC2-d.json gives A = 2,1,2,2,1, equal to the official scores on the page (project.html:584 data-scores and :586 'Official scoring: C1 2 · C2 1 · C3 2 · C4 2 · C5 1').")
row("fc2d-rubric-calib-B", "calibration of Exemplar B against the official scoring", "course/modules/FC/FC2/project.html:520-583 (article#exemplar-b, data-scores 4,4,3,3,3)", "PASS",
    "Calibration instruction applied: ~/.fanout/blind/FC2-d.json gives B = 4,3,3,3,3 against the official 4,4,3,3,3 (project.html:520 and :522). The one difference is C2 (3 blind, 4 official), within one level, so accepted.")
row("fc2d-exemplar-numbers", "numbers in both exemplars", "course/modules/FC/FC2/project.html:520-583", "PASS",
    CARRY + " lines 520-583 unchanged. Numbers spot-checked again this round against out/rederive_r15.out: 226, 540, 63, 3, 166, 480, cost 60 = 3 x (8 + 12), discounted strikes 6500 to 6175 and 7000 to 6650.")
row("fc2d-exemplar-annotations", "annotations of both exemplars", "course/modules/FC/FC2/project.html:520-641", "PASS",
    CARRY + " lines 520-641 unchanged (the changed line 518 is outside this range).")
row("fc2d-exemplar-brief-structure", "exemplar notes against the brief's six headings",
    "course/modules/FC/FC2/project.html:489-499 (brief), :518 (intro sentence), :525-573 (B headings), :589-626 (A headings)", "FAIL",
    "The brief (project.html:489-499 list) has six headings: Summary; Chain and cost model; Findings; Model-free and model-dependent; Explanation and settlement; Limitations. Exemplar B's h5 headings (:525, :537, :549, :561, :573) are Summary, Findings, Model-free and model-dependent, Explanation and settlement, Limitations: five, without Chain and cost model, as the new :518 says. Exemplar A's h5 headings are Findings (:589), Costs (:601), Assumptions and models (:613) and Conclusion (:626). Findings is one of the six, so A has one heading, not none. The new :518 sentence 'Exemplar A has none' is therefore false.",
    "Edit project.html:518 so it states Exemplar A's count: 'Exemplar A has one of them, Findings, and Exemplar B has five, without Chain and cost model.' Re-check the sentence after the edit.")
row("fc2d-spec-explanation-labels", "explanation labels per finding kind are checked as the spec states them",
    "course/modules/FC/FC2/project.html:301 (spec), :327 (P4), :329 (model-free definition); course/modules/FC/FC2/grader/test_project.py:42-43, 674-686", "FAIL",
    "The spec (project.html:301) says a parity finding names P1, P2, P3, P4 and P6, and a convexity finding names P1, P2, P5 and P6. The suite checks presence only, so a convexity explanation that also names P4 survives: mutant r15_b (ledgers/FC2/mutants/r15_b_convexity_explanation_names_P4_as_an_input.py) passes 98/98 on seeds 0-9 and 0 kills on seeds 10-49 (ledgers/FC2/scripts/FC2-d-r15/out/mutate_graders_with_r15.out). P4 is not an input of the convexity test (project.html:327: 'the convexity test does not'; :329: model-free is a test that 'uses only P1, P2 and P5').",
    "In test_scan_explanations_are_nonempty_and_name_the_rule, assert the label set of each kind equals the spec's list (parity P1, P2, P3, P4, P6; convexity P1, P2, P5, P6), so a convexity explanation naming P4 fails.")
row("fc2d-spec-errors-scope", "named error conditions and their scope", "course/modules/FC/FC2/project.html:305-316; course/modules/FC/FC2/grader/test_project.py", "PASS",
    CARRY + " lines 305-316 unchanged.")
row("fc2d-hours", "time budget arithmetic", "course/modules/FC/FC2/project.html:339-357; course/modules/FC/FC2/index.html:29", "PASS",
    "Fresh: the table rows are 2 + 3 + 5 + 9 + 3 + 5 + 3 = 30, equal to the total row and data-hours-project=\"30\" (index.html:29). Hub: data-hours-lessons=60 plus data-hours-project=30 = 90, matching the eyebrow '90 hours' (index.html line 30 area). index.html:29 is outside the changed hunk (@@ -30).")
row("fc2d-reading-theorem-locator", "reading list gives no unread locators", "course/modules/FC/FC2/project.html:652-660", "PASS",
    CARRY + " lines 652-660 unchanged.")
row("fc2d-references-no-locator", "references carry no locator from memory", "course/modules/FC/FC2/project.html:652-660", "PASS",
    CARRY + " lines 652-660 unchanged.")
row("fc2d-notation", "every symbol against notation/notation.json", "course/modules/FC/FC2/project.html; notation/notation.json", "PASS",
    "notation/notation.json is byte-identical since 1431aa1d. The two changed lines (37, 518) introduce no mathematical symbol; the new label 'P1' is the page's own label, defined at project.html:327, which also says the labels P1 to P6 are not the put price P. Other lines byte-identical (carried from round 14).")
row("fc2d-simulated-label", "SIMULATED labelling", "course/modules/FC/FC2/project.html (18 occurrences); course/modules/FC/FC2/grader/instance.py:1, 120", "PASS",
    "Fresh: grep -o SIMULATED project.html gives 18, as in round 14. instance.py is byte-identical (carried).")
row("fc2d-process-banned", "no process words in learner text", "course/modules/FC/FC2/project.html", "PASS",
    "Fresh grep (builder, verifier, round N, planner, draft, TODO, agent, ruling, fragment, pin, blind): no hits. 'round' occurs only as round_cents (code) and rounding/rounds (prose). 'calibrat' occurs only in the learner-facing self-assessment (:321, :638).")
row("fc2d-ladder-claims", "ladder claims", "course/modules/FC/FC2/project.html:40-50", "PASS",
    CARRY + " lines 40-50 unchanged.")
row("fc2d-curriculum-scope", "curriculum scope of the project", "curriculum/02-economics-finance-core.yaml:425-431", "PASS",
    CARRY + " curriculum/02 unchanged.")
row("fc2d-no-external", "no external links", "course/modules/FC/FC2/project.html", "PASS",
    "Fresh: grep -c http project.html = 0. 21 internal href anchors, all resolve to an id on the page; 12 relative hrefs, all exist on disk (scratch check in this round).")
row("fc2d-new-tests", "new tests of the round", "course/modules/FC/FC2/grader/test_project.py", "PASS",
    CARRY + " test_project.py unchanged since the previous pin.")
row("fc2d-lab1-hypothesis-terms", "Lab 1 hypothesis terms", "course/modules/FC/FC2/project.html:55", "PASS",
    CARRY + " line 55 unchanged.")
row("fc2d-r6-project-line335", "model-free and model-dependent defined before use", "course/modules/FC/FC2/project.html:37, :285, :335, :495, :511", "PASS",
    "Fresh: line 37 (changed) uses 'P1 under Conventions and assumptions, below', which resolves to h3#conventions (:325) where P1 is defined (:327). Lines 285, 335, 495 and 511 are byte-identical (carried).")
row("fc2d-r7-project-anchor-links", "internal anchors resolve", "course/modules/FC/FC2/project.html:37, :282", "PASS",
    "Fresh: all 21 internal anchors in project.html resolve to an id (scratch check); line 37 has one more anchor than round 14 and it resolves.")
row("fc2d-dag-closure", "prerequisite closure of FC2", "coursekit.prerequisite_closure('FC2')", "PASS",
    "Fresh: ['AC1', 'CF1', 'E1', 'FC1', 'M1', 'M2', 'M4', 'P0.1']. FC1, CF1 and M4 are direct prerequisites; index.html's meta row says the closure 'adds M1, M2, AC1, E1 and P0.1', which matches.")
row("fc2d-r14-delta", "the round-14-to-round-15 delta inside the slice", "course/modules/FC/FC2/project.html; course/modules/FC/FC2/grader/*; tests/labs/FC2/lab-FC2-project-{1,2,3}.py; ledgers/FC2/mutants", "PASS",
    "git diff 1431aa1d..dde0486b: project.html changes only lines 37 (lede) and 518 (exemplar intro), both re-read in full above; grader/*, the three project labs, notation/, references/ and curriculum/02 are byte-identical. git diff marks ledgers/FC2/mutants/r14_a..r14_e as added since 1431aa1d (the round-14 fragment counted them); all five are KILLED in this round's run. The four r15 files are new in this round. Outside this slice in the same range: tests/labs/FC2/lab-FC2-L02-1.py and lab-FC2-L06-1.py (lesson labs), course/modules/FC/FC2/index.html (hub lede and ladder) and cards.json; these belong to the other FC2 slices and were not verified here.")
row("fc2d-r15-mut-a-parity-explanation-direction", "mutant r15_a (positive-gap parity explanation gives the reverse trade) survives",
    "ledgers/FC2/mutants/r15_a_parity_explanation_reverses_the_positive_gap_trade.py; course/modules/FC/FC2/grader/test_project.py", "PASS",
    "Survives 98/98 on seeds 0-9 and 0 kills on seeds 10-49 (mutate_graders_with_r15.out; scratch harness). The spec (project.html:301) requires the explanation to name the rule and the labels, not the trade direction; the round-6 ruling (fc2d-r5-mut-direction) makes explanation direction a non-finding. Recorded as a ruled survivor, not a grader defect. Note for the builder: project.html:336 states the trade for a positive gap, and the explanation contradicts it.")
row("fc2d-r15-mut-b-convexity-names-P4", "mutant r15_b (convexity explanation also names P4) survives",
    "ledgers/FC2/mutants/r15_b_convexity_explanation_names_P4_as_an_input.py; course/modules/FC/FC2/grader/test_project.py", "FAIL",
    "Survives 98/98 on seeds 0-9 and 0 kills on seeds 10-49. Unlike r15_a, this is a label claim, which the spec does state: project.html:301 'A convexity finding names P1, P2, P5 and P6' and 'the assumptions the finding depends on'; project.html:327 'The parity gap uses it, and the convexity test does not' (P4); :329 model-free means the test 'uses only P1, P2 and P5'. A convexity explanation that names P4 names a dependency it does not have.",
    "Assert the label set of each explanation equals the spec's list for its kind (see fc2d-spec-explanation-labels).")
row("fc2d-r15-mut-c-explanation-net-as-gross", "mutant r15_c (parity explanation prints gross where net belongs) survives",
    "ledgers/FC2/mutants/r15_c_parity_explanation_prints_gross_where_net_belongs.py", "PASS",
    "Survives on seeds 0-9 (98/98 each) and 0 kills on seeds 10-49. The spec (project.html:301) asks only for a non-empty explanation naming the rule and labels; explanation numbers are not in the grader spec (same ruling as fc2d-r5-mut-direction). Recorded as a ruled survivor. The C2 rubric (project.html:509) concerns the note, not the explanation string.")
row("fc2d-r15-mut-d-convexity-explanation-side", "mutant r15_d (convexity explanation says the call lies below the chord) survives",
    "ledgers/FC2/mutants/r15_d_convexity_explanation_reverses_the_chord_side.py", "PASS",
    "Survives on seeds 0-9 (98/98 each) and 0 kills on seeds 10-49. Explanation direction, same ruling as fc2d-r5-mut-direction; the convexity definition itself ('strictly above the chord', project.html:310) is enforced by the returned indices, which the suite does check.")
row("fc2d-r15-alt-integer-decimal", "two new correct alternatives (integer-only scaled by 1e6; Decimal at 60 digits) pass",
    "ledgers/FC2/scripts/FC2-d-r15/alts/alt7_integer_scaled.py; alt8_decimal_60.py", "PASS",
    f"Fresh: {OUT}/alt_alt7_integer_scaled.out and alt_alt8_decimal_60.out: both 50/50 seeds exit 0. Both are independent of Fraction and both reuse the reference's validation text.")

assert len(rows) == 68, len(rows)
ids = [r["id"] for r in rows]
assert len(set(ids)) == len(ids)
non_pass = [r["id"] for r in rows if r["status"] != "PASS"]
print("rows", len(rows), "non-pass", non_pass)

fragment = {
    "unit": "FC2",
    "slice": "d",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 15 (did not build FC2)",
    "pin": "dde0486beeb0312e4ac1cc03aaa02e56644adb24",
    "base": "1431aa1d842a5d2d05fd5953c098500bf78a4307 (round-14 pin; an ancestor of dde0486b)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD15-FC2-d (detached at dde0486b, .venv symlinked, course/assets/vendor present)",
    "scratch": f"{S}/ (harness.py, alts/, build_fragment_r15.py, lab_compare_r15.py) and {OUT}/ (every command output)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [
        "curriculum/02-economics-finance-core.yaml:427-429 says 'Given an embedded option-chain snapshot', which conflicts with the SIMULATED decision (plans/FC2-build-plan.md B1, Architect decisions). Not a slice defect; the page's honest-pending note is correct. Flagged for the curriculum owner (carried from rounds 6 and 14; curriculum unchanged since 1431aa1d).",
        "hull2021options, stoll1969relationship, cox1979option: registry records carry no edition, volume or issue. The page quotes none (carried from rounds 7 and 14).",
    ],
    "freshness_flags": [
        "plans/FC2-open-items.md departure 4 says 'the test count is 75 for seeds 0 to 49'. The page says 98 and pytest --collect-only gives 98 on every seed (out/collect_per_seed.out). The open-items note is stale; the page is correct.",
        "plans/FC2-open-items.md DAG_DEFECTS says FC2's closure excludes FC1. The closure now includes FC1 as a direct prerequisite (fc2d-dag-closure). The open-items note is stale.",
        "plans/FC2-open-items.md departure 7 says mutants are 10/10 killed. The directory now holds 107 files: 103 builder mutants (all killed) and four round-15 mutants, of which r15_b is a real survivor (FAIL) and r15_a, r15_c, r15_d are ruled survivors.",
        "course/modules/FC/FC2/index.html changed in the delta (lede: 'any forward price other than the cost-of-carry price admits a riskless profit'; ladder: 'six-strike'). Outside this slice; the hub verifier should re-check the lede's claim against the derivation.",
    ],
    "notes": [
        "Round 15 on pin dde0486b (the round-14 pin 1431aa1d is an ancestor). The round-14 fragment was read as context only. Every round-14 non-PASS row was re-verified from scratch; every other row is either re-run this round (fresh evidence cited) or carried with the prefix, where the cited files are byte-identical since 1431aa1d.",
        "Interpretation of 'subject byte-identical' for project.html: git diff 1431aa1d..dde0486b changes only lines 37 and 518 of project.html. Rows citing other line ranges of project.html are carried; rows citing line 37 or 518 are re-verified.",
        "Round-15 change in scope: line 37 (lede pointer to P1) is correct: P1 is defined at project.html:327 as exercise only at expiry. Line 518 is wrong (FAIL, fc2d-exemplar-brief-structure): Exemplar A has the heading Findings (:589), so it has one of the six headings, not none.",
        "The four round-15 mutants: r15_b survives on a label claim the spec states (FAIL). r15_a, r15_c, r15_d survive on explanation content (direction or numbers) that the grader spec does not state; they follow the round-6 ruling (fc2d-r5-mut-direction) and are recorded as ruled survivors. The killed_by string for these three follows the earlier convention 'SURVIVED (ruled non-finding...)'. The ledger's merge uses that string as truthy, so the ruled survivors count as killed there; the verdict FAIL comes from rows and from r15_b.",
        "Lab 2 page code differs from its twin only in three blanked lines (completion design, project.html:166-277). Its expected block equals the twin's output.",
        "Exemplar calibration used the file named in the brief (~/.fanout/blind/FC2-d.json), per the instruction: A matches the official scores; B differs by one level on C2 and is accepted. The exemplars were not scored blind by this verifier.",
        "Out of this slice but changed in the same delta range: tests/labs/FC2/lab-FC2-L02-1.py, lab-FC2-L06-1.py, index.html and cards.json. Not verified here.",
        "The bare mypy --strict on the grader folder without scanner.py reports import-not-found (scratch artefact). The grader strict check was run through run_graders, which copies the reference in.",
        "Alternatives: the round-14 set (alt1 to alt5, alt6) and two new ones (alt7 integer-only, alt8 Decimal at 60 digits) all pass 50/50. The float scanner without a cutoff is a deliberate non-compliant control and fails as the spec requires.",
    ],
    "summary": (
        f"FC2-d round 15: {len(rows) - len(non_pass)} PASS, {len(non_pass)} non-PASS of {len(rows)} rows. "
        "Non-PASS: fc2d-exemplar-brief-structure (the new project.html:518 sentence says Exemplar A has none of the six headings, but A has Findings at :589); "
        "fc2d-spec-explanation-labels and fc2d-r15-mut-b-convexity-names-P4 (the suite accepts a convexity explanation that also names P4, which the spec's label list and the P4 definition exclude). "
        "All gates pass on dde0486b (check_pages, check_dag, check_projects, run_labs 11/11, page_smoke, run_graders 50/50, ruff, mypy, pytest FC2, verify_refs). "
        "Collect count is 98 on every seed 0-49. Alternatives 8/8 pass 50/50. Mutants: 103/103 builder mutants killed; of the 4 round-15 mutants, r15_b is a FAIL and r15_a, r15_c, r15_d are ruled non-findings."
    ),
}

problems = []
import sys
sys.path.insert(0, str(ROOT / "tools"))
import ledger  # noqa: E402

problems = ledger.validate(fragment, "FC2-d")
print("validate:", problems)
(ROOT / "ledgers/FC2/FC2-d.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote ledgers/FC2/FC2-d.json")
