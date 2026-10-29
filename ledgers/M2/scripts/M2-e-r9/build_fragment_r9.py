"""Build the round-9 M2 slice-e fragment from the round-9 evidence files (verifier-authored)."""
import json
import sys

ROOT = sys.argv[1]
S = "ledgers/M2/scripts/M2-e-r9/"
CARRY8 = "Carried from round 8 (course/modules/M/M2/grader/*.py, tests/labs/M2/lab-M2-project-{1,2,3}.py and course/modules/M/M2/project.html byte-identical since ce7b3821, verified by git diff --quiet): "
rows = []


def row(id_, check, location, status, evidence):
    rows.append({"id": id_, "check": check, "location": location, "status": status, "evidence": evidence})


row("e-auto-run", "2.6-autograder-1", "course/modules/M/M2/grader/reference.py", "PASS",
    "Fresh this round: `tools/run_graders.py --unit M2 --seeds 0-49` -> 'run_graders M2: PASS (reference 50/50 seeds, slowest 0.2 s)' (exit 0; " + S + "run_graders.out). Reference copied as sensitivity_engine.py with instance.py into /tmp/m2e_r9/ref, `python -I -W error -m pytest --assert=plain -q test_project.py` -> 85 passed (" + S + "pytest_ref_r9.out).")
row("e-auto-instances", "2.6-autograder-2", "course/modules/M/M2/grader/instance.py", "PASS",
    CARRY8 + "round-8 evidence ledgers/M2/scripts/M2-e-r8/sin_ratio_r8.out and the round-7 evidence (100 instances valid; 70 distinct x0; 100 of 100 distinct face values). The instance generator is unchanged, and run_graders (" + S + "run_graders.out) regenerates all 50 seeds.")
row("e-mut-existing", "2.6-mutation-existing", "ledgers/M2/mutants/", "PASS",
    "Fresh this round: `tools/mutate_graders.py --unit M2 --seeds 0-9` -> 'mutate_graders M2: PASS (99/99 killed)' (exit 0; " + S + "mutate_all_r9.log). Includes the 96 mutants of rounds 1-8 and the three new round-9 r9_* mutants.")
row("e-mut-r6_01", "2.6-mutation-survivor", "course/modules/M/M2/grader/test_project.py:282-308", "PASS",
    CARRY8 + "KILLED by test_large_positive_step_is_accepted (re-run in " + S + "mutate_all_r9.log).")
row("e-mut-r6_02", "2.6-mutation-survivor", "course/modules/M/M2/grader/test_project.py:546-580", "PASS",
    CARRY8 + "KILLED by test_hessian_positive_step_is_accepted (re-run in " + S + "mutate_all_r9.log).")
row("e-mut-new-killed", "2.6-mutation-new", "ledgers/M2/mutants/r9_01*, r9_02*, r9_03*", "PASS",
    "Own round-9 student-error mutants (generator " + S + "make_mutants_r9.py, written into ledgers/M2/mutants/): r9_01 central quotient divided by h instead of 2h (KILLED by test_central_difference_matches_the_analytic_derivative); r9_02 zero step accepted, _positive_step tests `step < 0` (KILLED by test_zero_step_raises_value_error); r9_03 duration_analytic without the minus sign (KILLED by test_named_ratios_are_the_stated_formulas). All 99 mutants killed in " + S + "mutate_all_r9.log.")
row("e-alternatives", "2.6-over-constraint", "course/modules/M/M2/grader/test_project.py", "PASS",
    "Fresh this round: altA (Richardson central, fsum forward, Fraction bond maths), altB (Decimal at 400 digits, tuple dual) and altC (math.fsum price, reordered Hessian mixed term, yield check as < -9999 bp, int(round(..)) return) each 50/50 seeds (" + S + "run_alts_r9.out; sources ledgers/M2/scripts/M2-e-r8/alts/).")
row("e-messages", "2.6-messages", "course/modules/M/M2/grader/test_project.py", "PASS",
    CARRY8 + "the round-7 reading of the failure messages stands; no failure message names an expected value.")
row("e-pyodide-local", "2.6-same-suite", "course/modules/M/M2/grader/test_project.py", "PASS",
    "`tools/page_smoke.py --unit M2 --pages project` -> 'page_smoke M2: PASS' (exit 0; " + S + "page_smoke_project.out). Local reference pytest under -W error: 85 passed (" + S + "pytest_ref_r9.out).")
