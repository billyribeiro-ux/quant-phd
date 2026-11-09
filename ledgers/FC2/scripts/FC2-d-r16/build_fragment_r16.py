"""Build the round-16 FC2 slice-d fragment from the scripts' outputs (run from the checkout root).

Mutant entries are parsed from out/mutate_graders_FC2_0-49_r16.out; row evidence cites the output files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/FC2/scripts/FC2-d-r16/out"
PIN = "e896b7a45344d1bc17ebfbf7fb05d87698ec9d6a"
PREV = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"
CARRY = "Carried from round 15 ({files} byte-identical since the previous pin {prev}): "

mutants = []
for line in (OUT / "mutate_graders_FC2_0-49_r16.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?): (.*) -> (.*)$", line)
    if not m:
        continue
    status, name, description, killed = m.groups()
    killed_by = None if killed.strip() == "None" else f"{killed} [seeds 0-49 run]"
    mutants.append({"id": name, "description": description, "killed_by": killed_by})

R = []


def row(rid, check, location, status, evidence, fix=""):
    entry = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        entry["fix"] = fix
    R.append(entry)


GATE = "tools/{tool} --unit FC2 on pin e896b7a4, run by the verifier this round"
row("fc2d-gate-check-projects", "tools/check_projects.py --unit FC2", "tools/check_projects.py", "PASS",
    "check_projects.py --unit FC2 -> 'check_projects FC2: PASS', exit 0 (out/check_projects.out).")
row("fc2d-gate-check-pages", "tools/check_pages.py --unit FC2", "tools/check_pages.py", "PASS",
    "check_pages.py --unit FC2 -> 'check_pages FC2: PASS', exit 0 (out/check_pages.out).")
row("fc2d-gate-check-dag", "tools/check_dag.py --unit FC2", "tools/check_dag.py", "PASS",
    "check_dag.py --unit FC2 -> 'check_dag FC2: PASS', exit 0 (out/check_dag.out).")
row("fc2d-gate-run-labs", "tools/run_labs.py --unit FC2", "course/modules/FC/FC2/*.html lab sections; tests/labs/FC2", "PASS",
    "run_labs.py --unit FC2 -> 'run_labs FC2: PASS (11/11)', exit 0 (out/run_labs.out). The tool checks each page lab's code is byte-identical to its twin, runs each twin under python -I -W error, and matches the expected block (covers L04 and L06 after the delta).")
row("fc2d-gate-page-smoke", "tools/page_smoke.py --unit FC2 and --pages project", "course/modules/FC/FC2/project.html",
    "PASS", "page_smoke.py --unit FC2 -> 'page_smoke FC2: PASS', exit 0 (out/page_smoke.out); page_smoke.py --unit FC2 --pages project (alone) -> PASS, exit 0 (out/page_smoke_project_alone.out).")
row("fc2d-gate-run-graders", "tools/run_graders.py --unit FC2 --seeds 0-49", "course/modules/FC/FC2/grader", "PASS",
    "run_graders.py --unit FC2 --seeds 0-49 -> 'run_graders FC2: PASS (reference 50/50 seeds, slowest 0.3 s)', exit 0 (out/run_graders.out).")
row("fc2d-gate-ruff", "ruff check and ruff format --check on the grader and tests/labs/FC2",
    "course/modules/FC/FC2/grader; tests/labs/FC2", "PASS",
    "ruff check -> 'All checks passed!' (out/ruff_check.out); ruff format --check -> '15 files already formatted' (out/ruff_format.out).")
row("fc2d-gate-mypy", "mypy (repo config) and mypy --strict on the grader", "pyproject.toml; course/modules/FC/FC2/grader", "PASS",
    "mypy --no-incremental (repo config) -> 'Success: no issues found in 385 source files' (out/mypy.out). mypy --strict on test_project.py, instance.py, starter.py, reference.py and scanner.py (= reference) copied to a scratch directory -> 'Success: no issues found in 5 source files' (out/mypy_strict_grader.out).")
row("fc2d-gate-pytest", "pytest -k 'FC2 or project' tests/", "tests/", "PASS",
    "pytest -q -k 'FC2 or project' tests/ -> 18 dots, '[100%]', exit 0 (out/pytest_fc2.out).")
row("fc2d-gate-verify-refs", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    "verify_refs.py --offline -> 'offline integrity: 560 entries, 0 problems', exit 0 (out/verify_refs.out).")
row("fc2d-collect-count", "pytest --collect-only count equals the page count", "course/modules/FC/FC2/project.html:320", "PASS",
    "harness_r16.py reference.py collect 0-49: 'N tests collected' with N = 98 on every seed 0-49 (out/collect_per_seed.r16.out, 50 lines). project.html:320 says 'collects 98 checks'. The new test in this delta replaces a loop with one assert, so the count is unchanged.")
row("fc2d-seeds-84", "reference passes the suite on the seed window", "course/modules/FC/FC2/grader/test_project.py", "PASS",
    "run_graders.py --seeds 0-49 reference 50/50 (out/run_graders.out); harness_r16.py reference.py run 0-49: 50 lines exit=0, '98 passed' (out/reference.r16.out).")
row("fc2d-starter-fails", "the starter fails the suite", "course/modules/FC/FC2/grader/starter.py", "PASS",
    "harness_r16.py starter.py run 0-49: exit=1 on 50/50 seeds (out/starter.r16.out).")
row("fc2d-alternatives", "five plus one alternative correct implementations, and two new ones, pass the suite",
    "ledgers/FC2/scripts/FC2-d-r14/alts/alt1..alt5, FC2-d-r14/alt6_round6_alternative.py, FC2-d-r15/alts/alt7, alt8", "PASS",
    "harness_r16.py on each of the eight alternatives, seeds 0-49: alt1_fraction_class, alt2_integer_only, alt3_float_epsilon_cutoff, alt4_adjacent_slopes, alt5_forward_price_parity, alt6_round6_alternative, alt7_integer_scaled, alt8_decimal_60 each 50/50 exit=0 (out/alt_*.r16.out). The new explanation check (test_project.py:682-686) passes all eight.")
row("fc2d-alt-r14-float-no-cutoff", "plain float implementation without cutoff is rejected", "course/modules/FC/FC2/grader/test_project.py:286-291, 802-806", "PASS",
    CARRY.format(files="test_project.py lines 286-291 and 802-806", prev=PREV) +
    "the only hunk in test_project.py since the previous pin is at :682-686. The float-no-cutoff control was not re-run this round.")
row("fc2d-alt-r6-overconstraint", "round-6 alternative passes the suite", "ledgers/FC2/scripts/FC2-d-r14/alt6_round6_alternative.py", "PASS",
    "harness_r16.py alt6_round6_alternative.py run 0-49: 50/50 exit=0 (out/alt_alt6_round6_alternative.r16.out).")
row("fc2d-mutate-builder", "all builder mutants are killed (pre-existing set, 103 files)", "ledgers/FC2/mutants/", "PASS",
    "mutate_graders.py --unit FC2 --seeds 0-49 (out/mutate_graders_FC2_0-49_r16.out): 106/108 killed. The two survivors are not builder mutants: r15_a (row fc2d-r15-mut-a-parity-explanation-direction) and r16_c (row fc2d-r16-mut-c-float-chord-weights). All 103 builder mutants print KILLED.")
for rid, label, names in [
    ("fc2d-mut-new-r14", "round-14 new mutants r14_a to r14_e are killed", "r14_a..r14_e"),
    ("fc2d-mut-v03", "mutant v03 killed", "v03"),
    ("fc2d-mut-v04", "mutant v04 killed", "v04"),
    ("fc2d-mut-v05", "mutant v05 killed", "v05"),
    ("fc2d-mut-v06", "mutant v06 killed", "v06"),
    ("fc2d-mut-v01-boundary", "mutant v01 (zero net boundary) killed", "v01"),
    ("fc2d-mut-v02-labels", "mutant v02 (explanation labels) killed", "v02"),
    ("fc2d-r5-mut-swap-weights", "mutant r5_b killed", "r5_b"),
    ("fc2d-r5-mut-skip-first", "mutant r5_c killed", "r5_c"),
    ("fc2d-r6-mut-new", "round-6 new mutants r6_a to r6_c killed", "r6_a..r6_c"),
    ("fc2d-r7-mut-new", "round-7 new mutants r7_a to r7_c killed", "r7_a..r7_c"),
]:
    row(rid, label, f"ledgers/FC2/mutants/ ({names})", "PASS",
        f"mutate_graders.py --unit FC2 --seeds 0-49 (out/mutate_graders_FC2_0-49_r16.out): every {names} line reads KILLED with a test name and seed.")
row("fc2d-r5-mut-direction", "round-5 mutant r5_d (explanation direction) is ruled a non-finding and is not in the suite",
    "ledgers/FC2/mutants/ (r5_d absent)", "PASS",
    "ls ledgers/FC2/mutants | grep -c '^r5_d' -> 0 (fresh this round).")
row("fc2d-r5-grader-exact-ties", "round-5 exact-tie tests", "course/modules/FC/FC2/grader/test_project.py:271-291, 795-822", "PASS",
    CARRY.format(files="test_project.py lines 271-291 and 795-822", prev=PREV) +
    "the only hunk in that file is at :682-686. The ties are re-checked in the r16 mutant runs (v03, v06, r6_a, r14_d, r16_c kill or survive as recorded).")
row("fc2d-r6-new-tie-tests", "round-6 new tie tests", "course/modules/FC/FC2/grader/test_project.py:809-850", "PASS",
    CARRY.format(files="test_project.py lines 809-850", prev=PREV) + "the only hunk is at :682-686.")
row("fc2d-grader-stdlib", "grader is standard library only", "course/modules/FC/FC2/grader/instance.py, reference.py, starter.py; test_project.py", "PASS",
    CARRY.format(files="instance.py, reference.py, starter.py and the import block of test_project.py", prev=PREV) +
    "instance.py, reference.py and starter.py are byte-identical (git diff --quiet). test_project.py imports at :16-32 are unchanged.")
row("fc2d-grader-messages", "named error messages", "course/modules/FC/FC2/grader/test_project.py:450-650; course/modules/FC/FC2/project.html:305-316", "PASS",
    CARRY.format(files="test_project.py lines 450-650 and project.html lines 305-316", prev=PREV) +
    "the project.html hunk is at :518 and the test_project.py hunk at :682-686.")
row("fc2d-grader-instance-validity", "instance generator validity", "course/modules/FC/FC2/grader/instance.py:41-60, 102-111, 118-131", "PASS",
    "instance.py is byte-identical since the previous pin. instance_validity_r16.py (out/instance_validity_r16.out, python -I): 100 instances (seeds 0-49, two chains each) checked against the input rules of project.html:287-291 (lengths, strictly increasing positive strikes, df_ppm in 1 to 1000000, non-negative spot and cost, integer quotes): 0 problems. run_graders.py checks determinism and distinctness on seeds 0-19 (out/run_graders.out: PASS).")
row("fc2d-grader-instance-diversity", "instance diversity across seeds", "course/modules/FC/FC2/grader/instance.py:6-9, 134-142", "PASS",
    "instance_validity_r16.py (out/instance_validity_r16.out): 54 distinct answer sets over the 100 instances, 53 instances with at least one finding, so the answers change with the seed, not only the labels. instance.py byte-identical since the previous pin.")
row("fc2d-lab1", "project Lab 1 page code, expected block and twin", "course/modules/FC/FC2/project.html:53-165; tests/labs/FC2/lab-FC2-project-1.py", "PASS",
    "run_labs.py --unit FC2: 'PASS (11/11)' (out/run_labs.out) covers the page code against the twin and the expected block against output. Twin and page lines are unchanged since the previous pin.")
row("fc2d-lab2", "project Lab 2 completion page code, expected block and twin", "course/modules/FC/FC2/project.html:166-277; tests/labs/FC2/lab-FC2-project-2.py", "PASS",
    "run_labs.py --unit FC2: PASS (11/11) (out/run_labs.out), which is the completion-lab rule (blanks allowed, twin lines match, output matches).")
row("fc2d-lab3", "project Lab 3 page code, expected block and twin", "course/modules/FC/FC2/project.html:375-488; tests/labs/FC2/lab-FC2-project-3.py", "PASS",
    "run_labs.py --unit FC2: PASS (11/11) (out/run_labs.out).")
row("fc2d-lab-twins-pure", "twins run alone under python -I -W error", "tests/labs/FC2/lab-FC2-project-{1,2,3}.py", "PASS",
    "run_labs.py runs each twin under python -I -W error with no stderr (out/run_labs.out: PASS 11/11). Also run by hand: python -I -W error tests/labs/FC2/lab-FC2-L04-1.py and lab-FC2-L06-1.py -> exit 0.")
row("fc2d-rederive-numbers", "every number in the Lab 1, Lab 2 and Lab 3 prose re-derived", "course/modules/FC/FC2/project.html:53-488", "PASS",
    CARRY.format(files="project.html lines 53-488", prev=PREV) +
    "the only project.html hunk since the previous pin is at :518. The lab outputs were re-run this round (run_labs 11/11).")
row("fc2d-rubric-observable", "rubric levels are observable", "course/modules/FC/FC2/project.html:504-516", "PASS",
    CARRY.format(files="project.html lines 504-516", prev=PREV) + "no change in that range.")
row("fc2d-rubric-calib-A", "calibration of Exemplar A against the official scoring", "course/modules/FC/FC2/project.html:584-641 (article#exemplar-a, data-scores 2,1,2,2,1)", "PASS",
    "blind scores in ~/.fanout/blind/FC2-d.json: A = [2, 1, 2, 2, 1]; official data-scores 2,1,2,2,1 (project.html:584). Every criterion matches exactly.")
row("fc2d-rubric-calib-B", "calibration of Exemplar B against the official scoring", "course/modules/FC/FC2/project.html:520-583 (article#exemplar-b, data-scores 4,4,3,3,3)", "PASS",
    "blind scores in ~/.fanout/blind/FC2-d.json: B = [4, 3, 3, 3, 3]; official data-scores 4,4,3,3,3 (project.html:520). Differences: C2 only, 3 against 4, which is one level (accepted, plans/KNOWN-ISSUES.md rubric calibration table).")
row("fc2d-exemplar-numbers", "numbers in both exemplars", "course/modules/FC/FC2/project.html:520-583", "PASS",
    CARRY.format(files="project.html lines 520-583", prev=PREV) + "the 518 hunk is outside this range.")
row("fc2d-exemplar-annotations", "annotations of both exemplars", "course/modules/FC/FC2/project.html:520-641", "PASS",
    CARRY.format(files="project.html lines 520-641", prev=PREV) + "the 518 hunk is outside this range.")
row("fc2d-exemplar-brief-structure", "exemplar notes against the brief's six headings",
    "course/modules/FC/FC2/project.html:489-499 (brief), :518 (intro sentence), :525-573 (B headings), :589-626 (A headings)", "PASS",
    "Brief list (project.html:491-497) has six headings: Summary; Chain and cost model; Findings; Model-free and model-dependent; Explanation and settlement; Limitations. Exemplar B h5 headings (:525, :537, :549, :561, :573) are Summary, Findings, Model-free and model-dependent, Explanation and settlement, Limitations: five, without Chain and cost model. Exemplar A h5 headings (:589, :601, :613, :626) are Findings, Costs, Assumptions and models, Conclusion: one of the six (Findings). The new :518 sentence 'Exemplar A has one of them, Findings, and Exemplar B has five, without Chain and cost model' is therefore correct. Fresh read of the hunk, this round.")
row("fc2d-spec-explanation-labels", "explanation labels per finding kind are checked as the spec states them",
    "course/modules/FC/FC2/project.html:301 (spec), :327 (P4), :329 (model-free definition); course/modules/FC/FC2/grader/test_project.py:42-43, 674-686", "PASS",
    "project.html:301 says a parity finding names P1, P2, P3, P4 and P6 and a convexity finding names P1, P2, P5 and P6. test_project.py:42-43 PARITY_LABELS and CONVEXITY_LABELS match those lists. test_project.py:683-686 now asserts set(re.findall(r'\\bP[1-6]\\b', text)) == set(labels). The reference passes 50/50 and all eight alternatives pass 50/50 (out/alt_*.r16.out). mutant r15_b (convexity names P4) is KILLED on seed 0 (out/mutate_graders_FC2_0-49_r16.out).")
row("fc2d-spec-errors-scope", "named error conditions and their scope", "course/modules/FC/FC2/project.html:305-316; course/modules/FC/FC2/grader/test_project.py", "PASS",
    CARRY.format(files="project.html lines 305-316 and the error-condition tests", prev=PREV) + "the 518 and :682-686 hunks are outside them.")
row("fc2d-hours", "time budget arithmetic", "course/modules/FC/FC2/project.html:339-357; course/modules/FC/FC2/index.html:29", "PASS",
    CARRY.format(files="project.html lines 339-357", prev=PREV) + "no change in that range.")
row("fc2d-reading-theorem-locator", "reading list gives no unread locators", "course/modules/FC/FC2/project.html:652-660", "PASS",
    CARRY.format(files="project.html lines 652-660", prev=PREV) + "no change in that range.")
row("fc2d-references-no-locator", "references carry no locator from memory", "course/modules/FC/FC2/project.html:652-660", "PASS",
    CARRY.format(files="project.html lines 652-660", prev=PREV) + "no change in that range.")
row("fc2d-notation", "every symbol against notation/notation.json", "course/modules/FC/FC2/project.html; notation/notation.json", "PASS",
    "notation/notation.json byte-identical since the previous pin. The only project.html hunk (:518) contains no symbol, so no new notation use; the rest of the file is carried (unchanged lines).")
row("fc2d-simulated-label", "SIMULATED labelling", "course/modules/FC/FC2/project.html (18 occurrences); course/modules/FC/FC2/grader/instance.py:1, 120", "PASS",
    "grep -o SIMULATED course/modules/FC/FC2/project.html | wc -l -> 18 (unchanged count).")
row("fc2d-process-banned", "no process words in learner text", "course/modules/FC/FC2/project.html", "PASS",
    "grep -n -i for verifier, ruling, round N, builder, delta, architect, known issue, TODO, TBD, lorem, for brevity, details omitted, beyond the scope, left as an exercise, you can add more, it is important to note, studies show, experts agree, it is well known, obviously, clearly, about 6%, roughly half, historically, it can be shown, and '...' (BUILDER_RULES 1.3-1.4) over project.html -> no hits (this round). The new :518 sentence contains none of them.")
row("fc2d-ladder-claims", "ladder claims", "course/modules/FC/FC2/project.html:40-50", "PASS",
    CARRY.format(files="project.html lines 40-50", prev=PREV) + "no change in that range.")
row("fc2d-curriculum-scope", "curriculum scope of the project", "curriculum/02-economics-finance-core.yaml:425-431", "PASS",
    "curriculum/02-economics-finance-core.yaml byte-identical since the previous pin (git diff --quiet). Carried.")
row("fc2d-no-external", "no external links", "course/modules/FC/FC2/project.html", "PASS",
    "page_smoke.py --unit FC2 and --pages project: zero requests to any host other than the local server (out/page_smoke.out, out/page_smoke_project_alone.out). Grep of project.html shows only ../../../assets/vendor and site.js sources.")
row("fc2d-new-tests", "new tests of the round", "course/modules/FC/FC2/grader/test_project.py:682-686", "PASS",
    "The one changed test (test_scan_explanations_are_nonempty_and_name_the_rule, :674-686) was run: reference 50/50, alternatives 8x50/50, the wording-only mutants 50/50 (equiv_text_r16.py: 159 explanation texts, 0 differences in records, labels or rule word), r15_b, r16_a and r16_b killed. The label-set assertion is the spec's list, so it does not reject any of the eight correct alternatives.")
row("fc2d-lab1-hypothesis-terms", "Lab 1 hypothesis terms", "course/modules/FC/FC2/project.html:55", "PASS",
    CARRY.format(files="project.html line 55", prev=PREV) + "no change at that line.")
row("fc2d-r6-project-line335", "model-free and model-dependent defined before use", "course/modules/FC/FC2/project.html:37, :285, :335, :495, :511", "PASS",
    CARRY.format(files="project.html lines 37, 285, 335, 495 and 511", prev=PREV) + "no change at those lines.")
row("fc2d-r7-project-anchor-links", "internal anchors resolve", "course/modules/FC/FC2/project.html:37, :282", "PASS",
    "check_pages.py --unit FC2 PASS and page_smoke.py --pages project PASS (out/check_pages.out, out/page_smoke_project_alone.out); no anchor change at :37 or :282.")
row("fc2d-dag-closure", "prerequisite closure of FC2", "check_dag.py --unit FC2", "PASS",
    "check_dag.py --unit FC2 -> PASS (out/check_dag.out) on this pin.")
row("fc2d-r14-delta", "the round-15-to-round-16 delta inside the slice",
    "course/modules/FC/FC2/project.html:518; course/modules/FC/FC2/grader/test_project.py:682-686; tests/labs/FC2/lab-FC2-L04-1.py; tests/labs/FC2/lab-FC2-L06-1.py; ledgers/FC2/equivalent/; ledgers/FC2/mutants/r15_a, r15_b, r16_*; plans/FINAL-ARCHITECT-RULINGS.md rulings 9, 10, 34", "PASS",
    "git diff dde0486b..e896b7a4 -- course/modules/FC/FC2 tests/labs/FC2 ledgers/FC2 plans/FINAL-ARCHITECT-RULINGS.md read hunk by hunk. In slice d: project.html one line (:518, row fc2d-exemplar-brief-structure); test_project.py one assert (:682-686, rows fc2d-spec-explanation-labels, fc2d-new-tests); L04 and L06 twin docstrings (rows fc2d-r16-lab-docstrings-L04-L06); equivalent/ README and three new files (rows fc2d-r15-mut-*); mutants/ r15_a and r15_b (rows fc2d-r15-mut-a and -b). The L04/L06 lesson HTML and cards.json changes belong to the lesson slices and are not verified here.")
row("fc2d-r15-mut-a-parity-explanation-direction",
    "mutant r15_a (positive-gap parity explanation gives the reverse trade) is not left in mutants/ (ruling 9, ruling 34)",
    "ledgers/FC2/mutants/r15_a_parity_explanation_reverses_the_positive_gap_trade.py; ledgers/FC2/equivalent/README.md:3-9", "FAIL",
    "r15_a differs from the reference only in the parity explanation's action string and the docstring (diff this round). It survives all 50 seeds (mutate_graders out/mutate_graders_FC2_0-49_r16.out: SURVIVED ... -> None). Its wording-only nature is the same as r15_c and r15_d, and ruling 34 places all three in ledgers/FC2/equivalent/ with the README. ledgers/FC2/equivalent/README.md says the three mutants 'here' include r15_a, but ledgers/FC2/equivalent/ holds only r15_c and r15_d (git ls-tree e896b7a4). ruling 9 forbids a survivor in mutants/, so r15_a is a FAIL as committed.",
    "git mv ledgers/FC2/mutants/r15_a_parity_explanation_reverses_the_positive_gap_trade.py ledgers/FC2/equivalent/ (the README already lists it). Then mutate_graders.py --unit FC2 no longer counts it. Equivalence is evidenced by row fc2d-r15-mut-c-explanation-net-as-gross's randomized check, which covers r15_a as well.")
row("fc2d-r15-mut-b-convexity-names-P4", "mutant r15_b (convexity explanation also names P4) is killed", "ledgers/FC2/mutants/r15_b_convexity_explanation_names_P4_as_an_input.py; course/modules/FC/FC2/grader/test_project.py:683-686", "PASS",
    "mutate_graders.py --unit FC2 --seeds 0-49: 'KILLED r15_b_... -> test_scan_explanations_are_nonempty_and_name_the_rule (seed 0)' (out/mutate_graders_FC2_0-49_r16.out). harness_r16.py on r15_b, seeds 0-49: exit=1 on 26 seeds, so the kill is seed-dependent but present. The round-15 survivor is fixed.")
row("fc2d-r15-mut-c-explanation-net-as-gross", "mutant r15_c (parity explanation prints gross where net belongs) is a wording-only equivalent (ruling 34)",
    "ledgers/FC2/equivalent/r15_c_parity_explanation_prints_gross_where_net_belongs.py; ledgers/FC2/equivalent/README.md", "PASS",
    "Proof of equivalence under the grader: the only code difference from reference.py is _explain_parity(_half_up(gap), gross, ...) for net (diff this round). The record fields other than explanation are identical, and the explanation's P-label set and rule word are identical. equiv_text_r16.py over seeds 0-49 with both instance chains per seed (100 chains, 159 explanation texts): 0 record, label or rule differences for r15_a, r15_c and r15_d. harness_r16.py r15_c seeds 0-49: 50/50 exit=0. The page never states the explanation's number. Caveat for the architect: ruling 34 calls r15_c 'wording only', but it changes a printed number; the page's Context sentence (project.html:282, 'the desk asks whether it survives the cost') is the only candidate statement and is a purpose, not an explanation-field contract (project.html:301).")
row("fc2d-r15-mut-d-convexity-explanation-side", "mutant r15_d (convexity explanation reverses the chord side) is a wording-only equivalent (ruling 34)",
    "ledgers/FC2/equivalent/r15_d_convexity_explanation_reverses_the_chord_side.py", "PASS",
    "Diff this round: only the convexity explanation string changes (above/below the chord, buy/sell). Same randomized check as row fc2d-r15-mut-c-explanation-net-as-gross (0 differences over 100 chains). harness_r16.py r15_d seeds 0-49: 50/50 exit=0.")
row("fc2d-r15-alt-integer-decimal", "two new correct alternatives (integer-only scaled by 1e6; Decimal at 60 digits) pass",
    "ledgers/FC2/scripts/FC2-d-r15/alts/alt7_integer_scaled.py; alt8_decimal_60.py", "PASS",
    "harness_r16.py on alt7 and alt8, seeds 0-49: 50/50 exit=0 each (out/alt_alt7_integer_scaled.r16.out, out/alt_alt8_decimal_60.r16.out).")
row("fc2d-r16-mut-a-parity-explanation-names-P5", "new student-error mutant: parity explanation also names P5",
    "ledgers/FC2/mutants/r16_a_parity_explanation_names_P5_too.py", "PASS",
    "KILLED by test_scan_explanations_are_nonempty_and_name_the_rule (seed 1) in the 0-9 and 0-49 runs (out/mutate_graders_FC2_0-9_with_r16.out, out/mutate_graders_FC2_0-49_r16.out). A parity explanation naming P5 violates the spec list at project.html:301.")
row("fc2d-r16-mut-b-convexity-without-convex-word", "new student-error mutant: convexity explanation never names convexity",
    "ledgers/FC2/mutants/r16_b_convexity_explanation_states_chord_rule_without_the_word.py", "PASS",
    "KILLED by test_scan_explanations_are_nonempty_and_name_the_rule (seed 0) (out/mutate_graders_FC2_0-49_r16.out). The explanation must name the rule (test regex r'\\bconvex', project.html:301 'names the rule').")
row("fc2d-r16-mut-c-float-chord-weights", "new student-error mutant: convexity chord weights as float quotients survive (exact fractions rule)",
    "ledgers/FC2/mutants/r16_c_convexity_chord_weights_as_float_fractions.py; course/modules/FC/FC2/grader/test_project.py (no non-dyadic convexity tie test); course/modules/FC/FC2/project.html:308 ('Each money value is computed from exact fractions and rounded once')", "FAIL",
    "SURVIVES all 50 seeds (out/mutate_graders_FC2_0-49_r16.out: SURVIVED r16_c ... -> None). Counterexample, from ledgers/FC2/scripts/FC2-d-r16/search_float_chord_r16.py (out/search_float_chord.r16.out, 5538 chains, 3 mismatches): strikes [1, 2, 7], calls [2, 3, 5], puts [3, 5, 12], spot 0, df_ppm 1000000, zero cost. Exact chord at 2 is (5*2 + 1*5)/6 = 5/2, so the violation is 1/2 cent and the gross is 1 (reference: [('convexity', 2, 1, 1)]). The float weights give a second difference that lands on the other side of the half cent, and the mutant returns no finding. project.html:308 states 'Each money value is computed from exact fractions and rounded once'. Every existing convexity tie test uses a dyadic weight (1/2): test_project.py:809-816 (chord 50.5) and :843-850 (chord 3850.5).",
    "Add to course/modules/FC/FC2/grader/test_project.py: def test_convexity_half_cent_tie_at_a_non_dyadic_chord_weight_rounds_once_up() with hand_chain([1, 2, 7], [2, 3, 5], [3, 5, 12], spot=0, df=PPM, fee=0, spread=0) and assert rows_of(sol.scan(chain)) == [('convexity', 2, 1, 1)]. Verified by the verifier in a scratch copy: passes on reference.py and fails on r16_c. Then update project.html:320 from 98 to 99 checks and re-run run_graders.py --seeds 0-49 and collect-only.")
row("fc2d-r16-lab-docstrings-L04-L06", "L04 and L06 twin docstring sentences match what the lab prints and checks",
    "tests/labs/FC2/lab-FC2-L04-1.py:7-11; tests/labs/FC2/lab-FC2-L06-1.py:4-9", "PASS",
    "L06 docstring: 'the one-period cost V0, the one-period discounted expectation, and the two-period V0 by backward induction and in closed form ... in integer cents'. Output (python -I -W error ..., this round) prints cents for V0 (3000), the discounted expectation (3000), backward-induction V0 (4500) and closed-form V0 (4500); code lines 74-79 and 81-86. L04 docstring: 'The lab makes no claim about that choice at any date.' The twin prints no statement about selling before expiry. run_labs passes both (out/run_labs.out), so the page code equals the twin.")
row("fc2d-r16-explanation-check-no-overconstraint", "new exact label-set check does not reject a correct explanation",
    "course/modules/FC/FC2/grader/test_project.py:683-686; ledgers/FC2/scripts/FC2-d-r16/out/alt_*.r16.out", "PASS",
    "Every correct implementation (reference, alt1 to alt8: 9 implementations x 50 seeds) passes the exact-set check. The spec states the list (project.html:301) and the exact-set reading follows it. Judgement noted: an explanation that names an extra label the finding does not depend on (for example 'P5 does not apply') would now fail. The spec does not state that case, so no FAIL is raised.")
row("fc2d-r16-equivalence-wording-scope", "the three wording-only equivalents change no label, rule word or record field",
    "ledgers/FC2/equivalent/README.md", "PASS",
    "README claims (a) the label set and the rule word are the reference's, and (b) all three pass the grader on seeds 0-9. Verified by equiv_text_r16.py (seeds 0-49, two chains each) and harness_r16.py (seeds 0-49, 50/50 each). Claim (c) 'The grader checks exactly that' matches test_project.py:683-686.")
mutants_list = mutants
frag = {
    "unit": "FC2",
    "slice": "d",
    "round": 16,
    "verifier": "Claude Haiku 5.5, independent verifier for FC2-d round 16 (did not build FC2)",
    "pin": PIN,
    "base": PREV + " (round-15 pin; previous fragment ~/.fanout/frags/D-FC2-d.round15.json, read as context, its PASS rows not trusted)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD16-FC2-d (detached at e896b7a4, .venv symlinked)",
    "scratch": "ledgers/FC2/scripts/FC2-d-r16/ (harness_r16.py, equiv_text_r16.py, probe_float_chord_r16.py, search_float_chord_r16.py, make_mutants_r16.py, build_fragment_r16.py) and out/",
    "verified_at": "2026-11-09T11:50:00+00:00",
    "verdict": "FAIL",
    "rows": R,
    "mutants": mutants_list,
    "registry_flags": [
        "curriculum/02-economics-finance-core.yaml:427-429 says 'Given an embedded option-chain snapshot', which conflicts with the SIMULATED decision (plans/FC2-build-plan.md B1). Flagged for the curriculum owner (carried from rounds 6, 14 and 15; curriculum byte-identical since dde0486b).",
        "hull2021options, stoll1969relationship, cox1979option: registry records carry no edition, volume or issue. The page quotes none (carried).",
    ],
    "freshness_flags": [
        "plans/FC2-open-items.md departure 4 says the test count is 75 for seeds 0 to 49. The page says 98 and collect-only gives 98 on every seed. The open-items note is stale.",
        "plans/FC2-open-items.md DAG_DEFECTS says FC2's closure excludes FC1. The closure now includes FC1 (check_dag PASS). The open-items note is stale.",
        "plans/FC2-open-items.md departure 7 says mutants are 10/10 killed. The directory holds 108 files; after the fixes in this report the count changes again.",
        "course/modules/FC/FC2/index.html changed in the earlier delta (outside this slice). The hub verifier should re-check its lede and ladder.",
    ],
    "notes": [
        "Delta since the previous pin dde0486b, read hunk by hunk: project.html :518 (one sentence); grader/test_project.py :682-686 (one assertion); tests/labs/FC2/lab-FC2-L04-1.py and L06 docstrings; ledgers/FC2/equivalent/ (README and r15_c, r15_d; r15_a is in mutants/); ledgers/FC2/mutants/ (r15_a and r15_b were added by the round-15 verifier and are committed in e896b7a4); plans/FINAL-ARCHITECT-RULINGS.md rulings 30-34; plans/KNOWN-ISSUES.md (not in this slice, read for the calibration table).",
        "Carry rule: a row is carried only where its cited lines are unchanged since dde0486b (the only hunks are :518, :682-686 and the two lab docstrings). Carried rows use the prefix 'Carried from round 15'.",
        "The full-file read of project.html and test_project.py was not repeated this round. The protocol for a delta round reads the hunks, and the rows whose subject is the whole file were re-checked by grep and by the gates.",
        "Ruling 34 calls r15_c 'wording only', but it changes a printed number inside the explanation. The verifier accepts it as an equivalent under the grader's stated contract (project.html:301 names labels, not numbers), and records the imprecision as a caveat in row fc2d-r15-mut-c.",
        "The explanation check is an exact set of P-labels. It matches the spec list and does not reject any of the nine correct implementations. A correct explanation that names an extra non-dependency label would be rejected; the spec does not state that case.",
        "Adding the test proposed in row fc2d-r16-mut-c changes the collected count to 99, so project.html:320 must change with it, or the count row fails.",
        "ledgers/FC2/equivalent/README.md is accurate about r15_c and r15_d and their check; it lists r15_a as a third member of equivalent/, which is false at e896b7a4 (r15_a is in mutants/). See row fc2d-r15-mut-a.",
    ],
    "summary": "FC2-d round 16 on e896b7a4: 72 PASS, 2 FAIL of 74 rows. Non-PASS: fc2d-r15-mut-a-parity-explanation-direction (r15_a is still in mutants/ and survives; ruling 9 requires equivalent/; git mv fixes it); fc2d-r16-mut-c-float-chord-weights (a float-weight convexity mutant survives all 50 seeds because no non-dyadic convexity tie test exists; counterexample strikes [1,2,7] calls [2,3,5]; proposed test kills it). Fixed since round 15: fc2d-exemplar-brief-structure (the new :518 sentence is correct), fc2d-spec-explanation-labels and fc2d-r15-mut-b (new label-set check kills r15_b). All gates PASS: check_pages, check_dag, check_projects, run_labs 11/11, page_smoke (FC2 and project alone), run_graders 50/50, ruff, mypy, pytest FC2, verify_refs (560, 0 problems), collect 98 on seeds 0-49, 8 alternatives 50/50 each, starter 0/50. Calibration against ~/.fanout/blind/FC2-d.json: A exact, B within one level.",
}
n_fail = sum(1 for r in R if r["status"] != "PASS")
frag["verdict"] = "PASS" if n_fail == 0 and all(m["killed_by"] for m in mutants_list) else "FAIL"
out_path = ROOT / "ledgers/FC2/FC2-d.json"
out_path.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(R), "fail", n_fail, "mutants", len(mutants_list), "killed", sum(1 for m in mutants_list if m["killed_by"]))
