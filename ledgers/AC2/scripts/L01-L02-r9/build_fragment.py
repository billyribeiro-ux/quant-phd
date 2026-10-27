# Round 9 fragment builder for slice L01-L02: carries round-8 rows whose subject is unchanged,
# replaces rows whose subject was touched or whose command was re-run this round.
import json, sys
R = "/tmp/verify-ac2r9-l12"
prev = json.load(open("/tmp/ac2-frags/L01-L02.round8.json", encoding="utf-8"))
S = "ledgers/AC2/scripts/L01-L02-r9"

CARRY = ("Carried from round 8 (cited subject byte-identical since e6788c2; the only change in the slice since e6788c2 is "
         "course/modules/AC/AC2/L02.html line 839, verified by git diff e6788c2 HEAD): ")

fresh = {
"L02-quiz": ("R9 (pin 792cb31): quiz re-read in full, L02.html lines 820-890 (items q1-q9). q3 (line 839) is the only changed item; "
  "its correct option is re-verified under L02-quiz-q3-option-scope. q2 2.6786 = 750/280 (tol 0.0002); q4 1.0909 = 2(1.2)/2.2 (tol 0.0005); "
  "q6 48 = 120/900*360 (48.67 on 365, as the page says); q9 0.3706 = lab stdout 2024-12-31 gross_margin (scripts/L01-L02-r9/twin-L02.stdout line 13); "
  "q8 'no previous year for 2020-12-31' matches the lab stdout ValueError line; q7 see L02-quiz-Q7; q1 and q5 match Theorem 3.2 and Remark 2.1. PASS."),
"L02-quiz-q3-option-scope": ("R9 (pin 792cb31): line 839 now reads 'Little on its own: with equity unchanged, average assets over average equity rises with any liability, including payables'. "
  "Witnesses scripts/L01-L02-r9/leverage_r9.py (output leverage_r9.txt, run with -I -W error): check 1 asserts avgA/avgE = 1 + avgL/avgE exactly (passes); check 2 equity fixed at 100, payables +40 in year 1: factor 4.0 -> 4.2 (rises); "
  "check 3 borrowing +40 and payables +40 give identical factors; check 4 liability +40 with equity +40 in year 1: 4.0 -> 3.5 (falls), so the equity condition is needed. "
  "The option now carries the condition of canon line 666 and card AC2-c024. Distractors are wrong: 'borrowed more' does not follow, and the margin is unrelated. One data-correct attribute on line 839. PASS."),
"L02-quiz-q3-explain": ("R9 (pin 792cb31): line 842 explanation re-read: 'Section 5: the factor is average total assets over average equity, and total assets equal total liabilities plus equity in each year.' "
  "Consistent with the identity A = L + E per year and with the option. It does not state the equity condition the option now states; non-blocking. PASS."),
"L02-canon-section5": ("R9 (pin 792cb31): canon bullet 1, L02.html line 666, re-read. (a) 'average assets over average equity equals one plus average liabilities over average equity': exact (leverage_r9.py check 1). "
  "(b) 'with equity unchanged, every liability raises the leverage factor': check 2 (4.0 -> 4.2 on a payables increase). "
  "(c) 'Payables and deferred revenue raise it as much as borrowings do': true for equal dollar changes with equity fixed (check 3); the sentence follows the qualified sentence, so the comparison is read as equal amounts. Non-blocking wording note: 'dollar for dollar' would make the scope explicit. "
  "(d) 'The A15 engine's leverage factor is average total assets over average equity by contract': atlas/A15.contract.md line 92 reads 'leverage = average total_assets / average equity'. "
  "(e) 'A rise in the leverage factor therefore does not mean the firm borrowed more': a rise can come from payables or from falling equity; the claim is a non-implication and holds. PASS."),
"L02-c024-card": ("R9 (pin 792cb31): cards.json AC2-c024 (grade T) back text: 'Total assets equal liabilities plus equity in each year, so average assets over average equity equals one plus average liabilities over average equity, and, with equity unchanged, every liability raises the leverage factor, payables and deferred revenue included.' "
  "Matches canon line 666 and quiz line 839 (both carry 'with equity unchanged'). The derivation is the page's identity, so grade T is the proved-on-page rule. cards.json is byte-identical to e6788c2 (git diff --quiet); scripts/L01-L02-r9/cards_scan.txt shows c024 grade T. PASS."),
"L02-canon-misc-scope": ("R9 (pin 792cb31): line 666 'as much as' see L02-canon-section5 (c). Line 678 'all fall together' re-verified against lab stdout (scripts/L01-L02-r9/twin-L02.stdout lines 3-6): net margin 0.1283, 0.1214, 0.1179, 0.0874; asset turnover 0.9142, 0.9133, 0.8701, 0.8511; leverage 1.7896, 1.7363, 1.6936, 1.6628. Each factor falls in every year pair. "
  "Lines 730, 780, 794, 82, 850 are unchanged since e6788c2 and carry the round-8 evidence. PASS."),
"L02-quiz-numbers": ("R9 (pin 792cb31): recomputed in Python: 750/280 = 2.67857 (key 2.6786, tol 0.0002); 2(1+0.2)/(2+0.2) = 1.09091 (key 1.0909, tol 0.0005); 120/900*360 = 48 and *365 = 48.67; lab stdout gross_margin 2024-12-31 = 0.3706. PASS."),
"L02-quiz-Q7": ("R9 (pin 792cb31): key 'Lab 1 uses the no-cut-off table, whose restated revenue differs from the filing that set receivables'. Twin main(): standardize(filer) with no as_of (no cut-off, line 409) and standardize(filer, as_of='2023-06-30') for the original revenue (line 440). "
  "Arithmetic: 43.28 = AR/1145.5*365 gives AR = 135.83; with the originally filed 1131.9, 135.83*365/1131.9 = 43.80 (computed, 43.80002). Matches Example 4.2 and the lab stdout. PASS."),
"L01-L02-sec-reuse-statement-access": ("R9 (pin 792cb31): index.html line 169 says the reuse statement 'has not been read from the SEC page by automated access'. Plain curl, recorded URLs (scripts/L01-L02-r9/access_check.txt, access_check.sh): https://www.sec.gov/os/webmaster-faq -> 403; https://www.sec.gov/os/accessing-edgar-data -> 403. No challenge page inspected, no bypass. Statement matches. PASS."),
"L02-access-statements": ("R9 (pin 792cb31): L02.html has no access statement. plans/AC2-open-items.md line 10 (SEC 403 on both sec.gov pages: reproduced, access_check.txt); line 16 (doi.org/10.2469/faj.v55.n5.2296 -> HTTP 302 to https://www.tandfonline.com/doi/full/10.2469/faj.v55.n5.2296, which returns 403: reproduced); line 24 (doi.org/10.2308/tar-9505096112 -> HTTP 302 to https://publications.aaahq.org/accounting-review/article/70/2/193/18940/Detecting-Earnings-Management, which returns 403: reproduced). "
  "Each status is reproduced with plain curl and a recorded URL. PASS."),
"L01-L02-companyfacts-fetch": ("R9 (pin 792cb31): plans line 10 says data.sec.gov serves the JSON to a descriptive, non-personal User-Agent. Reproduced: https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json with the default curl User-Agent -> 403; with a declared non-personal User-Agent (no contact address, no personal data) -> 200 (access_check.txt last line). Body not stored. PASS."),
"L01-L02-check-pages-dag": ("R9 (pin 792cb31): tools/check_pages.py --all: 'check_pages AC2: PASS' (rc 0); tools/check_dag.py --all: 'check_dag AC2: PASS' (rc 0). Scripts/L01-L02-r9/check_pages.txt, check_dag.txt. PASS."),
"L01-L02-pagesmoke": ("R9 (pin 792cb31): tools/page_smoke.py --unit AC2 --pages L01 L02 index --skip-sweep: 'page_smoke AC2: PASS' (rc 0); lab-AC2-L02-1 0.0 s, runtime boot 1.1 s (scripts/L01-L02-r9/page_smoke.txt). PASS."),
"L01-L02-run-labs": ("R9 (pin 792cb31): tools/run_labs.py --unit AC2 --page L01: 'run_labs AC2: PASS (1/1)' rc 0; --page L02: 'run_labs AC2: PASS (1/1)' rc 0. PASS."),
"L01-L02-twins-isolated": ("R9 (pin 792cb31): python -I -W error tests/labs/AC2/lab-AC2-L01-1.py and -L02-1.py, each from a fresh mkdtemp directory: rc 0 both; stderr 0 bytes both; stdout L01 1661 bytes, L02 1943 bytes (scripts/L01-L02-r9/twin-L0*.stdout, .stderr). PASS."),
"L01-L02-ruff-mypy-pytest": ("R9 (pin 792cb31): ruff check on both twins rc 0; ruff format --check rc 0; mypy --no-incremental on both twins: 'Success: no issues found in 2 source files' (rc 0); pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py: rc 0, 252 passing (72+72+72+36 progress dots; the -q run printed no summary line) (scripts/L01-L02-r9/ruff.txt, mypy.txt, pytest.txt). PASS."),
"L01-L02-verify-refs": ("R9 (pin 792cb31): tools/verify_refs.py --unit AC2: 'live re-verification of AC2: 7 of 560 entries, 0 problems' (rc 0); tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems' (rc 0). PASS."),
"L01-L02-run-graders": ("R9 (pin 792cb31): tools/run_graders.py --unit AC2: 'run_graders AC2: PASS (reference 50/50 seeds, slowest 0.3 s)' (rc 0). PASS."),
"L01-L02-cards-duplicates": ("R9 (pin 792cb31): cards_scan.py on course/modules/AC/AC2/cards.json: 140 cards, unique ids, no duplicate fronts or backs; L01 17 cards (c001-c016, c120), L02 18 cards (c017-c031, c134-c136) (scripts/L01-L02-r9/cards_scan.txt). PASS."),
"L02-banned-phrases": ("R9 (pin 792cb31): grep over L01.html, L02.html, index.html for roughly, historically, typically, usually, generally, about, ellipses and 'most firms': the new line 839 has none. The index.html line 110 ellipsis is a quiz-stem cloze ('the mechanism is called...'), not an omission (BUILDER 1.2 exemption). Other 'about' hits are non-numeric ('a claim about any filer'). PASS."),
}

