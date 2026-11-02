"""Verifier round-1: write the M4 slice d fragment (ledgers/M4/M4-d.json) from the recorded outputs.

The mutants list is parsed from the recorded output of tools/mutate_graders.py --unit M4 --seeds 0-9
(ledgers/M4/scripts/M4-d-r1/verifyD1_outputs/mutate_M4_seeds0-9.out). mutant m17_student_t_second_seed.py is left out of
the list: it is ruled not a fault under the contract (see the notes), and tools/ledger.py counts every listed mutant as a
fault that must be killed. Every other mutant in ledgers/M4/mutants is listed with its description and killer.

Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_write_fragment.py
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/M4/scripts/M4-d-r1/verifyD1_outputs/mutate_M4_seeds0-9.out"
FRAGMENT = ROOT / "ledgers/M4/M4-d.json"
EXCLUDED = {"m17_student_t_second_seed"}

SCRIPTS = "ledgers/M4/scripts/M4-d-r1"
OUTPUTS = f"{SCRIPTS}/verifyD1_outputs"
PROPOSED = f"{SCRIPTS}/verifyD1_proposed_tests.py"
SIGN = f"{SCRIPTS}/verifyD1_sign_test.py"
PROJECT_TEST = "course/modules/M/M4/grader/test_project.py"


def mutants() -> list[dict[str, object]]:
    pattern = re.compile(r"^(KILLED|SURVIVED) (\S+)\.py: (.*) -> (.*)$")
    out: list[dict[str, object]] = []
    for line in OUT.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        status, stem, description, killer = match.groups()
        if stem in EXCLUDED:
            continue
        killed_by = None if killer.strip() == "None" else killer.strip()
        out.append({"id": stem, "description": description.strip(), "killed_by": killed_by})
    return out


def rows() -> list[dict[str, str]]:
    r: list[dict[str, str]] = []

    def add(rid: str, check: str, location: str, status: str, evidence: str, fix: str = "") -> None:
        row = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
        if status != "PASS":
            row["fix"] = fix
        r.append(row)

    add(
        "d1-2.6-ladder",
        "2.6 ladder: rung 1 solved, rung 2 instant, rung 3 scope, rung 4 open",
        "course/modules/M/M4/project.html#ladder, #rungs, #spec, #stretch",
        "PASS",
        "Rung 1 is Lab 1: five numbered steps in its code and a printed expected block. Rung 2 is Lab 2: two `return ___` "
        "blanks checked by its expected block (run_labs --unit M4 --page project: PASS 3/3, "
        f"{OUTPUTS}/page_smoke_project.out). Rung 3 covers curriculum/01-foundations.yaml:222-227: simulate, the 99% "
        "change (report section 4), the moment proofs A1-A4. Rung 4 is open (#stretch). Tier F keeps rungs 1-2 at full "
        "length.",
    )
    add(
        "d1-2.6-spec-questions",
        "2.6 spec: questions a competent student would have to ask",
        "course/modules/M/M4/project.html#conditions; course/modules/M/M4/grader/reference.py:65",
        "FAIL",
        "One question I would have had to ask: is a negative (short) position valid? The conditions list "
        "(#conditions) rejects only 'a value that is not an int'; reference.py:65 accepts any whole number, so a "
        "negative position is accepted, and no test in test_project.py covers it. The instance docstring says the "
        "positions are 'all long', but the interface and the conditions are silent on the sign of a position. Every "
        "other interface question I checked (families, nu, n_draws, cov shape and symmetry, pivots, quantile types) is "
        "answered on the page.",
        "State in project.html #conditions whether a negative position is valid, and add the test that the page's "
        "choice implies to test_project.py (for example test_negative_position_is_rejected or "
        "test_negative_position_is_accepted), then re-run run_graders and mutate_graders.",
    )
    add(
        "d1-2.6-hours",
        "2.6 hours: component sum and own estimate within 30 %",
        "course/modules/M/M4/project.html#budget; data-hours-project",
        "PASS",
        "Table components 2+2+12+8+4+2 = 30, equal to data-hours-project=30 on the page and to the 30 h of the plan "
        "(plans/M4-build-plan.md, Time budget). My own estimate: rung 1 1 h, rung 2 1 h, simulator 8 h, proof appendix "
        "8 h, report and self-assessment 4 h, self-check 2 h = 24 h, which is 20 % under 30 h (inside the 30 % band).",
    )
    add(
        "d1-2.6-autograder-reference",
        "2.6 autograder: run_graders seeds 0-49 on reference.py",
        "course/modules/M/M4/grader/reference.py",
        "PASS",
        f"`.venv/bin/python tools/run_graders.py --unit M4 --seeds 0-49` -> 'run_graders M4: PASS (reference 50/50 seeds, "
        f"slowest 0.7 s)' ({OUTPUTS}/run_graders.out). Local pytest with the page's flags "
        "(QF_SEED=0,1,1093; -q -p no:cacheprovider --assert=plain -W error) gives 132 passed, 1 skipped each.",
    )
    add(
        "d1-2.6-instances",
        "2.6 instances: valid, and answers change across seeds",
        "course/modules/M/M4/grader/instance.py",
        "PASS",
        f"{SCRIPTS}/verifyD1_instances.py: seeds 0-1999 all valid (2 or 3 positions in [1000.00, 50000.00], covariance "
        "symmetric and positive definite by Cholesky, nu in 3..8, n_draws in the fixed set, none a multiple of 100, none "
        "above 19987): 2000 valid, 0 invalid. For seeds 0-19 the Gaussian 99% loss takes 20 distinct values (68098 to "
        "537314 cents) and the Student-t 99% loss 20 distinct values.",
    )
    add(
        "d1-2.6-mut-own",
        "2.6 mutation: at least 3 verifier-written student-error mutants, all killed",
        f"ledgers/M4/mutants/v1_01 .. v1_06 (written by {SCRIPTS}/verifyD1_make_mutants.py)",
        "PASS",
        "Six mutants written from student errors: v1_01 losses floored at zero (killed by "
        "test_gaussian_loss_variance_matches_portfolio_covariance, seed 0); v1_02 Student-t ignores the seed (killed by "
        "test_same_seed_gives_the_same_losses); v1_03 index round(0.99 n) (killed by "
        "test_quantile_99_convention_on_small_lists); v1_04 losses truncated by int(x+0.5) (killed by "
        "test_gaussian_losses_are_rounded_once_not_truncated); v1_05 positions read in dollars (killed by the variance "
        f"test); v1_06 inverted matched factor (killed by test_student_t_cross_term_matches_matched_covariance). "
        f"Output: {OUTPUTS}/mutate_M4_seeds0-9.out. The float version ceil(0.99 n) is equivalent on every integer n "
        f"(float_index_scan: 0 differences for n in 1..20000; proof in the notes), so it is not a mutant.",
    )
    add(
        "d1-2.6-mut-existing",
        "2.6 mutation: the 109 existing mutants re-run on seeds 0-9",
        "ledgers/M4/mutants/*.py (115 files including v1_*)",
        "PASS",
        "`tools/mutate_graders.py --unit M4 --seeds 0-9` run on this checkout: 115 mutants, 111 killed. The four survivors "
        "are rows d1-2.6-mut-m11, d1-2.6-mut-r9_03, d1-2.6-mut-v4_m02 and d1-2.6-mut-m17. Kill list in `mutants`.",
    )
    add(
        "d1-2.6-mut-m11",
        "2.6 mutation: m11 loss sign flipped survives",
        "ledgers/M4/mutants/m11_loss_sign_flipped.py; project.html Conventions item 2",
        "FAIL",
        "m11 returns round(+sum w R) instead of round(-sum w R). It survives seeds 0-9 (mutate output). Conventions item 2 "
        "states the sign ('ell = -sum_i w_i R_i ... positive when the portfolio falls'), so it violates a stated, binding "
        "behaviour. The suite cannot see it: every test reads the losses' variance, quantile or determinism, and the "
        "page admits it ('The suite does not test the sign of the loss', #contract-notes). No stream-free test can kill "
        "it: for every seed tested, m11's output equals a conforming implementation that draws -Z "
        f"({SCRIPTS}/verifyD1_alt_negated_normals.py, which passes the whole suite on seeds 0-49). The equality check is "
        f"{SCRIPTS}/verifyD1_sign_equivalence.py (output {OUTPUTS}/sign_equivalence.out: equal for both families, seeds 0-9).",
        "Freeze the Gaussian stream in Conventions item 5 (the k-th position's normal of draw d is taken in order from "
        "random.Random(seed).gauss(0, 1)) and add to test_project.py the test in "
        f"{SIGN}: the first Gaussian loss must equal round(-sum_i w_i (L z)_i) from that stream. Measured: it kills m11; "
        "it passes the reference and alt_3, alt_4, alt_5; it fails alt_1 (Box-Muller) and alt_2 (polar), which change "
        "the Gaussian stream, so those two must be removed from the five alternatives or re-keyed. The choice is the "
        "architect's.",
    )
    add(
        "d1-2.6-mut-r9_03",
        "2.6 mutation: r9_03 Student-t chi-square reused on every second draw survives",
        "ledgers/M4/mutants/r9_03_*.py; project.html Conventions item 5 and #contract-notes",
        "FAIL",
        "r9_03 draws one chi-square variable per pair of draws. It survives seeds 0-9. Conventions item 5 says 'one "
        "chi-square variable per draw', and the Student-t model needs independent draws, so this violates a stated "
        "behaviour. The page says the suite does not check it ('a family that reuses one chi-square variable on alternate "
        "draws passes the whole suite at seeds 0 to 9'). A stream-free test kills it: "
        f"proposed_student_t_draws_do_not_share_chi_square in {PROPOSED}. For draws (2k,2k+1) and (2k+1,2k+2) it checks "
        "that P(both |loss| above the median) is 1/4 within 5 standard errors (n = 40000, nu = 3). Measured: 0 of 50 seeds "
        "ok for r9_03; 50 of 50 for the reference, alt_1..alt_5 and the negated-normal variant.",
        f"Add the function proposed_student_t_draws_do_not_share_chi_square from {PROPOSED} to {PROJECT_TEST} and state "
        "in Conventions item 5 that each draw's chi-square variable is independent of the others' (that is what the "
        "test checks).",
    )
    add(
        "d1-2.6-mut-v4_m02",
        "2.6 mutation: v4_m02 matched factor skipped for nu of 3 and 4 survives",
        "ledgers/M4/mutants/v4_m02_*.py; project.html Conventions items 1 and #contract-notes; test_project.py:156-162",
        "FAIL",
        "v4_m02 applies the matched factor only when nu > 4, so the Student-t draws at nu = 3 and 4 have the wrong "
        "covariance. It survives seeds 0-9, because the variance check is skipped for nu < 5 "
        "(test_student_t_loss_variance_matches_matched_covariance) and the cross term is run at nu = 5 only. Conventions "
        "item 1 states R = sqrt((nu-2)/W) LZ for every nu > 2, and matched_scale is defined for nu > 2, so this violates "
        "a stated behaviour. A stream-free kill exists: proposed_student_t_mean_absolute_loss in "
        f"{PROPOSED}. For nu = 3..8 it checks E|loss| = w sigma sqrt((nu-2)/nu) E|T_nu| within 5 % (E|T_3| = 2 sqrt(3)/pi "
        "= 1.102658), n = 20000 draws, one position. Measured: 0 of 50 seeds ok for v4_m02; 50 of 50 for the reference and "
        "alt_1..alt_5. Six calls of 20000 draws take 0.11 s in CPython.",
        f"Add the function proposed_student_t_mean_absolute_loss from {PROPOSED} to {PROJECT_TEST} (it needs no skip), "
        "and drop the nu < 5 wording from #contract-notes if the check now covers nu = 3 and 4.",
    )
    add(
        "d1-2.6-mut-m17",
        "2.6 mutation: m17 Student-t family keyed to seed+1 survives (ruled not a fault)",
        "ledgers/M4/mutants/m17_student_t_second_seed.py; project.html line 198 (reproducible from its seed)",
        "PASS",
        "Ruled not a grader fault (verifier rules: equivalent under the contract). project.html states only that a run is "
        "reproducible from its seed (#spec Context). No sentence requires the two families to share random numbers, "
        "and Conventions item 5 leaves the stream order open. m17 is the reference with the Student-t stream re-keyed, "
        "a conforming stream, and it passes every property of the suite (survived seeds 0-9). The only 'same seed' "
        "sentence is a Lab 1 docstring (tests/labs/M4/lab-M4-project-1.py:85), which is not a grader property. The file "
        "stays in ledgers/M4/mutants and the mutate tool still prints SURVIVED; it is left out of `mutants` here. "
        "The orchestrator should move it to ledgers/M4/equivalent/ with this argument.",
    )
    add(
        "d1-2.6-alternatives",
        "2.6 alternatives: five correct implementations pass the suite",
        "ledgers/M4/scripts/alt_1.py .. alt_5.py; ledgers/M4/scripts/M4-d-r1/verifyD1_alt_*.py",
        "PASS",
        f"run_alternatives.py --seeds 0-9: reference and alt_1..alt_5 each PASS 10/10 seeds ({OUTPUTS}/alternatives.out). "
        "Two extra conforming variants written here, alt_tolerances (symmetry tolerance 1e-12, pivot > 1e-300, quantile by "
        "math.ceil(Fraction)) and negated_normals, PASS 50/50 seeds (verifyD1_run_extra.py). Diffs of each against the "
        "reference are in the scripts.",
    )
    add(
        "d1-2.6-starter",
        "2.6 starter: the suite fails on starter.py",
        "course/modules/M/M4/grader/starter.py",
        "PASS",
        "Copied starter.py to tail_risk.py and ran the suite with the page's flags: 131 failed, 1 passed (the instance-only "
        "test), 1 skipped (nu < 5). Starter raises NotImplementedError everywhere, so the suite cannot pass it.",
    )
    add(
        "d1-2.6-messages",
        "2.6 failure messages name the property and never leak the answer",
        f"{PROJECT_TEST}",
        "PASS",
        "grep for f-strings in test_project.py returns nothing; every check() and expect_value_error() message is a literal "
        "string naming a property (for example 'the gaussian losses' variance must match w prime Sigma w'). No message "
        "prints a computed value.",
    )
    add(
        "d1-2.6-count-and-pyodide",
        "2.6 test count, Pyodide and local runs match the page",
        f"{PROJECT_TEST}; course/modules/M/M4/project.html#grading-mode",
        "PASS",
        "pytest --collect-only gives 133 tests, the page says 133 checks. `tools/page_smoke.py --unit M4 --pages project`: "
        "'All 133 tests pass on seed 197439822' in the in-browser grader, the three lab twins run with zero console errors "
        f"({OUTPUTS}/page_smoke_project.out). Local run, page flags: 132 passed, 1 skipped on seeds 0, 1 and 1093.",
    )
    add(
        "d1-2.6-grader-comment-numbers",
        "2.6 numbers in the grader comments (tolerances and kill counts)",
        f"{PROJECT_TEST}:31-48",
        "PASS",
        f"{SCRIPTS}/verifyD1_variance_sweep.py over seeds 0-1999 (outputs in {OUTPUTS}/variance_sweep_*): reference max "
        "relative variance error 0.1259 (nu=5), 0.0967 (nu=6), 0.0728 (nu=7), 0.0624 (nu=8), as the comment says; no-matched "
        "variant fails on 347/347 (nu=5), 317/317 (nu=6), 342/343 (nu=7), 288/317 (nu=8); reference fails at seed 1093 "
        "(nu=3, error 1.0220). "
        f"{SCRIPTS}/verifyD1_cross_term_effect.py: one chi-square per asset moves the cross term by 14-16 % (comment: about "
        "15 %), matched factor on one asset by 27-31 % (comment: about 29 %), reference error 0.0177 on seeds 0-9 and "
        "0.0239 on seeds 0-49 (comment: 0.024), so tolerance 0.05 lies between them.",
    )
    add(
        "d1-rubric-observable",
        "2.6 rubric: every level descriptor observable",
        "course/modules/M/M4/project.html#rubric",
        "PASS",
        "Read all 20 cells. Each descriptor names an element a report can show (a formula, an integral, a printed line, a "
        "named limitation, a seed). Note, not a failure: C1 level 1 ('No proof') and level 2 ('states the formula ... "
        "misses an element of level 3') overlap for a report that states the formula without a proof; exemplar A is "
        "scored 2 by its annotation and 1 or 2 blind, which the within-one-level rule accepts.",
    )
    add(
        "d1-rubric-calibration",
        "2.6 rubric calibration: blind scores within one level of the exemplar annotations",
        "course/modules/M/M4/project.html#exemplar-a, #exemplar-b",
        "PASS",
        "Scored from the rubric cells alone. Exemplar A: C1 2 (1 or 2), C2 2, C3 2, C4 2, C5 2 (body 100 words with headings "
        "against the 300-word floor). Official 2,2,2,2,2. Exemplar B: C1 4, C2 4, C3 4, C4 4 (types and differences stated), "
        "C5 3 (no smallest undetectable inflation; body 697 words, inside 300-700; summary 71 words, inside 80). Official "
        "4,4,4,4,3. Every score is within one level of the official scoring. Caveat: I had read the annotations before I "
        "scored, so this is not a strictly blind score.",
    )
    add(
        "d1-rubric-question-bank",
        "2.6 rubric: question bank of at least 15 angles, if the section exists",
        "course/modules/M/M4/project.html",
        "PASS",
        "No question-bank section exists (Q13: the appendix is not an adversarial defence). check_projects.py M4: PASS.",
    )
    add(
        "d1-atlas",
        "2.6 atlas: contract match, cumulative suite, reuse",
        "curriculum/meta.yaml:194-276; course/modules/M/M4/project.html",
        "PASS",
        "No atlas entry names M4 and the project has no atlas key, so no atlas/<A-ID>.contract.md applies. Nothing to match.",
    )
    add(
        "d1-studio",
        "2.6 studios: every required module integrated",
        "curriculum/01-foundations.yaml:73-76",
        "PASS",
        "No studio requires M4: STUDIO-M requires [M7, M8] (01-foundations.yaml:76). Nothing to integrate.",
    )
    add(
        "d1-lab-project-1",
        "2.5 lab: lab-M4-project-1 (rung 1)",
        "course/modules/M/M4/project.html#lab-M4-project-1; tests/labs/M4/lab-M4-project-1.py",
        "PASS",
        f"run_labs --unit M4 --page project: PASS. Twin under python -I -W error exits 0 and its stdout equals the page's "
        f"expected block line for line (verifyD1_check_project_labs.py, {OUTPUTS}). Page code equals the twin except a "
        "trailing newline. Runtime 0.04 s. Hypothesis and interpretation numbers recomputed (verifyD1_prose_numbers.py): "
        "8400000000.0, 0.600000, 19800, 210946, 243004, 1.0447, ratio 1.152, 1.6667; the sampled 2267 and 32058 cents "
        "and 15.2 % in exemplar B match.",
    )
    add(
        "d1-lab-project-2",
        "2.5 lab: lab-M4-project-2 (rung 2, completion)",
        "course/modules/M/M4/project.html#lab-M4-project-2; tests/labs/M4/lab-M4-project-2.py",
        "PASS",
        "The page has two `return ___` blanks. Filling them with the twin's two return expressions gives exactly the twin, "
        "and the twin's stdout equals the expected block (0.600000, 0.333333, 19800, 100, True). Runtime 0.02 s.",
    )
    add(
        "d1-lab-project-3",
        "2.5 lab: lab-M4-project-3 (rung 3 closed-form numbers)",
        "course/modules/M/M4/project.html#lab-M4-project-3; tests/labs/M4/lab-M4-project-3.py",
        "PASS",
        "Twin stdout equals the expected block; page code equals the twin except the trailing newline. Recomputed: sd 91651.514, "
        "z 2.326348 (2.3263 to 4 d.p.), parametric 99% loss 213213 (213213.3045 unrounded), factors and inflations for nu = 3, 4, "
        "5, 8, index rows for n = 100, 101, 19987 (ceil 19788, floor 19787). The lab uses no random draws.",
    )
    add(
        "d1-prose-numbers",
        "2.2 numbers in prose recomputed from unrounded values",
        "course/modules/M/M4/project.html (Labs, Report, Exemplars A and B)",
        "PASS",
        f"{SCRIPTS}/verifyD1_prose_numbers.py: 19 displayed numbers, all agree with the unrounded recomputation (for example "
        "1.151973 -> 1.152; 15.1973 % -> 15.2 %; 4.4700 % -> 'about 4.5 %'; 213213.3045 -> 213213).",
    )
    add(
        "d1-prose-scope",
        "2.9 scope words backed by a computation",
        "course/modules/M/M4/project.html (exemplar A, line 354 and 359)",
        "PASS",
        "The only unbacked scope word is 'always' in exemplar A ('The Student-t model is always riskier'), and its own "
        "annotation marks it as unbacked (line 359), so it is an intentional miss, not a claim of the unit. Other scope words "
        "('every', 'only', 'exactly', 'same') sit on sentences backed by a formula or a printed line.",
    )
    add(
        "d1-prose-process-words",
        "2.9 no process words in learner text",
        "course/modules/M/M4/project.html",
        "PASS",
        "grep of learner-facing text for builder, verifier, round, draft, TODO, session, pending returned no hits. The lab "
        "phrase 'Stated before running' is the page's own pedagogy, not a process word.",
    )
    add(
        "d1-prose-banned-phrases",
        "2.9 banned phrases absent",
        "course/modules/M/M4/project.html",
        "PASS",
        "`tools/check_pages.py --unit M4` -> 'check_pages M4: PASS' (BANNED list at tools/check_pages.py:58-74 covers the page).",
    )
    add(
        "d1-dag",
        "2.9 DAG: no concept used or linked outside the closure",
        "course/modules/M/M4/project.html",
        "PASS",
        "project.html has no data-concept or concept link (grep: 0 matches). `tools/check_dag.py --unit M4` -> PASS. The page "
        "cites Lessons 1, 2, 5 and 6 only, all in M4.",
    )
    add(
        "d1-notation",
        "2.4 notation: symbols against notation/notation.json",
        "notation/notation.json; course/modules/M/M4/project.html",
        "PASS",
        "The registry has 8 program-wide entries: T, Phi, gamma_3, gamma_4, R^ast, R^{e ast}, R_f, Q-blackboard. The page "
        "uses none of them with a different meaning: it uses plain R (return), Q (quantile), F (distribution function), "
        "Z, W, L, nu, s, w, Sigma, ell, Gamma (not registered), and the \\E macro with its registered meaning. No collision.",
    )
    add(
        "d1-cites",
        "2.1 citations on the page: registry key, locator and attributions",
        "course/modules/M/M4/project.html#reading; references/references.json",
        "PASS",
        "Reading cites only blitzstein2019introduction and says no locator was read and no statement is attributed. Internal "
        "references check: Lesson 6 Definition 2.1 (chi-square) and Definition 2.5 and Proposition 2.6 exist in L06; "
        "Lesson 1 Q(p) = inf{x : F(x) >= p} exists in L01. `tools/verify_refs.py --offline`: 560 entries, 0 problems. "
        f"`tools/verify_refs.py --unit M4` (live): 1 of 560 entries, 0 problems ({OUTPUTS}/verify_refs_live.out).",
    )
    add(
        "d1-structure",
        "2.9 structure: template sections in order; check_pages and check_projects",
        "course/modules/M/M4/project.html",
        "PASS",
        "Sections present in order: ladder, rungs (labs 1-2), spec (conventions, conditions, contract notes, grading), budget, "
        "autograder panel, local run, report (lab 3, brief, rubric, exemplars, self-assessment), stretch, reading, references, "
        "module navigation. `tools/check_pages.py --unit M4`, `tools/check_projects.py --unit M4`: PASS.",
    )
    add(
        "d1-cards-schema",
        "2.7 cards: schema, ids, lesson coverage, grades",
        "course/modules/M/M4/cards.json",
        "PASS",
        f"212 cards; ids M4-c001..M4-c218 with gaps at c123, c184, c196, c202, c203, c206 (the spec says ids from c001 upward, so "
        "gaps are allowed; {SCRIPTS}/verifyD1_cards_check.py); no duplicate ids; every card has id, lesson, front, back, grade; lessons L01 to L10 each have 18 to 31 "
        "cards; grades 191 T, 21 C; each C card has a basis naming a lab part or seed.",
    )
    add(
        "d1-cards-numbers-in-lesson",
        "2.7 every number on a card occurs in its own lesson",
        "course/modules/M/M4/cards.json vs course/modules/M/M4/L01.html..L10.html",
        "PASS",
        f"{SCRIPTS}/verifyD1_cards_check.py (output {OUTPUTS}/cards_check.out): 'number tokens not found in own lesson: []' "
        "and 'theorem-style references not found in own lesson: []' over all 212 cards (Definition, Proposition, Example, "
        "Remark, Lemma, Theorem, Assumption, and Problem X matched as the lesson's 'X ·' heading).",
    )
    add(
        "d1-cards-labs",
        "2.7 C cards: lab numbers against the run output",
        "course/modules/M/M4/cards.json (21 C cards); tests/labs/M4/lab-M4-L02..L10-1.py",
        "PASS",
        f"Each lesson twin was run with python -I -W error (all exit 0; outputs in {OUTPUTS}/labout/). Every C-card number matches its "
        "output: M4-c030 3.469 (L02, seed 2026, n 10000); c033 489 (L02, seed 2027); c047 2.065 and 2.073 (L03); c082 "
        "0.00002223 and 0.00016257 (L05); c083 0.592936 and -0.007064 (L05); c098 1.669114 and 0.001469 (L06, n 100000, seed "
        "20260602+nu); c112 7.11e-13 at t=2 with 244.69193226 (L07); c113 -0.062124 and -0.062110 (L07, seed 20260701); c126 "
        "0.0187 (L08); c143 0.8552 and 0.0056 (L09, 4000 replications, seed 2026); c162 1.8220 and 1.8838 (L10, 400 "
        "replications); c166 3.4689 and 0.0311 (L09); c167 0.8548, 0.8518, 0.0056 (L09); c169 +0.9919 (L10, seed 2028); c170 "
        "1.0211, 0.9396 (L10); c171 0.8807, 1.1987 (L10); c183 5.580 and 5.625 (L03); c188 (0.9770, -2.0055) (L08); c189 "
        "+0.0031 (L10, seed 2026); c190 -0.0235 (L10, seed 2027).",
    )
    add(
        "d1-cards-math",
        "2.4/2.7 cards: T-card numbers and claims recomputed",
        "course/modules/M/M4/cards.json",
        "PASS",
        f"{SCRIPTS}/verifyD1_card_math.py (40 checks, all agree; {OUTPUTS}/card_math.out). Covers c011 198; c015 ceil(148.5)=149; c026 12500; c028 35/3 = 4 x 35/12; c029 "
        "91/6 and 35/12; c031 sqrt(2968750000)=54486.24; c041 and c045 (73/9, 7/3); c042 mean 7/4, Var 163/16; c043 5/3; c044 "
        "gamma_3=0; c048 64/9; c058 and c063 cell values; c074 Var(Y)=2/9; c081; c094 5/3; c141 7/60; c142 40.4006 -> 40; "
        "c157 (2/pi) arctan(0.1) = 0.063451 and 1/0.063451 ~ 1 in 16; c160 quartiles -1, 1; c161 10x0.063451 = 0.634510; "
        "c168 0.002128 (from the closed form); c172 and c187 (2.205308, 4 sqrt3/pi = 2.2053); c185 gaps -0.0080, +0.0066, "
        "+0.0022, -0.0056, -0.0074; c200 m3 = 2157/32, m4 = 149461/256; c209 density; c214, c215 sign(a); c216; c205 and c088; "
        "c102 (1-2t)^(-1/2); c107 modulus formula; c119, c207, c208 matrices; c125 quadratic form. All agree with the cards.",
    )
    add(
        "d1-cards-lesson-statements",
        "2.7 sample of T cards against the current lesson text",
        "course/modules/M/M4/cards.json vs L01..L10 propositions and examples",
        "PASS",
        "Checked against the lesson text (scratch extracts of L01..L10): c011 Example 3.5; c015 Example 3.5 and Prop 3.4; c093, "
        "c094, c096, c092 (L06 Prop 2.6, Def 2.5); c131 and c137 (L09 Prop 1.2, text after Thm 1.3, Problem M3 with bound 2); "
        "c133 and c147 (L09 Prop 2.2 bound |s|^3 E|Y|^3/3; L10 CDF); c156 (L10 Assumption 3, not graded); c160 (L10 Problem "
        "P2); c122 (L08 Section 4, P(X+Y=0) >= 1/2); c135 (L09 Section 2 remark); c153 and c186 (L10 Remark 2.2, Prop 1.5(c)); "
        "c154 (L10 Prop 2.3); c161 (L10 Problem E1); c125 (L08 Problem P3). Problem references P2, P3, R2, R3, M1, M3, E1, E3 "
        "all exist (format 'P3 ·' in the lesson). Section references point to the headings of the lesson they name.",
    )
    add(
        "d1-cards-duplicates",
        "2.7 cards: no duplicate cards (full scan)",
        "course/modules/M/M4/cards.json: M4-c066 and M4-c213; M4-c070 and M4-c211",
        "FAIL",
        f"Full pairwise scan ({SCRIPTS}/verifyD1_cards_check.py, difflib on fronts and backs; it lists only lexical near-pairs and "
        "does NOT flag the duplicates below, which I found by reading the 212 fronts and backs). Two real duplicates. M4-c066 (L04, "
        "'What is Cov(X, X) ...? Var(X)') and M4-c213 (L05, 'What is Cov(X, X)? Var(X)') test the same fact. M4-c211 (L05, "
        "'Cov(aX + b, Y) = a Cov(X,Y)') is the special case b = 0, c = 1, d = 0 of M4-c070 (L05, Prop 1.2, "
        "'Cov(aX + b, cY + d) = ac Cov(X,Y)'). The other near-pairs ask different facts.",
        "Delete M4-c213 (keep M4-c066, which carries the Problem R2 derivation) and delete M4-c211 (M4-c070 covers it). "
        "Re-run tools/check_pages.py --unit M4 for the card count and lesson coverage.",
    )
    add(
        "d1-cards-c191-grade",
        "2.3/2.7 cards: grade of a derivation",
        "course/modules/M/M4/cards.json M4-c191",
        "FAIL",
        "M4-c191 derives the covariance matrix of the two-asset construction (a computation: Sigma = [[S1^2, rho S1 S2], "
        "[rho S1 S2, S2^2]]) and is graded C with basis 'Example 2.5'. BUILDER_RULES grades derivations T; the lesson "
        "treats the same computation as a derivation under Assumption 1 of Example 2.5 (L05 line 634), and the other "
        "cards that depend on a stated assumption (for example M4-c085, M4-c093) are graded T with 'under Assumption 1'. "
        "The grade is inconsistent with that rule.",
        "Regrade M4-c191 to T and state in its back 'under the hypotheses of Example 2.5 (S1, S2 > 0; |rho| < 1; Z1, Z2 "
        "independent, mean 0, variance 1)', dropping the basis field.",
    )
    add(
        "d1-cards-hypotheses",
        "2.7 cards carry the hypotheses of their propositions (sample)",
        "course/modules/M/M4/cards.json",
        "PASS",
        "Sampled the cards that cite a proposition: c005, c006, c008, c022, c023, c024, c040, c046, c071, c072, c091, c133, "
        "c134, c137, c216, c218 state their hypotheses as the lesson does. c070 has none, and Proposition 1.2 of L05 has none "
        "(no finitely-valued hypothesis in its statement), so the card matches.",
    )
    add(
        "d1-data",
        "2.8 data and SIMULATED labels",
        "course/modules/M/M4/project.html; grader/instance.py",
        "PASS",
        "No dataset: no data-files, no MANIFEST entry, no real data. The page says every input is SIMULATED (project.html "
        "line 37 and the inputs paragraph), the instance docstring says it, and the grader header says it.",
    )
    add(
        "d1-freshness-registry",
        "2.1 registry and freshness flags",
        "references/references.json (blitzstein2019introduction)",
        "PASS",
        "The unit's only key was re-verified live (1 of 560, 0 problems). No debate brief exists for M4 (no debate key). "
        "No registry or freshness flags raised.",
    )
    add(
        "d1-gates-repo",
        "repo gates touching this slice: ruff, mypy, pytest subset",
        "pyproject.toml; tests/labs/M4; tests/test_page_checks.py, tests/test_labs.py, tests/test_run_labs.py, tests/test_page_smoke.py",
        "PASS",
        "`ruff check .` All checks passed (the ledgers folder is excluded by pyproject extend-exclude); `ruff format --check "
        "tests/labs/M4`: 13 files formatted. `mypy --no-incremental` (strict, repo config): 'Success: no issues found in 331 "
        f"source files' ({OUTPUTS}/mypy.out). pytest on the four files: all pass ({OUTPUTS}/pytest_subset.out).",
    )
    add(
        "d1-tools-structure",
        "2.9 check_pages, check_dag, check_projects, run_labs, page_smoke (project)",
        "tools/*.py",
        "PASS",
        f"check_pages M4: PASS; check_dag M4: PASS; check_projects M4: PASS; run_labs M4: PASS (13/13); page_smoke M4 "
        f"project: PASS (outputs in {OUTPUTS}/).",
    )
    return r


def main() -> int:
    fragment = {
        "unit": "M4",
        "slice": "d",
        "round": 1,
        "verifier": "independent verifier (Haiku), not a builder of M4",
        "pin": "d0f39c09 (checkout detached at the pin; the task names d0f39c0)",
        "base": "none: first independent verification of slice d in this round",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyD1-M4-d",
        "scratch": "/tmp/M4-d-r1",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": "FAIL",
        "rows": rows(),
        "mutants": mutants(),
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Scope: project.html (rubric and exemplars), grader/ (reference, starter, instance, test_project.py), the three "
            "project labs, all 212 cards of cards.json, and the mutants and alternatives (seeds 0-9). Nothing outside the slice "
            "was edited; new files are the fragment, the scripts under ledgers/M4/scripts/M4-d-r1/, and mutants v1_01..v1_06.",
            "Equivalence (float ceiling index): quantile index math.ceil(0.99 n) with a float 0.99 equals (99 n + 99) // 100 for "
            "every integer n >= 1. Proof: fl(0.99) = 0.99 - delta with 0 < delta < 1e-17, so fl(0.99 n) lies within n*1e-17 of "
            "99n/100. If 99n/100 is not an integer its fractional part is at least 0.01, far above that error, so the ceiling "
            "is unchanged; if it is an integer m, the rounded product is m, because n*delta is far below half an ulp of m. "
            "Numerical check over n = 1..20000: 0 differences (verifyD1_float_index_scan.py). Not listed as a mutant.",
            "Equivalence/ruling (m17, seed+1 for the Student-t family): see row d1-2.6-mut-m17. Left out of `mutants`.",
            "Survivor m11 is indistinguishable from a conforming implementation with negated normals, which is why the row "
            "cannot be closed by a stream-free test; the fix is a spec decision (freeze the stream), with the conflict stated.",
            "Mutants: the verifier-written set is v1_01..v1_06 (this round); the existing 109 files are listed with their "
            "killers from the seeds 0-9 run. The number 105/112 in the earlier ledger is not reproduced: this checkout has "
            "115 files in ledgers/M4/mutants and 111 are killed on seeds 0-9.",
            "Blind rubric scoring: the annotations were read before scoring, so the calibration is not strictly blind.",
            "Not checked, and why: (a) the cards were not read line by line against every lesson paragraph; all numbers, all "
            "lab-derived numbers, all cross-references and a sample of T claims were checked, and the lessons themselves belong "
            "to slices a to c; (b) mutate_graders was run on seeds 0-9 only (the window the task names), not on 0-49; "
            "(c) page_smoke ran for the project page only (the task's slice); (d) the 'graded instantly' behaviour of Lab 2 "
            "was checked through its expected block and the page_smoke lab run, not by clicking in a browser; (e) no live "
            "Crossref run beyond the one M4 entry, which returned 0 problems; (f) the proposed tests and the sign test were "
            "validated on this checkout, not added to the grader (the verifier may not edit).",
            "The mutants directory still contains the m11, r9_03, v4_m02 survivors; the fix rows describe each change.",
            "Card ids have gaps at c123, c184, c196, c202, c203, c206. Allowed by the spec, recorded only.",
        ],
        "summary": {},
    }
    counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
    for row in fragment["rows"]:  # type: ignore[attr-defined]
        counts[row["status"]] += 1  # type: ignore[index]
    killed = sum(1 for m in fragment["mutants"] if m["killed_by"])  # type: ignore[attr-defined]
    fragment["summary"] = {
        "rows": len(fragment["rows"]),  # type: ignore[arg-type]
        "pass": counts["PASS"],
        "fail": counts["FAIL"],
        "unverifiable": counts["UNVERIFIABLE"],
        "mutants_killed": killed,
        "mutants": len(fragment["mutants"]),  # type: ignore[arg-type]
    }
    FRAGMENT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(fragment["summary"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
