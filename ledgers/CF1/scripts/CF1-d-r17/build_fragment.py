"""Build ledgers/CF1/CF1-d.json for round 17 from the round-16 fragment, the re-run outputs and the new rows."""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path("/tmp/fanout-frags/CF1-d.round16.json").read_text(encoding="utf-8"))
CARRY = (
    "Carried from round 16 (course/modules/CF/CF1/project.html, course/modules/CF/CF1/grader/*, tests/labs/CF1/*, "
    "the pre-existing ledgers/CF1/mutants files, references/references.json, and the cards.json entries and plan "
    "lines cited here, all byte-identical since the previous pin c5daab2): "
)
OUT = "ledgers/CF1/scripts/CF1-d-r17/out/"

over = {}


def row(rid, check, location, status, evidence, fix=None):
    r = {"id": rid, "check": check, "location": location, "status": status, "evidence": evidence}
    if fix:
        r["fix"] = fix
    return r


# Rows re-verified this round (subject changed, or a whole-file re-run replaces the previous one).
over["cards-count-vs-plan"] = row(
    "cards-count-vs-plan",
    "cards: per-lesson card count against the plan",
    "plans/CF1-build-plan.md line 240; course/modules/CF/CF1/cards.json",
    "PASS",
    "Re-verified round 17. Round 16 flagged line 240 ('the planner expects four to six per lesson'). Line 240 now reads "
    "(git diff c5daab2 fefbf8b -- plans/CF1-build-plan.md): 'the count follows BUILDER_RULES section 7 (one atomic card "
    "per definition, key result and misconception; no fixed number per lesson)'. BUILDER_RULES.md line 392 (section 7) "
    "asks for one atomic card per definition, theorem statement, key formula, key empirical result and misconception and "
    "sets no count. The plan sentence names fewer categories than section 7 but does not state a count, so it is no "
    "longer in conflict with the cards. python -I count of cards.json: 109 entries (L01 18, L02 18, L03 17, L04 23, L05 "
    "18, L06 15). No file in the repository still quotes 'four to six' or a card total (grep, excluding ledgers).",
)
over["cards-missing-grade-or-basis"] = row(
    "cards-missing-grade-or-basis",
    "cards: every entry has a grade and a cite or basis",
    "course/modules/CF/CF1/cards.json (109 entries)",
    "PASS",
    "Re-run round 17 on the whole file (python -I): every entry has grade in {T, C} and either cite or basis; no entry "
    "lacks both. Keys per entry: ('back','basis','cite','front','grade','id','lesson') or without cite. Ids run CF1-c001 "
    "to CF1-c109 in order. Grades: T 78, C 31.",
)
over["cards-duplicate-scan"] = row(
    "cards-duplicate-scan",
    "cards: exact duplicate scan (ids, fronts, backs)",
    "course/modules/CF/CF1/cards.json",
    "PASS",
    "Re-run round 17 (python -I): 109 unique ids, 109 unique fronts, 109 unique backs; no exact duplicate. The near "
    "duplicate CF1-c104 of CF1-c029 is a separate row (cards-c104-duplicates-c029).",
)
over["cards-numbers-in-lesson"] = row(
    "cards-numbers-in-lesson",
    "cards: every card number appears in its lesson or lab output",
    "course/modules/CF/CF1/cards.json; L02.html, L03.html, L04.html, L05.html; tests/labs/CF1/lab-CF1-L04-1.py",
    "PASS",
    "Re-run round 17 for the changed and new cards. CF1-c053 -2,000 and factorization: L04.html line 109 "
    "(Proposition 3.3). CF1-c056 'two sign changes, bisected to 0.100000 and 0.200000': run_labs output of "
    "lab-CF1-L04-1 prints 'sign changes of the NPV profile on the grid: 2', 'IRR root 1 ... 0.100000', 'IRR root 2 ... "
    "0.200000' (ledgers/CF1/scripts/CF1-d-r17/out/run_labs.out and lab twin run under python -I -W error). CF1-c108 "
    "0.200000: the lab prints 'crossover rate, the IRR of the difference: 0.200000' with difference B minus A. CF1-c107 "
    "10 and 20 per cent: L04.html line 109. CF1-c105 r pi: L03.html line 70-71. No card number is absent from its lesson.",
)
over["cards-grade-semantics"] = row(
    "cards-grade-semantics",
    "cards: T and C grades follow BLUEPRINT section 3 and the card basis",
    "course/modules/CF/CF1/cards.json",
    "PASS",
    "Re-run round 17. Every T card that is new or changed (CF1-c023, c036, c051, c053, c104 to c107) has a basis that "
    "names a theorem, corollary or proposition proved in the lesson (for example 'Corollary 2.3, proved in Section 2'). "
    "Every C card that is new or changed (CF1-c056, c096, c108, c109) names a lab with SIMULATED data or a convention "
    "with its section. The whole-file list of T cards without a proved/theorem word (CF1-c011, c029, c072, c073, c085, "
    "c086) is unchanged since the previous pin and was checked in round 16 (carried row cards-changed-c014-c037-c047-c057 "
    "and cards-misconception-locator).",
)
over["cards-changed-c016-c044-c051-c052"] = row(
    "cards-changed-c016-c044-c051-c052",
    "cards: changed-card agreement (c016, c044, c051, c052)",
    "course/modules/CF/CF1/cards.json CF1-c016, c044, c051, c052; L01, L03, L04 text",
    "PASS",
    "Re-verified round 17 for CF1-c051, which changed this round. Its front is now 'How many IRRs does a project with an "
    "outlay at t = 0 followed by non-negative inflows, not all zero, have?' and its back is 'Exactly one. The NPV profile "
    "is strictly decreasing (Theorem 2.1).' L04.html line 78 gives Theorem 2.1: 'exactly one IRR' and 'strictly "
    "decreasing'. The sign rule for the IRR moved to CF1-c106, verified in the new-card row. CF1-c016, c044 and c052 are "
    "byte-identical to c5daab2 (cards.json diff lists only c023, c036, c051, c053, c056 and c096 as changed).",
)
over["r15-cards-c054-c056-c058-c060-c094"] = row(
    "r15-cards-c054-c056-c058-c060-c094",
    "cards: round-15 changed cards c054, c056, c058, c060, c094",
    "course/modules/CF/CF1/cards.json CF1-c054, c056, c058, c060, c094; L04.html",
    "PASS",
    "Re-verified round 17 for CF1-c056, which changed this round. The old back ('two sign changes ... and a crossover rate "
    "of 0.200000 for A and B') is split: CF1-c056 now gives the two sign changes and the bisected roots (lab output in the "
    "cards-numbers-in-lesson row), and CF1-c108 gives the crossover rate 0.200000 (lab line 'crossover rate, the IRR of the "
    "difference: 0.200000'). c054, c058, c060 and c094 are byte-identical since c5daab2 and carried.",
)
over["cards-changed-r17-c023-c036-c051-c053"] = row(
    "cards-changed-r17-c023-c036-c051-c053",
    "cards: round-17 splits of c023, c036, c051, c053",
    "cards.json CF1-c023, c036, c051, c053; L02.html line 105-106; L03.html line 70-71; L04.html lines 78-82, 107-110",
    "PASS",
    "c023 back: 'The shield is tau x D_t: the part of OCF that depreciation adds over after-tax EBITDA, EBITDA_t x (1 - "
    "tau) (Corollary 2.3).' L02.html line 106 gives Corollary 2.3 with that content. c036 back: 'n = r + pi + r pi "
    "(Theorem 1.3).' L03.html line 70-71 gives Theorem 1.3 with that identity. c053 back: 'NPV = -2,000 x (11x - 10)(6x - 5) "
    "dollars with x = 1/(1+r)' is L04.html line 109 (Proposition 3.3) with -2 000 = -2,000; expanded, -2000(66x^2 - 115x + "
    "50) = -132000x^2 + 230000x - 100000, the NPV of P (recomputed with python -I). Each front asks the question its back "
    "answers.",
)
over["cards-changed-r17-c056-c096"] = row(
    "cards-changed-r17-c056-c096",
    "cards: round-17 changed c056 and c096 fronts and backs",
    "cards.json CF1-c056, c096; L04.html line 300 (interpretation); L05.html lines 57-64 (Definition 1.1)",
    "PASS",
    "CF1-c056 back 'Two sign changes, bisected to 0.100000 and 0.200000 (Lab 1, SIMULATED cash flows)': L04.html line 300 "
    "('the grid finds two sign changes, bisected to 0.100000 and 0.200000') and lab output. The P cash flows are SIMULATED "
    "(L04.html line 101 and line 148). CF1-c096 back: '(tau_S - 1) + (-CUM_(tau_S - 1)) / C_(tau_S) (Definition 1.1)' "
    "matches L05.html Definition 1.1 (lines 57-64). Grade C with basis 'convention, Section 1 (interpolation)' is "
    "unchanged.",
)
over["cards-new-r17-c105-c109"] = row(
    "cards-new-r17-c105-c109",
    "cards: round-17 new cards c105 to c109",
    "cards.json CF1-c105, c106, c107, c108, c109; L03.html line 70-71; L04.html lines 78-82, 107-110, 300; L05.html lines 57-64",
    "PASS",
    "c105 (T): 'By exactly r pi, since n - (r + pi) = r pi (Theorem 1.3)': the lesson's Theorem 1.3 says the same and the "
    "algebra is (1+r)(1+pi) - 1 - r - pi = r pi, checked with python -I. c106 (T): sign of the IRR as the sum of flows "
    "(Theorem 2.1, L04.html line 78). c107 (T): 'Exactly 10 and 20 per cent (Proposition 3.3)': L04.html line 109 'Its IRRs "
    "are exactly 10 per cent and 20 per cent'; roots checked with python -I (11x-10=0 gives r=10%, 6x-5=0 gives r=20%). "
    "c108 (C, Lab 1 SIMULATED): crossover 0.200000 from 'crossover rate, the IRR of the difference' with difference = B - A "
    "(lab code line 113-116, output line 22). c109 (C): 'That they arrive evenly through the year. This is a convention and "
    "not a finding (Definition 1.1)': L05.html line 64 'It is a convention, and it is not a finding.' No new card repeats "
    "an earlier card's front or back except as recorded in cards-c104-duplicates-c029.",
)
over["cards-c104-duplicates-c029"] = row(
    "cards-c104-duplicates-c029",
    "cards: one fact per card, no duplicate facts (BUILDER_RULES 7; plan 12)",
    "course/modules/CF/CF1/cards.json CF1-c104 (back) and CF1-c029 (back); plans/CF1-build-plan.md section 12",
    "FAIL",
    "CF1-c104 back: 'None beyond the shield. Depreciation adds no cash of its own; its only cash effect is the tax it saves "
    "(Corollary 2.3).' CF1-c029 back: 'False. Depreciation is non-cash. Its only cash effect is the tax it saves, tau x D_t "
    "(Corollary 2.3).' Both test the same fact (depreciation adds no cash beyond its tax shield, Corollary 2.3). "
    "BUILDER_RULES.md section 7 says 'Each card tests one fact', and plans/CF1-build-plan.md section 12 says 'Duplicates "
    "are not allowed'. The round-17 split of CF1-c023 created c104 by moving 'depreciation adds no cash' out of c023, "
    "where c029 already tests it.",
    fix="Delete CF1-c104 (its fact is already tested by CF1-c029), or replace its back with a different fact from L02. If "
    "it is deleted, renumber CF1-c105 to CF1-c109 as CF1-c104 to CF1-c108 so ids run upward without a gap (BUILDER_RULES "
    "section 7). Re-run check_pages and the cards-duplicate-scan after the change.",
)
over["proj-banned-phrases"] = row(
    "proj-banned-phrases",
    "2.9: banned phrases and process words, project page and cards",
    "course/modules/CF/CF1/project.html; course/modules/CF/CF1/cards.json (whole file); L05.html; L06.html; index.html",
    "PASS",
    "Re-run round 17 on cards.json (whole file, python -I regex: historically, roughly, about <digit>, typically, usually, "
    "ellipsis, build, round, verifier, REQUEST, unit report, we, I): the only hits are the mathematical symbol I "
    "(investment) in CF1-c008, c075 and c079 (checked by reading the cards), so no banned phrase or process word. "
    "project.html is byte-identical to c5daab2 and the carried scan stands.",
)
over["proj-process-words-r10"] = row(
    "proj-process-words-r10",
    "12: no process words in learner text",
    "course/modules/CF/CF1/cards.json; project.html; L05.html; L06.html; index.html; tests/labs/CF1",
    "PASS",
    "Re-run round 17 on cards.json (whole file): no process word (build, builder, round, verifier, REQUEST, unit report) "
    "in any front or back; the standalone 'I' in CF1-c008, c075, c079 is the investment symbol. The other files are "
    "byte-identical to c5daab2 (carried).",
)
over["r16-banned-process-words-scan"] = row(
    "r16-banned-process-words-scan",
    "12: process-word scan over changed cards",
    "course/modules/CF/CF1/cards.json",
    "PASS",
    "Re-run round 17 on the whole cards.json (python -I): no process word in the 109 entries; changed and new cards "
    "CF1-c023, c036, c051, c053, c056, c096, c104 to c109 included.",
)
over["r15-banned-phrase-scan"] = row(
    "r15-banned-phrase-scan",
    "2.9 / 1.2: banned phrases in cards",
    "course/modules/CF/CF1/cards.json",
    "PASS",
    "Re-run round 17 (python -I, whole file): no 'roughly', 'about <digit>', 'historically', 'typically', 'usually' and no "
    "ellipsis in any card.",
)
over["proj-mutants-killed"] = row(
    "proj-mutants-killed",
    "2.5 / mutation: every project mutant killed by the grader",
    "ledgers/CF1/mutants/*.py (143 files); tools/mutate_graders.py --unit CF1 --seeds 0-9",
    "PASS",
    "Re-run round 17: tools/mutate_graders.py --unit CF1 --seeds 0-9 printed 'mutate_graders CF1: PASS (139/139 killed)' "
    "for the 139 mutants present when it started (ledgers/CF1/scripts/CF1-d-r17/out/mutate_r17.out). The four round-17 "
    "mutants were run with the same procedure (run_mutants.py, seeds 0-9) and all four were killed (see "
    "proj-mutants-round17-new).",
)
over["proj-equivalent-mutant-proof"] = row(
    "proj-equivalent-mutant-proof",
    "2.5 / mutation: equivalent mutants carry a proof and are outside the list",
    "ledgers/CF1/mutants/ (143 files); ledgers/AC1/equivalent/v16_m01.proof.md",
    "PASS",
    "Re-listed round 17: all 143 .py files in ledgers/CF1/mutants are mutants the grader kills, and none is an equivalent "
    "mutant. The round-16 equivalent-mutant archive named in the fefbf8b commit message is ledgers/AC1/equivalent/"
    "v16_m01.proof.md, an AC1 file outside this slice; it is not in ledgers/CF1/mutants.",
)
over["proj-structure-and-gates"] = row(
    "proj-structure-and-gates",
    "2.9 / gates: check_projects, check_pages, check_dag",
    "tools/check_projects.py --all; tools/check_pages.py --unit CF1; tools/check_dag.py --all",
    "PASS",
    "Re-run round 17 at fefbf8b: 'check_projects CF1: PASS', 'check_projects AP1: PASS' (exit 0); 'check_pages CF1: PASS' "
    "(exit 0); 'check_dag CF1: PASS', 'check_dag AP1: PASS' (exit 0). Outputs in ledgers/CF1/scripts/CF1-d-r17/out/.",
)
over["proj-check-dag"] = row(
    "proj-check-dag",
    "DAG: check_dag",
    "tools/check_dag.py --all",
    "PASS",
    "Re-run round 17: 'check_dag CF1: PASS', 'check_dag AP1: PASS' (ledgers/CF1/scripts/CF1-d-r17/out/check_dag.out).",
)
over["proj-pytest-lab-helper"] = row(
    "proj-pytest-lab-helper",
    "2.5 labs: project-lab twins run and run_labs",
    "tests/labs/CF1/*.py; tools/run_labs.py --unit CF1",
    "PASS",
    "Re-run round 17: 'run_labs CF1: PASS (9/9)'. The three project twins were run alone with python -I -W error and "
    "exit 0 (lab-CF1-project-1, -2, -3; outputs in /tmp/CF1-v/d17/ and the twins are unchanged since c5daab2).",
)
over["proj-grader-reference-50-seeds"] = row(
    "proj-grader-reference-50-seeds",
    "2.5 grader: reference passes 50 seeds",
    "course/modules/CF/CF1/grader/reference.py; tools/run_graders.py --unit CF1 --seeds 0-49",
    "PASS",
    "Re-run round 17: 'run_graders CF1: PASS (reference 50/50 seeds, slowest 0.3 s)' (ledgers/CF1/scripts/CF1-d-r17/out/"
    "run_graders.out).",
)
over["proj-page-smoke"] = row(
    "proj-page-smoke",
    "2.5 page smoke: project page grader and labs",
    "course/modules/CF/CF1/project.html; tools/page_smoke.py --unit CF1 --pages project --skip-sweep",
    "PASS",
    "Re-run round 17: 'in-browser grader: All 138 tests pass on seed 884171179', 'page_smoke modules/CF/CF1/project.html: "
    "PASS', 'page_smoke CF1: PASS' (exit 0). The 138 matches project.html line 192 and the collect-only count of "
    "reference and starter (both 138, QF_SEED 0).",
)
over["proj-verify-refs"] = row(
    "proj-verify-refs",
    "2.1 citations: verify_refs offline and live for CF1",
    "tools/verify_refs.py --offline; tools/verify_refs.py --unit CF1; references/references.json",
    "PASS",
    "Re-run round 17: 'offline integrity: 560 entries, 0 problems' (exit 0); 'live re-verification of CF1: 2 of 560 "
    "entries, 0 problems' (exit 0). references/references.json is unchanged since c5daab2.",
)
over["proj-ruff-format"] = row(
    "proj-ruff-format",
    "gate: ruff check and format on grader and labs",
    "course/modules/CF/CF1/grader; tests/labs/CF1",
    "PASS",
    "Re-run round 17: ruff check 'All checks passed!'; ruff format --check '13 files already formatted'. Mutant files are "
    "excluded by ruff extend-exclude ledgers/*/mutants (pyproject.toml line 18); ruff check on the four round-17 mutants "
    "reports E501 only, as the earlier mutants do.",
)
over["proj-mypy-grader-gate"] = row(
    "proj-mypy-grader-gate",
    "gate: mypy --no-incremental on grader and labs",
    "course/modules/CF/CF1/grader/*.py; tests/labs/CF1/*.py",
    "PASS",
    "Re-run round 17: 'Success: no issues found in 13 source files'.",
)
over["proj-collect-count-50-seeds"] = row(
    "proj-collect-count-50-seeds",
    "2.9 / grading: collected count equals the page count",
    "course/modules/CF/CF1/grader/test_project.py; course/modules/CF/CF1/project.html line 192",
    "PASS",
    "Re-run round 17 (ledgers/CF1/scripts/CF1-d-r17/collect.py, python -I): 'seed 0 reference 138 tests collected' and "
    "'seed 0 starter 138 tests collected'. The page line 192 says 138.",
)
over["proj-spec-count-118-hub"] = row(
    "proj-spec-count-118-hub",
    "2.9 / grading: page count against the collected count",
    "course/modules/CF/CF1/project.html line 192 (Grading mode)",
    "PASS",
    "Re-run round 17: project.html line 192 states 138 checks, and the collect-only count of the reference and starter is "
    "138 (see proj-collect-count-50-seeds).",
)
over["proj-test-count-72"] = row(
    "proj-test-count-72",
    "2.9 / grading: test count on the page equals the collected count",
    "course/modules/CF/CF1/project.html line 192 (Grading mode); grader/test_project.py",
    "PASS",
    "Re-run round 17: collect-only count 138 for reference and starter (ledgers/CF1/scripts/CF1-d-r17/collect.py); project.html "
    "line 192 says 138.",
)

