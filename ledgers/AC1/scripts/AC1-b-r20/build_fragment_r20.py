"""Build ledgers/AC1/AC1-b.json for round 20 (slice AC1-b, pin fd9a9b7).

Reads the round-19 fragment as context only. Rows whose cited subject is on a line changed since
51fa336 are re-verified (new evidence, see RE/NEW). Other rows are carried with the prefix required
by the brief, and only when the cited subject is not on a changed line.
"""

import json
import sys

PREV = "/tmp/fanout-frags/AC1-b.round19.json"
OUT = "/tmp/verify20-AC1-b/ledgers/AC1/AC1-b.json"
CARRY = (
    "Carried from round 19 (course/modules/AC/AC1/cards.json byte-identical since 51fa336; "
    "L04.html changed only at lines 52 and 134, L05.html only at lines 52, 121, 333, 387 and 401, "
    "L06.html only at line 296, tests/labs/AC1/lab-AC1-L04-1.py only at line 4; the cited subject is not on a changed line): "
)
TWIN_OUT = "scripts/AC1-b-r20/out/"

RE = {
    "AC1b-cmd-pin": ("PASS", "git rev-parse --short HEAD in /tmp/verify20-AC1-b = fd9a9b7 (detached; out/pin.txt). Delta read with git diff 51fa336 fd9a9b7: 14 files in slice b (L04.html, L05.html, L06.html, lab-AC1-L04-1.py) plus the AC1-d, AC1-c, M1 and CF1 files, which are other slices."),
    "AC1b-cmd-run_labs": ("PASS", "tools/run_labs.py --unit AC1 --page L04, L05, L06: each prints 'run_labs AC1: PASS (1/1)' with rc=0 (out/run_labs_L04.txt, L05, L06)."),
    "AC1b-cmd-twins": ("PASS", "python -I -W error on tests/labs/AC1/lab-AC1-L04-1.py, lab-AC1-L05-1.py, lab-AC1-L06-1.py: rc=0 for all three (out/twin_L0*.txt). out/embed_cmp.txt: page code block equals twin file for L04, L05, L06 (True). out/expcmp.txt: pre.expected equals twin stdout (True; 20, 22 and 19 lines)."),
    "AC1b-cmd-check_pages": ("PASS", "tools/check_pages.py --unit AC1: 'check_pages AC1: PASS', rc=0 (out/check_pages.txt)."),
    "AC1b-cmd-check_dag": ("PASS", "tools/check_dag.py --unit AC1: 'check_dag AC1: PASS', rc=0 (out/check_dag.txt)."),
    "AC1b-cmd-check_projects": ("PASS", "tools/check_projects.py --unit AC1: 'check_projects AC1: PASS', rc=0 (out/check_projects.txt)."),
    "AC1b-cmd-page_smoke": ("PASS", "tools/page_smoke.py --unit AC1 --pages L04 L05 L06: each page PASS and 'page_smoke AC1: PASS', rc=0 (out/page_smoke.txt). Timings were not at issue; no re-run was needed."),
    "AC1b-cmd-lint-mypy": ("PASS", "ruff check tests/labs/AC1: 'All checks passed!'; ruff format --check: '11 files already formatted'; mypy --no-incremental on the three twins: 'Success: no issues found in 3 source files' (out/ruff_check.txt, ruff_format.txt, mypy.txt)."),
    "AC1b-cmd-verify_refs": ("PASS", "tools/verify_refs.py --offline: 'offline integrity: 560 entries, 0 problems'; tools/verify_refs.py --unit AC1 (live): 'live re-verification of AC1: 2 of 560 entries, 0 problems' (out/verify_refs_offline.txt, verify_refs_live.txt). The live check reached the registry's endpoints; no publisher page was read by this slice."),
    "AC1b-cmd-pytest": ("PASS", "pytest -q -k 'AC1 or lab' -p no:cacheprovider: exit 0; 143 progress dots, no F or E (out/pytest.txt). The configuration printed no summary line, so the count is the number of dots, not a collect-only count."),
    "AC1b-num-L04-lab": ("PASS", "L04 pre.expected equals the twin's stdout line for line (20 lines; out/expcmp.txt L04 True). Twin printed under python -I -W error with rc=0 (out/twin_L04.txt)."),
    "AC1b-num-L05-lab": ("PASS", "L05 pre.expected equals the twin's stdout (22 lines; out/expcmp.txt L05 True); twin rc=0 (out/twin_L05.txt)."),
    "AC1b-num-L06-lab": ("PASS", "L06 pre.expected equals the twin's stdout (19 lines; out/expcmp.txt L06 True); twin rc=0 (out/twin_L06.txt)."),
    "AC1b8-twins-match-pages": ("PASS", "Twin code equals the page's embedded data-run block for L04, L05, L06 (out/embed_cmp.txt, True x3); pre.expected equals twin stdout (out/expcmp.txt, True x3)."),
    "AC1b-num-L05-prose": ("PASS", "L05 interpretation (line 333) recomputed by python from the displayed integers: 5,434,051/12 floor 452,837, remainder 452,844; 35,732,298/12 floor 2,977,691, remainder 2,977,697; 6*452,837 + 6*2,977,691 = 20,583,168 (= month-6 difference, twin output); 50,471,362/80,495,111 = 0.62701 (0.6270); 23,333,398/80,495,111 = 0.28987 (0.2899); shares 0.0675+0.1173+0.3713+0.4439 = 1.0000. Every figure matches twin_L05 output. Misconceptions and section 4 bullets are on unchanged lines (carried)."),
    "AC1b-num-L06-prose": ("PASS", "L06 interpretation (line 296) recomputed: 6.30% of 71,992,763 = 4,535,544.069, printed 4,535,544; 14,820,224 - 13,034,272 = 1,785,952; 11,057,175 - 13,034,273 = -1,977,098; sum of payments 91,239,905; final payment 13,034,273, adjustment 1. All match twin_L06 output. Remark 2.5 (line 120) is unchanged."),
    "AC1b4-L04-why-scope": ("PASS", "L04 line 52 (changed, new text): 'one SIMULATED set of 36 ledger entries over eight quarters' matches twin_L04 output (ledger_entries 36, quarters 8). The scope sentence 'the lesson does not state what US GAAP or IFRS Standards require, because this lesson cites neither primary text' matches the page's own text: L04 line 63 ('states no rule of either framework') and References block (L04 lines 560-562: 'No source is cited on this page, and the page states no claim that depends on the text of a standard')."),
    "AC1b-data-simulated": ("PASS", "SIMULATED is present on L04 line 52 (why-it-matters), 129 (lab h3), 133 (twin docstring embedded), 324 (honest-pending: 'No real company appears in this lesson'); L05 lines 52, 127, 131, 340 (honest-pending: 'No real contract appears'); L06 lines 52, 124, 126, 303 (honest-pending). Current locators observed by grep -n on the pages."),
    "AC1b3-L05-top-line": ("PASS", "L05 line 52 'Revenue is the first item that L02 lists for the income statement (revenue, the costs that match it, and net income)' matches L02.html line 64 ('reports flows over a fiscal year: revenue, the costs that match it, and net income'); revenue is the first listed item."),
    "AC1b4-L05-interp-remainders": ("PASS", "L05 interpretation (line 333) remainder and floor figures recomputed (see AC1b-num-L05-prose): 452,837 and 452,844; 2,977,691 and 2,977,697; sums to 20,583,168 printed by twin_L05."),
    "AC1b6-locators-L05": ("PASS", "L05 lines verified by sed -n: 52 why-it-matters; 68 Definition 1.3 body; 72 Proposition 1.4 title; 96 Proposition 2.1 statement; 124 paragraph 'Convention 1 and convention 2 agree at month 12'; 128 lab hypothesis; 333 interpretation (changed, checked above)."),
    "AC1b-L05-remark24-bullet": ("PASS", "L05 section 4 bullet 3 (lines 345-348) says 'Remark 2.4 shows that the balance can be large in between. Lab 1 shows both a liability and an asset under two billing ...'. Remark 2.4 (line 121, changed) still says the balance 'can be large in between'; twin_L05 prints max_contract_liability 32,792,272 and max_contract_asset 23,333,398 (both billing scenarios). The bullet's 'can be large' claim is supported."),
    "AC1b-scope-words": ("PASS", "Changed lines re-read for scope words (only, all, always, as much as, same, drives, offsets, raises). L04 line 52 'same transactions' and 'the same quarter' are witnessed by twin_L04 quarter q1 (ni_rule_a -52,491 vs ni_rule_b 3,612,039). L05 line 121 adds the condition 'When total billing equals the price' (a condition, not a scope claim). L05 line 333 and L06 line 296 add no scope words. Carried lines 58, 330, 341, 473 (L04), 87, 345, 488 (L05), 308, 432 (L06) are unchanged."),
    "AC1b8-mutants-AC1-rerun": ("PASS", "ledgers/AC1/mutants now holds 179 files (ls | wc -l). git diff --name-only 51fa336 fd9a9b7 -- ledgers/AC1/mutants lists 14 added files (fix19d01-d10, v19_m01-m04), so the earlier count of 160 plus 5 v18 files is now 165 plus 14. Slice b has no project grader (course/modules/AC/AC1/grader/ is not in this slice), so the mutants are not scored here; they belong to the project slice. Recorded as scope, not as a mutant run."),
    "AC1b7-process-words": ("PASS", "grep -inE 'builder|build|round|verifier|verified|REQUESTS|unit report' over course/modules/AC/AC1/L04.html, L05.html, L06.html: the only match is 'round(pv)' inside L06 twin code (L06.html line 177), which is a Python call, not learner prose."),
    "AC1b-card-c069": ("FAIL", "cards.json AC1-c069 back reads 'The convention-1 revenue from the over-time obligations through month m (Remark 2.4 in Section 2; problem P3).' Remark 2.4 (L05 line 120-121) is 'a timing wedge' about the balance and says nothing about the two conventions. The sentence it should support is the paragraph at L05 line 124 ('Convention 1 and convention 2 agree at month 12 ... the difference at any month m < 12 equals the convention-1 revenue ... from the over-time obligations'), which follows Remark 2.4. cards.json is byte-identical to 51fa336 (git diff quiet), so the locator is the same defect the round-19 verifier reported."),
    "AC1b-cards-L04-L06": ("FAIL", "Every slice-b card re-read against its lesson text. The other cards match (AC1-c046, c052, c053, c058, c066, c140 re-read and carried). AC1-c069 still cites Remark 2.4 for a sentence that is not in it (AC1b-card-c069), so the card set does not pass."),
}

