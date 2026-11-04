# BK4 open items and gaps

Requests and gaps raised while reconciling the project slice (slice c) with `plans/BK4-build-plan.md` §5. Each item
records a deviation between the built project and the plan, and the decision taken. Where the built project was
internally consistent (page, `grader/instance.py`, `grader/test_project.py` and the lab twins agree), the plan text was
changed to match the project. Architect may overrule any of these.

## Status of the plan conformance items (round 3)

Items 1 to 4 below are the builder's proposals, not Architect rulings. The 2026-11-03 Architect block in
`plans/BK4-build-plan.md` is binding ("where the plan states a recommendation ... follow it"), and the builder's edits to
that plan (lines 419, 478, 481 and 515 in commit 67a2d13) have not been ratified, and they remain in the plan until the
Architect rules. Until the Architect records a
ruling in the plan's "Architect decisions" block, the project page and suite deviate from the binding plan on the points
below. Round-3 verifier row `proj-plan-conformance` stays FAIL for these reasons. Not yet listed in round 2:

- (e) Monotonicity: the plan asks for "on each seed" (plan 517). The suite checks `INST` and `INST2` only
  (`test_margin_is_non_decreasing_in_the_target`).
- (f) Exception table: the plan names five conditions (plan 441-445). The page and suite add `cover_bps` with an empty
  `losses_cents` (project.html Constraints; `test_empty_losses_are_refused_in_cover_bps_with_the_scenario_message`).
- (g) Plan 5.3 period convention (the settlement date is period 0; the scenario index starts at 1) appears nowhere on the
  page. Not checked whether the page must state it.

Round 3 also added grader tests for the defaulter-id, sizing and cover conditions (`test_project.py`, 81 checks). These
follow the page's named conditions and do not change any rule in plan 5.2.

## Plan conformance decisions (round 2 verifier rows `proj-plan-conformance`)

1. **Target set (plan §5.2).** The plan gave `target_bps` from {9900, 9950, 9975}. The project uses {9000, 9500, 9750}
   on the page (Inputs), in `grader/instance.py` (`target_bps = rng.choice((9_000, 9_500, 9_750))`), in the suite
   (`TARGETS`), and in Lab 3 (`TARGETS = (9_000, 9_500, 9_750)`). Decision: the project is authoritative. The plan now
   states {9000, 9500, 9750}. The plan's set appears in no built file, so the built set is kept.
2. **Exemplar levels (plan §5.4).** The plan gave exemplar-a level 4 and exemplar-b level 2. The page gives exemplar-a
   `data-level="2"` with scores 2,2,1,2,2, and exemplar-b `data-level="4"` with scores 4,4,4,4,4, and each annotation
   matches its own level. Decision: the page is authoritative (the planner's assignment was reversed). The plan now
   states the page's levels.
3. **Criterion 5 wording (plan §5.4).** The plan's level-4 descriptor names "no procyclicality". The page names "no
   change in margins in stress", and exemplar-b uses the same words. Decision: the page wording is kept; the plan now
   quotes it. "Procyclicality" is not defined on the page, so the page does not use the term.
4. **Brute-force sizing check (plan §5.5).** The plan asked for the brute-force sizing check "on every seed". The suite
   runs it on the two cases `INST` (seed) and `INST2` (seed + 7919), for each of the three targets. The page says the
   sizing is checked "against a brute-force search over whole-cent margins" and names no seed set. Decision: the suite
   stands. The page does not promise a search on every seed, and the suite already runs the brute-force search at all
   three targets on two cases, so the plan now states those two cases. In the suite, seeds 0 to 49 are used only by the
   instance-dependence test, which checks at least three distinct sizing answers.

## Tooling fix (plan §10 mypy command)

5. **Grader imports under the repository mypy command.** `.venv/bin/mypy tests/labs/BK4 course/modules/BK/BK4/grader`
   reported `import-not-found` for `clearing_house` (the learner's module, created beside the suite at run time) and
   `instance` (beside the suite, not on the repository's `explicit_package_bases` path). Decision: the two imports carry
   `# type: ignore[import-not-found]` with a comment saying where the module is found. The plan command is unchanged. It
   exits 0 after this change. `tools/run_graders.py` typechecks `reference.py`, `instance.py` and `starter.py` under
   `mypy --strict --ignore-missing-imports` in the scratch layout and is not changed.
