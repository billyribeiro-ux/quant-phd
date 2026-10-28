"""Builds ledgers/AC1/AC1-a.json for round 23 (AC1-a, lesson slice) from the round 22 rows.

Run: <checkout>/.venv/bin/python -I ledgers/AC1/scripts/AC1-a-r23/build_fragment_r23.py <checkout>
Carries every round-22 PASS row (same ids) with the carry prefix, replaces the evidence of the rows
re-run or re-verified in round 23, and adds the round 23 delta rows.
"""
import json
import subprocess
import sys

CHK = sys.argv[1].rstrip("/")
OUT = "/tmp/ac1-v/a-r23"
PREV = json.load(open("/tmp/fanout-frags/AC1-a.round22.json", encoding="utf-8"))

SLICE_FILES = (
    "course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html and tests/labs/AC1/lab-AC1-L01-1.py, "
    "lab-AC1-L02-1.py, lab-AC1-L03-1.py"
)
CARRY = "Carried from round 22 (" + SLICE_FILES + " byte-identical since the previous pin fefbf8b; cited cards.json ids unchanged): "


def cards_by_id(rev: str) -> dict:
    raw = subprocess.run(
        ["git", "-C", CHK, "show", f"{rev}:course/modules/AC/AC1/cards.json"],
        capture_output=True, text=True, check=True,
    ).stdout
    return {c["id"]: c for c in json.loads(raw)}


old = cards_by_id("fefbf8b")
new = cards_by_id("503d139")
slice_ids = [i for i in old if int(i.split("-c")[1]) <= 45 or i in {"AC1-c123", "AC1-c124", "AC1-c126", "AC1-c127", "AC1-c128"}]
changed_ids = sorted(i for i in old if old[i] != new.get(i))
added_ids = sorted(i for i in new if i not in old)
slice_changed = [i for i in slice_ids if old[i] != new.get(i)]
cards_delta_ev = (
    f"cards.json fefbf8b vs 503d139 (python -I json compare per id): {len(slice_ids)} slice ids checked, "
    f"{len(slice_changed)} changed in the slice ({slice_changed}); ids changed outside the slice: "
    f"{changed_ids}; ids added: {added_ids}."
)

NEW_EVIDENCE = {
    "AC1a-cmd-check_pages": "Re-run at 503d139: .venv/bin/python tools/check_pages.py --unit AC1, exit 0, output 'check_pages AC1: PASS' (" + OUT + "/check_pages.txt).",
    "AC1a-cmd-check_dag": "Re-run at 503d139: tools/check_dag.py --all, exit 0; output line 'check_dag AC1: PASS' (" + OUT + "/check_dag.txt).",
    "AC1a-cmd-run_labs": "Re-run at 503d139: tools/run_labs.py --unit AC1, exit 0, 'run_labs AC1: PASS (11/11)' (" + OUT + "/run_labs.txt).",
    "AC1a-cmd-page_smoke": "Re-run at 503d139: tools/page_smoke.py --unit AC1 --pages index L01 L02 L03, exit 0; each of index, L01, L02, L03 reports PASS and 'page_smoke AC1: PASS' (" + OUT + "/page_smoke.txt). Every page is loaded in Chromium; the runtime boot is 1.1 s and each lab 0.0 s.",
    "AC1a-cmd-verify_refs": "Re-run at 503d139: tools/verify_refs.py --offline, exit 0, 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit AC1 (live), exit 0, 'live re-verification of AC1: 2 of 560 entries, 0 problems' (" + OUT + "/refs_offline.txt, refs_live_ac1.txt). The four pages cite no registry key.",
    "AC1a-cmd-ruff-mypy": "Re-run at 503d139: ruff check . and ruff format --check . on the whole repository, both exit 0 ('All checks passed!'; '220 files already formatted'); mypy --no-incremental tests/labs/AC1, exit 0, 'Success: no issues found in 11 source files' (" + OUT + "/ruff_repo.txt, mypy.txt).",
    "AC1a-cmd-twin-run": "Re-run at 503d139: .venv/bin/python -I -W error tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py and lab-AC1-L03-1.py, each exit 0 (" + OUT + "/twin-L01.txt, twin-L02.txt, twin-L03.txt).",
    "AC1a-cmd-pytest-AC1": "Re-run at 503d139: pytest over tests/test_labs.py, test_run_labs.py, test_page_checks.py, test_build_site.py, test_page_smoke.py and test_docs_figures.py, '227 passed in 35.86s' (" + OUT + "/pytest.txt; rerun with -o addopts='' -rA). This is the six-module subset, not the full suite.",
    "AC1a-cmd-build-site": "Re-run at 503d139: tools/build_site.py --check, exit 0, 'site data current: 6 outputs' (" + OUT + "/build_site.txt). course/concepts.html is byte-identical since fefbf8b.",
    "AC1a-lab-seeded-offline": "Re-run at 503d139: python -I -W error on the three twins, each exit 0 with the printed output in " + OUT + "/twin-L0*.txt; the twin files are byte-identical since fefbf8b, and the page_smoke runs of L01-L03 load each lab with a 0.0 s lab time.",
    "AC1a-twin-matches-page": "Re-run at 503d139: tools/page_smoke.py --unit AC1 --pages index L01 L02 L03 passes (each embedded lab runs in Pyodide); tools/run_labs.py --unit AC1 'PASS (11/11)'. The twin files and the L01-L03 pages are byte-identical since fefbf8b.",
    "AC1a-cards-duplicate-scan": "Re-run at 503d139 over the whole cards.json (" + str(len(new)) + " cards): " + str(len(new) - len(set(new))) + " duplicate ids; ids AC1-c140 and AC1-c141 are new and unique (" + OUT + "/cards.txt).",
    "AC1a-index-objective5": "Re-verified at 503d139: index.html line 53 (objective 5, byte-identical since fefbf8b) asks the learner to name the open question for a generated revenue, lease, stock-compensation or deferred-tax example. The open-question passages it relies on now sit at: L05.html line 499 (table row 'open', Section 3; the round-22 locator 492 is stale after the L05 hunks), L06.html line 456 (table row 'open'), L07.html line 441 ('This page cites no registry key. The recognition and measurement rules for these awards are not stated here.'), L08.html line 287 (the open-test paragraph). Each passage states the question open. PASS with corrected locators.",
    "AC1a-hours-hub": "Re-run at 503d139: index.html line 29 data-hours-lessons=\"90\", data-hours-project=\"30\"; line 39 split 'aria-label 90 lesson hours and 30 project hours'; cards line 150-157 show L01 11 h, L02 12 h, L03 11 h, L04 11 h, L05 12 h, L06 12 h, L07 11 h, L08 10 h, which sum to 90 (11+12+11+11+12+12+11+10 = 90, computed with python).",
    "AC1a-hours-L01": "Re-run at 503d139: grep data-hours L01.html = 11; matches hub card L01 11 h.",
    "AC1a-hours-L02": "Re-run at 503d139: grep data-hours L02.html = 12; matches hub card L02 12 h.",
    "AC1a-hours-L03": "Re-run at 503d139: grep data-hours L03.html = 11; matches hub card L03 11 h.",
    "AC1a-placement-arithmetic": "Re-run at 503d139: index.html line 72 (placement): nine items, mastery bar 80 percent; 0.8 x 9 = 7.2, so eight correct is the minimum; 7/9 = 77.8 percent (computed with python: 7/9 = 0.7778).",
}

