"""Builds ledgers/FC1/FC1-c.json (round 3, slice c) from the verifier's recorded outputs.

Usage: python ledgers/FC1/scripts/FC1-c-r3/build_fragment_r3.py <checkout-root>
Reads mutate_r3.out (the output of tools/mutate_graders.py --unit FC1 --seeds 0-9) for the mutant list.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

root = Path(sys.argv[1])
S = root / "ledgers/FC1/scripts/FC1-c-r3"
mut_lines = (S / "mutate_r3.out").read_text(encoding="utf-8").splitlines()
mutants = []
for line in mut_lines:
    m = re.match(r"(KILLED|SURVIVED) (\S+?): (.*) -> (\S+(?: \(seed \d+\))?)$", line)
    if not m:
        continue
    status, fname, desc, killer = m.groups()
    killed_by = None if killer == "None" else killer.split(" (seed")[0]
    seed = "" if killed_by is None else f" (seed {killer.split('seed ')[1].rstrip(')')})"
    mutants.append({
        "id": fname.removesuffix(".py"),
        "description": desc,
        "killed_by": (killed_by + seed) if killed_by else None,
    })

PASS = "PASS"
rows = [
    ("proj-run-graders", "2.6-grader", "course/modules/FC/FC1/grader/", PASS,
     "tools/run_graders.py --unit FC1 -> 'run_graders FC1: PASS (reference 50/50 seeds, slowest 0.2 s)', exit 0 (scripts/FC1-c-r3/run_graders.out). The gate also checks that the starter fails the suite."),
    ("proj-collect-count-55", "2.6-autograder", "course/modules/FC/FC1/project.html (Grading mode, 'runs 55 checks'); grader/test_project.py", PASS,
     "pytest --collect-only -q on the reference copy -> '55 tests collected'; grep -c '^def test_' test_project.py -> 55; project.html says 55 checks."),
    ("proj-browser-suite", "2.6-autograder", "project.html grader panel; grader/", PASS,
     "tools/page_smoke.py --unit FC1 --pages project -> 'in-browser grader: All 55 tests pass on seed 1917324657', 'page_smoke FC1: PASS' (scripts/FC1-c-r3/page_smoke_project.out)."),
    ("proj-local-command", "2.6-autograder", "project.html section 'Running the suite locally'", PASS,
     "The stated command (QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py) was run on the reference copy for seeds 0-49 by scripts/FC1-c-r3/run_suite.sh: 0 failing seeds."),
    ("proj-alternatives-five", "2.6-autograder", "ledgers/FC1/alternatives/a1..a5 (plan 5.5 list of five)", PASS,
     "scripts/FC1-c-r3/run_suite.sh on each of the five alternatives, seeds 0-49: a1 0/50, a2 0/50, a3 0/50, a4 0/50, a5 0/50 failing. a5 is the float implementation the plan lists as (5)."),
    ("proj-instances-50", "2.6-autograder", "grader/instance.py", PASS,
     "scripts/FC1-c-r3/numbers_r3.py: seeds 0-49 all valid (asserts on periods, face, coupon, yield, quantity, price, side, settlement); 50 distinct bond prices and 50 distinct trade amounts; seed 0 price 4281937, seed 1 price 4323085."),
    ("proj-starter-vs-spec", "2.6-spec", "grader/starter.py; project.html Required outputs", PASS,
     "Starter signatures Bond(face_cents, coupon_bps, periods), events(), bond_price_cents(bond, yield_bps), CashTrade(quantity, price_cents, side, settlement_day) match the page's Required outputs word for word; run_graders checks the starter fails the suite."),
    ("proj-spec-questions", "2.6-spec", "project.html section 'Rung 3 · Specification'", PASS,
     "Read as a student: inputs, outputs, conventions (periods from 1, rounding once half away from zero, holder's side), refusals and the fixtures are all stated. No clarifying question found. Period 0 is defined as the trade date, and the zero-amount rule is stated."),
    ("proj-ladder", "2.6-ladder", "project.html section#ladder", PASS,
     "tools/check_projects.py --unit FC1 -> 'check_projects FC1: PASS'; four li in order Worked example, Completion problem, Independent project, Stretch; rung 1 and 2 are annotated labs; rung 4 is ungraded."),
    ("proj-stretch-scope", "2.6-ladder", "project.html section#stretch; plans/FC1-build-plan.md 5.1 item 4; Architect decisions", PASS,
     "The plan's stretch items (callable bond, reconciliation) were written for the four-instrument design. The binding Architect decision narrows the project to cash instruments and a trade-lifecycle and order-book simulator, and the page's two stretch items (order matching, odd first period) fit it. Ungraded and open-ended. Noted, not failed."),
    ("proj-lab1-twin", "2.5-labs", "project.html Lab 1 (lab-FC1-project-1); tests/labs/FC1/lab-FC1-project-1.py", PASS,
     "tools/run_labs.py --unit FC1 -> 'run_labs FC1: PASS (8/8)'. labs_r3.py: page code == twin; twin under python -I -W error exit 0, stderr 0 bytes; stdout == expected block. Numbers: 102775.091033 and 102775 recomputed (scripts/FC1-c-r3/numbers_r3.out)."),
    ("proj-lab2-completion", "2.5-labs", "project.html Lab 2 (lab-FC1-project-2)", PASS,
     "lab2_blanks_r3.out: page has 2 blanks; with them filled as the Lab 2 prose states (period; -side * quantity * price_cents) the page code equals the twin text. labs_r3.out reports the Lab 2 page/twin difference only because of the two blanks (by design). Twin runs under python -I -W error exit 0 with empty stderr, and its stdout equals the expected block. Tolerance: compare_output uses tolerance*(1+|y|) = 1e-6*(1+102775) = 0.1028, matching 'about 0.1 cent'."),
    ("proj-lab3-fixtures", "2.5-labs", "project.html Lab 3 (lab-FC1-project-3); tests/labs/FC1/lab-FC1-project-3.py", PASS,
     "labs_r3.py: page code == twin, twin exit 0 with empty stderr, stdout == expected block. numbers_r3.out recomputes fixtures A (10000), B (exact 11052.6316, rounds 11053), C ([(1,5001),(2,15002)]), D ([(1,2)]), F (1/2 -> 1; round() gives 0), G (5000.5 -> 5001), rounding fixture (10277.509103 -> 10278; term-by-term 10277)."),
    ("proj-prose-numbers", "2.2-numbers", "project.html prose and lab hypotheses", PASS,
     "Each number in prose recomputed in numbers_r3.out: coupon 5000; events (1,5000),(2,5000),(3,105000); PV 102775.091033; trade (2,-98500); 480.77/462.28/9334.46 terms; 10277.509103; 11052.6316; 6861.894; 0.6 percent (30/5000); tolerance 0.1 cent. All match the page."),
    ("proj-hours-arithmetic", "2.9-hours", "project.html table#hours; hub data-hours-project", PASS,
     "Rows 1+2+5+4+2+3+3 = 20 = data-hours-project; 20 of 70 = 28.6 % (hub line 41). Ruling: hours are design targets, so the estimate is not failed."),
    ("proj-check-pages-dag", "2.9-structure", "course/modules/FC/FC1/project.html", PASS,
     "tools/check_pages.py --unit FC1 -> PASS; tools/check_dag.py --unit FC1 -> PASS (scripts/FC1-c-r3/check_pages.out, check_dag.out)."),
    ("proj-dag-closure", "2.9-DAG", "project.html discount-factor and present-value links", PASS,
     "The links point to M1/L05 anchors (course/concepts.html lines 69, 75). Closure: FC1 prereqs P0.1 and E1 (curriculum.json); E1 prereq M2; M2 prereq M1. So M1 is in the closure and the links are allowed."),
    ("proj-notation", "2.4-notation", "project.html math; notation/notation.json", PASS,
     "Project math symbols: y, t, (1+y)^(-t), y = 400/10000, 1+y. None is registered in notation.json (T, Phi, gamma_3, gamma_4, R*, R^e*, R_f, Q). No collision."),
    ("proj-banned-phrases", "2.9-prose", "project.html; grader/*.py; tests/labs/FC1 (BUILDER_RULES 1.3-1.4)", PASS,
     "grep for TODO, TBD, lorem, beyond the scope, obviously, clearly, it is important, well known, studies show, experts agree, you can add more, left as an exercise, process words: no hit in learner text. One '11052.63...' repeating decimal in grader/test_project.py line 259 is a decimal expansion, not omitted content. Noted."),
    ("proj-reading-list", "2.1-citations", "project.html section#reading; references/references.json", PASS,
     "Keys harris2002trading (registry year 2002) and mishkin2021economics (2021) exist; the page writes no year and attributes no statement. tools/verify_refs.py --unit FC1 -> '2 of 560 entries, 0 problems'; --offline -> '560 entries, 0 problems'."),
    ("proj-named-conditions", "2.6-exceptions", "grader/test_project.py must_raise tests; project.html Constraints", PASS,
     "ValueError is required only for the 8 named conditions (Bond periods, face, coupon; yield at or below -10000; quantity, price, side, settlement_day), each with a boundary test on both sides. The float and bool tests accept any exception."),
    ("proj-failure-messages", "2.6-autograder", "grader/test_project.py messages", PASS,
     "Messages name the property (for example 'periods < 1: the page requires a ValueError') and never print an expected value; pytest runs with --assert=plain."),
    ("proj-mutants-killed", "2.6-mutation", "ledgers/FC1/mutants/ (29 files of the earlier rounds, c3n03/c3n04/c3n05)", PASS,
     "mutate_graders --unit FC1 --seeds 0-9 (scripts/FC1-c-r3/mutate_r3.out): 30 of 34 killed. The killed set includes all f, m, v and c2n03 mutants and the three new mutants c3n03, c3n04, c3n05; see the mutants list."),
    ("proj-lint-types", "gate", "repo-wide", PASS,
     "ruff check . -> 'All checks passed!'; ruff format --check . -> '340 files already formatted'; mypy --no-incremental -> 'Success: no issues found in 229 source files'; pytest -k FC1 -> exit 0."),
    ("cards-scan-98", "2.7-cards", "course/modules/FC/FC1/cards.json (98 cards, L01 22, L02 18, L03 23, L04 17, L05 18)", PASS,
     "Full scan: each card's back read against the lesson text (scripts/FC1-c-r3/cards_r3.py over the L01-L05 texts; the definitions, propositions, assumptions and problems named in each back were located in the lesson). Ids unique; no duplicate fronts; no two cards test the same fact."),
    ("cards-numbers", "2.2-numbers", "cards.json backs", PASS,
     "cards_r3.py: every number in every back appears in the lesson text (0 unmatched). Recomputed: 6,861.89 (c010, 6861.8940391); 1,818.18 (c011); 18.18 % (c011); 1900 (c015); 6.8619 (c016); 0.006 (c037); 4000 and 3455 = 4000 - 545 (c053, c098); 14282414 / 68398886 = 0.20881 -> 0.209 (c084); 2172960 = 216 x 10060 (c082); 2026-10-30 is Friday (c083); 121 = 11 x 11 (c054)."),
    ("cards-labels-and-hypotheses", "2.7-cards", "cards.json backs vs lesson labels (Definition, Proposition, Assumption, Example, Remark, Problem)", PASS,
     "Every cited label exists in the cited lesson (for example Problem P2 = L01 'No limit at a zero reserve ratio'; Problem R1 = L03 'Three dealers'; Problem R2 = L04 'What fails from a crossed start' and L05 'Where the sign assumption fails'; Problem R3 = L04). Cards for propositions carry their hypotheses (c007 under Assumption 2.0 with d>0; c009 A2' with A1, A3 and 0<rho<=1; c041 under A1 to A3; c050 under B1 to B4; c065 under A1; c080 under A1 and A4)."),
    ("cards-misconception-refs", "2.7-cards", "cards.json (misconception N); lessons' 'Misconceptions' sections", PASS,
     "Lessons list misconceptions as an unnumbered sequence. Cards number them by position (L01 three, L02 three, L03 three, L04 three, L05 four), and each number matches the bullet it describes."),
    ("cards-grades-and-basis", "2.3-grades", "cards.json grade and basis fields", "FAIL",
     "Cards that state a lab-printed result must name a basis (BUILDER_RULES 7) and grade C. Four cards do not: c028 (grade T, cites 'Lab 2, Part D prints 14 for 13 entries'), c033 (no grade or basis; a property of the typed-in register), c034 ('Lab 2, Part C prints that the four exchange entries span three exposure classes'), c086 ('Lab 1 prints 14282414 ... 68398886', SIMULATED), c088 ('In Lab 1 ... 10117 ... 10060'). All values are correct; the labelling is missing."),
    ("mutant-c2n01", "2.6-mutation", "ledgers/FC1/mutants/c2n01_warns_on_long_schedule.py; project.html 'Constraints' sentence 'On a valid input and on each named refused input, no function prints or warns.'", "FAIL",
     "Survives 10 seeds. Bond warns for periods > 8, a valid input (page sentence above). The grader's warning and silence tests use only INST, INST2 and the ROUNDING_CASE, whose periods are at most 8 (numbers_r3.out: max periods 8 over seeds 0-49; make_instance draws 1..8). No test builds a bond with more than 8 periods."),
    ("mutant-c2n02", "2.6-mutation", "ledgers/FC1/mutants/c2n02_refuses_quantity_above_500.py; project.html Constraints 'CashTrade: quantity less than 1'", "FAIL",
     "Survives. CashTrade refuses quantity above 500, a refusal the page never names (its only quantity condition is quantity less than 1, and 'Any other invalid input may raise any exception or return' applies only to invalid input). Instances draw 1..500 and seeds 0-49 reach at most 461, so no test uses a quantity above 500."),
    ("mutant-c3n01", "2.6-mutation", "ledgers/FC1/mutants/c3n01_face_capped_at_five_million.py; project.html Constraints 'Bond: face_cents not positive'", "FAIL",
     "Survives. Bond refuses face above 5,000,000 cents, a cap the page does not state. Instance faces are 100000 to 5000000 and seeds 0-49 reach 4,999,067 (numbers_r3.out), so no test uses a face above the cap."),
    ("mutant-c3n02", "2.6-mutation", "ledgers/FC1/mutants/c3n02_settlement_capped_at_five_periods.py; project.html Constraints 'CashTrade: settlement_day less than 1'", "FAIL",
     "Survives. CashTrade refuses settlement_day above 5, a cap the page does not state. Instances draw 1..5 (seeds 0-49 reach 5), so no test uses a settlement day above 5."),
    ("proj-reference-deployment", "2.9-structure / BLUEPRINT 7", "BLUEPRINT.md lines 400-401; course/modules/FC/FC1/grader/reference.py; .github/workflows/ci.yml", "FAIL",
     "BLUEPRINT requires deployment to exclude every grader/reference.py. reference.py sits under course/, which is the published tree. The repo contains no publish or deploy configuration; its own docstring says 'no file in this repository enforces that'. Not verifiable from this repo, so fail closed. Cross-unit: applies to every grader. Fix: exclude course/**/grader/reference.py at publish (or keep reference solutions outside course/), and add a CI assertion that the published tree has none."),
]

rows_out = []
for rid, check, loc, status, ev in rows:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != PASS:
        row["fix"] = {
            "mutant-c2n01": "Add a test in test_project.py, with the module-level filterwarnings('error') active, that builds Bond(face, coupon, 12) and calls events() and bond_price_cents(); assert no warning and capsys empty.",
            "mutant-c2n02": "Add a test that accepts CashTrade(10_000, 9_850, 1, 2) with events [(2, -98_500_000)] and CashTrade(501, 9_850, 1, 2) with no exception.",
            "mutant-c3n01": "Add a test that accepts Bond(10**9, 500, 1).events() with [(1, 5 * 10**6 + 10**9)] ... (any face above 5,000,000 must be accepted).",
            "mutant-c3n02": "Add a test that accepts CashTrade(10, 9_850, 1, 100).events() == [(100, -98_500)].",
            "proj-reference-deployment": "Exclude course/**/grader/reference.py from the published tree (or move reference solutions out of course/) and add a CI assertion on the published tree.",
            "cards-grades-and-basis": "c028: grade T with basis 'Remark 2.6' (or grade C with basis 'Lab 2, Part D (typed-in register)'); c033: grade C, basis 'Lab 2 register (typed-in), Definition 2.1'; c034: grade C, basis 'Lab 2, Part C (typed-in register)'; c086: grade C, basis 'Lab 1 (SIMULATED, seed 2026), Part two'; c088: grade C, basis 'Lab 1 (SIMULATED), clearing state'.",
        }[rid]
    rows_out.append(row)

frag = {
    "unit": "FC1",
    "slice": "FC1-c",
    "round": 3,
    "verifier": "Claude Haiku 5.5, independent verifier for FC1 slice c, round 3 (did not build FC1; no round-2 fragment exists at the given path, so every row is re-verified from scratch)",
    "pin": "ccfdf4c18f5ae9d86e6fe1ca9141382fd6055f83",
    "base": "none (no round-2 fragment at /Users/billyribeiro/.fanout/frags/C-FC1-c.round2.json; full re-verification)",
    "checkout": str(root),
    "scratch": "/tmp/fc1c3",
    "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
    "verdict": "FAIL",
    "rows": rows_out,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Mutants: tools/mutate_graders.py --unit FC1 --seeds 0-9 -> 30/34 killed. Survivors: c2n01, c2n02, c3n01, c3n02. "
        "Five new student-error mutants written by this verifier: c3n01..c3n05 (ledgers/FC1/mutants/). "
        "Alternatives a1..a5 pass 50/50 seeds. Lab twins pass. Cards: all 98 read against L01-L05. "
        "Not checked: a live Pyodide run beyond page_smoke for project only; no independent rubric (none required); "
        "live Crossref re-verification was run for FC1 only."
    ),
    "summary": {},
}
counts = {"PASS": 0, "FAIL": 0, "UNVERIFIABLE": 0}
for r in rows_out:
    counts[r["status"]] += 1
frag["summary"] = {"rows": len(rows_out), "pass": counts["PASS"], "fail": counts["FAIL"],
                   "unverifiable": counts["UNVERIFIABLE"], "mutants": len(mutants),
                   "mutants_killed": sum(1 for m in mutants if m["killed_by"])}
(root / "ledgers/FC1/FC1-c.json").write_text(json.dumps(frag, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote ledgers/FC1/FC1-c.json", frag["summary"])
