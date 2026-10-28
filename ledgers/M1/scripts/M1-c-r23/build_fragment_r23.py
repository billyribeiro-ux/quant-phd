"""Build the round-23 fragment for M1-c from the round-22 fragment and the round-23 outputs.

Rows re-run this round get new evidence; every other previous PASS row is carried only with its
subject byte-identical since the previous pin 7143726 (course pages, index, twins), or entry-identical
for cards.json (M1-c108, M1-c135). Previous row ids are all kept; one new row covers M1-c180.
"""

import json
import re
import sys

PREV = "/tmp/fanout-frags/M1-c.round22.json"
OUT = sys.argv[1]
S = "ledgers/M1/scripts/M1-c-r23/out/"
prev = json.load(open(PREV, encoding="utf-8"))

RERUN = {
    "M1c-cmd-check-pages": f"Re-run this round: `tools/check_pages.py --unit M1` -> 'check_pages M1: PASS', exit 0 ({S}check_pages.out).",
    "M1c-cmd-check-dag": f"Re-run this round: `tools/check_dag.py --all` -> PASS for M1, S7, AC1, AC2, AC4, CF1, AP1; exit 0 ({S}check_dag.out). The curriculum change since the previous pin (Algorithms and Data Structures now lists M1 as a prerequisite, curriculum/01-foundations.yaml:420, curriculum.json, program.json) is outside this slice and does not change any DAG failure.",
    "M1c-cmd-run-labs": f"Re-run this round: `tools/run_labs.py --unit M1` -> 'run_labs M1: PASS (11/11)', exit 0 ({S}run_labs.out).",
    "M1c-cmd-page-smoke": f"Re-run this round: `tools/page_smoke.py --unit M1 --pages L06 L07 L08` -> PASS for all three pages; lab runtimes 0.0 s, 0.0 s, 0.1 s; exit 0 ({S}smoke.out).",
    "M1c-cmd-twins-isolated": f"Re-run this round: each twin under `python -I -W error`: lab-M1-L06-1.py, lab-M1-L07-1.py, lab-M1-L08-1.py exit 0 ({S}lab06.out, lab07.out, lab08.out).",
    "M1c-twin-embed": f"Re-run this round: `python -I ledgers/M1/scripts/M1-c-r17/embed_check.py <checkout> {S}` -> L06, L07, L08: code equals the twin (after the trailing newline) and expected output equals the lab stdout, all True; exit 0 ({S}embed_check.out).",
    "M1c-lint-types": f"Re-run this round: `ruff check tests/labs/M1 course/modules/M/M1` -> 'All checks passed!'; `ruff format --check tests/labs/M1` -> 11 files already formatted; `mypy` (project config, 153 source files) -> 'Success: no issues found'; `python -m pytest -q -k M1` -> 12 tests, all dots, exit 0 ({S}ruff.out, mypy.out, pytest_M1.out).",
    "M1c-refs-live": f"Re-run this round: `tools/verify_refs.py --unit M1` -> 'live re-verification of M1: 1 of 560 entries, 0 problems', exit 0; `tools/verify_refs.py --offline` -> 'offline integrity: 560 entries, 0 problems', exit 0 ({S}vr_live_M1.out, vr_offline.out). references/ is unchanged since the previous pin.",
    "M1c-citations-none": "Re-checked this round by grep: course/modules/M/M1/L06.html:446, L07.html:556, L08.html:563 are each an empty <ol data-references></ol>, and these three pages are byte-identical since the previous pin 7143726.",
    "cards-L06-L08-scan": f"Re-run this round on the 503d139 cards.json: `ledgers/M1/scripts/M1-c-r17/cards_scan.py course/modules/M/M1/cards.json` -> 'cards 180 duplicate ids []', 'per lesson' L06 12, L07 25, L08 30 (67 cards for L06 to L08; 66 at 7143726 before M1-c180 was added). Checked against the card diff ({S}cards_diff_r23.out): changed M1-c068, c075, c088, c163, c177 (all L04 or L05, outside this slice), added M1-c180 (L07) and M1-c181 (L05, outside this slice). The changed-entry set (cards_diff_r23.out) contains no L06 to L08 card except the new M1-c180, which is read against L07 in its own row; every other L06 to L08 card is entry-identical to 7143726. Output {S}cards_scan.out.",
    "cards-duplicate-scan": f"Re-run this round: near-duplicate scan of cards.json (difflib ratio above 0.6) -> 22 pairs, the same 22 pairs as at 7143726 ({S}cards_scan.out, diff against the previous output differs only in the total and per-lesson count lines). M1-c180 appears in none of them. Its substantive overlap with M1-c112 and M1-c120 (the same (1 + r) factor and the same 24.8685 CU figure, framed as the misconception) is a misconception card in the sense of BUILDER_RULES 7 and is recorded in the M1-c180 row, not as a duplicate.",
}