NEW = [
    ("AC1b20-L04-why-same-quarter", "PASS", "L04 line 52 'can report different net income in the same quarter, as Lab 1 shows': twin_L04 output quarter q1 gives ni_rule_a -52,491 and ni_rule_b 3,612,039 (out/twin_L04.txt). Witness exists in the printed output."),
    ("AC1b20-L04-docstring-no-ratio", "PASS", "Twin docstring line 4 and page code line 134: 'The lab prints no ratio.' twin_L04 stdout (out/twin_L04.txt, 20 lines) contains only integers and True/False, no ratio or fraction. The ratio 0.1193 at L04 line 435 is a hand computation (3,319,293/27,832,482 = 0.119260, unrounded 0.11926 to five decimals) in a solution, not a printed lab value; the docstring claim is about the lab."),
    ("AC1b20-L05-why-def13", "PASS", "L05 line 52 'a transaction price (Definition 1.3)': Definition 1.3 at L05 line 68 sets the transaction price as the integer P in cents. Pointer correct."),
    ("AC1b20-L05-remark24-condition", "PASS", "L05 line 121 'When total billing equals the price, it is zero at the end of the contract under Proposition 2.3': Proposition 2.3 (line 110 block) says 'If total billing equals P and total revenue equals P, then D12 = 0'. The added condition is exactly the proposition's hypothesis; the claim is correctly conditional."),
    ("AC1b20-L05-interp-identities", "PASS", "L05 line 333 'The balance identity and the month-6 identity are true by the construction of the lab': twin_L05 code computes balance = billed_cum - recognized_cum, so balance_identity True is true by definition; month_6_difference_equals_over_time_revenue compares revenue_cum[5]-revenue_2_cum[5] with the first six monthly shares of the over-time obligations, and revenue_2 moves those amounts to month 12, so the check holds by construction. Both prints are True (out/twin_L05.txt). The sentence states what the code does, and it does not claim an economic test."),
    ("AC1b20-L05-M2-solution", "PASS", "L05 line 387 (M2 solution): obligation A = 60,000 in month 3; obligation B = 24,000/12 = 2,000 per month 1..12. Month 3 = 62,000; month 6 = 2,000 (B only, A is a point obligation in month 3); cumulative through month 6 = 60,000 + 6*2,000 = 72,000. Recomputed; all match."),
    ("AC1b20-L05-M4-solution", "PASS", "L05 line 401 (M4 solution, 'as Remark 1.5 states'): weights 10, 20, 30 with W = 60 and P = 100,000 (M1 weights 1, 2, 3 per M1 at line 378). Floors 16,666, 33,333, 50,000; remainders 40, 20, 0 (1,000,000 - 60*16,666; 2,000,000 - 60*33,333); L = 1 goes to the largest remainder, obligation 1: 16,667, 33,333, 50,000 (python recomputed). Remark 1.5 (L05 line 87) says scaling 'leaves it unchanged', so 'states' is the right verb."),
    ("AC1b20-L06-interp-articulation", "PASS", "L06 line 296 'That check follows from how the schedule is built, so it tests the code and not the economics': twin_L06 code sets rou_closing = rou - amort and closing = liability + interest - payment, so (rou - liability) change = payment - expense_F identically; articulation_every_year True is therefore true by construction (out/twin_L06.txt). Statement correct."),
    ("AC1b20-L04-embedded-twin", "PASS", "The changed twin docstring (lab-AC1-L04-1.py line 4) is the same text as the page code block at L04 line 134 (out/embed_cmp.txt L04 True)."),
]

