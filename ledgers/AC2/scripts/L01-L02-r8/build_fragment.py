"""Builds ledgers/AC2/L01-L02.json (round 8) from the round-7 fragment: carried rows get the
'Carried from round 7' prefix; re-verified rows get round-8 evidence; one new FAIL row is added."""
import json
import sys

SRC = "/tmp/ac2-frags/L01-L02.round7.json"
OUT = sys.argv[1]
r7 = json.load(open(SRC, encoding="utf-8"))
CARRY = ("Carried from round 7 (course/modules/AC/AC2/L01.html, tests/labs/AC2/lab-AC2-L01-1.py, "
         "atlas/A15.contract.md, references/references.json byte-identical since 6adfd01):")
R8 = "R8 (this round, pin e6788c2): "

# round-8 overrides: id -> (status, evidence, fix-or-None)
OVR = {
    "L01-cross-ref-reference-request": ("PASS", R8 + "L01.html line 66 and line 850 unchanged since 6adfd01 (carried); plans/AC2-open-items.md line 22 (the SEC documentation row) re-read this round, unchanged in the 6adfd01..e6788c2 diff (only line 16 changed). PASS.", None),
    "L02-quiz": ("FAIL", R8 + "quiz re-read lines 822-885. Items q1, q2, q4, q5, q6, q7, q8, q9 keys verified (see L02-quiz-numbers, L02-quiz-q7). Item q3 (line 839) fails: see L02-quiz-q3-option-scope.",
                 "Qualify the correct option of L02q3 at line 839 with 'with equity unchanged' (see L02-quiz-q3-option-scope)."),
    "L02-canon-section5": ("PASS", R8 + "section 5 bullet 1 (line 666) re-read. Added 'with equity unchanged' before 'every liability raises the leverage factor' is correct: A/E = 1 + L/E (year-end identity, same form for averages), so with E fixed a liability increase raises the factor. The following sentence 'Payables and deferred revenue raise it as much as borrowings do' carries no qualifier of its own but sits under the qualified sentence; non-blocking (equal-size liability changes with equity fixed). Contract line 92: leverage = average total_assets / average equity (matches).", None),
    "L02-misconception1-label": ("PASS", R8 + "line 678 now reads 'The factor is average total assets over average equity.' Matches contract line 92. Lab 1 table: net margin, asset turnover and leverage all fall 2021->22, 22->23, 23->24 (run_labs output scripts/L01-L02-r8/twin-L02.stdout lines 3-6), so 'all fall together' holds.", None),
    "L02-misconceptions": ("PASS", R8 + "misconceptions 1-4 (lines 676-691) re-read. 0.1925/0.1820 - 1 = 5.8%; 0.1838 vs 0.1925 (lines 682, 686) match twin output lines 590, 602.", None),
    "L02-c024-card": ("PASS", R8 + "cards.json AC2-c024 (grade T) back text now says 'with equity unchanged, every liability raises the leverage factor', matching canon bullet 1 (line 666). git diff 6adfd01 HEAD on cards.json changes only c024, c072, c107 (no other L01/L02 card changed). scripts/L01-L02-r8/cards_scan.txt.", None),
    "L02-quiz-q3-explain": ("PASS", R8 + "line 842 explanation re-read: 'Section 5: the factor is average total assets over average equity, and total assets equal total liabilities plus equity in each year.' Both statements verified against contract line 92 and the identity.", None),
    "L02-definition-4-1-title": ("PASS", R8 + "line 652 'Definition 4.1 (four ratios)' re-read; names no category. PASS.", None),
    "L02-access-statements": ("PASS", R8 + "L02.html has no access statement. plans/AC2-open-items.md line 10 (SEC: 403 reproduced for both sec.gov pages, scripts/L01-L02-r8/access_check.txt), line 16 (Beneish: DOI https://doi.org/10.2469/faj.v55.n5.2296 -> HTTP 302 to https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, which returned HTTP 403: reproduced, the two recorded URLs), line 24 (Dechow: publications.aaahq.org URL reached via the DOI redirect returned HTTP 403: reproduced). Every statement reproduced with plain curl; no challenge page inspected.", None),
    "L01-L02-access-statements": ("PASS", R8 + "same as L02-access-statements: plans lines 10, 16, 24 reproduced with plain curl (access_check.txt, sec_ua_check.txt).", None),
    "L01-L02-companyfacts-fetch": ("PASS", R8 + "plans line 10 claims data.sec.gov 'serves the JSON to a descriptive, non-personal User-Agent'. Reproduced: curl default UA -> HTTP 403; curl with -A 'AC2-verifier/1.0 (descriptive, non-personal; quant-phd course build)' -> HTTP 200 (scripts/L01-L02-r8/sec_ua_check.txt). The JSON body was not stored. Plain curl with the declared UA is the documented access route, not a challenge bypass.", None),
    "L01-L02-sec-reuse-statement-access": ("PASS", R8 + "index.html line 169 says the reuse statement 'has not been read from the SEC page by automated access'. Reproduced: https://www.sec.gov/os/webmaster-faq -> 403; https://www.sec.gov/os/accessing-edgar-data -> 403 (access_check.txt). Statement matches.", None),
    "L01-L02-data-request-open": ("PASS", R8 + "plans lines 1-10 re-read; line 10 open status unchanged; data_sources.yaml has no SEC entry (grep), so 'Nothing is in tools/data_sources.yaml yet' (index.html line 169) holds.", None),
    "L01-L02-cards-changed": ("PASS", R8 + "cards.json git diff 6adfd01..HEAD touches only c024 (L02), c072 (L05), c107 (L08). L01 cards c014, c026, c031, c120 are byte-identical in the diff and unchanged; L02 c024 re-verified (L02-c024-card).", None),
    "L01-L02-cards-c134-c136": ("PASS", R8 + "cards.json AC2-c134, c135, c136 (L02 Definition 4.1 cards) are not in the 6adfd01..HEAD diff; scripts/L01-L02-r8/cards_scan.txt shows 18 L02 cards and 140 total.", None),
    "L01-L02-cards-duplicates": ("PASS", R8 + "scripts/L01-L02-r8/cards_scan.txt: 140 cards, unique ids, no duplicate fronts or backs; L01 17 cards (c001-c016, c120), L02 18 cards (c017-c031, c134-c136).", None),
    "L01-L02-hub-hours": ("PASS", R8 + "index.html re-read in full (186 lines). Card hours 9+10+8+9+8+10+10+12 = 76 = data-hours-lessons; project 34; 76/110 = 69.1%, 34/110 = 30.9%. The L05 card text changed (line 148) but its 'L05 · 8 h' kicker did not.", None),
    "L01-L02-hub-placement-count": ("PASS", R8 + "index.html lines 68-136 re-read: 9 items (4 AC1, 2 S0, 3 skill checks); mastery bar 80% of 9 = 7.2, so 8 correct; 7/9 = 77.8% ('78%' on line 70) is below the bar. No item tests S2 and the hub says so (line 70). PASS.", None),
    "L01-L02-hub-links": ("PASS", R8 + "index.html line 28-186 re-read; check_pages AC2: PASS (scripts/L01-L02-r8/check_pages.txt); page_smoke AC2 PASS (page_smoke.txt).", None),
    "L01-L02-hub-objectives": ("PASS", R8 + "index.html lines 48-55 re-read; each objective maps to L01-L08 or the project. PASS.", None),
    "L01-L02-hub-honest-pending": ("PASS", R8 + "index.html lines 167-169 ('SIMULATED data only, for now') re-read; L02.html line 613 interpretation labelled SIMULATED. PASS.", None),
    "L01-L02-hub-core-reading": ("PASS", R8 + "index.html lines 172-180 re-read: reading list keys penman2013financial, sloan1996stock, dechow1995detecting, piotroski2000value, beneish1999detection; authored prose names no dechow authors. verify_refs --unit AC2: 7 of 560, 0 problems; --offline 560, 0 problems (verify_refs_live.txt, verify_refs_offline.txt).", None),
    "L01-L02-hub-card-jones": ("PASS", R8 + "index.html line 149 (L06 card) unchanged since 6adfd01; it cites the contract definition by key dechow1995detecting. PASS.", None),
    "L01-L02-hub-ladder-seeds": ("PASS", R8 + "index.html line 161 re-read unchanged. PASS.", None),
    "L01-L02-hub-penman-c": ("PASS", R8 + "index.html line 175 re-read (data-cite penman2013financial, grade C via L02 claims). PASS.", None),
    "L01-L02-check-pages-dag": ("PASS", R8 + "check_pages.py --all: check_pages AC2: PASS; check_dag.py --all: check_dag AC2: PASS (scripts/L01-L02-r8/check_pages.txt, check_dag.txt).", None),
    "L01-L02-pagesmoke": ("PASS", R8 + "page_smoke.py --unit AC2 --pages L01 L02 index --skip-sweep: page_smoke AC2: PASS; lab-AC2-L01-1 and lab-AC2-L02-1 ran (scripts/L01-L02-r8/page_smoke.txt).", None),
    "L01-L02-run-labs": ("PASS", R8 + "run_labs.py --unit AC2 --page L01: PASS (1/1); --page L02: PASS (1/1) (run_labs_L01.txt, run_labs_L02.txt).", None),
    "L01-L02-twins-isolated": ("PASS", R8 + "python -I -W error tests/labs/AC2/lab-AC2-L01-1.py and -L02-1.py, run from a fresh scratch directory: rc 0 both, stderr 0 bytes, L02 stdout 1943 bytes matching the page expected block (run_labs PASS) (twins.sh; twin-L01/L02.stdout, .stderr).", None),
    "L01-L02-ruff-mypy-pytest": ("PASS", R8 + "ruff check and ruff format --check on both twins: PASS; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files'; pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py: 252 passed, rc 0. Not run: pytest collection of course/modules/AC/AC2/grader/test_project.py (a root-level collection error; project slice, not this slice).", None),
    "L01-L02-notation": ("PASS", R8 + "index.html, L02.html re-read; notation as in L01 (round 7). No new notation in the changed lines (666, 678). PASS.", None),
    "L01-L02-run-graders": ("PASS", R8 + "run_graders.py --unit AC2: 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.4 s)' (run_graders_AC2.txt).", None),
    "L01-L02-verify-refs": ("PASS", R8 + "verify_refs --unit AC2: '7 of 560 entries, 0 problems'; verify_refs --offline: '560 entries, 0 problems' (verify_refs_live.txt, verify_refs_offline.txt).", None),
    "L01-banned-about-90": ("PASS", R8 + "grep (this round) over L02.html and index.html for roughly, historically, about [0-9], half, this build, builder, REQUESTS, unit report: no match. The '...' on index.html line 110 is a quiz-stem cloze (BUILDER_RULES, rule d).", None),
    "L01-L02-process-jargon": ("PASS", R8 + "grep of L02.html and index.html for this build, builder, REQUESTS, unit report: no match. PASS.", None),
    "L01-L02-lab-numbering": ("PASS", R8 + "L02.html uses 'Lab 1' (lines 86, 637 ... 882) and 'Lesson 1's lab' (lines 87, 90); no 'Lab 2' or other numbering. PASS.", None),
    "L01-L02-no-contrary": ("PASS", R8 + "L02.html and index.html: no Beneish constant or -1.78 appears (grep). Card AC2-c107 (L08, outside the slice) carries the UNCONFIRMED label. PASS.", None),
    "L02-hours": ("PASS", R8 + "L02.html line 2 data-hours=10 and line 34 '10 study hours' unchanged; index.html card 'L02 · 10 h' (line 145). PASS.", None),
    "L02-canon-misc-scope": ("PASS", R8 + "scope words re-read: line 666 'as much as' (qualified by the preceding 'with equity unchanged'); line 678 'all fall together' (verified against twin output lines 3-6); line 682 and 686 numbers verified; line 730, 780, 794, 82, 850 unchanged. PASS, with the non-blocking note in L02-canon-section5.", None),
}

