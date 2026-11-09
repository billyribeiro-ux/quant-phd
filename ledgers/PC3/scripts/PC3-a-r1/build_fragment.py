"""Build ledgers/PC3/PC3-a.json (round 1, closing delta of slice a) from the round-12 base fragment.

Rows whose subject changed since 5db69a9b, or that are gate rows, are re-verified (evidence rewritten, status
PASS only with the command output in outputs/). Every other row is carried with the carry prefix. Row ids are kept.
Read-only with respect to the course; it writes only the fragment.
"""

import json
from pathlib import Path

CHECKOUT = Path("/Users/billyribeiro/.fanout/wt/verifyF31-PC3-a")
BASE = Path("/Users/billyribeiro/.fanout/frags/E-PC3-a.round12.json")
OUT = CHECKOUT / "ledgers/PC3/PC3-a.json"
O = "ledgers/PC3/scripts/PC3-a-r1/outputs"

SLICE = (
    "course/modules/PC/PC3/index.html, L01.html, L02.html, L03.html and tests/labs/PC3/lab-PC3-L01-1.py, "
    "L02-1.py, L03-1.py"
)
CARRY = "Carried from round 12 (" + SLICE + " byte-identical since the previous pin 5db69a9b): "
EXTRA_CARRY = {
    "PC3a-hub-P0.1-claim": "Carried from round 12 (" + SLICE + " and course/concepts.html byte-identical since 5db69a9b): ",
    "PC3a-notation": "Carried from round 12 (" + SLICE + " and notation/notation.json byte-identical since 5db69a9b): ",
    "PC3a-L02-spaced-repetition": (
        "Carried from round 12 (" + SLICE + ", course/review.html and curriculum/06-profession-capstone.yaml "
        "byte-identical since 5db69a9b): "
    ),
    "PC3a-r10-process-and-dag-terms": (
        "Carried from round 12 (" + SLICE + " byte-identical since 5db69a9b; plans/PC3-build-plan.md section 4 "
        "lines 284-302 unchanged, the plan hunks of 5db69a9b..95f3f8cb are at lines 316 and 403-417 only): "
    ),
}