def main() -> int:
    prev = json.load(open(PREV, encoding="utf-8"))
    rows = []
    seen = set()
    for r in prev["rows"]:
        rid = r["id"]
        if rid in seen:
            continue  # round-19 fragment listed two ids twice; each id appears once here
        seen.add(rid)
        if rid in RE:
            status, ev = RE[rid]
            row = {"id": rid, "check": r["check"], "location": r["location"], "status": status, "evidence": ev}
        elif r["status"] == "PASS":
            row = {"id": rid, "check": r["check"], "location": r["location"], "status": "PASS",
                   "evidence": CARRY + r["evidence"]}
        else:
            raise SystemExit(f"unhandled previous non-PASS row {rid}")
        if status_of(row) != "PASS" and "fix" not in row:
            row["fix"] = FIXES[rid]
        rows.append(row)
    for rid, status, ev in NEW:
        rows.append({"id": rid, "check": "2.2-numbers" if "numbers" in ev or "M2" in rid else "2.5-lab",
                     "location": "see evidence", "status": status, "evidence": ev})
    return rows

def status_of(row):
    return row["status"]

FIXES = {
    "AC1b-card-c069": "Re-point AC1-c069 to the paragraph after Remark 2.4 in Section 2 (L05 line 124, 'Convention 1 and convention 2 agree at month 12 ...'), or drop the Remark 2.4 locator, then re-run tools/check_pages.py --unit AC1.",
    "AC1b-cards-L04-L06": "Fix AC1-c069 as in AC1b-card-c069; re-run tools/check_pages.py --unit AC1 and re-verify the card set.",
}