NEW_ROW = {
    "id": "L02-quiz-q3-option-scope",
    "check": "2.4 quiz key / scope of a claim (architect ruling: scope words)",
    "location": "L02.html line 839 (quiz item L02q3, correct option); cards AC2-c024 and canon line 666 for comparison",
    "status": "FAIL",
    "evidence": R8 + "the correct option reads 'Little on its own: average assets over average equity rises with any liability, including payables'. Unqualified, this is false: with A = L + E in each year, A/E = 1 + L/E, so the factor rises with a liability increase only when equity is unchanged. Witness (scripts/L01-L02-r8/leverage_check.py, leverage_witness.txt): liability 100 -> 110 with equity 100 fixed gives 2.0 -> 2.1; liability 100 -> 110 with equity 100 -> 130 gives 2.0 -> 1.8462 (the factor falls). The canon bullet (line 666) and card AC2-c024 both carry 'with equity unchanged' and this option does not.",
    "fix": "Change the option text at line 839 to: 'Little on its own: with equity unchanged, average assets over average equity rises with any liability, including payables'. No number changes.",
}

rows = []
for r in r7["rows"]:
    rid = r["id"]
    row = {k: r[k] for k in ("id", "check", "location", "status", "evidence")}
    if rid in OVR:
        status, ev, fix = OVR[rid]
        row["status"] = status
        row["evidence"] = ev
        if fix:
            row["fix"] = fix
    elif rid.startswith("L01-") and not rid.startswith("L01-L02-"):
        row["evidence"] = CARRY + " " + r["evidence"]
    else:
        # L02-* and other L01-L02 rows: subject re-read or command re-run this round
        row["evidence"] = R8 + "re-verified this round (L02.html re-read in full, 903 lines). Round-7 evidence: " + r["evidence"]
    rows.append(row)
    if rid == "L02-quiz":
        rows.append(NEW_ROW)