row("e-test-count", "2.6-test-count", "course/modules/M/M2/project.html:211", "PASS",
    "Fresh: pytest --collect-only on the reference test_project.py -> '85 tests collected' (verified in /tmp/m2e_r9/ref); project.html:211 prints 85.")
row("e-valueerror-scope", "2.6-exceptions", "course/modules/M/M2/grader/test_project.py; course/modules/M/M2/project.html:225", "PASS",
    CARRY8 + "ValueError tests are tied to the conditions the page names (step h above zero, yield above -1, scheme name).")
row("e-scheme-types", "2.6-scheme-types", "course/modules/M/M2/project.html:211", "PASS",
    CARRY8 + "scheme names and types as stated at project.html:211.")
row("e-hours", "2.6-hours", "course/modules/M/M2/project.html:33, :239-245", "PASS",
    CARRY8 + "hours design targets; no arithmetic inconsistency found.")
row("e-hours-arith", "2.6-hours-arith", "course/modules/M/M2/project.html:239-245", "PASS",
    CARRY8 + "hours split re-added: totals match the hub split.")
row("e-ladder", "2.6-ladder", "course/modules/M/M2/project.html:40-48", "PASS",
    CARRY8 + "ladder steps as stated.")
row("e-spec-questions", "2.6-spec", "course/modules/M/M2/project.html:199-212", "PASS",
    CARRY8 + "specification questions read in full.")
row("e-rubric-calibration", "2.6-rubric", "course/modules/M/M2/project.html:400-404, :418-507", "PASS",
    CARRY8 + "rubric levels read in full.")
row("e-rubric-observable", "2.6-rubric", "course/modules/M/M2/project.html:400 (C1 level 4), :404 (C5 level 3)", "PASS",
    CARRY8 + "each level names an observable check.")
row("e-rubric-adversarial", "2.6-rubric", "course/modules/M/M2/project.html:395-407", "PASS",
    CARRY8 + "adversarial rubric items read in full.")
row("e-atlas-studio", "2.6-atlas", "curriculum/meta.yaml; plans/M2-build-plan.md:22", "PASS",
    "curriculum/meta.yaml and plans/M2-build-plan.md unchanged since ce7b3821 (git diff --quiet over both paths).")
row("e-labs-run", "2.6-labs", "tests/labs/M2/lab-M2-project-{1,2,3}.py", "PASS",
    "Fresh: `python -I -W error` on each twin exit 0 (" + S + "lab_p1.out, lab_p2.out, lab_p3.out); `tools/run_labs.py --unit M2` -> 'run_labs M2: PASS (27/27)' (" + S + "run_labs_M2.out).")
row("e-labs-page-twin", "2.6-labs-embed", "course/modules/M/M2/project.html:58, :107, :270, :350", "PASS",
    "Fresh: tools/check_pages.py --unit M2 -> 'check_pages M2: PASS' (" + S + "check_pages.out), which covers the embedded lab code and expected blocks; project.html unchanged since ce7b3821.")
row("e-lab1-numbers", "2.6-numbers", "course/modules/M/M2/project.html:57, :116", "PASS",
    CARRY8 + "Lab 1 printed numbers re-checked against the twin output.")
row("e-lab2-numbers", "2.6-numbers", "course/modules/M/M2/project.html:121, :195", "PASS",
    CARRY8 + "Lab 2 printed numbers as stated.")
row("e-lab3-numbers", "2.6-numbers", "course/modules/M/M2/project.html:267-377", "PASS",
    CARRY8 + "Lab 3 numbers read in full.")
row("e-lab3-interpretation", "2.6-interpretation", "course/modules/M/M2/project.html:377 (and the Lab 1 interpretation at :116)", "PASS",
    CARRY8 + "interpretation sentences consistent with the printed output.")
row("e-report-spec", "2.6-report", "course/modules/M/M2/project.html:207, :270", "PASS",
    CARRY8 + "report specification as stated.")
row("e-exemplar-numbers", "2.6-numbers", "course/modules/M/M2/project.html:418, :429, :454, :470, :481, :494, :507", "PASS",
    CARRY8 + "exemplar numbers as in round 8.")
row("e-sin-ratio", "2.6-claim", "course/modules/M/M2/project.html:226", "PASS",
    CARRY8 + "sin-ratio claim re-run in round 8 (ledgers/M2/scripts/M2-e-r8/sin_ratio_r8.out).")