if __name__ == "__main__":
    rows = main()
    frag = {
        "unit": "AC1",
        "slice": "AC1-b",
        "round": 20,
        "round_note": "round 20: delta since the round-19 pin 51fa336 is the L04.html docstring and why-it-matters (lines 52, 134), L05.html why-it-matters, Remark 2.4, interpretation and M2/M4 solutions (lines 52, 121, 333, 387, 401), L06.html interpretation (line 296), and tests/labs/AC1/lab-AC1-L04-1.py line 4. cards.json unchanged.",
        "verifier": "Haiku independent verifier for slice AC1-b, round 20; did not build AC1 and shares no context with its builders",
        "pin": "fd9a9b7",
        "base": "51fa336 (round-19 pin; /tmp/fanout-frags/AC1-b.round19.json is context only, its PASS rows were re-verified or carried with the changed-line condition)",
        "checkout": "/tmp/verify20-AC1-b (detached at fd9a9b7; .venv symlink)",
        "scratch": "/tmp/v20b_out",
        "verified_at": "2026-10-28T12:00:00+00:00",
        "verdict": None,
        "rows": rows,
        "mutants": [],
        "registry_flags": [],
        "freshness_flags": [],
        "notes": [
            "Slice b is pages and twins, not a project slice: no project grader is in scope, so no student-error mutant is required and none is run. ledgers/AC1/mutants now holds 179 files; the 14 files added since 51fa336 belong to project slices (fix19d01-d10, v19_m01-m04) and are not run by this slice.",
            "Round-19 fragment listed AC1b-data-simulated and AC1b4-L06-misc3-residual twice; this fragment lists each id once.",
            "Lab output is SIMULATED (seeds 2604, 2605, 2606); every result read off a lab is grade C naming the lab. Results proved on the page are T.",
            "Not checked: live reachability of any publisher or SEC source (no slice-b row cites one); the pytest collect-only count (the configuration printed no summary); hours on pace (architect ruling, not failed); the card rows carried unchanged from round 19 were not re-read line by line this round, because cards.json and the cited subject lines are byte-identical since 51fa336.",
        ],
        "summary": "",
    }
    passed = sum(1 for r in rows if r["status"] == "PASS")
    failed = sum(1 for r in rows if r["status"] == "FAIL")
    unv = sum(1 for r in rows if r["status"] == "UNVERIFIABLE")
    frag["verdict"] = "PASS" if failed == 0 and unv == 0 else "FAIL"
    frag["summary"] = (f"AC1-b round 20 (L04, L05, L06 and twins; pin fd9a9b7): {len(rows)} rows, {passed} PASS, "
                       f"{failed} FAIL, {unv} UNVERIFIABLE. Verdict {frag['verdict']} (card AC1-c069 locator).")
    json.dump(frag, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    sys.stdout.write(frag["summary"] + "\n")