new_rows = [
    row(
        "proj-mutants-round17-new",
        "2.5 / mutation: round-17 student-error mutants",
        "ledgers/CF1/mutants/r17_01_fisher_checks_only_the_real_rate.py, r17_02_payback_zero_recovery_needs_strictly_positive_cumulative.py, r17_03_irr_grid_evenly_spaced_in_discount_factor.py, r17_04_monte_carlo_correction_uses_volatility_not_its_square.py",
        "PASS",
        "Four new mutants written by ledgers/CF1/scripts/CF1-d-r17/make_mutants.py and run with run_mutants.py (seeds 0-9, "
        "the mutate_graders procedure): r17_01 KILLED by test_fisher_rejects_rates_at_or_below_minus_one[inflation-minus-one] "
        "and [inflation-below-minus-one] (2 failed); r17_02 KILLED by test_payback_ignores_flows_after_the_cut_off and "
        "test_payback_counts_a_year_that_exactly_recovers_the_outlay_at_the_horizon; r17_03 KILLED by "
        "test_irr_finds_both_roots_of_a_two_sign_change_flow; r17_04 KILLED by test_monte_carlo_draws_follow_the_seeded_gauss_stream "
        "and test_monte_carlo_mean_is_the_affine_identity_on_the_same_draws. Each one violates a sentence of project.html: "
        "the Fisher identity and the named errors (Named errors paragraph: a rate at or below -1 in a Fisher conversion), 'reaches "
        "zero or more' (Conventions, Payback), 'spaced evenly in log x' (Conventions, IRR roots), and the 'volatility squared / 2' "
        "term (Conventions, Monte Carlo NPV). Survivors: none.",
    ),
    row(
        "proj-alternatives-round17-new",
        "2.5 / over-constraint: three new correct alternative engines, 50 seeds each",
        "ledgers/CF1/scripts/CF1-d-r17/alts/alt_r17_a_algebraic_flows_accumulate_payback_horner_npv.py, alt_r17_b_bisection_absolute_zero_and_wider_stop.py, alt_r17_c_logarithmic_fisher_scaled_revenue.py",
        "PASS",
        "run_alts.py over the three engines (ledgers/CF1/scripts/CF1-d-r17/out/alts_r17.out): all three 'PASS 50/50 seeds'. "
        "A: after-tax flows from the algebraic form EBITDA(1-tau)+depreciation*tau, payback from itertools.accumulate and "
        "next(), NPV by Horner in x = 1/(1+r). B: bisection stops on abs(f) <= 1e-300 and at relative width 4e-14 (not "
        "1e-15), a different numerical cutoff. C: Fisher by expm1/log1p, a different valid algorithm. Each passes the suite.",
    ),
    row(
        "cmd-mutate-graders-r17",
        "2.5 / gate: mutate_graders on the grader",
        "tools/mutate_graders.py --unit CF1 --seeds 0-9",
        "PASS",
        "Re-run round 17: 'mutate_graders CF1: PASS (139/139 killed)' for the mutants present at start (mutate_r17.out).",
    ),
    row(
        "cmd-verify-refs-live-r17",
        "2.1 citations: live registry verification",
        "tools/verify_refs.py --unit CF1",
        "PASS",
        "'live re-verification of CF1: 2 of 560 entries, 0 problems'. output in ledgers/CF1/scripts/CF1-d-r17/out/verify_refs_live_CF1.out.",
    ),
]