new_rows = [{
  "id": "L02-line839-change-scope",
  "check": "delta / change scope since e6788c2",
  "location": "course/modules/AC/AC2/L02.html line 839; git diff e6788c2 HEAD (whole repo)",
  "status": "PASS",
  "evidence": "R9 (pin 792cb31): git diff --stat e6788c2 HEAD: 1 file changed, 1 insertion, 1 deletion, in course/modules/AC/AC2/L02.html; the diff hunk is the L02q3 correct option at line 839 only. No other file in the repo changed. Every round-8 row not listed as re-verified in this round is carried by byte-identity of its subject."
}]

rows = []
for r in prev["rows"]:
    rid = r["id"]
    if rid in fresh:
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS", "evidence": fresh[rid]})
    else:
        ev = r["evidence"]
        if r["status"] != "PASS":
            raise SystemExit(f"unexpected non-PASS carry {rid}")
        rows.append({"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                     "evidence": CARRY + ev if not ev.startswith("Carried") else CARRY + ev})
rows.extend(new_rows)
# the two round-8 FAIL rows are re-verified above; L02-quiz and L02-quiz-q3-option-scope are in `fresh`
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicate id"
assert set(prev_id for prev_id in (x["id"] for x in prev["rows"])) <= set(ids), "previous id dropped"
summary = {"rows": len(rows), "pass": sum(r["status"] == "PASS" for r in rows),
           "fail": sum(r["status"] == "FAIL" for r in rows), "unverifiable": sum(r["status"] == "UNVERIFIABLE" for r in rows)}
frag = {
 "unit": "AC2", "slice": "L01-L02", "round": 9,
 "verifier": "independent round-9 verifier for AC2 slice L01-L02 (fresh context; round-8 fragment read as context; delta is one line, L02.html line 839; quiz, canon line 666 and card AC2-c024 re-verified from scratch; all command rows re-run)",
 "pin": "792cb31", "base": "e6788c2", "checkout": R, "scratch": "/tmp/ac2-v/l12/r9", "verified_at": "2026-10-27",
 "verdict": "PASS" if summary["fail"] == 0 and summary["unverifiable"] == 0 else "FAIL",
 "mutants": [], "registry_flags": [], "freshness_flags": [],
 "notes": [
  "Delta e6788c2..792cb31 is one line: L02.html line 839 (L02q3 correct option gains 'with equity unchanged'). Re-verified from scratch: the quiz row L02-quiz (both round-8 FAIL rows now PASS), L02-quiz-q3-option-scope, L02-quiz-q3-explain, canon line 666 (L02-canon-section5, L02-canon-misc-scope), card AC2-c024 (L02-c024-card), quiz numbers and q7.",
  "Round-8 FAIL rows L02-quiz and L02-quiz-q3-option-scope: fixed by the one-line wording change; the new option states the equity condition the canon line and card carry; the witnesses are in scripts/L01-L02-r9/leverage_r9.txt.",
  "Command rows re-run this round: check_pages, check_dag, page_smoke, run_labs L01 and L02, run_graders, verify_refs live and offline, twins alone under python -I -W error in fresh directories, ruff check and format, mypy --no-incremental, pytest subset. All PASS with the outputs archived in scripts/L01-L02-r9/.",
  "Access statements (plans lines 10, 16, 24; index line 169) reproduced with plain curl and recorded URLs (access_check.sh, access_check.txt). The SEC data.sec.gov JSON returns 403 to the default User-Agent and 200 to a declared non-personal User-Agent. No challenge page inspected; no bypass.",
  "Honest gaps unchanged: the Beneish 1999 paper (Beneish constants on Wikipedia only, grade D/UNCONFIRMED per ruling 1), the Dechow 1995 paper body (publisher 403), the Penman passage locator (grade C), and the SEC reuse statement (not readable by automated access) stay labelled as such.",
  "Non-blocking: canon line 666 'as much as' is true for equal dollar changes with equity fixed; 'dollar for dollar' would make the scope explicit. The line 842 explanation does not restate the equity condition; the option does.",
  "Round-number note: the brief header says round=4 in the format sentence; the user instruction says round=9, and this fragment uses round=9."
 ],
 "rows": rows,
 "summary": summary,
}
json.dump(frag, open(f"{R}/ledgers/AC2/L01-L02.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", summary, frag["verdict"])