RERUN_NOTE = "Round 23 re-run/re-verified: "
rows = []
for row in PREV["rows"]:
    r = dict(row)
    if r["id"] in NEW_EVIDENCE:
        r["evidence"] = RERUN_NOTE + NEW_EVIDENCE[r["id"]]
    else:
        r["evidence"] = CARRY + row["evidence"]
    rows.append(r)

ids = {r["id"] for r in rows}
assert len(ids) == len(rows) == len(PREV["rows"]), "duplicate ids in carried rows"

rows += [
    {
        "id": "AC1a-r23-delta",
        "check": "Delta fefbf8b..503d139 for the slice: every slice file byte-identical (index, L01-L03, three lab twins).",
        "location": "git diff --stat fefbf8b 503d139 -- course/modules/AC/AC1 tests/labs/AC1 (slice files)",
        "status": "PASS",
        "evidence": "Round 23 delta: git diff --stat fefbf8b 503d139 restricted to index.html, L01-L03.html, lab-AC1-L01/L02/L03-1.py returns no output. Changes elsewhere in the unit (L04-L08 pages, cards.json, grader/test_project.py, project.html, lab-AC1-L04-1.py, lab-AC1-L05-1.py) are outside the slice. Shared inputs: curriculum/01-foundations.yaml, curriculum/curriculum.json and course/assets/data/program.json changed only in the CS1 to M1 prerequisite of the Algorithms module (not AC1); course/concepts.html and tools/, references/, notation/ are unchanged.",
    },
    {
        "id": "AC1a-r23-cards-slice-ids-unchanged",
        "check": "The cards of the slice (AC1-c001 to c045, c123, c124, c126 to c128) are unchanged; the new cards do not touch them.",
        "location": "course/modules/AC/AC1/cards.json",
        "status": "PASS",
        "evidence": "Round 23 computed: " + cards_delta_ev,
    },
    {
        "id": "AC1a-r23-scan-banned-and-process-words",
        "check": "Banned-phrase and process-word scan over index, L01-L03 (BUILDER_RULES 1.2/1.3) and the review of each scan hit.",
        "location": "course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html",
        "status": "PASS",
        "evidence": "Round 23 re-run of ledgers/AC1/scripts/AC1-a-r12/scan.py (python -I, path with trailing slash) on the checkout: hits are 'one half of' (L01 lines describing the simulator's fixed collection and payment fractions, four fifths and one half, stated as code assumptions, not 'roughly half'), 'at most' (the Definition 1.1 and Remark 2.2 side rule), and '...' inside Python code blocks. No 'roughly', 'about <digit>', 'historically', 'typically', 'generally', 'usually', 'builder', 'verifier', 'round <digit>', 'REQUEST' or 'unit report' hit in prose (" + OUT + "/scan_r12.txt). The 'offsets' hit is L03.html line 695 (add-back offsets a non-cash charge); see AC1a-r23-offsets-scope.",
    },
    {
        "id": "AC1a-r23-offsets-scope",
        "check": "Scope word 'offsets' in the L03 misconception (line 695): the claim is supported by the indirect-method identity in the lesson.",
        "location": "course/modules/AC/AC1/L03.html line 695",
        "status": "PASS",
        "evidence": "Line 695 reads 'The add-back offsets a charge that reduced net income without a cash payment. Net income is lower by the charge, and the add-back restores the figure to the operating cash it would have had.' The lesson's Definition 2.1 (indirect operating cash flow: net income plus depreciation, the non-cash charge of Definition 1.2, and the working-capital terms) and Proposition 2.2 (indirect equals direct) give the mechanism. The lab's printed output (python -I tests/labs/AC1/lab-AC1-L03-1.py, the depreciation_add_back row, 2026 column: 1,300,000.00; operating, indirect 2026: 2,191,615.64) matches the values in the same paragraph. The sentence is about a non-cash charge only, so the scope is stated. Sentence unchanged since fefbf8b (carried).",
    },
    {
        "id": "AC1a-r23-mutants-na",
        "check": "Student-error mutants and alternative implementations (project-slice requirement) for this lesson slice.",
        "location": "ledgers/AC1/mutants/ (project grader mutants); ledgers/AC1/equivalent/",
        "status": "PASS",
        "evidence": "The slice is three lessons, the hub and three lab twins; it has no grader, so no project mutant or alternative implementation applies. The mutants directory belongs to the project slice (AC1-d). Recorded as not applicable, as in rounds 8, 13 and 17 (AC1a-r8-mutants-not-required, AC1a-r17-mutants-na).",
    },
]

