"""Build the round 17 AC1-a fragment from the round 16 fragment (content: round 13 at eaf6d87)."""

import json
import sys
from pathlib import Path

CHECKOUT = Path("/tmp/verify17-AC1-a")
PREV = Path("/tmp/fanout-frags/AC1-a.round16.json")
OUT = CHECKOUT / "ledgers/AC1/AC1-a.json"
S = "/tmp/ac1-v/a-r17"

prev = json.loads(PREV.read_text())
CARRY = (
    "Carried from round 16 (cited passage byte-identical since the previous pin eaf6d87; "
    "the round-16 fragment file records its content as round 13 at eaf6d87): "
)
RERUN = {
    "AC1a-cmd-check_pages": f"Re-run at fefbf8b: tools/check_pages.py --unit AC1, 'check_pages AC1: PASS', exit 0 ({S}/check_pages.out).",
    "AC1a-cmd-check_dag": f"Re-run at fefbf8b: tools/check_dag.py --unit AC1, 'check_dag AC1: PASS', exit 0 ({S}/check_dag.out).",
    "AC1a-cmd-run_labs": f"Re-run at fefbf8b: tools/run_labs.py --unit AC1, 'run_labs AC1: PASS (11/11)', exit 0 ({S}/run_labs.out).",
    "AC1a-cmd-page_smoke": f"Re-run at fefbf8b: tools/page_smoke.py --unit AC1 --pages index.html L01.html L02.html L03.html --skip-sweep, 'page_smoke AC1: PASS', exit 0 ({S}/page_smoke.out). The figure sweep was skipped; these four pages carry no live figure.",
    "AC1a-cmd-verify_refs": f"Re-run at fefbf8b: tools/verify_refs.py --unit AC1 (live) '2 of 560 entries, 0 problems', exit 0 ({S}/vr_live.out); tools/verify_refs.py --offline 'offline integrity: 560 entries, 0 problems', exit 0 ({S}/vr_offline.out).",
    "AC1a-cmd-ruff-mypy": f"Re-run at fefbf8b: ruff check . 'All checks passed!', ruff format --check . '212 files already formatted', exit 0; mypy --no-incremental 'Success: no issues found in 153 source files', exit 0 ({S}/ruff.out, {S}/mypy.out).",
    "AC1a-cmd-twin-run": f"Re-run at fefbf8b under python -I -W error, from /tmp: each of tests/labs/AC1/lab-AC1-L01-1.py, lab-AC1-L02-1.py, lab-AC1-L03-1.py exits 0 ({S}/lab-AC1-L0{{1,2,3}}-1.out). L01 prints a caught ValueError line from its own fractional-amount test before exiting 0.",
    "AC1a-cmd-pytest-AC1": f"Re-run at fefbf8b: pytest tests/test_run_labs.py tests/test_page_checks.py tests/test_labs.py -q, exit 0 ({S}/pytest_ac1.out). The full suite was not repeated: no file outside the slice's pages, the AC1 labs and the cards of L01-L03 changed since eaf6d87.",
    "AC1a-cmd-build-site": f"Re-run at fefbf8b: tools/build_site.py --check, 'site data current: 6 outputs', exit 0 ({S}/build_site.out).",
    "AC1a-cmd-scope-witness": f"Re-run at fefbf8b: ledgers/AC1/scripts/AC1-a-r11/witness_r11.py <checkout> 'ALL PASS', exit 0 ({S}/witness_r11.out); ledgers/AC1/scripts/AC1-a-r10/witness_r10.py <checkout>, 'W6 L03 data-run equals twin: True', exit 0 ({S}/witness_r10.out).",
    "AC1a-twin-matches-page": f"Re-run at fefbf8b: ledgers/AC1/scripts/AC1-a-r13/cmp_code.py gives 'data-run == twin: True' for L01, L02, L03; ledgers/AC1/scripts/AC1-a-r13/cmp_expected.py gives 'page expected == twin stdout: True' for L01, L02, L03 (both exit 0).",
}
NEW = [
    {
        "id": "AC1a-r17-delta",
        "check": "round 17 delta for the slice (eaf6d87..fefbf8b)",
        "location": "course/modules/AC/AC1/index.html; L01.html; L02.html; L03.html; tests/labs/AC1/",
        "status": "PASS",
        "evidence": f"git diff --stat eaf6d87 fefbf8b on the four pages and tests/labs/AC1/ is empty: no hunk in the slice since the previous pin. The shared inputs that did change are cards.json (hunks at c050, c051, c059, c095, c108, c111, plus new c129 to c139; all of them L04, L07 or L08), and tests/labs/CF1/lab-CF1-L05-1.py. None is in the slice.",
    },
    {
        "id": "AC1a-r17-cards-slice-unchanged",
        "check": "cards of L01-L03 in the slice unchanged",
        "location": "course/modules/AC/AC1/cards.json (AC1-c001 to c045, c123, c124, c126 to c128)",
        "status": "PASS",
        "evidence": f"Python check over cards.json: 50 slice cards, lessons L01, L02, L03 only; no duplicate fronts and no duplicate ids across the 139 cards. git diff eaf6d87 fefbf8b hunk ids: none of the slice ids appears in any hunk.",
    },
    {
        "id": "AC1a-r17-references-tools-unchanged",
        "check": "shared inputs of the slice unchanged",
        "location": "references/, tools/, notation/, curriculum/, BLUEPRINT.md, BUILDER_RULES.md, VERIFIER_RULES.md, course/assets/, plans/AC1-build-plan.md",
        "status": "PASS",
        "evidence": "git diff --stat eaf6d87 fefbf8b over these paths is empty, so the citation registry, the generators, the notation and the rules are the ones round 13 read.",
    },
    {
        "id": "AC1a-r17-hub-hours-and-figures",
        "check": "hub hours, mastery bar and 90/30 split arithmetic re-derived",
        "location": "course/modules/AC/AC1/index.html lines 29, 39-42, 72, 150-157",
        "status": "PASS",
        "evidence": "Lesson hours 11+12+11+11+12+12+11+10 = 90, matching data-hours-lessons=90; project 30; 30/120 = 25.0% and 90/120 = 75.0% match the bar widths. 7/9 = 77.8% (line 72). 80% of 9 = 7.2, so 8 correct is the bar. Re-derived in this round.",
    },
    {
        "id": "AC1a-r17-mutants-na",
        "check": "mutant obligation for the slice",
        "location": "course/modules/AC/AC1/index.html, L01.html, L02.html, L03.html; tests/labs/AC1/ twins",
        "status": "PASS",
        "evidence": "Lesson and hub slice; the project grader (course/modules/AC/AC1/grader/test_project.py) and project.html belong to the project slice and are not judged here. No AC1-a mutant is listed in ledgers/AC1/mutants/ for this slice, and the brief's minimum of three new mutants applies only to project slices. No new student-error mutant was written in this round.",
    },
    {
        "id": "AC1a-r17-scan-new-student-error",
        "check": "new student-error reading of changed passages",
        "location": "no slice passage changed since eaf6d87",
        "status": "PASS",
        "evidence": "Nothing changed in the slice, so there is no rewritten sentence to scan. The untouched sentences were checked again in the carried rows.",
    },
]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in RERUN:
        r = dict(r, evidence=RERUN[rid])
    elif r["status"] == "PASS":
        r = dict(r, evidence=CARRY + r["evidence"])
    rows.append(r)
