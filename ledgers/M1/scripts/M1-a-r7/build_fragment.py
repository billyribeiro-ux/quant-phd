"""Build the round-7 M1-a fragment from the round-6 rows (carry rules applied, re-verified rows updated)."""
import json
import re
import sys

PIN_PREV = "d57df1e"
src = json.load(open("/tmp/fanout-frags/M1-a.round6.json", encoding="utf-8"))
out_path = sys.argv[1]

REVERIFIED = {
    "M1A-cmd-check_pages": "Re-run on de53f7e: `.venv/bin/python tools/check_pages.py --unit M1` printed 'check_pages M1: PASS', exit 0 (output in /tmp/M1-v/M1-a/r7/pages.out).",
    "M1A-cmd-check_dag": "Re-run on de53f7e: `tools/check_dag.py --all` exit 0; output includes 'check_dag M1: PASS' (/tmp/M1-v/M1-a/r7/dag.out).",
    "M1A-cmd-run_labs": "Re-run on de53f7e: `tools/run_labs.py --unit M1` printed 'run_labs M1: PASS (11/11)', exit 0.",
    "M1A-cmd-twin-isolated": "Re-run on de53f7e: `.venv/bin/python -I -W error tests/labs/M1/lab-M1-L01-1.py` (and L02, L03): exit 0 each; outputs in /tmp/M1-v/M1-a/r7/twin-01.out, twin-02.out, twin-03.out.",
    "M1A-cmd-page_smoke": "Re-run on de53f7e: `tools/page_smoke.py --unit M1` exit 0, 'page_smoke M1: PASS'; per-lab timings 0.0 s for lab-M1-L01-1, L02-1, L03-1 (/tmp/M1-v/M1-a/r7/smoke.out).",
    "M1A-cmd-ruff-mypy": "Re-run on de53f7e: `.venv/bin/python -m ruff check tests/labs/M1` 'All checks passed!'; `-m ruff format --check tests/labs/M1` '11 files already formatted'; `-m mypy --no-incremental`: 'Success: no issues found in 153 source files'.",
    "M1A-cmd-verify_refs": "Re-run on de53f7e: `tools/verify_refs.py --offline` 'offline integrity: 560 entries, 0 problems'; `tools/verify_refs.py --unit M1` 'live re-verification of M1: 1 of 560 entries, 0 problems'.",
    "M1A-cmd-pytest-labs": "Re-run on de53f7e: `.venv/bin/python -m pytest -q tests/test_labs.py tests/test_run_labs.py` all dots, no F or E in output.",
    "M1A-r6-delta-read": "Delta read for every hunk in the slice: `git diff --stat d57df1e de53f7e` for index.html, L01-L03, tests/labs/M1, references, curriculum: only course/modules/M/M1/index.html changed (2 hunks, lines 63 and 149). The cards file also changed (M1-c009, L01), read in M1A-cards-L01-L03. L01-L03 and tests/labs/M1/* are byte-identical since d57df1e.",
    "M1A-hub-structure": "Re-read index.html:29-65 after the line 63 edit: section order (objectives, prerequisites, placement, lessons, ...) unchanged; the placement section and the lessons section keep their headings.",
    "M1A-hub-no-algebra-claim": "Re-read index.html:63 (now lists the zero-product rule) against L01-L03: no page defines an algebra concept (L02 defines parity and divisibility, coprimality, even/odd; L03 defines the logarithm from the exponential, the lesson's own concept). The zero-product rule is used in L03.html:78 and is not defined anywhere on the pages.",
    "M1A-hub-algebra-list-scope": "index.html:63 now lists 'the rule that a product is zero only when one of its factors is zero (used to cancel a non-zero factor, as in Proposition 1.2 of Lesson 3)'. L03.html:78 (Proposition 1.2): 'u(u - 1) = 0. By A1, u > 0, so u != 0, and therefore u - 1 = 0': this is the cancellation the bullet names. The other cancellations on the pages (division by e^x at L03.html:88, division by t at L03.html:150, division by e^y at L03.html:327, and division by 2 at L02.html:82 and :128) are the division of both sides by a non-zero coefficient, which the list covers as 'fractions' and 'the solution of a linear equation'. Judgment: PASS, because the enumerated list names the zero-product rule explicitly and the other divisions fall under the listed items.",
    "M1A-new-hunt-rewritten-sentences": "Round-7 hunt over the two rewritten sentences of the delta: index.html:63 (zero-product bullet: rule stated correctly as the 'only when' direction; the cited step is written out at L03.html:78) and index.html:149 (hours sentence: 'Lessons 1 and 5 declare 8 hours, the other six declare 9' matches data-hours and the eyebrows L01=8, L05=8, L02/L03/L04/L06/L07/L08=9). The round-6 FAIL (M1A-hub-algebra-list-scope) is resolved by the index.html:63 edit. All other sentences of round 6 are carried.",
    "M1A-lesson-structure-claim": "Re-counted on de53f7e per lesson page L01-L08: class=\"lab\" 1 each; class=\"problem\" 12 each; class=\"item\" 9,10,9,9,9,10,9,10; data-grade present on every page. The four named components (graded claims, runnable labs, problem set with worked solutions, retrieval quiz) are present on all eight pages.",
    "M1A-hours": "Re-read index.html:149 and the hub cards at 151-158 on de53f7e: L01 8 h, L02 9, L03 9, L04 9, L05 8, L06 9, L07 9, L08 9; eyebrows in L01-L08 and data-hours agree. Sum 70; 70 + 30 = 100 matches 'Tier F · 100 hours' (index.html:31) and curriculum/01-foundations.yaml M1 hours: 100. Pace not failed (architect ruling).",
    "M1A-hours-total": "Recomputed on de53f7e: 8+9+9+9+8+9+9+9 = 70; 70 + 30 = 100; index.html:29 (data-hours-lessons=70) and :42 ('70 h lessons · 30 h project (30%)') agree.",
    "M1A-banned": "grep on index.html, L01-L03 on de53f7e for 'roughly half', 'about 6%', 'historically', 'builder', 'verifier', ' round ', 'REQUESTS', 'unit report', 'typically', 'usually', 'generally', and an ellipsis '... ': 0 hits.",
    "M1A-hub-cards-vs-lessons": "Re-read index.html:151-158 (cards, unchanged) against L01-L03 headings: L01 'Sets, Quantifiers and Logical Statements', L02 'Direct Proof and Proof by Contradiction', L03 'Exponential and Logarithm Functions' match the card titles; card text matches each lesson's section list.",
    "M1A-cards-L01-L03": "Re-run on de53f7e: 68 cards with lesson L01 (21), L02 (23), L03 (24); no duplicate ids or fronts. The only changed card since d57df1e is M1-c009 (back now cites 'Theorem 3.2 (a)'): checked against L01.html:92-101, where Theorem 3.2 (a) states the negation of forall x exists y R(x, y) as exists x forall y not R(x, y), and the proof at :101 derives it. Other cards: unchanged, carried.",
    "M1A-r6-cards-added-c147-c151": "cards.json changed only at M1-c009 since d57df1e (checked by `git diff d57df1e de53f7e -- course/modules/M/M1/cards.json`); M1-c147..c151 are byte-identical and were re-read in the card listing: c147 (512 of 512 for both nested identities), c148 (3721 of 3721), c149 (2 coprime solutions), c150 (6 of 6), c151 (36 of 36).",
    "M1A-r6-lab-page-output": "Re-run on de53f7e with ledgers/M1/scripts/M1-a-r7/expected_vs_run.py (python -I -W error): the class=\"expected\" block of L01 (13 lines), L02 (10) and L03 (9) is IDENTICAL to the twin's run output.",
    "M1A-r6-recheck-numbers": "Round-6 recheck script is not in this checkout; recomputed the same numbers with ledgers/M1/scripts/M1-a-r7/recheck_numbers.py (python -I -W error): 2^4=16; 2^9=512; 7^3=343 (brute force on {0,1,2} gives 343); 39 of 39 primes; least failing n=40 with 1681 = 41 x 41; 61^2 = 3721; 500 solutions for p^2=4q^2 (q<=300, |p|<=500); 2 coprime; 300*1001 = 300300; 13^2 = 169; 13.8629 = 20 ln 2 = ln2/0.05; e^0.5 = 1.6487, gain 64.87 percent unrounded; 7/9 = 77.8 percent, 8/9 = 88.9 percent; 70 + 30 = 100.",
    "M1A-hub-reading-list": None,
}

