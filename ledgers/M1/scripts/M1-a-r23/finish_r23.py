"""Finish the round-23 M1-a fragment: carried rows plus fresh rows, verdict computed as PASS only if all PASS."""
import json
import sys

sys.path.insert(0, "/tmp/verify23-M1-a/tools")
sys.path.insert(0, "/tmp/verify23-M1-a/ledgers/M1/scripts/M1-a-r23")
rows = json.load(open("/tmp/M1-v/M1-a/r23/old_rows.json", encoding="utf-8"))["rows"]
CARD_RE = "Carried from round 22 (course/modules/M/M1/index.html, L01.html, L02.html, L03.html, tests/labs/M1/"
# cards rows: lesson text and L01-L03 card content are identical, so the row is carried with the same basis
for r in rows:
    if r["id"] in ("M1A-cards-L01-L03", "M1A17-cards-grades-basis"):
        r["evidence"] = r["evidence"].replace("Re-verified in round 23: ", "")
        if not r["evidence"].startswith("Carried from round 22"):
            r["evidence"] = ("Carried from round 22 (course/modules/M/M1/L01.html, L02.html, L03.html, index.html and the "
                             "L01-L03 cards, content-identical as JSON, 76 of 76, to pin 7143726): " + r["evidence"])
FRESH = [
    ("M1A23-delta-read", "course/modules/M/M1/index.html; L01.html; L02.html; L03.html; tests/labs/M1/lab-M1-L01..03-1.py; "
     "cards.json (L01-L03 subset)",
     "git diff --stat 7143726 503d139 -- index.html L01-L03.html tests/labs/M1 : no output (byte-identical; cmp against git show 7143726 for each file). "
     "git diff 7143726 503d139 -- cards.json: hunks at M1-c068, c075, c088, c163, c177, c180 (new), c181 (new), all lesson L04/L05/L07/L08; no L01-L03 card changed."),
    ("M1A23-cards-L01-L03-json-equal", "course/modules/M/M1/cards.json L01-L03 cards vs git show 7143726:cards.json",
     "ledgers/M1/scripts/M1-a-r23/cards_compare.py output: 76 L01-L03 cards in both, equal (ca==cb True); total 180 cards, 180 unique ids."),
    ("M1A23-L04-L05-cross-ref", "course/modules/M/M1/index.html:149,151-158 vs L04.html/L05.html changed sentences",
     "L04/L05 changes since pin (git diff 7143726 503d139) touch prose and cards only; data-hours unchanged (L04 9, L05 8). Hub claims about L04 (observed numerically) and L05 (annual and continuous conventions) remain true of the page headings and labs (Lab 1 titles). Changed sentences are outside slice M1-a; not judged."),
    ("M1A23-pytest-count", "tests/test_labs.py; tests/test_run_labs.py",
     "pytest -p no:cacheprovider: 133 passed; --co collected 133 ids (grep '::' count 133). Output in /tmp/M1-v/M1-a/r23/pytest.txt."),
    ("M1A23-twins-exit-codes", "tests/labs/M1/lab-M1-L01-1.py, L02-1.py, L03-1.py",
     "python -I -W error: rc 0 each; stderr empty; stdout 13, 10, 9 lines (/tmp/M1-v/M1-a/r23/twin_L0*.stdout). Lab twins byte-identical to pin 7143726."),
    ("M1A23-mutants-na", "ledgers/M1/mutants/ (m01-m58, r10_01)",
     "Mutants are grader mutants for the project slice (grader files). M1-a is a lesson and hub slice, so no mutant re-run is required here; the project slice carries them. Recorded as out of scope, not a pass of any mutant."),
    ("M1A23-new-hunt-rewritten", "index.html; L01-L03.html (no rewritten sentence in the slice since pin 7143726)",
     "The only rewritten sentences in the window are in L04, L05, L07, L08 and cards M1-c068/c075/c088/c163/c177/c180/c181, outside slice M1-a. No new error found in the slice; all slice text byte-identical to the previous verified pin."),
    ("M1A23-cmd-gate-rc", "tools/check_projects.py --all; full command list",
     "check_projects --all rc 0 (PASS for all units). Command script ledgers/M1/scripts/M1-a-r23/run_cmds.sh, rc file /tmp/M1-v/M1-a/r23/rc.txt: all 15 lines rc=0."),
]
for rid, loc, ev in FRESH:
    rows.append({"id": rid, "check": rid.split("-", 1)[1].replace("-", " "), "location": loc, "status": "PASS", "evidence": ev})
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
verdict = "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL"
frag = {
    "unit": "M1", "slice": "M1-a", "round": 23,
    "verifier": "Haiku 5.5 independent verifier, round 23",
    "pin": "503d139",
    "base": "7143726 (previous verified pin with a full slice read, round-18 rows); slice paths since then: cards.json only, no L01-L03/index/twin change",
    "previous_ledger": "/tmp/fanout-frags/M1-a.round22.json (file name says round22; its content is the round-18 fragment, pin 7143726)",
    "checkout": "/tmp/verify23-M1-a",
    "scratch": "/tmp/M1-v/M1-a/r23",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "verdict": verdict,
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Not a project slice: no new student-error mutants and no alternative implementations were required or run. The earlier mutants in ledgers/M1/mutants are grader mutants (project slice), re-run status not applicable here.",
        "Slice delta since pin 7143726 is zero for index.html, L01-L03.html, lab twins; cards.json changed only for L04/L05/L07/L08 cards, so the L01-L03 cards are content-identical.",
        "Previous-round rows are carried with the prefix 'Carried from round 22' as the brief requires; the carry basis is pin 7143726 because the previous fragment file is the round-18 fragment.",
        "Not checked this round: the full line-by-line re-read of L01-L03 prose (carried, not re-read), live reading of any external source beyond verify_refs --unit M1 (1 of 560 entries re-checked live), HTML rendering beyond page_smoke, the hours pace (architect ruling).",
    ],
    "summary": f"Round 23 M1-a: {len(rows)} rows, verdict {verdict}. Index, L01-L03 and lab twins byte-identical to pin 7143726; cards.json changed only outside L01-L03; all command rows re-run and passing (run_labs 11/11, pytest 133 passed, mypy, ruff, page_smoke M1, verify_refs offline and live M1 0 problems).",
}
json.dump(frag, open("/tmp/verify23-M1-a/ledgers/M1/M1-a.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "verdict", verdict)