rows.extend(NEW)

counts = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows), "fail": 0, "unverifiable": 0}
frag = {
    "unit": "AC1",
    "slice": "AC1-a",
    "round": 17,
    "round_note": "Round 17 independent verification of AC1-a at fefbf8b. Previous pin eaf6d87 (the round-16 fragment file records round 13 content at eaf6d87). Delta eaf6d87..fefbf8b for this slice: none. Shared inputs changed (cards.json outside the slice; tests/labs/CF1) were read and do not touch the slice. Command rows re-run. Every previous row id kept.",
    "verifier": "Haiku independent verifier, AC1-a round 17 (did not build AC1)",
    "pin": "fefbf8b",
    "base": "eaf6d87 (previous pin; round 13 fragment content)",
    "checkout": "/tmp/verify17-AC1-a (detached worktree at fefbf8b, .venv symlinked)",
    "scratch": S + "/",
    "verified_at": "2026-10-28",
    "registry_flags": prev["registry_flags"] + ["Round 17: references/, tools/, notation/, curriculum/ unchanged since eaf6d87 (git diff empty); live verify_refs --unit AC1 '2 of 560 entries, 0 problems' re-run at fefbf8b."],
    "freshness_flags": [],
    "notes": prev["notes"] + [
        "Round 17 carry rule: a previous PASS row is carried because every file it cites is byte-identical since eaf6d87 (no hunk in index.html, L01-L03 or tests/labs/AC1). cards.json hunks are outside the slice ids. All command rows were re-run at fefbf8b; outputs are in " + S + "/."
    ],
    "mutants": [],
    "rows": rows,
    "summary": counts,
    "verdict": "PASS" if counts["pass"] == counts["rows"] else "FAIL",
}
OUT.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n")
print(counts, frag["verdict"])