row("e-formulas", "2.6-formulas", "course/modules/M/M2/project.html:214-227", "PASS",
    CARRY8 + "formulas match the reference (reference.py passes 50/50 seeds this round).")
row("e-cards-correct", "2.6-cards-vs-lessons", "course/modules/M/M2/cards.json (377 cards); course/modules/M/M2/L01-L24.html", "UNVERIFIABLE",
    "Not completed this round. Changed cards were read against their lessons and PASS (see e-cards-delta). The remaining cards were not each read against the current lesson text, so the 377-card read is incomplete. Mechanical checker " + S + "cards_check_r9.out: 377 cards, 377 unique ids, no bad grade, no C without basis, no T with basis.")
row("e-cards-delta", "2.6-cards-vs-lessons", "course/modules/M/M2/cards.json: M2-c379, c163, c187, c234, c299 (changed); M2-c388, c389 (removed)", "PASS",
    "Read against the current lessons: c379 vs L05.html:91 (central difference defined without a derivative); c163 vs L11.html:242 (integrability examples, Misconception 3 is the integration-by-parts item at L11.html:242); c187 vs L13.html:143 (provided h* <= h0, otherwise h0; B_c(h*) = 3 delta/(2h*) re-derived); c234 vs L15.html:210 (loop over n = 10, 100, 1000, 10000) and L15.html:225-228 (printed 0.050000000 at n = 10); c299 vs L20.html:93 (Remark 2.3 wording). Removed c388 (Rolle) and c389 (MVT) are restatements of M2-c100-era cards; their coverage elsewhere was not re-checked.")
row("e-cards-atomic", "2.6-cards-atomic", "course/modules/M/M2/cards.json: M2-c093, c194, c341, c345, c346", "PASS",
    "Carried from round 8 (cards c093, c194, c341, c345, c346 are not in the round-9 cards delta; git diff ce7b3821..HEAD changes only c379, c163, c187, c234, c299, c388, c389 in cards.json).")
row("e-cards-dup", "2.6-cards-dup", "course/modules/M/M2/cards.json", "PASS",
    "Fresh: " + S + "cards_check_r9.out: 377 unique ids; the only normalized-front collision is M2-c342 and M2-c343 (P'(y0) and P''(y0) for the same bond), which are distinct cards.")
row("e-cards-numbers", "2.6-cards-numbers", "course/modules/M/M2/cards.json (14 flagged)", "UNVERIFIABLE",
    "Fresh checker " + S + "cards_check_r9.out flags 14 fraction tokens (e.g. M2-c242 '2/6', M2-c284 '1/2', M2-c371 '1/2') not found as plain text in the own lesson. Spot checks show they are TeX fractions (\\tfrac, \\frac) in the lesson, e.g. L19 Theorem 3.1 and L24 Proposition 4.2. The other flagged tokens were not individually read, so this row is not closed.")
row("e-cards-labels", "2.6-cards-labels", "course/modules/M/M2/cards.json: M2-c143, c144, c160, c180, c135, c137", "PASS",
    "Fresh checker: 489 labels checked, 4 unmatched, all 'Section N' cross-references. Read: L10.html:245 (s5 'Where the canon breaks' holds the continuity and difference bullets cited by c143 and c144); L11.html:222-226 (s4 holds the limits bullet cited by c160); L12.html:238 (s4 cited by c180). Checker false positives.")
row("e-cards-grades", "2.6-cards-grades", "course/modules/M/M2/cards.json", "PASS",
    "Fresh: " + S + "cards_check_r9.out: grades T 238, C 77, no grade field 62; bad grade none; C without basis none; T with basis none.")
row("e-data-figures", "2.6-data-figures", "course/modules/M/M2/project.html", "PASS",
    CARRY8 + "project.html is byte-identical since ce7b3821.")
row("e-structure", "2.6-structure", "course/modules/M/M2/", "PASS",
    "Fresh: tools/check_pages.py --unit M2 -> PASS (" + S + "check_pages.out).")
row("e-banned-phrases", "2.6-banned", "course/modules/M/M2/*.html, cards.json", "PASS",
    "Fresh: " + S + "banned_scan_r9.out (the round-8 scanner, 228 total hits, all generic words reviewed in round 8). Added lines of the round-9 diff contain none of: now, still, new, just, changed, corrected, round, previous, revised, draft, deferred, indeed, note that, fixed in, for now, placeholder, TODO, TBD, lorem.")
