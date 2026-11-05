"""Writes ledgers/BK4/BK4-c.json (round 8) from the outputs in ledgers/BK4/scripts/BK4-c-r8/out/. Run from the checkout root."""
from __future__ import annotations

import datetime
import json
import pathlib
import re

ROOT = pathlib.Path.cwd()
OUT = "ledgers/BK4/scripts/BK4-c-r8/out"
MUT_OUT = (ROOT / OUT / "mutate_seeds0-9_all.out").read_text(encoding="utf-8").splitlines()

mutants = []
for line in MUT_OUT:
    m = re.match(r"^KILLED (\S+?): (.*) -> (\S+) \(seed (\d+)\)$", line)
    if m:
        name, desc, test, seed = m.groups()
        mutants.append({
            "id": name,
            "file": f"ledgers/BK4/mutants/{name}",
            "description": desc,
            "killed_by": f"{test} (seed {seed})",
            "seeds": "0-9",
        })
assert len(mutants) == 58, len(mutants)

PRE = "Round 8 re-run: "
R8 = "ledgers/BK4/scripts/BK4-c-r8"

def row(i, check, location, status, evidence, fix=""):
    r = {"id": i, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != "PASS":
        r["fix"] = fix
    return r

rows = [
    row("proj-lab1-numbers", "2.5-labs", "course/modules/BK/BK4/project.html:56-139; tests/labs/BK4/lab-BK4-project-1.py", "PASS",
        PRE + f"run_labs --unit BK4 PASS ({OUT}/run_labs_bk4.out); twin alone 'python -I -W error' exit 0, empty stderr, page code == twin, expected == output ({OUT}/twin_vs_page_r8.out). Every printed and hypothesis number (50000/6000/20000, residual 4000, shares 1333/1666/1000 and leftover 1, 1334/1666/1000, index 39 from 38.2, margin 117088, covers 9750 and 9500) re-derived with Fraction in {R8}/rederive_r8.py ({OUT}/rederive_r8.out)."),
    row("proj-lab2-numbers", "2.5-labs", "course/modules/BK/BK4/project.html:141-190; tests/labs/BK4/lab-BK4-project-2.py", "PASS",
        PRE + f"Line-by-line comparison: 42 lines each; only page lines 25 and 38 differ from the twin and both contain ___ (twin_vs_page_r8.py, {OUT}/twin_vs_page_r8.out). Twin output equals expected block (survivor shares 1334/1666/1000, index 39, margin 117088). Hypothesis numbers re-derived ({OUT}/rederive_r8.out)."),
    row("proj-lab3-numbers", "2.5-labs", "course/modules/BK/BK4/project.html:252-366; tests/labs/BK4/lab-BK4-project-3.py", "PASS",
        PRE + f"Twin output equals expected block (5 waterfall rows, sizing 9000/9500/9750 -> margins 105154/111074/117088, covers 9000/9500/9750, one-cent-below 8750/9250/9500, brute force agrees, Part C counts 2/2/0/0 at 9500 and 4/2/0/0 at 9000). Every value re-derived with Fraction and an independent sort in {OUT}/rederive_r8.out; largest seeded loss 118151 re-derived."),
    row("proj-fixture-tables", "2.6-spec, 2.6-tests", "course/modules/BK/BK4/project.html:229-250; course/modules/BK/BK4/grader/test_project.py:281-368", "PASS",
        PRE + f"All 11 layer-order rows (losses 80..300), the 3 remainder cases (1, 2, 4 cents) and the 6 sizing/cover fixture values re-derived by an independent waterfall and order-statistic oracle ({OUT}/rederive_r8.out, 'fixture row' and 'remainder' lines). Each row has an isolated test in test_project.py (test_fixture_loss_80 .. test_fixture_loss_300, test_remainder_*, test_fixture_five_losses_*, test_cover_* ); 86 tests pass on the reference (proj-grader-reference-run)."),
    row("proj-named-conditions", "2.6-spec, 2.6-tests, 2.6-failure-messages", "course/modules/BK/BK4/project.html:201, :203-212; course/modules/BK/BK4/grader/test_project.py:867-1000", "PASS",
        PRE + "The page names six refusal conditions (Constraints list, project.html:203-212): margin_for_cover empty, target outside 1..10000, margin_for_cover/cover_bps negative loss, cover_bps empty, waterfall negative amount or loss, waterfall defaulter not a member. Each has a must_refuse test with the naming check, and each boundary (target 1 and 10000; zero loss; zero margin/fund/capital; defaulter at lowest and highest id) has a must_accept test. Refusal-by-refusal print silence is tested (test_refused_inputs_print_nothing_before_they_raise)."),
    row("proj-conventions-prose", "2.9-prose, 2.6-mathematics", "course/modules/BK/BK4/project.html:219-224; course/modules/BK/BK4/grader/reference.py:36-109", "PASS",
        PRE + "Layer order, survivor pro rata with leftover by ascending id among DF>0, conservation, cover floor and sizing ceiling index in project.html:219-224 match reference.py lines 57-100 exactly; reference passes 50/50 seeds (run_graders_0-49.out). Alternatives 1-5 implement the same rules and pass (alternatives_reference_starter_0-49.out)."),
    row("proj-hours", "2.9-structure, hours", "course/modules/BK/BK4/project.html:34, :373-386 (table#hours); course/modules/BK/BK4/index.html:29, :39, :42", "PASS",
        PRE + "Component hours 2+2+3+3+2+2+1 = 15 = data-hours-project = eyebrow '15 hours'. Hub 35 + 15 = 50, 15/50 = 30 %. Independent estimate: Rung 1 about 2 h, Rung 2 about 1.5-2 h, waterfall with 11 fixtures and refusals about 3-4 h, sizing and cover about 2-3 h, the 86-test suite run and edge cases 2-3 h, memo 2-3 h, self-assessment 1 h: total 14-18 h, within 30 % of 15 h."),
    row("proj-grader-reference-run", "2.6-autograder 1", "course/modules/BK/BK4/grader/reference.py; course/modules/BK/BK4/grader/test_project.py", "PASS",
        PRE + f"run_graders --unit BK4 --seeds 0-49: PASS, reference 50/50 seeds, slowest 0.3 s ({OUT}/run_graders_0-49.out). Local command of the page run in a scratch copy: 86 passed, QF_SEED=0 ({OUT}/reference_local_cmd_seed0.out); QF_SEED=7 also 86 passed."),
    row("proj-grader-starter-fails", "2.6-autograder, 2.6-failure-messages", "course/modules/BK/BK4/grader/starter.py; course/modules/BK/BK4/grader/test_project.py:1091-1114", "PASS",
        PRE + f"starter.py on seeds 0-49: 0/50 seeds pass; every failure is a named pytest.fail with 'has no implementation for <name>', no traceback ({OUT}/alternatives_reference_starter_0-49.out, starter line)."),
    row("proj-collect-count", "2.6-count", "course/modules/BK/BK4/project.html:201 (no), :214; course/modules/BK/BK4/grader/test_project.py", "PASS",
        PRE + f"pytest --collect-only in a scratch copy: '86 tests collected' ({OUT}/collect_only_scratch.out); page line 214 says 86 checks. Matches."),
    row("proj-instances", "2.6-autograder 2, 2.8-data", "course/modules/BK/BK4/grader/instance.py:22-50", "PASS",
        PRE + f"instance_check_r8.py ({OUT}/instance_check_r8.out): all 50 seeds 0-49 valid (N 4..6, ids 1..N, IM>=0, DF>=1, K>=0, defaulter a member, S 40..80, integer losses, target in {{9000,9500,9750}}); each case has a loss inside the margin, inside the fund and past every layer; 50 distinct sizing answers; 49 seeds differ from seed 0; 20 seeds sampled with random.Random(20261104) printed in full."),
    row("proj-mutants-builder", "2.6-mutants", "ledgers/BK4/mutants/m01_fund_before_margin.py .. m10_seed0_hardcoded.py", "PASS",
        PRE + f"mutate_graders --unit BK4 --seeds 0-9: all 10 plan mutants KILLED ({OUT}/mutate_seeds0-9_all.out)."),
    row("proj-mutants-own", "2.6-mutants", "ledgers/BK4/mutants/ (r3a..r5f, vc01..vc15, n1..n4)", "PASS",
        PRE + f"The 38 non-plan, non-round-7 mutants (r3a..r3f, r4a..r4h, r5a..r5f = 20; vc01..vc15 with 14 files present = 14; n1..n4 = 4) are all KILLED on seeds 0-9 in {OUT}/mutate_seeds0-9_all.out (mutate exit 0)."),
    row("proj-mutants-round7", "2.6-mutants", "ledgers/BK4/mutants/s01..s05 (written by ledgers/BK4/scripts/BK4-c-r7/make_r7_mutants.py)", "PASS",
        PRE + f"s01..s05 KILLED on seeds 0-9 ({OUT}/mutate_seeds0-9_all.out)."),
    row("proj-mutants-round8", "2.6-mutants", "ledgers/BK4/mutants/t8a..t8e (written by ledgers/BK4/scripts/BK4-c-r8/make_r8_mutants.py)", "PASS",
        PRE + f"Five new student-error mutants, each one line from reference.py, each KILLED: t8a half-up survivor shares (killed by the conservation test), t8b ceiling cover (one-of-three floored test), t8c descending sort in the sizing (order-statistic test), t8d capital charged on loss after margin only (oracle test), t8e waterfall pops the defaulter from the caller's dict (purity test). Mutation run: 58/58 killed ({OUT}/mutate_seeds0-9_all.out)."),
    row("proj-large-cent-claim", "2.6-autograder, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
        PRE + f"The test's expected shares 6055950114045320 and 529746839784068 re-derived: floors 6055950114045319 and 529746839784068, leftover 1 to member 1 (ascending id, DF>0), sum equals the residual 6585696953829388; R*DF_1 > 2**53 true ({OUT}/rederive_r8.out, 'large-cent' lines)."),
    row("proj-mutant-float", "2.6-mutants", "ledgers/BK4/mutants/vc10_float_arithmetic.py; course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
        PRE + f"vc10 KILLED ({OUT}/mutate_seeds0-9_all.out)."),
    row("proj-mutant-argument", "2.6-mutants", "ledgers/BK4/mutants/r4f_sizing_sorts_caller_list_in_place.py; course/modules/BK/BK4/project.html:203; course/modules/BK/BK4/grader/test_project.py:1062-1068", "PASS",
        PRE + f"r4f KILLED ({OUT}/mutate_seeds0-9_all.out); the argument rule on project.html:203 is tested by test_margin_for_cover_and_cover_bps_do_not_change_their_list_argument and test_waterfall_does_not_change_its_arguments (t8e KILLED by the latter)."),
    row("proj-labs-simulated-stdlib", "2.8-data, 2.5-labs", "tests/labs/BK4/lab-BK4-project-1..3.py; course/modules/BK/BK4/project.html:54", "PASS",
        PRE + "All three labs use random.Random(1) (seeded), import only random, read no file and open no network; each is labelled SIMULATED in its docstring and on project.html:54. Twin runs: exit 0, empty stderr, under python -I -W error."),
    row("proj-page-smoke", "2.9-smoke", "course/modules/BK/BK4/project.html", "PASS",
        PRE + f"page_smoke --unit BK4 --pages project: PASS, including the in-browser grader (86 tests pass) and labs ({OUT}/page_smoke_project.out)."),
    row("proj-check-tools", "2.9-structure, 2.6-ladder", "course/modules/BK/BK4/project.html", "PASS",
        PRE + f"check_projects --unit BK4: PASS ({OUT}/check_projects.out). check_pages --unit BK4: PASS ({OUT}/check_pages_unit.out). check_dag --unit BK4: PASS ({OUT}/check_dag.out)."),
    row("proj-ruff", "2.9-tooling", "tests/labs/BK4; course/modules/BK/BK4/grader", "PASS",
        PRE + f"ruff check on the slice: all checks passed ({OUT}/ruff_check_slice.out); ruff format --check: 12 files already formatted ({OUT}/ruff_format_slice.out)."),
    row("proj-mypy-repo", "2.9-tooling", "pyproject.toml [tool.mypy]", "PASS",
        PRE + f"mypy --no-incremental over the repository: Success, no issues in 385 source files ({OUT}/mypy_repo.out)."),
    row("proj-mypy-plan-command", "2.9-tooling", "course/modules/BK/BK4/grader/test_project.py:28, :30", "PASS",
        PRE + f".venv/bin/mypy --no-incremental tests/labs/BK4 course/modules/BK/BK4/grader: no issues in 12 files ({OUT}/mypy_slice_plan_cmd.out)."),
    row("proj-pytest-labs", "2.5-labs", "tests/test_labs.py; tests/test_run_labs.py", "PASS",
        PRE + f"pytest tests/test_labs.py tests/test_run_labs.py: exit 0 ({OUT}/pytest_labs_slice.out)."),
    row("proj-refs", "2.1-citations", "course/modules/BK/BK4/project.html:501-506 (reading list); references/references.json:2853 (bisndcpmi), :7411 (duffie2011central)", "PASS",
        PRE + f"verify_refs --offline: 560 entries, 0 problems ({OUT}/verify_refs_offline.out). Live, plain curl: Crossref api.crossref.org/works/10.1093/rapstu/rar001 returns title 'Does a Central Clearing Counterparty Reduce Counterparty Risk?', Duffie and Zhu, Review of Asset Pricing Studies, 2011 (matches duffie2011central) ({OUT}/crossref_duffie_r8.json). Plain curl https://www.bis.org/committees/cpmi/publications: HTTP 200, title 'CPMI publications | Bank for International Settlements' (matches bisndcpmi) ({OUT}/curl_bisndcpmi_r8.html). The page attributes no statement to either (project.html:501-506)."),
    row("proj-banned-and-process-words", "2.9-prose", "course/modules/BK/BK4/project.html; grader/*.py; tests/labs/BK4/lab-BK4-project-*.py", "PASS",
        PRE + f"check_pages banned-string check PASS (out/check_pages_unit.out). Visible-text scan of project.html for process words (verifier, builder, batch, agent, round, ledger, TODO, pending, plan, architect, Haiku, Claude, slice, ...): zero hits ({OUT}/prose_scan_r8.out)."),
    row("proj-anchors-links", "2.9-structure", "course/modules/BK/BK4/project.html", "PASS",
        PRE + "Every href='#...' resolves to an id on the page; linked files (L05.html, index.html, index.html#placement, grader/test_project.py, grader/instance.py, grader/starter.py, ../../../review.html) exist."),
    row("proj-dag-concepts", "2.9-DAG", "course/modules/BK/BK4/project.html", "PASS",
        PRE + "The project page has zero <dfn> and zero concept links (grep), so no concept is used by link outside the closure. Lesson 3 is referenced by name (project.html:223) and is in the same module (check_dag PASS)."),
    row("proj-rung-ladder", "2.6-ladder", "course/modules/BK/BK4/project.html:41-50, :193-216, :490-497", "PASS",
        PRE + "Four rungs in order (worked example, completion, independent project, stretch); rung 2 is class 'lab completion' with two blanks and an instant check; rung 4 is ungraded and open-ended (stretch bullets). Tier U full-length rungs 1-2. check_projects PASS."),
    row("proj-exemplar-a-calibration", "2.7-rubric-calibration", "course/modules/BK/BK4/project.html:424-453 (exemplar A), :408-417 (rubric table#rubric)", "PASS",
        PRE + f"Blind scoring (memo text only, annotations, verdict and data-scores removed by blind_memo_text.py, {OUT}/blind_memo_text_r8.out), scored by the rubric descriptors before the annotations were read: C1 2, C2 2, C3 1, C4 2, C5 2. Official data-scores 2,2,1,2,2; annotations read afterwards. Within one level on every criterion (exact match)."),
    row("proj-exemplar-b-calibration", "2.7-rubric-calibration", "course/modules/BK/BK4/project.html:455-481 (exemplar B), :457 (official scoring)", "PASS",
        PRE + f"Blind scoring of exemplar B memo text ({OUT}/blind_memo_text_r8.out) before reading annotations: C1 4 (all layers, cents for 80000, 'used only after the one before'), C2 4 (9500, k 38 from exact 38.0, 38th loss, cover 9500 and 9250 one cent below), C3 4 (pro rata and leftover rules, 1334+1666+1000=4000), C4 4 (margin 111074 with cover, count 0, alternative 9000), C5 4 (all four limits, no B/C claim). Official 4,4,4,4,4. Exact match."),
    row("proj-exemplar-b-numbers", "2.2-numbers, 2.3-grades", "course/modules/BK/BK4/project.html:404 (memo rule), :422, :457 (disclosure), :459-470", "PASS",
        PRE + f"Every number in exemplar B re-derived: pool 12000, residual 4000, shares 1333/1666/1000 and 1334 after leftover, exact position 38.0, k 38, margin 111074 (Lab 3 Part B/C), 9250 one cent below, 105154 and 117088, past-margin count 2 (9500) and 4 (9000), past-survivors 0, difference 5920 = 111074-105154 ({OUT}/rederive_r8.out). Grade: no B or C claim, no citation, memo rule (project.html:404) permits each number's source."),
    row("proj-rubric-c1-levels", "2.7-rubric", "course/modules/BK/BK4/project.html:412 (C1 row, data-criterion C1)", "FAIL",
        PRE + "Level descriptors are not mutually exclusive. A memo that names all four layers in order but gives no amount for any scenario matches level 2 ('Names the layers, but gives the cents for no scenario') AND level 1 ('Names fewer than two of the layers, or gives no layer amount'). Exemplar A is scored 2 by the page, so the calibration passes, but the level-1 clause is subsumed by the level-2 clause.",
        "In the C1 row, level 1 cell, delete 'or gives no layer amount' so that level 1 reads 'Names fewer than two of the layers.' Level 2 then owns every memo that names two or more layers without a scenario amount."),
    row("proj-rubric-c2-levels", "2.7-rubric", "course/modules/BK/BK4/project.html:413 (C2 row, data-criterion C2)", "FAIL",
        PRE + "Level 1 ('Gives no margin, or gives a margin with no target stated') and level 2 ('States the margin for a stated target, with no check of the cover') are ambiguous for a memo that states only a sizing rule (exemplar A: 'For a target of 9500 bps, the margin is the k-th smallest loss ...'). 'Gives no margin' can be read as 'gives no margin value', which matches level 1, while level 2 matches the rule. The page's own level for exemplar A is 2, so the calibration passes, but two descriptors fit the same memo.",
        "Make the level-1 cell say 'Gives no margin value and no sizing rule, or gives a margin with no target stated', and make the level-2 cell say 'States a margin value or sizing rule for a stated target, with no check of the cover'."),
    row("proj-rubric-c3-descriptors", "2.7-rubric", "course/modules/BK/BK4/project.html:414 (C3 row, data-criterion C3)", "FAIL",
        PRE + "Level 2 ('Gives survivor amounts, or states one of the two rules ...') and level 1 ('Names no sharing rule.') both match a memo that gives survivor amounts for a stated scenario but names no sharing rule. The page's C3 levels therefore do not give one level for that memo. Calibration of exemplar A (level 1, names no rule) still passes.",
        "Change level 1 to 'Names no sharing rule and gives no survivor amount.' so that a memo with survivor amounts but no rule falls to level 2, as the level-2 cell already says."),
    row("proj-rubric-c5-descriptor", "2.7-rubric", "course/modules/BK/BK4/project.html:416 (C5 row)", "PASS",
        PRE + "Levels 4 (all four limits named, B/C counter-evidence or none-cited statement), 3 (three limits with direction), 2 (one or two), 1 (none) are disjoint and observable. Exemplar B level 4 and exemplar A level 2 match the descriptors (blind scoring above)."),
    row("proj-rubric-c4-descriptors", "2.7-rubric", "course/modules/BK/BK4/project.html:415 (C4 row)", "PASS",
        PRE + "Levels 4..1 are disjoint: L4 cover plus count plus alternative; L3 cover plus alternative without count; L2 margin without cover; L1 no margin. Exemplar A (L2) and B (L4) match."),
    row("proj-rubric-observable-wording", "2.7-rubric", "course/modules/BK/BK4/project.html:412-416", "PASS",
        PRE + "Every descriptor names a checkable feature (a named layer, a stated number, a sum, a count, a named limit). Vague words (e.g. 'clear', 'sound') do not appear in the rubric rows (grep)."),
    row("proj-exemplar-annotations-agree", "2.7-rubric", "course/modules/BK/BK4/project.html:424-481 (aside.annotation)", "PASS",
        PRE + "Read after blind scoring: exemplar A annotations (C1 L2, C2 L2 and misses L3, C3 L1, C4 L2, C5 L2) and exemplar B annotations (all L4) agree with the official data-scores and with my blind scores."),
    row("proj-rubric-self-form", "2.7-rubric", "course/modules/BK/BK4/project.html:482-487", "PASS",
        PRE + "section.rubric-self has data-rubric='rubric', data-exemplars='exemplar-a exemplar-b', and the no-JS notice names the rubric and both exemplars as readable without it (check_projects PASS)."),
    row("proj-lab2-learner-text", "2.6-prose, 2.5-labs", "course/modules/BK/BK4/project.html:146-147, :186; tests/labs/BK4/lab-BK4-project-2.py:1-3", "PASS",
        PRE + "Lab 2 hypothesis and interpretation: the completed expressions are the ones Lab 1 uses (checked against the twin); 'token by token' and '1e-6 times one plus its size' match labs.js compareOutput (|x-y| <= tol*(1+|y|)), the runtime comparator loaded by site.js. Under that rule any one-cent error in a number of at most 117088 fails (tolerance <= 0.12 cent)."),
    row("proj-lab3-claim-checks-rules", "2.5-labs, 2.3-prose", "course/modules/BK/BK4/project.html:253-366 (Lab 3 hypothesis and interpretation)", "PASS",
        PRE + "Each Lab 3 claim checked against the twin output: five rows and their conservation column True; 36/38/39 indices; brute force agrees; 'one cent below falls short' (8750, 9250, 9500 vs targets); Part C counts. The sentence 'the printed values describe this set of 40 scenarios only' is a scope limit, not a general claim."),
    row("proj-notation-T", "2.4-notation", "course/modules/BK/BK4/project.html; notation/notation.json (8 symbols)", "PASS",
        PRE + "Symbols used on the page: L, R (residual), K, D, DF_i, IM_d, a1..a3, S, Lambda, M, k, t, bps. None is one of the registered symbols (T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q), and no registered symbol occurs in the page (grep for \\bT\\b, Q, Phi, gamma, R_f, R^ returns 0)."),
    row("proj-failure-leak", "2.6-failure-messages", "course/modules/BK/BK4/grader/test_project.py (all tests and helpers)", "PASS",
        PRE + f"Failure samples from three mutants with --assert=plain ({OUT}/failure_messages_sample_r8.out): messages name the property and the input (target, loss) but never the expected value. Helper messages in must_refuse, check_waterfall, checked_int state the rule."),
    row("proj-plan-conformance", "2.9-plan", "plans/BK4-build-plan.md:751-756 (Architect ruling 2026-11-04); plans/BK4-open-items.md; course/modules/BK/BK4/project.html:208; course/modules/BK/BK4/grader/test_project.py:735-743, :931-944", "PASS",
        PRE + "Round-7 FAIL cause resolved by the binding ruling dated 2026-11-04 (plan lines 751-756): (1) target set 9000/9500/9750 and exemplar levels A=2, B=4 as built, criterion 5 and brute-force scope as built; (2) cover_bps empty-losses condition kept on the page (project.html:208) and in the grader (test_project.py:931-944); (3) section 5.3 period sentence struck, and the page states no period convention. Monotonicity over seeds 0-49 is implemented (test_project.py:735-743). Not a project defect: plan text in section 5.2 (the five-condition table) and the section 5.3 line at plan 458 still carry the superseded wording; the architect should amend them textually. Non-blocking."),
    row("proj-sizing-duplicate-losses", "2.6-tests, 2.6-mathematics", "course/modules/BK/BK4/project.html:223; course/modules/BK/BK4/grader/test_project.py:682-694, :805-816", "PASS",
        PRE + "Repeated losses count once per occurrence: [5,5,10,20] at 5000 gives 5 (k=2); [5,5,5,9,12] at 6000 gives 5 (k=3), both by the page's definition with S the full count. Killed the distinct-loss mutants r3a, r3e."),
    row("proj-context-sentences", "2.9-prose", "course/modules/BK/BK4/project.html:197 (spec Context); course/modules/BK/BK4/grader/reference.py:36-109", "PASS",
        PRE + "Context states the layer order as a rule of this simulator, one default at a time, fixed scenario set; reference.py follows exactly this model; no claim about any real clearing house (project.html:219)."),
    row("proj-alternatives", "2.6-autograder 5", "ledgers/BK4/alternatives/alt1_comprehensions.py .. alt5_bisection.py", "PASS",
        PRE + f"Five alternatives pass seeds 0-49, 50/50 each ({OUT}/alternatives_reference_starter_0-49.out). Spot check: alt4 computes k as (x+9999)//10000 and indexes sorted(); alt5 bisects the integer margin on cover_bps with no sort; alt3 imports Fraction (12 uses, grep); alt2 defines class ClearingHouse (grep). alt1 was not read line by line. None is a byte copy of reference.py."),
    row("proj-survivor-leftover-order", "2.6-tests, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:411-429; ledgers/BK4/mutants/r4a_leftover_in_mapping_order.py", "PASS",
        PRE + f"r4a KILLED; test_leftover_cent_goes_to_the_lowest_id_when_the_dictionaries_list_members_out_of_order passes on the reference ({OUT}/run_graders_0-49.out)."),
    row("proj-silence-named-refusals", "2.6-tests, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:1010-1059; ledgers/BK4/mutants/r4g_*.py, r4h_*.py", "PASS",
        PRE + "r4g and r4h (debug print on refusal and on uncovered loss) KILLED on seeds 0-9 by the silence tests (mutate output)."),
    row("proj-refusal-count-docstring", "2.9-prose", "course/modules/BK/BK4/grader/test_project.py:1021-1022", "PASS",
        PRE + "The docstring says 'Each named refusal in the list below' and does not state a count; the list contains 15 calls covering the six named conditions."),
    row("proj-remainder-spec", "2.6-spec, 2.6-tests", "course/modules/BK/BK4/project.html:248; course/modules/BK/BK4/grader/test_project.py:362-368", "PASS",
        PRE + "The remainder rule on page (ascending id, DF>0, one cent each) equals reference.py lines 74-80 and the tests on fixtures {1:1,2:1,3:1} and {1:0,2:1,3:0}."),
    row("proj-money-integer-claim", "2.6-spec, 2.6-tests", "course/modules/BK/BK4/project.html:203, :224; course/modules/BK/BK4/grader/test_project.py:442-451", "PASS",
        PRE + "checked_int rejects float and bool for every money field in every test that compares money; test_waterfall_returns_plain_int_money and the margin/cover int tests run on the reference (86 passed). vc10 (float) KILLED."),
    row("proj-zero-loss-sizing", "2.6-tests, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:697-703; ledgers/BK4/mutants/r5c_*.py", "PASS",
        PRE + "r5c (zero losses dropped before counting) KILLED; the zero-loss test [0,10,20,30] at 5000 gives 10 on the reference."),
    row("proj-zero-loss-cover", "2.6-tests, 2.6-mutants", "course/modules/BK/BK4/grader/test_project.py:812-816; ledgers/BK4/mutants/r5d_*.py", "PASS",
        PRE + "r5d (zero losses excluded from the cover denominator) KILLED; test_zero_losses_are_in_the_cover_denominator gives 5000 on the reference."),
    row("proj-round7-prose-delta", "2.9-prose, 2.6-spec", "course/modules/BK/BK4/project.html:43, :220, :500-502 (round-7 to round-8 hunks)", "PASS",
        PRE + "Delta since pin 06994db1 in project.html: three hunks (ladder sentence at :43 now names the placement diagnostic, which matches the hub's placement rule at index.html:150; the Survivors convention at :220 now defines DF_i before D, matching reference.py; the Reading lead-in at :500-502 now says 'two registry sources listed as reading'). Each checked against the reference and hub text. No other slice file changed (grader, labs, alternatives, instance, starter byte-identical)."),
    row("proj-local-run", "2.6-autograder, 2.9-prose", "course/modules/BK/BK4/project.html:397-399 (local command)", "PASS",
        PRE + f"Command 'QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py' run in a scratch directory with reference.py as clearing_house.py: 86 passed ({OUT}/reference_local_cmd_seed0.out)."),
    row("proj-spec-signatures", "2.6-spec, 2.6-atlas", "course/modules/BK/BK4/grader/starter.py:29-47; course/modules/BK/BK4/project.html:201", "PASS",
        PRE + "starter.py signatures equal the page's: waterfall(loss_cents, defaulter_id, initial_margin_cents, default_fund_cents, ccp_capital_cents), margin_for_cover(losses_cents, target_bps), cover_bps(losses_cents, margin_cents); Waterfall fields in page order. No Atlas milestone for BK4 (plan section 8)."),
    row("proj-spec-inputs-instance", "2.6-spec, 2.8-data", "course/modules/BK/BK4/project.html:199; course/modules/BK/BK4/grader/instance.py:25-39", "PASS",
        PRE + f"Page Inputs (N 4..6, DF>=1, S 40..80, target 9000/9500/9750, SIMULATED) equal instance.py and the independent validity check on seeds 0-49 ({OUT}/instance_check_r8.out)."),
    row("proj-l03-crossref", "2.9-prose, 2.4-mathematics", "course/modules/BK/BK4/project.html:223 (cross-reference to Lesson 3); course/modules/BK/BK4/L03.html (Proposition 2.3)", "PASS",
        PRE + "L03.html defines the cover and states Proposition 2.3 (the sized margin is an order statistic, k = ceil(t S / 10000), L_(k), under Assumptions A3 and A4). The page's sentence 'Lesson 3 defines the cover and states the sizing rule with its proof under its own assumptions' is accurate. The proof itself is the L03 slice's row, not re-derived here; the page's rule is checked numerically by the oracle and brute force."),
]

NOTES = (
    "Delta since pin 06994db1 in the slice: project.html (three hunks), plans/BK4-build-plan.md (architect ruling appended), "
    "ledgers/BK4/mutants/s01..s05 and the round-7 scripts. Grader files, labs, alternatives, instance, reference and starter are "
    "byte-identical to the round-7 pin, but every row was re-run this round anyway. Read in full: project.html (all 521 lines, "
    "the exemplar memos through blind_memo_text.py), grader/test_project.py (1114 lines), reference.py, instance.py, starter.py, "
    "the three project twins and the Lab 2 line-by-line diff, alt1-alt5 (run 50/50 each; alt4 and alt5 read in their sizing functions; alt3 grep-checked for Fraction; alt1 and alt2 not read line by line). Blind exemplar scores equal "
    "the official data-scores. Three rubric rows FAIL on descriptor exclusivity (C1, C2, C3), not on calibration: "
    "calibration passes within one level. Not checked: the Duffie and Zhu full text (the page makes no claim from it); "
    "the Lesson 3 proof itself (the L03 slice); the Pyodide run is page_smoke only (no separate Pyodide session); "
    "verify_refs was run offline for the whole registry, and the live run was limited to the two project keys."
)
SUMMARY = (
    "Slice BK4-c round 8 is FAIL on three rubric rows (proj-rubric-c1-levels, proj-rubric-c2-levels, proj-rubric-c3-descriptors): "
    "overlapping level descriptors. Everything else re-run and PASS: run_graders 50/50, 86 collected and passing, 5 alternatives 50/50 each, "
    "58/58 mutants killed on seeds 0-9 (4 new student-error mutants t8a-t8d plus t8e), labs 3/3 with page code and expected output matching, "
    "exemplar blind scores exact (A 2,2,1,2,2; B 4,4,4,4,4), page_smoke, check_pages, check_projects, check_dag, ruff, mypy, verify_refs offline."
)
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
status_counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("PASS", "FAIL", "UNVERIFIABLE")}
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
fragment = {
    "unit": "BK4",
    "slice": "BK4-c",
    "round": 8,
    "verifier": "Claude Haiku 5.5, independent verifier for BK4-c (round 8); did not build BK4",
    "pin": "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3",
    "base": "06994db16d1ab449bcf29898a7f56cfa999dce57 (round-7 pin; previous fragment /Users/billyribeiro/.fanout/frags/E-BK4-c.round7.json used as context only; no round-7 PASS row carried: every row re-derived or re-run this round)",
    "checkout": "/Users/billyribeiro/.fanout/wt/verifyE8-BK4-c",
    "scratch": "scratch dirs under /private/tmp removed; all scripts are in ledgers/BK4/scripts/BK4-c-r8/ and command output in ledgers/BK4/scripts/BK4-c-r8/out/",
    "verified_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "verdict": verdict,
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": NOTES,
    "summary": SUMMARY,
}
pathlib.Path(ROOT / "ledgers/BK4/BK4-c.json").write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), status_counts, "mutants", len(mutants), "verdict", verdict)