ROUND6_PREFIX = re.compile(r"^Carried from round [56] \((?:[^()]*)\): ")

new_rows = []
for row in src["rows"]:
    rid = row["id"]
    if rid in REVERIFIED and REVERIFIED[rid] is not None:
        row["evidence"] = REVERIFIED[rid]
        row["status"] = "PASS"
    elif rid == "M1A-hub-reading-list":
        pass
    else:
        ev = row["evidence"]
        ev2 = ROUND6_PREFIX.sub("", ev)
        if row["status"] == "PASS":
            row["evidence"] = ("Carried from round 6 (files byte-identical since the previous pin d57df1e): " + ev2)
    new_rows.append(row)

# Re-verified/carry: the reading-list row keeps its carry prefix (index.html:179-185 unchanged).
for row in new_rows:
    if row["id"] == "M1A-hub-reading-list":
        row["evidence"] = "Carried from round 6 (files byte-identical since the previous pin d57df1e): " + ROUND6_PREFIX.sub("", row["evidence"])

rows = new_rows
rows.append({
    "id": "M1A-r7-expected-vs-run",
    "check": "page expected blocks equal the twins' run output (script)",
    "location": "course/modules/M/M1/L01.html:296; L02.html:249; L03.html:251; tests/labs/M1/lab-M1-L0[1-3]-1.py",
    "status": "PASS",
    "evidence": "ledgers/M1/scripts/M1-a-r7/expected_vs_run.py run with python -I: L01 13 lines IDENTICAL, L02 10 IDENTICAL, L03 9 IDENTICAL.",
})
rows.append({
    "id": "M1A-r7-zero-product-step",
    "check": "the zero-product rule added to the hub is used on L03 and is stated in the 'only when' direction",
    "location": "course/modules/M/M1/index.html:63; L03.html:78",
    "status": "PASS",
    "evidence": "L03.html:78: 'u(u - 1) = 0. By A1, u > 0, so u != 0, and therefore u - 1 = 0' uses 'a product is zero only when one factor is zero'. The bullet's words 'the rule that a product is zero only when one of its factors is zero' state that direction (not the converse, which is not needed here).",
})
rows.append({
    "id": "M1A-r7-hub-hours-sentence",
    "check": "hub hours sentence matches each lesson's declared hours",
    "location": "course/modules/M/M1/index.html:149; L01-L08.html line 2 data-hours and line 34-35 eyebrows",
    "status": "PASS",
    "evidence": "'Eight lessons of eight or nine study hours each (Lessons 1 and 5 declare 8 hours, the other six declare 9)': data-hours and eyebrows give 8 for L01 and L05 and 9 for L02, L03, L04, L06, L07, L08. The sentence's 'the hours shown are the ones each lesson page declares' matches the eyebrows.",
})
rows.append({
    "id": "M1A-r7-card-c009",
    "check": "changed card M1-c009 agrees with its lesson",
    "location": "course/modules/M/M1/cards.json M1-c009; L01.html:92-101",
    "status": "PASS",
    "evidence": "Card back: '∃x ∀y ¬R(x, y). Each quantifier flips and the inner predicate is negated (Theorem 3.2 (a)).' Theorem 3.2 (a) on L01.html:92-99 gives the same negation for the predicate R(x, y), and the proof at :101 derives it from Theorem 3.1. The card's basis 'Theorem 3.2 (a)' is the statement the card cites.",
})