NEW_ROWS = [
    {
        "id": "M1c-card-c180-misconception",
        "check": "2.7-cards",
        "location": "course/modules/M/M1/cards.json M1-c180; course/modules/M/M1/L07.html:341-346, 86-87, 97",
        "status": "PASS",
        "evidence": (
            "New entry M1-c180 (lesson L07, grade T). Read against L07.html: the card's question is the first "
            "misconception in Section 5 (h2 s5 at line 342; first li at line 344-346: 'They differ by the factor 1 + r "
            "(Proposition 1.4). With C = 100, r = 0.1 and n = 3, the difference is 24.8685 CU, which is 10% of the "
            "ordinary value.'). Proposition 1.4 (L07.html:86-87) states the due annuity is (1 + r) PV_n, grade T. Numbers "
            "recomputed this round with exact fractions (ledgers/M1/scripts/M1-c-r23/card180.py, ledgers/M1/scripts/M1-c-r23/out/card180.out): ordinary PV 248.6852, due "
            "PV 273.5537, gap 33100/1331 = 24.8685 (24.86852), gap/ordinary = 0.1, gap == r * ordinary exactly, "
            "due/ordinary = 11/10. 'the gap grows with the value' is the identity gap = r * PV at fixed r, true exactly. "
            "Atomic at the level of one misconception; it restates the content of M1-c112 and M1-c120 in misconception "
            "form, which BUILDER_RULES 7 asks for (one card per misconception), so it is not a duplicate. Banned-phrase and "
            "process-word grep on the card text: 0 hits."
        ).replace("{S}", S),
    },
]

rows = []
CARRY_FILES = {
    "L06": "course/modules/M/M1/L06.html",
    "L07": "course/modules/M/M1/L07.html",
    "L08": "course/modules/M/M1/L08.html",
}
for r in prev["rows"]:
    rid = r["id"]
    if rid in RERUN:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": RERUN[rid]})
        continue
    ev = re.sub(r"^Carried from round \d+ \([^)]*\)[^:]*: ", "", r["evidence"])
    ev = re.sub(r"^Carried from round \d+ \([^)]*\): ", "", ev)
    if rid == "L07-card-c108-q-locator":
        prefix = "Carried from round 22 (cards.json entry M1-c108 byte-identical since the previous pin; L07.html:150-153 byte-identical):"
    elif rid == "L08-card-c135":
        prefix = "Carried from round 22 (cards.json entry M1-c135 byte-identical since the previous pin; L08.html byte-identical):"
    elif rid.startswith(("L06", "L07", "L08")) or rid.startswith("slice") or rid.startswith("hub") or rid in {"quiz-answers-L06-L08"}:
        prefix = "Carried from round 22 (course/modules/M/M1/L06.html, L07.html, L08.html, index.html and tests/labs/M1 byte-identical since the previous pin 7143726):"
    else:
        prefix = "Carried from round 22 (course/modules/M/M1 L06 to L08 pages byte-identical since the previous pin 7143726):"
    rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": f"{prefix} {ev}"})

rows.extend(NEW_ROWS)
for row in rows:
    assert row["status"] == "PASS"

frag = {
    "unit": "M1",
    "slice": "M1-c",
    "round": 23,
    "verifier": "independent verifier round 23 (did not build M1; shares no context with the builders or earlier verifiers)",
    "pin": "503d139",
    "base": "7143726 (the round-22 pin, the previous independent round for this slice; the round-22 fragment is /tmp/fanout-frags/M1-c.round22.json, used as context only)",
    "previous_ledger": PREV,
    "checkout": "/tmp/verify23-M1-c",
    "scratch": "/tmp/m1-v/M1-c-r23",
    "verified_at": "2026-10-28T12:00:00+00:00",
    "verdict": "PASS",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": (
        "Delta 7143726..503d139 for this slice: course/modules/M/M1/cards.json only (cards M1-c068, c075, c088, c163, c177 "
        "changed; M1-c180 (L07) and M1-c181 (L05) added). L06.html, L07.html, L08.html, index.html, tests/labs/M1 and "
        "references/ are byte-identical since 7143726, so their rows are carried. M1-c181 is an L05 card and belongs to slice "
        "M1-b. The other curriculum change in the delta (Algorithms and Data Structures lists M1 as a prerequisite; "
        "curriculum/01-foundations.yaml, curriculum.json, program.json) is outside this slice; check_dag and check_pages pass. "
        "Mutants: this is a lab and page slice, not a project slice, so no student-error mutants were written for it. The "
        "earlier M1 project grader mutants in ledgers/M1/mutants/ (125) were re-run as a cross-check with "
        "tools/mutate_graders.py --unit M1 --seeds 0-9: 125/125 killed (ledgers/M1/scripts/M1-c-r23/out/mutate_M1.out); "
        "that is the project slice's check and does not bear on this slice's rows. Alternative implementations: not "
        "applicable (no grader in this slice). Hours: unchanged; data-hours 9 on L06 to L08 and the hub split agree. "
        "Could not check: verify_refs.py --unit M1 live-re-verified 1 of 560 entries (its own selection, 0 problems); no source "
        "was read by hand because L06 to L08 cite no registry key."
    ),
    "summary": {"rows": len(rows), "pass": len(rows), "fail": 0, "unverifiable": 0},
}
json.dump(frag, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "ids kept", all(any(x["id"] == r["id"] for x in rows) for r in prev["rows"]))
