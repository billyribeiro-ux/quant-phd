"""Write the round-2 ledger fragment for M7 slice d (project.html, grader, project labs, cards.json).

Usage: .venv/bin/python ledgers/M7/scripts/M7-d-r2/build_fragment_r2.py <mutate-output.txt>
The mutant list is read from the output of `tools/mutate_graders.py --unit M7 --seeds 0-49`. Validate afterwards with
    .venv/bin/python -c "import sys,json; sys.path.insert(0,'tools'); import ledger; print(ledger.validate(json.load(open('ledgers/M7/M7-d.json')), 'M7-d'))"
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "ledgers/M7/M7-d.json"

PASS = "PASS"
FAIL = "FAIL"
UNV = "UNVERIFIABLE"


def row(rid: str, check: str, location: str, status: str, evidence: str, fix: str | None = None) -> dict[str, str]:
    out = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if status != PASS:
        out["fix"] = fix or ""
    return out


ROWS: list[dict[str, str]] = [
    row("m7d-lab1-numbers", "2.5-lab / 2.2-numbers",
        "course/modules/M/M7/project.html lines 53-166; tests/labs/M7/lab-M7-project-1.py", PASS,
        "Ran python -I -W error tests/labs/M7/lab-M7-project-1.py; output equals the expected block (project.html 155-165) "
        "line for line. Hypothesis numbers (5.0%, 3.0%, -2.0%, gamma 2) match MU and GAMMA in the twin. Interpretation (166): "
        "step 1 weights 54/65, 5/26, -3/130 (third negative, held at zero), answer (9/11, 2/11, 0), nu -21/1100, bound "
        "multiplier 9/1100, objective -3/220 = -0.0136363 rounded to -0.013636: all match the output."),
    row("m7d-lab2-completion", "2.5-lab",
        "course/modules/M/M7/project.html lines 169-283; tests/labs/M7/lab-M7-project-2.py", PASS,
        "The twin (completed solution) runs under -I -W error and prints the block at project.html 271-281 exactly. The page "
        "has three blanks (lines 248, 259, 260), matching the hypothesis (line 171), the ladder (line 45) and the hub "
        "rung-2 text. The stationarity residual the blank must compute (gamma Sigma w - mu + nu, minus the bound multiplier "
        "in the loop) matches the completed code in the same file."),
    row("m7d-lab3-certificate", "2.5-lab / 2.4-math",
        "course/modules/M/M7/project.html lines 369-438; tests/labs/M7/lab-M7-project-3.py", PASS,
        "Twin output equals the block at lines 435-437. Re-derived by hand: candidate B stationarity = 2 x 9/1100 = 9/550 and "
        "dual = 9/1100; candidate C moves the gradient by (6e-5, -1.6e-4, -4e-5), so stationarity = 1.6e-4 = 1/6250; "
        "primal and complementary residuals are 0 in all three (the interpretation at line 438 says exactly this)."),
    row("m7d-spec-residual-definitions", "2.4-math / spec",
        "course/modules/M/M7/project.html lines 303-318; grader/test_project.py lines 84-116", PASS,
        "Stationarity r^w_i and r^t_i (lines 309-311) re-derived from the Lagrangian of the linearized problem (budget +nu, "
        "bounds -lambda_l +lambda_u, sector +eta, turnover +alpha -beta; r^t = kappa - alpha - beta); the suite's "
        "stationarity() (test_project.py 84-102) uses the same signs. Primal, dual and complementary definitions (313-316) "
        "match recomputed_certificate (105-116)."),
    row("m7d-spec-residual-wording", "2.9-prose",
        "course/modules/M/M7/project.html line 311", PASS,
        "Round-1 FAIL repaired: line 311 now reads 'The four certificate fields are defined as follows' and no longer "
        "describes all four as absolute values."),
    row("m7d-spec-tolerance-agreement-1e-8", "2.4-spec",
        "course/modules/M/M7/project.html line 318; grader/test_project.py lines 36, 356-369", PASS,
        "Tolerance 1e-8 on each field is enforced (test_certificate_residuals_are_within_tolerance, TOL = 1e-8); agreement "
        "1e-9 is enforced (test_certificate_agrees_with_the_recomputed_residuals, line 360). Both match the page."),
    row("m7d-proof-uniqueness-midpoint", "2.4-proofs",
        "course/modules/M/M7/project.html line 321", PASS,
        "Round-1 FAIL repaired. The midpoint of two feasible (w,t) is feasible because the constraints are affine; strict "
        "convexity of f in w gives f(mid) < f(w) when w != w'; that contradicts minimality, so the minimizer is unique in w. "
        "The steps are valid given the stated hypotheses (see m7d-proof-differentiability for the one missing hypothesis)."),
    row("m7d-proof-differentiability", "2.4-proofs / hypotheses",
        "course/modules/M/M7/project.html lines 320-321 (statement and proof); line 322 (hypotheses)", FAIL,
        "The proposition is graded T (line 320) and its statement only says f is convex in w. The proof (line 321) says "
        "'the stationarity conditions say that its gradient vanishes at (w, t), so (w, t) minimizes L', which needs f and "
        "L differentiable, and the stationarity conditions of (K1) presuppose a gradient. Differentiability appears nowhere in "
        "the statement or in the hypotheses paragraph (line 322), so the hypotheses are incomplete.",
        "Add 'f is differentiable and convex in w' to the proposition's statement and to line 322."),
    row("m7d-proof-multiplier-existence", "2.4-claims / hypotheses",
        "course/modules/M/M7/project.html line 322", FAIL,
        "Line 322 says 'Whether the multipliers exist for every generated instance is not proved here and is open.' 'Is open' "
        "asserts an unresolved mathematical status with no computation and no read source. The instances have affine "
        "constraints and a box-bounded feasible set, so existence of multipliers at the minimizer is a standard consequence "
        "of linear constraints; the page does not establish that, and 'open' is not supported by anything on the page.",
        "Replace 'is not proved here and is open' with 'is not proved on this page; the suite checks seeds 0 to 49 only'."),
    row("m7d-spec-tolerance-1e-9", "2.4-spec / architect-a",
        "course/modules/M/M7/project.html line 318; grader/test_project.py lines 443-461 (tests at 1e-8 refused, 1e-10 accepted)",
        FAIL,
        "Line 318 states the starting portfolio is checked 'with a tolerance of 1e-9'. The suite only brackets it: the "
        "starting-sum, bound and cap cases use 1e-8 (refused) and 1e-10 (accepted). Witness: the reference with TOL = 5e-9 "
        "(ledgers/M7/scripts/M7-d-r2/witnesses_r2.py, workspace start-5e-9) passes 140 of 140 on seed 0 and seeds 3, 5, 11. "
        "The architect ruling says a requirement the tests do not enforce must not be claimed.",
        "Either state 'a tolerance between 1e-10 and 1e-8' or add a refusal test at 2e-9 and an acceptance test at 5e-10."),
    row("m7d-spec-nan-inf-named", "2.4-spec",
        "course/modules/M/M7/project.html line 323; grader/test_project.py lines 611-619", PASS,
        "NaN and +/-infinity are refused with ValueError in each numeric field (NON_FINITE_FIELDS, 8 fields x 3 values)."),
    row("m7d-spec-named-message", "2.4-spec / architect-a",
        "course/modules/M/M7/project.html line 323 ('the message names the condition'); grader/test_project.py lines 554-560, 593-596",
        FAIL,
        "Every named refusal uses pytest.raises(ValueError, match=r'\\S'), which only requires a non-empty message. "
        "Witness: ledgers/M7/mutants/v06_every_refusal_says_invalid_input.py (all 19 ValueError messages replaced by "
        "'invalid input') SURVIVES all 140 tests on seed 0 and in the full mutation run (tools/mutate_graders.py --unit M7).",
        "Delete 'and the message names the condition' from line 323, or add a test that matches a condition-specific word."),
    row("m7d-spec-named-list-coverage", "2.4-spec / architect-a",
        "course/modules/M/M7/project.html lines 323, 329; grader/test_project.py lines 577-589 (other side), 661-665", FAIL,
        "Line 323 lists 'a list does not have one entry per asset' as a named condition and line 329 says 'a list one entry "
        "short or one entry long'. The suite tests one-entry-too-many for w0, lower, upper, sector and the sigma rows, and "
        "one-entry-too-few for w0, lower, upper, sector, sigma. The 'mu' field is never tested one entry long. Witness: "
        "ledgers/M7/mutants/v05_mu_longer_than_sigma_truncated.py (mu truncated to the matrix size) SURVIVES. The other 12 "
        "named conditions have a refusal test and a boundary test in NAMED_CONDITIONS (lines 534-548).",
        "Add ('mu one entry too long', _one_entry_too_many('mu')) to OTHER_SIDE_REFUSED."),
    row("m7d-spec-boundary-claim", "2.4-spec",
        "course/modules/M/M7/project.html lines 323-324; grader/test_project.py lines 285-317, 534-572, 620-717", PASS,
        "Each refusal test starts with a control that the valid case is accepted, and NAMED_CONDITIONS supplies a valid form "
        "for every condition with a limit (gamma 1e-6, turnover 0, equal bounds, sector cap 1e-10 inside, start sum 1e-10). "
        "Sigma PD valid form has smallest eigenvalue 1e-4 (computed: 0.01 J + 1e-4 I)."),
    row("m7d-spec-test-count-and-seeds", "2.9-prose / 2.5",
        "course/modules/M/M7/project.html line 329 ('collects 140 checks')", PASS,
        "pytest --collect-only with QF_SEED = 0..49 gives 140 tests on every seed (50 of 50 lines '140 tests collected')."),
    row("m7d-spec-hours", "2.9-structure / hours",
        "course/modules/M/M7/project.html lines 33, 341-347; course/modules/M/M7/index.html line 29; L01-L08 data-hours", PASS,
        "Project rows 2+3+10+6+7+5 = 33 = data-hours-project. Lesson data-hours 9+9+10+10+10+10+9+10 = 77 = data-hours-lessons; "
        "77 + 33 = 110. No arithmetic inconsistency (pace not checked, per architect ruling)."),
    row("m7d-spec-other-claims", "2.9-prose",
        "course/modules/M/M7/project.html lines 297-299, 324-327, 355, 362-363", PASS,
        "Starter raises NotImplementedError and the suite fails on it (137 failed, 3 passed on seed 0; checked). Standard "
        "library only (test_only_standard_library_imports). Purity and silence tests (725-744) exist. The local command "
        "(line 362) and the decode command (line 363) use the file names and the make_instance payload that exist."),
    row("m7d-hand-cases", "2.4-math / architect-b",
        "course/modules/M/M7/grader/test_project.py lines 218-246", PASS,
        "Each hand answer re-derived by hand. Budget only: w = mu + nu, nu = 0.3, w = (0.6, 0.4). Zero turnover: w0 = (0.5, 0.5). "
        "Single asset: w = 1. Upper bound binding: unconstrained (0.35, 0.65) cut at upper 0.3 gives (0.7, 0.3); turnover 0.2 <= 0.5. "
        "Turnover binding: unconstrained (0.7, 0.3) cut to (0.6, 0.4), turnover 0.2 = limit."),
    row("m7d-hand-case-tolerance", "2.4-math / architect-b",
        "course/modules/M/M7/grader/test_project.py lines 394-395 (weights to 1e-9)", FAIL,
        "The hand-case test requires each weight within 1e-9 of the worked answer. The page states no weight tolerance; it "
        "states 1e-8 on the certificate fields (line 318). Witness: the reference with each two-asset answer moved by 2e-9 "
        "along the budget-preserving direction (workspace hand-2e-9, ledgers/M7/scripts/M7-d-r2/witnesses_r2.py) passes 136 of "
        "140 and fails only the four two-asset hand cases, all on the 1e-9 weight check. The perturbed output stays within the "
        "stated 1e-8 field tolerances, so it is a correct answer under the page.",
        "Either state a weight tolerance of 1e-8 on the page and use it in the test, or compare certificate fields only."),
    row("m7d-comparators-and-edges", "2.4-math / architect-b",
        "course/modules/M/M7/grader/test_project.py lines 372-379", PASS,
        "The three comparators are convex mixes of the answer and w0; w0 is feasible per the page, so each comparator is "
        "feasible. Edge cases (bound equal to start, turnover 0, gamma 1e-6) are in NAMED_CONDITIONS. Note: the sector-cap "
        "edge is tested 1e-10 below the starting sector weight, not at equality; that is inside the stated tolerance."),
    row("m7d-grader-suite-over-constraint", "2.6-grader / architect-b",
        "course/modules/M/M7/grader/test_project.py (whole suite); ledgers/M7/scripts/M7-d-r2/alt_bland.py, alt_exact.py, alt_first.py; ledgers/M7/scripts/M7-d-r1/alt_core.py",
        PASS,
        "Eight correct alternatives pass all 140 tests on seeds 0-49, 50 of 50 each: five round-1 routes (run_alts.py output: "
        "alt1-alt5 50/50) and three round-2 routes (Bland's rule, exact Fraction arithmetic, first-improvement: 50/50 each). "
        "The only over-constraint found is the hand-case weight tolerance (m7d-hand-case-tolerance)."),
    row("m7d-mutants-existing", "2.6-mutants",
        "ledgers/M7/mutants/m01..m24 (24 files)", PASS,
        "tools/mutate_graders.py --unit M7 --seeds 0-49 killed all 24 (output saved at /tmp/M7-v/d-r2/mutate_all.txt, lines "
        "KILLED m01..m24)."),
    row("m7d-mutants-new-v01-v04", "2.6-mutants",
        "ledgers/M7/mutants/v01..v04", PASS,
        "v01 (NaN in mu silently zeroed) round-1 survivor is now KILLED by test_non_finite_value_is_refused_with_value_error[mu-nan]; "
        "v02, v03, v04 killed. Round-1 FAIL (m7d-mutant-v01-survivor) repaired."),
    row("m7d-mutants-new-v05", "2.6-mutants / spec",
        "ledgers/M7/mutants/v05_mu_longer_than_sigma_truncated.py; project.html line 323, 329", FAIL,
        "Mutant SURVIVES: an expected-return list one entry longer than the asset count is silently truncated and the answer "
        "is returned. The page names this as refused (lines 323 and 329).",
        "Add a refusal test for mu one entry too long (see m7d-spec-named-list-coverage)."),
    row("m7d-mutants-new-v06", "2.6-mutants / spec",
        "ledgers/M7/mutants/v06_every_refusal_says_invalid_input.py; project.html line 323", FAIL,
        "Mutant SURVIVES: every ValueError says 'invalid input'. The page claims the message names the condition.",
        "Remove the claim from line 323 or test the message."),
    row("m7d-mutants-new-v07-v08", "2.6-mutants",
        "ledgers/M7/mutants/v07_starting_sector_cap_never_checked.py; v08_turnover_total_residual_sign_flipped.py", PASS,
        "v07 killed by test_named_condition_is_refused_with_value_error[start-within-sector-cap-invalid]; v08 killed by "
        "test_certificate_agrees_with_the_recomputed_residuals (seed 0)."),
    row("m7d-grader-run-graders", "2.6-grader",
        "tools/run_graders.py --unit M7 --seeds 0-49", PASS,
        "Output: 'run_graders M7: PASS (reference 50/50 seeds, slowest 1.2 s)'."),
    row("m7d-grader-mypy", "2.9-gates",
        "plans/M7-build-plan.md line 376 command; course/modules/M/M7/grader/test_project.py", PASS,
        "The plan command (MYPYPATH=...grader mypy --strict reference, instance, starter, tests/labs/M7/*.py) prints "
        "'Success: no issues found in 14 source files'. test_project.py under --strict with the solution present (MYPYPATH "
        "set to a workspace with constrained_allocator.py) prints 'Success: no issues found in 3 source files'. Round-1 FAIL "
        "was the absent solution module; the plan excludes test_project.py for that reason."),
    row("m7d-ruff", "2.9-gates",
        "tests/labs/M7; course/modules/M/M7/grader", PASS,
        "ruff check: All checks passed. ruff format --check: 15 files already formatted."),
    row("m7d-run-labs", "2.5-labs",
        "tools/run_labs.py --unit M7", PASS,
        "run_labs M7: PASS (11/11). Project twins 1, 3 and the completed twin 2 run under python -I -W error with output equal "
        "to the embedded blocks."),
    row("m7d-check-projects-pages-dag", "2.9-gates / DAG",
        "tools/check_projects.py, check_pages.py, check_dag.py --unit M7", PASS,
        "check_projects M7: PASS; check_pages M7: PASS; check_dag M7: PASS. Project page links only envelope-theorem (M2, in the "
        "closure, project.html line 450). No concept link outside the closure in project.html or cards.json (cards carry no links)."),
    row("m7d-page-smoke-project", "2.5-labs / browser",
        "tools/page_smoke.py --unit M7 --pages project", PASS,
        "page_smoke modules/M/M7/project.html: PASS; in-browser grader 'All 140 tests pass on seed 1666640586 (1.4 s)'."),
    row("m7d-pytest-M7", "2.9-gates",
        "pytest -k M7", PASS, "pytest -q -k M7 printed 12 passed (no failures)."),
    row("m7d-lab-numbers-cards-subset", "2.2-numbers / 2.7-cards",
        "course/modules/M/M7/cards.json (numeric claims); ledgers/M7/scripts/M7-d-r1/card_numbers.py", PASS,
        "Nine cards flagged by card_numbers.py carry fractions printed as \\tfrac in the lesson (checked: L03 Remark 4.3, "
        "L04 lines with 7/300, 199/150, 49/300, L05 Remark 2.4 with 11/4 and 18/11, L05 1/8 identity). Recomputed: c026 "
        "(lambda 2/3, w* (2/3, 1/3), min value 1/3); c048 and c053 (Sigma^-1 mu = (14/15, -11/30), sum 17/30); c060 "
        "(restricted dual grid gap 7/300, recomputed with Fractions: max -157/300 at nu -3/5 and -7/10); c064 (-199/300 = "
        "-0.6633); c080 (Q = [[4,1,0],[1,3,1],[0,1,2]] from the completed square, v'Qv = 19); c084 (midpoint identity "
        "f((x+y)/2) = (f(x)+f(y))/2 - (1/8)(x-y)'Q(x-y)); c093 (Lab 1 Part A lambda = (-36/19, 11/19)); c118 (L06 twin prints "
        "kkt_matches_closed_form True and budget_exact True per gamma); c016 (L01 twin: 2573 of 3125)."),
    row("m7d-cards-schema", "2.9-structure",
        "course/modules/M/M7/cards.json (147 cards)", PASS,
        "All 147 cards have a grade (111 T, 36 C); every C card has a basis; no card has a cite field now."),
    row("m7d-cards-grade-field", "2.3-grades / BUILDER_RULES 7",
        "course/modules/M/M7/cards.json", PASS,
        "Round-1 FAIL repaired: every card carries grade T or C. The C cards with a basis are checked for their basis text in "
        "m7d-cards-basis-stale-lab."),
    row("m7d-cards-duplicates", "2.7-cards / duplicate scan",
        "course/modules/M/M7/cards.json lines 124 (M7-c018) and 240 (M7-c034); lines 282 (M7-c040) and 375 (M7-c054)", FAIL,
        "Two pairs state the same result in the same lesson. M7-c018 ('State the necessity theorem for the Lagrange condition "
        "...', Theorem 2.2) and M7-c034 ('Key result: the Lagrange condition at a regular local minimizer ...', Theorem 2.2) "
        "give the same statement. M7-c040 ('What is the gradient inequality ... and what does it give at a zero gradient?', "
        "Lemma 1.4) and M7-c054 ('Key result: the gradient inequality ...', Lemma 1.4) give the same statement. Round-1 "
        "duplicates c125/c138 are gone (c138 removed); these two pairs were not caught before.",
        "Delete M7-c034 and M7-c054 (the 'Key result' cards); keep the question cards."),
    row("m7d-cards-basis-stale-lab", "2.7-cards / 2.2",
        "course/modules/M/M7/cards.json line 438 (M7-c063)", FAIL,
        "M7-c063 front says 'In Lab 1' but its basis field still says 'Lab 2 (exact arithmetic on the listed grids)'. "
        "course/modules/M/M7/L04.html contains no 'Lab 2' text (grep count 0); the L04 lab is 'Lab 1'.",
        "Change the basis to 'Lab 1 (exact arithmetic on the listed grids)'."),
    row("m7d-cards-cite-attribution", "2.1-citations",
        "course/modules/M/M7/cards.json (no cite fields; removed cards M7-c045 and M7-c066 cited boyd2004convex)", PASS,
        "grep for boyd, stokey and cite in cards.json returns nothing. The two cards that cited a source with no locator read "
        "were removed in this round. No attribution is left in a card."),
    row("m7d-cards-vs-lesson-text", "2.7-cards (full read)",
        "course/modules/M/M7/cards.json (147 cards) against L01-L08", UNV,
        "Not completed. Mechanical checks: every Definition/Theorem/Proposition/Lemma/Example/Remark/Problem/Lab label in a card "
        "appears in that card's own lesson (script check, 0 missing). Card-by-card reading against the lesson prose was done "
        "for the changed and new cards only: M7-c060, c069, c071, c142, c144, c145, c152, c160, c161 agree with the current "
        "lesson text, except the basis fault in m7d-cards-basis-stale-lab (c063). The other 130 cards were not read against "
        "their lesson prose in this round.",
        "Read every card against its lesson (or re-run this check with a full prose comparison) before the unit is passed."),
    row("m7d-registry-and-citations", "2.1-citations / registry",
        "course/modules/M/M7/project.html lines 459-460 (reading list); references/references.json lines 3648, 21295", PASS,
        "The reading list holds the registry keys boyd2004convex (references.json line 3648) and stokey1989recursive (line 21295) "
        "only, both read in this round. No locator is attributed on the project page; "
        "no external source was read in this round."),
    row("m7d-ruling-hours-pace", "hours",
        "course/modules/M/M7/project.html lines 341-347", PASS,
        "Only arithmetic was checked (architect ruling: pace is not a failure). Declared 33 h equals the rows; see m7d-spec-hours."),
]

MUTANT_LINE = re.compile(r"^(KILLED|SURVIVED) (\S+): (.*) -> (.*)$")


def mutants_from(path: Path) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MUTANT_LINE.match(line)
        if not match:
            continue
        state, name, description, killed = match.groups()
        found.append({
            "id": name,
            "description": description,
            "killed_by": None if state == "SURVIVED" else killed,
        })
    return found


def main() -> int:
    mutants = mutants_from(Path(sys.argv[1]))
    if len(mutants) != 32:
        raise SystemExit(f"expected 32 mutant lines, found {len(mutants)}")
    fragment = {
        "unit": "M7",
        "slice": "M7-d",
        "round": 2,
        "verifier": "Claude Haiku 5.5 (independent verifier, round 2, slice M7-d: project.html, grader, project labs, cards.json; did not build M7)",
        "pin": "1817191 (detached checkout /tmp/verifyB2-M7-d; round-1 pin c11ae01; delta c11ae01..1817191 covers project.html, grader/test_project.py, cards.json, L02/L04/L06/L08 twins, plan line 1 edit)",
        "base": "c11ae01",
        "checkout": "/tmp/verifyB2-M7-d",
        "scratch": "/tmp/M7-v/d-r2/",
        "verified_at": "2026-10-28",
        "verdict": "FAIL",
        "rows": ROWS,
        "mutants": mutants,
        "registry_flags": [],
        "freshness_flags": [],
        "notes": (
            "Round-2 delta re-verification. Commands run on the pin: run_graders M7 (50/50); mutate_graders M7 --seeds 0-49 "
            "(30 of 32 killed; survivors v05 and v06 are the FAIL rows); alternative routes (5 round-1 + 3 new) 50/50 each; "
            "witnesses hand-2e-9 and start-5e-9; collect-only 140 on seeds 0-49; starter run 137 failed; run_labs M7 11/11; "
            "page_smoke project PASS; check_projects, check_pages, check_dag PASS; ruff PASS; mypy plan command PASS; "
            "pytest -k M7 PASS. Not done: a full card-by-card read of all 147 cards against the lesson prose "
            "(m7d-cards-vs-lesson-text is UNVERIFIABLE); proof rows for L01-L08 are outside this slice; the external-source "
            "rows are not applicable (no source read this round). The sec.gov and bot-check issue does not arise."
        ),
        "summary": {},
    }
    counts: dict[str, int] = {}
    for item in ROWS:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    fragment["summary"] = {
        "rows": len(ROWS),
        "pass": counts.get(PASS, 0),
        "fail": counts.get(FAIL, 0),
        "unverifiable": counts.get(UNV, 0),
        "mutants": len(mutants),
        "mutants_survived": sum(1 for m in mutants if not m["killed_by"]),
    }
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} rows={len(ROWS)} counts={counts} mutants={len(mutants)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