# the quiz FAIL row names its fix
fails = [r for r in rows if r["status"] != "PASS"]
assert all(r.get("fix") for r in fails), "every non-PASS row needs a fix"
out = {
    "unit": "AC2",
    "slice": "L01-L02",
    "round": 8,
    "verifier": "independent round-8 verifier for AC2 slice L01-L02 (fresh context; round-7 fragment read as context only; L02.html read in full; index.html read in full; L01 subject carried by byte-identity)",
    "pin": "e6788c2",
    "base": "6adfd01",
    "checkout": "/tmp/verify-ac2r8-l12",
    "scratch": "/tmp/ac2-v/l12/r8",
    "verified_at": "2026-10-27",
    "verdict": "FAIL" if fails else "PASS",
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Delta 6adfd01..e6788c2 for this slice: L02.html (canon bullet 1 line 666; misconception 1 line 678), cards.json AC2-c024 (L02), index.html (only the L05 card line 148, outside the L01-L02 claims), plans/AC2-open-items.md (line 16, Beneish DOI access). L01.html, the L01 and L02 lab twins, tests/, course/assets, references, tools, atlas are byte-identical since 6adfd01 (git diff --quiet; sha256 in scripts/L01-L02-r8/hashes.txt).",
        "New FAIL: L02-quiz-q3-option-scope (quiz key at L02.html line 839 states the leverage factor rises with any liability without the equity-unchanged condition; witness in leverage_witness.txt). Fix is a one-line wording change; no number changes.",
        "Every access statement reproduced with plain curl and the recorded URLs (scripts/L01-L02-r8/access_check.txt). The SEC data.sec.gov JSON returns 403 to the default curl User-Agent and 200 with a declared descriptive User-Agent, as plans line 10 says; no challenge page was inspected.",
        "Honest gaps unchanged: the Beneish paper, the dechow1995detecting body (publisher page 403), the Penman passage locator, and the SEC reuse statement are not readable by plain curl; they stay labelled UNCONFIRMED or C.",
        "Non-blocking: canon line 666 'Payables and deferred revenue raise it as much as borrowings do' sits under the qualified sentence; builder may repeat 'with equity unchanged' there.",
    ],
    "rows": rows,
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    },
}
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(out["summary"], out["verdict"])