RERUN = {
    "PC3a-check-pages": (
        "Re-run at 95f3f8cb (whole unit, because project.html, L04-L06, grader and cards.json changed since 5db69a9b): "
        "tools/check_pages.py --unit PC3 printed 'check_pages PC3: PASS', exit 0 (" + O + "/check_pages.out, exit_codes.txt)."
    ),
    "PC3a-check-dag": (
        "Re-run at 95f3f8cb: tools/check_dag.py --unit PC3 printed 'check_dag PC3: PASS', exit 0 (" + O + "/check_dag.out). "
        "Independent link scan of the four slice pages (ledgers/PC3/scripts/PC3-a-r1/link_scan.py, " + O + "/link_scan.out): "
        "84 local hrefs, 0 missing files, 0 missing anchors, exit 0."
    ),
    "PC3a-check-projects": (
        "Re-run at 95f3f8cb (project.html changed since 5db69a9b): tools/check_projects.py --unit PC3 printed "
        "'check_projects PC3: PASS', exit 0 (" + O + "/check_projects.out)."
    ),
    "PC3a-run-labs": (
        "Re-run at 95f3f8cb: tools/run_labs.py --unit PC3 printed 'run_labs PC3: PASS (9/9)', exit 0 (" + O + "/run_labs_unit.out); "
        "per page L01, L02, L03 each 'PASS (1/1)' (" + O + "/run_labs_L0{1,2,3}.out). The tool compares each page's code with its "
        "twin and each expected block with the twin's output; this round's run is the source of the PASS, and the twins are "
        "byte-identical to 5db69a9b (PC3a-r10-twins-unchanged)."
    ),
    "PC3a-twins-alone": (
        "Re-run at 95f3f8cb: each slice twin alone under 'python -I -W error' in a fresh mktemp directory: L01 exit 0, "
        "26 stdout lines; L02 exit 0, 32 lines; L03 exit 0, 30 lines; stderr empty for all three; stdout byte-identical to the "
        "round-12 twin outputs (ledgers/PC3/scripts/PC3-a-r12/outputs/twin-L0x-1.stdout). Copies in " + O + "/twin-L0x-1.stdout."
    ),
    "PC3a-pytest-labs": (
        "Re-run at 95f3f8cb: .venv/bin/pytest -q -k PC3 exit 0, nine dots, 100 percent (" + O + "/pytest_pc3.out)."
    ),
    "PC3a-page-smoke": (
        "Re-run at 95f3f8cb, each slice page alone: tools/page_smoke.py --unit PC3 --pages index | L01 | L02 | L03 printed "
        "'page_smoke PC3: PASS', exit 0 (" + O + "/page_smoke_index.out, page_smoke_L01.out, page_smoke_L02.out, page_smoke_L03.out)."
    ),
    "PC3a-ruff-mypy": (
        "Re-run at 95f3f8cb (pyproject.toml changed since 5db69a9b, an extend-exclude entry only): ruff check tests/labs/PC3 "
        "'All checks passed!' exit 0; ruff format --check '9 files already formatted' exit 0; mypy --no-incremental "
        "tests/labs/PC3 'Success: no issues found in 9 source files' exit 0 (" + O + "/ruff_check.out, ruff_format.out, mypy.out)."
    ),
    "PC3a-verify-refs": (
        "Re-run at 95f3f8cb (references/references.json changed since 5db69a9b: generated_at and the used_by of the Black and "
        "Scholes record, now DV1 and FC2; no PC3 key changed): offline 'offline integrity: 560 entries, 0 problems', exit 0 "
        "(" + O + "/verify_refs_offline.out); live 'live re-verification of PC3: 2 of 560 entries, 0 problems', exit 0 "
        "(" + O + "/verify_refs_unit_live.out)."
    ),
    "PC3a-hub-hours": (
        "Re-run (project.html time budget changed text only): index.html:29 data-hours-lessons=36 and data-hours-project=14; "
        "index.html:42 '36 h lessons · 14 h project (28%)'; index.html:167 '1 + 1 + 3 + 2 + 2 + 4 + 1 = 14'. project.html:419-436 "
        "time-budget rows 1, 1, 3, 2, 2, 4, 1 and total 14 (same seven lines). Lesson hours L01-L03 data-hours=6 (x6 = 36). "
        "L04-L06 data-hours unchanged (no hunk in the diff). Sum 36 + 14 = 50. Consistent."
    ),
    "PC3a-hub-lesson-map": (
        "Re-run (L04-L06 changed; hub lesson map unchanged): index.html:145-150 lesson map; link scan (" + O + "/link_scan.out) "
        "resolves every lesson link with 0 problems; L04-L06 h1 titles unchanged ('Market-making games and inventory risk' at L04.html:36, "
        "'Timed coding interviews' at L05.html:36, 'Technical finance questions and case interviews' at L06.html:36)."
    ),
    "PC3a-hub-objectives": (
        "Re-run for objective 7 (index.html:55 'pass the autograder on seeds 0 to 49 and on your own workspace seed') against the "
        "changed grader: course/modules/PC/PC3/grader/test_project.py:10 names the fixed seeds 0 to 49, the learner's SEED and "
        "SEED + 7919; line 37 FIXED_SEEDS = tuple(range(50)); line 38 SEEDS includes SEED + 7_919. Objectives 1-6 unchanged "
        "(index.html:47-54 byte-identical)."
    ),
    "PC3a-hub-data": (
        "Re-run against the changed project and grader: grep of course/modules/PC/PC3/project.html, grader/*.py, "
        "tests/labs/PC3/lab-PC3-project-*.py and L04-L06 for data-files, 'data/', open(, read_text and .csv found no input file "
        "read. The only .json hits are data-cards=\"cards.json\" on the L04-L06 quiz sections and project.html:393, which names "
        "game_log.json as a file the learner's own run writes (output, not data). index.html:37 and 170-173 unchanged and consistent."
    ),
    "PC3a-r6-hub-ladder-rung2-wording": (
        "Re-verified; project.html changed since 5db69a9b. project.html:42 now reads 'If you reached the mastery bar and answered "
        "both skill checks on the module page'; rung 2 at project.html:45 unchanged. index.html:156 reads 'Rungs 1 and 2 "
        "scaffold the skills the placement check tests. To skip them, a student must reach the placement bar and answer both "
        "skill checks.' index.html:74 defines 'The mastery bar is 80 percent'. Both name the same skip condition (the 80 percent "
        "bar on the placement diagnostic plus both skill checks). The term differs ('placement bar' in the hub at index.html:156, "
        "'mastery bar' in the project and index.html:74). This is a LOW wording inconsistency, not a ruling-26 kind; see notes."
    ),
    "PC3a-r6-hub-project-file-names": (
        "Re-verified; project.html changed. The hub names market_maker.py (index.html:160 and 167 region, 2 occurrences) and "
        "analysis.md (index.html:160, 1 occurrence). project.html names market_maker.py (9), analysis.md (4), self_assessment.md (3), "
        "game_log.json (393, learner output), grader/test_project.py (2). The grader/ directory holds engine.py, instance.py, "
        "reference.py, starter.py and test_project.py (ls). No file name conflicts."
    ),
    "PC3a-r6-hours-curriculum-attribution": (
        "Re-verified: index.html:167 states the project as 14 hours split into seven lines; project.html:419-436 Time budget totals 14 "
        "(rows 1, 1, 3, 2, 2, 4, 1). Consistent with the re-run of PC3a-hub-hours."
    ),
    "PC3a-r7-hub-hours-line-items": (
        "Re-verified; project.html:419-436 changed text only. Lines 1 (rung 1), 1 (rung 2), 3 (quote), 2 (replay), 2 (autograder), "
        "4 (analysis), 1 (self-assessment) total 14; index.html:167 gives the same seven figures, and the project total row says "
        "'Equals the project hours in the hub: 14 of the module's 50, or 28.0 %.' Consistent."
    ),
    "PC3a-r7-hub-autograder-seeds": (
        "Re-verified against the changed grader: course/modules/PC/PC3/grader/test_project.py:10 names seeds 0 to 49, the "
        "learner's SEED and SEED + 7919; lines 37-38 define FIXED_SEEDS = range(50) and SEEDS = (0..49, SEED, SEED + 7919). "
        "index.html:55 (objective 7) and index.html:160 say the autograder runs on seeds 0 to 49, on the workspace seed and on "
        "that seed plus 7919. Consistent. The hub states no check count (grep for 486, 489, 495, 498 in index.html: no match)."
    ),
    "PC3a-r10-hub-claims-outside-slice": (
        "Re-verified for every hub claim about pages outside the slice: index.html:33-37 (project graded by autograder and rubric; "
        "data none; project does not read a data file), 143-150 (lesson titles and 6-hour lessons; titles unchanged), 160-161 "
        "(autograder seeds, rung 4), 167 (hours; 14), 172 (no real data). project.html and grader hunks read for these claims. "
        "L04-L06 hunks change text only, not titles or hours. Consistent."
    ),
    "PC3a-r4-delta-read": (
        "Round-1 delta read: git diff 5db69a9b..95f3f8cb for index.html, L01-L03 and the three slice twins is empty (blob hashes "
        "identical, see PC3a-r10-twins-unchanged). Out-of-slice hunks read for hub claims: project.html (all hunks), grader/"
        "test_project.py (header and seed definitions), L04.html, L05.html, L06.html and lab-PC3-L06-1.py (text, titles, hours), "
        "M/M4/L01.html (cited definitions), plans/PC3-build-plan.md (hunks at 316, 403, 417), curriculum/01-foundations.yaml "
        "and course/assets/data/program.json (not PC3 surfaces; M4 brief), references/references.json (not a PC3 key)."
    ),
    "PC3a-r10-twins-unchanged": (
        "Re-verified: git diff --name-only 5db69a9b 95f3f8cb for tests/labs/PC3/lab-PC3-L01-1.py, L02-1.py, L03-1.py is empty; "
        "blob hashes ece5093230115ea63a4551a224c16f9ce07b9298, 3a3f2995acceb7d12be1887a00d01fe21dc9387f, "
        "09d3b859118c39a1fb5b2d6e836ee2940665fd5b are identical at 5db69a9b and 95f3f8cb."
    ),
    "PC3a-r6-def21-m4-weights-positivity": (
        "Re-verified; M4 Lesson 1 changed (course/modules/M/M4/L01.html: meta description and the right-continuity sentence "
        "(d) only). The finite probability space definition at M4 L01 (lines 55-59) is unchanged; PC3 L02.html:57 and L03.html:57 "
        "still cite M4 Lesson 1 for it and for the events, and PC3 L02.html:57 keeps Definition 2.1 as the PC3 numbering."
    ),
    "PC3a-r4-restated-M4-concepts": (
        "Re-verified; M4 pages changed. PC3 L02.html:57, 67 and L03.html:62 link M4 concepts; link scan (" + O + "/link_scan.out) "
        "finds 0 missing targets and 0 missing anchors; check_dag PASS (" + O + "/check_dag.out)."
    ),
    "PC3a-L02-finite-probability-space-redefined": (
        "Re-verified; M4 Lesson 1 changed only as stated above. PC3 L02.html:57 and :62 cite M4 Lesson 1 "
        "(course/modules/M/M4/L01.html) for the finite probability space; the definition at M4 L01 lines 55-59 is present; "
        "link scan 0 problems."
    ),
    "PC3a-r4-recompute-all-numbers": (
        "Re-run: python3 -I ledgers/PC3/scripts/PC3-a-r12/numbers_r12.py exit 0; output identical to the round-12 output "
        "(diff -q empty; " + O + "/numbers_r12_rerun.out). Slice pages byte-identical."
    ),
}