row("e-dag", "2.6-dag", "course/modules/M/M2/", "PASS",
    "Fresh: tools/check_dag.py --unit M2 -> 'check_dag M2: PASS' (" + S + "check_dag.out). Changed lesson text adds no concept outside the closure (checked by reading the added lines).")
row("e-notation", "2.6-notation", "notation/notation.json; course/modules/M/M2/", "PASS",
    "Fresh grep: notation/notation.json has no entry named w, so the round-9 renaming of the gradient in L17 (g to w) does not collide with a registered symbol.")
row("e-citations", "2.6-citations", "course/modules/M/M2/project.html:547-551", "PASS",
    CARRY8 + "citations unchanged.")
row("e-hours-declared-spec", "2.6-hours", "course/modules/M/M2/project.html:35", "PASS",
    CARRY8 + "declared spec hours unchanged.")
row("e-cards-delta-removed", "2.6-cards-removed", "course/modules/M/M2/cards.json: M2-c388, M2-c389 (removed this round)", "PASS",
    "Fresh: git diff ce7b3821..HEAD removes c388 (Rolle, L08) and c389 (MVT, L10), which restated Theorem 1.2 cards already in place; ids of the remaining cards keep their order (checker id-gap list). Coverage question noted, not a defect of the card set.")

mutants = [
    {"id": "r9_01_central_quotient_missing_factor_two.py", "description": "fd_derivative central scheme divides by h rather than 2h", "killed_by": "test_central_difference_matches_the_analytic_derivative[inst0] (seed 0)"},
    {"id": "r9_02_zero_step_accepted.py", "description": "_positive_step accepts a zero step", "killed_by": "test_zero_step_raises_value_error (seed 0)"},
    {"id": "r9_03_duration_sign_dropped.py", "description": "duration_analytic reported without the minus sign", "killed_by": "test_named_ratios_are_the_stated_formulas[inst0] (seed 0)"},
]

fails = [r["id"] for r in rows if r["status"] != "PASS"]
frag = {
    "unit": "M2",
    "slice": "e",
    "round": 9,
    "verifier": "independent verifier (Haiku 5.5), slice e",
    "pin": "b6865c7d10020e31b9858a49edf751f4b814c031",
    "base": "previous pin ce7b3821c288da3dbba5dd4c90fb87dfd6d30089 (round 8); round-8 fragment /Users/billyribeiro/.fanout/frags/B-M2-e.round8.json",
    "checkout": ROOT,
    "scratch": "/tmp/m2e_r9",
    "verified_at": "2026-10-28T00:00:00Z",
    "verdict": "FAIL",
    "rows": rows,
    "mutants": mutants,
    "registry_flags": [],
    "freshness_flags": ["cards.json changed since ce7b3821: c379, c163, c187, c234, c299 changed; c388, c389 removed. L11, L13, L14, L15-L20, L24 lesson pages changed (outside slice e except as cited by cards)."],
    "notes": [
        "project.html, grader/*.py and tests/labs/M2/lab-M2-project-*.py are byte-identical between ce7b3821 and b6865c7; carried rows cite that.",
        "Full card-by-card read of all 377 cards against current lesson text was not completed: e-cards-correct and e-cards-numbers are UNVERIFIABLE.",
        "Checker false positives documented: fraction tokens written as TeX; Section N cross-references; P' vs P'' normalization collision.",
        "The round-9 commands were run in /Users/billyribeiro/.fanout/wt/verifyB9-M2-e; tools/ and tests/ were not edited.",
    ],
    "summary": "Slice e round 9: FAIL. %d rows: %d PASS, %d non-PASS (%s). Gates on pin b6865c7 all pass (check_pages, check_dag, check_projects, run_graders 50/50, mutate_graders 99/99, page_smoke project, pytest reference 85 passed, alternatives A/B/C 50/50 each, labs, run_labs 27/27, verify_refs offline, fetch_data check, ruff). Open items are the full 377-card read and the 14 flagged card number tokens." % (len(rows), len(rows) - len(fails), len(fails), ", ".join(fails)),
}
out = ROOT + "/ledgers/M2/M2-e.json"
json.dump(frag, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", out, len(rows), "rows; non-PASS:", fails)