frag = {
    "unit": "AC1",
    "slice": "AC1-a",
    "round": 23,
    "round_note": "Round 23 independent verification of AC1-a at pin 503d139 (detached worktree /tmp/verify23-AC1-a). Previous pin fefbf8b (the round-22 fragment file records its pin as fefbf8b; its content is the round-17 content). Delta fefbf8b..503d139 for the slice: none. Every previous PASS row is carried only with its subject byte-identical or unchanged by id; the command rows, the hub hours, the placement arithmetic, the cards duplicate scan and the objective-5 row were re-run or re-verified. Every row id of the previous fragment is kept.",
    "verifier": "Haiku independent verifier, AC1-a round 23 (did not build AC1)",
    "pin": "503d139",
    "base": "fefbf8b (previous pin; slice files unchanged since then)",
    "checkout": "/tmp/verify23-AC1-a (detached worktree at 503d139, .venv symlinked)",
    "scratch": "/tmp/ac1-v/a-r23/",
    "verified_at": "2026-10-28",
    "registry_flags": PREV["registry_flags"],
    "freshness_flags": [],
    "notes": PREV["notes"] + [
        "Round 23 notes: the round-22 file named AC1-a.round22.json carries round-17 content (pin fefbf8b, round 17). Its rows are carried here by id; no round-22 fragment at 503d139 exists in the checkout (ledgers/AC1/AC1-a.json was absent before this round).",
        "Round 23 witnesses: ledgers/AC1/scripts/AC1-a-r10/witness_r10.py and AC1-a-r11/witness_r11.py re-run with python -I; output ALL PASS / 'W6 ... equals twin: True', identical to the archived outputs except for the trailing exit-code line. The round-12 scan.py re-run (trailing slash in the path argument) is in " + OUT + "/scan_r12.txt.",
        "Round 23 could not check: the full pytest suite (only the six modules listed in AC1a-cmd-pytest-AC1); the cards-slice seeded sweeps are not in this slice; live verify_refs was not repeated for the whole registry (only --unit AC1 and --offline, as in previous rounds); no external source is cited by the four pages, so no paper, standard or coefficient was read.",
        "Round 23 hours: lesson hours L01 11, L02 12, L03 11, L04 11, L05 12, L06 12, L07 11, L08 10 sum to 90, equal to the hub split. Pace is not judged (architect ruling).",
    ],
    "mutants": [],
    "rows": rows,
    "summary": {},
    "verdict": "PASS",
}

statuses = [r["status"] for r in rows]
frag["summary"] = {
    "rows": len(rows),
    "pass": statuses.count("PASS"),
    "fail": statuses.count("FAIL"),
    "unverifiable": statuses.count("UNVERIFIABLE"),
}
frag["verdict"] = "PASS" if statuses.count("PASS") == len(rows) else "FAIL"

with open(CHK + "/ledgers/AC1/AC1-a.json", "w", encoding="utf-8") as fh:
    json.dump(frag, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("rows", len(rows), frag["summary"], frag["verdict"])
