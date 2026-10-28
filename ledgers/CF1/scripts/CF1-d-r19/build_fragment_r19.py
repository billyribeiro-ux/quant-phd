"""Build ledgers/CF1/CF1-d.json (round 19, slice d) from the round-18 fragment, the round-19 delta and the outputs.

Every round-18 row id is kept. Rows whose cited subject changed in the round-19 delta (project.html lines 186, 192,
213, 428; L06.html lines 211, 327, 364, 366; grader/test_project.py test bodies; cards.json CF1-c096) are re-verified
and overridden below; every other PASS row is carried with the required prefix. Run with the checkout as argv[1].
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/CF1-d.round18.json").read_text(encoding="utf-8"))
OUT = root / "ledgers/CF1/scripts/CF1-d-r19/out"
CARRY = "Carried from round 18 ({files} cited subject byte-identical since the previous pin 7143726; line numbers may have moved after the round-19 hunks listed in notes): "
FILES_NOTE = "course/modules/CF/CF1/project.html lines 186, 192, 213, 428 and L06.html lines 211, 327, 364, 366 and cards.json CF1-c096 changed"

# ---- re-verified rows (status and evidence are this round's) ----
over: dict[str, dict[str, str]] = {}


def set_row(rid: str, status: str, evidence: str, fix: str = "", location: str | None = None) -> None:
    over[rid] = {"status": status, "evidence": evidence, "fix": fix, "location": location or ""}


set_row(
    "proj-named-errors-nonfinite-rate-untested",
    "PASS",
    "Round 19: project.html line 213 names a rate that is not finite (nan or infinity) in an NPV, a discounted payback, "
    "a Fisher conversion and a Monte Carlo request. The round-19 grader covers each: NPV test_project.py line 112 "
    "(nan, inf); discounted payback test_payback_rejects_a_discount_rate_that_is_not_finite lines 437-442; Fisher "
    "test_fisher_rejects_a_rate_that_is_not_finite lines 475-481 (real and inflation, nan and inf); Monte Carlo "
    "test_monte_carlo_refuses_a_rate_that_is_not_finite lines 906-912. Reference passes 154/154 on seeds 0-49 "
    "(run_graders CF1 PASS 50/50). Round-18 survivors d18_m01 and d18_m02 are now KILLED (mutate_r19_final.out).",
    location="course/modules/CF/CF1/project.html line 213; course/modules/CF/CF1/grader/test_project.py lines 112, 437-442, 475-481, 906-912",
)
set_row(
    "proj-inputs-missing-space-inflation",
    "PASS",
    "Round 19: project.html line 186 now reads '...at least 0 and below 1. <code>inflation</code>: above −1.' (a space "
    "after the full stop, checked by reading the line). page_smoke CF1 PASS (zero console errors, unrendered math).",
    location="course/modules/CF/CF1/project.html line 186",
)
set_row(
    "cards-c096-grade-t-on-convention",
    "PASS",
    "Round 19: cards.json CF1-c096 is now grade 'C', basis 'convention, Definition 1.1 (linear interpolation inside the "
    "payback year)'. L05.html Definition 1.1 (lines 58-62) says the interpolation 'is a convention, and it is not a "
    "finding'; the course grade legend (L01.html line 46, L02.html line 46) lists 'C single study or convention'. The "
    "back text matches the Definition 1.1 formula in L05.html.",
    location="course/modules/CF/CF1/cards.json CF1-c096; course/modules/CF/CF1/L05.html lines 58-62",
)
set_row(
    "cards-grade-semantics",
    "FAIL",
    "Round 19: CF1-c096 is fixed (C, convention basis). Reading the basis field of all 77 T cards found 17 more cards "
    "graded T whose basis is a Definition, the same defect class: a definition is not a theorem proved on the page "
    "(BLUEPRINT section 3, T = 'Theorem: proved on the page'). They are listed in cards-definition-basis-graded-t.",
    fix="See cards-definition-basis-graded-t: regrade the 17 definition cards to C with a convention basis.",
    location="course/modules/CF/CF1/cards.json",
)
set_row(
    "cards-changed-r17-c056-c096",
    "PASS",
    "Round 19: CF1-c056 unchanged (grade C, basis 'Lab 1 (SIMULATED cash flows)', agrees with the lab's two roots 0.1 and "
    "0.2, see proj-two-root-witness). CF1-c096 now C with a convention basis matching L05.html Definition 1.1; the round-18 "
    "T grade is withdrawn.",
    location="course/modules/CF/CF1/cards.json CF1-c056, CF1-c096",
)
set_row(
    "lesson-l06-rewrites",
    "PASS",
    "Round 19 re-verified the three rewritten sentences at their current lines (the round-18 line numbers 129, 138, 147 are "
    "stale: the file is 465 lines and the text moved). Section 3 (L06.html line 211): the printed quantiles 14896.62, "
    "79457.94, 143406.13 match the lab output; the unrounded quantiles 14896.623057 and 143406.126569 and their difference "
    "128509.5035 were reproduced by re-running the twin's own quantile and draw code without its print step "
    "(ledgers/CF1/scripts/CF1-d-r19/recompute_l06_section3.py, out/recompute_l06_section3.out); the 0.0065 gap is "
    "128509.51 − 128509.5035. The solution at line 327 says 'from the re-run described in Section 3', matching. The "
    "misconception at line 240 and the E2 solution at line 320 (0.0552 ± 1.96 × 0.0010 = 0.05324 to 0.05716, printed "
    "0.0532 to 0.0572) recomputed. The one open defect in this area is the Remark 2.4 scope sentence at line 106, "
    "row lesson-l06-remark-2-4-each-result-conditional.",
    location="course/modules/CF/CF1/L06.html lines 211, 240, 320, 327",
)
set_row(
    "proj-mutants-round18-new",
    "PASS",
    "Round 19 re-run of the round-18 mutants: d18_m01 (payback nan rate) KILLED by "
    "test_payback_rejects_a_discount_rate_that_is_not_finite[nan]; d18_m02 (Fisher nan inflation) KILLED by "
    "test_fisher_rejects_a_rate_that_is_not_finite[inflation-nan]; d18_m04 KILLED by "
    "test_fisher_rejects_rates_at_or_below_minus_one[inflation-minus-one]. d18_m03 remains archived as equivalent "
    "(proj-equivalent-d18-m03). Source: ledgers/CF1/scripts/CF1-d-r19/out/mutate_r19_final.out.",
    location="ledgers/CF1/mutants/d18_m01..d18_m04",
)
set_row(
    "cmd-mutate-graders-r18",
    "PASS",
    "Round 19 full run tools/mutate_graders.py --unit CF1 --seeds 0-9 over all 173 mutants in ledgers/CF1/mutants/ "
    "(ledgers/CF1/scripts/CF1-d-r19/out/mutate_r19_final.out): the 157 round-18 files are all KILLED, including d18_m01 "
    "and d18_m02. The only survivor of the full run is d19_m01 (row proj-mutant-d19-m01-irr-zero-outlay-refused).",
    location="ledgers/CF1/mutants/*.py",
)
set_row(
    "proj-mutants-killed",
    "FAIL",
    "Round 19: 'tools/mutate_graders.py --unit CF1 --seeds 0-9' printed 'mutate_graders CF1: FAIL (172/173 killed)' on "
    "173 mutants. The one survivor is d19_m01_irr_zero_outlay_only_refused.py (an IRR request [-100, 0] is refused; the "
    "reference returns []). Output: ledgers/CF1/scripts/CF1-d-r19/out/mutate_r19_final.out, line 4 SURVIVED.",
    fix="Add to grader/test_project.py a test asserting irr_roots([-100.0, 0.0]) == [] with the message that only all-zero "
    "flows are refused and that the NPV is -100 at every rate, so it has no root. The reference passes it.",
    location="ledgers/CF1/mutants/*.py (173 files); tools/mutate_graders.py --unit CF1 --seeds 0-9",
)
set_row(
    "lesson-l06-remark-2-4-each-result-conditional",
    "FAIL",
    "Re-verified in round 19: L06.html line 106 (Remark 2.4) is unchanged since 7143726 and still says 'the two exercises "
    "that apply it (E1 and E2) label each result as conditional on that reading'. E1 (L06.html lines 309-314) gives three "
    "results: the error 84543.40 − 79078.68 = 5464.72 cents, the number of standard errors 5464.72 / 4400.22 = 1.2419 "
    "(recomputed, out/recompute_l06_section3.out), and the two-sided tail 0.2143. Only the tail is labelled 'under that "
    "reading'. The cents error and the standard-error count are arithmetic on printed values and need no normal reading, "
    "so the sentence overstates the labelling. E2 labels its band as conditional, which is correct.",
    fix="Change Remark 2.4 to say that E1 and E2 label the normal-based probability and band as conditional on that "
    "reading (the cents error and the standard-error count need no normal reading).",
    location="course/modules/CF/CF1/L06.html line 106; E1 solution lines 312-314",
)

# ---- round-19 delta rows that were PASS before and whose subject changed: re-verified ----
set_row(
    "proj-test-count-72",
    "PASS",
    "Round 19: project.html line 192 states 'collects 154 checks'. pytest --collect-only on the reference solution "
    "(copy as capbudget.py in /tmp/CF1-v/d19/ref) gives 154 on every seed 0-49 (out/run_graders.out; collect loop 50 x 154).",
    location="course/modules/CF/CF1/project.html line 192; course/modules/CF/CF1/grader/test_project.py",
)
set_row(
    "proj-spec-count-118-hub",
    "PASS",
    "Round 19: the grading-mode count is 154 (project.html line 192), equal to the collected count on the reference "
    "for all seeds 0-49.",
    location="course/modules/CF/CF1/project.html line 192",
)
set_row(
    "proj-count-cause-wording",
    "PASS",
    "Round 19: line 192 says the count does not depend on the seed because no parametrize list's length depends on the seed. "
    "Every parametrize list in test_project.py is a literal list (grep for parametrize arguments found no seed or instance "
    "input); the 50-seed collect gives 154 throughout.",
    location="course/modules/CF/CF1/project.html line 192; course/modules/CF/CF1/grader/test_project.py",
)
set_row(
    "proj-collect-count-50-seeds",
    "PASS",
    "Round 19: pytest --collect-only for QF_SEED 0..49 on the reference gives 154 on all 50 seeds; the suite passes "
    "154/154 with -W error --assert=plain (run_graders CF1 50/50).",
    location="course/modules/CF/CF1/grader/test_project.py; course/modules/CF/CF1/project.html line 192",
)
set_row(
    "r13-collect-count-126",
    "PASS",
    "Round 19 (row kept from round 13; its count has been updated): the page now states 154 (project.html line 192), and "
    "the collect count is 154 on seeds 0-49. The 126 of round 13 is historical.",
    location="course/modules/CF/CF1/project.html line 192",
)
set_row(
    "r15-page-count-138",
    "PASS",
    "Round 19 (row kept from round 15; count updated): project.html line 192 now says 154, and collect-only on the reference "
    "gives 154. The 138 of round 15 is historical.",
    location="course/modules/CF/CF1/project.html line 192",
)
set_row(
    "r16-collect-count-138",
    "PASS",
    "Round 19 (row kept from round 16; count updated): collect-only on the reference gives 154 for seeds 0-49, matching "
    "project.html line 192.",
    location="course/modules/CF/CF1/grader/test_project.py; course/modules/CF/CF1/project.html line 192",
)
set_row(
    "proj-page-round18-count-sentence",
    "PASS",
    "Round 19: project.html lines 186 and 192 re-read. Line 186 has the space fix; line 192 states 154 checks, verified "
    "by collect-only on the reference.",
    location="course/modules/CF/CF1/project.html lines 186, 192",
)
set_row(
    "proj-npv-empty-overconstraint",
    "PASS",
    "Round 19: line 213 names 'an NPV over an empty list of flows' as a named error; test_npv_rejects_empty_flows (line 117) "
    "requires ValueError, and the reference raises for an empty list. Over-constraint check: the alternatives of round 19 "
    "(Horner NPV, alt_d19_a) raise for an empty list too, and every alternative passes 10 seeds.",
    location="course/modules/CF/CF1/project.html line 213; course/modules/CF/CF1/grader/test_project.py line 117",
)
set_row(
    "proj-named-errors-tax-share-one",
    "PASS",
    "Round 19: line 213 says a tax rate at or above 1 and a working-capital share at or above 1 are refused, and 0 is valid. "
    "Tests tax-one (test_project.py line 632), share-one (line 634), test_tax_rate_of_zero_alone_is_valid (line 702), "
    "test_working_capital_share_of_zero_is_valid (line 712) cover each clause.",
    location="course/modules/CF/CF1/project.html line 213; course/modules/CF/CF1/grader/test_project.py lines 632-712",
)
set_row(
    "proj-exemplar-b-locator",
    "PASS",
    "Round 19: Exemplar B, 2 Cash flows annotation (project.html line 428) now reads 'each flow from year 1 includes the "
    "shield, and the year-3 flow includes the working-capital recovery'. Lab 1 step 3 prints a shield of 750.00 in years 1-3 "
    "and a year-3 working-capital flow of 650.00; the statement is true of the printed numbers.",
    location="course/modules/CF/CF1/project.html line 428",
)
set_row(
    "proj-new-grader-tests-r18",
    "PASS",
    "Round 19: the round-18 payback first-flow case [1e-9, 10.0] is still in the parametrize list (test_project.py line 422); "
    "the test bodies are unchanged, only line numbers moved after the round-19 additions.",
    location="course/modules/CF/CF1/grader/test_project.py lines 420-426",
)
set_row(
    "r13-l06-unrounded-difference-basis",
    "PASS",
    "Round 19: L06.html lines 211, 327 re-verified (see lesson-l06-rewrites: the unrounded difference 128509.5035 is "
    "reproduced by re-running the twin's own code). The rounding statement at line 211 is correct.",
    location="course/modules/CF/CF1/L06.html lines 211, 327",
)
set_row(
    "r16-l06-line66-and-section3-share-se",
    "PASS",
    "Round 19: L06.html lines 63 and 66 unchanged; line 211 re-read: the share 0.0552 with standard error 0.0010 from "
    "sqrt(p(1-p)/n) at the estimated p. Recomputed: sqrt(0.05522 × 0.94478 / 50000) = 0.00102 at the unrounded share, "
    "printed 0.0010 by the lab.",
    location="course/modules/CF/CF1/L06.html lines 63, 66, 211",
)
set_row(
    "proj-exemplar-numbers",
    "PASS",
    "Round 19: Exemplar B figures recomputed: 926.00 − 885.85 = 40.15; 40.15 / 54.68 = 0.734 (0.73); 787 / 2000 = 39.35 "
    "percent; 2,445.52 / 885.85 = 2.761 (2.76); E[exp(0.2z)] = exp(0.02) by the lognormal mean. The Lab 3 values "
    "885.85, 2,445.52, 54.68, 787 and 926.00 are in its embedded expected block (MATCH, project_labs_isolated.out).",
    location="course/modules/CF/CF1/project.html lines 400-440",
)
set_row(
    "proj-banned-phrases",
    "PASS",
    "Round 19 re-scan of project.html, cards.json and the changed L06 lines: no 'roughly half', 'about 6%', 'historically', "
    "ellipsis, or process word. L06.html line 111 contains 'roughly as the square root of n', which is not one of the banned "
    "examples named in the brief ('roughly half', 'about 6%', 'historically', an ellipsis).",
    location="course/modules/CF/CF1/project.html; course/modules/CF/CF1/cards.json",
)
set_row(
    "proj-process-words-r10",
    "PASS",
    "Round 19 re-scan of project.html and cards.json for 'round ', 'builder', 'verifier', 'REQUEST' and 'unit report': none.",
    location="course/modules/CF/CF1/project.html; course/modules/CF/CF1/cards.json",
)
set_row(
    "r15-banned-phrase-scan",
    "PASS",
    "Round 19 re-scan of cards.json: no banned phrase or ellipsis (see proj-banned-phrases).",
    location="course/modules/CF/CF1/cards.json",
)
set_row(
    "r16-banned-process-words-scan",
    "PASS",
    "Round 19 re-scan of cards.json and project.html for process words: none.",
    location="course/modules/CF/CF1/cards.json; course/modules/CF/CF1/project.html",
)
set_row(
    "cards-missing-grade-or-basis",
    "PASS",
    "Round 19 re-run: 109 cards; every card has a grade in {T, C} and a non-empty basis (script in scratch; output "
    "unchanged apart from CF1-c096).",
    location="course/modules/CF/CF1/cards.json",
)
set_row(
    "cards-duplicate-scan",
    "PASS",
    "Round 19 re-run: no duplicate ids, fronts or backs across the 109 cards.",
    location="course/modules/CF/CF1/cards.json",
)
set_row(
    "cards-numbers-in-lesson",
    "PASS",
    "Round 19: the only changed card (CF1-c096) contains no number; every other card is byte-identical since 7143726.",
    location="course/modules/CF/CF1/cards.json",
)
set_row(
    "cards-count-vs-plan",
    "PASS",
    "Round 19: 109 cards (77 T, 32 C); plans/CF1-build-plan.md is unchanged in the CF1 slice, so the plan's card count "
    "still matches.",
    location="course/modules/CF/CF1/cards.json",
)
set_row(
    "proj-structure-and-gates",
    "PASS",
    "Round 19: check_projects --all PASS (CF1 PASS); check_pages CF1 PASS; check_dag --all PASS (ledgers/CF1/scripts/CF1-d-r19/out/).",
    location="tools/check_projects.py --all; tools/check_pages.py --unit CF1; tools/check_dag.py --all",
)
set_row(
    "proj-pytest-lab-helper",
    "PASS",
    "Round 19: run_labs --unit CF1 9/9 PASS; the three project twins run under python -I -W error with exit 0 "
    "(project_labs_isolated.out); their stdout equals the embedded expected blocks of project.html (checked by "
    "comparing each lab's stdout with the pre.expected block, all three MATCH).",
    location="tests/labs/CF1/lab-CF1-project-1..3.py; course/modules/CF/CF1/project.html",
)
set_row(
    "proj-grader-reference-50-seeds",
    "PASS",
    "Round 19: run_graders --unit CF1 --seeds 0-49: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.4 s)'.",
    location="course/modules/CF/CF1/grader/reference.py; tools/run_graders.py --unit CF1 --seeds 0-49",
)
set_row(
    "proj-page-smoke",
    "PASS",
    "Round 19: tools/page_smoke.py --unit CF1 --pages project.html: 'page_smoke CF1: PASS' (exit 0).",
    location="course/modules/CF/CF1/project.html; tools/page_smoke.py --unit CF1",
)
set_row(
    "proj-verify-refs",
    "PASS",
    "Round 19: verify_refs --offline: 560 entries, 0 problems; verify_refs --unit CF1 live: 2 of 560 entries, 0 problems. "
    "references/references.json is unchanged in 7143726..51fa336.",
    location="references/references.json; tools/verify_refs.py",
)
set_row(
    "cmd-verify-refs-live-r17",
    "PASS",
    "Round 19 re-run: verify_refs --unit CF1 live, 2 of 560 entries, 0 problems.",
    location="tools/verify_refs.py --unit CF1",
)
set_row(
    "r16-live-registry-refs",
    "PASS",
    "Round 19 re-run: references/references.json unchanged; verify_refs offline 560/0 and live CF1 2/0.",
    location="references/references.json; tools/verify_refs.py",
)
set_row(
    "proj-check-dag",
    "PASS",
    "Round 19: check_dag --all PASS (AC2, AC4, CF1, AP1).",
    location="tools/check_dag.py --all",
)
set_row(
    "proj-ruff-format",
    "PASS",
    "Round 19: ruff check and ruff format --check on course/modules/CF/CF1/grader and tests/labs/CF1: 'All checks passed!' "
    "and '13 files already formatted' (ledgers/CF1/scripts/CF1-d-r19/out/ruff_check.out).",
    location="course/modules/CF/CF1/grader; tests/labs/CF1",
)
set_row(
    "proj-mypy-grader-gate",
    "PASS",
    "Round 19: mypy --strict --no-incremental on the reference (as capbudget.py), instance.py and test_project.py: "
    "'Success: no issues found in 3 source files' (ledgers/CF1/scripts/CF1-d-r19/out/mypy_grader.out).",
    location="course/modules/CF/CF1/grader/*.py",
)
set_row(
    "proj-lab-twins-isolated-r18",
    "PASS",
    "Round 19 re-run: the three project twins under python -I -W error exit 0 (project_labs_isolated.out).",
    location="tests/labs/CF1/lab-CF1-project-1.py, lab-CF1-project-2.py, lab-CF1-project-3.py",
)
set_row(
    "cmd-gates-r18",
    "PASS",
    "Round 19 re-run of the round-18 gates: check_projects, check_pages, check_dag, run_labs, run_graders, page_smoke, "
    "mypy, ruff, verify_refs all PASS (ledgers/CF1/scripts/CF1-d-r19/out/).",
    location="ledgers/CF1/scripts/CF1-d-r19/out/",
)
set_row(
    "proj-alternatives-round18-new",
    "PASS",
    "Round 19 re-run of alt_d18_1, alt_d18_2, alt_d18_3 over seeds 0-9: PASS (alts_all_r19_seeds0-9.out).",
    location="ledgers/CF1/scripts/CF1-d-r18/alts/",
)
set_row(
    "proj-alternatives-rerun-all-prior-r18",
    "PASS",
    "Round 19 re-run of all 56 alternative engines in ledgers/CF1/scripts/CF1-d-r*/alts/ (rounds 7-18) and the three "
    "round-19 engines over seeds 0-9: every engine passes the 154-test suite on every seed (alts_all_r19_seeds0-9.out).",
    location="ledgers/CF1/scripts/CF1-d-r*/alts/",
)
set_row(
    "proj-equivalent-d18-m03",
    "PASS",
    "Carried from round 18: ledgers/CF1/scripts/CF1-d-r18/make_mutants.py writes d18_m03 (Monte Carlo with an inline NPV and "
    "no guard on the rate); npv() inside npv_monte_carlo still raises for nan, so the mutant is equivalent. The file is not "
    "in ledgers/CF1/mutants/. Carried from round 18 (make_mutants.py unchanged since 7143726).",
    location="ledgers/CF1/scripts/CF1-d-r18/make_mutants.py",
)

# ---- new rows ----
new_rows = [
    {
        "id": "cards-definition-basis-graded-t",
        "check": "cards: grade semantics (BLUEPRINT section 3: T = theorem proved on the page; a definition is a convention, graded C as in the round-18 ruling for CF1-c096)",
        "location": "course/modules/CF/CF1/cards.json CF1-c001, c018, c021, c024, c033, c034, c035, c047, c048, c049, c062, c063, c075, c076, c088, c099, c100 (grade T, basis 'Definition ...'); course/modules/CF/CF1/L01.html line 46 (grade legend: 'C single study or convention')",
        "status": "FAIL",
        "evidence": "Reading the basis field of all 77 T cards: 17 have a basis that is a Definition (Definitions 1.1, 1.2, 2.1, 3.1 in L01 to L06). Their backs state definitions, e.g. CF1-c001 'Flows fall at period ends, a convention of Section 1 (Definition 1.1)'; CF1-c034 'It is an exact definition of the real rate for a given inflation rate'. A definition is not a theorem proved on the page (BLUEPRINT.md line 158: 'T | Theorem: proved on the page'). The round-18 ruling graded CF1-c096, the same kind of card, C. The other T cards have proof bases (Proposition, Theorem, Corollary), computed examples (Example 1.2, 1.4, 4.2: exact arithmetic on the page), Problems with solutions on the page, or misconception answers that cite a Proposition; those were read and are not flagged.",
        "fix": "Regrade CF1-c001, c018, c021, c024, c033, c034, c035, c047, c048, c049, c062, c063, c075, c076, c088, c099 and c100 to grade 'C' with a basis such as 'convention, Definition x.y', or keep T only where the card's answer is a proved proposition rather than the definition itself.",
    },
    {
        "id": "proj-mutant-d19-m01-irr-zero-outlay-refused",
        "check": "2.5 / mutation: a student-error mutant that refuses a request the page does not refuse",
        "location": "ledgers/CF1/mutants/d19_m01_irr_zero_outlay_only_refused.py; course/modules/CF/CF1/project.html line 206 (IRR roots bullet), line 213 (named errors: IRR refused only for every flow zero)",
        "status": "FAIL",
        "evidence": "Round 19 mutant: irr_roots raises when all(cf == 0 for cf in flows[1:]) (the outlay is skipped). It "
        "SURVIVED seeds 0-9 (ledgers/CF1/scripts/CF1-d-r19/out/mutate_r19_final.out line 4). Witness: the reference returns "
        "irr_roots([-100.0, 0.0]) == [] (NPV is -100 at every rate, so no root), and the mutant raises. On seed 3 the mutant "
        "passes all 154 tests (run in /tmp/CF1-v/d19/m01). No test calls irr_roots with an outlay followed only by zeros: "
        "test_irr_rejects_all_zero_flows (line 285) uses all-zero lists and test_irr_accepts_some_zero_flows (line 290) uses "
        "[0, 5]. project.html line 206 defines IRR roots as the rates where the NPV is zero, and line 190 says the conventions "
        "define the numbers the engine returns, so the refusal is not a named error for this request.",
        "fix": "Add to grader/test_project.py a test: assert irr_roots([-100.0, 0.0]) == [] with the message that only "
        "all-zero flows are refused, and that the NPV is -100 at every rate so it has no root. The reference passes it.",
        "verdict_note": "student error: refusing an outlay with zero inflows",
    },
    {
        "id": "proj-mutants-round19-new",
        "check": "2.5 / mutation: the five other round-19 student-error mutants are killed",
        "location": "ledgers/CF1/mutants/d19_m02..d19_m06",
        "status": "PASS",
        "evidence": "d19_m02 (IRR with a zero first flow refused) KILLED by test_irr_accepts_some_zero_flows_when_not_all_are_zero (seed 0); d19_m03 (discounted payback exponent t-1) KILLED by test_discounted_payback_uses_discounted_flows (seed 0); d19_m04 (NPV refuses rate above 1) KILLED by test_npv_reads_a_rate_above_one_as_a_decimal_per_year (seed 0); d19_m05 (Monte Carlo refuses zero volatility) KILLED by test_monte_carlo_with_zero_volatility_is_the_deterministic_npv (seed 0); d19_m06 (Fisher adds the rates) KILLED by test_fisher_round_trip_is_exact (seed 0). Output: out/mutate_r19_final.out.",
        "fix": "",
    },
    {
        "id": "proj-grader-delta-tests-r19",
        "check": "2.6 / 2.9: the round-19 grader additions test what the page states",
        "location": "course/modules/CF/CF1/grader/test_project.py lines 296-301, 379-384, 437-442, 475-481, 906-912 (additions); 420-426 (parametrize extended)",
        "status": "PASS",
        "evidence": "Eleven new cases, each checked against the spec: [0, 0, 5] has no root (NPV 5/(1+r)^2 never changes sign; line 296); [-100, 0, 100] payback 2 (the zero year is kept; line 379); payback first flow nan (line 422); payback rate nan and inf (437-442); Fisher real/inflation nan and inf (475-481); Monte Carlo rate nan and inf (906-912). Every new expectation is a value the conventions of project.html (lines 189-214) define; each new refusal is a named error at line 213. The reference passes all of them (154/154 on seeds 0-49).",
        "fix": "",
    },
    {
        "id": "proj-alternatives-round19-new",
        "check": "2.6 / over-constraint: three new correct engines pass the suite",
        "location": "ledgers/CF1/scripts/CF1-d-r19/alts/alt_d19_a_horner_npv.py, alt_d19_b_fisher_logarithms.py, alt_d19_c_monte_carlo_affine.py",
        "status": "PASS",
        "evidence": "alt_d19_a: NPV by Horner's rule from the last flow back to the outlay; alt_d19_b: Fisher as expm1(log1p(r) + log1p(pi)); alt_d19_c: Monte Carlo by the affine identity NPV(m) = NPV(0) + m (NPV(1) - NPV(0)) on the same seeded draws. Each passes the 154-test suite on seeds 0-9 (alts_all_r19_seeds0-9.out). The 4001-point log grid, the window and the validation are kept.",
        "fix": "",
    },
    {
        "id": "proj-alternatives-rerun-all-r19",
        "check": "2.6 / over-constraint: every earlier alternative still passes",
        "location": "ledgers/CF1/scripts/CF1-d-r*/alts/*.py (rounds 7-18, 56 engines in total with the three of round 19; ref_reference.py included)",
        "status": "PASS",
        "evidence": "run_alts.py over seeds 0-9: 'PASS (10 seeds)' for every engine (alts_all_r19_seeds0-9.out). Scope: seeds 0-9 only (the 50-seed run was done for the reference); the engines do not read the seed except through the Monte Carlo draws.",
        "fix": "",
    },
    {
        "id": "proj-delta-coverage-r19",
        "check": "2.9: every changed hunk of this slice was read",
        "location": "git diff --stat 7143726 51fa336 -- course/modules/CF/CF1 tests/labs/CF1 ledgers/CF1/mutants",
        "status": "PASS",
        "evidence": "Changed slice files: project.html (hunks at lines 186, 192, 213, 428), cards.json (CF1-c096 only), grader/test_project.py (six hunks: 293-300, 369-380, 405-425, 434-450, 472-486, 903-915), L06.html (lines 211, 327, 364, 366; these are the lesson slice but were re-read because the round-18 fragment cites them). tests/labs/CF1 unchanged. The 19 mutant files added by the delta are included in the 173-file run (172 killed; d19_m01 is the round-19 survivor). Every hunk was read.",
        "fix": "",
    },
    {
        "id": "proj-named-errors-coverage-r19",
        "check": "2.9 / 1.4: each named error on project.html line 213 maps to a test id",
        "location": "course/modules/CF/CF1/project.html line 213; course/modules/CF/CF1/grader/test_project.py",
        "status": "PASS",
        "evidence": "Clauses mapped: capex float/bool/text (capex-float line 610, capex-bool 654, capex-text 655); life 0 and fractional (life-zero 612, life-fractional 636, life-negative 656); revenue/cost lists wrong length, negative, nan, inf (revenue-length, cost-negative, revenue-nan, cost-inf etc., lines 604-680); tax and share at or above 1 and below 0 (tax-one 632, share-one 634, tax-negative 633, share-negative 635, tax-above-one 665, share-above-one 666); inflation at or below -1 (647-653); rate not finite or at or below -1 in NPV (112-113), discounted payback (429-442), Fisher (466-481), Monte Carlo (898-912); empty NPV (117); IRR fewer than two flows and all-zero (280-286); payback fewer than two flows (415-416) and first flow not an outlay (420-426); Monte Carlo fewer than two draws (887-891) and negative volatility (922-924); missing field (681-684). Just-inside values: payback -0.999 (359-365), first flow -1e-9 (367-372), Fisher -0.999 (484-489), Monte Carlo -0.999 (914-919): each returns a value.",
        "fix": "",
    },
    {
        "id": "proj-l06-table-rows-r19",
        "check": "2.4 / 2.9: rewritten Proposition rows in the L06 result table match the propositions",
        "location": "course/modules/CF/CF1/L06.html lines 364, 366; Proposition 2.1 (line 71-73) and Proposition 2.3 (line 91-93)",
        "status": "PASS",
        "evidence": "Row 364 'the standard error of the sample mean of n independent, identically distributed draws with variance sigma^2 is sigma/sqrt(n) (Proposition 2.1)' matches Proposition 2.1 (iid, finite variance, Var = sigma^2/n). Row 366 'for independent receipts with a common mean mu and a common variance sigma^2' matches Proposition 2.3 (lines 92-93: receipts independent, X_t has mean mu and variance sigma^2). Both are T with 'Proved in §2'.",
        "fix": "",
    },
    {
        "id": "cards-c096-r19",
        "check": "cards: CF1-c096 front, back, grade and basis agree with the lesson",
        "location": "course/modules/CF/CF1/cards.json CF1-c096; course/modules/CF/CF1/L05.html lines 58-62 and 111",
        "status": "PASS",
        "evidence": "Front 'How is the fractional simple payback computed?'; back 'linear interpolation inside the payback year: (tau_S - 1) + (-CUM_(tau_S - 1)) / C_(tau_S) (Definition 1.1)' equals the L05 Definition 1.1 formula; grade C, basis 'convention, Definition 1.1 (linear interpolation inside the payback year)' matches L05 line 111 ('The payback convention is linear interpolation inside the year...').",
        "fix": "",
    },
    {
        "id": "cards-count-r19",
        "check": "cards: 109 entries, grade counts",
        "location": "course/modules/CF/CF1/cards.json",
        "status": "PASS",
        "evidence": "python json check: 109 entries; 77 T and 32 C; no duplicate ids, fronts or backs; no missing grade or basis. Grades changed in the delta: CF1-c096 only (T to C).",
        "fix": "",
    },
    {
        "id": "cmd-run-graders-r19",
        "check": "2.5 command: tools/run_graders.py --unit CF1 --seeds 0-49",
        "location": "course/modules/CF/CF1/grader/reference.py; tools/run_graders.py",
        "status": "PASS",
        "evidence": "'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.4 s)' (ledgers/CF1/scripts/CF1-d-r19/out/run_graders.out).",
        "fix": "",
    },
    {
        "id": "cmd-run-labs-r19",
        "check": "2.5 command: tools/run_labs.py --unit CF1",
        "location": "tests/labs/CF1/*.py",
        "status": "PASS",
        "evidence": "'run_labs CF1: PASS (9/9)' (ledgers/CF1/scripts/CF1-d-r19/out/run_labs.out).",
        "fix": "",
    },
    {
        "id": "cmd-mutate-graders-r19",
        "check": "2.5 command: tools/mutate_graders.py --unit CF1 --seeds 0-9 (all mutants in ledgers/CF1/mutants/)",
        "location": "ledgers/CF1/mutants/*.py (173 files); ledgers/CF1/scripts/CF1-d-r19/out/mutate_r19_final.out",
        "status": "FAIL",
        "evidence": "Observed last line: 'mutate_graders CF1: FAIL (172/173 killed)'. The survivor is d19_m01_irr_zero_outlay_only_refused.py. The other 172 are KILLED.",
        "fix": "See proj-mutant-d19-m01-irr-zero-outlay-refused: add the irr_roots([-100.0, 0.0]) == [] test.",
    },
    {
        "id": "cmd-check-gates-r19",
        "check": "2.5 command: check_projects --all, check_pages --unit CF1, check_dag --all",
        "location": "tools/check_projects.py, tools/check_pages.py, tools/check_dag.py",
        "status": "PASS",
        "evidence": "check_projects --all: CF1 PASS (exit 0); check_pages --unit CF1: PASS (exit 0); check_dag --all: PASS (exit 0). Outputs in ledgers/CF1/scripts/CF1-d-r19/out/.",
        "fix": "",
    },
    {
        "id": "cmd-verify-refs-r19",
        "check": "2.1 command: verify_refs offline and live",
        "location": "references/references.json; tools/verify_refs.py",
        "status": "PASS",
        "evidence": "verify_refs --offline: 'offline integrity: 560 entries, 0 problems'; verify_refs --unit CF1: 'live re-verification of CF1: 2 of 560 entries, 0 problems'.",
        "fix": "",
    },
    {
        "id": "proj-collect-154-r19",
        "check": "2.9: the page's collect count equals the real collect-only count",
        "location": "course/modules/CF/CF1/project.html line 192; course/modules/CF/CF1/grader/test_project.py",
        "status": "PASS",
        "evidence": "pytest --co on the reference for QF_SEED 0..49: 154 on each seed (50 of 50). The page says 154.",
        "fix": "",
    },
    {
        "id": "proj-lab-twins-r19",
        "check": "2.5 labs: project twins isolated; embedded expected blocks equal their stdout",
        "location": "tests/labs/CF1/lab-CF1-project-1.py, -2.py, -3.py; course/modules/CF/CF1/project.html expected blocks",
        "status": "PASS",
        "evidence": "python -I -W error on each twin: exit 0. Stdout compared with the three pre.expected blocks in project.html: MATCH, MATCH, MATCH.",
        "fix": "",
    },
    {
        "id": "proj-gates-ruff-mypy-r19",
        "check": "2.5 command: ruff and mypy for the grader and the labs",
        "location": "course/modules/CF/CF1/grader; tests/labs/CF1",
        "status": "PASS",
        "evidence": "ruff check: 'All checks passed!'; ruff format --check: '13 files already formatted'; mypy --strict --no-incremental on the grader trio: 'Success: no issues found in 3 source files'.",
        "fix": "",
    },
    {
        "id": "proj-page-smoke-r19",
        "check": "2.5 command: page_smoke for the project page",
        "location": "course/modules/CF/CF1/project.html; tools/page_smoke.py --unit CF1",
        "status": "PASS",
        "evidence": "'page_smoke CF1: PASS', exit 0 (ledgers/CF1/scripts/CF1-d-r19/out/page_smoke_project.out). No timing failure.",
        "fix": "",
    },
]

# ---- assemble ----
rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in over:
        o = over[rid]
        row = {"id": rid, "check": r["check"], "location": o["location"] or r["location"], "status": o["status"], "evidence": o["evidence"]}
        if o["status"] != "PASS":
            row["fix"] = o["fix"]
        rows.append(row)
    elif r["status"] == "PASS":
        ev = r["evidence"]
        rows.append({
            "id": rid,
            "check": r["check"],
            "location": r["location"],
            "status": "PASS",
            "evidence": CARRY.format(files=r["location"].split(";")[0].strip()) + ev,
        })
    else:
        raise SystemExit(f"round-18 non-PASS row not re-verified: {rid}")
ids = {r["id"] for r in rows}
for nr in new_rows:
    if nr["id"] in ids:
        raise SystemExit(f"duplicate id {nr['id']}")
    if nr["status"] == "PASS":
        nr.pop("fix", None)
    nr.pop("verdict_note", None)
    rows.append(nr)

# ---- mutants from the final run ----
mutants = []
for line in (OUT / "mutate_r19_final.out").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^(KILLED|SURVIVED) (\S+?\.py): (.*) -> (.*)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    mutants.append({
        "file": f"ledgers/CF1/mutants/{fname}",
        "description": desc,
        "killed_by": None if status == "SURVIVED" else re.sub(r"\s*\(seed \d+\)$", "", killer),
    })
assert len(mutants) == len(list(( root / "ledgers/CF1/mutants").glob("*.py"))), len(mutants)

fragment = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 19,
    "verifier": "independent verifier (Haiku), round 19 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "51fa336 (detached, /tmp/verify19-CF1-d)",
    "base": "7143726 (round-18 pin); delta computed with git diff --stat 7143726 51fa336 and every hunk in this slice read (notes)",
    "checkout": "/tmp/verify19-CF1-d",
    "scratch": "/tmp/CF1-v/d19",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": (
        "Round-19 delta for this slice (7143726..51fa336): " + FILES_NOTE + ". Grader hunks: 293-300 (leading-zero IRR test), 369-380 (zero-flow payback test), 405-425 (payback first-flow nan case; ids renamed), 434-450 (payback nan/inf rate), 472-486 (Fisher nan/inf), 903-915 (Monte Carlo nan/inf). Labs and references unchanged. Scripts: ledgers/CF1/scripts/CF1-d-r19/ (make_mutants_r19.py, make_alts_r19.py, run_alts.py, recompute_l06_section3.py, build_fragment_r19.py, alts/, out/). Mutants: 173 .py files in ledgers/CF1/mutants/ run with mutate_graders --seeds 0-9 (172 killed); new this round: d19_m01..d19_m06 (d19_m01 survives). Alternatives: 56 engines plus 3 new, 10 seeds each, all pass. Not checked: the full BLUEPRINT re-grade of every card against lesson text (only the changed card and its lesson section); hours not re-estimated (architect ruling: design targets); live Monte Carlo and browser run of the grader in Pyodide beyond page_smoke; L06 is the lesson slice and was re-read only for the hunks the round-18 fragment cites."
    ),
    "summary": "",
}
n_fail = sum(1 for r in rows if r["status"] != "PASS")
fragment["summary"] = (
    f"CF1-d round 19 (pin 51fa336): {len(rows)} rows, {len(rows) - n_fail} PASS, {n_fail} FAIL. FAIL: "
    "proj-mutant-d19-m01-irr-zero-outlay-refused (an IRR request of an outlay then zeros is refused by a mutant the suite does not kill; fix: test irr_roots([-100, 0]) == []), proj-mutants-killed and cmd-mutate-graders-r19 (both 172/173 from the same survivor), lesson-l06-remark-2-4-each-result-conditional (Remark 2.4 overstates the labelling of E1), cards-grade-semantics and cards-definition-basis-graded-t (17 definition cards graded T; fix: regrade to C). Mutants: 173 run, 172 killed, 1 survivor. Alternatives: 3 new and 56 earlier engines pass seeds 0-9."
)
out = root / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "fail", n_fail, "mutants", len(mutants), "killed", sum(1 for m in mutants if m["killed_by"]))