rows = [r for r in rows if r["status"]]
fragment = {
    "unit": "M1",
    "slice": "M1-a",
    "round": 7,
    "verifier": "Haiku 5.5 independent verifier, round 7",
    "pin": "de53f7e",
    "base": "d57df1e (round-6 pin; delta d57df1e..de53f7e read for every hunk in the slice: index.html 63 and 149; cards.json M1-c009 (L01); L01-L03 and tests/labs/M1 byte-identical)",
    "previous_ledger": "/tmp/fanout-frags/M1-a.round6.json",
    "checkout": "/tmp/verify7-M1-a",
    "scratch": "/tmp/M1-v/M1-a/r7",
    "verified_at": "2026-10-27T00:00:00+00:00",
    "verdict": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL",
    "rows": rows,
    "mutants": [],
    "registry_flags": [],
    "freshness_flags": [],
    "notes": [
        "Mutants: none. M1-a is a hub and lesson slice, not a project slice; the mutant and alternative-implementation requirements apply to the project slice only.",
        "Round-6 FAIL rows (M1A-new-hunt-rewritten-sentences, M1A-hub-algebra-list-scope) are resolved by the index.html:63 edit and re-verified here.",
        "Division by a non-zero quantity on the pages (L03.html:88, :150, :327; L02.html:82, :128) is judged covered by the listed 'fractions' and 'the solution of a linear equation'. This is a judgment call on list scope, recorded in M1A-hub-algebra-list-scope.",
        "Carried rows are cited with the round-6 prefix; their subjects are byte-identical since d57df1e (checked with git diff --stat d57df1e de53f7e). Rows citing index.html lines 63 and 149 were re-verified, not carried.",
        "Not checked: L04-L08, project.html, the grader and the L04-L08 cards (other slices). Hours: pace not failed (architect ruling). The Velleman book text was not read. No publisher page was opened. page_smoke prints one unit-level PASS line; per-page timing is not shown separately (per-lab timings 0.0 s).",
        "The round-6 recheck script (ledgers/M1/scripts/M1-a-r6) is not in this checkout; the same numbers were recomputed in ledgers/M1/scripts/M1-a-r7/recheck_numbers.py.",
        "The verifier brief's generic prerequisite sentence (AC1, S0, S2) does not match the M1 curriculum entry (prereqs [P0.1]); the page follows the curriculum entry.",
    ],
    "summary": {
        "rows": len(rows),
        "pass": sum(1 for r in rows if r["status"] == "PASS"),
        "fail": sum(1 for r in rows if r["status"] == "FAIL"),
        "unverifiable": sum(1 for r in rows if r["status"] == "UNVERIFIABLE"),
    },
}
json.dump(fragment, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(fragment["verdict"], fragment["summary"])
