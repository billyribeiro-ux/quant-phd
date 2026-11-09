"""Builds ledgers/E3/E3-d.json (round 15) from the round-15 verifier run outputs in this directory.

Every row's status and evidence is written by the verifier from the outputs it cites; this script only assembles them.
Usage (from the checkout root): python3 -I ledgers/E3/scripts/E3-d-r15/verifier/build_fragment.py
"""
import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.cwd()
V = ROOT / "ledgers/E3/scripts/E3-d-r15/verifier"
V_REL = "ledgers/E3/scripts/E3-d-r15/verifier"
PIN = "dde0486beeb0312e4ac1cc03aaa02e56644adb24"

# ---- mutants: the official tool's output, plus the verifier's three new mutants -------------------------------
mut = []
for line in (V / "mutate_E3_0-9.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"(KILLED|SURVIVED) (\S+?)\.py: (.*?) -> (.*)$", line)
    if m:
        status, name, desc, killed = m.groups()
        mut.append({"id": name, "description": desc.strip(), "killed_by": killed.strip() if status == "KILLED" else None,
                    "source": "tools/mutate_graders.py --unit E3 --seeds 0-9"})
official_line = next((l for l in (V / "mutate_E3_0-9.out").read_text(encoding="utf-8").splitlines() if l.startswith("mutate_graders")), "")

NEW = {
    "v15d_01_crra_certainty_equivalent_truncated_toward_zero": (
        "Student error: CRRA certainty equivalent (gamma not 0) rounded by int(y), truncation toward zero, instead of the nearest cent with an exact half going up.",
        "test_crra_within_half_cent_of_oracle_for_instance_lotteries (all seeds 0-9)"),
    "v15d_02_crra_zero_gamma_exact_half_rounds_to_even": (
        "Student error: at gamma = 0 the exact expected prize is rounded with round(), so an exact half cent goes to the even neighbour, against the Whole cents paragraph.",
        "test_crra_gamma_zero_is_expected_final_wealth_exactly and test_half_cent_rounding_on_exact_halves (all seeds 0-9)"),
    "v15d_03_reported_gamma_clamped_at_0_99": (
        "Student error: reported curvature clamped at 0.99, inside the page's supported range [0.001, 0.999]; the estimate is not the reported maximum for fits in (0.99, 0.999).",
        "SURVIVED on seeds 0-9 (52 passed on every seed); killed only by the grader's own maximum helper on a fit the suite does not generate (see grader-local-max-in-range-fit)"),
}
for stem, (desc, killed) in NEW.items():
    mut.append({"id": stem, "description": desc, "killed_by": None if stem.endswith("0_99") else killed,
                "source": "verifier round 15, ledgers/E3/mutants/" + stem + ".py"})

killed_total = sum(1 for m in mut if m.get("killed_by"))

# ---- rows ---------------------------------------------------------------------------------------------------------
CARRY = "Carried from round 14 (project.html lines 53-150 byte-identical since 1431aa1d; the round-14 check still holds): "
R = []


def row(rid, check, location, status, evidence, fix=None):
    d = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        d["fix"] = fix or ""
    R.append(d)


# gates, re-run at dde0486b
row("gate-check-pages", "tools/check_pages.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{V_REL}/check_pages.out: 'check_pages E3: PASS', EXIT=0.")
row("gate-check-dag", "tools/check_dag.py --unit E3", "course/modules/E/E3/", "PASS",
    f"{V_REL}/check_dag.out: 'check_dag E3: PASS', EXIT=0.")
row("gate-check-projects", "tools/check_projects.py --unit E3", "course/modules/E/E3/project.html", "PASS",
    f"{V_REL}/check_projects.out: 'check_projects E3: PASS', EXIT=0.")
row("gate-run-labs-project", "tools/run_labs.py --unit E3 --page project", "project.html Labs 1-3", "PASS",
    f"{V_REL}/run_labs_project.out: 'run_labs E3: PASS (3/3)', EXIT=0.")
row("gate-run-graders-seeds-0-49", "tools/run_graders.py --unit E3 --seeds 0-49", "course/modules/E/E3/grader/", "PASS",
    f"{V_REL}/run_graders_0_49.out: 'run_graders E3: PASS (reference 50/50 seeds, slowest 40.1 s)', EXIT=0 (limit 60 s).")
row("gate-collect-51", "pytest --collect-only on grader/test_project.py (count on page)", "grader/test_project.py; project.html Grading mode", "PASS",
    f"{V_REL}/collect_only.out: '52 tests collected'. The id keeps its round-14 name; the count now matches the page's '52 checks'.")
row("gate-suite-scan-0-399", "full suite on reference.py, seeds 0-399 (8 workers)", "grader/test_project.py; project.html Constraints and Grading mode", "PASS",
    f"{V_REL}/reference_scan_0_399.txt: 392 seeds pass; the 8 failing seeds are 89, 108, 110, 157, 165, 235, 269, 373, the page's list (Constraints and Grading mode).")
row("gate-starter-fails", "run_graders.py starter check (empty implementation must fail)", "course/modules/E/E3/grader/starter.py", "PASS",
    f"{V_REL}/run_graders_0_49.out: run_graders reports PASS, which includes the starter-fails check per its docstring.")
row("gate-ruff", "ruff check and ruff format --check on grader and tests/labs/E3", "course/modules/E/E3/grader; tests/labs/E3", "PASS",
    f"{V_REL}/ruff_check.out 'All checks passed!' EXIT=0; ruff_format.out '15 files already formatted' EXIT=0.")
row("gate-mypy-repo", "mypy --no-incremental (repository)", "repository", "PASS",
    f"{V_REL}/mypy_repo.out: 'Success: no issues found in 385 source files' EXIT=0.")
row("gate-mypy-grader-strict", "mypy --strict on grader with reference copied as elicit.py", "course/modules/E/E3/grader/", "PASS",
    f"{V_REL}/mypy_grader_with_reference.out: 'Success: no issues found in 3 source files' EXIT=0. Without the copy mypy reports import-not-found for elicit and instance (the layout, not the code).")
row("gate-verify-refs-offline", "tools/verify_refs.py --offline", "references/references.json", "PASS",
    f"{V_REL}/verify_refs_offline.out: 'offline integrity: 560 entries, 0 problems', EXIT=0. No reference changed in the delta.")
row("gate-pytest-relevant", "pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py", "tests/", "PASS",
    f"{V_REL}/pytest_relevant.out: all dots, EXIT=0.")
row("gate-page-smoke-project", "tools/page_smoke.py --unit E3 --pages project", "course/modules/E/E3/project.html", "PASS",
    f"{V_REL}/page_smoke_project.out: 'page_smoke E3: PASS', EXIT=0 (run alone).")
row("gate-mutate-existing-161", "tools/mutate_graders.py --unit E3 --seeds 0-9 (all 165 files in ledgers/E3/mutants at round 14 plus the 3 new verifier mutants are run separately)", "ledgers/E3/mutants/", "PASS" if official_line.startswith("mutate_graders E3: PASS") else "FAIL",
    f"{V_REL}/mutate_E3_0-9.out: '{official_line}'.",
    fix="A mutant of the 165 survived the official run; see the mutants list and the grader-related rows.")
row("gate-mutants-count", "count of mutant files and their kills (official run)", "ledgers/E3/mutants/", "PASS" if len(mut) == 168 else "FAIL",
    f"ledgers/E3/mutants holds 165 files at dde0486b (161 at 1431aa1d, +r14d_01, r14d_03, r14d_04; e12_03 moved to mutants as r14d_02) plus 3 verifier files v15d_01..03 = 168. The mutants list in this fragment has {len(mut)} entries.")

# labs
row("lab-1-expected-equals-output", "Lab 1 expected block equals twin output", "project.html Lab 1 (lab-E3-project-1)", "PASS",
    "run_labs PASS (above); tests/labs/E3/lab-E3-project-1.py run in isolation under python -I -W error: EXIT=0, 7 lines; page_vs_twin_project.py: 'lab 1: expected block == twin output: True'.")
row("lab-2-expected-equals-output", "Lab 2 expected block equals twin output", "project.html Lab 2 (lab-E3-project-2)", "PASS",
    "twin run in isolation under python -I -W error: EXIT=0, 4 lines; page_vs_twin_project.py: 'lab 2: expected block == twin output: True'.")
row("lab-3-expected-equals-output", "Lab 3 expected block equals twin output", "project.html Lab 3 (lab-E3-project-3)", "PASS",
    "twin run in isolation: output equals the expected block line for line (answers 12 | mixed 11; gamma_hat 0.6352; lambda_hat 6.1503; kappa_hat 2.0201; loglik -7.1445; both True lines); page_vs_twin: True.")
row("lab-twins-isolated", "each project twin runs alone under python -I -W error", "tests/labs/E3/lab-E3-project-1..3.py", "PASS",
    "Lab 1, 2 and 3 twins each exit 0 under python -I -W error with no stderr (/tmp/e3d-r15-num/lab*.out).")
row("lab-page-code-equals-twin", "page data-run code equals twin", "project.html data-run blocks", "PASS",
    "page_vs_twin_project.py: lab 1 code == twin True (83 lines); lab 3 code == twin True (213 lines); lab 2 differs only in the two blanks ___ that the completion problem removes (diff: twin 'return -math.log1p(...)' vs page '___').")
row("lab1-prose-numbers", "Lab 1 prose numbers (Rung 1 and the Lab 1 hypothesis)", "project.html:53-75", "PASS",
    CARRY + "the Lab 1 block and its hypothesis are unchanged by the delta (the hunks start at line 210); the twin output prints the stated values, checked by run_labs.")
row("lab2-prose-numbers", "Lab 2 prose numbers", "project.html Lab 2 (lines 151-200)", "PASS",
    CARRY + "Lab 2 block unchanged; run_labs PASS.")
row("lab3-prose-numbers", "Lab 3 prose numbers: estimates, SEs, 11 of 12 mixed, lambda SE above estimate", "project.html:394-617", "PASS",
    "Re-verified: hypothesis line 398 states gamma_hat 0.6352, lambda_hat 6.1503, kappa_hat 2.0201, SEs to two decimals, 11 of 12 mixed; the twin prints 0.6352/6.1503/2.0201, se 0.32/9.59/1.86, 'mixed-sign answers: 11'; se_lambda 9.59 > lambda_hat 6.1503 (the page's claim).")
row("lab-hypothesis-claims", "Lab 3 interpretation claims about what the lab shows", "project.html:616 (Lab 3 interpretation)", "PASS",
    "Re-verified after the delta's rewrite: the twin computes central differences at step h = 1e-6 (tests/labs/E3/lab-E3-project-3.py:80) and prints 'largest score component below 1e-6: True' (line 198); the printed output has no score digit, so 'it prints no digit of the score' holds; the log-likelihood -7.1445 is the printed value at the estimate.")

# grader
row("grader-tolerances-vs-page", "grader tolerances match the Grading mode paragraph", "grader/test_project.py; project.html:213 Grading mode", "PASS",
    "Re-grepped the constants: half cent plus TOL 1e-6 (lines 42-43, 178, 198); 1e-9 relative for log-likelihood (450, 472, 528); 1e-7 for the reported likelihood (562, 642); 2e-5 score at steps 1e-5/1e-6 (589, 695, 969); 1e-9 absolute for the local move check (606, 653, 705); 47 of 50 within four SE (609-625); 10% SE (1187-1190). All match the page's sentences. The page-versus-grader consistency holds; see grader-local-max-in-range-fit for the reference.")
row("grader-seed49-se-docstring", "seed-49 standard error numbers in the docstring", "grader/test_project.py (test_standard_errors_match...)", "PASS",
    CARRY + "the docstring lines are unchanged; the reverse-order re-run (below) reproduces its seed-49 numbers.")
row("grader-reverse-order-docstring", "reverse-order numbers in the docstring (135.05 to 136.78; 97.67 to 98.09)", "grader/test_project.py:1187-1196", "PASS",
    "Re-run: ledgers/E3/scripts/E3-d-r14/reverse_order_se_r14.py on the pin: 'step 1e-05: forward se_lambda 135.0541, reverse 136.7795, change +1.28%'; 'step 1e-06: 97.6747 -> 98.0856, +0.42%'. Docstring: 135.05, 136.78, +1.3%; 97.67, 98.09, +0.4%. Match.")
row("grader-all-A-docstring", "all-A (pure) twelve-response docstring", "grader/test_project.py (B-side and A-side tests)", "PASS",
    CARRY + "the docstrings of the two B-side tests are unchanged; estimates re-run for the B-side set (0.1174).")
row("grader-fixed26-b-side-numbers", "fixed 26-response and B-side fixture estimates", "grader/test_project.py:982-1008; ledgers/E3/equivalent/README.md", "PASS",
    "Re-run with the pinned reference via the test's own fixtures: FIXED_26 gamma_hat 0.6534 and B-side set gamma_hat 0.1174, both tests pass.")
row("grader-low-kappa-seed30", "seed-30 fixture has kappa below 1", "grader/test_project.py:36; project.html Grading mode", "PASS",
    "Re-run: make_instance(30) estimate gamma_hat 0.5190, lambda_hat 1.4738, kappa_hat 0.8973 (below 1).")
row("grader-large-lambda-seed49", "seed-49 fixture has lambda above 10", "grader/test_project.py:37; project.html Grading mode", "PASS",
    "Re-run: make_instance(49) estimate gamma_hat 0.7063, lambda_hat 20.6864 (above 10), kappa_hat 2.2797.")
row("grader-stall-seed108", "seed-108 fixture: the search stops without a stationary point", "grader/test_project.py:38, 1010-1020; project.html Grading mode", "PASS",
    "Re-run: test_a_search_that_stops_without_a_stationary_point_is_not_returned_as_the_estimate passes on the reference (the reference raises on this participant; the test does not penalise the error). Scan: seed 108 own participant raises 'no damped Newton step raises the likelihood' (" + f"{V_REL}/estimates_800.out" + ").")
row("grader-recovery-47", "recovery check: 47 of 50 seeds within four SE", "grader/test_project.py:609-625", "PASS",
    "The changed try/except (lines 614-618) cannot trigger on seeds 0-49: estimates_800.out lists no own-participant failure below seed 108. Suite passes on all 50 seeds (run_graders PASS).")
row("grader-exception-table", "exception table: named exception types and messages", "grader/test_project.py (must_raise); project.html:228 exception table", "PASS",
    CARRY + "the must_raise tests and the exception table (lines 228-243) are unchanged.")
row("grader-messages-no-answer", "error messages do not reveal answers", "grader/test_project.py expect() and must_raise()", "PASS",
    CARRY + "the helper functions are unchanged; the suite passes on seeds 0-49.")
row("grader-no-network-no-print", "no network, no print, no warnings", "grader/test_project.py:1342-1392; project.html Constraints", "PASS",
    CARRY + "the test bodies at these lines are unchanged (the delta's test hunks are at 281 and 614).")
row("grader-instances-sample-20", "instance.py rejects draws that break the stated guards", "grader/instance.py", "PASS",
    "instance.py is byte-identical to 1431aa1d (not in the delta); its guards (_clear_of_half_cent at line 102, the 1e-6 margin at line 45) are the ones the README cites.")
row("grader-dual-mode", "both modes apply; count and mode statements", "grader/test_project.py; project.html:213 and Grading mode", "PASS",
    "project.html:213 'Both modes apply ... runs 52 checks' matches the collect count (52).")
row("grader-own-mutants-r14d", "verifier mutants r14d_01..04 are killed", "ledgers/E3/mutants/r14d_01..04", "PASS" if all(m.get("killed_by") for m in mut if m["id"].startswith("r14d")) else "FAIL",
    "Killed status per mutant in the mutants list (mutate_E3_0-9.out).",
    fix="Restore the grader kill for the surviving r14d mutant(s), or record them as equivalent with a proof.")

# alternatives
alts = json.loads((V / "alt_summary.json").read_text(encoding="utf-8")) if (V / "alt_summary.json").exists() else {}
for k in range(1, 6):
    key = f"alt_v{k}"
    row(f"alt-v{k}-seeds-0-9", f"verifier alternative {key} passes the suite on seeds 0-9", f"ledgers/E3/scripts/E3-d-r14/alts/alt_v{k}/elicit.py", "PASS",
        f"{V_REL}/alternatives_seeds_0-9.raw: {key} seeds 0..9 each 'EXIT=0 52 passed' (10 of 10).")

# claims that changed in the delta
row("crra-exact-half-tie-rule", "CRRA gamma != 0 exact tie may come out either way; grader accepts either; half-up elsewhere",
    "project.html Whole cents and Grading mode; grader/test_project.py:284-296; grader/reference.py:72-74, 125-126", "PASS",
    "Re-derived: wealth 1, prizes 97 and 391, p = 1/2: E sqrt = (7+14)sqrt2/2, sure final wealth 220.5, CE 219.5 (hand derivation: sqrt(98) = 7 sqrt2 and sqrt(392) = 14 sqrt2, so the expected root is 21 sqrt2 / 2, the sure wealth is 220.5 and the CE is 219.5). The reference returns 219 (raw float 219.49999999999997); the test accepts {219, 220}. Under the CRRA risky-lottery check the page states a half-cent slack, which also accepts either neighbour. The gamma = 0 test (line 266-281) still requires 3 for [2, 3] at a half cent. Scope note (LOW): the Grading mode names the gamma = 1/2 tie only, while Whole cents says any gamma != 0 tie; the slack covers the rest.")
row("equiv-stall-e12_03", "e12_03 deleted with a README line; stall branch unreachable on the suite's inputs",
    "ledgers/E3/equivalent/README.md section 'Removed: e12_03'; grader/reference.py:321-334", "PASS",
    f"{V_REL}/stall_branch_probe.out: 'TOTAL 800 STALL_BRANCH_HITS 0 RUNS_WITH_HIT 0' for own and second participants of seeds 0-399; the eight raising runs raise the other two messages (RAISED list). e12_03 is absent from equivalent/; git records it as renamed to ledgers/E3/mutants/r14d_02 with changed content (97% similar), and r14d_02 is a different student error (the CRRA log case), so the e12_03 deletion stands (LOW: the README does not mention the rename). Ruling 28 asserts the branch is dead; the verifier's evidence is that no tested input reaches it (not a proof of unreachability).")
row("rubric-descriptors-observable", "rubric C1 level 4, C1 level 3 and C5 levels 4, 3, 2, 1 are observable",
    "project.html rubric table (data-criterion C1 and C5)", "PASS",
    "Read the cells: C1 4 (lists every pair, cents, exact probabilities, mixed-sign pairs), C1 3 (count >= 12, unit cents, reason for gains and losses, >= 2 example lotteries), C1 2 (unit dollars or cents, reason for losses, no example lottery), C1 1 (no count, no unit, no lottery). C5 4 (every result carries a grade and a key or a derivation), C5 3, C5 2, C5 1 each name a checkable condition (grade, hypothesis mark, registry key, Lab 3 basis). No cell uses an undefined term. Calibration against the exemplars is in exemplar-blind-calibration.")
row("exemplar-A-annotations", "Exemplar A data-scores 2,2,1,2,1 and annotations", "project.html:653-700 (exemplar-a)", "PASS",
    "Blind scorer (ledgers and ~/.fanout/blind/E3-d-fresh.json, the dedicated scorer of ruling 23): A C1 2, C2 2, C3 1, C4 2, C5 1 = official 2,2,1,2,1. Annotations match the rubric cells (LOW wording: C1 level 3 annotation says 'no example pair' where the cell says 'example lotteries'; not a count error).")
row("exemplar-B-annotations", "Exemplar B official scores 3,3,4,3,3 and annotations", "project.html:713 exemplar-b C1 annotation", "FAIL",
    "The C1 level-3 annotation reads: 'two example lotteries with cents and exact probabilities (lottery A of pair 0, and both lotteries of pair 3)'. That parenthesis names three lotteries (pair 0 lottery A; pair 3 lotteries A and B). The blind scorer scored the three-lottery reading (blind file B C1 descriptor: 'pair 0's lottery A ...; pair 3's two lotteries'). Wrong count in a calibration annotation (ruling 26 'wrong number').",
    fix="Change 'two example lotteries' to 'three example lotteries' (or 'at least two example lotteries') in the exemplar-b C1 annotation at line 713.")
row("exemplar-word-counts", "exemplar memo word counts stated on the page", "project.html:648 ('the memo text of Exemplar A is 117 words and that of Exemplar B is 456 words')", "FAIL",
    f"ledgers/E3/scripts/E3-d-r14/wordcount_exemplars.py (the base's script) on 1431aa1d: Exemplar B memo 456 words; on dde0486b: 459 words (+3 from the Evidence paragraph's 'and the log-likelihood value'). Exemplar A 117 on both. The page still says 456.",
    fix="Change '456 words' to '459 words' at project.html:648 (re-run wordcount_exemplars.py to confirm; the count moves again if the Evidence paragraph changes).")
row("exemplar-blind-calibration", "dedicated blind scorer (ruling 23) on both exemplars against the official scores",
    "~/.fanout/blind/E3-d-fresh.json; project.html rubric and exemplars", "PASS",
    "Blind result (scorer never opened the page; ruling 23): A = C1 2, C2 2, C3 1, C4 2, C5 1 (official 2,2,1,2,1); B = C1 3, C2 3, C3 4, C4 3, C5 1 strict (official 3,3,4,3,3). The one B mismatch was C5: strict reading gave 1 because the log-likelihood -7.1445 was not in the Evidence paragraph's grading list. The fix is in the memo (project.html:756 now lists 'the log-likelihood value above') and the C5 level-3 annotation (line 760). On my reading of the fixed memo the strict C5 is 3, the lenient reading's value. Caveat: the blind scorer did not re-score after the fix; this PASS rests on the blind run plus the fix text, as the round's instruction states.")
row("exemplar-B-data-claims", "Exemplar B data claims: prize range, prizes per lottery, mixed count, pairs 0 and 3", "project.html exemplar-b Instrument paragraph", "PASS",
    "ledgers/E3/scripts/E3-d-r14/exemplar_b_data_check_r14.py on tests/labs/E3/lab-E3-project-3.py: 'min prize -18700 max prize 19000 prizes per lottery [2, 3] mixed pairs 11'; pair 0 A [6200, -15100] (9/10, 1/10), B has three prizes; pair 3 A [18800, -12500] (3/4, 1/4) vs B [16500, -17700] (2/5, 3/5), both mixed. All match.")
row("hours-arithmetic", "hours table sums to the header and the hub", "project.html #hours; course/modules/E/E3/index.html data-hours-project", "PASS",
    "Re-summed the hours table: 1+1+3+4+3+2 = 14; data-hours-project=\"14\" on project.html and index.html; the hub's 14 of 70 unchanged.")
row("structure-sections", "section structure and ids", "course/modules/E/E3/project.html", "PASS",
    "check_pages PASS; the delta changes text inside existing elements (hunks at lines 210-753); no section or id added or removed.")
row("ladder-rungs", "ladder rungs and their text", "project.html:40-49", "PASS",
    CARRY + "lines 40-49 are unchanged (first hunk at 210).")
row("notation", "symbols vs notation and the page's own use", "project.html math", "PASS",
    "Re-checked: the delta adds \\(\\hat\\gamma\\) (the curvature estimate, the same meaning as \\hat\\lambda in exemplar B) and \\(\\gamma \\ne 0\\), with no reuse of an E3 symbol with another meaning. The ruling-29 symbols (tau, eta, tilde u, epsilon, psi) do not occur in project.html (grep). notation/notation.json holds only the registered cross-unit symbols.")
row("process-words", "no process words in learner text", "project.html", "PASS",
    "grep of the page for ruling, round, ledger, verifier, builder, fixer, architect, mutant, equivalent: no process-word hits (only 'certainty equivalent'). The delta adds no process word.")
row("banned-phrases", "banned phrases (check_pages BANNED)", "project.html", "PASS",
    "check_pages PASS (it applies the BANNED list to visible prose).")
row("concept-links-dag", "concept links and the DAG", "project.html concept links; check_dag", "PASS",
    f"check_dag PASS ({V_REL}/check_dag.out); the delta adds no concept link.")
row("reading-keys-and-attribution", "reading section keys and attribution", "project.html Reading section", "PASS",
    CARRY + "the Reading section and its attribution sentence are unchanged.")
row("cross-lesson-definitions", "cross-lesson definitions cited on the page", "project.html Rung 1 and Conventions", "PASS",
    "The new Whole cents and Estimation sentences cite no lesson definition; the lesson references in Rung 1 are unchanged.")
row("figures", "figures and their sweeps", "project.html", "PASS",
    "page_smoke PASS for project (figure sweeps run unless skipped; not skipped).")
row("lab-page-claims-about-engine", "Autograder, Running the suite locally, footer claims about the engine", "project.html Autograder and Running the suite locally", "PASS",
    "Re-read: the local run command and '-W error' statement are unchanged; the only count statement (52 checks) matches the collect count.")

# equivalent-mutant ledger and gamma-clamp mutants
row("equiv-tie-mutants-proof", "README proof that f05, m06, r13n01, w05 are equivalent (rulings 9 and 27)",
    "ledgers/E3/equivalent/README.md sections 'Tie-rule mutants' items 1-4 and the Change column; the four files",
    "FAIL",
    "The proof's central sentences are false in exact arithmetic on floats. Item 1 says the mutant and the reference 'differ only when y is exactly k + 1/2', and that 'every output is a nearest whole cent' (|y - n| <= 1/2). Counterexamples (ledgers/E3/scripts/E3-d-r15/verifier/halfs.py and nearest.py): y = 0.49999999999999994: reference floor(y+1/2) = 1 (|y-1| > 1/2, not nearest); f05 ceil(y-1/2) = 0. y = -0.49999999999999994: f05 and w05 return -1 (|y+1| > 1/2), reference returns 0. So the difference set includes float neighbours of halves, not only exact halves (halfs.py over k + 1/2 for k in -300..299 and their 3 ulp neighbours: f05 differs at all 600 exact halves, m06, r13n01 and w05 at 300 each, and each has at least one float neighbour outside the exact halves). Also, the four files are stale copies: each still contains the removed stall-branch raise ('the step became negligible before the score did'), so they do not 'differ only in _half_up' as the README's section header says. Item 3's 'differs only on an exact tie' is false for the same reason.",
    fix="Restate the difference set: the four mutants differ from the reference on exact halves and on floats within a few ulps of a half (give the two examples above). Decide the float policy: make the reference's _half_up exact (floor(Fraction(y) + 1/2)) so 'nearest' is literal, then re-derive which mutants remain equivalent (f05 and w05 would then violate nearest at -0.49999999999999994 and become student errors needing a fixture). Regenerate the four files from the current reference so that only _half_up differs, and state that the README's equivalence claim is about the page's stated scope.")
row("equiv-gamma-clamp-floor", "ruling 28 (gamma clamps): r11_03 and r12d_03 stay in equivalent/ only if the reference does not converge outside [0.001, 0.999]",
    "ledgers/E3/equivalent/README.md 'Gamma-clamp mutants' and the Estimation convention in project.html", "FAIL",
    f"Ruling 28 (plans/FINAL-ARCHITECT-RULINGS.md item 28): if the reference converges with gamma_hat below 0.001 or above 0.999 'mutants r11_03 and r12d_03 return to mutants/ and are killed'. The reference DOES converge below 0.001: {V_REL}/gamma_scan_low_2000_r15.txt (the builder's file, parsed by the verifier: 85 converged fits, min gamma_hat 7.23e-13, max 8.59e-4). The README's own text says so. Its reason for not restoring them is that these sit at the domain edge, which the instance guard rejects; that is not the ruling's condition. High side: the README's bold claim 'No converged fit lies above 0.999' is a universal claim the probes do not prove (4000 random trials, 480 targeted, 576 survey: none found); it should read 'none found in N trials'. Also the two files are stale copies (they still contain the removed stall raise, so they differ from the reference in that branch too), and the README's 'differs only' statements are therefore not exact (message text only). Evidence the clamp at 0.99 is a real gap (row grader-gamma-0.99-clamp-survivor) also concerns the same mutant family.",
    fix="Either (a) build a fixture below 0.001 (e.g. from the 85 converged fits), add a local-maximum and reported-likelihood test, return r12d_03 to mutants/ and confirm it is killed, then keep r11_03 in equivalent/ only if the high side is shown empty by the probes with the word 'none found'; or (b) obtain an architect amendment to ruling 28 that accepts the edge-of-domain exception in writing. Replace 'No converged fit lies above 0.999' with 'No converged fit above 0.999 was found in N trials'. Regenerate both files from the current reference.")
row("grader-gamma-0.99-clamp-survivor", "a grader mutant that clamps the reported curvature at 0.99 (inside the stated range) must be killed",
    "ledgers/E3/mutants/v15d_03_reported_gamma_clamped_at_0_99.py; grader/test_project.py; project.html Estimation convention and Grading mode", "FAIL",
    f"The mutant survives the official suite on seeds 0-9 (52 passed on each of 10 seeds: {V_REL}/new_mutants_seeds_0-9.raw). The page states the supported range [0.001, 0.999] (Estimation convention) and that the Grading mode's checks, including the local maximum check ('This is the local maximum check that the page states'), apply to estimates in that range. The mutant changes the reported gamma for fits in (0.99, 0.999), which the page's range covers. No suite participant reaches it (the 800 own and second participants of seeds 0-399 have gamma_hat between 0.0249 and 0.9864), so the survival is not a page-stated exception.",
    fix="Add a fixture with gamma_hat inside (0.99, 0.999): ledgers/E3/scripts/E3-d-r15/verifier/high_side_check.py finds sim_pinned.sim(seed=2, gamma=0.99, lambda=1.0, kappa=20.0, n=26) with gamma_hat 0.994442, lambda_hat 0.511, kappa_hat 1921 (converged, non-degenerate). The grader's own _assert_estimate_is_a_maximum rejects the clamped mutant on that fit (reported likelihood mismatch) and rejects the reference too (next row). Fix the reference first, then add the fixture to the suite so the mutant dies.")
row("grader-local-max-in-range-fit", "the reference estimate on an in-range fit satisfies the page's local-maximum check",
    "grader/reference.py (_maximise stopping rule, lines 284-336); grader/test_project.py _assert_estimate_is_a_maximum and the 1e-9 move check (lines 594-606)", "FAIL",
    "On the in-range fit sim_pinned.sim(2, 0.99, 1.0, 20.0, 26) (gamma_hat 0.994442, in [0.001, 0.999]) the reference's estimate fails the page's local-maximum check: moving gamma up by 0.1% raises the log-likelihood by 2.74e-9, above the 1e-9 bound the page states ('requires that no move raise the log-likelihood by more than 1e-9'). The gradient there is 7.9e-8 (below the page's 2e-5 score bound), so the search stopped on a very flat direction. The test helper reports 'a nearby parameter has a higher likelihood: the estimate is not the maximum'. Measured with ledgers/E3/scripts/E3-d-r15/verifier/high_side_check.py and an inline check of _objective. The suite's own participants never reach this region (their gamma_hat is at most 0.9864), so no grader run shows it.",
    fix="Either refine the reference's search along gamma until no 0.1% move raises the likelihood by more than the stated bound (and re-run the 800-participant scan and the eight-seed list, which must not change), or state the bound relatively (scale by max(1, |L|)) and document the flat-direction limit in the Grading mode, or narrow the stated range so that the fit lies outside it. Whichever route, the page's range statement and the reference must agree.")

# ---- assemble ----------------------------------------------------------------------------------------------------
fails = [r for r in R if r["status"] != "PASS"]
counts = {s: sum(1 for r in R if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if not fails and all(m.get("killed_by") for m in mut) else "FAIL"
fragment = {
    "unit": "E3",
    "slice": "d",
    "round": 15,
    "verifier": "Claude Haiku 5.5, independent delta verifier for E3-d, round 15 (did not build E3; read verifier-rules.md, VERIFIER_RULES.md, plans/FINAL-ARCHITECT-RULINGS.md rulings 23, 25-30, the round-14 fragment)",
    "pin": PIN,
    "base": "1431aa1d842a5d2d05fd5953c098500bf78a4307 (round-14 fragment /Users/billyribeiro/.fanout/frags/D-E3-d.round14.json, verdict FAIL). Delta 1431aa1d..dde0486b read for project.html (22 changed lines in 8 hunks), grader/reference.py (5), grader/test_project.py (18), ledgers/E3/equivalent/README.md (106), mutants (r14d_01/03/04 added, e12_03 moved to mutants as r14d_02); tests/labs/E3/lab-E3-project-*.py unchanged in the delta.",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyD15-E3-d",
    "scratch": "/tmp/e3d-r15-* and /var/folders/.../T/grader-E3-* (removed by the tools)",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": R,
    "mutants": mut,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": "",
    "summary": "",
}
fragment["summary"] = (f"E3-d round 15 at {PIN[:8]}: {len(R)} rows: {counts['PASS']} PASS, {counts['FAIL']} FAIL, "
                       f"{counts['UNVERIFIABLE']} UNVERIFIABLE. Mutants listed: {len(mut)}, killed {killed_total}.")
out = ROOT / "ledgers/E3/E3-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(fragment["summary"])
print("FAIL rows:", [r["id"] for r in fails])
print("wrote", out)
