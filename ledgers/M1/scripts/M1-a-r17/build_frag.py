"""Build the round-17 M1-a fragment from the round-16 rows (carry or re-verify each id)."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
prev = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
CARRY = "Carried from round 16 (course/modules/M/M1/index.html, L01.html, L02.html, L03.html, tests/labs/M1 byte-identical since the previous pin de53f7e; checked with git diff --quiet): "
CMD = {
    "M1A-cmd-check_pages", "M1A-cmd-check_dag", "M1A-cmd-run_labs", "M1A-cmd-twin-isolated",
    "M1A-cmd-page_smoke", "M1A-cmd-ruff-mypy", "M1A-cmd-verify_refs", "M1A-cmd-pytest-labs",
}
CMD_EVID = {
    "M1A-cmd-check_pages": "Round 17: `.venv/bin/python tools/check_pages.py --unit M1` printed 'check_pages M1: PASS', exit 0 (/tmp/M1-v/M1-a/r17/pages.out).",
    "M1A-cmd-check_dag": "Round 17: `tools/check_dag.py --all` exit 0; 'check_dag M1: PASS' among the unit lines (/tmp/M1-v/M1-a/r17/dag.out).",
    "M1A-cmd-run_labs": "Round 17: `tools/run_labs.py --unit M1` printed 'run_labs M1: PASS (11/11)', exit 0 (/tmp/M1-v/M1-a/r17/labs.out).",
    "M1A-cmd-twin-isolated": "Round 17: `python -I -W error tests/labs/M1/lab-M1-L0[1-3]-1.py` each exit 0 (/tmp/M1-v/M1-a/r17/twin*.out).",
    "M1A-cmd-page_smoke": "Round 17: `tools/page_smoke.py --unit M1 --pages index.html L01.html L02.html L03.html` exit 0, 'page_smoke M1: PASS' (/tmp/M1-v/M1-a/r17/smoke.out). Unit-level line only; per-page timing not shown.",
    "M1A-cmd-ruff-mypy": "Round 17: `ruff check .` exit 0; `ruff format --check .` '212 files already formatted'; `mypy --no-incremental` 'Success: no issues found in 153 source files'.",
    "M1A-cmd-verify_refs": "Round 17: `verify_refs.py --offline` '560 entries, 0 problems'; `verify_refs.py --unit M1` '1 of 560 entries, 0 problems' (exit 0 both).",
    "M1A-cmd-pytest-labs": "Round 17: `pytest -q tests/test_labs.py tests/test_run_labs.py` exit 0 (/tmp/M1-v/M1-a/r17/pytest.out).",
}
CHANGED_CARD_ROW = "M1A-cards-L01-L03"
REVERIFY_R17 = {
    "M1A-hours-total": "Round 17 re-run: lesson data-hours L01-L08 = 8,9,9,9,8,9,9,9 (L01.html:2, L02.html:2, L03.html:2, L04-L08 data-hours); sum 70 equals index.html:29 data-hours-lessons=\"70\" and :149 sentence; 70+30=100.",
    "M1A-r6-recheck-numbers": "Round 17: `ledgers/M1/scripts/M1-a-r7/recheck_numbers.py` re-run, exit 0 (/tmp/M1-v/M1-a/r17/recheck.out); every printed value matches its page sentence.",
    "M1A-r7-expected-vs-run": "Round 17: `ledgers/M1/scripts/M1-a-r7/expected_vs_run.py /tmp/verify17-M1-a` printed L01/L02/L03 IDENTICAL, ALL IDENTICAL.",
}
CARRY_ROWS_CITING_CARDS_UNCHANGED = {"M1A-r6-cards-added-c147-c151", "M1A-r7-card-c009"}
rows = []
for r in prev["rows"]:
    rid = r["id"]
    row = {k: r[k] for k in ("id", "check", "location", "status", "evidence")}
    if rid in CMD:
        row["evidence"] = CMD_EVID[rid]
        row["status"] = "PASS"
    elif rid in REVERIFY_R17:
        row["evidence"] = REVERIFY_R17[rid]
    elif rid == CHANGED_CARD_ROW:
        row["status"] = "FAIL"
        row["fix"] = "Fix M1-c060 (exact equality with a rounded printed value) and delete M1-c175 (duplicate of M1-c063). See M1A17-card-c060 and M1A17-card-c175-dup."
        row["evidence"] = "Round 17 re-verification of all 77 L01-L03 cards against the lesson text (course/modules/M/M1/cards.json vs de53f7e). Two rows fail; see M1A17-card-c060 and M1A17-card-c175-dup. The other changed and new cards agree with their lessons (M1A17-cards-changed-*, M1A17-cards-new)."
    elif rid in CARRY_ROWS_CITING_CARDS_UNCHANGED:
        row["evidence"] = CARRY + r["evidence"]
    else:
        row["evidence"] = CARRY + r["evidence"]
    rows.append(row)
    if rid == "M1A-r6-cards-added-c147-c151" or rid == "M1A-r7-card-c009":
        pass
extra = [
    ("M1A17-delta-read", "git diff --stat de53f7e fefbf8b on the slice paths", "course/modules/M/M1/cards.json; index.html; L01-L03.html; tests/labs/M1", "PASS",
     "`git diff --quiet de53f7e fefbf8b -- course/modules/M/M1/index.html course/modules/M/M1/L01.html course/modules/M/M1/L02.html course/modules/M/M1/L03.html tests/labs/M1` prints IDENTICAL. The only changed slice file is cards.json (234 lines changed in the cards file overall, of which L01-L03 entries are listed in M1A17-cards-changed-* and M1A17-cards-new); every hunk of its L01-L03 part was read in `git diff de53f7e fefbf8b -- course/modules/M/M1/cards.json`."),
    ("M1A17-cards-changed-L01", "changed cards M1-c002, M1-c008, M1-c017 against L01.html", "course/modules/M/M1/cards.json; L01.html:50-125, 375-388", "PASS",
     "M1-c002 back = 'A set of objects that a variable may take values in.' = Definition 1.1 (L01.html text). M1-c008 = 'the negation of ∀x∈D P(x) is ∃x∈D ¬P(x) (Theorem 3.1)'. M1-c017 back: 'n = 40 ... first failure ... nothing about n = 41 or later' matches Lab 1 output line 'least n in 1 to 50 ... : 40' (/tmp/M1-v/M1-a/r17/labs.out) and L01 lab prose 'the 39 primes say nothing about n = 41'; grade C with basis Lab 1."),
    ("M1A17-cards-changed-L02", "changed cards M1-c024, M1-c025, M1-c029, M1-c030, M1-c038 against L02.html", "course/modules/M/M1/cards.json; L02.html:24-53 (Definitions 1.2-1.3, Fact 1.4, Theorem 1.5, Lemma 2.2, Theorem 2.5)", "PASS",
     "M1-c024 = Definition 1.3 (n = dk). M1-c025 = Fact 1.4, stated as given, not proved (L02.html text 'the unit takes it as given. It is not proved here'). M1-c029 = Theorem 1.5 a+b = 2(m+n). M1-c030 = Lemma 2.2. M1-c038 = Theorem 1.5 starts from arbitrary integers; the removed sentence on counterexamples is covered by M1-c039/c040 and is not a claim the card now lacks."),
    ("M1A17-cards-changed-L03", "changed cards M1-c049, M1-c052, M1-c062 against L03.html", "course/modules/M/M1/cards.json; L03.html Propositions 1.4, 1.6, 1.7 and 2.1", "PASS",
     "M1-c049 = Proposition 1.4 ln(e^x)=x. M1-c052 = Proposition 1.6(a) ln 1 = 0. M1-c062 = Proposition 1.7 factor at 2r is the square of factor at r; the doubling-time consequence moved to M1-c162 which agrees with Proposition 2.1 (L03.html Misconceptions)."),
    ("M1A17-cards-new", "new cards M1-c159, c161, c162, c170, c171, c172, c173, c174 against the lesson text", "course/modules/M/M1/cards.json; L01.html Theorem 3.2(b), Definition 1.1, Theorem 3.1; L02.html Fact 1.4, Theorem 1.5, Lemma 2.2; L03.html Propositions 1.4, 2.1", "PASS",
     "M1-c159 = Theorem 3.2(b) ¬∃x∀y R = ∀x∃y ¬R. M1-c161 = 'no truth value until its domain is stated' (Definition 1.1). M1-c162 = (ln 2)/(2r) half of (ln 2)/r (Prop 2.1). M1-c170 = Theorem 3.1 second identity. M1-c171 = Fact 1.4 is taken as given, not proved. M1-c172 = Theorem 1.5 ab = 4mn. M1-c173 = Lemma 2.2. M1-c174 = Proposition 1.4 e^(ln y)=y. Each answer is in its cited lesson text; no new number is introduced."),
    ("M1A17-card-c060", "M1-c060 back: '13.8629 years, which equals (ln 2)/0.05 = 20 ln 2'", "course/modules/M/M1/cards.json M1-c060; L03.html Lab 1 output line 'doubling time log(2)/rate = 13.8629 years' and E2 (:L03.html Problem E2)", "FAIL",
     "Recomputed: ln(2)/0.05 = 13.862943611..., so 13.8629 is that value rounded to four decimals (ledgers/M1/scripts/M1-a-r7/recheck_numbers.py: '13.8629  20 ln2 = 13.8629'). The back states exact equality ('which equals ... = 20 ln 2') for a rounded printed value and the front does not state the rounding. The lesson itself says 'to four decimals' (E2). The card overstates the exactness of the printed value."),
    ("M1A17-card-c056", "M1-c056 back: '1.6487, which is e^0.5'", "course/modules/M/M1/cards.json M1-c056; L03.html Example 2.3", "PASS",
     "Front says 'to four decimals', so the 1.6487 is the four-decimal form of e^0.5 = 1.6487212707 (recomputed in recheck_numbers.py: 'e^0.5 = 1.6487'). The basis is stated in the question; no overclaim."),
    ("M1A17-card-c175-dup", "M1-c175 'For y > 0, what is ln(1/y)?' vs M1-c063", "course/modules/M/M1/cards.json M1-c175, M1-c063; L03.html Proposition 1.6(c)", "FAIL",
     "M1-c175 asks the same fact with the same answer and citation as M1-c063 ('ln(1/y) = −ln y (Proposition 1.6(c))'). The deck tests one fact twice. Full duplicate scan: ledgers/M1/scripts/M1-a-r17/card_delta.py output at /tmp/M1-v/M1-a/r17/card_delta.out. No other pair of L01-L03 cards has the same answer; M1-c025/M1-c171 ask whether the fact is true versus whether the unit proves it and are kept."),
    ("M1A17-card-c171-c025", "M1-c171 vs M1-c025 (both about parity of integers)", "course/modules/M/M1/cards.json", "PASS",
     "Different questions: M1-c025 asks whether every integer is even or odd (Yes, Fact 1.4); M1-c171 asks whether the unit proves it (No, taken as given). Both answers appear in L02.html Fact 1.4 text. Not a duplicate."),
    ("M1A17-cards-grades-basis", "every L01-L03 card graded C names its basis; T cards are proved on the page", "course/modules/M/M1/cards.json L01-L03", "PASS",
     "Cards graded C: M1-c016, c017, c034, c035, c036, c041, c056, c058, c059, c060, c147, c148, c149, c150, c151; each has a basis naming Lab 1 (run output /tmp/M1-v/M1-a/r17/labs.out and twin outputs). Cards graded T cite a proposition, theorem, lemma, definition or example on the page (checked in the card-by-card read)."),
    ("M1A17-lessons-unchanged", "L01-L03 and index.html byte-identical since de53f7e", "course/modules/M/M1/L01.html, L02.html, L03.html, index.html; tests/labs/M1", "PASS",
     "git diff --quiet de53f7e fefbf8b on these paths exits 0. Carried rows cite their lines unchanged."),
    ("M1A17-hub-lessons-hours", "hub split and lesson hours arithmetic (not pace)", "course/modules/M/M1/index.html:29,149,151-158; L01-L08 data-hours", "PASS",
     "Lesson hours 8+9+9+9+8+9+9+9 = 70 equals the hub lesson hours 70 (index.html:29) and the declared 70 h lessons (index.html eyebrow). Hub sentence 'Lessons 1 and 5 declare 8 hours, the other six declare 9' matches the data-hours list. Pace not judged (architect ruling)."),
    ("M1A17-mutants-na", "student-error mutants and alternative implementations", "ledgers/M1/mutants/ (project slice)", "PASS",
     "Not applicable: M1-a is a hub and lesson slice; the mutant and alternative-implementation requirements apply to the project slice (brief section (g) and the round-16 notes). The lab twins were run isolated under -I -W error (M1A-cmd-twin-isolated) and their printed output matches every page expected block (M1A-r7-expected-vs-run, re-run)."),
]
for rid, check, loc, status, ev in extra:
    row = {"id": rid, "check": check, "location": loc, "status": status, "evidence": ev}
    if status != "PASS":
        row["fix"] = "M1-c060: '13.8629 years, which equals (ln 2)/0.05 = 20 ln 2' -> '13.8629 years (to four decimals), the value of (ln 2)/0.05 = 20 ln 2'. M1-c175: delete (duplicate of M1-c063)." if rid == "M1A17-card-c060" or rid == "M1A17-card-c175-dup" else "see evidence"
    rows.append(row)
out = {
    "unit": "M1",
    "slice": "M1-a",
    "round": 17,
    "verifier": "Haiku 5.5 independent verifier, round 17",
    "pin": "fefbf8b",
    "base": "de53f7e (previous pin; delta de53f7e..fefbf8b on the slice paths: cards.json only; index.html, L01-L03 and tests/labs/M1 byte-identical)",
    "previous_ledger": "/tmp/fanout-frags/M1-a.round16.json",
    "checkout": "/tmp/verify17-M1-a",
    "scratch": "/tmp/M1-v/M1-a/r17",
    "verified_at": "2026-10-28T00:00:00+00:00",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: not required, M1-a is not a project slice (the round-16 notes say the same). No alternative implementations were run for the same reason.",
        "Round-16 rows whose subject changed (cards.json L01-L03 entries) were re-verified; rows whose subject is byte-identical are carried with the round-16 prefix.",
        "The file named round16 carries pin de53f7e in its own text; this round treats de53f7e as the previous pin.",
        "Not checked: L04-L08 lesson text and cards (other slices), project.html and the grader (other slices), the Velleman source (not read; no publisher page opened), the hours pace (architect ruling).",
    ],
    "summary": "Round 17 M1-a: two FAIL rows on cards (M1-c060 exact equality with a rounded printed value; M1-c175 duplicate of M1-c063). Hub and lesson pages and lab twins byte-identical to the previous pin; all commands re-run and passing.",
}
Path(sys.argv[3]).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(rows), "rows")