NOTES_ROW_ID_NOTE = "All 85 row ids of the round-12 base are kept; no row is added or removed."


def main() -> None:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    rows = []
    for r in base["rows"]:
        row = dict(r)
        rid = row["id"]
        if rid in RERUN:
            row["status"] = "PASS"
            row["evidence"] = RERUN[rid]
            if rid == "PC3a-r6-hub-ladder-rung2-wording":
                row["location"] = "index.html:156, 74; course/modules/PC/PC3/project.html:42, 45"
        else:
            prefix = EXTRA_CARRY.get(rid, CARRY)
            row["evidence"] = prefix + r["evidence"]
        rows.append(row)
    print(f"base rows {len(base['rows'])}, fragment rows {len(rows)}, rerun {sum(1 for r in base['rows'] if r['id'] in RERUN)}")
    missing = [k for k in RERUN if k not in {r['id'] for r in base['rows']}]
    print("RERUN ids not in base:", missing)
    fragment = {
        "unit": "PC3",
        "slice": "PC3-a",
        "round": 1,
        "verifier": "Claude Haiku 5.5, independent verifier PC3 slice a, round 1 closing delta (ruling 30); did not build PC3",
        "pin": "95f3f8cb21c2cd9fc904430bd30a6b734d01f672",
        "base": "5db69a9bee460736c318ebfacc7200ee5a6eb0f0 (the round-12 pin; base fragment ~/.fanout/frags/E-PC3-a.round12.json, verdict PASS, 85 rows)",
        "checkout": "/Users/billyribeiro/.fanout/wt/verifyF31-PC3-a (detached at 95f3f8cb; .venv symlinked to /Users/billyribeiro/dev/quant-phd/.venv)",
        "scratch": "ledgers/PC3/scripts/PC3-a-r1/outputs (gate outputs, twin stdout, numbers rerun); twin runs in fresh mktemp directories under /tmp/pc3a-r1-twins.*",
        "verified_at": "2026-11-09T00:00:00+00:00",
        "verdict": "PASS",
        "scope": base["scope"],
        "rows": rows,
        "mutants": [],
        "registry_flags": [
            "references/references.json changed since 5db69a9b (generated_at 2026-11-09; the Black and Scholes record used_by now DV1 and FC2). No PC3 key changed. Live verify_refs --unit PC3: 2 of 560 entries, 0 problems (" + O + "/verify_refs_unit_live.out). Offline: 560 entries, 0 problems."
        ],
        "freshness_flags": [
            "course/assets/data/program.json changed since 5db69a9b (one M4 project brief, generated). Not a PC3 surface; check_pages PASS at 95f3f8cb."
        ],
        "notes": [
            "Delta since 5db69a9b: git diff --name-only over the slice paths (index.html, L01-L03, the three slice twins) is empty, so no slice row subject changed. Changed out-of-slice subjects the slice cites: project.html, grader/test_project.py, L04-L06 (text and the L06 twin), M4 L01, plans/PC3-build-plan.md (sections 5.x), references/references.json (B&S record, not PC3), program.json (M4 brief). Every row that cites one of these was re-verified (see the evidence of each RERUN row); every other row is carried with the carry prefix.",
            "Ruling 26 kinds checked on the re-verified rows: no false or unproved statement, missing hypothesis, wrong number, over-graded claim, failing gate, surviving non-equivalent mutant, or lab statement the code does not support was found in slice a. Hub hours sum to 50 (36 + 14), the project time budget sums to 14, and the autograder seed claims match grader/test_project.py.",
            "Observation (LOW wording, not a ruling-26 kind, not counted as a FAIL): index.html:156 says 'the placement bar' where project.html:42 (changed this delta) and index.html:74 say 'the mastery bar' for the same 80 percent skip condition. Suggested fix for the slice-a owner: change 'placement bar' to 'mastery bar' at index.html:156. The fix is in a slice-a file, so it is recorded here and not edited.",
            "Mutants: none. Slice a has no grader (ruling: lab twins are demonstrations), so the standing mutant set is empty; ruling 37 forbids new mutants in a closing round. The base had no mutants either.",
            "Ruling 23 blind calibration: not applicable to slice a (no rubric exemplars in index, L01-L03).",
            NOTES_ROW_ID_NOTE,
            "Not checked in this round: run_graders and mutate_graders (slice a has no grader; the project and grader slices carry those); the live Crossref path (no Crossref call is made by verify_refs --unit PC3; the live run is the registry's openlibrary-verified records, 2 entries, exit 0); fetch_data --check (no data in PC3); cards.json (not in slice a; changed since 5db69a9b but outside this slice's paths).",
        ],
        "summary": None,
    }
    counts = {"rows": len(rows), "pass": sum(1 for r in rows if r["status"] == "PASS"), "fail": 0, "unverifiable": 0, "mutants_killed": 0, "mutants_total": 0}
    fragment["summary"] = counts
    OUT.write_text(json.dumps(fragment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", OUT, counts)


if __name__ == "__main__":
    main()