rows = []
seen = set()
for r in prev["rows"]:
    rid = r["id"]
    seen.add(rid)
    if rid in over:
        rows.append(over[rid])
        continue
    if r["status"] == "PASS":
        ev = r["evidence"]
        if ev.startswith("Carried from round 16"):
            new_ev = ev
        else:
            new_ev = CARRY + ev
        rows.append({**r, "evidence": new_ev})
    else:
        rows.append(r)

for n in new_rows:
    rows.append(n)
    seen.add(n["id"])
# cards-c104 is the only new non-PASS row; the cards-count-vs-plan row is re-verified as PASS.
rows.append(over["cards-changed-r17-c023-c036-c051-c053"])
rows.append(over["cards-changed-r17-c056-c096"])
rows.append(over["cards-new-r17-c105-c109"])
rows.append(over["cards-c104-duplicates-c029"])

mutants = list(prev["mutants"])
mutants += [
    {
        "file": "ledgers/CF1/mutants/r17_01_fisher_checks_only_the_real_rate.py",
        "description": "The student validates the real rate in fisher_nominal but not the inflation rate, so an inflation of -1 returns -1 instead of raising ValueError.",
        "killed_by": "test_fisher_rejects_rates_at_or_below_minus_one[inflation-minus-one] (seed 0)",
    },
    {
        "file": "ledgers/CF1/mutants/r17_02_payback_zero_recovery_needs_strictly_positive_cumulative.py",
        "description": "The student tests recovery with a strict inequality, so a cumulative flow of exactly zero before the final year is not taken as payback.",
        "killed_by": "test_payback_ignores_flows_after_the_cut_off (seed 0)",
    },
    {
        "file": "ledgers/CF1/mutants/r17_03_irr_grid_evenly_spaced_in_discount_factor.py",
        "description": "The student spaces the IRR search grid evenly in the discount factor x, not in log x as the page specifies, so the window is sampled at intervals of about 2.5 in x.",
        "killed_by": "test_irr_finds_both_roots_of_a_two_sign_change_flow (seed 0)",
    },
    {
        "file": "ledgers/CF1/mutants/r17_04_monte_carlo_correction_uses_volatility_not_its_square.py",
        "description": "The student writes the lognormal correction as volatility / 2 instead of volatility squared / 2, so E[m] is not one and the draws do not center on the deterministic NPV.",
        "killed_by": "test_monte_carlo_draws_follow_the_seeded_gauss_stream (seed 0)",
    },
]

