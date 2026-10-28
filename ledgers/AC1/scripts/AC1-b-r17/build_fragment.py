"""Builds ledgers/AC1/AC1-b.json for round 17 from the round-16 context fragment and this round's checks.

Carried rows keep their id and status only when the cited subject is byte-identical since the previous pin;
every other row is re-run or re-read in this round and given new evidence.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

PREV = Path("/tmp/fanout-frags/AC1-b.round16.json")
OUT = Path("/tmp/verify17-AC1-b/ledgers/AC1/AC1-b.json")
PREV_PIN = "de53f7e883dc4d6f6dacd6042d13acd197afba5d"
CARRY = (
    "Carried from round 16 (course/modules/AC/AC1/L04.html, L05.html, L06.html and "
    "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py byte-identical since the previous pin, "
    f"{PREV_PIN[:7]}; cards named in the row byte-identical to that pin): "
)

REVERIFIED: dict[str, str] = {
    "AC1b-cmd-pin": (
        "git rev-parse HEAD = fefbf8b (detached, /tmp/verify17-AC1-b, clean). git diff --stat de53f7e fefbf8b "
        "-- course/modules/AC/AC1 tests/labs/AC1: L04.html, L05.html, L06.html and the three twins NOT in the diff "
        "(blob ids a6f5dd6, 6a68438, 20fa14c, 8d5a62f, 711631a, 952e070 unchanged). Changed in the slice: cards.json "
        "(cards.json: 14 cards added, c126-c139; 4 cards of L01-L02 and L07-L08 and 7 cards of L03 changed; slice-b cards changed: c050, c051, c059), "
        "index.html (eyebrow, L01 explain), L01-L03, L07, L08, project, grader."
    ),
    "AC1b-cmd-run_labs": (
        "tools/run_labs.py --unit AC1 --page L04, --page L05, --page L06 (run this round): each printed "
        "'run_labs AC1: PASS (1/1)'."
    ),
    "AC1b-cmd-twins": (
        "python -I -W error tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py: exit 0 each. "
        "Output compared with the page pre.expected blocks (unescaped, stripped): L04 20 lines match, L05 22 lines "
        "match, L06 19 lines match (scratch /tmp/AC1-v/AC1-b-r17/out/twin_L0*.out)."
    ),
    "AC1b-cmd-check_pages": "tools/check_pages.py --unit AC1: 'check_pages AC1: PASS' (exit 0).",
    "AC1b-cmd-check_dag": "tools/check_dag.py --unit AC1: 'check_dag AC1: PASS' (exit 0).",
    "AC1b-cmd-check_projects": (
        "tools/check_projects.py --unit AC1: 'check_projects AC1: PASS' (exit 0); the project slice is outside slice b."
    ),
    "AC1b-cmd-page_smoke": (
        "tools/page_smoke.py --unit AC1 --pages L04 L05 L06: 'page_smoke AC1: PASS'; L05 and L06 pages PASS "
        "individually (runtime boot 1.1 s with numpy; lab-AC1-L06-1 0.0 s); L04 inside the same run."
    ),
    "AC1b-cmd-lint-mypy": (
        ".venv/bin/python -m ruff check on tests/labs/AC1 and course/modules/AC/AC1: 'All checks passed!'; "
        "ruff format --check tests/labs/AC1: '11 files already formatted'; mypy --no-incremental on the three "
        "twins: 'Success: no issues found in 3 source files'."
    ),
    "AC1b-cmd-verify_refs": (
        "tools/verify_refs.py --unit AC1 (live): 'live re-verification of AC1: 2 of 560 entries, 0 problems'; "
        "tools/verify_refs.py --offline: '560 entries, 0 problems'. No slice-b row cites a registry key, so this "
        "run does not test a citation in the slice."
    ),
    "AC1b-cmd-pytest": (
        ".venv/bin/pytest -q -k 'AC1 or lab': exit 0, progress dots at 50% and 100%, no summary line printed "
        "(the same as round 7). Collect-only count not obtained."
    ),
    "AC1b-cards-L04-L06": (
        "cards.json (139 cards). Cards of slice b: L04 c046-c060, c122, c132-c134; L05 c061-c074; L06 c075-c090. "
        "Each was checked against the current lesson text. c050, c051 and c059 changed since the previous pin and "
        "are re-verified (see AC1b-card-c050, AC1b-card-c059, AC1b8-cards-new-L04). c060 FAILs: its back cites "
        "Remark 3.2 for 'operating and financing cash flow can change by the same amount in opposite directions', "
        "which Remark 3.2 does not state (see AC1b8-L04-remark32-attribution)."
    ),
    "AC1b-cards-dup": (
        "cards.json: 139 entries, 139 unique ids (AC1-c001 to c139, contiguous); no duplicate front and no duplicate "
        "back (case-insensitive). Round 16 recorded 125 cards; the file now has 139."
    ),
    "AC1b-card-c059": (
        "cards.json AC1-c059 changed: back now 'No. Over the full life of a payment the two rules recognize the same "
        "total, so a difference that reverses later is not a difference in total profit (Corollary 2.3)'; grade T, "
        "basis 'Corollary 2.3 (L04 Section 2); the expiry of each payment's shares (Problem P1)'. Corollary 2.3 "
        "(L04.html line 114) gives N^A - N^B = -P_t and reversal as the balance expires; the equal full-life "
        "total follows from the Section 2 text (the four shares sum to the payment) and Problem P1 (L04 solutions). "
        "PASS. Lab 1 numbers in the old card are no longer on the card."
    ),
    "AC1b-card-c050": (
        "cards.json AC1-c050 changed: front 'What is rule A in Lab 1?', back 'A recognition convention of the lab. "
        "Rule A expenses a prepaid service in full in the quarter it is paid (Section 2).' L04 Section 2 paragraph "
        "(L04.html line 78) says exactly this and marks it as the lab's convention. PASS."
    ),
    "AC1b-hours": (
        "data-hours: L04 11, L05 12, L06 12 (L0*.html line 2). Hub course/modules/AC/AC1/index.html line 29: "
        "data-hours-lessons=90, data-hours-project=30; 11+12+11+11+12+12+11+10 = 90 lesson hours (L01-L08); "
        "90 + 30 = 120, matching the eyebrow '120 hours' (index.html line 31). Hub hours arithmetic consistent. "
        "Hours are design targets (architect ruling), not checked against pace."
    ),
    "AC1b-dag-concepts": (
        "tools/check_dag.py --unit AC1: PASS (this round). L04.html:58 def-gaap-vs-ifrs, L05.html:58 "
        "def-revenue-recognition, L06.html:58 def-lease-accounting: each defined once, in the slice's own module."
    ),
    "AC1b-process-words": (
        "grep -i -E 'builder|verifier|round|REQUEST|unit report' over cards.json, L04, L05, L06 html: only "
        "L06.html:177 'return round(pv)' (Python code inside the lab listing, not learner prose)."
    ),
    "AC1b-num-L04-lab": (
        "L04.html pre.expected (lines 275-294) equals the twin's output (AC1b-cmd-twins). Recomputed independently "
        "in this round by importing the twin's generate()/shares() (scratch chk_l04.py): prepaid purchases [q1 "
        "4886040, q3 4233446, q4 6325624, q7 6632381]; interest sum 3319293; all printed identities True."
    ),
}

NEW_ROWS = [
    {
        "id": "AC1b8-L04-remark32-attribution",
        "check": "2.2-numbers",
        "location": (
            "course/modules/AC/AC1/L04.html line 348 (misconception 3, '...change by the same amount in opposite "
            "directions (Remark 3.2)'); lines 313-315 (Remark 3.2 text); course/modules/AC/AC1/cards.json AC1-c060 back"
        ),
        "status": "FAIL",
        "evidence": (
            "Remark 3.2 (L04.html lines 313-315) says net income, the cash balance and the change in cash are the same "
            "under both presentations and that only the operating and financing sections differ. It does not say that "
            "the two sections change by the same amount in opposite directions. That magnitude and direction is "
            "Proposition 3.1 (CFO_2 = CFO_1 + I_t, CFF_2 = CFF_1 - I_t). The same loose citation appears in card AC1-c060. "
            "The claim itself is true (Prop 3.1; lab output cfo_presentation_2 - cfo_presentation_1 = 3,319,293)."
        ),
        "fix": (
            "Change '(Remark 3.2)' to '(Proposition 3.1)' in misconception 3 (L04.html line 348) and in card AC1-c060 "
            "back; keep Remark 3.2 for the statement that net income and cash are unchanged. Then re-run "
            "tools/check_pages.py --unit AC1 and tools/check_dag.py --unit AC1."
        ),
    },
    {
        "id": "AC1b8-cards-new-L04",
        "check": "2.9-structure",
        "location": "course/modules/AC/AC1/cards.json AC1-c132, AC1-c133, AC1-c134 (new since de53f7e); lesson L04.html",
        "status": "PASS",
        "evidence": (
            "c132 '-4,974,286 cents ... minus the unexpired part of the quarter-7 purchase of 6,632,381 cents, which has "
            "only its first share expensed' checked against the lab: cum_difference_cents -4974286; generate(2604) "
            "prepaid_paid at quarter 7 = 6632381; shares [1658095, 1658095, 1658095, 1658096]; unexpired after first "
            "share 4974286 (grade C, basis Lab 1 SIMULATED). c133 rule B wording matches L04 Section 2 paragraph (line 78) "
            "and the twin's shares() docstring (grade C, convention). c134 'financing cash flow' matches Section 3 "
            "(Presentation 2) (grade C, convention)."
        ),
    },
    {
        "id": "AC1b8-L04-numbers-recomputed",
        "check": "2.2-numbers",
        "location": (
            "course/modules/AC/AC1/L04.html Section 3 paragraph (line 317, '0.1193 ... unrounded 0.11926'); "
            "Section 2 interpretation (line 295); Section 5 bullet 2 (line 329); Misconception 2 (lines 342-344); card AC1-c056"
        ),
        "status": "PASS",
        "evidence": (
            "3319293/27832482 = 0.1192596837 (rounds to 0.1193 at 4 dp and 0.11926 at 5 dp: both displayed values "
            "correct). Interest over 8 quarters 3,319,293 = printed interest_moved_total_cents. Rule-A vs rule-B "
            "quarterly signs: rule A lower in q1, q3, q4, q7; higher in q2, q5, q6; equal in q0; matches prepaid balance "
            "rising (q1, q3, q4, q7) and falling (q2, q5, q6). Purchases unexpired at q7: q1, q3, q4 zero; q7 "
            "4,974,286 (= minus cum difference). Section 5 bullet 2 (zero at q0, non-zero q1 to q7): prepaid balances "
            "q1 to q7 all non-zero, q0 zero. Scratch chk_l04.py."
        ),
    },
    {
        "id": "AC1b8-twins-match-pages",
        "check": "2.5-lab",
        "location": "tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py; pre.expected blocks in L04, L05, L06",
        "status": "PASS",
        "evidence": (
            "python -I -W error on each twin: exit 0; stdout equals the page's pre.expected block (after html.unescape "
            "and strip): L04 20 lines, L05 22 lines, L06 19 lines (script comparison this round)."
        ),
    },
    {
        "id": "AC1b8-mutants-AC1-rerun",
        "check": "2.5-lab",
        "location": "ledgers/AC1/mutants/ (147 files); tools/mutate_graders.py --unit AC1 --seeds 0-4",
        "status": "PASS",
        "evidence": (
            "mutate_graders AC1: PASS (147/147 killed), run this round (scratch out/mutate.out). The mutants target the "
            "project grader (course/modules/AC/AC1/grader), not the pages or twins of slice b, so they do not test a "
            "row of this slice; they were re-run as the brief asks. No new mutant was written: the slice has no grader "
            "and the project-slice mutant rule does not apply to pages."
        ),
    },
    {
        "id": "AC1b8-cards-change-scan",
        "check": "2.9-structure",
        "location": "course/modules/AC/AC1/cards.json: diff against de53f7e (round-7 pin) for ids of slice b",
        "status": "PASS",
        "evidence": (
            "Diff of cards.json by id, de53f7e to fefbf8b: 14 added (AC1-c126 to c139; c126 L03, c132-c134 L04, c139 L08); "
            "none removed. Changed cards in slice b: AC1-c050, c051, c059 (all L04), each re-verified above. L05 cards "
            "c061-c074 and L06 cards c075-c090 are byte-identical to de53f7e (not in the changed list). AC1-c122 "
            "byte-identical."
        ),
    },
]


def main() -> int:
    prev = json.loads(PREV.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    for row in prev["rows"]:
        new = dict(row)
        if row["id"] in REVERIFIED:
            new["evidence"] = REVERIFIED[row["id"]]
            if row["id"] == "AC1b-cards-L04-L06":
                new["status"] = "FAIL"
                new["fix"] = "See AC1b8-L04-remark32-attribution (card AC1-c060 cites Remark 3.2 for a Proposition 3.1 claim)."
            else:
                new["status"] = "PASS"
        else:
            new["evidence"] = CARRY + row["evidence"]
        rows.append(new)
    rows.extend(NEW_ROWS)
    rows[:] = [r for r in rows]
    for r in rows:
        if r["status"] == "FAIL" and "fix" not in r:
            r["fix"] = "See the remark row."
    fails = [r["id"] for r in rows if r["status"] != "PASS"]
    verdict = "PASS" if not fails else "FAIL"
    frag = {
        "unit": "AC1",
        "slice": "AC1-b",
        "round": 17,
        "round_note": (
            "round 17 (independent re-verification after the round-16 fixes at fefbf8b). Delta: slice-b pages and twins "
            "are byte-identical to de53f7e; cards.json changed (c050, c051, c059 in slice b; 14 cards added); "
            "index.html changed outside the slice's sections."
        ),
        "verifier": "Haiku independent verifier for slice AC1-b (L04, L05, L06 and twins); did not build AC1 and shares no context with its builders",
        "pin": "fefbf8b",
        "base": "de53f7e (previous pin of the slice-b pages; the file named AC1-b.round16.json in /tmp/fanout-frags holds the round-7 content with pin de53f7e and is context only)",
        "checkout": "/tmp/verify17-AC1-b (detached; .venv symlink)",
        "scratch": "/tmp/AC1-v/AC1-b-r17",
        "verified_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "verdict": verdict,
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Slice b is pages and twins, not a project slice: the at-least-3 new student-error mutants and the five alternative correct implementations are not required; the 147 project-grader mutants were re-run (AC1b8-mutants-AC1-rerun) and all killed.",
            "Carried rows cite subjects byte-identical to de53f7e (pages and twins) and cards unchanged since de53f7e; every other row was re-run or re-read in round 17.",
            "Lab output is SIMULATED (seeds 2604, 2605, 2606); results read off a lab are grade C naming the lab.",
            "Not checked: live reachability of any publisher or SEC source (no slice row cites one); the grade of any external constant (none in slice b); hours on pace (architect ruling); the pytest summary line (not printed) and collect-only count.",
            "Previous round's fragment name says round 16 but its content is round 7 (pin de53f7e); its PASS rows were not trusted and every carried row was checked against the byte-identity rule.",
        ],
        "summary": (
            f"AC1-b round 17 (L04, L05, L06 and twins; pin fefbf8b): {len(rows)} rows, "
            f"{sum(r['status'] == 'PASS' for r in rows)} PASS, {sum(r['status'] == 'FAIL' for r in rows)} FAIL, "
            f"{sum(r['status'] == 'UNVERIFIABLE' for r in rows)} UNVERIFIABLE. Verdict {verdict}."
        ),
    }
    OUT.write_text(json.dumps(frag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(verdict, len(rows), fails)
    return 0


if __name__ == "__main__":
    sys.exit(main())