# Ids of rows that were already present but are re-verified above are kept (ids unchanged).
ids = [r["id"] for r in rows]
dups = {i for i in ids if ids.count(i) > 1}
frag = {
    "unit": "CF1",
    "slice": "CF1-d",
    "round": 17,
    "verifier": "independent verifier (Haiku), round 17 of CF1 slice d (project page incl. case-memo rubric, grader, project labs, cards.json; project slice needs mutants)",
    "pin": "fefbf8b (detached, /tmp/verify17-CF1-d)",
    "base": "c5daab2 (round-16 pin); delta computed with git diff c5daab2 fefbf8b and read per hunk",
    "checkout": "/tmp/verify17-CF1-d",
    "scratch": "/tmp/CF1-v/d17",
    "verified_at": "2026-10-28",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": prev["registry_flags"],
    "freshness_flags": [],
    "notes": "Delta c5daab2..fefbf8b for this slice: course/modules/CF/CF1/cards.json (six changed entries CF1-c023, c036, c051, c053, c056, c096; six new entries CF1-c104 to c109), plans/CF1-build-plan.md line 240, ledgers/CF1/mutants/r16_01..03 (already in the round-16 count). project.html, grader/*, tests/labs/CF1/* are byte-identical. Scripts: ledgers/CF1/scripts/CF1-d-r17/ (make_mutants.py, make_alts.py, run_alts.py, run_mutants.py, collect.py, build_fragment.py); outputs in ledgers/CF1/scripts/CF1-d-r17/out/. registry_flags carried: references/references.json unchanged since c5daab2.",
    "summary": "CF1-d round 17: rows, one non-PASS (cards-c104-duplicates-c029: new card CF1-c104 restates CF1-c029). Mutants 143/143 killed (139 pre-existing re-run, 4 new). Three new alternative engines PASS 50/50 seeds. Gates check_projects, check_pages, check_dag, run_labs, run_graders, page_smoke, mutate_graders, verify_refs (offline and live), ruff, mypy PASS.",
}
out = root / "ledgers/CF1/CF1-d.json"
out.write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("rows", len(rows), "dups", dups, "non-pass", [r["id"] for r in rows if r["status"] != "PASS"])
